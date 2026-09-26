# Code Mode Standard

## 1. Purpose

Code Mode is a constrained deterministic execution environment used to perform work that should not consume repeated model turns. It coordinates approved capabilities and transforms data; it does not grant authority or replace domain tools.

## 2. Use Code Mode when work requires

- Iteration over multiple targets or pages
- Polling with a bounded termination condition
- Filtering, sorting, grouping, joining, or aggregation
- Validation, hashing, comparison, parsing, or format conversion
- Repeated MCP or CLI calls
- Bulk processing with controlled concurrency
- Reproducible calculations
- Reducing a large result before it enters context

## 3. Do not use Code Mode to

- Bypass gateway policy, approval, audit, or capability scopes
- Store or reveal credentials
- Invent missing business decisions
- Execute arbitrary user-supplied code without an explicitly designed sandbox product feature
- Replace a reusable backend capability that requires a protected boundary
- Hide high-impact mutations inside a script
- Perform open-ended autonomous loops

## 4. Execution contract

Every Code Mode run MUST declare:

- Purpose and parent workflow trace
- Inputs and their provenance
- Allowed capability identifiers and targets
- Read/write risk class
- CPU, memory, wall-time, call-count, byte, and concurrency budgets
- Network and filesystem access policy
- Expected output schema and maximum size
- Result Store behavior
- Cancellation and cleanup behavior

## 5. Sandbox rules

- Default-deny network and filesystem access.
- Allow only the domains, paths, commands, packages, and capabilities required by the task.
- Use an ephemeral workspace unless persistence is explicitly required.
- Mount secrets only through a brokered mechanism that does not expose their values to code output or model context.
- Prevent privileged host access and cross-tenant data access.
- Record runtime image and dependency versions.

## 6. Capability calls

Code Mode SHOULD call capabilities through the approved CLI or gateway client. It MUST use the same user delegation, policy, quotas, audit, and approval rules as direct agent calls.

Batch or parallel calls MUST be bounded. Per-target failures MUST be captured without discarding successful independent results.

## 7. Large-result handling

Raw datasets MUST go to the Result Store. Code Mode SHOULD return:

- An opaque result reference
- Schema and provenance summary
- Counts and completeness information
- Aggregates relevant to the task
- A small policy-safe sample, if needed
- Warnings and failed-target summary

## 8. Polling

Polling loops MUST define:

- Maximum elapsed time and attempts
- Initial interval and capped backoff
- Terminal success and failure states
- Cancellation behavior
- Handling of unknown states

Do not make the model decide whether to continue every iteration.

## 9. Retries

Retry only typed, explicitly retryable failures. Use bounded exponential backoff with jitter where appropriate. Do not retry non-idempotent mutations unless an idempotency key and known outcome semantics make it safe.

## 10. Reproducibility

Deterministic transformations MUST record script or code version, dependency versions, input references, parameters, and output content hash. Randomized algorithms MUST set and record a seed where feasible.

## 11. Example: backup compliance over many targets

The agent selects `sqlserver.get_backup_status`. Code Mode enumerates authorized databases, calls the capability with bounded concurrency, filters results older than the policy threshold, writes full results to the Result Store, and returns only noncompliant counts plus a compact evidence table.

Do not create separate tools such as `get_old_backups`, `find_missing_backups`, and `check_backup_compliance` when the existing capability plus deterministic processing is sufficient.

## 12. Example: Jira aggregation

Use `jira.search_issues` with server-side filtering and pagination. Code Mode follows cursors, groups approved fields by owner and priority, and returns aggregate counts. Issue bodies are not inserted into model context unless the task and permissions require them.

## 13. Output and exit status

Code Mode output MUST be structured and distinguish:

- Complete success
- Partial success
- Safe cancellation
- Policy denial
- Budget exceeded
- Validation failure
- Backend failure
- Unknown mutation outcome

An execution that exceeds a budget MUST stop safely and preserve auditable partial results when permitted.

## 14. Testing

Test deterministic correctness, maximum input, budget enforcement, cancellation, partial failure, retry rules, unauthorized capability access, result-store handoff, secret redaction, concurrency limits, and cleanup.

