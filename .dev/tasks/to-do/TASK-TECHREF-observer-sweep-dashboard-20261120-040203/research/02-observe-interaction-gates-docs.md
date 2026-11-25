# Research: How a person uses the observer and which release stage it is in
**Investigation type:** Code Tracer + Doc Analyst
**Scope:** src/superclaude/cli/observe/{commands,view,render,keys,terminal,theme,sanitize}.py; tests/observe/*; src/superclaude/cli/main.py registration; docs/user-guide/cli-groups.md; README.md; CHANGELOG.md; docs/testing/v6.0.0/post-release-report.md; issue 409 gate records; PRs #503, #514, #577, #592, #598, #673
**Status:** Complete
**Date:** 2026-11-20
---

Path convention: every code path below is relative to the repo root of the read-only export of origin/master 61ac2c2e6 (/home/coder/.cache/ic-snap-20261120/master) unless it starts with `/home/coder/workspaces/IronClaude` (checkout, docs branch docs/409-orca-dashboard-designs).

## 1. Command surface: src/superclaude/cli/observe/commands.py (525 lines)

**Click shape.** One `click.group(name="observe", invoke_without_command=True, help=HELP)` named `observe_group` (commands.py:449-521). It is a group but defines no subcommands; `if ctx.invoked_subcommand is not None: return` (commands.py:508-509) is the only subcommand handling. Running `superclaude observe` with no flag starts the interactive loop. `__all__` = Deps, Options, SystemClock, execute, observe_group, run_loop (commands.py:524).

**Flags (commands.py:450-496), all verified in code:**

| Flag | Click declaration | Behavior (code) |
|---|---|---|
| `--once` | is_flag (450-454) | Read once, print text, exit. Routed at `execute` (commands.py:419-420) to `run_once` |
| `--width` | `click.Choice(("160","116","80"))`, default None (455-460; WIDTHS at 61) | Binds the layout width. With `--once` prints the rendered screen text instead of the record (commands.py:257-260). Converted with `int(width)` (commands.py:512) |
| `--ascii` | is_flag, dest `ascii_mode` (461-466) | Forces ASCII; passed into `resolve_policy` via `{"ascii": options.ascii}` (commands.py:157-159) |
| `--fixture` | text, callback `_check_fixture` (467-472) | Replays a synthetic fixture via `FixtureSource`; callback calls `load_fixture` and turns ValueError into `click.BadParameter` (427-435) |
| `--run` | dest `run_id`, callback `_check_run` (473-479) | One Run only; `check_run_id` raising `ArgvRejected` becomes `click.BadParameter` (438-446) |
| `--snapshot` | `click.Path(dir_okay=False)` (480-486) | JSON snapshot file; with `--once` written after the text (commands.py:264-268); in the interactive loop, default is `snapshot_path(directory)` in the state dir (commands.py:405-407) |
| `--questions` | is_flag (487-496) | Lists coordinator questions of the one `--run` Run; guarded by `QUESTION_GATE_PASSED` (see section 5) |

Options dataclass is frozen with the seven fields (commands.py:121-129). `Deps` (commands.py:132-147) holds injected runner, discover, clock, env, encoding, size, platform, key_source, screen_factory, state_directory, stdout, interval; used by tests.

**Constants.** POSIX_ONLY_TEXT (53-55); NO_TERMINAL_TEXT (56); READ_TIMEOUT = 0.1 s (57); REDRAW_SECONDS = 0.5 (58-60); default poll interval 15.0 passed in `run_interactive` (commands.py:391). HELP text (81-99) states: read-only, "no key and no option maps to an Orca call", poll cap "one read every 15 s, at most 5 calls per read" per observer process, and the --questions description.

**Execution path.** `execute(options, deps)` (commands.py:412-421): (1) `_question_refusal` before any Orca call (414-417); (2) `--once` -> `run_once`; else `run_interactive`. `observe_group` calls `ctx.exit(code)` when code is non-zero (commands.py:519-521).

### 1.1 Exit-code table (every value cited to code)

| Code | Condition | Where |
|---|---|---|
| 0 | `--once` read printed (snapshot, if asked, written) | run_once returns 0 (commands.py:269) |
| 0 | Interactive loop ended by `q` (Effect.QUIT) | commands.py:346-347 |
| 0 | Interactive loop ended by Ctrl-C (decoded key `ctrl_c`) | view.py:1250-1251 -> Effect.QUIT |
| 0 | Interactive loop ended by KeyboardInterrupt (SIGINT handler in keys.py raises it) | commands.py:362-363; keys.py:115-117 |
| 1 | `--once` snapshot could not be written ("snapshot failed: ...", stderr) | commands.py:264-268 |
| 1 | Render failure in the loop ("observe: display failed: ...", stderr) | commands.py:364-369 |
| 1 | `--questions` with `QUESTION_GATE_PASSED` False ("question read not enabled...") | commands.py:195-196 (unreachable today: constant is True) |
| 2 | `--questions` with `--fixture` (QUESTIONS_NEED_LIVE_TEXT) | commands.py:187-188 |
| 2 | `--questions` without `--run` (QUESTIONS_NEED_RUN_TEXT) | commands.py:189-190 |
| 2 | `--questions` with a `--run` id that `check_run_id` rejects | commands.py:191-194 |
| 2 | Interactive on `sys.platform == "win32"` (POSIX_ONLY_TEXT, printed to stdout) | commands.py:377-379 |
| 2 | Interactive with no terminal on standard input (NO_TERMINAL_TEXT, stdout) | commands.py:385-387 |
| 2 | Click usage error (bad `--width` choice, bad `--fixture` name, bad `--run` id) | click `Choice`/`BadParameter`; callbacks at commands.py:427-446. This is click's own exit code, not set in this module [click default behavior; not read in this repo] |
| 143 (128+15) | SIGTERM while the key source holds the terminal | keys.py:119-121 |
| 129 (128+1) | SIGHUP while the key source holds the terminal | keys.py:123-125 |

Notes: the `--questions` refusals print to stderr via `click.echo(..., err=True)` (commands.py:416); the two interactive refusals print to stdout (commands.py:378, 386). `--once` with a live source whose Orca read fails still returns 0: `run_once` returns 1 only for a snapshot write failure (commands.py:264-269); a failed read shows as a view state (FAILED), not an exit code [CODE-VERIFIED on run_once; collector internals not part of this file].

### 1.2 `--once` text record versus interactive loop

- `run_once` (commands.py:244-269): builds `Collector(source, clock, run_id, questions=_questions_on, link=_link_on)`, `collector.run_once()`, `apply_cycle(Session(), ...)`, `build_view`. Without `--width` the output is `record_text(view)` (plain-text record from export.py); with `--width` it is the rendered screen through a recorded console (`_screen_text`, commands.py:234-241), styled (colour/weight escapes) only when the colour policy has a colour system AND stdout is a TTY (`_stdout_is_tty`, 225-231, and 259). Piped output stays plain.
- `run_interactive` (commands.py:375-409): refuses on win32 (377-379), imports `KeySource` lazily (380), enters `with keys:` (384), refuses if `not keys.available` (385-387), builds the Collector with interval 15.0 and the question/link switches, picks `state_dir()` and the snapshot file, and calls `run_loop`. `write_snapshots=live or bool(options.snapshot)` (commands.py:408): live runs write one snapshot per poll cycle by default; fixture runs write only with `--snapshot`.
- `run_loop` (commands.py:306-372): starts the collector (323); each pass takes `collector.latest()`, applies a new cycle to the session (328-331), writes at most one snapshot per cycle "after failures too" (332-339), reads a key with 0.1 s timeout (341), applies it (343), on `Effect.EXPORT` writes `record_path(directory, view)` atomically and sets the message `exported <path>` or `export failed: ...` (348-354), consumes the SIGCONT redraw flag (356), and repaints when dirty or 0.5 s since last draw (358-361). `finally` runs `collector.stop()` and `screen.close()` (370-372).
- `LiveScreen` (commands.py:275-303): `rich.live.Live(screen=True, auto_refresh=False)`; re-created when the shape tuple (width, height, ascii, no_color, color_system) changes (283-297).
- Read-only claim: module docstring says the only Orca calls are the ones adapter.py makes (commands.py:3-4). In commands.py the only writes are the snapshot file and the exported record file (`write_atomic`) on local disk.

### Key Takeaways
- Single click group `observe` with seven flags, no subcommands.
- Interactive loop polls every 15 s, repaints at least every 0.5 s, writes one JSON snapshot per cycle in live mode.
- `--once` prints the plain record by default and the width-bound screen text with `--width`.
- Exit codes 0/1/2 plus signal-derived 129/143; a failed Orca read is not an exit code.

## 2. Key map: keys.py (decoder) and view.py `apply_key` (meaning)

**Split of responsibility.** `keys.py` (236 lines, POSIX only, imports `termios`, `tty`) decodes bytes into `Key` objects; the meaning of each key lives in `view.py:apply_key` (view.py:1246-1300). Key names the decoder emits (view.py:30 `KEY_NAMES`): up, down, enter, escape, backspace, ctrl_c, text.

**Decoder (keys.py).**
- `KeySource(fd=None)` context manager (keys.py:36-49): cbreak via `tty.setcbreak` with ISIG kept so Ctrl-C raises SIGINT (keys.py:1-6, 59-61); a non-TTY descriptor makes `available` False and `read` sleeps then returns None (keys.py:54-58, 147-149).
- Read: max wait `MAX_TIMEOUT = 0.25` s (22); a lone ESC waits `ESC_WAIT = 0.05` s for an arrow sequence (23, 157, 163-165).
- `_take` (176-195): 0x0D/0x0A -> enter; 0x7F/0x08 -> backspace; 0x03 -> ctrl_c; other control bytes swallowed; printable ASCII -> text; UTF-8 multi-byte via `_take_utf8` (197-215), non-printable dropped.
- `_take_escape` (217-235): `ESC [ A`/`ESC [ B` and `ESC O A`/`ESC O B` -> up/down; any other CSI/SS3 final byte swallowed (returns None); ESC followed by a non-bracket byte -> escape. Left, right, Home, End, PgUp, PgDn are not mapped [CODE-VERIFIED keys.py:227, 233].
- Signals: handlers for SIGINT, SIGTERM, SIGHUP, SIGTSTP, SIGCONT installed only in the main thread (keys.py:94-105). SIGINT -> restore terminal, raise KeyboardInterrupt (115-117); SIGTERM/SIGHUP -> restore, `SystemExit(128+signo)` (119-125); SIGTSTP -> restore terminal then SIGSTOP (127-132); SIGCONT -> re-enter cbreak, set redraw flag (134-136); `consume_redraw` (138-141).

**Full key map (view.py:1246-1300), in evaluation order.** Keys change the Session only; "there is no refresh key and none reaches Orca" (view.py:1249).

| Order | Key | Condition | Effect | view.py line |
|---|---|---|---|---|
| 1 | Ctrl-C | any focus (checked before filter focus) | Effect.QUIT | 1250-1251 |
| 2 | any key while `focus == "filter"` | filter typing mode | text appends to filter; Backspace deletes last char; Enter or Esc returns to list focus; arrows and others do nothing | 1252-1253, 1236-1243 |
| 3 | Up arrow or `k` | list or inspector focus | `_move(-1)`: select previous visible row (first press with nothing selected selects the last); resets inspector scroll | 1257-1259, 1195-1209 |
| 4 | Down arrow or `j` | list or inspector focus | `_move(+1)`: next visible row (first press selects the first) | 1260-1261 |
| 5 | `d` / `u` | inspector focus only, and an inspector exists | scroll inspector down/up by `INSPECTOR_SCROLL_STEP = 3` lines, clamped | 1261-1265; step at 131 |
| 6 | `q` | any non-filter focus | Effect.QUIT | 1266-1267 |
| 7 | `e` | any non-filter focus | Effect.EXPORT: loop writes the plain-text record file and shows `exported <path>` | 1268-1269; commands.py:348-354 |
| 8 | `m` | any non-filter focus | new "changed since" baseline from all rows; `marked=True`, `mark_wall_time=now` | 1270-1280 |
| 9 | Esc | inspector focus | back to list focus, scroll reset | 1281-1282 |
| 10 | `n` / `p` | list focus, questions panel with link on and at least one question line | `_move_question`: next/previous question, oldest first, stops at the ends; none selected starts at first (n) or last (p) | 1285-1289, 1212-1224 |
| 11 | Esc | list focus, link-on panel, a question selected | clears the question selection | 1290-1291 |
| 12 | Enter | list focus and a row is selected | focus becomes inspector | 1292-1293 |
| 13 | `/` | list focus | focus becomes filter (substring match over eight cells, `_matches` view.py:587-600) | 1294-1295 |
| 14 | `h` | list focus | toggle show-historical (terminal state `released` or `retained`, HISTORICAL_STATES view.py:36) | 1296-1299 |
| - | anything else | | no change | 1300 |

Footer key lines on screen: `QUESTIONS_KEYS_LINE` = "j/k move  Enter detail  / filter  h history  e export  q quit" (view.py:91, also `KEYS_LINE` at 118); with the link on, `QUESTIONS_LINK_KEYS_LINE` adds "n/p question" (93-95); inspector help `INSPECTOR_HELP` = "Esc back  j/k move  d/u scroll  e export  q quit" (128). The comment at view.py:90 says Up/Down, Esc, m, d/u still work although not listed; `m` is named in neither keys line [CODE-VERIFIED].

**Observations (not recommendations).** `n`/`p` do nothing when the link is off or the panel has no lines (fall through to view.py:1300). Ctrl-C is both a decoded key and a SIGINT; both exit 0.

### Key Takeaways
- 14 distinct key behaviors; no key refreshes data, calls Orca, writes to Orca, answers a question or sends a message.
- Question selection (n/p/Esc) exists only with `--questions` and the link on, and only when the panel has lines.
- Arrow keys up/down only; left/right/page keys are swallowed.

## 3. Width layouts, terminal policy, theme, sanitizer, Decision Desk

### 3.1 terminal.py (193 lines): the one owner of colour, ASCII, width class, clipping, Console

- Thresholds (terminal.py:21-24): `MIN_WIDTH=80`, `MIN_ROWS=8` (marked PROPOSED, CD-4), `FULL_WIDTH=160`, `LINE_WIDTH=116`. `width_class(width)` (82-89): >=160 "full"; >=116 "line"; >=80 "short"; else "narrow". `--width` accepts only 160, 116, 80 (commands.py:61, 455-460). Without `--width`, the live terminal size is used (`detect_size`, 136-139; fallback 80x24) so any real width maps to one of four classes.
- Below 80 columns every view prints `TOO_NARROW_TEXT` "terminal too narrow (min 80)" plus the counts and the gap notice (terminal.py:26; render.py:1263-1268). Fewer than 8 rows prints `TOO_SMALL_TEXT` "terminal too small (min 8 rows)" plus collected text and gap notice (terminal.py:27; render.py:1269-1272).
- `resolve_policy` (104-124): `NO_COLOR` set and non-empty disables colour (113-114); ASCII when `--ascii` OR the stream encoding is not UTF-8 (116, "PROPOSED"); colour depth `_color_system` (92-101): none for `NO_COLOR`/TERM dumb/unknown, "truecolor" for COLORTERM truecolor/24bit, "256" for TERM ending 256color, else "standard".
- `make_console` (142-157) is the only place a Rich `Console` is built (explicit width/height, no markup, no emoji, no highlight, safe_box in ASCII). `glyph` table (30-51) holds unicode/ASCII pairs (selected marker, hrule, alive dot, big-digit block, round and heavy box characters). `clip` (170-192) is the single truncation helper; a cut ends in `>`.

### 3.2 render.py (1462 lines): layouts per width class

Module contract: lays out and truncates only; every literal comes from `View`; text built as `rich.text.Text` from data, never markup (render.py:1-11). Each screen line is a `Line` (plain text plus role spans); `render()` (1449-1461) turns spans into Rich styles only when `policy.color_system` is not None.

**Ledger columns by width class (`_columns`, render.py:480-568):**

| Width class | Columns (header: width) | Source lines |
|---|---|---|
| full (>=160, "160") | marker 2, dispatchId (<=48), run 12, workerState 12, status (default 36, grows to longest), nextAction.kind 16, alive 14, evidence age 12 | 494-520 |
| line (116-159, "116") | marker 2, kind 18, dispatchId (<=48), alive 14, status (default 36), age 7 | 521-543 |
| short (80-115, "80") | marker 2, kind 14, dispatchId (remainder), alive (5-12), status (default 30), age 6 | 544-568 |

Status cell shows the badge `ACTIVE` only when dispatchStatus/terminalState/outcome are exactly active/active/none; any other combination shows the three raw values joined by `/` (render.py:426-444). Liveness cell is a dot, spelled out after the dot for non-alive verdicts (447-452). The next-action kind is verbatim and never colour-classified (579-580). Selected row marker and `*` change marker (455-458). `m`-baseline and `*` flags come from view.py `_changes` (951-965).

**Screen anatomy (`_compose`, render.py:1258-1446).** Title bar with right-aligned `READ ONLY` badge (1114-1126; screen only, never in the record per view.py:123-124); second header line (freshness cells); counts strip (`counts_line_objects`, max 2 lines, protected tokens wrap, others cut with `>`; 364-411); optional `changes_line`; then either the gap notice (with `GAP_NOTICE` text from view.py:45-47: `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`) or, when questions are on and have been read, the R2 panel; the ledger (framed when it leaves at least `MIN_LEDGER_ROWS=3` rows, `_framed_ledger` 1170-1245; else plain, `_plain_ledger` 1129-1161); a rule line and a footer of keys plus `shown x/y`. Inspector view replaces the ledger when focus is inspector (1418-1423; `_inspector_lines` 660-690 with above/below scroll lines).

**R2 panel layouts A, B, C (render.py:942, 1083-1111, 1376).** `LAYOUTS = ("A","B","C")`: A = count strip + list frame + RETAIN CONTEXT pane; B drops the RETAIN pane under height pressure; C drops the strip too (count becomes a plain list line). Widths 160 and 116 try A, B, C in order and take the first that shows at least `MIN_QUESTION_ROWS=3` rows (or fewer if fewer exist); 80 columns uses C only (render.py:1376, 1379-1386). The count strip is a cyan frame titled "SEEN, NOT RESOLVED" with a 3-row block-digit font when the figure is digits or `+` (render.py:209-234, 945-981). The oldest questions stay on screen when the list is cut; the newer ones are reachable only by export, and the cut line says so (view.py:305-321; owner decision 2026-11-12 per the docstring).

**Heights.** The questions win over the ledger on a short terminal (render.py:1320-1321): the ledger keeps its title, one row and its overflow line.

### 3.3 Decision Desk (R3), built only with `--questions` and the link on

- Model: `DeskView` (view.py:253-264) and `_desk` (888-948). It returns None unless the panel is link-on and a question is selected (904-905). Join is exact: the question's verified `dispatch_id` against `raw.dispatch_id` of a collected row (900-901, 913-915). Linked fields: dispatchId, workerState, dispatchStatus, terminalState, outcome, nextAction.kind, liveness, evidence age, resource.worktreeId (917-927). Notes: `DESK_WORKTREE_NOTE` ("worktree is evidence for this one session; other sessions in it are not inferred affected", view.py:99-102), `DESK_NOT_REOBSERVED`, `DESK_NO_READ`, `DESK_NOT_FOUND`, `DESK_PARTIAL`, and "worker list STALE/FAILED; values as of ..." (928-938). Unlinked: `DESK_UNKNOWN_SCOPE` "affected scope unknown" plus the link reason (939-940). Evicted selection: `DESK_EVICTED` (907-909). No text: `DESK_NO_TEXT` "question text not given" (944).
- Rendering: `_desk_question_pane` (render.py:787-806; heavy frame titled "DECISION DESK", age line then question text up to `DESK_TEXT_LINES=4` lines with `...`), `_desk_evidence_pane` (809-824; round frame titled "LINKED SESSION", rows session/state/alive/next/status/worktree from `_desk_rows` 832-879, worktree shown as "<id>  (this session only)" 878).
- Layout per width class (`_desk_widths`, 925-936; `_desk_block`, 1058-1080): full: left column = question pane over list, right column = evidence pane 80 wide (`RIGHT_DESK=80`, 921); line: question pane spans the width, evidence on the left and list 46 wide (`RIGHT_LIST=46`, 922) on the right; short: three panes stacked.
- Height fallback: if the desk does not fit, a one-line notice `DESK_HIDDEN` "decision desk hidden: terminal too short" goes inside the list frame; if even that does not fit the summary line names it (render.py:1328-1371, 1400-1405; view.py:109). The selected row in the list shows at most `DESK_STUB_CELLS=24` cells of question text ending in `>` (render.py:63, 759-763).
- No key in the desk acts on the question: n/p/Esc only move the selection (view.py:1285-1291). The question text from the payload is screen-only; "not written to the record or snapshot" per the HELP text (commands.py:97-98, 493-495) [export claim [CODE-VERIFIED] in section 4: export.py:101-102, 158-159].

### 3.4 theme.py (127 lines) and sanitize.py (49 lines)

- theme.py: sixteen colour roles (ROLES, theme.py:16-33) mapped to eight palette colours per colour depth (`_COLOURS`, 59-90); bold roles (54-56); `STATE_ROLE` maps only seven (field, exact raw value) pairs to a state role: workerState running/succeeded/failed, dispatchStatus completed/failed, liveness alive/live (95-103); "a display choice, not a count mapping and not a health verdict". `style_for(role, depth)` caches styles per (role, depth) (111-126); no blink, dim or reverse (docstring 7-8). It never builds a console or reads the environment.
- sanitize.py: `sanitize(text, mode="line"|"block")` (27-48) strips OSC, DCS/SOS/PM/APC, CSI (7-bit and 8-bit) and other ESC forms (`_ESCAPES`, 15-20), normalizes newlines, and drops Unicode categories Cc, Cf, Cs (24). Mode "block" keeps newlines (used for `stage.detail`, `stage.activity`, stderr in the inspector, per the docstring 30-31). It states that markup safety is not its job: the renderer never parses worker text as markup (sanitize.py:3-6; render.py:3-5).

### Key Takeaways
- Three width classes (160 full, 116 line, 80 short) change the ledger columns, the question-panel layouts (A/B/C at 160/116; C only at 80) and the Decision Desk arrangement (side-by-side, split, stacked).
- Below 80 columns or 8 rows the observer prints a short refusal plus the denominators and the gap notice.
- The theme maps only seven exact state words to colours and says it is not a health verdict.
- Text from workers is sanitized and never parsed as markup.

## 4. R2 (questions) and R3 (link, Decision Desk) runtime wiring, and the C8 reachability check

**Gate constants (src/superclaude/cli/observe/commands.py).**
- `QUESTION_GATE_PASSED = True` at commands.py:67, comment cites `.dev/issues/409/owner-pass-record-20261112.md`; the prose at 63-66 says plan Task 18 flipped it only against that record and that with False `--questions` makes no Orca call, not even discovery.
- `QUESTION_LINK_PASSED = True` at commands.py:70, comment cites `.dev/issues/409/bmad/spec-orca-observer/release-gates.md QUESTION-LINK`; prose at 68-69.
- `_questions_on(options)` = `options.questions and QUESTION_GATE_PASSED` (173-175); `_link_on` = questions on AND `QUESTION_LINK_PASSED` (178-180). Both are passed to `Collector(..., questions=, link=)` on the `--once` path (commands.py:247-253) and the interactive path (388-395).
- Tests pin both constants: `test_the_guard_is_true_only_with_a_cited_owner_record_that_exists` (tests/observe/test_commands.py:754-763) requires that a True guard cites `owner record: <path>` and that the path exists as a file under the repo root; `test_the_link_guard_is_true_only_with_the_recorded_gate_pass` (769-779) requires `release-gates.md` to contain `## QUESTION-LINK` and `QUESTION-LINK: passed`. Neither test can pass on the snapshot, because the snapshot export omits `.dev/` (see Gaps); on the real repo they read `.dev/issues/409/...`, which exists only on origin/master (verified in section 6).

**Call chain traced end to end (C8 check).**
1. `observe_group` -> `execute` -> `run_once`/`run_interactive` (commands.py:498-521, 412-421).
2. `Collector.__init__`: `self._questions = bool(questions and run_id)`; `self._link = bool(link and self._questions)` (collector.py:152-153).
3. `Collector._question_fields` calls `self._source.read_questions(clock, deadline, run_id)` (collector.py:214), then `parse_questions(reply.pages[0], namespace, number, run_id, link=self._link)` (collector.py:219-220) and `merge_questions(...)` (collector.py:230); sets `question_state` "OK" and `questions` (240-244). Questions fetch is capped separately: `QUESTION_PAGE_CAP = 4` worker-list calls per cycle plus one message call (collector.py:32-34, 273).
4. `LiveSource.read_questions` (adapter.py:469-512): builds argv with `build_question_argv` and runs it through the runner; one call, no paging; maps `consumer_fenced` and `no_active_terminal` error envelopes to source codes `consumer-fenced` and `no-active-terminal` (adapter.py:66-69, 503-507).
5. The argv template is `orchestration check --all --types question --run <runId> --json` (adapter.py:32; confirmed by test_commands.py:665-670: `["/opt/fake/orca","orchestration","check","--all","--types","question","--run",QRUN,"--json"]`). The allow-list `assert_allowed` accepts only three templates: discovery `skills list --json`, the 5-token worker-list template with optional `--run`/`--cursor`, and the 8-token question shape (adapter.py:135-170). `FORBIDDEN_PREFIXES` (adapter.py:34-50) includes `check`, `--ack`, `--wait`, `--peek`, `dispatch`, `inbox`, `run-use`, `run-create`, `send`, `ask`, `reply`, `reset`, but the verb `check` at token index 1 of the question template is excluded from the check (`_option_positions` returns positions minus {1,4,6}, adapter.py:121-126). Note that `--peek` is on the forbidden list and the test asserts it is absent (test_commands.py:672, 818), i.e. the observer calls `check` WITHOUT `--peek`. Whether that call consumes or acknowledges messages on the Orca side is [UNVERIFIED] by this topic's code (no Orca source here); the HELP states "Message bodies are received by this process; subjects are shown, bodies are not kept" (commands.py:94-95). The owner gate record (section 6) is where this was decided.
6. Rendering: `build_view` -> `_questions_panel` (view.py:709-885) -> `QuestionsPanel`; `_desk` (888-948); render.py `_panel_lines`/`_desk_block` (1083-1111, 1058-1080).
7. Fixture path: `FixtureSource.read_questions` returns `FAILED` code `no-question-fixture` (collector.py:125-129), but `_question_refusal` blocks `--questions --fixture` with exit 2 first (commands.py:187-188). So the fixture path never reaches it.

**Result of the C8 check (R2 questions, R3 link, Decision Desk, snapshot, `--once`):** all five are wired at the runtime entrypoint. R2 and R3 have a production caller chain (steps 1-6); the gate constants are True; the questions read is not dead-guarded. `--once` and the snapshot are reached from `observe_group` (commands.py:264-268, 405-408). **No unwired-capability DEFECT found for R2, R3, snapshot or `--once`.** DEFECT-CANDIDATES: none for these. (Different matter: see 5.3 for the snapshot having no in-repo consumer; that is absence of a consumer, not an unwired capability of the observer, and the HELP/docs do not claim a consumer.)

**What is screen-only and what reaches files [CODE-VERIFIED, export.py]:**
- Record (`record_text`, export.py:71-86 and `_question_lines` 89-118): every question as `<qid> | <age  subject  reason unknown>` and, with the link on, ` | dispatchId=<id or unknown> | link=<state>`; "never carries the question text (screen-only)" (export.py:101-102); test `test_once_record_question_lines_carry_the_link_suffix_and_never_the_text` (test_commands.py:822-836) asserts the payload text is not in the record. The record does carry the subject (`q.text`, view.py:811).
- Snapshot (`snapshot_dict`, export.py:183-216; `_questions_dict` 158-180): questions group with ids, times, counts and `closureEvidence: "unavailable"` only; "never subject or body" (export.py:159). Schema version 1 (export.py:20), schema file `src/superclaude/cli/observe/snapshot.schema.json` (exists per the Glob/Grep hit; not read in detail).
- Local files: state dir `$XDG_STATE_HOME/superclaude/observe` when absolute, else `~/.local/state/superclaude/observe` (export.py:236-244); record name `observe-<generatedAt with : -> ->.txt` (247-250); snapshot name `snapshot.json` (21, 253-254); atomic write mode 0600 with temp file, fsync and `os.replace`, dir mode 0700 (257-274).

### Key Takeaways
- Both R2 and R3 are live: the gates are True and the call chain from the click option to an Orca `orchestration check --all --types question --run <id> --json` call exists and is tested with a fake runner.
- The observer never runs `run-use` or binds a Run; fence codes surface as FAILED states with an instruction line.
- Question text from the payload is screen-only; the record has the subject and ids; the snapshot has ids, times and counts.

## 5. Interaction record: tests, release stage markers, consumers, docs

### 5.1 Tests that pin the interaction layer (tests/observe/)

Directory holds 41 entries (Glob): test_commands.py, test_session.py, test_view.py, test_render.py, test_live_screen_pty.py, test_keys_spike.py, test_registration.py, test_height_budget.py, test_terminal.py, test_theme.py, test_sanitize.py, test_questions.py, test_question_cap.py, test_question_quiet_scope.py, test_cancel.py, test_export.py, test_snapshot_schema.py, test_golden_contract.py, test_linkoff_screen_reference.py, test_inspector_scroll.py, test_deep_nesting.py, test_styled_capture.py, test_fixtures.py, test_collector.py, test_adapter.py, test_parse.py, fixtures and golden JSON files, plus helper scripts (live_child.py, spike_child.py, record_golden*.py, release1_surface.py, conftest.py).

Verified in tests/observe/test_registration.py (72 lines): the group is registered as `main.commands["observe"] is observe_group` (test_registration.py:16); the `--help` of `observe` lists all seven options and "never runs run-use" (22-35); `--questions` through the shipped CLI is refused with "question read not enabled" when the gate is monkeypatched False (38-48); `--once --fixture base` prints a record whose first line contains "SYNTHETIC FIXTURE base, not Orca data" and no ESC byte (51-56); main.py contains exactly one deferred registration block before `if __name__ == "__main__":` (59-71). Registration in main.py confirmed: import at src/superclaude/cli/main.py:590 and `main.add_command(observe_group, name="observe")` at line 592 [CODE-VERIFIED].

Verified in tests/observe/test_commands.py (889 lines): `--once` works with termios, tty and fcntl blocked and never imports keys.py (73-100); `--once --fixture base` record has 80 `dispatchId=` lines (103-111); `--width` 160/116/80 produce lines no wider than the width and keep the gap notice (114-130); `--ascii` yields ASCII-only (133-138); a live `--once` makes only allow-listed argv: `skills list --json` then one `orchestration worker-list --json --limit 100` (144-156); no validated Orca prints "worker-list NOT AVAILABLE (no Orca CLI validated)" and makes no calls (159-168); `--snapshot` written only when asked (174-200); unwritable snapshot exits 1 with "snapshot failed" (203-209); bad `--fixture`, `--run`, `--width` exit 2 with no traceback (224-235); win32 prints POSIX_ONLY_TEXT, exits non-zero, never imports keys (241-255); scripted keys j / "/" "w-0" Enter h m e q drive the session, exit 0 and release the terminal (310-357); failed export shows a message and the loop goes on (360-380); exactly one snapshot per published cycle, failed cycles included (413-453); fixture mode writes no snapshot unless asked (456-477); `e` writes one record under `XDG_STATE_HOME/superclaude/observe` (480-500); non-TTY exits 2 (503-511); a render exception exits 1 with "observe: display failed: boom" (514-534); Ctrl-C during a read exits 0 (537-551); the screen follows terminal size on each redraw 160 -> 116 -> 80 (554-572); no module except adapter.py imports subprocess and commands.py names no Orca verb (585-601); R2 refusals and R3 link wiring (627-889, see section 4).

### 5.2 Other interaction-layer tests (names and docstrings read; bodies not all read)

- tests/observe/test_session.py: 29 test functions found by grep (names at lines 68-541). They pin: first successful observation is the baseline (68), no baseline before a successful read (83), a later cycle never replaces it (93), `m` replaces it (157), added/removed rows count in "changed since" (136), selection by identity with clamping (195, 248), Enter opens and Esc leaves the inspector (273), filter mode takes letters including `q` (291), `h` toggles historical and `e`/`q` effects (325), "unknown keys do nothing and there is no refresh key" (339), "no key can reach the adapter or collector" (359), transitions never mutate their input (396), n/p/Esc question-selection rules including filter and inspector focus and link-off (471-541).
- tests/observe/test_view.py: 61 test functions; tests/observe/test_render.py: 135 test functions (counted by `^def test_`, parametrized cases not expanded). R3 desk tests in test_render.py begin at the "R3: the question text and the Decision Desk on screen (T60, T61, T66)" banner (test_render.py:921) and include: selected glyph and the desk follow (974), each unlinked reason shows in the desk (1007), a long question shows a visible mark (1032), desk text bounded to four lines at 80 columns (1047), "the desk gives way to its notice and the list is kept" (1077), a plan-approval ask with a 64-hex hash (1112).
- tests/observe/test_height_budget.py: parametrized over WIDTHS, HEIGHTS, question counts 3 and 20, selected 0 or None: "The questions-on screen never has more rows than the terminal" (test_height_budget.py:1-21).
- tests/observe/test_live_screen_pty.py (108 lines): the real `LiveScreen` on a pexpect pseudo-terminal using `live_child.py`; skipped on win32 or without pexpect (14-17). Tests: last row of the framed screen is the `shown x/y` footer at 24 and 40 rows (68-76); alternate screen `ESC[?1049h/l` entered and left, no mouse sequences, no blink SGR 5/6 (79-83); truecolor gets `38;2;` (86-88); 256-colour gets `38;5;` only (91-93); 16-colour gets only 16-colour SGR codes (96-100); `NO_COLOR` writes no SGR (103-107).
- tests/observe/test_keys_spike.py: "R0 key-reader spike ... the only test module in tests/observe that uses a real pty (AD-14, AD-16)" (docstring lines 1-4; note test_live_screen_pty.py also uses a pty, so that docstring sentence is older than the later file [observation]). Tests: lone ESC vs arrow (117), burst of keys in order while repainting (133), terminal attributes restored after q, SIGINT, SIGTERM, SIGHUP and an exception (153-154), SIGTSTP restore and SIGCONT re-enter cbreak (180-181), resize repaints within one second (208), non-TTY unavailable without raising (224), decoder for enter/backspace/ctrl-c/text/unknown sequences (242), Key name/char validation (262).
- Release-surface pin: tests/observe/release1_surface.py and golden_release1_surface.json, golden_release1_records.json, golden_questions_linkoff.json, test_linkoff_screen_reference.py, test_golden_contract.py exist (Glob). They were not read in this topic; their role is [UNVERIFIED] beyond their names.

### 5.3 Does anything else in the repo read the snapshot or call the observer?

Searches of the origin/master snapshot (all of src/, plugins/, scripts/, .github/, docs/ and top-level files, excluding tests/observe):
- Files that mention `superclaude observe` or the module path: src/superclaude/cli/main.py (registration), the observe package itself, README.md, docs/user-guide/cli-groups.md, docs/testing/v6.0.0/{post-release-report.md, post-release-manifest.json, audit.log, c-e2e-transcript.txt}. **No file under src/superclaude/{commands,skills,agents,core,hooks} names `superclaude observe`, `superclaude.cli.observe`, `ORCA OBSERVER` or the observer snapshot [CODE-VERIFIED by Grep returning no such hit]. No agent or command calls the observer.**
- No module outside `src/superclaude/cli/observe/` imports `superclaude.cli.observe` except main.py (Grep hits above).
- Snapshot consumers: `snapshot_path`/`state_dir`/`SNAPSHOT_NAME` are used only inside observe/commands.py and observe/export.py (Grep). The other `snapshot.json` hits in the tree belong to a different producer: `src/superclaude/skills/agent-work-report/scripts/compare.py:186` writes `<run>/snapshot.json` for the living work report; its `state_dir()` is defined in `skills/agent-work-report/scripts/common.py:59`, not the observer's. These are different files in different directories [observation: same filename, different producer and schema; whether any consumer was planned is a design question, not answered by code].
- The observer's record and snapshot are therefore produced for a human or an external reader; the only reader of the observer snapshot in the repo is tests (tests/observe/test_snapshot_schema.py, test_export.py, test_commands.py:174-200 validate it against `src/superclaude/cli/observe/snapshot.schema.json` with Draft7Validator, test_commands.py:17, 44) [CODE-VERIFIED for test_commands.py; the other two named by their file names only].

### 5.4 Documentation versus code

| Doc claim | Where | Check against code | Tag |
|---|---|---|---|
| Read-only; "no key and no option maps to an Orca call" | docs/user-guide/cli-groups.md:42; HELP commands.py:85 | No key reaches Orca (view.py:1249; test_session.py:359 names this). But `--run` becomes the `--run` argument of the worker-list call and `--questions` selects the `orchestration check` call (adapter.py:173-179, 469-512; test_commands.py:155-156, 665-670). commands.py itself builds no argv (commands.py:3-4). So "no option maps to an Orca call" holds for writes and for argv construction in commands.py but is loose for read selection | [CODE-VERIFIED] for keys; wording loose for options (listed in Gaps) |
| Seven options with the stated meanings | cli-groups.md:44-52 | All seven exist with the same names and choices (commands.py:450-496); the doc's `--snapshot FILE` default text matches commands.py:405-407 | [CODE-VERIFIED] |
| "polls Orca once every 15 seconds with at most 5 calls per read; caps are per observer process" | cli-groups.md:54 | `interval` 15.0 (commands.py:391; collector.py:28); `MAX_CALLS_PER_CYCLE = 5` (adapter.py:57); with questions 4 worker-list calls plus 1 message call (collector.py:32-34) | [CODE-VERIFIED] |
| "With --questions it never runs run-use and never binds to a Run" | cli-groups.md:54 | `run-use` and `run-create` are on the forbidden list (adapter.py:34-50); `execute` never constructs them | [CODE-VERIFIED] |
| "bursts of more than 100 rows between reads may be lost" | cli-groups.md:54; QUESTIONS_DISCLOSURE view.py:55-58 | Disclosure text exists (view.py:55-58); `window_is_full` logic in questions.py not read here | disclosure text and the 100-row window [CODE-VERIFIED] (questions.py:22, 141-142) |
| `observe` listed among "read-only supervision of Orca workers" | README.md:136 (and README.md:35 "read-only Orca supervision (`sweep`, `observe`)") | Group is registered (main.py:590-592) and is read-only apart from the exported/snapshot files on local disk | [CODE-VERIFIED] |
| `observe` has no CHANGELOG entry | CHANGELOG.md | Grep for "observ" (case-insensitive) returns only lines 170 and 365, neither about this group: 170 concerns sweep liveness classes, 365 is a pr-submit Codex note. Sections are [Unreleased] line 5, [6.1.0] line 23, [6.0.0] line 69, [5.0.0] line 318. So no entry in [Unreleased], 6.1.0 or 6.0.0 | [CODE-VERIFIED] absence |
| "No technical doc for `superclaude observe` (13 source files)" | docs/testing/v6.0.0/post-release-report.md:173 (gap row 6); coverage row line 56: user docs created, technical docs missing; sysop guide deferred by decision 6.6 (line 135, 182, row 15); CHANGELOG gap row 4 (line 171) | The package holds 14 .py files by Glob (adapter, parse, export, commands, questions, theme, fixtures/__init__, render, keys, terminal, view, __init__, collector, sanitize), 13 if the fixtures package `__init__` is not counted. Note this report is for v6.0.0; the snapshot's pyproject.toml version is 6.1.0 (pyproject.toml:7) | [CODE-VERIFIED] count (13 or 14 depending on counting); gap [STALE DOC risk: still an open gap at origin/master as far as docs/ search shows, no observer design/reference doc found under docs/ by the Grep above] |

Docs/design places that name the observer but are outside this snapshot's docs: the #409 design package (.dev/design/orca-observer-20261106/, .dev/issues/409/) read in section 6.

### Key Takeaways
- The observer is documented only as a one-section CLI listing (cli-groups.md:40-54) plus two README lines; no CHANGELOG entry; no technical doc; no sysop guide (deferred by decision 6.6 per the post-release report).
- Nothing in the repo calls the observer or reads its snapshot; the only readers are tests. The `snapshot.json` in agent-work-report is another producer.
- The interaction layer is test-pinned on three levels: pure functions (session/view/render), click and loop with fakes (commands), and real pty (keys spike and live screen).

## 6. Gate records (issue 409) and the six PRs: release stage

### 6.1 Where the cited gate records live

Read with `git -C /home/coder/workspaces/IronClaude show origin/master:<path>` (origin/master tip when read: 61ac2c2e6, "feat(reflect): grade a spec behaviour the plan lets slip as Blocking (issue 552, stage 3c) (#688)").
- `.dev/issues/409/owner-pass-record-20261112.md` exists on origin/master (blob) and does NOT exist in the checkout /home/coder/workspaces/IronClaude (ls: No such file) [CODE-VERIFIED]. The checkout's `.dev/issues/409/` holds README.md, attachment-status.json, attachments, branch-links.md, create-result.json, description.md, draft-notes.md, flags.md, issue-body.md and orca-observer-design-package.zip (first ten entries listed), i.e. the checkout is behind origin/master for this folder.
- `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` exists on origin/master (blob); 68 lines when read.
- Sibling records on origin/master: `.dev/issues/409/owner-direction-record-20261116.md`, `owner-decisions-20261111.md`, `owner-decisions-20261112.md`, `live-test-guide.md`, and the spec set under `.dev/issues/409/bmad/spec-orca-observer/` (SPEC.md, acceptance-tests.md, adapter-contract.md, owner-decisions-and-risks.md, rendering-rules.md, snapshot-export-schema.md, stack.md, unverified-register.md, write-back-future-stage.md).

### 6.2 What the records say (read in full)

**owner-pass-record-20261112.md (13 lines; headed "Written by the owner").** QUESTION-OBSERVATION passes for release 2 on these terms: the owner accepts the Q-1 result FAIL ("The observer reads only from the terminal that holds the Run"), accepted 2026-11-12; the Run is `run_93bfa00cae2b`, the coordinator's own Run, read with `--types question`, one call per cycle; the owner states awareness that message rate and identity on real traffic are unmeasured and that non-consumption by a non-owner reader is unverified; the label "bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost" stays on screen (owner-pass-record-20261112.md:5-13). Note: the record names `run_93bfa00cae2b` as the Run but the code takes the Run from `--run <runId>` for any valid id (commands.py:473-479, 183-197); nothing in code restricts it to that Run [observation: the record's "terms" are narrower than the code's behaviour].

**release-gates.md (origin/master).**
- Recorded decision 1 (staged releases, binding): R1 = worker ledger on the verified `worker-list`; Attention Ledger follows QUESTION-OBSERVATION; Decision Desk (C) sits behind QUESTION-LINK; DIRECTION-SELECTED passed 2026-11-16 on `.dev/issues/409/owner-direction-record-20261116.md` (release-gates.md:3).
- Data-gate rule (line 5): a data gate passes only on recorded, redacted samples of four kinds (success, missing, stale, contradictory), each pinned in a contract test; "Without all four the gate stays closed."
- Release table (lines 7-18): R0 fixture replay and design material (offline); DIRECTION-SELECTED (gate, not a release; passed 2026-11-16); R1 live worker-list (gate: DIRECTION-SELECTED plus golden samples of four kinds and test T32); R2 question ledger, QUESTION-OBSERVATION "passed 2026-11-12" on the owner-written record; R3 links and C's inspector, QUESTION-LINK, "Built 2026-11-17 behind QUESTION-LINK: the minimal Decision Desk (one stacked block, dispatch-level link, question text on screen only). Default B stays; the optional re-confirm was not taken"; R4 remote fleet (`--include-remote`, "Not established"); later: closure evidence ("Not established"), history ("Not established"), admission/verification/cost/deep links ("none established"); future stage write-back ("Never R1", needs a boundary change on #409 and a TUIBBS FR-X-13 amendment) (release-gates.md:9-18).
- QUESTION-OBSERVATION section (36-54): status "passed 2026-11-12"; Q-1 FAIL (consumer_fenced), Proof (a) "withdrawn as worded": `--run` is a fence, not a filter (46); non-consumption passed only on a probe Run as the Run's owner, only `--all` is used because `--peek` hides acknowledged rows (50); question identity `message.id` (51); budget one message call per cycle (53). A live test on 2026-11-17 by the owner: two hand-sent questions listed as "seen, not resolved: 2" and `check --peek --types question` still listed both afterwards (40); a synthetic load test: 181 sent, 181 retained, 0 lost in steady traffic, and in a burst test about 30 of about 415 lost, "not shown to be the only loss path" (42). This resolves the [UNVERIFIED] noted in section 4 about `check` without `--peek`: the record states `--all` is used on purpose and non-consumption was tested as the Run's owner only.
- QUESTION-LINK section (56-66): "QUESTION-LINK: passed 2026-11-17 at dispatch level, on the owner's confirmation in chat ("yes"), recorded here by the agent" (line 58). Evidence: 41 `question` messages read from the coordinator's own terminal; 39 carry a JSON payload with `dispatchId`, 39 of 39 equal to the sender's dispatch id; 18 distinct dispatches in the Run's 144 worker-list rows, 11 distinct worktrees (60); link = message -> `dispatchId` -> worker-list row -> `resource.worktreeId` (61); limit: worktree is evidence of one session, never an inferred set; a message with no `dispatchId` reads "affected scope unknown" (62); still unverified: one Run, one host, 41 messages, payload shapes (63); decided 2026-11-17 by the owner in chat ("Keep it onscreen for now"): question text stays on screen only, out of record and snapshot (64); real rate 41 questions over about 66 hours, at most 6 in one hour (66).
- Provenance difference [observation]: QUESTION-OBSERVATION's gate record is an owner-written file (the test requires a cited existing owner record, test_commands.py:758-762); QUESTION-LINK's is an agent-written status line recording a chat confirmation (release-gates.md:58), and the test for it checks only that release-gates.md contains the heading and the status text (test_commands.py:777-779). Whether the four-kinds data-gate rule (line 5) was met for the question and link gates is [UNVERIFIED] here: the four golden worker-list samples are named in tests/observe/test_golden_contract.py:22 (`golden-success`, `golden-missing`, `golden-stale`, `golden-contradictory`), but the QUESTION-LINK evidence section lists one real-traffic Run and does not state recorded stale or contradictory samples for messages.

**owner-direction-record-20261116.md (5 lines).** Owner states the fallback date is not needed; chose the order "worker list first, then questions, third screen later"; "Tool is authorized to run as a command and read the real system"; confirms the Python and name decisions (owner-direction-record-20261116.md:2-5). The Decision Desk is the "third screen"; release-gates.md:13 says it was built on 2026-11-17 behind QUESTION-LINK.

### 6.3 The six PRs (read-only `gh pr view <n> --repo IronbellyOrg/IronClaude`; merge commits checked with `git merge-base --is-ancestor <merge> origin/master`)

| PR | Title | State | mergedAt (UTC) | Merge commit | On origin/master | Content (from the file list; the tool lists only the first 100 files) |
|---|---|---|---|---|---|---|
| #503 | feat(observe): release 1 of the Orca terminal observer, superclaude observe (#409) | MERGED | 2026-11-11T19:54:57Z | 9e2608b03857 | yes | head `ironbelly/issue-409-mvp`; first 100 files are the design package `.dev/design/orca-observer-20261106/` (DESIGN-CONTRACT, PLAN, PREVIEWS, QA, README, agent-focus exports at 116 and 160 columns); source and tests were beyond the first 100 files returned |
| #514 | feat(observe): release 2, coordinator questions for one named Run (live read off) (#409) | MERGED | 2026-11-12T12:36:19Z | cd873619957b | yes | head `409-Phase2`; first 100 files are `.dev/issues/409/bmad/...` (architecture, PRD, spec, UX, final-review); body states `QUESTION_GATE_PASSED = False` at that merge, `--questions` refused with no Orca call, plan task 18 (flip guard) not done, retention bounded at 1,000 questions, 691 observer tests passed |
| #577 | feat(observe): enable the live questions read, apply the 11 cuts, record the owner's direction decision (#409) | MERGED | 2026-11-17T00:40:16Z | 44ff04aeff5c | yes | head `409-Phase3-gate-pass`; adds the owner pass record, the live-test-guide, owner decisions 20261108/20261112, the direction record 20261116, the ponytail-review cuts package (debate files), archived task packages; body: "applies the 11 debated cuts (-208 lines net, 684 observe tests pass)" and "PR #514 was already squash-merged" |
| #592 | feat(observe): question text, dispatch link and Decision Desk behind QUESTION-LINK (#409) | MERGED | 2026-11-17T14:19:18Z | 3206bdb9cb6b | yes | head `feat/409-decision-desk`; code: collector.py (+3/-1), commands.py (+20/-3), export.py (+11/-1), parse.py (+69/-3), render.py (+97/-6), view.py (+173/-7); tests: conftest, golden_questions_linkoff.json, test_collector, test_commands (+126), test_deep_nesting, test_export, test_linkoff_screen_reference, test_parse, test_render (+184), test_session (+117), test_snapshot_schema, test_view (+283); body: link guard `QUESTION_LINK_PASSED`, keys n/p/Esc, link-off screens byte-identical (reference capture), "762 observer tests pass" |
| #598 | docs(observe): record the owner's decision to keep question text on screen only (#409) | MERGED | 2026-11-17T17:28:23Z | 10f6ec670bf5 | yes | docs only: release-gates.md (+2/-1) |
| #673 | feat(observe): observer visual parity at 160, 116 and 80 columns (#606) | MERGED | 2026-11-19T19:16:52Z | b68d5eeaf618 | yes | head `ironbelly/issue-606`; first 100 files: rendering-rules.md (+23/-23), `.dev/issues/409/visual-parity/` (REDESIGN-SPEC.md 699 lines, render_current.py, render_compare.py, rubric, scores p1-p6/final), `.dev/issues/606/` records, reflect and task packages; source files beyond the first 100 listed (the observer render/view changes are not visible in this listing; they are in the origin/master code read in sections 1-4) |

All six are MERGED and their merge commits are ancestors of origin/master 61ac2c2e6 [CODE-VERIFIED via git]. For #503, #514, #673 the `files` field was truncated at 100 entries, so their full source and test contents are not stated here [UNVERIFIED beyond what is listed].

### 6.4 Release stage of the observer (facts, no recommendation)

- Code at origin/master: R0 (fixtures, `--fixture`), R1 (live worker ledger, `--once`, snapshot), R2 (coordinator questions, `--questions`, gate True) and R3 (link, Decision Desk, gate True) are all present and enabled by constants in code (commands.py:67, 70). Visual parity work (PR #673, issue 606) merged 2026-11-19.
- Not built, per release-gates.md:14-18: R4 remote fleet, closure evidence ("closed by evidence" prints `unavailable (no source)`, view.py:72), message history older than 100 rows, admission/verification/cost/deep links, write-back. These are the ledger values shown as unavailable in the screen strip (view.py:120-122, 134: `UNAVAILABLE_FACTS = ("report status", "acceptance", "tests", "approval")`, "no source: settled, frozen, cost").
- Package ships in `superclaude` 6.1.0 per pyproject.toml:7 of the snapshot; the v6.0.0 post-release report lists `superclaude observe` as part of the 6.0.0 external surface (post-release-report.md:56, 135). Whether R3 (built 2026-11-17) is part of the 6.0.0 tag (CHANGELOG [6.0.0] and [6.1.0] both dated 2026-11-18, CHANGELOG.md:23, 69) is [UNVERIFIED] in this topic: the CHANGELOG has no observer entry in either section.
- Usage constraints that bound how a person can use R2/R3 today: must run in the terminal that holds the named Run (Q-1 FAIL, accepted); `--questions` needs `--run` and a live source; question list is best effort with a 100-row read window; observer-side retention is bounded at 1,000 questions (`RETENTION_BOUND = 1000`, questions.py:21; matches the PR #514 body) and a read of exactly 100 rows marks the window full (`WINDOW_ROWS = 100`, questions.py:22; `window_is_full`, questions.py:141-142) [CODE-VERIFIED].

### Key Takeaways
- All six PRs are merged and on origin/master. R1 (#503) -> R2 built with the live read off (#514) -> live read enabled and the pass record added (#577) -> R3 Decision Desk (#592) -> docs decision on question text (#598) -> visual parity (#673).
- QUESTION-OBSERVATION has an owner-written pass record; QUESTION-LINK is an agent-written line recording a chat "yes"; the question text decision is also a chat decision recorded by an agent. The two gate records are on origin/master only.
- The pass record names one Run; the code accepts any valid `--run`.

## Gaps and Questions

1. **Snapshot cannot run two gate tests.** test_commands.py:754-763 and 769-779 read `.dev/issues/409/...`, which the snapshot export omits; they depend on origin/master carrying those records. Not verified by running (code under study was not run).
2. **Four-kinds data-gate rule for R2/R3 [UNVERIFIED].** release-gates.md:5 requires success, missing, stale and contradictory recorded samples per data gate; the four worker-list samples are named in tests/observe/test_golden_contract.py:22; for messages (questions, link) the gate text lists one Run and does not state recorded stale and contradictory samples. Whether golden_questions_linkoff.json or other fixtures cover them was not read.
3. **Option wording [CODE-CONTRADICTED, minor].** cli-groups.md:42 and HELP (commands.py:85) say "no key and no option maps to an Orca call"; `--run` and `--questions` do select which Orca read argv is built (adapter.py:173-179, 469-512), although commands.py builds no argv itself. The statement is true for keys and for writes.
4. **Pass-record scope versus code.** The owner pass record names `run_93bfa00cae2b`; code accepts any valid run id. Observation only; no scope decision in the record says other Runs are out.
5. **No consumer of the observer snapshot or record in-repo; no agent/command calls the observer** [CODE-VERIFIED by search]. Not a defect: the docs do not claim a consumer. Recorded because the owner is deciding how Clay's orchestrator design relates to these tools; the snapshot schema is `src/superclaude/cli/observe/snapshot.schema.json` (schemaVersion 1, export.py:20), read only by tests.
6. **100-row window and 1,000-question retention** are [CODE-VERIFIED] at questions.py:21-22, 141-142 (constants only; the `merge_questions` logic was not read in full). The claim that a burst over 100 rows loses questions is the gate record's measurement (release-gates.md:42), not re-tested.
7. **PR file lists truncated at 100** for #503, #514, #673; source/test contents of #503 and #514 not enumerated.
8. **tests/observe golden and release1_surface files not read** (test_golden_contract bodies, golden_*.json, release1_surface.py); their role beyond names is [UNVERIFIED].
9. **Version placement of R3.** CHANGELOG has no observer entry in [Unreleased], 6.1.0 (line 23) or 6.0.0 (line 69); which tag first contained R2 and R3 is [UNVERIFIED] here (no git tag lookup was done).
10. **Defect check (C8).** No unwired in-scope capability found for R2, R3, snapshot, `--once`; no DEFECT-CANDIDATE to report; no remediation task created (read-only brief).
11. test_keys_spike.py:3 says it is "the only test module in tests/observe that uses a real pty", but test_live_screen_pty.py also spawns a pexpect pty (test_live_screen_pty.py:34); the docstring is older than the second file. Cosmetic.

## Stale Documentation Found

- **[STALE DOC] docs/testing/v6.0.0/post-release-report.md:173 and :56** ("No technical doc for `superclaude observe`; user doc created, technical doc missing"): accurate for the 6.0.0 run it records; at origin/master 61ac2c2e6 no observer technical or reference doc was found by Grep under docs/ (only cli-groups.md and the testing artifacts), so the gap still reads as open [CODE-VERIFIED absence by search]. The "13 source files" count differs from the Glob count of 14 `.py` files (13 without `fixtures/__init__.py`).
- **[STALE DOC, wording]** tests/observe/test_keys_spike.py:3 "only test module that uses a real pty" (see Gap 11).
- cli-groups.md:40-54 and README.md:35,136 match the code for options, caps and read-only claims except the wording noted in Gap 3.
- The 6.0.0 post-release manifest, audit.log and e2e transcript mention `observe` (Grep); their cells were not read in detail.

## Summary

The observer is one click group `superclaude observe` (registered at main.py:590-592) with seven flags, a 15-second poll loop with a 14-behavior key map in view.py:apply_key, three width layouts (160, 116, 80) and an R3 Decision Desk, and exit codes 0, 1, 2 plus 129 and 143 on signals. R0 through R3 are built and enabled in code: both gate constants are True (commands.py:67, 70), the call chain from `--questions` to the Orca `orchestration check --all --types question --run <id> --json` read is wired and tested, and no unwired-capability defect was found. All six PRs (#503, #514, #577, #592, #598, #673) are merged and on origin/master; the pass records live only on origin/master, QUESTION-OBSERVATION has an owner-written record and QUESTION-LINK an agent-written line recording a chat confirmation. Nothing in the repo calls the observer or reads its snapshot except tests; documentation is a one-section CLI listing plus two README lines, with no CHANGELOG entry, technical doc or sysop guide. R4 remote fleet, closure evidence, history beyond 100 rows and write-back are not established.



see gapfill-c1-GF4-public-entry-points.md for the resolution of GF-4 (observer entry-point signatures, View/RowView field lists, panel and snapshot-field contracts).
