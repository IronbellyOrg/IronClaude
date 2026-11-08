# QA Report - Gate D, citation-evidence lens

**Topic:** issue-watch Phase 8 (conftest part 5 + seven cross-cutting test files)
**Date:** 2026-11-08
**Phase:** task-integrity / gate review (report only, fix_authorization: false)
**Fix cycle:** 1

**Lens:** citation-evidence (rf-qa, fix_authorization: false, report only; this is the only file written)

## Overall Verdict: FAIL (2 blocking, 10 minor notes)

## Items Reviewed

Sources opened for every check: `docs/designs/issue-watcher.md` (lines 106-124, 200-270, 304-366, 495-540, 535-605, 604-650, 640-700, 697-725, 755-800, 829-849, 866-902), `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (112-172, 205-217), `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/06-gap-fill-decisions.md` (16-85, 150-195), `research/01-cli-package-conventions.md` (99-113), the task file Steps 8.1-8.8 and 8.G3, and the cited repository files.

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Design line anchors in docstrings/comments (693 twice, 8.5, 7.6, 5.3, 9.1, T1/T6/T10/T11, C18) | PASS | `test_security_invariants.py:59-60,171` cite "design line 693": design line 693 holds `random.Random(331)`, 2,000 draws, integers/hostile strings/floats/booleans. `:357` "design 8.5" matches design 640-649 (gh 20 s, probe 10 s, git 10 s, floor 5 s, launch 120 s never shortened). `test_crash_injection.py:4` "design section 7.6" matches design 507-533. `test_module_boundaries.py:3,19,21` "design 5.3", "C18 ... inside save", "types only" match design 229-242 and 99. `test_no_shell.py:1` T6 = design 662; `test_no_text.py:1` T1 = 657, T11 = 667. |
| 2 | DF-nn ids cited (DF-10, 12, 14, 15, 28, 29, 32, 34, 55, 56) | PASS with notes M2, M4 | Each row read in research/06: DF-10 (stubs in tmp_path), DF-12 (seed 331, 2,000 draws, no marker), DF-14 (`$after: String` nullable; `test_security_invariants.py:897`), DF-15 (5 reruns, lock released in finally), DF-28 (`--method GET` rule), DF-29 (ast.walk, function-level import in `save`), DF-32 (`_assumed_shape`), DF-34 (subprocess e2e, multiprocessing lock test), DF-55 (AC-19 split), DF-56 (conftest split by phase). Two attributions are looser than their rows (M2, M4). |
| 3 | FR/NFR/AC/NG ids cited | FAIL (CE-1) | FR-001, FR-003, FR-010, FR-012 (GWT inputs 9, "9", True, 0, -1, 10**9, 9.0 = `EDGE_VALUES` head), FR-013 (12 elements), FR-017, FR-029, NFR-001/002/003/004/005/006/009/010/014 and NG-2 match spec-final lines 121, 145, 151-154, 172, 199, 205-231, 69. AC-1, AC-7, AC-11, AC-20, AC-25 match design 872-898. `test_crash_injection.py:1` cites AC-17, which is "Each verb's exit codes match section 4" (design line 890); the crash criterion is AC-22 (design line 895). |
| 4 | Stub protocol in conftest part 5 vs research/06 Table 1.4, row by row | PASS | Location (`conftest.py:1122-1126`), stub files and shebang/mode (`:973,1129-1135`), interpreter and PATH (`:1136,1140`), scenario JSON, first-match-wins, no-match exit 99 with `stub: unscripted argv` and `matched: false` (`:985-1032`), log header `{call, tool, argc, cwd, matched}` plus one `{call, i, arg}` per argument (`:1003-1013`), `IW_STUB_STATE_DIR` snapshot `{call, dispatch_json}` for orca/orca-ide on `agent launch` (`:1014-1021`), `sleep` key (`:1033`), guard `shutil.which` for all four names (`:1146-1150`), teardown failure on unmatched (`:1152-1155`). The "Orca probe" row is only partly mirrored by the e2e scenario (M6). |
| 5 | Crash recipes vs research/06 Table 1.3 and design 525-531 | PASS | `CrashingStore` (`conftest.py:129-173`): C1 and C4 raise before delegating, C3 and C5 after, no C2 (patched `os.replace` in `test_crash_injection.py:238-279`, once-only, dst endswith `dispatch.json`, orphan tmp asserted; true because `swarm/atomic.py:33` is `except Exception:`). Durable-state assertions and the five reruns (`RERUNS = 5`, `:36,137`) match each Table 1.3 row; at-most-one launch checked after every run (`:117-125,142`). |
| 6 | No Phase 8 file reads `.dev/`, the design, or the spec | PASS | Grep for `.dev/`, `docs/designs`, `spec-final`, `brainstorms`, `research/`, `read_text`, `open(` over the seven test files: the only reads are `src/superclaude/cli/issue_watch/*.py`, tmp_path files, and `/proc/self/mountinfo` (`test_cli_e2e.py:67`). Mentions of `research/06` and the design are docstring text only. |
| 7 | No unverified gh/Orca shape asserted outside `_assumed_shape` fixtures | FAIL (CE-2) | `test_cli_e2e.py:342,409` and `test_security_invariants.py:345` load `orca_launch_success.json`. `test_no_text.py:499-505` writes the Orca launch reply inline (`{"receipt": {"operation_id": "op-ok-1"}, ...}`), contrary to `conftest.py:300-304` and design 636, 847. The probe reply (`test_cli_e2e.py:42`) is allowed: design 842 marks `skills list --json` verified. |
| 8 | Repository file:line anchors cited by the Phase 8 steps | PASS | `swarm/atomic.py:33` is `except Exception:`; `tests/pr_submit/test_conflict_scripts.py:167-179` (private bin dir, chmod 0o755, PATH in `env=`) and `:1555-1571` (symlinked restricted PATH); `tests/swarm/test_parallel_executor_routing.py:343-364` (AST scan) and `:372-406` (mutation guards); `tests/swarm/test_inv012_tui_opt_in.py:130-143` (subprocess with env and timeout); `tests/unit/test_ccsession_tag.py:4496-4518` (flock holder); `pyproject.toml:114,135` and `tests/conftest.py:14` (checked with sed). |
| 9 | Code claims in docstrings (what the package does) | PASS with note M1 | `record.py:372,853,389` confirm function-level `write_prepared_bytes` in `save` and `save_dry_run` and `fcntl` in `lock`; `cli.py:26-27` confirm `from . import audit, cycle, record` and `from .launch import`; `audit.py:159-173,402` confirm `_COMMON`, `_KEYS`, fallback keys; no `except BaseException`/bare `except` in the package (Grep), so `SystemExit` escapes as `test_crash_injection.py:8-10` says. `record.py:23-29` imports four functions and one type, not "three functions and one type" (M1). |
| 10 | Numbers in `gate-d-change-set.md` copied from result files | PASS | `wc -l` reproduces 1155/443/961/373/275/191/961/375; `wc -c` 32824 and 34121; `find tests/issue_watch -type f -perm /111` prints nothing; `p8-g1-summary.md` and `p8-g3-summary.md` give 2616 passed (16.86 s and 6.40 s), `p8-g8.txt` EXIT=1 NO_MATCH, `p8-ruff.txt` check 0 / 31 files formatted / format 0; `test_audit.py:215-219` pins 59 names; the four stale scratch `.pyc` names exist under the gitignored `__pycache__` with no source file. |
| 11 | Gate C ids cited in conftest (C-3, C-6, C-7, C-11) | PASS | `qa/gate-c/qa-consolidated-findings.md` lines 17, 20, 21, 25 name exactly those findings (run-cycle crash handling, `_save`, `_commit`, the None-timeout guard). |
| 12 | Step map (8.1-8.8) vs files | PASS | Task file lines 585-606 match the file names in each docstring ("plan step 8.1/8.2/8.3"). |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| CE-1 | blocking (false claim) | `tests/issue_watch/test_crash_injection.py:1` | Docstring says "(NFR-005, AC-17)". Design section 17 line 890: AC-17 = "Each verb's exit codes match section 4; `check-config` and `status` write nothing" (FR-026, FR-021). The criterion this file implements is AC-22 (design line 895: "Crash points C1 to C5 and 50 cycles never exceed one launch per issue", NFR-005, NFR-010, NFR-011). The traceability claim is false and would send a reader to the wrong criterion. | Change "AC-17" to "AC-22" on line 1. |
| CE-2 | blocking (unverified Orca shape inline; test no longer pins what it names) | `tests/issue_watch/test_no_text.py:494-510` (scenario `launch_ok_with_text_fields`) | The Orca launch-success reply is written inline as `{"receipt": {"operation_id": "op-ok-1"}, "title": SENT, "body": SENT}`. Design 636 and 840 mark the reply shape UNVERIFIED and require it to live in an `_assumed_shape` fixture until FU-1; `conftest.py:300-304` states "never from inline JSON"; every other launch reply in the suite uses `load_fixture("orca_launch_success.json")["payload"]`. The scenario asserts nothing about the entry state, so after FU-1 replaces the fixture and `OPERATION_ID_PATHS` changes, this scenario silently becomes an `unknown` launch and still passes, no longer testing "a launched success that carries text fields". | Build the payload as `{**load_fixture("orca_launch_success.json")["payload"], "title": SENT, "body": SENT}` and assert the cycle's entry for issue 7 is `launched`, so a shape change fails the test instead of weakening it. |

## Minor notes (carried forward, never rechecked)

| # | Location | Note |
|---|----------|------|
| M1 | `test_module_boundaries.py:20-21` | "it imports three functions and one type": `record.py:23-29` imports `format_utc`, `parse_utc`, `valid_issue_number`, `valid_operation_id` (four functions) and `ApprovalResult` (one type). |
| M2 | `test_module_boundaries.py:10-11` | The parenthesis credits DF-29 for "`fcntl` is imported inside a function". DF-29 covers only the `write_prepared_bytes` import; the `fcntl` rule comes from design 6.2 step 1 (a non-Linux host must reach exit 2 `platform_unsupported`) and the `record.py:389` comment. |
| M3 | `test_cli_e2e.py:282` | Test and docstring are named "AC-1 guard" for the PATH-stub guard. AC-1 (design 874) is the FR-001 call order, which `test_fr010_fr013_...` covers; the guard is the DF-10 / Table 1.4 guard. |
| M4 | `test_concurrency.py:12,215-244` | "(decision DF-34)" is attached to the single-process lock cases, but DF-34 decides the multiprocessing mechanism and the e2e invocation. The missing-lock and directory-lock tests carry `ac11`, yet AC-11 (design 884) names only the second process and a symlinked or foreign lock; missing lock is FR-017 and the directory case is design 7.6 step 1. |
| M5 | `test_crash_injection.py:4`, `test_module_boundaries.py:216` | "research/06 Table 1.3" and "research F6" give no path. They resolve (research/06 Table 1.3 exists; research/01 F6 says the walker must resolve `ImportFrom.level >= 1`), but a reader needs the `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/research/` prefix. |
| M6 | `test_cli_e2e.py:172-177` | Table 1.4 "Orca probe" says both the `orca` and `orca-ide` scenarios answer `skills list --json`; `Watcher.script` registers only `orca-ide`. Harmless because `orca-ide` resolves first and the unmatched-argv teardown guard would fail any `orca` call. |
| M7 | `test_no_text.py:13-15` | "Every scenario proves the canary was served": true for the table-driven scenarios (`:530`), not for `test_a_crash_inside_a_gh_call...`, `test_a_build_deps_failure...` and `test_a_damaged_store...`, where the canary enters through an exception message or a file. |
| M8 | Step 8.4 and 8.5 text vs files (outside this lens) | Step 8.4 asks for one parametrized test per crash point; the file has separate tests per point. Step 8.5 asks for polls of at most 10 s; `test_concurrency.py:43-44` uses 30 s and 60 s. Both are bounded, so nothing hangs; passed to the test-adequacy lens. |
| M9 | Task file Step 8.7 (not a Phase 8 file) | Cites design "line 663" for the no-text control; line 663 is T7 (host and login on every line), the T11 stderr control is line 667. |
| M10 | `tests/issue_watch/__pycache__/` | Stale bytecode for four deleted scratch tests (already disclosed in the change set); gitignored, no source file, harmless. |

## Summary
- Checks passed: 10 / 12 (check 9 carries only minor note M1 and counts as a pass with notes)
- Checks failed: 2 (checks 3 and 7: CE-1 and CE-2, both blocking)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false; no file other than this report was written)

## Actions Taken
None besides this report. Experiments: none needed; all checks were reads and read-only greps/`wc`/`find`.

## Recommendations
- Fix CE-1 (one token) and CE-2 (build the payload from the fixture and assert `launched`) before Gate D closes. Minor notes M1 to M10 are carried forward and are not rechecked.

## Confidence
**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: ~47 | Grep: ~33 | Glob: 0 | Bash: 2 (one read-only batch of `wc`, `find`, `cat`, `grep`, `sed`; one read-only `find`/`ls`/`git status`/`sed` batch). No web research performed (no Tavily or fallback calls).

## QA Complete
