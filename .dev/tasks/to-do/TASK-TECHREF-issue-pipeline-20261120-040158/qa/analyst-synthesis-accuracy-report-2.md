# Synthesis Accuracy and Source-Tracing Report (Partition 2 of 2)

**Analysis type:** synthesis-accuracy + source-tracing
**Partition:** 2 (synth-04, synth-05, synth-06)
**Date:** 2026-11-20
**Status:** Complete (see the final `Status: Complete` line)

---

## Working notes (written incrementally; final tables follow below once all files are analysed)

Method: read synth-04, synth-05, synth-06 in full; re-read live snapshot lines (/home/coder/.cache/ic-snap-20261120/master, read-only) for constants, argv, exit codes, line counts, test counts and test-function line numbers; re-read the removed tree only through `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>` / `git ls-tree`; grepped research files for supporting rows.

Progress log:
- synth-05 Appendix A: all 48 per-file line counts and `def test_` counts re-counted against the snapshot: every one matches (the 44 research-notes EXISTING_FILES test files + 4 added).
- synth-04 5.3 level grid, approval regex, IMPL list, G2 rule 2, GOVERNED_TOOLS (23), block-word count (18): re-read in launch-level-guard.sh and orca_worktree.py: match.
- synth-06 Appendix B: removal commit 01e7a9e23 (PR 682, 2026-11-19 18:02:35 -0600), 10 files 1,597 lines, 10 test files 116 tests 2,391 lines, old WORKER-CONTRACT 350 lines, WC-17 old :59, duties old :291-300, old guard case old :444, old cli.py verb lines: re-read via git show, all match.
- Candidate BLOCKING (scope rule (i)): citations of docs/designs/orchestrator.md. See findings table.

## Claim-tracing table (synth-04)

Legend: research files R01..R06 are in `research/`; snapshot = /home/coder/.cache/ic-snap-20261120/master (all line numbers re-read live); GL = gaps-and-questions.md.

