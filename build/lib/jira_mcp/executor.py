from __future__ import annotations

import asyncio
import contextlib
import json
import time
from datetime import UTC, datetime
from typing import Any, Literal

from jsonschema import Draft202012Validator

from jira_mcp.adapters import adapter_for
from jira_mcp.client import JiraHttpClient
from jira_mcp.config import Limits, TargetResolver
from jira_mcp.cursor import CursorCodec
from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.inventory import Capability, Inventory
from jira_mcp.models import CallerContext, Completeness, TargetConfig, ToolResult
from jira_mcp.observability import AuditSink, MetricSink, NullMetricSink, audit_event
from jira_mcp.result_store import ResultStore
from jira_mcp.security import (
    ApprovalVerifier,
    IdempotencyStore,
    PolicyEngine,
    SecretBroker,
    action_digest,
    normalized_action,
    redact,
    validate_json_bounds,
)


class JiraToolExecutor:
    def __init__(
        self,
        *,
        inventory: Inventory,
        resolver: TargetResolver,
        policy: PolicyEngine,
        approvals: ApprovalVerifier,
        secret_broker: SecretBroker,
        result_store: ResultStore,
        idempotency: IdempotencyStore,
        audit: AuditSink,
        cursor_codec: CursorCodec,
        client: JiraHttpClient,
        limits: Limits,
        metrics: MetricSink | None = None,
    ) -> None:
        self.inventory = inventory
        self.resolver = resolver
        self.policy = policy
        self.approvals = approvals
        self.secret_broker = secret_broker
        self.result_store = result_store
        self.idempotency = idempotency
        self.audit = audit
        self.cursor_codec = cursor_codec
        self.client = client
        self.limits = limits
        self.metrics = metrics or NullMetricSink()
        self._concurrency = asyncio.Semaphore(limits.max_concurrency)
        self._target_concurrency: dict[tuple[str, str], asyncio.Semaphore] = {}

    async def invoke(self, capability_id: str, args: dict[str, Any], caller: CallerContext) -> dict[str, Any]:
        capability = self.inventory.get(capability_id)
        trace_id = str(args.get("trace_id", "missing-trace"))
        started = time.monotonic()
        target: TargetConfig | None = None
        policy_version: str | None = None
        approval_id: str | None = None
        action_digest_value: str | None = None
        try:
            self._validate(capability, args)
            if not caller.authenticated:
                raise JiraMcpError(ErrorCode.AUTHENTICATION_REQUIRED, "Authenticated gateway caller context is required.", stage="authentication")
            target = self.resolver.resolve(str(args["environment"]), str(args["target_id"]), caller.tenant_id)
            self._require_production_controls(target)
            adapter = adapter_for(target.jira_version)
            decision = await self.policy.authorize(capability, target, caller, args)
            policy_version = decision.policy_version
            if not decision.allowed:
                code = ErrorCode.POLICY_UNAVAILABLE if decision.reason_code == "policy_unavailable" else ErrorCode.AUTHORIZATION_DENIED
                raise JiraMcpError(code, "Policy denied the Jira capability call.", stage="authorization", details={"reason_code": decision.reason_code})
            action = normalized_action(capability, args, target, caller)
            digest = action_digest(action)
            action_digest_value = digest
            idempotency_key = str(args.get("idempotency_key", ""))
            if capability.mutation:
                prior = await self.idempotency.lookup(idempotency_key, digest)
                if prior is not None:
                    return prior
            if capability.risk_class in {"W2", "W3"}:
                approval_ref = args.get("approval_ref")
                if not approval_ref:
                    raise JiraMcpError(ErrorCode.APPROVAL_REQUIRED, "Formal approval is required for this mutation.", stage="approval")
                approval_id = await self.approvals.consume(str(approval_ref), digest, capability.risk_class, args.get("break_glass_ref"))
            if capability.mutation:
                prior = await self.idempotency.reserve(idempotency_key, digest)
                if prior is not None:
                    return prior
            prepared = adapter.prepare(capability, args)
            credential = await self.secret_broker.get_jira_credential(target, caller)
            request_bytes = len(json.dumps(redact(args), ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode())
            target_semaphore = self._target_concurrency.setdefault(
                (target.environment, target.target_id), asyncio.Semaphore(self.limits.max_concurrency_per_target)
            )
            async with self._concurrency, target_semaphore:
                async with asyncio.timeout(self.limits.timeout_seconds):
                    response = await self.client.request(target, credential, prepared, mutation=capability.mutation)
            result = await self._success(capability, args, caller, target, response.payload, response.raw_size)
            wire = result.wire()
            try:
                await self.audit.emit(
                    audit_event(
                        event_type="mutation_completed" if capability.mutation else "sensitive_read",
                        trace_id=trace_id,
                        actor_id=caller.actor_id,
                        delegated_user_id=caller.delegated_user_id,
                        tenant_id=caller.tenant_id,
                        environment=target.environment,
                        capability_id=capability.capability_id,
                        risk_class=capability.risk_class,
                        target_id=target.target_id,
                        outcome="completed" if result.status == "succeeded" else "partial",
                        policy_version=policy_version,
                        approval_id=approval_id,
                        reason_code=None,
                        duration_ms=int((time.monotonic() - started) * 1000),
                        record_count=result.completeness.record_count if result.completeness else 0,
                        request_bytes=request_bytes,
                        response_bytes=response.raw_size,
                        result_ref=result.result_ref.id if result.result_ref else None,
                        action_digest=action_digest_value,
                    )
                )
            except Exception:
                if not capability.mutation:
                    raise JiraMcpError(
                        ErrorCode.EXTERNAL_CONTROL_UNAVAILABLE,
                        "The required audit event could not be recorded.",
                        stage="audit",
                    ) from None
                wire["status"] = "partial"
                wire.setdefault("warnings", []).append(
                    {
                        "code": "AUDIT_DELIVERY_FAILED",
                        "message": "Jira completed the mutation, but required audit delivery failed; do not repeat the mutation blindly.",
                    }
                )
            if capability.mutation:
                await self.idempotency.complete(idempotency_key, digest, wire)
            await self._emit_metrics(capability, target, trace_id, wire["status"], response.attempt_count, started)
            return wire
        except asyncio.CancelledError:
            error = JiraMcpError(ErrorCode.CANCELLED, "The Jira capability call was cancelled.", stage="execution")
            return await self._failure(capability, trace_id, caller, target, error, policy_version, approval_id, action_digest_value, started)
        except TimeoutError:
            error = JiraMcpError(
                ErrorCode.UNKNOWN_MUTATION_OUTCOME if capability.mutation else ErrorCode.TIMEOUT,
                (
                    "The Jira mutation exceeded its end-to-end deadline after possible dispatch; its outcome is unknown."
                    if capability.mutation
                    else "The Jira read exceeded its end-to-end deadline."
                ),
                retryable=not capability.mutation,
                stage="execution_deadline",
            )
            return await self._failure(capability, trace_id, caller, target, error, policy_version, approval_id, action_digest_value, started)
        except JiraMcpError as error:
            return await self._failure(capability, trace_id, caller, target, error, policy_version, approval_id, action_digest_value, started)
        except Exception:
            internal_error = JiraMcpError(ErrorCode.INTERNAL_ERROR, "The Jira capability call failed safely.", stage="internal")
            return await self._failure(capability, trace_id, caller, target, internal_error, policy_version, approval_id, action_digest_value, started)

    def _require_production_controls(self, target: TargetConfig) -> None:
        unavailable = self.production_control_problems(target)
        if unavailable:
            raise JiraMcpError(
                ErrorCode.EXTERNAL_CONTROL_UNAVAILABLE,
                "Required production integrations are unavailable.",
                stage="production_preflight",
                details={"unavailable_controls": unavailable},
            )

    def production_control_problems(self, target: TargetConfig) -> list[str]:
        if target.environment != "production":
            return []
        controls = {
            "policy": self.policy,
            "approval verifier": self.approvals,
            "secret broker": self.secret_broker,
            "Result Store": self.result_store,
            "audit sink": self.audit,
            "metrics sink": self.metrics,
        }
        unavailable = [name for name, control in controls.items() if not getattr(control, "production_ready", False)]
        return unavailable

    async def _emit_metrics(self, capability: Capability, target: TargetConfig, trace_id: str, status: str, attempt_count: int, started: float) -> None:
        attributes = {
            "capability_id": capability.capability_id,
            "trace_id": trace_id,
            "risk_class": capability.risk_class,
            "environment": target.environment,
            "target_id": target.target_id,
            "status": status,
        }
        try:
            await self.metrics.emit("jira_mcp.call.duration_ms", (time.monotonic() - started) * 1000, attributes)
            await self.metrics.emit("jira_mcp.call.attempt_count", float(attempt_count), attributes)
        except Exception:
            return

    def _validate(self, capability: Capability, args: dict[str, Any]) -> None:
        schema = self.inventory.input_schema(capability.capability_id)
        errors = sorted(Draft202012Validator(schema).iter_errors(args), key=lambda item: list(item.absolute_path))
        if errors:
            first = errors[0]
            path = ".".join(str(part) for part in first.absolute_path) or "$"
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, f"Invalid tool arguments at {path}: {first.message}", stage="validation")
        validate_json_bounds(args)
        encoded = json.dumps(args, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
        hard_limit = self.limits.max_attachment_bytes * 2 if capability.capability_id == "jira_issue_add_attachment" else self.limits.max_request_bytes
        if len(encoded) > hard_limit:
            raise JiraMcpError(ErrorCode.VALIDATION_ERROR, "Tool arguments exceed the hard byte limit.", stage="validation")

    async def _success(
        self, capability: Capability, args: dict[str, Any], caller: CallerContext, target: TargetConfig, payload: Any, raw_size: int
    ) -> ToolResult:
        record_count, page = self._record_count_and_page(payload)
        next_cursor = None
        state: Literal["complete", "paginated", "filtered", "sampled", "truncated"] = "complete"
        total = page.get("total")
        if page.get("next_start") is not None:
            state = "paginated"
            next_cursor = self.cursor_codec.encode(
                {
                    "capability_id": capability.capability_id,
                    "contract_version": "1.0.0",
                    "target_id": target.target_id,
                    "environment": target.environment,
                    "jira_version": target.jira_version,
                    "next_start": page["next_start"],
                    "max_results": page.get("max_results", 50),
                }
            )
        completeness = Completeness(
            state=state,
            record_count=record_count,
            total_count=total,
            byte_count=raw_size,
            next_cursor=next_cursor,
            reason="Additional Jira page available" if next_cursor else None,
        )
        inline_encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
        result_ref = None
        data = payload
        warnings: list[dict[str, str]] = []
        storage_failed_after_mutation = False
        if len(inline_encoded) > self.limits.max_inline_bytes or record_count > self.limits.max_inline_records:
            try:
                result_ref = await self.result_store.put(
                    payload=payload,
                    capability_id=capability.capability_id,
                    trace_id=str(args["trace_id"]),
                    caller=caller,
                    target=target,
                    completeness=completeness.model_dump(mode="json"),
                )
                data = self._bounded_projection(payload)
                if state == "complete":
                    completeness.state = "truncated"
                completeness.reason = "Full payload stored; inline projection is bounded"
                warnings.append(
                    {
                        "code": "RESULT_STORED",
                        "message": "The full authorized result is in the Result Store; inline data is a bounded projection.",
                    }
                )
            except JiraMcpError:
                if not capability.mutation:
                    raise
                storage_failed_after_mutation = True
                data = None
                completeness.state = "truncated"
                completeness.reason = "Jira completed the mutation, but its oversized response could not be stored"
                warnings.append(
                    {
                        "code": "RESULT_STORE_DELIVERY_FAILED",
                        "message": "Jira completed the mutation, but the oversized response is unavailable; do not repeat the mutation blindly.",
                    }
                )
        partial_errors: list[Any] = payload.get("errors", []) if isinstance(payload, dict) and isinstance(payload.get("errors"), list) else []
        partial = bool((partial_errors and record_count > 0) or storage_failed_after_mutation)
        return ToolResult(
            status="partial" if partial else "succeeded",
            capability_id=capability.capability_id,
            trace_id=str(args["trace_id"]),
            data=redact(data),
            result_ref=result_ref,
            completeness=completeness,
            provenance=[
                {
                    "source": "jira-rest",
                    "target_id": target.target_id,
                    "environment": target.environment,
                    "jira_version": target.jira_version,
                    "matrix_id": capability.matrix_id,
                    "source_matrix": capability.source,
                    "collected_at": datetime.now(UTC).isoformat(),
                }
            ],
            warnings=warnings,
            errors=[
                {
                    "code": "PARTIAL_BACKEND_FAILURE",
                    "message": "One Jira sub-operation failed; see the authorized result payload for scoped details.",
                    "retryable": False,
                    "stage": "backend",
                    "remediation_hint": None,
                    "details_ref": result_ref.id if result_ref else None,
                }
                for _item in partial_errors[:20]
            ],
        )

    async def _failure(
        self,
        capability: Capability,
        trace_id: str,
        caller: CallerContext,
        target: TargetConfig | None,
        error: JiraMcpError,
        policy_version: str | None,
        approval_id: str | None,
        action_digest_value: str | None,
        started: float,
    ) -> dict[str, Any]:
        result = ToolResult(
            status="failed",
            capability_id=capability.capability_id,
            trace_id=trace_id,
            error=error.as_dict(),
        ).wire()
        with contextlib.suppress(Exception):
            await self.audit.emit(
                audit_event(
                    event_type="capability_invoked",
                    trace_id=trace_id,
                    actor_id=caller.actor_id,
                    delegated_user_id=caller.delegated_user_id,
                    tenant_id=caller.tenant_id,
                    environment=target.environment if target else "unknown",
                    capability_id=capability.capability_id,
                    risk_class=capability.risk_class,
                    target_id=target.target_id if target else "unresolved",
                    outcome="unknown" if error.code == ErrorCode.UNKNOWN_MUTATION_OUTCOME else "failed",
                    policy_version=policy_version,
                    approval_id=approval_id,
                    reason_code=error.code.value,
                    duration_ms=int((time.monotonic() - started) * 1000),
                    action_digest=action_digest_value,
                )
            )
        if target is not None:
            await self._emit_metrics(capability, target, trace_id, "failed", 1, started)
        return result

    @staticmethod
    def _record_count_and_page(payload: Any) -> tuple[int, dict[str, int | None]]:
        if isinstance(payload, list):
            return len(payload), {"total": len(payload), "next_start": None, "max_results": None}
        if not isinstance(payload, dict):
            return (0 if payload is None else 1), {"total": None, "next_start": None, "max_results": None}
        sequence = next(
            (
                value
                for key, value in payload.items()
                if key in {"issues", "values", "comments", "worklogs", "projects", "versions", "sprints", "boards"} and isinstance(value, list)
            ),
            None,
        )
        count = len(sequence) if sequence is not None else (0 if not payload else 1)
        start = payload.get("startAt")
        maximum = payload.get("maxResults")
        total = payload.get("total")
        is_last = payload.get("isLast")
        next_start: int | None = None
        if isinstance(start, int) and isinstance(maximum, int) and maximum > 0:
            candidate = start + count
            if is_last is False or (isinstance(total, int) and candidate < total):
                next_start = candidate
        return count, {
            "total": total if isinstance(total, int) else None,
            "next_start": next_start,
            "max_results": maximum if isinstance(maximum, int) else None,
        }

    def _bounded_projection(self, payload: Any) -> Any:
        if isinstance(payload, list):
            return payload[: self.limits.max_projection_records]
        if isinstance(payload, dict):
            projected: dict[str, Any] = {}
            for key, value in payload.items():
                projected[key] = value[: self.limits.max_projection_records] if isinstance(value, list) else value
            encoded = json.dumps(projected, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode()
            if len(encoded) <= min(self.limits.max_inline_bytes, 16_384):
                return projected
            return {"projection": "omitted", "reason": "projection_byte_limit"}
        return payload
