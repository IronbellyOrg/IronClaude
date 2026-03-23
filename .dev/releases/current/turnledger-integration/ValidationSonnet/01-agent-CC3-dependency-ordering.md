# CC3: Dependency Chain and Ordering Validation Report

**Agent**: CC3 — Dependency Chain and Ordering Constraints
**Spec**: v3.3-requirements-spec.md
**Roadmap**: v3.3-TurnLedger-Validation/roadmap.md
**Date**: 2026-03-23

---

## Validation Findings

---

### CC3-1: Phase 1 — No Dependency / Can Start Immediately

- **Spec constraint**: "Phase 1: Infrastructure (No production changes) … **Dependency**: None. Can start immediately." (Spec §Phased Implementation Plan, Phase 1)
- **Roadmap response**: Phase 1 header: "**Duration**: ~3 days (range: 2–4) … **Objective**: Build the two cross-cutting infrastructure pieces that all subsequent phases depend on." The Timeline Summary row for Phase 1 lists "**Blocked By**: —" (em-dash, i.e., nothing). (Roadmap §Timeline Summary)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — correctly sequenced.
- **Recommended correction**: None required.

---

### CC3-2: Phase 2 — Hard Dependency on Phase 1 (Audit Trail Fixture)

- **Spec constraint**: "Phase 2: Test Coverage … **Dependency**: Phase 1 (audit trail fixture must exist)." (Spec §Phased Implementation Plan, Phase 2)
- **Roadmap response**: Phase 2 header explicitly states: "**Hard dependency**: Phase 1A (audit trail fixture must exist)." (Roadmap §Phase 2: Core E2E Test Suites)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — correctly stated.
- **Recommended correction**: None required.
- **Note**: The roadmap narrows the dependency to Phase 1A specifically (rather than all of Phase 1, which includes 1B). This is accurate because Phase 2 tests need the audit trail fixture (1A) but do not require the AST analyzer (1B). The narrowing is correct and appropriate.

---

### CC3-3: Phase 3 — Hard Dependency on Phase 1 (AST Analyzer) and Phase 2 (Baseline)

- **Spec constraint**: "Phase 3: Pipeline Fixes … **Dependency**: Phase 1 (AST analyzer must exist). Phase 2 establishes baseline." (Spec §Phased Implementation Plan, Phase 3)
- **Roadmap response**: Phase 3 header states: "**Hard dependency**: Phase 1B (AST analyzer), Phase 2 (tests exist to validate fixes)." (Roadmap §Phase 3: Pipeline Fixes + Reachability Gate Integration)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — correctly stated and accurately decomposed to Phase 1B.
- **Recommended correction**: None required.
- **Note**: The roadmap correctly identifies Phase 1B (not all of Phase 1) as the relevant dependency for the AST analyzer. This is a legitimate and more precise restatement of the spec's "Phase 1 (AST analyzer must exist)."

---

### CC3-4: Phase 4 — Hard Dependency on All Previous Phases

- **Spec constraint**: "Phase 4: Validation … **Dependency**: Phases 1-3 complete." (Spec §Phased Implementation Plan, Phase 4)
- **Roadmap response**: Phase 4 header states: "**Hard dependency**: All previous phases complete." (Roadmap §Phase 4: Regression Validation + Final Audit)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — correctly stated.
- **Recommended correction**: None required.

---

### CC3-5: FR-4 Infrastructure (AST Analyzer) in Phase 1 Before FR-4.3 Gate Integration in Phase 3

- **Spec constraint**: FR-4.2 (AST call-chain analyzer, standalone module) is listed under Phase 1, item 3: "FR-4.2: AST call-chain analyzer (standalone module)." FR-4.3 (Reachability Gate Integration) is listed under Phase 3: "FR-4.3: Reachability gate integration." (Spec §Phased Implementation Plan, Phase 1 and Phase 3)
- **Roadmap response**: Task 1B.2 places the AST call-chain analyzer module (`src/superclaude/cli/audit/reachability.py`) in Phase 1B. Task 3A.4 places the `GateCriteria`-compatible gate interface (FR-4.3) in Phase 3. (Roadmap §1B: AST Reachability Analyzer and §3A: Production Code Changes)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — ordering is correct; the analyzer module exists before gate integration attempts to use it.
- **Recommended correction**: None required.

---

### CC3-6: Critical Path — Phase 3 Omitted from Roadmap's Stated Critical Path