| ID | Synth file and location | Claim | Research support | MATCH/DRIFT/UNTRACEABLE |
|---|---|---|---|---|
| C-01 | synth-04 5.2 status table, IR-7 row | `IR7_REFUSE = False` at orca_worktree.py:822, refusal branch :1757-1758, pinned by test_issue_l2_install.py:639 | R04:208; R05; snapshot lines 822 and 1757-1758 read; test at :639-640 read | MATCH |
| C-02 | synth-04 5.2 orca_worktree.py launch order step 7 | launch argv is `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`, no --model/--effort/link flag, OW:1776-1793 | R04:237; snapshot :1776-1793 read | MATCH |
| C-03 | synth-04 5.2 launch order step 4 | IR-4 checks guard registered on UserPromptSubmit and on PreToolUse for all 23 GOVERNED_TOOLS (OW:841-867) | R04:209; tuple counted: 14 names + 9 mcp names = 23 | MATCH |
| C-04 | synth-04 5.2 subcommands table | `pending --level worktree|full|full-submit` prints `{"ok": true, "nonce": ...}`, OW:1515-1523, :1886-1893, no production caller | R04 section 8.7; R05; snapshot read (it also prints `level`; ellipsis covers it) | MATCH |
| C-05 | synth-04 5.2 tiers table | t3 `claude-gw-tier2b` + `effort: low` line 7, t2 `claude-gw-tier2`, t1 `claude-gw-tier1b`, tools on line 5, model line 6, 35 lines each | R04 Gap-fill c1 B-2 erratum; frontmatter of the three agent files and `wc -l` read | MATCH |
| C-06 | synth-04 5.2 Key Files | templates/ holds 15 files; claim-comment.md 23 lines, accuracy-check-comment.md 20, launch-prompt.md 34 with blocks at :11, :20, :25, :28 | R04:170 (Glob 15); snapshot `ls`/`wc -l`/grep read | MATCH |
| C-07 | synth-04 5.2 default-level rule | prose rule at claim.md:81 (bug full; simple/medium feature <=16 h full; complex or >16 h worktree; unreadable gives worktree; `Level:` line forms) | R04; claim.md:81 read in full | MATCH |
| C-08 | synth-04 5.2 STOP codes | E-CREATE-ONLY-FLAG / E-CLAIM-ONLY-FLAG / E-SUBMIT-NEEDS-FULL at issue.md:53,57,59; origin_repo exit 1/3/4; E-GH-AUTH, E-ORCA-REQUIRED at claim.md:16,17 | R04; issue.md:50-59 and claim.md:15-17 read | MATCH |
| C-09 | synth-04 5.2 tiers (X-23) | tiers.md heading `E-TIER-UNAVAILABLE (default D4)` appears twice (:32 and :44); fallback text :34-42; issue 488 decision :17 | R04:80, :403; tiers.md read in full | MATCH |
| C-10 | synth-04 5.3 level matrix | IMPL blocks at W only; COMMIT/PUSH/SUBMIT/SKILL block at W, WA, F and allow at FS; 10 classes block at every level; unmatched cell is LL-BROKEN (GD:783-803) | R05:328 and matrix; guard lines 783-808 read | MATCH |
| C-11 | synth-04 5.3 typed approval | regex `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` at GD:347; no `sc:task` in the guard (0 grep hits); launch-prompt.md:23 names `/sc:task` | R04:318, :404; snapshot guard grep count 0, launch-prompt.md:23 read | MATCH |
| C-12 | synth-04 5.3 classifiers | Skill name normalisation and `implement | task | cleanup` IMPL at GD:398-413 (line :409), `pr-submit` SUBMIT, `issue` ESCAPE | R05:58; snapshot read | MATCH |
| C-13 | synth-04 5.3 G2 rule 2 | allow-list of orca verbs GD:480-491; rule at GD:496-537, 8192 bytes, 64 args, `--to/--run/--environment/--pairing-code` prefix rule | R05; snapshot lines 452-537 read | MATCH |
| C-14 | synth-04 5.3 registrations | guard on UserPromptSubmit HJ:63-71 and PreToolUse HJ:115-124 with the exact matcher, identity hook on Bash HJ:125-134, timeout 5 each | R05 section 4; hooks.json read (lines 60-136) | MATCH |
| C-15 | synth-04 5.3 plugin hooks.json | plugin copy 154 lines, lacks ccsession-tag entries and pragmatic-subagent.js, `async: true` on freshness-subagent-start.sh | R05:167; plugin hooks.json lines 125-154 and src lines 155-192 read | MATCH |
| C-16 | synth-04 5.3 installer | install_hooks scripts listed at install_hooks.py:90, :93, :96; skip-if-exists unless force :282-289; callers main.py:219 (force flag) and :412 (force=True) | R05; install_hooks.py lines 86-98, 280-290 and main.py grep read | MATCH |
| C-17 | synth-04 5.4 rules | WC-2..WC-16 = 15 rules, no WC-1/WC-17; line numbers 31, 32, 40, 46, 47, 53-58, 59, 60, 61-64, 72, 287-289; 339 lines; section headings :9, :27, :49, :68, :299 | R06 A1; contract grep/sed read | MATCH |
| C-18 | synth-04 5.4 issue-related lines | l.23 never-as-worker list includes /sc:issue; l.57 "grant row" once; l.66 "Messages carry no `--to`"; l.243 progress posts; l.258 and l.289 | R06; sed of lines 66, 242-245, 258, 289 read | MATCH |
| C-19 | synth-04 5.3 ledger | G2 rule 1 / route A REMOVED; 0 hits for `release-worker`; comment at GD:496-497; only `.ok` writer left GD:358 | R05:363, :448; snapshot grep and guard lines 496-497, 358 read | MATCH |
| C-20 | synth-04 5.3 L2 hook | PP exits 0 at once for an ordinary actor (:188), protected refs main/master (:17), `L2-PROTECTED`/`L2-UNKNOWN` exit 1, `L2-MALFORMED` exit 2 | R05; pre-push lines 1-12, 17, 185-208 read | MATCH |
| C-21 | synth-04 5.3 ID hook | `exec uv run --no-project python -I` at :582; stderr texts `launch job: governed Bash call cannot be wrapped safely` (:501), `UV is required` (:52), `invalid invocation or unavailable private state` (:579) | R05; snapshot lines read | MATCH |
| C-22 | synth-04 5.3 test pins | test_grid_policy :3394, test_grid_complete :3401, test_grid_level_steps :3457, test_precedence_order :4520, test_design_table_holds_all_eighteen_ids :1712, EXPECTED :806, test_apr_* :3737/:3800/:3852 | R05:328-; snapshot grep read | MATCH |
| C-23 | synth-04 5.3 observations | one test parametrized over 12 entries skips unconditionally (observations.py:79-84); 6 tests | R05; file read in full | MATCH |
| C-24 | synth-04 5.3 orca-ide gap | guard matches basename `orca` only (GD:457); `orca-ide` default at sweep/probes.py:43; first in install_user_setup.py:36; architecture reference :83 records a DEFECT | R05:427; GL Q-17; snapshot lines read | MATCH |
| C-25 | synth-04 5.4 stale-doc remark | architecture reference :268 says the section was removed in issue 655 and no contract rule says who starts the worker; :196 / :285 rule counts and ranges stale; "739 tests" at :208 | R06:63-66; line :268 read (the quote elides "the orchestrator design replaces them" with "[its replacement]") | MATCH (see B-1 on the sibling citations) |
| C-26 | synth-04 5.3 launch-path table, G1 row and ledger | recorded as "not governed" at docs/designs/orchestrator.md:117 | R05:222 and R05:467 cite that line; the line text is the new orchestrator design's DQ7 (it says "no L1 guard"; the words "not governed" are at :129) | DRIFT (scope violation, finding B-1) |

