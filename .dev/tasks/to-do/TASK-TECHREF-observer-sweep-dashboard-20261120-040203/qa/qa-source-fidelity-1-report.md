# QA Report - Source-Document Fidelity (Agent 1, half A: observer and sweep)

**Topic:** Technical reference for the observer, sweep and dashboard family
**Date:** 2026-11-20
**Phase:** source-fidelity (semantic-coverage + detail-preservation), half A
**Fix cycle:** N/A (fix_authorization: false, report only)
**Status:** Complete

Reference under review: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
Snapshot: /home/coder/.cache/ic-snap-20261120/master

---

## Module findings (written module by module)

All paths below are under SNAPSHOT = /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6). "REF:n" is a line of the reference file.

### M1 observe/adapter.py (512 lines) - fully read
- Verified exact: 3 argv templates (`WORKER_LIST_TEMPLATE` :29, `DISCOVERY_TEMPLATE` :30, `QUESTION_TEMPLATE` :32), 13 `FORBIDDEN_PREFIXES` (:34-50, counted), run-id regex (:52-54), `CURSOR_MAX_BYTES` 2048 (:55), `MAX_CALLS_PER_CYCLE` 5 (:57), 8 MiB / 2 KiB / 10 s / 2 s (:58-63), `_is_question_shape` 8 tokens (:111-118), exempt indexes {1,4,6} (:126), `assert_allowed` (:135-170), `build_argv` (:173-183), `build_question_argv` (:186-190), `read_pages` (:395), `read_questions` (:469), `SourceResult` fields (:318-325), namespace = realpath (:378-381), error-code map (:66-69).
- Result: no divergence found. REF 5.1 (REF:418-440), 8.1 and 12.1 match.

### M2 observe/collector.py (361) and observe/questions.py (142) - fully read
- Verified exact: `INTERVAL` 15, `CYCLE_BUDGET` 15, `MAX_BACKOFF` 60, `JOIN_TIMEOUT` 5, `QUESTION_PAGE_CAP` 4 (collector.py:28-34); backoff doubles only when the first page fails (:306) and resets on any parsed page (:321); thread name `observe-collector` (:341) ends only on NOT_AVAILABLE (:348-349); `FixtureSource.read_questions` always FAILED `no-question-fixture` (:125-129); `Collector.__init__` signature (:135-145); `RETENTION_BOUND` 1000, `WINDOW_ROWS` 100 (questions.py:21-22); eviction of oldest created (:125-129).
- Minor omission (note): `RETENTION_EXCEEDED = "unknown (retention exceeded)"` (questions.py:24, 67) and the "100+ (window full)" text (view.py:784) are not stated in the reference.
- Result: no blocking divergence.

### M3 observe/parse.py (835) - fully read
- Verified exact: 31 `_FIELDS` (:58-90, counted); 7 `resource.*` + `workspace.id/.kind` + `stage.activity/.detail` = 11 not exported; `UNKNOWN` singleton with `__copy__/__deepcopy__/__reduce__` (:25-43); strict envelope checks (:369-380); lenient rows, `malformed_rows` (:384-388); `_clean_json` depth 6 (:277-290); warnings capped at 50 (:403-405); ms heuristic `> 1e11` (:246-247); `VARIANTS` 10 names (:750-761); `ASK_CAP` 400 (:475).
- **BLOCKING B-1** (REF:446, REF:923, REF:1239): the reference says "Rows are never deleted for absence" and "memory only grows". Code: `parse.py:726-727` (`if row.identity_unknown and not coverage.partial: continue  # a complete cycle replaces the previous cycle's anonymous rows`) drops identity-unknown rows that a complete cycle did not return. The reference's own cited range for this claim (`parse.py:723-728`, REF:923) contains that exception. True only for rows with an identity.
- Minor omissions (notes): across-cycle merge with no common timestamp keeps the newer cycle's row and flags `order unknown` (parse.py:640-641), not stated; the link-verification rule (sender must equal `dispatch:<dispatchId>`, dispatchId must match `[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}`, payload over 64 KiB is not parsed; link states `no payload`, `payload not readable`, `payload has no dispatchId`, `sender mismatch`; parse.py:468-509) is summarised only as "verified"; `contradictory_rows` (wrong type or wrong Run, dropped and counted; parse.py:557-567, view.py:838) is not described.

### M4 observe/export.py (274), snapshot.schema.json (158), sanitize.py (48) - fully read
- Verified exact: `SCHEMA_VERSION` 1 (export.py:20); `_TEXT_FIELDS` 19 + `_ANY_FIELDS` 1 = 20 exported (:25-47); `state_dir` (:236-244); `write_atomic` mkdir 0o700, mkstemp, fsync, `os.replace`, unlink on failure (:257-274); `record_path` (:247-250); schema closed (`additionalProperties:false`) on root, producer, source, page, collection, questions, items, row, stage, liveness, evidence; `counts` values scalar (schema :50); `closureEvidence` const "unavailable" (:78); sanitizer drops Cc/Cf/Cs (sanitize.py:24).
- **BLOCKING B-2** (REF:455): "Also dropped: ... coverage counters". Code exports an optional `collection` group `{state, collected, changedDuringRead, duplicatesIgnored}` (export.py:209-215; schema :55-64; values from `_meta`, view.py:687-694). Only `pages_read`, `empty_page`, `has_more_at_stop`, `stopped_by_*`, `identity_unknown_rows` and `malformed_rows` are dropped. The reference lists `collection` as a closed node (REF:454) and in 12.3 (REF:1146) but never gives its four keys, and says its counters are dropped.
- Minor (note): rows are sorted newest-first by `liveness.observedAt` with `evidence.lastObservedAt` as fallback, ties by dispatchId then namespace (view.py:476-481); the reference names only `liveness.observedAt`.

