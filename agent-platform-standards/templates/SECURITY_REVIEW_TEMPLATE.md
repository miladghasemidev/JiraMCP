# Security Review: `<capability or component>`

## 1. Scope

- Artifact/version: `<ID/version>`
- Owner: `<team>`
- Environments: `<list>`
- Data classifications: `<list>`
- Read/write class: `<R0-R2/W1-W3>`

## 2. Identities and trust boundaries

| Boundary | Caller identity | Target identity | Authentication | Delegation |
|---|---|---|---|---|
|  |  |  |  |  |

## 3. Permissions

- Minimum required permissions: `<list>`
- Explicitly denied permissions: `<list>`
- Resource/parameter constraints: `<list>`
- Tenant/environment isolation: `<controls>`

## 4. Approval

- Approval class: `<none/class>`
- Action-digest fields: `<list>`
- Expiry/max uses: `<values>`
- Separation of duties: `<rule>`
- Replay/change prevention: `<control>`

## 5. Data flow

- Inputs and sources: `<list>`
- Outputs and destinations: `<list>`
- Model-context projection: `<fields/limits>`
- Result Store retention/access: `<rules>`
- Logs/traces/audit: `<fields and redaction>`

## 6. Threat checklist

- [ ] Prompt injection and untrusted content
- [ ] Excessive agency/confused deputy
- [ ] Secret exposure
- [ ] Unauthorized mutation
- [ ] Cross-tenant/environment access
- [ ] SQL/shell/path/URL/template injection
- [ ] Replay/idempotency/unknown outcome
- [ ] Result-reference access
- [ ] Supply-chain risk
- [ ] Denial of service/cost exhaustion

For each applicable threat, record attack path, control, residual risk, owner, and test.

## 7. Failure behavior

- Ambiguous target: `<behavior>`
- Policy dependency unavailable: `<fail-closed behavior>`
- Approval unavailable/expired: `<behavior>`
- Secret broker unavailable: `<behavior>`
- Partial failure: `<behavior>`
- Unknown mutation outcome: `<behavior>`

## 8. Verification

| Test | Expected result | Evidence |
|---|---|---|
|  |  |  |

## 9. Decision

- Decision: `Approved / Approved with conditions / Rejected`
- Conditions: `<list>`
- Reviewer/date: `<name/date>`
- Re-review trigger/date: `<value>`

