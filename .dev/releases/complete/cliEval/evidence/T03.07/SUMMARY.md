# T03.07 Evidence — NFR-REL1 Signal Handling + Per-Eval Cancellation

## Task
Implement signal handler module + per-eval cancellation/timeout
enforcement inside `EvalRunner.run()`.

## Acceptance Criteria Verification

| AC | Requirement | Verified by |
|----|-------------|-------------|
| AC1 | SIGINT during a parallel run cancels in-flight evals → `INTERRUPTED`; partial summary; exit 3. | `EXIT_INTERRUPTED = 3` constant; `CancellationToken` + `SignalHandlerInstaller` (`TestCancellationToken::*`, `TestSignalHandlerInstaller::*`); `EvalRunner` runtime conversion to INTERRUPTED (`test_pre_cancelled_token_returns_interrupted_without_spawn`, `test_keyboard_interrupt_with_token_returns_interrupted`). Partial-summary writer is owned by T03.13 / T03.15. |
| AC2 | Per-eval timeout kills PtyDriver and reaps zombie; outcome `TIMEOUT`. | `test_timeout_invokes_executor_cancel` (records `executor_cancel_*` events + `TIMEOUT` outcome); `test_pty_driver_terminate_kills_real_subprocess` (real `/proc/<pid>` reap check). |
| AC3 | No zombie processes after a timeout (verified by `ps`/`/proc` snapshot). | `test_pty_driver_terminate_kills_real_subprocess` polls `/proc/<pid>` for 5 s after `terminate(force=True) + close()` and asserts the directory has disappeared. |
| AC4 | `artifacts/D-0050/spec.md` documents the signal + timeout contract. | `.dev/releases/current/cliEval/artifacts/D-0050/spec.md` written. |

## Test Result

`uv run pytest tests/cli/eval/test_signal_handling.py -v` →
**25 passed in 0.61s** (see `pytest-signal-handling.txt`).

Breakdown:
* `TestCancellationToken` — 10 tests (one-shot semantics, signum capture, wait, concurrency).
* `TestSignalHandlerInstaller` — 8 tests (install/restore, callback, main-thread guard, idempotency).
* EvalRunner integration — 6 tests covering pre-cancelled token, in-flight KeyboardInterrupt, regression (no-token), timeout cancel path (success/failure/skipped).
* End-to-end PtyDriver — 1 test confirming real subprocess kill + zombie reap.

## Regression Check

`uv run pytest tests/cli/eval/ -q` → **817 passed** (see
`pytest-regression.txt`). Notably, the T03.05 KeyboardInterrupt
propagation guard (`test_keyboard_interrupt_in_expect_propagates`)
still passes, confirming the new behaviour only kicks in when a
`cancellation_token` is explicitly wired.

## Files Modified / Added

| Path | Change |
|---|---|
| `src/superclaude/cli/eval/signal_handler.py` | **New.** `EXIT_INTERRUPTED`, `DEFAULT_INTERRUPT_SIGNALS`, `CancellationToken`, `SignalHandlerInstaller`. |
| `src/superclaude/cli/eval/runner.py` | New `cancellation_token` kwarg on `EvalRunner.__init__`; pre-flight cancel check in `run()`; KeyboardInterrupt→INTERRUPTED conversion (gated on token); `_handle_timeout` now calls `_cancel_executor`; new helpers `_cancel_executor` + `_make_interrupted_outcome`; new event-name constants (`EVENT_TIMEOUT_FIRED`, `EVENT_INTERRUPTED_FIRED`, `EVENT_EXECUTOR_CANCEL_*`, `EVENT_OUTCOME`). |
| `src/superclaude/cli/eval/__init__.py` | Exported `CancellationToken`, `SignalHandlerInstaller`, `EXIT_INTERRUPTED`, `DEFAULT_INTERRUPT_SIGNALS`. |
| `tests/cli/eval/test_signal_handling.py` | **New.** 25 tests covering NFR-REL1 ACs + production cancel path. |
| `.dev/releases/current/cliEval/artifacts/D-0050/spec.md` | **New.** Contract spec. |
| `.dev/releases/current/cliEval/artifacts/D-0050/notes.md` | **New.** Implementation notes / design decisions. |
| `.dev/releases/current/cliEval/artifacts/D-0050/evidence.md` | **New.** Pointer to this summary. |

## Manual SIGINT Smoke Test

A live SIGINT smoke test against a multi-eval suite belongs to the
orchestrator wiring task (T03.15) because the orchestrator owns the
loop the signal would interrupt. The primitives shipped here are
end-to-end tested by `test_pty_driver_terminate_kills_real_subprocess`
(real subprocess kill) and by the integration suite for the runner +
token. The smoke test will be added when T03.15 wires the
`SignalHandlerInstaller` around the `ThreadPoolExecutor`.
