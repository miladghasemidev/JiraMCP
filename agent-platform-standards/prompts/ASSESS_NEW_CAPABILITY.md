# Prompt: Assess a New Capability

Use this prompt before implementation.

```text
You are the architecture reviewer for this agent-platform project.

Requested outcome:
<INSERT USER OUTCOME AND CONSTRAINTS>

You MUST read and comply with:
- AGENTS.md
- docs/agent-platform/01-AGENT_PLATFORM_ARCHITECTURE.md
- docs/agent-platform/02-AGENT_ENGINEERING_PRINCIPLES.md
- docs/agent-platform/15-DECISION_TREES.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

Then inspect the existing repository and capability catalog.

Tasks:
1. Restate the requested user outcome without assuming an implementation.
2. List missing decisions only when they materially change architecture, scope, permission, or side effects.
3. Search the Agent Registry, declared and observed Dependency Map, Capability Catalog, and repository for reusable agents, MCP servers, tools, skills, models, runtimes, scripts, queries, resources, and ordinary application code.
4. Walk the decision tree explicitly and record node IDs and answers.
5. Choose the smallest correct result: reuse, existing capability plus Code Mode, ordinary code, new/update tool, new/update skill, agent reasoning, or reject/defer.
6. Identify security class, permissions, approvals, output bounds, evidence needs, and failure/stop behavior.
7. Inspect ownership, lifecycle, version compatibility, permissions, and direct/transitive change impact for affected Registry components.
8. Complete templates/CAPABILITY_REQUEST_TEMPLATE.md.
9. List only the artifacts and Registry relationships justified by the decision.

Do not implement anything during this assessment.
Do not create one tool per backend endpoint.
Do not treat a plan as authorization.
Do not invent backend support, permissions, or unresolved product decisions.

Return:
- The completed capability request file
- A concise decision summary
- Blocking questions, if any
```
