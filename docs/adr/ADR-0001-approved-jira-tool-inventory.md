# ADR 0001: Lock the Approved Jira MCP Tool Inventory

- Status: Accepted
- Date: 2026-09-08
- Owners: Jira MCP project
- Review date or expiry: None
- Supersedes/superseded by: None

## Context

The Jira MCP capability analysis has already classified the implementable Jira on-premises capabilities. The approved project matrix contains exactly 114 MCP tools.

The general enterprise platform standards intentionally discourage mechanical one-tool-per-endpoint designs and require an admission decision for new tools. Re-running that generic admission step against an already-approved project inventory could change the approved Jira scope by merging, removing, splitting, or substituting capabilities.

## Decision drivers

- Preserve the exact capability scope already reviewed for Jira.
- Apply the enterprise engineering standard without silently reopening product scope.
- Keep a deterministic, auditable relationship between the approved matrix and implementation.
- Prevent coding agents from optimizing away approved capabilities.

## Decision

The real file matching `project-inputs/APPROVED_JIRA_CAPABILITY_MATRIX.*` is the authoritative capability inventory for this Jira MCP project.

Exactly 114 approved tool rows are in scope.

For these 114 capabilities, the design-time Tool Admission/classification decision is considered already completed and approved. The generic decision tree must not be used to change the number or boundaries of approved tools.

The platform standards remain fully applicable to how every approved tool is specified and implemented, including contracts, security, bounded output, Result Store behavior, errors, reliability, observability, Registry metadata, dependencies, testing, evaluation, and release gates.

No approved tool may be added, removed, merged, split, renamed, or substituted unless a later approved scope decision explicitly changes the matrix.

If technical evidence demonstrates that an approved capability is not implementable for the exact approved Jira product/version range, the capability remains in the inventory with status `BLOCKED_ARCHITECTURE_REVIEW`. It must not be silently replaced.

## Consequences

### Positive

- Scope remains stable and auditable.
- The standards govern engineering quality without redefining the approved product inventory.
- Final accounting can prove that all 114 capabilities were handled.

### Negative or tradeoffs

- Some tool boundaries may differ from what a greenfield application of the generic admission tree would choose.
- A technically blocked capability requires explicit architecture review rather than an automatic substitution.

## Risks and compensating controls

| Risk | Control | Owner | Review date |
|---|---|---|---|
| Approved inventory contains a weak boundary | Apply all contract/security/testing standards and record a future scope-change proposal separately | Jira MCP project | As needed |
| Backend version does not actually support a capability | Require concrete technical evidence and `BLOCKED_ARCHITECTURE_REVIEW` | Jira MCP project | During implementation |
| Coding agent invents missing matrix content | Hard-stop when the real 114-row matrix is absent or does not validate | Jira MCP project | Every implementation run |

## Implementation and migration

- Parse the approved matrix into a machine-readable internal inventory without changing its semantics.
- Maintain one implementation status per approved capability.
- Produce a final reconciliation report against the original matrix.

## Validation

- Approved distinct tool count equals 114 before implementation.
- Final `IMPLEMENTED + BLOCKED_ARCHITECTURE_REVIEW` equals 114.
- No extra MCP tools exist outside the approved inventory.

## Rollback or reversal

A change to the approved capability inventory requires a new reviewed project decision and an updated authoritative matrix.

## Standard exceptions

The only project-specific interpretation is that the generic new-tool admission/classification gate is not rerun to alter the already-approved 114-tool inventory. All implementation, security, reliability, observability, Registry, testing, evaluation, and release requirements remain in force.
