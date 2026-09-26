# Tool Specification: `<domain.verb_object>`

## 1. Identity

| Field | Value |
|---|---|
| Capability ID | `<stable namespaced ID>` |
| Registry component ID | `<tool.<stable-name>>` |
| Contract version | `<semver>` |
| MCP server | `<server ID>` |
| Owner | `<team>` |
| Status | `Draft / Review / Active / Deprecated` |

## 2. Purpose

- What it does: `<one precise paragraph>`
- When to use: `<positive triggers>`
- When not to use: `<negative triggers/alternatives>`
- Why an existing tool plus Code Mode is insufficient: `<required for new tool>`

## 3. Classification

| Field | Value |
|---|---|
| Domain | `<domain>` |
| Atomic/domain operation | `<description>` |
| Read/write class | `<R0/R1/R2/W1/W2/W3>` |
| Side effects | `<none or exact effects>` |
| Idempotent | `<yes/no/conditional>` |
| Required permission | `<capability permission>` |
| Approval class | `<none/class>` |

## 4. Supported targets

| Backend | Versions | Environments | Limitations |
|---|---|---|---|
|  |  |  |  |

## 5. Input contract

| Field | Type/format | Required | Default | Validation/max | Security relevance |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Include the authoritative machine-readable schema reference: `<path/ID>`

Target ambiguity behavior: `<fail/candidate response>`

## 6. Output contract

| Field | Type/format | Required | Meaning |
|---|---|---|---|
|  |  |  |  |

- Maximum inline records: `<number>`
- Maximum inline bytes: `<number>`
- Pagination/cursor: `<contract>`
- Result Store threshold: `<rule>`
- Completeness/truncation fields: `<fields>`
- Evidence/provenance fields: `<fields>`
- Example success response: `<fixture reference>`

## 7. Error contract

| Error code | Condition | Retryable | Partial result? | Safe caller action |
|---|---|---|---|---|
|  |  |  |  |  |

Unknown mutation outcome behavior: `<required for writes>`

## 8. Execution behavior

- Timeout: `<duration>`
- Cancellation: `<behavior>`
- Retry: `<errors, attempts, backoff>`
- Concurrency: `<limit>`
- Backend resource limits: `<query/API controls>`
- Cache/freshness: `<policy>`

## 9. Mutation controls

Complete for W1-W3; otherwise write `Not applicable`.

- Exact action preview: `<contract>`
- Approval binding fields: `<list>`
- Idempotency key: `<contract>`
- Preconditions/concurrency: `<contract>`
- Verification: `<method>`
- Rollback/compensation: `<limits>`
- Partial success: `<per-target result>`

## 10. Security and privacy

- Input threat analysis: `<list>`
- Sensitive output fields: `<list>`
- Field-level redaction: `<rules>`
- Tenant/environment isolation: `<rules>`
- Credential handling: `<reference>`
- Prohibited use: `<list>`

## 11. Observability

- Trace attributes: `<list>`
- Metrics: `<list>`
- Audit events: `<list>`
- Prohibited telemetry: `<list>`
- Providing MCP Registry ID: `<ID/version>`
- Backend/gateway/policy/evaluation relationships: `<IDs/versions>`
- Declared/observed relationship reconciliation: `<reference>`

## 12. Examples

### Valid invocation

```json
{}
```

### Invalid or unsafe invocation

```json
{}
```

Expected rejection: `<code/reason>`

## 13. Tests

- [ ] Schema minimum/maximum boundaries
- [ ] Empty and not-found results
- [ ] Pagination/truncation/Result Store
- [ ] Supported backend versions
- [ ] Permission allow and deny
- [ ] Environment and target ambiguity
- [ ] Injection and secret redaction
- [ ] Timeout/cancellation/retry
- [ ] Partial failure
- [ ] Mutation approval/idempotency/preconditions, if applicable
- [ ] Capability discovery positive and negative cases

## 14. Deprecation and rollback

- Replacement: `<capability/version or none>`
- Migration period: `<duration>`
- Disablement/rollback: `<procedure>`

## 15. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Domain owner |  |  |  |
| Architecture |  |  |  |
| Security |  |  |  |
