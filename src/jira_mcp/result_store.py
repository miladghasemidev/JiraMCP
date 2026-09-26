from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol

from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.models import CallerContext, ResultReference, TargetConfig


class ResultStore(Protocol):
    production_ready: bool

    async def put(
        self, *, payload: Any, capability_id: str, trace_id: str, caller: CallerContext, target: TargetConfig, completeness: dict[str, Any]
    ) -> ResultReference: ...
    async def project(self, reference_id: str, *, caller: CallerContext, max_records: int, max_bytes: int) -> Any: ...


class UnavailableResultStore:
    production_ready = False

    async def put(self, **kwargs: Any) -> ResultReference:
        del kwargs
        raise JiraMcpError(ErrorCode.RESULT_STORE_UNAVAILABLE, "A governed Result Store is required for this output.", stage="result_store")

    async def project(self, reference_id: str, *, caller: CallerContext, max_records: int, max_bytes: int) -> Any:
        del reference_id, caller, max_records, max_bytes
        raise JiraMcpError(ErrorCode.RESULT_STORE_UNAVAILABLE, "The Result Store is unavailable.", stage="result_store")


@dataclass(slots=True)
class StoredResult:
    payload: Any
    tenant_id: str | None
    actor_id: str
    target_id: str
    environment: str
    trace_id: str
    capability_id: str
    created_at: datetime
    expires_at: datetime
    content_hash: str
    completeness: dict[str, Any]


class InMemoryResultStore:
    """Development/test fake with scoped reauthorization and short retention."""

    production_ready = False

    def __init__(self, ttl_minutes: int = 60) -> None:
        self.ttl = timedelta(minutes=ttl_minutes)
        self._items: dict[str, StoredResult] = {}

    async def put(
        self, *, payload: Any, capability_id: str, trace_id: str, caller: CallerContext, target: TargetConfig, completeness: dict[str, Any]
    ) -> ResultReference:
        now = datetime.now(UTC)
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        reference_id = f"result:{secrets.token_urlsafe(24)}"
        expires_at = now + self.ttl
        self._items[reference_id] = StoredResult(
            payload=payload,
            tenant_id=caller.tenant_id,
            actor_id=caller.actor_id,
            target_id=target.target_id,
            environment=target.environment,
            trace_id=trace_id,
            capability_id=capability_id,
            created_at=now,
            expires_at=expires_at,
            content_hash=hashlib.sha256(encoded).hexdigest(),
            completeness=completeness,
        )
        return ResultReference(id=reference_id, expires_at=expires_at)

    async def project(self, reference_id: str, *, caller: CallerContext, max_records: int, max_bytes: int) -> Any:
        item = self._items.get(reference_id)
        if item is None:
            raise JiraMcpError(ErrorCode.TARGET_NOT_FOUND, "The result reference does not exist.", stage="result_store")
        if item.expires_at <= datetime.now(UTC):
            del self._items[reference_id]
            raise JiraMcpError(ErrorCode.TARGET_NOT_FOUND, "The result reference has expired.", stage="result_store")
        if item.tenant_id != caller.tenant_id or item.actor_id != caller.actor_id:
            raise JiraMcpError(ErrorCode.AUTHORIZATION_DENIED, "The caller is not authorized for this result reference.", stage="result_store")
        payload = item.payload[:max_records] if isinstance(item.payload, list) else item.payload
        encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
        if len(encoded) > max_bytes:
            return {"projection": "omitted", "reason": "projection_byte_limit", "content_hash": item.content_hash}
        return payload
