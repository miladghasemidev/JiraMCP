# Prompt: Create a Skill

```text
You are creating an approved reusable skill for this agent-platform project.

Approved capability request:
<PATH OR CONTENT>

You MUST read and comply with:
- AGENTS.md
- docs/agent-platform/05-SKILL_DESIGN_STANDARD.md
- docs/agent-platform/06-CODE_MODE_STANDARD.md
- docs/agent-platform/07-CAPABILITY_DISCOVERY_STANDARD.md
- docs/agent-platform/11-CONTEXT_MANAGEMENT_STANDARD.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

First:
1. Confirm that this is a recurring procedure, not an atomic tool, ordinary deterministic library, or one-time answer.
2. Inspect the Agent Registry, Dependency Map, existing skills, and capabilities; document reuse and affected dependents.
3. Complete templates/SKILL_TEMPLATE.md.
4. Verify that every required capability exists at a compatible version and is separately authorized.

Create only needed package contents:
skills/<name>/SKILL.md
skills/<name>/scripts/      when deterministic reusable logic is needed
skills/<name>/queries/      when reviewed parameterized queries are needed
skills/<name>/references/   when routed reference material is needed
skills/<name>/examples/     when examples improve reliable use
skills/<name>/tests/        always

Requirements:
- Define precise positive and negative triggers.
- Encode an evidence-first workflow, safety constraints, prohibited actions, stop behavior, and completion criteria.
- Use Code Mode for deterministic loops, filtering, joining, polling, and aggregation.
- Keep raw large results outside model context.
- State permissions and approval classes but never embed credentials or grant authority.
- Separate proposed commands or remediation from executed actions.
- Load supporting resources progressively.
- Add positive, negative, difficult, adversarial, permission, and safety evaluation cases.
- Register the exact Skill version, owner, lifecycle, required capability versions, policies, evaluation suite, supported targets, and agent dependents.

After creation, validate Registry relationships and catalog projection, run the evaluation suite, and report trigger quality, tool selection, evidence coverage, safety, unnecessary calls, output conformance, latency, and cost. Do not auto-merge improvement proposals.
```
