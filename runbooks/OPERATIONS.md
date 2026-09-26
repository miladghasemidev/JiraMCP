# Jira MCP operations

## Configuration and readiness

Set `JIRA_MCP_CONFIG` to a reviewed non-secret JSON configuration. Targets must be unique by environment and target ID. Credentials stay in the external secret broker. `--health` confirms process/package health; `--ready` checks target registration and returns `not_ready` when none is configured. Production deployment must additionally bind verified gateway context, policy, approvals, secrets, Result Store, audit, stable cursor signing, and deployment-specific concurrency controls.

## Start and verify

Install the exact locked dependencies, run `jira-mcp-on-prem --ready`, then start the stdio transport with `jira-mcp-on-prem`. An MCP client should list exactly 114 tools. A call through the default factory is expected to fail closed because it has no verified gateway identity or enterprise services.

## Monitoring

Monitor success/partial/denial/failure rates, p95 latency, backend timeouts, rate limits, unknown mutation outcomes, approval failures, Result Store usage/expiry, redaction events, audit failures, Registry/catalog drift, and disabled-component calls. Trace IDs must propagate to the gateway, MCP server, adapter, Jira request metadata where supported, Result Store, audit, and evaluation records.

## Disablement and rollback

1. Deny the capability or MCP server in gateway policy.
2. Change Registry lifecycle/catalog visibility to disabled for runtime discovery.
3. Revoke scoped credentials or the route if containment is required.
4. Preserve audit and authoritative inventory history.
5. Deploy the previous exact package artifact when code rollback is required.

W3 is never enabled by the repository default. Break-glass activation must be separately authenticated, time-limited, one-use, target-bound, visible, audited, and reviewed after use.

## Known deployment boundary

No real Jira target, production credential, enterprise policy, approval service, Result Store, or audit sink is included. Automated tests use deterministic local fakes and mocked Jira transport; they do not perform production mutations.

