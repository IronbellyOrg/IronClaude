# QA Report - Gate C structural verification of the fix, cycle 2 (Step 7.G15)

**Topic:** issue-watch implementation, Gate C cycle 2 (blocking id C2-1 = N-1)
**Date:** 2026-11-08
**Phase:** fix-cycle (structural verification, report-only, `fix_authorization: false`)
**Fix cycle:** 2

---

## Overall Verdict: PASS

The one blocking finding (C2-1) is FIXED in the repository files. No cycle-1 fix was undone. No new blocking structural issue. Minor notes are not rechecked.

## One row per blocking finding

| id | Verdict | Evidence |
|---|---|---|
| C2-1 (N-1) | FIXED | `src/superclaude/cli/issue_watch/cycle.py` `_launch`: `launch_allowed()` at line 1039 (pre-check) and the `timeout_for(GIT_TIMEOUT_S)` None guard at 1041-1043, both before `_origin_ok` (1044); a second `launch_allowed()` at 1048-1049 sits after `_origin_ok` and before `mark_pending` (1060), `_save` (1061) and `launcher.launch` (1062); it raises `_Skip("budget_exhausted")`. New test `test_cycle.py:4293` (`..._inside_the_origin_call_starts_no_launch__fr029_n1`): +115 s at the reserved `items` re-read, +10 s inside the second `origin` call; asserts exit 0 `cycle_complete`, decisions `[(9, "budget_exhausted")]`, two `origin` calls, no launcher call, no entry, issue 9 not stamped. My mutants (copy under /tmp, repo not mutated): second check removed -> 1 failed, 795 passed (the new test fails); second check raising `origin_mismatch` instead -> 1 failed (the new test). |

## Environment checks run by me

| # | Check | Result | Evidence |
|---|---|---|---|
| E1 | `uv run pytest tests/issue_watch/ -v` | PASS | 2243 passed in 8.81 s (fix report: 2243). |
| E2 | Same suite on Python 3.10 (`uv run --offline --isolated --python 3.10 ...`) | PASS | 2243 passed in 10.14 s. Grep over the nine modules: no `tomllib`, `StrEnum`, `except*`, `datetime.UTC`, `Self`; the one `fromisoformat` hit is a docstring in `predicates.py:30` saying it is not used. |
| E3 | `make lint` | PASS | 0 architecture errors, 5 warnings (the known 5); `ruff check .` all checks passed. |
| E4 | `uvx --offline ruff@0.15.20 check` on `src/superclaude/cli/issue_watch`, `tests/issue_watch`, `src/superclaude/cli/main.py` | PASS | "All checks passed!" |
| E5 | `uvx --offline ruff@0.15.20 format --check` on the same paths | PASS | "24 files already formatted". |
| E6 | `uv run superclaude issue-watch --help` | PASS | Five commands: check-config, init-state, once, reset, status. |
| E7 | Imports against design lines 233-242 | PASS | `cycle.py` imports (lines 10-31): stdlib, `audit, github, launch, predicates, record` and `.runner` only; the allowed set for `cycle`. The other eight modules are unchanged since before the cycle-1 verification (mtimes: audit/cli 00:40, github 21:33, launch/record 22:47, predicates 22:43, runner 21:33; the cycle-1 verification reports are 00:57), so their cycle-1 import verdict stands. |
| E8 | Scope, via `git status` and `find -newer qa-consolidated-findings-cycle2.md` | PASS | Files modified after the cycle-2 consolidation: only `cycle.py`, `tests/issue_watch/test_cycle.py`, the cycle-2 fix report and the task file (executor ticks). `git status` outside `.dev/` shows only `M src/superclaude/cli/main.py` (mtime 11-07 23:48, the earlier registration, untouched), and untracked `docs/designs/issue-watcher.md` (mtime 11-07 15:08, the design), `src/superclaude/cli/issue_watch/`, `tests/issue_watch/`. `pyproject.toml` and `Makefile` mtimes 11-07 06:41. Nothing changed outside `src/superclaude/cli/issue_watch/`, `tests/issue_watch/` and `main.py`. |
| E9 | Repo not left mutated by me | PASS | My mutants ran in `mktemp -d /tmp/ironclaude-batch.*` copies removed by trap; `git status` after the runs unchanged. One older `/tmp/ironclaude-batch.*` directory is not mine and was left alone. |

## Regression section (cycle-1 items marked FIXED or PASS)

The cycle-2 change touched only `_launch` in `cycle.py` (one added guard) and added one test. All 13 cycle-1 ids (C-1 to C-13) remain fixed: the full suite, which holds every cycle-1 test, passes (2243, on 3.10 and 3.11). I re-ran cycle-1 mutants against the current tree; each is killed:

| Cycle-1 id | Mutant | Result |
|---|---|---|
| C-1 | pre-check `launch_allowed()` skip turned into `origin_mismatch` | killed (1 failed) |
| C-1 / C-11 | `origin_timeout is None` skip turned into `origin_mismatch` | killed (1 failed) |
| C-2 | clean-cycle reason `cycle_complete` back to `not_approved` | killed (1 failed) |
| C-9 | dry-run also saves the migrated store (`cycle.py:727`) | killed (1 failed) |
| C-10 | `self.halt = True` replaced by `pass` (`cycle.py:815`) | killed (1 failed) |

C-3 (`cli.py`), C-4, C-5, C-12 and C-13 live in files the cycle-2 fix did not touch (`cli.py` unchanged since 00:40; tests other than `test_cycle.py` unchanged); their tests are in the green suite. No regression.

## New blocking findings

None.

Notes (minor, not rechecked): removing the pre-check `launch_allowed()` at line 1039 (the cycle-1 check, before the git call) survives the suite (2243 passed): for elapsed between 120 s and 235 s no test pins that the git call is skipped. The launch outcome stays correct without it (the post-check still ends the step with `budget_exhausted` and no entry); only a needless git call would be made. Cycle-1 notes M-1 (`pytest.skip` in `test_cycle.py`) and M-3 (C-3 test raises only `RuntimeError`) stand unchanged.

## Summary

- Blocking ids: 1 / 1 FIXED, 0 NOT FIXED. Environment checks: 9 / 9 PASS. Regressions: 0. New blocking issues: 0.

**Confidence:** Verified: 10 / 10 (1 finding row, 9 environment checks; the regression section rests on the same suite plus 5 re-run mutants) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%.
**Tool engagement:** Read: 9 | Grep: 3 | Glob: 0 | Bash: 7

## QA Complete
