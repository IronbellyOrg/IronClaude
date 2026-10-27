# Adversarial Review
**Date**: 2026-03-23
**Depth**: Standard adversarial pass (Steps 4.1–4.9)

---

## Step 4.1 — Fresh Re-Read Assessment

Re-read both documents with adversarial lens. Key observations before challenging COVERED assessments:

1. The roadmap is a single well-structured document with 4 phases, 8 appendix integration points, and a comprehensive risk table. The Executive Summary is accurate in its delivery outcome claims with notable exception: it claims FR-7.3 and FR-7.1 are addressed but the schema field count is inconsistent.

2. The spec has a subtle ordering anomaly: FR-1.21 appears *between* FR-1.7 and FR-1.8 numerically, which means any extraction algorithm scanning sequentially would miss it if it expected FR-1.8 to follow FR-1.7.

3. The roadmap's 2A task table explicitly lists "FR-1.1–FR-1.18" as its coverage range. This is a precision claim that excludes FR-1.19, FR-1.20, FR-1.21 by name. This is not a vague gap — it's an explicit boundary that leaves three requirements outside scope.

---

## Step 4.2 — COVERED Assessment Challenges

### Challenge 1: REQ-017 (FR-1.14 BLOCKING lifecycle) — UPHELD as COVERED

**Claim**: 3 tests (2A.9) covering format→debit→recheck→restore/fail.
**Challenge**: Does roadmap specify both branches of the recheck outcome? Spec says "on recheck pass: task status restored to PASS, wiring turns credited" AND "on recheck fail: task status remains FAIL."
**Finding**: Roadmap 2A.9 says "3 tests: BLOCKING remediation lifecycle: format → debit → recheck → restore/fail" — the "restore/fail" captures both branches. UPHOLD COVERED.

### Challenge 2: REQ-024 (FR-2.1 convergence path) — UPHELD as COVERED

**Claim**: Task 2B.1 covers debit/credit/reimburse cycle.
**Challenge**: Spec FR-2.1 requires three assertions: (1) budget cycle, (2) budget_snapshot recorded in registry, (3) budget logging includes consumed/reimbursed/available.
**Finding**: Roadmap 2B.1 says "execute_fidelity_with_convergence() E2E — debit CHECKER_COST → run checkers → credit CONVERGENCE_PASS_CREDIT → reimburse_for_progress(); budget_snapshot recorded" — verbatim match including budget_snapshot. UPHOLD COVERED.

### Challenge 3: REQ-042 (FR-4.3 GateCriteria integration) — DOWNGRADE to PARTIAL

**Claim**: Task 3A.4 covers GateCriteria-compatible interface.
**Challenge**: Spec FR-4.3 says the gate "integrates with existing GateCriteria infrastructure" and produces "structured report: PASS: All required targets reachable; FAIL: List of unreachable targets with spec references." Roadmap 3A.4 says "Add GateCriteria-compatible interface: reads manifest, runs AST analysis, produces structured PASS/FAIL report."
**Finding**: UPHOLD COVERED — roadmap exactly mirrors spec language. GateCriteria infrastructure integration is explicitly named.

### Challenge 4: REQ-057 (FR-7.2 verifiability properties) — UPHELD as COVERED

**Claim**: Task 1A.4 covers 4 verifiability properties.
**Challenge**: Spec FR-7.2 names 4 specific properties. Does roadmap 1A.4 enumerate all 4?
**Finding**: Roadmap 1A.4 says "confirm JSONL output meets 4 third-party verifiability properties (real timestamps, spec-traced, runtime observations, explicit verdict)" — matches all 4. UPHOLD COVERED.

### Challenge 5: REQ-029 (FR-3.1 mode matrix 4 criteria) — UPHELD as COVERED

**Claim**: 2C.1 covers all 4 verification criteria for each mode.
**Challenge**: Spec FR-3.1 says each mode test must verify 4 things: TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording. Does roadmap preserve all 4?
**Finding**: Roadmap 2C.1 says "Each verifies: TaskStatus/GateOutcome, TurnLedger state, DeferredRemediationLog entries, ShadowGateMetrics recording" — verbatim. UPHOLD COVERED.

---

## Step 4.3 — Orphan Requirements Search

### Pattern Scan Results

**Pattern 1: Modal requirements** — `(shall|must|required to|needs to)`

Spec matches found and checked:

- L78: "Tests MUST NOT mock gate functions" → REQ-002, COVERED in Phase 4 task 4.2. ✓
- L312: "Each release spec declares a wiring_manifest section" → REQ-039, COVERED (partial). ✓
- L398: "assert it detects the gap and references the correct spec (v3.2-T02)" → REQ-043, COVERED. ✓
- L479: "A third party with no prior knowledge MUST be able to determine" → REQ-057, COVERED. ✓
- L648: "UV only — uv run pytest, not python -m pytest" → REQ-NFR2. ✓
- L649: "No mocks on gate functions" → REQ-NFR1. ✓
- L650: "Branch from v3.0-v3.2-Fidelity" → REQ-PROC2. Roadmap mentions this? **CHECK**: Roadmap says "Branch from v3.0-v3.2-Fidelity" in Resource Requirements section — IMPLICIT COVERED. Low finding generated below.
- L652: "Audit trail: Every test must emit a JSONL record" → REQ-NFR4. COVERED in Checkpoint B, but see CC4 finding about Phase 2D/3B tests.

**Pattern 2: Negation requirements** — `(must not|shall not|never|prohibited|forbidden)`

- L78: "Tests MUST NOT mock gate functions" → Already extracted.
- No additional orphan negation requirements found.

**Pattern 3: Quantitative NFRs** — `(at least|at most|within|maximum|minimum) \d+`

- L83: "at least one E2E test" → REQ-001, COVERED. ✓
- L547: "Test count ≥ 20" → REQ-SC1, PARTIAL (GAP-H008). ✓
- L551: "≥4894 passed, ≤3 pre-existing failures" → REQ-NFR3, COVERED. ✓
- L554: "4 modes × 2 paths = 8+ scenarios" → REQ-SC3, COVERED. ✓

**Pattern 4: Conditional** — `(if|when|unless) .{5,40} (must|shall|should)`

- L397: "If files_analyzed == 0 AND source directory is non-empty: return a FAIL report" → REQ-044, PARTIAL (GAP-M002). ✓

**New orphan found via Pattern 1:**

### ADV-001: Branch constraint weakly mapped
- **Type**: ORPHAN_REQUIREMENT (weak coverage)
- **Severity**: LOW
- **Spec**: `v3.3-requirements-spec.md:L650 (Constraints)` — *"Branch from v3.0-v3.2-Fidelity"*
- **Roadmap**: `roadmap.md:Resource Requirements` — *"v3.0-v3.2-Fidelity branch | All | Medium | Must be stable; any upstream changes require rebase"* — mentioned as a dependency, not as a process requirement to be enforced
- **Impact**: Low — the branch constraint is informational. No implementer would start work on main instead of the correct branch. Already exists as REQ-PROC2 IMPLICIT.
- **Verdict**: VALID-LOW

---

## Step 4.4 — Orphan Roadmap Tasks

Tasks in roadmap with no spec traceability:

| Task | Roadmap location | Has spec backing? | Type |
|------|-----------------|-------------------|------|
| 4.6: Update docs/memory/solutions_learned.jsonl | Phase 4 task 4.6 | NO — "—" in requirement column | Team practice |
| Appendix A sections A.1–A.9 | Appendix A | NO explicit FR mapping | Supplemental architecture doc |

**Assessment**: Task 4.6 is a team practice task with no spec requirement. It does not conflict with any spec requirement and does not introduce risk. Flagged as informational orphan. Appendix A is documentation that adds value.

### ADV-002: Task 4.6 orphan — solutions_learned.jsonl
- **Type**: ORPHAN_TASK
- **Severity**: LOW (informational)
- **Roadmap**: `roadmap.md:Phase 4 task 4.6` — *"Update docs/memory/solutions_learned.jsonl with v3.3 patterns"*
- **Spec backing**: None — requirement column is "—"
- **Verdict**: VALID-LOW (team practice, does not conflict)

---

## Step 4.5 — Sequencing and Dependency Validation

### Finding: Checkpoint B scope ambiguity

**Issue**: Checkpoint B states "All E2E tests pass; SC-1 through SC-6, SC-8, SC-12 validated." But SC-1 cannot be validated at Checkpoint B without FR-1.19, FR-1.20, and FR-1.21 tasks existing. This is a structural issue that means Checkpoint B's criteria are unachievable as written.

### ADV-003: Checkpoint B success criteria unachievable without GAP-H001/H002/H003 fixes
- **Type**: SEQUENCING_ERROR
- **Severity**: HIGH
- **Spec evidence**: `v3.3-requirements-spec.md:SC-1` — *"All 20+ wiring points have ≥1 E2E test"*
- **Roadmap evidence**: `roadmap.md:Validation Checkpoint B` — *"SC-1 through SC-6, SC-8, SC-12 validated"*
- **Impact**: Checkpoint B is defined as a gate before Phase 3 can proceed. If SC-1 cannot be satisfied (because FR-1.19/1.20/1.21 have no tasks), Phase 3 cannot proceed under the roadmap's own sequencing.
- **Recommended correction**: After adding tasks 2A.13–2A.15, Checkpoint B becomes achievable. Alternatively, defer SC-1 validation to Checkpoint D and remove it from Checkpoint B.
- **Verdict**: VALID-HIGH