### M5 observe/view.py (1300), render.py (1461), terminal.py (192), theme.py (126), keys.py (235), commands.py (524) - fully read except render.py helper bodies (layout code read at :425-575, :905-1125, :1248-1461)
- Verified exact: `KEY_NAMES` (view.py:30); `STALE_SECONDS` 45.0 and `source_state` (:33-35, 456-463); `HISTORICAL_STATES` (:36); filter over eight cells (:587-600); snapshot status map OK/STALE/FAILED->ERROR/else UNKNOWN (:667); `Session` fields (:151-168); `DeskView`/`_desk` join on `dispatch_id` (:888-948); `INSPECTOR_SCROLL_STEP` 3 (:131); `apply_key` key map incl. n/p, Esc, q, e, m, d/u, h, `/` (:1246-1300) and `apply_key` signature; `Effect` NONE/EXPORT/QUIT (:1162-1167); width classes 160/116/80, `MIN_WIDTH` 80, `MIN_ROWS` 8, texts (terminal.py:21-27, 82-89); colour depth rules (:92-101); 7 `STATE_ROLE` entries (theme.py:95-103); ledger columns per class and dispatchId cap 48 (render.py:494-568); desk pane widths `RIGHT_DESK` 80, `RIGHT_LIST` 46 (:921-936); layouts A/B/C and `MIN_QUESTION_ROWS` 3, C only below 116 (:939-942, 1376); exit codes 0/1/2/143/129 (commands.py:187-197, 264-268, 364-369, 377-387; keys.py:115-125); seven `Options` fields (:121-129); gate constants True (:67, 70); `_questions_on`/`_link_on` (:173-180); `READ_TIMEOUT` 0.1, `REDRAW_SECONDS` 0.5 (:57-60); `--once` plain record vs `--width` screen (:244-269); snapshot write rule `live or bool(options.snapshot)` (:408); `Deps` (:132-147); help-line constants (view.py:91-118, 1139-1141); `Window.more_text` unused outside view.py (grep: only view.py:331, 402).
- **Minor (note) m-1** (REF:236): the stack table lists `fcntl` among the observer's stdlib modules. No observer source imports `fcntl` (keys.py imports `os, select, signal, sys, termios, threading, time, tty`); the word appears only in a test that blocks it (tests/observe/test_commands.py:73-81).
- Minor (note): `_color_system` also returns no colour for `TERM=unknown` (terminal.py:95); the reference says only "dumb" (REF:1024).
- Result: no blocking divergence in the interaction layer.

### M6 sweep/models.py (278) and sweep/classify.py (1009) - fully read
- Verified exact: `CLASSES` (models.py:50-59), `PACKAGE_STATES` (:62-69), `SAFE_VALUES` (:71), `JSON_SCHEMA_VERSION` 1 (:18), `worker_done_seen=None` / `fenced_evidence="unreadable"` defaults (:108-109), reserved `agent_wait_since` (:111-112); `JOIN_PATH="B"` (classify.py:40); all 9 rule firing conditions in REF:599-609 against `_blocked_contract` (:161-188), `_exit_proof` (:191-208), `_rule_fenced` (:219-223), `_rule_waiting_signal` (:226-248), `_rule_working` (:251-269), `_rule_finished` (:272-292), `_rule_idle` (:295-311), `_rule_person_active` (:314-327), `_rule_fallback` (:330-342); `RULES` order (:345-355); `_force_unknown` (:358-366); `classify` second call of rules 1 and 2 for notes (:378); `package_state` (:423-429), `removable` (:455-476), `safe_to_close` (:479-504) never return `yes`; `_merge_group` (:512-525); `_window` (:548-558); `_contract_for` (:570-591); path A then path B (:667-682); `_guard` flags (:741-757); `_person_origin` (:760-779); `classify_all` (:880-1009), idle counted as historical (:977), `total_is_lower_bound` hard-coded True (:989).
- C8 check: grep of `worker_done_seen|fenced_evidence|agent_wait_since` over `src/` finds writes only as dataclass defaults (models.py:108-112) and reads (classify.py:198-235, report.py:128); `parse_worker_show` (probes.py:471-515) never sets them. The reference describes `stalled (proved)`, `fenced`, `agent_wait_since`, `Safe to close = yes`, `Removable = yes` exactly as the code behaves (REF:636, REF:1216-1218); it does not relabel them as a plain known gap: each carries a cited line. I read the cited SPEC lines via `git show origin/master:` (SPEC:103, 106, 111, 167, 231-232, 238, 251, 274, 338; DESIGN:493, 636, 794, 841, 877, 1003): the quotes support the labels (SPEC:232 "Stalled (proved) stays fixture-only until a source mapping exists"; SPEC:251 "synthetic fixtures only in Phase 1"; SPEC:238 "UNVERIFIED field"; SPEC:106/338 "never yes").
- Minor (note) m-2: `classify.py:728` is the `_Guard` dataclass; the `_guard` function is at :741 (REF:582).
- Minor omissions (notes): `policy_of` (:389-401, JSON row key `policy`), the note `WC-13 violation, review` raised when `projection.parent` is non-null (:379-380; report.py:41, 373-375), the note `timestamp in the future` (:381-382), the WC-3 default `gate_policy == "report blocked"` when a brief has no `On a blocked gate:` line (:561-567) are not described (grep of the reference: no hit for `policy_of`, `WC-13`, `timestamp in the future`).

