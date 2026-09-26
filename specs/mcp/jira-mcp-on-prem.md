# MCP Server Specification: Jira on-premises

## Document control

| Field | Value |
|---|---|
| Server ID | `jira-mcp-on-prem` |
| Registry component ID | `mcp.jira_on_prem` |
| Specification version | 1.0.0 |
| Owner | Jira MCP project |
| Status | Active in development/test; production binding pending |
| Last review | 2026-09-13 |

## Purpose and boundary

One coherent Jira Data Center/Server trust boundary exposes exactly the 114 matrix-approved Agile, issue, project, and version capabilities. It does not expose arbitrary REST, credentials, workflow reasoning, bulk loops, generic URLs, or non-Jira backends. Deterministic pagination/bulk orchestration belongs in Code Mode.

## Supported systems and adapters

| Backend | Version | Environments | Adapter |
|---|---|---|---|
| Jira Server/Data Center | 8.20.0 | development, test, production | `Jira820Adapter` |
| Jira Data Center | 9.12.0 | development, test, production | `Jira912Adapter` |
| Jira Data Center | 10.3.0 | development, test, production | `Jira103Adapter` |

Only registered HTTPS targets and these exact versions resolve. Environment and target are mandatory. Production has no default and fails readiness when gateway, secret broker, policy, Result Store, or audit bindings are missing.

## Architecture and trust boundaries

`Caller -> enterprise Gateway -> Jira MCP -> version adapter -> registered Jira target`; large output flows from Jira MCP to the authorized Result Store. Identity/policy/approval, secrets, results, and audit services are strict external interfaces with in-memory development/test fakes only.

## Authentication and authorization

- Gateway/server authentication and delegated identity are deployment bindings; the server requires verified invocation context rather than accepting user/password/token arguments.
- Backend credentials are short-lived values obtained by a `SecretBroker` for the resolved target and never logged or returned.
- Deny-overrides policy evaluates capability/version, caller, tenant, environment, target, risk, normalized parameters, budget, and approval after resolution.
- W2 uses formal one-use human approval; W3 is default-denied and requires exceptional break-glass validation; conversational consent is insufficient.

## Capability inventory

