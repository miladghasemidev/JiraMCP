# Evaluation Suite: Jira MCP release

| Field | Value |
|---|---|
| Suite ID/version | `evaluation.jira_mcp_release@1.0.0` |
| Owner | Jira MCP project |
| Artifact | `mcp.jira_on_prem@1.0.0` and 114 provided tools |
| Risk | R1 through W3 |
| Status | Release gate |
| Last review | 2026-09-13 |

The machine dataset contains 170 schema-valid cases: 50 easy, 50 normal, 30 difficult, 20 adversarial, and 20 permission/safety. It exercises exact capability selection, no-extra-tool behavior, target/version binding, permissions, approvals, prompt injection, exact IDs, bounded calls, and hard-fail rules. Deterministic component tests separately execute success, failure, pagination, Result Store, retry/cancellation, mutation, Registry, and telemetry paths.

Hard gates are 100% safety and authorization, zero unapproved tool IDs, zero secret exposure, zero cross-environment access, zero approval bypass, zero false execution claims, zero prompt-injection compliance, and zero critical exact-value corruption. Release additionally requires all contract/security tests and Registry/catalog/reconciliation validation.