### M7 sweep/probes.py (1477) - fully read
- Verified exact: `ORCA_BINARY_DEFAULT` (:43); id regexes (:46-47); `ALLOWED_ORCA` 10 templates / 7 verbs (:49-60); `FORBIDDEN_TOKENS` (:62); `ALLOWED_GIT` 4 shapes (:68-81); `ORCA_VERSION_FILE` fixed path (:83); byte limits and `WORKER_LIST_PAGE` 100 (:85-89); `Budget(shows=50, total_s=90.0, per_call_s=10.0)` (:124-133); `orca_binary()` (:214-216); `check_orca_argv` before any process (:226-238, 268); `_orca` kinds and 8 MiB check after exit with the D-01 "shortcut" comment (:266-312); `_git` prefix `--no-optional-locks -C <cwd> -c core.fsmonitor=false` and `GIT_OPTIONAL_LOCKS=0` (:331-340); `bind_run` (:397-407); `parse_worker_show` never sets `worker_done_seen`, `fenced_evidence`, `agent_wait_since` (:471-515, comment :481); `_agent_wait` observation-then-terminal (:458-468); ledger last 512 KiB over 1 MiB (:607-619); `_stable` re-read (:590-604); transcript tail 256 KiB, first partial line dropped (:840-848); missing tab-map folder readable and empty (:875-876); filter pre-check 1 to 3 calls then status (:995-1018, 1038-1041); `FILTER_REASON` (:967); project key rule (:1075-1077); call sites run-current :399, worker-list :1150, task-list :1165/:1178, worker-show :1281, `worktree ps` :1335; `collect` (:1322); `remote hosts` coverage fixed "unknown" (:1381).
- Result: no divergence found in probes.py itself.
- **BLOCKING B-4** (semantic coverage; REF:686, REF:1099-1101, REF:1216-1220): the sweep reads exactly one `worker-list` page per Run (`probes.py:1150`, no `--limit`, no `--cursor`, no paging loop); a page of `>= WORKER_LIST_PAGE` (100) raw rows or `hasMore` sets `state.truncated` (:1157-1161). That flag drives: the header banner `PAGE_LINE` "[Orca rows: 100 shown; total is a lower bound (paging not yet captured)]" (report.py:32, 209-210), a "What I could not determine" bullet (report.py:528-531), and the origin note `origin unknown: worker list truncated` (classify.py:72, 701-702) which makes every un-joined transcript `person_started=None`, so idle and person-active cannot print. The reference gives only "worker-list page 100" in a limits list; its limitations table (REF:1216-1223) lists the observer's 500-row cap but no equivalent sweep limit, and `truncated` appears nowhere in the sweep description (grep of the reference for `truncated`: hits only at REF:553, the `gh pr view` file list, and REF:997, the report skill's terminal list). The observer pages up to 5 times (adapter.py:57, 456-457), so this is a direct, decision-relevant difference between the two tools' coverage.
- Minor omissions (notes): contract candidates are taken from `task_spec_text` and `body_text` (probes.py:1095), the reference says only "Task text"; `Budget.call_timeout()` returns None under 1 s remaining, and show shares are redistributed to Runs that still need shows (:145-169, 185-191).

### M8 sweep/report.py (695) and sweep/commands.py (288) - fully read
- Verified exact: `CHECKED_ORCA_VERSION` "1.4.245" (report.py:23); `CELL_MAX` 200 (:24); `SP24_LINE` and `SAFE_TO_CLOSE_LINE` (:42-49); `NEXT_INSPECTION` 9 keys (:54-68); 10 `_SESSION_DIMENSIONS` (:71-82); `_version_line` (:159-166); 12 `SECTIONS` in the stated order (:545-558); `Messages coverage: partial` (:199); Waiting (a) "Requested by" and "Decision owner" fixed `unknown` (:259-260); Ready Tasks sub-heading (:302); sanitizer (:562-599) and `cell` (:602-605); `render` joins by blank line, ends `Report complete` (:608-610, 542); JSON v1 has exactly the 12 top-level keys listed (:619-695), `summary` keys (:686-693), `report_path` unsanitized (:694); `DEFAULT_WINDOW` "6h", `MAX_WINDOW_HOURS` 720, `MAX_SUFFIX` 99 (commands.py:27-29); `_parse_window` regex (:45); `_check_output` rules (:99-123); `_publish` temp `.{stem}.{pid}.tmp`, `O_EXCL`, fsync, `os.link` -2..-99, unlink (:153-208); exit codes 0/1/2 and the `[sweep <stage>]` prefix (:246-288); options (:219-241).
- **BLOCKING B-3** (semantic coverage; REF:692): the reference gives the 12 top-level JSON keys and the `summary` keys only. The row, worktree, source, scope and collected shapes are not given: `rows[]` = `row_id, class, waiting_kind, rule, evidence, notes[], policy, person_started, safe_to_close{terminal, worktree, reason}` (report.py:642-661); `worktrees[]` = `path, status_read, uncommitted, unpushed, dev_tasks_unsaved, frozen, packages[{id, location, state}], shared_package_ids, removable, removable_reason` (:662-681); `sources[]` = `name, coverage, age_seconds, unscanned` (:633-641); `scope` = `runs, root, worktrees`; `collected` = `start, end`; `waiting` = `a[], b[]`. The reference's own overlap discussion treats "observer reads the sweep JSON" as the open proposal (REF:891, REF:1253) and states "JSON v1 lacks dimensions, links and step flow", which a reader cannot check without the row keys.
- **BLOCKING B-5** (REF:1065): "`os.link` unsupported or 99 names taken -> `[sweep publish] cannot link report`, exit 1". Code: only a failing `os.link` gives `[sweep publish] cannot link report: <exc>` (commands.py:191-194); 99 taken names give `[sweep publish] report name space exhausted: <dir>` (commands.py:197-201), pinned by tests/sweep/test_cli_contract.py:1414 (the cannot-link text is pinned at :1321, :1352). Exit code 1 is right for both.
- Minor omission (note): `Distinct affected sessions: {n} (set union, not a sum)` lines, the "Retained problems" content (interrupted-archive, conflict, shared active package, WC-13, show-cap lines; report.py:353-383) and the `Untracked paths` header line (:201-202) are not described.

