# D-0049 — COMP-004 EvalRunner class

**Task:** T03.05 (Phase 3, Roadmap COMP-004 / R-049)
**Module:** `src/superclaude/cli/eval/runner.py`
**Status:** Implemented 2026-05-20

## Scope

T03.05 wraps the FR-LC1 lifecycle skeleton (T03.04 / D-0048) in a
`EvalRunner` class that owns two cross-cutting responsibilities the
skeleton intentionally deferred:

1. **Per-eval JSONL log** — every lifecycle transition is recorded as a
   single JSON line under `<home_path>/.eval-logs/<eval_id>.jsonl`.
   Downstream consumers (Expect.jsonl primitive — T04.03 — and
   ad-hoc post-mortem tooling) tail this file without re-parsing the
   captured stdout/stderr.
2. **Per-eval timeout** — when `EvalSpec.timeout_sec` is set, the runner
   returns an `EvalOutcome` with status `TIMEOUT` if the lifecycle does
   not return within budget. Cleanup of the underlying PtyDriver
   subprocess + zombie reaping is the contract of NFR-REL1 (T03.07);
   T03.05 only guarantees the status mapping.

The class is a thin wrapper: every step of the seven-step lifecycle is
still executed by `run_eval` (the T03.04 entrypoint). The runner injects
*logging proxies* around the user-supplied `HomeIsolation`,
`LifecycleExecutor`, `expect_callables`, and `deploy_hooks` so the JSONL
events fire at the exact moment each step begins/ends without
modifying the lifecycle skeleton.

## Public surface

```python
class EvalRunner:
    LOG_DIR_RELPATH: ClassVar[Path] = Path(".eval-logs")

    EVENT_SETUP_STARTED        = "setup_started"
    EVENT_SETUP_COMPLETED      = "setup_completed"
    EVENT_HOOKS_DEPLOYED       = "hooks_deployed"
    EVENT_SPAWN_STARTED        = "spawn_started"
    EVENT_INJECT_STARTED       = "inject_started"
    EVENT_OBSERVE_STARTED      = "observe_started"
    EVENT_OBSERVE_COMPLETED    = "observe_completed"
    EVENT_ASSERTION_STARTED    = "assertion_started"
    EVENT_ASSERTION_COMPLETED  = "assertion_completed"
    EVENT_TEARDOWN_STARTED     = "teardown_started"
    EVENT_TEARDOWN_COMPLETED   = "teardown_completed"
    EVENT_TEARDOWN_ERROR       = "teardown_error"
    EVENT_TIMEOUT_FIRED        = "timeout_fired"
    EVENT_OUTCOME              = "outcome"

    def __init__(
        self,
        *,
        home: HomeIsolation,
        config: EvalConfig,
        executor: LifecycleExecutor,
        run_dir: Path,
        artifacts_dir: Path,
        stdout_path: Path,
        stderr_path: Path,
        transcript_path: Path,
        expect_callables: Sequence[ExpectCallable] = (),
        deploy_hooks: Callable[[Path], None] = deploy_hooks_to,
        keep_home_on_pass: bool = False,
        default_timeout_sec: float | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None: ...

    def run(self, spec: EvalSpec) -> EvalOutcome: ...
```

All constructor arguments after the leading `*` are keyword-only so a
new lifecycle field cannot silently re-bind positional callers (the
convention `EvalContext.from_runner_state` and `run_eval` already
follow). `default_timeout_sec` is the fallback used when
`spec.timeout_sec is None`; `None` on both means "no timeout, run to
completion." `clock` is monotonic by default so wall-clock skew (NTP
adjustments mid-run) cannot produce negative deltas in the JSONL log.

## Per-eval JSONL log

### File location

`<home_path>/.eval-logs/<eval_id>.jsonl`

