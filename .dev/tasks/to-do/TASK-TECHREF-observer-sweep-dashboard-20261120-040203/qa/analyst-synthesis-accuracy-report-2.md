# Synthesis Accuracy and Source-Tracing Review (Partition 2 of 2)

**Status:** Complete
**Verdict:** FAIL (1 blocking finding B-1; 8 minor findings; details in sections 4 and 5)
**Analysis type:** synthesis-quality (accuracy and source tracing lens)
**Date:** 2026-11-20
**Assigned files:** synth-05-subsystem-work-report-dashboard.md, synth-06-integration-config-perf.md, synth-07-conventions-extension-debt.md
**Fix authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

**Method.** Read all three synthesis files completely. "Traced" means a statement was found in the named research, gap-fill or register file by Grep or Read. "Verified" means I also read the snapshot code or record myself (snapshot `/home/coder/.cache/ic-snap-20261120/master`; design package in the checkout; `.dev/issues/409` records through `git show origin/master:<path>`; read-only `gh pr view --repo IronbellyOrg/IronClaude`). Only read-only shell commands were run (`sed`, `grep`, `wc`, `ls`, `git show`, `gh pr view`). No source, design or synthesis file was modified. Abbreviations: S5 = synth-05, S6 = synth-06, S7 = synth-07, R05 = research 05, GFn = gap-fill n, REG = `gaps-and-questions.md`.

---

## 1. Traced-claims table

### 1.1 synth-05 (44 claims)

| # | Claim in synth-05 (line) | Supporting statement (research / register) | My own read of code or record | Result |
|---|---|---|---|---|
| 1 | Scripts total 5,777 L, 5,971 with SKILL.md; R05 "6,321" wrong (9) | REG G-43 (`gaps-and-questions.md:144`) | `wc -l` of 16 scripts plus SKILL.md = 5,971 | traced, verified |
| 2 | PR #684 merged 2026-11-20T02:01:07Z, d7d645ddd (7) | R05:363 | `gh pr view 684`: MERGED 2026-11-20T02:01:07Z, d7d645dddd | traced, verified |
| 3 | SKILL.md 194 L, run.py 887, common.py 507 (11-14) | R05:21 | `wc -l`: 194, 887, 507 | traced, verified |
| 4 | Test file 4,005 L, 142 `def test_` (21) | R05:596 ("count of definitions") | `wc -l` 4005, `grep -c 'def test_'` 142 | traced, verified |
| 5 | `config.json` 14 keys, `templates/` 7 files (20) | M-14 | `config.json` read: 14 top-level keys; `ls templates` 7 | traced, verified |
| 6 | Step 4b writes two `*-before-exclude.json` copies (41) | R05:95 | not re-read | traced |
| 7 | Lock: budget daily 120 / hourly 10, skip record, exit 3, older lock kept as `stuck` (63) | R05:66 | `run.py:95-131` | traced, verified |
| 8 | Gate `run.py:204-368`, seven checks (63) | R05:75 | `run.py:204-212` lists the 7 names; `:366-368` `sys.exit(0 if ok else 1)` | traced, verified |
| 9 | `clickup.py dm` enforces whole gate; `close` only checks plus sha (63) | REG CC-04 | `clickup.py:619` `deliverable`; `run.py:376-379` `passed()` (skipped when kind is hourly) | traced, verified (hourly bypass not mentioned, minor) |
| 10 | Compare closes only on HTTP 404/410 (63) | R05; REG | `compare.py:40` `NOT_FOUND = ("HTTP 404","HTTP 410","Could not resolve to")` | traced, verified (third pattern omitted here, present in S6; minor) |
| 11 | Detached `python -m http.server 8765 --bind 127.0.0.1 --directory <state>` (74) | R05 s27 | `page.py:318-327` | traced, verified |
| 12 | Wake line "Wake (daily report): run /agent-work-report for today's report." (74) | R05:129 | `waker.py:37` | traced, verified |
| 13 | Entry-file contract `common.py:133-151` (76) | R05:508 area | `common.py:131-138` comment | traced, verified |
| 14 | `move_to_closed` `run.py:483` is the only entry-file writer (82) | R05:508 | `run.py:481-485` (inside the function body) | traced, verified |
| 15 | `refresh` prunes by `info_ttl_days` 14 (85) | R05:340 | not re-read | traced |
| 16 | Waker retries 15 x 120 s, `hourly` recorded skip (86) | R05:130 | `waker.py:39-42`, `:214-221` | traced, verified |
| 17 | `typing_or_fresh` unsafe under 60 s (87) | R05:117 | `orca_term.py:14` `FRESH_OUTPUT_SECONDS = 60` | traced, verified |
| 18 | `settle.sh:1037-1042` prints `ENTRY escalated key=<k> why=surface_absent` (95) | GF3 | `sc-closeout-protocol/scripts/settle.sh:1035-1043` | traced, verified |
| 19 | Master `_TOP_KEYS` rejects `orchestrator_repo` (`cycle.py:216-220`) (96) | R05:325 | `cycle.py:214-220` rejects unknown keys | traced, verified |
| 20 | PR A #686 and PR P #690 open (96) | R05 s19 | `gh pr view`: OPEN, OPEN | traced, verified |
| 21 | Ruling 37 `orchestrator.md:3`; lines 510, 791, 1020, 1021, 1041 (100) | GF1:128 | all six lines read; text matches | traced, verified |
| 22 | `prefs.check_url` accepts only GitHub and ClickUp urls (`prefs.py:20`) (100) | R05:579 | `prefs.py:20` regex `^https://(github\.com|app\.clickup\.com)/\S+$`; `:30-32` `check_url` | traced, verified |
| 23 | Package: 406 files, 20 designs, fixture sha `1f17a907...bd42e4` (137, 139) | R06:25 | `find` = 406 files (no `__pycache__`); `git ls-tree origin/master` = 406; 495eb96d1 is not an ancestor of origin/master | traced, verified |
| 24 | `render.py` 130, `fixtures.py` 122, `canvas.py` 122, `integration-gaps.md` 28 (139-144) | R06:23 | `wc -l`: 130, 122, 122, 28 | traced, verified |
| 25 | `Pillow==13.0.0`, `wcwidth==0.9.4` (144) | R06:23 | `requirements.txt` | traced, verified |
| 26 | `tests/test_designs.py` 19 tests (145) | R06:62 | `grep -c 'def test_'` = 19 | traced, verified |
| 27 | Observer 13 top-level `.py` (6,011 L), schema 158 L (147) | M-4, REG G-41..47 | `ls`/`cat | wc`: 13 files, 6,011; schema 158 | traced, verified |
| 28 | Observer registered `cli/main.py:590-592` (147, 189) | R06 | `main.py:590` import, `:592` `add_command` | traced, verified |
| 29 | 31 worker-list keys parsed (`parse.py:58-90`) (160) | R06 | 31 quoted entries in 58-90 | traced, verified |
| 30 | PR #503 merge 9e2608b03, 2026-11-11T19:54:57Z; 545 files REST; #673 2,831 (137) | R06:56, :94 | `ls-tree origin/master` shows 406 package files | traced, verified (file counts of the PRs not re-run) |
| 31 | Ten variant names `parse.py:750-761`; 19 fixtures: 8 golden + `question-cap-100` (162) | R06:35 | `parse.py:748-762`; fixtures dir has 19 JSON | traced, verified |
| 32 | Code reuse banned: `ARCHITECTURE-SPINE.md:172`, `SPEC.md:76` (162) | R06:45 | `SPEC.md:76` "the design prototype (`canvas.py`) is never imported" | traced, verified (SPINE line not re-read) |
| 33 | Eight palette colours equal (`theme.py:59-69`, `canvas.py:7`) (162) | R06:96 | converted all eight hex values: equal to the observer RGB values | traced, verified |
| 34 | Signal Bridge `view.py:48`; Attention Ledger `view.py:54`; `REDESIGN-SPEC.md:75-76, 78, 82` (166-167) | R06:86-87 | `view.py:48` `LEDGER_TITLE`, `:54` `QUESTIONS_TITLE`; REDESIGN-SPEC AD-1, AD-2, AD-4, AD-8 rows | traced, verified |
| 35 | PR #539 merged 2026-11-14 (189) | R06:274 | `gh pr view 539`: MERGED 2026-11-14T17:41:26Z | traced, verified |
| 36 | `QA.md:19` FAIL for pre-correction snapshots (196) | R06:66 | `QA.md:19` read | traced, verified |
| 37 | `owner-decisions-20261108.md:5-9`, `owner-direction-record-20261116.md:2-5`, `release-gates.md:3,10` (196) | R06:72 | all read through `git show origin/master:`; owner record names an order, not designs | traced, verified |
| 38 | D-1: `commands.py:77-78,183-188`, `collector.py:125-129`, `acceptance-tests.md:25`, `SPEC.md:32`, `release-gates.md:9` (198) | R06:231, GF1 3.8 | all five read; match | traced, verified |
| 39 | About 30 designed verb forms, 4 match a sweep template, none the observer's (205) | GF3:84 | compared with `probes.py:49-62` | traced, verified |
| 40 | FG-1..14 statuses (179) | R06:140-154 | table compared line by line | traced (identical) |
| 41 | Rules status table (175-178) | R06:108-138 | table compared | traced; S1 and S2 flattened (see M-5) |
| 42 | AWR writes `worktree set --unread --comment` (waker only) (71) | R05 | `waker.py:88-96` | traced, verified |
| 43 | `render.py --width` default 116; `NO_COLOR` presence (212) | R06 | `render.py:127-130` | traced, verified |
| 44 | Six statuses and their one-line definitions (52-59) | R05 | `SKILL.md:140` read | traced, verified |

