from __future__ import annotations

import json

import httpx
import pytest
from conftest import caller_for, json_response, make_executor, valid_args
from mcp import Client

from jira_mcp.server import build_server


@pytest.mark.asyncio
async def test_official_mcp_transport_lists_exactly_the_approved_114(inventory, target) -> None:
    capability = next(item for item in inventory.capabilities if not item.mutation)
    args = valid_args(inventory, capability)
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({}))
    server = build_server(executor, lambda _ctx: caller)
    async with Client(server) as client:
        listed = await client.list_tools()
    names = [tool.name for tool in listed.tools]
    assert len(names) == len(set(names)) == 114
    assert set(names) == set(inventory.by_id)
    assert not {"execute_rest", "jira_rest", "http_request"}.intersection(names)


@pytest.mark.asyncio
async def test_official_mcp_transport_invokes_typed_tool(inventory, target) -> None:
    capability = next(item for item in inventory.capabilities if not item.mutation)
    args = valid_args(inventory, capability)
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return json_response({"id": "1"})

    executor, _caller, _audit, _store = make_executor(inventory, capability, target, args, handler)
    server = build_server(executor, lambda _ctx: caller_for(capability))
    async with Client(server) as client:
        result = await client.call_tool(capability.capability_id, args)
    payload = result.structured_content
    assert payload is not None
    assert payload["status"] == "succeeded"
    assert json.loads(result.content[0].text)["capability_id"] == capability.capability_id
    assert len(requests) == 1


@pytest.mark.asyncio
async def test_default_mcp_context_is_fail_closed(inventory, target) -> None:
    capability = next(item for item in inventory.capabilities if not item.mutation)
    args = valid_args(inventory, capability)
    executor, _caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({}))
    async with Client(build_server(executor)) as client:
        result = await client.call_tool(capability.capability_id, args)
    assert result.is_error is True
    assert result.structured_content["error"]["code"] == "AUTHENTICATION_REQUIRED"


@pytest.mark.asyncio
async def test_unapproved_mcp_name_returns_typed_failure(inventory, target) -> None:
    capability = next(item for item in inventory.capabilities if not item.mutation)
    args = valid_args(inventory, capability)
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({}))
    async with Client(build_server(executor, lambda _ctx: caller)) as client:
        result = await client.call_tool("jira_unapproved_request", args)
    assert result.is_error is True
    assert result.structured_content["error"]["code"] == "CAPABILITY_DISABLED"
