# QA Report: M4 fidelity gate, structural verification (cycle 1 fix check)

**Topic:** issue-watch implementation, source-fidelity gate, Step 9.M6
**Date:** 2026-11-08
**Phase:** fix-cycle (verification of fix cycle 1, report-only, `fix_authorization: false`)
**Fix cycle:** 1

## Overall Verdict: PASS

The only blocking finding (M-1) is fixed in the files and proven by tests that fail when the fix is reverted. No new blocking structural issue was found. No row is NEEDS OWNER DECISION.

## Blocking findings

| id | Status | Evidence |
|---|---|---|
| M-1 | FIXED | `src/superclaude/cli/issue_watch/cycle.py:751-756`: `self.clock_skew_s = int(round(skew))` is now set whenever the `Date` header parsed (`server is not None`); only `self._warn("clock_skew", ...)` stays under `if skew > SKEW_WARN_S` (60). `_conclude` (`cycle.py:1154`) still passes the attribute to the cycle line. `audit.py` needs no change: `_optional` drops only `None`, `_TYPES["clock_skew_s"] = (int, False)` (line 195) and the cycle-line key set (line 165) accept `0`. Tests: `tests/issue_watch/test_cycle.py:1701-1714` is now parametrized over skew 0, 59, 60, -60 and asserts no warning line AND `clock_skew_s == seen` (int); lines 1717-1731 keep the 61, -61, 300 cases (warning and cycle-line value); line 1743 asserts the key is absent when the date is unparseable (DF-35); line 1307 (whole-line idle test) expects `"clock_skew_s": 0`. Runbook `docs/designs/issue-watcher-setup.md:414` now says the field is on every cycle that read GitHub's date and the warning is written only above 60 s. I reverted the fix in a throw-away copy (field set only above 60): 5 tests failed (the four new `[0-0|59-59|60-60|-60-60]` cases with `KeyError: 'clock_skew_s'`, plus `test_idle_cycle_makes_two_gh_calls_and_writes_one_cycle_line__fr001`) and 2630 passed. So the new assertions detect the old behaviour. No assertion was weakened: the one removed assertion (`not in`) was the one pinning the defect; the replacement is stricter. |

Needs owner decision rows: none. The fix report's "Needs owner decision: None" is correct (M-1 needs no design or spec change; it follows spec line 100 and design line 715).

## Re-run results (my own runs, not taken from the fix report)

| Check | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` (plain, repo venv, Python 3.11) | 2635 passed in 18.89s |
| xdist: `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -q` | 2635 passed in 7.54s (plain `-n` is not installed in the repo env; I used the same `--with` form as the gate-D reproduction report) |
| Python 3.10.20 (interpreter confirmed by `sys.version`: `3.10.20 (main, Apr 14 2026...)`), full `tests/issue_watch` on a `/tmp` copy, method as in `qa/gate-d/qa-structural-module-boundaries-report.md` row 7 (venv of the uv 3.10 interpreter, pure-Python deps of the 3.11 venv via `.pth`, `exceptiongroup` and `tomli` from the uv cache, a `jsonschema` import shim needed only by the unrelated `eval` and `swarm` modules; `rpds` is a cp311 binary and cannot load) | 2635 passed in 23.61s, including the three subprocess e2e tests |
| `make lint` | architecture policy "PASS (5 warning(s))", `ruff check .`: "All checks passed!" |
| Pinned `uvx --offline ruff@0.15.20 --version` | `ruff 0.15.20` |
| Pinned `ruff@0.15.20 check src/superclaude/cli/issue_watch tests/issue_watch` | All checks passed |
| Pinned `ruff@0.15.20 format --check` on the same two trees | 30 files already formatted |
| Imports match design lines 233-242 | `tests/issue_watch/test_module_boundaries.py` (the import-table test) is inside the 2635 passed on 3.11, xdist and 3.10. The fix touched no import line (`cycle.py` diff is lines 751-756 only, by the fix report and the code I read). |

## Scope check (git status)

- `git diff --name-only` (tracked changes): the task file (executor's checkbox ledger) and `src/superclaude/cli/main.py` (the 4-line `issue-watch` registration, which the fix prompt allows).
- Untracked: `src/superclaude/cli/issue_watch/`, `tests/issue_watch/`, `docs/designs/issue-watcher-setup.md`, `docs/designs/issue-watcher.md` (the design; mtime 2026-11-07 15:08, older than the findings file, so not touched by the fix), `.dev/brainstorms/...`, `.dev/issues/331/`, and the task package's `phase-outputs/` and `qa/` directories.
- Files modified after `qa-fidelity-consolidated-findings.md` was written (`find -newer`, excluding caches and `.codegraph`): `tests/issue_watch/test_cycle.py`, `src/superclaude/cli/issue_watch/cycle.py`, `docs/designs/issue-watcher-setup.md`, the fix report, and the task file. All are inside the allowed set or are the QA report and ledger. No change under `.claude/`, `pyproject.toml`, `Makefile`, workflows, the spec, the design, or research files.
- Nothing in the repo was modified by this verification; my 3.10 copy and its mutation were in a `/tmp` directory that I removed.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR (note) | `phase-outputs/reports/ac-trace.md` lines 5 and 7 (M-8) | Test counts in the change-set reports (2628 passed, 844 tests) are older than the 2635 now measured. | None needed now; already carried as minor note M-8. |
| 2 | MINOR (note) | `qa/m4/qa-fidelity-fix-report.md` | Says "2635 passed" and gives the mutant result; both reproduced. No discrepancy. | None. |

No new blocking findings. Minor findings M-2 to M-66 are notes and were not rechecked.

## Confidence

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
(Items: M-1 code, M-1 tests, M-1 runbook, mutation of the fix, plain pytest, xdist pytest, Python 3.10.20 pytest, `make lint`, pinned ruff check, pinned ruff format, import table (boundary test), git-status scope.)

**Tool engagement:** Read: 9 | Grep: 8 | Glob: 0 | Bash: 14 (two blocked by the bare-python hook and rerun through `uv run`; no web research, so no Tavily or fallback calls)

## QA Complete
