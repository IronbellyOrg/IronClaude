# Phase 1 -- Pre-Implementation Decisions

Establish implementation constraints, resolve all deferred architecture decisions (OQ-A through OQ-J), and freeze the intended design before modifying any behavior. This phase produces the decision log, traceability matrix, and module ownership map that all subsequent phases depend on.

### T01.01 -- Resolve OQ-A/OQ-B GateCriteria.aux_inputs Decision

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002 |
| Why | FR-079 implementation path and FR-088 extended validation deferral depend on whether GateCriteria.aux_inputs exists |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0001/evidence.md`

**Deliverables:**
1. Written decision: OQ-A resolved with chosen option (A or B) and cascading impact on OQ-B/OQ-C documented

**Steps:**
1. **[PLANNING]** Identify `GateCriteria` definition location in `models.py`
2. **[PLANNING]** Check if `aux_inputs` field exists on `GateCriteria`
3. **[EXECUTION]** Inspect `GateCriteria` dataclass definition in `src/superclaude/cli/sprint/models.py`
4. **[EXECUTION]** Document Option A (aux_inputs) vs Option B (frontmatter embedding) decision
5. **[EXECUTION]** Document cascading impact on OQ-B (extended validation) and OQ-C (PRE_APPROVED extraction)
6. **[VERIFICATION]** Confirm decision is recorded with rationale
7. **[COMPLETION]** Write decision to `D-0001/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0001/evidence.md` exists with OQ-A resolution documented
- Decision explicitly states whether Option A or Option B was chosen
- Cascading impact on OQ-B and OQ-C is documented
- OQ-C fully resolved: PRE_APPROVED ID extraction method decided and documented in D-0001/evidence.md
- Decision references the inspected `GateCriteria` definition with field list

**Validation:**
- Manual check: OQ-A decision artifact contains chosen option with rationale
- Evidence: linkable artifact produced at `D-0001/evidence.md`

**Dependencies:** None
**Rollback:** TBD (investigation task; no code changes)
**Notes:** 30-minute task per roadmap estimate. Resolve immediately by inspecting GateCriteria definition.

---

### T01.02 -- Resolve OQ-E/OQ-F and Inspect fidelity.py Signatures

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003, R-004, R-010 |
| Why | OQ-E/OQ-F concern extraction helper function signatures that almost certainly reside in fidelity.py; must confirm, not assume |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0002/evidence.md`

**Deliverables:**
1. Written confirmation of `_extract_fidelity_deviations()` and `_extract_deviation_classes()` signatures, including whether fidelity.py requires modification

**Steps:**
1. **[PLANNING]** Locate `fidelity.py` in the codebase
2. **[PLANNING]** Identify expected function names from roadmap
3. **[EXECUTION]** Inspect `fidelity.py` for `_extract_fidelity_deviations()` signature
4. **[EXECUTION]** Inspect `fidelity.py` for `_extract_deviation_classes()` signature
5. **[EXECUTION]** Determine if fidelity.py requires modification for v2.26 or is inspected-only
6. **[VERIFICATION]** Confirm findings recorded with actual signatures or "not found" disposition
7. **[COMPLETION]** Write findings to `D-0002/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0002/evidence.md` exists with OQ-E and OQ-F resolutions
- Each function signature is documented or explicitly marked "not found — requires creation"
- fidelity.py disposition recorded as "inspected, no modification required" or "modification required with scope"
- Impact on Phase 2 Files Modified table documented

**Validation:**
- Manual check: Both function signatures confirmed or creation plan documented
- Evidence: linkable artifact produced at `D-0002/evidence.md`

**Dependencies:** None
**Rollback:** TBD (investigation task; no code changes)

---

### T01.03 -- Resolve OQ-G/OQ-H/OQ-I Executor Interface Questions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005, R-006, R-007 |
| Why | Confirm build_remediate_step() location, roadmap_run_step() interface for hash injection, and token_count field availability |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0003/evidence.md`

**Deliverables:**
1. Written confirmation of `build_remediate_step()` module location, `roadmap_run_step()` interface, and `token_count` field availability

**Steps:**
1. **[PLANNING]** Identify files containing `build_remediate_step()` and `roadmap_run_step()`
2. **[PLANNING]** Identify Claude subprocess API response structure for token_count
3. **[EXECUTION]** Confirm `build_remediate_step()` module location from v2.24 codebase
4. **[EXECUTION]** Confirm `roadmap_run_step()` interface for post-step hook needed for `roadmap_hash` injection
5. **[EXECUTION]** Verify token-count field availability in Claude subprocess API response (best-effort per NFR-024)
6. **[VERIFICATION]** Confirm all three questions resolved with concrete evidence
7. **[COMPLETION]** Write findings to `D-0003/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0003/evidence.md` exists with OQ-G, OQ-H, OQ-I resolutions
- `build_remediate_step()` module path confirmed
- `roadmap_run_step()` interface documented with hook injection point
- `token_count` availability documented as confirmed or best-effort fallback defined

**Validation:**
- Manual check: All three executor interface questions resolved with codebase evidence
- Evidence: linkable artifact produced at `D-0003/evidence.md`

**Dependencies:** None
**Rollback:** TBD (investigation task; no code changes)

---

### T01.04 -- Document OQ-J FR-077 Dual-Budget-Exhaustion Handling

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | v2.26 must document handling for FR-077 dual-budget-exhaustion; mechanism deferred to v2.26 |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0004/notes.md`

