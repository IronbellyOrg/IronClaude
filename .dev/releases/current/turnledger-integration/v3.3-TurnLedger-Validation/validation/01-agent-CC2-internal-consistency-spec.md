# Agent CC2: Internal Consistency Check — v3.3 Requirements Spec

**Spec**: `v3.3-requirements-spec.md`
**Date**: 2026-03-23
**Agent**: CC2 (Internal Consistency)

---

## Summary

| Check | Result |
|---|---|
| 1. Section cross-references valid | PASS |
| 2. FR-1 sub-items FR-1.1 through FR-1.18 | PASS |
| 3. FR-3.1 mode matrix has 4 modes (a-d) | PASS |
| 4. FR-3.2 budget scenarios have 4 entries (a-d) | PASS |
| 5. No contradictory statements | WARNING |
| 6. Numeric values consistent | PASS |
| 7. Code State Snapshot table internally consistent | WARNING |
| 8. Wiring manifest (lines 530-586) vs FR-4.1 (lines 280-325) | WARNING |
| 9. Test File Layout matches FR references | WARNING |
| 10. Success Criteria SC-1 through SC-12 all present | PASS |
| 11. Phased Implementation Plan matches FR ordering | PASS |
| 12. Open Questions numbered 1-8 | N/A (section absent) |
| 13. Risk table FR cross-references | WARNING |

**Overall**: PASS with 5 WARNINGS requiring attention before sprint execution.

---

## Detailed Findings

### Check 1: Section Cross-References Valid — PASS

All internal cross-references resolve correctly:

- FR-5.3 (line 384): `"This IS FR-4. Cross-referenced here for traceability."` — FR-4 exists at line 273. VALID.
- Phase 4 validation (line 491): `"every SC-* success criterion"` — SC table exists at lines 511-524. VALID.
- FR-4.3 (line 345): `"Reads the wiring manifest from the release spec"` — manifest present at lines 528-586. VALID.
- FR-6.1 T08/T10 note (line 401): `"already verified fixed in code state snapshot"` — snapshot table at lines 17-46. VALID.
- Phase dependencies (lines 469, 477, 485, 493): Phase 1 → Phase 2 → Phase 3 → Phase 4. Chain is acyclic and complete.

### Check 2: FR-1 Sub-Items FR-1.1 Through FR-1.18 — PASS

All 18 sub-items present and sequentially numbered:

| Sub-item | Line | Title |
|---|---|---|
| FR-1.1 | 80 | TurnLedger Construction Validation |
| FR-1.2 | 89 | ShadowGateMetrics Construction |
| FR-1.3 | 95 | DeferredRemediationLog Construction |
| FR-1.4 | 101 | SprintGatePolicy Construction |
| FR-1.5 | 107 | Phase Delegation — Task Inventory Path |
| FR-1.6 | 115 | Phase Delegation — Freeform Fallback Path |
| FR-1.7 | 121 | Post-Phase Wiring Hook — Both Paths |
| FR-1.8 | 129 | Anti-Instinct Hook Return Type |
| FR-1.9 | 135 | Gate Result Accumulation |
| FR-1.10 | 141 | Failed Gate -> Remediation Log |
| FR-1.11 | 147 | KPI Report Generation |
| FR-1.12 | 157 | Wiring Mode Resolution |
| FR-1.13 | 162 | Shadow Findings -> Remediation Log |
| FR-1.14 | 168 | BLOCKING Remediation Lifecycle |
| FR-1.15 | 179 | Convergence Registry Args |
| FR-1.16 | 185 | Convergence Merge Args |
| FR-1.17 | 191 | Convergence Remediation Dict->Finding |
| FR-1.18 | 197 | Budget Constants |

No gaps, no duplicates. 18/18 confirmed.

### Check 3: FR-3.1 Mode Matrix Has 4 Modes (a-d) — PASS

Lines 242-247, 4 modes present:

| Mode | Test ID | Line |
|---|---|---|
| off | FR-3.1a | 244 |
| shadow | FR-3.1b | 245 |
| soft | FR-3.1c | 246 |
| full | FR-3.1d | 247 |