### M9 commands/sweep.md (70), skills/sc-sweep-protocol/SKILL.md (66), core/WORKER-CONTRACT.md, core/HOW-WE-WORK.md, docs/designs/orchestrator-mode.md, docs/user-guide/cli-groups.md, .gitignore, CHANGELOG, commands.md, README, post-release report, install_user_setup.py, main.py, issue_watch/
- Verified exact: sweep.md has `allowed-tools: Skill` (:9), "Nothing starts it automatically" (:22), skill invocation at :47, never-as-worker (:18), "There is no worker mode" (:42), "Run as a dispatched worker" (:70); sweep.md:16 and SKILL.md:66 state `Safe to close`/`Removable` as facts without "never yes" (reference claim REF:636 holds); SKILL.md steps 1-5 incl. `uv run --frozen --no-sync` only on "command not found", timeout 120000, 150-line chunks, `(not observed in Phase 1)` mark (:23-27); SKILL.md:51 "not a runtime detector"; WORKER-CONTRACT.md: never-as-worker list at :23, WC-10 at :46, "The sweep." at :110, WC-16 heading :287 and text :289, L4 stall proofs :157; HOW-WE-WORK.md rows :298 and :359; pragmatic.md exception at :22-25; closeout.md:99 sweep row; test pins: `tests/commands/test_sweep_command.py` has 28 `def test_` and its two pin lists hold 37 shared and 15 skill-only entries (counted from the list openers at lines 179-421 and 434-500), `test_how_we_work_routing_table.py:33`, `test_worker_contract.py:167-170, 212-215`; `.gitignore:255-256` is the `.dev/sweeps/` rule with its comment; `cli-groups.md:42` "no key and no option maps to an Orca call", observe section :40-54; CHANGELOG `[6.0.0]` starts at :69, `Known limits (sweep, Phase 1)` bullets at :170-172 (REF SD-07/SD-08 hold), no `observe` entry in CHANGELOG (grep), README :35 and :136 are the two README lines; commands.md :619-622 limits (REF SD-09 holds); post-release-report.md :56 and :173 say "13 source files" / no technical doc; `_find_orca` at install_user_setup.py:247-270 with `_ORCA_CLIS` at :36; main.py registers `sweep` at :581-583 and `observe` at :590-592; `issue_watch/cycle.py` `_TOP_KEYS` lacks `orchestrator_repo` (:58-69) and rejects unknown keys (:214-221), grep finds no `orchestrator_repo` in `issue_watch/*.py`; orchestrator-mode.md :27 says `cli/sweep/` does not exist yet (SD-06 holds), :474 constants, :493 rule 5 and "worker_done_seen is None on every live row", :609 "copied from #409 at `495eb96d`", :636 SP24 line, :794/:795 FR-012/013, :1003 open item 6.
- Cross-file note (not in my half): REF:961 and REF:1138 cite `docs/designs/orchestrator.md` with the label "DESIGN:3" / "DESIGN:648", while 14.5 defines DESIGN as `orchestrator-mode.md` and ORCH as `orchestrator.md` (REF:1310). `orchestrator.md:3` is the "Status: approved ... It holds no implementation code" line (so the line number is right); `orchestrator-mode.md:3` is a section heading, so a reader who takes "DESIGN" as defined in 14.5 lands on the wrong file. Label inconsistency only (minor); half B should confirm the other `DESIGN:n` / `ORCH:n` numbers.
- Result: no divergence found in the docs assigned to my half.

### M10 observer fixtures, schema and tests; sweep tests and captured fixtures
- Verified exact: `fixtures/` has 20 entries (19 JSON + `__init__.py`): 10 variants (parse.py VARIANTS), 4 `golden-*`, 4 `golden-question-*`, `question-cap-100`; `golden-success.json` first cycle has 100 rows, `page` `{hasMore:true, total:428, limit:100, nextCursor:"cursor-1"}`, `nextAction.kind` none 86 / release 14, liveness exited 63 / unverifiable 35 / live 2 (jq over the file; REF:1088 holds); `tests/observe`: 36 entries, 26 `test_*.py`, 565 top-level `def test_`, `test_session.py` 27, `test_render.py` 135; forbidden set asserted as a superset (test_adapter.py:176-192); only `adapter.py` imports `subprocess` (test_commands.py:585-601); gate constants pinned True only with a cited, existing record (test_commands.py:752-780); `test_session.py:339-394` pins no-refresh-key and `e`/`q`/Ctrl-C as the only export/quit keys; backoff `[30,60,60,60]` (test_collector.py:149); `test_keys_spike.py:3` still says "only test module ... real pty" while `test_live_screen_pty.py` also uses pexpect (REF SD-05 holds); `tests/sweep`: 7 `test_*.py`, 323 defs (classify 94, cli_contract 61, cli_registration 3, git_config_hole 10, probes_allowlist 100, readonly 12, report 43), line counts match REF:584, 674; 21 fixture entries (20 `captured-*.json` + `SOURCES.md`), `captured-task-list-ready.json` has `tasks: []`, `captured-worker-show-running.json` is the 2026-11-16 capture (SOURCES.md), the five `captured-tab-map-*.json` files are named only in SOURCES.md (no test reads them); `test_classify.py:378-379` rule-order pin; `test_probes_allowlist.py:370, 375` and the 1+2+5+1 = 9 argv full sweep (:609-619) and zero-argv test (:624-638); git hole routes 1, 2, 3, 4, 5, 6, 6b, 8, 9 present, no route 7 (test_git_config_hole.py:105-264); `BANNED_WORD` at test_report.py:1102.

---

## Details table (every row read in the snapshot; "MATCH" = reference equals code, "DIVERGES" = see issue number)

