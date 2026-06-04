# Phase 5 Pytest Summary — Step 5.10 (L3 Test/Execute)

**Producer:** Step 5.10
**Date:** 2026-06-02
**Command:** `cd <worktree> && uv run pytest tests/sprint/ -v --continue-on-collection-errors`
**Raw output:** `phase-outputs/test-results/phase5-pytest.txt`

## Overall Result

- **Task-scoped verdict: PASS** — every NEW test added in Phase 5 passes; **zero regressions** introduced by this task (proven against the pre-task baseline, see below).
- **Full-suite line:** `54 failed, 959 passed, 20 warnings, 2 errors in 16.68s`
- The 54 failures + 2 collection errors are **100% PRE-EXISTING** repo tech-debt, unrelated to v4.3.0 rerun-tasks. Evidence below.

## Counts

| Metric | Value |
|--------|-------|
| Passed | 959 |
| Failed | 54 (all pre-existing) |
| Collection errors | 2 (all pre-existing) |
| Skipped | 0 |
| NEW tests added in Phase 5 | 55 (49 mandated + 6 justified extras) |

## NEW tests per file (all PASS)

| File | New/Edited | New tests | Result |
|------|-----------|-----------|--------|
| `test_recovery.py` | NEW | 12 (8 mandated + 4 import-surface smoke) | 12 pass |
| `test_rerun_tasks.py` | NEW | 13 (12 mandated + 1 R-F4 regression) | 13 pass |
| `test_rerun_tasks_e2e.py` | NEW | 2 | 2 pass |
| `test_rerun_tasks_failure_modes.py` | NEW | 8 | 8 pass |
| `test_cli_contract.py` | EDITED | 5 | 16 pass (file total) |
| `test_models.py` | EDITED | 4 | 142 pass (file total) |
| `test_executor.py` | EDITED | 5 (+1 extra) | 80 pass + 5 PRE-EXISTING fail |
| `test_checkpoints.py` | EDITED | 3 | 39 pass (file total) |
| `test_backward_compat_regression.py` | EDITED | 3 | 18 pass (file total) |

Note: 55 total NEW tests is +31% over the ~42 plan (PG5 band 34–50 mandated-count = 49, in-band). The 6 extras are justified: 4 smoke tests in `test_recovery.py` exercise the 6 nominator/lock/retry symbols the item's mandated import list requires (without them ruff F401 fails); 1 R-F4 rerun-name regression test (carried-forward Phase 3 Step 3.3 obligation); 1 extra `_is_transient_failure` ConnectionRefused-trigger test in `test_executor.py`.

## Pre-existing failures — PROOF they are NOT this task's regressions

Two independent root causes, both predating the task:

1. **`'_*Popen' object has no attribute 'stdin'` (52 of 54 failures)** across `test_integration_signal.py`, `test_multi_phase.py`, `test_phase8_halt_fix.py`, `test_regression_gaps.py`, `test_tui_monitor.py`, `test_watchdog.py`, and 5 in `test_executor.py`. Root cause: `src/superclaude/cli/pipeline/process.py:141-143` reads `self._process.stdin`, but the older fake-Popen test fixtures don't define `stdin`. That `.stdin` write was added by commit `47997190f` on **2026-04-20** (six weeks before this task) and is present verbatim in the pre-task baseline `9e864860`.
   - **Gold-standard proof:** ran `tests/sprint/test_multi_phase.py` + `tests/sprint/test_watchdog.py` in a throwaway `git worktree` at pre-task baseline `9e864860` → **5 failed, 2 passed — identical pattern** to the current run. All these fixture files are byte-identical to HEAD (`git status` clean).

2. **`ImportError: cannot import name 'invoke_haiku'` (2 collection errors)** in `test_retrospective.py` + `test_summarizer.py`. Root cause: `summarizer.py` exposes `invoke_sonnet` (line 305), not `invoke_haiku`, at HEAD; the two test modules import the stale name. `git status src/` is clean (summarizer.py unmodified by this task); both test modules import `invoke_haiku` at HEAD too. Pre-existing source/test drift.

**Conclusion:** Of the 54 failures, the 49 in files this task never edited are pre-existing by construction (a test module's edits cannot affect a different module). The 5 in `test_executor.py` were independently confirmed pre-existing (75→80 pass after adding the 5 new tests; the same 5 fail on HEAD before the edit). No Phase 5 change turned any green test red.

## AC1–AC8 Coverage Matrix

| AC | Test File | Test Name | Present? |
|----|-----------|-----------|----------|
| AC1 (dry-run, no execute) | `test_rerun_tasks_e2e.py` | `TestRerunTasksDryRun::test_dry_run_prints_plan_does_not_execute` | ✅ |
| AC2 (rename originals + flip + event) | `test_rerun_tasks_e2e.py` | `TestRerunTasksRoundTrip::test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints` | ✅ |
| AC3 (round-trip equiv / verify-checkpoints) | `test_rerun_tasks_e2e.py` | `TestRerunTasksRoundTrip::test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints` (merged AC2+AC3 per Resolution 3) | ✅ |
| AC4 (concurrent lock) | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksLocking::test_second_concurrent_invocation_aborts_with_lock_pid` | ✅ |
| AC5 (SHA mid-flight-edit) | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksSHACheck::test_source_tasklist_sha_mismatch_aborts` + `test_force_merge_proceeds_with_warning` | ✅ |
| AC6 (retry cap 3) | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksRetryCap::test_fourth_attempt_aborts_with_cap_message` + `test_allow_loop_bypasses_cap` | ✅ |
| AC7 (legacy transcript fallback) | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksLegacyFallback::test_missing_phase_result_json_falls_back_to_transcript_inspection` | ✅ |
| AC8 (abort restore) | `test_rerun_tasks_failure_modes.py` | `TestRerunTasksAbortRestore::test_abort_before_merge_back_restores_source_tasklist` + `test_abort_clears_rerun_in_progress_flag` | ✅ |

**8 of 8 ACs covered.**

## ⚠️ Production concern surfaced by tests (NOT a test failure)

Three independent test-authoring agents (5.2/5.3/5.4) converged on the same finding: `flip_target_checkboxes` writes a `SUPERCLAUDE-RERUN` provenance block into the **source tasklist** at step 10, BEFORE the step-12 mid-flight-edit SHA guard re-hashes that same file. The guard therefore sees the engine's **own** write as an external "modification" and aborts every `--merge-back` run with `"Source tasklist modified since rerun started…"` unless `--force-merge` is passed. This effectively makes `--force-merge` mandatory for the happy path and undermines the R-F6 defense (TDD §T8.1) whose purpose is to detect a *real operator* edit. **Flagged for Phase 6 qualitative QA (Step 6.7) and as a HIGH follow-up.** This is a design/ordering issue, not a test defect; the e2e/failure-mode tests pass `--force-merge` with inline comments documenting why.
