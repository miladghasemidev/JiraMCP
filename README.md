# Jira MCP On-Premises

This repository implements the exact 114-tool Jira Server/Data Center inventory approved in `project-inputs/APPROVED_JIRA_CAPABILITY_MATRIX.xlsx` for Jira 8.20.0, 9.12.0, and 10.3.0.

## Implementation

The Python 3.12 package uses the official MCP SDK and an async HTTP client. It provides strict generated input schemas, exact registered method/path dispatch, version adapters, typed errors, deny-overrides policy and approval boundaries, idempotency, bounded retry/cancellation, Result Store handoff, trace/audit events, Registry/catalog metadata, and fail-closed external integrations.

Install for development with `python -m pip install -e ".[dev]"`, run `pytest`, `ruff check src tools tests`, and `mypy src`. Run `jira-mcp-on-prem --ready` before serving over stdio.

## Safety boundary

Production never defaults from ambiguous configuration. The repository does not contain Jira credentials or fabricate an enterprise Gateway, secret broker, Result Store, identity provider, audit sink, or policy service. The default server factory denies execution until those controls and registered targets are supplied. Automated tests use local fakes and mocked Jira responses; they never mutate a production Jira instance.

## Authoritative artifacts

The matrix controls scope; the immutable vendored standards control implementation. Generated inventory and specifications live under `specs/`, runtime Registry/catalog metadata under `registry/`, evaluations under `evals/`, and operational guidance under `runbooks/`.
