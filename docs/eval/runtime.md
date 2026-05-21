# Eval Suite Runtime Budget (NFR-PERF3)

**Status:** Stable as of T03.21 (Phase 3, D-0062).

## TL;DR

The full 15-eval baseline at `--parallel 8` is bounded to **600 seconds
(10 minutes)** of wall-clock time on a dev host. When a single failing
eval forces a re-run, use the `--eval <id>` subset path so only the
failing rows pay the runtime cost — not the whole 15-eval suite.

```text
NFR-PERF3 budget       : 600 s (10 minutes)
Baseline scenario       : 15 evals × --parallel 8
Baseline evidence       : .dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json
Pin constants           : superclaude.cli.eval.test_suite_runtime.SUITE_RUNTIME_BUDGET_SEC
                          superclaude.cli.eval.test_suite_runtime.SUITE_RUNTIME_BUDGET_TEXT
```

## Why a 10-minute budget?

The harness ships a **bounded full-suite runtime** so the operator
feedback loop stays fast enough that diagnosis happens in the same
sitting as the run. The [design-spec §11][design-spec-11] enumerates the
constraint:

[design-spec-11]: ../../.dev/releases/current/cliEval/design-spec.md

> *Full-suite duration MUST stay <= 600 seconds (10 minutes) when the
> 15-eval baseline is scheduled at `--parallel 8` on the dev host
> (Linux, 4 GB+ free RAM).*

Concretely:

* The orchestrator (`RunOrchestrator`, T03.15) schedules workers via
  `concurrent.futures.ThreadPoolExecutor + as_completed` with a default
  concurrency of 8 (`RunOrchestrator.DEFAULT_PARALLEL`). The 600 s
  budget is sized so 15 evals at this concurrency comfortably fit
  inside one operator-visible feedback cycle.
* `Reporter` (COMP-008, T03.13) stamps the measured wall-clock into
  `RunSummary.duration_sec`. The reporter does not enforce the budget —
  it is reported, not gated — so a slow run still produces a valid
  artifact the operator can inspect.
* The wall-clock measurement is taken via `time.monotonic()` around
  `RunOrchestrator.run()` so NTP slew, system clock changes, and DST
  transitions cannot move the budget under the harness's feet.

## Re-running a subset — the `--eval` flag

After a run completes, the Reporter writes `summary.{md,json}` to the
run directory. Inspect the table, identify the failing eval ids, then
re-run only those evals — there is no reason to pay the full 15-eval
runtime when only one or two need a second look:

```bash
# Full baseline run (15 evals at the design default)
superclaude eval run suites/full.yaml --parallel 8

# Re-run only the failing ids after diagnosis (any number of --eval)
superclaude eval run suites/full.yaml --eval E03 --eval E07

# Quick smoke (3-4 evals); same flag, different subset
superclaude eval run suites/quick.yaml --eval E01 --eval E02
```

Notes mirror [`docs/eval/retry.md`](retry.md) — the `--eval` subset
flag is the same one the bounded-retry policy directs operators to for
single-eval re-runs:

* `--eval` accepts the **expanded** id (post-parameterize) so a
  parameterized eval like `E07[case=a]` is targetable by its full
  identifier. An id that does not match any expanded eval exits with
  code 2 (FR-CLI3, `tests/cli/eval/test_eval_id_regex.py`).
* Subset runs are independent processes — they allocate fresh
  `HomeIsolation` per eval and emit a fresh `summary.{md,json}` under
  their own run directory. There is no shared state with the
  originating run, and the subset run's own wall-clock is bounded
  proportionally (e.g. a 1-eval subset is expected to complete in
  well under a minute on the dev host).
* The subset run reuses the same `--parallel 8` default; if you are
  re-running a single eval there is no point lowering it, but if you
  need to pin behaviour against a specific concurrency for diagnosis,
  pass `--parallel 1` explicitly so the orchestrator's clamp does not
  bias the result.

## Baseline evidence

The `T03.21` benchmark (`tests/cli/eval/test_suite_runtime.py`)
captures the baseline wall-clock at the design-default composition
(15 evals, `--parallel 8`) and writes `suite-runtime.json` to the
evidence directory:

```bash
CLIEVAL_SUITE_RUNTIME_REPORT_PATH=\
.dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json \
  uv run pytest tests/cli/eval/test_suite_runtime.py::TestFullSuiteRuntimeBaseline::test_fifteen_eval_baseline_within_budget -v
```

The artifact records the measured `duration_sec`, the `budget_sec`
ceiling, the host's free-RAM snapshot, and a `within_budget` boolean.
A regression bisect should compare its `duration_sec` against the
captured baseline to identify the offending change.

## Operator-facing invariants

* `SUITE_RUNTIME_BUDGET_SEC = 600` is the canonical pin. Reading it
  from a script (e.g. CI safety check) lets a deployment confirm the
  harness build still targets the 10-minute ceiling.
* `BASELINE_SPEC_COUNT = 15` and `BASELINE_PARALLEL = 8` are the
  canonical pins for the baseline scenario. Any change to either
  requires a corresponding design-spec §11 update.
* Hosts with `<4 GB` free RAM fall under the same xfail carve-out the
  NFR-PERF2 bench uses (see
  [`tests/cli/eval/test_perf_resource_bounds.py`](../../tests/cli/eval/test_perf_resource_bounds.py)).
  The runtime ceiling is not meaningful when paging dominates the
  wall-clock.

## See also

* `src/superclaude/cli/eval/orchestrator.py` — `RunOrchestrator`,
  `DEFAULT_PARALLEL`, `MAX_PARALLEL`.
* `tests/cli/eval/test_suite_runtime.py` — baseline benchmark,
  `SUITE_RUNTIME_BUDGET_SEC`, `BASELINE_SPEC_COUNT`, `BASELINE_PARALLEL`.
* `docs/eval/retry.md` — bounded retry policy (NFR-REL2). The `--eval`
  subset flag is shared between the runtime budget and the retry
  policy.
* `.dev/releases/current/cliEval/design-spec.md §11` — NFR-PERF3
  budget contract.
* `.dev/releases/current/cliEval/artifacts/D-0062/spec.md` — Per-task
  deliverable record for T03.21.
* `.dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json` —
  Captured baseline artifact.
