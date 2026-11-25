# QA Report - Gate 3, lens: code-example-accuracy

**Status:** Complete
**Topic:** Observer, Sweep and Dashboard technical reference
**Date:** 2026-11-20
**Phase:** report-validation (domain lens: code-example-accuracy), fix authorization: false
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Snapshot:** /home/coder/.cache/ic-snap-20261120/master

---

## Snippet / reference table (appended as verified)

Doc location = line in the assembled document. Source paths are relative to the snapshot root. "Identical" = the text, signature, flag, constant or value in the document equals what the source says at the cited place (yes / NO / yes-minor = true claim with a moved or imprecise line number).

### A. Observer (`src/superclaude/cli/observe/`)

| # | Snippet or reference | Doc location | Source path:line read | Identical |
|---|---|---|---|---|
| 1 | `skills list --json` (`DISCOVERY_TEMPLATE`), exact-match check | L445 | adapter.py:30, 148-149 | yes |
| 2 | `orchestration worker-list --json --limit 100 [--run <id>] [--cursor <c>]`, pairs in that order, each once | L446, L1152, L1360 | adapter.py:29, 127-170, 173-183 | yes |
| 3 | `orchestration check --all --types question --run <id> --json` (8 tokens), `_is_question_shape` | L447, L1153 | adapter.py:32, 111-118, 186-190 | yes |
| 4 | `FORBIDDEN_PREFIXES` = 13 prefixes (check, --ack, --wait, --retry-request, --peek, dispatch, inbox, run-use, run-create, send, ask, reply, reset) | L451, L1360 | adapter.py:34-50 | yes |
| 5 | Question shape exempts token indexes 1, 4, 6 | L451 | adapter.py:121-126 | yes |
| 6 | `RUN_ID_PATTERN` `^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$` (PROPOSED) | L449 | adapter.py:52-54 | yes |
| 7 | `CURSOR_MAX_BYTES = 2048`; cursor non-empty str, no leading `-`, no NUL | L449 | adapter.py:55, 98-108 | yes |
| 8 | `MAX_CALLS_PER_CYCLE` 5, 8 MiB, 2 KiB stderr, `PER_CALL_TIMEOUT` 10.0, kill grace 2 s | L455-458, L1330 | adapter.py:57-63 | yes |
| 9 | `_ERROR_CODES` `consumer_fenced`, `no_active_terminal` -> `consumer-fenced`, `no-active-terminal` | L485, L1279 | adapter.py:65-69, 503-507 | yes |
| 10 | `LiveSource.read_pages(clock, budget_deadline, run_id=None, max_calls=MAX_CALLS_PER_CYCLE) -> SourceResult` (:395) | L502 | adapter.py:395-401 | yes |
| 11 | `read_questions(clock, budget_deadline, run_id) -> SourceResult` (:469) | L502 | adapter.py:469-471 | yes |
| 12 | `SourceResult(state, pages, code, diagnostic, capped, calls)` | L502 | adapter.py:318-325 | yes |
| 13 | `build_argv(orca, run_id=None, cursor=None)`, `build_question_argv(orca, run_id)`, `assert_allowed(argv)`, `check_run_id`, `check_cursor`, `ArgvRejected` | L503 | adapter.py:173, 186, 135, 92, 98, 72 | yes |
| 14 | Cycle codes `not-found`, `timeout`, `overrun`, `output-cap`, `spawn-error`, `exit:<n>`, `json`, `cursor-rejected`, `cursor-stalled`, `empty-page` and their line cites (:403, :409-411, :296-305, :422-430) | L476-484 | adapter.py:403, 409-411, 296-305, 413-466 | yes |
| 15 | `Collector(source, clock, interval=15.0, budget=15.0, max_backoff=60.0, run_id=None, questions=False, link=False)` (:135-145) | L504, L1632 | collector.py:28-30, 135-145 | yes |
| 16 | `run_once() -> CycleResult`, `latest()`, `start()`, `stop()` | L504 | collector.py:248, 177, 335, 353 | yes |
| 17 | `CycleSource` protocol (`mode`, `variant`, `available`, `namespace`, `read_pages`, `read_questions`) | L504 | collector.py:71-89 | yes |
| 18 | `QUESTION_PAGE_CAP` 4 (4 + 1 message call); `INTERVAL` 15, `CYCLE_BUDGET` 15, `MAX_BACKOFF` 60, `JOIN_TIMEOUT` 5 | L459-460, L1329 | collector.py:28-34, 273 | yes |
| 19 | Daemon thread name `observe-collector`; `_loop` ends on NOT_AVAILABLE; backoff doubling 15->30->60->60 | L471, L1129, L1377 | collector.py:306, 340-351 | yes |
| 20 | `FixtureSource.read_questions` always FAILED `no-question-fixture` | L486, L622, L1608 | collector.py:125-129 | yes |
| 21 | Question failure leaves rows and backoff untouched ("collector.py:290") | L1279 | collector.py:290-293, 205-245 | yes |
| 22 | `UNKNOWN` singleton (parse.py:43) | L419, L1363 | parse.py:25-43 | yes |
| 23 | `_FIELDS` = 31 keys (parse.py:58-90); 7 `resource.*`, `workspace.id/.kind`, `stage.activity/.detail` unexported = 11; 20 exported | L419, L466, L490 | parse.py:58-90; export.py:25-47 | yes |
| 24 | `parse_page` strict envelope (`result`, `workers`, `page`, `hasMore` bool), `ShapeError` | L465, L1376 | parse.py:365-407 | yes |
| 25 | warnings capped at 50 | L1331 | parse.py:403-405 | yes |
| 26 | `_clean_json` depth 6 | L493 | parse.py:277-290 | yes |
| 27 | ms heuristic `> 1e11` (parse.py:247) | L1509, L1565 | parse.py:246-247 | yes-minor (condition on :246, PROPOSED comment on :247) |
| 28 | `Question` identity = Run + `message.id` (parse.py:416-418) | L1404 | parse.py:415-421 | yes |
| 29 | `merge_questions`, `RETENTION_BOUND` 1000, `WINDOW_ROWS` 100, `window_is_full` (questions.py:21-22, 125-129) | L421, L461 | questions.py:21-22, 81-142 | yes |
| 30 | `STALE_SECONDS = 45.0` (view.py:33-35) | L422, L462 | view.py:33-35 | yes |
| 31 | `source_state` OK/PARTIAL -> STALE at 45 s (view.py:456-463) | L470 | view.py:456-463 | yes |
| 32 | `source.status` mapping OK/STALE/FAILED->ERROR/else UNKNOWN (view.py:667) | L470 | view.py:667 | yes |
| 33 | `KEY_NAMES` (up, down, enter, escape, backspace, ctrl_c, text) (view.py:30) | L572, L645 | view.py:30 | yes |
| 34 | `apply_key` key map rows (ctrl-c, q, k/j, d/u, enter, esc, `/`, h, e, m, n/p) | L574-582 | view.py:1246-1300 | yes |
| 35 | `INSPECTOR_SCROLL_STEP` = 3 | L578 | view.py:131 | yes |
| 36 | `Session` fields list (view.py:151-168) | L1118 | view.py:151-168 | yes-minor (list omits `selected_row`, `mark_wall_time`) |
| 37 | `build_view(result, session, clock) -> View`, "the only `View` constructor" | L626, L1366 | view.py:968, 1104; grep `View(` shows one constructor | yes |
| 38 | `apply_cycle(session, result, clock) -> Session`; `Effect` NONE/EXPORT/QUIT | L626 | view.py:1174, 1162-1167 | yes |
| 39 | `render(view, policy, message=None) -> Group` (:1449); `screen_lines(view, policy, message=None) -> list[str]` | L626, L1632 | render.py:1449, 1248-1255 | yes |
| 40 | `KeySource(fd=None)` | L626 | keys.py:36-43 | yes |
| 41 | `QUESTION_GATE_PASSED = True`, `QUESTION_LINK_PASSED = True` (:67, :70) | L596, L1262 | commands.py:67, 70 | yes |
| 42 | `_questions_on`, `_link_on` | L596, L621 | commands.py:173-180 | yes |
| 43 | `_question_refusal` exit 2 (fixture / no run / bad run id), exit 1 (gate False) | L569, L622 | commands.py:77-78, 183-197 | yes |
| 44 | Flags `--once`, `--width {160,116,80}`, `--ascii`, `--fixture <name>`, `--run <id>`, `--snapshot <file>`, `--questions` | L551-559, L1261 | commands.py:449-496 | yes |
| 45 | `observe_group(ctx, once, width, ascii_mode, fixture, run_id, snapshot, questions)` | L625 | commands.py:498-507 | yes |
| 46 | `Options` frozen, seven fields; `Deps` (:132-147) | L625, L1453 | commands.py:121-147 | yes |
| 47 | `execute(options, deps=None) -> int`; `run_loop(collector, keys, screen, clock, *, make_policy, directory, snapshot_file, write_snapshots) -> int` | L625 | commands.py:412, 306-316 | yes |
| 48 | `READ_TIMEOUT` 0.1, `REDRAW_SECONDS` 0.5 | L1331 | commands.py:57-60 | yes |
| 49 | Exit codes 0/1/2 and cites (:264-268, :364-369, :187-196, :377-387) | L565-569, L1280 | commands.py:264-268, 364-369, 183-197, 377-387 | yes |
| 50 | Exit 143 / 129 (keys.py:119-125); SIGINT (keys.py:115-117) | L567, L570 | keys.py:115-125 | yes |
| 51 | Width classes `MIN_WIDTH` 80, `MIN_ROWS` 8, 160 / 116, refusal strings (terminal.py:21-24, 82-89) | L584 | terminal.py:21-27, 82-89 | yes |
| 52 | `NO_COLOR`, `COLORTERM`, `TERM` colour policy (terminal.py:92-116) | L1250 | terminal.py:92-124 | yes |
| 53 | `sanitize.py` drops Cc/Cf/Cs and all escape forms | L258, L1358 | sanitize.py:15-24, 41-48 | yes |
| 54 | Eight palette colours equal (`theme.py:59-69` vs `canvas.py:7`) | L258, L1054, L1196 | theme.py:59-69 (hex of rgb values) vs canvas.py:7 PALETTE: ink, muted, line, warn, accent, good, bad, frozen all equal | yes |
| 55 | `_find_orca` tries `orca-ide` then `orca`, `skills list --json`, timeout 10, topic `orca-cli` (install_user_setup.py:36, 247-270); `any(...)` outside the `try` (:265-268) | L426, L499, L1147, L1507 | install_user_setup.py:36, 247-270 | yes |
| 56 | `SCHEMA_VERSION = 1`, `SNAPSHOT_NAME` (export.py:20-21) | L489 | export.py:20-21 | yes |
| 57 | `_TEXT_FIELDS` (19 pairs) and `_ANY_FIELDS` (export.py:25-47); skeleton C `("<jsonKey>", "<row_attr>"),` | L490, L1438-1439 | export.py:25-47 | yes (skeleton conforms) |
| 58 | `state_dir` `$XDG_STATE_HOME/superclaude/observe` else `~/.local/state/...` (export.py:236-244) | L495, L310 | export.py:236-244 | yes |
| 59 | `write_atomic` mkdir 0700, mkstemp, fsync, `os.replace`, unlink on failure | L495 | export.py:257-274 | yes |
| 60 | Record name `observe-<generatedAt ":"->"-">.txt` (export.py:247-250) | L322, L1296 | export.py:247-250 | yes |
| 61 | Record lines carry question subject, not payload (view.py:811; export.py:103-111) | L492 | view.py:805-819; export.py:103-111 | yes |
| 62 | Snapshot schema closed on listed nodes, `schemaVersion` const 1, `counts` scalar values (schema :50), `source.status` enum | L489, L493, L1211 | snapshot.schema.json:3-9, 27, 50, 106-155 | yes |
| 63 | `main.py:590-592` observe registration | L217, L272, L543 | main.py:590-592 | yes |
| 64 | Test pins: `test_adapter.py:178-192`, `test_commands.py:585-601`, `test_commands.py:754-779` | L418, L451, L596 | test_adapter.py:178; test_commands.py:585-601, 754-779 | yes |
| 65 | `golden_release1_records.json`, `golden_release1_surface.json`; `WITHHELD_QUESTION_KEYS`; privacy keys list | L526, L1421-1422 | tests/observe (Glob); test_snapshot_schema.py:269-272, 424 | yes |
| 66 | `launch.py:148-152` documents the `topics` hole (U-03 corroboration) | L1507 | issue_watch/launch.py:144-153 | yes |

