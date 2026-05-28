# Phase 2 -- Build Controls

Define the operational controls that make endpoint caching safe under mutation, outage, traffic spikes, and bounded-staleness scenarios. This phase converts cache behavior into implementable requirements for invalidation, purge, fallback, stampede protection, and stale-if-error gates.

### T02.01 -- Define expiration and invalidation plan

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | All cached endpoints require TTL expiration, and mutation-affected resources require event-driven or mutation-hook invalidation. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | data, cache |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/notes.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**

- Expiration and invalidation requirements covering TTL, mutation hooks, event-driven invalidation, and short-TTL/no-cache fallback.

**Steps:**

1. **[PLANNING]** Load FR5 and identify TTL and invalidation requirements.
2. **[PLANNING]** Check blockers for unknown event source or mutation model.
3. **[EXECUTION]** Define TTL requirements for every cached endpoint policy.
4. **[EXECUTION]** Define mutation-driven invalidation requirements and waiver criteria.
5. **[VERIFICATION]** Run quality-engineer review for stale-read failure modes.
6. **[COMPLETION]** Record invalidation evidence and unknown event-source questions.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0005/spec.md` exists and distinguishes TTL, event-driven invalidation, and no-cache fallback.
- Mutation-affected cached resources require invalidation or documented short-TTL/no-cache rationale.
- Invalidation requirements can be applied repeatedly per endpoint policy.
- Evidence links requirements to `merged-requirements.md` FR5 and AC3.

**Validation:**

- Manual check: reviewer confirms every mutation-affected cached resource has an invalidation or no-cache path.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Dependencies:** T01.01, T01.04
**Rollback:** TBD (if not specified in roadmap)

### T02.02 -- Specify manual purge controls

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Operators must be able to purge cache entries by supported scopes and receive explicit failure signals when purge propagation fails. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | audit, all |
| Tier | STRICT |
| Confidence | [██████████] 95% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/notes.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**

- Manual purge control requirements for global, endpoint, resource, tenant/cohort, and policy-version scopes.

**Steps:**

1. **[PLANNING]** Load FR6 and AC5 to identify purge scopes and audit fields.
2. **[PLANNING]** Check blockers for unknown cache replica topology.
3. **[EXECUTION]** Define required purge scopes and failure signaling behavior.
4. **[EXECUTION]** Define audit fields for actor, time, scope, and reason.
5. **[VERIFICATION]** Run quality-engineer review for purge propagation and audit gaps.
6. **[COMPLETION]** Record purge evidence and unknown topology assumptions.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0006/spec.md` exists and lists all FR6 purge scopes.
- Purge failures across replicas produce explicit failure signals.
- Manual purge audit requirements include actor, time, scope, and reason.
- Evidence links purge requirements to `merged-requirements.md` FR6 and AC5.

**Validation:**

- Manual check: reviewer confirms all purge scopes and audit fields are present.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Dependencies:** T02.01
**Rollback:** TBD (if not specified in roadmap)

### T02.03 -- Define cache fallback behavior

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Cache backend failures must not take down the API layer or bypass authorization. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | security, cache |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/notes.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**

- Cache fallback behavior plan covering origin fallback, controlled errors, alerting, and authorization preservation.

**Steps:**

1. **[PLANNING]** Load FR7 and AC6 to identify fallback constraints.
2. **[PLANNING]** Check blockers for unknown origin behavior under outage.
3. **[EXECUTION]** Define origin read-through fallback and controlled-error conditions.
4. **[EXECUTION]** Define alerts and safety checks that prevent authorization bypass.
5. **[VERIFICATION]** Run quality-engineer review for outage and leakage scenarios.
6. **[COMPLETION]** Record fallback evidence and unresolved origin assumptions.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0007/spec.md` exists and specifies origin fallback and controlled-error behavior.
- Cache failure handling never bypasses authorization or changes tenant isolation.
- Fallback behavior can be tested under cache backend outage conditions.
- Evidence links fallback behavior to `merged-requirements.md` FR7 and AC6.

**Validation:**

- Manual check: reviewer confirms cache outage behavior fails safely without data leakage.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Dependencies:** T01.02, T02.01
**Rollback:** TBD (if not specified in roadmap)

### T02.04 -- Specify stampede and stale-if-error controls

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008, R-009 |
| Why | Hot-key stampedes and stale-if-error behavior can overload origin systems or serve unsafe stale responses if not explicitly controlled. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | performance, latency, data |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena; Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/notes.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**

- Stampede protection and stale-if-error gating requirements.

**Steps:**

1. **[PLANNING]** Load FR8, FR9, AC8, and AC9.
2. **[PLANNING]** Check blockers for unknown cache backend capabilities.
3. **[EXECUTION]** Define acceptable stampede protection mechanisms.
4. **[EXECUTION]** Define stale-if-error approval, forbidden cases, and bounded stale window requirements.
5. **[VERIFICATION]** Run quality-engineer review for traffic spike and stale authorization risks.
6. **[COMPLETION]** Record control evidence and unresolved backend capability questions.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/artifacts/D-0008/spec.md` exists and names at least one approved stampede protection mechanism.
- Stale-if-error is forbidden for revocation-sensitive and sensitive endpoints unless explicitly approved.
- Hot-key simultaneous-expiry behavior is covered by the validation plan.
- Evidence links controls to `merged-requirements.md` FR8, FR9, AC8, and AC9.

**Validation:**

- Manual check: reviewer confirms stampede and stale-if-error controls address FR8 and FR9.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Dependencies:** T01.02, T02.03
**Rollback:** TBD (if not specified in roadmap)

### T02.05 -- Checkpoint: End of Phase 02

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Gate: verify outputs of tasks T02.01-T02.04 before continuing. |
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
| Deliverable IDs | D-CP02 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`

**Purpose:** Confirm invalidation, purge, fallback, stampede, and stale-if-error artifacts are ready for rollout planning.

**Verification:**

- Confirm `TASKLIST_ROOT/artifacts/D-0005/spec.md` exists.
- Confirm `TASKLIST_ROOT/artifacts/D-0006/spec.md` exists.
- Confirm `TASKLIST_ROOT/artifacts/D-0008/spec.md` exists.

**Exit Criteria:**

- Mutation-affected resources have invalidation or no-cache rationale.
- Manual purge scopes and audit fields are specified.
- Stale-if-error is gated by endpoint safety classification.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.04
**Rollback:** N/A (checkpoints are read-only verifications)
