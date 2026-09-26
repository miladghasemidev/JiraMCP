from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.executor import JiraToolExecutor
from jira_mcp.models import CallerContext, ToolResult


def unauthenticated_context() -> CallerContext:
    return CallerContext(actor_id="unverified-mcp-caller", authenticated=False, gateway_verified=False)


def build_server(executor: JiraToolExecutor, context_provider: Callable[[Any], CallerContext] | None = None) -> Any:
    """Build the official low-level MCP server with exact generated schemas.

    A production deployment must inject a context provider that verifies gateway
    identity and delegated claims. The default is intentionally unauthenticated.
    """
    from mcp.server import Server
    from mcp.types import CallToolRequestParams, CallToolResult, ListToolsResult, PaginatedRequestParams, TextContent, Tool, ToolAnnotations

    async def list_tools(_ctx: Any, _params: PaginatedRequestParams | None) -> ListToolsResult:
        tools = [
            Tool(
                name=capability.capability_id,
                title=capability.description.rstrip("."),
                description=(
                    f"{capability.description} Approved Jira {capability.category} capability; "
                    f"risk {capability.risk_class}; target and environment required; no arbitrary REST."
                ),
                input_schema=executor.inventory.input_schema(capability.capability_id),
                annotations=ToolAnnotations(
                    read_only_hint=not capability.mutation,
                    destructive_hint=capability.risk_class == "W3",
                    idempotent_hint=not capability.mutation,
                    open_world_hint=False,
                ),
            )
            for capability in executor.inventory.capabilities
        ]
        return ListToolsResult(tools=tools)

    async def call_tool(ctx: Any, params: CallToolRequestParams) -> CallToolResult:
        if params.name not in executor.inventory.by_id:
            trace_id = str((params.arguments or {}).get("trace_id", "missing-trace"))
            result = ToolResult(
                status="failed",
                capability_id=params.name,
                trace_id=trace_id,
                error=JiraMcpError(
                    ErrorCode.CAPABILITY_DISABLED,
                    "The capability is not part of the approved Jira inventory.",
                    stage="capability_resolution",
                ).as_dict(),
            ).wire()
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, separators=(",", ":")))],
                structured_content=result,
                is_error=True,
            )
        caller = context_provider(ctx) if context_provider is not None else unauthenticated_context()
        result = await executor.invoke(params.name, params.arguments or {}, caller)
        return CallToolResult(
            content=[TextContent(type="text", text=json.dumps(result, ensure_ascii=False, separators=(",", ":"), allow_nan=False))],
            structured_content=result,
            is_error=result.get("status") == "failed",
        )

    return Server(
        "jira-mcp-on-prem",
        version="1.0.0",
        title="Jira MCP On-Premises",
        description="Exact approved 114-capability Jira Server/Data Center MCP boundary.",
        on_list_tools=list_tools,
        on_call_tool=call_tool,
    )


def health() -> dict[str, str]:
    return {"status": "ok", "service": "jira-mcp-on-prem", "version": "1.0.0"}


def readiness(executor: JiraToolExecutor) -> dict[str, Any]:
    ready, problems = executor.resolver.readiness()
    for target in executor.resolver.config.targets:
        if target.enabled:
            problems.extend(f"target {target.target_id}: unavailable production {control}" for control in executor.production_control_problems(target))
    ready = ready and not problems
    return {"status": "ready" if ready else "not_ready", "inventory_count": len(executor.inventory.capabilities), "problems": problems}