### 1.2 synth-06 (40 claims)

| # | Claim in synth-06 (line) | Supporting statement | My own read of code or record | Result |
|---|---|---|---|---|
| 1 | Observer `_find_orca`: candidates `orca-ide`, `orca`; accepted on exit 0 and topic `orca-cli` (38) | R01 | `install_user_setup.py:36`, `:247-268` | traced, verified |
| 2 | Sweep binary `orca-ide` or `$ORCA_CLI_COMMAND`, "never bare orca" (38) | R04 | `probes.py:43`, `:214-216` | traced, verified |
| 3 | Observer 3 argv shapes, 13 forbidden prefixes (38) | R01 | `adapter.py:29-50`: count = 13 | traced, verified |
| 4 | Sweep 10 templates, 7 verbs, `--include-remote` forbidden (38) | R04 | `probes.py:49-62` | traced, verified |
| 5 | Observer `worker-list --json --limit 100 [--run][--cursor]` (43) | R01 | `adapter.py:173-183` `build_argv` | traced, verified |
| 6 | Sweep `worker-list --run`, `worker-show --dispatch` call sites (46-47) | R04 | `probes.py:1150`, `:1281` | traced, verified |
| 7 | Four templates pinned and not called (zero-argv test) (50-51) | R04 | `test_probes_allowlist.py:624-628`; `probes.py:56-59` comments | traced, verified |
| 8 | AWR `terminal list/read/wait` (52) | R05 | `orca_term.py:24-31`; `sessions.py:291` | traced, verified |
| 9 | AWR `terminal send`, `terminal create` are writes (53) | R05 | `waker.py:186-189`, `:296-303` | traced, verified |
| 10 | AWR `worktree list` read, `worktree set --unread --comment` write (54) | R05 | `sessions.py:308-313`; `waker.py:88-96` | traced, verified |
| 11 | AWR `automations list/runs` (55) | R05 | `run.py:160-164` | traced, verified |
| 12 | AWR `tab list ...` (56) | R05 | `page.py:354-358` | traced, verified |
| 13 | `issue_watch` builds a 12-element `orca agent launch` argv (73) | GF3 | `launch.py:95-100` docstring | traced, verified |
| 14 | WC-16 chain: WC:287-289, "The sweep." WC:110, `commands/sweep.md:47`, `main.py:581-583`, `sweep.md:22` (79) | R04 s6 | `WORKER-CONTRACT.md:289` (also "Phase 1 adds this duty, not a scheduler"), `:110`; `sweep.md:22`, `:47`; `main.py:580-583` | traced, verified |
| 15 | `.gitignore:255-256` ignores `.dev/sweeps/` (80) | R04 | `.gitignore:255` comment, `:256` rule | traced, verified |
| 16 | Snapshot schema root keys (105) | R01 | `snapshot.schema.json:3-9` required list | traced, verified |
| 17 | Sweep names `<stem>.md`, `-2` to `-99` (106) | R04 | `commands.py:29` `MAX_SUFFIX = 99` | traced, verified |
| 18 | `config.json` 14 keys and recorded values (127) | M-14 | `config.json` read (person, orgs, timezone, budgets, prefix match; "07"/"09" are shorthand for "07:00"/"09:00") | traced, verified |
| 19 | `session_tag` read at `waker.py:175, 273, 362`; `person_name` at `classify.py:35, 62`; no read of `clickup_email`/`clickup_user_id` from CONFIG (127) | R05 | my own grep of `CONFIG[` in all scripts: same lines; `clickup.py:559` reads `settings.json`, not CONFIG | traced, verified |
| 20 | `_TOP_KEYS` `cycle.py:58-69` (128) | R05 | `cycle.py:58-62` and `:216-220` | traced, verified |
| 21 | Env vars `ORCA_CLI_COMMAND`, `XDG_STATE_HOME`, `AWR_ROOT`, `AWR_HOOK_FILE`, `AWR_PROJECTS`, `CLICKUP_WORKSPACE_ID`, `GIT_OPTIONAL_LOCKS` (140-147) | R01, R04, R05 | `probes.py:214`, `export.py:236-244`, `common.py:35`, `sessions.py:44,47`, `clickup.py:132`, `probes.py:331-340` | traced, verified |
| 22 | `NO_COLOR`, `COLORTERM`, `TERM` policy (142) | R02 | `terminal.py:92-100` | traced, verified |
| 23 | Observer flags `--once --width --ascii --fixture --run --snapshot --questions` (153-156) | R02 | `commands.py:449-521` | traced, verified |
| 24 | Gate constants `QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED` True (157) | R02 | `commands.py:66-71` | traced, verified |
| 25 | Sweep flags `--run --window --root --output` (158) | R04 | `sweep/commands.py:219-241` | traced, verified |
| 26 | Per-call 10 s, 8 MiB, 2 KiB stderr, 5 calls, 2 s kill grace, cursor 2,048 (169, 231) | R01 | `adapter.py:52-63` | traced, verified |
| 27 | Observer exits 129 SIGHUP, 143 SIGTERM (173) | R02 | `keys.py:115-125` | traced, verified |
| 28 | Sweep exits 0/1/2 and message format (176) | R04 | `sweep/commands.py:279-288` | traced, verified |
| 29 | Questions on: 4 pages = 400 rows; 428 live rows (184) | R01 s12 | `collector.py:32-34` `QUESTION_PAGE_CAP = 4`; `golden-success.json` `total` 428 | traced, verified |
| 30 | `_find_orca` iterates `topics` outside the `try` (187) | R01 | `install_user_setup.py:264-268` (`any(...)` at 268 after the `except`) | traced, verified |
| 31 | `stalled (proved)`, `fenced`, `agent_wait_since` cannot fire on live data (189) | R03, GF1 | `models.py:106-112`; `probes.py:479-481`; `classify.py:196-200` | traced, verified |
| 32 | Transcript tail over 256 KiB forces `could not determine` (191) | R03 | `probes.py:85-89` `TRANSCRIPT_TAIL`; `classify.py:617-629` | traced, verified |
| 33 | Golden sample: `total` 428, `hasMore` true, `nextAction` none 86 / release 14, verdict exited 63 / unverifiable 35 / live 2 (217) | R01 s9 | `golden-success.json` counted with `grep -o`: 428, true, 86, 14, 63, 35, 2 | traced, verified |
| 34 | Question traffic 41 / 66 h / 6 per hour / 181 / about 30 of about 415 (219) | R02:249-250 | record not re-read (research quotes `release-gates.md`) | traced |
| 35 | Full-sweep fixture 9 argv (1 + 2 + 5 + 1) (220) | R04 | `test_probes_allowlist.py:609-619` | traced, verified |
| 36 | Live sweeps 180 rows; #590 264 sessions, 263 undetermined (221, 192) | R03:276-277 | issue not re-read | traced |
| 37 | Observer tests 691, 684, 762; `tests/observe` 36 entries, 26 test files (222) | R02:260-262 | `ls tests/observe`: 36; 26 `test_*.py` | traced, verified |
| 38 | Package sizes 15,653,280 / 13,952,741 / ZIP 14,438,526 (224) | R06 | `ls -l` | traced, verified |
| 39 | Poll 15 s, budget 15 s, backoff cap 60 s, join 5 s; STALE 45 s; key read 0.1 s; redraw 0.5 s (230-232) | R01, R02 | `collector.py:28-34`; `view.py:33-35`; `commands.py:56-61` | traced, verified |
| 40 | AWR limits: 8 repo threads, 6 activity threads, first read 24 h / 30 MB, ClickUp 200 / 400 / 30 d / 10 min, 429 wait up to 65 s, GET 3 retries, page server about 10 s (236-237) | R05 | `collect.py:267`; `activity.py:225`; `sessions.py:48-49`; `clickup.py:40-44, 68, 113`; `page.py:334-341` (20 x 0.5 s) | traced, verified |

