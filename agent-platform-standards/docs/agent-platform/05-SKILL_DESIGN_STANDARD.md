# Skill Design Standard

## 1. Definition

A skill defines **how an agent should perform a reusable job**. It combines instructions, capability requirements, deterministic scripts or queries, reference material, examples, tests, safety constraints, stop conditions, and an output contract.

A skill is not merely a long prompt, an API wrapper, a credential bundle, or a substitute for application code.

## 2. When to create a skill

Create a skill when the workflow:

- Recurs across tasks or users.
- Requires domain-specific procedure or evidence rules.
- Coordinates one or more existing tools, resources, scripts, or Code Mode steps.
- Has meaningful safety constraints, completion criteria, or failure handling.
- Benefits from independent versioning and evaluation.

Do not create a skill for:

- An atomic backend operation; use a tool.
- A one-time answer; use agent reasoning.
- Purely deterministic reusable logic; use a library or script.
- A workflow whose needed capability does not yet exist; specify the capability gap first.

## 3. Required package structure

```text
skills/<skill-name>/
├── SKILL.md
├── scripts/       # optional deterministic helpers
├── queries/       # optional reviewed queries
├── references/    # optional task-relevant reference material
├── examples/      # optional worked examples
└── tests/         # required evaluation and contract cases
```

Do not create empty directories. Add only assets the skill actually uses.

## 4. Required `SKILL.md` content

`SKILL.md` MUST define:

- Name, version, owner, status, and supported domains
- Goal and non-goals
- Trigger conditions and negative triggers
- Required capabilities and minimum contract versions
- Required permissions and approval classes
- Inputs, assumptions, and ambiguity checks
- Ordered workflow and which steps are deterministic
- Evidence requirements and provenance rules
- Safety constraints and prohibited actions
- Stop, escalation, and partial-completion conditions
- Output contract, uncertainty language, and completion criteria
- Referenced scripts, queries, and documents
- Evaluation suite and known limitations
- Registry ID, owner, lifecycle state, agent dependents, and declared capability relationships

Use `templates/SKILL_TEMPLATE.md`.

## 5. Progressive loading

The Capability Catalog SHOULD expose compact metadata projected from approved active Registry entries for all selectable skills. The runtime loads the full `SKILL.md` only after selection. Supporting references, examples, and scripts are loaded only when the selected workflow requires them.

Skill metadata MUST be sufficient to decide:

- When the skill applies
- When it must not be used
- Which permissions and capabilities it needs
- Its risk class, supported environments, and expected cost/latency class

## 6. Workflow design

Each step MUST identify:

- Purpose
- Required input and produced output
- Tool, resource, code, or reasoning mechanism
- Read/write and risk classification
- Evidence captured
- Success, retry, skip, and stop behavior

The workflow SHOULD collect evidence before forming a diagnosis. It MUST NOT prescribe unsupported conclusions before evidence is available.

## 7. Capability references

Skills SHOULD reference stable capability identifiers, not backend URLs or runtime-specific SDK functions. Declare minimum compatible contract versions. A skill MUST NOT assume that discovering a tool means the caller is authorized to execute it.

## 8. Scripts and queries

Bundle deterministic, repeatedly used logic as reviewed scripts or queries when it improves reliability or context efficiency.

Bundled code MUST:

- Have explicit inputs and outputs.
- Respect runtime budgets and sandbox restrictions.
- Avoid embedded credentials or environment-specific secrets.
- Use parameterized queries and safe APIs.
- Produce structured output.
- Have tests and a documented supported-version range.

## 9. Safety

A skill MUST list actions it can never perform. For diagnostic database skills, safe defaults are:

- Read-only evidence collection
- No `KILL`, DDL, DML, login/role change, service restart, failover, restore, or configuration mutation
- Remediation delivered as separately reviewable instructions unless an approved mutation capability is explicitly selected

The skill MUST stop if target, environment, authorization, approval, or evidence identity is ambiguous.

## 10. Evidence and output

The final output SHOULD contain:

1. Finding or conclusion
2. Evidence supporting it
3. Confidence and uncertainty
4. Impact
5. Safe recommendations
6. Explicitly separated proposed commands or changes
7. Validation and rollback guidance when applicable

The output MUST NOT claim that a proposed remediation has been executed.

## 11. Failure handling

Specify behavior for unavailable capabilities, insufficient permission, partial data, stale evidence, timeout, conflicting sources, unsupported backend version, and unsafe requests. Safe partial results MAY be returned when clearly labeled.

## 12. Skill composition

A skill MAY invoke another skill only when the dependency is explicit, version-compatible, bounded, and does not create cycles. Prefer calling underlying capabilities directly when composition adds no reusable procedural value.

## 13. Versioning

- Patch: clarification or compatible implementation fix.
- Minor: backward-compatible workflow or capability addition.
- Major: trigger, safety, output, or behavior change that may alter callers or results.

Record the exact skill version and stable Registry ID in every trace.

## 14. Evaluation

Each skill MUST be evaluated for:

- Correct trigger and rejection behavior
- Correct capability and tool selection
- Evidence sufficiency
- Unnecessary calls and loops
- Permission and approval handling
- Hallucination and unsupported conclusions
- Partial-failure and stop behavior
- Output-contract conformance
- Latency, token, and execution cost

Use the benchmark composition in the Evaluation Standard.

The exact evaluated version and required capability relationships MUST be registered before production activation.

## 15. Continuous improvement

Execution traces MAY be analyzed periodically to propose improvements. Proposals MUST identify evidence, expected benefit, affected cases, risks, and evaluation results. They MUST go through review and MUST NOT be auto-merged.
