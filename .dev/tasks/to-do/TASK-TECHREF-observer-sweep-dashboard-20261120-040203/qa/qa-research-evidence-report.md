# QA Report - Research Gate (evidence-quality lens)

**Topic:** Observer, sweep and dashboard family technical reference
**Date:** 2026-11-20
**Phase:** research-gate
**Fix cycle:** N/A
**Status:** Complete

---

**Lens:** evidence-quality (QA runs in parallel with the analyst; no analyst report consulted)
**Fix authorization:** false (report only; no research file was modified)
**Code snapshot:** /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6; `git rev-parse origin/master` in the checkout still prints 61ac2c2e6effc24baa5ccef2a71a0a08d85bd5cd)
**Files reviewed:** the six research files in `.../research/` (01 to 06) and `.../research-notes.md`

---

## Overall Verdict: FAIL

Two blocking findings (both cheap to fix, no re-research needed): F-1 unresolved C8 contradiction between research files 03 and 04 (two capabilities); F-2 a false statement about `docs/user-guide/commands.md` in file 03. Everything else sampled (about 150 `file:line` ranges across the six files, 6 PR records, 10 live gh reads, 5 absence greps) matched. Minor notes are listed after the findings and never fail the gate.

(Sections below were appended incrementally while the checks ran.)

---

## Sampled-citation table

Method: each row is a citation (or a small cluster of citations from one passage) that I re-read in the snapshot (or via `git show origin/master:` or `gh` read-only, where the research file says so) and compared with the claim. "yes" means the code or text says what the research file says. Paths are relative to the snapshot root unless they start with `/` or say origin/master.

### File 01 (observe data contract): 25 rows

| # | Research file | Citation | Match | Note |
|---|---|---|---|---|
| 1 | 01 | src/superclaude/cli/observe/adapter.py:29-32 | yes | WORKER_LIST, DISCOVERY and QUESTION templates as stated |
| 2 | 01 | adapter.py:34-50 | yes | 13 prefixes, same names |
| 3 | 01 | adapter.py:57-63 | yes | 5 calls, 8 MiB, 2 KiB, 10.0 s with the UNVERIFIED comment, 2.0 s |
| 4 | 01 | adapter.py:111-118, 121-132 | yes | 8-token shape; positions minus {1,4,6} |
| 5 | 01 | adapter.py:232-238 | yes | Popen list argv, DEVNULL, new session |
| 6 | 01 | adapter.py:296-306 | yes | timeout, output-cap, kill grace |
| 7 | 01 | adapter.py:447-467 | yes | empty-page, OK, PARTIAL capped, cursor-stalled, cursor-rejected |
| 8 | 01 | adapter.py:63-69, 495-512 | yes | two error codes map; exit:n, json, OK |
| 9 | 01 | adapter.py:365-381 | yes | discover once; namespace is realpath |
| 10 | 01 | parse.py:43 | yes | `UNKNOWN: Any = _Unknown()` |
| 11 | 01 | parse.py:365-380 | yes | four ShapeError conditions |
| 12 | 01 | parse.py:620-651, 722-744 | yes | like-field timestamps; older never overwrites; reobserved=False |
| 13 | 01 | collector.py:28-34, 304-307, 321 | yes | constants; doubling backoff; reset |
| 14 | 01 | collector.py:125-129, 152-153, 273-276, 345-361 | yes | no-question-fixture; questions need run; cap 4; loop ends on NOT_AVAILABLE |
| 15 | 01 | questions.py:21-24, 70-73, 123-142 | yes | 1000 bound, 100 window, eviction, window_is_full |
| 16 | 01 | view.py:32-36, 456-463, 667, 681 | yes | 45 s STALE; status map; error only for ERROR |
| 17 | 01 | export.py:20-22, 24-48, 141-155, 160-170, 184-192, 236-244, 257-274 | yes | 19 text fields + 1 any field = 20; 0600 temp+replace |
| 18 | 01 | src/superclaude/cli/install_user_setup.py:36, 247-270 | yes | `_ORCA_CLIS`; probe; `any(...)` outside the try (line 268) |
| 19 | 01 | commands.py:63-70 | yes | both gate constants True with cited records |
| 20 | 01 | snapshot.schema.json:50 | yes | counts values restricted to scalars |
| 21 | 01 | tests/observe/test_adapter.py:176-192 | yes | `FORBIDDEN_PREFIXES >=` the 13 names |
| 22 | 01 | tests/observe/test_golden_contract.py:22, 43-58, 505 | yes | GOLDEN tuple; PARTIAL 100 of 428; "Run run-b, not Run run-a" |
| 23 | 01 | tests/observe/record_golden_questions.py:1-17, 35-49 | yes | no Orca call; 13 message keys |
| 24 | 01 | origin/master `.dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/RESEARCH-REPORT-phase2-gate.md` lines 86-100 | yes | quoted question text and the 9-step table |
| 25 | 01 | origin/master `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` lines 3, 5, 9-18, 40, 42, 50, 58, 64 | yes | provenance label (origin/master only) is right |