All 4 modes (off/shadow/soft/full) present with unique test IDs.

### Check 4: FR-3.2 Budget Scenarios Have 4 Entries (a-d) — PASS

Lines 257-262, 4 scenarios present:

| Scenario | Test ID | Line |
|---|---|---|
| Budget exhausted before task launch | FR-3.2a | 259 |
| Budget exhausted before wiring analysis | FR-3.2b | 260 |
| Budget exhausted before remediation | FR-3.2c | 261 |
| Budget exhausted mid-convergence | FR-3.2d | 262 |

All 4 scenarios present with unique test IDs.

### Check 5: No Contradictory Statements — WARNING

**5a. SC-1 through SC-6 reference mismatch**

Line 397 (FR-6.1, gap T11):
> `tests/roadmap/test_convergence_e2e.py` — 6 tests for SC-1 through SC-6

But SC-1 through SC-6 in the v3.3 Success Criteria table (lines 513-518) are NOT convergence-specific:
- SC-1: "All 20+ wiring points have >= 1 E2E test" (wiring, not convergence)
- SC-2: "TurnLedger lifecycle covered for all 4 paths" (broader than convergence)
- SC-3: "Gate rollout modes covered" (not convergence)
- SC-4: "Zero regressions from baseline" (global)
- SC-5: "KPI report accuracy validated" (not convergence)
- SC-6: "Budget exhaustion paths validated" (not convergence)

**Diagnosis**: This likely references a v3.05-specific SC numbering scheme (where SC-1 through SC-6 were convergence-related), not the v3.3 SC table. The reference is ambiguous and could mislead implementors.

**Recommendation**: Clarify whether T11 tests v3.05 success criteria or v3.3 SC-1 through SC-6. If v3.05, prefix explicitly (e.g., "v3.05-SC-1 through v3.05-SC-6").

**5b. Risk table mentions "2 pre-existing wiring pipeline failures"**

Line 505:
> `The 2 pre-existing wiring pipeline failures may be related`

But baseline (line 7, 488, 516, 616) consistently states "3 pre-existing failures". The risk text narrows to "2 wiring pipeline failures" — this implies 2 of the 3 failures are wiring-related. This is not strictly contradictory but could cause confusion during triage.

**Recommendation**: Add a parenthetical: "2 of the 3 pre-existing failures are wiring-related" if that is the intended meaning.

**5c. Test count: 18 sub-items vs "20 tests" claim**

Line 472: `FR-1.1-FR-1.18: Wiring point E2E tests (20 tests)`
SC-1 (line 513): `Test count >= 20, mapped to FR-1`

FR-1 has exactly 18 sub-items. The "20" claim is plausible because FR-1.7 (both paths) and FR-1.14 (pass + fail recheck) each require 2 tests, yielding 18 + 2 = 20. However, this derivation is implicit.

**Recommendation**: Add a note: "18 FRs; FR-1.7 and FR-1.14 each require 2 tests = 20 total."

### Check 6: Numeric Values Consistent — PASS

**Baseline: 4894 passed, 3 pre-existing failures**:
- Line 7: `4894 passed, 3 pre-existing failures, 0 regressions`
- Line 488: `assert >= 4894 passed, <= 3 pre-existing failures, 0 regressions`
- Line 516: `>= 4894 passed, <= 3 pre-existing failures`
- Line 616: `4894 passed, 3 pre-existing failures`

All 4 mentions consistent.

**MAX_CONVERGENCE_BUDGET = 61**:
- Line 43: `TurnLedger(initial_budget=MAX_CONVERGENCE_BUDGET=61)`
- Line 199: `uses 61 (not 46)`

Both mentions consistent. The "(not 46)" on line 199 documents a prior incorrect value, not a current one.

### Check 7: Code State Snapshot Table Internally Consistent — WARNING

**7a. DeferredRemediationLog line number mismatch**

Code State Snapshot table (line 21):
> `DeferredRemediationLog constructed | executor.py:1135 | WIRED`

FR-1.3 spec reference (line 99):
> `executor.py:1133-1137`

