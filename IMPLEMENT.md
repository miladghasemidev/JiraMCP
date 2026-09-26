# End-to-End Codex Implementation Task: Jira MCP On-Premises

You are the principal engineer responsible for delivering this Jira MCP project from authoritative inputs through tested implementation and final conformance audit.

Do not stop after analysis or planning. Work through the complete lifecycle described below, using resumable internal batches where needed.

## 0. Governing instructions

Read `AGENTS.md` first and follow it exactly.

Then read:

- `PROJECT_DECISIONS.yaml`
- `docs/adr/ADR-0001-approved-jira-tool-inventory.md`
- `docs/adr/ADR-0002-standards-and-scope-precedence.md`
- the complete vendored `agent-platform-standards/` package, beginning with its `AGENTS.md`, `README.md`, and `00-IMPLEMENTATION_WORKFLOW.md`

The standards snapshot is pinned and must not be edited.

The approved Jira capability matrix controls scope. The standards control implementation conformance.

## 1. Hard prerequisite: validate the real approved matrix

Find the real project input matching:

`project-inputs/APPROVED_JIRA_CAPABILITY_MATRIX.*`

Ignore `MATRIX_REQUIRED.md`, `README.md`, and any file explicitly marked placeholder/example.

Parse the source faithfully. Preserve exact capability identifiers, names, Jira product/version support, backend operations/endpoints, read/write semantics, permissions, limitations, and any implementation notes present in the matrix.

Before writing implementation code, prove that the source resolves to exactly **114 distinct approved MCP tool capabilities**.

Create:

- `specs/APPROVED_CAPABILITY_INVENTORY.json`
- `specs/APPROVED_CAPABILITY_INVENTORY.md`
- `IMPLEMENTATION_STATUS.md`

The machine-readable inventory must preserve a reference back to the source row/cell/section for every capability.

If the real matrix is absent, cannot be parsed reliably, or does not resolve to exactly 114 approved tools:

1. do not invent or infer tool names;
2. do not start implementation;
3. report exactly what is missing or inconsistent;
4. stop with status `BLOCKED_INPUT_MATRIX`.

This is the only permitted early stop before implementation.

## 2. Scope invariant

For the 114 approved capabilities:

- do not add;
- do not remove;
- do not merge;
- do not split;
- do not silently rename;
- do not substitute with another tool, Skill, Code Mode operation, or agent-only behavior.

The generic new-tool admission decision has already been completed for this approved matrix and must not reopen scope.

Apply the standards to the implementation of all 114 capabilities.

If concrete Jira-version evidence proves one approved capability cannot be implemented as approved, preserve it in all inventories and mark it `BLOCKED_ARCHITECTURE_REVIEW` with:

- exact capability ID;
- affected Jira product/version;
- concrete API/backend evidence;
- why no conformant implementation exists;
- what decision is required.

Do not create a substitute capability.

## 3. Establish the implementation architecture

Inspect the repository before choosing files or libraries.

If this is a new/empty implementation repository and the authoritative inputs do not mandate another stack, use:

- Python 3.12 or newer;
- a currently supported official MCP SDK;
- typed request/response models;
- pinned dependency versions;
- an asynchronous HTTP client suitable for Jira REST calls;
- strict linting/type checking/testing appropriate to the selected stack.

Do not hard-code secrets or production endpoints.

Isolate Jira product/version differences behind version-aware backend adapters. Do not scatter version conditionals across tool handlers.

The architecture must provide clear boundaries for at least:

- MCP server bootstrap and transport;
- capability registration;
- validated configuration;
- Jira connection/target resolution;
- authentication integration;
- Jira REST/backend client;
- version-aware Jira adapters;
- authorization/policy context;
- approval enforcement for mutations;
- standard result envelope;
- typed error mapping;
- pagination and completeness state;
- bounded-output enforcement;
- Result Store integration boundary;
- trace/correlation propagation;
- audit and metrics integration boundary;
- Registry and Capability Catalog metadata;
- health/readiness;
- cancellation, timeout, retry, and partial-failure behavior.

External enterprise components such as the Gateway, secret broker, Result Store, identity provider, audit backend, or policy engine must be represented by strict integration interfaces when their implementation is outside this repository. Do not fabricate a production service. Provide test fakes where required and fail closed for missing production controls.

Record material architecture choices in project ADRs under `docs/adr/`.

## 4. Produce specifications before implementation

Follow the pinned standards workflow.

Create a complete Jira MCP server specification based on:

`agent-platform-standards/templates/MCP_TEMPLATE.md`

Store it under:

`specs/mcp/`

For every one of the 114 approved tools, create a complete tool specification based on:

`agent-platform-standards/templates/TOOL_TEMPLATE.md`

