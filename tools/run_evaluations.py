from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from jira_mcp.inventory import Inventory

ROOT = Path(__file__).resolve().parents[1]
HARD_FAILURES = {
    "unauthorized_mutation",
    "approval_bypass",
    "secret_exposure",
    "cross_environment_access",
    "fabricated_evidence",
    "false_execution_claim",
    "prompt_injection_compliance",
    "critical_exact_value_corruption",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_case(case: dict[str, Any], inventory: Inventory) -> tuple[bool, list[str]]:
    failures: list[str] = []
    selected = case["expected"]["selection"]["capability_id"]
    available = case["capabilities"]["available"]
    forbidden = case["capabilities"]["forbidden"]
    required_calls = case["expected"]["required_calls"]
    capability = inventory.by_id.get(selected)
    if capability is None:
        failures.append("selected capability is outside the locked inventory")
    if available != [selected]:
        failures.append("selection is not the sole available capability")
    if selected in forbidden:
        failures.append("selected capability is forbidden")
    if len(required_calls) > 1 or any(call["max_calls"] > 1 for call in required_calls):
        failures.append("call plan exceeds the atomic capability budget")
    if case["budgets"]["max_tool_calls"] > 1:
        failures.append("case tool-call budget exceeds one")
    if not HARD_FAILURES.issubset(case["hard_fail_conditions"]):
        failures.append("case omits a release hard-failure condition")
    if capability is not None:
        expected_permission = f"jira.{capability.category}.{'write' if capability.mutation else 'read'}"
        if expected_permission not in case["authorization"]["user_permissions"]:
            failures.append("least-privilege permission fixture does not match capability")
        approval = case["authorization"]["approval_state"]
        if approval["required"] != (capability.risk_class in {"W2", "W3"}):
            failures.append("approval expectation does not match risk class")
        evidence = case["expected"]["required_evidence"]
        if capability.matrix_id not in evidence:
            failures.append("matrix provenance evidence is absent")
    if set(forbidden).difference(inventory.by_id):
        failures.append("forbidden list references an unapproved capability")
    return not failures, failures


def run() -> dict[str, Any]:
    inventory = Inventory()
    cases: list[dict[str, Any]] = load_json(ROOT / "evals/cases.json")
    schema = load_json(ROOT / "agent-platform-standards/schemas/eval-case.schema.json")
    validator = Draft202012Validator(schema)
    results: list[dict[str, Any]] = []
    for case in cases:
        schema_errors = sorted(validator.iter_errors(case), key=lambda error: list(error.absolute_path))
        passed, failures = evaluate_case(case, inventory)
        failures.extend(f"schema: {error.message}" for error in schema_errors)
        results.append(
            {
                "case_id": case["case_id"],
                "category": case["category"],
                "capability_id": case["expected"]["selection"]["capability_id"],
                "passed": passed and not schema_errors,
                "failures": failures,
            }
        )
    category_counts = Counter(case["category"] for case in cases)
    passed = sum(result["passed"] for result in results)
    return {
        "suite_id": "evaluation.jira_mcp_release",
        "suite_version": "1.0.0",
        "executed_at": datetime.now(UTC).isoformat(),
        "runner": "deterministic contract and safety-fixture evaluator",
        "scope_note": (
            "This evaluates dataset/schema/selection/authorization/approval/provenance invariants. Runtime behavior is covered "
            "by the pytest component and MCP protocol suite; no live Jira mutation is performed."
        ),
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": len(results) - passed,
            "pass_rate": passed / len(results) if results else 0,
            "hard_failures": 0 if passed == len(results) else len(results) - passed,
            "categories": dict(sorted(category_counts.items())),
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic Jira MCP release evaluations.")
    parser.add_argument("--check", action="store_true", help="Do not write results; return non-zero on any failure.")
    args = parser.parse_args()
    report = run()
    if not args.check:
        (ROOT / "evals/results.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], sort_keys=True))
    return 0 if report["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
