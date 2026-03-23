# Adversarial Review — v3.3 TurnLedger Validation

**Date**: 2026-03-23
**Reviewer**: Orchestrator (Phase 4)

## Methodology

Fresh re-read of spec and roadmap, independent of agent reports. Systematic challenge of all COVERED assessments. Pattern scan for orphan requirements (negation patterns, conditional requirements). Orphan task detection.

---

## Adversarial Findings

### ADV-1: FR-1.19 (SHADOW_GRACE_INFINITE) MISSING from roadmap
- **Type**: MISSED_GAP
- **Severity**: HIGH
- **Description**: The spec (L211-217) defines FR-1.19 requiring tests for the `SHADOW_GRACE_INFINITE` constant — its definition in models.py and its behavioral effect on shadow mode grace period. The roadmap's Phase 2A task table (L79-91) covers FR-1.1 through FR-1.18 only. FR-1.19 is not referenced in any roadmap task, checkpoint, or success criteria validation matrix entry.
- **Spec evidence**: spec:FR-1.19 (L211-217) — "Assert: `SHADOW_GRACE_INFINITE` is defined in models.py with expected sentinel value" and "when `wiring_gate_grace_period` is set to `SHADOW_GRACE_INFINITE`, shadow mode never exits grace period"
- **Roadmap evidence**: ABSENT. Searched: "FR-1.19", "SHADOW_GRACE", "post_init", "check_wiring_report" — zero matches across entire roadmap.
- **Impact**: A verified wiring point (models.py:293) would have no test. The constant's sentinel value and grace period logic are untested.
- **Recommended correction**: Add task to Phase 2A (e.g., 2A.13) covering FR-1.19 with 1 test.

### ADV-2: FR-1.20 (__post_init__ config derivation) MISSING from roadmap
- **Type**: MISSED_GAP
- **Severity**: HIGH
- **Description**: The spec (L219-225) defines FR-1.20 requiring tests for `__post_init__()` derivation of sprint config fields and default behavior. Not referenced in any roadmap task.
- **Spec evidence**: spec:FR-1.20 (L219-225) — "Assert: derived fields (wiring_gate_enabled, wiring_gate_grace_period, wiring_analyses_count) are computed from base config values" and "invalid or missing base config values produce sensible defaults"
- **Roadmap evidence**: ABSENT (same search as ADV-1).
- **Impact**: Critical config derivation logic (models.py:338-384) would have no test. Incorrect derivation could silently break sprint behavior.
- **Recommended correction**: Add task to Phase 2A (e.g., 2A.14) covering FR-1.20 with 1 test.

### ADV-3: FR-1.21 (check_wiring_report wrapper) MISSING from roadmap
- **Type**: MISSED_GAP
- **Severity**: HIGH
- **Description**: The spec (L129-135) defines FR-1.21 requiring a test that `check_wiring_report()` wrapper is called within the wiring analysis flow. Not referenced in any roadmap task.
- **Spec evidence**: spec:FR-1.21 (L129-135) — "Assert: `run_post_phase_wiring_hook()` or `run_post_task_wiring_hook()` invokes `check_wiring_report()` as part of wiring analysis" and "the wrapper delegates to the underlying analysis and returns a valid report structure"
- **Roadmap evidence**: ABSENT (same search as ADV-1).
- **Impact**: A verified wiring point (wiring_gate.py:1079) would have no dedicated test. The wrapper's delegation and return structure are untested.
- **Recommended correction**: Add task to Phase 2A (e.g., 2A.15) covering FR-1.21 with 1 test.

### ADV-4: FR-2.1a (handle_regression reachability) MISSING from roadmap
- **Type**: MISSED_GAP
- **Severity**: HIGH
- **Description**: The spec (L241-246) defines FR-2.1a as a separate sub-requirement for testing `handle_regression()` reachability from `_run_convergence_spec_fidelity` and its behavior on regression detection. Roadmap task 2B.1 covers FR-2.1 (convergence path) but does not mention `handle_regression()` or regression detection behavior.
- **Spec evidence**: spec:FR-2.1a (L241-246) — "Assert `handle_regression()` is reachable from `_run_convergence_spec_fidelity` and is called on regression detection" and "logs the regression event and adjusts budget accordingly"
- **Roadmap evidence**: ABSENT. Task 2B.1 (L101) covers `execute_fidelity_with_convergence()` E2E with debit/credit/reimburse but never mentions `handle_regression`. Searched: "FR-2.1a", "handle_regression", "regression handler" — zero matches.
- **Impact**: The regression detection path in convergence would be untested. `handle_regression` IS in the wiring manifest (spec:L618-620) so the reachability gate would detect it as reachable, but the behavioral test (logging, budget adjustment) would be missing.
- **Recommended correction**: Add task to Phase 2B (e.g., 2B.1a or 2B.5) covering FR-2.1a with 1 test.

