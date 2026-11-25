# Scope 01: observer (`src/superclaude/cli/observe/`)
**Scope:** observe package, main.py registration, tests/observe, docs mentioning `superclaude observe`
**Status:** Complete
**Date:** 2026-11-20
**Code snapshot:** /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6). All file:line cites below are in this snapshot under `src/superclaude/cli/observe/` unless a full path is given.
---

## 1. Per-file table (13 modules + schema + fixtures; 6,169 lines incl. schema)

Layering (from module docstrings): adapter (only Orca edge) -> parse -> collector (poll thread) -> view (pure view model) -> render/export (layout / files); commands wires it all. render.py:3-4 says it never imports adapter or collector; view.py:6-7 says it does no I/O.

| Path | Lines | Purpose | Key public names |
|---|---|---|---|
| `__init__.py` | 1 | one-line docstring "Read-only terminal observer for Orca workers" | none |
| `commands.py` | 524 | click group, option checks, `--once` path, interactive loop, gate guards | `observe_group` (449), `Options` (122), `Deps` (133), `SystemClock` (105), `execute` (412), `run_once` (244), `run_loop` (306), `run_interactive` (375), `LiveScreen` (275) |
| `adapter.py` | 512 | the ONE read-only edge to the Orca CLI: argv templates, forbidden-token allow-list, subprocess runner with caps, `LiveSource` | `WORKER_LIST_TEMPLATE` (29), `QUESTION_TEMPLATE` (32), `assert_allowed` (135), `build_argv` (173), `build_question_argv` (186), `production_runner` (224), `cancel_active` (216), `SourceResult` (319), `LiveSource` (343), `check_run_id` (92), `ArgvRejected` (72), `RunnerFailure` (80) |
| `collector.py` | 361 | single-flight bounded polling loop; publishes one immutable `CycleResult` per cycle; backoff; question source per cycle | `Collector` (132), `CycleResult` (38), `CycleSource` Protocol (71), `FixtureSource` (92); constants `INTERVAL=15.0`, `CYCLE_BUDGET=15.0`, `MAX_BACKOFF=60.0`, `QUESTION_PAGE_CAP=4` (28-33) |
| `parse.py` | 835 | strict-envelope / lenient-row parsing of `worker-list` pages, `merge` across pages/cycles, question parsing + payload link, fixture loader | `UNKNOWN` sentinel (43), `Row` (110), `ParsedPage` (165), `Coverage` (180), `Snapshot` (222), `parse_page` (365), `merge` (654), `Question` (416), `parse_questions` (512), `load_fixture` (801), `VARIANTS` (750), `ShapeError` (51) |
| `questions.py` | 142 | pure question retention store (bounded 1,000; nothing ever "closed" - no closure source) | `QuestionRecord` (28), `QuestionState` (41), `merge_questions` (81), `window_is_full` (140), `RETENTION_BOUND=1000`, `WINDOW_ROWS=100` |
| `view.py` | 1300 | pure `(CycleResult, Session, clock) -> View`; every status literal defined once; key handling | `build_view`, `apply_cycle` (1174), `apply_key` (~1245), `Session` (152), `Key` (138), `Effect` enum NONE/EXPORT/QUIT (1162), `View` (335), `RowView` (179), `QuestionsPanel` (268), `DeskView` (254), `STALE_SECONDS=45.0` (33) |
| `render.py` | 1461 | Rich renderables from `View` + `TerminalPolicy`; 3 width layouts, framed ledger, questions list, Decision Desk pane | `render` (1449), `screen_lines` (1248), `Line`/`Span`, `LAYOUTS=("A","B","C")` (942), `OBSERVATION_TITLE` (1164) |
| `export.py` | 274 | plain-text record + versioned JSON snapshot from one `View`; atomic 0600 writes; state dir | `record_text` (71), `snapshot_dict` (183), `snapshot_json` (219), `state_dir` (236), `record_path` (247), `snapshot_path` (253), `write_atomic` (257), `SCHEMA_VERSION=1`, `SNAPSHOT_NAME="snapshot.json"` |
| `keys.py` | 235 | POSIX cbreak key reader (termios/tty/select), signal-safe terminal restore; imported lazily | `KeySource` (36), `MAX_TIMEOUT=0.25`, `ESC_WAIT=0.05` |
| `terminal.py` | 192 | sole owner of colour, ASCII mode, width classes, truncation and every Rich `Console` | `TerminalPolicy` (55), `resolve_policy` (104), `make_console` (142), `detect_size` (136), `clip` (170), `MIN_WIDTH=80`, `MIN_ROWS=8`, `FULL_WIDTH=160`, `LINE_WIDTH=116` (21-24) |
| `theme.py` | 126 | colour-role -> Rich Style tables per depth (truecolor / 256 / standard) | `ROLES` (16), `style_for` (111), `STATE_ROLE` (95) |
| `sanitize.py` | 48 | strips escape sequences / control / bidi chars from untrusted worker text | `sanitize(text, mode)` (27) |
| `snapshot.schema.json` | 158 | JSON Schema draft-07 of snapshot v1, titled "PROPOSED, not an Orca contract" (line 3) | see section 3 |
| `fixtures/` | 18 JSON + `__init__.py`, 862,823 bytes | synthetic variants (base, uneven, shared-unmapped, historical, long-identifiers, source-loss, missing-fields, duplicate-out-of-order, empty, injection; parse.py:750-761) plus 4 `golden-*` worker-list samples, 4 `golden-question-*` samples and `question-cap-100.json` | loaded via `importlib.resources` by `load_fixture` (parse.py:801); largest: golden-contradictory 234,753 B, base 127,843 B |