- **Spec constraint**: Phase dependencies form a chain: Phase 1 → Phase 2 (depends on Phase 1) → Phase 3 (depends on Phase 1 and Phase 2) → Phase 4 (depends on Phases 1-3). This implies Phase 3 is on the critical path between Phase 2 and Phase 4. (Spec §Phased Implementation Plan)
- **Roadmap response**: "**Critical path**: Phase 1A → Phase 2 → Phase 4. Phase 1B can run in parallel with Phase 1A but must complete before Phase 3." (Roadmap §Timeline Summary)
- **Verdict**: PARTIALLY_RESPECTED
- **Severity**: MEDIUM
- **Impact**: The stated critical path "Phase 1A → Phase 2 → Phase 4" skips Phase 3. This is technically defensible only if Phase 3 can run in parallel with something and still complete before Phase 4 begins. However, Phase 4 has a hard dependency on all previous phases including Phase 3. The critical path omission is misleading: Phase 3 IS on the critical path to Phase 4 (since Phase 4 hard-depends on Phase 3). The roadmap's critical path statement is incomplete at minimum, and misleading at worst. The parallel note about Phase 1B is correct but unrelated to the Phase 3 omission.
- **Recommended correction**: Update the critical path statement to read: "**Critical path**: Phase 1A → Phase 2 → Phase 3 → Phase 4. Phase 1B runs in parallel with Phase 1A and must complete before Phase 3 begins." This accurately reflects the full dependency chain the spec establishes.

---

### CC3-7: FR-6.2 T02 (Confirming Test for run_post_phase_wiring_hook) — Placement in Phase 2

- **Spec constraint**: "FR-6.2: v3.2 Gaps — T02: `run_post_phase_wiring_hook()` call — Already verified WIRED — write confirming test." FR-6.2 is listed under Phase 2, item 4: "FR-6.1–FR-6.2: QA gap closure tests." (Spec §FR-6.2 and §Phased Implementation Plan, Phase 2)
- **Roadmap response**: Task 2D.5 states: "FR-6.2 T02 | `tests/v3.3/test_wiring_points_e2e.py` | Confirming test for `run_post_phase_wiring_hook()` (may overlap 2A.3)" in Phase 2D. (Roadmap §2D: Remaining QA Gaps)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — correctly placed in Phase 2.
- **Recommended correction**: None required. The "(may overlap 2A.3)" notation is appropriate—task 2A.3 already covers FR-1.7 (post-phase wiring hook, both paths), so 2D.5 serves as a gap-closure audit step. The file placement (`test_wiring_points_e2e.py`) is consistent with 2A.3.

---

### CC3-8: Test File Layout — FR-3.2a-d Assigned to test_gate_rollout_modes.py vs. Spec's test_budget_exhaustion.py

- **Spec constraint**: "Test File Layout" specifies two separate files: `test_gate_rollout_modes.py` for FR-3.1–FR-3.3 and `test_budget_exhaustion.py` for FR-3.2a–FR-3.2d. (Spec §Test File Layout)
- **Roadmap response**: Task 2C.2 assigns FR-3.2a–FR-3.2d (4 budget exhaustion tests) to `tests/v3.3/test_gate_rollout_modes.py`. No `test_budget_exhaustion.py` file is mentioned anywhere in the roadmap. The "New Files Created" table does not include `test_budget_exhaustion.py`. (Roadmap §2C: Gate Rollout Mode Matrix and §New Files Created)
- **Verdict**: VIOLATED
- **Severity**: MEDIUM
- **Impact**: The spec's file layout is a declared organizational constraint intended to keep budget exhaustion scenarios isolated for independent review and traceability. Folding FR-3.2a-d into `test_gate_rollout_modes.py` violates the spec's layout and may complicate audit trail traceability, as the audit JSONL `test_id` fields would reference the wrong test file in the audit record vs. spec. Third-party verification relies on the spec's declared file layout matching actual artifact locations.
- **Recommended correction**: Either (a) create `tests/v3.3/test_budget_exhaustion.py` as a separate file for FR-3.2a-d and update the "New Files Created" table accordingly, or (b) explicitly acknowledge the deviation in the roadmap with a rationale note. Option (a) is preferred to maintain spec fidelity.

---

### CC3-9: Phase 4 Task 4.2 (Grep-Audit for no mock.patch) — Implicit Dependency on Phase 2 Tests Existing

