from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.models import TargetConfig


class Limits(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_request_bytes: int = Field(default=1_048_576, ge=1024, le=8_388_608)
    max_attachment_bytes: int = Field(default=6_291_456, ge=1024, le=16_777_216)
    max_response_bytes: int = Field(default=5_242_880, ge=1024, le=16_777_216)
    max_inline_bytes: int = Field(default=65_536, ge=1024, le=262_144)
    max_inline_records: int = Field(default=100, ge=1, le=1000)
    max_projection_records: int = Field(default=20, ge=1, le=100)
    timeout_seconds: float = Field(default=20.0, ge=1.0, le=120.0)
    connect_timeout_seconds: float = Field(default=5.0, ge=0.1, le=30.0)
    max_read_retries: int = Field(default=2, ge=0, le=3)
    max_concurrency: int = Field(default=8, ge=1, le=64)
    max_concurrency_per_target: int = Field(default=4, ge=1, le=32)


class ServerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    environment: str | None = None
    targets: tuple[TargetConfig, ...] = ()
    limits: Limits = Limits()
    production_gateway_required: Literal[True] = True
    production_result_store_required: Literal[True] = True
    production_audit_sink_required: Literal[True] = True
    production_metrics_sink_required: Literal[True] = True

    @classmethod
    def load(cls, path: Path | None = None) -> ServerConfig:
        selected = path or (Path(value) if (value := os.getenv("JIRA_MCP_CONFIG")) else None)
        if selected is None:
            return cls()
        return cls.model_validate(json.loads(selected.read_text(encoding="utf-8")))


class TargetResolver:
    def __init__(self, config: ServerConfig) -> None:
        self.config = config

    def resolve(self, environment: str, target_id: str, tenant_id: str | None) -> TargetConfig:
        matches = [target for target in self.config.targets if target.enabled and target.environment == environment and target.target_id == target_id]
        if not matches:
            raise JiraMcpError(
                ErrorCode.TARGET_NOT_FOUND, "No enabled registered Jira target matches the exact environment and target ID.", stage="target_resolution"
            )
        if len(matches) != 1:
            raise JiraMcpError(ErrorCode.TARGET_AMBIGUOUS, "More than one Jira target matches; configuration must be corrected.", stage="target_resolution")
        target = matches[0]
        if target.tenant_ids and (tenant_id is None or tenant_id not in target.tenant_ids):
            raise JiraMcpError(ErrorCode.AUTHORIZATION_DENIED, "The caller tenant is not authorized for this Jira target.", stage="target_resolution")
        return target

    def readiness(self) -> tuple[bool, list[str]]:
        problems: list[str] = []
        if not self.config.targets:
            problems.append("no registered Jira targets")
        ids = [(target.environment, target.target_id) for target in self.config.targets]
        if len(ids) != len(set(ids)):
            problems.append("duplicate environment/target registrations")
        return not problems, problems
