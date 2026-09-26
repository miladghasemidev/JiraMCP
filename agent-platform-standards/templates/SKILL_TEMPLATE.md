---
name: <kebab-case-skill-name>
version: 0.1.0
owner: <team>
status: draft
registry_id: <skill.stable_name>
description: <selection-focused summary including when this skill should be used>
domains:
  - <domain>
risk_class: <R0/R1/R2/W1/W2/W3>
---

# `<Skill title>`

## Goal

`<One observable reusable job this skill completes.>`

## Non-goals

- `<What this skill does not do>`

## Trigger conditions

Use this skill when:

- `<positive trigger>`

Do not use this skill when:

- `<negative trigger and correct alternative>`

## Supported targets and versions

| Target | Versions/environments | Limitations |
|---|---|---|
|  |  |  |

## Required inputs

| Input | Required | Validation | Ambiguity behavior |
|---|---|---|---|
|  |  |  |  |

## Required capabilities

| Capability ID | Minimum version | Purpose | R/W class | Permission |
|---|---:|---|---|---|
|  |  |  |  |  |

Fallback when unavailable: `<stop, partial result, or named compatible fallback>`

Registry relationship declarations:

| Source registry ID | Relation | Target registry ID | Version constraint | Environment |
|---|---|---|---|---|
| `<this skill>` | `requires/uses/governed_by/evaluated_by` | `<tool/resource/policy/eval>` |  |  |

## Safety constraints

Never:

- `<prohibited action>`

Stop and request a decision when:

- `<ambiguity or risk condition>`

## Evidence requirements

| Claim/decision | Required evidence | Freshness | Provenance requirement |
|---|---|---|---|
|  |  |  |  |

## Workflow

### Step 1 — `<name>`

- Purpose: `<why>`
- Mechanism: `<tool/resource/code/reasoning>`
- Input: `<input>`
- Output: `<output>`
- Evidence captured: `<evidence>`
- On failure: `<retry/stop/partial behavior>`

### Step 2 — `<name>`

- Purpose: `<why>`
- Mechanism: `<tool/resource/code/reasoning>`
- Input: `<input>`
- Output: `<output>`
- Evidence captured: `<evidence>`
- On failure: `<retry/stop/partial behavior>`

## Code Mode usage

- Deterministic operations: `<loops/filtering/aggregation/etc.>`
- Execution budgets: `<calls/time/bytes/concurrency>`
- Result Store output: `<reference and projection>`
- Script/query references: `<paths or none>`

## Approval behavior

- Approval class: `<none/class>`
- Exact action digest fields: `<list>`
- Behavior when missing/expired/changed: `<stop>`

## Completion criteria

- `<observable criterion>`
- `<evidence criterion>`
- `<safety criterion>`

## Partial completion and escalation

- Safe partial output: `<allowed content>`
- Escalation conditions: `<list>`
- Unsupported conditions: `<list>`

## Output contract

1. Finding/outcome
2. Supporting evidence and citations
3. Confidence, uncertainty, and missing evidence
4. Impact
5. Recommendations
6. Proposed commands or changes, clearly marked as not executed
7. Validation/rollback guidance when applicable

Maximum response/projection: `<limits>`

## References and assets

- Scripts: `<paths>`
- Queries: `<paths>`
- References: `<paths>`
- Examples: `<paths>`

## Evaluation

- Suite: `<path/ID>`
- Required thresholds: `<values>`
- Hard-fail conditions: `<list>`
- Known limitations: `<list>`

## Change history

| Version | Date | Change | Evaluated by |
|---:|---|---|---|
| 0.1.0 | `<date>` | Initial draft | `<suite>` |
