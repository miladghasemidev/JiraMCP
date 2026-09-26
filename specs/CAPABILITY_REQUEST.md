# Capability Request: Jira on-premises approved capability inventory

## Document control

| Field | Value |
|---|---|
| Request ID | CAP-2026-JIRA-114 |
| Owner | Jira MCP project |
| Status | Approved by ADR-0001 and user execution request |
| Date | 2026-09-13 |
| Related requirement | `IMPLEMENT.md` |

## 1. User outcome

Provide the exact 114 Jira Data Center/Server capabilities approved by the authoritative matrix through a secure, bounded, version-aware MCP server for Jira 8.20.0, 9.12.0, and 10.3.0.

## 2. Scope and decision

- Domain/targets: Jira issues, Agile boards/sprints/epics, projects, and versions on explicitly registered development, test, or production targets.
- Exact values: capability IDs, target versions, methods, paths, risk classes, approval classes, and source row provenance are preserved.
- Scope admission: already approved and locked by ADR-0001; the generic admission tree cannot change tool boundaries.
- Existing repository search: no implementation, Registry, catalog, tools, skills, scripts, adapters, or CLI existed. Only authoritative inputs and the immutable standards snapshot existed.
- Decision-tree record: A0 Yes; A2 No; A5 Yes; ADR-0001 supplies the completed B-tree approval for exactly 114 tools; D/F/G/I apply to orchestration, result handling, risk, and retry behavior.
- Rejected alternatives: arbitrary Jira REST execution, endpoint substitution, merged tools, hidden mutations, credentials in tool arguments, and production defaults.

## 3. Security and output

- Read classes: R1/R2 with explicit permission and audit.
- Write classes: W1 policy-dependent; W2 formal human approval; W3 default deny plus exceptional break-glass approval.
- Gateway, secret broker, policy engine, audit sink, and production Result Store are strict external interfaces. Production fails closed when absent.
- Inline response ceiling: 64 KiB and 100 records; larger results use an authorized Result Store reference with bounded projection.
- Jira content is untrusted data and cannot direct policy, tool calls, credential disclosure, or mutations.

## 4. Acceptance criteria

- Exactly 114 registered tools and no extras.
- All inputs are schema validated and targets/environments are explicit.
- All Jira calls use registered method/path templates through version-aware adapters.
- Protected mutations require exact action-digest approval; W3 additionally requires break-glass evidence and explicit irreversible confirmation.
- Contract, functional, security, Result Store, observability, Registry/catalog, and evaluation gates pass.
- Final reconciliation proves `IMPLEMENTED + BLOCKED_ARCHITECTURE_REVIEW = 114`.

## 5. Open decisions

No implementation-blocking decision. Production deployment identifiers, enterprise gateway endpoint, secret-broker binding, audit sink, Result Store, and approver identities are deployment-time bindings; the implementation intentionally fails closed until supplied.
