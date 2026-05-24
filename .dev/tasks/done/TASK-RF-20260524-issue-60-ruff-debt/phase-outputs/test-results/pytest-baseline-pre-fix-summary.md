# Pytest Pre-Fix Baseline Summary

**Timestamp:** 2026-05-25 03:12
**Command:** `uv run pytest --tb=no -q`
**Branch:** `fix/issue-60-ruff-debt` (off latest master)

## Metrics

| Metric | Count |
|--------|-------|
| Passed | 7277 |
| Failed | 88 |
| Errors | 1 |
| Skipped | 110 |
| Warnings | 27 |
| Exit Code | 1 |
| Duration | 93.25s (0:01:33) |

## Summary Line (Verbatim)

```
= 88 failed, 7277 passed, 110 skipped, 27 warnings, 1 error in 93.25s (0:01:33) =
```

## Acceptance Rules for Preservation

After each phase, the comparison report must verify:
- `passed_after >= 7277`
- `failed_after <= 88`
- `errors_after <= 1`

Skipped count may vary (some tests are skipped conditionally).

## Notes

- The baseline shows 88 pre-existing failures and 1 error — these are NOT introduced by this task. The goal is preservation, not improvement.
- One known sample: `tests/sprint/test_watchdog.py::TestWatchdogWarnAction::test_stall_warn_action` (FAILED in baseline).
- One known error: `tests/v3.3/test_zero_files_analyzed.py::TestZeroFilesAnalyzedFail::test_zero_files_analyzed_returns_fail` (ERROR in baseline).

## Raw Output

See `pytest-baseline-pre-fix.txt` for the complete pytest output.