**Deliverables:**
1. Written documentation of v2.26 handling for FR-077 (placeholder behavior) and v2.26 deferral

**Steps:**
1. **[PLANNING]** Review FR-077 requirements from roadmap
2. **[PLANNING]** Confirm v2.26 deferral scope
3. **[EXECUTION]** Document v2.26 placeholder behavior for dual-budget-exhaustion note in `_print_terminal_halt()`
4. **[EXECUTION]** Document what v2.26 will implement
5. **[VERIFICATION]** Confirm documentation covers both v2.26 behavior and v2.26 deferral
6. **[COMPLETION]** Write to `D-0004/notes.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0004/notes.md` exists with FR-077 handling documented
- v2.26 placeholder behavior explicitly described
- v2.26 deferral scope documented
- No implementation ambiguity remains for Phase 4 T04.07

**Validation:**
- Manual check: FR-077 handling document covers both current and deferred behavior
- Evidence: linkable artifact produced at `D-0004/notes.md`

**Dependencies:** None
**Rollback:** TBD (documentation task; no code changes)

---

### T01.05 -- Verify Architecture Constraints Against Codebase

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Must verify no modifications to generic pipeline layer, no new executor primitives, no normal reads of dev-*-accepted-deviation.md, acyclic dependency hierarchy |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0005/evidence.md`

**Deliverables:**
1. Architecture constraint verification report confirming 4 constraints hold against live codebase

**Steps:**
1. **[PLANNING]** List the 4 architecture constraints from roadmap
2. **[PLANNING]** Identify files to inspect for each constraint
3. **[EXECUTION]** Verify no modifications to `pipeline/executor.py` and `pipeline/models.py` are planned
4. **[EXECUTION]** Verify no new executor primitives (Step, GateCriteria, SemanticCheck reuse only)
5. **[EXECUTION]** Verify no normal execution reads of `dev-*-accepted-deviation.md`
6. **[EXECUTION]** Verify module dependency hierarchy remains acyclic
7. **[VERIFICATION]** Confirm all 4 constraints verified with evidence
8. **[COMPLETION]** Write verification report to `D-0005/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0005/evidence.md` exists with all 4 constraints verified
- Each constraint has explicit pass/fail with evidence
- No constraint violations found (or violations escalated as blockers)
- Import graph analysis confirms acyclic dependencies

**Validation:**
- Manual check: All 4 architecture constraints verified against live codebase
- Evidence: linkable artifact produced at `D-0005/evidence.md`

**Dependencies:** None
**Rollback:** TBD (verification task; no code changes)

---

### Checkpoint: Phase 1 / Tasks 1-5

**Purpose:** Verify all open questions except OQ-J have been investigated and architecture constraints confirmed.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P01-T01-T05.md`
**Verification:**
- All OQ-A through OQ-I resolutions documented in evidence artifacts
- Architecture constraint report complete with 4 verified constraints
- No unresolved blocker that would force Phase 2 rework
**Exit Criteria:**
- D-0001 through D-0005 artifacts exist and are non-empty
- All investigation questions have concrete answers (not "TBD")
- No constraint violation escalated as blocker

---

