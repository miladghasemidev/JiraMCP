from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
import pytest

from jira_mcp.client import JiraHttpClient
from jira_mcp.config import Limits, ServerConfig, TargetResolver
from jira_mcp.cursor import CursorCodec
from jira_mcp.executor import JiraToolExecutor
from jira_mcp.inventory import Capability, Inventory
from jira_mcp.models import CallerContext, Credential, TargetConfig
from jira_mcp.observability import InMemoryAuditSink
from jira_mcp.result_store import InMemoryResultStore
from jira_mcp.security import (
    ApprovalRecord,
    InMemoryApprovalVerifier,
    InMemoryIdempotencyStore,
    InMemorySecretBroker,
    StaticPolicy,
    action_digest,
    normalized_action,
)

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def inventory() -> Inventory:
    return Inventory()


@pytest.fixture
def target() -> TargetConfig:
    return TargetConfig(
        target_id="jira-test",
        environment="test",
        base_url="https://jira.example.test/jira/",
        jira_version="9.12.0",
        secret_ref="secret://jira-test",
        tenant_ids=("tenant-a",),
    )


def caller_for(capability: Capability) -> CallerContext:
    return CallerContext(
        actor_id="user-a",
        delegated_user_id="user-a",
        tenant_id="tenant-a",
        permissions=frozenset({f"jira.{capability.category}.{'write' if capability.mutation else 'read'}"}),
        authenticated=True,
        gateway_verified=True,
        policy_version="test-1.0.0",
    )


def _value_for(name: str, schema: dict[str, Any]) -> Any:
    values = {
        "environment": "test",
        "target_id": "jira-test",
        "trace_id": "trace-12345678",
        "request_id": "request-1",
        "tenant_id": "tenant-a",
        "idempotency_key": "idem-12345678",
        "approval_ref": "approval:12345678",
        "break_glass_ref": "break-glass:12345678",
        "issue_id_or_key": "TEST-1",
        "project_id_or_key": "TEST",
        "project_key_or_id": "TEST",
        "project_type_key": "software",
        "property_key": "example.key",
        "global_id": "global-1",
        "state": "active",
    }
    if name in values:
        return values[name]
    if "const" in schema:
        return schema["const"]
    if "enum" in schema:
        return schema["enum"][0]
    kind = schema.get("type")
    if isinstance(kind, list):
        kind = next(item for item in kind if item != "null")
    if kind == "integer":
        return max(1, schema.get("minimum", 0))
    if kind == "boolean":
        return True
    if kind == "array":
        if name == "attachments":
            return [{"filename": "evidence.txt", "content_base64": "ZXZpZGVuY2U=", "media_type": "text/plain"}]
        return ["1"]
    if kind == "object":
        properties = schema.get("properties", {})
        return {key: _value_for(key, properties.get(key, {})) for key in schema.get("required", [])}
    return "1"


def valid_args(inventory: Inventory, capability: Capability, *, include_optional_query: bool = False) -> dict[str, Any]:
    schema = inventory.input_schema(capability.capability_id)
    properties = schema["properties"]
    args = {name: _value_for(name, properties[name]) for name in schema["required"]}
    if include_optional_query:
        reserved = {
            "request_id",
            "tenant_id",
            "precondition",
        }
        for name, subschema in properties.items():
            if name not in args and name not in reserved:
                args[name] = _value_for(name, subschema)
    return args


def make_executor(
    inventory: Inventory,
    capability: Capability,
    target: TargetConfig,
    args: dict[str, Any],
    handler: Callable[[httpx.Request], httpx.Response],
    *,
    caller: CallerContext | None = None,
    limits: Limits | None = None,
    allow_w1: bool = True,
    allow_w3: bool = True,
) -> tuple[JiraToolExecutor, CallerContext, InMemoryAuditSink, InMemoryResultStore]:
    selected_caller = caller or caller_for(capability)
    selected_limits = limits or Limits()
    approvals: list[ApprovalRecord] = []
    if capability.risk_class in {"W2", "W3"}:
        digest = action_digest(normalized_action(capability, args, target, selected_caller))
        approvals.append(
            ApprovalRecord(
                approval_ref=str(args["approval_ref"]),
                action_digest=digest,
                expires_at=datetime.now(UTC) + timedelta(minutes=5),
                break_glass_ref=args.get("break_glass_ref"),
            )
        )
    config = ServerConfig(targets=(target,), limits=selected_limits)
    audit = InMemoryAuditSink()
    result_store = InMemoryResultStore()
    executor = JiraToolExecutor(
        inventory=inventory,
        resolver=TargetResolver(config),
        policy=StaticPolicy(allow_w1=allow_w1, allow_w3=allow_w3),
        approvals=InMemoryApprovalVerifier(approvals),
        secret_broker=InMemorySecretBroker({"secret://jira-test": Credential(username="svc", password="not-a-real-secret")}),
        result_store=result_store,
        idempotency=InMemoryIdempotencyStore(),
        audit=audit,
        cursor_codec=CursorCodec(b"0123456789abcdef0123456789abcdef"),
        client=JiraHttpClient(selected_limits, transport=httpx.MockTransport(handler)),
        limits=selected_limits,
    )
    return executor, selected_caller, audit, result_store


def json_response(payload: Any, status_code: int = 200) -> httpx.Response:
    return httpx.Response(status_code, json=payload, headers={"Content-Type": "application/json"})
