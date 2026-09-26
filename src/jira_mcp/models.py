from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

Environment = Literal["development", "test", "production"]
RiskClass = Literal["R0", "R1", "R2", "W1", "W2", "W3"]


class TargetConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    target_id: str = Field(pattern=r"^[A-Za-z0-9._:-]{1,128}$")
    environment: Environment
    base_url: HttpUrl
    jira_version: Literal["8.20.0", "9.12.0", "10.3.0"]
    secret_ref: str = Field(min_length=1, max_length=512)
    enabled: bool = True
    tls_verify: bool = True
    tenant_ids: tuple[str, ...] = ()

    @field_validator("base_url")
    @classmethod
    def require_https_except_development(cls, value: HttpUrl, info: Any) -> HttpUrl:
        environment = info.data.get("environment")
        if environment != "development" and value.scheme != "https":
            raise ValueError("test and production Jira targets must use HTTPS")
        return value


class CallerContext(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    actor_id: str = Field(min_length=1, max_length=256)
    delegated_user_id: str | None = Field(default=None, max_length=256)
    tenant_id: str | None = Field(default=None, max_length=128)
    permissions: frozenset[str] = frozenset()
    authenticated: bool = True
    gateway_verified: bool = False
    policy_version: str | None = None


class Credential(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    username: str = Field(min_length=1, max_length=256)
    password: str = Field(min_length=1, max_length=4096, repr=False)


class Completeness(BaseModel):
    model_config = ConfigDict(extra="forbid")

    state: Literal["complete", "paginated", "filtered", "sampled", "truncated"]
    record_count: int = Field(ge=0)
    total_count: int | None = Field(default=None, ge=0)
    byte_count: int = Field(ge=0)
    next_cursor: str | None = None
    reason: str | None = None


class ResultReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    expires_at: datetime
    schema_version: str | None = "1.0.0"


class ToolResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["succeeded", "partial", "failed"]
    capability_id: str
    contract_version: str = "1.0.0"
    trace_id: str
    collected_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    data: Any | None = None
    result_ref: ResultReference | None = None
    completeness: Completeness | None = None
    provenance: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[dict[str, str]] = Field(default_factory=list)
    errors: list[dict[str, Any]] = Field(default_factory=list)
    error: dict[str, Any] | None = None

    def wire(self) -> dict[str, Any]:
        document = self.model_dump(mode="json", exclude_none=True)
        if self.status == "failed":
            allowed = {"status", "capability_id", "contract_version", "trace_id", "collected_at", "error"}
            return {key: value for key, value in document.items() if key in allowed}
        document.pop("error", None)
        return document


class BackendResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status_code: int
    content_type: str
    payload: Any
    raw_size: int = Field(ge=0)
    request_url: str
    response_headers: dict[str, str] = Field(default_factory=dict)
    attempt_count: int = Field(default=1, ge=1)
