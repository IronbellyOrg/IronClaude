# D-0062 — NFR-PERF3 Full-Suite Runtime Baseline

**Roadmap entry**: R-062
**Task**: T03.21
**Component(s) under test**: COMP-003 `RunOrchestrator` × COMP-006 `HomeIsolation`
**Source**: `tests/cli/eval/test_suite_runtime.py`
**Non-functional requirement**: NFR-PERF3 — "Full-suite duration MUST
stay <= 600 seconds (10 minutes) when the 15-eval baseline is
scheduled at `--parallel 8` on the dev host (Linux, 4 GB+ free RAM)."

## 1. Goal

Pin the harness's wall-clock budget at the design-default composition
(15 evals, `--parallel 8`) so a future regression that doubles per-
worker latency surfaces before it manifests as a CI timeout. The
sibling NFR-PERF2 benchmark (T03.17 / D-0059) pins the resident-memory
ceiling at the same composition; together they bound the harness's two
operator-facing resource axes — RAM and time.

The deliverable has two surfaces:

1. An executable baseline benchmark that emits a structured artifact
   (`suite-runtime.json`) on every run.
2. An operator-facing doc (`docs/eval/runtime.md`) describing the
   budget and the `--eval` subset re-run path.

## 2. Public Surface

```python
from tests.cli.eval.test_suite_runtime import (
    SUITE_RUNTIME_BUDGET_SEC,        # 600
    SUITE_RUNTIME_BUDGET_TEXT,       # "10 minutes"
    BASELINE_SPEC_COUNT,             # 15
    BASELINE_PARALLEL,               # 8
)
```

These constants are also imported by:

* `docs/eval/runtime.md` (in prose form, kept in sync via the
  `TestBaselineConstants` test class).

## 3. Baseline Scenario

The benchmark composes :class:`RunOrchestrator` (T03.15 / D-0057) over
the same real-:class:`HomeIsolation` worker shape used by
`test_parallel_15.py` (T03.16 / D-0058). The choice is deliberate:

* The NFR-PERF3 budget is per-orchestration-process, not per Claude
  subprocess. A real `claude` subprocess would add seconds of upstream
  startup that belong to the Claude binary, not the harness; pinning
  the harness budget without that contamination is the goal.
* Real `HomeIsolation` is included (rather than a pure stub) because
  isolation setup/teardown is the dominant per-eval cost in the harness
  layer the budget is meant to bound. Skipping it would under-count
  the budget.

| Parameter | Value | Source |
|---|---|---|
| `N_EVALS` | 15 | `BASELINE_SPEC_COUNT`; mirrors FR-G2 (T03.16). |
| `PARALLEL` | 8 | `BASELINE_PARALLEL == RunOrchestrator.DEFAULT_PARALLEL`. |
| `BUDGET_SEC` | 600 | `SUITE_RUNTIME_BUDGET_SEC`; design-spec §11. |
| Spec id pattern | `E000..E014` | FR-SCH2 regex-safe, lexicographic = numeric. |
| Wall-clock source | `time.monotonic()` | Unaffected by NTP slew. |

## 4. Evidence Artifact — `suite-runtime.json`

Written to the path resolved by
:func:`test_suite_runtime._report_destination`:

1. `os.environ["CLIEVAL_SUITE_RUNTIME_REPORT_PATH"]` when set (release
   evidence harvest).
2. `tmp_path / "suite-runtime.json"` otherwise (isolated pytest runs).

### Evidence sink — `CLIEVAL_SUITE_RUNTIME_REPORT_PATH`

```
CLIEVAL_SUITE_RUNTIME_REPORT_PATH=<TASKLIST_ROOT>/evidence/T03.21/suite-runtime.json
```

### Schema — `suite-runtime.json`

