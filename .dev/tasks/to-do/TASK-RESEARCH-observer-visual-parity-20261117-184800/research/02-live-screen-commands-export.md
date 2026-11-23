# Research: live screen, one-shot path, export and collector
**Investigation type:** Code Tracer
**Scope:** the files listed above
**Status:** Complete
**Date:** 2026-11-17
---

All paths below are under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/` (short names: `commands.py` = `src/superclaude/cli/observe/commands.py`, same for `export.py`, `collector.py`, `questions.py`, `keys.py`, `terminal.py`, `render.py`, `view.py`, `parse.py`). Installed Rich version: **15.0.0** (`uv run python -c "import importlib.metadata as m; print(m.version('rich'))"`). Line counts of the five scoped files match the task (500, 274, 361, 142, 235) [CODE-VERIFIED].

## 1. Every code path that turns the view into terminal output (a)

| Path | Entry | Console used | Console options | Output route |
|---|---|---|---|---|
| Interactive live screen | `run_interactive` commands.py:351 -> `run_loop` :282 -> `LiveScreen.draw` :264 | `make_console(policy)` at :270 (file=None, record=False) inside `Live(screen=True, auto_refresh=False)` :269-271 | via `make_console` terminal.py:110-125: `width=policy.width, height=policy.height, highlight=False, markup=False, emoji=False, color_system=None if policy.no_color else "standard", no_color=policy.no_color, safe_box=policy.ascii, record=False`; `file` None (Rich resolves to current `sys.stdout`) | Rich writes ANSI directly to stdout; alt screen only if `console.is_terminal` |
| One-shot, width-bound (`--once --width N`) | `run_once` commands.py:225, branch :238-242 | `make_console(policy, file=io.StringIO(), record=True)` :240 | same as above plus `file=StringIO`, `record=True` | `console.print(render(view, policy))` :241, then `console.export_text()` :242 (plain), then `_emit(text, deps)` :245 -> stdout bytes encoded with `errors="replace"` :200-210 |
| One-shot, no width (`--once`) | commands.py:243-244 | none | none | `record_text(view)` (export.py:71), never touches Rich |
| `e` key export (interactive) | `Effect.EXPORT` handler commands.py:324-330 | none | none | `write_atomic(record_path(...), record_text(view))` |
| Snapshot (once and interactive) | `_write_snapshot` commands.py:213-219; called :247 and :312 | none | none | `write_atomic(target, snapshot_json(view))` |

- `force_terminal`, `legacy_windows`, `_environ` and `style` are never passed anywhere in the package: the only `Console(` construction is terminal.py:114-125 (the callers are commands.py:240 and :270) [CODE-VERIFIED]. Rich therefore auto-detects terminal-ness from `file.isatty()` (and from `TTY_COMPATIBLE` / `FORCE_COLOR` in the environment, per `Console.is_terminal` in Rich 15.0.0) and Windows legacy mode.
- `color_system` is the literal string `"standard"` (16 colours) unless `NO_COLOR` is non-empty, in which case it is `None` plus `no_color=True` (terminal.py:83 `bool(env.get("NO_COLOR"))`, :121-122).
- The width option feeds `_policy_maker` (commands.py:150-161): `options.width or columns`; it also applies to the interactive path, not only `--once`. The interactive loop calls `make_policy()` on every draw (:336), so a terminal resize is picked up on the next redraw (<= REDRAW_SECONDS = 0.5, :58).
- No other output path exists: Grep for `print(|click.echo|.write(` over the package shows only `_emit`, the `click.echo` error/refusal messages (:249, :344, :354, :362, :392) and `write_atomic` [CODE-VERIFIED].

**Key Takeaways**
- Exactly two paths use Rich: the Live screen (commands.py:269) and the recorded one-shot console (commands.py:240). Both go through the single `make_console` factory (terminal.py:110).
- The record (`record_text`) and snapshot (`snapshot_json`) never see a Console.
- `legacy_windows`, `force_terminal` and `file` (for the live console) are left at Rich defaults.

## 2. What `export_text()` does today and what styled export would need (b)

- Today's call: `console.export_text()` (commands.py:242) with defaults. Rich 15.0.0 signature (read from the installed package): `Console.export_text(self, *, clear: bool = True, styles: bool = False) -> str`. With `styles=False` it joins `segment.text` of every non-control segment in the record buffer, so **every style is dropped**; `clear=True` empties the buffer after export. It asserts `record=True`.
- With `styles=True` it joins `style.render(text)` per recorded segment (ANSI SGR codes). Important differences from what the Live path emits (verified by a probe run, `uv run python -I`, Rich 15.0.0, console built like `make_console` with `file=StringIO`, `width=40`, one `Text("hello", style="bold red")`):
  - NO_COLOR false: stream value `'\x1b[1;31mhello\x1b[0m\n'`, `export_text()` -> `'hello\n'`, `export_text(styles=True)` -> `'\x1b[1;31mhello\x1b[0m\n'`.
  - NO_COLOR true (`color_system=None`, `no_color=True`): stream value `'hello\n'` (colour removed), `export_text()` -> `'hello\n'`, but **`export_text(styles=True)` -> `'\x1b[1;31mhello\x1b[0m\n'` (colour still present)**. The record buffer stores segments before `Console._render_buffer` strips colour (`Segment.remove_color` when `self.no_color and color_system`), and `export_text(styles=True)` calls `style.render(text)` with no `color_system` argument. So `export_text(styles=True)` **bypasses NO_COLOR and the `color_system="standard"` down-conversion**. [CODE-VERIFIED by probe]
  - The probe console reported `is_terminal: False` yet the stream still held ANSI, because `_render_buffer` applies `style.render(..., color_system=...)` whenever a style exists and `color_system` is set; terminal-ness only suppresses control segments.
- Options to get styled one-shot text (none is implemented):
  1. Read `console.file.getvalue()` from the `io.StringIO` after `console.print(...)`. Already NO_COLOR-correct and standard-colour-converted (probe evidence above); needs no `record=True`.
  2. `export_text(styles=True)` only if the caller skips styles when `policy.no_color`; also no down-conversion of 256 or truecolor styles.
  3. `export_html` (params `theme, clear, code_format, inline_styles`) and `export_svg` (`title, theme, clear, code_format, font_aspect_ratio, unique_id`) exist in Rich 15.0.0 and need `record=True`; they produce markup files, not terminal text, so they do not fit stdout piping.
- **Current styling state (anomaly relevant to Q5):** `render()` (render.py:524-531) builds `Text(line, no_wrap=True, overflow="crop")` per line with **no style at all**, and a grep for `style|bold|dim|reverse` over the package finds no Rich style in the render path. So today **neither path emits any ANSI**: the live path would keep styles and the one-shot path would drop them, but nothing is styled yet [CODE-VERIFIED]. Existing tests pin this: `"\x1b" not in out` for `--once --width` (tests/observe/test_commands.py:121), for the record (:99, :105; tests/observe/test_export.py:53) (tests/observe/test_golden_contract.py:212 and :514 only check that the golden fixture JSON input files hold no escape byte; they do not test screen output).

**Key Takeaways**
- Q5 answer: yes as machinery. Live draws the `Group` directly (Rich writes styled ANSI); the one-shot path calls `export_text()` with `styles=False` (commands.py:242), which drops styles. Today nothing is styled, so both outputs are plain text.
- `export_text(styles=True)` is NOT a safe styled export: it ignores NO_COLOR and colour-system down-conversion. `console.file.getvalue()` of the StringIO console is the NO_COLOR-correct route.
- A styled-capture gate must test: (i) ANSI present in the one-shot width path when colour is on; (ii) no ANSI at all with `NO_COLOR` set; (iii) plain text unchanged vs the current golden lines; (iv) widths 160/116/80 and ASCII. The test asserting `"\x1b" not in out` on the width-bound one-shot (test_commands.py:121) would need changing; the ones on the record (test_commands.py:99, :105; test_export.py:53, :275) and the fixture-file checks (test_golden_contract.py:212, :514) must stay.

## 3. LiveScreen: drawing, refresh, alternate screen, resize, key loop (c)

- `LiveScreen` (commands.py:257-279) holds one `Live` and the last `shape = (policy.width, policy.height, policy.ascii, policy.no_color)` (:265). `draw()` renders `render(view, policy, message)` to a `Group` (:266). If there is no Live or the shape changed, it closes the old one and creates `Live(group, console=make_console(policy), screen=True, auto_refresh=False)` and `start()` (:267-273), then always `update(group, refresh=True)` (:274). `close()` stops the Live (:276-279).
- Alternate screen: `screen=True`. In Rich 15.0.0 `Live.start` calls `console.set_alt_screen(True)` and `console.show_cursor(False)` (Live.start source, read from the installed package); `Console.set_alt_screen` only writes the control code `if self.is_terminal and not self.legacy_windows`. So with stdout not a tty, no alt screen is entered. No mouse or blink sequences are emitted anywhere in the package (grep for `mouse|blink` in `src/superclaude/cli/observe/*.py` is not needed here: the only terminal control calls are the Live's own, and `keys.py` sets only cbreak) [CODE-VERIFIED for keys.py:60-61; the Live control codes are Rich's].
- Refresh: `auto_refresh=False`, so Rich starts no refresh thread; the loop drives every repaint. `run_loop` redraws when `dirty` (new cycle, key, SIGCONT redraw flag) or every `REDRAW_SECONDS = 0.5` (commands.py:335-337), because ages and STALE change with time. Key reads use `READ_TIMEOUT = 0.1` (:57, :317); `KeySource.read` caps a wait at `MAX_TIMEOUT = 0.25` (keys.py:22, :146).
- Resize: no SIGWINCH handler (keys.py `_HANDLED` is INT, TERM, HUP, TSTP, CONT only, :27-33). Resize is noticed by polling: `make_policy()` calls `detect_size()` (`shutil.get_terminal_size`, terminal.py:104-107) each draw; a changed width, height, ascii or no_color value rebuilds the Live. The Console width and height are explicit (terminal.py:116-117), so Rich never re-queries the size itself.
- Styles survive in Live: Live renders through the console's normal pipeline (`_render_buffer` keeps `style.render(...)` with `color_system="standard"`, or strips colour when `no_color`). Whatever `Text` styles `render()` gave would reach the terminal. Today there are none (section 2).
- Failure and exit: any exception in the loop closes the screen and prints `observe: display failed: ...` to stderr, exit 1 (commands.py:340-345); `finally` always stops the collector and closes the screen (:346-348). `q`, Ctrl-C key, or KeyboardInterrupt end the loop (:322-323, :338-339).
- `_on_tstp` stops the process with SIGSTOP after restoring the tty; `_on_cont` re-enters cbreak and sets the redraw flag (keys.py:127-136), consumed at commands.py:332-333.

**Key Takeaways**
- Live repaints are fully driven by `run_loop`; the screen is an alternate screen only on a real terminal.
- Resize handling is by polling `detect_size()`; a policy-shape change rebuilds the `Live`, so any styled change must keep `shape` covering every policy field that affects style (today `no_color` and `ascii` are in it).
- The Live path keeps styles by design; nothing currently styles. Section 9 (addendum) measures the live bytes: alternate-screen codes, width-padded rows, and a silent bottom crop at `policy.height` that drops the footer.

## 4. Gate constants and the pinned-regex tests (d)

- `QUESTION_GATE_PASSED = True` (commands.py:67), comment `owner record: .dev/issues/409/owner-pass-record-20261112.md`; `QUESTION_LINK_PASSED = True` (commands.py:70), comment `gate record: .dev/issues/409/bmad/spec-orca-observer/release-gates.md QUESTION-LINK`. Both lines end with `# fmt: skip` so the formatter keeps them on one line for the regex tests.
- Use: `_questions_on(options)` = `options.questions and QUESTION_GATE_PASSED` (:173-175); `_link_on` = `_questions_on and QUESTION_LINK_PASSED` (:178-180); `_question_refusal` returns exit 1 with `QUESTION_GATE_TEXT` when the gate is False, exit 2 for fixture or missing/invalid run (:183-197). `execute()` runs the refusal before any Orca call (:390-393).
- Other constants: `READ_TIMEOUT` 0.1, `REDRAW_SECONDS` 0.5, `WIDTHS = ("160","116","80")` (:57-61), `POSIX_ONLY_TEXT`, `NO_TERMINAL_TEXT`, `QUESTIONS_NEED_RUN_TEXT`, `QUESTIONS_NEED_LIVE_TEXT`; collector `INTERVAL` 15.0, `CYCLE_BUDGET` 15.0, `MAX_BACKOFF` 60.0, `JOIN_TIMEOUT` 5.0, `QUESTION_PAGE_CAP` 4 (collector.py:28-34); questions `RETENTION_BOUND` 1000, `WINDOW_ROWS` 100 (questions.py:21-22); parse `PAYLOAD_CAP` 64 KiB and `ASK_CAP` 400 (parse.py:474-475).
- Pinned-regex tests: `tests/observe/test_commands.py:747-756` reads commands.py as text, `re.findall(r"^QUESTION_GATE_PASSED = (True|False)(.*)$", text, re.M)` must find exactly one match equal to the live value; when True the comment must match `owner record: (\S+)` and that file must exist (:752-755); it also asserts the text contains `release-gates.md` and `Task 18` (:756). `:762-772` does the same for `^QUESTION_LINK_PASSED = (True|False)(.*)$`: it requires `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` to contain `## QUESTION-LINK` and `QUESTION-LINK: passed`, and the comment to contain both `release-gates.md` and `QUESTION-LINK`. Other tests monkeypatch the constants (test_commands.py:627, :646, :656, :681, :698, :875; tests/observe/test_registration.py:43).
- Consequence: a styled change must keep both gate lines byte-identical in shape (one assignment each, starting at column 0, comments kept), and must not move the words `release-gates.md` and `Task 18` out of commands.py.

**Key Takeaways**
- Both gates are True and are pinned by regex over the source text of commands.py; editing those two lines or removing `Task 18` from the file breaks tests.
- `_link_on` is the only switch that lets question text and the dispatch link reach the view.

## 5. export.py: the record, the snapshot, and proof that question text is never written (e)

- Imports are `json, os, tempfile, pathlib, typing`, `sanitize`, and view types (export.py:11-18): no Rich import, so the exporters cannot use a Console. Module docstring says the same (:1-6) [CODE-VERIFIED].
- `record_text(view)` (:71-86): header1, header2, counts tokens, a filter line, gap notice, ledger title, `ledger_empty`, one `_row_line` per `view.all_rows` (:53-68, ` | `-joined `name=value`, sanitized), then `_question_lines(view)` (:85), each line sanitized (:86). Every line is `sanitize(line, "line")`.
- `_question_lines` (:89-118): title, run line, summary only when not `replaces_gap`, state lines, disclosure, counts, caveat, then for each `q in panel.lines`: `f"{q.qid} | {q.text}"` plus, when `q.link` is non-empty, `f" | dispatchId={q.dispatch_id or 'unknown'} | link={q.link}"` (:103-111). That is the ` | dispatchId=<id> | link=<state>` suffix [CODE-VERIFIED]. Then empty/window-full text, notes, retention line.
- `q.text` is built in view.py:744 as `"  ".join(lead + [text_of(q.subject), QUESTIONS_REASON])`: age, optional bracketed state, the **subject**, and `reason unknown`. The payload question text goes only to `screen_text` (view.py:748), `ask` (:749) and `shown` (:757) [CODE-VERIFIED]. The comment at view.py:738 states the same.
- Proof by reading every write path that question text cannot be written:
  1. Writers to disk: `write_atomic` is called only at commands.py:216 (`snapshot_json(view)`) and commands.py:327 (`record_text(view)`); a grep of the package for `write_atomic|write_text|open(|.write(` shows no other file write (export.py:257-274 defines it; commands.py:202-209 write to stdout only).
  2. `record_text` reads `q.qid`, `q.text`, `q.dispatch_id`, `q.link` and panel fields only. A grep for `.ask`, `screen_text`, `.shown` over the package finds uses only in view.py (:215, :739, :748, :870) and render.py (:321, :339-340) and in parse/question building, never in export.py [CODE-VERIFIED].
  3. `_questions_dict` (snapshot, export.py:158-180) writes `runId, state, observedOpen, windowFull, retained, evicted, closureEvidence, items[id, createdAt, ageSeconds, inWindow]` and optional `code`; no text, subject, link or dispatch id (docstring: "ids, times and counts only").
  4. `snapshot_dict` (:183-216) takes rows through `_row_dict` with a fixed field list (`_TEXT_FIELDS`, :25-45) that holds no question data.
  5. Tests pin it: tests/observe/test_export.py:307-332 (`ASK` text and `DQ-4711` absent from the record, suffix regex `msg_\w+ \| .* \| dispatchId=w-001 \| link=linked`, `dispatchId=unknown | link=no payload` for a bare one), test_commands.py:815-829 and :832-841.
- **Anomaly to flag (not a violation of the stated constraint):** the one-shot width path `--once --width N` prints the **screen** text to stdout, and the screen contains the question text (test_commands.py:832-841 asserts `"Which branch do we ship?" in out`). Stdout of that path is neither the record nor the snapshot, so the "screen-only" constraint holds, but a piped/redirected `--once --width` output does carry the text. Any styled-output change keeps it that way; it must not be used to feed a file writer.
- The snapshot contract: `SCHEMA_VERSION = 1`, `json.dumps(indent=2, sort_keys=True, default=_unknown_in_json)` (export.py:20, :219-224); pinned by tests/observe/test_snapshot_schema.py and test_export.py:149 (same JSON whatever the session).
- File mechanics: `state_dir()` is `$XDG_STATE_HOME/superclaude/observe` when absolute, else `~/.local/state/superclaude/observe` (:236-244); record name `observe-<generated_at with ':' -> '-'>.txt` (:247-250); snapshot `snapshot.json` (:253-254); `write_atomic` makes the directory 0700, writes via `mkstemp` + fsync + `os.replace` (:257-274).

**Key Takeaways**
- No code path writes `ask`, `shown`, `screen_text` or any payload text to a file; the record uses the subject-based `q.text`, the snapshot carries no question text at all.
- The record and snapshot are built from `View` data and never from Rich output, so a Rich styling change cannot alter them unless `view.py` field values change.
- The only place question text leaves the process is the screen (live or `--once --width` stdout).

## 6. collector.py: how `questions=` and `link=` reach the data the view reads (f)

- `Collector.__init__` (collector.py:135-174): `self._questions = bool(questions and run_id)` (one named Run only, :152); `self._link = bool(link and self._questions)` (:153). The initial `CycleResult` carries `question_state="NOT_POLLED" if self._questions else "OFF"`, `question_run`, `question_retention_wall` (:171-173).
- Callers: `run_once` (commands.py:228-234) and `run_interactive` (:364-371) pass `questions=_questions_on(options)` and `link=_link_on(options)`; tests pin both paths (test_commands.py:796-881).
- Each cycle: `run_once()` (collector.py:248) reads worker pages with `max_calls=QUESTION_PAGE_CAP` (4) when questions are on (:273-276), then `_question_fields` (:205-245) makes one `read_questions` call in the same cycle budget (:214), returns `question_state="FAILED"`/`question_code` on overrun, failure or shape error and otherwise parses with `parse_questions(reply.pages[0], namespace, number, self._run_id, link=self._link)` (:219-221). `FixtureSource.read_questions` always fails with `no-question-fixture` (:125-129); `--questions` with `--fixture` is refused earlier (commands.py:187-188).
- `parse_questions` (parse.py:512-607): with `link` true, `_read_payload(raw.get("payload"), raw.get("from_handle"))` returns `(ask, dispatch_id, link_state)` (parse.py:479-509, :581-587) and the results go into the `Question` as `ask`, `dispatch_id`, `link`. States: `linked`, `no payload`, `payload not readable`, `payload has no dispatchId`, `sender mismatch` (parse.py:468-472). `ask` is `sanitize(question, "line").strip()` cut to `ASK_CAP` 400 with `...` (:499-503). Linked requires `from_handle == f"dispatch:{dispatchId}"` (:507). Without `link`, nothing from the payload is read (docstring :525-527).
- Retention: `merge_questions(previous.questions, parsed.rows, number, window_is_full(parsed.raw_count), True, run_id)` (collector.py:230-237) keeps records by (Run, message id), marks absent ones `in_window=False`, bounds at 1,000 and never closes (questions.py:81-137). A failed read carries all question fields from the previous cycle unchanged (`_carry`, collector.py:192-203).
- The view reads `result.questions` records and `q.ask`, `q.dispatch_id`, `q.link` in `_questions_panel` (view.py:723-759) and builds the `QuestionLine`s; `_desk` (view.py:814-874) builds the Decision Desk from the selected line.
- Decision Desk join: exact `raw.dispatch_id == line.dispatch_id` across `all_rows` (view.py:838-842); fields are `dispatchId, workerState, dispatchStatus, terminalState, outcome, nextAction.kind, liveness, evidence age, resource.worktreeId` (:843-853); unlinked states yield notes `DESK_UNKNOWN_SCOPE` and the link state (:865-866); an evicted selected question yields `DESK_EVICTED` (:833-835); the desk is None unless `panel.link_on` and a question is selected (:830-831). `ask` shows `DESK_NO_TEXT` ("question text not given", view.py:95) when empty (:870).

**Key Takeaways**
- Flow: `Options.questions` -> gate + run id -> `Collector(questions, link)` -> `parse_questions(link=...)` -> `QuestionState` -> `_questions_panel` -> `QuestionLine` -> `_desk` / render.
- The link and the text exist in the data only when both gates are True and `--questions --run` are given; with the link off, `ask`, `dispatch_id`, `link` are empty and the record and screen are the Release 2 form.

## 7. keys.py and key effects (g)

- `KeySource` decodes only: `enter`, `backspace`, `ctrl_c`, `up`, `down` (CSI or SS3 A/B), `escape`, and `text` for printable characters (keys.py:176-235). It never decodes mouse reports (an ESC `[` `M`/`<` sequence is consumed as a CSI sequence whose final byte is not A or B and returns None, :222-228) and enables no mouse mode (only `tty.setcbreak`, :61) [CODE-VERIFIED].
- `apply_key` (view.py:1150-1204) is the whole key map: ctrl_c quits; focus `filter` routes text, backspace, enter/escape (:1140-1147); `up`/`k` and `down`/`j` move the worker selection (:1161-1164, `_move` :1099-1113); `d`/`u` scroll the inspector (focus inspector only, :1165-1169); `q` quit, `e` export (:1170-1173); `m` re-baseline (:1174-1184); `escape` in the inspector goes back (:1185-1186); with focus not inspector and a linked questions panel with lines, `n`/`p` select next/previous question (oldest first, stopping at the ends, `_move_question` :1116-1128) and `escape` clears the question selection (:1188-1195); `enter` opens the inspector for a selected worker (:1196-1197); `/` starts the filter (:1198-1199); `h` toggles historical rows (:1200-1203).
- What changes the display: `selected_question` (set by n/p, cleared by escape; evicted selection stays) produces the Decision Desk and the selection marker (`selected` glyph `▸`/`@` in render.py:317); `selected` / `focus` produce the inspector; `filter_text` and `show_historical` change the visible rows only (record and snapshot use `view.all_rows`). `inspector_scroll` resets on selection moves. No key reaches Orca; `Effect` is NONE, EXPORT or QUIT (view.py:1066-1071).
- Help text strings that list keys: view.py:79 and :105 (`KEYS_LINE`). Not re-verified line by line beyond the grep hits.

**Key Takeaways**
- The only keys that affect the Decision Desk and question focus are `n`, `p`, `escape` (list focus); worker focus uses `up/down/j/k`, `enter`, `escape`, `d/u`.
- Key handling is independent of rendering and styling.

## 8. Places a styled change would touch, and places that must stay byte-identical (h)

Would have to change (to make styles reach each output):
1. `render.py:524-531` `render()`: today one unstyled `Text(line, ...)` per `screen_lines` line; styles (and any per-token segmentation) would be added here or by changing `screen_lines`/`_row_line` to return styled `Text` (plain-line helpers feed `cell_len`-based width logic in render.py:62-92, :311-326, so the plain width maths must stay on plain strings).
2. `commands.py:240-242` one-shot width path: replace `export_text()` (plain) with a styled route (preferably `console.file.getvalue()`), decided together with a NO_COLOR rule, and keep `--once --width` plain when colour is off.
3. `commands.py:257-279` `LiveScreen`: nothing to change for styles to flow; keep `shape` including `no_color` and `ascii`.
4. `terminal.py:110-125` `make_console`: the single place for `color_system` / `no_color` / `force_terminal` choices; the gate must test NO_COLOR here.
5. Tests: `tests/observe/test_commands.py:121` (`"\x1b" not in out` on `--once --width`), the width tests at :113-128, and any golden screen tests would need updating; add a styled-capture test via `console_factory` (tests/observe/conftest.py:222-229) and the NO_COLOR variant.

Must stay byte-identical:
- `record_text` output and `_question_lines` (export.py:71-118), including the ` | dispatchId=<id> | link=<state>` suffix and the absence of question text.
- `snapshot_json` / `snapshot_dict` / `_questions_dict` (export.py:158-224), `SCHEMA_VERSION = 1`.
- `--once` without `--width` (commands.py:243-244), which prints `record_text` with no escape byte (test_commands.py:99, :105).
- The two gate lines and their comments (commands.py:67, :70) and the words `release-gates.md` and `Task 18` in commands.py.
- `view.py` field construction of `QuestionLine.text` (subject-based, view.py:744) versus `screen_text`/`shown`/`ask` (screen-only).

**Key Takeaways**
- The change surface is small: `render()`, the one-shot export call, and `make_console`'s colour policy, plus the tests that pin ANSI-free screen output.
- All safety-relevant contracts (record, snapshot, question text screen-only) live in `export.py` and `view.py` and are independent of Rich.

## Gaps and Questions

- [UNVERIFIED] I did not read `FINDINGS.md`, `rendering-rules.md` or the research notes named in the protocol, so no claim here is doc-sourced; the only doc-like inputs (line references `~242` and `~257` from the task text) were checked: export_text is at commands.py:242 and `LiveScreen` starts at commands.py:257 [CODE-VERIFIED].
- Mouse and blink: a case-insensitive grep for `mouse|blink` and the mouse-mode and blink escape sequences over `src/superclaude/cli/observe/*.py` returned no match [CODE-VERIFIED]; keys.py enables only cbreak, and Rich's `Live` writes only alt-screen and cursor-hide control codes (read from Live.start). A future styled change must not add a blink SGR (Rich style `blink`) to stay inside the no-blinking constraint.
- [UNVERIFIED] The line numbers in view.py for help strings (79, 105) came from a grep and were not read in context.
- Open design question: `export_text(styles=True)` ignores NO_COLOR; the chosen styled route (StringIO `getvalue()` vs `styles=True` with a NO_COLOR guard) is a decision for the design step.
- Open question: whether a piped `--once --width` output may carry ANSI by default or only when stdout is a tty (the console uses `file=StringIO`, so Rich cannot see the real stdout; today there is no tty check at all, commands.py:238-245).
- Open question: Windows (`legacy_windows`) is left to Rich; `run_interactive` refuses win32 (commands.py:353-355), but `--once --width` is cross-platform and `_emit` encodes with `errors="replace"`.
- Not covered: `render.py` row/column styling points (only `render()` and the question/desk helpers were read); `view.py` was read only around questions, desk and keys.

## Stale Documentation Found

- None found in the files read. Comments checked against code: commands.py HELP text lines 90-98 (question text shown on screen, not in record or snapshot) matches view.py:738-757 and export.py:101-111 [CODE-VERIFIED]; questions.py module docstring (1,000 bound, nothing closed) matches questions.py:21 and :125-137 [CODE-VERIFIED]; the `--width` option help ("with --once prints the screen text instead of the record", commands.py:435) matches :238-245 [CODE-VERIFIED]. The `commands.py:63-66` comment says the gate was flipped by "plan Task 18" and cites a record file; the file's existence is checked by test_commands.py:752-755 and I did not open it [UNVERIFIED].

## Summary

The live screen and the one-shot width path both use `make_console` (terminal.py:110) and `render()`, but render emits only unstyled `Text`, so no output carries ANSI today; Live would carry styles, while `export_text()` (commands.py:242) drops them, and the safe styled one-shot route is the StringIO `getvalue()` because `export_text(styles=True)` ignores NO_COLOR (probe-verified on Rich 15.0.0). The record and JSON snapshot are built in export.py from `View` data with no Rich involvement; the record uses the subject-based `QuestionLine.text` plus ` | dispatchId=<id> | link=<state>`, and no write path touches the payload question text, which exists only on screen (including the stdout of `--once --width`). Both gate constants are True and pinned by regexes in tests/observe/test_commands.py:747-772. A styled change touches `render()`, the one-shot export call and `make_console`'s colour policy, and must leave export.py, the gate lines and the no-width `--once` path byte-identical.

## 9. Addendum (Phase 3 gate fix, finding 2): the live screen path from `view` to terminal bytes

Added after the Phase 3 gate found that sections 2 and 3 described the live path from reading only. Every claim below was re-read in code and re-measured with read-only probes (`uv run python -I`, Rich 15.0.0 at `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.venv/lib/python3.10/site-packages/rich/`); nothing was started against Orca and no observer code was changed. Tags: [CODE-VERIFIED] = read in code and reproduced by a probe; [UNVERIFIED] = not measured here.

### 9.1 The trace, hop by hop

| Hop | Code | What it does |
|---|---|---|
| 1 | `LiveScreen.draw` `commands.py:264-274` | `group = render(view, policy, message)` (:266); on first draw or a changed `shape` it builds `Live(group, console=make_console(policy), screen=True, auto_refresh=False)` (:269-271), `start()` (:272), then every draw calls `update(group, refresh=True)` (:274) [CODE-VERIFIED] |
| 2 | `render` `render.py:524-531` | One `Text(line, no_wrap=True, overflow="crop")` per `screen_lines` line inside a `Group`; no style, no wrap, no height clamp [CODE-VERIFIED] |
| 3 | `make_console` `terminal.py:110-125` | `Console(file=None, width=policy.width, height=policy.height, color_system=None if no_color else "standard", ...)`; no `force_terminal`, so Rich decides `is_terminal` from the real stdout [CODE-VERIFIED] |
| 4 | `Live.start` `rich/live.py:127-128` | `if self._screen: self._alt_screen = self.console.set_alt_screen(True)`, then `show_cursor(False)`; `Console.set_alt_screen` (`rich/console.py:1201-1217`) writes the control code only `if self.is_terminal and not self.legacy_windows` [CODE-VERIFIED] |
| 5 | `Live.renderable` `rich/live.py:228` | `return Screen(renderable) if self._alt_screen else renderable`: on the alternate screen the whole group is wrapped in `rich.screen.Screen` [CODE-VERIFIED] |
| 6 | `Screen.__rich_console__` `rich/screen.py:40-54` | `render_lines(..., pad=True)` then `Segment.set_shape(lines, width, height)`: every line is padded with spaces to the console width and the line list is cut to exactly the console height; lines are joined with `Segment.line()` and the last line gets no newline [CODE-VERIFIED] |
| 7 | `Live.process_renderables` `rich/live.py:279-296` | When `console.is_interactive`, prefixes `Control.home()` (cursor to top-left) on an alternate screen, then the renderable; `vertical_overflow` defaults to `"ellipsis"` (`rich/live.py:68`) and `stop()` resets it to `"visible"` (`:161`) [CODE-VERIFIED] |

### 9.2 Measured bytes

All four measurements fed the same shape of group the observer feeds (`Group` of `Text(no_wrap=True, overflow="crop")`), at the console arguments `make_console` uses (width and height explicit, `"standard"` colour, no highlight, no markup, no emoji).

1. Five-line group (line 1 `bold red`), console 10 wide, 3 high, `force_terminal=True`, `StringIO` file. Bytes: `'\x1b[?1049h\x1b[H\x1b[?25l\x1b[H\x1b[1;31mL1\x1b[0m        \nL2        \nL3        \x1b[?25h\x1b[?1049l'`. So: enter alternate screen `ESC[?1049h`, home `ESC[H`, hide cursor `ESC[?25l`, home again, then only the first 3 lines, each padded with spaces to 10 cells, then show cursor `ESC[?25h` and leave the alternate screen `ESC[?1049l` on `stop()`. Lines 4 and 5 are absent and there is no ellipsis row [CODE-VERIFIED]. The style survives as an SGR (`ESC[1;31m ... ESC[0m`) and the padding spaces carry no style.
2. The same group at height 5 (it fits): all five lines, each padded to 10 cells, same control codes [CODE-VERIFIED].
3. The real observer screen: `LINES=40 uv run superclaude observe --once --width 80 --fixture base` (read-only fixture run) gave 40 lines; those 40 lines fed to a `Live(screen=True)` console 80 wide: at height 40 all 40 rows are written (last row `shown 28/54 | collected 80 / reported 80`, the counts line); at height 38 only 38 rows are written and the last two source lines are gone: the key list `Up/Down j/k move  Enter detail  Esc back` and the `shown 28/54 | collected 80 / reported 80` line. `vertical_overflow` read `ellipsis` before `stop()` and no ellipsis appears: `Screen` has already cut the lines to the console height before `Live`'s own ellipsis step can run [CODE-VERIFIED]. This used the fixture's lines in a stand-in console, not the real `LiveScreen`.
4. `make_console`-shaped console with no `force_terminal` and a `StringIO` file (what the one-shot path and every test console is): `is_terminal` is False, `Live(screen=True)` wrote nothing at all (`''`) [CODE-VERIFIED]. The same group through plain `Console.print` at height 3 printed all 5 lines (`export_text` showed 5 newlines): `print` never crops to `height`, only `Screen` does [CODE-VERIFIED].

### 9.3 Capture routes for live styled bytes, and their limits

| Route | Measured | Gives | Limits |
|---|---|---|---|
| A. `Console(<make_console arguments>, force_terminal=True, file=StringIO())` plus `Live(screen=True)`, as in measurements 1 to 3 | yes | The exact alt-screen codes, padding, crop and SGR bytes, with `\n` line ends | `make_console` has no `force_terminal` parameter and `LiveScreen.draw` calls `make_console(policy)` directly (`commands.py:270`), so the real `LiveScreen` cannot be pointed at it without a test seam (a parameter, an injected factory or a monkeypatch of `make_console`); a harness that builds its own `Console` tests the stand-in, not `LiveScreen` [CODE-VERIFIED] |
| B. Run a child process under a pty with `pexpect` (4.9.0 installed) and read the bytes | yes, with a stand-in child (`Console(width=10, height=3, color_system="standard")` plus `Live(screen=True)`, no `force_terminal`): `'\x1b[?1049h\x1b[H\x1b[?25l\x1b[H\x1b[1;31mL1\x1b[0m        \r\nL2        \r\nL3        \x1b[?25h\x1b[?1049l'` and `is_terminal True` | The same bytes as route A but from Rich's own terminal detection, so it exercises `make_console` as shipped; the pty turns `\n` into `\r\n` | The real `observe` interactive command was not started here (it needs Orca data or a fixture flag for the interactive mode: [UNVERIFIED] whether `run_interactive` accepts `--fixture`); `tests/observe/spike_child.py:64` already runs a raw `Live(screen=True)` on a pty for the key-reader spike, so the pattern exists in the repo [CODE-VERIFIED]; a pty size must be set to match `policy.width` and `policy.height` |
| C. One-shot `getvalue()` or `export_text` | not the live path | Styled body bytes only | No alt-screen codes, no padding, no crop at height: it cannot show the bottom crop or the footer loss |

No test in `tests/observe/` references `LiveScreen` or `run_interactive` (grep over `tests/observe` for `LiveScreen|run_interactive` found none; the `Live(` match is `spike_child.py:64` only) [CODE-VERIFIED]. So the live path has no styled-capture test today, and the issue 606 requirement that styled output is verified on the live screen path needs route A with a seam or route B.

### 9.4 Consequences for Q5, the height budget and the footer

- Styles do reach the live terminal unchanged: `Text` styles on `render()` lines come out as SGR in the alternate-screen stream (measurement 1). Section 3's statement that "Whatever `Text` styles `render()` gave would reach the terminal" is now measured, not inferred.
- Height is a hard cut from the bottom, silently. `screen_lines` already budgets the ledger against `policy.height`: `reserved = len(top) + len(body) + footer_height + 1` and `capacity = max(policy.height - reserved, 1)` (`render.py:499-502`), so the ledger window shrinks to absorb extra rows in `top` or `body`. The danger is any row not counted in `reserved`: a frame border or heading added in `render()` after `screen_lines`, or rows that push `top + body + footer` past `policy.height` (the `max(..., 1)` forces one ledger row, so very small heights and the inspector body (`render.py:491`, `max(..., 1)`) can overflow). On the live screen the lost rows are the last ones, which are the footer key list and the `shown x/y | collected` line (measurement 3). `--once --width` and every plain `screen_lines` test print or compare all lines (measurement 4), so they cannot see this.
- A frame-heavy redesign therefore must (1) count every new row inside `screen_lines`' `top`, `body` and `footer_height`, (2) assert in a test that `len(screen_lines(...)) <= policy.height` at 24, 40 and 44 rows and at `MIN_ROWS = 8` (`terminal.py:22`), and (3) treat each added frame row as one fewer ledger row (the base fixture at 80 wide and height 40 already fills all 40 rows, so there is no spare row). Heights below 40 were not measured against a frame design here [UNVERIFIED].
- Width is safe on the live path: `no_wrap=True, overflow="crop"` plus `Screen` padding mean a line longer than `policy.width` is cut, never wrapped into an extra row (`render.py:528`; `rich/screen.py:46-49`). A styled design must still keep each line within `policy.width` cells so the cut never removes a border.

**Key Takeaways**
- The live path is `LiveScreen.draw` -> `render` -> `Live(screen=True)` -> `Screen` crop and pad -> stdout; the bytes are alt-screen codes, home, hide-cursor, width-padded styled rows, show-cursor, leave-alt-screen.
- Overflow past `policy.height` drops the footer silently with no ellipsis, and nothing in the plain or one-shot tests can see it.
- Live styled capture needs a pty (`pexpect`) or a `force_terminal` console with a seam into `LiveScreen`; a `make_console` `StringIO` console writes nothing for `Live(screen=True)`.