---

## Step 4.6 — Silent Assumption Detection

### Pattern scan: `(assumes|assuming|given that|prerequisite|depends on)`

- Roadmap:1B: "Hard dependency: Phase 1A" → explicit, not silent.
- Roadmap:3: "Hard dependency: Phase 1B, Phase 2" → explicit.
- Roadmap:4: "Hard dependency: All previous phases complete" → explicit.

### Pattern scan: `(existing|current|already|previously) .{5,40} (service|system|API|database|table|endpoint)`

- Roadmap:2A.3: "Existing injection seam" (re: _subprocess_factory) → spec confirms this is stable.
- Roadmap:2D.1: "Extend existing 7 tests (verify already present)" → **assumption: 7 tests already exist in test_convergence_wiring.py**. The file exists but no agent verified the 7-test count inside it. This is a silent assumption.

### ADV-004: Silent assumption — test_convergence_wiring.py contains 7 tests
- **Type**: SILENT_ASSUMPTION
- **Severity**: MEDIUM
- **Roadmap evidence**: `roadmap.md:2D.1` — *"Extend existing 7 tests (verify already present, add any missing)"*
- **Impact**: If the existing file contains fewer than 7 tests covering T07 scope, the "verify already present" path fails silently and SC-8 cannot be satisfied.
- **Recommended correction**: Add explicit verification step: "Check test count in test_convergence_wiring.py against T07 test IDs before declaring 2D.1 complete"
- **Verdict**: VALID-MEDIUM (not a new gap — absorbed into GAP-H006 correction)

---

## Step 4.7 — Test Coverage Mapping Validation

**Spec test count (FR-1)**: FR-1.1 through FR-1.21 = 21 named subtests.
**Roadmap claim**: "~21 tests" in 2A subtotal. However, this is achieved by counting FR-1.14 as 3 tests (2A.9) while FR-1.19, FR-1.20, FR-1.21 have zero tasks. The count is numerically inflated.

**Spec test count (FR-2)**: 4 subtests (FR-2.1, FR-2.1a, FR-2.2, FR-2.3, FR-2.4 = 5 items). Roadmap maps to 4 tasks (2B.1–2B.4), omitting FR-2.1a.

**Spec test count (FR-3)**: FR-3.1a-d (4) + FR-3.2a-d (4) + FR-3.3 (1) = 9 spec items. Roadmap: 2C.1 (8 tests) + 2C.2 (4 tests) + 2C.3 (1 test) = 13 tests. Count ≥ spec items. ✓

**Spec test count (FR-6)**: T07 (7), T11 (6), T12 (1), T14 (1), T02 (1), T17-T22 (6) = ~22 tests. Roadmap maps all 6 gap items.

---

## Step 4.8 — Adversarial Findings Summary

New findings not already in gap registry:

| Finding | Type | Severity | Status |
|---------|------|----------|--------|
| ADV-001 | ORPHAN_REQUIREMENT (weak) | LOW | VALID-LOW |
| ADV-002 | ORPHAN_TASK | LOW | VALID-LOW |
| ADV-003 | SEQUENCING_ERROR | HIGH | VALID-HIGH |
| ADV-004 | SILENT_ASSUMPTION | MEDIUM | Absorbed into GAP-H006 |

---

## Step 4.9 — Updated Score After Adversarial Pass

ADV-003 is a new HIGH finding. Total HIGH findings: **10** (was 9).

| Metric | Pre-Adversarial | Post-Adversarial |
|--------|----------------|-----------------|
| HIGH findings | 9 | 10 |
| MEDIUM findings | 5 | 5 |
| LOW findings | 2 | 4 |
| Verdict | NO_GO | NO_GO |

**Verdict unchanged**: NO_GO. ADV-003 confirms Checkpoint B is internally inconsistent under the current roadmap, but does not change the fundamental verdict since NO_GO was already triggered by >3 HIGH findings and weighted coverage <85%.

---

## What the Parallel Agents Missed

1. **ADV-003 (Checkpoint B inconsistency)**: Domain agents focused on per-requirement coverage. The cascading impact on Checkpoint B sequencing was a systemic view not naturally captured by individual domain agents.
2. **ADV-001 (branch constraint)**: The Constraints section at the bottom of the spec was lightly covered — domain agents focused on their FR sections. The branch constraint is low-severity but represents systematic under-extraction of the Constraints section.
3. **ADV-004 (test_convergence_wiring.py count assumption)**: Domain agent D6 flagged the language weakness but did not name the silent assumption explicitly.
