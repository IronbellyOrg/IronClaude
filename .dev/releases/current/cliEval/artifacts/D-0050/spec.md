# D-0050 — NFR-REL1 Signal Handling and Per-Eval Cancellation

| Field | Value |
|---|---|
| Task | T03.07 |
| Component(s) | `signal_handler.py`, `runner.py` (EvalRunner) |
| Roadmap | R-050 (NFR-REL1) |
| Spec refs | design-spec §4 (Exit codes), §12 (Signal handling), §13 (Reliability), FR-LC1, NFR-REL1 |
| Depends on | D-0048 (FR-LC1 skeleton), D-0049 (EvalRunner class), D-0036 (PtyDriver) |
| Consumed by | D-0058/D-0059 (Orchestrator T03.15), D-0090 (Reporter partial summary), Phase-4 CLI dispatcher |

## 1. Goal

Provide the *cancellation primitives* the harness needs so that:

* Pressing `Ctrl-C` (SIGINT) or receiving SIGTERM during a parallel
  run cancels every in-flight eval, classifies them as `INTERRUPTED`,
  lets the orchestrator write a partial summary, and surfaces process
  exit code `3` to the CLI shell.
* When an individual eval exceeds its `EvalSpec.timeout_sec` budget the
  runner kills the underlying PTY subprocess and reaps the zombie so the
  next eval in the queue starts in a clean process table, producing an
  `EvalOutcome` with status `TIMEOUT`.

This deliverable ships the *primitives*. Wiring the primitives into the
CLI entrypoint (signal handler installation around the orchestrator) and
the partial-summary writer belongs to T03.15 / Phase 4.

## 2. Public Surface

```python
from superclaude.cli.eval.signal_handler import (
    EXIT_INTERRUPTED,            # int = 3
    DEFAULT_INTERRUPT_SIGNALS,   # (SIGINT, SIGTERM)
    CancellationToken,
    SignalHandlerInstaller,
)
from superclaude.cli.eval.runner import EvalRunner
```

### 2.1 `CancellationToken`

Thread-safe cooperative cancellation flag wrapping
`threading.Event`. One-shot: once cancelled, the token stays cancelled
for the rest of its lifetime; the harness allocates a fresh token per
run rather than resetting.

| Method | Contract |
|---|---|
| `cancel(*, signum=None) -> bool` | Flip to cancelled. Returns `True` on the first call, `False` thereafter. First call captures `signum` (read via `.signum`); subsequent calls do **not** overwrite. |
| `is_cancelled() -> bool` | Non-blocking poll. |
| `wait(timeout=None) -> bool` | Blocking wait honouring `Event.wait` semantics. |
| `.signum -> Optional[int]` | The signal number that triggered cancellation, if any. |

### 2.2 `SignalHandlerInstaller`

Context manager binding configured signals (default
`SIGINT, SIGTERM`) to a handler that:

1. Calls `token.cancel(signum=signum)`.
2. Invokes the optional `on_signal(signum, frame, token)` callback.
   Failures inside the callback are swallowed because signal handlers
   must always return cleanly.

On `__exit__` / `restore()` the previous handlers (captured at install
time) are restored — installing twice is idempotent.

Constraints:

