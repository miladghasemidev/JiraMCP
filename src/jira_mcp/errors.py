from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    AUTHORIZATION_DENIED = "AUTHORIZATION_DENIED"
    POLICY_UNAVAILABLE = "POLICY_UNAVAILABLE"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    APPROVAL_INVALID = "APPROVAL_INVALID"
    APPROVAL_EXPIRED = "APPROVAL_EXPIRED"
    APPROVAL_REPLAYED = "APPROVAL_REPLAYED"
    TARGET_NOT_FOUND = "TARGET_NOT_FOUND"
    TARGET_AMBIGUOUS = "TARGET_AMBIGUOUS"
    UNSUPPORTED_JIRA_VERSION = "UNSUPPORTED_JIRA_VERSION"
    CAPABILITY_DISABLED = "CAPABILITY_DISABLED"
    BACKEND_AUTHENTICATION_FAILED = "BACKEND_AUTHENTICATION_FAILED"
    BACKEND_AUTHORIZATION_DENIED = "BACKEND_AUTHORIZATION_DENIED"
    BACKEND_NOT_FOUND = "BACKEND_NOT_FOUND"
    BACKEND_CONFLICT = "BACKEND_CONFLICT"
    BACKEND_RATE_LIMITED = "BACKEND_RATE_LIMITED"
    BACKEND_UNAVAILABLE = "BACKEND_UNAVAILABLE"
    RESPONSE_TOO_LARGE = "RESPONSE_TOO_LARGE"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    PARTIAL_FAILURE = "PARTIAL_FAILURE"
    UNKNOWN_MUTATION_OUTCOME = "UNKNOWN_MUTATION_OUTCOME"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    RESULT_STORE_REQUIRED = "RESULT_STORE_REQUIRED"
    RESULT_STORE_UNAVAILABLE = "RESULT_STORE_UNAVAILABLE"
    SECRET_BROKER_UNAVAILABLE = "SECRET_BROKER_UNAVAILABLE"
    EXTERNAL_CONTROL_UNAVAILABLE = "EXTERNAL_CONTROL_UNAVAILABLE"
    INTERNAL_ERROR = "INTERNAL_ERROR"


@dataclass(slots=True)
class JiraMcpError(Exception):
    code: ErrorCode
    message: str
    retryable: bool = False
    stage: str = "internal"
    remediation_hint: str | None = None
    details: dict[str, Any] | None = None

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "code": self.code.value,
            "message": self.message,
            "retryable": self.retryable,
            "stage": self.stage,
            "remediation_hint": self.remediation_hint,
            "details_ref": None,
        }
