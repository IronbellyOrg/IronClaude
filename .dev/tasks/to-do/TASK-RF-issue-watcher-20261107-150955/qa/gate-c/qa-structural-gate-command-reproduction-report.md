# QA Report: Gate C, lens "gate-command-reproduction" (Phases 6 and 7)

**Topic:** issue-watch implementation (cycle and cli modules, registry edit, conftest part 4, three test files)
**Date:** 2026-11-08
**Phase:** task-integrity / gate verification (report only, `fix_authorization: false`)
**Fix cycle:** N/A (first review of Gate C for this lens)

---

## Overall Verdict: PASS (0 blocking findings, 5 minor notes)

I re-ran every command from the repository root and compared each result with the recorded files. Every command exits 0 and every recorded result is reproduced, with the explanations given below for the two count differences. I found no skip, xfail or warning other than the one allowed skip. I found no blocking defect.

I could not find 15 errors in this lens. I looked for them by running each command, comparing counts per test file and checking the scope of each ruff run. The remaining issues are the minor notes at the end.

## Commands re-run

| # | Command (from repo root) | Exit | Result now | Recorded | Match |
|---|---|---|---|---|---|
| 1 | `uv run pytest tests/issue_watch/ -v` | 0 | `2194 passed in 8.45s`, no skip, no xfail, no warnings section | p6-g1: `2098 passed in 7.68s` | Count differs by 96; explained below (N-1) |
| 2 | `uv run pytest tests/issue_watch/ tests/skills/test_model_alias_policy.py tests/docs/test_retired_docs_absent.py tests/cli/test_cli_registration.py tests/swarm/test_cli_registration.py tests/recommend/test_cli_registration.py -v -rs` | 0 | `2224 passed, 1 skipped in 10.32s`; the one skip is `tests/swarm/test_cli_registration.py:127` "got empty parameter set for (subcommand)" | p7-g2: `2224 passed, 1 skipped` | Match |
| 2b | Same selection exactly as written in the lens prompt (`-v`, no `-rs`) | 0 | `2224 passed, 1 skipped in 10.60s` | p7-g2 | Match |
| 3 | `make lint` | 0 | architecture policy: 0 errors, 5 warnings; `ruff check .` All checks passed | p7-g4: same (0 errors, 5 warnings) | Match |
| 4 | `uv run superclaude issue-watch --help` | 0 | Commands block lists exactly `check-config`, `init-state`, `once`, `reset`, `status` | p7-g9: identical text | Match |
| 5 | `uvx --offline ruff@0.15.20 check` on the 7 Python files of the change set | 0 | `All checks passed!` | p6-ruff and p7-ruff: check 0 | Match |
| 6 | `uvx --offline ruff@0.15.20 format --check` on the same 7 files | 0 | `7 files already formatted` | p6-ruff `5 files`, p7-ruff `3 files` | Match for p7; p6 see N-2 |
| 7 | Same two ruff commands on the whole `src/superclaude/cli/issue_watch` and `tests/issue_watch` trees | 0, 0 | `All checks passed!`, `23 files already formatted` | n/a (wider than recorded) | Clean |
| 8 | Same format check on exactly the 4 Phase 6 files, and on exactly the 3 Phase 7 files | 0, 0 | `4 files already formatted`, `3 files already formatted` | p6-ruff `5 files`, p7-ruff `3 files` | p7 match, p6 see N-2 |
| 9 | `uv run pytest tests/issue_watch/ -q -W error` (extra probe: any warning becomes an error) | 0 | `2194 passed in 8.42s` | n/a | Clean, so no latent warning |
| 10 | `uv run superclaude --help` | 0 | lists `issue-watch    Poll GitHub for approved issues and start one Orca claim...` | Step 7.3 requirement | Match |
| 11 | `uv run pytest tests/issue_watch/test_cli.py tests/cli_portify/test_cli.py --collect-only -q` (extra probe: same-basename collision) | 0 | `119 tests collected`, no collection error | n/a | No collision |

## Detail checks