### 1.3 synth-07 (42 claims)

| # | Claim in synth-07 (line) | Supporting statement | My own read of code or record | Result |
|---|---|---|---|---|
| 1 | Forbidden set may grow, not shrink (`test_adapter.py:178-192`); only `adapter.py` imports `subprocess` (`test_commands.py:585-601`) (14) | R01, R02 | `test_adapter.py:178-184` (`>=` superset assert); `test_commands.py:583-602`; my grep: only `adapter.py` and `probes.py` import it | traced, verified |
| 2 | Sweep git shapes always `--no-optional-locks`, `core.fsmonitor=false`, `GIT_OPTIONAL_LOCKS=0` (15) | R04 | `probes.py:331-340` | traced, verified |
| 3 | AWR subprocess exceptions `page.py:318`, `sessions.py:119` (16) | R05 s27 | both lines read | traced, verified |
| 4 | `NO_RECORDS`, `SP24_LINE`, `SAFE_TO_CLOSE_LINE` (17, 18) | R04 | `report.py:29`, `:42-49` | traced, verified |
| 5 | Gate constants need a cited record; tests cannot pass on the snapshot (22) | R02, G-07 | `test_commands.py:754-760`; snapshot has no `.dev/` | traced, verified |
| 6 | `RULES` nine `Rule` entries, first match wins (29) | R03 | `classify.py:345-355` | traced, verified |
| 7 | Collector 15 s, backoff 15/30/60 (31) | R01 | `collector.py:28-34`; `test_collector.py:149` `[30.0, 60.0, 60.0, 60.0]` | traced, verified |
| 8 | Sweep classes 8; `SAFE_VALUES`; `PACKAGE_STATES` (43) | R03 | `models.py:50-71` | traced, verified |
| 9 | AWR statuses 6 (44) | R05 | `SKILL.md:140` | traced, verified |
| 10 | FR-9 eight states, mapping in a spec outside the snapshot (45) | GF3:94-96, :232 | `orchestrator.md:572, 648` not re-read | traced (UNVERIFIED stays) |
| 11 | Ninth `CLASSES` entry breaks the unpack at import (55, 13.1 A) | GF4:240 | `classify.py:42-51` unpacks 8 names | traced, verified by reading |
| 12 | `report.py:26-27` use `CLASSES[5]`, `CLASSES[7]` (71) | GF4 | `report.py:26-27` | traced, verified |
| 13 | `class_name` outside `CLASSES` raises KeyError at `classify.py:976` (71) | GF4 | `classify.py:976` `counts[c.classification.class_name] += 1` (dict built from CLASSES not re-read) | traced, partly verified |
| 14 | `ALLOWED_ORCA` comment ":60" "10 templates, 7 verbs (NFR-014)" (72) | R04 | `probes.py:60` | traced, verified |
| 15 | Entry-point signatures: `collect` `probes.py:1322`, `classify` `classify.py:369`, `classify_all` `:880`, `render` `report.py:608`, `to_json` `:613`, `_publish` `commands.py:153`, `build_view` `view.py:968`, observer `render` `render.py:1449`, `Collector.__init__` `collector.py:135`, `read_pages` `adapter.py:395`, `CycleSource` `collector.py:71` (100) | GF4 | all eleven lines read: signatures match | traced, verified |
| 16 | Sweep JSON v1 12 top-level keys (106, 323) | R04 s6.6 | `report.py:613-695` key list read (rows, worktrees, waiting, summary ...); not counted to 12 by me | traced, partly verified |
| 17 | Snapshot path `$XDG_STATE_HOME/superclaude/observe`, else `~/.local/state/...` (107) | R02 | `export.py:236-244` | traced, verified |
| 18 | Four sanitizers, three Orca wrappers (112-113) | R01, R04, R05, M-3 | `adapter.py:224`, `probes.py:214, 266`, `orca_term.py:17-21` | traced (wrappers partly verified) |
| 19 | Shared Orca read: 4 designed forms match a sweep template, none the observer's (114) | GF3:84 | `probes.py:49-62` | traced, verified |
| 20 | Test inventory: 135 render tests, 27 session tests, 28 sweep-command guards, 142 AWR tests (125-134) | R02, R04, R05 | `grep -c 'def test_'`: 135, 27, 28, 142 | traced, verified |
| 21 | `captured-tab-map-*.json` read by no test (136) | R03 | five files exist; grep finds the name only in `SOURCES.md` | traced, verified |
| 22 | `Window.more_text` "no reader" (168) | REG G-40 | `view.py:331, 402` define and set it; tests read it (`test_view.py:586, 605`) | traced; "no reader" is true only of production code (M-4) |
| 23 | `PER_CALL_TIMEOUT` comment possibly stale (172) | REG SD-02 | `adapter.py:60-62` | traced, verified |
| 24 | `agent_wait_since` set nowhere (177) | R03, GF1 | `models.py:111-112`; `probes.py:481` | traced, verified |
| 25 | Waker hourly mode leftover (179) | R05 | `waker.py:8-9`, `:216-220` | traced, verified |
| 26 | SD-06 `orchestrator-mode.md:27` "does not exist yet", "checked 2026-11-08" (206) | REG SD-06 | `orchestrator-mode.md:25-27` read | traced, verified |
| 27 | SD-07/SD-08 `CHANGELOG.md:170`; open item 6 resolved at `orchestrator-mode.md:1003` (207-208) | REG, GF2 | both lines read | traced, verified |
| 28 | CC-04 and CC-05 (220-221) | REG | `clickup.py:619`, `run.py:376-379`, `run.py:788-793` | traced, verified |
| 29 | All 35 SD rows, 5 CC rows, 40 U rows present in 14.4 (200-240) | REG | scripted comparison of REG ids against ids and ranges in synth-07 | traced (see section 3) |
| 30 | Replacement paragraph for the sweep limits (227) | GF2 section 3 | `CHANGELOG.md:170`, `commands.md` 619-621 quotes match GF1 1.4 | traced, verified |
| 31 | C8-1: SPEC:103, :231, :232; `classify.py:196-200` (268) | GF1 1.1 | `git show` SPEC lines 103 and 232 read; `classify.py:196-200` | traced, verified |
| 32 | C8-4/C8-5: `classify.py:479-504`, `:455-476`, `:88-90`; SPEC:106, 274, 338 (271-272) | GF1 1.1, 1.3 | `classify.py:479-493`, `:88-90` read | traced, verified |
| 33 | C8-6 ORCH:3, 510, 791, 1020, 1021, 1041; `settle.sh:1037-1042` (273) | GF1 3.4 | all read | traced, verified |
| 34 | C8-7 ORCH:372, 374, 1018; `cycle.py:216-220` (274) | GF1 | all read | traced, verified |
| 35 | C8-8 `prefs.py:20, 30-32`; `render.py:339, 347` (275) | GF1 3.7 | all read | traced, verified |
| 36 | C8-9 `commands.py:77-78, 183-188, 414`; `collector.py:125-129`; `test_collector.py:675` (276) | GF1 3.8 | all read; `:414` is inside the refusal block (the call is at `:412`) | traced, verified (`:414` imprecise, minor) |
| 37 | 15.1 counts 134 = 40 + 5 + 35 + 2 + 52 (292) | REG section 3 | counted the Type column: 40, 5, 35, 2, 52 | traced, verified |
| 38 | SPEC 653 lines (333) | GF1 | `git show ... | wc -l` = 653 | traced, verified |
| 39 | WC-16 :287-289, "The sweep." WC:110, never-as-worker WC:23, coordinator WC:70 (312, 327) | R04, GF3 | all four lines read | traced, verified |
| 40 | Orchestrator "a standing-grant coordinator and not a worker" ORCH:799 (326) | GF3 | `orchestrator.md:799` | traced, verified |
| 41 | Sweep rule names in glossary (336) | R03 | `classify.py:345-355` | traced, verified |
| 42 | `working` produced since 2026-11-16 (340) | R03, GF1 | `classify.py:251-256`; `test_cli_contract.py:1133-1140` | traced, verified |