### B. Sweep (`src/superclaude/cli/sweep/`, command, skill, contract)

| # | Snippet or reference | Doc location | Source path:line read | Identical |
|---|---|---|---|---|
| 67 | `ALLOWED_ORCA` = 10 templates, 7 verbs, comment ":60" "10 templates, 7 verbs (NFR-014)" | L799-808, L1147, L1419 | probes.py:49-60 | yes |
| 68 | `FORBIDDEN_TOKENS` = `--include-remote` | L797 | probes.py:62 | yes |
| 69 | `<run>` = `run_[0-9a-f]{12}`, `<dispatch>` = `ctx_[0-9a-f]{12}` | L797, L1649 | probes.py:46-47, 91 | yes |
| 70 | `ALLOWED_GIT` four shapes: `status --porcelain=v1 -z --branch --untracked-files=all --ignore-submodules=all`, `config --show-origin --list -z`, `ls-files -z`, `check-attr --stdin -z filter` | L812 | probes.py:68-80 | yes |
| 71 | git seam prefix `git --no-optional-locks -C <cwd> -c core.fsmonitor=false`, env `GIT_OPTIONAL_LOCKS=0` (probes.py:331-340) | L812, L1255, L1361 | probes.py:324-340 | yes |
| 72 | `orca_binary()` = `$ORCA_CLI_COMMAND` else `orca-ide`; "never bare orca (SPEC section 8, INV-017)" | L228, L797, L1248 | probes.py:43, 214-216 | yes |
| 73 | `Budget(shows=50, total_s=90.0, per_call_s=10.0, clock=time.monotonic)` | L858 | probes.py:124-133 | yes |
| 74 | Byte limits: output 8 MiB, contract and ledger 1 MiB, ledger split 512 KiB, transcript tail 256 KiB, `WORKER_LIST_PAGE` 100 (probes.py:85-89) | L816-823, L1333 | probes.py:85-89 | yes |
| 75 | `ORCA_VERSION_FILE` `/opt/Orca/resources/app.asar.unpacked/out/package.json` | L820, L1496 | probes.py:83 | yes |
| 76 | `collect(ctx, runs, root, budget) -> SweepInput` (probes.py:1322) | L857, L1632 | probes.py:1322-1324 | yes |
| 77 | `bind_run(budget) -> str` | L858 | probes.py:397 | yes |
| 78 | `check_orca_argv(args)` / `check_git_args(args)` raise `ValueError` | L859 | probes.py:226-244 | yes |
| 79 | Call sites: run-current :399, worker-list :1150, `task-list --ready` :1165, `task-list` :1178, worker-show :1281, `worktree ps --json` :1335 | L801-806, L1154-1158 | probes.py:399, 1150, 1165, 1178, 1281, 1335 | yes |
| 80 | `parse_worker_show` (:471-515); `agent_wait_since` unset (:481); `agentWait` from `observation` else `terminal` | L731, L733, L1146 | probes.py:458-481; models.py:97-112 | yes |
| 81 | `_orca` (:266), `_git` (:315), `Budget` (:124) | L780 | probes.py:266, 315, 124 | yes |
| 82 | Result kinds `ok`, `no_binding`, `unavailable`, `call_failed` | L810, L1281 | probes.py:112-118, 254-312, 369-394 | yes |
| 83 | `models.CLASSES` (8 strings), (50-59) | L665, L695, L1389 | models.py:50-59 | yes |
| 84 | `PACKAGE_STATES` (62-69), `SAFE_VALUES` (71) | L665, L725 | models.py:62-71 | yes |
| 85 | `JSON_SCHEMA_VERSION = 1` | L1264, L1367 | models.py:18 | yes |
| 86 | `worker_done_seen` / `fenced_evidence` defaults `None` / `"unreadable"` (models.py:108-109) | L731 | models.py:108-109 | yes |
| 87 | `SessionRow` dimension comment "The #409 dimensions, nine fields ... report-only, never JSON keys" (models.py:162-164) | L1085 | models.py:162-164 | yes (ellipsised quote) |
| 88 | `RULES` = 9 `Rule(name, fn)` entries (classify.py:345-355) and the nine rule names | L681-691, L742 | classify.py:345-355 | yes |
| 89 | Rule 1 firing condition and decline note | L683 | classify.py:161-188 | yes |
| 90 | Rule 2 `orca_exit_proof` (liveness exited, transcript not unreadable, `worker_done_seen is False`, `fenced_evidence == "absent"`) | L684, L1600 | classify.py:191-216 | yes |
| 91 | Rule 3 `fenced` needs `"present"` (classify.py:219-223) | L685, L1601 | classify.py:219-223 | yes |
| 92 | Rule 4 `waiting_signal` (a) `agent_wait` not None, (b) failed + freeze code, (b) `status == "ready"` (classify.py:226-248; :229-235) | L686, L1602 | classify.py:226-248 | yes |
| 93 | Rule 5 `working` (live, `in_progress`, `agent_wait_present is True`, `agent_wait is None`; `dispatch.status` not tested) (:251-269) | L687, L1540 | classify.py:251-269 | yes |
| 94 | Rule 6 `finished` (`guard refused:` first line, or settled + parsed contract; note partial) | L688 | classify.py:272-292 | yes |
| 95 | Rule 7 `idle`, Rule 8 `person_active` conditions | L689-690 | classify.py:295-327 | yes |
| 96 | Rule 9 `fallback` evidence text and "no contract read" note | L691 | classify.py:330-342, 86 | yes (note text is a prefix of `NOTE_NO_CONTRACT`) |
| 97 | `classify(row: SessionRow, ctx: SweepContext) -> Classification` (:369) and the second call of rules 1 and 2 at :378 | L693, L740 | classify.py:369-386 | yes |
| 98 | `classify_all(inp: SweepInput, ctx: SweepContext) -> SweepResult` (:880) | L741 | classify.py:880 | yes |
| 99 | `Rule(name: str, match: Callable[[SessionRow, SweepContext], Classification \| None])` | L742 | classify.py:155-158 | yes |
| 100 | `_classification(class_name, rule, evidence, waiting_kind=None, notes=()) -> Classification` (:130) | L743, L1432 | classify.py:130-143 | yes |
| 101 | `safe_to_close(row, worktree: WorktreeState \| None) -> SafeToClose`; `removable(worktree) -> tuple[str, str]` (479, 455) | L744 | classify.py:455, 479 | yes |
| 102 | `package_state` (423-429), `_REMOVAL_BLOCKING_STATES` | L725 | classify.py:408-429 | yes |
| 103 | `JOIN_PATH = "B"` (classify.py:40); read in `_guard` (745) | L713-714, L1264 | classify.py:40, 745 | yes |
| 104 | Key-files line "`_guard` 728" | L664 | classify.py:728 is the `@dataclass` of `_Guard`; `def _guard` is :741 | yes-minor (wrong line, true claim) |
| 105 | Unpack of `CLASSES` into eight names (classify.py:42-51) | L766, L1401, L1419 | classify.py:42-51 | yes |
| 106 | `class_name` not in `CLASSES` raises `KeyError` at :976; `idle`/`person_active` suffix test at :958 | L1419 | classify.py:958, 976 | yes |
| 107 | `_force_unknown` (358-366); `_contract_for` (570; docstring :575); `_window` (548-558); `_merge_group` (512-525); `_join_path_b` (609); `_person_origin` (760) | L664, L706, L713 | classify.py:358, 570-575, 548-558, 512, 609, 760 | yes |
| 108 | `CHECKED_ORCA_VERSION = "1.4.245"` (report.py:23); `CELL_MAX` 200 | L239, L1264 | report.py:23-24 | yes |
| 109 | `NO_RECORDS`, `SP24_LINE`, `SAFE_TO_CLOSE_LINE`, "Messages coverage: partial", "creator not observable in Phase 1", "not an assurance of completeness" (report.py:29, 42-49, 199, 302) | L1363-1364 | report.py:29, 42-49, 199, 302, 513 | yes |
| 110 | `NEXT_INSPECTION` keyed by rule name (54-68), `_NEXT_DEFAULT`; `CLASSES[5]`, `CLASSES[7]` (26-27) | L1405, L1419 | report.py:26-27, 54-69 | yes |
| 111 | `SECTIONS` = 12 functions (545-558); footer "Report complete" | L835, L1212 | report.py:545-558, 540-542 | yes |
| 112 | `sanitize` (569-599) escapes `\ \| < > [ ]`, drops Cc/Cf/Cs/Co; `cell` cuts at 200; empty cell prints `none` (report.py:143) | L258, L837 | report.py:569-605, 143 | yes |
| 113 | `render(result, ctx) -> str` (608); `to_json(result, ctx, report_path) -> dict` (613) | L860 | report.py:608-616 | yes |
| 114 | JSON v1 top-level keys (12) and `summary` keys | L833, L1213 | report.py:619-695 | yes |
| 115 | `DEFAULT_WINDOW = "6h"`, `MAX_WINDOW_HOURS = 720`, `MAX_SUFFIX = 99` (commands.py:27-29) | L1263, L1212 | commands.py:27-29 | yes |
| 116 | `sweep run [--run RUN]... [--window 6h] [--root PATH] [--output PATH]` (commands.py:220-241); window regex `[1-9][0-9]{0,3}[hd]` | L856, L1263 | commands.py:43-52, 219-244 | yes |
| 117 | `_publish(text: str, output_dir: Path, now: datetime) -> Path` (:153); temp `.<stem>.<pid>.tmp`, `O_EXCL`, `os.link`, `-2`..`-99` | L825, L861 | commands.py:153-208 | yes |
| 118 | `_check_output` (:99) | L781, L825 | commands.py:99-123 | yes |
| 119 | Exit codes 0 / 1 / 2 and `[sweep <stage>] <msg>` (commands.py:279-288) | L827-831, L1283 | commands.py:279-288 | yes |
| 120 | "Writer only (commands.py:100-132, 240)" | L1189 | the writer is `_publish` commands.py:153-208; :100-132 is the tail of `_check_output` and `_sweeps_base`; :240 is `--output` help | yes-minor (wrong cite, true claim) |
| 121 | `commands/sweep.md`: `allowed-tools: Skill`, "Nothing starts it automatically" (:22), `Skill sc:sweep-protocol` (:47) | L839, L1188 | commands/sweep.md:9, 22, 47 | yes |
| 122 | `sc-sweep-protocol/SKILL.md`: `uv run --frozen --no-sync` only on "command not found", timeout 120000, chunks of at most 150 lines, `Report complete`, ":51" scope sentence | L839 | SKILL.md:23-25, 51 | yes |
| 123 | WC-16 text at `WORKER-CONTRACT.md:287-289`; never-as-worker list `:23` | L845, L1645 | WORKER-CONTRACT.md:23, 287-289 | yes |
| 124 | `.gitignore:255-256` `.dev/sweeps/` | L240, L1189 | .gitignore:255-256 | yes |
| 125 | `BANNED_WORD` (stop, retry, release, merge, remov*) (`test_report.py:1102-1130`) | L1405 | tests/sweep/test_report.py:1102, 1111, 1127 | yes |
| 126 | Test names `test_allowed_orca_is_exactly_the_ten_templates`, `..._names_seven_verbs`; `test_probes_allowlist.py:624-638`; `RULE_NAMES` (:351, :378-379); `_rule_cases` (:277); `RULE_CLASS` (test_report.py:1091) | L810, L1419, L1459 | test_probes_allowlist.py:370, 375, 625; test_classify.py:277, 351, 379; test_report.py:1091 | yes |