`home_path` is the directory `HomeIsolation.setup` materialises; the
runner cannot know the value until step 1 returns. Events emitted
*before* setup completes (the `setup_started` event in particular) are
buffered in memory and flushed once `home_path` becomes available. If
setup raises before `home_path` is resolved, the buffered events are
discarded — there is nowhere to write them. The Reporter does not depend
on the JSONL log; failures here never flip the EvalOutcome status.

### Event line format

Each line is a single JSON object. Field order is stable across runs so
diffing two log files of the same eval stays reviewable:

```json
{
  "event": "<event-name>",
  "ts_offset_sec": 0.012,
  "eval_id": "ExampleEval1",
  "step": "spawn",
  "extra": { "...": "..." }
}
```

| Field            | Type   | Notes |
|------------------|--------|-------|
| `event`          | string | One of the `EVENT_*` class constants. |
| `ts_offset_sec`  | float  | Seconds since `EvalRunner.run()` began. Monotonic clock; never negative. Rounded to microseconds (`round(value, 6)`) so JSON diff output stays compact and stable. |
| `eval_id`        | string | The eval id this log records. Already regex-guarded by FR-SCH2 upstream, so consumers can use it verbatim in filenames. |
| `step`           | string | Coarse-grained lifecycle bucket: `"setup"`, `"deploy_hooks"`, `"spawn"`, `"inject"`, `"observe"`, `"assert"`, `"teardown"`, `"timeout"`, `"outcome"`. Lets consumers grep events by lifecycle phase without enumerating every event name. |
| `extra`          | object | Event-specific payload. Always present (empty object when no extra fields). |

### Required events (acceptance criterion)

The acceptance bullet pins exactly four event names — the runner emits
each one at the documented moment. The remaining events are documented
above and below but are not load-bearing for T03.05 acceptance.

| Event                | When                                                                                       |
|----------------------|--------------------------------------------------------------------------------------------|
| `setup_started`      | Before `home.setup()` runs. Buffered in memory until `home_path` is known.                 |
| `spawn_started`      | Before `executor.spawn(ctx)` runs.                                                          |
| `assertion_started`  | Before each `ExpectCallable` runs. `extra.index` carries the zero-based index; `extra.name` is the callable's `__name__` if discoverable (`None` otherwise). |
| `teardown_started`   | Before `home.teardown(keep=...)` runs. `extra.keep` carries the resolved keep flag.        |

### Extra payload contracts (informational)

| Event                | `extra` keys                                                                |
|----------------------|------------------------------------------------------------------------------|
| `setup_started`      | (none)                                                                       |
| `setup_completed`    | `home_path` (str)                                                            |
| `hooks_deployed`     | (none)                                                                       |
| `spawn_started`      | (none)                                                                       |
| `inject_started`     | (none)                                                                       |
| `observe_started`    | (none)                                                                       |
| `observe_completed`  | `exit_code` (int), `duration_sec` (float)                                    |
| `assertion_started`  | `index` (int), `name` (str | null)                                           |
| `assertion_completed`| `index` (int), `name` (str | null), `passed` (bool)                          |
| `teardown_started`   | `keep` (bool)                                                                |
| `teardown_completed` | (none)                                                                       |
| `teardown_error`     | `error_class` (str), `message` (str)                                         |
| `timeout_fired`      | `timeout_sec` (float)                                                        |
| `outcome`            | `status` (str), `duration_sec` (float), `error_class` (str | null)           |

## Per-eval timeout

### Trigger

`EvalRunner.run(spec)` runs the lifecycle inside a daemon worker
thread (`threading.Thread(daemon=True)`). The main thread joins with
`timeout=resolved_timeout_sec`. The resolution rule:

```python
resolved_timeout_sec = spec.timeout_sec or default_timeout_sec
```

When `resolved_timeout_sec is None`, the join is unbounded and the
worker runs to completion exactly as `run_eval` would have.

### TIMEOUT handling

When `thread.join(timeout=resolved_timeout_sec)` returns while
`thread.is_alive()` is still `True`:

