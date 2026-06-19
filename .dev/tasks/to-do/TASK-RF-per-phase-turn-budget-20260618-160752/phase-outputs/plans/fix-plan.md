# Phase 5 Fix Plan — Step 5.2

**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Run 1 result:** 1 failed, 45 passed. TM-0 PASSED (regression gate green).

## Failure 1 — TM-11 `test_skip_and_python_phases_construct_no_ledger`

**Error:** `SystemExit: 1` raised by `execute_sprint(config)` (executor.py:2602).

**Root-cause analysis (evidence-based):**
- `execute_sprint` sets `_exitcode = 0 if outcome == SUCCESS else 1` and raises `SystemExit(_exitcode)` when non-zero (executor.py:2598-2602).
- The outcome is downgraded to ERROR when `not all(r.status.is_success for r in sprint_result.phase_results)` (executor.py:2495-2498).
- TM-11's sprint deliberately contains a **skip phase** (per the spec). `PhaseStatus.SKIPPED` is **not** in `PhaseStatus.is_success` (models.py:442-450) — only PASS/PASS_*/PREFLIGHT_PASS/PASS_MISSING_CHECKPOINT are. So a sprint with a skip phase ALWAYS yields outcome ERROR → SystemExit(1).
- This is **pre-existing skip-phase behavior**, NOT caused by the per-phase ledger change (R-1..R-10). The per-phase ledger change only governs ledger construction; it does not alter outcome/exit logic. The other multi-phase tests with only task phases (TM-0, TM-13) returned SUCCESS and did not raise.
- TM-11's actual assertions — exactly one `TurnLedger.__init__` construction, and the skip phase recorded `SKIPPED`/`exit_code 0` — are satisfied BEFORE the exit: the `TurnLedger.__init__` spy increments during the phase loop, and `logger.write_summary(sprint_result)` (which captures the SprintResult) runs at executor.py:2573, before the raise at 2602.

**Conclusion:** This is a **test-only bug** (the test failed to anticipate that a skip-phase sprint exits non-zero). NO source change is warranted — changing `is_success` to include SKIPPED, or suppressing the exit, would be an out-of-scope behavioral change beyond the spec's blast radius. TM-11 is not about the sprint outcome; it is about ledger-construction count and skip-phase status.

**Fix (file:line):** `tests/sprint/test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger` — wrap the `execute_sprint(config)` call in `pytest.raises(SystemExit)` (the documented, pre-existing consequence of a skip phase). The construction-count and skip-status assertions remain unchanged and run after the `with` block, against the spy counter and the captured SprintResult.

**Priority:** Highest among failures is always TM-0 (regression) — already PASSING, so no action there. This single non-regression test fix is applied next.

## Re-run

After applying the fix, re-run the Step 5.1 command and confirm 0 failures, 0 errors, TM-0 still PASSED.