### C. Agent-work-report (`src/superclaude/skills/agent-work-report/`) and orchestrator-side code it touches

| # | Snippet or reference | Doc location | Source path:line read | Identical |
|---|---|---|---|---|
| 127 | `run.py open <daily\|hourly\|on-demand> \| gate\|summary\|close <run> \| abandon <run> <reason> \| log <run> <action> <item\|-> <reason> \| refresh [--run <run>] \| status`, "exit 3 = run active" | L995 | scripts/run.py:4-22, 112-113, 868-887 | yes |
| 128 | `collect\|clickup\|sessions\|exclude\|match\|classify\|compare\|activity\|render.py <run>` | L996 | each script's `__main__` (collect.py:314, clickup.py:635, sessions.py:441, exclude.py:106, match.py:280, classify.py:144, compare.py:194 (1 or 2 args), activity.py:276, render.py:623) | yes |
| 129 | `check.py <run> [--links]` | L996 | check.py:346-350 | yes |
| 130 | `page.py <run> [--open]` | L996 | page.py:381-387: only `page.py --open` (no run) or `page.py <run>`; `page.py <run> --open` has 3 argv and falls to `sys.exit(__doc__)` | **NO (F-1)** |
| 131 | `page.py --open` (step 13) and `page.py --open` (9.3) | L937, L1265 | page.py:382-383 | yes (contradicts L996) |
| 132 | `clickup.py dm <run> <message_file>` | L996 | clickup.py:639-640 | yes |
| 133 | `prefs.py priority <run> <item url> <Urgent\|High\|Medium\|Low\|clear>`; `prefs.py answer <run> <url\|-> <session\|clickup-dm>` | L997 | prefs.py:4-6, 57-64 | yes |
| 134 | `waker.py morning\|hourly\|check-missed` | L997, L1265 | waker.py:4, 398-405 | yes |
| 135 | `common.repo_root() -> Path` (`$AWR_ROOT`, else `orchestrator_repo` of `~/.config/superclaude/issue-watch.json`, dir must hold `repos.yaml`) (common.py:28-51) | L998, L1251 | common.py:25, 28-51 | yes |
| 136 | `REQUIRED_CHECKS` seven names (run.py:204-212) | L954, L1423 | run.py:204-212 | yes |
| 137 | `config.json` 14 keys (person, person_name, orgs, excluded_repos, timezone, daily_run_local, report_days, missed_run_dm_local, time_budget_minutes, session_tag, automation_prefix, clickup_user_id, clickup_email, priority_labels) | L911, L1235 | config.json:1-21 | yes |
| 138 | Recorded values "`daily_run_local` 07, `missed_run_dm_local` 09" | L1235 | config.json:7, 9 hold `"07:00"` and `"09:00"` | NO-minor (F-3) |
| 139 | Orca argv: `terminal list [--worktree path:<p>] --json`, `terminal read --terminal <h> --screen --json`, `terminal wait --terminal <h> --for tui-idle --timeout-ms <ms> --json`, `terminal send --terminal <h> --text <t> [--enter --wait-submit <s>] --json` | L1161-1162 | orca_term.py:17-31, 87-110, 124-133 | yes |
| 140 | `terminal create --worktree path:<ws>` (waker.py:186-189) | L1162 | waker.py:186-189 | yes |
| 141 | `worktree list --json`; `worktree set --worktree path:<repo> --unread --comment <text>` | L1163 | sessions.py:309-312; waker.py:88-96 | yes |
| 142 | `automations list --json`; `automations runs --id <id> --json` | L1164 | run.py:160-201 | yes |
| 143 | `tab list\|close\|switch\|create ...`; `eval --page <id> --expression location.reload()` | L1165 | page.py:354-377 | yes |
| 144 | GitHub argv: `gh repo list <org> --limit 1000`; `gh issue list` / `gh pr list --repo <o>/<r> --state open --limit 1000 --json ...`; `gh project list --owner <org>`; `gh project item-list <n> --owner <org>`; `gh search issues --owner <org> --involves <person> --state open [--include-prs]` | L960 | collect.py:127-137, 156-175, 204-217, 236-244 | yes |
| 145 | `gh api --paginate --slurp repos/<o>/<r>/issues/<n>/timeline`; `gh pr view <url> --json mergeable,isDraft,reviewDecision,statusCheckRollup` | L960 | activity.py:71-76, 122-128 | yes |
| 146 | `gh issue or pr view <url> --json state,closedAt` (compare) | L960 | compare.py:88-94 passes `state,closedAt` plus `,mergedAt` for a PR | yes-minor (omits `mergedAt`) |
| 147 | `--json number` (check); `gh issue view <n> --repo <r> --json state,stateReason,assignees` (run) | L960 | check.py:317-325; run.py:502-509 | yes |
| 148 | ClickUp: `API` base, `MAX_TASK_PAGES` 200, `MAX_COMMENT_CALLS` 400, `ACTIVE_DAYS` 30, `OVERLAP_MS` 10 min, max 6 attempts, GET retried 3x on 5xx, 429 wait <= 65 s | L1223, L1336 | clickup.py:39-44, 58-113 | yes |
| 149 | `python -m http.server 8765 --bind 127.0.0.1 --directory <.dev/coordinator>`; `REPORT_PORT = 8765`; Popen at page.py:318; wait ~10 s | L964, L1225, L1362 | page.py:318-342; common.py:404-405 | yes |
| 150 | Hook file `~/.config/orca/agent-hooks/last-status.json` version 2; join key `<tabId>:<leafId>`; `providerSession.id`, `transcriptPath`; `AWR_HOOK_FILE`, `AWR_PROJECTS`; `FIRST_WINDOW_HOURS` 24, `FIRST_READ_BYTES` 30 MB | L962, L1252, L1336 | sessions.py:42-49, 282, 323-330 | yes |
| 151 | `ORCA_TERMINAL_HANDLE`, `CLAUDE_TOPIC` read from `/proc/<pid>/environ` (orca_term.py:34-58) | L1254 | orca_term.py:34-58 | yes |
| 152 | `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID`, `AWR_ROOT` | L1251, L1253 | clickup.py:60, 132; common.py:35 | yes |
| 153 | Waker: `HOLD_RETRIES, HOLD_WAIT_S = 15, 120`; `START_WAIT_S` 120; `SHELL_WAIT_S` 30; wake line "Wake (daily report): run /agent-work-report for today's report."; `/clear`; `ccsession coordinator`; hourly = recorded skip (:216-220) | L964, L976, L1335 | waker.py:36-42, 140-143, 201, 216-220, 278-302 | yes |
| 154 | `FRESH_OUTPUT_SECONDS` 60; `orca_term` default timeout 60; `run_cmd` timeout 120 | L977, L1335 | orca_term.py:14, 17; common.py:103 | yes |
| 155 | `info_ttl_days` default 14, read by line from `repos.yaml` | L975 | run.py:443-452 | yes |
| 156 | `move_to_closed` sets `closed_at`, `close_reason` (run.py:483) | L971, L1194 | run.py:466-488 | yes (line is inside the function) |
| 157 | `prefs.check_url` accepts only `https://(github.com\|app.clickup.com)/...`; error "not an item URL" (prefs.py:20, 30-32) | L1607 | prefs.py:20, 30-32 | yes |
| 158 | `run.py close` re-checks only `passed()`; `clickup.py dm` uses `deliverable()` (run.py:376-379, clickup.py:619) | L954, L1553 | run.py:219, 245, 371-379; clickup.py:619 | yes |
| 159 | `"Other work in progress"`, no `"Watching"` string (run.py:788-793) | L1554 | run.py:791; common.py:239 | yes |
| 160 | closeout `settle.sh:1037-1042`: probe `superclaude orchestrator report-entry --help`, `ENTRY escalated key=%s why=surface_absent` | L985, L1610 | sc-closeout-protocol/scripts/settle.sh:1037-1042 | yes |
| 161 | Master poll config `_TOP_KEYS` (cycle.py:58-69) rejects keys outside it (:216-220); no `orchestrator_repo` in `cycle.py` | L986, L1236, L1551 | issue_watch/cycle.py:58-69, 216-218 | yes |
| 162 | `issue_watch` 12-element `orca agent launch` argv (launch.py:95-131) | L1182 | issue_watch/launch.py:95-116 (`retry_argv` 119-132 adds 2) | yes |
| 163 | `ORCH:3` "holds no implementation code"; `ORCH:372, 374` `_TOP_KEYS (58-68)` reshape; `ORCH:510` `report-entry`; `ORCH:744, 748` verbs; `ORCH:930` | L163, L1167, L1606 | docs/designs/orchestrator.md:3, 372, 374, 510, 744, 748, 930 | yes |
| 164 | `orchestrator-mode.md:27` "does not exist yet", `:609` "copied from #409 at `495eb96d`", `:636`, `:877`, `:1022` "Total: 23 open items" | L1539, L1085, L1544 | docs/designs/orchestrator-mode.md:27, 609, 636, 877, 1022 | yes |

