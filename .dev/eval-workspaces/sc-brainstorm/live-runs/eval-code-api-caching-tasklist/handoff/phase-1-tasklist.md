# Phase 1 -- Foundations

Establish the cache governance foundation before any endpoint serves cached responses. This phase defines endpoint policy, eligibility, scope, and key correctness requirements.

### T01.01 -- Define endpoint cache-policy registry artifact

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The merged requirements require an endpoint cache-policy registry as the control plane for eligibility, TTL, key dimensions, invalidation, rollout state, and ownership. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | cache, api contract |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**

- Cache policy registry specification covering endpoint identifier, eligibility, TTL, key dimensions, invalidation source, stale-if-error eligibility, rollout flag, policy version, owner, and reviewer.

**Steps:**

1. **[PLANNING]** Load the merged requirements and identify all FR1 policy fields.
2. **[PLANNING]** Check dependencies on endpoint inventory and security classification.
3. **[EXECUTION]** Draft the registry field list and required validation rules.
4. **[EXECUTION]** Define how policy version, owner, and reviewer are represented.
5. **[VERIFICATION]** Run quality-engineer review against FR1 and acceptance criteria.
6. **[COMPLETION]** Write evidence and unresolved assumptions to the deliverable artifacts.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0001/spec.md` exists and names every FR1 cache-policy field.
- The registry specification rejects cached endpoints with missing eligibility, TTL, key dimensions, invalidation source, rollout flag, owner, or reviewer.
- The registry specification is repeatable for additional endpoints without changing its structure.
- Evidence links the registry fields back to `merged-requirements.md` FR1.

**Validation:**

- Manual check: reviewer confirms every FR1 field appears in the registry specification.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0001/evidence.md`.

**Dependencies:** R-001
**Rollback:** TBD (if not specified in roadmap)

### T01.02 -- Create endpoint sensitivity classification matrix

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Caching is disabled by default until endpoints are classified as public, tenant-scoped, user-scoped, confidential, or non-cacheable. |
| Effort | M |
| Risk | High |
| Risk Drivers | security, data, all |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**

- Endpoint sensitivity classification matrix with approval requirements for each class.

**Steps:**

1. **[PLANNING]** Load FR2 and identify each required classification category.
2. **[PLANNING]** Check blockers for unknown endpoint inventory or security review process.
3. **[EXECUTION]** Define classification criteria for public, tenant-scoped, user-scoped, confidential, and non-cacheable responses.
4. **[EXECUTION]** Define approval requirements for each classification.
5. **[VERIFICATION]** Run quality-engineer review for leakage and approval gaps.
6. **[COMPLETION]** Record classification evidence and unresolved endpoint questions.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0002/spec.md` exists and contains all five FR2 classification categories.
- Tenant-scoped, user-scoped, confidential, and regulated responses require explicit policy and security approval.
- Classification rules consistently default unknown endpoints to non-cacheable until reviewed.
- Evidence links each category to `merged-requirements.md` FR2.

**Validation:**

- Manual check: reviewer confirms unknown or sensitive endpoints cannot be cached by default.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0002/evidence.md`.

**Dependencies:** T01.01
**Rollback:** TBD (if not specified in roadmap)

### T01.03 -- Inventory approved read-endpoint scope

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Initial caching scope is limited to safe, idempotent read endpoints and excludes mutation, auth/session, and secret-bearing endpoints. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/notes.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**

- Approved read-endpoint scope list and exclusion list.

**Steps:**

1. **[PLANNING]** Load FR3 and identify included endpoint classes.
2. **[PLANNING]** Check blockers for unknown API framework and endpoint inventory.
3. **[EXECUTION]** Define included read endpoint classes for list, detail, reference data, computed summaries, and public metadata.
4. **[EXECUTION]** Define excluded endpoint classes for mutation, auth/session, secrets, and credential material.
5. **[VERIFICATION]** Validate the scope list against FR3.
6. **[COMPLETION]** Record scope evidence and unresolved inventory gaps.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0003/spec.md` exists and lists included and excluded endpoint classes from FR3.
- Mutation, auth/session, secret-bearing, and credential-bearing endpoints are excluded by default.
- The scope list can be regenerated from the same merged requirements without changing classifications.
- Evidence links scope decisions to `merged-requirements.md` FR3.

**Validation:**

- Manual check: reviewer confirms the approved scope excludes non-read and sensitive endpoint classes.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Dependencies:** T01.02
**Rollback:** TBD (if not specified in roadmap)

### T01.04 -- Specify cache key correctness tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Cache keys must include every response-shaping dimension to prevent incorrect or cross-tenant responses. |
| Effort | L |
| Risk | High |
| Risk Drivers | security, data, cache |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/notes.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**

- Cache key dimension test plan covering route, path parameters, query parameters, API version, tenant, authorization, content negotiation, locale/region, and feature flags.

**Steps:**

1. **[PLANNING]** Load FR4 and AC2 to identify required dimensions.
2. **[PLANNING]** Check blockers for unknown authorization and feature-flag models.
3. **[EXECUTION]** Define positive and negative key-variation checks for each dimension.
4. **[EXECUTION]** Define normalization checks for query and path parameters.
5. **[VERIFICATION]** Run quality-engineer review for missing response-shaping dimensions.
6. **[COMPLETION]** Record key-test evidence and unresolved model assumptions.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0004/spec.md` exists and names every FR4 key dimension.
- The test plan proves tenant, authorization, API version, query, and content negotiation variations produce distinct entries when responses differ.
- Query and path normalization checks are deterministic and repeatable.
- Evidence links each key dimension to `merged-requirements.md` FR4 and AC2.

**Validation:**

- Manual check: reviewer confirms no FR4 key dimension is missing from the test plan.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Dependencies:** T01.01, T01.02, T01.03
**Rollback:** TBD (if not specified in roadmap)

### T01.05 -- Checkpoint: End of Phase 01

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Gate: verify outputs of tasks T01.01-T01.04 before continuing. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Purpose:** Confirm policy, classification, scope, and key-correctness artifacts are ready for build planning.

**Verification:**

- Confirm `TASKLIST_ROOT/artifacts/D-0001/spec.md` exists.
- Confirm `TASKLIST_ROOT/artifacts/D-0002/spec.md` exists.
- Confirm `TASKLIST_ROOT/artifacts/D-0004/spec.md` exists.

**Exit Criteria:**

- Cache policy registry fields are complete.
- Sensitivity classification defaults unknown endpoints to non-cacheable.
- Cache key test plan covers FR4 dimensions.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.04
**Rollback:** N/A (checkpoints are read-only verifications)
