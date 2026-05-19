# Phase 7 — sprint+pipeline pytest Summary

**Result: PASSED (for this task's scope); 57 pre-existing failures documented (independent of C1-C4)**

## Counts
| Metric | Value |
|---|---|
| Total tests collected | 1408 |
| Passed | 1350 |
| Failed (all pre-existing) | 57 |
| Skipped | 1 |
| Duration | 10.70s |

## All 57 failures share the same pre-existing root cause
Every failure message is `AttributeError: '<Fake>Popen' object has no attribute 'stdin'`. The root cause is commit `47997190` (2026-04-20 — "use stdin for the roadmap pipeline instead of passing the prompt as argument") which added `self._process.stdin is not None` to `src/superclaude/cli/pipeline/process.py:141`. The existing test files predate this commit and their fake Popen helper classes do not define `.stdin`.

This was verified to be pre-existing during Phase 5: `git stash` of all C1-C4 changes still produced the same 3 `test_watchdog.py` failures. The pattern is identical for all 57 — none are caused by this task's changes.

## All 13 NEW tests added by this task PASS

| # | File | Test | Result |
|---|---|---|---|
| 1 | tests/sprint/test_executor.py | TestTimeoutFormulaConsistency::test_remediation_step_timeout_matches_canonical_formula | PASSED |
| 2 | tests/sprint/test_executor.py | TestTimeoutFormulaConsistency::test_remediation_step_timeout_matches_per_phase_for_various_max_turns | PASSED |
| 3 | tests/sprint/test_executor.py | test_run_task_subprocess_uses_task_output_file | PASSED |
| 4 | tests/sprint/test_regression_gaps.py | TestSprintLoggerPhaseStart::test_phase_start_emitted_for_per_task_branch | PASSED |
| 5 | tests/sprint/test_config.py | TestStartupStallTimeoutDefaults::test_startup_stall_timeout_default_300 | PASSED |
| 6 | tests/sprint/test_config.py | TestStartupStallTimeoutDefaults::test_startup_stall_timeout_override | PASSED |
| 7 | tests/sprint/test_config.py | TestStartupStallTimeoutDefaults::test_startup_stall_timeout_zero_disables | PASSED |
| 8 | tests/sprint/test_watchdog.py | TestStartupStallWatchdog::test_startup_stall_fires_when_no_events_received | PASSED |
| 9 | tests/sprint/test_watchdog.py | TestStartupStallWatchdog::test_mid_stall_unchanged_when_events_received | PASSED |
| 10 | tests/sprint/test_models.py | TestTaskOutputFileHelpers::test_task_output_file_generates_per_task_path | PASSED |
| 11 | tests/sprint/test_models.py | TestTaskOutputFileHelpers::test_distinct_tasks_get_distinct_paths | PASSED |
| 12 | tests/sprint/test_models.py | TestTaskOutputFileHelpers::test_legacy_output_file_unchanged | PASSED |
| 13 | tests/pipeline/test_process.py | TestClaudeProcessOutputFileCollision::test_two_starts_distinct_output_files_preserve_both_outputs | PASSED |

## Out-of-scope decision

Per F1 execution rules and the qualitative reviewer's C7 follow-up, the 57 pre-existing failures are documented out-of-scope. Fixing them would require adding `self.stdin = MagicMock()` to ~24+ fake Popen helper classes scattered across 8 test files — a large mechanical refactor unrelated to the 4 sprint-runner fixes (C1-C4) this task implements.

**Recommended follow-up:** Open a separate task to add `.stdin` attribute to all fake Popen helpers (or refactor them to inherit from a common base that includes `.stdin`). This is mechanical, low-risk, but ~24 separate test classes need updating. Should NOT block this task.

Raw output: `.dev/tasks/to-do/TASK-RF-20260518-015659/phase-outputs/test-results/phase-7-sprint-pipeline-pytest-output.txt`
