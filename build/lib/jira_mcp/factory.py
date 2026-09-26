from __future__ import annotations

import secrets

from jira_mcp.client import JiraHttpClient
from jira_mcp.config import ServerConfig, TargetResolver
from jira_mcp.cursor import CursorCodec
from jira_mcp.executor import JiraToolExecutor
from jira_mcp.inventory import Inventory
from jira_mcp.observability import UnavailableAuditSink
from jira_mcp.result_store import UnavailableResultStore
from jira_mcp.security import (
    DenyAllPolicy,
    InMemoryIdempotencyStore,
    UnavailableApprovalVerifier,
    UnavailableSecretBroker,
)


def build_fail_closed_executor(config: ServerConfig | None = None) -> JiraToolExecutor:
    selected = config or ServerConfig.load()
    return JiraToolExecutor(
        inventory=Inventory(),
        resolver=TargetResolver(selected),
        policy=DenyAllPolicy(),
        approvals=UnavailableApprovalVerifier(),
        secret_broker=UnavailableSecretBroker(),
        result_store=UnavailableResultStore(),
        idempotency=InMemoryIdempotencyStore(),
        audit=UnavailableAuditSink(),
        cursor_codec=CursorCodec(secrets.token_bytes(32)),
        client=JiraHttpClient(selected.limits),
        limits=selected.limits,
    )
