# QA Report — Structural Lint/Format Validation

**Topic:** ruff check + ruff format --check on tests/troubleshoot/backtest/
**Date:** 2026-06-12
**Phase:** task-integrity (structural lint/format gate)
**Fix cycle:** N/A (report-only, fix_authorization: false)

---

## Overall Verdict: PASS

Both `ruff check` and `ruff format --check` are green in their FINAL state on
`tests/troubleshoot/backtest/`, independently re-run and confirmed. No source file modified.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | `uv run ruff check tests/troubleshoot/backtest/` green | PASS | Re-ran via Bash → `All checks passed!`, exit code 0 (`---CHECK_EXIT=0---`). Matches claimed FINAL STATE in ruff-backtest-output.txt:10. |
| 2 | `uv run ruff format --check tests/troubleshoot/backtest/` green | PASS | Re-ran via Bash → `20 files already formatted`, exit code 0 (`---FORMAT_EXIT=0---`). Matches claimed FINAL STATE in ruff-backtest-output.txt:11. |
| 3 | Path is real & populated (not a no-op against empty/wrong dir) | PASS | `find ... -name '*.py' \| wc -l` → 20 .py files. The "20 files already formatted" count equals the actual file count, proving format actually scanned all files. |
| 4 | Files present on disk (untracked or otherwise) | PASS | `git status --short` → `?? tests/troubleshoot/backtest/` (untracked). All 20 files exist on disk and were scanned by both commands. |
| 5 | CI parity (format --check run separately from make lint) | PASS | Both `ruff check` AND `ruff format --check` independently green — CI runs `ruff format --check src/ tests/` separately, both surfaces covered for this path. |

## Summary
- Checks passed: 5 / 5
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found
None. Adversarial probes (empty-path no-op, untracked files unscanned, stale
output file) all came back clean: file count (20) equals the format-pass count (20),
and both commands were independently re-executed this session rather than trusted
from the recorded output.

## Actions Taken
None — fix_authorization: false. No source file modified.

## Confidence
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 | Glob: 0 | Bash: 3

## Recommendations
- None blocking. Both ruff surfaces are green for `tests/troubleshoot/backtest/`.
- Note: the `VIRTUAL_ENV=/lsiopy does not match .venv` warning is environmental
  (UV targeting `.venv`) and does not affect lint/format results — ruff still ran and passed.

## QA Complete
