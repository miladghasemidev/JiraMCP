from __future__ import annotations

import json
from pathlib import Path

import pytest
from conftest import json_response, make_executor, valid_args
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from jira_mcp.config import ServerConfig, TargetResolver
from jira_mcp.factory import build_fail_closed_executor
from jira_mcp.models import TargetConfig
from jira_mcp.observability import InMemoryMetricSink
from jira_mcp.server import health, readiness

ROOT = Path(__file__).resolve().parents[1]


def test_non_development_targets_require_https() -> None:
    with pytest.raises(ValidationError):
        TargetConfig(
            target_id="jira-production",
            environment="production",
            base_url="http://jira.example.test/",
            jira_version="9.12.0",
            secret_ref="secret://jira-production",
        )


def test_readiness_fails_without_targets_and_on_duplicate_registration(target) -> None:
    assert TargetResolver(ServerConfig()).readiness() == (False, ["no registered Jira targets"])
    ready, problems = TargetResolver(ServerConfig(targets=(target, target))).readiness()
    assert ready is False
    assert "duplicate environment/target registrations" in problems


def test_fail_closed_factory_has_no_implicit_production_integrations() -> None:
    executor = build_fail_closed_executor(ServerConfig())
    assert readiness(executor)["status"] == "not_ready"
    assert health() == {"status": "ok", "service": "jira-mcp-on-prem", "version": "1.0.0"}


@pytest.mark.asyncio
async def test_test_fakes_cannot_be_used_for_a_production_target(inventory) -> None:
    target = TargetConfig(
        target_id="jira-production",
        environment="production",
        base_url="https://jira.example.test/",
        jira_version="9.12.0",
        secret_ref="secret://jira-test",
        tenant_ids=("tenant-a",),
    )
    capability = next(item for item in inventory.capabilities if not item.mutation)
    args = valid_args(inventory, capability)
    args.update(environment="production", target_id="jira-production")
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({}))
    ready = readiness(executor)
    assert ready["status"] == "not_ready"
    assert len(ready["problems"]) == 6
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "failed"
    assert result["error"]["code"] == "EXTERNAL_CONTROL_UNAVAILABLE"


@pytest.mark.asyncio
async def test_audit_event_validates_and_contains_no_secrets(inventory, target) -> None:
    capability = next(item for item in inventory.capabilities if not item.mutation)
    args = valid_args(inventory, capability)
    executor, caller, audit, _store = make_executor(
        inventory,
        capability,
        target,
        args,
        lambda _r: json_response({"token": "backend-secret", "value": "safe"}),
    )
    metrics = InMemoryMetricSink()
    executor.metrics = metrics
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "succeeded"
    assert len(audit.events) == 1
    event = {key: value for key, value in audit.events[0].items() if key not in {"event_hash", "previous_event_hash"}}
    schema = json.loads((ROOT / "agent-platform-standards/schemas/audit-event.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(event)
    assert event["action"]["action_digest"]
    encoded = json.dumps(audit.events, sort_keys=True)
    assert "backend-secret" not in encoded
    assert "not-a-real-secret" not in encoded
    assert {item["name"] for item in metrics.measurements} == {"jira_mcp.call.duration_ms", "jira_mcp.call.attempt_count"}
    assert all(item["attributes"]["trace_id"] == args["trace_id"] for item in metrics.measurements)