### T01.06 -- Decide _parse_routing_list() Module Placement

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Circular import risk must be resolved before Phase 2; mid-phase refactor would collapse timeline estimates |
| Effort | S |
| Risk | Medium |
| Risk Drivers | Cross-cutting scope (import graph impact) |
| Tier | EXEMPT |
| Confidence | [████████░░] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0006/notes.md`

**Deliverables:**
1. Module placement decision: `_parse_routing_list()` in `remediate.py` or extracted to new `parsing.py`, with import graph analysis

**Steps:**
1. **[PLANNING]** Review import graph between `gates.py`, `remediate.py`, and `executor.py`
2. **[PLANNING]** Identify circular import risk if placed in `remediate.py`
3. **[EXECUTION]** Analyze import dependencies for both placement options
4. **[EXECUTION]** Choose placement using tie-breaker rules: prefer no new dependencies, then reversible, then fewest interface changes
5. **[VERIFICATION]** Confirm chosen placement does not introduce circular imports
6. **[COMPLETION]** Document decision in `D-0006/notes.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0006/notes.md` exists with placement decision
- Import graph analysis shows no circular dependency with chosen placement
- Decision is actionable for Phase 2 T02.03 implementation
- If new module `parsing.py` chosen, file creation scope documented

**Validation:**
- Manual check: Import graph analysis confirms no circular dependency risk
- Evidence: linkable artifact produced at `D-0006/notes.md`

**Dependencies:** None
**Rollback:** TBD (decision task; no code changes)
**Notes:** Tie-breaker applied: prefer remaining in remediate.py (no new external dependencies) unless circular import detected.

---

### T01.07 -- Produce Decision Log, Traceability Matrix, and Module Map

| Field | Value |
|---|---|
| Roadmap Item IDs | R-012, R-013, R-014, R-015 |
| Why | Phase 0 deliverables: implementation decision log, requirement traceability matrix, module ownership map, and test plan |
| Effort | M |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [████████░░] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007, D-0008 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0007/spec.md`
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0008/spec.md`

**Deliverables:**
1. Implementation decision log consolidating all OQ resolutions and architecture decisions
2. Requirement traceability matrix mapping requirement -> file(s) -> test(s) -> milestone, plus confirmed module ownership map and test plan aligned to SC-1 through SC-10

**Steps:**
1. **[PLANNING]** Gather all resolved OQ decisions from T01.01-T01.06
2. **[PLANNING]** Map FR requirements to source files and test files
3. **[EXECUTION]** Compile implementation decision log with all OQ resolutions
4. **[EXECUTION]** Build requirement traceability matrix (requirement -> file -> test -> milestone)
5. **[EXECUTION]** Document module ownership map including fidelity.py disposition
6. **[EXECUTION]** Create test plan aligned to SC-1 through SC-10
7. **[VERIFICATION]** Cross-check every OQ has an entry in the decision log
8. **[COMPLETION]** Write decision log to `D-0007/spec.md` and traceability matrix to `D-0008/spec.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0007/spec.md` exists with all 8 OQ resolutions consolidated
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0008/spec.md` exists with traceability matrix, module map, and test plan
- Every requirement (FR-xxx) mentioned in roadmap appears in the traceability matrix
- Module ownership map includes confirmed `_parse_routing_list()` placement decision from T01.06 (D-0006)
- Test plan section present as distinct section within D-0008/spec.md, mapping each SC-1 through SC-10 to test file paths and verification methods

**Validation:**
- Manual check: Decision log contains entries for OQ-A through OQ-J; traceability matrix maps all FR requirements
- Evidence: linkable artifacts produced at `D-0007/spec.md` and `D-0008/spec.md`

**Dependencies:** T01.01, T01.02, T01.03, T01.04, T01.05, T01.06
**Rollback:** TBD (documentation task; no code changes)

---

### T01.08 -- Validate Phase 1 Exit Criteria

| Field | Value |
|---|---|
| Roadmap Item IDs | R-016 |
| Why | Gate check: all 8 open questions resolved, fidelity.py inspected, _parse_routing_list() placed, no unresolved rework-forcing decisions |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████░] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0009/evidence.md`

**Deliverables:**
1. Phase 1 exit criteria checklist with all 5 criteria verified

**Steps:**
1. **[PLANNING]** Load Phase 0 exit criteria from roadmap (5 checkboxes)
2. **[PLANNING]** Gather evidence from T01.01-T01.07 artifacts
3. **[EXECUTION]** Verify: all 8 open questions resolved or deferred with documented fallback
4. **[EXECUTION]** Verify: fidelity.py inspection complete with scope impact documented
5. **[EXECUTION]** Verify: _parse_routing_list() module placement decided
6. **[EXECUTION]** Verify: no unresolved decision that could force rework in gates, parsing, or executor resume flow
7. **[VERIFICATION]** Verify: architecture constraint verification complete against live codebase
8. **[COMPLETION]** Write exit criteria verification to `D-0009/evidence.md`

**Acceptance Criteria:**
- File `.dev/releases/current/v2.26-roadmap-v5/artifacts/D-0009/evidence.md` exists with all 5 exit criteria checked
- Each criterion references the artifact(s) that provide evidence
- No criterion marked as unverified or pending
- Phase 2 is unblocked

**Validation:**
- Manual check: All 5 Phase 0 exit criteria verified with artifact references
- Evidence: linkable artifact produced at `D-0009/evidence.md`

**Dependencies:** T01.07
**Rollback:** TBD (validation task; no code changes)

---

### Checkpoint: End of Phase 1

**Purpose:** Confirm all pre-implementation decisions are finalized and Phase 2 (Foundation) can begin without risk of rework.
**Checkpoint Report Path:** `.dev/releases/current/v2.26-roadmap-v5/checkpoints/CP-P01-END.md`
**Verification:**
- All 8 OQ resolutions documented and consolidated in decision log
- Architecture constraints verified; no violations found
- Module placement for `_parse_routing_list()` decided with import graph evidence
**Exit Criteria:**
- D-0001 through D-0009 artifacts exist and are non-empty
- Phase 1 exit criteria checklist (D-0009) shows all 5 criteria verified
- No unresolved decision remains that could force rework in subsequent phases
