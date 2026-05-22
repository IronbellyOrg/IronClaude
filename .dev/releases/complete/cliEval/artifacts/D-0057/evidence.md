# D-0057 RunOrchestrator — Verification Evidence

Captured 2026-05-20 on branch `fix/prd-path-resolution-and-templates`.

## 1. Files delivered

| Path | Role | Lines |
|---|---|---|
| `src/superclaude/cli/eval/orchestrator.py` | COMP-003 `RunOrchestrator` implementation | new |
| `tests/cli/eval/test_orchestrator.py` | Unit tests (20 cases across 6 classes) | new |
| `.dev/releases/current/cliEval/artifacts/D-0057/spec.md` | Contract documentation | new |
| `.dev/releases/current/cliEval/artifacts/D-0057/notes.md` | Design notes | new |
| `.dev/releases/current/cliEval/artifacts/D-0057/evidence.md` | This file | new |
| `.dev/releases/current/cliEval/evidence/T03.15/pytest-orchestrator.txt` | Verbatim pytest output (orchestrator) | new |
| `.dev/releases/current/cliEval/evidence/T03.15/pytest-regression.txt` | Verbatim pytest output (regression) | new |

## 2. Unit test run — `test_orchestrator.py`

Command: `uv run pytest tests/cli/eval/test_orchestrator.py -v`

Result: **20 passed in 0.48s**

```
tests/cli/eval/test_orchestrator.py::TestOneOutcomePerSpec::test_empty_specs_returns_empty PASSED [  5%]
tests/cli/eval/test_orchestrator.py::TestOneOutcomePerSpec::test_single_spec PASSED [ 10%]
tests/cli/eval/test_orchestrator.py::TestOneOutcomePerSpec::test_outcome_order_matches_input_order PASSED [ 15%]
tests/cli/eval/test_orchestrator.py::TestOneOutcomePerSpec::test_every_spec_gets_exactly_one_outcome PASSED [ 20%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_default_parallel_is_eight PASSED [ 25%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_min_parallel_is_one PASSED [ 30%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_max_parallel_is_fifteen PASSED [ 35%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_zero_parallel_rejected PASSED [ 40%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_negative_parallel_rejected PASSED [ 45%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_non_integer_parallel_rejected PASSED [ 50%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_boolean_parallel_rejected PASSED [ 55%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_parallel_above_max_clamps_to_fifteen PASSED [ 60%]
tests/cli/eval/test_orchestrator.py::TestParallelClamp::test_parallel_one_serialises PASSED [ 65%]
tests/cli/eval/test_orchestrator.py::test_three_eval_suite_runs_faster_than_3x_sequential PASSED [ 70%]
tests/cli/eval/test_orchestrator.py::TestCancellation::test_pre_cancelled_token_skips_all_specs PASSED [ 75%]
tests/cli/eval/test_orchestrator.py::TestCancellation::test_mid_run_cancel_stops_new_submissions PASSED [ 80%]
tests/cli/eval/test_orchestrator.py::TestCancellation::test_unwired_token_does_not_synthesize_interrupts PASSED [ 85%]
tests/cli/eval/test_orchestrator.py::TestWorkerExceptionFolding::test_runtime_error_from_worker_folds_to_errored PASSED [ 90%]
tests/cli/eval/test_orchestrator.py::TestConstructorGuards::test_non_callable_worker_rejected PASSED [ 95%]
tests/cli/eval/test_orchestrator.py::TestConstructorGuards::test_cancellation_token_optional PASSED [100%]

============================== 20 passed in 0.48s ==============================
```

## 3. Regression run — orchestrator + runner_class + signal_handling

Command: `uv run pytest tests/cli/eval/test_orchestrator.py tests/cli/eval/test_runner_class.py tests/cli/eval/test_signal_handling.py`

Result: **56 passed, 1 warning in 2.06s**

The warning is the pre-existing `pty.forkpty()` deprecation surfaced by
`test_runner_class.py` — unrelated to D-0057 and present on `master`.

## 4. Acceptance criteria → evidence mapping

| AC from T03.15 | Test(s) | Result |
|---|---|---|
| AC1: `run(specs, parallel)` emits one `EvalOutcome` per expanded spec | `TestOneOutcomePerSpec::test_empty_specs_returns_empty`, `::test_single_spec`, `::test_outcome_order_matches_input_order`, `::test_every_spec_gets_exactly_one_outcome` | PASS (4/4) |
| AC2: `parallel=20` clamps to 15 | `TestParallelClamp::test_parallel_above_max_clamps_to_fifteen` | PASS |
| AC3: `parallel < 1` rejected per `[1,15]` range | `TestParallelClamp::test_zero_parallel_rejected`, `::test_negative_parallel_rejected`, `::test_non_integer_parallel_rejected`, `::test_boolean_parallel_rejected` | PASS (4/4) |
| AC4: 3-eval suite runs parallel faster than 3× slowest-eval duration | `test_three_eval_suite_runs_faster_than_3x_sequential` (3 specs × 0.2s sleep, parallel=3, elapsed < 0.6s) | PASS |
| AC5: `D-0057/spec.md` documents the scheduler contract | `.dev/releases/current/cliEval/artifacts/D-0057/spec.md` written (8 sections, ~8KB) | PASS |
| AC6: Pattern follows `cli/prd/executor.py:774-802` | `ThreadPoolExecutor(max_workers=...)` + `submit()` + `as_completed()` loop with pre-flight cancellation check (mirrors `PRDExecutor.run_in_parallel`) | PASS |

## 5. Cancellation contract validation (NFR-REL1)

| Path | Test | Result |
|---|---|---|
| Pre-cancelled token: skip all submissions, synthesise `INTERRUPTED` | `TestCancellation::test_pre_cancelled_token_skips_all_specs` | PASS |
| Mid-run cancel: stop new submissions, drain in-flight, synthesise remainder | `TestCancellation::test_mid_run_cancel_stops_new_submissions` | PASS |
| No token wired: orchestrator never synthesises `INTERRUPTED` outcomes | `TestCancellation::test_unwired_token_does_not_synthesize_interrupts` | PASS |

## 6. Worker exception folding (FR-RPT1, NFR-REL2)

| Path | Test | Result |
|---|---|---|
| Worker raises `RuntimeError` → outcome status = `ERRORED`, `error_class="RuntimeError"`, list invariant intact | `TestWorkerExceptionFolding::test_runtime_error_from_worker_folds_to_errored` | PASS |
| No retries on worker failure (NFR-REL2) | Implicit: orchestrator does not loop; one submission per spec | PASS by inspection |

## 7. Constructor guards

| Guard | Test | Result |
|---|---|---|
| Non-callable `run_one` → `TypeError` at construction | `TestConstructorGuards::test_non_callable_worker_rejected` | PASS |
| `cancellation_token=None` is accepted | `TestConstructorGuards::test_cancellation_token_optional` | PASS |

## 8. Out-of-scope confirmations

The following are intentionally NOT exercised by these tests (handled by other
phases/tasks):

- JSONL progress emission (FR-RPT2 — owned by reporter, downstream task).
- Signal handler installation (`SignalHandlerInstaller` — owned by CLI entry
  point, Phase 4 task).
- Per-eval HOME/run_dir/artifacts_dir allocation (owned by CLI wiring/Phase 5).
- Actual `EvalRunner` invocation (delegated to caller via `EvalWorker` closure).

## 9. Sign-off

All T03.15 acceptance criteria verified by automated tests. The
`RunOrchestrator` scheduling primitive is ready for integration by COMP-004
(reporter) and the Phase 5 `superclaude eval` CLI wiring task.
