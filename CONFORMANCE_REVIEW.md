# Independent conformance review

Review date: 2026-09-13. Review basis: the complete pinned standards snapshot, `prompts/REVIEW_MCP.md`, `prompts/REVIEW_TOOL.md`, the approved matrix, generated specifications, implementation, Registry/catalog, tests, and evaluation evidence. This pass reviewed conformance of the locked inventory; it did not reopen capability admission.

## Outcome

All code- and repository-correctable findings were fixed and re-tested. The 114 approved capabilities are implemented without additions, omissions, merges, splits, renames, substitutions, or a generic REST escape hatch. One production-release dependency finding remains open because the repository intentionally does not contain enterprise infrastructure or live Jira targets. That finding does not change capability implementation status, but it blocks a production `RELEASE_READY` decision.

## Findings and dispositions

### CR-001 — Resolved — P1 — Failure envelope violated the standard schema

- Evidence before fix: `ToolResult.wire()` serialized success-only `provenance`, `warnings`, and `errors` fields on failed results, conflicting with `agent-platform-standards/schemas/tool-result.schema.json` failure `additionalProperties: false`.
- Violated requirement: standard result/error contracts must conform to the vendored schema.
- Impact: strict clients could reject otherwise typed failures.
- Smallest corrective action: emit only the six failure-envelope fields permitted by the standard.
- Resolution evidence: `src/jira_mcp/models.py:87`; `tests/test_inventory_contracts.py::test_standard_result_model_emits_schema_valid_success_and_failure`.

### CR-002 — Resolved — P1 — Trace identity stopped at the MCP boundary

- Evidence before fix: the validated trace ID was present in results and audit events but absent from Jira request headers.
- Violated requirement: trace and correlation identifiers must propagate through the backend adapter.
- Impact: Jira-side requests could not be correlated with gateway, MCP, Result Store, and audit records.
- Smallest corrective action: set adapter-controlled `X-Correlation-ID` and optional `X-Request-ID`; do not accept arbitrary caller headers.
- Resolution evidence: `src/jira_mcp/adapters.py:90`; `tests/test_all_capabilities.py:30` exercises the header for all 114 capabilities.

### CR-003 — Resolved — P2 — Per-target concurrency did not match the specification

- Evidence before fix: the executor enforced only the global semaphore while tool specifications documented a four-call per-target bound.
- Violated requirement: implementation and declared operational limits must agree.
- Impact: one Jira target could consume all global capacity and overload its own backend pool.
- Smallest corrective action: add a validated per-target limit and a semaphore keyed by environment and target ID.
- Resolution evidence: `src/jira_mcp/config.py:26`, `src/jira_mcp/executor.py:106`, `deployment/config.example.json`.

### CR-004 — Resolved — P1 — Test fakes could be accidentally injected for production

- Evidence before fix: interfaces failed closed in the default factory, but an alternate composition could bind in-memory policy, approval, secret, Result Store, or audit fakes to a production target.
- Violated requirement: required external enterprise controls must fail closed in production.
- Impact: a composition mistake could bypass the intended enterprise trust boundary.
- Smallest corrective action: declare production readiness on each strict integration boundary and reject production dispatch unless every required control attests readiness.
- Resolution evidence: `src/jira_mcp/executor.py:163`; `src/jira_mcp/security.py:85`; `src/jira_mcp/result_store.py:15`; `src/jira_mcp/observability.py:13`; `tests/test_config_and_observability.py::test_test_fakes_cannot_be_used_for_a_production_target`.

### CR-005 — Resolved — P1 — Delivery-control failure could create a false mutation outcome

- Evidence before fix: if Result Store or audit delivery failed after Jira completed a mutation, the generic exception path could report an undifferentiated failed call.
- Violated requirement: no false execution claims; unknown or partial post-dispatch outcomes must be explicit and must not encourage blind retry.
- Impact: a caller could repeat a mutation that Jira had already completed.
- Smallest corrective action: preserve the completed mutation as `partial`, remove unavailable oversized data, emit a typed warning, and retain idempotency state.
- Resolution evidence: `src/jira_mcp/executor.py:136`, `src/jira_mcp/executor.py:271`; `tests/test_functional_behavior.py::test_mutation_reports_partial_when_oversized_result_cannot_be_stored`.

### CR-006 — Resolved — P2 — Capability Catalog IDs were not schema-conformant

- Evidence before fix: the approved underscore MCP names do not match the standards schema’s required dotted catalog namespace.
- Violated requirement: Capability Catalog entries must validate while approved MCP tool names remain unchanged.
- Impact: Registry/catalog validation failed or risked an unauthorized tool rename.
- Smallest corrective action: retain each exact matrix name as the MCP tool and Registry metadata capability ID, while projecting a deterministic `jira.<category>_<operation>` catalog ID.
- Resolution evidence: `tools/generate_specs.py::catalog`; `tests/test_registry_and_evals.py::test_catalog_schema_and_no_extra_capabilities`.

### CR-007 — Open production gate — P1 — Enterprise bindings and live Jira evidence are absent

- Evidence: `runbooks/OPERATIONS.md` records that no real Jira target, production credential, enterprise gateway/policy/approval services, production Result Store, or audit sink is included. Automated tests use mocked Jira backends and do not perform production mutations.
- Requirement: production release requires registered deployment targets, least-privilege credentials, functioning mandatory controls, operational telemetry, and evidence for each supported Jira version.
- Impact: the repository can be built and tested, but cannot safely be activated against production Jira or claim live compatibility.
- Smallest corrective action: supply reviewed implementations with `production_ready = true`, register non-production Jira 8.20.0, 9.12.0, and 10.3.0 targets, run read and controlled mutation conformance suites with least-privilege accounts, verify dashboards/alerts/audit retention, then repeat the final release audit.
- Disposition: not correctable from repository contents without external infrastructure, credentials, and separately authorized mutation testing. Production remains fail closed.

## Verification after fixes

- Ruff: pass.
- Mypy strict mode: pass for all 15 source modules.
- Pytest: 157 passed.
- Deterministic release evaluation: 170/170 passed; zero hard failures.
- Full-inventory MCP/adapter dispatch: 114/114 exercised.
- Vendored standards checksum: 48/48 entries unchanged.
