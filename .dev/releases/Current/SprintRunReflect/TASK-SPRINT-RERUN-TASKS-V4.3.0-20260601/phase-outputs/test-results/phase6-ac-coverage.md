# Phase 6 — AC1–AC8 Coverage Verification (Step 6.4)

**Date:** 2026-06-02 · **Collect raw:** `phase6-ac-collect.txt`
**Command:** `uv run pytest tests/sprint/test_rerun_tasks_e2e.py tests/sprint/test_rerun_tasks_failure_modes.py -v --collect-only` → **10 tests collected, exit 0**

| AC | Test File | Test Name | Verified Present? |
|----|-----------|-----------|-------------------|
| AC1 | test_rerun_tasks_e2e.py | `TestRerunTasksDryRun::test_dry_run_prints_plan_does_not_execute` | ✅ |
| AC2 | test_rerun_tasks_e2e.py | `TestRerunTasksRoundTrip::test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints` | ✅ |
| AC3 | test_rerun_tasks_e2e.py | `TestRerunTasksRoundTrip::test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints` (AC2+AC3 merged per Resolution 3; asserts verify-checkpoints `--recover` + round-trip equivalence) | ✅ |
| AC4 | test_rerun_tasks_failure_modes.py | `TestRerunTasksLocking::test_second_concurrent_invocation_aborts_with_lock_pid` | ✅ |
| AC5 | test_rerun_tasks_failure_modes.py | `TestRerunTasksSHACheck::test_source_tasklist_sha_mismatch_aborts` (+ `test_force_merge_proceeds_with_warning`) | ✅ |
| AC6 | test_rerun_tasks_failure_modes.py | `TestRerunTasksRetryCap::test_fourth_attempt_aborts_with_cap_message` (+ `test_allow_loop_bypasses_cap`) | ✅ |
| AC7 | test_rerun_tasks_failure_modes.py | `TestRerunTasksLegacyFallback::test_missing_phase_result_json_falls_back_to_transcript_inspection` | ✅ |
| AC8 | test_rerun_tasks_failure_modes.py | `TestRerunTasksAbortRestore::test_abort_before_merge_back_restores_source_tasklist` (+ `test_abort_clears_rerun_in_progress_flag`) | ✅ |

**8 of 8 ACs covered** by concrete, collected tests. (All 10 tests pass when executed — see `phase5-pytest-summary.md`.) BUILD_REQUEST VALIDATION_REQUIREMENT (each AC has a corresponding pytest test) satisfied.
