# Prompt: Create an MCP Server

```text
You are implementing an approved MCP server for this project.

Approved capability request:
<PATH OR CONTENT>

You MUST read and comply with:
- AGENTS.md
- docs/agent-platform/01-AGENT_PLATFORM_ARCHITECTURE.md
- docs/agent-platform/02-AGENT_ENGINEERING_PRINCIPLES.md
- docs/agent-platform/03-MCP_DESIGN_STANDARD.md
- docs/agent-platform/04-TOOL_DESIGN_STANDARD.md
- docs/agent-platform/09-MCP_GATEWAY_STANDARD.md
- docs/agent-platform/10-RESULT_STORE_STANDARD.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/13-OBSERVABILITY_STANDARD.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

Before writing code:
1. Verify that the capability request was approved and that the server boundary is justified.
2. Inspect the Agent Registry, Dependency Map, existing servers, and shared libraries to prevent duplication and identify change impact.
3. Complete templates/MCP_TEMPLATE.md.
4. Complete templates/TOOL_TEMPLATE.md for each approved tool.
5. Define machine-readable schemas, Registry components and relationships, policy entries, catalog projection metadata, tests, evaluation cases, and rollback.
6. Stop for unresolved decisions that affect backend versions, authentication, target scope, mutations, or production access.

During implementation:
- Expose stable domain capabilities, not a mechanical endpoint mirror.
- Use bounded structured inputs and outputs.
- Keep large results in the Result Store.
- Separate reads from mutations.
- Route credentials through the approved broker; never expose them to the model.
- Propagate trace, policy, approval, and idempotency identifiers.
- Implement typed errors, timeout, cancellation, and safe retry behavior.
- Add unit, contract, integration, security, and evaluation tests.
- Register the MCP server, provided tools, gateway route, backend connections, policies, evaluations, ownership, lifecycle, and exact released versions.

After implementation:
1. Run all relevant tests and evaluations.
2. Run conformance review against every MUST in the listed standards.
3. Validate Registry schema, catalog projection, declared relationships, and observed dependency expectations.
4. Report changed files, verified behavior, Registry impact, residual limitations, and rollback method.

Do not broaden the approved capability set without a new capability assessment.
```