Registration: `src/superclaude/cli/main.py:590` imports `observe_group` (deferred, to avoid a circular import) and `main.py:592` does `main.add_command(observe_group, name="observe")`.

## 2. Command surface: `superclaude observe`

Defined at commands.py:449-521 as `@click.group(name="observe", invoke_without_command=True)`. It is a group but has NO subcommands (grep for `observe_group.command`/`add_command` in the package finds none); with no subcommand it runs the observer itself (commands.py:508-521). So the surface is flags only.

| Flag | Type / default | Effect (cite) |
|---|---|---|
| `--once` | flag, off | one read, print plain-text record to stdout, exit (453; `run_once` 244) |
| `--width` | Choice 160/116/80, none | bind output width; with `--once` prints the rendered screen text instead of the record (455-460; 257-262). Styled escapes only when colour is on AND stdout is a TTY (259) |
| `--ascii` | flag, off | ASCII only; also auto when encoding is not UTF-8 (terminal.py:115 says that part is PROPOSED) |
| `--fixture TEXT` | none | replay a bundled synthetic variant, no Orca call; validated at parse time by `load_fixture` (427-435) |
| `--run TEXT` | none | restrict to one Orca run id; regex `^[A-Za-z0-9_][A-Za-z0-9_.:-]{0,127}$` (adapter.py:52, marked PROPOSED) |
| `--snapshot FILE` | path, none | write JSON snapshot there; live default is `<state_dir>/snapshot.json` (commands.py:405-408) |
| `--questions` | flag, off | list coordinator questions (Orca message type `question`) of the ONE `--run` Run; needs `--run`, live source (487-496) |

No `--interval`, `--no-snapshot`, `--json` or output-dir flag exists. (`Deps.interval` is a test seam, commands.py:147.)

Modes: `--once` -> one-shot (no TUI, works on any platform); otherwise interactive full-screen (`run_interactive` 375).

Exit codes (derived from `execute`/`run_*`; no central table in code):
- 0: normal end, `q`, Ctrl-C (commands.py:347, 363), `--once` success.
- 1: `--once` snapshot write failed (266-268); interactive render exception, "observe: display failed" (368-369); `--questions` with the gate guard closed (196; currently unreachable because `QUESTION_GATE_PASSED=True`, 67).
- 2: `--questions` without `--run`, with `--fixture`, or with an invalid run id (184-194); interactive on `win32` (377-379); interactive with no terminal on stdin (385-387). Click `BadParameter` for bad `--width`/`--fixture`/`--run` also exits 2 (standard click behaviour, UNVERIFIED by running).
- Refusals at 414-417 go to stderr; the two interactive refusals (378, 386) print to STDOUT (no `err=True`).
- No validated Orca CLI: not a failure. Screen/record shows `NOT AVAILABLE (no Orca CLI validated)` (view.py:51; collector.py:252-270 state NOT_AVAILABLE, code `not-found`); `run_once` then returns 0 (269). UNVERIFIED by running.

Interactive keys (view.py `apply_key`, ~1245-1300; footer text view.py:91,128): `j`/`k`/Up/Down move; Enter opens INSPECTOR; Esc back; `d`/`u` scroll inspector 3 lines; `/` filter; `h` toggle historical rows (released/retained, view.py:36); `m` mark a baseline for change flags; `e` export a timestamped plain-text record; `q`/Ctrl-C quit; with link on `n`/`p` select a question (1286-1289). `Effect` has only NONE/EXPORT/QUIT (view.py:1162-1167): "no effect ever reaches Orca".

