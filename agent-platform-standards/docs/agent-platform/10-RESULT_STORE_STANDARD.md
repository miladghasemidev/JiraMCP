# Result Store Standard

## 1. Purpose

The Result Store keeps large, sensitive, or reusable execution results outside model context. It lets Code Mode and authorized tools operate on full data while the model receives only compact, governed projections.

## 2. Core rule

Raw large datasets MUST NOT be returned directly to the model. Store them and return:

- An opaque result reference
- Data classification and authorization scope
- Schema and provenance summary
- Record and byte counts
- Completeness and truncation status
- Collection and expiry timestamps
- A bounded task-relevant projection or aggregate

## 3. Result object

Each result object MUST include:

- Stable opaque identifier
- Tenant, owner, workflow, and originating capability references
- Contract and schema version
- Creation, collection, and expiration timestamps
- Target/environment references
- Content type, encoding, compression, row and byte counts
- Content hash or integrity metadata
- Classification and access policy
- Provenance and lineage
- Completeness, filter, sample, and truncation metadata
- Parent and derived-result references when applicable

## 4. Access control

Possession of a result reference MUST NOT be sufficient for access. Every read, projection, share, or derivation MUST re-evaluate user, tenant, workflow, purpose, target, and expiry policy.

Opaque references MUST not reveal backend names, query text, tenant identifiers, or sensitive metadata.

## 5. Allowed operations

The store or an adjacent deterministic service MAY support:

- Read a bounded range or page
- Project allowlisted fields
- Filter using a constrained expression model
- Sort, group, and aggregate
- Join explicitly compatible authorized results
- Produce a small sample
- Export to an approved destination
- Delete or shorten retention

Operations MUST preserve lineage and MUST NOT broaden access or classification.

## 6. Context projection

Before entering model context, a projection MUST have explicit maximum records, fields, bytes, and tokens. Sensitive fields MUST be removed or transformed according to policy. The projection MUST state whether it is complete or representative.

## 7. Retention

- Default retention SHOULD be short and task-appropriate.
- Retention MUST respect source-system rules, legal requirements, and user/tenant policy.
- Expiration MUST revoke access and trigger deletion or cryptographic erasure as designed.
- Audit metadata MAY have a different retention period from result content.
- Extending retention is a governed action, not an automatic side effect.

## 8. Security

- Encrypt data in transit and at rest.
- Isolate tenants and environments.
- Use separate authorization for result content and metadata.
- Prevent path traversal, reference guessing, insecure direct object references, and cross-workflow access.
- Scan supported file payloads for malicious active content where applicable.
- Do not execute content stored in a result object.

## 9. Integrity and reproducibility

Derived results MUST record parent references, transformation or script version, parameters, executor identity, and content hash. If a source result changes, the derived result remains tied to the original immutable version.

## 10. Failure behavior

The platform MUST distinguish missing, expired, deleted, corrupted, unauthorized, and temporarily unavailable results. It MUST NOT regenerate a result through side effects without explicit workflow logic.

## 11. Observability and audit

Record create, access, projection, export, share, retention change, and deletion events. Logs MUST contain references and counts, not full sensitive result payloads.

## 12. Anti-patterns

- Putting the full result in a trace and also storing it
- Returning a signed storage URL as the stable public reference
- Treating an opaque ID as authorization
- Keeping all results indefinitely
- Allowing arbitrary code execution over stored results
- Losing provenance during aggregation
- Sending a sample to the model without identifying sampling

## 13. Testing

Test tenant isolation, expiry, authorization changes, field projection, classification preservation, lineage, integrity validation, size limits, deletion, inaccessible references, malicious payloads, concurrent access, and audit completeness.

