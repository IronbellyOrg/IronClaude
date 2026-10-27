# D-0057 — COMP-003 RunOrchestrator

**Task:** T03.15 (Phase 3, Roadmap COMP-003 / R-057)
**Module:** `src/superclaude/cli/eval/orchestrator.py`
**Tests:** `tests/cli/eval/test_orchestrator.py`
**Status:** Implemented 2026-05-20

## 1. Goal

Schedule per-spec `EvalRunner` workers in parallel via
`concurrent.futures.ThreadPoolExecutor + as_completed` — the AC6
pattern the cliEval design-spec pins (referenced shape:
`src/superclaude/cli/prd/executor.py:774-802`). The orchestrator owns
three cross-cutting concerns the lifecycle layer (T03.04) and runner
class (T03.05) deliberately deferred:

1. **Concurrency budget** — `max_workers` clamped to `[1, 15]` per
   design-spec §11 / NFR-PERF2 with default `8`.
2. **Outcome contract** — one `EvalOutcome` per input `EvalSpec`, in
   input order, regardless of completion order (the Reporter / FR-RPT1
   N'-vs-K invariant relies on this).
3. **Cooperative cancellation** — when the shared `CancellationToken`
   (NFR-REL1 / T03.07) flips, scheduling stops and unsubmitted specs
   synthesise an `INTERRUPTED` outcome so the per-spec contract still
   holds.

The orchestrator does **not** install signal handlers. That belongs to
the CLI dispatcher (Phase 4): the dispatcher allocates a token, wraps
the orchestrator call in a `SignalHandlerInstaller`, and threads the
token down so runners observe the same flag the signal handler flips.

## 2. Public Surface

```python
from superclaude.cli.eval.orchestrator import RunOrchestrator, EvalWorker
from superclaude.cli.eval.signal_handler import CancellationToken
```

### 2.1 `EvalWorker`

Type alias:

```python
EvalWorker = Callable[[EvalSpec], EvalOutcome]
```

A worker callable wraps everything from per-eval HOME allocation through
`EvalRunner.run`. Keeping the orchestrator agnostic of construction
details lets the CLI dispatcher own resource allocation and lets tests
substitute a stub worker that returns a canned outcome.

### 2.2 `RunOrchestrator`

| Attribute / method | Contract |
|---|---|
| `DEFAULT_PARALLEL: ClassVar[int] = 8` | Default concurrency level. |
| `MIN_PARALLEL: ClassVar[int] = 1` | Minimum accepted `parallel`. Values below raise `ValueError`. |
| `MAX_PARALLEL: ClassVar[int] = 15` | Upper bound; values above saturate. |
| `__init__(*, run_one, cancellation_token=None)` | Worker callable + optional token. Non-callable `run_one` raises `TypeError`. |
| `run(specs, *, parallel=DEFAULT_PARALLEL) -> list[EvalOutcome]` | Schedule and collect outcomes. Empty `specs` → `[]`. |

### 2.3 Outcome shape

The orchestrator emits two synthesised outcome shapes itself:

| Shape | Trigger | Status | `duration_sec` | `error_class` |
|---|---|---|---|---|
| Interrupted | Cancellation token set before spec submitted | `INTERRUPTED` | `0.0` | `None` |
| Errored | Worker callable raised | `ERRORED` | `0.0` | `f"{type(exc).__module__}.{type(exc).__qualname__}"` |

Every other outcome shape is returned verbatim from the worker —
notably `PASS` / `FAIL` / `TIMEOUT` / `INTERRUPTED` from the in-runner
classification (D-0049 / D-0050).

## 3. Scheduling Pattern

```python
with ThreadPoolExecutor(
    max_workers=max_workers, thread_name_prefix="cliEval"
) as pool:
    futures: dict[Future[EvalOutcome], int] = {}
    for index, spec in enumerate(specs):
        if self._is_cancelled():
            cancelled_indices.append(index)
            continue
        futures[pool.submit(self._invoke_worker, spec)] = index

    for future in as_completed(futures):
        index = futures[future]
        try:
            outcomes[index] = future.result()
        except BaseException as exc:  # noqa: BLE001
            outcomes[index] = self._errored_outcome(specs[index], exc)

for index in cancelled_indices:
    outcomes[index] = self._interrupted_outcome(specs[index])
```

Notes:

* `outcomes` is pre-allocated and indexed by submission order so the
  return-value order is independent of completion order.
* The cancellation check is per-spec inside the submission loop, not
  per-future. In-flight runners observe the same token via
  `EvalRunner._cancellation_token` (D-0050) and convert worker-thread
  `KeyboardInterrupt` / `SystemExit` into `INTERRUPTED` outcomes
  themselves — the orchestrator never has to translate an exception
  into a status.
* `thread_name_prefix="cliEval"` makes per-eval threads identifiable in
  `py-spy` / `ps` output for diagnosing hangs.

## 4. Parallelism Validation

`tests/cli/eval/test_orchestrator.py::test_three_eval_suite_runs_faster_than_3x_sequential`
asserts the runtime contract directly:

* 3 specs × 0.2s sleep each.
* `parallel=3`.
* Elapsed must be `< 3 × eval_duration_sec` (i.e. `< 0.6s`). A truly
  serialised execution would be ≥ 0.6s. The 2× margin absorbs
  ThreadPoolExecutor startup overhead on slow CI hosts.

Concurrency-bound tests
(`test_parallel_above_max_clamps_to_fifteen`,
`test_parallel_one_serialises`) snapshot the maximum number of workers
running simultaneously to confirm the clamp is honoured at runtime, not
just at validation time.

## 5. Out of Scope

* **Signal handler installation.** Phase 4 CLI dispatcher owns this.
* **Partial summary writing.** Reporter (COMP-008 / T03.13) reads the
  outcomes the orchestrator returns and persists `summary.{md,json}`.
* **Exit-code translation.** Phase 4 dispatcher maps the outcome set
  to `EXIT_INTERRUPTED` (`3`), `1`, `2`, or `0` per design-spec §4.
* **Per-eval timeout enforcement.** Already in `EvalRunner` (D-0049 +
  D-0050); the orchestrator never time-slices a single eval.
* **15-eval isolation integration scenario.** T03.16 owns the end-to-end
  proof; this deliverable owns only the scheduling primitive.

## 6. Failure Modes & Containment

| Mode | Behaviour |
|---|---|
| `parallel < 1` | `ValueError` raised before any submission. |
| `parallel` not `int` (or `bool`) | `TypeError` raised. |
| `parallel > 15` | Saturates to `MAX_PARALLEL = 15`. |
| Worker raises | Folded into `ERRORED` outcome with `error_class`. `run()` never re-raises. |
| Token pre-cancelled | No worker is submitted; every spec receives an `INTERRUPTED` outcome. |
| Token cancelled mid-run | Specs already submitted run to completion (their in-runner observation of the same token converts them to `INTERRUPTED` if they have not finished); unsubmitted specs get synthesised `INTERRUPTED`. |
| `run_one` not callable at construction | `TypeError` from `__init__`. |
| Empty `specs` | Returns `[]` immediately; no pool started. |

## 7. Acceptance Criteria → Test Mapping

| AC | Test |
|---|---|
| One `EvalOutcome` per expanded spec, input order preserved. | `TestOneOutcomePerSpec::test_outcome_order_matches_input_order`, `TestOneOutcomePerSpec::test_every_spec_gets_exactly_one_outcome` |
| `parallel=20` clamps to 15. | `TestParallelClamp::test_parallel_above_max_clamps_to_fifteen` |
| `parallel < 1` rejected. | `TestParallelClamp::test_zero_parallel_rejected`, `TestParallelClamp::test_negative_parallel_rejected` |
| 3-eval suite runs faster than 3× slowest-eval duration. | `test_three_eval_suite_runs_faster_than_3x_sequential` |
| Pre-cancelled token → all `INTERRUPTED`, no worker invoked. | `TestCancellation::test_pre_cancelled_token_skips_all_specs` |
| Mid-run cancel stops new submissions. | `TestCancellation::test_mid_run_cancel_stops_new_submissions` |
| Worker exception folded into `ERRORED` outcome. | `TestWorkerExceptionFolding::test_runtime_error_from_worker_folds_to_errored` |
| Constructor rejects non-callable worker. | `TestConstructorGuards::test_non_callable_worker_rejected` |

See `evidence.md` for the recorded pytest output.

## 8. References

* Reference pattern: `src/superclaude/cli/prd/executor.py:774-802`
  (PRD pipeline's parallel step scheduler).
* Upstream contracts: D-0049 (EvalRunner class), D-0050 (signal
  handling + cancellation token).
* Downstream consumers: T03.16 (FR-G2 15-eval integration), Phase 4
  CLI dispatcher (signal handler installation + exit-code translation),
  COMP-008 Reporter (FR-RPT1 N'-vs-K invariant on the returned outcome
  list).