### D. Design package (`.dev/design/orca-observer-20261106/`, checkout path)

| # | Snippet or reference | Doc location | Source path:line read | Identical |
|---|---|---|---|---|
| 165 | `render.py [--batch {1,2}] [--show SLUG] [--width N]`, defaults 1 and 116, `--width` ignored in export mode, `NO_COLOR` presence | L1044, L1092, L1266 | render.py:126-130 | yes |
| 166 | `fixtures.fixture(owners=8, count=80, variant="base")`; `metrics(f, owner=None)`; `write_fixtures(root)` | L1093 | fixtures.py:11, 98, 114 | yes |
| 167 | `render.designs(batch=1)`; `render.screen(spec, f, width, ascii_mode=False) -> Canvas`; layout fn `(c, f, m)` | L1094, L1046 | render.py:20-29 | yes |
| 168 | Font paths `/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf` and `-Bold.ttf`, read at import (render.py:16-18) | L240, L386, L1239 | render.py:16-18 | yes |
| 169 | `manifest.json` keys `{synthetic, as_of, batch, widths, concepts[], fixture_sha256}` | L1215 | render.py:45, 71 | yes |
| 170 | `requirements.txt`: `Pillow==13.0.0`, `wcwidth==0.9.4` | L240, L1036, L1239 | requirements.txt:1-2 | yes |
| 171 | Fixture top-level keys (12), five `demo:*` sources, owners 5/8/10, count 50/80/100, 9 variants + 9 `scale-*` | L385, L1052, L1045 | fixtures.py:11-21, 65, 117-122 | yes |
| 172 | Session has no PR / issue / url field (fixtures.py:30-43) | L1052 | fixtures.py:30-43 | yes |
| 173 | 20 design slugs (set 1 and set 2) | L1036 | layouts/group_a.py:224-229; group_b.py:218-223; agent_focus.py:171-182 | yes |
| 174 | `canvas.py` `sanitize` (:10-17), `clip` (:19-29), `Canvas.text` (:38-55), `PALETTE` (:7) | L258, L397 | canvas.py:7-55 | yes |
| 175 | README reproduce commands (README.md:24-28), "design collaboration branch" (:9), "preserved unchanged" (:44), Bubble Tea (:46-48) | L227, L1051 | README.md:9, 24-28, 44, 46-48 | yes |
| 176 | `tests/test_designs.py` 19 tests | L178, L1037 | grep `def test_` count 19 | yes |