## 3. Data read, data model, data written

### 3a. What it reads (Orca CLI only; no transcripts, no repo files, no network)
Every live read is a subprocess of the Orca CLI, no shell, own session, stdin=DEVNULL (adapter.py:232-238). Exactly three argv shapes are allowed (adapter.py:1-7, 135-170):
1. Discovery probe (made by `install_user_setup._find_orca`, install_user_setup.py:247-270 in the snapshot): `<orca> skills list --json`, accepted only if the output lists a topic named `orca-cli` (so the GNOME screen reader `orca` is never used). Candidates come from `_ORCA_CLIS` (not read here).
2. Worker list: `<orca> orchestration worker-list --json --limit 100 [--run <runId>] [--cursor <cursor>]` (adapter.py:29, 173-183). Paged; per-cycle cap 5 calls (`MAX_CALLS_PER_CYCLE`, 57); 4 when `--questions` is on (collector.py:32).
3. Questions (R2, only with `--questions` + `--run`): `<orca> orchestration check --all --types question --run <runId> --json` (adapter.py:32, 186-190). Note `check` is also on the forbidden list (adapter.py:37); the question template is an explicit exemption (`_option_positions` 121-132). Forbidden prefixes: check, --ack, --wait, --retry-request, --peek, dispatch, inbox, run-use, run-create, send, ask, reply, reset (34-50). Tests assert no module but the adapter imports subprocess (test_commands: `test_no_module_other_than_the_adapter_imports_subprocess_and_none_names_an_orca_...`). The `check` template carries no `--ack`/`--wait`/`--peek`, so the code intends a non-acknowledging read; whether the real Orca `check` marks messages read is UNVERIFIED here (questions.py:12-16 states rows carry no read marker).

Limits: per-call timeout 10 s (`PER_CALL_TIMEOUT`, adapter.py:60, comment "UNVERIFIED until the first permitted live read measures it"), stdout cap 8 MiB, stderr keep 2 KiB (58-59), cycle budget 15 s, poll interval 15 s, backoff doubles to 60 s on failure (collector.py:28-30, 306), STALE after 45 s without a good read (view.py:33). Cursor/ run-id syntax checks are marked PROPOSED (adapter.py:52-55).

Worker-row keys read (parse.py:58-89, 31 verified paths): dispatchId, taskId, runId, workerState, dispatchStatus, terminalState, `resource.{id,ownershipState,releaseState,worktreeId,ownerDispatchId,originDispatchId,recoveryAttemptCount}`, `projection.{outcome,role,provider.id,host.id/kind,workspace.id/kind,stage.worker/dispatch/activity/detail,nextAction.kind,liveness.{verdict,source,observedAt},evidence.{durable,liveStatus,lastObservedAt}}`. Unknown keys are counted and dropped (parse.py docstring 1-6). Question rows: keys "seen on probe Runs only, UNVERIFIED for other Runs" (parse.py:410); the payload may carry a dispatchId used to link a question to a worker row (parse.py:467-476; `PAYLOAD_CAP=64 KiB`, `ASK_CAP=400` chars).

Fixture mode reads bundled JSON under `observe/fixtures/` and never calls Orca (collector.py:92-129; `FixtureSource.read_questions` always fails with `no-question-fixture`, 125-129).

### 3b. Snapshot data model (`snapshot.schema.json`, schemaVersion 1, "additive-only", unknown value = string `"UNKNOWN"`, lines 3-4)
- Top level (required, additionalProperties false; lines 7-9): `schemaVersion` (const 1), `producer{name,version}` (name `superclaude-observe`, view.py:32; version = `superclaude.__version__`, view.py:17), `cycle`, `generatedAt` (UTC `...Z`), `source{namespace,status OK|STALE|ERROR|UNKNOWN,observedAt,error?}`, `page{hasMore,total,limit}`, `scope`, `counts`, `rows[]`; optional `collection{state COMPLETE|PARTIAL|MISMATCH,collected,changedDuringRead,duplicatesIgnored}` (55-64) and `questions{...}` (65-94).
- `source.namespace` = realpath of the validated Orca binary (adapter.py:379-381) or `fixture:<variant>`.
- Row (97-156): dispatchId, taskId, runId, workerState, dispatchStatus, terminalState, role, provider, hostKind, hostId, `stage{worker,dispatch}`, outcome, `liveness{verdict,source,observedAt}`, `evidence{durable,liveStatus,lastObservedAt}`, nextAction; optional orderUnknown, notReobserved, absentFields[]. Mapping from typed Row in export.py:25-46. Note the snapshot drops resource.*, workspace.*, stage.activity/detail even though parse reads them (UNVERIFIED that this is deliberate).
- `questions` group (opt-in): runId, state PENDING|OK|STALE|FAILED, observedOpen, windowFull, retained, evicted, `closureEvidence` const "unavailable", items[{id,createdAt,ageSeconds,inWindow}]. "No subject, body, handle or payload is ever exported" (schema line 66).