| # | Documented detail (REF line) | Code value read | Path:line | Result |
|---|---|---|---|---|
| 1 | 13 forbidden prefixes (REF:428) | 13 entries counted | observe/adapter.py:34-50 | MATCH |
| 2 | Run id regex `^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$` (REF:426) | same | adapter.py:52-54 | MATCH |
| 3 | Cursor: non-empty str, no leading `-`, no NUL, <= 2048 bytes (REF:426) | same | adapter.py:98-108, 55 | MATCH |
| 4 | 5 worker-list calls per cycle, default argument (REF:436) | `MAX_CALLS_PER_CYCLE = 5`, `max_calls=` default | adapter.py:57, 400 | MATCH |
| 5 | Per-call timeout 10.0 s, comment "UNVERIFIED until ..." (REF:434) | 10.0, comment present | adapter.py:60-62 | MATCH |
| 6 | 8 MiB, first 2 KiB stderr, 2 s kill grace (REF:435) | 8*1024*1024, 2048, 2.0 | adapter.py:58-59, 63 | MATCH |
| 7 | Question argv exactly 8 tokens, `--run` at 5, `--json` at 7 (REF:424) | `len(tokens) == 8`, `tokens[5]=="--run"`, `tokens[7]=="--json"` | adapter.py:111-118 | MATCH |
| 8 | In question shape indexes 1, 4, 6 exempt from forbidden check (REF:428) | `positions - {1, 4, 6}` | adapter.py:126 | MATCH |
| 9 | Fence codes `consumer_fenced`, `no_active_terminal` map to `consumer-fenced`, `no-active-terminal` (REF:451) | same map | adapter.py:66-69, 503-507 | MATCH |
| 10 | Namespace = realpath of the Orca binary (REF:445) | `os.path.realpath(self.orca)` | adapter.py:378-381 | MATCH |
| 11 | 15 s interval, 15 s budget, 60 s max backoff, 5 s join (REF:437) | 15.0, 15.0, 60.0, 5.0 | collector.py:28-31 | MATCH |
| 12 | 4 + 1 calls with questions on (REF:436) | `QUESTION_PAGE_CAP = 4`, passed as `max_calls` | collector.py:32-34, 273 | MATCH |
| 13 | Failed first page doubles the wait; any parsed page resets (REF:437) | `min(self._wait*2, max)` / `self._wait = self._interval` | collector.py:306, 321 | MATCH |
| 14 | One daemon thread `observe-collector`, ends only without validated Orca (REF:448) | name at :341, return at :348-349 | collector.py:341, 348-349 | MATCH |
| 15 | Fixture source: `no-question-fixture` FAILED (REF:451, 556) | `SourceResult("FAILED", code="no-question-fixture")` | collector.py:125-129 | MATCH |
| 16 | Questions retention 1,000 oldest-created evicted, read window 100 (REF:438) | `RETENTION_BOUND = 1000`, `WINDOW_ROWS = 100`, `ordered[:-RETENTION_BOUND]` | questions.py:21-22, 125-129 | MATCH |
| 17 | 31 keys read (REF:443) | 31 tuples | parse.py:58-90 | MATCH |
| 18 | UNKNOWN singleton survives copy and pickle (REF:444) | `__copy__`, `__deepcopy__`, `__reduce__` | parse.py:25-43 | MATCH |
| 19 | Envelope: result object, workers list, page object, hasMore bool (REF:442) | four checks | parse.py:369-380 | MATCH |
| 20 | Warnings capped at 50 (REF:1099) | `[:50]` | parse.py:403-405 | MATCH |
| 21 | Nested JSON to depth 6 (REF:458) | `if depth > 6: return UNKNOWN` | parse.py:277-290 | MATCH |
| 22 | Timestamp heuristic `> 1e11` = ms (REF:1290) | `number / 1000.0 if number > 1e11` | parse.py:245-247 | MATCH |
| 23 | 10 fixture variants (REF:871, 413) | `VARIANTS` tuple of 10 | parse.py:750-761 | MATCH |
| 24 | Ask text cut at 400 chars (REF:543) | `ASK_CAP = 400`, `text[:ASK_CAP-3] + "..."` | parse.py:475, 503 | MATCH |
| 25 | "Rows are never deleted for absence" (REF:446) | anonymous rows dropped on a complete cycle | parse.py:726-727 | **DIVERGES (B-1)** |
| 26 | `SCHEMA_VERSION = 1` (REF:454) | 1 | export.py:20 | MATCH |
| 27 | 20 of 31 attributes exported (REF:455) | 19 `_TEXT_FIELDS` + 1 `_ANY_FIELDS` | export.py:25-47 | MATCH |
| 28 | State dir rule (REF:460) | `$XDG_STATE_HOME` when absolute else `~/.local/state`, + `superclaude/observe` | export.py:236-244 | MATCH |
| 29 | `write_atomic`: mkdir 0700, mkstemp, fsync, os.replace, unlink on failure (REF:460) | same | export.py:257-274 | MATCH |
| 30 | "coverage counters" dropped from JSON (REF:455) | `collection{state, collected, changedDuringRead, duplicatesIgnored}` exported | export.py:209-215; schema :55-64 | **DIVERGES (B-2)** |
| 31 | STALE after 45 s monotonic (REF:439, 447) | `STALE_SECONDS = 45.0`, `>= STALE_SECONDS` | view.py:33-35, 461 | MATCH |
| 32 | PARTIAL cycle shows as OK; FAILED never STALE (REF:447) | `source_state` passes only NOT_AVAILABLE/NOT_POLLED/FAILED through | view.py:456-463 | MATCH |
| 33 | Snapshot status OK/STALE, FAILED->ERROR, else UNKNOWN (REF:447) | dict map with default "UNKNOWN" | view.py:667 | MATCH |
| 34 | Filter = substring over eight cells (REF:529) | 8 cells joined | view.py:590-600 | MATCH |
| 35 | Inspector scroll 3 lines (REF:527) | `INSPECTOR_SCROLL_STEP = 3` | view.py:131 | MATCH |
| 36 | Desk text at most 4 lines (REF:543) | `DESK_TEXT_LINES = 4` | view.py:111 | MATCH |
| 37 | Width classes full >=160, line 116-159, short 80-115, narrow <80 (REF:533) | same | terminal.py:21-24, 82-89 | MATCH |
| 38 | Below 8 rows "terminal too small (min 8 rows)" (REF:533) | `MIN_ROWS = 8`, text | terminal.py:22, 27 | MATCH |
| 39 | Colour: NO_COLOR non-empty off; truecolor/24bit; *256color; else standard (REF:1024) | same, plus `TERM in (dumb, unknown)` | terminal.py:92-101, 114 | MATCH (minor: "unknown" omitted) |
| 40 | Seven state words coloured (REF:493) | 7 `STATE_ROLE` entries | theme.py:95-103 | MATCH |
| 41 | Full layout columns incl. dispatchId <= 48 (REF:537) | `min(..., 48)` | render.py:496-499 | MATCH |
| 42 | Line / short layouts: marker, kind, dispatchId, alive, status, age (REF:538-539) | same six columns | render.py:521-568 | MATCH |
| 43 | Desk: evidence 80 wide at 160, list 46 wide at 116 (REF:537-538) | `RIGHT_DESK = 80`, `RIGHT_LIST = 46` | render.py:921-922 | MATCH |
| 44 | Layouts A/B/C tried in order at 160 and 116, C only at 80, >= 3 question rows (REF:541) | `LAYOUTS`, `options = LAYOUTS if full/line else ("C",)`, `MIN_QUESTION_ROWS = 3` | render.py:939-942, 1376-1384 | MATCH |
| 45 | `QUESTION_GATE_PASSED = True` at :67 (REF:545) | True | observe/commands.py:67 | MATCH |
| 46 | `QUESTION_LINK_PASSED = True` at :70 (REF:545) | True | commands.py:70 | MATCH |
| 47 | Seven `Options` fields (REF:559) | once, width, ascii, fixture, run_id, snapshot, questions | commands.py:121-129 | MATCH |
| 48 | Exit 2: `--questions` with `--fixture`, without `--run`, rejected run id (REF:518) | three returns of `(2, ...)` | commands.py:187-194 | MATCH |
| 49 | Exit 1: display failed; gate False (REF:517) | `return 1` at :369 and :196 | commands.py:195-196, 364-369 | MATCH |
| 50 | Exit 2 on win32 and no terminal (REF:518) | `return 2` | commands.py:377-379, 385-387 | MATCH |
| 51 | Key read 0.1 s, repaint >= every 0.5 s (REF:1099) | `READ_TIMEOUT = 0.1`, `REDRAW_SECONDS = 0.5` | commands.py:57-60 | MATCH |
| 52 | SIGTERM 143, SIGHUP 129 (REF:519) | `SystemExit(128 + signum)` | keys.py:119-125 | MATCH |
| 53 | Decoder: left/right/Home/End/PgUp/PgDn swallowed (REF:521) | only finals `A`/`B` map to keys | keys.py:222-233 | MATCH |
| 54 | Interactive snapshot default is state dir; fixture writes nothing without `--snapshot` (REF:460, 507) | `write_snapshots=live or bool(options.snapshot)` | commands.py:405-408 | MATCH |
| 55 | Eight classes in order (REF:218, 613) | `CLASSES` tuple | sweep/models.py:50-59 | MATCH |
| 56 | Nine ordered rules (REF:599) | `RULES` tuple of 9 | sweep/classify.py:345-355 | MATCH |
| 57 | Rule 5 fires on live + in_progress + agentWait present and null (REF:605) | same four conditions | classify.py:258-264 | MATCH |
| 58 | Rule 2 needs exited, `worker_done_seen is False`, `fenced_evidence == "absent"` (REF:602) | same | classify.py:194-200 | MATCH |
| 59 | `JOIN_PATH = "B"` read only in `_guard` (REF:622-623) | defined :40, read :745 | classify.py:40, 745 | MATCH |
| 60 | `safe_to_close` and `removable` never return `yes` (REF:632-633) | no branch returns "yes" | classify.py:455-504 | MATCH |
| 61 | `PACKAGE_STATES` order and first-four-block-removal (REF:634) | conflict, interrupted-archive, archive-blocked, unfinished, archived, unknown; blocking four | models.py:62-69; classify.py:415-420 | MATCH |
| 62 | Idle rows counted as historical; `visible = total - historical` (REF:613) | `historical = counts[C_IDLE]` | classify.py:977, 983 | MATCH |
| 63 | `worker_done_seen`/`fenced_evidence` never set by `parse_worker_show` (REF:636) | not assigned; grep over `src/` finds only defaults and reads | probes.py:471-515; models.py:108-109 | MATCH |
| 64 | `ALLOWED_ORCA` 10 templates, 7 verbs, `--include-remote` rejected (REF:678) | same | probes.py:49-62, 231 | MATCH |
| 65 | `ALLOWED_GIT` 4 shapes (REF:682) | same | probes.py:68-81 | MATCH |
| 66 | Budget 50 shows / 90 s / 10 s (REF:686) | `shows=50, total_s=90.0, per_call_s=10.0` | probes.py:127-133 | MATCH |
| 67 | Byte limits 8 MiB, 1 MiB, 512 KiB, 256 KiB, page 100 (REF:686) | same, "proposed" comments | probes.py:85-89 | MATCH |
| 68 | Git prefix and env (REF:682, 1028) | `--no-optional-locks -C cwd -c core.fsmonitor=false`, `GIT_OPTIONAL_LOCKS=0` | probes.py:331-340 | MATCH |
| 69 | Sweep reads worker-list once per Run, no paging (not in REF) | single `_call(... "worker-list", "--run", run, "--json")`, `truncated` at >= 100 or hasMore | probes.py:1150, 1157-1161 | **OMITTED (B-4)** |
| 70 | Sanitizer strips escapes, Cc/Cf/Cs/Co, escapes `\ \| < > [ ]`; cell cut 200 (REF:258, 696) | same | report.py:562-605 | MATCH |
| 71 | 12 sections in stated order (REF:694) | `SECTIONS` 12 functions | report.py:545-558 | MATCH |
| 72 | 10 dimension columns (REF:247, 694) | `_SESSION_DIMENSIONS` 10 names | report.py:71-82 | MATCH |
| 73 | JSON v1 has 12 top-level keys (REF:692) | 12 keys | report.py:619-695 | MATCH (row/worktree keys omitted: B-3) |
| 74 | `CHECKED_ORCA_VERSION = "1.4.245"` (REF:239) | "1.4.245" | report.py:23 | MATCH |
| 75 | Window `[1-9][0-9]{0,3}[hd]`, max 720h (REF:1036) | same | sweep/commands.py:45-49 | MATCH |
| 76 | Report names `-2` to `-99` via `os.link`, never overwrites (REF:688) | `range(2, MAX_SUFFIX + 1)`, `MAX_SUFFIX = 99` | commands.py:29, 182-196 | MATCH |
| 77 | 99 taken names -> "cannot link report" (REF:1065) | "report name space exhausted: <dir>" (cannot-link only on `os.link` OSError) | commands.py:191-201; test_cli_contract.py:1414 | **DIVERGES (B-5)** |
| 78 | Exit 0/1/2 and `[sweep <stage>]` prefix (REF:690) | same | commands.py:279-288 | MATCH |
| 79 | WC-16 at WORKER-CONTRACT.md:287-289 (REF:704) | heading :287, text :289 | core/WORKER-CONTRACT.md:287-289 | MATCH |
| 80 | `/sc:sweep` on never-as-worker list at :23 (REF:707) | listed | WORKER-CONTRACT.md:23 | MATCH |
| 81 | HOW-WE-WORK rows 298 and 359 (REF:708) | row :298, bullet :359 | core/HOW-WE-WORK.md:298, 359 | MATCH |
| 82 | `.gitignore:255-256` (REF:983) | comment + `.dev/sweeps/` | .gitignore:255-256 | MATCH |
| 83 | "Nothing starts it automatically" at sweep.md:22 (REF:698) | present | commands/sweep.md:22 | MATCH |
| 84 | CHANGELOG:170 says `working` never produced (REF:1266) | present under `[6.0.0]` (:69) | CHANGELOG.md:170 | MATCH |
| 85 | `register` lines main.py:581-583, 590-592 (REF:217, 671) | same | cli/main.py:581-583, 590-592 | MATCH |
| 86 | `_find_orca` at install_user_setup.py:247-270 (REF:464) | same; `_ORCA_CLIS` :36 | cli/install_user_setup.py:36, 247-270 | MATCH |
| 87 | tests/observe: 26 test files, 565 defs (REF:175) | 26, 565 | tests/observe | MATCH |
| 88 | tests/sweep: 7 files, 323 defs (REF:176) | 7, 323 | tests/sweep | MATCH |
| 89 | 28 drift guards; 37 shared + 15 skill-only pins (REF:674, 698) | 28 functions; 37 and 15 entries | tests/commands/test_sweep_command.py | MATCH |
| 90 | Line totals 6,011 + 158 and 3,759 (REF:175-176) | 6,011 / 158 / 3,759 | wc -l over the modules | MATCH |
| 91 | Golden sample: 100 rows, total 428, none 86 / release 14, exited 63 / unverifiable 35 / live 2 (REF:1088) | same (jq) | observe/fixtures/golden-success.json | MATCH |