| Check | Evidence | Result |
|---|---|---|
| Help lists exactly five commands | `/tmp/gc-help.txt` from this run and `p7-g9.txt` both show only `check-config`, `init-state`, `once`, `reset`, `status` | PASS |
| No skip or xfail inside the change set | Grep of the run-1 output for `SKIPPED`, `XFAIL`, `XPASS`, `xfailed`, `deselected`, `warnings summary`: no match. Run 2 output: the single line `SKIPPED [1] tests/swarm/test_cli_registration.py:127` | PASS |
| No collection warning | Run 1 and run 2 outputs contain no `PytestCollection` or `PytestUnknown` text; `-W error` run passes | PASS |
| Per-file test counts equal recorded counts | Now vs p6-g1-raw: audit 178, cycle 499, find_orca_parity 76, github 403, launch 168, marker_contract 3, origin_parity 38, predicates 108, record 587, runner 17, slo_helper 21 are identical. `test_cli.py` adds 96 (not in p6). | PASS |
| p7-g2 per-file counts equal now | The 17 file counts of the run-2 output equal the counts in `p7-g2-raw.txt` (cli 6, docs 2, recommend 3, skills 13, swarm 7 plus the issue_watch counts above) | PASS |
| Arithmetic | 2098 + 96 (`test_cli.py`) = 2194; 2194 + 30 passed from the five other selections (6+2+3+13+7 = 31 collected, 1 skipped) = 2224 | PASS |
| `make lint` warnings are outside issue_watch | The 5 warning lines (lint output lines 57-61) name `brainstorm.md`, `reflect.md`, `spawn.md`, `spec-panel.md`, `troubleshoot.md` (command-file length), none under `issue_watch` | PASS |
| Change-set line counts | `wc -l` now: cycle.py 1350, cli.py 339, main.py 569, conftest.py 889, test_cycle.py 4153, test_slo_helper.py 416, test_cli.py 1443, identical to the table in `gate-c-change-set.md` | PASS |
| main.py diff verbatim | `git diff -- src/superclaude/cli/main.py` now equals the diff block in the change set (index `ffe4a34d..74ffc1a9`, 4 added lines at line 560 onward) | PASS |
| File lists | `ls` shows 9 source files in `src/superclaude/cli/issue_watch/`, 14 Python test files, 17 JSON fixtures in `_assumed_shape/`, as the change set states | PASS |
| `.claude/` absent from the change set | Grep count of `.claude/` in `gate-c-change-set.md`: 0 | PASS |
| Real HOME untouched by tests | `~/.config/superclaude/` does not exist; `~/.local/state/superclaude` holds only `codegraph-init.log` | PASS |
| Recorded commands vs task step text | Step 7.7 text has no `-rs`, `p7-g2` ran with `-rs` and says so; run 2b without `-rs` gives the same result | PASS |

## Findings (blocking)

| id | severity | command or file | evidence | expected versus actual |
|---|---|---|---|---|
| none | | | | |

## Minor notes (do not fail the gate)

| id | command or file | note |
|---|---|---|
| N-1 | `phase-outputs/test-results/p6-g1-summary.md` and `gate-c-change-set.md` | The recorded G-1 count (2098) differs from the current count of the same command (2194). The 96 extra tests are `tests/issue_watch/test_cli.py`, added in Phase 7. The change set says that Phase 7 G-1 is "same run as G-2" but does not state that G-1 now collects 2194 tests. A reader who re-runs G-1 sees a number that is not in any result file. No action needed to pass. |
| N-2 | `phase-outputs/test-results/p6-ruff.txt` | The file reports `5 files already formatted` for a step that names 4 files. Re-running on exactly the 4 named files gives `4 files already formatted`. The fifth file is not named, so that recorded count cannot be reproduced from the stated command. The change set discloses this. Whole-tree ruff check and format check now pass on all 23 files, so no code defect hides behind it. |
| N-3 | `phase-outputs/test-results/gate-b-postfix.txt` (1577 passed, quoted in the change set) | The other 9 test files now sum to 1578. The one-test difference comes from `tests/issue_watch/test_github.py` reading the new fixture `gh_issue_reread.json` (Phase 6 pinned the fixtures at 17). This is historic, outside the commands of this lens, and explained. |
| N-4 | Recorded command text | Step 7.7 omits `-rs`; the run used it. The change set discloses it; selection is unchanged. |
| N-5 | `git status` | `src/superclaude/cli/issue_watch/`, `tests/issue_watch/` and `docs/designs/issue-watcher.md` are untracked (not staged), and `.dev/tasks/to-do/.../phase-outputs/` and `qa/gate-a|b|c/` are untracked. The project rule says `.dev/tasks/` is always staged. This is not a command-reproduction defect and I changed nothing. The orchestrator should stage it with `git add .dev/tasks` when it commits. |

## Summary

- Commands re-run: 11 (all exit 0)
- Recorded results reproduced: p6-g1 (with N-1), p6-ruff (check; format with N-2), p7-g9, p7-g2, p7-g4, p7-ruff
- Blocking findings: 0
- Minor notes: 5
- Files modified by this agent: this report only. The test and lint runs created ordinary `__pycache__` and pytest cache files, which the commands create themselves.

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (checklist = the 11 command rows plus the 6 recorded result files)
**Tool engagement:** Read: 9 | Grep: 6 | Glob: 1 | Bash: 8

## QA Complete