## Claim-tracing table (synth-05)

| ID | Synth file and location | Claim | Research support | MATCH/DRIFT/UNTRACEABLE |
|---|---|---|---|---|
| C-27 | synth-05 8.1 watcher | all seven `gh` argv are reads; `REPO = "IronbellyOrg/IronClaude"` P/github.py:37 | R02 section 7(c); snapshot github.py:37 read | MATCH |
| C-28 | synth-05 8.1 Orca launch | 12-element argv at launch.py:95-116; retry argv 14 elements with `--retry-launch <id>` before `--json` (:119-132) | R02; launch.py lines 84-132 read | MATCH |
| C-29 | synth-05 8.1 Orca discovery | `[<abs path>, "skills", "list", "--json"]`, accepted only if topic `orca-cli` listed (launch.py:144-203) | R02; snapshot read | MATCH |
| C-30 | synth-05 8.1 C2 | ClickUp PUT `https://api.clickup.com/api/v2/task/{task_id}` body `{"assignees": {"add": [<user id>]}}` at clickup_claim.py:232-237; skipped without token/workspace :164-169 | R04:103; clickup_claim.py lines 70-259 read | MATCH |
| C-31 | synth-05 8.2 CLI | `orca_worktree.py` subcommands/choices at :1857-1894; `--submit needs --level full` exit 2 at :1900-1901; origin_repo exit 0/1/3/4 | R04; snapshot lines 1850-1906 read | MATCH |
| C-32 | synth-05 8.4 hooks table | SessionStart 4 hooks (10/5/5/5), PreToolUse Bash block-bare-python and require-orca-worktree-agent (3, 3), Edit|Write freshness-pre-edit (1), SubagentStart (1, 5), SubagentStop async (1) | R05 section 4; hooks.json lines 1-192 grep/read | MATCH |
| C-33 | synth-05 9.1 config | `_TOP_KEYS` = 8 keys (cycle.py:58-69); `enabled` default False (:228); label rules (:127-139); `_APPROVERS_MAX_BYTES` 1 MiB (:75); network FS set (:50-52) | R03; cycle.py lines 30-80, 118-139, 183-362 read | MATCH |
| C-34 | synth-05 9.2 IR-7 row | `IR7_REFUSE` False, pinned test_issue_l2_install.py:639 | R04:208 | MATCH |
| C-35 | synth-05 9.3 env | `SC_ORCA_TIMEOUT`, `DEFAULT_TIMEOUT=120`, `PREFLIGHT_TIMEOUT=30`, `TERMINAL_READ_TIMEOUT=15` (OW:88-91); `SHIM_TRIES=5`, interval 2.0 s via `SC_ORCA_SHIM_INTERVAL` (OW:798-800); guard reads only HOME (GD:23) | R04; snapshot read | MATCH |
| C-36 | synth-05 10.1 exit table | precedence `_PRECEDENCE = (2, 6, 7, 5, 3, 4)` cycle.py:462; `_EXIT_*` constants cli.py:34-38 | R01 section 8; snapshot grep read | MATCH |
| C-37 | synth-05 10.2 vocabularies | REASON_TABLE 59 = 27 cycle + 17 skip + 9 entry + 1 note + 4 warning + 1 operator; the exit of every word | R01:297; audit.py:26-102 counted by hand | MATCH |
| C-38 | synth-05 10.2 L1 words | 18 `LL-*` words and block order BIG..SKILL | R05:22; GD:783 read | MATCH |
| C-39 | synth-05 10.4 guard exit codes | L2 hook is the only one that exits 1 (PP:9-10) | R05; header lines read | MATCH |
| C-40 | synth-05 11.1 budgets | CALL_CAP 35 (github.py:46), RESERVED_CALLS 3 (:49), PAGE_SIZE 100 (:40), PAGE_CAP 5 (:43), DISCOVERY_BOUND 100 (:486), RATE_LIMIT_MAX_WAIT_S 3600 (:376); cycle.py constants :34-47 | R01:29, R02; snapshot read | MATCH |
| C-41 | synth-05 11.1 record constants | MAX_ATTEMPTS 3 (record.py:434), BACKOFF 10 min (:437), LEASE 60 min (:440), DAY_CAP_WINDOW 24 h (:443); STDERR_CAP_BYTES 500 (runner.py:15) | R02; snapshot grep read | MATCH |
| C-42 | synth-05 Appendix A.1 | 21 rows; line counts and `def test_` counts of all 20 watcher test files and the fixtures dir (19 files, 12,059 bytes) | R01-R03 test-pin tables | MATCH (all re-counted) |
| C-43 | synth-05 Appendix A.2 to A.4 | hooks 11 rows, skills 9, other 7; every count (e.g. guard 4631/162, job identity 1530/56, ccsession_tag 7101/277) | R04, R05 test-pin tables | MATCH (all re-counted) |
| C-44 | synth-05 Appendix A closing | 48 rows = 44 named + 4 added; 44 = 20 watcher files + fixtures + 9 + 7 + 1 + 2 + 3 + 1 | research-notes EXISTING_FILES (44 entries counted) | MATCH |