The table cites line 1135 (a single line); the FR cites the range 1133-1137. These are compatible (1135 is within 1133-1137), but the inconsistency could cause confusion when an implementor tries to verify the exact line.

**7b. No duplicate line references found**

All other entries in the table have unique, non-overlapping line references. No two rows claim the same line number for different constructs.

**7c. executor.py vs convergence.py vs models.py vs kpi.py vs wiring_gate.py — all referenced files are distinct**

No file-level inconsistencies found.

### Check 8: Wiring Manifest (Lines 530-586) vs FR-4.1 (Lines 280-325) — WARNING

The body manifest at lines 530-586 is a **strict superset** of the FR-4.1 manifest at lines 280-325.

**Entries in body manifest but NOT in FR-4.1 manifest (4 additional entries)**:

| Target | spec_ref | Body Line |
|---|---|---|
| `run_post_task_anti_instinct_hook` | v3.1-T05 | 546-548 |
| `execute_phase_tasks` | v3.1-T04 | 561-563 |
| `SprintGatePolicy` | v3.2-T06 | 572-574 |
| `handle_regression` | v3.05-FR8 | 583-585 |

**spec_ref differences between the two manifests (same targets, different granularity)**:

| Target | FR-4.1 spec_ref | Body spec_ref |
|---|---|---|
| `_log_shadow_findings_to_remediation_log` | v3.1-T05 | v3.1-T05/R3 |
| `_format_wiring_failure` | v3.1-T06 | v3.1-T06/R4 |
| `_recheck_wiring` | v3.1-T07 | v3.1-T07/R4 |
| `_resolve_wiring_mode` | v3.2-T09 | v3.2-T09/R5 |

**Diagnosis**: The FR-4.1 section appears to be an earlier draft; the body manifest (lines 530-586) is the more complete, authoritative version.

**Recommendation**: Update the FR-4.1 section to match the body manifest exactly, or add a note that the body manifest supersedes FR-4.1's example.

### Check 9: Test File Layout Matches FR References — WARNING

**9a. Mapped correctly**:

| Test File | FR Reference | Status |
|---|---|---|
| `test_wiring_points.py` | FR-1.1-FR-1.18 | MATCH |
| `test_turnledger_lifecycle.py` | FR-2.1-FR-2.4 | MATCH |
| `test_gate_rollout_modes.py` | FR-3.1-FR-3.3 | MATCH |
| `test_budget_exhaustion.py` | FR-3.2a-FR-3.2d | MATCH |
| `test_reachability_eval.py` | FR-4.2-FR-4.4 | MATCH |
| `test_pipeline_fixes.py` | FR-5.1-FR-5.2 | MATCH |
| `test_convergence_wiring.py` | FR-6.1 T07 | MATCH |
| `test_convergence_e2e.py` | FR-6.1 T11 | MATCH |

**9b. Missing test file mappings**:

| FR/Gap | Expected Test | Status |
|---|---|---|
| FR-6.1 T12 (smoke test convergence path) | No test file listed | MISSING |
| FR-6.1 T14 (wiring-verification artifact) | No test file listed | MISSING |
| FR-6.2 T17-T22 (integration, regression, gap audit) | No test file listed | MISSING |
| FR-7 (audit trail validation) | No test file listed | MISSING |

**9c. `audit-trail/audit_trail.py` is a module, not a test file**

Line 606: `audit-trail/audit_trail.py` is listed under `tests/` but described as the "FR-7 JSONL writer module." The FR-7.3 fixture lives in `conftest.py` (line 595), but there is no test file to validate the audit trail itself works correctly.

**Recommendation**: Add test file entries for T12, T14, T17-T22, and FR-7 validation, or note explicitly that these are covered within existing files.

### Check 10: Success Criteria SC-1 Through SC-12 — PASS

All 12 success criteria present at lines 513-524:

