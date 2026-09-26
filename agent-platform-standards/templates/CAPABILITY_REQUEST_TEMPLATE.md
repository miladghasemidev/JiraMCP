# Capability Request: `<short title>`

## Document control

| Field | Value |
|---|---|
| Request ID | `<CAP-YYYY-NNN>` |
| Owner | `<name/team>` |
| Status | `Draft / Review / Approved / Rejected / Implemented` |
| Date | `<YYYY-MM-DD>` |
| Related requirement/ticket | `<reference>` |

## 1. User outcome

Describe the outcome in user language. Do not name a tool, skill, MCP server, or implementation yet.

`<required>`

## 2. Example requests

- Positive example: `<request that should be supported>`
- Positive example: `<request that should be supported>`
- Negative example: `<similar request outside scope>`

## 3. Domain and targets

| Item | Value |
|---|---|
| Domain | `<SQL Server / Jira / Oracle / KMS / ...>` |
| Target types | `<instances, issues, documents, ...>` |
| Environments | `<development/test/production>` |
| Supported versions | `<backend versions>` |

## 4. Inputs and decisions

- Required inputs: `<list>`
- Optional inputs: `<list>`
- Decisions that require the user: `<list>`
- Defaults that are safe and approved: `<list>`
- Ambiguities that must stop execution: `<list>`

## 5. Evidence and output

- Evidence required: `<list>`
- Expected output: `<structure>`
- Exact-value requirements: `<IDs, dates, numbers, versions>`
- Maximum acceptable output: `<records/bytes/tokens>`
- Freshness requirement: `<duration>`

## 6. Side effects and risk

| Question | Answer |
|---|---|
| Read-only? | `<yes/no>` |
| Possible side effects | `<none or exact effects>` |
| Risk class | `<R0/R1/R2/W1/W2/W3>` |
| Required permissions | `<list>` |
| Human approval | `<none/class and approver>` |
| Sensitive data | `<classification/fields>` |

## 7. Existing capability search

Record actual search results.

| Existing artifact | Contract/version | Coverage | Gap |
|---|---|---|---|
| `<tool/skill/code/resource>` | `<version>` | `<what it covers>` | `<remaining gap>` |

### Registry and dependency impact

- Registry components inspected: `<stable IDs/versions>`
- Declared relationships inspected: `<references>`
- Observed relationships inspected: `<references/time window>`
- Direct dependents affected: `<list>`
- Transitive dependents affected: `<list/reference>`
- Ownership, lifecycle, compatibility, or unmanaged-component findings: `<list>`

## 8. Decision-tree outcome

- [ ] Reuse existing capability
- [ ] Existing capability plus Code Mode
- [ ] Create ordinary application code/library
- [ ] Create or update MCP tool
- [ ] Create or update skill
- [ ] Agent reasoning only
- [ ] Reject or defer

Decision path: `<node IDs and answers>`

Rationale: `<why this is the smallest correct abstraction>`

## 9. Proposed artifacts

List only artifacts justified by the decision.

- `<artifact and purpose>`

Registry components and relationships to create or update:

- `<component/relationship stable ID, version, owner, lifecycle state, and reason>`

## 10. Acceptance criteria

- `<observable criterion>`
- `<safety/permission criterion>`
- `<failure behavior criterion>`
- `<evaluation threshold>`

## 11. Open decisions

| Decision | Owner | Due date | Blocking? |
|---|---|---|---|
| `<question>` | `<owner>` | `<date>` | `<yes/no>` |

## 12. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Product/domain owner |  |  |  |
| Architecture |  |  |  |
| Security, if applicable |  |  |  |
