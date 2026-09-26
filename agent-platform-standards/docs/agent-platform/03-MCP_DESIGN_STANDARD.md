# MCP Design Standard

## 1. Scope

This standard governs every Model Context Protocol server integrated into the platform, whether local, remote, first-party, or third-party.

## 2. Server boundary

An MCP server SHOULD represent one coherent domain or security boundary, such as SQL Server administration, Jira, Oracle, or KMS. Split a server when capabilities require materially different owners, credentials, network zones, release cadences, or risk controls.

Do not split solely because a backend exposes many endpoints.

## 3. Required server specification

Before implementation, every server MUST define:

- Purpose and non-goals
- Domain owner and technical owner
- Supported backend products and versions
- Deployment environments and network boundaries
- Authentication and delegated-identity model
- Authorization and approval model
- Tools, resources, and any prompt assets
- Versioning and compatibility policy
- Input/output limits and Result Store behavior
- Error model, timeout, cancellation, and retry policy
- Audit events, metrics, traces, and redaction rules
- Test and evaluation plan
- Disablement and rollback procedure
- Registry component ID, lifecycle state, owner, deployments, and declared relationships

Use `templates/MCP_TEMPLATE.md`.

## 4. Capability selection

Every proposed tool MUST pass the capability decision tree after the Agent Registry, Dependency Map, and Capability Catalog have been searched. An endpoint MUST NOT become a tool merely because it exists.

Prefer:

- Reusable domain operations
- High-signal diagnostic bundles when the bundle is deterministic and broadly reusable
- Server-side filtering and aggregation
- Stable concepts that survive backend API changes

Avoid:

- Overlapping synonyms
- Tools differentiated only by a fixed filter
- Hidden multi-step mutations
- Generic arbitrary-query or arbitrary-command tools exposed to ordinary agents
- Unbounded data export through model context

## 5. Contract rules

- Tool names MUST be stable, namespaced, and action-oriented: `sqlserver.get_blocking_context`.
- Input and output schemas MUST be explicit and versioned.
- Required and optional fields MUST be distinguishable.
- Units, timezone, encoding, and null semantics MUST be stated.
- Identifiers MUST be opaque strings unless their format is a contract.
- Enum evolution MUST be backward-compatible or versioned.
- Responses MUST use the standard result or error envelope.
- Breaking changes require a new major contract version and a migration period.

## 6. Output control

Every list or search capability MUST support at least one of:

- A stable cursor with a page limit
- A server-side aggregation contract
- A bounded top-N result contract
- A Result Store reference

Responses MUST declare whether they are complete, paginated, sampled, filtered, or truncated. Silent truncation is prohibited.

## 7. Authentication and authorization

- The server MUST authenticate the gateway or trusted caller.
- End-user identity and delegated service identity MUST remain distinguishable.
- Authorization MUST be checked for the operation and target at call time.
- Tool discovery MUST NOT imply permission to execute.
- Backend credentials MUST be retrieved from an approved secret broker and MUST NOT appear in tool arguments.
- Production access MUST be explicit.

## 8. Read and mutation separation

Read and write operations MUST use separate tool contracts and capability permissions. A diagnostic tool MUST NOT perform cleanup, remediation, state refresh, or configuration change as a side effect.

Mutation tools MUST declare:

- Exact side effects and affected resource types
- Risk class and required approval class
- Preconditions and concurrency controls
- Idempotency behavior
- Dry-run or preview support where technically meaningful
- Rollback or compensation limits
- Verification behavior

## 9. Errors

Servers MUST return typed errors with:

- Stable error code
- Safe human message
- Retryable flag
- Failure stage
- Correlation identifier
- Optional safe remediation hint
- Details that do not expose secrets or sensitive backend internals

Transport failures, authorization failures, validation failures, backend failures, partial failures, policy denials, timeouts, and unknown mutation outcomes MUST remain distinguishable.

## 10. Timeout, cancellation, and retry

- Each tool MUST declare a maximum execution time.
- Long operations SHOULD return an operation identifier and support status/cancel capabilities.
- Cancellation SHOULD propagate to the backend when supported.
- The server MUST NOT retry non-idempotent mutations without an idempotency key and a known prior outcome.
- Backoff and maximum retry counts MUST be bounded.

## 11. Resources and prompts

Use MCP resources for versioned, addressable reference content that benefits from direct retrieval. Use skills for operational procedure. Server-provided prompts MUST NOT replace platform policy or silently modify authorization behavior.

## 12. Observability

The server MUST accept and propagate a workflow trace identifier and record:

- Capability and contract version
- Caller and delegated identity references
- Target environment and resource scope
- Start/end timestamps, latency, result status, and row/byte counts
- Policy and approval references for protected actions
- Result Store reference when applicable
- Stable Registry IDs for the server, capability, gateway route, and backend target

Do not log credentials, full prompts, prohibited sensitive fields, or unbounded backend payloads.

## 13. Health and readiness

The server MUST expose operational health separately from backend readiness. Health checks MUST NOT require destructive access. Readiness SHOULD verify critical configuration and dependency reachability using the least privilege possible.

## 14. Required tests

At minimum:

- Schema and contract tests
- Authentication and authorization tests
- Backend-version integration tests
- Pagination, truncation, and Result Store tests
- Timeout, cancellation, retry, and partial-failure tests
- Secret-redaction and prompt-injection tests
- Mutation approval, idempotency, concurrency, and unknown-outcome tests
- Catalog discovery and version compatibility tests

## 15. Release criteria

An MCP server MAY enter production only when its exact version, owner, supported versions, Registry entry and relationships, capability-catalog projection, least-privilege credentials, policies, dashboards, alerts, test evidence, evaluation score, and rollback method are recorded and approved.