- **Spec constraint**: No explicit ordering statement for this check in the spec. The spec requires "No mocks on gate functions" (§Constraints) as a cross-cutting rule, but the grep audit step itself is not phased in the spec. The implied dependency is that there must be test files to grep before a grep-audit is meaningful.
- **Roadmap response**: Task 4.2: "Grep-audit: confirm no `mock.patch` on gate functions or orchestration logic across all v3.3 test files." This is placed in Phase 4, after Phase 2 (which produces all v3.3 test files). (Roadmap §Phase 4: Regression Validation + Final Audit)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — the grep-audit is correctly sequenced after Phase 2 delivers all test files. Running it before Phase 2 would produce false-clean results (no test files → no violations found).
- **Recommended correction**: None required. To make the implicit dependency explicit, the roadmap could optionally note: "Meaningful only after Phase 2 test files exist," but this is cosmetic.

---

### CC3-10: Phase 4 Task 4.4 (Manifest Completeness Check) — Implicit Dependency on Phase 1B (Manifest Exists)

- **Spec constraint**: No explicit ordering statement for this check in the spec. FR-4.1 (wiring manifest) is placed in Phase 1, and the validation step in Phase 4 would be meaningless without a manifest to check against. The implied dependency is Phase 1B must complete before manifest completeness can be validated.
- **Roadmap response**: Task 4.4: "Validate wiring manifest completeness: every known wiring point from FR-1 has a manifest entry." Placed in Phase 4, after Phase 1B (which produces `tests/v3.3/wiring_manifest.yaml` at task 1B.4). Phase 4 hard dependency states "All previous phases complete," which includes Phase 1. (Roadmap §Phase 4 and §1B: AST Reachability Analyzer)
- **Verdict**: RESPECTED
- **Severity**: LOW
- **Impact**: N/A — the "All previous phases complete" dependency on Phase 4 transitively covers Phase 1B manifest creation. The manifest (1B.4) will exist by the time task 4.4 executes.
- **Recommended correction**: None required. The catch-all "All previous phases complete" dependency on Phase 4 is sufficient to ensure the manifest exists. An explicit call-out would be clearer but is not strictly necessary.

---

## Summary

| Check | Title | Verdict | Severity |
|-------|-------|---------|----------|
| CC3-1 | Phase 1 — No Dependency / Can Start Immediately | RESPECTED | LOW |
| CC3-2 | Phase 2 — Hard Dependency on Phase 1A (Audit Trail Fixture) | RESPECTED | LOW |
| CC3-3 | Phase 3 — Hard Dependency on Phase 1B + Phase 2 | RESPECTED | LOW |
| CC3-4 | Phase 4 — Hard Dependency on All Previous Phases | RESPECTED | LOW |
| CC3-5 | AST Analyzer (1B.2) in Phase 1 Before Gate Integration (3A.4) in Phase 3 | RESPECTED | LOW |
| CC3-6 | Critical Path Statement Omits Phase 3 | PARTIALLY_RESPECTED | MEDIUM |
| CC3-7 | FR-6.2 T02 Confirming Test Placed in Phase 2 (task 2D.5) | RESPECTED | LOW |
| CC3-8 | FR-3.2a-d Assigned to test_gate_rollout_modes.py, Not test_budget_exhaustion.py | VIOLATED | MEDIUM |
| CC3-9 | Task 4.2 Grep-Audit Depends on Phase 2 Tests Existing | RESPECTED | LOW |
| CC3-10 | Task 4.4 Manifest Check Depends on Phase 1B (Manifest Exists) | RESPECTED | LOW |

**Total ordering checks**: 10
**Respected**: 8
**Violated**: 1
**Partially respected**: 1

---

## Agent Recommendation

Two issues require roadmap correction before implementation begins:

1. **CC3-6 (MEDIUM)**: The critical path statement should include Phase 3. The omission creates a planning ambiguity—implementers might deprioritize Phase 3 relative to Phase 4, not realizing Phase 4 is gated on Phase 3 completing fully. The fix is a one-line update to the Timeline Summary section.

2. **CC3-8 (MEDIUM)**: The spec's Test File Layout is a declared organizational constraint. Folding `test_budget_exhaustion.py` scenarios into `test_gate_rollout_modes.py` violates it. The preferred resolution is to create the separate file as specified, or to record an explicit deviation with rationale in the roadmap. This is not a logic error (the tests would still run) but it is a fidelity gap against the spec.

All eight remaining dependency chains are correctly represented in the roadmap. Phase sequencing is sound: infrastructure before tests, tests before production fixes, all before final validation.
