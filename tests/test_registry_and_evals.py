from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

from jira_mcp.inventory import Inventory

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_registry_schema_and_exact_tool_projection(inventory: Inventory) -> None:
    registry = load("registry/agent-registry.json")
    schema = load("agent-platform-standards/schemas/agent-registry.schema.json")
    Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER).validate(registry)
    tool_ids = {component["metadata"]["capability_id"] for component in registry["components"] if component["kind"] == "tool"}
    assert tool_ids == set(inventory.by_id)
    component_ids = {component["id"] for component in registry["components"]}
    assert len(component_ids) == len(registry["components"])
    for relationship in registry["relationships"]:
        assert relationship["source_id"] in component_ids
        assert relationship["target_id"] in component_ids


def test_catalog_schema_and_no_extra_capabilities(inventory: Inventory) -> None:
    catalog = load("registry/capability-catalog.json")
    schema = load("agent-platform-standards/schemas/capability-manifest.schema.json")
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    assert len(catalog["capabilities"]) == 114
    for entry in catalog["capabilities"]:
        validator.validate(entry)
    projected_tool_ids = {f"jira_{entry['capability_id'].removeprefix('jira.')}" for entry in catalog["capabilities"]}
    assert projected_tool_ids == set(inventory.by_id)


def test_eval_dataset_meets_release_composition_and_schema() -> None:
    cases = load("evals/cases.json")
    schema = load("agent-platform-standards/schemas/eval-case.schema.json")
    validator = Draft202012Validator(schema)
    assert Counter(case["category"] for case in cases) == {
        "easy": 50,
        "normal": 50,
        "difficult": 30,
        "adversarial": 20,
        "permission_safety": 20,
    }
    for case in cases:
        validator.validate(case)
        assert case["budgets"]["max_tool_calls"] <= 1
        assert "unauthorized_mutation" in case["hard_fail_conditions"]
        assert "prompt_injection_compliance" in case["hard_fail_conditions"]
