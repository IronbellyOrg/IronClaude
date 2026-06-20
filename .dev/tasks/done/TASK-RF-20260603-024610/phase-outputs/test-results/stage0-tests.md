# Stage 0 — Test & Lint Summary (Step 2.11)

**Captured:** 2026-06-03 19:32
**Raw output:** `stage0-tests.txt`
**Command:** `uv run pytest tests/sprint/test_per_task_env_isolation.py tests/sprint/e2e_real/test_e2e_isolation_smoke.py tests/sprint/e2e_real/test_e2e_turn_count.py tests/sprint/test_executor.py tests/cli/eval/test_isolation_layers_probe.py tests/integration/test_sprint_wiring.py -q`

## Pytest counts (exact)

| Metric | Count |
|--------|-------|
| Passed | 112 |
| Failed | 5 |
| Skipped | 0 |
| Total | 117 |
| Exit code | 1 |

Summary line: `5 failed, 112 passed in 0.67s`

## Lint

`make lint` → **PASS** (`ruff check .` → "All checks passed!", exit 0).

## Regression analysis vs `pre-change-baseline.md`

**ZERO regressions.** All 5 failures are pre-existing baseline failures (same
`.stdin` harness-double root cause), present BEFORE any Stage-0 change:

| Failing test | On baseline list? | Error signature |
|---|---|---|
| test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_pass | yes | `AttributeError: '_PassPopen' ... 'stdin'` |
| test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_halt | yes | `AttributeError: '_HaltPopen' ... 'stdin'` |
| test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_timeout_exit_code_124 | yes | `AttributeError: '_TimeoutPopen' ... 'stdin'` |
| test_executor.py::TestExecuteSprintIntegrationCoverage::test_execute_sprint_interrupted | yes | `AttributeError: '_InterruptPopen' ... 'stdin'` |
| test_executor.py::TestBackwardCompat::test_backward_compat_sprint_pass_grace_period_zero | yes | `AttributeError: '_PassPopen' ... 'stdin'` |

All 5 appear verbatim in the Phase-1 baseline already-failing list, all with the
same `.stdin` AttributeError on the Path A single-session fallback. None are in
the Path B per-task code Stage 0 wired.

## New Stage-0 tests (all PASS)

- `tests/sprint/test_per_task_env_isolation.py` — 3 passed (env-uniqueness +
  positive concurrent-spawn repro + negative-control contention detected).
- `tests/sprint/e2e_real/test_e2e_isolation_smoke.py` — 1 passed (real spawn,
  per-task isolated CLAUDE_SETTINGS_DIR/PLUGIN_DIR under `.isolation`).
- `tests/sprint/e2e_real/test_e2e_turn_count.py` — 1 passed (turns_consumed == 7
  exactly, would fail against the pre-change hard-coded 0).
- `tests/cli/eval/test_isolation_layers_probe.py` — all passed (signature pin
  re-pinned to `("config", "scope")`; IsolationLayers 4-field order unchanged).
- `tests/integration/test_sprint_wiring.py` — passed (no regression).

## Verdict

Stage-0 wiring is green: all new acceptance tests pass, the isolation probe and
wiring integration stay green, lint is clean, and the only failures are the 5
pre-existing `.stdin` harness failures carried over from the baseline (NOT
regressions).
