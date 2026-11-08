# QA Report - Gate C, lens citation-evidence

**Topic:** issue-watch implementation, Phases 6 and 7 (cycle.py, cli.py, main.py edit, conftest part 4, test_cycle.py, test_slo_helper.py, test_cli.py)
**Date:** 2026-11-08
**Phase:** task-integrity / citation-evidence (report only, fix_authorization: false)
**Fix cycle:** N/A

## Overall Verdict: FAIL (2 blocking findings: CE-1, CE-2; 11 minor notes)

Scope read in full or in the citation-bearing parts: `gate-c-change-set.md`; `cli.py` (339 lines); `cycle.py` (1350 lines); `conftest.py` part 4 (lines 237-889); `test_slo_helper.py` (416); `test_cli.py` (lines 1-340, 565-700, 837-1000, 1300-1443 plus a grep of every comment and docstring); `test_cycle.py` (header, every comment line, every test name carrying an id tag, and the bodies around lines 1040-1270, 1655-1730, 1876-1980, 2010-2270, 2878-3010, 3310-3520, 3925-4153); the new fixture `gh_issue_reread.json` and three sibling fixtures. Sources opened: `docs/designs/issue-watcher.md` (lines 62-166, 168-390, 451-650, 695-830, 868-899), `spec-final.md` (96-106, 109-201, 213-229, 322-363), `research/06-gap-fill-decisions.md` (DF-01 to DF-59), the Open Questions of the task file (section D, E, G), `qa/gate-a|gate-b/qa-fix-report*.md`, the p6/p7 result files, `git diff HEAD -- src/superclaude/cli/main.py`, `git show HEAD:src/superclaude/cli/main.py`.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Registry edit is exactly the import line with its noqa suffix plus the add_command line after the reflect pair, nothing else | PASS | `git diff HEAD -- src/superclaude/cli/main.py`: 4 added lines only (blank, `from superclaude.cli.issue_watch.cli import issue_watch_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports`, blank, `main.add_command(issue_watch_group, name="issue-watch")`), 4 insertions, 0 deletions; the text equals DF-29 and Step 7.3 byte for byte; two blank lines still precede `if __name__`; anchors 555/557/559/561/564 confirmed with `git show HEAD:...main.py` |
| 2 | The change-set main.py diff is verbatim | PASS | Same hunk header `@@ -560,6 +560,10 @@` and index `ffe4a34d..74ffc1a9` as the live `git diff` |
| 3 | No text repeats the false claim that the package is imported lazily | PASS | Grep `lazy|lazily|defer|on demand` over `src/superclaude/cli/issue_watch/*.py`, `tests/issue_watch/*.py`, `main.py`: only `test_record.py:666` (true: `record.save` imports `swarm.atomic` inside the function, `record.py:370`) and the DF-29-mandated noqa comment, which says "deferred subcommand registration", the same words as its neighbours; task line 988 states the claim is not repeated |
| 4 | No text repeats the false `tests/cli_portify/test_cli.py` collision claim | PASS | Grep `cli_portify|collid|collision|basename`: no hit in the change set (only `main.py:535-537`, pre-existing); `tests/issue_watch/__init__.py` is 0 bytes with no docstring |
| 5 | No model-alias string in any file | PASS | Grep `opus|sonnet|haiku|fable|claude-[0-9]|gpt|gemini|o1/o3/o4-mini` and `claude-gw|tier[0-9]` over `src/superclaude/cli/issue_watch/**` and `tests/issue_watch/**` (py and json): only `SuperClaude-Org` negative fixtures in `test_github.py:350`, `test_launch.py:448-449` (Gate A and B files) and the agent id `"claude"` (`test_cli.py:221`, DF-11, not an alias) |
| 6 | No gh or Orca reply shape the design marks unverified is stated as fact outside an `_assumed_shape` fixture | FAIL | CE-1 |
| 7 | Every design section cited in cycle.py/cli.py/tests exists and says what is claimed | PASS with notes | 4.1, 4.2, 4.3, 5.2, 5.4, 6.2 "Stop", 8.5, 10.2, 10.3, 14 opened and matched; mismatches only M-1, M-2, M-5 (true claims, imprecise section) |
| 8 | Every DF id cited exists and supports the claim | PASS with notes | Unique ids found: DF-03, 04, 06, 13, 15, 17, 20, 22, 23, 32, 35, 39, 41, 43, 45, 47, 50, 51, 52, 53, 55, 57 (plus test-name tags df02); all exist in `06-gap-fill-decisions.md`; supporting text confirmed for all except the points in M-4, M-8 |
| 9 | Every FR/NFR/AC/PF/OD/T-/S1/C22 id cited exists and matches | PASS with notes | FR-001/002/003/004/009/010/011/014/016/018/019/020/022/023/024/025/027/028/029, NFR-005/007/009/010/013, AC-5/14/19/24, PF-008, OD-10 (design line 166), T-10/T-11/T-12 (design 7.4), S1 (design line 104), C22, R10: all resolved; mis-tagged test names are M-7 |
| 10 | OQ ids cited resolve | PASS with notes | OQ-36, OQ-39, OQ-50 are defined in task file Open Questions section D (lines 951, 954, 961) and the code matches each; they resolve only inside the task folder (M-10); `(OQ)` at `cycle.py:1115` has no id (M-6) |
| 11 | Section-10.2 `status` fields, 900 s, 24 h, exit 1 follow the design | PASS | `test_cli.py:630-639` field set equals design 10.2 lines 732-739; `HEALTH_AGE_S=900`, `STALE_AGE_S=86400` match design 14 line 824 |
| 12 | Section-14 constants match | PASS | MAX_CANDIDATES 10, DAY_CAP 6, GH 20, PROBE 10, GIT 10, LAUNCH 120, DEADLINE 240, floor 5, cutoff 120, SKEW 60, DISCOVERY_WARN 80, health 900, stale 86400 against design lines 809-826 and spec FR-003/FR-016/FR-029 |
| 13 | Hand-worked numbers in test comments are right | FAIL | CE-2; all other numbers checked (7/10, 10/23, 16/19, ceil ranks, 14,460 s, 28/32/35, 23.5 h, 79/80, 60/61, 236/121/120) are right |
| 14 | Design-named tests exist under the design's names | PASS | `test_fifty_cycles` (`test_cycle.py:3974`) and `test_acceptance_property` (`:4019`, N in 1, 2, 6, 7, 50, 99) match design 12 lines 786-787 |
| 15 | New fixture `gh_issue_reread.json` is labelled and sourced | PASS | `_assumed_shape: true`; `source` names design 8.1 G7 (line 549) and flags the lower-case state value UNVERIFIED; fixture pin 17 at `test_github.py:578`; read by name at `test_github.py:1668` |
| 16 | Sibling fixture source anchors (design section 15 lines 834, 835, 838, 840-841) | PASS | Design lines 834 (`gh issue list`), 835 (`gh api user --include`), 838 (stderr substrings), 840-841 (`orca agent launch` reply, `agent_session_operation_unknown`) read at `docs/designs/issue-watcher.md` |
| 17 | Change-set file list and counts | PASS | Source 9 files, tests 14 `.py`, fixtures 17 `.json` (Glob); line counts 1350/889/4153/416/339/569/1443 equal `wc -l`; stale `__pycache__/*.pyc` for scratch tests have no `.py` source |
| 18 | Change-set gate rows equal the result files | PASS | G-1 2098 passed 7.68 s; G-2 2224 passed 1 skipped 10.37 s with the skip at `tests/swarm/test_cli_registration.py:127` (`p7-g2-raw.txt:2237`); G-4 0 errors 5 warnings (`p7-g4-raw.txt:155-157`, none in issue_watch); G-9 five commands; ruff rows as recorded |
| 19 | Change-set Gate A/B fix lists equal the fix reports | PASS | A-1..A-18 files and fixtures, A-7 cycle 2 (686 passed), B-1..B-13 files, 1577 passed, cycle 2 "skipped: cycle 2 not selected" |
| 20 | Phase 6 ruff row (4 files named, "5 files already formatted") | UNVERIFIABLE | `p6-ruff.txt` holds tool output only and does not name its files; Step 6.11 names 4; belongs to the gate-command-reproduction lens |
| 21 | Step references ("plan step 6.4 to 6.9", "Part 1/2") | PASS | Task headings lines 458-482 and 497-509 |
| 22 | Click behaviour claim in `test_cli.py:9-12` | PASS | Click 8.1 `mix_stderr=True` default and Click 8.2 interleaved `output` are the documented behaviours; installed Click 8.5.1 runs the tests |
| 23 | Caller/callee liveness for cited collaborators | PASS | `find_orca(..., which=, timeout=)` (`launch.py:163-168`), `retry_argv` (`launch.py:119`), `FileStore.migrated` (`record.py:345,367`), `DryRunDoc`/`load_dry_run`/`save_dry_run`, `OPERATION_ID_PATHS` (`launch.py:42-45`) all exist and are used |
| 24 | Counterfactual numbers in `test_slo_helper.py:340` and `test_cycle.py` | PASS | Recomputed by hand: p95 9000, share 1 / 2, claimed 2 / 2 are right |