| Capability ID | Version | Class | Purpose | Max output | Approval |
|---|---:|---|---|---|---|
| `jira_agile_create_board` | 1.0.0 | W2 | Create board. | 64 KiB/100 records | Human approval |
| `jira_agile_create_sprint` | 1.0.0 | W2 | Create sprint. | 64 KiB/100 records | Human approval |
| `jira_agile_delete_board` | 1.0.0 | W3 | Delete board. | 64 KiB/100 records | Exceptional human approval / default deny |
| `jira_agile_delete_sprint` | 1.0.0 | W3 | Delete sprint. | 64 KiB/100 records | Exceptional human approval / default deny |
| `jira_agile_estimate_issue_for_board` | 1.0.0 | W1 | Estimate issue for board. | 64 KiB/100 records | Policy-dependent |
| `jira_agile_get_all_boards` | 1.0.0 | R2 | Get all boards. | 64 KiB/100 records | None |
| `jira_agile_get_all_sprints_for_board` | 1.0.0 | R2 | Get all sprints for a board. | 64 KiB/100 records | None |
| `jira_agile_get_all_versions_for_board` | 1.0.0 | R2 | Get all versions for a board. | 64 KiB/100 records | None |
| `jira_agile_get_board` | 1.0.0 | R2 | Get board. | 64 KiB/100 records | None |
| `jira_agile_get_configuration` | 1.0.0 | R2 | Get board configuration. | 64 KiB/100 records | None |
| `jira_agile_get_epic` | 1.0.0 | R2 | Get epic. | 64 KiB/100 records | None |
| `jira_agile_get_epics` | 1.0.0 | R2 | Get epics. | 64 KiB/100 records | None |
| `jira_agile_get_issue_agile` | 1.0.0 | R2 | Get issue (Agile view). | 64 KiB/100 records | None |
| `jira_agile_get_issue_estimation_for_board` | 1.0.0 | R2 | Get issue estimation for board. | 64 KiB/100 records | None |
| `jira_agile_get_issues_for_backlog` | 1.0.0 | R2 | Get issues for backlog. | 64 KiB/100 records | None |
| `jira_agile_get_issues_for_board` | 1.0.0 | R2 | Get issues for board. | 64 KiB/100 records | None |
| `jira_agile_get_issues_for_board_epic` | 1.0.0 | R2 | Get issues for epic within a board. | 64 KiB/100 records | None |
| `jira_agile_get_issues_for_epic` | 1.0.0 | R2 | Get issues for epic. | 64 KiB/100 records | None |
| `jira_agile_get_issues_for_sprint` | 1.0.0 | R2 | Get issues for sprint. | 64 KiB/100 records | None |
| `jira_agile_get_issues_for_sprint_on_board` | 1.0.0 | R2 | Get issues for a sprint within a board. | 64 KiB/100 records | None |
| `jira_agile_get_issues_without_epic` | 1.0.0 | R2 | Get issues without epic. | 64 KiB/100 records | None |
| `jira_agile_get_issues_without_epic_for_board` | 1.0.0 | R2 | Get issues without epic within a board. | 64 KiB/100 records | None |
| `jira_agile_get_projects_for_board` | 1.0.0 | R2 | Get projects associated with a board. | 64 KiB/100 records | None |
| `jira_agile_get_sprint` | 1.0.0 | R2 | Get sprint. | 64 KiB/100 records | None |
| `jira_agile_move_issues_to_backlog` | 1.0.0 | W2 | Move issues to backlog. | 64 KiB/100 records | Human approval |
| `jira_agile_move_issues_to_epic` | 1.0.0 | W2 | Move issues to epic. | 64 KiB/100 records | Human approval |
| `jira_agile_move_issues_to_sprint` | 1.0.0 | W2 | Move issues to sprint. | 64 KiB/100 records | Human approval |
| `jira_agile_partially_update_epic` | 1.0.0 | W2 | Partially update epic (Agile-specific fields). | 64 KiB/100 records | Human approval |
| `jira_agile_partially_update_sprint` | 1.0.0 | W2 | Partially update sprint. | 64 KiB/100 records | Human approval |
| `jira_agile_rank_epics` | 1.0.0 | W1 | Rank epics. | 64 KiB/100 records | Policy-dependent |
| `jira_agile_rank_issues` | 1.0.0 | W1 | Rank issues. | 64 KiB/100 records | Policy-dependent |
| `jira_agile_remove_issues_from_epic` | 1.0.0 | W2 | Remove issues from epic. | 64 KiB/100 records | Human approval |
| `jira_agile_swap_sprint` | 1.0.0 | W2 | Swap sprint. | 64 KiB/100 records | Human approval |
| `jira_agile_update_sprint` | 1.0.0 | W2 | Update sprint (full). | 64 KiB/100 records | Human approval |
| `jira_issue_add_attachment` | 1.0.0 | W2 | Add one or more attachments to an issue. | 64 KiB/100 records | Human approval |
| `jira_issue_add_comment` | 1.0.0 | W2 | Add a new comment to an issue. | 64 KiB/100 records | Human approval |
| `jira_issue_add_vote` | 1.0.0 | W1 | Cast the current user vote on an issue. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_add_watcher` | 1.0.0 | W1 | Add a user to an issue watcher list. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_add_worklog` | 1.0.0 | W2 | Add a worklog entry to an issue. | 64 KiB/100 records | Human approval |
| `jira_issue_archive_issue` | 1.0.0 | W2 | Archive an issue. | 64 KiB/100 records | Human approval |
| `jira_issue_archive_issues` | 1.0.0 | W2 | Archive a list of issues. | 64 KiB/100 records | Human approval |
| `jira_issue_assign` | 1.0.0 | W2 | Assign an issue to a user. | 64 KiB/100 records | Human approval |
| `jira_issue_can_move_sub_task` | 1.0.0 | R2 | Check whether a sub-task can be moved. | 64 KiB/100 records | None |
| `jira_issue_create_issue` | 1.0.0 | W2 | Create an issue or sub-task. | 64 KiB/100 records | Human approval |
| `jira_issue_create_issues` | 1.0.0 | W2 | Create issues or sub-tasks in bulk. | 64 KiB/100 records | Human approval |
| `jira_issue_create_or_update_remote_issue_link` | 1.0.0 | W2 | Create or update a remote issue link. | 64 KiB/100 records | Human approval |
| `jira_issue_delete_comment` | 1.0.0 | W2 | Delete an existing comment. | 64 KiB/100 records | Human approval |
| `jira_issue_delete_issue` | 1.0.0 | W3 | Delete an issue. | 64 KiB/100 records | Exceptional human approval / default deny |
| `jira_issue_delete_property` | 1.0.0 | W1 | Remove an issue property. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_delete_remote_issue_link_by_global_id` | 1.0.0 | W2 | Delete a remote issue link by global ID. | 64 KiB/100 records | Human approval |
| `jira_issue_delete_remote_issue_link_by_id` | 1.0.0 | W2 | Delete a remote issue link by ID. | 64 KiB/100 records | Human approval |
| `jira_issue_delete_worklog` | 1.0.0 | W2 | Delete an existing worklog entry. | 64 KiB/100 records | Human approval |
| `jira_issue_do_transition` | 1.0.0 | W2 | Perform an issue transition. | 64 KiB/100 records | Human approval |
| `jira_issue_edit_issue` | 1.0.0 | W2 | Edit an issue. | 64 KiB/100 records | Human approval |
| `jira_issue_get_comment` | 1.0.0 | R2 | Get a single comment. | 64 KiB/100 records | None |
| `jira_issue_get_comments` | 1.0.0 | R2 | Get comments for an issue. | 64 KiB/100 records | None |
| `jira_issue_get_create_issue_meta_fields` | 1.0.0 | R2 | Get create-issue metadata fields for a project issue type. | 64 KiB/100 records | None |
| `jira_issue_get_create_issue_meta_project_issue_types` | 1.0.0 | R2 | Get issue types used for create-issue metadata. | 64 KiB/100 records | None |
| `jira_issue_get_edit_issue_meta` | 1.0.0 | R2 | Get edit metadata for an issue. | 64 KiB/100 records | None |
| `jira_issue_get_issue` | 1.0.0 | R2 | Get a full issue representation. | 64 KiB/100 records | None |
| `jira_issue_get_issue_picker_resource` | 1.0.0 | R2 | Get suggested issues for the issue picker. | 64 KiB/100 records | None |
| `jira_issue_get_issue_watchers` | 1.0.0 | R2 | Get watchers for an issue. | 64 KiB/100 records | None |
| `jira_issue_get_issue_worklog` | 1.0.0 | R2 | Get worklogs for an issue. | 64 KiB/100 records | None |
| `jira_issue_get_properties_keys` | 1.0.0 | R2 | Get issue property keys. | 64 KiB/100 records | None |
| `jira_issue_get_property` | 1.0.0 | R2 | Get an issue property. | 64 KiB/100 records | None |
| `jira_issue_get_remote_issue_link_by_id` | 1.0.0 | R2 | Get a remote issue link by ID. | 64 KiB/100 records | None |
| `jira_issue_get_remote_issue_links` | 1.0.0 | R2 | Get remote issue links. | 64 KiB/100 records | None |
| `jira_issue_get_sub_tasks` | 1.0.0 | R2 | Get an issue sub-task list. | 64 KiB/100 records | None |
| `jira_issue_get_transitions` | 1.0.0 | R2 | Get available issue transitions. | 64 KiB/100 records | None |
| `jira_issue_get_votes` | 1.0.0 | R2 | Get issue voters. | 64 KiB/100 records | None |
| `jira_issue_get_worklog` | 1.0.0 | R2 | Get a specific worklog. | 64 KiB/100 records | None |
| `jira_issue_move_sub_tasks` | 1.0.0 | W1 | Reorder sub-tasks. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_notify` | 1.0.0 | W2 | Send an issue notification. | 64 KiB/100 records | Human approval |
| `jira_issue_remove_vote` | 1.0.0 | W1 | Remove the current user vote from an issue. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_remove_watcher` | 1.0.0 | W1 | Remove a user from an issue watcher list. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_restore_issue` | 1.0.0 | W2 | Restore an archived issue. | 64 KiB/100 records | Human approval |
| `jira_issue_set_property` | 1.0.0 | W1 | Set an issue property. | 64 KiB/100 records | Policy-dependent |
| `jira_issue_update_comment` | 1.0.0 | W2 | Update an existing comment. | 64 KiB/100 records | Human approval |
| `jira_issue_update_remote_issue_link` | 1.0.0 | W2 | Update a remote issue link. | 64 KiB/100 records | Human approval |
| `jira_issue_update_worklog` | 1.0.0 | W2 | Update an existing worklog entry. | 64 KiB/100 records | Human approval |
| `jira_project_archive_project` | 1.0.0 | W2 | Archive a project. | 64 KiB/100 records | Human approval |
| `jira_project_create_project` | 1.0.0 | W2 | Create a new project. | 64 KiB/100 records | Human approval |
| `jira_project_delete_project` | 1.0.0 | W3 | Delete a project. | 64 KiB/100 records | Exceptional human approval / default deny |
| `jira_project_get_accessible_project_type_by_key` | 1.0.0 | R1 | Get an accessible project type by key. | 64 KiB/100 records | None |
| `jira_project_get_all_project_types` | 1.0.0 | R1 | Get all project types. | 64 KiB/100 records | None |
| `jira_project_get_all_projects` | 1.0.0 | R1 | Get all visible projects. | 64 KiB/100 records | None |
| `jira_project_get_all_statuses` | 1.0.0 | R1 | Get issue types and valid statuses for a project. | 64 KiB/100 records | None |
| `jira_project_get_project` | 1.0.0 | R1 | Get a project. | 64 KiB/100 records | None |
| `jira_project_get_project_components` | 1.0.0 | R1 | Get project components. | 64 KiB/100 records | None |
| `jira_project_get_project_role` | 1.0.0 | R1 | Get a project role in a project. | 64 KiB/100 records | None |
| `jira_project_get_project_roles` | 1.0.0 | R1 | Get project roles. | 64 KiB/100 records | None |
| `jira_project_get_project_type_by_key` | 1.0.0 | R1 | Get project type by key. | 64 KiB/100 records | None |
| `jira_project_get_project_versions` | 1.0.0 | R1 | Get project versions. | 64 KiB/100 records | None |
| `jira_project_get_project_versions_paginated` | 1.0.0 | R1 | Get project versions with pagination. | 64 KiB/100 records | None |
| `jira_project_get_security_levels_for_project` | 1.0.0 | R1 | Get accessible issue security levels for a project. | 64 KiB/100 records | None |
| `jira_project_restore_project` | 1.0.0 | W2 | Restore an archived project. | 64 KiB/100 records | Human approval |
| `jira_project_update_project` | 1.0.0 | W2 | Update a project. | 64 KiB/100 records | Human approval |
| `jira_version_create_or_update_remote_version_link_post_remotelink` | 1.0.0 | W2 | Create or update a remote version link. | 64 KiB/100 records | Human approval |
| `jira_version_create_or_update_remote_version_link_post_remotelink_2` | 1.0.0 | W2 | Create or update a remote version link by global ID. | 64 KiB/100 records | Human approval |
| `jira_version_create_version` | 1.0.0 | W2 | Create a project version. | 64 KiB/100 records | Human approval |
| `jira_version_delete_delete_version` | 1.0.0 | W3 | Delete a project version. | 64 KiB/100 records | Exceptional human approval / default deny |
| `jira_version_delete_post_remove_and_swap` | 1.0.0 | W2 | Delete a project version and swap references. | 64 KiB/100 records | Human approval |
| `jira_version_delete_remote_version_link` | 1.0.0 | W2 | Delete a remote version link. | 64 KiB/100 records | Human approval |
| `jira_version_delete_remote_version_links_by_version_id` | 1.0.0 | W2 | Delete all remote version links for a version. | 64 KiB/100 records | Human approval |
| `jira_version_get_paginated_versions` | 1.0.0 | R1 | Get paginated project versions. | 64 KiB/100 records | None |
| `jira_version_get_remote_version_link` | 1.0.0 | R1 | Get a remote version link. | 64 KiB/100 records | None |
| `jira_version_get_remote_version_links` | 1.0.0 | R1 | Get remote version links by global ID. | 64 KiB/100 records | None |
| `jira_version_get_remote_version_links_by_version_id` | 1.0.0 | R1 | Get remote version links by version ID. | 64 KiB/100 records | None |
| `jira_version_get_version` | 1.0.0 | R1 | Get a project version. | 64 KiB/100 records | None |
| `jira_version_get_version_related_issues` | 1.0.0 | R1 | Get counts of issues related to a version. | 64 KiB/100 records | None |
| `jira_version_get_version_unresolved_issues` | 1.0.0 | R1 | Get unresolved issue count for a version. | 64 KiB/100 records | None |
| `jira_version_merge` | 1.0.0 | W2 | Merge versions. | 64 KiB/100 records | Human approval |
| `jira_version_move_version` | 1.0.0 | W1 | Move a version sequence within a project. | 64 KiB/100 records | Policy-dependent |
| `jira_version_update_version` | 1.0.0 | W2 | Update a project version. | 64 KiB/100 records | Human approval |

