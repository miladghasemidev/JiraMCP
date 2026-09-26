# Prompt: Implement an Approved Platform Change

```text
Implement only the approved change below:
<APPROVED SPECIFICATION AND ADR REFERENCES>

Read AGENTS.md, `docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md`, and every standard named by the approved specification. Treat MUST and MUST NOT as release gates.

Before editing:
1. Verify the approval status and exact scope.
2. Inspect the current implementation, Agent Registry, Dependency Map, Capability Catalog, and unrelated user changes.
3. Identify the smallest file set and the relevant tests/evaluations.
4. Stop if a missing product, architecture, target, permission, or mutation decision materially changes the result.

During implementation:
- Preserve existing compatible contracts and unrelated work.
- Do not add capabilities, permissions, dependencies, data access, or side effects outside scope.
- Update specifications, schemas, Registry entries and relationships, catalog projections, policy, tests, and operations documentation together with code.
- Keep large data outside model context and preserve trace/audit behavior.
- Use reversible migration and rollout steps where possible.

Verification:
- Run focused tests first, then the affected full suite.
- Run security and trace evaluations.
- Validate configuration and schema files.
- Confirm rollback or disablement.
- Validate Registry schema, ownership, lifecycle, dependency compatibility, and direct/transitive change impact.

Final report:
- Outcome
- Files changed
- Tests/evaluations and results
- Contract or migration notes
- Registry and dependency-map changes
- Residual limitations/risks
- Rollback method

Do not deploy or execute external mutations unless the approved request explicitly authorizes them and all required approval controls are active.
```