## Summary
- Checks passed: 21 / 24 (items 7, 8, 9, 10 pass with minor notes); failed: 2 (items 6 and 13); unverifiable: 1 (item 20, a pass-through to the gate-command-reproduction lens).
- Blocking findings: 2 (CE-1, CE-2). Critical issues: 0. Minor notes: 11 (M-1 to M-11).
- Issues fixed in place: 0 (fix_authorization: false; only this report was written).

## Issues Found

### Blocking

| id | Severity | File and lines | Evidence | Expected versus actual |
|---|---|---|---|---|
| CE-1 | blocking (missing required deliverable: design-mandated fixture rule; same defect Gate B graded blocking as B-2) | `tests/issue_watch/test_cycle.py:2956-2974` (`_UNKNOWN_OUTCOMES`, params `no_operation_id` and `empty_operation_id`) | The cases build Orca launch replies inline: `json.dumps({"outcome": {"kind": "launched"}})` (line 2963) and `json.dumps({"receipt": {"operation_id": ""}})` (line 2970). Design 8.4 line 636 and section 15 lines 840-841 mark `outcome.kind`, `receipt.detail` and the operation-id path UNVERIFIED and send them to an `_assumed_shape` fixture; `orca_launch_success.json` `note` says the id path is a proposal. `conftest.py:240-244` states the rule for this very phase ("Every gh or Orca reply whose shape is unverified is built from an `_assumed_shape` fixture ... never from inline JSON") and names only two exceptions (probe reply, `git remote get-url`). Gate B finding B-2 (`qa/gate-b/qa-consolidated-findings.md:14`) blocked the same pattern in `test_launch.py` and was fixed by deriving the bodies from `orca_launch_success.json` at `launch.OPERATION_ID_PATHS[0]` (`qa/gate-b/qa-fix-report.md:12`). The Phase 6 task-log judgment call (5) (task file line 1023) lists only the two conftest exceptions, so these two inline bodies are also undisclosed | Expected: both bodies start from `load_fixture("orca_launch_success.json")["payload"]` and delete or blank the id at `OPERATION_ID_PATHS[0]` (or reuse the helpers `_success_payload`, `_id_holder`, `_no_id_reply` of `test_launch.py`). Actual: two literals that keep passing for the wrong reason after FU-1 changes the id path (any body without an id at the new path is also `unknown`) |
| CE-2 | blocking (false claim in the evidence comment of a test whose docstring promises hand-worked numbers) | `tests/issue_watch/test_slo_helper.py:256-257` (module docstring lines 4-7 promise "Every expected number is a literal worked out by hand in the comment beside the fixture") | The comment says: "Counting the old lines would give 10 / 23, the disabled and not_enabled lines 16 / 19, the dry-run lines 13 / 20." Recomputed by running `_cycle_lines()` through the reducer rules: counted 7 / 10; plus the 13 old lines 10 / 23 (right); plus 9 disabled and not_enabled lines 16 / 19 (right); plus the 8 dry-run lines (6 exit-0 and 2 exit-3, lines 177-180) 13 / 18, not 13 / 20 (script output: `counted (7, 10) old (10, 23) disabled (16, 19) dry (13, 18)`) | Expected: "13 / 18". Actual: "13 / 20". The assertion `== 0.7` itself is right and still discriminates (13 / 18 = 0.72), so no behaviour is wrong; the stated working is wrong |

