from __future__ import annotations

import httpx
import pytest
from conftest import json_response, make_executor, valid_args

from jira_mcp.adapters import adapter_for


@pytest.mark.asyncio
@pytest.mark.parametrize("index", range(114))
async def test_every_approved_capability_dispatches_with_its_locked_contract(inventory, target, index: int) -> None:
    capability = inventory.capabilities[index]
    args = valid_args(inventory, capability, include_optional_query=True)
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return json_response({"id": "1", "ok": True})

    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, handler)
    result = await executor.invoke(capability.capability_id, args, caller)

    assert result["status"] == "succeeded", result
    assert result["capability_id"] == capability.capability_id
    assert len(requests) == 1
    prepared = adapter_for(target.jira_version).prepare(capability, args)
    assert requests[0].method == capability.http_method == prepared.method
    assert requests[0].url.path.endswith(prepared.path)
    assert requests[0].headers["X-Correlation-ID"] == args["trace_id"]
    assert "authorization" in requests[0].headers
    assert "password" not in args
    assert "base_url" not in args


def test_locked_inventory_has_no_generic_rest_escape_hatch(inventory) -> None:
    forbidden = {"url", "base_url", "path", "method", "headers", "authorization", "password", "token", "cookie"}
    for capability in inventory.capabilities:
        properties = set(inventory.input_schema(capability.capability_id)["properties"])
        assert not properties.intersection(forbidden), capability.capability_id
        assert capability.http_method in {"GET", "POST", "PUT", "DELETE"}


def test_every_read_capability_is_http_get(inventory) -> None:
    assert all(item.http_method == "GET" for item in inventory.capabilities if not item.mutation)
