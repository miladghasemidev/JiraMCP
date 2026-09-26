# MCP Server Specification: `<server name>`

## Document control

| Field | Value |
|---|---|
| Server ID | `<stable ID>` |
| Registry component ID | `<mcp_server.<stable-name>>` |
| Specification version | `<semver>` |
| Owner | `<team>` |
| Status | `Draft / Review / Approved / Deprecated` |
| Last review | `<YYYY-MM-DD>` |

## 1. Purpose

- Domain: `<domain>`
- User/platform outcomes: `<required>`
- Non-goals: `<required>`
- Why this is one coherent server boundary: `<required>`

## 2. Supported systems

| Backend | Edition/version | Environment | Support level |
|---|---|---|---|
|  |  |  |  |

## 3. Architecture and trust boundaries

- Deployment location: `<zone/runtime>`
- Gateway route: `<route ID>`
- Network dependencies: `<allowlist>`
- Data residency constraints: `<rules>`
- Failure domains: `<list>`

Add a diagram when more than two trust boundaries are involved.

## 4. Authentication

- Gateway/server authentication: `<mechanism>`
- End-user delegation: `<mechanism>`
- Backend identity: `<workload/delegated>`
- Secret broker: `<reference, never secret value>`
- Token lifetime and scope: `<values>`

## 5. Authorization and approval

- Policy namespace: `<ID>`
- Resource attributes: `<list>`
- Deny rules: `<list>`
- Mutation approval classes: `<list>`
- Break-glass handling: `<reference>`

## 6. Capability inventory

| Capability ID | Version | R/W class | Purpose | Max output | Approval |
|---|---:|---|---|---:|---|
|  |  |  |  |  |  |

Attach a completed `TOOL_TEMPLATE.md` for each tool.

Registry relationship declarations:

| Source registry ID | Relation | Target registry ID | Version constraint | Environment |
|---|---|---|---|---|
| `<mcp server>` | `provides/connects_to/routes_through/governed_by/evaluated_by` | `<tool/backend/gateway/policy/eval>` |  |  |

## 7. Resources and reference content

| Resource ID | Version | Purpose | Access rule | Size/retention |
|---|---:|---|---|---|
|  |  |  |  |  |

## 8. Contract conventions

- Schema format/version: `<reference>`
- Result envelope: `<reference>`
- Error envelope: `<reference>`
- Identifier semantics: `<rules>`
- Timezone/units/encoding: `<rules>`
- Compatibility and deprecation: `<policy>`

## 9. Limits and Result Store

| Limit | Default | Hard maximum | Enforcement point |
|---|---:|---:|---|
| Request bytes |  |  |  |
| Response bytes |  |  |  |
| Page size |  |  |  |
| Execution time |  |  |  |
| Concurrent calls |  |  |  |

Result Store threshold and projection policy: `<required>`

## 10. Reliability

- Timeout: `<per capability>`
- Retry policy: `<typed errors and attempts>`
- Cancellation: `<behavior>`
- Circuit breaker: `<behavior>`
- Async operations: `<status/cancel contract>`
- Partial failure: `<behavior>`
- Unknown mutation outcome: `<behavior>`

## 11. Error mapping

| Backend condition | Platform error code | Retryable | Safe message |
|---|---|---|---|
|  |  |  |  |

## 12. Observability and audit

- Trace fields: `<list/reference>`
- Metrics and SLOs: `<list>`
- Security audit events: `<list>`
- Redacted/prohibited fields: `<list>`
- Dashboard and alert owner: `<team>`

## 13. Security analysis

- Threats: `<list>`
- Input validation: `<controls>`
- Injection controls: `<controls>`
- Tenant/environment isolation: `<controls>`
- Credential handling: `<controls>`
- Emergency disablement: `<procedure>`

## 14. Test and evaluation plan

- Contract tests: `<list>`
- Backend integration matrix: `<list>`
- Authorization and approval tests: `<list>`
- Limits/reliability tests: `<list>`
- Security/adversarial tests: `<list>`
- Workflow eval suites: `<references>`

## 15. Deployment and operations

- Configuration: `<non-secret settings>`
- Health/readiness: `<endpoints/semantics>`
- Rollout/canary: `<plan>`
- Rollback: `<plan>`
- On-call owner/runbook: `<reference>`
- Registry lifecycle and review date: `<state/date>`
- Declared/observed dependency reconciliation: `<process/dashboard>`

## 16. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Domain owner |  |  |  |
| Architecture |  |  |  |
| Security |  |  |  |
| Operations |  |  |  |
