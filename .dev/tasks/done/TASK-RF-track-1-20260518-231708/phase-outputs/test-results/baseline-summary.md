---
phase: baseline (pre-migration)
captured: 2026-05-19
workspace: /config/workspace/IronClaude-T1-sprint
branch: feat/sprint-state-migration
---

# Baseline test + lint state

Captured before any Phase 2 source modification. Defines the "no regression" bar for Phase 2, Phase 3, and Phase 4 validation sweeps.

## Ruff (`uv run ruff check src/superclaude/cli/sprint/ tests/sprint/`)

- **Result:** FAIL — 11 errors
- **Scope of errors:** All 11 errors are pre-existing in `tests/sprint/diagnostic/*` (E731 lambda assignment + E402 module-level imports not at top + a few quoted-string-annotation issues at `tests/sprint/conftest.py:909-914`). NONE are in files this task modifies (`models.py`, `config.py`, `commands.py`, `executor.py`, `tmux.py`, `tests/sprint/test_tmux.py`).
- **Disposition:** Pre-existing. Out of scope for FU-001. Post-migration ruff must show the same count (11) or fewer; any NEW error introduced by Phase 2 edits is a regression.
- **Environment note:** Ruff was NOT installed in the `uv` `.venv` at task start. Installed via `uv pip install ruff` (==0.15.13) as a one-time bootstrap. This is a workspace-setup issue, not a baseline finding.

## Pytest (`uv run pytest tests/sprint/ tests/pipeline/ -v --tb=short`)

- **Result:** 57 failed, 1350 passed, 1 skipped, 22 warnings
- **Failure scope:** All 57 failures share the same root cause: `AttributeError: 'X object' has no attribute 'stdin'` from FakePopen/-style test doubles that mock `subprocess.Popen` but don't expose `.stdin`. Affected files:
  - `tests/sprint/test_execute_sprint_integration.py` (3)
  - `tests/sprint/test_executor.py` (5)
  - `tests/sprint/test_integration_halt.py` (5)
  - `tests/sprint/test_integration_lifecycle.py` (4)
  - `tests/sprint/test_integration_signal.py` (4)
  - `tests/sprint/test_multi_phase.py` (2)
  - `tests/sprint/test_phase8_halt_fix.py` (7)
  - `tests/sprint/test_regression_gaps.py` (1)
  - `tests/sprint/test_tui_monitor.py` (5)
  - `tests/sprint/test_watchdog.py` (3)
  - (others within tests/sprint/ — total 57)
- **`tests/pipeline/` failures:** 0 — pipeline suite is clean.
- **Disposition:** Pre-existing failures unrelated to FU-001. The task does NOT modify subprocess.Popen mocking. Post-migration pytest must show ≤ 57 failures with the SAME failing test set (i.e., zero NEW failures); any new failure in a previously-passing test is a regression.

## Test_tmux baseline (the file Step 2.6 modifies)

- **All 11 tests in `tests/sprint/test_tmux.py` PASSED on baseline.**
- The BUILD_REQUEST narrative described `tests/sprint/test_tmux.py:100` as "pre-existing flaky" — current observation shows the test (`TestThreePaneLayout::test_launch_creates_three_panes`) is **currently passing**. Step 2.6's "PASS-on-old → PASS-on-new" transition criterion is therefore "PASS → PASS"; the new `state_dir` write path must not regress this case.
- Line 100 in test_tmux.py reads: `sentinel = config.release_dir / ".sprint-exitcode"` followed by `sentinel.write_text("0\n")`. Phase 2.6 will migrate this to `config.state_dir` and add a `mkdir(parents=True, exist_ok=True)`.

## Tracked sentinel inventory (Step 1.5)

- **Count:** 40 tracked `.sprint-exitcode` files — matches research expectation exactly.
- **List:** see `phase-outputs/discovery/tracked-sentinels.txt`.

## No-regression bar for Phase 2 / 3 / 4

| Gate | Pass condition |
|---|---|
| Ruff over sprint module | ≤ 11 errors total; **zero new** errors in models/config/commands/executor/tmux/test_tmux |
| Pytest tests/sprint/ tests/pipeline/ | ≤ 57 failed; same set of failing tests; **zero new** failures |
| test_tmux.py | all 11 tests PASS (including the migrated `test_launch_creates_three_panes`) |
| `make verify-sync` | reports trees in sync |
| `git ls-files \| grep -c '\.sprint-exitcode$'` | returns 0 (Step 3.3 acceptance) |
