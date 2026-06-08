# Full Sprint Pytest — Step 5.1

**Date:** 2026-06-05
**Command:** `uv run pytest tests/sprint/ -q` (from the worktree)

## Result: PASS (clean)

```
================= 1159 passed, 20 warnings in 83.88s (0:01:23) =================
```

| Metric | Value |
|--------|-------|
| Total | **1159 passed, 0 failed** |
| Failing node ids | None |
| Baseline attribution | The documented baseline `tests/sprint/test_e2e_success.py::test_jsonl_events_for_each_phase` **also passed** in this run — the suite is fully clean, exceeding the task's "passes cleanly OR fails only the documented baseline" bar. |
| Warnings | 20 (pre-existing `DiagnosticBundle.config=None` DeprecationWarnings — unrelated to this change, not introduced by the fix) |

- The pytest run also serves as compile/import proof for the edited modules (`rerun_tasks.py`, `handoff.py`) and edited tests — all imported and executed without error.
- New regression tests included in the green count: `TestRerunTargetsPassed` (3) + the extended `test_is_validated_success_only_for_pass_plus_gate_success` (10 cases).

Raw output: `pytest-sprint-full.txt`.
