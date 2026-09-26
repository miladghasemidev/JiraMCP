# Capability Classification Examples

These examples demonstrate the intended separation. They are not permission grants or production-ready contracts.

| Requested outcome | Classification | Why |
|---|---|---|
| Count current active SQL Server sessions | Existing or new atomic read tool | A reusable backend fact behind a protected boundary |
| Diagnose the cause of blocking | Skill using read tools | A reusable evidence-driven procedure |
| Sort sessions by transaction age | Code Mode | Deterministic transformation over existing evidence |
| Explain one supplied execution plan | Agent reasoning | One-time reasoning when all evidence is already present |
| Check 500 databases and report backup age over 24 hours | Existing backup-status tool plus Code Mode; skill if recurring | Iteration/filtering is deterministic; avoid fixed-filter tools |
| Kill the root blocker | Separate W2/W3 mutation capability or reject | Material state change cannot hide inside diagnosis |
| Search Jira issues and group them by owner | Search tool plus Code Mode | Backend retrieval plus deterministic aggregation |
| Investigate a production incident across logs, deployment, Jira, and SQL | Skill, potentially with bounded parallel branches | Reusable multi-domain procedure and evidence fan-in |
| Answer what CLI means | Agent reasoning | No backend capability or reusable workflow needed |
| Add `get_old_backups` when `get_backup_status` exists | Reuse plus Code Mode | A threshold filter is not a distinct backend capability |

## Example anti-explosion mapping

Do not create:

```text
get_old_backups
find_missing_backups
find_failed_backups
analyze_backup_health
check_backup_compliance
get_backup_age
```

Prefer:

```text
Tool:  sqlserver.get_backup_status
Code:  filter, calculate age, group, and aggregate
Skill: sqlserver.assess_backup_compliance (only if the procedure recurs)
```

## Design-time versus runtime

- Decision trees classify a requirement at design time.
- Standards define how the selected artifact is built.
- Templates record its contract.
- Prompts direct an AI coding agent to apply the standards.
- CLI invokes approved capabilities at runtime.
- Code Mode executes deterministic multi-step work at runtime.
- Gateway authorizes and routes every protected call at runtime.

