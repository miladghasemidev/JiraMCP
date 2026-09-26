from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.inventory import Capability
from jira_mcp.models import CallerContext, Credential, TargetConfig

PROHIBITED_KEYS = {
    "authorization",
    "cookie",
    "credentials",
    "connection_string",
    "password",
    "private_key",
    "secret",
    "session",
    "token",
}


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: "[REDACTED]" if key.lower() in PROHIBITED_KEYS else redact(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact(item) for item in value]
    return value


def validate_json_bounds(value: Any, *, max_depth: int = 12, max_items: int = 1000, max_string: int = 262_144) -> None:
    item_count = 0

    def walk(item: Any, depth: int) -> None:
        nonlocal item_count
        if depth > max_depth:
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "JSON input exceeds the maximum nesting depth.", stage="validation")
        item_count += 1
        if item_count > max_items:
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "JSON input exceeds the maximum item count.", stage="validation")
        if isinstance(item, dict):
            for key, nested in item.items():
                if not isinstance(key, str) or len(key) > 256 or any(ord(char) < 32 for char in key):
                    raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "JSON input contains an invalid object key.", stage="validation")
                if key.lower() in PROHIBITED_KEYS:
                    raise JiraMcpError(ErrorCode.VALIDATION_ERROR, f"Credential-like field '{key}' is prohibited in tool arguments.", stage="validation")
                walk(nested, depth + 1)
        elif isinstance(item, list):
            for nested in item:
                walk(nested, depth + 1)
        elif isinstance(item, str) and len(item) > max_string:
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "JSON input contains an oversized string.", stage="validation")
        elif not isinstance(item, (str, int, float, bool, type(None))):
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "JSON input contains an unsupported scalar type.", stage="validation")

    walk(value, 0)


def normalized_action(capability: Capability, args: dict[str, Any], target: TargetConfig, caller: CallerContext) -> dict[str, Any]:
    volatile = {"approval_ref", "break_glass_ref", "trace_id", "request_id"}
    parameters = {key: args[key] for key in sorted(args) if key not in volatile}
    return {
        "capability_id": capability.capability_id,
        "contract_version": "1.0.0",
        "requester_id": caller.actor_id,
        "tenant_id": caller.tenant_id,
        "environment": target.environment,
        "target_id": target.target_id,
        "jira_version": target.jira_version,
        "normalized_parameters": parameters,
        "expected_side_effects": [capability.description] if capability.mutation else [],
    }


def action_digest(action: dict[str, Any]) -> str:
    payload = json.dumps(action, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False).encode()
    return hashlib.sha256(payload).hexdigest()


class SecretBroker(Protocol):
    production_ready: bool

    async def get_jira_credential(self, target: TargetConfig, caller: CallerContext) -> Credential: ...


class UnavailableSecretBroker:
    production_ready = False

    async def get_jira_credential(self, target: TargetConfig, caller: CallerContext) -> Credential:
        del target, caller
        raise JiraMcpError(ErrorCode.SECRET_BROKER_UNAVAILABLE, "The external secret broker is not configured.", stage="credentials")


class InMemorySecretBroker:
    """Development/test fake. Never load this mapping from production configuration."""

    production_ready = False

    def __init__(self, credentials: dict[str, Credential]) -> None:
        self._credentials = credentials

    async def get_jira_credential(self, target: TargetConfig, caller: CallerContext) -> Credential:
        del caller
        try:
            return self._credentials[target.secret_ref]
        except KeyError as exc:
            raise JiraMcpError(ErrorCode.SECRET_BROKER_UNAVAILABLE, "No test credential is bound to the target secret reference.", stage="credentials") from exc


@dataclass(frozen=True, slots=True)
class PolicyDecision:
    allowed: bool
    policy_version: str
    reason_code: str


class PolicyEngine(Protocol):
    production_ready: bool

    async def authorize(self, capability: Capability, target: TargetConfig, caller: CallerContext, args: dict[str, Any]) -> PolicyDecision: ...


class DenyAllPolicy:
    production_ready = False

    async def authorize(self, capability: Capability, target: TargetConfig, caller: CallerContext, args: dict[str, Any]) -> PolicyDecision:
        del capability, target, caller, args
        return PolicyDecision(False, "unconfigured", "policy_unavailable")