## Claim-tracing table (synth-06)

| ID | Synth file and location | Claim | Research support | MATCH/DRIFT/UNTRACEABLE |
|---|---|---|---|---|
| C-45 | synth-06 12.1 closed guard words | 18 words = 16 classes + LL-NOBIND + LL-BROKEN | R05:22; GD:783 loop has 16 classes | MATCH |
| C-46 | synth-06 12.1 write-ahead | test name `test_a_failed_outcome_save_after_the_launch_never_relaunches__fr010_nfr005_c6` at test_cycle.py:4737 | R01; grep read | MATCH |
| C-47 | synth-06 12.1 one subprocess module | test_no_shell.py:150 and :156 | R03; grep read | MATCH |
| C-48 | synth-06 14.1.1 platform | `check_platform` via `_load_config` cli.py:88; reset at :314; status `platform=False` at :169 | R03; cli.py read | MATCH |
| C-49 | synth-06 14.1.2 KW-1 | skew 300 s is SKEW_TOLERANCE_S (predicates.py:17, used :295); warning is SKEW_WARN_S 60 (cycle.py:44); DES:827 row reads "skew tolerance | 300 s | equals the cadence" | R01 row 22; R03 Gap-fill c1 F-1; DES:827 and :510 read | MATCH (refuted with evidence) |
| C-50 | synth-06 KW-2 / D-01 | MAX_LAUNCHES_PER_CYCLE defined at cycle.py:35, no other hit in src or tests; cap is halt at :833-834 | R01 Gap-fill c1 B-1; whole-tree grep read | MATCH |
| C-51 | synth-06 KW-3, KW-4 | WORKER-CONTRACT has no "Issue pipeline duties"; issue-watcher-live-test.md absent; fu1.md:64-66 uses removed `issue-pipeline plan-hash` | R03, R06 | MATCH |
| C-52 | synth-06 KW-6 | GD:409 `implement | task | cleanup`; design lists six; `/sc:task` not accepted | R05 rows 1-2 | MATCH |
| C-53 | synth-06 KW-7 / X-24 | sc-issue-command.md:3 "Design only"; T3 pin tier2b at agent file :6; TIER_TEXT_DIRS :50, TIER_TEXT_ALLOWED :38-44 | R04:390-391, Gap-fill c1 F-2 | MATCH |
| C-54 | synth-06 KW-8, X-27 | zero launch-level text in ccsession-tag; plugin hooks.json also lacks pragmatic-subagent.js and has `async` on freshness-subagent-start | R05 section 5.2, row 21 | MATCH |
| C-55 | synth-06 D-19 | IR-7 constant OD-3 / 2026-11-08 comment at OW:818-822 | R04:208 | MATCH |
| C-56 | synth-06 Appendix B.1 | removal commit 01e7a9e23 (PR 682), 2026-11-19 18:02:35 -0600; 10 files, 1,597 lines (5, 62, 416, 74, 395, 90, 161, 66, 301, 27) | R06:398; `git show`/`git ls-tree` read | MATCH |
| C-57 | synth-06 B.2 | 10 verbs with decorator lines :61, :76, :96, :108, :117, :134, :161, :179, :200, :335; `_EXIT_REFUSED=1`, `_EXIT_CONFIG=2`, `_EXIT_LOCK_HELD=75` (cli.py:29-32); group at :56-58 | R06; `git show 01e7a9e23^:.../cli.py` grep read | MATCH |
| C-58 | synth-06 B.5/B.6 | old WORKER-CONTRACT 350 lines, WC-17 at old :59, duties :291-300, "grant row" at old :57 and :300, 0 hits for COORD-; old guard 811 lines, TAMPER case at :444 with comment :441-443 | R06 | MATCH |
| C-59 | synth-06 B.8 | 116 tests in 10 files (2+3+9+21+12+10+10+7+29+13), 2,391 lines; registration test 15 lines, 1 test; test_worker_contract 3,181/61 to 3,135/59; guard worker test 330/13 to 300/11, numstat +13/-43 = -30 | R06:238-241; `git show` counts read | MATCH |
| C-60 | synth-06 B.1 same commit | CHANGELOG +4, tech reference one line, cli-groups 10, main.py -4, WORKER-CONTRACT +1/-12, guard 5 removed and 2 added | R06; `git show --numstat` read | MATCH |
| C-61 | synth-06 14.2 intro and D-18, D-27, D-31 | decisions "recorded" at docs/designs/orchestrator.md:991, :116, :117 | R06:100, R05:448; GL D-28, Q-11 | DRIFT (scope violation, finding B-1) |

