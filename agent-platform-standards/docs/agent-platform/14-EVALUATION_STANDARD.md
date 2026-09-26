# Evaluation Standard

## 1. Purpose

Agent evaluation measures both the final outcome and the workflow used to reach it. A correct-looking answer is insufficient if the agent selected the wrong capability, leaked data, ignored permissions, made unnecessary calls, or performed unsafe state changes.

## 2. Evaluation layers

| Layer | What it tests |
|---|---|
| Contract tests | Schemas, types, limits, errors, versioning |
| Component tests | Tool, skill, retriever, gateway, Result Store behavior |
| Workflow tests | Multi-step planning, execution, state, recovery |
| Trace grading | Selection, calls, evidence, permissions, efficiency |
| Outcome grading | Correctness, completeness, clarity, citations |
| Security tests | Injection, privilege, leakage, approval, tenancy |
| Operational tests | Latency, concurrency, outage, cancellation, cost |
| Registry/topology tests | Registration, ownership, lifecycle, compatibility, declared/observed dependency drift |

## 3. Minimum skill dataset

For a production-critical skill, the baseline SHOULD contain at least:

- 50 easy cases
- 50 normal cases
- 30 difficult cases
- 20 adversarial cases
- 20 permission or safety cases

A smaller pilot suite MAY be used before production, but the risk owner MUST document the gap and completion date.

## 4. Case structure

Each case MUST define:

- Stable case ID, version, category, and risk level
- Input conversation and environment fixtures
- Available and forbidden capabilities
- User permissions and approval state
- Backend/tool fixtures and injected failures
- Expected decisions, calls, evidence, and state changes
- Allowed variation
- Forbidden behavior and hard-fail conditions
- Expected output facts and uncertainty
- Token, call, latency, and cost budgets

Use `templates/EVAL_TEMPLATE.md` and `schemas/eval-case.schema.json`.

## 5. Trace grading dimensions

Grade whether the run:

- Selected the correct skill or correctly used none
- Selected the minimum sufficient tools
- Avoided unnecessary, duplicate, or overly broad calls
- Used Code Mode for deterministic repetition
- Respected target, permission, approval, and data boundaries
- Retrieved sufficient and relevant evidence
- Preserved provenance and exact values
- Distinguished evidence, inference, and uncertainty
- Handled partial failure, retries, cancellation, and stopping correctly
- Kept raw large data out of context
- Produced the required structured output
- Used only approved registered component versions and produced expected dependency observations

## 6. Hard-fail conditions

Regardless of aggregate score, a run fails if it:

- Performs or attempts an unauthorized mutation
- Bypasses a required approval or gateway control
- Exposes credentials or prohibited sensitive data
- Crosses a tenant or environment boundary
- Invokes an unmanaged, disabled, retired, or explicitly forbidden component
- Fabricates evidence or claims execution that did not occur
- Silently selects an ambiguous destructive target
- Follows prompt injection from untrusted content
- Loses or alters an exact critical identifier in a strict-accuracy task

## 7. Scoring

Use weighted dimensions appropriate to the capability. Safety and authorization MUST be gating dimensions, not small weighted deductions. Report both average score and worst-case failures. Do not hide category regressions behind an improved overall mean.

## 8. Ground truth

Ground truth SHOULD combine deterministic assertions, approved expected traces, backend fixture state, and expert review. Model-based graders MAY assist but MUST be calibrated against human-labeled cases and must not be the sole authority for security gates.

## 9. Regression gate

Any change to a skill, tool, model, prompt, retrieval strategy, capability catalog, gateway, policy, or Code Mode runtime MUST run the affected benchmark. Release requires:

- No new hard failures
- No security or permission regression
- Contract tests passing
- Accuracy and trace quality at or above the approved threshold
- Latency and cost within budget
- Documented review of newly failing or changed cases
- Updated Registry entries, dependency impact analysis, and compatibility checks for affected components

## 10. Counterfactual and negative tests

Include cases where:

- No tool should be called
- An existing tool must be reused instead of creating another
- The requested target is ambiguous
- Evidence is missing or contradictory
- The user lacks permission
- Approval expires or parameters change
- A backend times out after a mutation with unknown outcome
- Retrieved content contains malicious instructions
- A large dataset must remain in the Result Store

## 11. Retrieval evaluation

Measure permission-filter correctness, recall, precision, reranking quality, citation accuracy, exact-token recall, freshness, duplication, and whether retrieval changes the answer appropriately.

## 12. Production evaluation

Sample production traces according to privacy policy. Track drift, new intents, failure clusters, unnecessary calls, user corrections, escalations, cost, latency, and security signals. Do not add sensitive production content to a training or evaluation set without governance approval.

## 13. Skill self-improvement

Periodically aggregate:

- Task and selected skill
- Tool calls, errors, retries, and stop behavior
- Token, latency, and cost measures
- Final outcome and human feedback
- Evaluator findings

An improvement proposal MUST include affected version, evidence, change diff, expected gain, risk analysis, and benchmark results. It requires review and MUST NOT auto-merge.

## 14. Reporting

Evaluation reports MUST show dataset version, runtime/model/tool/skill/policy versions, environment, pass rate by category, hard failures, confidence interval or run variability where relevant, latency/cost, regressions, and release decision.

## 15. Ownership

Every suite MUST have an owner, review cadence, and retirement policy. Failed safety cases require security ownership; they cannot be waived only by the feature implementer.

Evaluation suites and their supported component versions SHOULD themselves be registered so the platform can determine whether an active agent, skill, tool, or model is covered by a current approved evaluation baseline.
