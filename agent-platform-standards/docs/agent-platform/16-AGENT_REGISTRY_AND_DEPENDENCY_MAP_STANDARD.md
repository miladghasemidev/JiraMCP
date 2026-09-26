# Agent Registry and Dependency Map Standard

## 1. Purpose

The Agent Registry is the authoritative inventory of agent-platform components, their ownership, versions, lifecycle state, risk, permissions, endpoints, and declared relationships. The Dependency Map is the governed graph derived from declared metadata and observed runtime traces.

Together they answer:

- What agents, MCP servers, tools, skills, models, gateways, endpoints, backends, and knowledge sources exist?
- Who owns and supports each component?
- Which components are approved, active, deprecated, disabled, unmanaged, or ownerless?
- What does each component use, provide, invoke, read, write, or route through?
- What will be affected if a component changes, fails, is revoked, or is compromised?
- Do declared dependencies match actual runtime behavior?

## 2. Registry versus Capability Catalog

The Capability Catalog and Agent Registry are related but not identical.

| Capability Catalog | Agent Registry |
|---|---|
| Optimized for runtime discovery and selection | Optimized for governance and complete inventory |
| Primarily indexes tools, skills, resources, and callable operations | Includes agents, runtimes, models, MCP servers, gateways, endpoints, backends, policies, and data sources |
| Contains compact selection metadata | Contains ownership, lifecycle, security, deployment, evaluation, and relationship metadata |
| May be permission-filtered per request | Maintains the governed system of record |

The Capability Catalog SHOULD be generated as a permission-aware runtime projection of approved active Registry entries. It MUST NOT become an independent conflicting source of truth.

## 3. Required component types

The Registry MUST support at least:

- `agent`
- `mcp_server`
- `tool`
- `skill`
- `model`
- `runtime`
- `cli`
- `gateway`
- `endpoint`
- `backend`
- `knowledge_source`
- `result_store`
- `policy`
- `evaluation_suite`

Organizations MAY add types, but their semantics and relationship rules MUST be versioned.

## 4. Required common metadata

Every component MUST record:

- Stable registry identifier
- Type, name, description, and semantic version
- Owner team and technical contact
- Lifecycle status
- Creation, last modification, last verification, and next review dates
- Supported environments and deployment instances
- Risk class and data classifications
- Permission and approval-policy references
- Source repository and immutable release or artifact reference
- Configuration or manifest locator, without secret values
- Observability and evaluation references
- Declared dependencies and dependents
- Deprecation, replacement, disablement, and rollback information

A production component without an owner, version, environment, or policy reference is nonconformant.

## 5. Type-specific metadata

### 5.1 Agent

Record purpose, positive/negative selection cues, runtime, models, skills, tool permissions, channels, audiences, autonomy level, maximum execution budget, memory/KMS access, approval behavior, and evaluation status.

### 5.2 MCP server

Record transport, gateway route, provided tool/resource versions, authentication method, backend targets, network zone, health/readiness endpoint, supported backend versions, and operational owner.

### 5.3 Tool

Record capability ID, providing MCP server, input/output/error schema versions, read/write class, side effects, limits, permissions, approval class, Result Store behavior, and deprecation replacement.

### 5.4 Skill

Record skill package/version, triggers, required capabilities and minimum versions, risk class, evaluation suite, supported targets, and active deployment instances.

### 5.5 Model

Record provider or local runtime, model/version, approved data classifications, region or hosting boundary, context limits, cost/latency class, intended tasks, fallback policy, and evaluation baseline.

### 5.6 Backend or knowledge source

Record target type, environment, owner, access boundary, data classification, approved capability paths, supported versions, residency, and availability expectations. Do not store credentials.

### 5.7 Runtime, CLI, gateway, and shared platform services

Record exact release version, deployment environments, supported contract versions, owners, routes, policy bindings, observability, evaluation coverage, and dependencies. A CLI entry MUST identify the gateway and capability-contract versions it can invoke; it MUST NOT encode hidden direct-backend routes.

## 6. Relationship model

Dependencies MUST be represented as directed, typed edges. Supported relationship types SHOULD include:

- `uses`
- `requires`
- `provides`
- `invokes`
- `routes_through`
- `connects_to`
- `reads_from`
- `writes_to`
- `runs_on`
- `governed_by`
- `evaluated_by`
- `depends_on`
- `replaces`

Each relationship MUST record:

- Source and target registry IDs
- Relationship type and direction
- Environment and optional target scope
- Required or optional status
- Declared, observed, or both
- Minimum/maximum compatible version when applicable
- Data classification or access mode when relevant
- First seen, last seen, and observation count for runtime relationships
- Evidence reference, such as a manifest, configuration revision, or trace query

## 7. Static and runtime topology

The Dependency Map MUST combine two sources without confusing them:

### 7.1 Declared topology

Generated from reviewed manifests, skill requirements, MCP/tool contracts, deployment configuration, policies, and ADRs. It represents intended architecture.

### 7.2 Observed topology

Generated from authorized runtime traces and gateway/MCP telemetry. It represents actual calls and data-access paths.

### 7.3 Reconciliation

The platform MUST detect and report:

- Observed relationship with no approved declaration
- Declared required dependency never observed within its expected period
- Version or endpoint mismatch
- Disabled or deprecated component still invoked
- Production component absent from the Registry
- Ownerless or stale component
- Tool or agent using permissions beyond its registered purpose

An observed edge is evidence of behavior, not automatic approval.

## 8. Lifecycle states

Use explicit lifecycle states:

| State | Meaning |
|---|---|
| `draft` | Defined but not approved for use |
| `review` | Under architecture/security/evaluation review |
| `approved` | Approved but not necessarily deployed |
| `active` | Available in one or more declared environments |
| `deprecated` | Still available during a documented migration period |
| `disabled` | Execution and discovery blocked |
| `retired` | Removed from operation; retained only as governed history |
| `unmanaged` | Discovered but not yet governed; default-denied |

Transitions MUST be authorized, timestamped, and audited. An unmanaged component MUST NOT become executable merely because it was discovered.

## 9. Registration workflow

Before production activation:

1. Create or update the component entry.
2. Assign an accountable owner.
3. Record artifact version and immutable source/release reference.
4. Declare relationships, environments, permissions, and risk.
5. Link specifications, policies, evaluations, and operational controls.
6. Validate the entry and relationship graph against the schema.
7. Run security and evaluation gates.
8. Approve and activate the exact version.
9. Generate the allowed Capability Catalog projection.

Use `templates/AGENT_REGISTRATION_TEMPLATE.md` for agents. MCP, Tool, and Skill specifications MUST supply equivalent Registry metadata through their own templates.

## 10. Discovery and shadow components

The platform SHOULD ingest component metadata automatically from approved CI/CD pipelines and supported runtimes. Runtime telemetry MAY identify unregistered components or relationships.

Discovered unknown components MUST be marked `unmanaged`, assigned a triage owner, excluded from ordinary discovery, and default-denied until reviewed. Automatic discovery MUST NOT silently confer trust.

## 11. Ownership and review

- Every active component MUST have an accountable owner and backup owner or owning team.
- Owner departure or team deletion MUST trigger review.
- Stale entries MUST be flagged after a configurable review interval.
- Components with expired evaluation, unsupported dependency versions, or unresolved critical risk MUST be disabled or explicitly excepted through an ADR and risk approval.

## 12. Change-impact analysis

Before changing or retiring a component, query both incoming and outgoing relationships.

The impact report MUST include:

- Direct and transitive dependents
- Environments and deployment instances
- Required contract/version ranges
- Affected agents, skills, MCP servers, policies, data sources, and evaluation suites
- Observed call volume and last use
- Security and data-flow changes
- Migration, test, rollout, and rollback requirements

A high-impact change MUST NOT rely only on declared dependencies when observed traces are available.

## 13. Security and visibility

- Registry read access MUST be permission-aware because topology can reveal sensitive systems and data flows.
- Editing ownership, status, permissions, endpoints, policies, or relationships is a privileged audited action.
- Secret values MUST never be stored in Registry metadata.
- Dependency views MUST redact targets and classifications the viewer cannot access.
- Deleting history MUST follow audit and retention policy.
- Registry and topology APIs MUST enforce tenant and environment isolation.

## 14. Dependency health and operational use

The Registry SHOULD incorporate health and compatibility signals without becoming the source of raw telemetry. It may show:

- Current availability and last health observation
- Error and latency status
- Contract compatibility
- Evaluation status
- Policy or approval readiness
- Deprecation and end-of-support warnings

Operational state must identify its timestamp and source.

## 15. Minimum administrative capabilities

The platform SHOULD provide controlled operations to:

- Register, update, deprecate, disable, and retire components
- Search and filter by type, owner, status, risk, environment, and capability
- Show direct and transitive relationships
- Find ownerless, unmanaged, stale, risky, or over-permissioned components
- Compare declared and observed topology
- Perform change-impact analysis
- Export a permission-filtered inventory
- Audit registry changes

## 16. Implementation guidance

The initial implementation MAY use a relational database with component and relationship tables. A dedicated graph database is not required initially. Add a graph database only when measured traversal, scale, or topology-query requirements justify it.

Recommended logical model:

```text
registry_component
registry_component_version
registry_deployment
registry_relationship
registry_relationship_observation
registry_owner
registry_policy_binding
registry_evaluation_status
registry_audit_event
```

The Registry is a control-plane service. Request execution SHOULD continue to use the gateway and runtime catalog projection rather than making every tool call depend on a large Registry query.

## 17. MVP boundary

Required from the beginning:

- Registry schema and stable IDs
- Component ownership and lifecycle state
- Declared dependency registration
- CI validation and release gate
- Capability Catalog generated from approved entries

May be delivered later:

- Rich administrative UI
- Interactive topology visualization
- Automated trace-derived relationship reconciliation
- Advanced transitive risk and blast-radius analysis
- Dedicated graph storage

Defining the schema early prevents unmanaged agents and MCP servers even when the complete UI is postponed.

## 18. Required tests

- Schema and relationship validation
- Duplicate and stable-ID behavior
- Lifecycle transition authorization
- Ownerless and stale detection
- Tenant/environment visibility controls
- Unmanaged component default-deny
- Declared-versus-observed drift detection
- Version compatibility and deprecation behavior
- Direct and transitive impact analysis
- Catalog projection excludes unauthorized, disabled, or unmanaged entries
- Audit completeness and secret redaction

## 19. Release criteria

An agent-platform component MUST NOT enter production unless its exact version is registered, owned, approved, policy-bound, evaluated, observable, related to its dependencies, and associated with a disablement or rollback method.

## 20. References

- [Google Cloud Agent Registry](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-registry)
- [Google Cloud agent relationships and topology](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/topology)
- [Microsoft 365 Agent Registry](https://learn.microsoft.com/en-ca/microsoft-365/admin/manage/agent-registry)
- [AWS Agent Registry documentation](https://docs.aws.amazon.com/agent-registry/)