## 2. Citation spot-check table (snapshot lines read by me)

Totals (rows; several rows bundle two or more citations): synth-05 20 rows (18 match, 2 partial); synth-06 28 rows (all match); synth-07 16 rows covering more than 40 citations (all match, one imprecise by two lines). No citation was a hard mismatch.

| # | File | Citation as written | What the line holds | Result |
|---|---|---|---|---|
| 1 | S5 | `run.py:483` `move_to_closed` | `:481-485` is inside the function (`entry = dict(entry, closed_at=..., close_reason=...)`, temp file) | match (body line) |
| 2 | S5 | `run.py:204-368` gate | `:204` `REQUIRED_CHECKS`, `:366-368` `sys.exit(0 if ok else 1)` | match |
| 3 | S5 | `common.py:133-151` contract comment | comment opens at `:133` ("The orchestrator's living report"), names `report-entry` | match |
| 4 | S5 | `cycle.py:216-220` | `unknown = set(raw) - _TOP_KEYS` raises "unknown configuration key" | match |
| 5 | S5 | `prefs.py:20`, `:30-32` | `URL` regex GitHub and ClickUp only; `check_url` exits "not an item URL" | match |
| 6 | S5 | `cli/main.py:590-592` | import at 590, `add_command(observe_group)` at 592 | match |
| 7 | S5 | `view.py:134` for `unavailable (no source)` | `:134` is `UNAVAILABLE_FACTS`; the literal is `UNAVAILABLE` at `:113` | partial (cite names the facts tuple; research 06 uses the same cite) |
| 8 | S5 | `page.py:318`, `sessions.py:119` direct subprocess | `subprocess.Popen([... "http.server" ...])` and `subprocess.run(["git","-C",...])` | match |
| 9 | S5 | `waker.py:216-220` hourly skip | `if mode == "hourly": ... "SKIPPED: there is no hourly check"` | match |
| 10 | S5 | `sessions.py:323-330` join fields `tabId, leafId, handle, worktreePath, connected, lastOutputAt` | `:323-330` holds `worktreePath`, `tabId`, `leafId`, `handle`; `connected` is at `sessions.py:370`, `lastOutputAt` at `orca_term.py:68, 118` | partial (see M-3) |
| 11 | S5 | `theme.py:59-69`, `canvas.py:7` palette | `_COLOURS["truecolor"]` eight RGB values equal the eight matching hex values in `PALETTE` | match |
| 12 | S5 | `commands.py:77-78, 183-188` | `QUESTIONS_NEED_LIVE_TEXT`; `if options.fixture: return 2, ...` | match |
| 13 | S5 | `collector.py:125-129` | `FixtureSource.read_questions` returns `FAILED`, `no-question-fixture` | match |
| 14 | S5 | `parse.py:750-761` | `VARIANTS` tuple of ten names | match |
| 15 | S5 | `settle.sh:1037-1042` | `report-entry --help` probe, `ENTRY escalated key=%s why=surface_absent` | match |
| 16 | S5 | `render.py:129` (design package) | `no_color="NO_COLOR" in os.environ` | match |
| 17 | S5 | README.md:9, :44, :46-48 | "design collaboration branch" phrase on line 9; "Previous prototype files are preserved unchanged" at 44; Bubble Tea at 46 | match |
| 18 | S5 | `SKILL.md:140, :183, :172, :22` | status list; "enforced again by `clickup.py dm` and `run.py close`"; `prefs.py answer ... session`; "unanswered 'Needs you' entry stays" | match |
| 19 | S5 | `SPEC.md:32`, `:76` (issue 409 spec) | CAP-1 fixture replay; "`canvas.py` is never imported" | match |
| 20 | S5 | `release-gates.md:3, 9, 10`; `owner-decisions-20261108.md:5-9`; `acceptance-tests.md:25` | read through `git show origin/master:` | match |
| 21 | S6 | `adapter.py:29-50` | templates and 13 forbidden prefixes | match |
| 22 | S6 | `install_user_setup.py:36, 247-270` | `_ORCA_CLIS = ("orca-ide","orca")`; `_find_orca` | match |
| 23 | S6 | `probes.py:43, 214-216` | `ORCA_BINARY_DEFAULT`, `orca_binary()` | match |
| 24 | S6 | `probes.py:1150`, `:1281` | `_call(... "worker-list", "--run", run, "--json")`; `"worker-show", "--dispatch"` | match |
| 25 | S6 | `orca_term.py:24-31`; `sessions.py:291, 309-312` | `terminals()`, `terminal list`, `worktree list` | match |
| 26 | S6 | `waker.py:186-189, 297-302, 88-96` | `terminal create`; `/clear` and wake `send`; `worktree set --unread --comment` | match |
| 27 | S6 | `run.py:160-186` | `automation_runs` begins at 160 | match |
| 28 | S6 | `page.py:354-377` | `tab list` at 354 | match |
| 29 | S6 | `launch.py:95-131` | `launch_argv` returns "the 12-element `orca agent launch` argv" | match |
| 30 | S6 | `test_probes_allowlist.py:609-619`, `:624-638` | `1 + 2 + 5 + 1` argv; zero-argv parametrized test | match |
| 31 | S6 | `collector.py:28-34` | `INTERVAL 15`, `CYCLE_BUDGET 15`, `MAX_BACKOFF 60`, `JOIN_TIMEOUT 5`, `QUESTION_PAGE_CAP 4` | match |
| 32 | S6 | `adapter.py:55-63` | caps 5, 8 MiB, 2048, 10.0, 2.0 | match |
| 33 | S6 | `view.py:33-35`; `commands.py:57-60`; `parse.py:403-405` | `STALE_SECONDS 45`; `READ_TIMEOUT 0.1`, `REDRAW_SECONDS 0.5`; `warnings[:50]` | match |
| 34 | S6 | `questions.py:21-22` | `RETENTION_BOUND 1000`, `WINDOW_ROWS 100` | match |
| 35 | S6 | `keys.py:115-125` | `128 + SIGTERM`, `128 + SIGHUP` | match |
| 36 | S6 | `sweep/commands.py:279-288` | exit 2 usage/binding, exit 1 publish/other | match |
| 37 | S6 | `probes.py:85-89`, `:127-133` | byte limits "proposed"; `Budget(shows=50, total_s=90.0, per_call_s=10.0)` | match |
| 38 | S6 | `classify.py:619-628` | tail incomplete forces `NOTE_TAIL_ONLY` | match |
| 39 | S6 | `collect.py:267-270`, `activity.py:225`, `sessions.py:48-49`, `clickup.py:40-44`, `waker.py:39-42` | 8 threads; 6 threads; 24 h / 30 MB; 200/400/30/10 min; 15 x 120 | match |
| 40 | S6 | `terminal.py:92-116`, `export.py:236-244`, `probes.py:331-340`, `common.py:28-51` | color system; `state_dir`; git argv and env; `AWR_ROOT` | match |
| 41 | S6 | `main.py:581-583`; `sweep.md:22, 47`; `.gitignore:255-256` | sweep registered; "Nothing starts it automatically"; `Skill sc:sweep-protocol`; ignore rule | match |
| 42 | S6 | `install_user_setup.py:265-268` | `topics` iteration after the `try` block | match |
| 43 | S6 | `parse.py:723-728`, `collector.py:155-184` | rows kept with `reobserved=False` | match (723-728 read) |
| 44 | S6 | `commands.py:66-71` | gate constants True | match |
| 45 | S6 | `models.py:106-112`, `probes.py:481` | defaults and "stays unset" comment | match |
| 46 | S6 | `snapshot.schema.json:3-9` | closed, additive-only, "PROPOSED" | match |
| 47 | S6 | `commands.py:29` | `MAX_SUFFIX = 99` | match |
| 48 | S6 | `golden-success.json` / `test_golden_contract.py:43-58` | 428, hasMore true; `reported_total == 428` | match |
| 49 | S7 | `adapter.py:29-50`; `test_adapter.py:178-192`; `test_commands.py:585-601` | forbidden set, superset assert, subprocess-import test | match |
| 50 | S7 | `probes.py:49-62`, `:60` | `ALLOWED_ORCA`; comment "10 templates, 7 verbs (NFR-014)" | match |
| 51 | S7 | `classify.py:42-51`, `:345-355`, `:130-134`, `:976`, `:958-961` | eight-name unpack; nine `Rule`s; `_classification`; `counts[...]`; `if forced` | match (":958-961 tested in two places" reads as one tuple test plus the `forced` branch; wording loose) |
| 52 | S7 | `report.py:26-29`, `:42-49` | `CLASSES[5]`, `CLASSES[7]`, `NO_RECORDS`, `SP24_LINE`, `SAFE_TO_CLOSE_LINE` | match |
| 53 | S7 | `models.py:50-71`, `:106-112` | classes, package states, `SAFE_VALUES`; reserved fields | match |
| 54 | S7 | `classify.py:196-200`, `:251-256`, `:479-493`, `:88-90` | exit-proof conditions; rule 5; `safe_to_close`; `REASON_NOT_OBSERVABLE` | match |
| 55 | S7 | `view.py:331, 402`; `adapter.py:60-62`; `waker.py:8-9` | `more_text`; timeout comment; hourly note | match |
| 56 | S7 | `clickup.py:619`; `run.py:376-379`; `run.py:788-793` | `deliverable`; `passed`; "Other work in progress" | match |
| 57 | S7 | `prefs.py:30-32`; `render.py:339, 347` | `check_url`; `answered_since`, `startswith(SESSION_URL) and u not in done` | match |
| 58 | S7 | `commands.py:77-78, 183-188, 414` (observe) | `:414` sits inside the refusal block; the call is at `:412` | imprecise by 2 lines (M-6) |
| 59 | S7 | `core/WORKER-CONTRACT.md:23, 70, 110, 287-289` | never-as-worker list; coordinator definition; "The sweep."; WC-16 | match |
| 60 | S7 | `orchestrator-mode.md:27, 609, 1003`; `CHANGELOG.md:170`; `models.py:162-164` (via S5) | dated fact; "copied from #409 at 495eb96d"; open item 6 resolved; changelog line; nine dimensions comment | match |
| 61 | S7 | `orchestrator.md:3, 372, 374, 510, 791, 799, 930, 1018, 1020, 1021, 1041` | all read | match |
| 62 | S7 | `cycle.py:58-62` and `:216-220` | `_TOP_KEYS` frozenset; rejection | match |
| 63 | S7 | `test_cli_contract.py:1133-1140`; `test_commands.py:754-760`; `test_collector.py:675` | working test; gate-record test; `no-question-fixture` assert | match |
| 64 | S7 | `.gitignore:255-256`; SPEC (653 lines) | comment and rule; `wc -l` 653 | match |

