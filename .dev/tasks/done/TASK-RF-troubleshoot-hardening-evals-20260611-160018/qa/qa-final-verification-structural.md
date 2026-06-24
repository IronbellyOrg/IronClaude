# QA Report — Fix Cycle (Final Structural Verification)

**Topic:** Troubleshoot hardening backtest harness — final lens fix verification (F-1, F-2, F-3, F-5)
**Date:** 2026-06-12
**Phase:** fix-cycle (report-only, fix_authorization: false)
**Fix cycle:** Final verification pass (post serialized I20 fix agent)

---

## Overall Verdict: PASS

All four code fixes (F-1, F-2, F-3, F-5) are independently verified against git ground-truth and source text. No regressions: backtest suite 42 passed / 11 skipped / 0 failed; in-scope ruff check + format clean.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| F-1 | E4 cites `acd5631f` (#158) as HEAD-heal; no remaining `20693bb8` HEAD-heal claim except the documented sibling-fix note; replay base still `1b0264f1` | PASS | `git merge-base --is-ancestor acd5631f HEAD` → EXIT 0 (ancestor); `20693bb8` → EXIT 1 (NOT ancestor); `1b0264f1` → EXIT 0 (ancestor). `acd5631f` appears 4× in `test_backtest_e4.py` (L14, L18, L46, L79). Only remaining `20693bb8` is the single documented sibling-fix disclaimer at `test_backtest_e4.py:16` ("the spec/research cited the HEAD-heal as `20693bb8`, a same-intent SIBLING fix on another branch"). Replay base pinned to `1b0264f1` at `test_backtest_e4.py:39` and `git_replay.py:56`. |
| F-2 | E5 asserts discriminating `--diff <BASE>..HEAD`; pre-fix grep ≥1, post-fix grep 0 | PASS | `git show d878bc6d:.../task-builder/SKILL.md \| grep -c -- '--diff <BASE>..HEAD'` = **1** (pre-fix present). Current `SKILL.md` same grep = **0** (post-fix absent → discriminating). `test_backtest_e5.py:48` asserts `"--diff <BASE>..HEAD" in text`; the non-discriminating assertion 2 (`"Do NOT use \`start_commit..HEAD\`" not in text`) retained at L56. |
| F-3 | Negative test: empty/whitespace `proxy_limitation` raises `ValueError` | PASS | `test_catch_rate_schema.py:268-286` — `@pytest.mark.parametrize("blank", ["", "   ", "\t", "\n  \t"])` over `test_backtest_proxy_limitation_empty_or_whitespace_raises`, asserting `pytest.raises(ValueError)` against `CatchRateReport(... proxy_limitation=blank)` with a valid `not_run` shape so ONLY the blank caveat triggers the raise. Guard is in `catch_rate.py:164-168` (`__post_init__` step 0). |
| F-5 | Wave-range docs in `git_replay.py` + `catch_rate.py` no longer contradictory | PASS | `git_replay.py:36-38` (`ReplayEscape.wave`): "H0..H5 is the FULL wave taxonomy; the E1-E5 escapes themselves only ever map to H1..H4 ... the two ranges are consistent, not contradictory." `catch_rate.py:79-81` (`EscapeResult.wave`): "H1..H4 are the waves the E1-E5 escapes actually map to; the full wave taxonomy is H0..H5 (see `ReplayEscape.wave` in `git_replay.py`) -- the narrower range here is a subset, not a contradiction." Both docstrings cross-reference each other and explicitly reconcile full-taxonomy vs. mapped-subset. |
| R-1 | No regressions: backtest suite passes | PASS | `uv run pytest tests/troubleshoot/backtest/ -q` → **42 passed, 11 skipped** in 10.26s, 0 failed/errored. |
| R-2 | ruff check clean (in scope) | PASS | `uv run ruff check tests/troubleshoot/backtest/` → "All checks passed!". Repo-wide ruff has 127 pre-existing errors but **0** touch `troubleshoot/backtest/` (`ruff check \| grep -c troubleshoot/backtest` = 0). |
| R-3 | ruff format clean (in scope) | PASS | `uv run ruff format --check tests/troubleshoot/backtest/` → "21 files already formatted". The 5 specific fix files all "already formatted". Repo-wide reformats (101 files) are pre-existing and out-of-scope (swarm/ etc.). |

## Summary

- Checks passed: 7 / 7
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization: false — no files modified)

## Issues Found

None.

Note on scope boundary (not an issue): repo-wide `ruff check` reports 127 pre-existing errors and `ruff format --check src/ tests/` would reformat 101 files. These are entirely outside the fix surface — zero are under `tests/troubleshoot/backtest/`. Per the spawn prompt's check #5 ("`uv run ruff check` + `uv run ruff format --check` clean"), scoped to the harness fix surface, the in-scope files are clean. The pre-existing repo-wide debt is documented here for transparency but does not block this verdict.

## Actions Taken

None — report-only verification. No file was modified.

## Confidence

Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 6 | Grep: 0 (via Bash grep) | Glob: 0 | Bash: 4

Every check maps to a specific tool-verified fact: F-1 to three `git merge-base --is-ancestor` exit codes + grep counts on `test_backtest_e4.py`; F-2 to `git show` pre-fix grep + current grep + assertion grep on `test_backtest_e5.py`; F-3 to a Read of `test_catch_rate_schema.py:268-286` and `catch_rate.py:164-168`; F-5 to Reads of `git_replay.py:36-38` and `catch_rate.py:79-81`; regressions to a live `pytest` run + scoped `ruff` runs.

## Recommendations

- Green light: the four lens-finding fixes are correct, git-grounded, and regression-free. The harness suite is shippable on this surface.
- The pre-existing repo-wide ruff debt (127 errors, 101 unformatted files, all outside `troubleshoot/backtest/`) is a separate, pre-existing concern and is out of scope for this task.

## QA Complete
