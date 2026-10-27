# D-0062 Full-Suite Runtime Baseline — Verification Evidence

Captured 2026-05-20 on branch `fix/prd-path-resolution-and-templates`.

## 1. Files delivered

| Path | Role | State |
|---|---|---|
| `tests/cli/eval/test_suite_runtime.py` | NFR-PERF3 baseline benchmark + schema pin + concurrency sanity | new |
| `docs/eval/runtime.md` | Operator-facing runtime budget doc with `--eval` subset re-run path | new |
| `.dev/releases/current/cliEval/artifacts/D-0062/spec.md` | Contract documentation | new |
| `.dev/releases/current/cliEval/artifacts/D-0062/notes.md` | Design notes | new |
| `.dev/releases/current/cliEval/artifacts/D-0062/evidence.md` | This file | new |
| `.dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json` | Captured baseline artifact | new |
| `.dev/releases/current/cliEval/evidence/T03.21/pytest-suite-runtime.txt` | Verbatim pytest output | new |

No production source files were modified — the deliverable is a test
plus documentation. The orchestrator (`RunOrchestrator`) and isolation
(`HomeIsolation`) surfaces are consumed read-only.

## 2. Benchmark run — `test_suite_runtime.py`

Command:

```bash
uv run pytest tests/cli/eval/test_suite_runtime.py -v
```

Result: **7 passed in 0.66s**

Per-class breakdown:

| Class | Tests | Result |
|---|---|---|
| `TestFullSuiteRuntimeBaseline` | 2 | PASS |
| `TestBaselineConstants` | 4 | PASS |
| `TestBaselineParallelism` | 1 | PASS |

## 3. Captured baseline artifact

Command (M3 evidence harvest form):

```bash
CLIEVAL_SUITE_RUNTIME_REPORT_PATH=\
.dev/releases/current/cliEval/evidence/T03.21/suite-runtime.json \
  uv run pytest \
    tests/cli/eval/test_suite_runtime.py::TestFullSuiteRuntimeBaseline::test_fifteen_eval_baseline_within_budget \
    -v
```

Result: **1 passed in 0.15s**

Artifact contents
(`evidence/T03.21/suite-runtime.json`, sort_keys=True):

```json
{
  "budget_sec": 600,
  "budget_text": "10 minutes",
  "deliverable": "D-0062",
  "duration_sec": 0.008907,
  "host_free_ram_bytes": 97542557696,
  "host_free_ram_gb": 90.84,
  "host_platform": "Linux-6.8.0-111-generic-x86_64-with-glibc2.39",
  "host_xfail_reason": null,
  "nfr": "NFR-PERF3",
  "parallel": 8,
  "roadmap_row": "R-062",
  "spec_count": 15,
  "subset_rerun_doc": "docs/eval/runtime.md",
  "task": "T03.21",
  "within_budget": true
}
```

Headline values:

| Field | Value | Interpretation |
|---|---|---|
| `duration_sec` | `0.008907` | Wall-clock for 15 evals at `--parallel 8` |
| `budget_sec` | `600` | NFR-PERF3 ceiling |
| `within_budget` | `true` | Headroom = 99.999% |
| `host_free_ram_gb` | `90.84` | Far above the 4 GB xfail floor |
| `host_xfail_reason` | `null` | Bench executed against the ceiling, not xfailed |

The measured baseline is ~67000x under the budget on this host, which
is the expected order of magnitude: the orchestrator's per-eval cost
at this layer (HomeIsolation setup + telemetry write + teardown)
runs in well under a millisecond per eval, and the 600 s budget
exists primarily to bound real-claude-subprocess wall-clock when the
Phase 4 dispatcher composes the orchestrator with the real PTY layer.

## 4. Acceptance criteria → evidence mapping

| AC from T03.21 | Test(s) / Artifact | Result |
|---|---|---|
| File `TASKLIST_ROOT/evidence/T03.21/suite-runtime.json` exists and records `duration_sec` for a 15-eval baseline at parallel 8 | `evidence/T03.21/suite-runtime.json` (`duration_sec=0.008907`, `parallel=8`, `spec_count=15`) | PASS |
| `docs/eval/runtime.md` documents the `--eval` subset re-run path | `docs/eval/runtime.md` §"Re-running a subset — the `--eval` flag" | PASS |
| Baseline duration `<600` seconds (or test marked xfail with host limitation) | `TestFullSuiteRuntimeBaseline::test_fifteen_eval_baseline_within_budget` (`within_budget=true`, host above 4 GB floor — no xfail required) | PASS |
| `TASKLIST_ROOT/artifacts/D-0062/spec.md` documents the baseline budget | `artifacts/D-0062/spec.md` (8 sections, schema table, AC mapping) | PASS |

## 5. Schema validation

| Path | Test | Result |
|---|---|---|
| `suite-runtime.json` carries the 15 documented keys | `TestFullSuiteRuntimeBaseline::test_suite_runtime_report_schema_is_stable` | PASS |
| `nfr` is `"NFR-PERF3"` | (same) | PASS |
| `budget_sec` matches `SUITE_RUNTIME_BUDGET_SEC` constant | (same) | PASS |
| `budget_text` matches `SUITE_RUNTIME_BUDGET_TEXT` constant | (same) | PASS |

## 6. Constant pins

| Constant | Test | Result |
|---|---|---|
| `SUITE_RUNTIME_BUDGET_SEC == 600` | `TestBaselineConstants::test_budget_is_ten_minutes` | PASS |
| `SUITE_RUNTIME_BUDGET_TEXT == "10 minutes"` | `TestBaselineConstants::test_budget_text_matches_seconds` | PASS |
| `BASELINE_SPEC_COUNT == 15` | `TestBaselineConstants::test_baseline_spec_count_matches_fr_g2` | PASS |
| `BASELINE_PARALLEL == RunOrchestrator.DEFAULT_PARALLEL == 8` | `TestBaselineConstants::test_baseline_parallel_matches_default` | PASS |

## 7. Concurrency sanity

| Path | Test | Result |
|---|---|---|
| At least 2 workers run simultaneously at `--parallel 8` | `TestBaselineParallelism::test_baseline_actually_runs_workers_concurrently` | PASS |
| Concurrency never exceeds `BASELINE_PARALLEL` | (same; upper-bound assertion) | PASS |

This defends against a future regression that drops effective
concurrency to 1 (e.g. a global lock wrapping
`RunOrchestrator.run`). Such a regression would still complete the
15-eval baseline under 600 s on a fast host while violating the
NFR-PERF3 design intent.

## 8. Regression guard — adjacent suites

Both adjacent benchmarks were re-run to confirm the new file does
not perturb them:

| Command | Result |
|---|---|
| `uv run pytest tests/cli/eval/test_perf_resource_bounds.py -v` | unchanged (T03.17 D-0059 baseline preserved) |
| `uv run pytest tests/cli/eval/test_parallel_15.py -v` | unchanged (T03.16 D-0058 baseline preserved) |
| `uv run pytest tests/cli/eval/test_orchestrator.py -v` | unchanged (T03.15 D-0057 baseline preserved) |

(See §9 for the captured pytest output of the suite-runtime run; the
regression runs are summarised here because no source files were
touched and their evidence already lives under T03.15/T03.16/T03.17.)

## 9. Sign-off

All T03.21 acceptance criteria verified by automated tests. The
NFR-PERF3 baseline is captured at the canonical evidence path, the
operator-facing doc is in place, and the schema pin guards against
silent drift. The deliverable is ready for the CP-P03-T17-T22
checkpoint.
