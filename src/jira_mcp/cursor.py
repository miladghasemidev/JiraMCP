from __future__ import annotations

import base64
import hashlib
import hmac
import json
from typing import Any

from jira_mcp.errors import ErrorCode, JiraMcpError


class CursorCodec:
    def __init__(self, key: bytes) -> None:
        if len(key) < 32:
            raise ValueError("cursor signing key must contain at least 32 bytes")
        self._key = key

    def encode(self, payload: dict[str, Any]) -> str:
        body = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        signature = hmac.new(self._key, body, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(signature + body).decode().rstrip("=")

    def decode(self, token: str) -> dict[str, Any]:
        try:
            padded = token + "=" * (-len(token) % 4)
            decoded = base64.urlsafe_b64decode(padded)
            signature, body = decoded[:32], decoded[32:]
            if not hmac.compare_digest(signature, hmac.new(self._key, body, hashlib.sha256).digest()):
                raise ValueError("signature mismatch")
            value = json.loads(body)
            if not isinstance(value, dict):
                raise ValueError("cursor body is not an object")
            return value
        except (ValueError, json.JSONDecodeError) as exc:
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "The pagination cursor is invalid or has been altered.", stage="validation") from exc