## Findings

| ID | Severity | Synth location | Problem | Evidence (research or source path:line) | Required fix |
|---|---|---|---|---|---|
| B-1 | BLOCKING | synth-04 lines 192 (5.3 G1 status row), 213 (launch-path table, coordinator-started worker row), 315 (ledger G1 row), 316 (ledger G2 rule 1 row), 378 (5.4 "grant row" line); synth-06 line 217 (14.2 intro, cites `docs/designs/orchestrator.md:991`, `:116`, `:117`) and, through "See the 14.2 clause", rows D-18, D-27, D-31 | The three files cite `docs/designs/orchestrator.md` as the place where a "decision" is recorded (G1 "not governed", removal of route A, retirement of the "grant row"). That file is the owner-approved design of the new issue-polling orchestrator (its header: "approved by the owner (Clay) ... The build starts from this text"), i.e. the rewrite design the owner put out of scope. Lines :116 (DQ6) and :117 (DQ7) are design decisions for the new orchestrator's workers, not decisions about the current pipeline, and :117 does not contain the quoted words "not governed" (they are at :129). Rule (i) of this review and the Gate 1 consolidated findings (M-5: "do not carry rows that rest only on docs/designs/orchestrator.md (the out-of-scope rewrite design) into synthesis; ... reworded to 'no decision found in the files this reference cites'") forbid this. The authors scrubbed the sibling sentence at SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268 ("the orchestrator design replaces them" became "[its replacement]"), so the six path citations are inconsistent with their own handling. Judged BLOCKING under the task's "any PR 686 / rewrite-design mention" severity rule; if the owner accepts a bare path citation as a "decision location" (a softer reading in the Gate 1 depth report), downgrade to MINOR. | /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/BUILD-REQUEST.md:14; qa/qa-research-consolidated-findings.md:21; snapshot docs/designs/orchestrator.md:3, :116, :117, :129, :991; grep of the three synth files returns 6 hits (synth-04:192, 213, 315, 316, 378; synth-06:217) | Remove every `docs/designs/orchestrator.md` citation. Replace by in-scope evidence: G1 "not governed" by `docs/designs/sc-issue-launch-level-hook.md:23` and `docs/designs/issue-pipeline-fu1.md:18`; removal of route A and of the duties by `CHANGELOG.md:17` and `GD:496-497`; for the "grant row" retirement and for D-18 write "no decision found in the files this reference cites". Reword the 14.2 intro clause and the Note cells of D-18, D-27, D-31 accordingly. |
| M-1 | MINOR | synth-04 5.2 status row "Coordinator hand-off after a --pipeline none claim" and 5.4 "Who starts a worker after a claim" | The live prose at issue.md:85, SKILL.md:140 and claim.md:96 still describes a coordinator "adoption row" that is `reserved` then `started`; that row belonged to the removed `adopt-create`/`adopt-mark` flow (Appendix B.5 duty 2). The synth calls the hand-off "prose only" but does not say the prose names a removed mechanism (research 04 recorded it only as [UNVERIFIED], GL C-40). | claim.md:96 and SKILL.md:140 read; synth-06 B.5 duty 2 | Add one clause: the prose still names an adoption row whose code was removed in 01e7a9e23 [STALE DOC]. |
| M-2 | MINOR | synth-05 10.2 entry-kind row | Line range `P/audit.py:84-91` ends one line early; `claimed` is at audit.py:92. | audit.py lines 83-92 read | Write `:84-92`. |
| M-3 | MINOR | synth-04 5.2 Key Files and tiers table; synth-04 header and 5.2 table cell "(erratum applied)", "(15 files, not 17)" | Build-process wording ("erratum applied", "not 17") leaks into the reference; a reader of the final document has no 17 or erratum to compare with. | research/04:405, qa-research-consolidated-findings.md M-4 | Delete the process words. |
| M-4 | MINOR | synth-06 D-16 capability cell | The capability cell names `COORD-<RepoName>`, "dispatcher" and "zero-setup install" as a debt capability although no file declares them; the evidence cell correctly says "not found in snapshot". Rule (j) allows the not-found statement but not a capability row built from those names. | BUILD-REQUEST.md:28; D-16 evidence cell | Keep the three names only in the "not found in snapshot" sentence, not in the capability name. |
| M-5 | MINOR | synth-04 5.4 last paragraph | The quote of SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268 is edited ("... and until [its replacement] lands ...") but tagged [CODE-VERIFIED by reading the line]; the line reads "the orchestrator design replaces them, and until it lands". The edit is editorial, the meaning is kept. | line :268 read | Optionally paraphrase instead of quoting. |

