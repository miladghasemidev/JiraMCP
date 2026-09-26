# Agent Instructions for This Repository

These instructions apply to all files and implementation work under this directory.

## Mandatory workflow

Before proposing or implementing a new capability:

1. Read `README.md`.
2. Read `docs/agent-platform/01-AGENT_PLATFORM_ARCHITECTURE.md` and `02-AGENT_ENGINEERING_PRINCIPLES.md`.
3. Read `docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md` and search the Agent Registry, Capability Catalog, and repository.
4. Apply `docs/agent-platform/15-DECISION_TREES.md`.
5. Complete `templates/CAPABILITY_REQUEST_TEMPLATE.md`.
6. Reuse an existing tool, skill, script, query, or workflow when it satisfies the requirement.
7. If a new artifact remains necessary, read its governing standard and complete its template before implementation.
8. Apply the security, observability, Registry, dependency, and evaluation standards to every change.

## Non-negotiable rules

- Do not create one MCP tool per backend API endpoint.
- Do not create a tool when deterministic code over existing capabilities is sufficient.
- Do not create a skill for a one-off answer or an atomic backend operation.
- Do not load every tool schema or every skill into model context.
- Do not return unbounded records or raw large datasets to the model.
- Do not place credentials, connection strings, private keys, access tokens, or sensitive raw data in prompts, model context, logs, traces, or errors.
- Do not execute a mutation without an explicit policy decision; high-impact or irreversible mutations require human approval.
- Do not silently broaden scope, permissions, data access, or affected resources.
- Do not claim a diagnosis without cited evidence, and clearly label inference and uncertainty.
- Do not auto-merge self-improvement proposals produced from traces or feedback.
- Do not deploy an unregistered, unmanaged, ownerless, unversioned, or unevaluated component to production.
- Do not treat a runtime-observed dependency as automatically approved.

## Required defaults

- Read-only, least privilege, bounded output, deny by default.
- Structured and versioned contracts.
- Stable identifiers and explicit timestamps with timezone.
- Idempotency for retryable writes.
- Short-lived, scoped credentials obtained outside model context.
- Result references for large data; only compact projections enter context.
- Hybrid permission-aware KMS retrieval where semantic retrieval is required.
- Trace propagation across agent, code, CLI, gateway, MCP server, and backend.
- Stable Registry identities and declared dependency relationships for every production component.

## Definition of done

No capability is complete until:

- The design classification and specification are committed.
- Contract, unit, integration, security, and trace-evaluation cases pass.
- Permissions and approval behavior have been tested negatively as well as positively.
- Output limits, pagination, timeout, retry, and cancellation behavior are verified.
- Documentation and capability-catalog metadata are current.
- Agent Registry metadata, ownership, lifecycle state, and declared/observed dependencies are current.
- Rollback or disablement is documented.

When requirements conflict with these standards, stop and request a decision or create a proposed ADR. Do not invent an exception.
