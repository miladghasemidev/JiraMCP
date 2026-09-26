from __future__ import annotations

import asyncio

import httpx
import pytest
from conftest import json_response, make_executor, valid_args

from jira_mcp.config import Limits
from jira_mcp.errors import ErrorCode, JiraMcpError
from jira_mcp.models import CallerContext
from jira_mcp.result_store import UnavailableResultStore


def first_capability(inventory, *, mutation: bool):
    return next(item for item in inventory.capabilities if item.mutation is mutation)


@pytest.mark.asyncio
async def test_empty_and_not_found_are_distinct(inventory, target) -> None:
    capability = first_capability(inventory, mutation=False)
    args = valid_args(inventory, capability)
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response([]))
    empty = await executor.invoke(capability.capability_id, args, caller)
    assert empty["status"] == "succeeded"
    assert empty["completeness"]["record_count"] == 0

    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({"message": "missing"}, 404))
    missing = await executor.invoke(capability.capability_id, args, caller)
    assert missing["status"] == "failed"
    assert missing["error"]["code"] == ErrorCode.BACKEND_NOT_FOUND


@pytest.mark.asyncio
async def test_pagination_cursor_is_opaque_bound_and_tamper_evident(inventory, target) -> None:
    capability = first_capability(inventory, mutation=False)
    args = valid_args(inventory, capability)
    payload = {"startAt": 0, "maxResults": 2, "total": 3, "issues": [{"id": "1"}, {"id": "2"}]}
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response(payload))
    result = await executor.invoke(capability.capability_id, args, caller)
    cursor = result["completeness"]["next_cursor"]
    decoded = executor.cursor_codec.decode(cursor)
    assert result["completeness"]["state"] == "paginated"
    assert decoded["capability_id"] == capability.capability_id
    assert decoded["target_id"] == target.target_id
    assert decoded["next_start"] == 2
    with pytest.raises(JiraMcpError) as exc:
        executor.cursor_codec.decode(cursor[:-1] + ("A" if cursor[-1] != "A" else "B"))
    assert exc.value.code == ErrorCode.VALIDATION_ERROR


@pytest.mark.asyncio
async def test_large_result_is_stored_and_acl_scoped(inventory, target) -> None:
    capability = first_capability(inventory, mutation=False)
    args = valid_args(inventory, capability)
    limits = Limits(max_inline_bytes=1024, max_inline_records=2, max_projection_records=1)
    payload = [{"id": str(i), "description": "x" * 600} for i in range(3)]
    executor, caller, _audit, store = make_executor(inventory, capability, target, args, lambda _r: json_response(payload), limits=limits)
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "succeeded"
    assert result["result_ref"]["id"]
    assert result["completeness"]["state"] == "truncated"
    assert len(result["data"]) == 1
    full = await store.project(result["result_ref"]["id"], caller=caller, max_records=10, max_bytes=10_000)
    assert len(full) == 3
    other = CallerContext(actor_id="other", tenant_id="tenant-a", authenticated=True, gateway_verified=True)
    with pytest.raises(JiraMcpError) as exc:
        await store.project(result["result_ref"]["id"], caller=other, max_records=10, max_bytes=10_000)
    assert exc.value.code == ErrorCode.AUTHORIZATION_DENIED


@pytest.mark.asyncio
async def test_partial_backend_payload_has_explicit_partial_semantics(inventory, target) -> None:
    capability = first_capability(inventory, mutation=False)
    args = valid_args(inventory, capability)
    payload = {"issues": [{"id": "1"}], "errors": [{"issue": "2", "message": "denied"}]}
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response(payload))
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "partial"
    assert result["errors"][0]["code"] == "PARTIAL_BACKEND_FAILURE"


