# Project Inputs

This directory contains the authoritative domain-specific inputs for the Jira MCP project.

## Authoritative capability scope

`APPROVED_JIRA_CAPABILITY_MATRIX.xlsx` is present and contains exactly **114 distinct approved Jira MCP tools**.

Scope composition:

- Agile: 34
- Issue: 46
- Project: 17
- Version: 17

See `MATRIX_PROVENANCE.md` for reconstruction provenance and target-version notes.

The matrix controls **WHAT** is in scope. The vendored `agent-platform-standards/` directory controls **HOW** the approved scope must be implemented.

Do not place secrets, Jira passwords, API tokens, session cookies, or production credentials in this directory.
