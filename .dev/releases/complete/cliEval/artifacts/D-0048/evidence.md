# D-0048 — FR-LC1 EvalRunner lifecycle evidence

**Task:** T03.04 (Phase 3, Roadmap FR-LC1 / R-048)
**Date:** 2026-05-20
**Status:** All acceptance criteria satisfied.

## Test output

`uv run pytest tests/cli/eval/test_eval_lifecycle.py -v` — full output
captured at `evidence/T03.04/test-output.txt`.

```
============================= 22 passed in 0.15s ==============================
```

### Per-test results

| # | Test | Outcome | AC link |
|---|---|---|---|
| 1 | `test_run_eval_executes_all_seven_steps_in_order` | PASSED | AC1 (7-step order) |
| 2 | `test_run_eval_setup_exception_yields_errored` | PASSED | AC2 (setup → ERRORED) |
| 3 | `test_run_eval_deploy_hooks_exception_yields_errored` | PASSED | AC3 (deploy → ERRORED) |
| 4 | `test_run_eval_spawn_exception_yields_errored` | PASSED | AC4 (spawn → ERRORED) |
| 5 | `test_run_eval_inject_exception_yields_errored` | PASSED | AC4 (inject → ERRORED) |
| 6 | `test_run_eval_observe_exception_yields_errored` | PASSED | AC4 (observe → ERRORED) |
| 7 | `test_run_eval_expect_raise_yields_errored` | PASSED | AC5 (Expect raise → ERRORED + partial expects) |
| 8 | `test_run_eval_passes_when_all_expects_pass` | PASSED | AC6 (PASS precondition) |
| 9 | `test_run_eval_empty_expects_yields_pass` | PASSED | AC6 (empty Expects → PASS) |
| 10 | `test_run_eval_failing_expect_yields_fail` | PASSED | AC7 (failing Expect → FAIL) |
| 11 | `test_run_eval_mixed_results_yields_fail` | PASSED | AC7 (mixed → FAIL, all results recorded) |
| 12 | `test_run_eval_teardown_keep_true_on_errored` | PASSED | AC8 (ERRORED forces keep=True) |
| 13 | `test_run_eval_teardown_keep_true_on_fail` | PASSED | AC8 (FAIL forces keep=True) |
| 14 | `test_run_eval_teardown_keep_false_on_pass_by_default` | PASSED | AC8 (PASS default keep=False) |
| 15 | `test_run_eval_teardown_keep_true_on_pass_when_requested` | PASSED | AC8 (PASS + keep_home_on_pass=True) |
| 16 | `test_run_eval_teardown_error_swallowed_callback_invoked` | PASSED | AC9 (teardown error best-effort + callback) |
| 17 | `test_run_eval_teardown_error_without_callback_is_silent` | PASSED | AC9 (teardown error silent w/o callback) |
| 18 | `test_run_eval_keyboard_interrupt_propagates_with_teardown[sigint]` | PASSED | AC10 (KeyboardInterrupt propagates, keep=True) |
| 19 | `test_run_eval_keyboard_interrupt_propagates_with_teardown[sysexit]` | PASSED | AC10 (SystemExit propagates, keep=True) |
| 20 | `test_run_eval_keyboard_interrupt_in_expect_propagates` | PASSED | AC10 (KbdInt in Expect propagates) |
| 21 | `test_run_eval_passes_observed_state_into_eval_context` | PASSED | AC11 (EvalContext carries observed state) |
| 22 | `test_run_eval_outcome_includes_observed_artifacts` | PASSED | AC11 (artifacts threaded into outcome) |

## Regression sweep

`uv run pytest tests/cli/eval/ -q` — full output captured at
`evidence/T03.04/regression-sweep.txt`.

```
============================= 781 passed in 8.34s ==============================
```

Zero regressions across the eval CLI suite after introducing
`runner.py` and re-exports through `superclaude.cli.eval.__init__`.

## Acceptance-criteria status

The roadmap row R-048 / T03.04 enumerates the following AC. Each row
links to the implementation site + the test that pins it.

