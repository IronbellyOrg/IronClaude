# Full `uv run pytest -q` (item 8.2)

Worktree: `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize`
Date: 2026-09-20
Baseline: `phase-outputs/discovery/baseline-summary.md` (25 failed + 1 error, 11361 passed)

## Summary line

```
25 failed, 11536 passed, 139 skipped, 2 xpassed, 37 warnings, 1 error in 355.53s (0:05:55)
```

Passed delta vs baseline: +175 (matches the 21 new files).

## Failing node ids (25 FAILED + 1 ERROR)

Same set as baseline items 1–26 (25 FAILED + ERROR `tests/v3.3/test_zero_files_analyzed.py::TestZeroFilesAnalyzedFail::test_zero_files_analyzed_returns_fail`). Includes known-red e4.

new reds: none