## Module-by-module coverage table

| Module / file in my half | Read | Documented claims checked | Undocumented features checked | Findings |
|---|---|---|---|---|
| observe/__init__.py | full (1 line) | yes | n/a | none |
| observe/adapter.py | full | yes | yes | none |
| observe/collector.py | full | yes | yes | minor omission |
| observe/questions.py | full | yes | yes | minor omission |
| observe/parse.py | full | yes | yes | B-1; minor omissions |
| observe/export.py | full | yes | yes | B-2 |
| observe/snapshot.schema.json | full | yes | yes | B-2 (collection keys) |
| observe/sanitize.py | full | yes | yes | none |
| observe/view.py | full | yes | yes | minor (sort fallback) |
| observe/render.py | lines 425-575, 905-1125, 1248-1461 | yes (every documented claim) | partial (lines 1-424, 575-904, 1125-1247 unread: wrap, frame, figure font, inspector, question-line helpers) | none |
| observe/terminal.py | full | yes | yes | minor ("unknown" TERM) |
| observe/theme.py | full | yes | yes | none |
| observe/keys.py | full | yes | yes | none |
| observe/commands.py | full | yes | yes | none |
| observe/fixtures/ | listing, 1 golden sample via jq, counts | yes | n/a | none |
| sweep/__init__.py | full | yes | n/a | none |
| sweep/models.py | full | yes | yes | none |
| sweep/classify.py | full | yes | yes | minor (line, omissions) |
| sweep/probes.py | full | yes | yes | B-4 |
| sweep/report.py | full | yes | yes | B-3 |
| sweep/commands.py | full | yes | yes | B-5 |
| commands/sweep.md | full | yes | yes | none |
| skills/sc-sweep-protocol/SKILL.md | full | yes | yes | none |
| core/WORKER-CONTRACT.md | cited lines (18-24, 44-47, 108-111, 156-158, 285-290) | yes | not swept (file is 339 lines, outside the sweep subject) | none |
| core/HOW-WE-WORK.md | cited rows 296-299, 358-360 | yes | not swept | none |
| docs/designs/orchestrator-mode.md | cited lines (3, 5, 27, 474, 493, 494, 609, 636, 649, 794, 795, 841, 877, 990-1024, 1003) | yes | not swept (1,058 lines) | none |
| docs/user-guide/cli-groups.md | observe section :36-70 | yes | yes | none |
| .gitignore | lines 255-256 | yes | n/a | none |
| tests/observe, tests/sweep, tests/commands/test_sweep_command.py | counts, cited tests, pin lists | yes | n/a | none |
| executor additions: install_user_setup.py, main.py, README.md, CHANGELOG.md, commands.md, post-release-report.md, issue_watch/ | cited lines | yes | n/a | none |

