# Capability Discovery and Dynamic Loading Standard

## 1. Purpose

The platform MUST search a compact permission-aware Capability Catalog projected from approved Agent Registry entries and dynamically load selected contracts. It MUST NOT place every tool schema and skill body into the model context.

The Agent Registry is the governance source of truth; the Capability Catalog is its runtime discovery view. Their relationship is defined in `16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md`.

## 2. Cataloged artifact types

- MCP tools
- MCP resources
- Skills
- CLI commands
- Deterministic scripts or transformations exposed for orchestration
- Result Store projection operations

Cataloging an artifact does not grant permission to execute it. Unmanaged, disabled, retired, unapproved, incompatible, ownerless, or policy-invalid Registry entries MUST be excluded from ordinary runtime discovery.

## 3. Required catalog metadata

Each entry MUST include:

- Stable capability identifier and version
- Artifact type
- Human title and concise description
- Domain and task intents
- Positive and negative selection cues
- Read/write and risk class
- Required permissions and approval class
- Supported backends, versions, and environments
- Input/output shape summary and output-size class
- Latency and cost class
- Availability status and owner
- Full-schema or skill-content locator
- Deprecation and replacement metadata
- Registry component ID, lifecycle state, last verification date, and declared dependency references

Use `schemas/capability-manifest.schema.json` as the minimum machine-readable contract.

## 4. Discovery sequence

1. Extract task intent, domain, environment, target type, risk, and evidence needs.
2. Apply user authorization, Registry lifecycle, policy, compatibility, and environment availability filters.
3. Search the compact catalog projection using lexical and semantic matching.
4. Prefer exact supported capabilities and existing reusable workflows.
5. Rank by semantic fit, safety, evidence coverage, contract compatibility, reliability, and cost.
6. Load full definitions only for the small selected set.
7. Validate inputs and execution authorization at call time.

## 5. Search behavior

Catalog search SHOULD combine:

- Exact identifiers and aliases
- Domain and task tags
- Lexical matching
- Semantic retrieval
- Policy and compatibility filtering
- Historical reliability signals that cannot override security policy

The catalog MUST prevent deprecated, incompatible, disabled, unmanaged, or unapproved entries from ranking as normal choices.

## 6. Selection rules

The selector MUST:

- Prefer reuse over new creation.
- Prefer the least powerful capability that satisfies the task.
- Prefer read-only evidence collection before mutation.
- Reject capabilities with unsupported target versions.
- Avoid loading overlapping tools when one sufficient capability exists.
- Record candidate set, selected entries, and selection rationale in the trace.

The model's selection is advisory until the gateway authorizes execution.

## 7. Dynamic skill loading

The runtime first loads only skill metadata. After selecting a skill, it MUST read the complete `SKILL.md`. It then loads referenced scripts, queries, or references only as required by the workflow.

If the skill's required capability version or permission is unavailable, the runtime MUST stop, select a documented fallback, or return partial completion. It MUST NOT silently substitute a semantically different tool.

## 8. Catalog quality controls

- Duplicate and overlapping capability detection
- Ownership and review-date enforcement
- Contract-schema validation
- Broken-locator checks
- Deprecation warnings and migration tracking
- Positive and negative retrieval tests
- Permission-filter tests
- Registry-to-catalog projection validation
- Ownerless, unmanaged, disabled, or stale entry exclusion
- Declared-versus-observed dependency-drift reporting

## 9. Discovery fallback

When no capability fits:

1. Recheck whether deterministic code over existing capabilities is sufficient.
2. Recheck whether the request is one-time reasoning.
3. Record the missing reusable backend or workflow capability.
4. Use the capability request template and design-time decision tree.

Do not improvise unrestricted backend access.

## 10. Context budget

Catalog search results MUST be compact. A default candidate set SHOULD contain only enough entries to make a reliable selection, and full definitions SHOULD be limited to selected candidates plus at most a small number of near alternatives needed for disambiguation.

## 11. Metrics

Track top-k selection recall, wrong-tool rate, unnecessary-load rate, unavailable-capability selection, permission-filter correctness, average schemas loaded, context tokens consumed, latency, and fallback rate.

Also track Registry projection lag, unmanaged component count, ownerless component count, stale entry count, and unexpected observed dependency count. These governance signals MUST NOT be used to expose restricted topology to unauthorized users.
