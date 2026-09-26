# Tool Design Standard

## 1. Definition

A tool exposes a reusable backend capability with a typed contract. It answers **what the platform can do**. It does not encode a full diagnostic or business procedure unless that procedure is a deterministic, cohesive backend operation with clear reuse value.

## 2. Admission test

A new tool is justified only when all are true:

1. No approved compatible Registry capability can satisfy the need directly or through bounded deterministic composition.
2. The operation crosses a backend, privilege, process, or trust boundary that should not be implemented only in agent reasoning.
3. It is reusable beyond one prompt or one hard-coded case.
4. It can have a stable typed contract, bounded output, security policy, and tests.
5. Its semantics are distinct from existing tools.

Otherwise use reuse, Code Mode, a skill, ordinary application code, or one-time agent reasoning.

## 3. Naming

Use `<domain>.<verb>_<object>` with a precise verb and domain language.

Good:

- `sqlserver.get_blocking_context`
- `jira.search_issues`
- `kms.get_document`
- `oracle.list_long_running_sessions`

Avoid:

- `execute`
- `run_query`
- `do_admin_task`
- Names that encode a UI screen, team nickname, or temporary implementation.

The name, title, and description MUST agree. Tool descriptions MUST state when to use the tool and when not to use it.

## 4. Granularity

Prefer one meaningful domain capability over one tool per backend endpoint. A tool SHOULD gather a tightly related evidence bundle when doing so reduces repeated calls, preserves a consistent snapshot, and stays broadly reusable.

Do not create multiple tools that differ only by a fixed threshold or filter. Expose the filter as a validated input or perform the variation in Code Mode.

## 5. Input contract

Every input field MUST define:

- Type and format
- Required or optional status
- Allowed values or validation rule
- Default, if any
- Unit and timezone, when relevant
- Maximum length or collection size
- Whether it selects an environment or protected target
- Whether it affects authorization or side effects

Inputs MUST NOT accept raw credentials. Free-form query languages, shell commands, SQL, regular expressions, file paths, URLs, or templates require explicit threat modeling and strict allowlisting or isolation.

Production targets MUST be explicit; a missing environment MUST fail rather than silently default to production.

## 6. Output contract

Every successful output MUST include, directly or through the standard envelope:

- `status`
- Capability and contract version
- Correlation or trace identifier
- Data or a Result Store reference
- Completeness state: complete, paginated, sampled, filtered, or truncated
- Record and byte counts when meaningful
- Evidence provenance and collection time
- Warnings and safe next cursor when applicable

The output MUST be sufficient to distinguish "no matching data" from "data unavailable," "not authorized," and "result truncated."

## 7. Bounded output

Each tool MUST set explicit maximums for records, bytes, execution time, and page size. Large results MUST be stored outside model context.

A list tool MUST support filtering and at least one of pagination, aggregation, or Result Store output. A tool MUST NOT claim completeness after reaching a limit unless the backend proves that the full set was returned.

## 8. Evidence quality

Diagnostic tools SHOULD return facts needed for later reasoning, not a confident narrative diagnosis. Evidence fields SHOULD include source, target, query or collector version, timestamp, relevant identifiers, and any collection limitations.

Computed fields MUST state their formula or semantic definition in the contract.

## 9. Read and write classes

| Class | Description | Default policy |
|---|---|---|
| R0 | Metadata discovery with negligible sensitivity | Authenticated and scoped |
| R1 | Ordinary read | Explicit read permission |
| R2 | Sensitive or production diagnostic read | Elevated scoped read and audit |
| W1 | Reversible, low-impact write | Explicit permission; approval per policy |
| W2 | Material or externally visible change | Human approval and verification |
| W3 | Destructive, irreversible, or high-blast-radius change | Default deny; exceptional approval |

Read tools MUST NOT contain hidden W1-W3 behavior.

## 10. Mutation requirements

A mutation tool MUST:

- Describe exact side effects.
- Return or accept a preview of the exact action when possible.
- Bind approval to target, parameters, requester, expiry, and contract version.
- Support an idempotency key if retry is possible.
- State concurrency/precondition semantics.
- Verify the resulting state without claiming rollback guarantees that do not exist.
- Return partial-success details per target.

## 11. Error behavior

Use stable typed errors. Do not encode errors only in prose or return success with an empty payload for failures.

Required distinctions include:

- Invalid input
- Authentication failure
- Authorization or policy denial
- Approval required or expired
- Target not found or ambiguous
- Backend unavailable
- Rate or quota limit
- Timeout or cancellation
- Partial failure
- Conflict or stale precondition
- Unknown mutation outcome
- Internal error

## 12. Retry and idempotency

The contract MUST state whether the operation is idempotent and which errors are retryable. Retryable does not mean the model should loop; the gateway or Code Mode performs bounded retries under policy.

## 13. Description quality checklist

A Registry/catalog discovery description MUST answer:

- What does this capability return or change?
- Which domain and targets does it support?
- When should it be selected?
- When should it not be selected?
- Is it read-only or mutating?
- What permissions and approval class apply?
- What are the main limits?

Descriptions MUST NOT use marketing language or make unsupported claims of accuracy.

## 14. Tool specification and tests

Complete `templates/TOOL_TEMPLATE.md` before implementation. Required tests include schema boundaries, empty results, maximum result, pagination, permissions, injection input, timeout, cancellation, backend errors, redaction, Registry/catalog projection, dependency compatibility, and any mutation-specific behaviors.

## 15. Anti-patterns

- One tool for every API endpoint
- A different tool for every saved filter
- Generic arbitrary SQL or shell execution for ordinary agents
- Returning HTML, logs, plans, or rows without a size contract
- Combining read, analysis, and remediation in one opaque call
- Returning only natural-language text
- Using tool presence as authorization
- Retry loops controlled through repeated LLM turns
- A tool whose only consumer is one one-off prompt and whose logic has no boundary to protect
- A production tool with no Registry owner, lifecycle state, providing MCP relationship, policy, or evaluation reference