### E. Section 13 skeletons (read against the real registration point)

| # | Skeleton | Doc location | Real interface read | Conforms |
|---|---|---|---|---|
| 177 | A: `def _rule_example(row: SessionRow, ctx: SweepContext) -> Classification \| None: ... return _classification(C_EXAMPLE, "example", "evidence text")` | L1429-1432 | classify.py:211-223 rule shape, :130 `_classification` | yes (shape and arg order) |
| 178 | A (comment): `# RULES += Rule("example", _rule_example)   models.CLASSES += "example"   report.NEXT_INSPECTION["example"] = "read ..."`; `C_EXAMPLE` | L1433 | `RULES` is a tuple of `Rule` ending with the always-matching `fallback` (classify.py:345-355); `CLASSES` is a tuple (models.py:50-59) unpacked into 8 names (classify.py:42-51); `C_EXAMPLE` is defined nowhere | **NO (F-2)** |
| 179 | B: `ALLOWED_ORCA = (..., ("orchestration", "<verb>", "--run", "<run>", "--json"),)` | L1436 | probes.py:49-60 (tuple of token tuples, `<run>` placeholder) | yes |
| 180 | C: `("<jsonKey>", "<row_attr>"),` | L1439 | export.py:25-45 | yes |
| 181 | D: `View` gains `example: ExamplePanel \| None = None`; `build_view` passes `example=_example_panel(result, clock)`; `_example_panel(result, clock) -> ExamplePanel \| None` | L1441-1442 | view.py:368 `questions: QuestionsPanel \| None = None`; :1004 `_questions_panel(...)`; :1146 `questions=panel` | yes (pattern; real builder takes a third argument) |
| 182 | E: `def main(run) -> None: ...` in `scripts/<name>.py` | L1445 | exclude.py:59, sessions.py:278, check.py:168 `main(run, ...)` | yes |

