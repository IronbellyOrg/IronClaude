# D-0057 RunOrchestrator — Design Notes

Companion to `spec.md`. These notes capture the design decisions made while
implementing T03.15 (COMP-003 `RunOrchestrator`), the alternatives considered,
and the reasoning behind the contract chosen.

## Why a worker callable instead of owning EvalRunner construction

The first sketch had `RunOrchestrator.__init__` take the wiring needed to build
an `EvalRunner` per spec (home root, config, executor, deploy hooks, …) and
internally instantiate one runner per submitted spec. This was rejected for
three reasons:

1. **Per-eval state the orchestrator cannot resolve.** `EvalRunner` requires a
   per-eval HOME isolation directory, a per-eval `run_dir`/`artifacts_dir`, and
   per-eval log file paths. Allocating those is the loader/runner layer's job
   (T03.05/T03.07), not the scheduler's. Pushing the allocation into
   `RunOrchestrator` would couple it to filesystem layout decisions that live
   outside D-0057.
2. **Testability.** With the worker callable contract
   (`EvalWorker = Callable[[EvalSpec], EvalOutcome]`), the orchestrator's unit
   tests use trivial stub workers (lambdas, classes with `__call__`,
   instrumented closures that record concurrency) without needing to stand up a
   real isolated HOME, pty pipeline, or hook deploy. The 20 tests in
   `tests/cli/eval/test_orchestrator.py` therefore exercise scheduling
   behaviour in isolation from runner internals.
3. **Composition over configuration.** The production call site (Phase 5
   `superclaude eval` CLI) composes the worker once:

   ```python
   def worker(spec: EvalSpec) -> EvalOutcome:
       runner = EvalRunner(home=..., config=..., executor=..., run_dir=...,
                          artifacts_dir=..., stdout_path=..., stderr_path=...,
                          transcript_path=..., expect_callables=...,
                          deploy_hooks=..., default_timeout_sec=...,
                          clock=..., cancellation_token=token, retry_count=0)
       return runner.run(spec)

   orchestrator = RunOrchestrator(run_one=worker, cancellation_token=token)
   outcomes = orchestrator.run(specs, parallel=parallel)
   ```

   This keeps the orchestrator focused on the one thing it owns: the
   `ThreadPoolExecutor + as_completed` scheduling loop.

## Why ThreadPoolExecutor + as_completed (and not asyncio)

The release spec (`AC6`) and `cli/prd/executor.py:774-802` both prescribe the
synchronous `ThreadPoolExecutor + as_completed` pattern. `EvalRunner` itself is
blocking (pty I/O, subprocess.Popen, signal handling), so an asyncio bridge
would add complexity without parallelism gains. Threads share the GIL but the
blocking time is dominated by I/O wait, so threads are sufficient.

## Why pre-allocate `outcomes[None] * len(specs)` instead of appending

`as_completed` yields futures in **completion** order, not submission order.
The `RunOrchestrator.run()` contract is that the returned list of outcomes
preserves the order of the input `specs`. Pre-allocating a list and indexing by
submission position is the simplest way to satisfy both constraints without
sorting at the end. `test_outcome_order_matches_input_order` covers this.

## Why fold worker exceptions into `ERRORED` outcomes

The N'-vs-K invariant (`len(outcomes) == counts.expanded_n_prime`, FR-RPT1)
requires one outcome per spec. If a worker raised, propagating the exception
would break the invariant and force the CLI layer to reconcile a partial list.
Instead, `RunOrchestrator._errored_outcome` synthesises a minimal
`EvalOutcome(status="ERRORED", duration_sec=0.0, error_class=<exc class name>)`
and the schedule loop continues. The CLI/reporter layer downstream sees a
clean per-spec list and can render the error class in the report.

A separate question is whether `KeyboardInterrupt`/`SystemExit` should fold or
propagate. The current implementation catches `BaseException` so the loop
finishes draining (other in-flight workers still get a chance to return their
outcomes); cancellation propagates through the `CancellationToken`, not through
exception propagation. Tests `test_runtime_error_from_worker_folds_to_errored`
and the cancellation suite cover both paths.

## Why pre-flight cancellation check before submission

`_is_cancelled()` is checked twice in the schedule loop:

1. **Before submission** — if the token fires while specs are being submitted,
   all remaining specs are appended to `cancelled_indices` and synthesised as
   `INTERRUPTED` outcomes after the pool drains. This avoids submitting work
   that will immediately be cancelled.
2. **In-flight** — already-submitted workers see the cancellation token via
   `EvalRunner`'s own cooperative cancel path; the orchestrator does not
   interrupt them externally.

The `test_mid_run_cancel_stops_new_submissions` test demonstrates this: with
parallel=2 and 5 specs, after the first batch completes the token fires; the
already-submitted-but-not-yet-completed work finishes, and the rest is
synthesised as `INTERRUPTED`.

## Why reject `bool` parallel explicitly

In Python, `bool` is a subclass of `int`, so `isinstance(True, int)` is
`True` and `True < 1` is `False`. Without an explicit `isinstance(parallel,
bool)` guard, `RunOrchestrator.run(specs, parallel=True)` would silently
coerce to `parallel=1`. The explicit guard surfaces the type confusion at the
call site (`TypeError`) rather than degrading the scheduler to single-threaded
operation. Test: `test_boolean_parallel_rejected`.

## Why MIN=1 and MAX=15 (not 0 and unbounded)

- **MIN=1**: `parallel=0` would deadlock `ThreadPoolExecutor` (no workers, no
  progress). The release spec range `[1, 15]` excludes zero. Negative values
  are nonsensical for a worker count.
- **MAX=15**: NFR-PERF2 caps RAM at ≤2.25GB. With each EvalRunner needing up
  to 150MB peak (pty + python + hook subprocess working set in worst-case),
  15 × 150MB ≈ 2.25GB. The clamp is a hard guarantee — even if the CLI
  passes `parallel=20` (T03.10's `--parallel` flag accepts up to 20 for
  forward-compat), the scheduler refuses to spawn more than 15 threads.

## Out-of-scope items deliberately not implemented

These belong in other tasks; D-0057 scope ends at the scheduling primitive:

- **Progress reporting** — JSONL emission is FR-RPT2's job; the orchestrator
  returns a list, it does not stream events.
- **Retry policy** — NFR-REL2 says no retries. The orchestrator does not loop;
  worker exceptions become `ERRORED` immediately.
- **Signal handler installation** — `SignalHandlerInstaller` is set up by the
  CLI entry point (Phase 4 task), the orchestrator accepts the resulting
  token.
- **`EvalRunner` construction** — handled by the CLI wiring layer (see "Why a
  worker callable" above).

## Reference implementation

- Pattern source: `src/superclaude/cli/prd/executor.py:774-802`
  (`run_in_parallel` method on `PRDExecutor` — same `ThreadPoolExecutor +
  as_completed` loop, same `shutdown_requested` pre-flight pattern, same
  exception folding shape).
- Spec source: `.dev/releases/current/cliEval/artifacts/D-0050/spec.md`
  (NFR-REL1 cancellation contract — orchestrator allocates token, installs
  handler around pool, T03.15 owns the wiring).

## Verification evidence

See `evidence.md` in this directory for verbatim pytest output. Summary:

- 20/20 orchestrator unit tests pass in 0.48s.
- 56/56 regression tests pass across orchestrator + runner_class + signal_handling
  in 2.06s.
- No regressions in the broader suite.
