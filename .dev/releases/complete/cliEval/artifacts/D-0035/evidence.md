# D-0035 — Evidence (Task T02.15)

## Test execution

```text
$ uv run pytest tests/cli/eval/test_perf_home_setup.py -v
============================== test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.3, pluggy-1.6.0 -- /config/workspace/IronClaude/.venv/bin/python
cachedir: .pytest_cache
SuperClaude: 4.2.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False ...)
rootdir: /config/workspace/IronClaude
configfile: pyproject.toml
plugins: superclaude-4.2.0, benchmark-5.2.3, cov-7.1.0
collected 1 item

tests/cli/eval/test_perf_home_setup.py::test_home_setup_p50_p95_under_15_parallel PASSED [100%]

============================== 1 passed in 0.33s ===============================
```

Full log: `TASKLIST_ROOT/evidence/T02.15/pytest-T02.15.log`.

## perf.json baseline (recorded run)

Report location:
`TASKLIST_ROOT/evidence/T02.15/perf.json`.

Header (excluding `durations_sec` and `iteration_summary`):

```json
{
  "task_id": "T02.15",
  "deliverable_id": "D-0035",
  "nfr_id": "NFR-PERF1",
  "schema_version": 1,
  "n_parallel": 15,
  "n_iterations": 30,
  "n_samples": 450,
  "budget_sec": 2.0,
  "p50_sec": 0.0014567420003004372,
  "p95_sec": 0.003443112366949208,
  "min_sec": 0.00024150096578523517,
  "max_sec": 0.006176039983984083,
  "mean_sec": 0.0016372410937522848,
  "stdev_sec": 0.000978905632235026,
  "overall_elapsed_sec": 0.21750996599439532,
  "host": {
    "platform": "Linux-6.8.0-111-generic-x86_64-with-glibc2.39",
    "python": "3.12.12",
    "machine": "x86_64",
    "processor": "x86_64"
  }
}
```

Budget headroom: `p50 = 1.46 ms` against a 2.0 s budget — ~1370× under.
The headroom is consistent with the spec scope note: this baseline
covers the isolation primitive only (`mkdtemp` + `containment_guard` +
atomic-setup bookkeeping), not the hook adapter or `claude` subprocess
spawn.

## Acceptance criteria checklist

- [x] **Benchmark exists.** `tests/cli/eval/test_perf_home_setup.py`
      authored with the 15-parallel / 30-iteration loop.
- [x] **JSON report produced.** `perf.json` written under
      `TASKLIST_ROOT/evidence/T02.15/` with p50, p95, per-iteration
      summary, and the full sample array.
- [x] **p50 ≤ 2.0s on the dev host.** Measured `p50 = 0.00146 s` —
      passes the NFR-PERF1 hard budget by three orders of magnitude.
      xfail branch is implemented (per AC) but not taken on this host.
- [x] **Report path correct.** `TASKLIST_ROOT/evidence/T02.15/perf.json`
      created via `mkdir(parents=True, exist_ok=True)`; override env var
      `T02_15_PERF_REPORT` documented for per-host CI matrices.
- [x] **Spec documents budget + methodology.** See `D-0035/spec.md`
      ("Budget" + "Methodology" sections).

## Files added / modified

| Path                                                              | Action |
|-------------------------------------------------------------------|--------|
| `tests/cli/eval/test_perf_home_setup.py`                          | added  |
| `.dev/releases/current/cliEval/artifacts/D-0035/spec.md`          | added  |
| `.dev/releases/current/cliEval/artifacts/D-0035/notes.md`         | added  |
| `.dev/releases/current/cliEval/artifacts/D-0035/evidence.md`      | added  |
| `.dev/releases/current/cliEval/evidence/T02.15/perf.json`         | added  |
| `.dev/releases/current/cliEval/evidence/T02.15/pytest-T02.15.log` | added  |

## Cross-task interactions

* **T02.11 (COMP-006 `HomeIsolation`)** — depended on for the
  `setup`/`teardown` surface under test. The benchmark exercises the
  current state of that class (no hook deploy call from inside
  `setup`; see `D-0035/notes.md` "Anti-patterns avoided").
* **T02.14 (hook adapter)** — listed as a dependency; in practice
  this baseline does not invoke `deploy_hooks_to`. The orchestrator
  wires the adapter call separately (T03.16); NFR-PERF3 (T03.21) will
  measure the combined cost.
* **T02.18 (Checkpoint CP-P02-T13-T17)** — the checkpoint's Exit
  Criteria explicitly require `perf.json` to exist on disk; this
  baseline satisfies that prerequisite.

## Reproduction

```bash
# Default report location.
uv run pytest tests/cli/eval/test_perf_home_setup.py -v

# Per-host override.
T02_15_PERF_REPORT=/tmp/host-perf.json \
  uv run pytest tests/cli/eval/test_perf_home_setup.py -v
```
