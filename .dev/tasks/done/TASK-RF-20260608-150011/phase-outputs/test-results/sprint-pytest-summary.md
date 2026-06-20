# Sprint Test Suite Summary — TASK-RF-20260608-150011

**Command:** `uv run pytest tests/sprint/ -v`
**Date:** 2026-06-08
**Raw output:** `sprint-pytest-raw.txt`

## Overall Result: ✅ PASSED

| Metric | Count |
|--------|-------|
| Passed | 1163 |
| Failed | 0 |
| Errors | 0 |
| Skipped | 0 |
| Warnings | 20 (pre-existing DeprecationWarnings, unrelated) |
| Duration | 82.37s |

Final pytest line:
```
================= 1163 passed, 20 warnings in 82.37s (0:01:22) =================
```

## New regression tests (this task)

| Test | File | Status |
|------|------|--------|
| `test_merge_relocates_deliverable_trees_or_partials` | tests/sprint/test_recovery.py::TestMergeRecoveryBundle | ✅ PASSED |
| `test_recover_reevaluates_stale_fail_to_unknown` | tests/sprint/test_checkpoints.py::TestRecoverMissingCheckpoints | ✅ PASSED |
| `test_recover_preserves_fail_when_tasks_still_failing` | tests/sprint/test_checkpoints.py::TestRecoverMissingCheckpoints | ✅ PASSED |

## Failed tests

None.

## Notes

- No fabrication: counts taken verbatim from `sprint-pytest-raw.txt` final summary line.
- The 20 warnings are pre-existing `DeprecationWarning`s (e.g. `DiagnosticBundle.config=None`) in `tests/sprint/diagnostic/` — unrelated to this change.
- The four modified source files (`recovery.py`, `rerun_tasks.py`, `checkpoints.py`, `commands.py`) and two modified test files (`test_recovery.py`, `test_checkpoints.py`) all import and run cleanly with the full suite green.
