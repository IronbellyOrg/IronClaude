# RED→GREEN Summary — CRITICAL rerun predicate (Step 4.1)

**Date:** 2026-06-05
**Test:** `tests/sprint/test_rerun_tasks.py::TestRerunTargetsPassed::test_pass_recovered_target_counts_as_passed`
**Fixture shape (carried correction F1):** `task_results`-wrapped per research/02:36-39 — `{"status": "pass_recovered", "task_results": [{"task": {"task_id": "T07.11"}, "status": "pass_recovered"}]}`. The broken inline form (no `task_results` wrapper) would have made GREEN fail; using the wrapped shape is what makes this a valid RED→GREEN.

| Phase | Predicate state | Node result | Evidence |
|-------|-----------------|-------------|----------|
| **RED** | old literal `status_by_id.get(t) == "pass"` restored | ❌ **1 failed** — `assert False is True` | `rerun-target-red.txt` |
| **GREEN** | fix reapplied (`_is_success_task_status(...)`) | ✅ **3 passed** | `rerun-target-green.txt` |

- RED fails for the old predicate (pass_recovered judged not-passed) → the test genuinely catches the bug.
- GREEN passes for the fixed predicate. The GREEN run covers the full `TestRerunTargetsPassed` class: `test_pass_recovered_target_counts_as_passed` (the regression), plus guards `test_plain_pass_target_still_counts_as_passed` (no regression of the literal-pass path) and `test_failed_target_is_not_passed` (no over-broadening to non-success).
- Worktree left in the **fixed** state (`rerun_tasks.py:1238` = `_is_success_task_status(...)`; no `RED-TEMP` marker remains).
- No unrelated test-file content modified.