Rows: 182 (observer 66, sweep 60, agent-work-report 38, design package 12, skeletons 6). Inline code references verified: well over 60 (rows 1-176 each carry one or more).

---

## Overall Verdict: FAIL

Two blocking findings (F-1, F-2). Everything else checked in this lens matches the snapshot or is a minor note.

VERDICT: FAIL (2 blocking, 7 minor)

## Checks (lens checklist)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Observer CLI flags (`--once --width --ascii --fixture --run --snapshot --questions`), defaults, exit codes | PASS | rows 41-50; commands.py:57-60, 183-197, 264-269, 364-387, 449-521 |
| 2 | Sweep CLI flags (`--run --window --root --output`), defaults, regex, exit codes | PASS | rows 115-119; commands.py:27-29, 43-52, 219-288 |
| 3 | Orca argv templates (observer 3, sweep 10 + 4 git, agent-work-report terminal/worktree/automations/tab/eval) | PASS | rows 1-3, 67-71, 139-143; adapter.py, probes.py, orca_term.py, waker.py, run.py, page.py |
| 4 | Function, class and constant names and values | PASS with minor notes | rows 8, 15, 18, 22-31, 73-75, 83-88, 103-110, 148-155 |
| 5 | Function signatures and defaults in the "Public Interface" blocks | FAIL | all signatures match except the `page.py` usage line (F-1) |
| 6 | Schema keys (observer snapshot, sweep JSON v1, fixture schema, manifest) | PASS | rows 23, 57, 62, 114, 169, 171 |
| 7 | Environment variables (`ORCA_CLI_COMMAND`, `XDG_STATE_HOME`, `NO_COLOR`, `COLORTERM`, `TERM`, `AWR_*`, `CLICKUP_*`, `ORCA_TERMINAL_HANDLE`, `CLAUDE_TOPIC`, `GIT_OPTIONAL_LOCKS`) | PASS | rows 52, 58, 71, 72, 150-152 |
| 8 | Section 13 skeletons A-E conform to the real registration points | FAIL | skeleton A comment (F-2); B-E conform (rows 177, 179-182) |
| 9 | Cited line numbers (sampled on every file cited in Sections 5, 8, 9, 12, 13) | PASS with minor notes | F-4, F-5, F-6, F-9; all other line cites read landed on the claimed code |
| 10 | No snippet reproduces a full function body beyond "key signatures only" | PASS | the code blocks at doc L739-745, L855-862, L994-999, L1091-1095, L1427-1446 are signatures or 1-4 line shapes; no body copied |