| Key                    | Type            | Meaning                                                |
|------------------------|-----------------|--------------------------------------------------------|
| `task`                 | string          | `"T03.21"`                                             |
| `deliverable`          | string          | `"D-0062"`                                             |
| `roadmap_row`          | string          | `"R-062"`                                              |
| `nfr`                  | string          | `"NFR-PERF3"`                                          |
| `budget_sec`           | int             | `SUITE_RUNTIME_BUDGET_SEC` (600)                       |
| `budget_text`          | string          | `"10 minutes"`                                         |
| `parallel`             | int             | concurrency the bench used (8 at the baseline)         |
| `spec_count`           | int             | number of eval specs (15 at the baseline)              |
| `duration_sec`         | float           | wall-clock delta around `RunOrchestrator.run`          |
| `host_free_ram_bytes`  | int or null     | `/proc/meminfo` `MemAvailable` (or `MemFree`) snapshot |
| `host_free_ram_gb`     | float or null   | rounded view                                           |
| `host_platform`        | string          | `platform.platform()`                                  |
| `host_xfail_reason`    | string or null  | populated when the bench xfailed                       |
| `within_budget`        | bool            | `duration_sec <= budget_sec`                           |
| `subset_rerun_doc`     | string          | `"docs/eval/runtime.md"` (FR-CLI3 `--eval` reference)  |

`test_suite_runtime_report_schema_is_stable` pins the key set so a
future patch that drops a field fails CI instead of silently breaking
downstream tooling.

## 5. Operator-facing Documentation — `docs/eval/runtime.md`

The doc documents:

* The 600 s budget, the baseline scenario, and the wall-clock source.
* The `--eval <id>` subset re-run path so an operator does not pay the
  full-suite cost when only one or two evals need a second look. The
  subset path is the same one `docs/eval/retry.md` describes for the
  bounded-retry policy (NFR-REL2 / T03.08).
* The xfail carve-out for hosts with less than 4 GB free RAM.
* The constants pin (`SUITE_RUNTIME_BUDGET_SEC`,
  `BASELINE_SPEC_COUNT`, `BASELINE_PARALLEL`) and the regression-bisect
  recipe (capture `duration_sec` from `suite-runtime.json`, compare to
  the prior baseline).

## 6. Out of Scope

* **CLI flag wiring.** The Phase 4 dispatcher already binds `--eval`
  (FR-CLI3). This deliverable does not modify the dispatch surface; it
  documents the existing flag's role in the runtime budget story.
* **Reporter budget gating.** `Reporter` (COMP-008 / T03.13) writes
  `duration_sec` into `RunSummary` but does **not** raise on a
  budget overrun — NFR-PERF3 is reported, not gated. A slow run still
  emits a valid summary the operator can inspect.
* **Per-eval timeout enforcement.** That contract is owned by
  T03.07 (signal handling + per-eval timeout). NFR-PERF3 is the
  suite-level wall-clock budget; per-eval timeouts are a separate
  axis.
* **Real `claude` subprocess timing.** The PTY lifecycle tests
  (T03.22) exercise the real subprocess; this benchmark pins the
  harness-only ceiling.

## 7. Acceptance Criteria → Test Mapping

| AC (verbatim from T03.21) | Test | Evidence |
|---|---|---|
| File `TASKLIST_ROOT/evidence/T03.21/suite-runtime.json` exists and records `duration_sec` for a 15-eval baseline at parallel 8 | `TestFullSuiteRuntimeBaseline::test_fifteen_eval_baseline_within_budget` | `evidence/T03.21/suite-runtime.json` |
| `docs/eval/runtime.md` documents the `--eval` subset re-run path | (doc) | `docs/eval/runtime.md` §"Re-running a subset" |
| Baseline duration `<600` seconds (or test marked xfail with host limitation) | `TestFullSuiteRuntimeBaseline::test_fifteen_eval_baseline_within_budget` (with xfail carve-out for `<4 GB` hosts) | `evidence/T03.21/suite-runtime.json` (`within_budget: true`) |
| `TASKLIST_ROOT/artifacts/D-0062/spec.md` documents the baseline budget | (this file) | — |

## 8. References

* Roadmap row: R-062.
* Design-spec sources: `.dev/releases/current/cliEval/design-spec.md`
  §11 (NFR-PERF3 budget).
* Upstream contracts: D-0057 (RunOrchestrator scheduling skeleton),
  D-0058 (FR-G2 15-eval integration shape), D-0029 (HomeIsolation
  contract).
* Sibling deliverable: D-0059 (T03.17 / NFR-PERF2 resident-memory
  ceiling at the same composition).
* Related documentation: `docs/eval/retry.md` (shared `--eval` subset
  flag with the bounded-retry policy).