## 3. Synthesis Quality Review checklist (9 items) and extra checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Section headers match the template | PASS (minor notes) | S5 5.5 and 5.6 carry Purpose, Key Files, How It Works, Public Interface, Dependencies, Consumers, Conventions & Patterns in template order. S6 uses 8.1-8.3, 9.1-9.3, 10.1-10.3, 11.1-11.3 as in the template; sections 6 and 7 are conditional and are collapsed to "N/A" plus tables without 6.1-6.4 headers. S7 has 12.1-12.3, 13.1-13.2, 14.1-14.3, 15.1-15.2, 16; it adds 14.4-14.6 and titles the appendix "Appendix: Document Provenance" (template: "Appendix A: [Title]") (M-8) |
| 2 | Table column structure | PASS with minor deviations | Deviations: S6 8.1 (Tool, Binary, Verb, Purpose, Status, Source instead of Endpoint, Method, Purpose, Request Shape, Response Shape); S6 11.1 "Value" for "Measured Value"; S6 11.2 "Value" for "Optimization"; S7 12.1 "Evidence" for "Example"; S7 14.2 "Research label" and "Evidence" for "Severity" and "Effort to Fix" (S7 line 164 discloses this and gives the reason). All other tables match the template (M-8) |
| 3 | No fabricated content | PASS | 126 claims traced (sections 1.1-1.3); the large majority also read by me in code or records (rows marked "traced" only are listed as such); none untraceable |
| 4 | Findings cite paths and evidence | PASS | every row in S5 to S7 carries a file:line or record citation; vague "the system uses X" statements: none found |
| 5 | Depth budget | PASS | S5 5.5 is 129 lines (complex tier 120-200); S5 5.6 is 90 lines (standard tier 80-120). S6 and S7 are section groups, not subsystem sections; S7 states it exceeds its 160-line brief and why (line 4) |
| 6 | Architecture backed by code-traced evidence | PASS | built-versus-designed split verified: PR #684 merged, #686 and #690 open, `orchestrator` package absent (`main.py` registers only observe and sweep; `settle.sh:1037-1042` probes the absent verb) |
| 7 | Cross-references consistent | PASS with a note | counts agree across S5, S6, S7 (5,777; 14 config keys; 10 and 3 templates; 31 and 20 attributes; 19 fixtures; 406 files). S6 uses the ids DC-01 and DC-02 for the two defect candidates while S7 uses C8-8 and C8-9 and never prints DC-01 or DC-02 (M-2) |
| 8 | No doc-only claims in Architecture or API sections | PASS | every design-only fact is tagged: S6 8.1 "[DESIGN-ONLY]"; WC-16 binding, FR-9 mapping, Orca automations and the orchestrator repo carry UNVERIFIED in S5 and S7 |
| 9 | Stale, contradicted, UNVERIFIED items and C8 candidates carried into Section 14 | **FAIL** | Register: all 134 ids are present in S7 by id or range except DC-01, DC-02 (carried as C8-8, C8-9), G-13, G-38, G-40 (content present, id not printed). All 35 STALE DOC rows, 5 CODE-CONTRADICTED rows, 40 UNVERIFIED rows and 9 C8 rows are in S7. Two UNVERIFIED items that the research files tag inline are in no row of Section 14: see B-1 |
| X1 | Orca verb inventory (S6 8.1) against research | PASS | every verb of R01, R04, R05 is listed with the right binary, allowlist status and file:line; design verbs match GF3 rows 1-34; the four token-for-token matches (`worker-show`, `worker-list --run`, `task-list --run`, `worktree current --json`) agree with GF3:84 and with `probes.py:49-62`; none match the observer's three templates |
| X2 | Live versus designed | PASS | no designed-only item is described as built. `report-entry`, `src/superclaude/cli/orchestrator/`, `/sc:orchestrator`, `sc-orchestrator-protocol` are described as designed or absent; reader side of the living report is described as built and fake-tested only |
| X3 | C8 wording | PASS with a note | no DEFECT-CANDIDATE was relabelled to a plain known gap. The three sweep limits and the writer and route are labelled KNOWN LIMIT (cited) with the citing lines printed (checked: SPEC:103, 106, 231, 232, 238, 251, 274, 338 through GF1 1.1 and `git show`; DESIGN:493, 636, 841, 877; ORCH:3, 510, 791, 1018-1021, 1041). The two defect candidates (C8-8, C8-9) keep the label and print the exact words "Remediation task not created (read-only brief); flagged for the owner" in S5 (100, 198), S6 (3, 186, 194) and S7 (275, 276). The exact words are absent from C8-4, C8-5 and C8-7, which S7's own rule 4 (line 262) would require for a limit with no tracked owner (M-1) |
| X4 | Neutrality | PASS | grep for should, recommend, suggest, unif, consolidat in the three files: every hit is a field name ("recommend" part of the work report), a statement that the sweep recommends nothing, a disclaimer, or the phrase "facts only; no unification recommendation". The "Unification touch points" list (S7 102-119) states facts with citations in all 14 rows |
| X5 | Scope-limit statements and contradictions | PASS | the C1-C6 contradiction table (S5 187-194) matches R06 section 7; the two-reasons problem of `CHANGELOG.md:170` versus SPEC:232 is stated and the GF2 replacement paragraph is carried verbatim (S7 227) |

