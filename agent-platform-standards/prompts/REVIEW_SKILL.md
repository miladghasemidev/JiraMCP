# Prompt: Review a Skill

```text
Act as an independent skill and agent-workflow reviewer.

Target skill:
<PATH OR SKILL ID>

Read:
- docs/agent-platform/05-SKILL_DESIGN_STANDARD.md
- docs/agent-platform/06-CODE_MODE_STANDARD.md
- docs/agent-platform/07-CAPABILITY_DISCOVERY_STANDARD.md
- docs/agent-platform/11-CONTEXT_MANAGEMENT_STANDARD.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

Inspect the complete SKILL.md and every referenced script, query, reference, example, and test actually required by it.

Review:
- Correct abstraction and reuse of existing capabilities
- Positive and negative trigger precision
- Compatible capability/version declarations
- Evidence-first workflow and provenance
- Deterministic work moved to Code Mode
- Safety constraints, prohibited actions, ambiguity stops, and escalation
- Permission and approval handling
- Context size and progressive loading
- Output contract, uncertainty, and execution-claim accuracy
- Failure and partial-completion behavior
- Test composition and trace-grade coverage
- Registry identity, owner, lifecycle, version, required capability relationships, agent dependents, and declared/observed drift

Identify unused assets, missing referenced assets, duplicated tool logic, long-prompt behavior that should be code/reference material, and any implied authorization.

For each finding provide severity, evidence, violated rule, impact, and minimum fix. End with Pass / Conditional / Fail and required evaluation cases. Do not modify files unless explicitly asked.
```