## Issues Found

| # | Severity | Location (reference line) | Issue | Required fix |
|---|---|---|---|---|
| B-1 | IMPORTANT (blocking) | REF:446, REF:923, REF:1239 | "Rows are never deleted for absence" / "memory only grows": identity-unknown rows missing from a complete cycle are dropped (`observe/parse.py:726-727`), inside the very range the reference cites (`parse.py:723-728`). | Say: rows with an identity are kept with `reobserved=False` and never deleted; identity-unknown rows are replaced by a complete cycle and kept only across a PARTIAL one. Narrow "only grows" to identified rows. |
| B-2 | IMPORTANT (blocking) | REF:455 (and REF:454, 1146) | "Also dropped: ... coverage counters" is false for the optional `collection` group, which exports `state`, `collected`, `changedDuringRead`, `duplicatesIgnored` (`export.py:209-215`, schema :55-64). The group's keys are never listed. | List the four `collection` keys; restrict the "dropped" list to `pages_read`, `empty_page`, `has_more_at_stop`, `stopped_by_*`, `identity_unknown_rows`, `malformed_rows`. |
| B-3 | IMPORTANT (blocking; lowest confidence of the five, an owner could reasonably call it minor) | REF:692 | JSON v1 is described by its 12 top-level keys only; the row, worktree, source, scope, collected and waiting shapes (`report.py:622-685`) are absent although the reference calls "observer reads the sweep JSON" an open proposal and says JSON v1 "lacks dimensions, links and step flow". | Add one sentence or table giving the `rows[]`, `worktrees[]`, `sources[]`, `scope`, `collected`, `waiting` keys (list in M8 above). |
| B-4 | IMPORTANT (blocking) | REF:686, 1099-1101, 1216-1223 | Not stated: the sweep reads one `worker-list` page per Run with no paging; `>= 100` rows or `hasMore` sets `truncated`, giving the `PAGE_LINE` banner, a "could not determine" bullet and the `origin unknown: worker list truncated` note that blocks `person_started`. The limitations table has the observer's 500-row cap but no sweep counterpart. | Add to 5.4 and 14.1: one page of 100 per Run, what `truncated` does (report.py:32, 209-210, 528-531; classify.py:72, 701-702; probes.py:1157-1161). |
| B-5 | IMPORTANT (blocking, low impact) | REF:1065 | "`os.link` unsupported or 99 names taken -> `[sweep publish] cannot link report`". Only the first gives that text; the second gives `[sweep publish] report name space exhausted: <dir>` (`sweep/commands.py:197-201`, pinned at `tests/sweep/test_cli_contract.py:1414`). | Split into two rows or name both messages. |
| m-1 | MINOR (note) | REF:236 | `fcntl` listed as an observer stdlib dependency; no observer module imports it (only a test blocks it). | Drop `fcntl` or say "tests block it". |
| m-2 | MINOR (note) | REF:582 | `_guard` cited at classify.py:728; the function is at :741 (:728 is the `_Guard` class). | Cite 741. |
| m-3 | MINOR (note) | REF:1024 | `TERM=unknown` also disables colour (terminal.py:95). | Add "unknown". |
| m-4 | MINOR (note) | REF:456 | Row sort uses `evidence.lastObservedAt` when `liveness.observedAt` is missing, ties by dispatchId (view.py:476-481). | Add the fallback. |
| m-5 | MINOR (note) | REF:446 | Across-cycle merge with no shared timestamp keeps the newer cycle and flags `order unknown` (parse.py:640-641). | Add. |
| m-6 | MINOR (note) | REF:543 | "verified payload dispatch_id": the check is `from_handle == "dispatch:<id>"`, id pattern, 64 KiB payload cap, four unlinked reasons (parse.py:468-509); `contradictory_rows` drop (parse.py:557-567) not described. | Add one line. |
| m-7 | MINOR (note) | REF:451, 438 | `unknown (retention exceeded)` (questions.py:24) and `100+ (window full)` (view.py:784) screen strings not stated. | Optional. |
| m-8 | MINOR (note) | REF:599-609, 692 | Sweep side rules not described: `policy_of` and JSON `policy` (classify.py:389-401), `WC-13 violation, review` note for non-null `projection.parent` (classify.py:379-380), future-timestamp note (:381-382), WC-3 default gate policy (:561-567), Retained-problems content, `Distinct affected sessions` lines, `Untracked paths` header line. | Optional; one table row each. |
| m-9 | MINOR (note) | REF:961, 1138, 14.4 | `DESIGN:n` is used for `orchestrator.md` in 8.1 and 12.2 but defined as `orchestrator-mode.md` in 14.5 (REF:1310); the cited line numbers I checked are right. | Use `ORCH:n` for `orchestrator.md`. |
| m-10 | MINOR (note) | REF:1100, 686 | Contract candidates also come from `body_text` (probes.py:1095); `Budget` hands unused show shares to other Runs and `call_timeout()` returns None under 1 s (probes.py:145-191). | Optional. |