Store each under:

`specs/tools/`

Do not leave material template fields as invented values. Resolve them from the matrix, standards, Jira semantics, and repository configuration. When a genuinely external organization-specific value is unavailable, define a clearly named configuration/policy binding rather than embedding a false value.

Each tool specification must make explicit, as applicable:

- stable capability ID and contract version;
- approved Jira product/version support;
- purpose and negative-use guidance;
- input schema and validation;
- target/environment semantics;
- output schema;
- record/byte/time/page limits;
- pagination/cursor behavior;
- completeness/truncation semantics;
- Result Store handoff;
- provenance and collection time;
- R0/R1/R2/W1/W2/W3 classification;
- exact side effects;
- required permissions;
- approval class;
- idempotency behavior;
- preconditions/concurrency semantics;
- verification behavior;
- timeout/cancellation/retry policy;
- Jira/backend error mapping;
- partial-failure behavior;
- unknown mutation outcome behavior;
- security and injection controls;
- trace/metrics/audit fields;
- Registry relationships;
- test requirements;
- deprecation/disablement behavior.

Create security-review specifications for sensitive or mutating capability groups using:

`agent-platform-standards/templates/SECURITY_REVIEW_TEMPLATE.md`

Create evaluation specifications using:

`agent-platform-standards/templates/EVAL_TEMPLATE.md`

Do not wait for a separate user prompt after specifications are complete. Continue to implementation unless a truly blocking decision meets the criteria in `AGENTS.md`.

## 5. Implement the shared Jira MCP foundation

Build shared infrastructure before duplicating behavior across 114 handlers.

At minimum implement or define conformant integration boundaries for:

### Configuration and target resolution

- explicit environment selection;
- explicit Jira base target selection;
- supported-version declaration and validation;
- safe configuration precedence;
- no production default;
- no secrets in ordinary configuration.

### Authentication and credentials

Support only authentication modes justified by the authoritative Jira inputs and supported Jira versions.

Credentials must come from an approved external mechanism/configuration reference and must never enter model-facing tool arguments or telemetry.

### Jira client

Implement:

- connection/session management;
- request timeout;
- cancellation where supported by the stack;
- bounded retries for typed retryable failures;
- no blind retry of unknown-outcome mutations;
- safe HTTP/Jira error normalization;
- pagination helpers that preserve backend semantics;
- response-size protection;
- version-aware endpoint/adaptor selection;
- deterministic serialization of approved fields.

### Standard result and error contracts

Conform to the vendored standard schemas and preserve:

- status;
- capability ID/version;
- trace ID;
- collection timestamp;
- data or authorized result reference;
- completeness state;
- record/byte counts;
- cursor where applicable;
- provenance;
- warnings;
- typed errors and retryability.

### Policy and approval boundary

Enforce capability, target, environment, risk class, and parameter-aware authorization.

For W1-W3 tools implement required policy/approval behavior. W2/W3 must not become executable merely because the tool exists.

Approval must bind to the normalized exact action and become invalid when material target/parameter/version details change.

### Result Store boundary

Implement an interface that supports large-output storage and bounded projection. In test/dev, use a safe fake or local test implementation if no production Result Store is supplied.

Possession of a result reference must not itself imply authorization.

### Observability and audit

Propagate trace IDs and emit structured events without raw secrets or unbounded Jira payloads.

### Registry and Capability Catalog

Generate project Registry entries and catalog projection metadata from the 114 approved implementations. Maintain stable IDs and declared relationships.

## 6. Implement all 114 approved tools

Implement tools in logical internal batches, but continue automatically from one batch to the next.

For each capability:

1. read the exact approved matrix row and its generated specification;
2. verify supported Jira version behavior;
3. implement only that approved semantic capability;
4. reuse shared client/validation/error/output/security infrastructure;
5. implement strict typed input/output schemas;
6. enforce hard limits;
7. preserve Jira pagination and completeness semantics;
8. classify and enforce read/write behavior;
9. add Registry and catalog metadata;
10. add focused tests before marking the capability implemented;
11. update `IMPLEMENTATION_STATUS.md`.

Never create a generic unrestricted `jira.request`, arbitrary URL fetch, or arbitrary REST execution tool merely to cover missing implementations unless such a capability is explicitly present and approved in the matrix and separately passes all required security controls.

Do not implement business workflow reasoning inside an atomic Jira tool unless the approved capability itself is a deterministic cohesive backend operation.

Use deterministic code for bulk pagination, filtering, joins, aggregation, polling, or batch orchestration outside atomic capability handlers where appropriate.

## 7. Test comprehensively

Create and run tests required by the standards and by each tool specification.

At minimum cover:

### Contract tests

- schema validity;
- required/optional fields;
- boundary values;
- stable identifiers;
- version compatibility;
- error envelope validity;
- completeness state;
- exact cursor/pagination behavior.

### Functional tests

- happy path;
- empty result;
- not found;
- maximum allowed result;
- pagination;
- filtering where approved;
- partial backend failure;
- unsupported Jira version;
- backend unavailable;
- timeout;
- cancellation;
- retryable errors;
- non-retryable errors.

### Security tests

- missing authentication;
- insufficient permission;
- policy deny precedence;
- ambiguous environment;
- ambiguous target;
- cross-environment/tenant isolation where applicable;
- secret redaction;
- malicious Jira content/prompt-injection text;
- oversized input/output;
- untrusted URL/path/template input where applicable;
- approval absence/expiry/replay/change;
- idempotency behavior;
- unknown mutation outcome;
- forbidden write through read tool.

### Result Store and observability tests

- large output stored rather than injected inline;
- projection limits;
- authorization on result access;
- trace propagation;
- audit field presence;
- prohibited payload redaction;
- Registry/catalog projection validation.

Use mocked/fixture Jira backends for deterministic automated tests. Do not require real production mutations to pass the test suite.

## 8. Evaluate against the agent-platform release gates

Create evaluation cases sufficient to exercise capability selection metadata, security constraints, exact-value handling, failure behavior, and output contracts as required by the standards.

Treat all standard hard failures as release blockers, including:

- unauthorized mutation;
- approval bypass;
- secret exposure;
- cross-environment/tenant access;
- unmanaged/forbidden component invocation;
- fabricated evidence;
- false execution claims;
- prompt-injection compliance;
- ambiguous destructive target selection;
- critical exact-value corruption.

Record evaluation results under `evals/` or another clearly documented project path.

## 9. Perform an independent conformance review

After implementation and tests, perform a new review pass as if you were an independent architecture/security/reliability reviewer.

Use the vendored review prompts as checklists:

- `agent-platform-standards/prompts/REVIEW_MCP.md`
- `agent-platform-standards/prompts/REVIEW_TOOL.md`

For this Jira project, do not use the generic review admission step to delete/merge/split an already-approved matrix capability. Review whether the approved capability is implemented conformantly.

Create:

`CONFORMANCE_REVIEW.md`

For every finding provide:

- severity;
- evidence with file/line or test reference;
- violated requirement;
- impact;
- smallest corrective action.

Then fix all blocking and accepted findings that can be corrected without changing the approved scope. Re-run affected tests/evaluations and update the review.

Do not stop merely after reporting findings.

## 10. Final scope reconciliation

Generate:

`FINAL_CAPABILITY_RECONCILIATION.md`

Compare the final implementation against the original approved matrix row by row.

The report must prove:

- authoritative approved count: 114;
- implemented count;
- `BLOCKED_ARCHITECTURE_REVIEW` count;
- missing count: 0;
- unapproved extra tool count: 0;
- merged/split/substituted count: 0;
- `IMPLEMENTED + BLOCKED_ARCHITECTURE_REVIEW = 114`.

For each blocked capability include the evidence and architecture decision required.

## 11. Final release audit

Create:

`FINAL_RELEASE_AUDIT.md`

Audit at least:

- standards snapshot and ADR compliance;
- exact 114-tool scope accounting;
- MCP and tool specifications;
- typed contracts;
- supported Jira versions;
- input/output limits;
- Result Store behavior;
- auth/authz and approvals;
- mutation safety;
- errors/retry/idempotency/cancellation;
- secret handling;
- observability/audit;
- Registry/Dependency Map/Capability Catalog;
- tests;
- evaluation gates;
- health/readiness;
- deployment configuration;
- rollback/disablement;
- unresolved risks.

The final line must be exactly one of:

`RELEASE_READY`

or

`NOT_RELEASE_READY`

Do not output `RELEASE_READY` when any standards hard gate, security blocker, scope mismatch, missing approved tool, unapproved extra tool, or unresolved critical defect remains.

## 12. Work-management behavior

Keep `IMPLEMENTATION_STATUS.md` current throughout the run. It must be sufficient to resume after interruption and include, at minimum:

- capability ID;
- source matrix reference;
- specification status;
- implementation status;
- test status;
- review status;
- final status;
- blocker/evidence reference.

Continue autonomously through the 114 capabilities. Use internal batches for maintainability, not as user approval gates.

Do not ask the user routine implementation questions already controlled by the standards or repository.

Do not claim completion based only on code generation or compilation. Completion requires the specifications, implementation, tests, evaluation, independent review/fixes, Registry/catalog metadata, and final 114-row reconciliation required above.