## 4. Findings

### Blocking

**B-1 (blocking) Section 14 omits two UNVERIFIED items that the research files tag inline** (synth-07, section 14.4 B, lines 229-240).

- Evidence: (a) R01:52 states "Both error-code names come from Orca's own envelope; the file does not say where the names were verified. [UNVERIFIED against a live Orca ...]". The names are `consumer_fenced` and `no_active_terminal` (`adapter.py:65-69, 496-507`). 14.4 B never lists them as UNVERIFIED; `grep -i 'error-code' synth-07` finds only the appendix row that names the research file. S6 10.1 (line 172) presents them as fact without a tag. (b) R05:571-572 (and GF3:185-186, design O1 and O3/O4) tag the Orca automation `orchestrator-poll` (`*/5 * * * *`) and the repo `IronbellyOrg/IronOrchestrator` as "[UNVERIFIED] outside the repo". They are in S5 line 97 only. 14.4 B row "U-17 to U-23" names `coordinator-morning-wake` and `coordinator-missed-check` but not `orchestrator-poll` or the repo. `grep -n 'orchestrator-poll\|IronOrchestrator' synth-07 gaps-and-questions.md` returns nothing.
- Why blocking: the requester's checklist item 9 and Gate 1 M-17 require every UNVERIFIED item of the six research files to reach Section 14. The register states it did not harvest inline body tags (`gaps-and-questions.md`, "How to read this file", last bullet), which is how these two slipped through. All other inline items I compared (R01 lines 177, 222, 286, 288, 348-351, 357; R02 169, 202, 251, 266, 272, 283, 289-290; R03 221, 287-295; R04 270-271; R05 27, 30, 146, 313, 326, 344, 380, 540, 546, 583-595; R06 62, 270-278; GF2, GF4, GF5 and the rest of GF3) are present.
- Required fix: add to 14.4 B (a) to the "Observer constants, tests, versions" row: "the Orca error-code names `consumer_fenced` and `no_active_terminal` (envelope `error.code`) are not shown to be verified against a live Orca (R01:52; `adapter.py:65-69, 496-507`)"; (b) to the "Report skill and orchestrator environment" row: "the Orca automation `orchestrator-poll` (`*/5 * * * *`) and the repo `IronbellyOrg/IronOrchestrator` are outside the repo and not checked (R05:571-572; GF3:185-186; design O1, O3, O4)". Optionally add "[UNVERIFIED]" to the S6 10.1 row.

