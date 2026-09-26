from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.inventory import Capability

QUERY_NAME_MAP = {
    "start_at": "startAt",
    "max_results": "maxResults",
    "validate_query": "validateQuery",
    "project_key_or_id": "projectKeyOrId",
    "board_id": "boardId",
    "notify_users": "notifyUsers",
    "update_history": "updateHistory",
    "delete_subtasks": "deleteSubtasks",
    "global_id": "globalId",
    "adjust_estimate": "adjustEstimate",
    "new_estimate": "newEstimate",
    "reduce_by": "reduceBy",
    "increase_by": "increaseBy",
    "current_jql": "currentJQL",
    "current_issue_key": "currentIssueKey",
    "current_project_id": "currentProjectId",
    "show_sub_tasks": "showSubTasks",
    "show_sub_task_parent": "showSubTaskParent",
    "transition_id": "transitionId",
    "include_archived": "includeArchived",
    "browse_archive": "browseArchive",
    "project_ids": "projectIds",
    "move_fix_issues_to": "moveFixIssuesTo",
    "move_affected_issues_to": "moveAffectedIssuesTo",
}

NON_TRANSPORT_FIELDS = {
    "environment",
    "target_id",
    "tenant_id",
    "trace_id",
    "request_id",
    "approval_ref",
    "break_glass_ref",
    "confirm_irreversible",
    "idempotency_key",
    "precondition",
    "body",
    "attachments",
}


@dataclass(frozen=True, slots=True)
class PreparedRequest:
    method: str
    path: str
    query: dict[str, Any]
    body: dict[str, Any] | None
    attachments: list[dict[str, str]] | None
    headers: dict[str, str]


class JiraAdapter:
    version: str

    def __init__(self, version: str) -> None:
        self.version = version

    def prepare(self, capability: Capability, args: dict[str, Any]) -> PreparedRequest:
        if self.version not in capability.supported_versions:
            raise JiraMcpError(ErrorCode.UNSUPPORTED_JIRA_VERSION, "The capability is not approved for this Jira version.", stage="adapter")
        path = capability.baseline_rest_path
        path_names = re.findall(r"\{([^}]+)\}", path)
        used: set[str] = set()
        for raw_name in path_names:
            name = re.sub(r"(?<!^)(?=[A-Z])", "_", raw_name).replace("-", "_").lower()
            value = args.get(name)
            if value is None:
                raise JiraMcpError(ErrorCode.VALIDATION_ERROR, f"Missing path parameter '{name}'.", stage="adapter")
            text = str(value)
            if not text or "/" in text or "\\" in text or any(ord(char) < 32 for char in text):
                raise JiraMcpError(ErrorCode.VALIDATION_ERROR, f"Invalid path parameter '{name}'.", stage="adapter")
            path = path.replace("{" + raw_name + "}", quote(text, safe=""))
            used.add(name)
        query = {
            QUERY_NAME_MAP.get(name, name): value for name, value in args.items() if name not in NON_TRANSPORT_FIELDS and name not in used and value is not None
        }
        headers: dict[str, str] = {}
        headers["X-Correlation-ID"] = str(args["trace_id"])
        if request_id := args.get("request_id"):
            headers["X-Request-ID"] = str(request_id)
        if precondition := args.get("precondition"):
            headers["If-Match"] = str(precondition)
        if capability.capability_id == "jira_issue_add_attachment":
            headers["X-Atlassian-Token"] = "no-check"
        return PreparedRequest(
            method=capability.http_method,
            path=path,
            query=query,
            body=args.get("body"),
            attachments=args.get("attachments"),
            headers=headers,
        )


class Jira820Adapter(JiraAdapter):
    def __init__(self) -> None:
        super().__init__("8.20.0")


class Jira912Adapter(JiraAdapter):
    def __init__(self) -> None:
        super().__init__("9.12.0")


class Jira103Adapter(JiraAdapter):
    def __init__(self) -> None:
        super().__init__("10.3.0")


ADAPTERS: dict[str, JiraAdapter] = {
    "8.20.0": Jira820Adapter(),
    "9.12.0": Jira912Adapter(),
    "10.3.0": Jira103Adapter(),
}


def adapter_for(version: str) -> JiraAdapter:
    try:
        return ADAPTERS[version]
    except KeyError as exc:
        raise JiraMcpError(ErrorCode.UNSUPPORTED_JIRA_VERSION, "Only Jira 8.20.0, 9.12.0, and 10.3.0 are supported.", stage="adapter") from exc