### File 02 (observe interaction, gates, docs): 31 rows

| # | Research file | Citation | Match | Note |
|---|---|---|---|---|
| 26 | 02 | commands.py:53-61 | yes | POSIX/no-terminal text, 0.1 s, 0.5 s, WIDTHS |
| 27 | 02 | commands.py:173-197 | yes | `_questions_on`, `_link_on`, refusal exit 2/2/2/1 |
| 28 | 02 | commands.py:244-269 | yes | run_once; snapshot failure exit 1; else 0 |
| 29 | 02 | commands.py:306-312, 330-340, 346-354, 362-372 | yes | one snapshot per cycle; QUIT 0; export message; exit 1 on display failure |
| 30 | 02 | commands.py:375-388, 396-410 | yes | win32 exit 2; no-terminal exit 2; write_snapshots rule |
| 31 | 02 | commands.py:449-460, 505-524 | yes | group, `--once`, `--width`; no subcommand handling; `ctx.exit(code)` |
| 32 | 02 | keys.py:20-24, 115-126, 225-235 | yes | 0.25 s, 0.05 s; SIGINT, 128+SIGTERM, 128+SIGHUP; only up/down arrows |
| 33 | 02 | view.py:28-31 | yes | KEY_NAMES |
| 34 | 02 | view.py:1246-1300 | yes | all 14 key behaviors in the stated order and lines |
| 35 | 02 | view.py:88-112, 134 | yes | key lines, desk literals, UNAVAILABLE_FACTS |
| 36 | 02 | view.py:253-264, 888-906 | yes | DeskView; `_desk` returns None unless link on and selected |
| 37 | 02 | terminal.py:21-27, 82-89, 108-118 | yes | thresholds; width classes; NO_COLOR; ASCII rule |
| 38 | 02 | render.py:494-500 | yes | full-width fixed columns 12/12/0/16/14/12; id <= 48 |
| 39 | 02 | render.py:1263-1272 | yes | too narrow / too small paths keep counts and gap notice |
| 40 | 02 | render.py:942, 1374-1386 | yes | LAYOUTS ("A","B","C"); 80 columns uses "C" only |
| 41 | 02 | render.py:787-790, 925-927, 1114-1118, 1320-1322 | yes | desk question pane; `_desk_widths`; READ ONLY title bar; questions win on short terminal |
| 42 | 02 | render.py:63, 921-922, 1167, view.py:131 | yes | 24, 80, 46, 3; step 3 |
| 43 | 02 | theme.py:94-104 | yes | seven state-role pairs |
| 44 | 02 | sanitize.py:14-26 | yes | escape classes; Cc, Cf, Cs dropped |
| 45 | 02 | src/superclaude/cli/main.py:588-593 | yes | observe registered at 590-592 |
| 46 | 02 | tests/observe/test_registration.py:14-18, 59-71 | yes | |
| 47 | 02 | tests/observe/test_commands.py:144-156, 665-672, 752-780 | yes | gate tests read `.dev/` paths the snapshot omits (research Gap 1 is right) |
| 48 | 02 | pyproject.toml:7 | yes | version 6.1.0 |
| 49 | 02 | CHANGELOG.md:5, 23, 69, 170-171, 365 | yes | section heads and dates; line 365 is a pr-submit note |
| 50 | 02 | docs/user-guide/cli-groups.md:40-54 | yes | seven options, 15 s and 5 calls |
| 51 | 02 | README.md:35, 136 | yes | |
| 52 | 02 | docs/testing/v6.0.0/post-release-report.md:56, 135, 173 | yes | "13 source files"; 14 `.py` files if fixtures `__init__` counted: also confirmed |
| 53 | 02 | gh PR #503, #514, #577, #592, #598, #673 | yes | title, MERGED, mergedAt and merge commit all equal the table |
| 54 | 02 | origin/master `.dev/issues/409/owner-pass-record-20261112.md`; `owner-direction-record-20261116.md`; checkout `.dev/issues/409/` listing | yes | exact text and listing |
| 55 | 02 | "Directory holds 41 entries (Glob)" for tests/observe | NO | snapshot `ls tests/observe` = 36 entries (minor note M-1) |
| 56 | 02 | "test_session.py: 29 test functions" | NO | `grep -c '^def test_'` = 27, and `grep -c 'def test_'` = 27 (minor note M-1) |

