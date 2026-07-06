# Full Sprint Pytest Summary (Step 5.2)

**Date:** 2026-06-04
**Command:** `uv run pytest tests/sprint/ -q`
**Run from:** worktree `fix-sprint-integrity-signalb-pass-recovered`
**Raw output:** `phase-outputs/test-results/full-sprint-pytest-output.txt`

| Check | Result |
|---|---|
| Command uses UV / no `python -m` | YES — compliant |
| Passed | 1156 |
| Failed | 0 |
| Warnings | 20 (pre-existing `DeprecationWarning: DiagnosticBundle.config=None`; unrelated to this change) |
| Exit code | 0 |
| Duration | ~83 s |

## Baseline node status

The known pre-existing baseline node `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` **did NOT fail** in this run — the full `tests/sprint/` suite passed cleanly (1156 passed, 0 failed). The documented baseline exception is therefore **not invoked** (not fabricated when absent). No failures are owned by this task.

**Verdict:** The full sprint suite is green with the Opt-2a fix and the three new/converted tests in place. No regressions introduced. Ready for ruff checks.
