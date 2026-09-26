from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

from jira_mcp.inventory import Inventory

ROOT = Path(__file__).resolve().parents[1]


def test_exact_authoritative_inventory(inventory: Inventory) -> None:
    assert len(inventory.capabilities) == 114
    assert len(inventory.by_id) == 114
    assert Counter(item.category for item in inventory.capabilities) == {"agile": 34, "issue": 46, "project": 17, "version": 17}
    assert Counter(item.http_method for item in inventory.capabilities) == {"GET": 56, "POST": 27, "PUT": 17, "DELETE": 14}
    assert Counter(item.risk_class for item in inventory.capabilities) == {"R1": 19, "R2": 37, "W1": 11, "W2": 42, "W3": 5}
    source = ROOT / "project-inputs" / "APPROVED_JIRA_CAPABILITY_MATRIX.xlsx"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == inventory.source_sha256


def test_every_input_schema_is_valid_and_secure(inventory: Inventory) -> None:
    for capability in inventory.capabilities:
        schema = inventory.input_schema(capability.capability_id)
        Draft202012Validator.check_schema(schema)
        assert schema["additionalProperties"] is False
        assert {"environment", "target_id", "trace_id"} <= set(schema["required"])
        assert "base_url" not in schema["properties"]
        assert "password" not in schema["properties"]
        for placeholder in re.findall(r"\{([^}]+)\}", capability.baseline_rest_path):
            snake = re.sub(r"(?<!^)(?=[A-Z])", "_", placeholder).replace("-", "_").lower()
            assert snake in schema["required"]
        if capability.mutation:
            assert "idempotency_key" in schema["required"]
        if capability.risk_class in {"W2", "W3"}:
            assert "approval_ref" in schema["required"]
        if capability.risk_class == "W3":
            assert {"break_glass_ref", "confirm_irreversible"} <= set(schema["required"])


def test_generated_artifact_counts_match_inventory(inventory: Inventory) -> None:
    assert len(list((ROOT / "specs" / "tools").glob("*.md"))) == 114
    assert len(list((ROOT / "specs" / "schemas" / "inputs").glob("*.json"))) == 114
    assert sum(1 for line in (ROOT / "IMPLEMENTATION_STATUS.md").read_text(encoding="utf-8").splitlines() if line.startswith("| `jira_")) == 114
    spec_ids = {path.stem for path in (ROOT / "specs" / "tools").glob("*.md")}
    assert spec_ids == set(inventory.by_id)


def test_vendored_standards_snapshot_is_unchanged() -> None:
    entries = []
    for line in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        if relative.startswith("./agent-platform-standards/"):
            entries.append((digest, relative.removeprefix("./")))
    assert len(entries) == 48
    for expected, relative in entries:
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_standard_result_model_emits_schema_valid_success_and_failure() -> None:
    from jira_mcp.models import Completeness, ToolResult

    schema = json.loads((ROOT / "agent-platform-standards/schemas/tool-result.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    success = ToolResult(
        status="succeeded",
        capability_id="jira_issue_get_issue",
        trace_id="trace-12345678",
        data={"id": "1"},
        completeness=Completeness(state="complete", record_count=1, byte_count=10),
    ).wire()
    failure = ToolResult(
        status="failed",
        capability_id="jira_issue_get_issue",
        trace_id="trace-12345678",
        error={
            "code": "TEST",
            "message": "failure",
            "retryable": False,
            "stage": "test",
            "remediation_hint": None,
            "details_ref": None,
        },
    ).wire()
    validator.validate(success)
    validator.validate(failure)
    assert set(failure) == {"status", "capability_id", "contract_version", "trace_id", "collected_at", "error"}