@pytest.mark.asyncio
async def test_reads_retry_but_mutations_do_not(inventory, target) -> None:
    read = first_capability(inventory, mutation=False)
    read_args = valid_args(inventory, read)
    read_calls = 0

    def read_handler(_request: httpx.Request) -> httpx.Response:
        nonlocal read_calls
        read_calls += 1
        return json_response({"retry": read_calls}, 503 if read_calls < 3 else 200)

    executor, caller, _audit, _store = make_executor(inventory, read, target, read_args, read_handler)
    assert (await executor.invoke(read.capability_id, read_args, caller))["status"] == "succeeded"
    assert read_calls == 3

    mutation = first_capability(inventory, mutation=True)
    mutation_args = valid_args(inventory, mutation)
    mutation_calls = 0

    def mutation_handler(_request: httpx.Request) -> httpx.Response:
        nonlocal mutation_calls
        mutation_calls += 1
        return json_response({"message": "unavailable"}, 503)

    executor, caller, _audit, _store = make_executor(inventory, mutation, target, mutation_args, mutation_handler)
    result = await executor.invoke(mutation.capability_id, mutation_args, caller)
    assert result["error"]["code"] == ErrorCode.BACKEND_UNAVAILABLE
    assert mutation_calls == 1


@pytest.mark.asyncio
async def test_mutation_transport_loss_is_unknown_outcome(inventory, target) -> None:
    capability = first_capability(inventory, mutation=True)
    args = valid_args(inventory, capability)

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("lost after dispatch", request=request)

    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, handler)
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "failed"
    assert result["error"]["code"] == ErrorCode.UNKNOWN_MUTATION_OUTCOME


@pytest.mark.asyncio
async def test_cancellation_returns_typed_failure(inventory, target) -> None:
    capability = first_capability(inventory, mutation=False)
    args = valid_args(inventory, capability)

    async def handler(_request: httpx.Request) -> httpx.Response:
        await asyncio.sleep(10)
        return json_response({})

    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, handler)
    task = asyncio.create_task(executor.invoke(capability.capability_id, args, caller))
    await asyncio.sleep(0)
    task.cancel()
    result = await task
    assert result["status"] == "failed"
    assert result["error"]["code"] == ErrorCode.CANCELLED


@pytest.mark.asyncio
async def test_oversized_backend_response_is_aborted(inventory, target) -> None:
    capability = first_capability(inventory, mutation=False)
    args = valid_args(inventory, capability)
    limits = Limits(max_response_bytes=1024)
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({"value": "x" * 2048}), limits=limits)
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["error"]["code"] == ErrorCode.RESPONSE_TOO_LARGE


@pytest.mark.asyncio
async def test_mutation_reports_partial_when_oversized_result_cannot_be_stored(inventory, target) -> None:
    capability = first_capability(inventory, mutation=True)
    args = valid_args(inventory, capability)
    limits = Limits(max_inline_bytes=1024)
    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, lambda _r: json_response({"value": "x" * 2048}), limits=limits)
    executor.result_store = UnavailableResultStore()
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "partial"
    assert result["warnings"][0]["code"] == "RESULT_STORE_DELIVERY_FAILED"


def test_unsupported_adapter_version_is_typed() -> None:
    from jira_mcp.adapters import adapter_for

    with pytest.raises(JiraMcpError) as exc:
        adapter_for("9.13.0")
    assert exc.value.code == ErrorCode.UNSUPPORTED_JIRA_VERSION


@pytest.mark.asyncio
async def test_precondition_is_forwarded_only_as_conditional_header(inventory, target) -> None:
    capability = next(item for item in inventory.capabilities if item.mutation and "precondition" in inventory.input_schema(item.capability_id)["properties"])
    args = valid_args(inventory, capability)
    args["precondition"] = '"revision-1"'
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return json_response({"id": "1"})

    executor, caller, _audit, _store = make_executor(inventory, capability, target, args, handler)
    result = await executor.invoke(capability.capability_id, args, caller)
    assert result["status"] == "succeeded"
    assert requests[0].headers["If-Match"] == '"revision-1"'
