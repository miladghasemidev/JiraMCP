# ADR 0002: Separate Scope Authority from Implementation Authority

- Status: Accepted
- Date: 2026-09-08
- Owners: Jira MCP project
- Review date or expiry: None
- Supersedes/superseded by: None

## Context

The Jira project has a domain-specific approved capability matrix and a reusable enterprise agent-platform standards repository. They serve different purposes and must not be treated as competing sources of truth.

## Decision drivers

- Make precedence unambiguous for human developers and coding agents.
- Preserve the reusable standards package unchanged.
- Prevent Jira-specific scope choices from weakening security or engineering requirements.

## Decision

The authoritative Jira capability matrix controls **what capabilities are in scope**.

The pinned `agent-platform-standards` snapshot controls **how those capabilities are designed, implemented, secured, tested, evaluated, governed, reviewed, and released**.

A matrix row does not waive security, approval, least-privilege, bounded-output, observability, Registry, or evaluation requirements.

If a scope requirement and a mandatory safety/security requirement cannot both be satisfied, implementation must stop for architecture/security review. The coding agent must not invent an exception.

Future capabilities not already present in the approved matrix must follow the full generic capability-assessment and decision-tree workflow before they may be added.

## Consequences

### Positive

- The reusable standards repository remains reusable across domains.
- Jira scope decisions remain stable.
- Safety requirements cannot be silently weakened by a capability row.

### Negative or tradeoffs

- Genuine conflicts require explicit review rather than automatic resolution.

## Validation

- Every implemented Jira tool maps to one approved matrix row.
- Every tool passes applicable MUST/MUST NOT requirements or has an accepted explicit ADR exception.
- No future capability is added solely because a backend endpoint exists.

## Rollback or reversal

Replace this ADR only through a reviewed architecture decision that explicitly defines new precedence rules.

## Standard exceptions

None beyond the project-specific scope-lock interpretation documented in ADR 0001.
