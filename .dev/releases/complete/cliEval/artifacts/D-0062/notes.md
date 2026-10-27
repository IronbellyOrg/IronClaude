# D-0062 — NFR-PERF3 Full-Suite Runtime Baseline — Design Notes

## 1. Why a benchmark, not a constant?

The simplest implementation would be a one-line constant
`SUITE_RUNTIME_BUDGET_SEC = 600` in `runner.py` plus a doc entry, with
the runtime "verified" by manual observation. We rejected that for two
reasons:

* A constant without empirical anchoring drifts silently. The first
  refactor that doubles per-eval setup cost (e.g. a leaky telemetry
  buffer or a synchronously-flushed log file) lands without a CI
  signal because nothing measures the actual baseline.
* The sibling NFR-PERF2 benchmark (T03.17 / D-0059) already
  established the pattern for "harness ceiling + empirical artifact +
  schema-pin". Replicating the shape for NFR-PERF3 keeps the two
  ceilings legible together and lets a single evidence-harvest step
  collect both `perf-ram.json` and `suite-runtime.json` from adjacent
  paths.

The benchmark therefore lives at `tests/cli/eval/test_suite_runtime.py`
and runs under the standard pytest invocation. The `M3` release
harvest sets `CLIEVAL_SUITE_RUNTIME_REPORT_PATH` to redirect the
artifact into `evidence/T03.21/`; in isolated runs the artifact lands
in `tmp_path` so the test still produces a verifiable file.

## 2. Why real `HomeIsolation`, not a stub?

The NFR-PERF2 bench (T03.17) uses a *stub* worker because the RAM
measurement is dominated by the orchestrator's per-thread overhead;
mixing in real `mkdtemp` calls would add noise that does not belong to
the ceiling under test. The NFR-PERF3 bench takes the opposite
position:

* `HomeIsolation.setup` performs `mkdtemp` + ancestor-allowlist
  containment checks + permissive-config hook deployment. On a slow
  filesystem this is the dominant per-eval cost in the harness layer
  the budget is meant to bound.
* `HomeIsolation.teardown` removes the deployed hooks. The teardown
  cost also belongs to the harness budget.
* The Reporter would persist exactly this composition's `duration_sec`
  in `RunSummary.duration_sec` if invoked through the dispatcher; the
  bench is a faithful proxy for the production wall-clock the operator
  sees.

The worker therefore mirrors the `test_parallel_15.py` isolation
worker shape rather than the `test_perf_resource_bounds.py` stub
worker shape. The differential aligns each benchmark with the layer
its ceiling targets.

## 3. Why `time.monotonic()` instead of `datetime.utcnow()`?

`time.monotonic` is the canonical wall-clock for durations:

| Property | `time.monotonic` | `datetime.utcnow` |
|---|---|---|
| Affected by NTP slew | No | Yes |
| Can go backwards | No | Yes (during sync) |
| Resolution | Sub-millisecond | Microsecond (but coarsened by OS) |
| Tied to wall-clock display | No | Yes |

The Reporter persists `duration_sec` as a float, not a pair of
ISO-8601 timestamps, so the benchmark using `time.monotonic` matches
production's persistence model exactly. A future refactor of `Reporter`
that switches to `time.perf_counter` (which has the same monotonic
guarantee but higher resolution) would still pass this benchmark
unchanged.

## 4. The xfail carve-out

The AC explicitly carves out hosts that cannot meet the 4 GB free-RAM
floor. The benchmark adopts the same `/proc/meminfo`-based probe the
NFR-PERF2 bench uses (`_free_ram_bytes`) so the two benchmarks
xfail-on-the-same-hosts. Hosts that lack `/proc/meminfo` entirely
(non-Linux dev environments) also xfail.

The xfail does *not* skip the artifact: `suite-runtime.json` is still
written to its resolved destination so the M3 harvest can capture the
host limitation along with the measured duration. The schema field
`host_xfail_reason` carries the reason; the test-runner output records
the xfail.

## 5. Concurrency sanity test

The `TestBaselineParallelism` class defends against a future
regression that drops effective concurrency to 1 (e.g. a global lock
wrapping `RunOrchestrator.run`). Such a regression would still
complete the 15-eval baseline under 600 s on a fast host while
violating the NFR-PERF3 design intent ("8 workers at peak"). The test
instruments the worker with a peak-concurrency counter and asserts at
least 2 peers run simultaneously at `--parallel 8`. The upper-bound
clamp at `BASELINE_PARALLEL` is also asserted to defend against a
regression in the opposite direction.

## 6. The `--eval` subset path

The runtime budget story implies a workflow: when the budget is tight
and only one or two evals failed, re-running the full 15-eval suite is
wasteful. The harness already ships `--eval <id>` for FR-CLI3; the doc
(`docs/eval/runtime.md`) connects the dots and points operators at it.

The same flag is referenced from `docs/eval/retry.md` (NFR-REL2 /
T03.08) — both docs describe the *same* CLI surface, just for
different reasons (retry-after-failure vs subset-after-timeout).
Keeping both docs consistent is enforced by editorial review; there
is no test that auto-syncs them today because the textual overlap is
small.

## 7. Constants pin

`SUITE_RUNTIME_BUDGET_SEC` lives on the test module rather than on
`runner.py` because:

* The constant is *not* a runtime guard — `Reporter` does not enforce
  the budget. There is no code path in `runner.py` that reads it.
* The constant is the *bench's* expectation of what the harness can
  deliver. A change to it requires the corresponding design-spec §11
  update; co-locating it with the bench keeps the change record
  auditable in one place.

Future work that promotes the constant into a CLI-surfaced warning
(e.g. `superclaude doctor` flags "current baseline exceeds 80% of
budget") would migrate the constant into `commands.py` or
`doctor.py`. Until then, the test-module home is intentional.

## 8. Evidence-harvest invocation

The canonical command for the M3 evidence harvest is:

```bash
CLIEVAL_SUITE_RUNTIME_REPORT_PATH=\
.dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json \
  uv run pytest \
    tests/cli/eval/test_suite_runtime.py::TestFullSuiteRuntimeBaseline::test_fifteen_eval_baseline_within_budget \
    -v
```

This mirrors the T03.17 harvest command in shape, differing only in
the env-var name and the test selector. A future CI step that runs
both benchmarks back-to-back can chain them in a single shell with
parallel env exports.
