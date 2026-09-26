# Agent Engineering Principles

## 1. Separation of concerns

Use this invariant throughout design and review:

```text
Tools expose capabilities.
Skills encode procedures.
Code performs deterministic computation.
Agents perform reasoning.
CLI exposes capabilities efficiently.
Gateway controls access and routing.
Registry governs identity, ownership, lifecycle, versions, and dependencies.
Result Store keeps large data out of context.
Evaluators measure outcomes and traces.
```

An artifact that mixes these responsibilities SHOULD be redesigned before implementation.

## 2. Reuse before creation

Before adding an artifact, the designer MUST search existing:

- Tool and resource catalog entries
- Skills and workflow components
- Queries, scripts, CLI commands, and backend adapters
- Result Store transformations
- KMS knowledge and prior ADRs

A new artifact requires a documented gap. Similar names are not proof of a gap; compare contracts and semantics.

## 3. Domain capability over endpoint wrappers

MCP servers MUST expose stable domain capabilities, not mechanically mirror every REST endpoint, stored procedure, or SDK method. A tool boundary should represent an operation the platform repeatedly needs and can secure, test, observe, and explain.

## 4. Evidence-first behavior

- A factual diagnosis MUST cite the evidence used.
- Evidence, inference, recommendation, and unknowns MUST be distinguishable.
- Missing evidence MUST produce a bounded follow-up action or an explicit limitation, not fabricated certainty.
- The platform SHOULD capture provenance close to collection time.

## 5. Bounded everything

Every operation MUST define:

- Maximum records and bytes
- Pagination or cursor behavior
- Timeout and cancellation behavior
- Retry eligibility and maximum attempts
- Context projection size
- Resource and cost budget

"All results" is not a valid default.

## 6. Keep raw data out of model context

Large results MUST be written to the Result Store. The model receives a compact summary, schema, important samples, truncation indicators, provenance, and an opaque authorized reference. Deterministic filtering and aggregation SHOULD happen before model inspection.

## 7. Progressive disclosure

The runtime MUST discover and load only what the current task needs:

1. Compact capability metadata.
2. Full schema for selected tools.
3. Full instructions for selected skills.
4. Referenced supporting material only when the workflow requires it.

## 8. Read-only first

Analysis and retrieval capabilities SHOULD be read-only. Mutation must be a distinct operation with a distinct permission, risk class, audit record, and approval policy. A read tool MUST NOT produce hidden writes.

## 9. Least privilege and short-lived access

Credentials MUST be scoped to the selected capability, target, environment, operation, and time window. The model MUST NOT receive raw credentials. Authorization is evaluated at execution time, not inferred from the ability to see a tool description.

## 10. Deterministic work belongs in code

Use Code Mode for loops, polling, joining, sorting, aggregation, validation, bulk operations, and repeatable transformations. The agent chooses and explains the computation; deterministic code executes it.

## 11. Human control over material side effects

High-impact, destructive, irreversible, externally visible, or financially meaningful operations MUST require explicit approval unless a narrowly scoped pre-approved policy exists. Approval MUST bind to the exact action plan and expire.

## 12. Plan is not permission

The planner may propose an action it cannot execute. The gateway makes the authorization decision for each capability call. An evaluator cannot retroactively authorize an action.

## 13. Fail closed on uncertainty

If target identity, environment, scope, authorization, or side effect is ambiguous, stop or request clarification. Do not guess a production instance, recipient, project, database, or destructive target.

## 14. Idempotency and safe retries

- Reads SHOULD be idempotent.
- Retryable mutations MUST accept an idempotency key.
- Timeouts with unknown outcomes MUST NOT be blindly retried.
- Retry decisions MUST use typed error metadata.

## 15. Explicit state and versioning

Plans, skills, tool schemas, policies, results, and approvals MUST carry stable identifiers and versions. The trace MUST record the exact versions used.

## 16. Structured contracts

Machine-facing inputs and outputs MUST use typed, structured schemas. Human-readable text MAY accompany structured data but MUST NOT be the only carrier of identifiers, status, pagination, truncation, errors, or evidence references.

## 17. Runtime portability

Business rules belong in standards, policies, skills, domain services, or reusable code—not in a one-off system prompt. Host-specific adapters SHOULD be thin.

## 18. No silent scope expansion

The execution MUST stay within the user's requested goal, selected targets, permitted data, and approved action. Additional attractive work is a proposal, not implicit authorization.

## 19. Parallelize only independent work

Parallel execution MAY be used when branches are independent, have bounded resource use, preserve audit order, and have a defined fan-in step. Do not add agents merely to increase activity.

## 20. Improvement requires evidence

Changes to prompts, skills, tools, models, routing, gateways, or policies MUST be evaluated against a versioned benchmark. Trace-derived improvement proposals require human review and MUST NOT auto-merge.

## 21. Graceful degradation

When a nonessential component is unavailable, the platform SHOULD offer a safe reduced mode. It MUST NOT bypass authorization, inject unverified cached data, or convert a failed protected operation into an unprotected one.

## 22. Secure defaults are product behavior

Security, auditability, output limits, and approval are not optional infrastructure concerns. They are part of the capability contract and Definition of Done.

## 23. Every production component is registered

Agents, MCP servers, tools, skills, models, runtimes, gateways, backends, and governed data sources MUST have stable Registry identities, accountable owners, exact versions, lifecycle state, policy/evaluation references, and declared dependencies before production activation. Runtime-observed relationships are reconciled as evidence and never auto-approved.
