from __future__ import annotations

import asyncio
import base64
import json
import secrets
from typing import Any
from urllib.parse import urljoin

import httpx

from jira_mcp.adapters import PreparedRequest
from jira_mcp.config import Limits
from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.models import BackendResponse, Credential, TargetConfig

RETRYABLE_STATUS = {429, 502, 503, 504}


class JiraHttpClient:
    def __init__(self, limits: Limits, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self.limits = limits
        self.transport = transport

    async def request(self, target: TargetConfig, credential: Credential, prepared: PreparedRequest, *, mutation: bool) -> BackendResponse:
        base = str(target.base_url).rstrip("/") + "/"
        url = urljoin(base, prepared.path.lstrip("/"))
        timeout = httpx.Timeout(
            self.limits.timeout_seconds,
            connect=self.limits.connect_timeout_seconds,
            read=self.limits.timeout_seconds,
            write=self.limits.timeout_seconds,
            pool=self.limits.connect_timeout_seconds,
        )
        auth = httpx.BasicAuth(credential.username, credential.password)
        attempts = 1 if mutation else self.limits.max_read_retries + 1
        last_error: JiraMcpError | None = None
        async with httpx.AsyncClient(
            auth=auth,
            timeout=timeout,
            verify=target.tls_verify,
            follow_redirects=False,
            transport=self.transport,
            headers={"Accept": "application/json", "User-Agent": "jira-mcp-on-prem/1.0.0"},
        ) as client:
            for attempt in range(attempts):
                try:
                    response = await self._send(client, prepared, url)
                    if response.status_code in RETRYABLE_STATUS and attempt + 1 < attempts:
                        await asyncio.sleep(min(0.05 * (2**attempt) + secrets.randbelow(10) / 1000, 0.25))
                        continue
                    return self._normalize_response(response, url, attempt_count=attempt + 1)
                except asyncio.CancelledError:
                    raise
                except httpx.TimeoutException as exc:
                    if mutation:
                        raise JiraMcpError(
                            ErrorCode.UNKNOWN_MUTATION_OUTCOME,
                            "The Jira mutation timed out after dispatch; its outcome is unknown and it was not retried.",
                            stage="backend",
                            details={"request_sent": True},
                        ) from exc
                    last_error = JiraMcpError(ErrorCode.TIMEOUT, "The Jira request timed out.", retryable=True, stage="backend")
                except httpx.TransportError as exc:
                    if mutation:
                        raise JiraMcpError(
                            ErrorCode.UNKNOWN_MUTATION_OUTCOME,
                            "The Jira mutation lost transport after dispatch; its outcome is unknown and it was not retried.",
                            stage="backend",
                            details={"request_sent": True},
                        ) from exc
                    last_error = JiraMcpError(ErrorCode.BACKEND_UNAVAILABLE, "The Jira backend is unavailable.", retryable=True, stage="backend")
                if attempt + 1 < attempts:
                    await asyncio.sleep(min(0.05 * (2**attempt) + secrets.randbelow(10) / 1000, 0.25))
        assert last_error is not None
        raise last_error

    async def _send(self, client: httpx.AsyncClient, prepared: PreparedRequest, url: str) -> httpx.Response:
        kwargs: dict[str, Any] = {"params": prepared.query, "headers": prepared.headers}
        if prepared.attachments is not None:
            files: list[tuple[str, tuple[str, bytes, str]]] = []
            total = 0
            for attachment in prepared.attachments:
                try:
                    data = base64.b64decode(attachment["content_base64"], validate=True)
                except (ValueError, TypeError) as exc:
                    raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "Attachment content is not valid base64.", stage="validation") from exc
                total += len(data)
                if total > self.limits.max_attachment_bytes:
                    raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "Attachment aggregate exceeds the configured byte limit.", stage="validation")
                files.append(("file", (attachment["filename"], data, attachment["media_type"])))
            kwargs["files"] = files
        elif prepared.body is not None:
            encoded = json.dumps(prepared.body, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
            if len(encoded) > self.limits.max_request_bytes:
                raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "The Jira JSON request body exceeds the configured byte limit.", stage="validation")
            kwargs["content"] = encoded
            kwargs["headers"] = {**prepared.headers, "Content-Type": "application/json"}
        request = client.build_request(prepared.method, url, **kwargs)
        response = await client.send(request, stream=True)
        content = bytearray()
        try:
            async for chunk in response.aiter_bytes():
                content.extend(chunk)
                if len(content) > self.limits.max_response_bytes:
                    raise JiraMcpError(
                        ErrorCode.RESPONSE_TOO_LARGE,
                        "The Jira response exceeded the hard receive limit.",
                        stage="backend",
                    )
        finally:
            await response.aclose()
        return httpx.Response(
            status_code=response.status_code,
            headers=response.headers,
            content=bytes(content),
            request=request,
        )

    def _normalize_response(self, response: httpx.Response, url: str, *, attempt_count: int) -> BackendResponse:
        raw = response.content
        if len(raw) > self.limits.max_response_bytes:
            raise JiraMcpError(ErrorCode.RESPONSE_TOO_LARGE, "The Jira response exceeded the hard receive limit.", stage="backend")
        if response.status_code >= 400:
            mapping = {
                400: (ErrorCode.VALIDATION_ERROR, False, "Jira rejected the validated request."),
                401: (ErrorCode.BACKEND_AUTHENTICATION_FAILED, False, "Jira authentication failed."),
                403: (ErrorCode.BACKEND_AUTHORIZATION_DENIED, False, "Jira denied the operation."),
                404: (ErrorCode.BACKEND_NOT_FOUND, False, "The Jira resource was not found."),
                409: (ErrorCode.BACKEND_CONFLICT, False, "Jira reported a conflict or stale precondition."),
                429: (ErrorCode.BACKEND_RATE_LIMITED, True, "Jira rate-limited the request."),
            }
            code, retryable, message = mapping.get(
                response.status_code, (ErrorCode.BACKEND_UNAVAILABLE, response.status_code >= 500, "Jira returned an unsuccessful response.")
            )
            raise JiraMcpError(code, message, retryable=retryable, stage="backend", details={"http_status": response.status_code})
        content_type = response.headers.get("content-type", "application/octet-stream").split(";", 1)[0].lower()
        if not raw:
            payload: Any = None
        elif content_type == "application/json" or content_type.endswith("+json"):
            try:
                payload = response.json()
            except ValueError as exc:
                raise JiraMcpError(ErrorCode.BACKEND_UNAVAILABLE, "Jira returned invalid JSON.", stage="response_validation") from exc
        else:
            payload = raw.decode("utf-8", errors="replace")
        return BackendResponse(
            status_code=response.status_code,
            content_type=content_type,
            payload=payload,
            raw_size=len(raw),
            request_url=url,
            response_headers={key.lower(): value for key, value in response.headers.items() if key.lower() in {"etag", "last-modified", "x-arequestid"}},
            attempt_count=attempt_count,
        )
