# Change Inventory — TASK-RF-20260604020650 (PR #120 Medium findings M1/M2/M3/M4)

**Generated:** 2026-06-04 (Phase 6, Step 6.4)

## Finding → source/test mapping

| Finding | Description | Source file(s) modified | Test file(s) added/extended |
|---------|-------------|--------------------------|------------------------------|
| **M1** | Subprocess handle leak on exception during per-task wait | `src/superclaude/cli/sprint/executor.py` (`_run_task_subprocess`: `try/except BaseException: proc.terminate(); raise`) | `tests/sprint/test_executor.py` (added `test_run_task_subprocess_closes_handles_when_poll_raises`) |
| **M2** | Warn-mode stall watchdog poll loop spins unbounded | `src/superclaude/cli/sprint/executor.py` (`_poll_with_stall_watchdog`: wall-clock ceiling on the `while` guard via `getattr(proc, "timeout_seconds", 3600)`) | `tests/sprint/test_poll_watchdog_ceiling.py` (NEW — warn-mode ceiling + kill-mode + disabled-path) |
| **M3** | Corrupt handoff file crashes resume | `src/superclaude/cli/sprint/handoff.py` (`FileHandoffStore.read`: `try/except (json.JSONDecodeError, ValueError): return None`) | `tests/sprint/test_handoff_store.py` (added `test_read_corrupt_handoff_returns_none`) |
| **M4** | Sprint scheduler had zero dedicated tests | (test-only; no source change) | `tests/sprint/test_scheduler.py` (NEW — 9 tests) |

**Six touched files:** `executor.py`, `handoff.py`, `test_handoff_store.py`, `test_executor.py`, `test_poll_watchdog_ceiling.py`, `test_scheduler.py`. No new imports added to any source file.

## Verification artifacts

| Artifact | Command | Overall | Counts |
|----------|---------|---------|--------|
| m3-handoff.txt / m3-summary.md | `pytest tests/sprint/test_handoff_store.py -v` | PASSED | 5 passed, 0 failed |
| m1-executor.txt / m1-summary.md | `pytest tests/sprint/test_executor.py -k "closes_handles or run_task_subprocess" -v` | PASSED | 2 passed, 0 failed (92 deselected) |
| m2-watchdog.txt / m2-summary.md | `pytest tests/sprint/test_poll_watchdog_ceiling.py -v` | PASSED | 3 passed, 0 failed |
| m4-scheduler.txt / m4-summary.md | `pytest tests/sprint/test_scheduler.py -v` | PASSED | 9 passed, 0 failed |
| full-sprint.txt / full-sprint-summary.md | `pytest tests/sprint/ -q` | PASSED | 1124 passed, 0 failed, 0 skipped |
| ruff-format.txt | `ruff format --check src/ tests/` | CLEAN | 781 files already formatted |
| make-lint.txt | `make lint` (`ruff check` + architecture lint) | ruff CLEAN on touched files; architecture lint has 1 **pre-existing UNRELATED** error in `commands/recommend.md` (not touched) | — |

## Full-suite / format / lint results

- **Full sprint suite:** 1124 passed, 0 failed, 0 skipped (20 pre-existing diagnostic DeprecationWarnings, unrelated).
- **Ruff format:** clean; reformat confined to the 3 task-owned files (cosmetic assert wrapping).
- **Ruff check (lint):** "All checks passed!" on all six touched files. The single `make lint` error is a pre-existing command↔skill architecture-link failure on `src/superclaude/commands/recommend.md`, outside this task's scope and left unfixed per scope discipline.

## Overall readiness statement

**ALL GREEN for the task's scope.** Each M1/M2/M3 source fix is paired with a regression test that fails-before/passes-after; M4 adds a dedicated 9-test scheduler suite asserting exact traced outputs. Full sprint suite, ruff format, and ruff-check (touched files) are all clean. The only outstanding `make lint` error is pre-existing and unrelated to the six touched files (no scope creep permitted to fix it). Ready for the FINAL_ONLY structural QA gate.
