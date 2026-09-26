# Prompt: Review a Tool

```text
Act as an independent tool-contract and security reviewer.

Target tool:
<PATH OR CAPABILITY ID>

Read:
- docs/agent-platform/04-TOOL_DESIGN_STANDARD.md
- docs/agent-platform/09-MCP_GATEWAY_STANDARD.md
- docs/agent-platform/10-RESULT_STORE_STANDARD.md
- docs/agent-platform/12-SECURITY_AND_APPROVAL_MODEL.md
- docs/agent-platform/14-EVALUATION_STANDARD.md
- docs/agent-platform/16-AGENT_REGISTRY_AND_DEPENDENCY_MAP_STANDARD.md

First apply the admission test again. Determine whether the tool should exist or should be replaced by reuse, Code Mode, ordinary code, or a skill. Inspect its Registry identity, owner, lifecycle, version, dependents, and declared/observed relationships.

Then inspect:
- Name, description, positive and negative selection cues
- Semantic overlap with existing tools
- Input/output/error schemas and versioning
- Target/environment ambiguity behavior
- Output bounds, pagination, completeness, provenance, and Result Store handoff
- Read/write classification, side effects, permissions, and approval
- Timeout, cancellation, retry, idempotency, preconditions, partial failure, and unknown outcomes
- Secret handling, injection controls, tenant isolation, audit, and redaction
- Discovery tests, contract tests, security tests, and trace evaluation
- Registry-to-catalog projection, dependency compatibility, change impact, and topology-drift handling

Report findings by severity with concrete evidence and minimum fixes. Flag any hidden mutation, arbitrary query/command input, unbounded output, false completeness, permission inferred from discovery, or blind mutation retry as blocking.

Return Pass / Conditional / Fail. Do not modify the implementation unless separately authorized.
```