## Contract, output, and reliability

- Input schemas: `specs/schemas/inputs/*.json`; result/error envelope: the vendored `tool-result.schema.json` plus typed Pydantic models.
- UTF-8 JSON, UTC RFC 3339 timestamps, opaque identifiers unless a schema states otherwise.
- 1 MiB ordinary request, 6 MiB attachment aggregate, 5 MiB received response ceiling, 64 KiB/100-record inline ceiling, 20-second call timeout, two read-only transient retries, and bounded concurrency.
- Completeness is explicit: complete, paginated, filtered, sampled, or truncated. Opaque cursors are integrity protected and target/capability/version bound.
- Large results are stored with tenant/workflow/capability/target scope, lineage, hash, classification, timestamps, counts, and expiry; every read reauthorizes.
- Cancellation propagates. Mutations are not blindly retried after dispatch. Unknown outcomes remain distinct.

## Errors, telemetry, health, and operations

- Stable typed errors cover validation/authn/authz/approval/target/version/backend/rate/timeout/cancel/conflict/partial/size/unknown outcome/internal stages.
- Structured trace/audit events contain identifiers, versions, target references, decisions, timings, counts, redaction flags, and relationship observations, never credentials or raw unbounded payloads.
- `/health` means process health; `/ready` checks safe configuration and dependency bindings without mutating Jira.
- Emergency disablement is enforced by Registry/catalog/policy state. Rollback is the previous exact package version or per-capability deny; disabling does not delete the locked inventory.

## Testing and release

Contract, functional, security, mutation-safety, Result Store, observability, Registry/catalog, exact inventory, adapter-version, cancellation/retry, and evaluation suites are mandatory. No live production mutation is part of automated testing.
