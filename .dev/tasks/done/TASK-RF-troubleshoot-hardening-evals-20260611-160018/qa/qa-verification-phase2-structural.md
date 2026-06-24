# QA Report — Phase 2 Fix Verification (Structural)

**Topic:** git-replay helper fixes for P2-1/P2-2/P2-3
**Date:** 2026-06-12
**Phase:** fix-cycle (verification)
**Fix cycle:** 1
**Mode:** report-only (fix_authorization: false — modified NO file)
**Target:** `tests/troubleshoot/backtest/git_replay.py`

---

## Overall Verdict: PASS

All 3 consolidated findings (P2-1 CRITICAL, P2-2 IMPORTANT, P2-3 MINOR) are
structurally addressed in `git_replay.py`; no new issues introduced; all
load-bearing invariants intact; all 6 tests green; ruff check + format clean.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| P2-1 | Each teardown `_subprocess.run` (remove + prune) in its OWN `try/except (TimeoutExpired, FileNotFoundError, OSError): pass` | PASS | remove guarded `git_replay.py:155-165` (try L155, run L156-163, except L164-165); prune guarded `git_replay.py:168-178` (try L168, run L169-176, except L177-178) |
| P2-1 | Ordering remove→rmtree→prune preserved; all three always attempt | PASS | remove L156-163, `shutil.rmtree(base, ignore_errors=True)` L166, prune L169-176 — sequential in `finally`, each independent; `rmtree` cannot raise (`ignore_errors=True`) so it never skips prune |
| P2-1 | No teardown step can mask body exception or skip subsequent steps | PASS | both subprocess steps swallow their own raises (L164-165, L177-178); `finally` re-raises the original body exception untouched — confirmed by unit test `test_backtest_..._teardown_fires_even_when_body_raises` asserting `excinfo.value is sentinel` (`test_git_replay_unit.py:49`) |
| P2-2 | git worktree calls anchored to one resolved repo via `cwd=` | PASS | `_repo_anchor()` resolves `git rev-parse --show-toplevel` `git_replay.py:69-92`; resolved once L137 (`anchor = _repo_anchor()`) and passed `cwd=anchor` to add (L145), remove (L162), prune (L175) |
| P2-2 | add + matching remove/prune target SAME repo | PASS | single `anchor` value (L137) reused by all three calls in the same `checkout_worktree` invocation; `worktree_list_porcelain` also anchors via `cwd=_repo_anchor()` (L102) |
| P2-3 | `base.mkdir(...)` only on `scratch_root is not None` branch | PASS | `mkdir` at `git_replay.py:131` sits inside `if scratch_root is not None:` (L127); else branch uses `tempfile.mkdtemp` (L133) which creates the dir itself |
| P2-4 | G1 no-caret: commitish passed verbatim | PASS | add argv `["git","worktree","add","--detach",str(wt),commitish]` `git_replay.py:140` — no `^` manipulation; unit test asserts `"^" not in add[-1]` (`test_git_replay_unit.py:37`) |
| P2-4 | REPLAY_ESCAPES bare parent shas unchanged | PASS | `git_replay.py:48-56` E1=94d5baa0, E2=10723863, E3=e97aa4fd, E4=1b0264f1, E5=d878bc6d — matches unit-test expected map (`test_git_replay_unit.py:63-69`); no carets |
| P2-4 | `from __future__ import annotations` first | PASS | `git_replay.py:16` — first statement after module docstring, before all other imports |
| P2-4 | Public API unchanged | PASS | `ReplayEscape` (L28), `REPLAY_ESCAPES` (L48), `escape_by_id` (L59), `worktree_list_porcelain` (L95), `checkout_worktree` (L106-109, signature `(commitish, *, scratch_root=None)` unchanged); only addition is private `_repo_anchor` (underscore) L69 |
| P2-4 | `_repo_anchor` stays under unit mock seam (no `-C`) | PASS | uses `_subprocess.run(["git","rev-parse","--show-toplevel"], ...)` `git_replay.py:82-88` not `-C`; argv-shape tests in unit suite remain green and do not break on the extra rev-parse call |
| TESTS | unit + integration suite green | PASS | 6 passed in 2.66s; both integration tests RAN (not skipped) — real-git teardown path exercised, incl. `test_backtest_replay_leaves_no_leaked_worktree` (before==after worktree list) |
| LINT | `ruff check` clean | PASS | "All checks passed!" |
| FMT | `ruff format --check` clean | PASS | "1 file already formatted" |

## Summary

- Checks passed: 14 / 14
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only mode — no files modified)

## Confidence

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 2

Tool-call count (6: 4 Read + 2 Bash) ≥ findings under review; the 2 Bash calls
executed the test suite (6/6 green, integration not skipped) and ruff
check+format. Structural claims verified directly against the Read source with
cited line numbers. No UNCHECKED or UNVERIFIABLE items.

## Issues Found

None. No NEW issues introduced by the serialized fix; all three prior findings
resolved.

## Notes — why integration coverage strengthens this verdict

The integration tests are not skipped in this environment (full-depth work-tree
with all 5 replay parents present), so P2-1 and P2-2 are validated on the REAL
git path, not just the mock seam: `test_backtest_replay_leaves_no_leaked_worktree`
forces a body `RuntimeError` and asserts the porcelain worktree list is
byte-identical before/after — proving remove+prune both fired through the new
per-call guards without the body exception masking them.

## QA Complete