### 3c. What it writes
- Plain-text record (`record_text`, export.py:71-86): header lines, counts strip, one line per ROW (`dispatchId=... | run=... | workerState=... | dispatchStatus=... | terminalState=... | outcome=... | nextAction=... | liveness=... | evidenceAge=... [| flags=...]`, 53-68), then question lines (every question id, never the text). Goes to stdout with `--once`; with `e` in interactive mode written to `<state_dir>/observe-<generatedAt with : -> ->.txt` (export.py:247-250; commands.py:348-354).
- JSON snapshot (`snapshot_json`, export.py:219-224): `json.dumps(indent=2, sort_keys=True)`, every collected row regardless of filter. Written (a) with `--snapshot FILE` in either mode, (b) automatically in LIVE interactive mode, once per published cycle (commands.py:332-339, 408: `write_snapshots=live or bool(options.snapshot)`), to `<state_dir>/snapshot.json`, overwritten each cycle (no history). Fixture mode writes none unless asked.
- Location: `state_dir()` = `$XDG_STATE_HOME/superclaude/observe` if absolute, else `~/.local/state/superclaude/observe` (export.py:236-244). Files via temp file + fsync + `os.replace`, mode 0600 (257-274; mkstemp default is 0600), dir mode 0700.
- Nothing else is written: no Orca write, no repo files, no logs, no database.

Interactive vs one-shot: both. TUI = Rich `Live(screen=True, auto_refresh=False)` over a console built by `terminal.make_console` (commands.py:275-303) plus a stdlib key reader (`termios`+`tty`+`select`, keys.py:15-20) - no curses, no Textual. Loop: collector runs in a daemon thread (collector.py:335-343), main thread reads keys with 0.1 s timeout and redraws on change or every 0.5 s (commands.py:57-61, 306-371). Screen layouts by width class 160 / 116 / 80, min 80 cols x 8 rows (terminal.py:21-27); badge "READ ONLY" on the title bar (view.py:123).

## 4. Built vs not built; stage markers

