# Worked Example: SQL Server Blocking Diagnosis

This example shows how one request is split across components without turning the whole workflow into one opaque tool.

## User outcome

> Diagnose the current SQL Server blocking incident, identify the likely root blocker, explain the evidence, and provide safe remediation instructions without changing the database.

## Classification

- Backend evidence collection crosses a protected boundary: use read-only tools.
- Correlation and diagnosis are a recurring expert procedure: use a skill.
- Sorting, graph construction, and bounded correlation are deterministic: use Code Mode.
- The final interpretation and explanation require judgment: use agent reasoning.
- Execution of `KILL`, DDL, DML, configuration change, or service control is outside this skill.

## Minimum capability set

Prefer one coherent snapshot capability when the backend can collect it consistently:

```text
sqlserver.get_blocking_context
```

Possible output fields:

- Instance and collection timestamp
- Blocking edges and root-blocker candidates
- Session/request identifiers and status
- Wait type and duration
- Transaction start time and age
- Database and object identifiers where safely resolvable
- Query hash/plan handle and bounded query text according to policy
- Completeness, permission, and truncation indicators

If one consistent snapshot is impossible, a skill may coordinate smaller existing read tools. Do not add tools simply to mirror each DMV.

## Skill

```text
sqlserver.diagnose_blocking
```

Workflow:

1. Confirm the exact instance and environment.
2. Confirm read-only diagnostic authorization.
3. Collect a bounded blocking snapshot.
4. Use deterministic code to construct blocking chains and calculate transaction age.
5. Identify root-blocker candidates using explicit evidence.
6. Correlate waits, transactions, query identity, and resource information.
7. Detect incomplete or stale evidence and reduce confidence accordingly.
8. Produce findings, evidence, impact, uncertainty, and separately marked remediation instructions.

## Safety contract

The workflow MUST NOT:

- Execute `KILL <session_id>`
- Run DDL or DML
- Change logins, roles, configuration, recovery, jobs, or services
- Claim that a proposed remediation was executed
- Recommend killing a session without stating transaction and business-impact uncertainty

## Code Mode example

Deterministic logic may:

- Validate there are no cycles or malformed edges
- Build the blocking graph
- Calculate chain depth and transaction age
- Sort root candidates by downstream impact
- Store the full snapshot and return a compact table

It may not gain extra database permissions or call a mutation tool.

## Output outline

1. Current finding
2. Root-blocker candidate and confidence
3. Evidence table with collection time
4. Affected sessions and impact
5. Missing evidence or limitations
6. Safe immediate recommendations
7. Optional T-SQL or PowerShell instructions, clearly labeled **proposed and not executed**
8. Validation steps

## Evaluation cases

Include no blocking, one chain, multiple independent chains, sleeping session with open transaction, stale snapshot, insufficient permission, truncated query text, session ended during collection, reused session ID, malicious SQL text containing instructions, ambiguous production target, request to execute `KILL`, and partial backend failure.

