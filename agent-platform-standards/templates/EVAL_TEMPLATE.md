# Evaluation Suite: `<name>`

## 1. Suite control

| Field | Value |
|---|---|
| Suite ID/version | `<stable ID/version>` |
| Owner | `<team>` |
| Artifact under test | `<skill/tool/model/prompt/gateway>` |
| Risk class | `<class>` |
| Status | `Draft / Baseline / Release gate / Retired` |
| Last review | `<YYYY-MM-DD>` |

## 2. Purpose and scope

- Behaviors evaluated: `<list>`
- Behaviors not evaluated: `<list>`
- Supported environments/versions: `<list>`

## 3. Dataset composition

| Category | Target count | Actual count | Notes |
|---|---:|---:|---|
| Easy | 50 |  |  |
| Normal | 50 |  |  |
| Difficult | 30 |  |  |
| Adversarial | 20 |  |  |
| Permission/safety | 20 |  |  |

## 4. Case template

### `<CASE-ID>: <title>`

- Category/risk: `<values>`
- Input conversation: `<fixture>`
- User/tenant/environment: `<fixture>`
- Available capabilities: `<allowlist>`
- Forbidden capabilities: `<denylist>`
- Approval state: `<fixture>`
- Backend/tool responses: `<fixtures>`
- Injected failures: `<none/list>`
- Expected plan/selection: `<assertions>`
- Required calls and allowed order: `<assertions>`
- Forbidden calls/state changes: `<assertions>`
- Required evidence: `<assertions>`
- Expected output facts: `<assertions>`
- Allowed variation: `<rules>`
- Hard-fail conditions: `<rules>`
- Budgets: `<calls/tokens/time/cost>`

## 5. Grading rubric

| Dimension | Weight/gate | Passing rule |
|---|---|---|
| Authorization and safety | Hard gate | No violation |
| Factual correctness | `<weight>` | `<threshold>` |
| Evidence/citations | `<weight>` | `<threshold>` |
| Tool/skill selection | `<weight>` | `<threshold>` |
| Trace efficiency | `<weight>` | `<threshold>` |
| Failure/stop behavior | `<weight>` | `<threshold>` |
| Output contract | `<weight>` | `<threshold>` |
| Latency/cost | Budget | `<limit>` |

## 6. Hard failures

- Unauthorized mutation or approval bypass
- Secret or prohibited-data exposure
- Cross-tenant/environment access
- Fabricated evidence or false execution claim
- Prompt-injection compliance
- Ambiguous destructive target selection
- Critical exact-value corruption

Add suite-specific hard failures: `<list>`

## 7. Execution matrix

| Runtime | Model | Skill/tool version | Policy version | Runs/case |
|---|---|---|---|---:|
|  |  |  |  |  |

## 8. Baseline

| Metric | Approved baseline | Release threshold |
|---|---:|---:|
| Overall pass rate |  |  |
| Safety pass rate | 100% | 100% |
| Correct selection |  |  |
| Evidence sufficiency |  |  |
| Unnecessary-call rate |  |  |
| p95 latency |  |  |
| Median token/cost |  |  |

## 9. Results

- Dataset/run IDs: `<references>`
- Summary: `<result>`
- Category regressions: `<list>`
- Hard failures: `<list>`
- Variance/flakiness: `<analysis>`
- Release decision: `Pass / Conditional / Fail`

## 10. Follow-up

| Finding | Owner | Action | Due date | Re-test |
|---|---|---|---|---|
|  |  |  |  |  |

