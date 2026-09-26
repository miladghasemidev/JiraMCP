# MCP Gateway Standard

## 1. Purpose

The MCP gateway is the mandatory control point between agent runtimes, CLI or Code Mode clients, and domain MCP servers. It centralizes authentication, policy, routing, quotas, result handling, and audit without absorbing domain-specific business logic.

## 2. Required responsibilities

The gateway MUST:

- Authenticate human, agent, workload, and delegated identities.
- Resolve tenant, environment, and request context.
- Authorize each capability call against target and parameters.
- Enforce approval requirements and bind approvals to exact actions.
- Route stable capability identifiers to compatible server versions.
- Enforce input, output, call-count, time, and concurrency budgets.
- Apply rate limits, circuit breakers, and cancellation.
- Propagate trace and idempotency identifiers.
- Redact prohibited fields from logs and error surfaces.
- Store large results and return bounded projections.
- Emit security audit and operational telemetry.
- Support emergency disablement by capability, server, environment, or tenant.
- Resolve routes only for approved compatible Registry component versions and emit observed dependency evidence.

## 3. Prohibited responsibilities

The gateway MUST NOT:

- Become the primary implementation of Jira, SQL Server, Oracle, KMS, or other domain logic.
- Rewrite a denied request into a weaker unprotected action.
- Treat catalog visibility as execution permission.
- Expose backend credentials to the model or CLI output.
- Silently route a production request to a different target.
- Retry an unknown-outcome mutation without safe idempotency semantics.

## 4. Invocation envelope

Every call MUST carry or derive:

- Capability identifier and requested contract version
- Caller, user delegation, tenant, and agent/run identity references
- Target environment and resource scope
- Trace, span, request, and optional idempotency identifiers
- Input payload
- Declared output budget
- Policy context
- Approval reference when required
- Client/runtime version

The gateway MUST reject missing security-critical context rather than applying an unsafe default.

## 5. Authorization model

Authorization SHOULD combine:

- Role or group permissions for broad assignment
- Attribute-based checks for environment, target, data sensitivity, time, network zone, and request properties
- Capability-based scoped execution grants
- Explicit deny rules that override allow rules
- Approval policy for protected mutations

The gateway MUST evaluate policy after resolving the concrete target and validated parameters.

## 6. Capability tokens

When delegating execution, the gateway SHOULD issue a short-lived token restricted to:

- One or a small allowlist of capability versions
- Specific environment and target scope
- Read/write class
- Maximum calls, duration, and result bytes
- User and workflow identity
- Approval identifier, if any

Tokens MUST be audience-bound, expire quickly, and be unusable as general backend credentials.

## 7. Approval enforcement

An approval MUST bind to a normalized action digest containing capability version, target, parameters, expected side effects, requester, approver, and expiry. Any material change invalidates the approval.

Approval cannot be inferred from conversational phrases when policy requires a formal approval record.

## 8. Routing and compatibility

- Routes MUST be versioned and environment-aware.
- The gateway MUST refuse incompatible contract versions.
- Failover MAY use an equivalent server only when semantics, authorization, data region, and audit guarantees are equivalent and documented.
- Canary and rollback controls SHOULD operate per capability version.
- Unmanaged, disabled, retired, incompatible, or policy-invalid Registry components MUST not receive ordinary production traffic.

## 9. Budget enforcement

The gateway MUST enforce hard ceilings for:

- Calls per workflow and per capability
- Concurrent calls
- Request and response bytes
- Page size and total records
- Wall time and backend time
- Result Store retention and reads
- Tenant/user rate and cost budget

Budget-exceeded errors MUST state which safe limit was reached without exposing sensitive quota configuration.

## 10. Result handling

The gateway validates response envelopes, applies classification/redaction, and decides whether data may return inline. When results exceed policy or size limits, it stores them and returns an opaque reference plus bounded metadata.

The gateway MUST NOT summarize data by dropping error, truncation, completeness, or provenance fields.

## 11. Reliability

- Use bounded retries only for typed retryable failures.
- Use circuit breakers per backend and capability where appropriate.
- Propagate cancellation.
- Distinguish dependency outage from policy denial.
- Preserve partial results when allowed and mark them explicitly.
- For async operations, expose stable status and cancellation capabilities.

## 12. Multi-tenancy

Tenant identity MUST be explicit in policy, routing, caching, Result Store access, and audit. Cross-tenant cache keys, result references, credentials, and logs are prohibited.

## 13. Caching

Cache only when the capability contract permits it. Cache keys MUST include security scope, target, contract version, relevant inputs, and data freshness class. Mutations and sensitive diagnostics SHOULD default to no cache. Responses MUST identify cached data and collection time.

## 14. Administration

Administrative interfaces MUST be separate from ordinary capability invocation, strongly authenticated, least-privileged, and fully audited. Configuration changes SHOULD require review and support rollback.

## 15. Testing

Required tests include policy allow/deny precedence, target resolution, approval binding and expiry, Registry lifecycle/version routing, observed relationship emission, token scope, tenant isolation, limits, retries, circuit breakers, result storage, redaction, emergency disablement, partial failure, and unknown mutation outcome.
