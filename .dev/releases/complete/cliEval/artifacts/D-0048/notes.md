# D-0048 — FR-LC1 EvalRunner lifecycle implementation notes

## Design decisions

### `LifecycleExecutor` Protocol vs. concrete class

The runner skeleton must be testable without spinning up a real
`PtyDriver` + `ClaudeProcessAdapter`. Three shapes were considered:

1. **Concrete `EvalRunner` class with PTY hard-wired** — rejected:
   forces every lifecycle unit test to build a fake PTY, and bakes
   COMP-004 (T03.05) details into a T03.04 deliverable.
2. **Function with a single `spawn_observe(...)` callable** —
   rejected: collapses three distinct lifecycle phases (spawn / inject
   / observe per design-spec §6) into one callable, so the runner can
   no longer distinguish "spawn failed" from "observe failed" in the
   `error_class` field, and tests cannot assert that step 3 ran but
   step 4 did not.
3. **Protocol with three methods** (chosen) — `LifecycleExecutor`
   surfaces `spawn(ctx) -> None`, `inject(ctx) -> None`, and
   `observe(ctx) -> ObservedRun`. Production wiring (T03.05) plugs in
   a `PtyClaudeExecutor` that delegates to `ClaudeProcessAdapter` +
   `PtyDriver`; tests substitute a `RecordingExecutor`.

The Protocol is *structural*: no `register()` call needed. Pythonic
duck typing means `RecordingExecutor` does not need to inherit from
`LifecycleExecutor`; a single `_PROTOCOL_CHECK: LifecycleExecutor =
RecordingExecutor()` in the test file pins the structural conformance
so a future field addition fails the test at import time.

### `ExecutorContext` vs. raw arguments

The executor needs a stable handle on the per-eval HOME, the run
paths, and the env overlay. Two options:

