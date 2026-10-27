# D-0050 — Implementation Notes (T03.07)

## Design Decisions

### Cooperative cancellation vs. signal-driven thread interruption

Python's `signal` module restricts handler installation to the main
thread. The worker thread inside `EvalRunner.run()` cannot reliably be
interrupted by re-raising a signal — the runtime has no
`pthread_kill` equivalent at the Python layer.

We therefore use a `threading.Event`-backed `CancellationToken` for
cooperative cancellation:

* Pre-flight check at `EvalRunner.run()` entry — cheap and predictable.
* `executor.cancel()` is the *real* unblocker: production wraps a
  `PtyDriver` whose `terminate(force=True)` issues SIGKILL to the PTY
  child, which causes any pending `expect()` call to wake up with an
  EOF.
* If the worker raised `KeyboardInterrupt` directly (e.g. inside an
  Expect callable) we observe it on `thread.join()` return and convert
  to an `INTERRUPTED` outcome only when the token was wired. Without a
  token wired, the propagation path documented by T03.05 / FR-LC1 is
  preserved verbatim.

### Why not `signal.alarm`?

The phase task wording mentions `signal.alarm` as an option. We chose
**not** to use it because:

1. Only one `alarm` can be active per process; nested timeouts
   (per-eval) would conflict with the suite-level timeout.
2. `alarm` triggers a signal handler running on the main thread, but
   our worker thread (where the timeout matters) cannot be interrupted
   from the main thread without `pthread_kill`.
3. The existing T03.05 implementation already uses
   `Thread.join(timeout=...)` which works regardless of GIL state and
   does not interfere with the SIGINT/SIGTERM handlers.

### Duck-typed `executor.cancel()`

We deliberately did **not** add `cancel()` to the `LifecycleExecutor`
Protocol because:

1. Most test stubs do not need cancellation; forcing the method into
   the Protocol would force every stub to grow a no-op `cancel`.
2. The production `ClaudeProcessAdapter` (D-0044 / T02.16) already has
   the kill + reap implementation; we only need to call it.
3. The cancel call is a best-effort cleanup, not a contract assertion.
   The runner records `executor_cancel_skipped` when the method is
   missing so post-mortem tooling still sees the attempt.

### Token semantics — one-shot, not resettable

A `CancellationToken` is allocated per run and never reset. This avoids
TOCTOU races where the orchestrator could reset the token *after* a
worker has already observed `is_cancelled() == True` but *before* the
worker's KeyboardInterrupt converted to an INTERRUPTED outcome. The
harness allocates fresh tokens for fresh runs.

### Signum capture — first-call-wins

If the user hits Ctrl-C twice in rapid succession (SIGINT, then again),
we capture **the first signum** rather than the second. Rationale: the
partial summary reads "interrupted by SIGINT" not "interrupted by
SIGINT-then-SIGINT-then-..." — the first signal is what stops the run;
later ones are noise. The boolean return from `cancel()` lets the
orchestrator distinguish "I cancelled" from "I observed an
already-cancelled token" if that distinction ever matters.

## Test Coverage Highlights

* **25 tests** total in `tests/cli/eval/test_signal_handling.py`:
  * 10 `CancellationToken` tests covering single/double cancel, signum
    capture, concurrent wait, default constants.
  * 8 `SignalHandlerInstaller` tests covering install/restore round
    trip, real signal delivery via `signal.raise_signal`, callback
    invocation + failure swallowing, idempotency, main-thread guard,
    empty signals validation.
  * 5 EvalRunner integration tests covering pre-cancelled token,
    in-flight KeyboardInterrupt with/without token, timeout +
    `executor.cancel()`, cancel failure swallowed, executor without
    cancel method.
  * 1 end-to-end PtyDriver real-subprocess kill + zombie reap test
    (uses `/proc/<pid>` to assert reaping).
* Test for real-subprocess kill is `pytest.importorskip("pexpect")` so
  CI without pexpect simply skips it. Locally with pexpect installed
  the test confirms `/proc/<pid>` is gone within 5 seconds of
  `terminate(force=True) + close()`.

## Regression Surface

* `tests/cli/eval/test_runner_class.py` — 11 tests including
  `test_keyboard_interrupt_in_expect_propagates` (the T03.05 AC4
  regression that ensures legacy callers without a token still get the
  exception). All pass.
* `tests/cli/eval/test_eval_lifecycle.py` — 22 tests covering the FR-LC1
  skeleton. All pass.
* Full `tests/cli/eval/` suite — **817 passed**, no regressions.

## Open Questions / Follow-ups (out of scope for T03.07)

* **Partial summary writer.** The reporter (COMP-008 / T03.13) needs to
  consume the JSONL log + the cancelled futures from the orchestrator
  to produce the partial-summary file. We left
  `SignalHandlerInstaller.on_signal` as the hook for it but did not
  implement.
* **Orchestrator integration.** T03.15 will allocate a shared
  `CancellationToken`, install the handler around the
  ThreadPoolExecutor, and translate cancelled futures into
  `EvalOutcome(status="INTERRUPTED")` rows. The `cancellation_token`
  kwarg on `EvalRunner` is the wiring point.
* **`exit_code` plumbing.** The CLI dispatcher (Phase 4) will check
  `token.is_cancelled()` after the orchestrator returns and use
  `EXIT_INTERRUPTED` instead of the FAIL exit code (1).