## Issues Found

| ID | Severity | Location (doc) | Evidence | Required fix |
|---|---|---|---|---|
| F-1 | IMPORTANT (blocking) | L996, Section 5.5 "Public Interface" | Doc text: `check.py <run> [--links];  page.py <run> [--open];  clickup.py dm <run> <message_file>`. Real code, `scripts/page.py:381-387`: `if sys.argv[1:] == ["--open"]: open_tab()` / `elif len(sys.argv) == 2: main(sys.argv[1])` / `else: sys.exit(__doc__)`; the script's own usage (page.py:4-5) is `page.py <run_folder>` and `page.py --open`. `page.py <run> --open` has three argv items, prints the docstring and exits 1. The doc contradicts itself: L937 (step 13) and L1265 (9.3) correctly say `page.py --open`. | Replace `page.py <run> [--open]` with `page.py <run>;  page.py --open` (two forms, `--open` takes no run). |
| F-2 | IMPORTANT (blocking) | L1433, Section 13 skeleton A (comment line) | Doc text: `# RULES += Rule("example", _rule_example)   models.CLASSES += "example"   report.NEXT_INSPECTION["example"] = "read ..."` and `_classification(C_EXAMPLE, ...)`. Real registration points: `RULES: tuple[Rule, ...]` ends with `Rule("fallback", _rule_fallback)`, which always returns (classify.py:345-355, :330-342, :376); `CLASSES` is a tuple of 8 strings unpacked into exactly 8 names `C_WAITING ... C_UNKNOWN` (models.py:50-59; classify.py:42-51). `tuple += Rule(...)` and `tuple += "example"` raise `TypeError`; if made to work by appending, the rule would sit after the always-matching fallback and never run. `C_EXAMPLE` exists nowhere and the skeleton never says it comes from the unpack. The table row above (L1419 step 2) correctly says "at the precedence position". | Rewrite the comment as: insert `Rule("example", _rule_example)` into the `RULES` tuple before `Rule("fallback", ...)` (classify.py:345-355); add `"example"` inside the `CLASSES` tuple (models.py:50-59) and a ninth name `C_EXAMPLE` in the unpack (classify.py:42-51); add `NEXT_INSPECTION["example"]` (report.py:54-68). |
| F-3 | MINOR | L1235, Section 9.1 | Doc: `daily_run_local 07, missed_run_dm_local 09`. `config.json:7, 9`: `"07:00"` and `"09:00"` (waker.py:56, 61 take `[:2]`). | Quote the values as `"07:00"` and `"09:00"`. |
| F-4 | MINOR | L664, Section 5.3 Key Files | `_guard` cited at 728; `classify.py:728` is the `@dataclass` line of `_Guard`; `def _guard` is at :741 (L714 correctly gives 745 for the body). | Change 728 to 741. |
| F-5 | MINOR | L1189, Section 8.2 | "Writer only (commands.py:100-132, 240)": the one writer `_publish` is `commands.py:153-208`; :100-132 is the tail of `_check_output` and `_sweeps_base`, :240 is the `--output` help text. | Cite `commands.py:153-208`. |
| F-6 | MINOR | L1068, Section 5.6 status table | `unavailable (no source)` cited at `view.py:134`; the constant `UNAVAILABLE` is `view.py:113` (:134 is `UNAVAILABLE_FACTS`). | Cite `view.py:113`. |
| F-7 | MINOR | L960, Section 5.5 | `gh issue or pr view <url> --json state,closedAt` (compare): `compare.py:88-94` adds `,mergedAt` for a PR. | Write `state,closedAt[,mergedAt for a PR]`. |
| F-8 | MINOR | L1118, Section 6 | `Session (focus, selected, filter_text, show_historical, baseline, marked, inspector_scroll, selected_question)` omits `selected_row` and `mark_wall_time` (view.py:155-167). | Add the two fields or write "among others". |
| F-9 | MINOR | L1509, L1565 | ms heuristic cited at `parse.py:247`; the `> 1e11` condition is on :246, :247 is its PROPOSED comment. | Cite `parse.py:246-247`. |