| SC | Line | Criterion |
|---|---|---|
| SC-1 | 513 | All 20+ wiring points have >= 1 E2E test |
| SC-2 | 514 | TurnLedger lifecycle covered for all 4 paths |
| SC-3 | 515 | Gate rollout modes covered (off/shadow/soft/full) |
| SC-4 | 516 | Zero regressions from baseline |
| SC-5 | 517 | KPI report accuracy validated |
| SC-6 | 518 | Budget exhaustion paths validated |
| SC-7 | 519 | Eval framework catches known-bad state |
| SC-8 | 520 | Remaining QA gaps closed |
| SC-9 | 521 | Reachability gate catches unreachable code |
| SC-10 | 522 | 0-files-analyzed produces FAIL |
| SC-11 | 523 | Impl-vs-spec fidelity check exists |
| SC-12 | 524 | Audit trail is third-party verifiable |

No gaps, no duplicates. Each SC maps to an FR:
- SC-1 -> FR-1, SC-2 -> FR-2, SC-3 -> FR-3, SC-4 -> Phase 4, SC-5 -> FR-1.11, SC-6 -> FR-3.2, SC-7 -> FR-4.4, SC-8 -> FR-6, SC-9 -> FR-4, SC-10 -> FR-5.1, SC-11 -> FR-5.2, SC-12 -> FR-7.

All FR sections exist and contain the referenced content.

### Check 11: Phased Implementation Plan Matches FR Ordering — PASS

| Phase | FRs Included | Dependency | Valid |
|---|---|---|---|
| Phase 1 (Infrastructure) | FR-7, FR-4.1, FR-4.2 | None | YES |
| Phase 2 (Test Coverage) | FR-1.1-1.18, FR-2.1-2.4, FR-3.1-3.3, FR-6.1-6.2 | Phase 1 | YES |
| Phase 3 (Pipeline Fixes) | FR-5.1, FR-5.2, FR-4.3, FR-4.4 | Phase 1 + Phase 2 baseline | YES |
| Phase 4 (Validation) | SC-* cross-validation | Phases 1-3 | YES |

All 7 FR sections (FR-1 through FR-7) appear in exactly one phase. No FR is orphaned. Dependencies are acyclic and logically sound (infrastructure before tests, tests establish baseline before production changes).

### Check 12: Open Questions Numbered 1-8 — N/A

The spec contains no "Open Questions" section. No references to "OQ-" or "open question" found in the document. This check was specified in the review task but does not apply to this spec.

### Check 13: Risk Table FR Cross-References — WARNING

Lines 499-505 contain 5 risks. None include explicit FR cross-references in the table, but all are traceable to specific FRs:

| # | Risk | Implicit FR | Explicit FR Ref? |
|---|---|---|---|
| 1 | AST analyzer can't resolve lazy imports | FR-4.2 | NO |
| 2 | E2E tests flaky due to subprocess timing | FR-1 (all) | NO |
| 3 | Impl-vs-spec checker false positives | FR-5.2 | NO |
| 4 | Audit trail JSONL grows unbounded | FR-7 | NO |
| 5 | 0-files-analyzed fix breaks existing tests | FR-5.1 | NO |

**Issue**: No risk entries explicitly reference FR numbers. Traceability relies on reader inference.

**Additionally**: Risk 5 mentions "2 pre-existing wiring pipeline failures" (see Check 5b above) which is inconsistent with the baseline "3 pre-existing failures."

**Recommendation**: Add an FR column to the risk table for explicit traceability.

---

## Recommendations Summary

| Priority | Finding | Action |
|---|---|---|
| HIGH | Check 5a: T11 references "SC-1 through SC-6" ambiguously | Clarify v3.05-SC vs v3.3-SC numbering |
| HIGH | Check 8: FR-4.1 manifest is subset of body manifest | Sync FR-4.1 to match body manifest (13 entries) |
| MEDIUM | Check 9: 4 FR/gap items have no test file mapping | Add test files or document coverage locations |
| MEDIUM | Check 13: Risk table lacks explicit FR references | Add FR column to risk table |
| LOW | Check 5b: "2 pre-existing wiring failures" vs "3 pre-existing failures" | Clarify relationship |
| LOW | Check 5c: "20 tests" from 18 FRs is implicit | Document derivation |
| LOW | Check 7a: DeferredRemediationLog line 1135 vs range 1133-1137 | Normalize to consistent format |
