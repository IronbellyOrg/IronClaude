# Stage 1 — Test & Lint Summary (Step 3.18)

**Captured:** 2026-06-03 20:12
**Raw output:** `stage1-tests.txt`
**Command:** `uv run pytest tests/sprint/test_handoff_record.py tests/sprint/test_handoff_store.py tests/sprint/test_stage1_wiring.py tests/sprint/test_handoff_backward_compat.py tests/sprint/test_context_injection.py tests/sprint/test_backward_compat_regression.py tests/sprint/test_executor.py tests/integration/test_sprint_wiring.py -q`

## Pytest counts (exact)

| Metric | Count |
|--------|-------|
| Passed | 144 |
| Failed | 5 |
| Skipped | 0 |
| Total | 149 |
| Exit code | 1 |

Summary line: `5 failed, 144 passed in 5.90s`

## Lint

`make lint` initially reported **1** error (`I001` import-block-unsorted in
`executor.py`, introduced by the new `from .handoff import FileHandoffStore`).
Fixed with `ruff check --fix src/superclaude/cli/sprint/executor.py` (import
reordered to alphabetical position). Re-run: **PASS** ("All checks passed!", exit 0).
`executor.py` re-verified to import cleanly after the reorder.

## Regression analysis vs `pre-change-baseline.md`

**ZERO regressions.** All 5 failures are pre-existing baseline `.stdin`
harness-double failures (same root cause documented in Phase 1), all in
`test_executor.py::TestExecuteSprintIntegrationCoverage` / `TestBackwardCompat`:

| Failing test | On baseline list? | Signature |
|---|---|---|
| test_execute_sprint_pass | yes | `_PassPopen ... 'stdin'` |
| test_execute_sprint_halt | yes | `_HaltPopen ... 'stdin'` |
| test_execute_sprint_timeout_exit_code_124 | yes | `_TimeoutPopen ... 'stdin'` |
| test_execute_sprint_interrupted | yes | `_InterruptPopen ... 'stdin'` |
| test_backward_compat_sprint_pass_grace_period_zero | yes | `_PassPopen ... 'stdin'` |

## New Stage-1 tests (all PASS)

- `test_handoff_record.py` — 4 passed (round-trip every H4 field, from_task_result derivation, forward-compat unknown key, schema_version=1).
- `test_handoff_store.py` — 4 passed (write/read round-trip, read-missing→None, exact phase-qualified key, no leftover `.tmp`).
- `test_stage1_wiring.py` — 4 passed (build_task_context reaches prompt + threaded via execute_phase_tasks; `task_complete` event distinct from `task_rerun_complete`; 12-entry M6 heading corpus routes/warns/reclassifies-nothing correctly).
- `test_handoff_backward_compat.py` — 2 passed (handoff=off legacy-exact: no records, no `task_complete`, +0 threads; positive control with handoff=on writes 2 records + 2 events).

## Existing tests held green

- `test_context_injection.py`, `test_backward_compat_regression.py`, `test_sprint_wiring.py` — all green (no regression from the Stage-1 wiring).

## Verdict

Stage-1 wiring is green: all new acceptance tests pass, existing
context/backward-compat/wiring tests stay green, lint clean (after a one-line
import-sort auto-fix), and the only failures are the 5 pre-existing `.stdin`
harness failures — NOT regressions.
