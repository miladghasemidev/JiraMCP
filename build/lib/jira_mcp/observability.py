from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Protocol

from jira_mcp.security import redact


class AuditSink(Protocol):
    production_ready: bool

    async def emit(self, event: dict[str, Any]) -> None: ...


class UnavailableAuditSink:
    production_ready = False

    async def emit(self, event: dict[str, Any]) -> None:
        del event
        raise RuntimeError("external audit sink is not configured")


@dataclass(slots=True)
class InMemoryAuditSink:
    production_ready = False
    events: list[dict[str, Any]] = field(default_factory=list)
    _previous_hash: str | None = None

    async def emit(self, event: dict[str, Any]) -> None:
        safe = redact(event)
        safe["previous_event_hash"] = self._previous_hash
        encoded = json.dumps(safe, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        self._previous_hash = hashlib.sha256(encoded).hexdigest()
        safe["event_hash"] = self._previous_hash
        self.events.append(safe)


def audit_event(
    *,
    event_type: str,
    trace_id: str,
    actor_id: str,
    delegated_user_id: str | None,
    tenant_id: str | None,
    environment: str,
    capability_id: str,
    risk_class: str,
    target_id: str,
    outcome: str,
    policy_version: str | None,
    approval_id: str | None,
    reason_code: str | None,
    duration_ms: int | None = None,
    record_count: int | None = None,
    request_bytes: int | None = None,
    response_bytes: int | None = None,
    result_ref: str | None = None,
    action_digest: str | None = None,
) -> dict[str, Any]:
    measurements = {
        key: value
        for key, value in {
            "duration_ms": duration_ms,
            "record_count": record_count,
            "request_bytes": request_bytes,
            "response_bytes": response_bytes,
        }.items()
        if value is not None
    }
    return {
        "event_id": hashlib.sha256(f"{trace_id}:{event_type}:{datetime.now(UTC).isoformat()}".encode()).hexdigest()[:32],
        "event_type": event_type,
        "occurred_at": datetime.now(UTC).isoformat(),
        "trace_id": trace_id,
        "span_id": None,
        "tenant_id": tenant_id,
        "environment": environment,
        "actor": {"actor_type": "user", "actor_id": actor_id, "delegated_user_id": delegated_user_id},
        "action": {"capability_id": capability_id, "contract_version": "1.0.0", "risk_class": risk_class, "action_digest": action_digest},
        "target": {"target_id": target_id},
        "decision": {"outcome": outcome, "policy_version": policy_version, "approval_id": approval_id, "reason_code": reason_code},
        "measurements": measurements,
        "result_ref": result_ref,
        "redactions_applied": [],
    }


class MetricSink(Protocol):
    production_ready: bool

    async def emit(self, name: str, value: float, attributes: dict[str, str]) -> None: ...


class NullMetricSink:
    production_ready = False

    async def emit(self, name: str, value: float, attributes: dict[str, str]) -> None:
        del name, value, attributes


@dataclass(slots=True)
class InMemoryMetricSink:
    production_ready = False
    measurements: list[dict[str, Any]] = field(default_factory=list)

    async def emit(self, name: str, value: float, attributes: dict[str, str]) -> None:
        self.measurements.append({"name": name, "value": value, "attributes": redact(attributes)})
