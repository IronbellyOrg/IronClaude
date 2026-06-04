# Phase 5 Aggregation — Test Coverage (~42 tests across 4 new + 5 edited files)

**Producer:** Step PG5.1 (L6 Aggregation pattern)
**Date:** 2026-06-02
**Phase status:** All work items (5.1–5.10) complete. 55 NEW tests authored (49 mandated + 6 justified extras); all NEW tests PASS. AC1–AC8 fully covered. Ready for rf-qa task-integrity gate (PG5.2).

## Summary

- **pytest (full `tests/sprint/`):** `54 failed, 959 passed, 2 errors` (`--continue-on-collection-errors`). All 54 failures + 2 collection errors are **PRE-EXISTING** repo tech-debt, proven at pre-task baseline `9e864860` (see `phase5-pytest-summary.md` for the throwaway-worktree proof and root causes). **Zero regressions introduced by Phase 5.**
- **NEW tests:** 55 total (mandated count 49 is within the PG5 band 34–50). All pass.
- **AC1–AC8:** 8/8 covered (matrix below).
- **Parallel-batch hazard resolved:** a sibling agent's `git checkout HEAD -- .` reverted 3 agents' edits mid-batch; detected and re-applied; final on-disk state verified (all 9 classes present).

## Test Files

| Path | New/Edited | NEW tests | File total (def test_) | Bytes |
|------|-----------|-----------|------------------------|-------|
| `tests/sprint/test_recovery.py` | NEW | 12 (8 mandated + 4 smoke) | 12 | 14,032 |
| `tests/sprint/test_rerun_tasks.py` | NEW | 13 (12 + R-F4 regression) | 13 | 21,668 |
| `tests/sprint/test_rerun_tasks_e2e.py` | NEW | 2 | 2 | 11,266 |
| `tests/sprint/test_rerun_tasks_failure_modes.py` | NEW | 8 | 8 | 21,425 |
| `tests/sprint/test_cli_contract.py` | EDITED | 5 | 16 | 5,791 |
| `tests/sprint/test_models.py` | EDITED | 4 | 112 defs (142 w/ params) | 43,929 |
| `tests/sprint/test_executor.py` | EDITED | 5 (+1 extra) | 85 | 63,819 |
| `tests/sprint/test_checkpoints.py` | EDITED | 3 | 39 | 28,339 |
| `tests/sprint/test_backward_compat_regression.py` | EDITED | 3 | 18 | 27,592 |
| `tests/sprint/test_e2e_success.py` | EDITED (incidental) | 0 (fake-Popen `stdin=None` fix to enable 5.9 reuse test) | 6 | — |

## AC1–AC8 Coverage Matrix

| AC | Test File | Test Name |
|----|-----------|-----------|
| AC1 | `test_rerun_tasks_e2e.py` | `TestRerunTasksDryRun::test_dry_run_prints_plan_does_not_execute` |
| AC2 | `test_rerun_tasks_e2e.py` | `TestRerunTasksRoundTrip::test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints` |
| AC3 | `test_rerun_tasks_e2e.py` | (merged into the AC2 round-trip test per Resolution 3) |
| AC4 | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksLocking::test_second_concurrent_invocation_aborts_with_lock_pid` |
| AC5 | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksSHACheck::test_source_tasklist_sha_mismatch_aborts` + `test_force_merge_proceeds_with_warning` |
| AC6 | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksRetryCap::test_fourth_attempt_aborts_with_cap_message` + `test_allow_loop_bypasses_cap` |
| AC7 | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksLegacyFallback::test_missing_phase_result_json_falls_back_to_transcript_inspection` |
| AC8 | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksAbortRestore::test_abort_before_merge_back_restores_source_tasklist` + `test_abort_clears_rerun_in_progress_flag` |

**8 of 8 ACs covered.**

## Output Files (this phase)

| Path | Producer |
|------|----------|
| `phase-outputs/test-results/phase5-pytest.txt` (253,775 B) | Step 5.10 |
| `phase-outputs/test-results/phase5-pytest-summary.md` (6,370 B) | Step 5.10 |
| `phase-outputs/reports/phase5-aggregation.md` (this file) | Step PG5.1 |

## Carry-forward for QA

1. **SHA-guard self-trip (HIGH):** documented in Phase 5 Findings + Follow-Up; routed to Step 6.7 qualitative QA for an operational verdict.
2. **Pre-existing suite breakage (MEDIUM, out-of-scope):** 54 failures + 2 collection errors; affects the literal "pytest green" BUILD_REQUEST expectation; recommend a separate cleanup task.
3. **Test-count overage:** 55 total NEW vs ~42 plan (mandated 49 in-band); 6 extras are justified (import-surface smoke, R-F4 regression, extra transient-trigger test).

## Ready-for-QA Assertion

All Phase 5 work items complete; every NEW test passes; AC1–AC8 covered; zero regressions introduced (proven). **Phase 5 is ready for the rf-qa task-integrity gate (PG5.2).**