### Minor (notes only; none fails the gate)

**M-1** synth-07 14.5, rows C8-4 (line 271), C8-5 (272), C8-7 (274) print only "Flagged for the owner." The exact sentence "Remediation task not created (read-only brief); flagged for the owner" is required by S7's own rule 4 (line 262) for a KNOWN LIMIT whose cited text names no tracked owner. C8-5 says "No later work named" and C8-4 says "no `yes` source stated", so both qualify; C8-7 has a tracked owner (PR A #686) and is fine. Fix: use the full sentence in C8-4 and C8-5.

**M-2** synth-07 never prints the register ids DC-01 and DC-02 (it uses C8-8, C8-9, "D-1") and does not print G-13, G-38, G-40, although S6 uses DC-01 and DC-02 (lines 3, 186, 194). The content of all five is present (14.4 A replacement paragraph for G-13 and G-38; 14.2 for G-40). Fix: add "(DC-01)" and "(DC-02)" to the C8-8 and C8-9 rows.

**M-3** synth-05 line 72 cites `sessions.py:323-330` for six join fields. Lines 323-330 hold `worktreePath`, `tabId`, `leafId`, `handle`; `connected` is read at `sessions.py:370` and `lastOutputAt` at `orca_term.py:68, 118`. The fields exist; the range is too narrow. The same range is in REG G-49 and synth-07 line 250.

