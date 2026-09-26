# Agent Registration: `<agent name>`

## 1. Registry identity

| Field | Value |
|---|---|
| Registry ID | `<agent.<stable-name>>` |
| Agent version | `<semver>` |
| Lifecycle status | `draft / review / approved / active / deprecated / disabled / retired / unmanaged` |
| Owner team | `<team>` |
| Technical contact | `<contact>` |
| Backup owner/team | `<owner>` |
| Created/updated | `<UTC timestamps>` |
| Next review date | `<YYYY-MM-DD>` |

## 2. Purpose and selection

- Purpose: `<approved business or operational outcome>`
- Non-goals: `<list>`
- Positive selection cues: `<list>`
- Negative selection cues: `<list>`
- Intended users/audiences: `<list>`
- Supported channels: `<web/API/CLI/Telegram/etc.>`

## 3. Deployment

| Environment | Deployment ID | Runtime | Endpoint | Region/zone | Status |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

- Source repository: `<reference>`
- Immutable artifact/release: `<digest/tag/commit>`
- Configuration manifest: `<reference; no secrets>`
- Disablement/rollback: `<procedure>`

## 4. Runtime and model

| Dependency | Registry ID/version | Purpose | Required? | Fallback |
|---|---|---|---|---|
| Runtime |  |  |  |  |
| Primary model |  |  |  |  |
| Fallback model |  |  |  |  |

- Autonomy level: `<workflow / supervised agent / bounded autonomous agent>`
- Maximum steps/calls/time/cost: `<budgets>`
- Stop and escalation conditions: `<list>`

## 5. Skills and capabilities

| Relationship | Registry ID/version range | Purpose | Environment/target scope | R/W class |
|---|---|---|---|---|
| requires skill |  |  |  |  |
| invokes tool |  |  |  |  |
| uses resource |  |  |  |  |
| routes through gateway |  |  |  |  |

## 6. Data and memory

| Relationship | Registry ID | Access | Classification | Retention/purpose |
|---|---|---|---|---|
| reads from KMS |  |  |  |  |
| uses memory |  |  |  |  |
| writes Result Store |  |  |  |  |
| reads/writes backend |  |  |  |  |

## 7. Security and approval

- Risk class: `<R0/R1/R2/W1/W2/W3>`
- Required permissions: `<list>`
- Explicitly denied actions: `<list>`
- Policy bindings: `<registry IDs/versions>`
- Approval classes: `<list>`
- Credential mechanism: `<broker/delegation reference; no secret>`
- Tenant/environment isolation: `<controls>`
- Data classifications permitted: `<list>`

## 8. Declared relationships

| Source ID | Relation | Target ID | Version constraint | Required? | Environment | Evidence |
|---|---|---|---|---|---|---|
|  | `uses/requires/provides/invokes/routes_through/connects_to/reads_from/writes_to/runs_on/governed_by/evaluated_by/depends_on/replaces` |  |  |  |  |  |

## 9. Observability and evaluation

- Trace/dashboard references: `<list>`
- Audit event classes: `<list>`
- Evaluation suite/version: `<registry ID/version>`
- Last evaluation result/date: `<result/date>`
- Release thresholds: `<reference>`
- Known risks or exceptions: `<ADR/risk references>`

## 10. Change impact

- Direct dependents: `<generated list/reference>`
- Transitive impact report: `<reference>`
- Compatibility/migration notes: `<list>`
- Last observed use: `<timestamp/source>`

## 11. Registration validation

- [ ] Stable unique ID and exact version
- [ ] Owner and backup owner/team assigned
- [ ] Environment and deployment instances explicit
- [ ] Runtime/model/tool/skill/gateway relationships declared
- [ ] Data access, permissions, policies, and approvals linked
- [ ] Evaluation and observability linked
- [ ] No secrets stored
- [ ] Schema validation passed
- [ ] Security and architecture review passed
- [ ] Disablement or rollback documented

## 12. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Product/domain owner |  |  |  |
| Architecture |  |  |  |
| Security |  |  |  |
| Operations |  |  |  |

