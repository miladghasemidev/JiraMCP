# Jira Capability Matrix Provenance

The authoritative project matrix is:

`APPROVED_JIRA_CAPABILITY_MATRIX.xlsx`

## Status

This workbook contains exactly **114 distinct approved Jira MCP tool capabilities**.

The earlier analysis had already locked the approved count to 114, but the physical spreadsheet itself was not persisted. At the user's explicit instruction, the authoritative workbook was reconstructed from the recovered historical Jira Data Center MCP operation inventory and the locked project scope.

## Recovered source

- Repository: `MSPbotsAI/jiradatacenter-mcp`
- Historical full-inventory commit: `2549afc321c14ebc02b13c07457d3e289657f50e`
- Recovered source inventory: 214 Jira operations
- Source table: repository `README.md` at the pinned commit

## Approved 114-tool composition

- Agile: 34
- Issue: 46
- Project: 17
- Version: 17
- Total: 114

The matrix preserves the recovered stable tool IDs and baseline HTTP method/path for those 114 capabilities.

## Target Jira versions

The approved target range is:

- Jira 8.20.0
- Jira 9.12.0
- Jira 10.3.0

The displayed endpoint is the recovered baseline route. Implementation must use version-aware adapters and verify endpoint/parameter/response differences per target version. If concrete evidence proves a capability cannot be implemented for an approved target version, the row remains in scope and must be marked `BLOCKED_ARCHITECTURE_REVIEW`; it must not be silently removed or substituted.

## Scope rule

This matrix controls **WHAT** must be implemented. The vendored `agent-platform-standards/` package controls **HOW** the tools must be implemented, secured, bounded, tested, evaluated, reviewed, and released.
