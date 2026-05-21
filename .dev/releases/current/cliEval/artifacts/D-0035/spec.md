# D-0035 — NFR-PERF1 HOME setup performance baseline (Task T02.15)

**Task**: T02.15 (Phase 2 — cliEval harness)
**Tier**: STANDARD
**Risk**: Low
**Roadmap**: R-035 / NFR-PERF1 (HOME setup p50 budget at 15-eval parallel)
**Cross-links**: D-0032 (COMP-006 integrated `HomeIsolation`, T02.11),
D-0033 (NFR-ISO2 atomic-setup wrapper, T02.13),
D-0034 (COMP-014 hook adapter, T02.14),
upstream NFR-PERF3 suite-runtime tracking (T03.21 / future).

## Goal

Record a reproducible p50 / p95 baseline for the wall-clock cost of
`HomeIsolation.setup` when 15 per-eval HOMEs are materialized in
parallel — the concurrency cap the cliEval orchestrator (T03.16) hits.
The baseline lands in
`TASKLIST_ROOT/evidence/T02.15/perf.json` so the
NFR-PERF3 suite-runtime tracking task (T03.21) and any future host
adoption review can diff against an authoritative reference point
rather than re-deriving it from a fresh run.

## Budget

| Metric | Budget | Source |
|--------|--------|--------|
| p50 setup time (s) at 15-eval parallel | **≤ 2.0** | NFR-PERF1 hard budget |
| p50 informational target (s)           | ~1.4     | NFR-PERF1 design target |
| p95 setup time (s)                     | tracked, no hard budget | trend-only (NFR-PERF3) |

The hard budget is asserted at the end of the test. The informational
target is *not* enforced — it is documented so trend analyses can see
the gap between "still acceptable" and "design target met".

## Methodology

* `N_PARALLEL = 15` — concurrency level matching the orchestrator
  cap. Implemented via
  `concurrent.futures.ThreadPoolExecutor(max_workers=15)`.
* `N_ITERATIONS = 30` — number of 15-parallel batches. Yields
  `15 × 30 = 450` samples, well above the ≥30-sample floor the task
  notes call out for statistical signal.
* Each worker constructs a fresh `HomeIsolation` (frozen dataclass,
  cheap), then times a single `setup(config=...)` call with
  `time.perf_counter`. The dataclass construction is intentionally
  outside the measured window — it is amortized across the eval body
  the orchestrator runs once per eval.
* After the timer stops the worker tears the HOME down with
  `keep=False` so the scratch root does not balloon during the run.
  Teardown is **not** counted toward the budget; NFR-PERF1 is a setup
  budget.
* Iteration index is folded into the eval id (`Perf{n:05d}`) so
  workers across iterations never collide on the `mkdtemp` prefix and
  the validate_eval_id regex (`^[A-Z][A-Za-z0-9]*(...)?$`) stays
  satisfied.

### Sample math

* `p50` and `p95` are computed via
  `statistics.quantiles(samples, n=100, method="inclusive")[49]` and
  `[94]` respectively. The same call is used in the NFR-PERF3 trend
  pipeline so the two reports compare apples to apples.

### Scope and non-scope

In scope:

* Cost of `HomeIsolation.setup` end-to-end (`tempfile.mkdtemp` +
  scratch-root materialization + FR-ISO2 `containment_guard` +
  atomic-setup wrapper bookkeeping). This is the cost the
  orchestrator pays per eval at the isolation seam.

Out of scope for this baseline (tracked elsewhere):

* Hook deploy cost (`deploy_hooks_to`). The adapter is **not**
  invoked from inside `HomeIsolation.setup` in the current code; the
  orchestrator (T03.16) calls it as a separate step. NFR-PERF3
  (T03.21) covers the end-to-end suite cost including hook deploy.
* PtyDriver spawn cost (COMP-007 / T02.16). Separate baseline if a
  budget is ever attached.
* Teardown cost. Implicit in the eval cleanup phase budget if one
  is added.

## Report schema

```jsonc
{
  "task_id": "T02.15",
  "deliverable_id": "D-0035",
  "nfr_id": "NFR-PERF1",
  "schema_version": 1,
  "n_parallel": 15,
  "n_iterations": 30,
  "n_samples": 450,
  "budget_sec": 2.0,
  "p50_sec": <float>,
  "p95_sec": <float>,
  "min_sec": <float>,
  "max_sec": <float>,
  "mean_sec": <float>,
  "stdev_sec": <float>,
  "overall_elapsed_sec": <float>,
  "host": {
    "platform": "<platform.platform()>",
    "python": "<platform.python_version()>",
    "machine": "<platform.machine()>",
    "processor": "<platform.processor() or 'unknown'>"
  },
  "iteration_summary": [
    {"iteration": <int>, "min_sec": <float>,
     "median_sec": <float>, "max_sec": <float>}
  ],
  "durations_sec": [<float>, ...]   // length == n_samples
}
```

`schema_version` is pinned at `1` and bumped on any breaking change so
NFR-PERF3 consumers (T03.21) can refuse to read an incompatible payload.

## Report destination

Default path:

```
TASKLIST_ROOT/evidence/T02.15/perf.json
```

The destination can be overridden with the `T02_15_PERF_REPORT`
environment variable. CI matrices that publish per-host baselines set
that variable so each host writes to its own well-known location.

## Budget-failure handling

When `p50 > BUDGET_SEC` the test invokes `pytest.xfail` with the
recorded p50 in the reason string. xfail (`strict=False`) is the
documented "host limitation" branch the acceptance criteria permit so
a slow host does not red-light the suite — but the report still lands
on disk so trend tooling can flag the regression. The xfail path is
*not* a permanent escape hatch: CI environments that keep hitting it
must update the host hardening plan rather than relax `BUDGET_SEC`.

## Acceptance criteria mapping

| AC (T02.15) | Where satisfied |
|------------|-----------------|
| File `tests/cli/eval/test_perf_home_setup.py` exists and produces a JSON report with p50, p95, and per-iteration durations. | `tests/cli/eval/test_perf_home_setup.py`; report schema above. |
| p50 setup time ≤ 2.0s at 15-eval parallel (or xfail with documented host limitation). | Final assertion in the test; xfail branch documented above. |
| Report `perf.json` is written to `TASKLIST_ROOT/evidence/T02.15/`. | `_default_report_path()` + override env var. |
| `TASKLIST_ROOT/artifacts/D-0035/spec.md` documents the budget and methodology. | This file. |

## References

* `tests/cli/eval/test_perf_home_setup.py` — the benchmark.
* `src/superclaude/cli/eval/isolation.py` — the primitive under test.
* `.dev/releases/current/cliEval/phase-2-tasklist.md` — task T02.15.
* `.dev/releases/current/cliEval/artifacts/D-0032/spec.md` — COMP-006
  integrated contract.
