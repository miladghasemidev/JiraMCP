# Observability and Audit Standard

## 1. Purpose

Observability explains platform behavior and supports reliability, cost control, debugging, evaluation, security investigation, and continuous improvement without copying sensitive raw data into logs.

## 2. End-to-end tracing

Every user request MUST receive a workflow trace identifier propagated through:

- Agent and planner
- Context and retrieval operations
- Capability discovery and skill loading
- Code Mode and CLI
- Gateway and policy engine
- MCP server and backend adapter
- Result Store
- Evaluator and final response
- Agent Registry relationship observation and reconciliation

Each operation receives its own span identifier and records its parent.

## 3. Required trace events

At minimum:

- Request accepted and classified
- Plan created or updated
- KMS/memory retrieval performed
- Capability candidates retrieved and selected
- Skill and contract versions loaded
- Policy and approval decision
- Tool or CLI invocation started and completed
- Retry, timeout, cancellation, and partial failure
- Result stored, projected, exported, or expired
- Evaluation outcome
- Final response completed
- Declared dependency observed, unexpected dependency observed, or topology drift detected

## 4. Event fields

Events SHOULD contain:

- Timestamp in UTC
- Trace, span, request, tenant, user-reference, and agent-run identifiers
- Component, environment, capability, contract, skill, model, and policy versions
- Target reference without prohibited secrets
- Status, typed error, retry count, latency, row and byte counts
- Token and cost measures where applicable
- Approval and Result Store references
- Data classification and redaction indicators

Use `schemas/audit-event.schema.json` for sensitive audit events.

## 5. Logs, traces, metrics, and audits

| Signal | Purpose | Content rule |
|---|---|---|
| Logs | Local diagnostic events | Structured, sampled as needed, redacted |
| Traces | End-to-end workflow path | IDs, timings, choices, status; no raw secrets |
| Metrics | Aggregate health and performance | Low-cardinality labels |
| Audit | Security/accountability record | Durable, tamper-evident, restricted |

Audit and debug logs MUST NOT be treated as interchangeable.

## 6. Prohibited telemetry

Do not record:

- Credentials or authentication artifacts
- Full sensitive prompts or retrieved documents by default
- Unbounded tool payloads
- Private keys, connection strings, or session cookies
- Sensitive personal data unless explicitly required and protected by audit policy
- Raw database query results when references and hashes suffice

Redaction MUST happen before telemetry export.

## 7. Metrics

Track at least:

- Request success, partial success, denial, and failure rate
- End-to-end and component latency percentiles
- Tool and skill selection frequency and failure rate
- Unnecessary call and retry rate
- Context tokens, output tokens, and schema-loading cost
- Result Store volume, access, and expiry
- Policy denial and approval frequency/latency
- Backend saturation, timeout, and circuit-breaker state
- Evaluation scores and regressions
- Cache hit rate with freshness and permission correctness
- Registered, unmanaged, ownerless, stale, disabled-but-invoked, and unexpected-relationship counts

## 8. Dependency observation

Authorized traces SHOULD produce bounded relationship observations such as agent-invokes-tool, skill-requires-tool, gateway-routes-to-MCP, MCP-connects-to-backend, and agent-uses-model. Observations MUST use stable Registry IDs, environment, timestamps, and counts rather than embedding raw request or result payloads.

Observed relationships are supplied to Registry reconciliation as evidence. They MUST NOT automatically alter approved declarations, permissions, lifecycle state, or catalog visibility.

## 9. Service objectives

Each production capability MUST define service-level indicators and objectives for availability, latency, correctness or contract success, and freshness where relevant. Targets are capability-specific and MUST not be invented by a generic standard.

## 10. Alerting

Alert on user-impacting or security-significant conditions, including sustained failure, latency regression, permission anomalies, cross-tenant control failures, approval bypass attempts, secret detection, result-store access anomalies, unusual mutation volume, evaluator regression, and cost exhaustion.

Alerts SHOULD be actionable and identify owner, impact, affected capability, trace examples, and safe mitigation.

Topology alerts SHOULD cover unregistered production components, ownerless active components, unexpected data-access edges, unsupported dependency versions, and calls to disabled or retired components.

## 11. Trace grading support

Traces MUST contain enough structured information to determine:

- Whether the correct skill/tool was selected
- Whether calls were necessary and ordered correctly
- Whether permissions and approvals were respected
- Whether evidence was collected before conclusions
- Whether the agent stopped safely
- Whether raw data entered context improperly

## 12. Retention and access

Define separate retention and access controls for operational logs, traces, metrics, security audit, evaluation datasets, and result content. User deletion or legal requirements MUST propagate according to policy without destroying required security evidence improperly.

## 13. Correlation and time

All systems MUST use synchronized UTC timestamps. Backend-native identifiers MAY be recorded as secondary correlation fields but MUST not replace platform trace identifiers.

## 14. Dashboards

Provide dashboards for platform health, gateway/MCP health, Registry inventory and topology drift, capability quality, security/approval, context and retrieval, Result Store, model cost/tokens, and evaluation regressions. Owners MUST be named.

## 15. Testing

Test trace propagation, stable Registry ID correlation, declared/observed relationship extraction, clock/timezone handling, field presence, redaction, sampling, audit immutability controls, cardinality limits, partial failures, Result Store correlation, alert triggering, and evaluator consumption.
