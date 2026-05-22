# D-0035 — Notes (Task T02.15)

## Design decisions

### Why ThreadPoolExecutor, not multiprocessing

`HomeIsolation.setup` is dominated by filesystem syscalls
(`mkdtemp`, `mkdir`, `Path.resolve`); the GIL releases for every one
of those. Threads give realistic parallel scheduling at a fraction
of the process-spawn overhead and match the orchestrator's
expected execution model (T03.16 uses a thread pool, not a process
pool, because the eval body is dominated by I/O wait on the
`claude` subprocess).

### Why 30 iterations of 15 parallel, not 1 iteration of 450 parallel

Two reasons:

1. The orchestrator caps concurrency at 15. Spawning 450 parallel
   workers measures the wrong system — it would expose pool-scheduler
   thrash that NFR-PERF1 explicitly excludes.
2. Multiple short iterations let cold/warm cache effects average
   out across measurements. The iteration_summary block in the
   report exposes per-iteration medians so a future drift analysis
   can spot a single-iteration outlier without re-running the
   benchmark.

### Why dataclass construction is outside the measured window

`HomeIsolation` is a frozen dataclass whose `__post_init__` runs
`validate_eval_id` (a single regex match) and sets one private
slot via `object.__setattr__`. The orchestrator builds the
instance once per eval, outside the hot loop; timing it inside
the benchmark would inflate measurements with a cost the
production caller does not pay per iteration.

### Why teardown is excluded

NFR-PERF1 is a *setup* budget. The orchestrator schedules teardown
on a separate worker pool (cleanup phase) and a slow teardown does
not block the next eval from starting. Including teardown in the
sample would conflate two budgets the design treats as independent.

### Why `pytest.xfail` is reachable

The acceptance criteria explicitly permit the test to xfail "with
documented host limitation" if the budget cannot be met on the
running host. `pytest.xfail` (not `pytest.skip`) is the right
verb because:

* It records the failure in the test report so trend tooling
  notices.
* It does not red-light the broader suite — a slow CI matrix entry
  cannot block merge while the host hardening plan catches up.
* It writes the report to disk *before* the xfail call so trend
  tooling has the data to diagnose the host.

## Observed numbers (initial measurement)

| Metric | Value |
|--------|-------|
| p50 (s) | 0.0014567 |
| p95 (s) | 0.0034431 |
| min (s) | 0.0002415 |
| max (s) | 0.0061760 |
| mean (s) | 0.0016372 |
| stdev (s) | 0.0009789 |
| overall_elapsed (s) | 0.21751 |
| n_samples | 450 |
| Host | Linux-6.8.0-111-generic-x86_64-with-glibc2.39 / Python 3.12.12 |

`p50 = 1.5 ms` vs the NFR-PERF1 budget of `2.0 s` — three orders of
magnitude of headroom. The headroom is consistent with the scope
note in the spec: `HomeIsolation.setup` does not currently include
the hook adapter call (`deploy_hooks_to` is a separate orchestrator
step). When the orchestrator wires the adapter into the per-eval
flow, NFR-PERF3 (T03.21) will measure the combined cost; this
baseline anchors the *isolation primitive* cost in isolation so
regressions in either layer can be attributed cleanly.

## Open questions / future work

* **Hook adapter inclusion.** If a future refactor pulls
  `deploy_hooks_to` into `HomeIsolation.setup` itself, NFR-PERF1's
  scope shifts and this baseline must be re-measured. The
  schema_version field exists to flag that boundary if the
  schema also changes.
* **NFR-PERF3 linkage.** Suite-runtime tracking (T03.21) consumes
  `perf.json` as one input. The exact diff predicate (regression
  threshold, etc.) is owned by T03.21 and not pinned here.
* **CI matrix integration.** Per-host baselines belong under
  `TASKLIST_ROOT/evidence/T02.15/<host>/perf.json` — the
  `T02_15_PERF_REPORT` override env var supports that layout
  without a code change.

## Anti-patterns avoided

* **Measuring with `pytest-benchmark`.** The fixture-based
  benchmark plugin's calibration runs would re-execute the
  benchmark dozens of times; the harness wants a single
  reproducible run with a documented sample count.
* **`statistics.quantiles(..., method='exclusive')`.** The
  exclusive method drops the min/max from the boundary calculation
  which would give different numbers from the NFR-PERF3
  consumer. Pinned to `inclusive` to keep them aligned.
* **Re-using a single HomeIsolation across iterations.**
  `setup()` raises `RuntimeError` on second invocation (the
  "idempotency rule"), so the per-iteration construct is required.