class StaticPolicy:
    """Deterministic development/test policy with deny-overrides behavior."""

    production_ready = False

    def __init__(self, *, version: str = "test-1.0.0", allow_w1: bool = False, allow_w3: bool = False) -> None:
        self.version = version
        self.allow_w1 = allow_w1
        self.allow_w3 = allow_w3

    async def authorize(self, capability: Capability, target: TargetConfig, caller: CallerContext, args: dict[str, Any]) -> PolicyDecision:
        del args
        if not caller.authenticated or not caller.gateway_verified:
            return PolicyDecision(False, self.version, "unverified_gateway_context")
        permission = f"jira.{capability.category}.{'write' if capability.mutation else 'read'}"
        if permission not in caller.permissions:
            return PolicyDecision(False, self.version, "missing_permission")
        if target.tenant_ids and caller.tenant_id not in target.tenant_ids:
            return PolicyDecision(False, self.version, "tenant_scope_denied")
        if capability.risk_class == "W1" and not self.allow_w1:
            return PolicyDecision(False, self.version, "w1_not_preapproved")
        if capability.risk_class == "W3" and not self.allow_w3:
            return PolicyDecision(False, self.version, "w3_default_deny")
        return PolicyDecision(True, self.version, "explicit_allow")


class ApprovalVerifier(Protocol):
    production_ready: bool

    async def consume(self, approval_ref: str, expected_digest: str, risk_class: str, break_glass_ref: str | None) -> str: ...


class UnavailableApprovalVerifier:
    production_ready = False

    async def consume(self, approval_ref: str, expected_digest: str, risk_class: str, break_glass_ref: str | None) -> str:
        del approval_ref, expected_digest, risk_class, break_glass_ref
        raise JiraMcpError(ErrorCode.APPROVAL_REQUIRED, "A formal external approval verifier is required for this mutation.", stage="approval")


@dataclass(slots=True)
class ApprovalRecord:
    approval_ref: str
    action_digest: str
    expires_at: datetime
    max_uses: int = 1
    uses: int = 0
    break_glass_ref: str | None = None


class InMemoryApprovalVerifier:
    """Atomic-enough single-process fake for deterministic development/test cases."""

    production_ready = False

    def __init__(self, records: list[ApprovalRecord]) -> None:
        self._records = {record.approval_ref: record for record in records}

    async def consume(self, approval_ref: str, expected_digest: str, risk_class: str, break_glass_ref: str | None) -> str:
        record = self._records.get(approval_ref)
        if record is None:
            raise JiraMcpError(ErrorCode.APPROVAL_INVALID, "The formal approval reference is unknown.", stage="approval")
        if record.expires_at <= datetime.now(UTC):
            raise JiraMcpError(ErrorCode.APPROVAL_EXPIRED, "The formal approval has expired.", stage="approval")
        if not hmac.compare_digest(record.action_digest, expected_digest):
            raise JiraMcpError(ErrorCode.APPROVAL_INVALID, "The approval does not match the normalized action.", stage="approval")
        if record.uses >= record.max_uses:
            raise JiraMcpError(ErrorCode.APPROVAL_REPLAYED, "The approval has already been consumed.", stage="approval")
        if risk_class == "W3" and (not break_glass_ref or record.break_glass_ref != break_glass_ref):
            raise JiraMcpError(ErrorCode.APPROVAL_INVALID, "W3 requires matching exceptional break-glass evidence.", stage="approval")
        record.uses += 1
        return approval_ref


class IdempotencyStore(Protocol):
    async def lookup(self, key: str, digest: str) -> dict[str, Any] | None: ...
    async def reserve(self, key: str, digest: str) -> dict[str, Any] | None: ...
    async def complete(self, key: str, digest: str, result: dict[str, Any]) -> None: ...


class InMemoryIdempotencyStore:
    def __init__(self) -> None:
        self._records: dict[str, tuple[str, dict[str, Any] | None]] = {}

    async def lookup(self, key: str, digest: str) -> dict[str, Any] | None:
        existing = self._records.get(key)
        if existing is None:
            return None
        prior_digest, result = existing
        if not hmac.compare_digest(prior_digest, digest):
            raise JiraMcpError(
                ErrorCode.IDEMPOTENCY_CONFLICT,
                "The idempotency key is already bound to a different action.",
                stage="idempotency",
            )
        if result is None:
            raise JiraMcpError(
                ErrorCode.UNKNOWN_MUTATION_OUTCOME,
                "The idempotency key has an in-flight or unknown prior outcome.",
                stage="idempotency",
            )
        return result

    async def reserve(self, key: str, digest: str) -> dict[str, Any] | None:
        existing = self._records.get(key)
        if existing is None:
            self._records[key] = (digest, None)
            return None
        prior_digest, result = existing
        if not hmac.compare_digest(prior_digest, digest):
            raise JiraMcpError(ErrorCode.IDEMPOTENCY_CONFLICT, "The idempotency key is already bound to a different action.", stage="idempotency")
        if result is None:
            raise JiraMcpError(ErrorCode.UNKNOWN_MUTATION_OUTCOME, "The idempotency key has an in-flight or unknown prior outcome.", stage="idempotency")
        return result

    async def complete(self, key: str, digest: str, result: dict[str, Any]) -> None:
        self._records[key] = (digest, result)