### File 03 (sweep classifier and joins): 32 rows

| # | Research file | Citation | Match | Note |
|---|---|---|---|---|
| 57 | 03 | src/superclaude/cli/sweep/classify.py:38-52 | yes | JOIN_PATH "B"; 8 class constants |
| 58 | 03 | classify.py:94-128 | yes | sets, STOP-code regex, `_settled`, `_freeze_codes`, `_ruling_halt` |
| 59 | 03 | classify.py:161-188 | yes | rule 1 branches (i) to (v) as tabled |
| 60 | 03 | classify.py:191-216 | yes | rule 2 needs exited + `worker_done_seen is False` + `fenced_evidence == "absent"` |
| 61 | 03 | classify.py:219-223 | yes | rule 3 |
| 62 | 03 | classify.py:226-248 | yes | rule 4 (a), (b) frozen, (b) ready Task |
| 63 | 03 | classify.py:251-269 | yes | rule 5, four conditions, status not tested |
| 64 | 03 | classify.py:272-292 | yes | rule 6 guard-refused first line; settled + contract; partial note |
| 65 | 03 | classify.py:295-327 | yes | rules 7 and 8 (rule 8 omits `orca is None` and `<= now` as stated) |
| 66 | 03 | classify.py:330-345 | yes | rule 9 and the no-contract note |
| 67 | 03 | classify.py:345-386 | yes | RULES order; `_force_unknown`; note harvest; unreadable transcript forcing |
| 68 | 03 | classify.py:389-400 | yes | `policy_of` |
| 69 | 03 | classify.py:423-436, 455-504 | yes | package_state, shared packages, removable, safe_to_close |
| 70 | 03 | classify.py:570-591 | yes | `_contract_for` algorithm; the docstring is at :575 not :571 (note M-3) |
| 71 | 03 | classify.py:609-629, 655-683 | yes | path B tail rule; path A then B per transcript |
| 72 | 03 | classify.py:741-779 | yes | `_guard` flags; `_person_origin` order |
| 73 | 03 | classify.py:793-798, 921-936, 974-984 | yes | lifecycle; transcript-only rows; counts, historical, visible |
| 74 | 03 | grep JOIN_PATH in sweep/*.py | yes | only :40 (definition) and :745 (use) |
| 75 | 03 | models.py:29-42, 48-59, 96-125, 160-166 | yes | `report_folders`; CLASSES; field comments; nine dimension fields |
| 76 | 03 | probes.py:478-490, 838-850, 1255-1261, 1473-1476 | yes | `agent_wait_since` unset; 256 KiB tail; ready-Task row; transcript source name |
| 77 | 03 | tests/sweep/fixtures/SOURCES.md:1-30 | yes | running-worker fixture and empty ready task list |
| 78 | 03 | docs/designs/orchestrator-mode.md:25-28, 493, 841, 1003 | yes | "does not exist yet" is stale; rule 5 restored; D7; open item 6 resolved |
| 79 | 03 | src/superclaude/commands/sweep.md:14, 16; skills/sc-sweep-protocol/SKILL.md:26 | yes | quotes found (long lines, confirmed by grep) |
| 80 | 03 | core/WORKER-CONTRACT.md:289, 61-63; grep `fenced` | yes | `fenced` occurs only at 61 and 63 |
| 81 | 03 | report.py:42-49 | yes | SP24_LINE, SAFE_TO_CLOSE_LINE |
| 82 | 03 | tests/sweep/test_classify.py:364-380 | yes | per-rule case, all classes reached, rules order pin |
| 83 | 03 | tests/sweep/test_cli_contract.py:1133-1141 | yes | captured running worker prints `working` |
| 84 | 03 | CHANGELOG.md:170 | yes | the line says what 03 reports (but see row 85) |
| 85 | 03 | docs/user-guide/commands.md:619-620 as "reason printed for stalled/fenced" | NO | line 619 gives no reason; the agentWait reason on line 620 belongs to `working` only (finding F-2) |
| 86 | 03 | origin/master SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` lines 103, 106, 107, 111, 167, 231, 232, 251, 274, 338 | yes | 653 lines; text equals the quotes in 03 |
| 87 | 03 | origin/master `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/design-base.md:813`; `sweep-live-check-1.4.md:19, 29` | yes | D7 row; "fenced evidence not readable" note |
| 88 | 03 | gh issue #590 and #534 | yes | both OPEN; titles match the description |

### File 04 (sweep read side and WC-16): 22 rows

| # | Research file | Citation | Match | Note |
|---|---|---|---|---|
| 89 | 04 | probes.py:43, 49-62 | yes | 10 templates; 4 comments "not called"; FORBIDDEN_TOKENS |
| 90 | 04 | probes.py:64-91 | yes | 4 git shapes; limits all marked "proposed" |
| 91 | 04 | probes.py:124-135 | yes | 50 shows, 90 s, 10 s |
| 92 | 04 | probes.py:214-245 | yes | binary choice; argv exact match |
| 93 | 04 | probes.py:266-312 | yes | result classification and the D-01 shortcut comment |
| 94 | 04 | probes.py:331-341 | yes | `--no-optional-locks`, fsmonitor off, `GIT_OPTIONAL_LOCKS=0` |
| 95 | 04 | probes.py:369-394 | yes | budgeted `_call`; first-call promotion to unavailable |
| 96 | 04 | probes.py:995-1020, 1036-1042 | yes | filter pre-check runs before status |
| 97 | 04 | probes.py:1150, 1281, 1335, 1381 | yes | call sites; remote hosts hard-coded unknown |
| 98 | 04 | probes.py:1398-1426 | yes | contract read |
| 99 | 04 | commands.py:99-123 | yes | `_check_output` |
| 100 | 04 | commands.py:153-208 | yes | temp file + `os.link`, MAX_SUFFIX names, unlink |
| 101 | 04 | commands.py:246-288 | yes | stage order; exit 2 / 1 |
| 102 | 04 | report.py:545-558, 693-695 | yes | 12 section functions; `report_path` last key |
| 103 | 04 | cli/main.py:581-583 | yes | |
| 104 | 04 | WORKER-CONTRACT.md:23, 46, 110, 157, 287-289 | yes | |
| 105 | 04 | HOW-WE-WORK.md:298, 359; .gitignore:254-257 | yes | |
| 106 | 04 | commands/sweep.md:22, 47 | yes | "Nothing starts it automatically"; Skill call |
| 107 | 04 | tests/sweep/test_probes_allowlist.py:370-392, 624-640 | yes | ten templates, seven verbs, zero argv for not-called |
| 108 | 04 | test counts: allowlist 100, cli_contract 61, report 43, git_config_hole 10, registration 3, sweep_command 28 | yes | `grep -c '^def test_'` |
| 109 | 04 | design docs/designs/orchestrator-mode.md:636, 813, 1022 | partly | :636 and :1022 yes; :813 is the NFR-005 row; the D7 row is at :841 (note M-4) |
| 110 | 04 | file 04 Section 5 DEFECT-CANDIDATE for stalled/fenced and `agent_wait_since` | NO | contradicts file 03; the scope text 04 says it could not find is in the SPEC (finding F-1) |

### File 05 (agent-work-report and living report): 23 rows

| # | Research file | Citation | Match | Note |
|---|---|---|---|---|
| 111 | 05 | agent-work-report/scripts/common.py:28-51 | yes | `repo_root` |
| 112 | 05 | common.py:133-150 | yes | entry-file contract comment |
| 113 | 05 | common.py:240-247, 404-405 | yes | six statuses; port 8765 |
| 114 | 05 | scripts/run.py:75-76, 95-125 | yes | lock; skip record; exit 3; run id |
| 115 | 05 | run.py:204-242 | yes | seven checks and sha gate |
| 116 | 05 | run.py:371-387, 686-690 | yes | close checks `passed` only |
| 117 | 05 | scripts/exclude.py:59-80 | yes | |
| 118 | 05 | scripts/orca_term.py:17-31, 124-133 | yes | terminals; `send` |
| 119 | 05 | scripts/waker.py:36-42, 214-232 | yes | wake line; 15 x 120 s; hourly skip |
| 120 | 05 | scripts/clickup.py:596-613 | yes | only ClickUp POSTs |
| 121 | 05 | clickup.py:616-632 | yes | `dm` calls `deliverable` |
| 122 | 05 | scripts/prefs.py:18-34 | yes | URL regex rejects `orca://` |
| 123 | 05 | scripts/page.py:308-335 | yes | http.server on `--directory state_dir()` |
| 124 | 05 | cli/issue_watch/cycle.py:56-70, 214-222 | yes | `_TOP_KEYS`; unknown key raises |
| 125 | 05 | skills/sc-closeout-protocol/scripts/settle.sh:1035-1045 | yes | probe `report-entry --help` |
| 126 | 05 | SKILL.md:10, 12, 14, 16, 24, 30, 172, 183, 194 | yes | 172 contradicts prefs.py:20 as stated |
| 127 | 05 | scripts/check.py:77-80; templates/report-template.html:8-10 | yes | |
| 128 | 05 | grep `report-entry`, `qa-report-template`, `orchestrator_repo`; `ls cli`, `ls commands`, `ls skills` | yes | no writer verb, no orchestrator package, template unreferenced |
| 129 | 05 | gh PR #681, #682, #683, #684 (MERGED, merge commits), #686 and #690 (OPEN), #539 | yes | equal to the table |
| 130 | 05 | gh api cycle.py on branch clayphi/issue-655-pr-a | yes | `orchestrator_repo` at :80, :117, :236-238, :263 |
| 131 | 05 | tests/skills/test_agent_work_report.py:2856-2858 | yes | "PR B's `report-entry` writes the same shape" |
| 132 | 05 | test counts 142 and 59 | yes | |
| 133 | 05 | "scripts total 6,321" | NO | the 16 scripts sum to 5,777 (5,971 with SKILL.md) (note M-2) |

### File 06 (dashboard design vs observer): 21 rows

| # | Research file | Citation | Match | Note |
|---|---|---|---|---|
| 134 | 06 | view.py:97-112 | yes | desk literals |
| 135 | 06 | view.py:314-322, 416-424, 427-440 | yes | omission text; `text_of`; `strip_hex`; `aggregate` |
| 136 | 06 | view.py:983-990, 1035, 1074-1076 | yes | fixture banner; "cost unavailable"; filter line |
| 137 | 06 | theme.py:59-70 against package canvas.py:7 | yes | all 8 palette values equal after hex to RGB |
| 138 | 06 | sanitize.py:3-6 | yes | prototype not used |
| 139 | 06 | questions.py:91-97; collector.py:304-317 | yes | failed read changes nothing; last good snapshot kept |
| 140 | 06 | commands.py:3-4, 77-80 | yes | |
| 141 | 06 | sweep/models.py:160-166 | yes | dimensions are report-only |
| 142 | 06 | package README.md:9, 46-52 | yes | "design collaboration branch" sentence is on line 9 (long line) |
| 143 | 06 | package DESIGN-CONTRACT.md:11 | yes | |
| 144 | 06 | package QA.md:9-11, 19, 29 | yes | FAIL for pre-correction snapshots; no later independent verdict |
| 145 | 06 | package integration-gaps.md:9-28 | yes | six "not established" items |
| 146 | 06 | package concepts.md:43-49 | yes | provisional top three |
| 147 | 06 | package fixtures.py:1, 24-26, 30-43 | yes | |
| 148 | 06 | observe/fixtures listing and descriptions | yes | 19 JSON files; uneven "run-a owns 60 of 80 rows"; golden-success "one redacted live worker-list read" |
| 149 | 06 | git: 495eb96d1 not an ancestor of origin/master; `diff --stat` over `.dev/design` empty; ls-tree 406 vs checkout 406; research folder 0 on origin/master and `??` locally | yes | provenance of local-only folder is right |
| 150 | 06 | gh api PR #503 files | yes | 545 = 406 + 52 + 34 + 27 + others |
| 151 | 06 | gh issue 409 body lines 13, 19, 25, 36, 82, 88, 110, 112, 125, 127; state OPEN, 8 comments | yes | |
| 152 | 06 | gh PR #539 MERGED 2026-11-14T17:41:26Z; issue #606 CLOSED 2026-11-20T00:20:54Z | yes | |
| 153 | 06 | observe/sweep cross-reference absence; no GitHub/ClickUp in observe or sweep (grep `clickup|github|\bgh\b`) | yes | 0 hits in observe, 0 in sweep; no `observer` in sweep, no `sweep` in observe |
| 154 | 06 | 02 section 5.3 absence: no primitive under commands, skills, agents, core, hooks names `superclaude observe` | yes | grep found 0 files |

Totals: 154 rows (file 01: 25, 02: 31, 03: 32, 04: 22, 05: 23, 06: 21). Result: 148 yes, 1 partly (row 109), 5 no (rows 55, 56, 85, 110, 133). Per-file minimum of 15 and total minimum of 90 are met.

---

## Checklist (10 items)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | Glob of `research/` shows exactly 01 to 06; each file has `**Status:** Complete` near the top and a closing `## Summary` (01 line 367, 02 line 301, 03 line 309, 04 line 295, 05 line 609, 06 line 299) |
| 2 | Evidence density | PASS | 154 sampled rows; 148 match, 1 partly, 5 do not (all five are counts, a wrong line number, or findings F-1/F-2). Every sampled path exists (all reads succeeded in the snapshot, checkout or `git show origin/master:`) |
| 3 | Scope coverage | PASS | Every EXISTING_FILES row of research-notes is discussed: observe modules (01, 02, 06), sweep modules, command, skill, WC-16, HOW-WE-WORK, design (03, 04), all 16 agent-work-report scripts, 7 templates and both designs (05), the #409 package, issue records and local-only folder (06) |
| 4 | Documentation cross-validation | FAIL | Doc-sourced claims are tagged almost everywhere; one tagged claim is false (F-2: commands.md:619-620 as a reason for stalled/fenced). Every `[CODE-VERIFIED]` I sampled (rows 1-154) held |
| 5 | Contradiction resolution | FAIL | F-1: files 03 and 04 give opposite C8 determinations for stalled (proved), fenced and `agent_wait_since`; not reconciled anywhere |
| 6 | Gap severity | PASS | Each file's "Gaps and Questions" lists items as UNVERIFIED, CODE-CONTRADICTED or owner questions; none would make the synthesis invent facts. The only blocking items are F-1 and F-2 above |
| 7 | Depth appropriateness | PASS | Standard tier: file-level coverage plus traced call chains (observer `--questions` chain; WC-16 hops; `report-entry` writer search) |
| 8 | Integration point coverage | PASS | Orca verbs per tool (01 argv templates; 04 ten templates; 05 `orca` terminal/automation/tab verbs), file formats (snapshot v1, sweep JSON v1, run-folder artifacts), consumers (02 5.3, 04 6.6, 05 15) |
| 9 | Pattern documentation | PASS | Read-only guards, UNKNOWN / could-not-determine, layering, per-tool sanitizers and Orca binary choices are documented in 01, 03, 04, 06 and summarised in research-notes |
| 10 | Incremental writing compliance | UNVERIFIABLE | No edit history exists to inspect; structure suggests iterative growth (05 forward-references "section 18" from section 15; 01 sections 9 to 12 are late additions) but that is not proof |

Provenance and write-boundary checks (extra): files that exist only on origin/master under `.dev/` (release-gates.md, owner records, SPEC, design-base.md, RESEARCH-REPORT, sweep-live-check) are labelled "origin/master only" or "blob" in files 01, 02, 03, 04, 06; the untracked `.dev/research/orca-dashboard-20261105/` is labelled LOCAL-ONLY in 06 and not relied on in 01 (its Gap 11). The only research text that says it wrote outside the task folder is file 03 line 10 (a scratch copy of the SPEC in `/tmp`, deleted again): note M-5.

---

## Issues Found (blocking findings)

### F-1 (IMPORTANT, blocking): research files 03 and 04 contradict each other on the C8 determination for three capabilities

| Item | Where | What each file says |
|---|---|---|
| `stalled (proved)` and `fenced` classes | 03 section 8.1, 8.2, Takeaways, Summary | "not a DEFECT-CANDIDATE under the C8 rule, because a cited, spec-level scope decision exists (SPEC:232 plus design D7)"; SPEC lines 231, 232, 251 and design lines 493, 841 are quoted |
| same | 04 section 5 (long DEFECT-CANDIDATE paragraph), Gaps item 1, Summary | "DEFECT-CANDIDATE ... no owner decision declaring the capability out of scope was found" |
| `agent_wait_since` has no producer | 03 section 8.5 | "Scope text exists ... Not a defect candidate on the same basis" |
| same | 04 section 5 "Second note" and Gaps item 2 | "DEFECT-CANDIDATE (low) ... no cited decision names the wait time as out of scope" |

What I checked:
- origin/master `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md` (653 lines) line 232 reads "`worker_done_seen` is None on live rows, because no named live source establishes its absence. Stalled (proved) stays fixture-only until a source mapping exists."; line 231 says `fenced_evidence` is "always `unreadable` on live rows in Phase 1"; line 251 says `fenced` fires on "synthetic fixtures only in Phase 1". So 03's quotes are accurate and the scope text exists.
- The snapshot design `docs/designs/orchestrator-mode.md` has `worker_done_seen is None on every live row` at line 493 and the D7 row at line 841; both are what the research-notes name as the on-record decision to quote ("docs/designs/orchestrator-mode.md Phase 1 limits, SKILL.md 'not observed in Phase 1'").
- File 04 quotes the same design line 493, D7 and the SKILL/command caveat itself and still labels the capability a DEFECT-CANDIDATE; it never read the SPEC. So 04 applied the research-notes rule differently from 03.
- The standard is also uneven across files: file 05 labels the missing `report-entry` writer a DEFECT-CANDIDATE although it cites the design's PR B sequencing ("whether it counts ... is for the owner"), which is the same kind of design-level decision file 03 accepted as sufficient. Files 01 and 02 say "no DEFECT-CANDIDATE" for R2/R3 while file 06 records D-1 (fixture replay of the question ledger and Decision Desk is refused by `--questions` with `--fixture`); those are different capabilities (live wiring versus spec-declared fixture replay), but a reader of Section 14 needs the scope of each "none found" stated.

Why it blocks: Section 14 of the final document must carry the C8 analysis for these items. With the files as they stand the assembler gets two incompatible labels for the same capability and no rule for choosing.

Required fix (no new code reading needed): before synthesis, add one reconciliation note (for example `research/07-c8-reconciliation.md` or a new section in research-notes) that (a) states the single rule used (a cited spec or design-level scope decision means "known limit with cited decision", otherwise DEFECT-CANDIDATE), (b) gives the resulting label and the cited decision for each of: stalled (proved), fenced, `agent_wait_since`, the living-report writer (05), D-1 (06), and (c) says that the "no DEFECT-CANDIDATE" lines in 01 and 02 cover live R2/R3 wiring only. The facts in 03, 04 and 05 do not need to change.

### F-2 (IMPORTANT, blocking): file 03 states that `docs/user-guide/commands.md:619-620` gives the agentWait capture gap as the reason for stalled/fenced; it does not

Where: 03 section 8.1 point 3 ("The reason printed in `CHANGELOG.md:170` and `docs/user-guide/commands.md:619-620` for stalled/fenced ..."), section 8 Takeaways ("The public wording of the reason for stalled/fenced (CHANGELOG, user guide) is out of line with the SPEC's reason"), and Gaps item 4 ("Both also give the `agentWait` capture gap as the reason for stalled/fenced").

What the files say (snapshot):
- `docs/user-guide/commands.md:619`: "The classes `stalled (proved)` and `fenced` are never observed in Phase 1, so a zero there means nothing. The counts carry the mark `(not observed in Phase 1)`." No reason is given.
- `docs/user-guide/commands.md:620`: "The class `working` is never produced yet, because the live names of Orca's `agentWait` field were never captured." The "because" belongs to `working` only.
- `CHANGELOG.md:170`: one sentence covering all three classes ("... never observed, and `working` is never produced, because the live `agentWait` names were never captured (design open item 6)"). Only this line can be read as giving that reason for stalled/fenced.

Why it blocks: the assembler will copy "CHANGELOG and user guide misstate the reason" into Section 14; for the user guide that is not true. Row 85 of the sampled table records it.

Required fix: restrict the misattribution claim in 03 (8.1 point 3, 8 Takeaways, Gaps 4) to `CHANGELOG.md:170`, say that `commands.md:619` gives no reason and that the `commands.md:620` clause is stale only because it says `working` is never produced. The 03 stale-doc table row for commands.md:620 is already correct.

---

## Minor notes (not rechecked, do not fail the gate)

| ID | Where | Note |
|---|---|---|
| M-1 | 02 sections 5.1, 5.2; research-notes (a) | "Directory holds 41 entries" is wrong: `ls tests/observe` has 36 entries, of which 26 are `test_*.py` files (the research-notes line "36 test files" counts entries; the rest are conftest, 3 golden JSON, 5 helper scripts and `__init__`). test_session.py has 27 tests, not 29. Use 26 test files / 36 entries / 27 tests in the final text |
| M-2 | 05 section 1 | "scripts total 6,321" is wrong; the 16 listed scripts sum to 5,777 lines (5,971 with SKILL.md). Per-file counts are right |
| M-3 | 03 section 4.6 | docstring cited at classify.py:571; it is at :575 (algorithm lines 570-591 are right) |
| M-4 | 04 Stale Documentation item 2 | says the D7 row lives at design-base.md:813 and that the snapshot's line 813 is another row. True for NFR-005 at :813, but the snapshot design carries the D7 row at `docs/designs/orchestrator-mode.md:841` (and cites it at :636). Cite :841 |
| M-5 | 03 line 10 | reports a scratch copy of the SPEC written to `/tmp` and deleted; a breach of the write boundary (task folder or output file only), no residue and no risk. Surface to the owner, nothing to fix |
| M-6 | 01 to 04 | line counts in headings are +1 against `wc -l` (for example adapter.py "513" vs 512, commands.py "525" vs 524, probes.py "1478" vs 1477); cosmetic |
| M-7 | 06 section 2 vs research-notes (a) | notes say "18 fixtures"; the snapshot has 19 JSON fixtures (10 variants, 8 golden, question-cap-100), as 06 says |

---

## Actions Taken
None. Fix authorization was false; no research file was modified. The only file written is this report.

## Recommendations
1. Resolve F-1 and F-2 as described (a short reconciliation note plus one corrected statement in file 03; neither needs new source reading), then re-run this gate once (fix cycle 1).
2. Carry M-1, M-2, M-3, M-4 and M-7 into the synthesis as corrected facts; do not copy the research figures.
3. Items the research files correctly mark UNVERIFIED (Orca non-consumption for a non-owner reader, Orca automations, orchestrator repo, test pass results, `agentWait` non-null meaning) must stay marked UNVERIFIED in the final document; none could be checked here either.

## Confidence

- **Confidence:** Verified: 9/10 | Unverifiable: 1 (item 10: no edit history to inspect) | Unchecked: 0 | Confidence: 100.0% (9 / (10 - 1)). Confidence is not the verdict driver: the verdict is FAIL because of the two blocking findings.
- **Tool engagement:** Read: 14 | Grep: 9 | Glob: 1 | Bash: 31 (6 `gh pr view`, 4 more `gh` PR/issue/API reads, 1 `gh api` file count, 1 `gh issue view`, 1 blocked by the UV-only hook and re-run with `jq`, the rest read-only line prints in private `/tmp/ironclaude-batch.*` directories under the Bash batching policy, each removed by an exit trap). No web research was needed (`tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0`).
- Read + Grep + Glob = 24 is above the 10 checklist items; many Bash calls print the cited ranges themselves (Bash output is not a tracked Read, so none of this report's claims rely on a later edit of those files).
- UNCHECKED items: none. UNVERIFIABLE items: item 10 only.

## QA Complete
