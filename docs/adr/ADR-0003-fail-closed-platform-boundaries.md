# ADR 0003: Fail-Closed External Platform Boundaries and Version-Aware Jira Dispatch

- Status: Accepted for implementation
- Date: 2026-09-13
- Owners: Jira MCP project
- Review date or expiry: 2026-12-13
- Supersedes/superseded by: None

## Context

The repository supplies no production Gateway, identity provider, secret broker, policy engine, Result Store, audit sink, or Jira deployment configuration. The approved matrix contains 114 exact capabilities across Jira 8.20.0, 9.12.0, and 10.3.0. The standards require strict boundaries and prohibit fabricating missing enterprise services.

## Decision

Implement one Python 3.12 MCP server using the official MCP Python SDK 2.2.0, Pydantic contracts, JSON Schema validation, and an async HTTPX Jira client. Generate exact tool schemas and Registry/catalog metadata from the authoritative matrix. Route every invocation through an inventory lookup and an exact version adapter; no caller can supply a method, path, URL, header, or credential.

External controls use typed protocols. Development/test may inject in-memory fakes. The default runtime binds deny-all policy, unavailable approval/secret/result/audit services, and no targets. Production therefore fails closed until the enterprise deployment supplies verified gateway context and all required bindings.

Jira credentials use Basic authentication because the pinned historical source and Jira Server 8.20 documentation justify it; values come only from the secret broker. This does not authorize credentials in MCP arguments or ordinary configuration.

## Consequences and controls

- Exact matrix IDs remain the MCP tool names even though they use the approved legacy underscore namespace.
- Jira custom fields and plugin extensions make some request object keys deployment-specific. Schemas enforce stable required top-level fields where documented and otherwise use a bounded JSON object with runtime depth, key, scalar, item, and byte validation.
- The three adapters currently preserve the approved baseline route because the matrix approves it for all target versions. Adapter selection remains exact and isolated so verified differences can be added without changing tool contracts.
- W2 requires one-use formal approval; W3 also requires exceptional break-glass evidence and explicit irreversible confirmation. W1 is deny-by-default unless policy grants it.
- A mutation transport failure after dispatch becomes `UNKNOWN_MUTATION_OUTCOME` and is never automatically retried.
- Large output requires the Result Store. Possession of a reference is not authorization.

## Validation

Contract, full-inventory dispatch, policy/approval/idempotency, result-size/projection, pagination/cursor, retry/timeout/cancellation, Registry/catalog/schema, MCP protocol, lint, type-check, and evaluation tests are release gates.

## Rollback or reversal

Disable the server or any capability through Registry/catalog/policy state and deploy the previous exact package version. The authoritative inventory is retained during disablement.

## Standard exceptions

None. ADR-0001 is the existing project interpretation that scope admission is already complete.