Not defects (checked): the shipped docs-versus-code disagreements the document itself reports (CC-01..CC-05, SD-xx) were not re-graded here; they are outside the code-example lens.

## Summary
- Checks passed: 8 / 10 (checks 5 and 8 fail on F-1 and F-2)
- Checks failed: 2
- Critical issues: 0; IMPORTANT (blocking): 2; MINOR (notes): 7
- Issues fixed in-place: 0 (fix authorization false; no file other than this report was modified)

## Actions Taken
None on the document. This report is the only file written.

## Recommendations
- Fix F-1 and F-2 (two one-line edits in Sections 5.5 and 13), then re-verify only those two lines; minor notes need no re-check.

## Confidence Gate
- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (line cites were verified on every cited code file; prose-only cites to `CHANGELOG.md`, `docs/user-guide/commands.md`, `docs/user-guide/cli-groups.md`, `core/HOW-WE-WORK.md` rows, `README.md:35,136` and the `.dev/issues/409/` records are outside "code snippet / code reference" and were not read)
- **Tool engagement:** Read: ~85 | Grep: ~27 | Glob: 4 | Bash: 0 (counts are estimates from the session; each call targeted a cited file; Read + Grep + Glob exceeds the 10 checklist items)
- No web research was performed (no Tavily or WebSearch calls).
- Limits: nothing was executed (read-only lens); behaviour claims such as `tuple += str` raising `TypeError` are from Python semantics, not a run. Origin/master-only `.dev/` files (`release-gates.md`, SPEC) are absent from the snapshot and were not read; no claim in this report depends on them.

## QA Complete