### ADV-5: _parse_phase_tasks() return type untested
- **Type**: MISSED_GAP
- **Severity**: MEDIUM
- **Description**: The Code State Snapshot (spec:L29) lists `_parse_phase_tasks()` returns `list[TaskEntry] | None` as a verified wiring point, but no FR explicitly tests the return type contract. FR-1.5 tests that task-inventory phases use `execute_phase_tasks()` but doesn't test the parser itself.
- **Spec evidence**: spec:Code State Snapshot (L29) — "`_parse_phase_tasks()` returns `list[TaskEntry] | None`"
- **Roadmap evidence**: Covered indirectly by task 2A.2 (FR-1.5) but return type contract not specified.
- **Impact**: If `_parse_phase_tasks()` changes return type, existing tests would catch functional failure but not the type contract.
- **Recommended correction**: Add return type assertion to task 2A.2 or document as indirectly covered.

### ADV-6: can_run_wiring_gate() has no dedicated test
- **Type**: MISSED_GAP
- **Severity**: LOW
- **Description**: The Code State Snapshot (spec:L35) lists `can_run_wiring_gate()` as a wiring point, but it has no dedicated FR. It IS exercised indirectly through FR-3.2b (budget exhaustion before wiring).
- **Spec evidence**: spec:Code State Snapshot (L35) — "`debit_wiring()` / `credit_wiring()` / `can_run_wiring_gate()`"
- **Roadmap evidence**: Indirectly covered by task 2C.2 (FR-3.2b).
- **Impact**: LOW — indirect coverage through budget exhaustion scenario is adequate.

### ADV-7: Orphan roadmap task 4.6
- **Type**: ORPHAN_TASK
- **Severity**: LOW (informational)
- **Description**: Roadmap task 4.6 "Update `docs/memory/solutions_learned.jsonl` with v3.3 patterns" has no spec traceability. This is implementation housekeeping and does not indicate a gap.

---

## Challenge Results on COVERED Assessments

### D1 Agent Corrections
- **REQ-022 (FR-1.19)**: D1 marked COVERED → **CORRECTED to MISSING**. No roadmap task references FR-1.19 or SHADOW_GRACE_INFINITE.
- **REQ-023 (FR-1.20)**: D1 marked COVERED → **CORRECTED to MISSING**. No roadmap task references FR-1.20 or __post_init__.
- **REQ-010 (FR-1.21)**: D1 marked COVERED → **CORRECTED to MISSING**. No roadmap task references FR-1.21 or check_wiring_report.

### D2 Agent Corrections
- **REQ-026 (FR-2.1a)**: D2 marked COVERED → **CORRECTED to MISSING**. Roadmap task 2B.1 covers FR-2.1 but not FR-2.1a.

### All Other Assessments
Remaining COVERED assessments withstood adversarial challenge. The roadmap tasks provide specific, traceable coverage with accurate FR ID references and matching descriptions.

---

## Orphan Requirements (Step 4.3a)

Negation pattern scan found 1 match (L78: "MUST NOT mock") — already captured as REQ-002/REQ-075.
No additional orphan requirements discovered.

## Orphan Tasks (Step 4.4)

Task 4.6 (`solutions_learned.jsonl`) is the only orphan task. Informational only — does not indicate missing spec requirements.

## Sequencing Validation (Step 4.5)

All spec-mandated ordering constraints respected:
- Phase 1 before Phase 2 ✓
- Phase 1B + Phase 2 before Phase 3 ✓
- All before Phase 4 ✓
- No circular dependencies ✓

## Silent Assumptions (Step 4.6)

No silent assumptions detected. The roadmap's dependency table and integration point registry are comprehensive.

---

## Impact on Consolidated Report

The adversarial pass found **4 new HIGH findings** (ADV-1 through ADV-4) that overturn agent COVERED assessments. This changes:

| Metric | Before Adversarial | After Adversarial |
|--------|-------------------|-------------------|
| COVERED | 81 | 77 |
| PARTIAL | 3 | 3 |
| MISSING | 0 | 4 |
| Full Coverage Score | 96.4% | 91.7% |
| Weighted Coverage Score | 98.2% | 93.5% |
| HIGH findings | 2 | 6 |
| Verdict | CONDITIONAL_GO | CONDITIONAL_GO (still meets criteria: 0 CRITICAL, ≤3 HIGH would be GO, but 6 HIGH → NO_GO threshold is >3) |

**REVISED VERDICT**: With 6 HIGH findings (>3), the verdict changes to **NO_GO**.

Wait — let me recount. Pre-adversarial HIGHs: GAP-H001 (audit retrofit), GAP-H002 (resource table). Plus 4 ADV HIGHs = 6 total HIGH. This exceeds the >3 HIGH threshold.

**FINAL REVISED VERDICT: NO_GO** — 6 HIGH findings exceed the maximum of 3 for CONDITIONAL_GO.

However, the fixes are straightforward: add 4 missing tasks to Phase 2A/2B. The roadmap requires targeted amendments, not substantial revision.