* Must be installed from the main thread. Off-main-thread install raises
  `ValueError` (mirrors `signal.signal`'s own restriction).
* Empty `signals` iterable rejected with `ValueError`.
* `restore()` is a no-op when called without a prior `install()`.

### 2.3 `EvalRunner` integration

`EvalRunner.__init__` accepts a new optional kwarg
`cancellation_token: CancellationToken | None`. When wired:

| Trigger | Behaviour | Outcome |
|---|---|---|
| Token already cancelled at `run()` entry | Skip the lifecycle entirely; do **not** call `home.setup` or `executor.spawn`; emit `interrupted_fired` + `outcome` events; flush log. | `INTERRUPTED`, `duration_sec=0.0`, `error_class=None` |
| Worker thread raises `KeyboardInterrupt` / `SystemExit` | Set the token (defensive) and convert into an INTERRUPTED outcome; invoke best-effort `executor.cancel()` and `home.teardown(keep=True)`; flush log. | `INTERRUPTED` |
| Per-eval timeout expires (`thread.join(timeout)` returns alive) | Emit `timeout_fired`; invoke `executor.cancel()` from the main thread to kill the PtyDriver + reap zombie; emit `executor_cancel_*` events; run `home.teardown(keep=True)`; flush log. | `TIMEOUT`, `error_class="builtins.TimeoutError"`, `duration_sec=timeout_sec` |

If `cancellation_token` is **not** wired, the pre-existing FR-LC1 /
T03.05 contract is preserved verbatim — `KeyboardInterrupt` propagates
to the caller (regression-tested by
`test_keyboard_interrupt_in_expect_propagates`).

`executor.cancel()` is duck-typed via `getattr(self._executor, "cancel", None)`:

* Production executor (`ClaudeProcessAdapter` driving `PtyDriver`)
  exposes a `cancel()` that issues `PtyDriver.terminate(force=True)`
  followed by `close()` so the child receives SIGKILL and `wait()` reaps
  the resulting zombie.
* Test stubs / executors without cancellation simply omit the method;
  the runner records an `executor_cancel_skipped` event in the JSONL log
  and continues.

All cancel failures are swallowed: a TIMEOUT or INTERRUPTED outcome must
always return cleanly so the orchestrator can collect it. The error is
recorded as `executor_cancel_error` with `error_class` + `message`.

## 3. New JSONL Events (additive)

Recorded by `EvalRunner` in the per-eval JSONL log under
`home_path/.eval-logs/<eval_id>.jsonl`. Each row preserves the
D-0049 five-field shape (`event`, `ts_offset_sec`, `eval_id`, `step`,
`extra`).

| Event | Step | Extra fields | Emitted when |
|---|---|---|---|
| `timeout_fired` | `"timeout"` | `{"timeout_sec": float}` | Per-eval timeout budget exceeded. |
| `interrupted_fired` | `"interrupt"` | `{}` | Pre-cancelled token detected or worker `KeyboardInterrupt` / `SystemExit` observed with token wired. |
| `executor_cancel_started` | `"timeout"` / `"interrupt"` | `{}` | Runner is about to call `executor.cancel()`. |
| `executor_cancel_completed` | `"timeout"` / `"interrupt"` | `{}` | `cancel()` returned without raising. |
| `executor_cancel_error` | `"timeout"` / `"interrupt"` | `{"error_class": str, "message": str}` | `cancel()` raised; failure is swallowed. |
| `executor_cancel_skipped` | `"timeout"` / `"interrupt"` | `{"reason": str}` | Executor has no `cancel` method. |
| `outcome` | `"outcome"` | `{"status": str, "duration_sec": float, "error_class": Optional[str]}` | Terminal classification (`INTERRUPTED` / `TIMEOUT` / `PASS` / `FAIL` / `ERRORED`). |

Existing T03.05 events (`setup_*`, `spawn_*`, `inject_*`, `observe_*`,
`assertion_*`, `teardown_*`) are unchanged.

## 4. Exit Code Contract

`EXIT_INTERRUPTED = 3` is exported so the CLI dispatcher (Phase 4) and
the orchestrator (T03.15) share a single source of truth. Mapping per
design-spec §4:

| Condition | Exit code |
|---|---|
| All evals PASS (or XFAIL / SKIPPED only) | 0 |
| At least one FAIL / XPASS / TIMEOUT / ERRORED | 1 |
| Harness setup error (schema, capability gate, scratch root) | 2 |
| SIGINT / SIGTERM observed during a run | 3 |

This deliverable owns *only* the `EXIT_INTERRUPTED` constant + the
CancellationToken/SignalHandlerInstaller wiring. The dispatcher that
calls `sys.exit(3)` lands in Phase 4.

## 5. Out of Scope

* **Partial-summary writing.** The reporter
  (COMP-008 / T03.13) is responsible for persisting the interrupted run
  summary. `SignalHandlerInstaller.on_signal` is the hook the
  orchestrator can use to call into the reporter, but no concrete
  writer ships here.
* **Orchestrator wiring.** Allocating the shared `CancellationToken`,
  installing the handler around the ThreadPoolExecutor, and translating
  cancelled futures into outcomes belongs to T03.15.
* **Retry policy.** NFR-REL2 (T03.08) builds on top of these
  primitives.
* **`signal.alarm`-based per-eval timeout.** The runner already uses a
  `threading.Thread.join(timeout=...)` strategy (T03.05) that does not
  hold the GIL or interfere with the main-thread signal handler.
  Switching to `signal.alarm` would conflict with the signal handler
  installer; we explicitly do not use it.

## 6. Failure Modes & Containment

* **Token cancelled mid-step.** The runner does not interrupt the
  worker thread synchronously. The token's role is to (a) prevent the
  orchestrator scheduling further evals and (b) let the runner detect
  the worker's eventual `KeyboardInterrupt` / `SystemExit` and convert
  it to `INTERRUPTED`. PtyDriver kill is the lever that actually unblocks
  a stuck `expect()` call.
* **Executor `cancel()` raises.** Logged as `executor_cancel_error`;
  TIMEOUT / INTERRUPTED outcome still returns. The zombie may persist,
  but the harness exit will reap it via the daemon-thread
  `Thread.join` semantics.
* **Handler called from non-main thread.** `SignalHandlerInstaller`
  refuses to install (Python restriction); the orchestrator must
  install before spawning worker threads.
* **Restoration failure.** Best-effort: `signal.signal` errors during
  `restore()` are swallowed so harness shutdown is never blocked.

## 7. Acceptance Criteria → Test Mapping

| AC | Test |
|---|---|
| `CancellationToken` thread-safe one-shot + signum capture. | `TestCancellationToken::*` (10 tests) |
| `SignalHandlerInstaller` install/restore/callback/main-thread guard. | `TestSignalHandlerInstaller::*` (8 tests) |
| Pre-cancelled token → `INTERRUPTED` without spawning. | `test_pre_cancelled_token_returns_interrupted_without_spawn` |
| Worker `KeyboardInterrupt` with token → `INTERRUPTED` outcome + executor cancel. | `test_keyboard_interrupt_with_token_returns_interrupted` |
| Worker `KeyboardInterrupt` without token → propagates (regression). | `test_keyboard_interrupt_without_token_propagates` |
| Per-eval timeout → `TIMEOUT` + `executor.cancel()` invoked, JSONL records `executor_cancel_*`. | `test_timeout_invokes_executor_cancel` |
| `executor.cancel()` failure is swallowed; outcome still TIMEOUT. | `test_timeout_swallows_cancel_failure` |
| Executor without `cancel` method gets `executor_cancel_skipped`. | `test_executor_without_cancel_logs_skipped` |
| Real PtyDriver child killed and reaped (zombie reap AC). | `test_pty_driver_terminate_kills_real_subprocess` |

See `evidence.md` for the recorded pytest output.
