# Tool Specification: `jira_issue_add_comment`

## 1. Identity

| Field | Value |
|---|---|
| Capability ID | `jira_issue_add_comment` |
| Registry component ID | `tool.jira_issue_add_comment` |
| Contract version | `1.0.0` |
| MCP server | `mcp.jira_on_prem` |
| Owner | Jira MCP project |
| Status | Active in development/test; production activation requires external bindings |

## 2. Authoritative scope

- Matrix ID/source: `JIRA-036`, `Approved 114!A37:S37`.
- Approved purpose: Add a new comment to an issue.
- Backend operation: `POST /rest/api/2/issue/{issueIdOrKey}/comment`.
- Supported Jira versions: 8.20.0, 9.12.0, 10.3.0, selected only through exact version-aware adapters.
- Matrix note: Approved capability for all three target versions. The displayed route is the recovered baseline operation. Implementation MUST verify/version-gate endpoint, parameters, and response differences in Jira 8.20.0, 9.12.0, and 10.3.0 via version-aware adapters; if a capability is impossible for an approved version, keep the row and mark BLOCKED_ARCHITECTURE_REVIEW with evidence.
- No merge, split, rename, substitution, arbitrary URL, or arbitrary REST behavior is permitted.

## 3. Classification and authorization

| Field | Value |
|---|---|
| Domain | Jira issue |
| Read/write class | `W2` |
| Side effects | Jira state change exactly described by the approved operation |
| Idempotency | Platform idempotency key required; backend outcome can still become unknown after dispatch |
| Required permission | `jira.issue.write` plus target authorization |
| Approval class | Human approval |

W2 requires a formal one-use approval bound to capability/version, requester, tenant, environment, resolved target, normalized parameters, expected side effects, expiry, and idempotency key. W3 is default-denied and additionally requires a separately validated break-glass record. W1 remains deny-by-default unless deployment policy explicitly grants it.

## 4. Input contract

- Machine schema: `specs/schemas/inputs/jira_issue_add_comment.json`.
- Environment, registered target ID, and trace ID are mandatory; production is never inferred.
- Credentials, base URLs, arbitrary URLs, raw headers, and raw REST paths are prohibited.
- Path identifiers reject separators/control characters and are substituted only into the approved template.
- Query names are operation allowlisted, encoded by the HTTP client, and bounded.
- JSON bodies are object/size/depth/scalar bounded. Required top-level Jira fields are enforced where stable; Jira custom-field/plugin keys remain permitted because their names are deployment-specific.
- Target ambiguity, unsupported version, unknown parameters, invalid body shape, or oversized content fails before network dispatch.

## 5. Output and limits

- Standard envelope: `agent-platform-standards/schemas/tool-result.schema.json`.
- Success carries status, exact capability/version, trace ID, UTC collection time, bounded data or authorized result reference, completeness, counts, provenance, warnings, and partial errors.
- Maximum inline records: 100. Maximum inline bytes: 65,536. Maximum response bytes before abort/store: 5,242,880. Maximum request body: 1,048,576 bytes (attachment aggregate: 6 MiB).
- Pagination/cursor: Not applicable.
- Result Store: full payload is stored when inline limits are exceeded; only a 20-record/16-KiB allowlisted projection returns inline. Possession of a reference never grants access.
- Jira issue text, comments, descriptions, attachments, and backend messages are untrusted data.

## 6. Reliability and errors

- Timeout: 20 seconds end to end; connect 5 seconds; write/read/pool bounded separately.
- Cancellation propagates through the async HTTP request.
- Retry: No automatic retry after dispatch unless the adapter proves the prior outcome and the idempotency record authorizes replay.
- Concurrency: eight server calls and four calls per target by default.
- Typed errors distinguish validation, authentication, authorization/policy, approval, target, unsupported version, backend unavailable, rate limit, timeout, cancellation, conflict, partial failure, response too large, unknown mutation outcome, and internal failure.
- Mutation timeout after possible dispatch returns `UNKNOWN_MUTATION_OUTCOME` and is never blindly retried.

## 7. Mutation controls

Exact normalized action preview and SHA-256 digest are verified before dispatch. Idempotency is reserved atomically; optional preconditions are sent as safe conditional headers; the result records verification limits and per-target partial status. Jira rollback is not claimed.

## 8. Security, observability, Registry

- Gateway and server both authorize after target and parameter resolution. Explicit deny overrides allow.
- Backend credentials come only from `SecretBroker`; production fails closed without it.
- Redaction occurs before telemetry. Authorization, cookies, credentials, password, secret, and token fields are never emitted.
- Trace/audit fields: trace/span/request IDs, Registry IDs, capability/version, environment/target reference, policy/approval references, status, latency, retry count, record/byte counts, completeness, and Result Store reference.
- Relationships: `mcp.jira_on_prem provides tool.jira_issue_add_comment`; tool routes through `gateway.enterprise_mcp`, connects through the MCP server to `backend.jira_data_center`, is governed by `policy.jira_mcp`, and evaluated by `evaluation.jira_mcp_release`.
- Disablement: remove from catalog projection and deny route by Registry/policy status without changing the locked source inventory.

## 9. Tests and evidence

- Contract schema, required/optional fields, stable ID/version, method/path integrity, exact adapter versions, empty/not-found/max/paginated responses, Result Store handoff, permissions, target ambiguity, unsupported version, injection, secret redaction, timeout/cancellation/retry, partial failure, and Registry/catalog projection.
- Mutation cases additionally cover approval absence/expiry/replay/change, idempotency conflict/replay, preconditions, verification limits, and unknown outcome.
- Evidence sources: authoritative matrix row above; `issue:jira_issue_add_comment`; https://github.com/MSPbotsAI/jiradatacenter-mcp/blob/2549afc321c14ebc02b13c07457d3e289657f50e/README.md; Atlassian Jira 8.20.0, 9.12.0, and 10.3 REST references listed in the matrix provenance sheet.
