# M1 Verification Summary

**Command:** `uv run pytest tests/sprint/test_executor.py -k "closes_handles or run_task_subprocess" -v`

**Overall result:** PASSED

**Counts:** 2 passed, 0 failed (92 deselected)

| Test | Status |
|------|--------|
| test_run_task_subprocess_uses_task_output_file | PASS |
| **test_run_task_subprocess_closes_handles_when_poll_raises** (new, M1) | **PASS** |

The new M1 regression test is present and passing; the existing `_run_task_subprocess` seam test is unaffected. The test pins both M1 invariants: `terminate()` fires on the exception path AND `KeyboardInterrupt` re-propagates (no swallow).
