# Prompt: Propose Skill Improvements from Traces

```text
You are evaluating an existing skill using execution traces and human feedback.

Skill/version:
<IDENTIFIER>

Trace dataset/evaluation suite:
<REFERENCES>

Read:
- docs/agent-platform/05-SKILL_DESIGN_STANDARD.md
- docs/agent-platform/13-OBSERVABILITY_STANDARD.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

Analyze only data approved for this evaluation. Do not expose sensitive trace content.

Tasks:
1. Group failures and inefficiencies by root cause, not superficial wording.
2. Quantify trigger mistakes, wrong tool selection, unnecessary calls, retries, insufficient evidence, permission/approval failures, unsafe behavior, hallucination, output-contract failures, token use, latency, and cost.
3. Separate skill defects from tool, model, retrieval, gateway, policy, Registry/dependency drift, fixture, or evaluator defects.
4. Propose the smallest changes with an explicit diff and expected effect.
5. Add or modify evaluation cases that reproduce every material issue.
6. Run the complete affected benchmark, not only the failing samples.
7. Report category-level results, hard failures, regressions, variance, and residual risk.

Output a proposal containing:
- Evidence summary
- Root-cause analysis
- Proposed changes and files
- Added/changed tests
- Before/after results
- Risks and rollback
- Human review checklist
- Required Registry version, relationship, or compatibility updates

Do not directly merge, publish, or activate the proposed skill change.
```
