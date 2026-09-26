from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any, cast

from jira_mcp.errors import ErrorCode, JiraMcpError

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INVENTORY = ROOT / "specs" / "APPROVED_CAPABILITY_INVENTORY.json"
DEFAULT_SCHEMA_DIR = ROOT / "specs" / "schemas" / "inputs"


@dataclass(frozen=True, slots=True)
class Capability:
    matrix_id: str
    capability_id: str
    category: str
    description: str
    http_method: str
    baseline_rest_path: str
    risk_class: str
    mutation: bool
    approval_class: str
    output_handling: str
    source: dict[str, Any]
    supported_versions: tuple[str, ...] = ("8.20.0", "9.12.0", "10.3.0")

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> Capability:
        return cls(
            matrix_id=row["matrix_id"],
            capability_id=row["capability_id"],
            category=row["category"],
            description=row["description"],
            http_method=row["http_method"],
            baseline_rest_path=row["baseline_rest_path"],
            risk_class=row["risk_class"],
            mutation=row["mutation"] == "Yes",
            approval_class=row["approval_class"],
            output_handling=row["output_handling"],
            source=row["source"],
        )


class Inventory:
    def __init__(self, path: Path = DEFAULT_INVENTORY, schema_dir: Path = DEFAULT_SCHEMA_DIR) -> None:
        document = json.loads(path.read_text(encoding="utf-8"))
        rows = document["capabilities"]
        self.path = path
        self.schema_dir = schema_dir
        self.source_sha256: str = document["source"]["sha256"]
        self.capabilities = tuple(Capability.from_row(row) for row in rows)
        ids = [item.capability_id for item in self.capabilities]
        matrix_ids = [item.matrix_id for item in self.capabilities]
        if len(ids) != 114 or len(set(ids)) != 114 or len(set(matrix_ids)) != 114:
            raise RuntimeError("approved inventory invariant failed: expected exactly 114 distinct capabilities")

    @cached_property
    def by_id(self) -> dict[str, Capability]:
        return {item.capability_id: item for item in self.capabilities}

    def get(self, capability_id: str) -> Capability:
        try:
            return self.by_id[capability_id]
        except KeyError as exc:
            raise JiraMcpError(
                ErrorCode.CAPABILITY_DISABLED,
                "The capability is not part of the approved Jira inventory.",
                stage="capability_resolution",
            ) from exc

    def input_schema(self, capability_id: str) -> dict[str, Any]:
        self.get(capability_id)
        return cast(dict[str, Any], json.loads((self.schema_dir / f"{capability_id}.json").read_text(encoding="utf-8")))
