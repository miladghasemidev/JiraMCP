# Prompt: Create a Tool

```text
You are implementing an approved MCP tool for this agent-platform project.

Approved capability request:
<PATH OR CONTENT>

You MUST read and comply with:
- AGENTS.md
- docs/agent-platform/04-TOOL_DESIGN_STANDARD.md
- docs/agent-platform/09-MCP_GATEWAY_STANDARD.md
- docs/agent-platform/10-RESULT_STORE_STANDARD.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/13-OBSERVABILITY_STANDARD.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

First:
1. Reconfirm from the decision record that this should be a tool rather than reuse, Code Mode, ordinary code, a skill, or agent reasoning.
2. Search the Agent Registry, Dependency Map, and Capability Catalog for semantic overlap, version conflicts, and affected dependents.
3. Complete templates/TOOL_TEMPLATE.md and resolve every blocking field.

Implementation requirements:
- Use a stable namespaced capability ID and versioned typed schemas.
- Validate every input, including target and environment.
- Define hard output, row, byte, time, call, and concurrency limits.
- Preserve completeness, truncation, pagination, provenance, and collection time.
- Store large output and return an authorized reference plus bounded projection.
- Return typed error envelopes.
- Separate read and mutation operations.
- For mutations, enforce approval binding, idempotency, preconditions, partial results, and verification.
- Never accept credentials through tool inputs.
- Emit required trace, metrics, and audit events without sensitive payloads.
- Register the exact Tool version and its providing MCP, gateway, backend, policy, evaluation, owner, lifecycle, and compatibility relationships.

Tests must cover normal, empty, boundary, incompatible version, permission denial, ambiguous target, malicious input, oversized output, timeout, cancellation, partial failure, and mutation-specific safety cases.

Return the specification, implementation, Registry entry and relationships, catalog projection entry, schemas, tests, evaluation changes, impact analysis, and a conformance report. Do not implement unrelated tools.
```