## Checks performed

Lens checklist (a) to (l) for partition 2:

| Check | Result | Basis |
|---|---|---|
| (a) no fabricated content beyond research | PASS | 61 sampled claims traced; every value traced to a research row and to a live line; no untraceable claim found |
| (b) paths and path:line evidence | PASS | about 140 distinct path:line citations re-read in the snapshot or in `git show 01e7a9e23^`; only one range one line short (M-2) |
| (c) architecture claims code-traced | PASS | all behaviour rows cite code lines; doc-only rows carry [CODE-CONTRADICTED], [STALE DOC] or [UNVERIFIED] |
| (d) no doc-only claim in integration content | PASS | synth-05 sections 8-11 cite code; doc-only items ("about 100 ms", `gh` reply shapes, GH_ERROR_SIGNS) are tagged [UNVERIFIED] |
| (e) research [CODE-CONTRADICTED]/[STALE DOC] findings reach Section 14 | PASS | research 04 rows :390-405, research 05 :476-481, research 06 :63-69, :95-99, :375-381 each map to KW-1..KW-8 or X-1..X-28 (the "17 template files" brief error is not a doc claim; M-3) |
| (f) contradicted claims corrected, unverified flagged | PASS | e.g. KW-1 refuted with evidence; "739 tests" kept [UNVERIFIED] |
| (g) cross-section consistency | PASS | test counts, 14+3 and 44+4 totals, 18 words, 23 tools, 59 reasons, 8+4 warning codes agree across synth-04/05/06 |
| (h) status words | PASS | only BUILT-ON / BUILT-OFF / NOT BUILT / REMOVED, with parenthetical qualifiers; D-19 explicitly says "not `enabled:false`" |
| (i) no PR 686 / rewrite design | FAIL | no literal "PR 686" or "rewrite design"; but six citations of `docs/designs/orchestrator.md` (B-1) |
| (j) no memory-note facts as facts | PASS | "zero-setup watcher", "COORD-", "dispatcher" appear only as "not found in snapshot"; "grant row" quoted from WORKER-CONTRACT.md:57 with its single-mention status (M-4 is cosmetic) |
| (k) Appendix A row count | PASS | 48 rows = 44 named (20 watcher files + fixtures dir + 9 + 7 + 1 + 2 + 3 + 1) + 4 added; the 44 equals the EXISTING_FILES test list, including the four tests/hooks companion files and the fixtures directory; every file exists in research test-pin tables (R05 section 11, R04 gap-fills) |
| (l) Section 14 rows trace; eight warnings present | PASS | KW-1..KW-8 map one to one to the eight BUILD-REQUEST warnings (KW-1 refuted with evidence); D-01..D-31 and X-1..X-28 trace to research rows and GL D-rows |

Counts: claims traced 61 (synth-04: 26, synth-05: 18, synth-06: 17; MATCH 59, DRIFT 2, UNTRACEABLE 0); findings 6 (BLOCKING 1, MINOR 5). Additional spot checks not in the table: 48 test-file line counts and 48 `def test_` counts (all equal), 22 test-function line numbers in test_launch_level_guard.py, test_launch_level_observations.py, test_issue_l2_install.py, test_worker_contract.py and test_model_alias_policy.py, 9 REASON_TABLE groups counted by hand, 10 removed-test file counts, 10 removed-package line counts.

Evidence limits: no test was run; the removed tree was read only through `git show` / `git ls-tree` / `git log` on `01e7a9e23^` and `01e7a9e23`; nothing under /home/coder/.cache/ic-snap-20261120/master was written; the only file written is this report.

## Verdict: FAIL

BLOCKING findings: 1 (B-1). All other content of synth-04, synth-05 and synth-06 matched the snapshot and the research.

Status: Complete