1. The runner emits a `timeout_fired` event carrying the resolved
   timeout value.
2. The runner emits a `teardown_started` event with `keep=True`
   (TIMEOUT preserves the partial HOME for forensics) and attempts a
   best-effort `home.teardown(keep=True)` from the main thread. Failure
   is swallowed and logged via `teardown_error`.
3. The runner constructs and returns an `EvalOutcome` with:
   - `status="TIMEOUT"`,
   - `duration_sec=resolved_timeout_sec` (the budget the eval used up),
   - `expects=()` (no assertion results trusted from a half-killed
     worker; the JSONL log retains whatever partial events the worker
     did emit before the timeout),
   - `error_class="builtins.TimeoutError"` so downstream consumers can
     group identical timeouts the same way they group `ERRORED` rows.
4. The runner writes the JSONL log (including the `outcome` event) and
   returns. The worker thread continues running detached; reaping the
   underlying PtyDriver subprocess is the contract of NFR-REL1
   (T03.07).

### Why threads, not signal.alarm

`signal.alarm` only fires on the main thread of the main process, which
makes it unsuitable for the parallel orchestrator (COMP-003 / T03.15
schedules many EvalRunner workers across a `ThreadPoolExecutor`).
Threads also let the unit tests for T03.05 exercise the timeout path
without manipulating process-wide signal state. The signal-based SIGINT
/ SIGTERM contract (cancel in-flight, mark INTERRUPTED, exit 3) is the
contract of T03.07 and is documented in `D-0050/spec.md`.

## KeyboardInterrupt / SystemExit propagation

Inside the worker thread, `run_eval` already propagates these so
NFR-REL1 can mark them as INTERRUPTED. The runner re-raises whatever
the worker raised by capturing it into a holder dict and re-raising on
the main thread after the join — the JSONL log flushes first so a Ctrl-C
mid-run does not lose the buffered events.

## Acceptance criteria → implementation map

| AC bullet (T03.05) | Implementation site |
|---|---|
| Class `EvalRunner` exposes `run(spec) -> EvalOutcome`. | `EvalRunner.run` in `runner.py`. Covered by `test_runner_class.py::test_run_returns_eval_outcome`. |
| Per-eval JSONL log written under `home_path/.eval-logs/` with at least `setup_started`, `spawn_started`, `assertion_started`, `teardown_started`. | `_JsonlLog` buffer + `_LoggingHomeProxy` / `_LoggingExecutor` / `_logging_expect` wrappers in `runner.py`. Covered by `test_runner_class.py::test_jsonl_log_written_with_required_events`. |
| Per-eval timeout honoured: tasks exceeding `EvalSpec.timeout_sec` return outcome with status `TIMEOUT`. | `_run_with_timeout` thread + join contract in `runner.py`. Covered by `test_runner_class.py::test_run_returns_timeout_when_observe_hangs` and `test_runner_class.py::test_timeout_event_recorded_in_jsonl`. |
| `artifacts/D-0049/spec.md` documents the class and logging contract. | This file. |

## Module symbol re-exports

`EvalRunner` is exported from `superclaude.cli.eval` so the
orchestrator (T03.15) and the integration tests can import it without
reaching into `runner`.

## Out of scope for T03.05

- **NFR-REL1 signal handling** (T03.07 / D-0050) — SIGINT/SIGTERM
  handlers, the cooperative cancellation flag, and the subprocess +
  zombie reap on TIMEOUT.
- **NFR-REL2 retry policy** (T03.08 / D-0051) — `retry_count=0` default
  lives on the orchestrator.
- **Parallel scheduling** (COMP-003 / T03.15) — `RunOrchestrator`
  composes many `EvalRunner` instances; T03.05 only owns one.
- **Capability-gate SKIPPED branch** — the orchestrator runs the
  capability gate before invoking `EvalRunner.run`, so SKIPPED never
  reaches the runner.
