# Phase 5 Test Summary — Step 5.1 (Run 1)

**Task:** TASK-RF-per-phase-turn-budget-20260618-160752
**Command:** `uv run pytest tests/sprint/test_per_phase_budget.py tests/sprint/test_models.py::TestTurnLedger tests/sprint/test_turn_ledger_concurrency.py tests/sprint/test_multi_phase.py -v`
**Raw output:** `phase-outputs/test-results/pytest-output.txt`

## Overall result (Run 2, after TM-11 fix): PASSED — 46 passed, 0 failed (4.33s)

After the Step 5.2 fix (wrapping TM-11's `execute_sprint` in `pytest.raises(SystemExit)` — the documented skip-phase exit), the full suite is green: **46 passed, 0 failed, 0 errors**. TM-0 (`test_regression_3x5_no_global_pool_starvation`) PASSED; TM-11 PASSED. All 13 spec §6 TM rows now PASS.

---

## Overall result (Run 1): FAILED — 1 failed, 45 passed (4.46s)

| Metric | Count |
|---|---|
| Collected | 46 |
| Passed | 45 |
| Failed | 1 |
| Skipped | 0 |
| Errors | 0 |

**TM-0 (`test_regression_3x5_no_global_pool_starvation`): PASSED** ✅ (the mandatory regression gate passes.)

## Failed tests

| Test Node | Error Type | Brief Message |
|---|---|---|
| `test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger` (TM-11) | SystemExit: 1 | `execute_sprint` raised SystemExit(1) because the sprint outcome was ERROR. Root cause: the sprint contains a SKIP phase; `PhaseStatus.SKIPPED` is NOT in `PhaseStatus.is_success` (models.py:442-450), so `all(is_success)` is False → outcome ERROR → exit 1 (executor.py:2495-2498, 2598-2602). This is PRE-EXISTING skip-phase behavior, independent of the per-phase ledger change. The test's actual assertions (exactly one TurnLedger.__init__; skip phase SKIPPED/exit 0) are captured before the exit. **Test bug: TM-11 must expect the SystemExit.** Fix applied in Step 5.2. |

## Per-TM checklist (TM-0..TM-14)

| TM | Test node | Run-1 result |
|----|-----------|--------------|
| TM-0 | `test_per_phase_budget.py::test_regression_3x5_no_global_pool_starvation` | PASS |
| TM-1 | `test_per_phase_budget.py::test_per_phase_ledger_is_fresh_each_phase` | PASS |
| TM-2 | `test_models.py::TestTurnLedger::test_per_phase_sizing_for_task_counts` | PASS |
| TM-5 | `test_per_phase_budget.py::test_phase1_reimbursement_does_not_affect_phase2` | PASS |
| TM-6 | `test_models.py::TestTurnLedger::test_no_in_place_reset_and_consumed_monotonic` | PASS |
| TM-7 | `test_multi_phase.py::TestTM7LegacyExecutionLogGolden::test_task_then_legacy_execution_log_golden` | PASS |
| TM-8 | `test_per_phase_budget.py::test_legacy_phase_after_task_phase_has_fresh_ledger` | PASS |
| TM-9 | `test_per_phase_budget.py::test_single_task_overspend_trips_safety_net` | PASS |
| TM-10 | `test_per_phase_budget.py::test_heavy_phase1_cannot_starve_phase2` | PASS |
| TM-11 | `test_per_phase_budget.py::test_skip_and_python_phases_construct_no_ledger` | **FAIL (test bug — see above)** |
| TM-12 | `test_turn_ledger_concurrency.py::test_try_launch_admits_exactly_task_count_under_kgt1` | PASS |
| TM-13 | `test_per_phase_budget.py::test_kpi_wiring_totals_accumulate_across_phases` | PASS |
| TM-14 | `test_per_phase_budget.py::test_resume_window_sizes_phase_identically` | PASS |

All 15 TM-IDs accounted for (TM-3/TM-4 are not defined in the spec's §6 matrix — the matrix is TM-0,1,2,5,6,7,8,9,10,11,12,13,14, i.e. 13 rows; TM-3 and TM-4 do not exist in the FINAL spec). 13/13 spec rows present; 12 PASS, 1 FAIL (test-only bug).
