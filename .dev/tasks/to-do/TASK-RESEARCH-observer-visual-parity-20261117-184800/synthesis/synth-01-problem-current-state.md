# Synthesis 01: Problem Statement and Current State Analysis

Feeds report Sections 1 and 2. Sources: research files 01 to 05 and `gaps-and-questions.md` (all under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/`). Paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/` unless absolute. `OBS` = `src/superclaude/cli/observe/`. `RR` = `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`. `FIND` = `.dev/issues/409/visual-parity/merged/FINDINGS.md`.

## 1. Problem Statement

### 1.1 The question

How should the read-only Orca terminal observer (`superclaude observe`) presentation be redesigned to reach theme, styling and layout parity with its design mockups (nine mockups: three screens x widths 160/116/80; `.dev/issues/409/visual-parity/inputs/mockups/{160,116,80}/`)? The redesign is phased, with a render gate per phase, and this report feeds that phasing (issue #606).

### 1.2 Why it matters

| Fact | Evidence | Source |
|---|---|---|
| The current screen carries no style at all: one unstyled `Text(line, no_wrap=True, overflow="crop")` per line | OBS/render.py:528 [CODE-VERIFIED] | 01 section 3 |
| The nine captured current-state ANSI exports contain 0 ESC bytes; the mockup `.ansi` files use 8 truecolor foreground roles plus bold | `grep` count 0 vs 48 ESC lines in `mockups/160/signal-bridge.ansi` [CODE-VERIFIED] | 04 section 2, 05 section 4 |
| Every screen differs from its mockup in chrome (panes, colour, badge, tiles), not in data meaning | 04 section 6 | 04 |
| Passing the existing 766 tests does not prove the screen looks right: no test covers the real `Live(screen=True)` path | `LiveScreen` referenced by no test [CODE-VERIFIED] | 02 section 9.3, 03 section 2 |

### 1.3 The trigger: merged findings, guards, divergences, open items, owner decision

Source of the list: `FIND`; each item was re-checked against code and `RR` by research file 04 (section 5). Severity as stated in FIND.

**Merged findings M-01 to M-18**

| ID | Finding (short) | Sev |
|---|---|---|
| M-01 | No colour or weight anywhere | High |
| M-02 | No boxed titled panes | High |
| M-03 | Questions screen has no two columns (conflicts with O-1) | High |
| M-04 | Decision Desk is stacked, not two-column (conflicts with O-1) | High |
| M-05 | Open-question count has no visual weight (no count tile) | High |
| M-06 | Ledger lacks attention slot, observation pane and tiles | Med |
| M-07 | Caveats outweigh question rows; no row emphasis or separation | Med (OPEN-1) |
| M-08 | Absent values (`unknown`, `unavailable (no source)`) are not muted (RR 70 already requires it) | Med (defect) |
| M-09 | State values uncoloured (`nextAction.kind` stays uncoloured per RR 31) | Med |
| M-10 | No column heading at 116 and 80 | Med (defect) |
| M-11 | 80-column key list cut at `e exp>`; `q quit` lost | Med (defect) |
| M-12 | Desk: question does not lead; evidence is an unaligned dump | Med |
| M-13 | No `READ ONLY` badge / title split | Med (OPEN-3) |
| M-14 | Supported facts scattered over three places; no RETAIN CONTEXT pane | Med (OPEN-2) |
| M-15 | Footer key pair split (`n/p` / `question`); no rule | Low |
| M-16 | 80-column counts cut inside a token (`runs seen>`, `cost un>`) | Low |
| M-17 | Wide blank band after the id at 116 and 80 | Low |
| M-18 | Selected question marked by a glyph only | Low |

**Guards, accepted divergences, open items, owner decision**

| ID | Content | Status |
|---|---|---|
| G-1 | New panes must emit `+ - \|` under `--ascii`, never `?` borders (RR 25) | Guard, keep |
| G-2 | Theme must stay distinct at the real colour depth; NO_COLOR stays `color_system=None` | Guard, keep; depth and detection are an open design item (spec silent) |
| AD-1 | "8 owners / 80 sessions / 80 mapped trees" header not built (RR 20) | Accepted |
| AD-2 | SIGNALS bars and SETTLED/UNKNOWN/STALE tiles not built (RR 20, 93) | Accepted |
| AD-3 | Two-line register rows and prose lifecycle not built (RR 30, 31) | Accepted |
| AD-4 | Requester, owner, `Affected:` and scope count not shown (RR 57, 91) | Accepted |
| AD-5 | Different key map; no `tab pane`; ledger stays under the desk (RR 13, 21, 39) | Accepted |
| AD-6 | No `workerState` column at 80, optional at 116 (RR 33) | Accepted |
| AD-7 | 80-column "Questions stay until explicit resolution." and forced focused card not adopted (RR 42, 61) | Accepted; RR 61 itself lists that sentence as an invariant line (spec self-contradiction, see 2.4) |
| OPEN-1 | M-07 severity (Astra High, Opus Medium) | Open; handled as Medium (gated) |
| OPEN-2 | M-14 severity and whether RETAIN CONTEXT is built (Opus Medium, Astra Low) | Open; handled as Medium (gated) |
| OPEN-3 | M-13 severity and scope (title bar) | Open; handled as Medium (gated) |
| O-1 | Owner decision: adopt two-column layouts at 160 and 116, reversing "one stacked block" (RR 43, 57) | Pending; recommendation in FIND is yes, 80 stays stacked, spec updated in the same change |

### 1.4 The seven research questions

| Q | Question |
|---|---|
| Q1 | Safest composition of styled spans, titled boxed panes, a count tile and two columns inside the line-based pipeline (Rich Text, Table, Panel, Layout or Columns vs hand-built lines), keeping records, JSON snapshot and NO_COLOR/ASCII output unchanged or deliberately changed, with width and height budgets at 160/116/80 |
| Q2 | Tests and goldens per phase, and a phase split that keeps the suite green |
| Q3 | Render-to-image harness and the fixed-rubric reviewer method |
| Q4 | ANSI colour depth, detection, fallbacks and 16-colour role distinctness |
| Q5 | Live path vs one-shot path styling and the styled-capture gate |
| Q6 | Zellij 0.44.2 go or no-go |
| Q7 | The 64-hex-character fixture in the 80-column Decision Desk frame |

### 1.5 Standing constraints

Read-only; real data only (no invented owners, requester, mapped trees or affected sessions); question text screen-only; NO_COLOR, ASCII and widths 160/116/80 keep working; ANSI-styled output is the primary rich mode; no blinking, no mouse; PR target `IronbellyOrg/IronClaude` via `/sc:pr-submit --monitor 3`.

### 1.6 Scope boundary of this synthesis

Section 2 below states only what the research traced to source code (or measured files). Items the research marks [UNVERIFIED] or [CODE-CONTRADICTED] are corrected or listed in 2.7 and are not asserted as current architecture. Options, recommendations and the phase plan belong to other report sections.

## 2. Current State Analysis

All claims are [CODE-VERIFIED] unless tagged otherwise. Citations are `file:line` from research files 01 to 05 (OBS = `src/superclaude/cli/observe/`).

### 2.1 Render, view and terminal pipeline

**Terminal policy and console (OBS/terminal.py, 160 lines)**

| Fact | Evidence |
|---|---|
| Constants `MIN_WIDTH=80`, `MIN_ROWS=8`, `FULL_WIDTH=160`, `LINE_WIDTH=116` | terminal.py:21-24 |
| Four width classes: `full` (>=160), `line` (>=116), `short` (>=80), `narrow` (<80). (Corrects the task prompt's three classes.) | terminal.py:63-70 |
| `TerminalPolicy` has `width`, `height`, `no_color`, `ascii`, `width_class`; no colour-depth or "styled" field | terminal.py:37-51 |
| `no_color = bool(env.get("NO_COLOR"))` (set and non-empty); `use_ascii = flags["ascii"] or not _is_utf8(encoding)`; colour and ASCII are independent; no TERM, COLORTERM or isatty check | terminal.py:73-92 |
| `make_console()` builds `Console(width, height, highlight=False, markup=False, emoji=False, color_system=None if no_color else "standard", no_color=..., safe_box=policy.ascii, record=...)`: colour depth fixed at Rich "standard" (16 colours), never "auto", "256" or "truecolor" | terminal.py:110-125 (depth at :121) |
| `GLYPHS` has exactly three names: `selected` (`▸`/`@`), `truncate` (`>`/`>`), `hrule` (`─`/`-`); no box-drawing glyph | terminal.py:30-34 |
| `safe_box=policy.ascii` does NOT turn a Rich `Panel` into `+-\|` borders: Rich 15.0.0 probe printed identical rounded Unicode borders for `safe_box` True and False; ASCII needs an explicit `box=rich.box.ASCII` [CODE-CONTRADICTED vs the earlier assumption; corrected] | probe in 01 section 1; rich/box.py:79-83 (03 section 6 rule 3); `test_terminal.py` pins only the attribute value (cited as :109 and :115 in gaps row 57) |
| `ascii_safe` encodes with `errors="replace"`: every non-ASCII char becomes one `?`; `clip()` returns plain `str` (cut tail becomes one `>`, never splits a wide char) | terminal.py:133-160 |
| Only one `Console(` construction exists in OBS | terminal.py:114 |
| `sanitize()` strips OSC/DCS/SOS/PM/APC/CSI/ESC and Cc/Cf/Cs; with `markup=False` worker text cannot inject ANSI, so styled spans must be made by the renderer, never by escape strings | OBS/sanitize.py:15-48; terminal.py:116 |

**Call chain and return types**

| Function | Location | Returns |
|---|---|---|
| `build_view(result, session, clock)` | view.py:894-1060 | frozen `View` (view.py:303-339); display strings only, no styled objects |
| `screen_lines(view, policy, message=None)` | render.py:390-521 | `list[str]`, each at most `policy.width` cells |
| `render(view, policy, message=None)` | render.py:524-531 | `rich.console.Group` of one `Text(line, no_wrap=True, overflow="crop")` per string (:528) |
| helpers `counts_lines`, `_panel_lines`, `_desk_lines`, `_inspector_lines`, `_notes`, `_help_lines`, `_header_lines`, `wrap`, `_row_line`, `_cell`, `_pad`, `_question_line` | render.py:94, 359, 329, 255, 290, 304, 246, 62, 233, 87, 83, 311 | `list[str]` or `str` |

- No render.py function returns `Text`, `Table`, `Panel`, `Layout` or `Columns`; render.py imports only `cell_len`, `Group`, `Text` (render.py:12-14). There is no per-span information anywhere in the pipeline.
- Source guard: `tests/observe/test_render.py:396-403` fails if render.py matches `observe\.(adapter|collector|parse)\b|sorted\(|\.sort\(|from_markup|Console\(`.

**Layout and fitting logic (render.py)**

| Area | Behaviour | Lines |
|---|---|---|
| `wrap` | cell-based; breaks at the last space inside the cut, else hard-cuts at the width with no marker; never truncates | 62-80 (cut rule :73, :77) |
| COUNTS strip | tokens joined by two spaces; protected tokens wrap, unprotected may be cut with `>` inside a token (cause of M-16) | 94-135 (cut path :127-132) |
| `_columns` | three layouts by width class; `full` has 11 columns and uses exactly 160 cells at 160 (2+114+22+12+10 separators), so a 2-cell border needs the elastic `flags` column to give up cells; `line` and `short` have no workerState/dispatchStatus column; `line` id width `min(width-64, 60)` (source of M-17 band at 116) | 155-230 (:159-192, :193-213, :214-230) |
| Column heading and rule | printed only when `policy.width_class == "full"` and rows are visible (cause of M-10; the condition is in `screen_lines`, not `render()`) | 497-498; budget mirror :439 |
| `_help_lines` | `clip` (cut with `>`) when questions are off, `wrap` when on (cause of M-11 and M-15) | 304-308 |
| `_question_line` | link on: `▸ ` or two spaces + lead (age, optional state) + text cut with `...` + `  reason unknown`; age is part of `lead`, no fixed gutter | 311-326 |
| `_desk_lines` | stacked list: `DECISION DESK`, `qid  age`, question text limited to `DESK_TEXT_LINES = 4` (last cut with `...`), `label: value` fields (two-cell continuation indent), notes | 329-356; view.py:99 |
| `_panel_lines` order | title, `one Run only`, state lines, disclosure, counts line, caveat, question lines, cut text, `DESK_SELECTED_HIDDEN`, desk, empty/window-full/notes, retention | 359-387 |
| Height budget with questions on | desk sized first; `spare = height - (len(head)+len(tail)+base+footer_height+ledger_fixed+1+1+1+selected_note)`; "questions win on a short terminal (2026-11-12)" | 433-481 (:447-457) |
| Ledger window | `reserved = len(top)+len(body)+footer_height+1`; `capacity = max(height - reserved, 1)`, so at least one row is always forced | 499-503 |
| Final clamp | none: there is no `lines[:height]` on the normal screen | absence verified, not exercised |

**Measured screens (base fixture, `LINES=40`, `--once --width W --fixture base`)**

| Width | header1 | header2 | counts | changes | gap | notes | title | heading+rule | rows | overflow | footer | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 160 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 2 | 28 | 1 | 1 (132 cells) | 40 |
| 116 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 0 | 29 | 1 | 2 | 40 |
| 80 | 2 (`as of` wraps) | 1 | 2 (cut `runs seen>`) | 1 | 1 | 1 | 1 | 0 | 28 | 1 | 2 (cut `e exp>`) | 40 |

At 80 columns and height 40 every row is used; there is no spare row (02 section 9.4).

**View-model facts that fix text**

- `QuestionLine.text` (subject based, `age  subject  reason unknown`, view.py:744) is separate from `screen_text`/`shown`/`ask` (payload question text, screen only; view.py:206-225, :748-757). `DeskView` holds `qid`, `age_text`, `ask`, `link`, `session_fields`, `notes` (view.py:229-239); `RowView` keeps raw state strings (view.py:158-179), so a state-colour table can key on them.
- `text_of` renders an absent value as bare `unknown`; a real source value `unknown` is quoted (view.py:377-385). A bare `unknown` also occurs inside free text, so a regex-based muting rule would also hit those.
- No `READ ONLY` text exists anywhere under OBS (grep) [confirms M-13]. `header1` is one string built at view.py:914-921.
- The counts token reads `POLICY FROZEN unavailable (no source)` (view.py:948); RR 20 says `FROZEN unavailable (no source)` [CODE-CONTRADICTED doc; code wording is used].

**Colour depth, measured (Rich 15.0.0, `Text("x", style="bold #ff8800")`)**

| `color_system` | Output |
|---|---|
| `standard` (what `make_console` builds) | `\x1b[1;91mx` (amber collapses to bright red 91) |
| `256` | `\x1b[1;38;5;208mx` |
| `truecolor` | `\x1b[1;38;2;255;136;0mx` |
| `auto` on a `StringIO` | resolves to `None`: plain text |

- Rich emits ANSI into a `StringIO` whenever `color_system` is explicit, so adding any style changes the `printed()` captures in tests. Under NO_COLOR (`color_system=None`, `no_color=True`) the same Text prints plain: bold is dropped together with colour, so hierarchy under NO_COLOR must live in text and glyphs.
- Rich caches a Style's ANSI codes per Style object, so the first colour system used in a process wins for later consoles (observed in the probe).
- Mockup palette downgraded with Rich to 16 colours (computed, not observed on a terminal; 04 section 3 measurement supersedes 01's inference): base 15, slate 8, cyan 14, amber 11, and muted, green, red, violet all 7. State colours are therefore not distinguishable by colour alone at 16 colours.

### 2.2 Live screen vs one-shot path, and the export contract

**Every path from view to output**

| Path | Entry | Console | Output |
|---|---|---|---|
| Interactive live screen | `run_interactive` commands.py:351 -> `run_loop` :282 -> `LiveScreen.draw` :264 | `make_console(policy)` at :270 inside `Live(screen=True, auto_refresh=False)` (:269-271) | ANSI to stdout; alternate screen only if `console.is_terminal` |
| `--once --width N` | `run_once` commands.py:238-242 | `make_console(policy, file=io.StringIO(), record=True)` (:240) | `console.print(render(...))` (:241), `console.export_text()` (:242, styles dropped), `_emit` (:245) |
| `--once` (no width) | commands.py:243-244 | none | `record_text(view)` (export.py:71), no Rich |
| `e` key export | commands.py:324-330 | none | `write_atomic(record_path(...), record_text(view))` |
| Snapshot | `_write_snapshot` commands.py:213-219 (called :247, :312) | none | `write_atomic(target, snapshot_json(view))` |

- `force_terminal`, `legacy_windows` and `_environ` are never passed; the live console has `file=None`. Only two paths use Rich and both go through `make_console`.
- No test references `LiveScreen` or `run_interactive` (`tests/observe/test_commands.py:285-297` uses a `FakeScreen`); the live path has no styled-capture test.

**Live path, hop by hop (02 section 9.1; Rich 15.0.0 installed at `.venv/lib/python3.10/site-packages/rich/`)**

| Hop | Code | Effect |
|---|---|---|
| 1 | `LiveScreen.draw` commands.py:264-274 | builds `Live` on first draw or on shape change `(width, height, ascii, no_color)` (:265), then `update(group, refresh=True)` |
| 2 | `render` render.py:524-531 | unstyled `Text` per line, no height clamp |
| 3 | `make_console` terminal.py:110-125 | explicit width and height, `"standard"` colour, Rich decides `is_terminal` |
| 4 | `Live.start` rich/live.py (~:125-130) | `set_alt_screen(True)` writes control code only if `is_terminal` and not legacy Windows |
| 5-6 | `Live.renderable` :228; `Screen.__rich_console__` rich/screen.py:40-54 | group wrapped in `Screen`; every line padded to console width and the list **cut to console height** |
| 7 | `Live.process_renderables` :279-296 | prefixes `Control.home()` on the alternate screen |

Measured bytes (stand-in console, `force_terminal=True`): `ESC[?1049h ESC[H ESC[?25l ESC[H`, then styled, width-padded rows, then `ESC[?25h ESC[?1049l`. Style survives as SGR (`ESC[1;31m ... ESC[0m`); padding carries no style.

- **Silent bottom crop:** with the real 80-column base screen (40 lines) in a console of height 38, the last two lines (the key list and `shown 28/54 | collected 80 / reported 80`) are dropped, with no ellipsis, because `Screen` cuts before `Live`'s ellipsis step. `--once --width` and plain tests print all lines, so they cannot see this.
- A non-terminal `make_console` console with `Live(screen=True)` writes nothing at all. Capture routes measured: A (`force_terminal=True` console plus `Live`; no seam into the real `LiveScreen` today) and B (`pexpect` 4.9.0 pty with a stand-in child; `tests/observe/spike_child.py:64` already runs a raw `Live(screen=True)` on a pty). Whether `run_interactive` accepts `--fixture` and the real `LiveScreen` under a pty are [UNVERIFIED].
- Resize is by polling (`make_policy()` each draw, no SIGWINCH handler; keys.py `_HANDLED` is INT/TERM/HUP/TSTP/CONT); redraw every `REDRAW_SECONDS = 0.5` (commands.py:58, :335-337). No mouse mode and no blink sequence exist (keys.py enables only cbreak, keys.py:61).

**`export_text` behaviour (probe, Rich 15.0.0)**

| Mode | NO_COLOR false | NO_COLOR true |
|---|---|---|
| stream value | `\x1b[1;31mhello\x1b[0m` | `hello` |
| `export_text()` | `hello` | `hello` |
| `export_text(styles=True)` | `\x1b[1;31mhello\x1b[0m` | `\x1b[1;31mhello\x1b[0m` (colour still present) |

`export_text(styles=True)` therefore ignores NO_COLOR and the `standard` down-conversion; the NO_COLOR-correct styled route is the StringIO `console.file.getvalue()`. `render_current.py` (94 lines, `.dev/issues/409/visual-parity/inputs/tools/render_current.py:73-75`) uses `export_text(styles=True)` with `HEIGHT = 50` (:38) while mockup frames are 48 (160) and 42 (116, 80) lines high [measured, gaps rows 13-14].

**Export contract (what must stay byte-stable)**

- export.py imports no Rich (export.py:11-18, module docstring :1-6). `record_text` (:71-86) writes `q.qid | q.text` plus ` | dispatchId=<id> | link=<state>` when linked (:103-111); `_questions_dict` (:158-180) writes ids, times and counts only; `snapshot_dict` uses a fixed field list (`_TEXT_FIELDS` :25-45); `SCHEMA_VERSION = 1` (:20).
- No write path touches question text: `write_atomic` is called only at commands.py:216 and :327; `.ask`, `screen_text` and `.shown` are used only in view.py and render.py. The question text leaves the process only on screen, including stdout of `--once --width` (asserted by `tests/observe/test_commands.py:832-841`).
- Both gates are `True`: `QUESTION_GATE_PASSED` (commands.py:67) and `QUESTION_LINK_PASSED` (commands.py:70), each one assignment per line ending `# fmt: skip`; pinned by regex over commands.py text (`tests/observe/test_commands.py:747-756`, `:762-772`), which also require the words `release-gates.md` and `Task 18` to stay in commands.py. `_link_on` (:178-180) is the only switch that lets question text and the dispatch link reach the view.

**Data flow for question text:** `Options.questions` -> gate + run id -> `Collector(questions, link)` (collector.py:152-153) -> `parse_questions(link=...)` (parse.py:512-607; `ask` capped at `ASK_CAP = 400` with `...`, :499-503) -> `QuestionState` -> `_questions_panel` (view.py:723-759) -> `QuestionLine` -> `_desk` (view.py:814-874) / render.

### 2.3 Tests and goldens

Baseline: `uv run pytest tests/observe/ -q -p no:cacheprovider` gave 766 passed in 25.70 s on 2026-11-17 across 22 test modules (28 Python files) and 2 goldens; no tracked file was modified.

**What the tests pin**

| Pin | Location | Breaks when |
|---|---|---|
| One renderable per plain line: `len(group.renderables) == len(screen_lines(...))` | test_render.py:396-399 | `render()` returns a Panel/Table/Columns as one renderable |
| Source regex on render.py (`sorted(`, `.sort(`, `from_markup`, `Console(`, `observe.adapter/collector/parse`) | test_render.py:400-404 | new code uses those tokens |
| Only terminal.py may contain `Console(`, `NO_COLOR`, `COLUMNS`, `stdout.encoding`, `getpreferredencoding` | test_terminal.py:181-198 | a theme module names them |
| export.py imports no `render`, `parse`, `adapter`, `collector`, `Console`, `rich` | test_export.py:238-243 | exporter gains Rich |
| Colour printed bytes equal NO_COLOR printed bytes | test_render.py:250-259 (:256) | any style is added (one test; must be rewritten, not deleted) |
| No SGR 5 or 6 (blink) in any render | test_render.py:177-185 | a blink attribute is added |
| NO_COLOR output has no ESC | test_render.py:970-987; test_terminal.py:41-51 | styles emitted under NO_COLOR |
| ASCII mode renders only ASCII | test_render.py:263, :591, :903; test_commands.py:131 | box glyphs lack ASCII forms |
| Whole-line equality and `startswith` | `GAP_NOTICE in lines` (:242, :454, :490), `DESK_TITLE in lines` (:900, :924, :997), `"/ab" in lines` (:393), `window full: ...` (:547; test_question_cap.py:77, :121), `lines[0].startswith("terminal too small")` (:241, :557), `dispatchId:` (:129, :964), `▸ ` (:897), ` *` (:373), `questions shown ` (:479, :646) | a border, gutter or column prefix is added |
| Desk slice `desk[2 : line startswith "dispatchId:"]`, 4 text lines at 80 | test_render.py:943-966 | the desk gets a left border |
| `endswith("reason unknown")` and `^\s*\d+[smh]  ` | test_render.py:930-950 | two columns or border suffixes |
| Vertical budgets | test_render.py:83, :460, :660 (decision_2), :990 (heights 8-60); test_inspector_scroll.py:36-72 | added chrome rows |
| `QUESTIONS_KEYS_LINE == KEYS_LITERAL` (107 chars) | test_linkoff_screen_reference.py:67-69 | key line wording changes |
| 80-column footer in last 3-4 lines, no line ending `>` with `exp` | test_render.py:748 | footer moves |

**Goldens**

| Golden | Producer | Pinned by | Content | Style-only change alters | Text or layout change alters |
|---|---|---|---|---|---|
| `tests/observe/golden_release1_surface.json` | `surface()` in tests/observe/release1_surface.py:41-62; `json.dumps(..., indent=1, sort_keys=True, ensure_ascii=False)`, no trailing newline | T47 `test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface` (test_render.py:611-624) | 5 variants x 14 keys (header1, header2, gap_notice, record_text, snapshot_json, `lines_{160,116,80}x{40,12}`, `printed_{160,116,80}`); docstring says generated from `git archive 9e2608b03` (commit verified to exist) | the 15 `printed_*` values (no ESC byte in the file today) | the 30 `lines_*` values and `printed_*`, plus header/gap/record keys if view or exporter strings move |
| `tests/observe/golden_questions_linkoff.json` | `capture(clock)` in test_linkoff_screen_reference.py:50-64; `json.dumps(..., indent=1, ensure_ascii=False) + "\n"`; no recorder script exists | T64 `test_the_link_off_questions_screen_equals_the_reference` (:72-75) | scenarios `five` and `long_subject`, widths 160/116/80, height 40 (24/24/25 and 22/22/23 lines) | nothing (plain lines only) | all six line lists |

- `record_golden.py` and `record_golden_questions.py` do not generate these two goldens; they record redacted fixtures under `OBS/fixtures/` that feed data-only tests (03 section 4c). In-memory runs of `surface()` and `capture(FakeClock())` reproduce both goldens byte for byte.
- Git history: one commit each (`cd8736199` #514 and `3206bdb9c` #592). Regenerating T47's golden from the current tree ends its "byte-identical to release 1" meaning; issue #606 lists the four files as deliberate presentation updates (`.dev/issues/606/issue-body.md:84`).
- Modules that touch screen text or the console: test_render.py, test_terminal.py, release1_surface.py, test_inspector_scroll.py, test_golden_contract.py, test_linkoff_screen_reference.py, test_export.py, test_question_cap.py, test_fixtures.py, conftest.py. test_view.py, test_snapshot_schema.py and the other modules are presentation-blind (classified from names and docstrings; not read line by line: [UNVERIFIED] for a literal-by-literal list).

**Q7 fixture (measured today, in memory)**

- No test fixture contains a 64-hex token, a hash or a long path (grep over `tests/observe/*.py`).
- With a synthetic 222-character plan ask (plan path, two file paths, 64 hex chars) through `r3_screen` (link on, height 70): at 160 the desk text is 2 lines, at 116 and 80 it is 3 lines, and the hash is whole on its own line at all three widths; the list line is cut with `...` before the hash. A single token longer than the width (about 140 to 165 characters) is hard-split at the width with no marker and no regard for `/`.
- Desk lines at 80 columns for that fixture are 78, 78 and 64 cells (gaps row 45 corrects a "exactly the width" statement). `_desk_lines` with a hash in the question produced 4 lines (exactly `DESK_TEXT_LINES`, no `...`); the `resource.worktreeId: <hash>` field printed as label then `  <hash>` (66 cells).
- No existing test runs wide characters, a hash or a long path through `session_fields` (render.py:347-353).

### 2.4 Mockups and spec versus current output

**Mockup colour decode (all nine `.ansi` files; 24-bit foreground only, no background code, no 256-colour or 16-colour code, no dim, italic, underline or reverse)**

| Role | RGB | Used for | 16-colour index | 256 index |
|---|---|---|---|---|
| base | 225,233,238 | body text, padding | 15 | 189 |
| muted | 165,182,194 | freshness line, keys hint, `Affected:`, footer caveat | 7 | 145 |
| slate | 82,108,128 | secondary pane borders, rules, secondary titles, empty bar fill | 8 | 60 |
| amber | 250,178,25 | attention panes (heavy frame), question text, ages, `SYNTHETIC · READ ONLY` badge, big count digit | 11 | 214 |
| cyan | 112,205,226 | screen title `◈ ...`, count tile, running sessions | 14 | 80 |
| green | 139,215,175 | settled | 7 | 115 |
| red | 240,141,150 | failed | 7 | 210 |
| violet | 194,173,242 | frozen | 7 | 147 |

Bold is used for titles, question text, ages and counts (3 to 16 `ESC[0;1;` occurrences per file). The mockups draw no selected row; selection is only a keys hint, so M-18 has no mockup evidence [UNVERIFIED how selection should look]. The PNGs show a dark navy background that the `.ansi` files do not set [UNVERIFIED whether part of the design].

**Mockup pane geometry (measured; frame 48 lines at 160, 42 at 116 and 80; widths exact; left margin 1)**

| Screen / width | Panes |
|---|---|
| signal-bridge 160 | HUMAN QUESTION heavy 46 wide over OBSERVATION WINDOW round 46; SESSION REGISTER round 74; SIGNALS heavy 34; rows 6-44 |
| signal-bridge 116 | HUMAN QUESTION heavy 114 (rows 6-12); SESSION REGISTER 78 beside OBSERVATION WINDOW 34 (rows 14-38); no SIGNALS |
| signal-bridge 80 | HUMAN QUESTION heavy 78; SELECTED FLEET SLICE round 78; counts as one cyan line |
| attention-ledger 160 | OPEN HUMAN QUESTIONS heavy 114 (rows 6-44); right column 42: SEEN IS NOT RESOLVED tile (cyan, rows 6-18) over RETAIN CONTEXT (slate, rows 21-38) |
| attention-ledger 116 | left 70, right 42, same structure |
| attention-ledger 80 | single column; three plain question lines above one SELECTED SIGNALS pane; no tile, no RETAIN CONTEXT |
| decision-desk 160 | HUMAN QUESTION heavy 76 over OTHER OBSERVED QUESTIONS 76; AFFECTED SESSION EVIDENCE 80 |
| decision-desk 116 | HUMAN QUESTION full width over AFFECTED SESSIONS 66 + OTHER OBSERVED QUESTIONS 46 |
| decision-desk 80 | three stacked 78-wide panes |

Common chrome: line 2 `◈ <SCREEN>` (bold cyan) with right-aligned `SYNTHETIC · READ ONLY` (amber); titles inset in the top border; a slate rule above a two-line footer. Pane titles differ across widths and `OPEN HUMAN QUESTIONS` is retired by RR 38 (code: `COORDINATOR QUESTIONS`, view.py:53), so titles must not be copied blindly. Frame arithmetic from the mockups: 160 ledger = 1 + 114 + 2 + 42 + 1 = 160 (supersedes 01's untagged 157-of-160 estimate).

**Spec versus code (current output captured in `.dev/issues/409/visual-parity/inputs/current/<w>/{ledger,questions,desk}.txt`, pre-fix baseline, produced by `render_current.py` with synthetic data at height 50)**

| Screen / width | Current structure | Differences vs mockup |
|---|---|---|
| ledger 160 | 4 header lines, gap notice, title, 12-column table with heading and rule, `39/54 shown +15 more`, one footer line | no colour, panes, tiles; one footer line instead of rule plus two |
| ledger 116 | 5 header lines, 4-column form without heading, two-line footer | M-10, M-17, no panes |
| ledger 80 | header wraps (`as of` alone), counts cut `runs seen>`, 3-column rows, key list cut `e exp>` | M-10, M-11, M-13, M-16 |
| questions 160 / 116 / 80 | one stacked block: title, run, state, disclosure, counts, caveat, rows, retention, then worker table; disclosure wraps to two lines at 116 and 80; `n/p` / `question` split at 116 | M-03, M-05, M-07, M-14, M-15, M-16 |
| desk 160 / 116 / 80 | bare `DECISION DESK` block under the list with 9 `label: value` lines, then the worker table repeated | M-04, M-12, M-18 |

Spec lines (verified against `RR`, 107 lines; FIND citations all resolved): the two O-1 reversal targets are RR 43 and RR 57 ("one stacked block"); lines that change if the fix proceeds are 17 (badge), 25 (pane glyph forms), 41 and 61 (RETAIN CONTEXT), 43 and 57 (columns), 70 (muting becomes implemented). Spec guards to keep: RR 20 and 32 (gap notice and COUNTS wording), 31 (`nextAction.kind` verbatim), 47 and 49 (count and disclosure verbatim), 50 (glyph and age format), 57 (desk line order), AC-9 T26-T28 (no SGR in NO_COLOR, no ESC in exports, no blink). RR 37-41 and 60-61 describe the two-column layout, `SEEN IS NOT RESOLVED` tile and `RETAIN CONTEXT` as the layout, but RR 43 says only the stacked block was built; treat them as design reference. RR 61 requires two 80-column invariant lines the output lacks and one of them contradicts RR 42 (AD-7): spec self-contradiction (CODE-CONTRADICTED).

**Per-finding code change map (where today's code decides each finding)**

| Id | Function and line to change |
|---|---|
| M-01 | `render()` render.py:524-531 (:528) plus a role table; `make_console` terminal.py:121 |
| M-02 | `_panel_lines` :368, `_desk_lines` :333, ledger title :495, header :410-412; box glyphs in terminal.py:30-34 |
| M-03, M-04 | `_panel_lines` 359-387, `_desk_lines` 329-356, sizing 433-479 (spare 447-457) |
| M-05 | render-only tile at `_panel_lines` :373; `counts_line` string is view.py:761 and is written verbatim to the record (export.py:99), so it must not change |
| M-06 | `screen_lines` 409-414, 433-486, 495-512; `counts_lines` 94-135 |
| M-07, M-18 | `_panel_lines` 368-376; `_question_line` 311-326 (mark :317) |
| M-08 | style pass in `render()`, or in builders: view.py:100, 377-385, 634-637, 706, 744, 761; render.py:319 |
| M-09 | `_row_line` 233-243 and desk fields (view.py:843-853); only `full` and the desk carry workerState and dispatchStatus; at 116 only the liveness verdict (`_verdict` :151-152) can be coloured |
| M-10 | render.py:497 (gate) and the `ledger_fixed` mirror :438-440; `reserved` :499-501 reads `len(body)`, which already holds the heading rows once :497-498 appends them, so it needs no separate edit |
| M-11, M-15 | `_help_lines` 304-308; footer branches 426-431, 514-520 |
| M-12 | `_desk_lines` 339-353; view.py:843-853 |
| M-13 | split inside render.py only (header1 is also used by `record_text`, export.py:76, and by `release1_surface.py:50`) |
| M-14 | `_panel_lines` 359-387; facts live in `run_line`, `caveat_line`, `counts_line`, `retention_line` (view.py:794, 798, 761, 804) |
| M-16 | `counts_lines` 127-132 |
| M-17 | render.py:195-196, 215 |
| G-1 | GLYPHS terminal.py:30-34; `ascii_safe` is applied in `wrap`, `clip`, `counts_lines`, `_question_line`, so new glyphs must go through `glyph()` not literals |
| G-2 | terminal.py:110-125 |

### 2.5 Environment: Zellij and offline render tools

**Installed Zellij (help text and config reads only; no session was started)**

| Item | Fact |
|---|---|
| Binary | `/usr/local/bin/zellij`, version 0.44.2; `zellij setup --check` reports config well defined, config dir `/home/coder/.config/zellij` |
| `config.kdl` (53 lines) | active: `theme "aidev02"`, `show_release_notes false`, `default_shell "/bin/bash"`, welcome-screen plugin settings; no `keybinds` block |
| `layouts/default.kdl` (58 lines) | tab bar 1 row on top and status bar 2 rows at the bottom (`zellij:tab-bar`, `zellij:status-bar`, lines 48-58) |
| `layouts/agent.kdl` (265 lines) | theme `aidev02_agent`; status bar only (2 rows, no tab bar); differs from aidev02 in `frame_selected` and `ribbon_selected` (magenta 5 vs cyan 6) |
| `themes/aidev02.kdl` (252 lines) | every value an ANSI-16 integer; cyan primary |
| Provenance | provisioned from `/etc/skel` (machine setup, not this repo); presence in CI [UNVERIFIED] |
| Help-text features | `-l/--layout`, `--layout-string`, `zellij run -f --width --height -x -y`, `zellij action dump-screen -a/--ansi -f -p --path` (text or ANSI only, never an image) |

Floating-pane behaviour, `dump-screen --ansi` fidelity for colours, wide glyphs and box drawing, command panes in a layout, reading the active Zellij theme at runtime, and Zellij in CI are all [UNVERIFIED] (no live session was allowed). Zellij chrome (1+2 rows plus pane frame) was not converted to usable rows against the 44-row contract (gaps row 42). Evidence-only reading for Q6: no-go as the render harness or an observer dependency (no image output, behaviour unverified); optional manual presentation environment. Web findings (`research/web-02-zellij-and-terminal-capture.md`) are external context and are outside this synthesis's input list.

**Offline render tools (project venv, Python 3.10.20, uv 0.11.8)**

| Tool | Present |
|---|---|
| Rich 15.0.0 (`export_text`, `export_html`, `export_svg`, `save_*`) | yes |
| PIL, cairosvg, pyte, playwright, fontTools | `ModuleNotFoundError` for all |
| chromium, chrome, rsvg-convert, inkscape, convert, magick, freeze, termshot, aha, ansi2html, unzip | missing |
| node 24 and npx | present |
| `~/.cache/ms-playwright` | absent |
| DejaVu Sans Mono (`/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf`) | present; glyph coverage of the mockup set [UNVERIFIED] |

- `pyproject.toml:34-43` declares runtime deps (pytest, click, rich>=13.0.0, pyyaml, jsonschema, jinja2, `pexpect>=4.9`, httpx); `dev` extra at :45-56 (pytest-cov, pytest-benchmark, scipy, `ruff==0.15.20`, mypy). No image, SVG, terminal-emulator or browser package is declared and the Makefile has no render, screenshot or observe target.
- Offline in this environment: text and ANSI assertions, Rich SVG/HTML export (text formats). No PNG can be produced without a new dependency or browser. Both Gate 1 QA reviewers read mockup PNGs successfully with the Read tool (gaps row 40), so a Claude reviewer can view the mockup images; rendering the new output to an image offline is the open piece.
- `render_current.py` already writes per-width text and ANSI for three screens and exposes the recorded console at line 73, so adding `export_svg` or `export_html` takes a few lines; it has no `if __name__` guard (calls `main()` at import, line 93). Mockups exist as `.png`, `.ansi` and `.txt`, so a text and ANSI comparison needs no image tool.

### 2.6 Contradictions between research files and which evidence wins

| Topic | Statement A | Statement B | Resolution |
|---|---|---|---|
| 16-colour role distinctness | 01 section 7: slate and muted land on greys, amber has no standard colour (inference) | 04 section 3: measured downgrade, amber 11 distinct, but muted, green, red, violet all 7 | 04 wins (measured, reproduced by two reviewers) |
| Styled one-shot export route | 01 and the existing harness use `export_text(styles=True)` | 02: `styles=True` ignores NO_COLOR and the standard downgrade (probe) | 02 wins; use `console.file.getvalue()` |
| Slack in the 160 two-column fit | 01 8.2 item 5: 114+1+42 = 157 (tagged UNVERIFIED) | 04 geometry: 1 margin + 114 + 2 gap + 42 + 1 margin = 160 | 04 wins (measured on mockups) |
| Full ledger width | FIND M-06 / 04: "153 cells" | 01 and 04 arithmetic: exactly 160 (render.py:159-192) | code wins; 153 is [UNVERIFIED] |
| Width classes | task prompt: full/line/narrow | code: full/line/short/narrow | code wins |
| `safe_box` ASCII boxes | earlier drafts of 03 and 04 | probe: not true | probe wins (corrected in cycle 1) |
| Token wording | RR 20 `FROZEN unavailable ...` | code `POLICY FROZEN unavailable ...` (view.py:948) | code wins |
| Location of header gate | FIND M-10: `render()` | code: `screen_lines` render.py:497 | code wins; behaviour confirmed |
| Gate-test ranges | 03 section 4d: 747-760, 762-777 | 02: 747-756, 762-772 | 02 wins |
| 80-column desk line width | 03: "exactly the width" | reproduced: 78 cells | reproduction wins |
| `QUESTION_GATE_PASSED` | doc `.dev/reviews/orchestrator-tui-alignment-20261113/05-observe-built-state.md:27`: False | code: True (commands.py:67) | code wins; doc predates #592 |

### 2.7 Items excluded from Current State as unverified (placed here, not asserted above)

| Item | Why excluded |
|---|---|
| Meaning of each of the three `+1` terms in `spare` (render.py:454-456) | read from a comment only |
| East-Asian-ambiguous box and block glyph width in the owner's terminals | Rich `cell_len` says 1; terminal behaviour not observed |
| Which of `injection` and `long-identifiers` fixtures interact with styling | not exercised |
| Frame cost at heights 24, 12 and `MIN_ROWS = 8` and the questions-on desk screens at heights below 70 | not measured |
| Real `superclaude observe --questions` and `--run` screens; real `LiveScreen` under a pty | need a live source or a seam |
| Content of plan-approval asks (path, file list, 64-char hash) being stored as `question` rows | pr-591-comment.md lines 26-31 list it as unverified |
| Mockup palette on light terminals; mockup PNG background as part of the design; selected-row look | no document or mockup decides |
| `test_view.py` literals a text phase would break; ten modules classified by docstring | not read line by line |
| Zellij runtime behaviour, theme readability, CI presence | no session started |
| Whether `pip` or `uv` can install Pillow, cairosvg, pyte or a Playwright browser here; cairo system library | network and system libraries not tested |

### 2.8 Current State Summary

**Pipeline (code-verified, as built today)**

```
Collector / FixtureSource
        |
        v
build_view(result, session, clock)        view.py:894-1060
  -> frozen View (strings only)           view.py:303-339
        |                         \
        |                          +--> record_text(view)   export.py:71   (no Rich; ids + subject text;
        |                          +--> snapshot_json(view) export.py:183   no question text)
        v
screen_lines(view, policy, message)       render.py:390-521
  -> list[str], each <= policy.width cells (wrap / clip / _cell, cell_len)
        |
        v
render(view, policy, message)             render.py:524-531
  -> Group(Text(line, no_wrap=True, overflow="crop") x N)   (no style)
        |
        v
make_console(policy)  "standard" 16-colour, NO_COLOR -> None      terminal.py:110-125
        |
        +--> LiveScreen.draw -> Live(screen=True) -> Screen pad + crop to height -> stdout   commands.py:264-274
        +--> --once --width N -> StringIO console -> export_text() (plain) -> stdout        commands.py:238-245
```

**Summary table**

| Area | Current state | Evidence | Implication for the redesign |
|---|---|---|---|
| Styling | none; one unstyled `Text` per line | render.py:528 | all colour, weight and role work is new; text must stay identical under NO_COLOR and ASCII |
| Pipeline type | pure `list[str]`; no `Text`, `Table`, `Panel`, `Layout`, `Columns` | render.py:12-14 | styles and panes need role metadata, a parallel styled path, or hand-built frame lines |
| Colour depth | fixed `"standard"`; NO_COLOR gives `None` and drops bold too | terminal.py:121-122 | per-depth explicit roles; hierarchy under NO_COLOR carried by text and glyphs (G-1, G-2) |
| ASCII panes | 3 glyphs only; `safe_box` does not ASCII-ize Rich boxes | terminal.py:30-34 | add box glyphs with `+ - \|` forms, or pass `box=rich.box.ASCII` explicitly |
| Width budget | 160 table uses all 160 cells; `flags` is the only elastic column | render.py:159-192 | a frame costs 2 to 4 cells per pane |
| Height budget | no final clamp; one ledger row forced; live screen crops the bottom silently | render.py:499-503; rich/screen.py:40-54 | every added frame or heading row must be counted in `screen_lines`; assert `len(lines) <= height` |
| Heading and keys | heading only at `full`; key list clipped at 80 with questions off | render.py:497, 304-308 | cause of M-10, M-11, M-15 |
| Live vs one-shot | live keeps styles; one-shot `export_text()` drops them; `styles=True` ignores NO_COLOR | commands.py:242; probe | styled capture should come from `console.file.getvalue()`; the width-bound `"\x1b" not in out` test (test_commands.py:121) would change |
| Export contract | record and snapshot independent of Rich; question text screen-only | export.py:11-18, 103-111, 158-180 | render-only changes for M-05, M-08, M-13, M-14; gates and `record_text` stay byte-stable |
| Tests | 766 pass; none covers the real Live screen | test_commands.py:285-297 | pixel-level checks need a render gate (pty or force_terminal seam) |
| Goldens | release-1 golden (T47) and link-off golden (T64) pin plain screens; style-only changes touch 15 `printed_*` values only | test_render.py:611-624; test_linkoff_screen_reference.py:72-75 | text or layout phases need an owner decision to re-baseline, or gated new look |
| 64-hex hash | fits whole on its own line at 160/116/80; long paths hard-split mid-word; no test pins either | 03 section 5c | add the fixture test before any frame narrows the text width |
| Mockups | 8 truecolor roles, heavy and rounded boxes, two or three columns at 160 and 116, single column at 80 | 04 sections 2, 4 | 16-colour collapse of muted, green, red, violet needs explicit roles |
| Environment | Zellij 0.44.2 installed (unexercised); Rich 15.0.0 SVG/HTML export offline; no rasteriser | 05 sections 1, 2 | PNG gate needs a new dependency or browser; text and ANSI gate works now |
| Spec | RR 43 and 57 stacked-block choice pending O-1; RR 61 self-contradiction | 04 section 5 | a deliberate spec edit accompanies layout phases |

Key findings carried from the research, with exclusions: the per-finding map (2.4), colour depth (2.1), live-path trace (2.2), test and golden pins (2.3), Q7 measurement (2.3), environment (2.5) and every contradiction (2.6) are reflected above. Excluded with rationale: the 01 inference on slate and muted collapse (superseded by 04); the per-test line-by-line P0 to P5 phase table in 03 section 6 and the web research files (`web-01`, `web-02`), which belong to the options and phasing sections of the report, not to current state.