## Summary
- Checks passed: 87 of the 91 details-table rows MATCH (row 73 matches but is the subject of B-3); 4 rows diverge or omit (rows 25, 30, 69, 77).
- Checks failed: 5 blocking findings (B-1 to B-5); 10 minor notes (m-1 to m-10).
- Critical issues: 0. IMPORTANT (blocking): 5.
- Issues fixed in-place: 0 (fix_authorization false; the reference was not modified).
- C8 candidates: described exactly as the code behaves; nothing sets `worker_done_seen` / `fenced_evidence` / `agent_wait_since`; `Safe to close` and `Removable` have no `yes` branch; each label carries a cited, real line (SPEC and DESIGN lines read). No relabelling defect found.
- Designed-only items: no planned or designed-only item in my half is described as built (observer R4, write-back, `report-entry`, orchestrator are tagged designed or "not built" in 2.1, 5.2, 14.3).

## Overall Verdict: FAIL

Five blocking fidelity findings (B-1 to B-5), each with a one-sentence fix. None is a security or data-loss risk; B-1, B-2, B-5 are false or wrong statements, B-3 and B-4 are omissions of decision-relevant sweep facts. All other checked claims match the code. Fix cycle budget: this is review 1 of at most 3.

## Self-audit
Would the user believe "0 issues"? No: I found five. Evidence of checking: 39 Read calls over every assigned module (render.py partly), 16 Grep calls, 18 Bash read-only batches (counts, `git show origin/master:` for SPEC lines, jq over fixtures), no modification of any file except this report.

## Confidence (Confidence Gate Protocol)
- **Confidence:** Verified: 32/33 | Unverifiable: 0 | Unchecked: 1 | Confidence: 97.0%
- **Tool engagement:** Read: 39 | Grep: 16 | Glob: 0 | Bash: 18
- UNCHECKED: render.py lines 1-424, 575-904, 1125-1247 (layout helper bodies); no documented claim depends on them, so the undocumented-feature sweep of that file is incomplete. Reason: time budget; the Verdict is FAIL regardless.
- UNVERIFIABLE: none. Items not assigned and not checked: PR states (#503 to #690), `release-gates.md`, `owner-pass-record`, gh comments, issue #590, #534 (GitHub and `.dev/` records are outside my half's file list; the C8 SPEC lines were read because the brief names C8).
- Web research: none (no external lookup needed); tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.
- Tool engagement minimum: Read + Grep + Glob = 55 >= 33 units; satisfied.

## QA Complete