| AC | Statement | Implementation | Test |
|---|---|---|---|
| AC1 | `run_eval(spec)` in `runner.py` executes the 7-step lifecycle and returns an `EvalOutcome`. | `run_eval(...)` in `src/superclaude/cli/eval/runner.py:172-358` | `test_run_eval_executes_all_seven_steps_in_order` |
| AC2 | Harness exceptions during lifecycle → status `ERRORED`. | `_classify_outcome` in `runner.py:393-415` (any captured exception → ERRORED + fqcn classname). | `test_run_eval_setup_exception_yields_errored`, `test_run_eval_deploy_hooks_exception_yields_errored`, `test_run_eval_{spawn,inject,observe}_exception_yields_errored`, `test_run_eval_expect_raise_yields_errored` |
| AC3 | Assertion failures → status `FAIL`. | `_classify_outcome` returns `FAIL` when any `ExpectResult.passed is False` and no harness exception fired. | `test_run_eval_failing_expect_yields_fail`, `test_run_eval_mixed_results_yields_fail` |
| AC4 | `PASS` only emitted when all Expects pass. | `_classify_outcome` returns `PASS` only when every result passed; empty Expects tuple also PASS (no assertions failed). | `test_run_eval_passes_when_all_expects_pass`, `test_run_eval_empty_expects_yields_pass` |
| AC5 | `TASKLIST_ROOT/artifacts/D-0048/spec.md` documents the lifecycle and status mapping. | `.dev/releases/current/cliEval/artifacts/D-0048/spec.md` (created in T03.04). | n/a (doc artefact) |

### Additional invariants verified (beyond the explicit AC list)

These were enforced by `design-spec.md §6` and the FR-LC1 / NFR-REL1
rows; the tests pin them so a regression cannot land silently.

| Invariant | Test |
|---|---|
| 7-step order is exactly setup → deploy → spawn → inject → observe → assert → teardown. | `test_run_eval_executes_all_seven_steps_in_order` |
| Teardown forces `keep=True` for every non-PASS outcome (forensic preservation). | `test_run_eval_teardown_keep_true_on_errored`, `test_run_eval_teardown_keep_true_on_fail` |
| Teardown honours `keep_home_on_pass` for PASS outcomes (default `False`). | `test_run_eval_teardown_keep_false_on_pass_by_default`, `test_run_eval_teardown_keep_true_on_pass_when_requested` |
| Teardown failures do NOT flip the outcome status (best-effort). | `test_run_eval_teardown_error_swallowed_callback_invoked`, `test_run_eval_teardown_error_without_callback_is_silent` |
| `on_teardown_error` callback receives the swallowed exception. | `test_run_eval_teardown_error_swallowed_callback_invoked` |
| `KeyboardInterrupt` / `SystemExit` propagate (NFR-REL1) with `teardown(keep=True)`. | `test_run_eval_keyboard_interrupt_propagates_with_teardown[sigint]`, `[sysexit]`, `test_run_eval_keyboard_interrupt_in_expect_propagates` |
| `EvalContext.from_runner_state(...)` is built from observed state and carries `exit_code` / `stdout` / `duration_sec` / `home_path`. | `test_run_eval_passes_observed_state_into_eval_context` |
| `ObservedRun.artifacts` is threaded into `EvalOutcome.artifacts`. | `test_run_eval_outcome_includes_observed_artifacts` |
| Steps 1-5 failures pin `duration_sec` to `0.0` (no stale observe value). | `test_run_eval_setup_exception_yields_errored`, `test_run_eval_deploy_hooks_exception_yields_errored`, `test_run_eval_spawn_exception_yields_errored`, `test_run_eval_observe_exception_yields_errored` |

## Manual validation

```
$ uv run python -c "from superclaude.cli.eval import run_eval, LifecycleExecutor, ObservedRun, ExecutorContext, ExpectCallable; print('imports OK')"
imports OK
```

All five symbols exposed by `runner.py` are re-exported through
`superclaude.cli.eval.__init__` per the spec's "Module symbol re-
exports" section.

## Out of scope / deferred

Per `spec.md §"Out of scope for T03.04"`:

* Per-eval JSONL logging → COMP-004 / T03.05 (D-0049).
* Per-eval timeout enforcement (`TimeoutError` → `TIMEOUT` mapping) →
  NFR-REL1 / T03.07. The skeleton classifies `TimeoutError` as
  `ERRORED` today; T03.07 swaps the branch.
* Parallel orchestration / suite-level aggregation → FR-G2 / T03.16.
* `SKIPPED` capability-gate branch → FR-CAP2 / T03.08.
* Concrete `PtyClaudeExecutor` wiring `ClaudeProcessAdapter` +
  `PtyDriver` → T03.05 (D-0049).