**M-4** synth-07 14.2 `Window.more_text` "no reader": production code does not read it, but `tests/observe/test_view.py:586, 605` do. Say "no production reader".

**M-5** synth-05 lines 175-176 file S1 and S2 under BY ABSENCE only; R06's rule table gives S1 "BY ABSENCE + ENFORCED" and S2 "PARTLY / BY ABSENCE" (R06:111-112), and S5 line 171 says the rule table is the stronger evidence.

**M-6** Moved or loose line numbers on true claims: synth-07 C8-9 `commands.py:414` (refusal call at `:412`); synth-05 `view.py:134` (the `unavailable (no source)` literal is `UNAVAILABLE` at `view.py:113`; `:134` is the facts tuple that renders as unavailable); synth-05 `run.py:483` points into the body of `move_to_closed`.

**M-7** synth-05 line 63 gives the close rule as "HTTP 404/410"; `compare.py:40` also treats "Could not resolve to" as closed (S6 8.3 has it). Line 63 also says `run.py close` enforces checks plus sha; for an hourly run `run.py:376-379` skips the check entirely.

**M-8** Template column and heading deviations listed in checklist rows 1 and 2. S7 line 164 discloses the 14.2 change; the others are not disclosed.

### Notes (not findings)

- C8-6 rests on a judgment (a PR-sequencing line is read as a cited decision). The synthesis states the judgment, the flip condition and that no fact changes (S5 100; S7 273, G-35). I found the cited ORCH lines say what is claimed (ORCH:510 "package, new, PR B", ORCH:1020 PR B contents), so the label follows rule R-C8 step 1 as written in GF1.
- S7 14.6 repeats R03's note that one scratch copy of the SPEC was written to `/tmp`; GF1 states it wrote none. This is surfaced for the owner, not a defect of the synthesis.
- I did not re-run the research claims that rest on live reads that cannot be repeated from the snapshot (issue #590 body, issue #534 comments, `release-gates.md` question traffic figures, PR file counts of #503 and #673). They are marked "traced" only.

## 5. Verdict

**FAIL: 1 blocking finding (B-1), 8 minor findings.** Partition B (synth-05, synth-06, synth-07) is accurate and well sourced: 126 claims traced (the large majority also re-read by me in code or records), 64 citation rows covering well over 100 individual citations checked with no hard mismatch, neutrality and live-versus-designed accuracy hold. The single blocking defect is the omission of two inline UNVERIFIED items from Section 14. The fix is two added clauses in synth-07 14.4 B.
