# Phase 5 Inventory (L6)

pytest wiring (suite-local conftest) + full suite run + lint/format parity.

## Deliverables

| File | Role |
|------|------|
| `tests/troubleshoot/backtest/conftest.py` | Suite-local conftest. Fixtures: `replay_scratch_root` (uuid-suffixed tmp dir, best-effort rmtree in finally, note that checkout_worktree still must remove+prune the common-dir admin record), `catch_rate_output_dir` (tmp_path-rooted subdir, explicitly NOT under docs/). `from __future__ import annotations` first. |
| `phase-outputs/test-results/pytest-backtest-output.txt` | Raw `uv run pytest tests/troubleshoot/backtest/ -v` output (exit 0). |
| `phase-outputs/test-results/pytest-backtest-summary.md` | Structured summary (counts + skip attribution + CI note). |
| `phase-outputs/test-results/ruff-backtest-output.txt` | Raw output of both `ruff check` + `ruff format --check`, with FINAL STATE summary. |
| `phase-outputs/plans/pytest-verdict.md` | L5 verdict: GREEN, no fixes needed. |

## conftest fixtures

- `replay_scratch_root` → unique `tempfile.gettempdir()/backtest-replay-<uuid>` dir; `shutil.rmtree(ignore_errors=True)` in `finally`.
- `catch_rate_output_dir` → `tmp_path / "catch-rate-out"`; never under `docs/`.

## Final pytest result

- passed = 32, skipped = 11, failed = 0, errored = 0 (exit 0).
- Skips: 5 NEW=CATCH proxies + 1 waiver + 5 aggregation parametrize (all designed; refs not landed).

## Final ruff state

- `uv run ruff check tests/troubleshoot/backtest/` → All checks passed!
- `uv run ruff format --check tests/troubleshoot/backtest/` → 20 files already formatted.
- Both pass (CI parity: CI runs `ruff format --check` separately from `make lint`).