Everything in the package is built and wired; no `TODO`, `NotImplemented` or stub function was found (grep of `*.py` for TODO/not implemented/stub returned only unrelated "stub" = a clipped-question-row name, render.py:63,727-762). Stage vocabulary inside the code:
- "R2" = coordinator-questions panel (collector.py:55,191; export.py:90; questions.py:1; parse.py:410). Gate constant `QUESTION_GATE_PASSED = True` (commands.py:67) citing owner record `.dev/issues/409/owner-pass-record-20261112.md` (QUESTION-OBSERVATION passed 2026-11-12).
- "R3" = question-to-worker link, Decision Desk, `n`/`p` select (view.py:96-112, 255, 898; parse.py:467). Gate constant `QUESTION_LINK_PASSED = True` (commands.py:70) citing `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` section QUESTION-LINK.
- "R0" = key-reader spike (tests/observe/test_keys_spike.py:1). tests/observe/release1_surface.py + golden_release1_*.json pin the "Release 1" surface (test_golden_contract.py, test_registration.py "release-gates.md reading 1").
- So the code is past Release 1 and ships R2 + R3 behind two Python constants that are both True. Setting either False disables the question read entirely (no Orca call, not even discovery, commands.py:63-64, 414).
- The cited spec/gate files are NOT in the snapshot (`.dev/issues/409/bmad/...` absent); in the stale checkout `.dev/issues/409/` has README.md, description.md, flags.md, issue-body.md and orca-observer-design-package.zip but no `bmad/spec-orca-observer/`. The gate claims are therefore UNVERIFIED from this scope (the Orca dashboard/design material for issue 409 is another slice's concern).
- Honest "not known" surfaces by design: SETTLED, POLICY FROZEN and cost show `unavailable (no source)`; "Human questions: source UNVERIFIED ..." gap notice shown until a question read succeeds (view.py:45-52, 120-121); question closure is never inferred (`closureEvidence: unavailable`).
- Docs: `docs/user-guide/cli-groups.md:40-54` documents the flags (matches code; it does not list the exit codes). README.md:136 lists observe under "read-only supervision of Orca workers". CHANGELOG.md has NO observe entry (grep for "observe"/"observer" hits only unrelated lines 170, 365). `docs/testing/v6.0.0/post-release-report.md:56,168,173` records gaps: no task guide, no sysop guide, "no technical doc for `superclaude observe` (13 source files)".

## 5. Consumers of its output
- Primary: a person at a terminal (full-screen TUI; or `--once --width N` for a pasteable screen). The footer, READ ONLY badge and disclosure lines are written for humans.
- Secondary: tools that read `<state_dir>/snapshot.json` or `--snapshot FILE` (versioned schema; "Consumers reject an unknown major schemaVersion", schema line 4). No in-repo consumer exists: a grep across src, tests, scripts, docs and .github for `cli.observe`, `superclaude observe`, `superclaude-observe` finds only main.py, cli-groups.md and the v6.0.0 post-release files. No agent, skill or command (including `/sc:sweep`) calls it or reads its snapshot. Whether the Orca dashboard design (issue 409) intends to consume it is UNVERIFIED here.
- `--once` plain-text record is stable-shaped one-line-per-row text and is scriptable, but nothing in the repo scripts it.
- Relation to sweep: independent. observe is a live poller of `orchestration worker-list`; sweep is a separate one-shot report command (documented in the same cli-groups.md, lines 19, 25-38). Not read in this slice.

## 6. Tests (tests/observe/, 36 files, 13,638 lines incl. goldens and helpers; counts are `def test_` per file)
render 135 tests (2,447 lines), view 61, parse 44, adapter 43, commands 36, collector 32, session 27, snapshot_schema 22, fixtures 22, export 20, golden_contract 19, terminal 18, questions 15, sanitize 10, theme 9, keys_spike 8, inspector_scroll 7, question_cap 6, styled_capture 6, live_screen_pty 6, registration 5, question_quiet_scope 4, cancel 3, deep_nesting 3, linkoff_screen_reference 3, height_budget 1. Helpers: conftest.py (516), record_golden.py (385), record_golden_questions.py (297), live_child.py, spike_child.py, release1_surface.py; data: golden_release1_surface.json (606), golden_release1_records.json, golden_questions_linkoff.json.
Covered themes (from test names): allow-listed argv only; no Orca = "not available" not "empty fleet"; snapshot only when asked / once per cycle in live mode; unwritable snapshot path -> non-zero; non-POSIX and no-TTY refusals; render exception restores terminal and exits non-zero; Ctrl-C quiet exit; XDG state dir; question gate/link guards (T56); help text contents; schema validity; sanitizer; deep-nesting JSON; real-pty Live+KeySource spike (`observe_real_process` marker lifts the subprocess guard, pyproject.toml:148). Not run in this slice.

## 7. Proposed deep-investigation agents (2)
1. **Adapter + data contract + exports** (topic: "what the observer reads from Orca and what it emits"). Files: adapter.py, parse.py, collector.py, questions.py, export.py, snapshot.schema.json, fixtures/golden-*.json, install_user_setup.py:247-270 (`_find_orca`), tests/observe/test_adapter.py, test_parse.py, test_collector.py, test_snapshot_schema.py, test_golden_contract.py. Why: this is the part another system (dashboard, sweep, an agent) could depend on; needs exact worker-list/`check` field semantics, error-code table, paging/backoff/STALE/merge rules (conflict, order-unknown, duplicates), question retention rules and the schema-vs-code gaps (rows dropped fields, `collection` meaning). Should also check whether Orca's `check --all --types question` is truly non-acknowledging.
2. **Interaction layer + gates + docs/status** (topic: "how a person uses it and what release stage it is"). Files: commands.py, view.py, render.py, keys.py, terminal.py, theme.py, sanitize.py, tests/observe/test_commands.py, test_session.py, test_view.py, test_render.py, test_live_screen_pty.py, docs/user-guide/cli-groups.md, README.md:136, CHANGELOG.md, and the issue-409 design/gate material in the checkout (`.dev/issues/409/`, `docs/designs/`, other slices' paths) to confirm R2/R3 gate records and the intended relationship with the dashboard and sweep. Why: needs the full key map, width layouts, Decision Desk behaviour, exit-code table verified by running `--help`/`--once --fixture base` (harmless), and a verdict on Release stage and doc gaps.

Open items for the main agent: (a) confirm whether any dashboard/sweep code in other slices reads `snapshot.json`; (b) confirm the QUESTION-OBSERVATION and QUESTION-LINK gate records exist anywhere in git (not in snapshot); (c) confirm exit code 0 with no Orca CLI by running `superclaude observe --once` (read-only, but it calls `skills list`).