### Minor notes (never fail the gate, not rechecked)

| id | File and lines | Note |
|---|---|---|
| M-1 | `cli.py:216` | `_save` docstring says a failed write is `state_dir_unwritable` "(design 7.6)". Design 7.6 (lines 507-533) never names that reason; it is at design 4.2 line 137, 4.3 line 162, 6.2 step 13 line 356, 10.1 line 722. Claim true, section wrong |
| M-2 | `cli.py:33-37` | "Exit codes of design 4.3 that this module returns itself" but `_EXIT_UNHEALTHY = 1` is not in the 4.3 table (lines 155-164); it is defined at design 4.1 lines 115 and 121 and 10.2 line 726 |
| M-3 | `cli.py:118` | The `once` docstring ends "(design 4.3)" and is printed in operator help (`p7-g9.txt`: "Run one poll cycle and exit with its code (design 4.3)."). An internal document number in `--help`; `docs/designs/` is not installed with the package |
| M-4 | `cycle.py:134`, `test_cycle.py:253`, `github.py:150-160` | Comment "DF-20: ... a leading dash reads as a flag". DF-20 (register line 147) covers only the comma and the quote; the leading-dash rule has no recorded source in the design, spec, register or task Open Questions |
| M-5 | `cycle.py:49` | `NETWORK_FS_TYPES` cites "design 4.2, DF-53". The list is in design 2.4 line 69 and DF-23; 4.2 line 137 only says "deny-listed" and DF-53 extends the check to `init-state` |
| M-6 | `cycle.py:1115`, `test_cycle.py:2025-2030` | "(OQ)" names no id, and the test docstring calls the clean-cycle reason rule "by design in cycle.py". No design, spec or DF row defines it; it exists only as Phase 6 task-log judgment call (1) "departs from the literal reading of DF-41". It is disclosed for Gate C but has no Open Question id |
| M-7 | `test_cycle.py:806-857` (12 tests `test_resolve_exit_*__fr028`), `:563,:569` (`check_platform` tests `__fr027`), `:755-791` (`validate_setup` tests `__fr027`) | Wrong id tags. The precedence source is OD-10 (design line 166), design 4.3, spec section 8 and AC-15; FR-028 is the rate-limit requirement. FR-027 (spec line 193) has no platform rule and no worktree-existence rule (FR-001, FR-013, design 4.2 `worktree` row). The section comment at `test_cycle.py:799` cites correctly |
| M-8 | `conftest.py:241` | "(decision DF-32)" for the rule "built from an `_assumed_shape` fixture, never from inline JSON". DF-32 (register line 159) is about the pre-commit-only hooks and the fixture JSON parse test; the rule comes from design 8.1/15, spec NFR-005 and DF-49 |
| M-9 | `conftest.py:548` and `:826-831` | `GhWorld.issue` hard-codes the discovery state `"OPEN"` and `_reread_payload` forces `state="open"`, the very "lower-case state value" `gh_issue_reread.json` flags UNVERIFIED, instead of reading the fixture value. `cycle.py:959` lowers the value, so the impact is small |
| M-10 | `cycle.py:908,1002,1207,1228`, `cli.py:3-6`, test docstrings ("plan step 6.x", DF-nn, OQ-nn) | These ids resolve only inside `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/` (OQ ids exist only in the task file) and will not resolve once the folder moves to `.dev/tasks/done/`. House style in Gate A and B files, so a note only |
| M-11 | `phase-outputs/test-results/p6-ruff.txt`, change set row "G-5 Phase 6" | Result file records "5 files already formatted" against 4 files named in Step 6.11 (task line 489) and does not record the command. Acknowledged in the change set; outside this lens (gate-command-reproduction) |

## Actions Taken
None. fix_authorization was false; the only file written is this report. Temporary helper `/tmp/qa_gatec_slo_check.py` (read-only recomputation) was deleted after use.

## Recommendations
- CE-1: replace the two inline bodies in `test_cycle.py:2961-2974` with bodies derived from `orca_launch_success.json` (copy the `_id_holder` approach of `test_launch.py`), and add the two bodies to the Phase 6 log note if the owner wants them disclosed.
- CE-2: change "13 / 20" to "13 / 18" at `test_slo_helper.py:257`.
- Minor notes M-1 to M-11 need no action before Gate D.

## Confidence
Verified: 23/23 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0% (24 checklist items, item 20 unverifiable; the two FAIL items are verified failures, not unchecked items)

**Tool engagement:** Read: 38 | Grep: 15 | Glob: 1 | Bash: 27 (counts from this session; Bash was used for `git diff/show`, `wc -l`, section extraction with `sed`, one read-only recomputation script and result-file inspection). No web research was performed, so no Tavily or fallback calls. Read+Grep+Glob (54) is above the 24 checklist items.

## QA Complete