1. **Pass each path as a positional argument to `spawn`** — rejected:
   adding a new path (e.g. T03.05's per-eval JSONL log) is a breaking
   change for every executor implementation, including test stubs.
2. **Frozen `ExecutorContext` dataclass** (chosen) — bundles
   `eval_spec`, `home`, `home_path`, `run_dir`, `artifacts_dir`,
   `stdout_path`, `stderr_path`, `transcript_path`, and `env`. Future
   field additions are non-breaking for executors that ignore them;
   T03.05 can grow the context with `jsonl_log_path` without
   touching `RecordingExecutor`.

`ExecutorContext` is intentionally distinct from `EvalContext`
(DM-010 / T03.03): the executor sees the pre-observe view (no
exit_code yet), the ExpectCallables see the post-observe view (15
fields, exit_code populated). Mixing them would force the executor to
either dereference fields that do not yet exist or accept a
half-populated record.

### `ObservedRun` carries `artifacts` and `jsonl_paths`

`ObservedRun` is the *executor return type* and is folded into both
`EvalOutcome.artifacts` and `EvalContext.{jsonl_paths,artifacts}`.
The choice to model these as `Mapping` fields with `MappingProxyType`-
compatible defaults mirrors the same immutability discipline the
DM-010 `EvalContext` uses (T03.03 / D-0047): an executor that returns
an `ObservedRun` containing a plain `dict` cannot be mutated by the
runner after-the-fact (the dataclass is frozen) but the runner *can*
re-wrap the mapping in `MappingProxyType` before threading it into
`EvalContext.from_runner_state(...)` — and does.

### Per-step `try`/`except` rather than a single outer `try`

The status mapping requires the runner to know *which* step raised so
`error_class` reflects the exception's classname and so the
status-mapping helper can distinguish "observe never ran" (pin
`duration_sec` to 0.0) from "observe ran but an Expect raised" (keep
the observed duration). Three options:

1. **Outer `try`/`except` only** — rejected: forces the classification
   helper to inspect the traceback to figure out which step raised.
2. **One `try`/`except` per step with a shared `_finalize` exit**
   (chosen) — each step's `except` calls `state.record_harness_failure(
   step=..., exc=...)` then returns through `_finalize(...)`. The
   classification helper reads `state.harness_failure_step` to decide
   whether to pin `duration_sec` to 0.0.
3. **`with`-style context manager per step** — rejected: the
   `__exit__` would either need to re-raise (defeating the capture)
   or swallow (defeating SIGINT propagation). The plain `try`/`except`
   stays simpler.

### `KeyboardInterrupt` / `SystemExit` propagation

NFR-REL1 (T03.07) requires cooperative cancellation: the orchestrator
installs a signal handler that converts `SIGINT` / `SIGTERM` into a
`KeyboardInterrupt` / `SystemExit` raised inside the runner. The
runner MUST NOT classify these as `ERRORED` — they are a graceful
shutdown signal, not a harness bug. Three options:

1. **Re-raise from every `except`** (chosen) — each per-step
   `except (KeyboardInterrupt, SystemExit): raise` re-raises before
   the broad `except BaseException` runs. The outer `try`/`except`
   then catches `(KeyboardInterrupt, SystemExit)` to run
   `_safe_teardown(home, keep=True)` before re-raising again. The
   orchestrator's signal handler converts the propagated exception
   into an `INTERRUPTED` outcome at the suite layer.
2. **Catch and convert to `EvalOutcome(status="INTERRUPTED")`** —
   rejected: the runner cannot tell whether the orchestrator is also
   tearing down. Returning an outcome when the process is mid-
   shutdown would leak the partial summary to the Reporter and cause
   the harness to "succeed" through a Ctrl-C.
3. **Catch only `KeyboardInterrupt`, let `SystemExit` propagate
   untouched** — rejected: NFR-REL1 must cover both signals
   uniformly. Diverging behaviour for the two would surprise
   operators.

### Teardown is best-effort (does NOT flip status)

The design-spec invariant is "teardown is best-effort": a failing
teardown must not flip `PASS` to `FAIL`. Three options:

1. **Re-raise the teardown exception** — rejected: a permissions
   error in `shutil.rmtree` would convert every clean PASS into an
   error, which contradicts the spec.
2. **Capture the exception silently** — rejected: losing the
   traceback makes debugging cleanup bugs impossible.
3. **Swallow with optional `on_teardown_error` callback** (chosen) —
   the callback is `Optional[Callable[[BaseException], None]]`; the
   COMP-004 runner class (T03.05) plugs in a callback that writes the
   exception to its per-eval JSONL log. The callback itself is
   guarded by a secondary `try`/`except` so a buggy callback cannot
   re-raise out of teardown.

### Why `keep_home_on_pass` defaults to `False`

The atomic-setup contract (T02.13) keeps partial HOMEs on disk for
forensics. By symmetry, the runner forces `teardown(keep=True)` on
every non-PASS outcome. PASS outcomes are the only branch that
honours the caller's preference — and the default is `False` so the
scratch root does not fill up with successful-eval HOMEs over a long
suite run. The `--keep-home` CLI flag (T03.18) flips the default at
the orchestrator layer when an operator wants to inspect a passing
eval's HOME.

### Why `duration_sec` is pinned to `0.0` for steps 1-5 failures

`_LifecycleState.observed` starts at the `_NO_OBSERVED_RUN` sentinel
with `duration_sec=0.0`. If observe never ran (or raised), the
sentinel's value is meaningful: the Reporter renders `0.0` as
"unknown" rather than a stale value from a prior eval. The
`_finalize` helper explicitly checks `harness_failure_step in {setup,
deploy_hooks, spawn, inject, observe}` and overrides any non-zero
value, because a future ObservedRun default could theoretically carry
a non-zero baseline.

### Module-level `deploy_hooks_to` import vs. lazy resolution

`deploy_hooks_to` (T02.14) is the default for the `deploy_hooks`
parameter so production callers do not have to spell it out, but
tests can override it with a stub. Two options:

1. **Lazy import inside `run_eval`** — rejected: every call would
   pay the import cost, and the default would be impossible to
   override at function-definition time.
2. **Top-of-module import** (chosen) — the function is captured by
   the default-argument bind at definition time, which is the
   standard Python idiom. The import does pull in `install_hooks` but
   that module is already loaded by the time the eval CLI is
   running.

## Future work touchpoints

* **T03.05 (COMP-004 EvalRunner class)** — wraps `run_eval` with
  per-eval JSONL logging (passes a real `on_teardown_error` callback),
  per-eval timeout enforcement (uses `signal.SIGALRM` or a
  `threading.Timer` to raise `TimeoutError` inside `executor.observe`,
  then classifies it as `TIMEOUT` once the spec rule swaps from
  `ERRORED`), and the production `PtyClaudeExecutor` implementation
  of `LifecycleExecutor`.
* **T03.07 (NFR-REL1 signal handling)** — installs the orchestrator
  signal handler that catches the propagated `KeyboardInterrupt` /
  `SystemExit` and emits an `EvalOutcome(status="INTERRUPTED")` at
  the suite layer.
* **T03.08 (capability-gate SKIPPED branch)** — runs the
  `CapabilityResolver` BEFORE invoking `run_eval`; an unresolved
  capability synthesises an `EvalOutcome(status="SKIPPED",
  skip_reason=..., skip_flag_triggered=...)` and never enters the
  lifecycle.
* **T04.01..T04.07 (Expect primitives)** — implement
  `ExpectCallable` functions that read the 15-field `EvalContext` the
  runner builds via `EvalContext.from_runner_state(...)`.

## Testability discipline

`HomeIsolation` is a frozen dataclass and its methods cannot be
monkey-patched per-test. The lifecycle test file introduces a
`FakeHome` duck-typed double exposing the same `setup` / `teardown` /
`env` / `home_path` surface; the real `HomeIsolation` contract is
covered by `test_home_isolation.py`, `test_atomic_setup.py`,
`test_containment.py`, and `test_hard_guard_real_home.py`. The fake
exists solely to make lifecycle scripting (per-test setup / teardown
overrides) ergonomic — production wiring uses the real
`HomeIsolation` via the same surface.
