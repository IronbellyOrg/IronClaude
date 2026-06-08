# Pre-Change Test Baseline (Step 1.4)

**Captured:** 2026-06-03 19:13 (before any Stage 0–3 change)
**Command:** `uv run pytest tests/sprint/ tests/cli/eval/test_isolation_layers_probe.py tests/integration/test_sprint_wiring.py -q`
**Raw output:** `pre-change-baseline.txt`

## Counts (exact, from the pytest summary line)

| Metric | Count |
|--------|-------|
| Passed | 1039 |
| Failed | 54 |
| Skipped | 0 |
| Warnings | 20 |
| Total collected | 1093 |
| Wall time | 18.14s |
| Exit code | 1 |

Summary line verbatim: `54 failed, 1039 passed, 20 warnings in 18.14s`

## Already-failing tests (NOT regressions — pre-existing harness drift)

**Root cause (single, shared):** all 54 failures are the SAME pre-existing test-harness
incompatibility — the integration/e2e tests inject fake `Popen` doubles (`_FakePopen`, `_HaltPopen`,
`_PassPopen`, `FakePopen`, `_FakeProcess`, etc.) that do **not** implement a `.stdin` attribute, but
the production pipeline `start()` at `src/superclaude/cli/pipeline/process.py:141` accesses
`proc.stdin`. The call is reached through the **Path A single-session fallback** in `execute_sprint`
(`executor.py:1331`, immediately after the `_phase_env_vars` / `ClaudeProcess` construction). 48 of the
54 surface as `AttributeError: '<double>' object has no attribute 'stdin'`; the remaining 6
(`test_e2e_success.py`) surface as a downstream `IndexError: list index out of range` from the same
broken-start path.

**Why this matters for this task:** none of these failures are in the Path B per-task code this task
wires (`execute_phase_tasks` / `_run_task_subprocess`). They must NOT be counted as regressions when
later stages re-run overlapping files (e.g. `test_executor.py`, `test_multi_phase.py`). Any NEW failure
not on this list, or any of these flipping for a *different* reason, IS a regression.

### Full already-failing list (54)

