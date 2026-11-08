# QA Report - Gate C structural verification of the fix (Step 7.G10)

**Topic:** issue-watch implementation, Gate C fix (blocking ids C-1 to C-13)
**Date:** 2026-11-08
**Phase:** fix-cycle (structural verification, report-only, `fix_authorization: false`)
**Fix cycle:** 1

---

## Overall Verdict: PASS

All 13 blocking findings are FIXED in the repository files; no new blocking structural issue found. Minor findings (C-14 to C-69) were not rechecked, per the severity rule.

## Environment checks run by me (not taken from the fix report)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| E1 | `uv run pytest tests/issue_watch/ -q` | PASS | 2242 passed in 8.26 s (fix report says 2242). |
| E2 | Same suite on Python 3.10 (`uv run --offline --isolated --python 3.10 --with pytest --with click --with rich pytest tests/issue_watch/`), `.venv` not touched | PASS | 2242 passed in 12.28 s. Also `ast.parse(feature_version=(3,10))` on all 23 .py files: 0 errors; grep found no `tomllib`, `StrEnum`, `Self`, `except*`, `fromisoformat`, `datetime.UTC`, `match` statement. `requires-python = ">=3.10"` (pyproject.toml:16). |
| E3 | `uvx --offline ruff@0.15.20 check src/superclaude/cli/issue_watch tests/issue_watch` | PASS | "All checks passed!" |
| E4 | `uvx --offline ruff@0.15.20 format --check` on the same two directories | PASS | "23 files already formatted" (all files, not only the 10 changed). |
| E5 | `make lint` | PASS | arch policy 0 errors, 5 warnings (the fix report's "5 existing warnings"); `ruff check .` all checks passed. |
| E6 | `uv run superclaude issue-watch --help` | PASS | Lists exactly five commands: check-config, init-state, once, reset, status. |
| E7 | Imports against design 5.3 table (design lines 233-242), read from `grep -nE '^\s*(from|import) '` over all 9 modules | PASS | `runner`, `predicates`, `audit`: stdlib only. `github`: `.predicates`, `.runner`. `record`: `predicates`, lazy `superclaude.cli.swarm.atomic`. `launch`: `.runner`, `superclaude.cli.install_user_setup._ORCA_CLIS`. `cycle`: `audit, github, launch, predicates, record, runner` (all allowed). `cli`: `audit, cycle, record, launch, runner` + `click`. No new import was added by the fix beyond the allowed set. |
| E8 | Scope of the fix, via `git status`, `git diff --stat`, mtimes (`find -newer qa-consolidated-findings.md`) | PASS | Files modified after the findings file: only `src/superclaude/cli/issue_watch/{cycle,audit,cli}.py`, `tests/issue_watch/{conftest,test_audit,test_cli,test_cycle,test_launch,test_github,test_slo_helper}.py`, two new files in `tests/issue_watch/fixtures/_assumed_shape/`, the fix report, and the task file (executor checkbox ticks, not the fix agent). `src/superclaude/cli/main.py` mtime is 2026-11-07 23:48, before the findings (00:37 on 11-08): it is the earlier two-line registration, not touched by the fix. `pyproject.toml`, `Makefile`, `.claude/`, design, spec, research: unchanged. No file outside `src/superclaude/cli/issue_watch/`, `tests/issue_watch/` was changed by the fix. |
| E9 | Repo not left mutated | PASS | `git status` shows only the expected set (staged `.dev/tasks` research, `M main.py`, untracked `issue_watch` source and tests, design, gate folders). No stray scratch tests; no `/tmp` mutant dir newer than the findings file remains (`/tmp/mut.py`, `/tmp/mut361.py`, `/tmp/mutrev`, `/tmp/ll-mut.*` all pre-date the fix). My own mutant runs used a copy under `/tmp/ironclaude-batch.*`, removed by trap. One `/tmp/ironclaude-batch.wQOyul55` (holds `src` and `tests` only, no `base`/`m` as my runs create) was present at the end; it is not mine, so I left it (outside the repo, not repo mutation). |

## One row per blocking finding

| id | Verdict | Evidence (repository files read or mutated by me) |
|---|---|---|
| C-1 | FIXED | `cycle.py:651-659` `_origin_ok(timeout)` no longer reads the deadline. `_launch` (`cycle.py:1039-1045`) tests `launch_allowed()` then `timeout_for(GIT_TIMEOUT_S) is None` and raises `_Skip("budget_exhausted")` before the git call; `origin_mismatch` only after a run call fails. Cycle-start check (`cycle.py:697-703`) raises `gh_timeout` on no time left. Tests `test_cycle.py:4258` (`..._c1_c11`) and siblings. My mutant: cut-off skip changed to `origin_mismatch` -> 3 failed, 2239 passed (killed). |
| C-2 | FIXED | `audit.py:61-64` adds `cycle_complete` ("cycle", 0), marked [PROPOSAL]; `cycle.py:1123-1133` `_cycle_reason` returns it for a clean cycle. `test_cycle.py:2032-2052` `check_line_kinds` is strict again (cycle line: cycle-kind reason with table exit equal to line exit, or an entry reason with exit 7; decision line never a cycle kind). My mutant: `_cycle_reason` fallback back to `not_approved` (run with `-x`) -> 1 failed (killed). |
| C-3 | FIXED | `cli.py:121-129` `except Exception` around `build_deps` and `run_cycle`, `audit.stderr_fallback("cycle_crashed", 1)`, class name only, `sys.exit(1)`; `audit.py:55-57` has the [PROPOSAL] reason. My mutants: catch `ValueError` only -> 2 failed (killed); catch `BaseException` -> 3 failed (killed). (Catching only `RuntimeError`, the exception the test raises, survives; a minor weakness, not blocking.) |
| C-4 | FIXED | `test_cycle.py:2998` and `:3009` build both bodies with `load_fixture("orca_launch_no_operation_id.json")["payload"]` and `load_fixture("orca_launch_empty_operation_id.json")["payload"]`; both fixtures exist under `tests/issue_watch/fixtures/_assumed_shape/`; `test_launch.py:804-823` pins their shape against `OPERATION_ID_PATHS`. Grep for the old inline `"operation_id": ""` in `test_cycle.py`: no match. |
| C-5 | FIXED | `test_slo_helper.py:257` now reads "dry-run lines 13 / 18." (grep for "13 / 20": no match). |
| C-6 | FIXED | `conftest.py:186` `FailingStore`; `test_cycle.py:4363` (pending save fails: no launch, exit 6) and `:4390` (outcome save fails after launch: no relaunch). My mutant: `_save` swallows `OSError` (`cycle.py:585-586` replaced by `pass`) -> `test_a_failed_pending_save_launches_nothing_and_is_exit_6__fr010_nfr005_c6` fails (killed). |
| C-7 | FIXED | `test_cycle.py:4421` (final save fails: exit 6, no cycle line, no health stamp). Test present and green on 3.10 and 3.11; I did not re-run the fix report's mutant M1b. |
| C-8 | FIXED | `test_cycle.py:4447` (`audit.jsonl` unwritable: same exit, one stderr line, store saved). Test present and green; I did not re-run mutant M1c. |
| C-9 | FIXED | `test_cycle.py:4492` (real cycle saves a migrated store) and `:4508` (dry-run never writes). My mutant: drop `not self.dry_run and` at `cycle.py:727` -> 1 failed (killed). |
| C-10 | FIXED | `test_cycle.py:4567` and `:4582` (S1 cases with issues 9 and 10). My mutant: `self.halt = True` replaced by `pass` at `cycle.py:815` -> 1 failed (killed). |
| C-11 | FIXED | `conftest.py` `FakeRunner` fails on a `None` timeout and the `gh_world` teardown asserts each recorded timeout is not None and in bounds; `test_cycle.py:4277` (probe) and `:4308` (literal timeout list of a launch cycle). My mutant: probe None guard disabled (`cycle.py:1018-1019`) -> 1 failed (killed). |
| C-12 | FIXED | `test_cli.py:51` captures `_REAL_BUILD_DEPS` before the autouse patch; `test_cli.py:588` calls it and asserts the assembled deps. My mutant: `which=(lambda n: None)` at `cli.py:72` -> 1 failed (killed). |
| C-13 | FIXED | `test_cycle.py:54` captures `_REAL_READ_MOUNTINFO`; tests at `:4602-4631`. My mutant: `_MOUNTINFO` set to `/proc/self/mountstats` (`cycle.py:77`) -> 1 failed (killed). |

## New blocking findings

None. Notes only (minor, not rechecked later):

- `cycle_complete` and `cycle_crashed` raise the reason table from 57 to 59 names; design text and spec still describe 57. Both are marked [PROPOSAL] for the owner; the design file is outside the change set.
- `cycle_crashed` uses exit 1, the number `status` uses for "unhealthy"; the two commands never share a run, so no clash in one process, but the owner may prefer another code.

## Summary

- Blocking ids: 13 / 13 FIXED, 0 NOT FIXED. Environment checks: 9 / 9 PASS. New blocking issues: 0.
- I ran 11 mutants on a /tmp copy (copy removed by trap, repo never mutated). All were killed except the `RuntimeError`-only catch, noted above.

**Confidence:** Verified: 22 / 22 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (13 finding rows plus 9 environment checks; C-7 and C-8 rest on test presence plus a green suite, not on my own mutant).
**Tool engagement:** Read: 9 | Grep: 5 | Glob: 0 | Bash: 10

## QA Complete
