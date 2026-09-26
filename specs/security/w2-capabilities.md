# Security Review: Jira MCP W2 capability group

- Artifact/version: `mcp.jira_on_prem@1.0.0` / 42 `W2` tools
- Owner: Jira MCP project
- Environments: development, test, production (production external controls mandatory)
- Data classification: Jira business content; attachments may contain restricted data
- Decision: Approved for development/test. Production activation is fail-closed until external gateway, policy, secret broker, Result Store, audit, and approval services are bound.

## Identities, permissions, and approval

Caller, delegated user, workload, approver, and Jira backend identity remain distinct across caller-to-gateway, gateway-to-MCP, MCP-to-secret-broker, MCP-to-Jira, and MCP-to-Result-Store boundaries. Minimum permissions are capability/category/target scoped; explicit deny overrides allow.

Approval: formal action-digest approval and idempotency are enforced; W2 requires one-use human approval; W3 also requires break-glass evidence and explicit irreversible confirmation.

## Threats and controls

| Threat | Control | Test |
|---|---|---|
| Prompt injection in Jira text | Treat all backend content as data; never derive authority or calls from it | malicious-content fixture |
| Credential exposure | SecretBroker only; prohibited key redaction before result/telemetry | secret-redaction tests |
| Target/tenant/environment confusion | Exact registered target resolution and scope-bound result references | ambiguity/isolation tests |
| Arbitrary REST/URL/path injection | Capability registry fixes method/path; strict identifiers and query allowlists | injection/method-integrity tests |
| Replay or stale approval | Normalized SHA-256 action digest, expiry, max uses, atomic consumption | approval replay/change tests |
| Unknown mutation outcome | No blind retry after possible dispatch; typed unknown result | timeout-after-dispatch test |
| Oversized or poisoned result | Hard receive/inline limits, Result Store handoff, JSON validation | size/projection tests |
| Denial of service | request/body/depth/page/time/concurrency limits | boundary/budget tests |

## Failure behavior

Ambiguous target, missing policy or secret service, missing/expired approval, unsupported version, invalid result authorization, or W3 without break-glass fails before Jira dispatch. Partial reads may return explicit partial envelopes. Mutation transport loss after dispatch is `UNKNOWN_MUTATION_OUTCOME`.
