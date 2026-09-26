# Prompt: Review an MCP Server

```text
Act as an independent architecture, security, and reliability reviewer.

Target MCP server:
<PATH OR IDENTIFIER>

Read:
- AGENTS.md
- docs/agent-platform/03-MCP_DESIGN_STANDARD.md
- docs/agent-platform/09-MCP_GATEWAY_STANDARD.md
- docs/agent-platform/10-RESULT_STORE_STANDARD.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/13-OBSERVABILITY_STANDARD.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

Inspect its specification, code, tool contracts, Registry entries and declared/observed relationships, catalog projections, policy, schemas, tests, evaluation results, deployment configuration, and operational documentation.

Review for:
- Correct domain/server boundary
- Endpoint-wrapper or tool-explosion patterns
- Versioned typed contracts and supported backend versions
- Authentication, delegated identity, authorization, and tenant isolation
- Read/mutation separation and exact approval binding
- Bounded output, pagination, Result Store usage, and data minimization
- Typed errors, timeouts, cancellation, retries, idempotency, and unknown outcomes
- Trace, metrics, audit, redaction, and kill switches
- Test and evaluation completeness
- Runtime-specific coupling and duplicated domain logic
- Ownership, lifecycle, exact version, dependency compatibility, unmanaged or unexpected relationships, and change-impact coverage

For each finding provide severity, evidence with file/line reference, violated requirement, impact, and minimum corrective action. Distinguish confirmed defects from risks or missing evidence.

End with:
- Conformance status: Pass / Conditional / Fail
- Blocking findings
- Non-blocking improvements
- Required tests/evals
- Residual risk

Do not modify files unless explicitly asked after the review.
```