- tests/sprint/test_diagnostics.py::TestFailureTriggersCollector::test_failure_triggers_collector
- tests/sprint/test_diagnostics.py::TestDiagnosticsExceptionNonFatal::test_diagnostics_exception_non_fatal
- tests/sprint/test_e2e_halt.py::TestE2EHalt::test_outcome_halted
- tests/sprint/test_e2e_halt.py::TestE2EHalt::test_no_phase3_events
- tests/sprint/test_e2e_halt.py::TestE2EHalt::test_resume_command_in_log
- tests/sprint/test_e2e_halt.py::TestE2EHalt::test_markdown_shows_halt_outcome
- tests/sprint/test_e2e_halt.py::TestE2EHalt::test_phase1_passed_in_log
- tests/sprint/test_e2e_success.py::TestE2ESuccess::test_all_phases_pass
- tests/sprint/test_e2e_success.py::TestE2ESuccess::test_jsonl_events_for_each_phase
- tests/sprint/test_e2e_success.py::TestE2ESuccess::test_jsonl_lines_are_valid_json
- tests/sprint/test_e2e_success.py::TestE2ESuccess::test_markdown_log_has_phase_rows
- tests/sprint/test_e2e_success.py::TestE2ESuccess::test_markdown_log_has_outcome
- tests/sprint/test_e2e_success.py::TestE2ESuccess::test_result_files_created
- tests/sprint/test_execute_sprint_integration.py::TestExecuteSprintFullPath::test_execute_sprint_full_path
- tests/sprint/test_execute_sprint_integration.py::TestExecuteSprintFullPath::test_turnledger_constructed
- tests/sprint/test_execute_sprint_integration.py::TestExecuteSprintFullPath::test_shadow_gate_metrics_constructed
- tests/sprint/test_execute_sprint_integration.py::TestExecuteSprintFullPath::test_deferred_remediation_log_constructed
- tests/sprint/test_execute_sprint_integration.py::TestExecuteSprintFullPath::test_sprint_gate_policy_constructed
- tests/sprint/test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_pass
- tests/sprint/test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_halt
- tests/sprint/test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_timeout_exit_code_124
- tests/sprint/test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_interrupted
- tests/sprint/test_executor.py::TestBackwardCompat::test_backward_compat_sprint_pass_grace_period_zero
- tests/sprint/test_integration_halt.py::TestHaltAndResume::test_halt_at_phase2
- tests/sprint/test_integration_halt.py::TestHaltAndResume::test_halt_phase_number
- tests/sprint/test_integration_halt.py::TestHaltAndResume::test_resume_command_format
- tests/sprint/test_integration_halt.py::TestHaltAndResume::test_phase3_not_executed
- tests/sprint/test_integration_halt.py::TestHaltAndResume::test_first_phase_passed_before_halt
- tests/sprint/test_integration_lifecycle.py::TestFullPhaseLifecycle::test_single_phase_passes
- tests/sprint/test_integration_lifecycle.py::TestFullPhaseLifecycle::test_single_phase_outcome_success
- tests/sprint/test_integration_lifecycle.py::TestFullPhaseLifecycle::test_two_phases_both_pass
- tests/sprint/test_integration_lifecycle.py::TestFullPhaseLifecycle::test_phase_result_has_timing
- tests/sprint/test_integration_signal.py::TestGracefulShutdown::test_sigint_sets_interrupted_outcome
- tests/sprint/test_integration_signal.py::TestGracefulShutdown::test_genuine_failure_still_produces_halted
- tests/sprint/test_integration_signal.py::TestGracefulShutdown::test_sigterm_also_produces_interrupted
- tests/sprint/test_integration_signal.py::TestGracefulShutdown::test_partial_results_captured
- tests/sprint/test_multi_phase.py::TestThreePhaseHappyPath::test_three_phase_happy_path
- tests/sprint/test_multi_phase.py::TestHaltAtPhaseThree::test_halt_at_phase_three
- tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_isolation_dir_created_with_one_file_before_subprocess_launch
- tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_isolation_dir_removed_after_successful_phase
- tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_isolation_dir_removed_after_failed_phase
- tests/sprint/test_phase8_halt_fix.py::TestIsolationWiring::test_startup_orphan_cleanup_removes_stale_isolation_tree
- tests/sprint/test_phase8_halt_fix.py::TestPreliminaryResultIntegration::test_t003_exit_code_0_no_agent_file_yields_pass
- tests/sprint/test_phase8_halt_fix.py::TestPreliminaryResultIntegration::test_t004_non_zero_exit_write_preliminary_not_called
- tests/sprint/test_phase8_halt_fix.py::TestPreliminaryResultIntegration::test_t006_stale_halt_overwritten_yields_pass
- tests/sprint/test_regression_gaps.py::TestExecutorTimeoutPath::test_timeout_exit_code_produces_halted_sprint
- tests/sprint/test_tui_monitor.py::TestTUIUpdateCalledWithMonitorState::test_tui_update_called_with_monitor_state
- tests/sprint/test_tui_monitor.py::TestTUIExceptionNonFatal::test_tui_exception_non_fatal
- tests/sprint/test_tui_monitor.py::TestOutputMonitorLifecycle::test_output_monitor_lifecycle
- tests/sprint/test_tui_monitor.py::TestTmuxUpdateWithSessionName::test_tmux_update_with_session_name
- tests/sprint/test_tui_monitor.py::TestTmuxUpdateWithSessionName::test_tmux_not_called_without_session_name
- tests/sprint/test_watchdog.py::TestWatchdogKillAction::test_stall_kill_action
- tests/sprint/test_watchdog.py::TestWatchdogWarnAction::test_stall_warn_action
- tests/sprint/test_watchdog.py::TestWatchdogStallReset::test_stall_reset_on_resume

## Regression-detection rule for later stages

A later stage has a **regression** iff: (a) a test passing in this baseline now fails, OR (b) one of
the 54 above fails with a *new* error signature unrelated to the `.stdin` harness root cause. Re-running
any of the 54 and seeing the same `.stdin`/`IndexError` failure is NOT a regression.
