# Technical Research Report: Observer visual-parity redesign (issue #606)

**Date:** 2026-11-17
**Depth:** Standard
**Research files:** 5 codebase + 2 web research
**Scope:** src/superclaude/cli/observe/, tests/observe/, .dev/issues/409/bmad/spec-orca-observer/, .dev/issues/409/visual-parity/, the installed Zellij 0.44.2 setup

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target State](#3-target-state)
4. [Gap Analysis](#4-gap-analysis)
5. [External Research Findings](#5-external-research-findings)
6. [Options Analysis](#6-options-analysis)
7. [Recommendation](#7-recommendation)
8. [Implementation Plan](#8-implementation-plan)
9. [Open Questions](#9-open-questions)
10. [Evidence Trail](#10-evidence-trail)

**Abbreviations used in this report** (all paths absolute; `TASK` = `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800`)

| Short form | Meaning | Full path |
|---|---|---|
| FIND | Merged findings M-01 to M-18, guards, divergences, open items | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/merged/FINDINGS.md` |
| RR (with a line number, "RR 43") | The observer rendering rules spec | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` |
| R01 to R05 (also "research file 01" to "05") | Codebase research files 01 to 05 | `TASK/research/01-render-view-terminal-pipeline.md`, `TASK/research/02-live-screen-commands-export.md`, `TASK/research/03-tests-goldens-fixtures.md`, `TASK/research/04-spec-mockups-and-findings.md`, `TASK/research/05-zellij-and-render-harness-environment.md` |
| W01, W02 (also web-01, web-02) | Web research files | `TASK/research/web-01-rich-composition-and-colour.md`, `TASK/research/web-02-zellij-and-terminal-capture.md` |
| GAPS row N | Row N of the research gaps and questions register | `TASK/gaps-and-questions.md` |
| synth-05 | The implementation-plan synthesis, which is Section 8 of this report | `TASK/synthesis/synth-05-implementation-plan.md` |
| OBS | The observer package | `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/` |

**Severity words.** Section 4 uses Critical, Important and Minor (scale in the Section 4 header). Sections 1.3 and 8.10 quote FIND, which says High, Medium (Med) and Low; mapping: FIND High = Critical here, FIND Med = Important, FIND Low = Minor.

---

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

Source of the list: `FIND`; each item was re-checked against code and `RR` by research file 04 (section 5). Severity as stated in FIND (High, Med, Low); Section 4 calls these Critical, Important and Minor (High = Critical).

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
| `_columns` | three layouts by width class; `full` has 11 columns (`line` 6 and `short` 5, all counting the 2-cell marker column) and uses exactly 160 cells at 160 (2+114+22+12+10 separators), so a 2-cell border needs the elastic `flags` column to give up cells; `line` and `short` have no workerState/dispatchStatus column; `line` id width `min(width-64, 60)` (source of M-17 band at 116) | 155-230 (:159-192, :193-213, :214-230) |
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

Probe (read-only; first run in research file 01 line 173, re-run in this fix cycle on 2026-11-17 with identical output): `uv run python -I -B -c '<code>' <depth>` run once per depth in a fresh process, where the code builds `Console(file=io.StringIO(), width=40, color_system=<depth>, highlight=False, markup=False, emoji=False)`, prints `Text("x", style="bold #ff8800")` and prints `repr(console.file.getvalue())`. **Caveat 1, one process per depth:** Rich caches a Style's ANSI codes on the Style object, so when the three depths run in one process on the same `Text`/Style (re-measured), `256` and `truecolor` also print `\x1b[1;91m`, the `standard` result; the table below is only valid with one process per depth. **Caveat 2, `auto`:** it resolves to `None` for a `StringIO` file (no colour), so it says nothing about a real terminal.

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

Probe (read-only; first run in research file 02 section 2, re-run in this fix cycle on 2026-11-17 with the same output; one process per `NO_COLOR` value): build `Console(file=io.StringIO(), width=40, height=10, color_system=None if no_color else "standard", no_color=no_color, highlight=False, markup=False, emoji=False, record=True)` (the arguments `make_console` passes, terminal.py:110-125, plus `record=True`), print `Text("hello", style="bold red")`, then read `console.file.getvalue()`, `console.export_text()` and `console.export_text(styles=True)`. **Caveat, call order:** `export_text()` clears the recording buffer by default, so calling it before `export_text(styles=True)` on the same console leaves `styles=True` with an empty string (re-measured: `export_text()` gave `'hello\n'`, then `styles=True` gave `''`); read `styles=True` first or use a fresh console per read. The table's three rows were taken from separate fresh consoles.

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
- **Fixture text** (synthetic, 222 characters; research file 03 line 171): `Approve plan .dev/tasks/to-do/example-plan-20261117/example-plan-20261117.md ? files: src/superclaude/cli/observe/render.py tests/observe/test_render.py hash ` followed by `"0123456789abcdef" * 4` (64 hex characters). Built with `r3_rows([("w-001", ASK)])` and `r3_screen(FakeClock(), rows, 0, width, height=70)` from `tests/observe/test_render.py:853-887` (link on, one question selected). Re-measured in this fix cycle (read-only `uv run python -I -B -c` probe; desk text = the lines between the `DECISION DESK` title plus one and the line starting `dispatchId:`): width 160 gives 2 desk text lines of 157 and 64 cells; width 116 gives 3 lines of 85, 71 and 64 cells; width 80 gives 3 lines of 78, 78 and 64 cells; the hash is on the last line, alone and whole, at all three widths.
- Measured with that fixture: at 160 the desk text is 2 lines, at 116 and 80 it is 3 lines, and the hash is whole on its own line at all three widths; the list line is cut with `...` before the hash. A single token longer than the width (about 140 to 165 characters) is hard-split at the width with no marker and no regard for `/`.
- Desk lines at 80 columns for that fixture are 78, 78 and 64 cells (gaps row 45 corrects a "exactly the width" statement). An earlier research note that a hash in the question gives exactly 4 desk lines (`DESK_TEXT_LINES`) did not reproduce and is withdrawn: one hash in the fixture above gives 2 or 3 lines; the 4-line cap (with a trailing `...`) is reached only by a longer ask (for example the `"word " * 200` case pinned at test_render.py:958-967). The `resource.worktreeId: <hash>` field printed as label then `  <hash>` (66 cells).
- No existing test runs wide characters, a hash or a long path through `session_fields` (render.py:347-353).

### 2.4 Mockups and spec versus current output

**Mockup colour decode (all nine `.ansi` files; 24-bit foreground only, no background code, no 256-colour or 16-colour code, no dim, italic, underline or reverse)**

| Role | RGB | Used for | 16-colour index | 256 index |
|---|---|---|---|---|
| base | 225,233,238 | body text, padding | 15 | 189 |
| muted | 165,182,194 | freshness line, keys hint, `Affected:`, footer caveat | 7 | 145 |
| slate | 82,108,128 | secondary pane borders, rules, secondary titles, empty bar fill | 8 | 60 |
| amber | 250,178,25 | attention panes (heavy frame), desk question text (list question text is base bold), ages, `SYNTHETIC · READ ONLY` badge, big count digit | 11 | 214 |
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
| ledger 160 | 4 header lines, gap notice, title, 11-column table (marker + 10 named columns, `_columns` render.py:166-178) with heading and rule, `39/54 shown +15 more`, one footer line | no colour, panes, tiles; one footer line instead of rule plus two |
| ledger 116 | 5 header lines, 6-column form (marker + `kind`, `dispatchId`, `liveness`, `age`, `flags`; render.py:197-204) without heading, two-line footer | M-10, M-17, no panes |
| ledger 80 | header wraps (`as of` alone), counts cut `runs seen>`, 5-column rows (marker + `kind`, `dispatchId`, `age`, `flags`; render.py:216-222), key list cut `e exp>` | M-10, M-11, M-13, M-16 |
| questions 160 / 116 / 80 | one stacked block: title, run, state, disclosure, counts, caveat, rows, retention, then worker table; disclosure wraps to two lines at 116 and 80; `n/p` / `question` split at 116 | M-03, M-05, M-07, M-14, M-15, M-16 |
| desk 160 / 116 / 80 | bare `DECISION DESK` block under the list with 9 `label: value` lines, then the worker table repeated | M-04, M-12, M-18 |

Spec lines (verified against `RR`, 107 lines; FIND citations all resolved): the two O-1 reversal targets are RR 43 and RR 57 ("one stacked block"); lines that change if the fix proceeds are 17 (badge), 25 (pane glyph forms), 41 and 61 (RETAIN CONTEXT), 43 and 57 (columns), 70 (muting becomes implemented). Spec guards to keep: RR 20 and 32 (gap notice and COUNTS wording), 31 (`nextAction.kind` verbatim), 47 and 49 (count and disclosure verbatim), 50 (glyph and age format), 57 (desk line order), AC-9 T26-T28 (no SGR in NO_COLOR, no ESC in exports, no blink). RR 37-41 and 60-61 describe the two-column layout, `SEEN IS NOT RESOLVED` tile and `RETAIN CONTEXT` as the layout, but RR 43 says only the stacked block was built; treat them as design reference. RR 61 requires two 80-column invariant lines the output lacks and one of them contradicts RR 42 (AD-7): spec self-contradiction (CODE-CONTRADICTED).

Further detail from 04 (sections 1, 7 and 8; read from the files, not run): (a) `render_current.py` mixes data modes: the ledger is fixture-mode data (`160/ledger.txt:1` reads `mode=fixture`) while the questions and desk screens are live-mode data (`160/questions.txt:1` reads `mode=live`); it does not capture NO_COLOR, `--ascii`, the live observer, error states, a hash-bearing question, or any height other than 50. (b) RR 17 header contract: line 1 is `ORCA OBSERVER  mode=...  scope=...  as of ...`, a fixture reads `SYNTHETIC FIXTURE <variant>, not Orca data`, the contract also names `one Run only: <runId>`, and it has no READ ONLY badge. (c) RR 26: the inspector and export paths show the full question text untruncated, while the Decision Desk caps it at `DESK_TEXT_LINES = 4` lines (view.py:99) and cuts the fourth with `...`. (d) RR 21 key list: Up/Down, j/k, Enter, Esc, `/`, h, m, e, q, plus n/p with the link switch; there is no `r` key.

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

**Proving commands for the Zellij facts** (read-only; first run in research file 05 lines 11-12, re-run in this fix cycle on 2026-11-17 with the same output; run from `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`; no Zellij session is started by any of them):

| Fact | Command | Observed output |
|---|---|---|
| Binary path | `command -v zellij` | `/usr/local/bin/zellij` |
| Version 0.44.2 | `zellij --version` | `zellij 0.44.2` |
| Config well defined, config dir | `zellij setup --check` | `[Version]: "0.44.2"`, `[CONFIG DIR]: "/home/coder/.config/zellij"`, `[CONFIG FILE]: Well defined.`, `[LAYOUT DIR]: "/home/coder/.config/zellij/layouts"`, `[DEFAULT EDITOR]: Not set` |
| Config, layout and theme line counts and directives | `wc -l` and `grep -n` on the files under `/home/coder/.config/zellij/` | read in research file 05 sections 1.2 to 1.5 (53, 58, 265 and 252 lines; directives at the cited line numbers); not re-run |
| Help-text features | `zellij --help`, `zellij run --help`, `zellij action dump-screen --help` | read in research file 05 section 1.6; not re-run |

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

**Proving commands for the tool table** (read-only; first run in research file 05 section 2, re-run in this fix cycle on 2026-11-17 from the repo root; `uv run python -I -c` keeps the working directory off `sys.path`):

| Fact | Command | Observed output |
|---|---|---|
| Python 3.10.20, uv 0.11.8 | `uv run python --version`; `uv --version` | `Python 3.10.20`; `uv 0.11.8 (x86_64-unknown-linux-musl)` |
| Rich 15.0.0 | `uv run python -I -c "import importlib.metadata as m; print(m.version('rich'))"` | `15.0.0` |
| PIL, cairosvg, pyte, playwright, fontTools absent | `uv run python -I -c "import PIL"` (and the same for each module) | `ModuleNotFoundError: No module named 'PIL'` (and `'cairosvg'`, `'pyte'`, `'playwright'`, `'fontTools'`) |
| chromium, chromium-browser, google-chrome, rsvg-convert, inkscape, convert, magick, freeze, termshot, aha, ansi2html, unzip missing | `command -v <name>` for each | no path printed for any of the twelve |
| node 24 and npx present | `command -v node`; `command -v npx`; `node --version` | `/usr/local/bin/node`; `/usr/local/bin/npx`; `v24.22.2` |
| No cached Playwright browsers | `ls /home/coder/.cache/ms-playwright` | `ls: cannot access '/home/coder/.cache/ms-playwright': No such file or directory` |
| DejaVu Sans Mono installed | `fc-list "DejaVu Sans Mono"` | four files under `/usr/share/fonts/truetype/dejavu/` (Book, Oblique, Bold, BoldOblique), including `DejaVuSansMono.ttf` |
| Rich `Console` has `export_html`, `export_svg`, `export_text`, `save_*` | `dir(Console)` through `uv run python -I -c` | read in research file 05 section 2; not re-run |

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

## 3. Target State

### 3.1 What parity means

| Aspect | Target | Evidence |
|---|---|---|
| Reference design | Nine mockups: three screens (signal-bridge, agent-focus-attention-ledger, decision-desk) at three widths (160, 116, 80), each as `.png`, `.ansi` and `.txt`; every file is exactly 160, 116 or 80 cells wide; frame height 48 lines at 160 and 42 at 116 and 80 | 04 section 4 [CODE-VERIFIED] |
| What must match | Chrome: colour and weight, titled boxed panes, two-column composition, count tile, READ ONLY badge, footer rule. Not data: AD-1 to AD-7 stay accepted divergences | 04 sections 5 and 6 |
| Pre-fix baseline | `inputs/current/{160,116,80}/` (ledger, questions, desk) holds 0 ESC bytes in all nine `ansi-*.txt` files; treat as the before picture | 04 section 7, 05 section 4 [CODE-VERIFIED] |
| Primary mode | ANSI-styled output; NO_COLOR and `--ascii` stay fully working | task constraints, 01 section 7 |

### 3.2 Colour roles the mockups use and what survives at 16 colours

The mockups use 24-bit foreground colour only (`ESC[0;38;2;R;G;Bm`, bold as `ESC[0;1;38;2;R;G;Bm`); there is no background code, no 256-colour code, no dim, italic, underline or reverse [CODE-VERIFIED, 04 section 2]. `make_console` pins Rich to `"standard"` (16 colours) unless NO_COLOR is set (terminal.py:121) [CODE-VERIFIED], so Rich downgrades every RGB style.

| Role | Mockup RGB | Used for (verified from segment text) | Rich 15.0.0 downgrade: standard-16 index | 256 index |
|---|---|---|---|---|
| base | 225,233,238 | body text, padding, question rows in the 160 ledger | 15 | 189 |
| muted | 165,182,194 | clock line, `Affected:` lines, keys hint, `7/7 lines shown`, footer caveat | 7 | 145 |
| slate | 82,108,128 | secondary pane borders (rounded), rules, secondary titles, empty bar fill | 8 | 60 |
| amber | 250,178,25 | attention frame (heavy), its title, desk question text and ages (bold; question rows in the 160 ledger are base), `SYNTHETIC / READ ONLY` badge, tile digit | 11 | 214 |
| cyan | 112,205,226 | screen title with the diamond glyph (bold), count-tile frame, running sessions | 14 | 80 |
| green | 139,215,175 | settled sessions | 7 | 115 |
| red | 240,141,150 | failed session | 7 | 210 |
| violet | 194,173,242 | frozen, `POLICY FROZEN` count | 7 | 147 |
| selected | none | no selected-row colour or reverse video exists in any mockup [UNVERIFIED how selection should look] | n/a | n/a |

Target consequence (Q4, G-2) [CODE-VERIFIED measurement, derived consequence]: at 16 colours base (15), slate (8), cyan (14) and amber (11) stay distinct, but muted, green, red and violet all collapse to index 7. State colour (M-09) therefore cannot be the only carrier of meaning: the theme needs explicit per-depth roles built from named ANSI colours (research examples: green, red, magenta, cyan, yellow, bright_black) and the raw state words must stay printed (RR 31 and 71). The exact 16-colour table is a design choice that is not yet in code; the web research [external context: https://rich.readthedocs.io/en/stable/appendix/colors.html] agrees that the first 16 colours are set by the user's terminal theme and that nearby hues collapse.

### 3.3 Target layout by width

All two-column and pane rows below depend on owner decision O-1 (reversing RR 43 and RR 57, "one stacked block"). Until O-1 is decided, the code builds only the stacked block (render.py:359-387) [CODE-VERIFIED]. Column pairs are measured from the mockups (1-cell left margin, 2-cell gap, 1-cell right margin: 1+114+2+42+1 = 160 and 1+70+2+42+1 = 116) [CODE-VERIFIED against mockup `.txt`, 04 section 4].

| Element | 160 (class `full`) | 116 (class `line`) | 80 (class `short`, 80 to 115) |
|---|---|---|---|
| Title bar | Title on the left, READ ONLY badge right-aligned (mockup line 2); RR 17 must change (M-13, OPEN-3) | same | same; the badge must not push `as of <time>` onto its own line as header1 does today (render.py:410, measured) |
| COUNTS strip | numbers only, no bars, no health name (RR 20, AD-1, AD-2); two lines | same | same; a cut may only drop a whole low-priority token with a visible `>`, never cut inside a token (M-16) |
| Questions screen | Attention pane 114 wide (title `COORDINATOR QUESTIONS`, not the mockup's `OPEN HUMAN QUESTIONS`) beside a 42-wide right column: count tile over RETAIN CONTEXT pane | Attention pane 70 wide beside the same 42-wide right column (RR 60) | Single column of panes 78 wide (74 usable); the mockup has no tile and no RETAIN CONTEXT pane here |
| Count tile | Prominent count in the tile; the text `seen, not resolved: n` with its `closed by evidence` clause stays as text for NO_COLOR, ASCII, 80 columns and the record (M-05) | same | text form only |
| Decision Desk | Question leads in the attention pane; evidence for the ONE linked session as aligned label and value rows in the second pane (mockup 76 + 80); no requester, owner, "Affected" or mapped trees (AD-4) | Question full width above two panes (mockup 66 + 46) | Three stacked 78-wide panes (mockup) |
| Ledger | 11-column table with heading and rule (exists); one row per worker, no `stage` column (RR 30, AD-3) | line form (kind, id, verdict, age, flags) with a column heading (M-10); no wide blank band after the id (M-17, optional) | short form (kind, id, age, flags) with a column heading (M-10) |
| Footer | Key list, never cut; key pairs such as `n/p question` never split; rule above the footer (mockup line 46) (M-11, M-15) | same | same; key list must not end in `>` (test_f08 pins this) |
| Selected question | Glyph `▸` (`@` in ASCII) plus a role style, never `>` or `*` (RR 50, M-18) | same | same |
| Narrow (below 80) | Diagnostic text unchanged | | |

Width classes: the code has FOUR (`full` at 160 or more, `line` 116 to 159, `short` 80 to 115, `narrow` below 80; terminal.py:63-70). [CODE-CONTRADICTED: the task prompt and `research-notes.md:24` name only full, line and narrow.]

### 3.4 Target by output mode

| Mode | Switch (terminal.py) | Target behaviour | Pinned by |
|---|---|---|---|
| ANSI-styled (primary) | `no_color` false; `color_system` today fixed `"standard"` (:121) | Roles from 3.2 applied by the renderer as `Text` spans after `wrap` and `clip` (those return plain `str`); bold on titles; no blink (SGR 5 or 6), no mouse mode, no background colour | test_render.py:177-185 (no blink); keys.py enables only cbreak [CODE-VERIFIED] |
| NO_COLOR | `bool(env.get("NO_COLOR"))` (:83) gives `color_system=None` and `no_color=True` | Zero ESC bytes in any output; hierarchy carried by text, glyphs and frame characters; text identical to styled output with SGR stripped. Under this console bold is dropped together with colour [CODE-VERIFIED probe]. Rich's own NO_COLOR keeps bold and dim [external context: https://rich.readthedocs.io/en/stable/console.html]; the stricter behaviour here is a project choice, not a Rich rule | test_render.py:985-987, test_terminal.py:41-51 |
| ASCII | `--ascii` or a non-UTF-8 stdout (:84-85) | Every printed byte and line is ASCII; frames use `+`, `-`, `\|`; selected marker `@`; truncation `>`; rule `-`. `safe_box=policy.ascii` does NOT turn a Rich `Panel` into ASCII borders (probe: identical `╭─╮│` output with `safe_box` True and False), so a Rich frame needs an explicit `box=rich.box.ASCII` and a hand-built frame needs new `GLYPHS` entries. [CODE-CONTRADICTED: the assumption that `safe_box` gives ASCII panes.] With only `+-\|` the heavy (attention) versus rounded (secondary) distinction is lost, so the attention role must come from title text and colour [derived] | test_render.py:263, :591, :903; test_commands.py:131 |
| Colour and ASCII together | independent booleans | Any combination works; width class independent of both | resolve_policy (:73-92) |

### 3.5 Width and height budgets

| Budget | Target rule | Evidence |
|---|---|---|
| Width, every line | `cell_len(line) <= policy.width` at 160, 116 and 80 in every mode; widths are measured in cells, not characters; styling layered on afterwards so spans cannot misalign (Rich `Span` offsets are character indexes) | test_render.py:73-77; 01 section 8.2 [CODE-VERIFIED] |
| Frame cost, width | inner width = pane width minus 2 (border) or minus 4 (border plus 1-cell padding); every `wrap` and `clip` feeding a pane receives the inner width. At 80 the mockup frame is 78 wide with 74 usable cells | 01 section 8.2 item 3; 04 section 8 |
| Full table at 160 | The 11-column table uses all 160 cells (2 + 114 + 22 + 12 + 10 separators). A framed table needs the elastic `flags` column (12 cells) to give up 2 to 4 cells. The "153 cells" figure in FIND M-06 is [UNVERIFIED] and not on RR line 30; use 160 | 01 section 4.3 |
| Height, every screen | `len(screen_lines) <= policy.height` at heights 40, 44 (RR 13, the 44-row contract), 24, 12 (the golden heights) and `MIN_ROWS = 8` | 02 section 9.4, 03 section 4a |
| Frame cost, height | Each pane adds 2 rows (top and bottom border). Every added row must be counted inside `screen_lines`' `head`, `reserved` (render.py:499-501), `ledger_fixed` (:438-440) and `spare` (:447-457), never added after the budget is computed | 01 sections 4.7 and 8.2 |
| Why it matters | There is no final `lines[:height]` clamp on the normal screen and one ledger row is always forced (render.py:502). On the live screen `Live(screen=True)` wraps the group in `Screen`, which pads each row to the width and cuts rows past the console height from the bottom with no ellipsis, so the footer key list and the `shown x/y` line are lost first (measured: at height 38 the last two source lines are gone). At base fixture and height 40 every width already fills all 40 rows, so any added row is a lost ledger row | 02 section 9 [CODE-VERIFIED]; [external context: https://rich.readthedocs.io/en/stable/live.html and rich/screen.py v15.0.0 agree that rows beyond the height are cropped under `screen=True`] |
| Mockup versus harness height | Mockup frames are 48 lines at 160 and 42 at 116 and 80; `render_current.py` fixes `HEIGHT = 50` (:38). The render gate compares like with like only if heights match, or the mismatch is recorded as accepted | 04 section 4, 05 section 4, gaps row 14 [CODE-VERIFIED] |
| Zellij chrome | The installed default layout spends 3 rows on bars (tab bar 1 row, status bar 2 rows, default.kdl lines 48-58); a 44-row contract leaves 41 before the pane frame, whose cost was not measured [UNVERIFIED] | 05 section 1.3; derived arithmetic |

### 3.6 Testable success criteria (each is pass or fail)

| ID | Criterion | How it is tested | Basis |
|---|---|---|---|
| SC-1 | Every `screen_lines` line and every printed line has `cell_len <= width` at 160, 116 and 80, in colour, NO_COLOR and ASCII | extend test_render.py:68-77 and :460-470; printed lines compared after stripping SGR (a raw styled line measures too wide: `cell_len` of an escape run counts its printable part, 16 cells for one SGR example) | 01 section 3 |
| SC-2 | NO_COLOR: zero ESC bytes in printed output at all three widths, all screens | test_render.py:985-987 kept; test_terminal.py:41-51 kept | 03 section 3 |
| SC-3 | ASCII: printed bytes and lines are `.isascii()`; panes use `+`, `-`, `\|`; no `?` stands in for a border | test_render.py:263, :591, :903 plus a new pane case | G-1 |
| SC-4 | No blink: SGR parameters 5 and 6 absent in colour and NO_COLOR output at every width; no mouse sequences | test_render.py:177-185 kept | 02 gaps, 03 section 3 |
| SC-5 | Colour on: ANSI present in the styled stream; with SGR stripped it equals the NO_COLOR output; `screen_lines` equal for both | rewrite (not delete) test_render.py:250-259: strip SGR, keep determinism and the `screen_lines` equality | 03 section 3 |
| SC-6 | At the 16-colour depth the four state roles (running, settled, failed, frozen) produce four pairwise distinct SGR codes; every value in the minimum `STATE_ROLE` table (step 1.4: the `(field, value)` keys for `running`, `alive`, `live`, `succeeded`, `completed` and `failed`, plus the `FROZEN_MARKER` flag held as `FROZEN_ROLE`) is coloured with its role, every other value is neutral, and the state word is always printed | `T/test_theme.py` (distinct codes at `standard`, non-empty table) and the `.ansi` census of RB-10; the table is owner decision D-7 with the stated default | 04 section 3 |
| SC-7 | The record and JSON snapshot are byte-identical to today, and contain no question text | test_export.py:307-332, test_snapshot_schema.py:457-479, golden `record_text` and `snapshot_json` keys; add a canary that the new fixture's hash is absent from both | 02 section 5 |
| SC-8 | Required text survives: counts text, disclosure, gap notice, `reason unknown` on every question line, retention sentence, PARTIAL literal never cut | flat-text tests (test_render.py:192, :202, :437, :679) | 03 section 1 |
| SC-9 | Height: `len(screen_lines) <= policy.height` at 40, 44, 24, 12 and 8 (or the too-small diagnostic); footer stays in the last 3 or 4 lines | new matrix test; test_render.py:748, test_inspector_scroll.py:36-72 kept | 02 section 9.4 |
| SC-10 | A 64-hex hash in a Decision Desk question appears whole on one line at 160, 116 and 80 inside the framed desk; the text loses nothing when under the 4-line cap; paths longer than the inner width hard-split and lose nothing | new `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk` (03 section 5d), parametrized over widths; synthetic hash only | 03 section 5 |
| SC-11 | At 80 columns the key list is not cut: no line ends in `>` and contains `exp`; the full list is present | test_render.py:748 (test_f08) generalised to questions-off | M-11 |
| SC-12 | At 80 columns no COUNTS token is cut inside its text | new assertion on `counts_lines`; `>` only after a whole token | M-16 |
| SC-13 | A column heading line is present at 116 and 80 when at least one row is visible | new test; today only at 160 (render.py:497) | M-10 |
| SC-14 | Mockup parity score from a fixed-rubric reviewer meets a threshold | The rubric is defined in Section 8.4 (RB-01 to RB-23, each with a pass or fail anchor and a checker) and the threshold is the phase-closure rule of 8.5 (every High and Medium row in scope passes in the last iteration; Low rows pass or are logged as deferred); the raw material is 04 sections 2 and 4 (eight roles, pane geometry); see Section 4 harness row | Q3 |
| SC-15 | Live path: the styled stream captured under a pty (or a `force_terminal` console seam) contains SGR when colour is on, none under NO_COLOR, and the footer is not cropped at the gated heights | pexpect route B or a seam into `LiveScreen` (route A); no test references `LiveScreen` today | 02 section 9.3 |
| SC-16 | Gate lines intact: the two `QUESTION_*_PASSED` assignments stay single-line at column 0 with their comments, and `release-gates.md` and `Task 18` stay in commands.py | test_commands.py:747-756 and :762-772 (the functions end at 756 and 772) | 02 section 4 |
| SC-17 | Source guards: render.py contains no `Console(`, `sorted(`, `.sort(`, `from_markup` or adapter, collector or parse import; only terminal.py contains `Console(`, `NO_COLOR`, `COLUMNS`; export.py imports no render or rich | test_render.py:396-404, test_terminal.py:181-198, test_export.py:238-243 | 03 section 6 |
| SC-18 | Worker text with markup or escape characters stays inert: `[bold]x[/bold]` prints literally, no ESC, C1 or format characters in NO_COLOR output | test_render.py:140-174, :970-982 | 01 section 2 |
| SC-19 | Questions-off screens: either byte-identical to the T47 golden, or the golden is re-baselined by an explicit owner decision in the same commit as the change | test_render.py:611-624 and test_linkoff_screen_reference.py:72-75 | G-A, Section 4 |

### 3.7 Constraints that must be preserved

| Constraint | What it means | Code anchor | How the target preserves it |
|---|---|---|---|
| G-1 (RR 25) | New panes emit `+`, `-`, `\|` under `--ascii`, never `?` borders | GLYPHS has three names only (terminal.py:30-34); `ascii_safe` turns any non-ASCII into `?` (:133-135) | New box glyphs added through `GLYPHS` and `glyph()` with ASCII forms, never as string literals; Rich frames pass an explicit ASCII box |
| G-2 | Theme stays distinct at the real colour depth; NO_COLOR stays `color_system=None` | terminal.py:121; no COLORTERM or TERM detection exists | Per-depth role table (3.2); NO_COLOR keeps `None` |
| AD-1 | `8 owners / 80 sessions / 80 mapped trees` header not built | RR 20 | The real COUNTS strip stays |
| AD-2 | No SIGNALS bars; no SETTLED, UNKNOWN, STALE tiles | RR 20, 93; view.py:947-949 | Tokens stay `unavailable (no source)` |
| AD-3 | One row per worker with raw fields; no two-line register rows, no prose lifecycle, no `stage` column | RR 30, 31; render.py:155-230 | Ledger keeps its raw-field columns |
| AD-4 | No requester, owner, `Affected:` list or affected-session count; one linked session only | RR 57, 91; view.py:87-90, 814-874 | Desk right pane shows the nine session fields of the linked session and the worktree note only |
| AD-5 | Different key map; no `tab pane`; no multi-pane focus; ledger stays under the desk | RR 13, 21, 39; view.py:78-83, 105 | One focus at a time (list, filter or inspector) |
| AD-6 | No `workerState` column at 80; optional at 116 | RR 33; render.py:193-229 | Short and line forms unchanged in content |
| AD-7 | Mockup 80-column "Questions stay until explicit resolution." and the forced focused card not adopted | RR 42, 61 | Retention wording stays as RR 42; RR 61 reworded in the same spec change |
| Question text screen-only | Payload question text exists only on screen, including the stdout of `--once --width`; never in the record, the snapshot, or any file | `export._question_lines` writes `q.text` (subject), never `q.shown` or `q.ask` (export.py:103-111); `_questions_dict` writes ids, times and counts only (:158-180) [CODE-VERIFIED] | New desk and tile code reads `q.shown` and `desk.ask` in render.py only and adds no `View` field that `record_text` or `snapshot_dict` reads |
| Records and JSON snapshot content | `record_text` and `snapshot_json` byte-identical; `SCHEMA_VERSION = 1`; `--once` without `--width` prints `record_text` with no ESC | export.py:71-118, :183-224; commands.py:243-244 | Changes of M-05, M-08, M-13, M-14 are render-only; `view.header1` (view.py:914-921) and `counts_line` (view.py:761) stay |
| Read-only | No key reaches Orca; no new write path | `Effect` is NONE, EXPORT or QUIT (view.py:1066-1071); `write_atomic` called only at commands.py:216 and :327 | Presentation work adds no collector call or file write |
| Real data only | No invented owners, requester, mapped trees, affected sessions | RR 57, 91; AD-1, AD-4 | Pane content comes from fields already on `View` |
| No blinking, no mouse | | keys.py:61 (cbreak only); no `mouse` or `blink` text in `observe/*.py` [CODE-VERIFIED] | Theme uses no blink attribute |
| Widths 160, 116, 80 and narrow diagnostic | | terminal.py:21-24, 63-70 | SC-1, SC-9 |
| PR target | `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3` | CLAUDE.md fork rule | Process constraint, not a code constraint |

### 3.8 Evidence-supported posture per research question

| Q | Posture the evidence supports | Strength |
|---|---|---|
| Q1 composition | Keep `screen_lines` (plain `list[str]`) as the source of truth and add styling as a render-only layer producing one `Text` per line; hand-built frame helper next to `_pad` and `_cell` using new `GLYPHS` entries. Rich `Panel`, `Table`, `Columns` and `Layout` each break a pinned rule: `len(group.renderables) == len(screen_lines)` (test_render.py:399), list-based height budgets, the `>` and `...` cut markers, and the fixed-width discipline. The web research [external context: https://rich.readthedocs.io/en/stable/text.html] independently recommends a thin pure style layer over `Text` spans | 01, 03, web-01 agree |
| Q2 phases | Research 03 section 6 groups the work as P0 tests only; P1 style-only (touches 1 test and 15 `printed_*` golden values; leaves `golden_questions_linkoff.json` and all `lines_*`); P2 text; P3 width-gated 160 layout; P4 boxed panes (touches most whole-line tests and both goldens); P5 optional Rich renderables. That is research 03's own grouping, not the plan. The phase scheme of record is P0 to P7 of Section 8 (synth-05): P0 harness, rubric, baseline and pinning tests; P1 style only (the 15 `printed_*` values are kept plain by an SGR strip in `release1_surface.py` `_printed`, so no golden is regenerated); P2 text and budget fixes; P3 single-column titled frames; P4 two-column questions screen with count tile and RETAIN CONTEXT pane; P5 two-column Decision Desk; P6 ledger panes; P7 spec reconciliation, final gate and PR. Each golden-changing phase (P2, P3, P4, P6) needs the owner's re-baseline decision (D-2) | 03 section 6; synth-05 |
| Q3 harness | Text and ANSI assertions work offline today; a PNG needs a rasteriser that is not installed (no PIL, cairosvg, pyte, playwright, browser, rsvg-convert or ImageMagick; Rich 15.0.0 and node 24 present). Rich SVG export is browser-only in practice [external context: https://github.com/Textualize/rich/issues/2153]. The Playwright MCP browser exists only inside the Claude session | 05, web-02 |
| Q4 colour depth | Today fixed `"standard"`; `color_system="auto"` reads COLORTERM then TERM [external context: https://rich.readthedocs.io/en/stable/console.html] but gives no colour on a non-terminal file; 16-colour roles must be explicit | 01, 04, web-01 |
| Q5 live versus one-shot | Live keeps SGR; `--once --width` uses `export_text()` (styles dropped, commands.py:242); `export_text(styles=True)` ignores NO_COLOR and the down-conversion; the NO_COLOR-correct styled route is `console.file.getvalue()` of the `make_console` StringIO console | 02 (probe-verified) |
| Q6 Zellij | Not a dependency of the observer or of the render gate; optional presentation environment | 05, web-02 (see Section 4) |
| Q7 hash | Fits whole at 160, 116 and 80 today (measured); paths hard-split without a marker; a frame narrows the width, so the test must exist before the layout phase | 01, 03 |

Section 3 sources: 01 sections 1 to 8, 02 sections 1 to 9, 03 sections 1 to 6, 04 sections 2 to 8, 05 sections 1 to 7, web-01, web-02, `gaps-and-questions.md`.

## 4. Gap Analysis

**Severity scale used in Section 4:** **Critical** = FINDINGS "High" or a C8 defect (spec-required behaviour that is not wired); **Important** = FINDINGS "Medium", a decision that gates other rows, or a Gate 1 "Important" gap; **Minor** = FINDINGS "Low" or a note. Gate 1 found 0 Critical research gaps; Critical here marks product gaps, not research gaps. A **C8 defect** is an in-scope capability that the spec names as required but the code does not wire at its runtime entrypoint, with no cited scope decision moving it to future work (full wording in 4.1).

### 4.1 Gap table

Severity follows the scale in the Section 4 header above (FINDINGS High = Critical, Med = Important, Low = Minor). FINDINGS severity is kept in Notes. Rows flagged **OPEN** are undecided. Rows flagged **C8 DEFECT** are unwired in-scope capabilities: the spec names the behaviour as required, the code does not wire it at its runtime entrypoint, and no cited scope decision moves it to future work, so each is a defect with a linked remediation need (Section 4.2) and is not downgraded. Fix locations are in `render.py` unless stated.

#### 4.1a Merged findings M-01 to M-18

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| M-01 No colour or weight anywhere | `render()` builds one unstyled `Text(line, no_wrap=True, overflow="crop")` per line (render.py:528); `View` and `screen_lines` are strings only (view.py:303-339; render.py:390-521); 0 ESC bytes in all nine `ansi-*.txt` [CODE-VERIFIED] | Eight role colours plus bold (3.2) applied after wrap and clip; plain text identical in NO_COLOR, ASCII and exports | Critical | FIND High. Change points: render.py:524-531, terminal.py:110-125. Styled `printed()` captures gain ESC bytes, so test_render.py:250-259 must be rewritten, and the `printed_*` keys of `golden_release1_surface.json` stay plain only if `surface()` strips SGR in `release1_surface.py` `_printed` (lines 34-38); the plan does that (synth-05 step 1.6(c)) instead of regenerating the 15 values in the style-only phase (03 section 3 offered either route). Composition choice is Q1 |
| M-02 No boxed titled panes | Titles are plain wrapped strings (render.py:368, 333, 495, 410-412); GLYPHS has `selected`, `truncate`, `hrule` only (terminal.py:30-34) | Titled panes: heavy attention frame, rounded secondary frames, titles inset in the top border; ASCII `+-\|` | Critical | FIND High. Needs the G-1 row (box glyphs). Breaks whole-line and `startswith` tests: `DESK_TITLE in lines`, `GAP_NOTICE in lines`, `"/ab" in lines`, `startswith("dispatchId:")`, `endswith("reason unknown")`, the desk slice `desk[2:...]` (03 section 6, P4) |
| M-03 Questions screen has no two columns | One stacked block: title, run line, state, disclosure, counts, caveat, rows, retention (render.py:359-387); composed as `gap_part` (:433-486) | 160: 114 + 42; 116: 70 + 42; 80 stacked (3.3) | Critical | FIND High. **OPEN** (O-1). Spec edit to RR 43 (and 60, 61). Panel `spare` formula (:447-457) must count frame rows |
| M-04 Decision Desk stacked | `_desk_lines` returns a full-width list inserted at render.py:383 (:329-356); sized at :458-471; the ledger repeats below | 160 two columns, 116 question over two panes, 80 three stacked panes; real data only (AD-4) | Critical | FIND High. **OPEN** (O-1). RR 43 and 57 edits. 4-line text cap `DESK_TEXT_LINES` (view.py:99) interacts with a narrower pane |
| M-05 Count has no weight | `counts_line` string (view.py:761) wrapped at render.py:373; `record_text` writes the same string (export.py:99) | Render-only tile with a prominent count; the text form kept for NO_COLOR, ASCII, 80 columns and the record | Critical | FIND High. Do not change view.py:761. 04 cites render.py:374; the line is 373 [CODE-CONTRADICTED line cite]. Block glyphs measured 1 cell each; FINDINGS does not require a 5-row digit font. Tile data: `open_total`, `retained`, `window_full`, `evicted`, `state` (view.py:246-266) |
| M-06 No attention slot, observation pane or tiles | Gap notice, counts and ledger are separate `wrap` calls (render.py:409-414, 480-486, 495-512); the full table is exactly 160 cells | Attention slot and observation pane per mockup while keeping gap notice and COUNTS wording (RR 20, 32) | Important | FIND Med. The "153 cells" figure is [UNVERIFIED]; code gives 160. AD-1 and AD-2 items stay unbuilt |
| M-07 Caveats outweigh question rows | Order is title, run, state, disclosure, counts, caveat, then rows (render.py:368-376); age is part of `lead` text, no gutter (view.py:735-737, 756); disclosure wraps to 2 lines at 116 and 80 | Question rows lead; caveats grouped; per-question hierarchy with row emphasis and separation (RR 49 disclosure kept verbatim) | Important | FIND Med. **OPEN** (OPEN-1: Astra High versus Opus Medium; handled as Medium, gated) |
| M-08 Absent values not muted | Bare `unknown`, `unavailable (no source)` and `reason unknown` (render.py:319; view.py:100, 384, 635-637, 706, 744, 748, 761) are inside unstyled strings; `text_of` quotes a real `"unknown"` value (view.py:377-385) | Absent values muted, plain under NO_COLOR (RR 70) | Critical | **C8 DEFECT**: RR 70 already requires it; no mute path exists (render.py:528). FIND Med raised to Critical per C8. Remediation: RN-1. Hazard: token matching can hit worker-controlled free text |
| M-09 State values uncoloured | `workerState` and `dispatchStatus` cells exist only in the `full` layout (render.py:166-191); `_row_line` joins cells into one string (:233-243) | Green settled, red failed, violet frozen, cyan running; `nextAction.kind` stays verbatim and uncoloured (RR 31) | Important | FIND Med. Narrower than it reads: at 116 and 80 only the liveness verdict (`_verdict`, :151-152) can be coloured; desk fields via view.py:845-846. 16-colour collapse (3.2) means state words must stay printed |
| M-10 No column heading at 116 and 80 | Heading and rule only when `policy.width_class == "full" and view.visible_rows` (render.py:497-498, mirrored at :439); names `kind`, `dispatchId`, `liveness`, `age` exist in `_columns` (:203-204, 218-221) but are never printed | Heading line at 116 and 80 when rows are visible | Critical | **C8 DEFECT** (callee exists, entrypoint gated off). FIND Med, coordinator ruling R-1 = defect; no downgrade. Remediation: RN-2. FIND says `render()` holds the condition; it is in `screen_lines` [CODE-CONTRADICTED location, behaviour CODE-VERIFIED] |
| M-11 80-column key list cut, `q quit` lost | `_help_lines` clips when `view.questions is None` (render.py:304-308); measured `... m mark  e exp>` at 80; wraps when questions are on | Key list never cut (RR 21) | Critical | **C8 DEFECT** (wrap path exists, not used for questions-off). FIND Med. Remediation: RN-3. Changes questions-off goldens (G-A row) |
| M-12 Desk: question does not lead; evidence is an unaligned dump | Question text and nine `label: value` lines stacked, unstyled (render.py:339-353; view.py:843-853) | Question leads and is emphasised; evidence aligned | Important | FIND Med. RR 57 line order is a guard |
| M-13 No READ ONLY badge, no title split | `header1` is one string (view.py:914-921) wrapped at render.py:410; `as of` lands on its own line at 80; no `READ ONLY` text anywhere under `observe/` [CODE-VERIFIED absence] | Title left, READ ONLY badge right-aligned (RR 17 changes) | Important | FIND Med. **OPEN** (OPEN-3). Split inside render.py only: `record_text` (export.py:76) and `release1_surface.py:50` read `header1` |
| M-14 Supported facts scattered; no RETAIN CONTEXT | Run line, caveat, counts and retention sit in three places (view.py:794, 798, 761, 804; render.py:369, 373-374, 387) | One RETAIN CONTEXT group (RR 41 and 61 change) | Important | FIND Med. **OPEN** (OPEN-2: Opus Medium, Astra Low). Render-only regrouping |
| M-15 Footer key pair split; no rule | `wrap` breaks at the last single space (render.py:72-75), so `n/p` and `question` can separate (116 questions screen) | Wrap by double-space groups; rule above the footer | Minor | FIND Low (R-2). Fix: `_help_lines` (:304-308) and footer branches (:423-431, 514-520) |
| M-16 80-column counts cut inside a token | `counts_lines` clips into the remaining room (render.py:127-132); measured `runs seen>` and `cost un>` | Cut only whole low-priority tokens (RR 20 allows `>` on low-priority tokens) | Minor | FIND Low. Protected tokens already never cut |
| M-17 Wide blank band after the id | `id_width = min(width - ..., 60)` at 116 (render.py:195) and `width - (2+14+6+16+sep*4)` at 80 (:215); observed with 5-cell fixture ids only | No wide dead band; widths must not shift between refreshes (M-17) | Minor | FIND Low (optional). Observed only with short ids |
| M-18 Selected question is a glyph only | `mark = glyph("selected") + " "` (render.py:317; `_marker` :145-148) | Glyph plus a role style; never `>` or `*` (RR 50) | Minor | FIND Low. No mockup draws a selected row, so the look is [UNVERIFIED]; score against RR 50, not the mockup |

#### 4.1b Guards, architecture and cross-cutting gaps

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| G-1 Box glyphs and ASCII panes | GLYPHS holds three names; `ascii_safe` maps non-ASCII to `?`; `safe_box=policy.ascii` does not ASCII-ize a Rich `Panel` (probe, Rich 15.0.0) | New box glyphs in `GLYPHS` with `+ - \|` forms; Rich frames pass `box=rich.box.ASCII` explicitly | Important | [CODE-CONTRADICTED]: the assumption that `safe_box` covers panes (corrected in Gate 1, cycle 1). `test_terminal.py` pins only the attribute (`safe_box is True`, lines 109 and 115). In ASCII, rule and border share the `-` character [derived] |
| Composition architecture (Q1) | String-only pipeline: `build_view` to `screen_lines` to `list[str]` to one `Text` per line; no span, border or column anywhere. Four findings (M-05, M-08, M-13, M-14) touch strings the record and goldens also read | A render-only style and frame layer; `screen_lines` stays the plain source; one renderable per line | Important | The dominant code obstacle (04). Options: (1) style map over unchanged strings, (2) segment-returning builders, (3) hand-built frame helper, (4) Rich `Panel`, `Table.grid`, `Columns`, `Layout`, (5) two-column zip with `cell_len` padding. Option 4 conflicts with test_render.py:399 and list-based budgets |
| Colour depth and detection (Q4, G-2) | `color_system` fixed `"standard"` (terminal.py:121); no COLORTERM, TERM or isatty check; RGB or 256 styles are downsampled at write time | Decide target depths and detection; per-depth role table; NO_COLOR stays `None` | Important | **OPEN** (owner decision on depths). Measured: `standard` gives bright red for amber text; `256` and `truecolor` keep it. `"auto"` resolved to no colour for a StringIO file. Rich caches a `Style`'s ANSI codes, so tests that build consoles with different systems in one process can see stale codes. [external context: https://rich.readthedocs.io/en/stable/console.html, auto reads COLORTERM then the last part of TERM] |
| Live versus one-shot styled capture (Q5) | Live path keeps SGR; `--once --width` calls `export_text()` (styles dropped, commands.py:242); `--once` without `--width` prints `record_text`; today nothing is styled | A styled capture route that honours NO_COLOR and the colour system; gate tests for ANSI present, none under NO_COLOR, plain text equal to the golden lines, widths 160, 116, 80 and ASCII | Important | `export_text(styles=True)` bypasses NO_COLOR and down-conversion (probe) [CODE-VERIFIED]; the NO_COLOR-correct route is `console.file.getvalue()`. 02 wins over 01 and 03 on the route (Section 4.3). **OPEN**: ANSI on a piped `--once --width` (no tty check today; decision D-4, default no); box-drawing in `--once --width` output (decision D-9, default yes, which step 3.6 assumes); test_commands.py:121 (`"\x1b" not in out`) changes only if the styled route is chosen |
| Live screen has no test (G-F) | No test references `LiveScreen` or `run_interactive`; `FakeScreen` records calls only; `make_console` has no `force_terminal` parameter | A pty (pexpect 4.9.0) or `force_terminal` seam capture of the real `LiveScreen` | Important | Cycle-1 measurements used a stand-in console. [UNVERIFIED]: whether `run_interactive` accepts `--fixture`. `spike_child.py:64` already runs a raw `Live(screen=True)` on a pty |
| Height budget and silent bottom crop (G-G) | No final `lines[:height]` clamp; one ledger row forced (render.py:502); `Screen` cuts rows past the height; footer lost first | Every frame, tile and heading row counted in the budget; matrix test at 40, 44, 24, 12 and 8 | Important | Only the base fixture at height 40, the `five` golden and desks at height 70 were run; frames at smaller heights are [UNVERIFIED]. Which of the three `+1` terms in `spare` is which (render.py:454-456) is [UNVERIFIED] |
| Golden re-baselining (G-A) | T47 (test_render.py:611-624) pins questions-off `lines_*` and `printed_*` to release 1 (`git archive 9e2608b03`); T64 pins link-off lines (`golden_questions_linkoff.json`) | Owner decision: re-baseline both, or freeze questions-off and gate the new look to questions-on, or add a new golden and keep T47 | Important | **OPEN**. M-10 and M-11 (C8 defects) change questions-off lines at 116 and 80, so this decision gates their remediation. No recorder exists for the link-off golden; regeneration commands are derived, not owner-approved; the exact `PYTHONPATH` layout is [UNVERIFIED]. Style-only changes touch 15 `printed_*` values and no link-off values |
| Render harness (Q3) | No PIL, cairosvg, pyte, playwright, fontTools, browser, rsvg-convert, ImageMagick, freeze or aha; `pyproject.toml` and the Makefile declare nothing for images; Rich `export_svg` and `export_html` available; `render_current.py` writes text and ANSI via `export_text(styles=True)` at height 50 | A reproducible text and ANSI tier (offline) plus an image tier for the reviewer, with a fixed rubric | Important | `render_current.py` ignores NO_COLOR and the 16-colour downgrade, so a harness built on it shows truecolor a 16-colour terminal never shows (F-02); capture `console.file.getvalue()` through `make_console` instead. Rich SVG needs a browser engine: rsvg-convert and ImageMagick failed on it [external context: https://github.com/Textualize/rich/issues/2153; whether Rich 15 changed this is UNVERIFIED]. freeze is the simplest ANSI to PNG binary but is an extra install [external context: https://github.com/charmbracelet/freeze]. Playwright MCP exists only in the Claude session, so CI cannot rely on it. Claude agents can view PNGs with Read (both Gate 1 QA reviewers did). **OPEN** (Q-7: new dev dependency or text rubric plus mockup PNG; decision D-10 in 8.2). The rubric criteria are written in Section 8.4 (SC-14) |
| 64-hex fixture in the 80-column Decision Desk (Q7, G-E) | Measured: the hash wraps whole at 160, 116 and 80; a path longer than the width hard-splits mid-word with no marker (render.py:62-80); no fixture, test or `session_fields` case holds a hash, a long path or a wide character; no real frame exists yet | A fixture and test pinned BEFORE the layout phase; a visible hard-wrap rule for tokens wider than the inner width; a decision whether a cut hash may be shown | Important | **OPEN** (Q-6: show the hash in full?). Frame inner width 74 at 80, so a 64-cell token fits; a label plus hash (20 + 64) moves to its own line. Risks are the 4-line cap cutting the hash when path and file list consume the lines, and a pane that clips instead of wraps. Plan-ask content is [UNVERIFIED] (pr-591-comment.md lines 26-31). Proposed second fixture with a trailing hash, and a 120-character `resource.worktreeId`. The "frame" premise of pr-591-comment consideration 8 is not yet true (no border at render.py:329-356) |
| Zellij 0.44.2 go or no-go (Q6) | Installed at `/usr/local/bin/zellij` with an ANSI-16 theme and two layouts from `/etc/skel`; help text lists `run -f` with size and position, `dump-screen --ansi`, `--layout-string`; no session was started; CI presence unknown | The observer works standalone and read-only at all widths, NO_COLOR and ASCII; Zellij only wraps it | Minor | Both sources agree: not a dependency of the observer or the render gate (05: no-go; web-02: conditional go for an optional layout). `dump-screen` yields text or ANSI, never an image. [external context: https://zellij.dev/documentation/nested-sessions.html, the `ZELLIJ` env var is set in every pane, so the observer may read it as a hint and must not require it.] [external context: https://zellij.dev/documentation/cli-actions.html] The docs describe a newer release (0.46.0, https://zellij.dev/news/terminal-inbox-session-previews) than the local 0.44.2, so run `--help` locally first. Floating-pane behaviour, `dump-screen` fidelity, command panes, truecolor pass-through, theme reading and tab-bar rows against the 44-row contract are all [UNVERIFIED] without a live session |
| Spec self-contradiction (G-H) | RR 61 lists the 80-column invariant lines "Questions stay until explicit resolution." and "No reply observed is not delivery failure."; neither is on screen; AD-7 rejects the first against RR 42 | RR 61 or RR 42 reworded deliberately | Important | [CODE-CONTRADICTED]. Reword in the same spec change as O-1 |

#### 4.1c Open items flagged open

| Gap | Current State | Target State | Severity | Notes |
|---|---|---|---|---|
| O-1 Two columns at 160 and 116 | RR 43 and 57 say one stacked block; code builds that | Decided yes or no by the owner | Important | **OPEN**, owner decision pending; FIND recommends yes, with 80 columns staying stacked and the spec text updated in the same change. Gates M-03 and M-04 (Critical) and Q1 |
| OPEN-1 Severity of M-07 | Astra High, Opus Medium | One agreed severity | Important | **OPEN**; handled as Medium (gated); Opus's condition makes it Medium while M-03 is High |
| OPEN-2 Severity and scope of M-14 | Opus Medium, Astra Low; RETAIN CONTEXT not built (RR 41) | Severity set; build or not build | Important | **OPEN**; handled as Medium (gated); scheduled late either way |
| OPEN-3 Scope of M-13 | Opus Low, Astra Medium; READ ONLY badge absent | Badge required; alignment and diamond glyph optional | Important | **OPEN**; RR 17 must be reconciled deliberately |

Source: rows built from 01 section 8.1, 04 section 5, 03 section 6, 02 sections 2 and 9, 05 sections 2 to 7, web-01, web-02 and `gaps-and-questions.md` Sections B and D.

### 4.2 Remediation needs linked from the C8 defects

| Need | Defect | Specific change | Depends on | Tests and goldens touched |
|---|---|---|---|---|
| RN-1 | M-08 | Add a muted role and apply it in the renderer to absent values: the bare token `unknown` (not the quoted real value `"unknown"`, view.py:377-385), `unavailable (no source)`, and the appended `reason unknown` (render.py:319; view.py:744, 748). Prefer building the line from segments (Q1 option 2) over regex matching, because free text such as `age unknown` or worker-controlled strings can contain the same word. Plain under NO_COLOR | Q1 composition choice; Q4 role table (a muted role must stay distinct from base at 16 colours: index 7 versus 15 is a small step) | test_render.py:250-259 rewrite; `release1_surface.py` `_printed` strips SGR so the 15 `printed_*` golden values keep their plain bytes (no regeneration in the style-only phase); no `lines_*` change |
| RN-2 | M-10 | Remove the `width_class == "full"` gate at render.py:497 for the `line` and `short` classes so `_header_lines` prints the existing names at 116 and 80 when `view.visible_rows`; add the 2 heading rows to `ledger_fixed` (:438-440), the separate budget used when the questions panel is sized. `reserved` (:499-501) needs no edit: it reads `len(body)`, and the heading rows are appended to `body` at :497-498 before `reserved` is computed, so a separate addition would count them twice | G-A owner decision (changes `lines_116x*` and `lines_80x*` in `golden_release1_surface.json` and the link-off golden); SC-9 height matrix | test_render.py:83-102 (the `^\d+/\d+ shown` and line-count checks), test_decision_2 (:660), test_inspector_scroll.py height budgets, both goldens |
| RN-3 | M-11 | Make `_help_lines` (render.py:304-308) wrap instead of clip when `view.questions is None`, wrapping by double-space key groups so pairs are not split (M-15); update `footer_height` (:423-431) and the footer branch (:514-520) | G-A owner decision (changes the questions-off 80-column footer and the 116 footer); SC-9 | test_render.py:748 (test_f08), `lines_80x*` goldens, test_linkoff_screen_reference.py `KEYS_LITERAL` (:34-37) only if the key text changes |

No cited scope decision defers RN-1 to RN-3. The only brake is the golden pin (T47), which is a sequencing dependency on the owner's re-baseline decision, not a scope decision.

### 4.3 Contradictions between research files, and stale documents

Every [CODE-CONTRADICTED] and [STALE DOC] finding in the research is listed once. Where two research files disagree, the stronger evidence is named.

#### 4.3a Conflicts and corrections

| Item | Claim | What code or measurement shows | Stronger evidence | Treatment |
|---|---|---|---|---|
| Width classes | Task prompt (g) and `research-notes.md:24`: full, line, narrow | Four classes: full, line, short, narrow (terminal.py:63-70) | Code (01) | Use four classes |
| `safe_box` | An earlier draft of 03 section 6 rule 3 and the 04 G-1 row said `safe_box=policy.ascii` gives Rich boxes an ASCII fallback | A Rich `Panel` prints identical Unicode borders with `safe_box` True and False; `box=rich.box.ASCII` prints `+---+`; Rich swaps in the ASCII box only when output is not UTF-8 (rich/box.py:79-83) | Probe reproduced by two reviewers; 01 had it right | Corrected in cycle 1; explicit ASCII box required |
| Styled export route | 01 (lines 55, 231) and 05 section 5 recommend `export_text(styles=True)`; web-02 B8 guesses the recording console is misconfigured | `export_text(styles=True)` returns SGR even with NO_COLOR and `color_system=None`, because the record buffer stores segments before colour is stripped; `make_console` is already what `render_current.py` uses | 02 probe (byte-level, Rich 15.0.0) beats web-02's inference | Use `console.file.getvalue()` (F-02) |
| Slate and muted collapse | 01 section 7 infers slate and muted both land on greys and amber has no standard colour | Measured downgrade: slate 8, muted 7, amber 11, and green, red, violet, muted all 7 | 04 (computed with Rich's own downgrade; reproduced by two reviewers) | Use the 04 table; drop the 01 inference |
| Rich NO_COLOR versus project NO_COLOR | web-01: Rich's NO_COLOR keeps bold, dim, italic, underline | `make_console` passes `color_system=None` as well, which drops all SGR including bold | Code (project choice, not a conflict) | Decide whether bold may survive NO_COLOR (keep a colour system and set `no_color=True`) |
| Live overflow marker | Rich docs: `Live` default `vertical_overflow="ellipsis"` | Under `screen=True` the `Screen` wrapper crops rows to the height first, so no ellipsis appears (measured) | Code measurement (02) | Do not rely on an ellipsis; reserve own overflow row |
| `FROZEN` token | `rendering-rules.md:20`: `FROZEN unavailable (no source)` [STALE DOC] | Code prints `POLICY FROZEN unavailable (no source)` (view.py:948) | Code; FIND already uses the code wording | Use the code wording |
| M-10 location | FIND: `render()` prints the header only for `full` | The condition is in `screen_lines` render.py:497-498; `render()` is at 524-531 | Code | Cite `screen_lines`; behaviour confirmed |
| Full ledger width | FIND M-06: "153 cells", attributed to RR line 30 [UNVERIFIED] | `_columns` gives exactly 160 at 160 (2 + 114 + 22 + 12 + 10) | Code arithmetic | Use 160; do not state 153 |
| Slack arithmetic | 01 section 8.2 item 5: 114 + 1 + 42 = 157 of 160 [UNVERIFIED] | 04 measured 1 + 114 + 2 + 42 + 1 = 160 | 04 (measured) | Use the 04 numbers |
| RR 61 versus RR 42 | RR 61 requires the two 80-column invariant lines; the output shows neither; AD-7 rejects the first as untruthful against RR 42 | Spec is self-contradictory | Spec text and code | Reword in the O-1 spec change |
| pr-591-comment.md consideration 8 | Check the 80-column Decision Desk "frame" with a plan-ask hash | No frame exists (render.py:329-356); measured: hash wraps whole; long paths hard-split mid-word | Code (03) | Premise becomes true when frames land |
| Gate test line ranges | 03 section 4d: test_commands.py:747-760 and :762-777 | Functions end at 756 and 772 | 02 | Cite 747-756 and 762-772 |
| Desk line width | 03 section 5c: the 80-column desk line is "exactly the width" | Reproduced as 78 cells (desk lines 78, 78, 64) | Reproduction (Gate 1) | Say 78 cells |
| Path split length | 03 section 5c: a 140-character path splits into three pieces | A hard cut at 80 cells gives two pieces for 139 characters (80, 59); three pieces need about 165 | Reproduction | Behaviour right (mid-word, no marker); correct the length |
| Mockup ESC counts and RR length | 04: `ESC[0;1;` count 2 to 15 per file; RR "108 lines" | Counted 3 to 16; RR has 107 lines | Re-count (Gate 1) | State the measure |
| Cited lines | 04 M-05 cites render.py:374; 03 and 04 cite test_terminal.py:114-116; 02 cites rich/live.py:127-128 | render.py:373; test_terminal.py:109 and 115; live.py about 125-130 | Re-read | Use the corrected lines |
| Grep counts | 03 section 2: hit counts per test file | Re-run differs (test_render 64 versus 65, conftest 4 versus 2, test_fixtures 4 versus 2, test_export 2 versus 3) | Re-run | Cosmetic |
| `research-notes.md:95` | O-1 "recorded in the findings" | FIND and 04 treat O-1 as pending the owner | FIND and 04 | Treat O-1 as open |
| Zellij verdict | 05: no-go as harness dependency; web-02: conditional go for an optional layout | Neither exercised a session | Both agree on not a dependency; 05's local help text is verified, web-02's docs describe 0.46.0 | See Zellij row |

#### 4.3b Stale documents

| Document | Stale content | Current state | Treatment |
|---|---|---|---|
| `RR:37-41, 60-61` | 160, 116, 80 layouts, the right-hand `SEEN IS NOT RESOLVED` tile and RETAIN CONTEXT described as the layout | Line 43 of the same file says R2 built one stacked block; code builds only that (render.py:359-387) | Design reference, not behaviour |
| `RR:20` | `FROZEN unavailable (no source)` | `POLICY FROZEN ...` (view.py:948) | Use the code wording |
| `RR:33` | 116 fields listed as kind, dispatchId, liveness.verdict, age | Code also prints a `flags` column at 116 and 80 (render.py:197-212, 216-229) | Minor |
| `RR:41, 43` | RETAIN CONTEXT "not built in R2"; two-column layout "stays design reference" | Match code today; become stale if O-1 and M-14 are adopted | Update with the O-1 decision |
| `RR:61` | RETAIN CONTEXT reachable only through the inspector; two invariant lines | Neither is true of the inspector (render.py:255-287) or the output; conflicts with RR 42 | Reword |
| `RR:38` and the 160 and 116 mockups | Title `OPEN HUMAN QUESTIONS` | Retired; code uses `COORDINATOR QUESTIONS` (view.py:53) | Do not copy this title from the mockups |
| 80 and 116 mockup headings | `AFFECTED SESSIONS`, `SELECTED SIGNALS`, `SELECTED FLEET SLICE` differ from the 160 titles | AD-4 limits desk evidence to one linked session | Copy structure, not titles |
| `RR:59` | Says some `observed open: n` wording elsewhere in the file is superseded until the spec owner re-words it | Self-admitted partial staleness | Treat the file as partly stale |
| `FIND` M-10 and M-06 | `render()` location; "153 cells" | See 4.3a | Corrected here |
| `render_current.py:6-9` | `ansi-*.txt` are "empty of escapes today" | True now (0 ESC bytes in nine files); false once styling lands | Treat `inputs/current/` as a pre-fix baseline |
| `.dev/issues/409/ponytail-review-20261116/tests-and-fixtures.md:51` | Commit `c69ce4b3a` for `golden_release1_surface.json`; test lines 616-629 | `git log` prints only cd8736199 (#514); test now at test_render.py:611-624 | Likely a pre-squash hash |
| `.dev/reviews/orchestrator-tui-alignment-20261113/05-observe-built-state.md:27` | `QUESTION_GATE_PASSED = False` on master | Both gates are True (commands.py:67, :70) after #592 (3206bdb9c) | Doc predates #592 |
| `.dev/issues/409/ponytail-review-20261116/design-docs-and-gates.md:46` | `commands.py:67` and test_commands.py:741-750 | Guard test now at :747-756 | Line shift only |
| Zellij layout and theme headers under `~/.config/zellij` | Cite phase-tasklist task IDs and a CI gate "deferred to CI"; `config.kdl` cites upstream `default.kdl:511` and `:236-238` | Concern machine provisioning, not this repo; upstream lines not read [UNVERIFIED] | Out of scope |
| `.dev/issues/409/attachments/` | Not named in any research file | Its three PNGs are byte-identical to the 160 mockup PNGs (`cmp`) | No information lost |

Source: 01 Stale Documentation section, 03 Stale Documentation section, 04 Stale Documentation section and sections 1 to 5, 05 Stale Documentation section, `gaps-and-questions.md` Section C.

### 4.4 Unverified items carried as open questions

These claims were not confirmed; none is presented as current state.

| Item | Why it matters | What would close it |
|---|---|---|
| Colour capability at run time; the 16-colour mapping is computed with Rich's downgrade, not observed on a terminal | Decides the Q4 role table | A run on a real terminal at 16, 256 and truecolor |
| East-Asian-ambiguous box and block glyphs may render at another width in the owner's terminals (Rich `cell_len` counts them as 1) [external context: https://github.com/Textualize/rich/blob/v15.0.0/rich/cells.py, no locale rule for ambiguous width] | A mismatch would misalign every frame border | Check in the owner's terminals; keep chrome to box drawing, ASCII and a short vetted set |
| Real `LiveScreen` under a pty; whether `run_interactive` accepts `--fixture` | SC-15 | pexpect run at fixed pty size |
| Heights below 40 against a frame design; questions-on desk screens at those heights | SC-9 | Matrix run at 24, 12 and 8 |
| Which `+1` term in `spare` is which (render.py:454-456) | Frame row accounting | Read the code with the comment at 444-445 when planning |
| Fixtures `injection` and `long-identifiers` under styling | SC-18 | Run once styling lands |
| Real `observe --questions` and `--run` screens (live source needed); `w-` ids are 5 cells so M-17 is seen only with short ids | M-17 scope | Live read |
| Plan-ask content (path, file list, 64-hex hash) as `question` rows | Realism of the Q7 fixture | Confirm against the plan-ask source |
| Selected-row look; mockup PNG background (dark navy versus no 48 code in `.ansi`); behaviour on light backgrounds | M-18 and theme | Owner or rubric decision |
| Regeneration `PYTHONPATH` layout for `golden_release1_surface.json`; no owner-approved procedure for the link-off golden | G-A | Verify when re-baselining |
| Classification of ten test modules and `test_view.py` literals from names and docstrings only | The P2 break list is incomplete | Enumerate at plan time |
| Zellij: floating panes, `dump-screen --ansi` fidelity, command panes in a layout, theme reading, CI presence, truecolor pass-through, tab-bar rows | Q6 stays provisional | A live background-session experiment (`zellij attach --create-background`) [external context: https://zellij.dev/documentation/cli-actions.html] |
| Whether Pillow, cairosvg, pyte or a Playwright browser can be installed here; cairo system library; DejaVu Sans Mono glyph coverage; whether Rich 15 SVG works with non-browser rasterisers | Q3 image tier | Network and install test, with approval |
| The `commands.py:63-66` comment's owner record file was not opened | None for presentation | Existing test checks the file exists (test_commands.py:752-755) |
| Windows `legacy_windows` handling of `--once --width` (interactive mode refuses win32, commands.py:353-355) | Cross-platform one-shot | Note only |

### 4.5 Research findings not carried into Sections 3 and 4, with rationale

| Finding | Rationale for exclusion |
|---|---|
| Per-test line-by-line assertion map and per-phase test-name checklist (03 sections 1, 2, 6) | Belongs to the phasing and test plan section; Sections 3 and 4 carry the constraints and the phase summary (3.8) |
| Phase table P0 to P5 detail and the proposed fixture code shape (03 sections 5d, 6) | Same; summarised in 3.8 and SC-10 |
| Insertion-point arithmetic for candidate composition options 1 to 7 (01 section 8.2) | Options analysis belongs to the options section; the gap table names the five options |
| Collector, parse and key-map internals (02 sections 6 and 7) | No gap: unchanged by presentation work; the screen-only rule is carried in 3.7 |
| Zellij config, layout and theme file details (05 sections 1.2 to 1.5) | No effect on the target; only the 3 bar rows and the verdict are carried |
| Cosmetic Gate 1 notes (headers lacking a scope list, grep counts, a Summary placed before an addendum) | No effect on any decision; counts are listed in 4.3a |
| `adapter.py` was not read | Context only; not expected to change |
| Licence status of freeze, pyte, aha, cairosvg, ansi2html (LGPLv3+) | Open and relevant only if a tool is chosen; raise when Q-7 is decided |
| Community Zellij material (zjstatus, theme specs) | Not relevant to parity |

Section 4 sources: all eight input files; row-level sources are named in each Notes cell and in the Source lines.

## 5. External Research Findings

All findings in this section are EXTERNAL CONTEXT (Rich 15.0.0 documentation and source, Zellij documentation, tool repositories, blogs) unless a row says it is a codebase fact. Codebase findings take precedence over external ones. Paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`. Verification tags: [CODE-VERIFIED] = the codebase research files (`research/02-live-screen-commands-export.md`, `research/05-zellij-and-render-harness-environment.md`) read it in code, by probe or by help text; [CODE-CONTRADICTED] = the code shows something different (corrected here); [UNVERIFIED] = not checked against the code or not run.

Inputs: `research/web-01-rich-composition-and-colour.md` and `research/web-02-zellij-and-terminal-capture.md` (external), `research/02-live-screen-commands-export.md` and `research/05-zellij-and-render-harness-environment.md` (used only to state each finding's relationship to the code).

### 5.1 Rich composition (Panel, Table, Columns, Layout, box styles, Text spans)

Question served: Q1 (safest composition) and Q7 (long unbroken token).

| # | Finding | Source (URL) | Relevance | Relationship to codebase |
|---|---|---|---|---|
| 5.1.1 | Rich separates content from style: `Text` holds plain text plus `Span(start, end, style)` (exclusive end). Built with `Text.assemble((str, style), ...)`, `Text.append(str, style)` or `Text.stylize(style, start, end)`; overlapping spans combine, later wins. A styled line can therefore keep a plain string identical to today's line. | https://github.com/Textualize/rich/blob/v15.0.0/rich/text.py ; https://rich.readthedocs.io/en/stable/text.html | HIGH | EXTENDS. `render()` (`src/superclaude/cli/observe/render.py:524-531`) builds one `Text(line, no_wrap=True, overflow="crop")` per `screen_lines` line with no style at all [CODE-VERIFIED]. Spans are the smallest addition to that structure. |
| 5.1.2 | Panel, Table, Columns and Layout all measure children with `cell_len` and render to Segment lists, so none breaks a one-renderable-per-line rule by itself, but each would replace the "one `Text` per line" structure. web-01 states the tests require one renderable per line and forbid `Console(` and `sorted(` in `render.py`. | https://rich.readthedocs.io/en/stable/panel.html ; https://rich.readthedocs.io/en/stable/reference/panel.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/color.py (web-01 section G2) | HIGH | SUPPORTS keeping the line model. The test constraint itself comes from web-01's executor summary and was not re-read by the codebase files cited here [UNVERIFIED in this synthesis]. 02 section 8 confirms the change surface is `render()`, the one-shot export call and `make_console` [CODE-VERIFIED]. |
| 5.1.3 | `Panel` defaults to `box.ROUNDED`, `safe_box=True`, `expand=True` (stretches to console width); `border_style` styles only the border. "Safe box" is a legacy Windows cmd.exe raster-font safeguard: unsafe boxes are replaced only there. Boxes are constants from `rich.box` passed as `box=`. | https://rich.readthedocs.io/en/stable/appendix/box.html ; https://rich.readthedocs.io/en/stable/reference/box.html | MEDIUM | PARTLY CONTRADICTS the intent of `safe_box=policy.ascii`. `make_console` passes `safe_box=policy.ascii` (`terminal.py:110-125`) [CODE-VERIFIED]. web-01's executor summary reports that Panel prints identical Unicode borders with or without `safe_box` on this platform and that `box=rich.box.ASCII` is needed under `--ascii` [UNVERIFIED in this synthesis, not re-probed]. So `safe_box` is not an ASCII switch; an ASCII border needs an explicit box choice. |
| 5.1.4 | The fetched box docs list only `SQUARE` and `ROUNDED` in text (the box list is an image). Existence of `box.HEAVY`, `box.ASCII` and `box.ASCII2` in the installed Rich 15.0.0 is not confirmed by the docs and should be checked with `dir(rich.box)`. | https://rich.readthedocs.io/en/stable/appendix/box.html | MEDIUM | EXTENDS. Rich 15.0.0 is installed [CODE-VERIFIED, 05 section 2]; the box-name check has not been run [UNVERIFIED]. |
| 5.1.5 | `Text` with `no_wrap=True, overflow="crop"` clips a long unbroken token silently at the width. `overflow="ellipsis"` reserves one cell for a visible marker. `fold` splits the token across lines (adds rows). `overflow="ignore"` skips width enforcement. Truncation works in cell width. | https://github.com/Textualize/rich/blob/v15.0.0/rich/text.py ; https://rich.readthedocs.io/en/stable/text.html | HIGH (Q7) | SUPPORTS. `render.py:528` uses `no_wrap=True, overflow="crop"`, so a line longer than `policy.width` is cut and never wrapped [CODE-VERIFIED, 02 section 9.4]. The earlier external-context claim that the 64-hex-character token in the 80-column Decision Desk is "silently clipped today" is SUPERSEDED by the code measurement (Section 2.3 Q7): `wrap` (render.py:62-80) runs inside `screen_lines` before `render()`, so every line already fits the width and `crop` never cuts the hash; in the measured fixture the hash is whole on its own line at 160, 116 and 80. Only the 4-line desk cap (`DESK_TEXT_LINES`, view.py:99; last line cut with `...`) and the 400-character ask cap (`ASK_CAP`, parse.py:475; applied at :499-503) can remove a trailing hash. `ellipsis` would add a marker at a cost of one cell per line and is not needed for the hash. |
| 5.1.6 | `cell_len` is table-based: wide East Asian characters 2, combining 0, ambiguous-width characters (box drawing, many symbols) count 1, no locale rule; printable-ASCII strings take a fast path. Terminals that draw ambiguous glyphs as 2 cells will misalign borders against Rich's count. Padding by `len()` differs from Rich for any wide or zero-width character. | https://github.com/Textualize/rich/blob/v15.0.0/rich/cells.py | HIGH | SUPPORTS. Width logic in `render.py:62-92, :311-326` is `cell_len`-based and must stay on plain strings [CODE-VERIFIED, 02 section 8]. Keep chrome to box drawing, ASCII and a short vetted symbol set; no emoji (consistent with `emoji=False` in `make_console`). |
| 5.1.7 | No documented Rich pattern exists for "line model plus styles". web-01 derives two options: a pure `style_spans(line, role) -> Text` layer keyed on line position or prefix, or `screen_lines` returning `list[Text]` whose `.plain` equals today's string. Text records and one-shot plain output should use `Text.plain`, never a styled capture. | Derived from https://github.com/Textualize/rich/blob/v15.0.0/rich/text.py (not a documented pattern) | HIGH (Q1) | EXTENDS. The record (`record_text`) and snapshot (`snapshot_json`) are built from `View` data in `export.py` with no Rich import, so Rich styling cannot change them unless `view.py` field values change [CODE-VERIFIED, 02 section 5]. Flagged as inference, not source-backed. |

Diagram (the line model with a thin style layer, as the external research supports it):

```text
View --> screen_lines(view, policy) --> list[str]  (today, plain, cell_len width maths)
                                            |
                                            v
                              style layer (pure, by role)       <- new, spans only
                                            |
                                            v
                         Text(line, no_wrap=True, overflow="crop") + Spans
                                            |
                                            v
                                  Group --> Console / Live

record_text(view), snapshot_json(view): View --> export.py   (no Rich, unchanged)
```

### 5.2 Rich colour system and detection (color_system values, COLORTERM and TERM, NO_COLOR)

Question served: Q4 (colour depth, detection, fallbacks, 16-colour role distinctness).

| # | Finding | Source (URL) | Relevance | Relationship to codebase |
|---|---|---|---|---|
| 5.2.1 | `Console(color_system=...)` accepts `None`, `"auto"` (default), `"standard"` (8 + bright = 16), `"256"`, `"truecolor"`, `"windows"`. Docs warn that forcing a higher system than the terminal supports can make text unreadable. | https://rich.readthedocs.io/en/stable/console.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py | HIGH | SUPPORTS. `make_console` passes the literal `"standard"` unless `NO_COLOR` is non-empty (`terminal.py:83, :121-122`) [CODE-VERIFIED, 02 section 1]. The pin is a deliberate floor, not Rich's default. |
| 5.2.2 | Auto detection (`_detect_color_system`): notebook gives truecolor; non-terminal or dumb terminal gives None; elsewhere `COLORTERM` of `truecolor` or `24bit` gives truecolor, otherwise the last hyphen-separated part of `TERM` (for example `xterm-256color` gives 256) picks the palette, default standard. | https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py ; https://rich.readthedocs.io/en/stable/console.html ; background: https://marvinh.dev/blog/terminal-colors (medium reliability blog) | HIGH | EXTENDS. Detection is cheap (`color_system="auto"`), so a 256 or truecolor tier is a small change in `make_console` plus tests. Because the code pins `"standard"`, this logic is bypassed today [CODE-VERIFIED]. |
| 5.2.3 | Terminal detection (`is_terminal`) order: explicit `force_terminal`; IDLE rejected; notebook rejected; `TTY_COMPATIBLE` 0/1; `FORCE_COLOR` present and non-empty means true (empty means false); else the stream's `isatty`. A pinned `color_system` does not bypass this: `is_terminal` still decides whether control codes reach a stream. | https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py | MEDIUM | SUPPORTS. `force_terminal`, `legacy_windows`, `_environ` and `style` are never passed anywhere in the package; the only `Console(` is `terminal.py:114-125` [CODE-VERIFIED, 02 section 1]. A `StringIO` console has `is_terminal` False, so `Live(screen=True)` writes nothing there [CODE-VERIFIED, 02 section 9.2 measurement 4]. |
| 5.2.4 | `TERM=dumb|unknown` disables colour and cursor features; non-empty `FORCE_COLOR` enables colour regardless of TERM; `NO_COLOR` set disables all colour and wins over `FORCE_COLOR`. | https://rich.readthedocs.io/en/stable/console.html (Environment variables section, via Context7 /textualize/rich) | HIGH | EXTENDS. The project reads `NO_COLOR` itself (`terminal.py:83`, `bool(env.get("NO_COLOR"))`) [CODE-VERIFIED]. `FORCE_COLOR` and `TERM=dumb` handling is Rich's only once `auto` is used; with `"standard"` pinned, only `is_terminal` is affected. |
| 5.2.5 | Rich's own `NO_COLOR` removes colour only: bold, dim, italic and underline are kept (`Segment.remove_color` when `no_color` and a colour system exist; `Style.without_color` keeps bold/dim). `Style.render` with `color_system=None` returns the text unchanged: no SGR at all, bold and dim included. | https://rich.readthedocs.io/en/stable/console.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/style.py | HIGH | EXTENDS (project choice, not a conflict). The code sets `color_system=None` plus `no_color=True` under `NO_COLOR` (`terminal.py:121-122`), which is stricter than Rich: it also drops bold/dim [CODE-VERIFIED; probe in 02 section 2 shows stream `'hello\n'` for a bold red `Text` under NO_COLOR]. Keeping bold/dim under NO_COLOR would mean keeping a colour system and using `no_color=True` only; that is an owner decision, not a research fact. |
| 5.2.6 | Truecolor to 256: RGB goes to HLS; saturation under 15 percent maps to the grey ramp (indices 16, 231, 232-255), otherwise channels are quantised to the 6-level cube (16 + 36r + 6g + b); arithmetic, not perceptual. Truecolor to standard matches against `STANDARD_PALETTE`. The first 16 colours are defined by the user's terminal theme, so identical indices look different per terminal. | https://github.com/Textualize/rich/blob/v15.0.0/rich/color.py ; https://rich.readthedocs.io/en/stable/appendix/colors.html | HIGH | SUPPORTS the code-side finding quoted in web-01's executor summary that the muted, green, red and violet hex roles all collapse to index 7 and slate to index 8 at 16 colours [UNVERIFIED in this synthesis: the mapping claim is in web-01's executor summary, not re-probed]. The collapse is a property of the downgrade, so the 16-colour tier needs named ANSI colours (`red`, `green`, `bright_black`, `magenta`, `dim`, `bold`) and a text or glyph cue, not hex values. |
| 5.2.7 | Not found in any source: Rich-documented guidance for keeping several muted roles distinct at 16 colours. The usual approach (carry role meaning in dim, bold, underline and a label or glyph as well as colour) is inference. | none (gap noted in web-01) | MEDIUM | EXTENDS. The installed Zellij theme is ANSI-16 only (cyan 6 accent, magenta 5, green 2, yellow 3, red 1, `FG_DIM` 8, ANSI 4 blue forbidden by its header) [CODE-VERIFIED, 05 section 1.5], which is a ready palette for named-colour roles. |
| 5.2.8 | Rich's `Live` with `screen=True` writes only alt-screen and cursor-hide control codes; no external source in the research files addresses blink or mouse. | https://rich.readthedocs.io/en/stable/live.html | LOW | SUPPORTS the standing no-blinking and no-mouse constraints: no `mouse` or `blink` match in `src/superclaude/cli/observe/*.py`, and `keys.py` sets only cbreak [CODE-VERIFIED, 02 sections 3 and 9]. A styled change must not add Rich's `blink` style (02 gaps note); that is a codebase rule, not an external finding. |

### 5.3 Rich export and Live behaviour (export_text styles, export_svg, export_html, record=True, Live with screen=True)

Questions served: Q5 (live versus one-shot path, styled-capture gate), Q7 (height budget) and Q3 (export as review artefact).

| # | Finding | Source (URL) | Relevance | Relationship to codebase |
|---|---|---|---|---|
| 5.3.1 | `export_text(clear=True, styles=False)` needs `record=True`; default output is plain text; `styles=True` includes ANSI codes. | https://rich.readthedocs.io/en/stable/reference/console.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py | HIGH | SUPPORTS. The one-shot width path calls `console.export_text()` with defaults (`commands.py:240-242`), so styles are dropped [CODE-VERIFIED, 02 section 2]. Today nothing is styled anyway: `render()` emits unstyled `Text`, and tests pin `"\x1b" not in out` (`tests/observe/test_commands.py:121`) [CODE-VERIFIED]. |
| 5.3.2 | web-01 (from source reading, flagged as inference "to verify"): `export_text(styles=True)` renders recorded segments through their style objects, so it ignores NO_COLOR and the colour-system downgrade, which apply at write time. | https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py | HIGH | SUPPORTS, and the codebase upgrades the inference to a fact. Probe on Rich 15.0.0 with a console built like `make_console`: under NO_COLOR the stream is `'hello\n'` but `export_text(styles=True)` still returns `'\x1b[1;31mhello\x1b[0m\n'` [CODE-VERIFIED by probe, 02 section 2]. A styled route that must honour NO_COLOR cannot use `export_text(styles=True)` alone. |
| 5.3.3 | web-01 recommends capturing the written stream (Console `file=` a `StringIO`, `force_terminal=True`, the production `color_system`) and asserting on SGR sequences. | https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py (source reading) | HIGH | EXTENDS, with a refinement from the code. For a plain `console.print`, `console.file.getvalue()` already holds NO_COLOR-correct, standard-converted SGR without `force_terminal`, because `_render_buffer` applies `style.render(..., color_system=...)` whenever a style exists and a colour system is set [CODE-VERIFIED by probe, 02 section 2]. `force_terminal=True` is needed only for the `Live(screen=True)` path: a `make_console`-shaped `StringIO` console has `is_terminal` False and `Live(screen=True)` wrote `''` [CODE-VERIFIED, 02 section 9.2 measurement 4]. `make_console` has no `force_terminal` parameter and `LiveScreen.draw` calls it directly (`commands.py:270`), so the real `LiveScreen` needs a test seam or a pty [CODE-VERIFIED, 02 section 9.3]. |
| 5.3.4 | `export_html` (params `theme, clear, code_format, inline_styles`) and `export_svg` (`title, theme, clear, code_format, font_aspect_ratio, unique_id`) need `record=True` and work on recorded segment styles and a fixed terminal theme from `rich.terminal_theme`, not on NO_COLOR or the colour system. They produce markup files, not terminal text. | https://rich.readthedocs.io/en/stable/reference/console.html ; https://rich.readthedocs.io/en/latest/console.html | MEDIUM | EXTENDS. Both methods exist in the installed Rich 15.0.0 [CODE-VERIFIED, 05 section 2]. The one-shot console is already `record=True` (`commands.py:240`) and `render_current.py` line 73 holds a recorded console, so adding export per width is a few lines [CODE-VERIFIED, 05 section 4]. Useful as a review artefact, not as the NO_COLOR test. Docs fetched are for 14.1.0; local is 15.0.0, so details may differ [UNVERIFIED]. |
| 5.3.5 | Docs: `Live(screen=True)` uses the alternate screen and restores the prompt on exit; `vertical_overflow` defaults to `"ellipsis"`. Source: `screen=True` wraps the renderable in `Screen`, which renders with `pad=True` and `Segment.set_shape(lines, width, height)`, so rows beyond the height are cropped and short rows are padded to full width. | https://rich.readthedocs.io/en/stable/live.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/live.py ; https://github.com/Textualize/rich/blob/v15.0.0/rich/screen.py | HIGH | SUPPORTS the code finding and contradicts the docs' ellipsis default under `screen=True`. Measured: with 40 observer lines at height 38 only 38 rows are written, the key list and the `shown 28/54 | collected 80 / reported 80` line vanish, and no ellipsis appears [CODE-VERIFIED, 02 section 9.2 measurement 3, stand-in console]. The base fixture at 80 wide and height 40 already fills all 40 rows [CODE-VERIFIED]. A taller design must fit the console height or add its own overflow row. |
| 5.3.6 | Styles survive Live drawing: segments keep their style and are written as SGR, subject to the console's `color_system`; padding cells carry no style. | https://rich.readthedocs.io/en/stable/live.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/screen.py | HIGH | SUPPORTS. Measured bytes: `ESC[?1049h ESC[H ESC[?25l ESC[H ESC[1;31mL1ESC[0m <pad> ... ESC[?25h ESC[?1049l` [CODE-VERIFIED, 02 section 9.2 measurement 1]. `LiveScreen` needs no change for styles to flow; its `shape` must keep covering `no_color` and `ascii` (`commands.py:265`) [CODE-VERIFIED]. |
| 5.3.7 | Plain `Console.print` never crops to `height`; only `Screen` does. | https://github.com/Textualize/rich/blob/v15.0.0/rich/screen.py | HIGH | EXTENDS. The one-shot `--once --width` path and every plain `screen_lines` test print or compare all lines, so they cannot see a footer lost on the live screen [CODE-VERIFIED, 02 section 9.2 measurement 4 and section 9.4]. A test asserting `len(screen_lines(...)) <= policy.height` at 24, 40, 44 and `MIN_ROWS = 8` (`terminal.py:22`) is the only guard. Heights below 40 were not measured against a frame design [UNVERIFIED]. |

Diagram (live path versus one-shot path as the code and Rich sources show it):

```text
LIVE:     render() Group --> Live(screen=True) --> Screen(pad width, cut to height)
                          --> ESC[?1049h ... styled padded rows ... ESC[?1049l   (stdout, real tty only)
ONE-SHOT: render() Group --> console.print --> record buffer --> export_text()  (styles=False, plain)
                                          \--> file.getvalue()  (SGR, NO_COLOR-correct)   <- not used today
`--once` (no --width): record_text(view)  (no Rich at all)
```

Contradiction between the research files (rule 6): web-02 section B1 and B8 infer that a recording Console created with a forced colour system, or with NO_COLOR, should record the downgraded styles, and web-02 recommendation 1 builds the harness on that. The codebase probe (02 section 2) shows the opposite for `export_text(styles=True)`: the record buffer keeps the original styles and NO_COLOR is not applied. The probe has the stronger evidence (measured on Rich 15.0.0), so the harness must either read `console.file.getvalue()` or accept that `export_html`/`export_svg` show the un-downgraded recorded styles; NO_COLOR and 16-colour cases need the stream capture. web-01 agrees with the probe (section C).

### 5.4 Zellij (layouts, floating panes, dump-screen, themes, status bar)

Question served: Q6 (Zellij 0.44.2 go or no-go). Local state: Zellij 0.44.2 at `/usr/local/bin/zellij`, minimal `config.kdl` (`theme "aidev02"`), layouts `agent.kdl` and `default.kdl`; no session was started and nothing was exercised [CODE-VERIFIED, 05 section 1].

| # | Finding | Source (URL) | Relevance | Relationship to codebase |
|---|---|---|---|---|
| 5.4.1 | Layouts are KDL files loaded with `zellij --layout <file>`; a `floating_panes { pane { x y width height } }` node (fixed counts or percentages) can sit at the layout root or inside a `tab`; floating panes cannot have children or `split_direction`. Command panes are `pane command="htop"` or `pane command="cargo" { args "test" }`. | https://zellij.dev/documentation/creating-a-layout.html ; https://zellij.dev/documentation/layouts.html ; https://zellij.dev/documentation/layout-examples | MEDIUM | EXTENDS. Neither installed layout defines a floating or observer pane (`default.kdl` lines 48-58 hold only tab-bar and status-bar; `agent.kdl` line 113-120 only a status bar) [CODE-VERIFIED, 05 sections 1.3, 1.4]. `zellij run -f --width --height -x -y` exists per help text [CODE-VERIFIED by help text]. Layout syntax for a command pane running `superclaude observe` is [UNVERIFIED]. |
| 5.4.2 | `zellij action dump-screen` dumps a pane viewport to stdout or `--path FILE`; `-f/--full` adds scrollback, `-p/--pane-id <id>`, `-a/--ansi` keeps colour and styling (cursor movement is not kept). Output is text or ANSI, never an image. | https://zellij.dev/documentation/cli-actions.html ; https://zellij.dev/documentation/programmatic-control.html | HIGH | SUPPORTS. Local help text shows the same flags: `-a/--ansi`, `-f/--full`, `-p/--pane-id <terminal_N|plugin_N|N>`, `--path` [CODE-VERIFIED by help text, 05 section 1.6]. Fidelity for colours, wide glyphs and box drawing is [UNVERIFIED]; web-02 infers Zellij re-renders cells itself, so a dump is not a byte copy of what the observer printed (inference, not in docs). |
| 5.4.3 | A headless session can be driven from the CLI: `zellij attach --create-background`, then `zellij --session NAME action dump-screen --pane-id terminal_1 --full`, `new-pane`, `paste`, `send-keys`, `list-panes --json`. The 0.44.0 release notes add `list-panes`, `send-keys` and `dump-screen` for any pane in any session. | https://zellij.dev/documentation/cli-recipes.html ; https://zellij.dev/news/remote-sessions-windows-cli | HIGH | EXTENDS. Local `zellij action --help` (first 120 lines only) lists `dump-screen`, `list-panes`, `new-pane`, `paste`, `dump-layout` but `send-keys` was not seen in that partial list, and `attach --create-background` was not run [CODE-VERIFIED for listed names; `send-keys` and `--create-background` on 0.44.2 are UNVERIFIED]. |
| 5.4.4 | Bars are drawn by `pane size=1 borderless=true { plugin location="zellij:tab-bar" }` (status-bar size 2, compact-bar one line) inside `default_tab_template`. Docs say the three are now one plugin `zellij:bars` with a `role` setting; the old URLs still work. | https://zellij.dev/documentation/layout-examples ; https://zellij.dev/documentation/plugin-aliases.html | MEDIUM | SUPPORTS. `default.kdl` uses `zellij:tab-bar` (1 row on top) and `zellij:status-bar` (2 rows at the bottom) [CODE-VERIFIED, 05 section 1.3]. These bars are chrome outside the observer's own header and footer; they would count toward mockup parity only if the mockups include them [UNVERIFIED]. A bar on `default.kdl` takes 3 rows from the pane height. |
| 5.4.5 | Themes are KDL `themes { name { ... } }` nodes selected by `theme "name"`; the new spec uses UI-component nodes, the legacy spec (`fg bg black red ...`) still works and accepts truecolor, 256 indexes or hex; `theme_dark` and `theme_light` switch with the host terminal. A theme styles Zellij's own chrome, not the observer's output (web-02 infers ANSI-16 indexes may map through the host palette; not in docs). | https://zellij.dev/documentation/themes.html ; https://zellij.dev/documentation/legacy-themes.html | MEDIUM | SUPPORTS. The installed theme `aidev02` is ANSI-16 only (every value an integer in 0-15; cyan 6 primary, magenta 5 secondary, green 2, yellow 3, red 1, dim 8) [CODE-VERIFIED, 05 section 1.5]; `agent.kdl` differs by magenta selected-frame colour [CODE-VERIFIED]. Reuse means choosing the same ANSI-16 indices in Rich; whether an application can read the active Zellij theme at runtime is [UNVERIFIED]. |
| 5.4.6 | Applications detect Zellij by the `ZELLIJ` environment variable set in every pane; `ZELLIJ_PANE_ID` and `ZELLIJ_SESSION_NAME` are also set (issue thread, medium reliability). A subshell that changes `TMPDIR` can lose the session, so detection is reliable but CLI control from inside is not always. | https://zellij.dev/documentation/nested-sessions.html ; https://github.com/zellij-org/zellij/issues/3637 | HIGH | EXTENDS. The codebase research found no `ZELLIJ` handling in the observer (the policy reads `NO_COLOR` via env at `terminal.py:83`) [UNVERIFIED that no other read exists]. The observer can read `ZELLIJ` as an optional hint and must not require it. |
| 5.4.7 | No Zellij documentation page was found stating how Zellij passes or downgrades 256-colour and truecolor output. | none (gap; general background https://marvinh.dev/blog/terminal-colors) | MEDIUM | EXTENDS. Not verified locally either [UNVERIFIED]. A 16-colour design avoids the question; a 256 or truecolor tier would need a live-session check first. |
| 5.4.8 | Version gap: zellij.dev announces 0.46.0 on 2026-11-11 and documents nested sessions since 0.45.0; the programmatic CLI (`list-panes`, `send-keys`, `dump-screen` for any pane) is documented as new in 0.44.0. Docs describe the latest version, so flags such as `--pane-id` on every action or `zellij:bars` may not exist in 0.44.2. | https://zellij.dev/news/terminal-inbox-session-previews ; https://zellij.dev/news/remote-sessions-windows-cli | HIGH | SUPPORTS the code finding that local is 0.44.2 [CODE-VERIFIED, 05 section 1.1]. Check `zellij action dump-screen --help` and `new-pane --help` locally before relying on a documented flag. |

Contradiction on Q6 (rule 6): web-02 recommends "GO conditional" (optional layout, optional manual capture), while 05 recommends "no-go as the Phase 0 render harness or a dependency, optional presentation environment after a verified session experiment". They agree on every operative point: the observer stays standalone, read-only, works at all widths with NO_COLOR and ASCII, Zellij is never a dependency of the render gate, and `dump-screen` yields text, not an image. They differ only in scope of the word "go". 05 has the stronger local evidence (help text read, install provisioned from `/etc/skel`, CI presence of Zellij unknown); web-02 has the stronger documentation evidence for what Zellij can do. Net external position: usable only as an optional manual presentation and capture check, not as harness or dependency; every runtime behaviour stays [UNVERIFIED] until a live-session experiment.

### 5.5 Offline render-to-image tools (install cost and offline suitability)

Question served: Q3 (render-to-image harness and the fixed-rubric reviewer method). Local state [CODE-VERIFIED, 05 section 2]: Rich 15.0.0 present; PIL, cairosvg, pyte, playwright, fontTools, chromium, rsvg-convert, inkscape, ImageMagick, freeze, termshot, aha, ansi2html and unzip all absent; node 24.22.2 and npx present; `pexpect` 4.9.0 declared (`pyproject.toml` line 41); no Playwright browser cache; DejaVu Sans Mono installed (glyph coverage of the mockups [UNVERIFIED]); `pyproject.toml` and `Makefile` have no image, SVG or render target.

| # | Tool or route | Finding | Source (URL) | Install cost | Offline suitability | Relevance | Relationship to codebase |
|---|---|---|---|---|---|---|---|
| 5.5.1 | Rich `export_svg` / `export_html` | Available with no new dependency. SVG uses `foreignObject` and a `@font-face` for Fira Code (`local()` plus remote URLs); a 2022 issue found it fully usable only in Chromium-based browsers, with `rsvg-convert` and ImageMagick failing. Why the issue was closed is not shown; whether Rich 15 changed this is unverified. | https://rich.readthedocs.io/en/latest/console.html ; https://github.com/Textualize/rich/issues/2153 | None | Produces files offline; turning them into PNG needs a browser engine | HIGH | SUPPORTS: both methods exist locally [CODE-VERIFIED, 05 section 2]; `render_current.py` line 73 already has a recorded console. [UNVERIFIED] whether Rich 15 SVG renders in a rasteriser. |
| 5.5.2 | Playwright MCP browser as rasteriser | `page.screenshot(path=...)`, `full_page=True`, `locator.screenshot()`, settable viewport; Python install needs `playwright install chromium` (downloads a browser). Opening a local SVG/HTML file is standard browser behaviour (inference). | https://snapshotflow.com/blog/playwright-screenshot ; https://www.scrapingbee.com/webscraping-questions/playwright/how-to-take-screenshot-with-playwright | Python route: package plus browser download (network). MCP route: none in a Claude session | MCP route works only inside the Claude session, not repo CI | HIGH | SUPPORTS: Playwright is not installed and `~/.cache/ms-playwright` is absent; the MCP tool exists only in the Claude session [CODE-VERIFIED, 05 sections 2 and 5]. Not exercised [UNVERIFIED]. |
| 5.5.3 | freeze (charmbracelet) | ANSI or code to PNG, SVG or WebP; defaults JetBrains Mono 14px, line height 1.2; `--font.file`, `--window`, `--padding`, `--margin`, `--background`; `--execute` runs a command in freeze's own pty where tools may drop colour. Adds window chrome and padding by default (would need disabling to compare with a mockup). Licence not confirmed. | https://github.com/charmbracelet/freeze ; https://www.getclaudeskills.com/skills/terminal-screenshot-daymade (low-medium reliability) | One static Go binary; absent locally; needs network or vendoring (Go toolchain not checked) | Yes once vendored or pre-installed | MEDIUM-HIGH | SUPPORTS "no render-to-image tool installed" [CODE-VERIFIED, 05 section 2]; conflicts with a "no new tools" stance if one applies. |
| 5.5.4 | pyte (with pexpect) | Pure-Python VTXXX emulator: `Screen(cols, rows)` plus `Stream`, read cell characters and attributes; no image output. With `pexpect` it captures a pty run exactly as a terminal shows it, including alt-screen output. Licence not confirmed. | https://pyte.readthedocs.io ; https://cefboud.com/posts/terminals-pty-tty-pyte (medium reliability) | One pure-Python dev dependency; absent locally | Yes after install | MEDIUM | SUPPORTS: `pyte` absent, `pexpect` 4.9.0 present, and `tests/observe/spike_child.py:64` already runs a raw `Live(screen=True)` on a pty [CODE-VERIFIED, 02 section 9.3 and 05 section 3]. A pty capture of a stand-in child produced the alt-screen bytes with `is_terminal True` [CODE-VERIFIED, 02 section 9.3 route B]. Whether `run_interactive` accepts `--fixture` is [UNVERIFIED]. |
| 5.5.5 | aha, ansi2html, termshot | ANSI to HTML converters; the HTML still needs a browser to become an image. ansi2html licence changed to LGPLv3+ in Nov 2017; aha licence not confirmed; termshot not assessed (no source found). | https://github.com/theZiz/aha ; https://github.com/pycontribs/ansi2html | Binary or package; all absent | Needs a browser for the image | LOW | EXTENDS: redundant with Rich `export_html`, already installed [CODE-VERIFIED, 05 section 2]. |
| 5.5.6 | cairosvg, rsvg-convert | `cairosvg.svg2png(url=..., parent_width=..., parent_height=...)`; needs the Cairo system library and Pillow; slim containers need extra OS packages. Rich SVG relies on `foreignObject` and `@font-face`, which non-browser rasterisers do not support; cairosvg itself was not tested on a Rich export (inference from issue 2153, which tested rsvg-convert and ImageMagick). | https://www.twilio.com/en-us/blog/developers/tutorials/product/sending-svg-images-sms-whatsapp-python-cairosvg ; https://phauer.com/2018/install-cairo-cairosvg-alpine-docker ; https://github.com/Textualize/rich/issues/2153 | New dev dependency plus system libcairo (presence not checked) | Offline after install, but likely not usable on Rich SVG | MEDIUM (negative finding) | SUPPORTS: modules and `rsvg-convert` absent [CODE-VERIFIED, 05 section 2]; libcairo presence [UNVERIFIED]. Do not plan on them without a test on a real Rich export. |
| 5.5.7 | Zellij `dump-screen --ansi` as a capture method | Text or ANSI per cell, no image (see 5.4.2). | https://zellij.dev/documentation/cli-actions.html | None; binary installed locally; CI presence unknown | Needs a live session; not CI-suitable today | MEDIUM | SUPPORTS 05's table row [CODE-VERIFIED by help text]; fidelity [UNVERIFIED]. |
| 5.5.8 | Text-first compare tier (no image) | Per-cell text and styles from Rich export or ANSI text can be diffed by a script or reviewer; an image is needed only for the visual score against the mockup PNGs. Fixed viewport and the same installed monospace font between runs keep reviewer scores stable (inference). | Derived from https://rich.readthedocs.io/en/stable/reference/console.html and https://zellij.dev/documentation/cli-actions.html; no direct source | None | Yes, offline today | HIGH | SUPPORTS: mockups exist as `.png`, `.ansi` and `.txt` per width (160, 116, 80) and `render_current.py` already writes per-width text and ANSI [CODE-VERIFIED, 05 section 4]. Today the rendered ANSI has 0 ESC bytes while the mockup `signal-bridge.ansi` has 48 lines with ESC, so ANSI diffing is meaningful only after styling lands [CODE-VERIFIED]. |
| 5.5.9 | Reviewer reading PNGs | Claude agents view PNG files with the Read tool; a fixed rubric file plus fixed-size per-width renders are needed (Playwright viewport is settable; freeze size flags not confirmed in the extract). | none external (local fact in web-02 section B7) | None | Works in a Claude session only | HIGH | EXTENDS. Whether a review subagent's Read shows a PNG reliably is [UNVERIFIED, not tested, 05 section 6]. Without a rasteriser the reviewer compares a mockup PNG against rendered text or ANSI, which is weaker (05 section 6). |

Contradiction check (rule 6): none between web-02 section B and 05 on tool availability; both agree no PNG renderer is installed and Rich export plus a browser is the only zero-dependency path. They differ in emphasis: web-02 recommends the Playwright MCP session route as the primary PNG step; 05 notes the same route does not exist in the repository or CI. 05 has the stronger evidence for what runs in CI; web-02's route is valid only for the interactive reviewer loop.

### 5.6 External Research Summary

All content here is external context weighed against the codebase files; codebase facts win on any conflict. No external finding contradicts a codebase fact outright; four are refinements or corrections of an external inference (rows marked below).

**Key external findings by question**

| Q | External finding (section) | Relevance | Relationship to codebase |
|---|---|---|---|
| Q1 | Keep the line model; add styling as `Text` plus `Span`s whose `.plain` equals today's line; Panel, Table, Columns and Layout replace the one-renderable-per-line structure (5.1.1, 5.1.2, 5.1.7). | HIGH | Supports; record and snapshot never touch Rich (`export.py`) |
| Q1 | `safe_box` is a legacy-Windows switch, not an ASCII switch; `--ascii` borders need an explicit box or hand-built ASCII glyphs; confirm `dir(rich.box)` first (5.1.3, 5.1.4). | MEDIUM | Partly contradicts the intent of `safe_box=policy.ascii` at `terminal.py:110-125`; box-name check [UNVERIFIED] |
| Q1, Q7 | `cell_len` is table-based; pad with `cell_len`, not `len`; keep chrome glyphs to box drawing and ASCII (5.1.6). | HIGH | Supports `cell_len`-based width logic in `render.py` |
| Q7 | In Rich, `crop` clips an over-wide token silently; `ellipsis` costs one cell; `fold` adds rows (5.1.5). In this code `wrap` runs before `render()`, so the 64-hex hash is not clipped today (measured whole at 160, 116, 80; Section 2.3). | HIGH | Supports `render.py:528` as a last-resort crop only; the hash claim is superseded by the code measurement |
| Q4 | `color_system` values and `auto` detection (`COLORTERM`, last part of `TERM`) are a cheap upgrade path above the pinned `"standard"` (5.2.1, 5.2.2). | HIGH | Extends `terminal.py:121-122` |
| Q4 | 16-colour downgrade is arithmetic and terminal-theme dependent, so hex roles collapse; design roles with named ANSI colours, dim, bold and a text or glyph cue (5.2.6, 5.2.7). | HIGH | Supports; collapse mapping [UNVERIFIED in this synthesis] |
| Q4 | Rich's `NO_COLOR` keeps bold and dim; the code's `color_system=None` drops all SGR (5.2.5). | HIGH | Extends; project choice, owner decision if it should change |
| Q5 | `export_text(styles=True)` ignores NO_COLOR and the downgrade; `console.file.getvalue()` is the correct styled one-shot capture (5.3.2, 5.3.3). | HIGH | Supports; [CODE-VERIFIED by probe] |
| Q5, Q7 | `Live(screen=True)` crops rows past height silently and pads width; no ellipsis; the footer is what is lost (5.3.5, 5.3.7). | HIGH | Supports; [CODE-VERIFIED by measurement]; docs ellipsis default does not apply under `screen=True` |
| Q5 | A `StringIO` console without `force_terminal` writes nothing for `Live(screen=True)`; live styled capture needs `force_terminal` plus a seam in `LiveScreen`, or a pty (`pexpect`) (5.3.3, 5.5.4). | HIGH | Extends web-01's capture recommendation |
| Q3 | Rich SVG is browser-only in practice; no PNG renderer is installed; the Playwright MCP route exists only in a Claude session; text and ANSI comparison works offline today (5.5.1, 5.5.2, 5.5.6, 5.5.8). | HIGH | Supports 05 sections 2 and 5 |
| Q3 | freeze is the simplest ANSI to PNG tool but is an extra binary (5.5.3). | MEDIUM-HIGH | Supports; needs approval and network at install |
| Q6 | Zellij is detectable by `ZELLIJ`; floating panes, `dump-screen --ansi`, themes and bars are documented; docs are ahead of the local 0.44.2; colour pass-through and runtime behaviour are unverified (5.4.1 to 5.4.8). | HIGH | Supports 05; Q6 position in the contradictions table |
| Q2 | No external source covers goldens; the external input is that a styled-capture gate must assert SGR in the stream: none under NO_COLOR, only 30-37, 90-97, 1 and 2 style codes at standard (web-01 Q5 recommendation). | MEDIUM | Extends; tests to change are in 02 section 8 |

**Contradictions and corrections between research files (rule 6)**

| Topic | Claim A | Claim B | Stronger evidence |
|---|---|---|---|
| Does a recording Console downgrade or strip colour in `export_text(styles=True)`? | web-02 B1, B8 and recommendation 1: a Console configured with a forced colour system or NO_COLOR should record downgraded styles (inference, untested) | 02 section 2: it does not; NO_COLOR still shows SGR in `export_text(styles=True)` | 02 (probe on Rich 15.0.0, 5.3) |
| `export_text(styles=True)` and NO_COLOR | web-01: inference to verify | 02: verified | 02 |
| Live overflow | Rich docs: ellipsis default | web-01 source reading and 02 measurement: rows cropped, no ellipsis under `screen=True` | 02 (measured) |
| Q6 Zellij | web-02: GO conditional | 05: no-go as harness or dependency | 05 for local state; both agree it is never a dependency (5.4) |
| Primary PNG step | web-02: Playwright MCP in the Claude session | 05: absent from repo and CI | 05 for CI; web-02's route valid for the interactive loop only (5.5) |
| Console capture needs `force_terminal`? | web-01: `force_terminal=True` | 02: not needed for `print`; needed for `Live(screen=True)` | 02 |

**Specific implementation implications (each tied to a cited location)**

1. `src/superclaude/cli/observe/render.py:524-531` `render()`: attach spans per role to each line; keep `.plain` equal to the current string; do not add `Console(` or `sorted(` there (test constraint per web-01, [UNVERIFIED] here).
2. `src/superclaude/cli/observe/commands.py:240-242`: replace `export_text()` with `console.file.getvalue()` for a styled one-shot, keep the plain route when `policy.no_color`; update `tests/observe/test_commands.py:121` (`"\x1b" not in out`); keep the record-path assertions (`test_commands.py:99, :105`; `tests/observe/test_export.py:53`).
3. `src/superclaude/cli/observe/terminal.py:110-125` `make_console`: single place for any `color_system` change (`"auto"` or tiers); replace `safe_box=policy.ascii` reliance with an explicit ASCII box choice after `dir(rich.box)`; add `force_terminal` as a parameter or inject the factory so `LiveScreen.draw` (`commands.py:270`) can be captured; keep `LiveScreen.shape` (`commands.py:265`) covering every style-affecting policy field.
4. Height: count every new frame row inside `screen_lines` `top`, `body` and `footer_height` (`render.py:499-502`); add a test `len(screen_lines(...)) <= policy.height` at 24, 40, 44 and `MIN_ROWS = 8`; reserve an own overflow row because Rich shows none.
5. Harness: extend `.dev/issues/409/visual-parity/inputs/tools/render_current.py` `emit` (lines 68-75) with `export_svg`/`export_html` and a stream capture; add a text and ANSI structural check first, then an image step only through the Playwright MCP session unless a new tool is approved.
6. Before any Zellij claim is relied on: run `zellij action dump-screen --help` and `new-pane --help` locally and a one-off background-session test, and test truecolor and 256-colour pass-through.

**Verification status roll-up**

| Tag | Items |
|---|---|
| [CODE-VERIFIED] | `make_console` options and `"standard"` pin; no `force_terminal` anywhere; `export_text()` plain at `commands.py:242`; `export_text(styles=True)` ignores NO_COLOR (probe); live bytes, crop, pad and no ellipsis (measured); Zellij 0.44.2 and `dump-screen` flags (help text); ANSI-16 theme; tool absence list |
| [CODE-CONTRADICTED] | web-02's inference that a recording Console carries the downgrade or NO_COLOR into `export_text(styles=True)` (corrected: it does not); docs' Live ellipsis default under `screen=True` (corrected: rows are cropped) |
| [UNVERIFIED] | `dir(rich.box)` names; `safe_box` no-effect probe and 16-colour collapse mapping (web-01 executor summary, not re-probed here); Zellij runtime behaviour, `send-keys` and `--create-background` on 0.44.2, colour pass-through, theme readability, command-pane layout syntax; Rich SVG in a rasteriser; PNG read by a subagent; licences of freeze, pyte, aha, cairosvg; libcairo presence; DejaVu Sans Mono glyph coverage; heights below 40 for a frame design |

**Key findings explicitly excluded**

| Finding | Rationale |
|---|---|
| web-02 B3 note that `brew install freeze` may install an unrelated cask | Single-source, unverified, and install method is irrelevant on this Linux host |
| termshot | No source found by web-02; not assessed |
| web-02 A3 zjstatus community status-bar plugin | Medium-reliability blog; the observer draws its own header and footer, so a custom Zellij bar does not affect parity |

Standing constraints check: every finding above leaves read-only behaviour, real data only, question text screen-only (record and snapshot unchanged, 02 section 5), NO_COLOR, ASCII and widths 160/116/80 intact; ANSI-styled output remains the primary rich mode; nothing external requires blinking or mouse input.

## 6. Options Analysis

### 6.0 Evidence conventions and contradictions between research files

| # | Contradiction or drift | Stronger evidence | Used in this report |
|---|---|---|---|
| 1 | R01 section 7 infers that slate and muted "can collapse"; R04 section 3 measured Rich's downgrade: standard-16 indexes base 15, slate 8, cyan 14, muted 7, amber 11, green 7, red 7, violet 7 (R04:63-76) | R04 (measured with Rich's own `Color.downgrade`; reproduced by two Gate 1 reviewers, GAPS row 12) | R04 table; R01's inference dropped. The collapse is muted + green + red + violet, not just slate/muted |
| 2 | R01 8.2 item 5 computes 114+1+42 = 157 of 160 [UNVERIFIED]; R04 section 4 measured the mockups: 1 + 114 + 2 + 42 + 1 = 160 | R04 (measured on the nine `.txt` files) | R04 widths (GAPS row 54) |
| 3 | FINDINGS M-06 says the full ledger is "153 cells"; code gives exactly 160 (render.py:159-192, `FULL_WIDTH` terminal.py:23) | Code (R01 4.3) | 160; "153" not stated as fact (GAPS row 9) |
| 4 | R01 lines 55 and 231 and R05 section 5 suggest `export_text(styles=True)` for styled capture; R02 section 2 probed that it ignores NO_COLOR and the standard-16 downgrade | R02 (probe, Rich 15.0.0) | `console.file.getvalue()` route (GAPS row 3, row 13) |
| 5 | R05 section 7 says no-go for Zellij; W02 recommendation 4 says "GO conditional" | Neither is exercised; R05 is stronger for local facts (binary, config, help text), W02 for documented features (external) | Both agree Zellij must not be a dependency of the render gate; the difference is wording. See 6.4 |
| 6 | Task prompt says three width classes; code has four: full (>=160), line (>=116), short (>=80), narrow (<80) (terminal.py:63-70) | Code | Four classes (GAPS row 10) |
| 7 | Assumption that `safe_box=policy.ascii` gives Rich boxes an ASCII fallback (terminal.py:123) | Probe in R01 and R03: a `Panel` prints identical rounded Unicode borders with `safe_box` True and False; `box=rich.box.ASCII` prints `+---+` [CODE-CONTRADICTED] | Explicit box or hand-built glyphs required (G-1) |
| 8 | W01 says Rich's own NO_COLOR keeps bold and dim; project code passes `color_system=None` under NO_COLOR, which drops bold too (R01 section 7 probe) | Code (project choice, not a Rich conflict) | Under NO_COLOR hierarchy must live in text and glyphs |
| 9 | FINDINGS M-10 attributes the header gate to `render()`; it is in `screen_lines`, render.py:497 | Code | Cite render.py:497 |

### 6.1 Decision Q1: how to compose styled spans, titled boxed panes, a count tile and two columns

Facts that bound every option [CODE-VERIFIED unless tagged]:

| Fact | Evidence |
|---|---|
| `screen_lines` returns `list[str]`; `render()` wraps each in `Text(line, no_wrap=True, overflow="crop")`; no function in render.py returns a Text, Table, Panel, Layout or Columns; render.py imports only `cell_len`, `Group`, `Text` | R01:44-52, render.py:524-531 |
| `tests/observe/test_render.py:399` pins `len(group.renderables) == len(screen_lines(...))`; `:401-404` regex-bans `observe.adapter/collector/parse`, `sorted(`, `.sort(`, `from_markup`, `Console(` in render.py | R03:36, R01:53 |
| `record_text` and `snapshot_json` are built in export.py from `View` fields; export.py imports no Rich (test_export.py:238-243); question text (`q.shown`, `desk.ask`) is read only by render.py and view.py | R02:75-94 |
| M-05, M-08, M-13, M-14 touch strings that `record_text` and the goldens also read (`counts_line` view.py:761, `header1` view.py:914-921) so they must be render-only | R01:221 |
| The full 160 ledger table uses all 160 cells (2 + 114 + id 22 + flags 12 + 10 separators); only `flags` is elastic | R01:85 |
| Every candidate frame glyph (`╭ ╮ ╰ ╯ ┏ ┓ ┗ ┛ │ ┃ ─ ━ █ ▌ ▸ · ◆`) measures `cell_len == 1` in Rich 15; Rich `Text` spans are character indexes while widths are cells | R01:210 |
| Mockup geometry (measured): 160 ledger 114 + 42; 116 ledger 70 + 42; 160 desk 76 + 80; 116 desk full-width question over 66 + 46; 80 all single column, 78-wide panes | R04:85-99 |

#### Option A: hand-built lines plus a separate styling pass

**Description.** Extend `_panel_lines` and `_desk_lines` in render.py to draw box characters and composed columns as plain strings; a second pass over the finished strings maps spans to Rich styles.

**How it works.**
1. Add box glyph names to `GLYPHS` (terminal.py:30-34: only `selected`, `truncate`, `hrule` exist today) with ASCII forms `+`, `-`, `|` (G-1); new glyphs go through `glyph()` because `ascii_safe` turns any literal non-ASCII character into `?` (terminal.py:133-135).
2. A helper `frame(title, lines, width, policy)` next to `_pad` and `_cell` (render.py:83-88) builds `top`, `side` and `bottom` lines; inner width = pane width minus 2 (border) or 4 (border plus one-cell padding). Every `wrap` and `clip` call that feeds a pane receives the inner width.
3. Two columns: `zip_longest(left, right)` with each row `_pad(l, wl) + gap + _pad(r, wr)` using `cell_len`.
4. Each frame adds 2 rows (top and bottom border) to the height terms at render.py:438-457 and 499-503.
5. A styling pass in `render()` recovers roles from the strings (token match for `unknown`, `unavailable (no source)`, state words; column offsets replayed from `_columns`).

| Assessment | |
|---|---|
| Effort | L |
| Risk | Medium to High. The styling pass has to recover roles from strings: a token match can hit free text and worker-controlled text (`unknown` also appears in `age unknown`, `source counts: unknown`); column offsets must come from ordered segment building, not cell widths, because a wide character makes offsets drift (R01:212). Frame rows not counted in `reserved` are silently cropped from the bottom on the live screen, taking the footer key list and `shown x/y` with them (R02:197-198) |
| Reuse of existing code | High: keeps `screen_lines`, `wrap`, `clip`, `_cell`, `_pad`, the `render()` one-Text-per-line shape and every `cell_len` width rule |
| Files and systems affected | render.py (`_panel_lines`, `_desk_lines`, `_question_line`, `counts_lines`, `_columns`, sizing 433-479, `render`), terminal.py (`GLYPHS`), tests/observe/test_render.py, test_commands.py, test_question_cap.py, test_inspector_scroll.py, both goldens |
| Pros | Keeps test_render.py:399 and the source guard valid; text identical across colour, NO_COLOR and exports; width maths stay in `cell_len`; ASCII box mapping is exact and controllable |
| Cons | Regex or offset role recovery is fragile and can style worker text by accident; every width and height term must be reduced by hand; `-` is both the ASCII `hrule` and the ASCII border, so rule and border are visually ambiguous in ASCII (R01:214) |

#### Option B: Rich renderables (Panel, Table, Columns, Layout) assembled in `render()`

**Description.** `render()` returns Rich `Panel`, `Table.grid`, `Columns` or `Layout` objects; Rich computes widths, borders and titles. `screen_lines` must still be derivable as the text contract.

**How it works.** `Panel(..., box=HEAVY | ROUNDED | ASCII, border_style=..., title=...)` for panes; `Table.grid` or `Layout` for 114 + 42 and 76 + 80 splits; `rich.box.ASCII` selected explicitly when `policy.ascii`; a second plain-line source kept for tests, records and `--once`.

| Assessment | |
|---|---|
| Effort | XL |
| Risk | High. Breaks `test_render.py:399` (one renderable per screen line) and the `--once --width` equality tests; heights are known only after `console.render_lines`, so the budgeting at render.py:438-457 and 499-503 needs rendered line counts (R01:215); `Table.grid` and `Columns` size columns by content unless widths are fixed, which reintroduces the column drift `_columns` avoids on purpose (FINDINGS M-17, R01:215e); Rich `Text` overflow does not reproduce the `>` and `...` markers the spec requires (R01:215c) |
| Reuse of existing code | Low: `wrap`, `clip`, `_cell`, `_row_line` become plain-text mirrors rather than the source of what is printed |
| Files and systems affected | render.py (rewrite of the composition), commands.py (`--once --width` export path), test_render.py, test_commands.py, both goldens; a plain-line twin of every pane |
| Pros | Rich handles cell widths, titles and box styles; `box.ASCII` gives `+---+` (probe, R03:194); fewer hand-written width formulas |
| Cons | `safe_box` does not ASCII-ize a Panel (explicit `box=rich.box.ASCII` needed) [CODE-CONTRADICTED assumption]; `box.HEAVY` existence in the installed Rich 15.0.0 was not confirmed (W01 says check `dir(rich.box)`) [UNVERIFIED]; R03 section 6 rates this phase "not recommended before P1 to P4 prove out" (R03:204; research 03's own labels, not the P0 to P7 scheme of Section 8); `screen_lines` stops being the byte source of what is printed |

External context (W01): Rich keeps content and style separate (`Text` plus `Span`s), so a styled line can keep an unchanged plain string; W01 recommends the line model plus a thin style layer over Table, Layout and Columns, because those replace the one-Text-per-line structure the tests require. Source: https://github.com/Textualize/rich/blob/v15.0.0/rich/text.py and https://rich.readthedocs.io/en/stable/console.html.

#### Option C: hybrid, a line-based text model that stays the source of truth plus a role map that Rich draws

**Description.** The plain-line model (`wrap`, `clip`, `_cell`, `_pad`, frame glyphs through `GLYPHS`) stays the authority for text, width and height. The line builders also record a role per line or per segment, so a parallel function returns one `Text` per line whose `.plain` equals today's string. `screen_lines` becomes `[t.plain for t in styled_lines]`; `render()` draws the styled `Text` lines. One theme table, fed only by `TerminalPolicy`, holds every role-to-style mapping.

**How it works.**
1. Builders emit `(text, role)` segments (for example `Text.append(text, style)` in segment order), so roles are never recovered by regex and offsets never come from cell widths.
2. `wrap` and `clip` keep their `>` and `...` markers and operate on `.plain`; spans are re-applied after clipping (clip returns a plain `str`, R01:20).
3. Frames are hand-built lines (as Option A) so heights stay countable in `screen_lines`.
4. The theme table reads only `policy.no_color` and `policy.ascii` (test_terminal.py:181-198 forbids the text `NO_COLOR`, `COLUMNS` or `Console(` in other modules).
5. One renderable per line is kept, so `test_render.py:399` holds.

| Assessment | |
|---|---|
| Effort | L |
| Risk | Medium. Widest builder refactor (`wrap`, `clip`, `_cell`, `_pad`, `counts_lines`, `_panel_lines`, `_desk_lines`, `_row_line`, `_header_lines` all return `str` today, R01:213); mitigated by staging: P1 can start with line-level roles on the existing `Text` per line and grow to segments |
| Reuse of existing code | High: all width and wrap authorities and the `render()` shape are kept |
| Files and systems affected | render.py, terminal.py (`GLYPHS`, theme table, colour policy), commands.py (capture route only, see 7.2 Q5), tests/observe/test_render.py (one test rewritten in P1), both goldens by phase |
| Pros | Smallest golden churn: a style-only phase changes only the 15 `printed_*` values and one test, and nothing in `golden_questions_linkoff.json` (R03:157, 200); roles cannot hit worker text because they are assigned at build time; one place for the theme; plain text for records, NO_COLOR and ASCII stays identical by construction |
| Cons | More builder code than Option A's pass; `Text` spans are character indexes, so builders must append in order; a role table that is out of step with a later text change silently mis-styles |

#### Options comparison: composition (Q1)

| Criterion | A hand-built plus style pass | B Rich renderables | C hybrid (text model plus roles) |
|---|---|---|---|
| Effort | L | XL | L |
| Keeps `test_render.py:399` and source guard | Yes | No (399 fails) | Yes |
| Plain text for records, JSON, NO_COLOR, `--once` | Unchanged | Needs a plain twin | Unchanged (`.plain`) |
| Role assignment | Recovered from strings (fragile) | By Rich objects | At build time (exact) |
| Height budgeting | By hand, +2 rows per pane | Needs rendered line counts | By hand, +2 rows per pane |
| ASCII panes (G-1) | `GLYPHS` + `+ - \|` | explicit `box=rich.box.ASCII` | `GLYPHS` + `+ - \|` |
| Two columns (O-1) | `zip_longest` with `cell_len` | `Table.grid`/`Layout`, fixed widths required | `zip_longest` with `cell_len` |
| Golden churn for a style-only phase | 15 `printed_*` values + 1 test (the plan keeps them plain by stripping SGR in `release1_surface.py` `_printed`, so no golden is regenerated; synth-05 step 1.6(c)) | Both goldens fully | 15 `printed_*` values + 1 test (same strip route) |
| Main risk | Styling worker text by token match | Test and budget rewrite | Builder refactor size |

### 6.2 Decision Q3: the render harness and the fixed-rubric reviewer

Facts [CODE-VERIFIED unless tagged]:

| Fact | Evidence |
|---|---|
| Installed: Rich 15.0.0 (`export_text`, `export_svg`, `export_html`), node v24, `pexpect` 4.9.0 (declared, pyproject.toml:41). Absent: PIL, cairosvg, pyte, playwright, fontTools, chromium, rsvg-convert, inkscape, ImageMagick, freeze, termshot, aha, ansi2html | R05:49-68, 76 |
| No render, screenshot or observe Makefile target; no image dependency in pyproject.toml | R05:76-77 |
| `render_current.py` (94 lines) already writes `current/<w>/{ledger,questions,desk}.txt` and `ansi-*.txt` per width at `HEIGHT = 50`, but via `export_text(styles=True)`, which bypasses NO_COLOR and the standard-16 downgrade | R04:187-196, R02:35 |
| Mockup frame heights are 48 (160) and 42 (116, 80); the harness height is 50 | R04:87, R05:84-88 (GAPS row 14) |
| The nine mockups exist as `.png`, `.ansi` and `.txt`; both Gate 1 reviewers read mockup PNGs with the Read tool successfully | R05:92, GAPS row 40 |
| `LiveScreen` has no test; a `make_console` StringIO console writes nothing for `Live(screen=True)`; pty route (`pexpect`) measured with a stand-in child | R02:159-199, R03:81 |

External context (W02): Rich SVG export works fully only in Chromium-based browsers (`foreignObject` plus a remote `@font-face`); `rsvg-convert` and ImageMagick failed on it in https://github.com/Textualize/rich/issues/2153 (Rich 12.1.0; whether Rich 15 changed this is [UNVERIFIED]). freeze (https://github.com/charmbracelet/freeze) renders ANSI to PNG but is an extra binary. pyte (https://pyte.readthedocs.io) emulates a terminal but makes no image. Playwright needs a downloaded browser; the Playwright MCP browser exists only inside the Claude session (R05:108).

#### Option H1: Rich export to SVG or HTML, then a headless renderer to PNG

**Description.** Extend `render_current.py` `emit()` (line 73 already holds the recording console) with `console.export_svg(...)` or `export_html(...)`, then open the file in a headless browser at a fixed viewport and screenshot it.

**How it works.** Per width and screen: record through a console built by `make_console` with a forced colour system, export HTML or SVG, rasterise in the Claude session through the Playwright MCP browser, hand the PNG to the reviewer next to the mockup PNG.

| Assessment | |
|---|---|
| Effort | S for the export (a few lines in `emit()`); M for a repeatable PNG step |
| Risk | Medium to High. The PNG step has no offline repo-level tool; the end-to-end path (export file opened in the MCP browser, glyph widths with DejaVu Sans Mono) was not run [UNVERIFIED]; fonts must be identical between runs or scores vary on glyph metrics (W02 inference) |
| Reuse of existing code | High: `render_current.py`, `make_console`, `render` |
| Files and systems affected | `.dev/issues/409/visual-parity/inputs/tools/render_current.py`; a new harness script; no `src/` change |
| Pros | Image-to-image comparison for the visual score; no new Python dependency for the export |
| Cons | Not runnable in plain CI (no browser, no network-tested install, GAPS row 39); `export_svg` and `export_html` do not exercise NO_COLOR or the colour system (W01:35) so they cannot be the NO_COLOR test |

#### Option H2: ANSI to PNG with an extra tool (freeze, or pyte plus an image library)

**Description.** Capture ANSI text per width, convert with a vendored binary or a Python emulator plus Pillow.

**How it works.** Capture `console.file.getvalue()` through `make_console`; feed to `freeze -o out.png` (disable window chrome and padding) or to `pyte.Screen` plus Pillow.

| Assessment | |
|---|---|
| Effort | M to L |
| Risk | High. Every tool is absent (R05:54-61); installability, cairo system library, licences (freeze, pyte, aha, cairosvg) and network at install time are all unconfirmed [UNVERIFIED]; adds a dependency the repo does not carry |
| Reuse of existing code | Medium: reuses the capture, not the render of the image |
| Files and systems affected | pyproject.toml (a new dev extra) or a vendored binary, Makefile (new target), CI image |
| Pros | Repo-level, scriptable PNG that works without the Claude session once installed; freeze is a single static binary (W02) |
| Cons | New dependency and a new approval; freeze adds window chrome by default; behaviour with the observer's glyphs was not tested |

#### Option H3: text and ANSI-escape assertions plus a model-judged fixed rubric

**Description.** Script structural checks on plain text and captured ANSI bytes; a fresh reviewer agent scores the output against the mockup PNG, using a fixed rubric file.

**How it works.**
1. Capture styled bytes with `console.file.getvalue()` through `make_console` (NO_COLOR-correct and down-converted, R02:35-38); capture the live path with a pty (pexpect, route B) or a `force_terminal` console seam (route A) (R02:188-190).
2. Scripted checks per width 160/116/80 and per mode (colour, NO_COLOR, ASCII): every line `cell_len <= width`; `len(lines) <= policy.height` at 24, 40 and 44 rows and at `MIN_ROWS = 8`; zero `\x1b` under NO_COLOR; only SGR codes valid for the depth; no SGR 5 or 6 (blink); ASCII output `.isascii()`; `screen_lines` unchanged by colour; question text absent from `record_text` and `snapshot_json`.
3. Reviewer: Read the mockup PNG (R05:113-116) and the rendered text or ANSI; score each rubric row on a fixed scale.
4. Fixed rubric rows (drawn from R04): the eight colour roles and bold use (R04:42-57); pane geometry per width (R04:89-99); title and badge (M-13); count tile (M-05); selected-question glyph (M-18, scored against RR 50 because the mockups draw no selected row, GAPS row 29); muted absent values (M-08); no blink; NO_COLOR and ASCII parity.

| Assessment | |
|---|---|
| Effort | S to M |
| Risk | Low to Medium. Reviewer compares a PNG (image) with text or ANSI (text), which is weaker than image-to-image (R05:115); rubric drift between runs is controlled only if the rubric file and the font are fixed |
| Reuse of existing code | High: `render_current.py` (with the capture fixed to `getvalue()` and per-width heights set to 48, 42, 42), `console_factory` (tests/observe/conftest.py:221-229), `printed()` helpers |
| Files and systems affected | `render_current.py`, a rubric file, new tests under tests/observe/, optionally a Makefile target |
| Pros | Runs offline today, in CI, with no new dependency; catches NO_COLOR, ASCII, width, height and blink regressions mechanically; the only option that checks bytes |
| Cons | Does not by itself show what a person sees; relies on a model judgement for visual parity |

#### Options comparison: harness (Q3)

| Criterion | H1 export + headless render | H2 ANSI to PNG tool | H3 text/ANSI + rubric |
|---|---|---|---|
| Effort | S export, M PNG | M to L | S to M |
| Works offline in CI today | No | No | Yes |
| New dependency | None for export; browser for PNG | Yes | None |
| Checks NO_COLOR and depth bytes | No | Only if fed `getvalue()` | Yes |
| Image-to-image reviewer input | Yes (in session) | Yes | No |
| Verified end to end | No [UNVERIFIED] | No [UNVERIFIED] | Parts verified (probes in R02) |

### 6.3 Decision Q4: ANSI colour depth

Facts [CODE-VERIFIED unless tagged]:

| Fact | Evidence |
|---|---|
| `make_console` sets `color_system=None if policy.no_color else "standard"` (terminal.py:121); no COLORTERM, TERM or isatty check in terminal.py | R01:17-18 |
| Probe, `bold #ff8800`: standard gives `\x1b[1;91m`; 256 gives `\x1b[1;38;5;208m`; truecolor gives `\x1b[1;38;2;255;136;0m`; `auto` on a StringIO file resolves to no colour | R01:173-176 |
| Rich caches a `Style`'s ANSI codes per Style object, so inside one process the first colour system used for a Style wins; test helpers building different systems in one process can see stale codes | R01:177 |
| Mockups use 8 truecolor foregrounds (`38;2;R;G;B`) plus bold, no background code, no dim | R04:38-57 |
| Standard-16 downgrade of the mockup RGB values: base 15, slate 8, cyan 14, muted 7, amber 11, green 7, red 7, violet 7; 256 indexes 189, 60, 80, 145, 214, 115, 210, 147 | R04:63-76 |
| Under NO_COLOR the console drops bold with colour (`color_system=None`) | R01:179 |

External context (W01): Rich `color_system` accepts None, `"auto"`, `"standard"`, `"256"`, `"truecolor"`, `"windows"`; `auto` reads `COLORTERM` (`truecolor` or `24bit`) and then the last part of `TERM` (https://rich.readthedocs.io/en/stable/console.html, https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py). The first 16 colours are defined by the user's terminal theme (https://rich.readthedocs.io/en/stable/appendix/colors.html).

#### Option D1: keep `standard` (16 colours) with explicit named roles

**Description.** Leave `make_console` at `"standard"`; define every role with a named ANSI colour plus bold, plus a text or glyph cue.

**How it works.** Theme table maps roles to named styles (for example amber to `yellow`, slate to `bright_black`, cyan to `cyan`, green `green`, red `red`, violet `magenta`) instead of the mockup RGB values, so the collapse of muted, green, red and violet to index 7 (R04:76) does not occur. The named mapping is a design choice, not code today [UNVERIFIED as a legible palette; not observed on a terminal].

| Assessment | |
|---|---|
| Effort | XS to S for the console, S for the theme table |
| Risk | Low. Muted versus base is only 7 versus 15 and slate versus muted 8 versus 7 depends on the terminal theme (R04:76); state colour cannot be the sole carrier (raw state words stay printed, RR 31 and 71) |
| Reuse of existing code | Total: terminal.py:121 unchanged |
| Files and systems affected | terminal.py (theme table), render.py (role lookup), tests asserting SGR codes |
| Pros | No detection code; stable in the pinned tests (`printed()` bytes identical across machines); fits 16-colour Zellij themes (R05:30) |
| Cons | Does not reach mockup parity in hue (amber becomes yellow); wastes truecolor terminals |

#### Option D2: detect 256 or truecolor through COLORTERM and TERM, with a 16-colour fallback

**Description.** `make_console` (or `resolve_policy`) chooses `truecolor`, `256` or `standard` from `COLORTERM` and `TERM`; the theme holds one role set per depth (mockup RGB at truecolor, 256 indexes, named 16-colour roles).

**How it works.** `COLORTERM` of `truecolor` or `24bit` selects truecolor; `TERM` ending in `256color` selects 256; otherwise standard; `no_color` keeps `color_system=None`. Detection lives in terminal.py (the only module allowed to read the environment, test_terminal.py:181-198). Rich's own `"auto"` does the same detection (W01) but returns None for a non-terminal file (R01:176), so a styled capture would need an explicit system or a forced terminal.

| Assessment | |
|---|---|
| Effort | M |
| Risk | Medium. Three role sets to keep in step; the Rich per-Style code cache can make tests that build consoles of different depths in one process see stale codes (R01:177); the real terminal capability and light-background behaviour are not observed [UNVERIFIED] (GAPS rows 2, 32) |
| Reuse of existing code | Medium: `TerminalPolicy` gains a depth field (currently none, terminal.py:37-51) |
| Files and systems affected | terminal.py (`TerminalPolicy`, `resolve_policy`, `make_console`), render.py theme lookup, test_terminal.py, LiveScreen `shape` tuple (commands.py:265, must include the depth) |
| Pros | Mockup-faithful colour on capable terminals; the 16-colour tier stays legible |
| Cons | More code and test matrix (3 depths x NO_COLOR x ASCII x 3 widths); `shape` rebuild logic must cover depth |

#### Option D3: pass mockup RGB through a single palette and let Rich downgrade

**Description.** Use the mockup hex values and set `color_system="auto"` or keep `standard`.

**How it works.** One palette; Rich picks the nearest colour at write time.

| Assessment | |
|---|---|
| Effort | XS |
| Risk | High. At 16 colours muted, green, red and violet all land on index 7 (R04:76); state colours would be indistinguishable by colour alone [CODE-VERIFIED by Rich's downgrade, not by terminal observation]; `auto` writes no colour to a non-terminal file so captures stay plain (R01:176) |
| Reuse of existing code | Total |
| Files and systems affected | terminal.py, render.py theme |
| Pros | Smallest change |
| Cons | Fails G-2 (theme must stay distinct at the real depth) at the standard tier |

#### Options comparison: colour depth (Q4)

| Criterion | D1 keep standard, named roles | D2 detect with fallbacks | D3 RGB through downgrade |
|---|---|---|---|
| Effort | XS to S | M | XS |
| Distinct roles at 16 colours | Yes if roles are named per depth | Yes (16-colour tier named) | No (4 roles collapse to 7) |
| Mockup hue parity on capable terminals | No | Yes | Partly |
| Test and capture stability | High | Medium (Style cache, depth matrix) | Medium |
| G-2 satisfied | Yes | Yes | No |

### 6.4 Decision Q6: Zellij 0.44.2

Facts. Local [CODE-VERIFIED by command output]: `zellij 0.44.2` at `/usr/local/bin/zellij`; config minimal; theme `aidev02` uses ANSI-16 integers only; `default.kdl` draws a 1-row tab bar and a 2-row status bar (R05:11-31); help text lists `run -f --width --height -x -y`, `action dump-screen --ansi`, `--layout-string`. No session was started, so floating-pane behaviour, `dump-screen --ansi` fidelity, command panes in a layout and CI presence are [UNVERIFIED] (R05:133-138). The observer sizes itself by polling `shutil.get_terminal_size` on every draw and rebuilds the `Live` on a shape change (R02:53), so it adapts to a pane's size without Zellij-specific code [CODE-VERIFIED]. The Zellij pane frame cost in rows and columns is [UNVERIFIED] (GAPS row 42).

External context (W02): `floating_panes { pane x y width height }` and `pane command="..."` in layouts (https://zellij.dev/documentation/creating-a-layout.html); `dump-screen -a/--ansi` (https://zellij.dev/documentation/cli-actions.html); `ZELLIJ`, `ZELLIJ_PANE_ID`, `ZELLIJ_SESSION_NAME` set in every pane (https://zellij.dev/documentation/nested-sessions.html, https://github.com/zellij-org/zellij/issues/3637); docs describe a newer release (0.46.0 announced 2026-11-11, https://zellij.dev/news/terminal-inbox-session-previews) than the local 0.44.2, so documented flags may not exist locally; no source found for Zellij's truecolor or 256-colour pass-through.

#### Option Z1: adopt Zellij as a dependency (render harness and required runtime)

**Description.** Run the observer in a Zellij session for capture and require it.

**How it works.** `zellij attach --create-background`, `new-pane`, `send-keys`, then `dump-screen --pane-id ... --ansi` (W02, 0.44.0 CLI per release notes).

| Assessment | |
|---|---|
| Effort | L |
| Risk | High. Behaviour unexercised; Zellij re-renders cells and applies its theme, so a dump is not byte-for-byte the observer's output (W02 inference); not guaranteed in CI (install here is provisioned from `/etc/skel`); `dump-screen` yields text, not an image |
| Reuse of existing code | Low |
| Files and systems affected | A new harness, CI image, layouts |
| Pros | Headless capture without a pty library |
| Cons | Violates "observer works standalone"; does not remove the need for a PNG renderer (R05:127-129) |

#### Option Z2: adopt as an optional layout and manual check only

**Description.** Ship or document a layout that places the observer in a pane (tiled or floating); the observer detects `ZELLIJ` at most as a hint and never requires it; `dump-screen --ansi` used as a manual second capture.

**How it works.** A KDL layout with a `pane command="superclaude" { args "observe" ... }` (syntax from W02, not verified against 0.44.2 [UNVERIFIED]); the policy continues to read the real pane size.

| Assessment | |
|---|---|
| Effort | S |
| Risk | Low, once a one-off session test is done on 0.44.2 before relying on any documented flag (W02 recommendation 5) |
| Reuse of existing code | High: the observer is unchanged |
| Files and systems affected | An optional layout file (outside `src/`); docs |
| Pros | Meets the conditions: standalone outside Zellij, read-only, all widths, NO_COLOR and ASCII (Zellij only wraps the program in a pane, R05:125) |
| Cons | Adds a manual verification burden; chrome rows and columns (tab bar 1, status bar 2, frame) reduce the area, so a pane may fall to the `line` or `short` class |

#### Option Z3: do not adopt

| Assessment | |
|---|---|
| Effort | XS |
| Risk | Low; no unverified dependency |
| Reuse of existing code | Total |
| Files and systems affected | None |
| Pros | Nothing unverified enters the plan |
| Cons | Gives up an optional presentation environment and a second manual capture method |

#### Options comparison: Zellij (Q6)

| Criterion | Z1 dependency | Z2 optional layout only | Z3 not adopted |
|---|---|---|---|
| Effort | L | S | XS |
| Keeps observer standalone and read-only | No | Yes | Yes |
| Evidence status | Unexercised | Help text and docs only | n/a |
| Removes the PNG-renderer need | No | No | No |
| Fit with the stated conditions | Fails | Meets | Meets |

## 7. Recommendation

### 7.1 Recommended option per decision

| Decision | Recommended | Rationale (comparison tables in 6.1 to 6.4) | Trade-off accepted |
|---|---|---|---|
| Q1 composition | Option C: line-based text model stays the source of truth, builders record roles, Rich draws one styled `Text` per line; frames and columns hand-built from `GLYPHS` | Only C and A keep `test_render.py:399` and the source guard valid and keep `record_text`, `snapshot_json` and NO_COLOR text untouched; C beats A because roles are assigned at build time instead of recovered from strings, so worker text cannot be styled by accident (R01:212-213). B is XL and fails 399 (R03:36, 204). External context agrees: W01 recommends the line model plus a thin style layer over Table, Layout and Columns | A larger builder refactor than A's string pass; start with line-level roles on the existing per-line `Text` in the style-only phase and grow to segments |
| Q3 harness | Option H3 as the gate (offline: scripted byte and structure checks plus a fixed-rubric reviewer reading the mockup PNG); H1 only as an in-session extra after one end-to-end trial | H3 is the only option that runs offline today, checks NO_COLOR, ASCII, depth and blink bytes, and needs no dependency; H1 and H2 need a rasteriser the repo and CI lack (R05:54-61) | Image-to-image comparison is not part of the gate; the reviewer compares a PNG with text or ANSI |
| Q4 colour depth | Option D2 delivered in two steps: first the named 16-colour roles (that is D1) as the floor, then COLORTERM and TERM detection for 256 and truecolor. Pending the owner's depth answer (7.3) | D3 fails G-2 (4 roles collapse to index 7, R04:76); D1 alone leaves truecolor terminals without the mockup palette | Three role sets and a depth-by-mode test matrix; Rich's per-Style code cache needs one console depth per test process (R01:177) |
| Q6 Zellij | Option Z2: optional layout and manual check only; not a dependency of the render gate or the observer | Evidence is help text and docs only (R05:133-138, W02); the observer already adapts to any pane size (R02:53); Z1 fails "standalone" | Needs one session test on 0.44.2 before any Zellij flag is relied on |

Recommended sequence. The phase scheme is the P0 to P7 scheme of Section 8 (the implementation plan, synth-05), which is the plan of record; this list mirrors it and every golden-per-phase assignment below is the one in Section 8. Each phase leaves `uv run pytest tests/observe/ -q` green (baseline 766 passed, R03:220):

1. P0, harness, rubric, baseline and pinning tests (no `src/` change): the `render_current.py` fix to capture `console.file.getvalue()` through `make_console` at heights 48, 42, 42, the `render_compare.py` harness with the scripted checks (H3), the rubric file; the 64-hex plan-ask test and a long-path desk-field test (R03:179-183), a second fixture with a hash trailing a long path and file list (GAPS row 5), an SGR-stripping helper, and a `len(screen_lines) <= policy.height` test at 24, 40, 44. No golden changes.
2. P1, style only: theme table, colour-depth detection, role spans on the per-line `Text` in `render()`; rewrite `test_render.py:250-259` to compare SGR-stripped colour output with NO_COLOR output; `release1_surface.py` `_printed` strips SGR so the 15 `printed_*` values keep their plain bytes; add the styled-capture gate (one-shot and pty). Neither golden is regenerated.
3. P2, text and budget fixes: M-10 heading at 116 and 80 (render.py:497 and the `ledger_fixed` term at :438-440; `reserved` at :499-501 reads `len(body)`, which already holds the heading rows), M-11 uncut key list (`_help_lines` 304-308), M-15 key pairs, M-16 token cut, M-13 badge split; a never-regenerated records golden is split off first, then both presentation goldens are re-baselined under the owner decision D-2.
4. P3, frame primitive and single-column titled panes on the questions-on screens, with ASCII `+ - |` glyphs from `GLYPHS`; every `wrap` and `clip` gets the inner width; every height term gains 2 rows per frame; the link-off golden is regenerated, the release-1 golden is not.
5. P4, two-column questions screen, count tile and RETAIN CONTEXT pane at 160 and 116 (80 stays stacked), behind O-1; link-off golden regenerated.
6. P5, two-column Decision Desk (160: 76 + 80; 116: question over 66 + 46; 80: three stacked panes), behind O-1; no golden changes.
7. P6, ledger panes (questions off); the release-1 golden is regenerated.
8. P7, spec reconciliation, final gate matrix and the PR. The Z2 Zellij layout is an optional manual check inside P7, after a session test.

Splitting the two-column work by width (160 first at 114 + 42 and desk 76 + 80, then 116 at 70 + 42 and desk 66 + 46; in P4 each width gives its own link-off golden diff) is this report's derivation from R03:202 (which gates "160 only") and the O-1 scope (160 and 116), and may be applied as an ordering inside P4 and P5; it is not stated in the research.

#### Width and height budgets at 160, 116 and 80 (Q1)

| Width class | Content layout from the mockups (R04:89-99) | Arithmetic | Current code constraint |
|---|---|---|---|
| 160 full | Ledger screen 114 + 42; desk 76 + 80; bridge 46 + 74 + 34 | 1 + 114 + 2 + 42 + 1 = 160; 1 + 76 + 2 + 80 + 1 = 160 | The 11-column table already uses all 160 cells; a framed table would need `flags` (elastic, 12 at 160) to give up 2 to 4 cells (R01:85, 138) |
| 116 line | Ledger screen 70 + 42; desk full-width question over 66 + 46 | 1 + 70 + 2 + 42 + 1 = 116; 1 + 66 + 2 + 46 + 1 = 116 | `line` layout id column up to 60 (render.py:195) must be reduced; M-17 blank band is in the same line |
| 80 short | Single column, 78-wide panes (inner 74 with `┃ ` and ` ┃`, R04:204) | 1 + 78 + 1 = 80 | Header, counts and key list need new wrapping rules (M-11, M-16) |

| Height rule | Evidence |
|---|---|
| Mockup frames are 48 rows (160) and 42 rows (116, 80); RR line 13 states the 44-row contract; code uses `policy.height` (render.py:447) | R04:87, 110 |
| The base fixture at height 40 already fills 40 rows at all three widths, so each added frame row removes one ledger row | R01:122-124, R02:198 |
| The questions block (title to retention) takes 12 lines at 160 and 13 at 116 and 80 before the ledger title; a frame adds 2 rows per pane | R01:125 |
| No final `lines[:height]` clamp exists; `Live(screen=True)` crops silently from the bottom and drops the footer key list and `shown x/y` with no ellipsis | R01:126, R02:179-198 |
| Frame cost at 24, 12 and `MIN_ROWS = 8` is not measured [UNVERIFIED] | GAPS row 7 |

### 7.2 Direct answers to Q1 to Q7

| Question | Answer | Evidence | Confidence and remaining caveat |
|---|---|---|---|
| Q1 composition; width and height budgets; records, JSON snapshot, NO_COLOR, ASCII | Use Option C. Records and the JSON snapshot are unchanged because export.py reads `View` fields only, imports no Rich and writes ids, times and counts (never question text); M-05, M-08, M-13 and M-14 must be render-only (do not edit `counts_line` view.py:761 or `header1` view.py:914-921). NO_COLOR: `color_system=None` drops bold as well as colour, so hierarchy must live in text and glyphs; the plain text is identical in all modes because styles are added after the plain line exists. ASCII: add box glyph names to `GLYPHS` with `+ - \|` forms; a Rich Panel would need explicit `box=rich.box.ASCII` (`safe_box` does not do it). Width and height budgets: see the tables in 7.1 | R01:18-19, 53, 85, 138, 186-221; R02:75-94, 131-139; R04:63-78, 85-99; R03:36; export.py:71-224; terminal.py:30-34, 121-123 | High for records, JSON and NO_COLOR (code and probes). Medium for frame arithmetic at 116 and 80 (mockup-measured, not yet built). Caveat: heights below 40 and the framed 160 table are unmeasured [UNVERIFIED] |
| Q2 tests and goldens per phase; phase split | The phase scheme is the P0 to P7 scheme of Section 8 (synth-05, the plan of record); the list below mirrors it. P0 tests and harness only, nothing changes, no golden. P1 style: one test rewritten (`test_render.py:250-259`) and `release1_surface.py` `_printed` made SGR-free, so `golden_release1_surface.json` (15 `printed_*` values and all 30 `lines_*`) and `golden_questions_linkoff.json` are untouched. P2 text and budget: literals in test_render.py, test_view.py, test_export.py, KEYS_LITERAL; a never-regenerated records golden is split off, then both presentation goldens re-baselined. P3 frames on the questions-on screens: whole-line tests (`GAP_NOTICE in lines`, `DESK_TITLE in lines`, `"/ab" in lines`, `startswith("dispatchId:")`, `startswith("▸ ")`, `endswith("reason unknown")`, the desk slice `desk[2:...]`), `test_commands.py:672-675, 690`, vertical-budget tests; link-off golden regenerated, release-1 golden not. P4 two-column questions screen, count tile, RETAIN CONTEXT pane (160 keys, then 116 keys: link-off `"160"` lists, then the 116 equivalents); link-off golden regenerated. P5 two-column Decision Desk: R3 tests only, no golden. P6 ledger panes: release-1 golden regenerated (`lines_*x40`, `printed_*`; `lines_*x12` stay plain). P7 spec reconciliation and PR: no code test or golden changes. Each phase updates tests and goldens in the same commit. Regeneration must run from the current tree, which ends T47's "byte-identical to release 1" meaning | R03:197-216, 124-158; R01:155-166; recorders: `surface()` release1_surface.py:41-62, `capture()` test_linkoff_screen_reference.py:50-64 | Medium to High. Caveat: `test_view.py` and ten modules were classified from names and docstrings, so the P2 literal list is incomplete (GAPS row 26); the regeneration command shapes were derived, not run (GAPS row 25); the golden strategy (re-baseline, keep questions-off frozen, or add a new golden) is an owner decision (GAPS row 1) |
| Q3 harness and fixed-rubric reviewer; offline versus in-session | Offline: Option H3 scripted checks on `console.file.getvalue()` captures at 160/116/80 x colour, NO_COLOR, ASCII x heights 24, 40, 44 and 8 (zero ESC under NO_COLOR, only depth-valid SGR, no SGR 5 or 6, widths and heights fit, ASCII only, question text absent from record and snapshot). In-session: a fresh reviewer agent reads the mockup PNG (confirmed to work) and the rendered text or ANSI, scoring a fixed rubric (eight colour roles, pane geometry per width, title and badge, count tile, selected glyph against RR 50, muted absent values, no blink); an H1 export rendered in the Playwright MCP browser is an optional image-to-image add-on after one trial. Do not use `export_text(styles=True)` as the capture. Live path: pty with `pexpect` or a `force_terminal` seam into `LiveScreen` | R05:47-119, 121-126; R04:38-57, 85-99, 187-196; R02:35, 159-199; W02 B1-B7 (external, https://github.com/Textualize/rich/issues/2153) | Medium. Verified: no rasteriser is installed; PNG reading by an agent works. [UNVERIFIED]: H1 end to end, installability of any PNG tool, whether the real `LiveScreen` works under a pty (GAPS rows 6, 39). Remaining decision: PNG dependency yes or no (Q-7), closed here as "no" for the gate |
| Q4 colour depth today; detection cost and benefit; fallbacks; 16-colour distinctness of muted, slate, amber | Today `color_system` is the literal `"standard"` unless NO_COLOR is set (then `None`); it is never `auto`, `256` or `truecolor`, and nothing reads COLORTERM or TERM. Detecting 256 and truecolor (Option D2) costs a depth field in `TerminalPolicy`, one theme set per depth, the `Live` shape tuple (commands.py:265) including depth, and a test matrix, and gives the mockup's 24-bit palette on capable terminals. Fallback: named 16-colour roles plus bold and a text cue. Distinctness at 16 colours with the mockup RGB through Rich's downgrade: amber 11, slate 8, muted 7, base 15 are distinct from each other (muted 7 vs base 15 is a small step; slate 8 vs muted 7 depends on the terminal theme), but muted, green, red and violet all become 7, so state colours need explicit named roles | terminal.py:37-51, 110-125; R01:17-18, 171-179; R04:59-83 (table 63-76); W01 (external, https://rich.readthedocs.io/en/stable/console.html) | High for the code state and the downgrade table. Medium for the named-role mapping (design choice, not observed on a terminal [UNVERIFIED]). Caveats: light backgrounds and real-terminal capability unverified (GAPS rows 2, 32); owner depth decision pending |
| Q5 live versus one-shot styling; styled-capture gate | Today nothing is styled, so both paths print plain text. Styles added in `render()` reach the live terminal unchanged as SGR inside the alternate screen (`Screen` pads rows and crops rows past the console height); `--once --width` calls `export_text()` (commands.py:242) which drops styles; `--once` without `--width` prints `record_text` and never uses Rich. `export_text(styles=True)` ignores NO_COLOR and the standard-16 downgrade (probe), so the styled capture is `console.file.getvalue()` from a `make_console` StringIO (NO_COLOR-correct, down-converted). Gate: (i) ANSI present in the styled capture at 160/116/80 when colour is on; (ii) zero escape bytes under NO_COLOR; (iii) SGR-stripped bytes equal `screen_lines` joined; (iv) ASCII output `.isascii()`; (v) `len(lines) <= policy.height`; (vi) no SGR 5 or 6; (vii) the live path captured by pty or seam. Keep `--once --width` plain by default so `"\x1b" not in out` (test_commands.py:121) and the record checks (:99, :105; test_export.py:53) hold | commands.py:240-245, 264-274; R02:30-61, 159-199 (measurements 1 to 4); R03:104-120 | High for the machinery (probed). Caveat: whether a piped `--once --width` may carry ANSI by default is an open decision (GAPS row 3); the real `LiveScreen` has no test (GAPS row 6) |
| Q6 Zellij 0.44.2 go or no-go; stated conditions | Conditional go as an optional layout and manual check only (Option Z2); no-go as a dependency of the observer or of the render gate. Conditions: standalone outside Zellij (the observer is a Rich program that already runs without it), read-only (no Zellij effect on data), all widths (it reads the pane size each draw), NO_COLOR and ASCII (Zellij only wraps the program). Must be preceded by one session test on 0.44.2 because the docs describe a newer release and no source covers truecolor or 256-colour pass-through | R05:11-45, 121-129, 133-138; R02:53; W02 A1-A7 (external, https://zellij.dev/documentation/creating-a-layout.html, https://zellij.dev/documentation/nested-sessions.html, https://zellij.dev/news/terminal-inbox-session-previews) | Medium. All Zellij runtime behaviour is [UNVERIFIED] (no session was started); CI presence unknown (GAPS rows 34 to 38, 42) |
| Q7 the 64-hex-character fixture in the 80-column Decision Desk frame; wrap or cut | Measured on the current code (no frame yet; fixture text and the measured line counts 2/3/3 at 160/116/80 are in Section 2.3, Q7 fixture): `wrap` leaves a 64-cell hash whole on its own line at 160, 116 and 80; a 100-character unbroken token is hard-cut at the width with no marker; the desk text is capped at `DESK_TEXT_LINES = 4` and the list line is cut with `...` before the hash. Inside a mockup-style 78-wide frame the inner width is 74, so a 64-cell hash still fits alone but `label: <hash>` (about 84) moves the hash to its own line; the risks are the 4-line cap replacing a hash that trails a long path and file list, and a pane that clips instead of wrapping. Recommended rule: wrap the hash so it is never split when it fits the inner width (64 cells fit at every planned width), and state the exception that the 4-line cap (and the 400-character ask cap at parse.py:503) still cut a hash that falls beyond the fourth wrapped line; pin both behaviours and leave any change of the caps to the owner (D-6); add the fixture and test in P0 (name proposed: `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk`, parametrized over 160/116/80, plus the screen-only canary `HASH not in record_text(view)` and `snapshot_json(view)`); add a second fixture with a trailing hash; give hard-wrapped tokens wider than the inner width a decided, tested rule | R01:128-134; R03:160-187, 232; R04:198-209; render.py:62-80, 339-346, 347-353; view.py:99 | High for the measured current behaviour. Medium for the framed case (derived arithmetic). [UNVERIFIED]: plan-ask content (path, file list, hash) is doc-only (pr-591-comment.md lines 26-31); the hash policy is an owner decision (Q-6) |

### 7.3 What the owner must decide

| Id | Decision | Recommendation | What it unblocks |
|---|---|---|---|
| O-1 (D-1) | Adopt two-column layouts for the questions screen and the Decision Desk at 160 and 116, reversing "one stacked block" in rendering-rules.md lines 43 and 57 | Yes, with 80 columns staying stacked and the spec text updated in the same change (FINDINGS recommendation; GAPS Q-1) | M-03, M-04 and the P4 and P5 phases; decides the Q1 layout scope |
| OPEN-1 (D-3) | Severity of the question-list hierarchy (M-07): Astra High, Opus Medium | Treat as Medium (gated) as FINDINGS does; Medium follows from M-03 being High | Whether M-07 gates the close of P4 |
| OPEN-2 (D-3) | Whether RETAIN CONTEXT is built and its severity (M-14): Opus Medium, Astra Low; changes RR lines 41 and 61 | Medium (gated); schedule late; decide with the 80-column wording | A render-only pane built from `run_line`, `caveat_line`, `retention_line` (view.py:794, 798, 804) |
| OPEN-3 (D-3) | Title bar and READ ONLY badge (M-13): severity and scope; RR line 17 must be reconciled | Medium (gated): badge required, exact alignment and the diamond glyph optional | Header split inside render.py only |

Further decisions that the research surfaced and the plan depends on. Together with the table above they are exactly the plan's decision set D-1 to D-12 of Section 8.2 (O-1 is D-1; OPEN-1 to OPEN-3 are D-3); each has a default and an effect if ruled otherwise in 8.2:

| Decision | Source | Effect |
|---|---|---|
| D-7: mapping from real state words to colour roles (the minimum `STATE_ROLE` table of step 1.4) | M-09; RR 93 (no verified mapping) | Which values are coloured; RB-10 and SC-6 |
| D-8: title of the Decision Desk evidence pane (default `LINKED SESSION`) | AD-4; step 5.1 | The `DESK_EVIDENCE_TITLE` constant and the RR 57 edit |
| D-2: Golden strategy: re-baseline `golden_release1_surface.json` and `golden_questions_linkoff.json` (ends T47's release-1 meaning), or keep the questions-off screen frozen and apply the redesign only with questions on, or add a new golden | GAPS row 1; R03:227 | Whether P2 and P6 may change questions-off screens and P3 and P4 the link-off questions screens |
| D-5: target colour depths (16 only, or truecolor with 16-colour fallback) | GAPS row 2, Q-5; W01 | Q4 option D1 or D2 |
| D-12: whether bold and dim should survive NO_COLOR | GAPS row 2, Q-5; W01; 9.2 row 7 | Keeps `color_system=None` (default) or rewrites `test_terminal.py:40-51` and `test_render.py:985-987` |
| D-6: whether the Decision Desk shows a plan hash in full, cut with a visible mark, or wrapped | GAPS row 5, Q-6 | Q7 rule and the hard-wrap rule |
| D-10: PNG renderer as a new dev dependency | GAPS Q-7 | Q3: this report recommends no for the gate |
| D-11: reword RR line 61 (80-column invariant lines) versus RR line 42 and AD-7 | GAPS row 8 | The 80-column spec text |
| D-4: whether a piped `--once --width` may carry ANSI | GAPS row 3; R03:228 | Q5 capture route and `test_commands.py:121` |
| D-9: whether `--once --width` output may include box-drawing (frame) lines | GAPS row 3; R03:228; step 3.6 | Whether step 3.6 edits `test_commands.py:672-675` and `:690` or a `frames` switch is added |

### 7.4 Coverage note

Carried into this report: the style-only phase economics and the NO_COLOR test rewrite (R03 sections 3 to 6); the `safe_box` correction (R01, R03, R04); the `export_text(styles=True)` hazard (R02); the live-path measurements, including the silent bottom crop (R02 section 9); the mockup palette, its 16-colour collapse and the pane geometry (R04 sections 2 to 4); the Zellij and harness environment (R05); the external context (W01, W02). Excluded with rationale: documentation line-number drift and cosmetic count mismatches in GAPS rows 43 to 58 (they do not change an option or an answer); the Zellij pane-frame arithmetic and the aidev02 theme lines 179-252 (not read, flagged [UNVERIFIED]); licence confirmation for freeze, pyte, aha and cairosvg (H2 is not recommended).

## 8. Implementation Plan

This is a plan for a later implementation of the observer redesign (issue #606); nothing here is an instruction to implement now. The phase scheme P0 to P7 in this Section 8 is the authoritative one for the whole report; the phase labels in Sections 3.8 and 7 mirror it and, where a wording differs, this Section 8 governs. All paths are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`. `OBS` means `src/superclaude/cli/observe/`; `T` means `tests/observe/`; `VP` means `.dev/issues/409/visual-parity/`; `RR` means `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`. Every plan step rests on a source-code read or probe recorded in research files 01, 02, 03 and 05. Mockup and spec facts (04, RR, FINDINGS) are used only as the design target, never as a statement of current architecture. Items that are `[UNVERIFIED]` appear in 8.8 and are not asserted as fact in any step.

### 8.1 Planning decisions (answers to Q1 to Q7 that every phase relies on)

| Q | Decision used by this plan | Evidence | Status |
|---|---|---|---|
| Q1 composition | Keep the line model. Introduce a `Line` (plain string plus role spans) layer in `OBS/render.py`; `screen_lines()` becomes `[l.plain for l in _compose(...)]` so every plain-string test and golden keeps its meaning. Frames and two columns are hand-built from `Line` objects using new `GLYPHS` entries. `render()` still returns one `Text` per line. No Rich `Panel`, `Table`, `Layout` or `Columns` in `render()`. | `render()` is one `Text(no_wrap=True, overflow="crop")` per string (render.py:524-531); `T/test_render.py:399` pins `len(group.renderables) == len(screen_lines(...))`; `wrap`/`clip` own the `>` and `...` markers; height budgets count `list[str]` lengths (render.py:438-457, 499-503); `safe_box` does not ASCII-ize a Panel (probe, Rich 15.0.0). [CODE-VERIFIED] | Decided |
| Q2 phases | Seven phases, ordered by golden impact: P0 tests and harness only; P1 style only; P2 text and budget fixes; P3 single-column frames; P4 and P5 two-column layouts (need O-1); P6 ledger frames; P7 spec reconciliation and final gate. | 03 section 6 (P0 to P5 grouping), with P2 and P6 added for the findings it does not cover. | Decided |
| Q3 harness | Standalone script `VP/tools/render_compare.py` built on `render_current.py`; no new dependency. Text and ANSI tier is machine-checked; PNG tier is made in the Claude session by opening Rich `export_html` output in the Playwright MCP browser; a fresh reviewer subagent scores a fixed rubric (8.4) against the mockup PNGs. | 05 sections 2, 4, 5, 6; web-02 B1, B2, B7 (external context). PNG route is untested. | Decided; PNG route [UNVERIFIED] until step 0.4 |
| Q4 colour depth | Add `TerminalPolicy.color_system` resolved in `resolve_policy` (`NO_COLOR` gives `None`; `COLORTERM` truecolor or 24bit gives `"truecolor"`; `TERM` ending `256color` gives `"256"`; otherwise `"standard"`). A new `OBS/theme.py` holds one explicit role table per depth; the 16-colour table uses named ANSI colours, not downgraded RGB. | `make_console` pins `"standard"` (terminal.py:121); the downgrade measured in 04 section 3 collapses muted, green, red and violet to index 7. [CODE-VERIFIED + probe] | Default; owner confirms target depths (8.2 table, D-5) |
| Q5 styled capture | One-shot path: replace `export_text()` (commands.py:242) with a helper that returns `console.file.getvalue()` when styled output is allowed, else `export_text()`. Live path: a pty test through `pexpect`. Gate tests in P1. | `export_text(styles=True)` bypasses NO_COLOR and the colour downgrade (probe, 02 section 2); a `StringIO` console writes nothing under `Live(screen=True)` (02 section 9.2). [CODE-VERIFIED] | Default; owner rules D-4 |
| Q6 Zellij | No-go as a render-harness dependency or observer dependency. The observer stays standalone. Zellij is an optional manual check in P7 only. | 05 section 7 (help text only, nothing exercised); web-02 A2, A5 (external context: Zellij sets `ZELLIJ`; docs are newer than the 0.44.2 binary). | Decided; runtime behaviour [UNVERIFIED] |
| Q7 hash fixture | Add the 64-hex plan-ask fixture in P0 (pins today's wrap), re-pin it in P3 for the framed 80-column desk. Rule, per surface: (1) in the desk question text, a token that fits the pane's inner width (64 or more cells at every planned width: 154/110/74 single column, 72/110/74 in P5) stays whole on its own wrapped line, but only if it falls inside the first four wrapped lines (`DESK_TEXT_LINES = 4`, view.py:99; render.py:341-345), where the fourth line is cut with `...`; a hash after that point is not shown, and the ask is already cut by `ASK_CAP = 400` at parse.py:503. So the hash is never split by wrap, and it is not guaranteed to appear. (2) In an evidence field a value wider than the pane's inner width minus 2 is hard-split with nothing lost and no marker (62 at 116 in P5, so a 64-cell `resource.worktreeId` splits there; whole at 160 and 80). | Probe: hash whole at 160, 116, 80; paths over the width hard-split mid-word (01 section 4.9; 03 section 5c); `_desk_lines` render.py:339-353 re-read. [CODE-VERIFIED] | Pinned as today's behaviour; owner rules D-6 on whether a cut hash is acceptable |

Data flow after the plan (text authority stays at the bottom; styles never feed the record or snapshot):

```
build_view -> View (plain strings only; adds one render-only field, P4)
                |-- record_text(view)   (export.py)  unchanged bytes
                |-- snapshot_json(view) (export.py)  unchanged bytes
                v
          _compose(view, policy, message) -> list[Line]   Line = plain str + role spans
                |-- screen_lines()  = [l.plain ...]       goldens, tests, --once without styles
                v
          render() -> Group(one Text per Line, spans -> theme.style_for(role, depth))
                v
          make_console(policy)  color_system = None | standard | 256 | truecolor
```

### 8.2 Owner decisions the plan depends on (defaults assumed, effect if different)

| ID | Decision | Default assumed | If the owner rules otherwise |
|---|---|---|---|
| D-1 (O-1) | Two columns at 160 and 116, reversing RR lines 43 and 57 | Yes (FINDINGS recommends yes) | P4 and P5 are skipped; P3 stacked frames stay; M-03, M-04 stay open |
| D-2 (G-A) | Re-baseline the questions-off and link-off goldens | Yes, regenerate from the current tree; `.dev/issues/606/issue-body.md:84` lists the four files as deliberate presentation updates. [CODE-VERIFIED line] Record and snapshot keys are split into a never-regenerated golden first (step 2.1) | "Freeze questions-off": P2 and P6 apply only to questions-on screens; M-06, M-10, M-11, M-13 stay open for the questions-off screens |
| D-3 (OPEN-1 to OPEN-3) | Severity of M-07, M-14, M-13 | Treated as Medium (gating) until ruled | A Low ruling removes the item from the gate |
| D-4 (Q5) | Should a piped `--once --width` carry ANSI | No: styled bytes only when stdout is a tty and colour is allowed (keeps `T/test_commands.py:121` true) | A styled-by-default ruling changes `T/test_commands.py:121` in P1 |
| D-5 (Q4/G-2) | Target colour depths | Truecolor, 256 and 16 with detection | "16 only": steps 1.1 detection and the two higher tables are dropped |
| D-6 (Q7) | Show a plan hash in full | Keep today's rule: the hash is whole (never split by wrap) when it lies inside the first four wrapped lines of the question text; a hash beyond the 4-line cap or the 400-character ask cap is cut with `...` and is not shown. The plan changes no cap | "Never show a cut hash" needs a raised `DESK_TEXT_LINES` or a hash-aware cap (view.py:99, render.py:341-345, parse.py:503), a changed pinned test (step 0.6, second test) and a spec edit; a "cut with a visible mark" rule needs a new test and a view-level rule |
| D-7 | Mapping from real state words to colour roles (M-09) | The minimum fixed `STATE_ROLE` table in step 1.4: workerState `running`, liveness `alive` and `live` are running; workerState `succeeded` and dispatchStatus `completed` are settled; workerState `failed` and dispatchStatus `failed` are failed; the `FROZEN` flag is frozen; every other value uses the body role; the state word is always printed. The code and spec state no meaning for these words (RR 93), so this is a display default for the owner to confirm | Owner supplies the table; the step 1.4 table is replaced and RB-10 is scored against the owner's table (it must stay non-empty) |
| D-8 | Title of the Decision Desk evidence pane (the mockups say `AFFECTED SESSION EVIDENCE` and `AFFECTED SESSIONS`, which claim an affected-session list the code does not have, AD-4) | `LINKED SESSION` (reuses the existing link vocabulary, parse.py:468-472); step 5.1 | Any other title that does not claim an affected list needs only the `DESK_EVIDENCE_TITLE` constant and the tests that name it changed; a title that claims an affected list needs new view data first (AD-4) and a spec edit to RR line 57 |
| D-9 | May `--once --width` output include frame (box-drawing) lines? (OPEN in 4.1b, 7.3 and 9.2 row 8) | Yes: the one-shot prints the same framed lines as the live screen. Step 3.6 therefore rewrites `T/test_commands.py:672-675` and `:690` to read framed output through `title_of` and `unframe` | No: add a `frames: bool` switch to `_compose` that `run_once` (commands.py:238-242) sets false, selecting the P2 unframed stacked layout for `--once --width` (and none of the P4 and P5 two-column layouts there); `T/test_commands.py:672-675` and `:690` then stay unchanged, step 3.6 drops those two edits, and tests are parametrised over `frames` for the one-shot path; the live screen still frames |
| D-10 | PNG renderer as a new dev dependency (Q-7) | No dependency: the gate is the text and ANSI tier plus the reviewer reading the mockup PNG; the image tier is session-only through the Playwright MCP browser (step 0.4) | Name one tool (for example `freeze`, or `playwright install chromium`), add a dev extra in `pyproject.toml` and a Makefile target, and make gate step G3 a script step; the licence and install checks of 9.3 row 21 come first |
| D-11 | Reword RR line 61 (the 80-column invariant lines) against RR line 42 and AD-7 (G-H) | Reword RR 61 in the P7 spec edit (step 7.1) so it no longer requires "Questions stay until explicit resolution."; RR 42 keeps the retention wording; the plan builds neither invariant line | The owner instead requires the lines on the 80-column screen: a text step is added to P4 (new literal in view.py, both goldens re-baselined) and the RB-05 literal list gains them; or RR 42 is reworded and AD-7 is withdrawn |
| D-12 | Keep bold and dim under NO_COLOR? (9.2 row 7) | No: keep `color_system=None`, which drops bold and dim with colour (G-2); hierarchy lives in text and glyphs | Use `no_color=True` with a colour system so bold and dim survive: rewrite `T/test_terminal.py:40-51` and `T/test_render.py:985-987`, and RB-06 changes from "zero ESC bytes" to "no colour SGR" |

### 8.3 Geometry and height budgets (design target from 04 section 4, checked against code arithmetic from 01)

| Screen | 160 | 116 | 80 |
|---|---|---|---|
| Questions screen | left 114, right 42, gap 2, margin 1 each side (1+114+2+42+1=160) | left 70, right 42, gap 2 (1+70+2+42+1=116) | one column, panes 78 wide |
| Decision Desk | left 76 (question over list), right 80 (session evidence) (1+76+2+80+1=160) | question 114 full width over 66 + 46 (1+66+2+46+1=116) | three stacked panes 78 wide |
| Ledger | table keeps all 160 cells today (render.py:159-192); a border-only frame needs `flags` to give 2 cells | `line` layout, frame 114 | `short` layout, frame 78 |
| Inner width of a framed pane | pane width minus 4 (border plus one cell padding each side) | same | same |
| Frame row cost | 2 rows per frame (top and bottom border) | 2 | 2 |
| Harness height for scoring | 48 (mockup frame height) | 42 | 42 |
| Extra height matrix (text only) | 44, 40, 24, 12, 8 | same | same |

Height rule: every added row must be counted inside `screen_lines` (`top`, `body`, `footer_height`), because on `Live(screen=True)` rows past `policy.height` are dropped from the bottom, which are the footer keys and `shown x/y` (02 section 9). [CODE-VERIFIED] `base` and `len(desk)` at render.py:441-457 are measured from returned lists, so frame rows are counted automatically once `_panel_lines` and `_desk_lines` return framed lines; the three `+1` terms stay as they are (which `+1` is which is [UNVERIFIED]; read the comment at render.py:444-445 before editing).

### 8.4 Fixed rubric for every render gate (written once in P0 to `VP/rubric/rubric.md`; the wording is not edited between phases)

| ID | Criterion | Severity | Findings | Checked by | In scope from |
|---|---|---|---|---|---|
| RB-01 | Colour roles, measured on the truecolour `.ansi` by mapping each SGR foreground RGB to a role (palette: base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242; 04 section 2). Pass only if all hold: (a) every foreground colour in the file is one of the eight triples; (b) the `header1` title text is cyan and bold; (c) every question age (in the list and in the desk) is amber and bold, and every question-text line in the desk is amber and bold; in the list the question subject text is base colour and bold (`body_bold`, step 1.4, RB-16(a); 04 line 57: amber question text in the desks, base bold in the 160 ledger), never amber; the one selected list row is scored under the `selected` role (marker and line bold amber, step 1.4; an unverified design choice, no mockup shows a selected row) and is exempt from the base-colour subject rule but not from the amber-age rule; (d) the `header2` freshness line, the keys hint and the footer text are muted; (e) every secondary-pane border glyph and the footer rule is slate (not applicable before P3, when no border exists); (f) ledger cells that carry no state or absent value are base. One counter-example, quoted with its line number, fails the row | High | M-01 | Script (`checks.json` role census for (a)) plus Reviewer for (b) to (f) | P1 |
| RB-02 | Every pane the mockup frames has a titled border with the title inset in the top border: heavy amber for the attention pane, rounded slate for secondary panes, cyan for the count tile | High | M-02 | Reviewer | P3 (questions, desk), P6 (ledger) |
| RB-03 | Column structure matches 8.3 at each width (two columns at 160 and 116, stacked at 80) | High | M-03, M-04 | Reviewer | P4 (questions), P5 (desk) |
| RB-04 | Count tile, at 160 and 116 only (none at 80). Pass only if all hold: (a) the tile frame's border glyphs carry the cyan role and its top border holds the title `QUESTIONS_COUNT_LABEL.upper()`; (b) when the tile inner width is at least `4 * len(figure)` the figure occupies at least 3 consecutive rows made of the block glyph (`█`, ASCII `#`), otherwise it is one bold amber line; either way it is the largest figure on the screen (taller than any other text in the right column); (c) the whitespace-collapsed plain pass (`panes_flat`, because the counts line wraps inside the tile) contains `seen, not resolved: N \| closed by evidence: unavailable (no source)` with N equal to the figure; (d) at 80 columns no tile frame exists and (c) still holds | High | M-05 | Script for (a) border role, (c) and (d); Reviewer for (b) | P4 |
| RB-05 | Required literals intact and uncut: gap notice, counts tokens without a mid-token cut, `PARTIAL (...)` text, the disclosure, `reason unknown`, desk title, retention line, `nextAction.kind` verbatim | High | guards RR 20, 31, 32, 47, 49 | Script (substring list) | every phase |
| RB-06 | NO_COLOR pass: zero ESC bytes; text equals the coloured pass after SGR removal; hierarchy is carried by text and glyphs | High | G-1 | Script | every phase |
| RB-07 | ASCII pass: output is pure ASCII; borders are `+ - |`; no `?` where a border should be | High | G-1 | Script | P3, and every phase for the ASCII text part |
| RB-08 | Fit: every line at most the width in cells; rows at most the height; the footer keys are the last lines; no SGR 5 or 6 (blink); no mouse sequences | High | AD-5, standing constraints | Script | every phase |
| RB-09 | 16-colour pass: the eight roles map to eight distinct ANSI colours (no two roles share an index) | High | G-2 | Script (theme table test plus SGR read) | P1 |
| RB-10 | State words follow the fixed `STATE_ROLE` table of step 1.4 (D-7 default). Pass only if all hold: (a) every `workerState`, `dispatchStatus` or liveness cell, desk field or flags cell whose raw value is in the table carries exactly the table's role in the `.ansi`; (b) every other value (and `terminalState`, `nextAction.kind`) carries the `body` role, never a state role; (c) the word is printed in the plain pass in every case; (d) the table is non-empty: `T/test_theme.py` asserts that the tuple keys `("workerState", "running")`, `("workerState", "succeeded")`, `("workerState", "failed")`, `("dispatchStatus", "completed")` and `("liveness", "alive")` are in `STATE_ROLE` and that `FROZEN_ROLE == "state_frozen"`, so the row cannot pass on an empty table; (e) at the `standard` depth the four state roles have four different SGR codes | Medium | M-09 | Script (`.ansi` census against the table, `T/test_theme.py`) | P1 (desk fields P5) |
| RB-11 | Absent values (`unknown`, `unavailable (no source)`, `reason unknown`) are muted; plain under NO_COLOR | Medium | M-08 | Reviewer | P1 |
| RB-12 | A column heading and rule appear at 116 and 80 whenever rows are visible | Medium | M-10 | Reviewer plus script | P2 |
| RB-13 | The 80-column key list is not cut and no key pair is split across lines | Medium | M-11 | Script | P2 |
| RB-14 | Desk, measured on the plain and `.ansi` passes of `desk` and `desk-planask`. Pass only if all hold: (a) the question text leads: the first body line of the first pane after `DESK_TITLE` is `qid  age`, and all question-text lines (at most `DESK_TEXT_LINES`) come before any `label: value` line; (b) question-text lines carry the amber role and bold; (c) in the evidence pane every one-line field starts its value at the same cell offset (`label_width` = longest label plus its colon), measured as the column of the first character after the label on each such line; (d) a value that does not fit beside its label sits on the next line indented two cells, and no line exceeds the width | Medium | M-12 | Script for (a), (c), (d); Reviewer for (b) | P5 |
| RB-15 | Title bar: the left title and a right `READ ONLY` badge (OPEN-3, gating until ruled) | Medium | M-13 | Reviewer | P2 |
| RB-16 | Question list hierarchy (OPEN-1, gating until ruled). Pass only if all hold in the `.ansi`: (a) every question row line is bold, and its subject text carries the `body_bold` role (base colour); the one selected row is accepted with its marker and line in the bold amber `selected` role (step 1.4) and is not counted against this clause; (b) every run, state, caveat and retention line carries the `muted` role and no bold; (c) at 160 and 116 the first line inside the list pane after the disclosure is a question row (the caveat lines sit in the RETAIN CONTEXT pane, step 4.4), and at 80 the row lines carry strictly more bold characters than the caveat lines (0) | Medium | M-07 | Script (role census per line class) | P4 |
| RB-17 | RETAIN CONTEXT grouping at 160 and 116 (OPEN-2, gating until ruled). Pass only if all hold: (a) when a frame whose top border contains `RETAIN CONTEXT` is drawn, it is slate-bordered and its body contains each of `run_line`, `caveat_line` and `retention_line` exactly once; (b) none of those three strings occurs anywhere else on the screen; (c) when the degrade rule of step 4.5 dropped the pane (small height), no such frame exists and each of the three strings still occurs exactly once, in the list pane; (d) at 80 columns no RETAIN CONTEXT frame exists | Medium | M-14 | Script (string census with `panes_flat`) | P4 |
| RB-18 | Ledger screen: observation and attention content is in titled panes, with no invented owner, requester, mapped-tree or SIGNALS content (AD-1 to AD-4) | Medium | M-06 | Reviewer | P6 |
| RB-19 | Q7: for the `PLAN_ASK` fixture (hash inside the first four wrapped lines) the 64-hex hash is whole on one line in the 80-column desk, nothing is lost, no line exceeds 80 cells; the trailing-hash fixture still ends its fourth line with `...` (D-6) | Medium | Q7 | Script | P3 |
| RB-20 | A rule line precedes the footer and the key pair `n/p question` is intact | Low | M-15 | Script | P2 |
| RB-21 | The 80-column counts strip is not cut inside a token | Low | M-16 | Script | P2 |
| RB-22 | No wide blank band after the id column at 116 and 80: the longest run of consecutive spaces between two non-space characters inside a ledger row line, on the `base` fixture, is at most N, where N is the same measure on the 160-column rows of the same fixture, recorded in `VP/scores/baseline.md` in step 0.8 (a number measured at the current commit, not assumed) | Low | M-17 | Script | P2 |
| RB-23 | The selected question has a role style in addition to the glyph | Low | M-18 | Reviewer | P1 |

A phase closes only when every High and Medium row that is in scope for it passes; Low rows are recorded and may be deferred with a log line. A reviewer scores only the rows in scope for the phase, and marks later rows `N/A (scheduled P<n>)`.

### 8.5 Render gate protocol (the last step of every phase, written once)

| Step | Action | Details |
|---|---|---|
| G1 | Implement | Phase steps are done; `uv run pytest tests/observe/ -v` is green (baseline 766 passed in 25.70 s on 2026-11-17, plus tests added by earlier phases). |
| G2 | Render | `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <out>/<phase>/iter-<n> --check --heights 44,40,24,12,8` runs the harness contract of step 0.3: widths 160, 116 and 80 for screens `ledger`, `questions`, `desk` and `desk-planask`, in the five passes truecolor, 256-colour, 16-colour, NO_COLOR and ASCII, plus the text-only height matrix, with the file names listed in 0.3. `--check` writes `checks.json` with the script-checked rows listed in 0.3 (RB-01(a), RB-04, RB-05 to RB-10, RB-13, RB-14, RB-16, RB-17, RB-19 to RB-22 for the parts marked Script in 8.4). |
| G3 | Rasterise | In the Claude session, open each truecolor and 16-colour `<screen>.<depth>.html` (step 0.3) through the Playwright MCP browser at a fixed viewport and save `.png` next to it (route proven in step 0.4). If 0.4 fails, the text and ANSI tier is used and the reviewer compares `.txt`/`.ansi` files with the mockup `.txt`/`.ansi` files, with the mockup PNG as the visual reference. |
| G4 | Score | Spawn one fresh reviewer subagent per width (no resume, no author context). Its inputs are only `VP/rubric/rubric.md`, the reviewer prompt, the mockup PNGs and `.txt` for that width, and the rendered `.png`, `.txt`, `.ansi`, `checks.json`. It returns `scores.json` with PASS or FAIL and one evidence line per in-scope row. |
| G5 | Fix and repeat | Fix every failing High or Medium row, re-render, and score again with a new reviewer. At most 3 iterations per phase. |
| G6 | Close or stop | Close the phase only if all in-scope High and Medium rows pass in the last iteration. If any still fails after iteration 3, stop, log the failing rows and the iteration scores in `VP/scores/<phase>/stop.md`, and ask the owner; do not start the next phase. |

All gates include the NO_COLOR and ASCII pass (guard G-1) as G2 outputs; a gate with a missing pass is not valid.

### 8.6 Contradictions between research files and which finding wins

| Topic | Conflicting statements | Used here | Why |
|---|---|---|---|
| Width classes | Task prompt (g): full, line, narrow; code: full, line, short, narrow | Four classes | `OBS/terminal.py:63-70` [CODE-VERIFIED] |
| `safe_box` and Rich boxes | Earlier 03 and 04 text: `safe_box=policy.ascii` gives ASCII panes; 01 probe: Panel prints identical Unicode borders with `safe_box` True or False | Hand-built `+ - |` glyphs through `GLYPHS` | Probe on Rich 15.0.0 (01 section 1; 03 section 6 rule 3); corrected in Gate 1 |
| Full ledger width | FINDINGS M-06: 153 cells; 01: exactly 160 | 160 | Arithmetic from `_columns` render.py:159-192 |
| 16-colour collapse | 01 section 7: slate and muted collapse; 04 section 3: muted, green, red, violet all index 7, slate 8 | 04 table | Measured with Rich's own downgrade, reproduced by two reviewers |
| Styled one-shot export | 01 and 05 and `render_current.py`: `export_text(styles=True)`; 02 probe: it ignores NO_COLOR and the downgrade | `console.file.getvalue()` | 02 probe |
| NO_COLOR and bold | web-01: Rich NO_COLOR keeps bold and dim; code: `color_system=None` drops them | Code behaviour kept | Project choice, probe in 01 section 7 |
| Live overflow | web-01 (Rich docs): `Live` shows an ellipsis; 02 section 9 measurement: `Screen` crops silently | Silent crop | Measured |
| Right-column slack | 01: 114+1+42=157 of 160; 04: 1+114+2+42+1=160 | 04 numbers | Measured from the mockup files |
| Zellij | web-02: go, conditional; 05: no-go as a harness dependency | Not a dependency; optional manual check | Both agree the observer must stay standalone; neither ran a session |
| Gate test line ranges | 03: test_commands.py:747-760 and 762-777; 02: 747-756 and 762-772 | 02 ranges | Gate 1 log row 43 |

### 8.7 External context (web research, not code facts)

| Claim used | Source |
|---|---|
| `color_system` values and auto detection read `COLORTERM` then `TERM` | https://rich.readthedocs.io/en/stable/console.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py |
| Rich `export_html`, `export_svg` need `record=True`; SVG output depends on a browser (`rsvg-convert` and ImageMagick failed) | https://rich.readthedocs.io/en/stable/reference/console.html ; https://github.com/Textualize/rich/issues/2153 |
| `Text` spans and `cell_len` rules (ambiguous width counted as 1) | https://github.com/Textualize/rich/blob/v15.0.0/rich/text.py ; https://github.com/Textualize/rich/blob/v15.0.0/rich/cells.py |
| Zellij sets `ZELLIJ` in panes; `dump-screen --ansi`; floating panes in layouts | https://zellij.dev/documentation/nested-sessions.html ; https://zellij.dev/documentation/cli-actions.html ; https://zellij.dev/documentation/creating-a-layout.html |
| Playwright screenshots at a set viewport | https://snapshotflow.com/blog/playwright-screenshot |

### Phase 0: Render-compare harness, rubric, baseline and pinning tests (no `src/` change)

**Goal:** make the visual gap measurable and pin today's behaviour before any code changes: a harness that writes per-width, per-screen outputs; a fixed rubric; a baseline score; the Q7 hash fixture; and tests that document the style contract.

**Dependencies:** none. Owner decision D-10 (no new PNG dependency by default). Baseline run: `uv run pytest tests/observe/ -q` gives 766 passed.

**Closes:** no finding. It prepares the gate for all of M-01 to M-18.

| Step | Action | Files | Details |
|---|---|---|---|
| 0.1 | Make `render_current.py` importable | `VP/inputs/tools/render_current.py` | Line 93 calls `main()` at import time with no guard. Wrap it in `if __name__ == "__main__":`. Outputs of a direct run stay identical. |
| 0.2 | Add the harness | `VP/tools/render_compare.py` (new) | Loads `render_current.py` by path (`importlib.util.spec_from_file_location`) to reuse its view builders (`questions_result`, `QUESTIONS`, the three views). Interface: `render_case(view, width: int, height: int, *, env: dict, ascii: bool, depth: str = "16") -> CaseOutput` where `CaseOutput` holds `plain` (`screen_lines`), `stream` (the string written by `make_console(policy, file=io.StringIO(), record=True)` printing `render(view, policy)`, read with `console.file.getvalue()`), and `html` (`console.export_html(inline_styles=True)`). Policy comes from `resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)`. It must not use `export_text(styles=True)`. |
| 0.3 | Define the harness contract (the one definition; G2 in 8.5 and step 7.3 refer to it) | `VP/tools/render_compare.py` | **Command:** `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <dir> [--depth 16,256,truecolor] [--heights 44,40,24,12,8] [--check]`. **Screens:** `ledger`, `questions`, `desk`, `desk-planask` (Q7 fixture, built in 0.6). **Widths:** 160, 116, 80, at heights 48, 42, 42 (mockup frame heights, 04 section 4; `render_current.py:38` uses 50, which is not like for like). **Five render passes** per width and screen: (1) truecolor, (2) 256-colour, (3) 16-colour, (4) NO_COLOR, (5) ASCII. **Depth selector:** `--depth` takes a comma list of `16`, `256`, `truecolor` (default all three), mapped to the Rich `color_system` values `standard`, `256`, `truecolor`; before step 1.1 adds `TerminalPolicy.color_system` the harness can only produce `16` (`make_console` pins `"standard"`, terminal.py:121), writes the other two as copies marked `not-available-before-P1` in `manifest.json`, and the baseline run has no ESC in any file anyway. **Output files** in `<dir>/<width>/`: `<screen>.txt` (plain `screen_lines`), `<screen>.<depth>.ansi` and `<screen>.<depth>.html` for each selected depth, `<screen>.nocolor.txt` (env `{"NO_COLOR": "1"}`), `<screen>.ascii.txt` (`ascii=True`, plain) and `<screen>.ascii.ansi` (`ascii=True`, 16-colour stream); plus `manifest.json` per width with line counts and cell widths. `--heights` adds a text-only matrix (`<screen>.h<height>.txt`). **`--check`** writes `<dir>/checks.json` with one entry per script-checked row: RB-01(a), RB-04(a, c, d), RB-05 to RB-10 (RB-10(a), (b), (d) from the `.ansi` census), RB-13, RB-14(a, c, d), RB-16, RB-17, RB-19 to RB-22; the checks are width fit by `rich.cells.cell_len`, no ESC in the NO_COLOR file, `isascii()` on both ASCII files, SGR 5 and 6 absent, mouse sequences absent, the required literal list present, `strip_sgr(stream) == plain + newlines`, and the role census of 8.4. Gates run with `--check`; a run without it is not valid. |
| 0.4 | Prove the PNG route once | `VP/png-route.md` (new) | In the Claude session, open one `.html` via `mcp__plugin_playwright_playwright__browser_navigate` (`file://`), set the page to `font-family: "DejaVu Sans Mono"` and a width of `<cols>ch`, take a screenshot with `browser_take_screenshot`, and Read the PNG back. Record viewport, font and result. [UNVERIFIED until run; DejaVu Sans Mono is the only mono font confirmed installed, and its coverage of the mockup glyphs is untested.] If it fails, record that the text and ANSI tier is the gate and that a PNG tool (freeze or Playwright) needs a separate owner approval; no dependency is added by this plan. |
| 0.5 | Write the rubric and reviewer prompt | `VP/rubric/rubric.md`, `VP/rubric/reviewer-prompt.md` (new) | `rubric.md` is the 8.4 table verbatim plus the palette from 04 section 2 and the geometry from 8.3. The reviewer prompt names the inputs (mockup `.png`/`.txt`/`.ansi` for the width, rendered `.png`/`.txt`/`.ansi`, `checks.json`), the pairing ledger to signal-bridge, questions to attention-ledger, desk to decision-desk, the PASS or FAIL JSON shape, and forbids edits. The screen pairing and the mockup titles that the spec retires (`OPEN HUMAN QUESTIONS`) are noted so the reviewer does not score the title text. |
| 0.6 | Add the Q7 fixture and tests | `T/test_render.py` (R3 block, after line 967, the last line of the test that starts at :958) | New `PLAN_ASK` constant: a synthetic ask with a plan path, two file paths and `"0123456789abcdef" * 4`, under `ASK_CAP = 400` characters (parse.py:475) and under four desk lines at 80 columns. Test `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk(width)` over `WIDTHS`: built with `r3_rows([("w-001", PLAN_ASK)])` and `r3_screen(fake_clock, rows, 0, width, height=70)`; asserts every line `cell_len <= width`; the hash is whole on one desk line; the ask with spaces removed equals the desk text with spaces removed when not cut. Second test with a hash after a long path and file list that fills the four-line cap, pinning today's `...` cut: the hash is not shown, and this is the one stated exception to "the hash is whole" (rule D-6). The first test's fixture keeps the hash inside the first four lines. Third test: a worker with a 120-character `resource.worktreeId` (pattern from `T/test_view.py` `r3_workers(worktree=...)`) pins the 2-cell continuation indent at render.py:347-353. Canary: `HASH not in record_text(view)` and `HASH not in snapshot_json(view)`. |
| 0.7 | Add helpers and a height test | `T/conftest.py`, `T/test_height_budget.py` (new) | `strip_sgr(text) -> str` using `re.sub(r"\x1b\[[0-9;]*m", "", text)` and `sgr_params(text) -> set[str]`, with a self-test. `test_questions_on_screen_fits_the_height(width, height)` for heights 24, 40, 44. Run it first: if a height fails on today's code, record the failing heights in `VP/scores/baseline.md` and pin only the passing set (the forced single ledger row at render.py:502 can overflow; 02 section 9.4). |
| 0.8 | Baseline score | `VP/scores/baseline.json` (new) | Run the harness at the current commit, rasterise per 0.4, spawn one fresh reviewer per width (8.5 G4), store the scores, and write the measured threshold N of RB-22 (longest interior blank run in the 160-column rows of the `base` fixture) to `VP/scores/baseline.md`. Expected: RB-01 to RB-04 and RB-09 to RB-18 FAIL (the plain-text rows RB-05 to RB-08 are expected to pass, since the current screens are plain text); script rows that check text pass. A baseline that passes any High rubric row is a sign the rubric is not discriminating; revise `rubric.md` once, then freeze. |

**Tests and goldens that change:** none change; tests are added. Golden files and `printed_*` bytes are untouched.

**Byte-identical in this phase:** everything under `src/`; `record_text`; `snapshot_json`; both goldens.

**Rubric rows scored (baseline only):** all, as a baseline; no pass is required.

**Migration or rollback:** delete the new files; no source depends on them. If 0.7 shows an existing overflow, it is a finding for P3, not a P0 fix.

**Render gate:** the baseline run in step 0.8 replaces the gate for this phase; the phase closes when `uv run pytest tests/observe/ -v` is green with the new tests and the baseline file exists.

### Phase 1: Colour depth, theme, role spans and the styled-capture gates (style only, no text change)

**Goal:** add colour and weight to every existing screen without changing one plain character; fix colour depth (Q4, G-2); make styled output capturable and tested on the one-shot path and the live path (Q5).

**Dependencies:** Phase 0 (harness, helpers `strip_sgr`, rubric, baseline). Owner decisions D-4, D-5, D-7, D-12 (defaults in 8.2 apply if not ruled).

**Closes:** M-01 (colour and weight on the current screens; frame and tile colours follow in P3 and P4), M-08, M-18; M-09 on the ledger rows (desk fields complete it in P5); guard G-2.

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Resolve the colour system in the policy | `OBS/terminal.py` (`TerminalPolicy` 37-51, `resolve_policy` 73-92, `make_console` 110-125) | Add field `color_system: str \| None = "standard"` last in the frozen dataclass so existing constructions keep working. In `resolve_policy`: `None` when `no_color`; `None` when `env.get("TERM")` is `dumb` or `unknown`; `"truecolor"` when `env.get("COLORTERM", "").lower()` is `truecolor` or `24bit`; `"256"` when `env.get("TERM", "")` ends with `256color`; otherwise `"standard"`. In `make_console` replace line 121 with `color_system=policy.color_system`; keep `no_color=policy.no_color`. NO_COLOR therefore still gives `color_system=None` and drops bold as well as colour (project behaviour, 01 section 7). `NO_COLOR` literal stays only in terminal.py (source scan `T/test_terminal.py:181-198`). Tests call `resolve_policy({}, ...)` with an empty env, so they stay at `"standard"`. |
| 1.2 | Add the theme module | `OBS/theme.py` (new) | `ROLES: tuple[str, ...]` (semantic roles: `title`, `attention`, `attention_title`, `identity`, `secondary`, `body`, `body_bold`, `muted`, `selected`, `border_attention`, `border_secondary`, `border_count`, `state_running`, `state_settled`, `state_failed`, `state_frozen`); `style_for(role: str, depth: str) -> rich.style.Style \| None` (returns `None` for depth `None`); one table per depth. Truecolor RGB from the mockups: base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242 (04 section 2). 256-colour indexes: base 189, slate 60, cyan 80, muted 145, amber 214, green 115, red 210, violet 147. 16-colour table with named colours: base `bright_white`, muted `white`, slate `bright_black`, cyan `bright_cyan`, amber `bright_yellow`, green `green`, red `red`, violet `magenta`. No role sets blink, dim or reverse. `Style` objects are cached per `(role, depth)` so an earlier depth in the same process cannot leave stale codes on a later one (Rich caches ANSI codes on a Style, 01 section 7). The file must not contain the literals `Console(`, `NO_COLOR`, `COLUMNS`, `stdout.encoding` or `getpreferredencoding` (also not in comments). |
| 1.3 | Add the `Line` layer | `OBS/render.py` (imports 12-14, `render` 524-531, `screen_lines` 390-521) | New frozen `Span(start: int, end: int, role: str)` (character offsets) and `Line(plain: str, spans: tuple[Span, ...] = ())` with construction helpers `seg(text, role=None) -> Line` and `join(*parts: Line) -> Line` that build in order, so offsets never come from cell widths (wide characters are 2 cells but 1 character, 01 section 8.2). `Line.clipped(width, policy) -> Line` calls `clip()` on `plain` and trims spans to the new length; `ascii_safe` replaces one character with one `?`, so offsets stay valid. `_roled(strings: list[str], role: str) -> list[Line]` wraps existing `wrap(...)` output with one whole-line role. Rename the body of `screen_lines` to `_compose(view, policy, message=None) -> list[Line]` and define `screen_lines(...) = [l.plain for l in _compose(...)]`, so the public signature and every string result are unchanged. `render()` builds `Text(l.plain, no_wrap=True, overflow="crop")` per line and calls `text.stylize(style, span.start, span.end)` only when `policy.color_system` is not `None`. Keep render.py free of `Console(`, `from_markup`, `sorted(`, `.sort(` and of `observe.adapter\|collector\|parse` (`T/test_render.py:400-404`). |
| 1.4 | Assign roles at the builders (no text edits) | `OBS/render.py` (`counts_lines` 94-135, `_row_line` 233-243, `_header_lines` 246-249, `_inspector_lines` 255-287, `_question_line` 311-326, `_desk_lines` 329-356, `_panel_lines` 359-387, footer 514-521) | `header1` `title`; `header2`, `changes_line`, `gap_notice`, `_notes`, `ledger_empty` text and the footer `muted` (the mockups draw the clock and freshness line and the keys hint in muted, 04 section 2); counts tokens: protected tokens `identity`, and the suffix span of a token ending in `UNAVAILABLE` (view.py:100) `muted`; panel title `attention_title`; run, state, disclosure, caveat and retention lines `muted`; `counts_line` `identity`; ledger title `secondary` bold; the question line is built as segments: age `attention` bold, subject `body_bold`, `QUESTIONS_REASON` tail `muted`, and the selected question marker and line `selected` (bold amber, the only list-row text that is amber besides the age; M-18; the glyph stays `glyph("selected")`, RR line 50); `DESK_TITLE` `attention_title`, the desk `qid  age` line (qid and age) `attention` bold, desk question text `attention` bold, field labels `muted`, values `body`. `_row_line` is rebuilt as `_row_segments(row, columns, policy) -> Line`: it appends each `_cell(...)` in order and tags cells; the `nextAction.kind` cell stays `body` (RR line 31, never classified); a cell whose stripped text equals the bare `unknown` is `muted` (a real value `"unknown"` is quoted by `text_of`, view.py:377-385, so the bare word means absent); `workerState`, `dispatchStatus` (full layout only, `_columns` 166-191) and the liveness verdict (`_verdict`, all layouts) take the D-7 mapping `STATE_ROLE: dict[tuple[str, str], str]` in theme.py, keyed by `(field, exact raw value)` (exact string equality on the raw `RowView` value, never a regex and never a substring; for liveness the value is `row.raw.liveness_verdict`, render.py:151-152, and in the `full` layout the cell text is `<verdict> (<source>)`, view.py:509, so only the verdict characters take the role); a flags cell containing `FROZEN_MARKER` (view.py:106) is `state_frozen`. **Minimum fixed table (the D-7 default; values taken from the fixtures under `OBS/fixtures/`, where `workerState` shows running, idle, blocked, exited, succeeded, failed, ready, stopped, abandoned, `dispatchStatus` shows active, blocked, completed, failed, dispatched, and the liveness verdict shows alive, live, ended, exited, unverifiable):** `("workerState", "running")` and `("liveness", "alive")` and `("liveness", "live")` map to `state_running`; `("workerState", "succeeded")` and `("dispatchStatus", "completed")` map to `state_settled`; `("workerState", "failed")` and `("dispatchStatus", "failed")` map to `state_failed`; a flags cell containing `FROZEN_MARKER` is not a tuple key: theme.py holds it as the separate constant `FROZEN_ROLE = "state_frozen"`. Every other value (idle, blocked, exited, ready, stopped, abandoned, active, dispatched, ended, unverifiable, any unseen value) and every `terminalState` and `nextAction.kind` value stays `body`; `terminalState=released` is never styled as done (RR 71). The table is a display choice, not a count mapping, so it does not contradict RR 93 (which records that no verified mapping from `workerState` or outcome to "settled" exists for the SIGNALS bars, AD-2); it is owner decision D-7 and the owner may replace it, but the minimum list above must stay non-empty so RB-10 cannot pass on an empty table. The state word is always printed; before coding, re-read `RowView` construction (view.py:481-518) and the parse.py value sets to confirm the key names. No regex runs over worker-controlled text; roles are attached where the builder already knows the field. |
| 1.5 | Make the one-shot path styled-capable | `OBS/commands.py` (`run_once` 225-247, `LiveScreen` 257-279) | Add `_screen_text(view, policy, *, styled: bool) -> str` that builds `make_console(policy, file=io.StringIO(), record=True)`, prints `render(view, policy)` and returns `console.file.getvalue()` when `styled`, else `console.export_text()`. `run_once` sets `styled = (policy.color_system is not None) and stdout_is_tty`, taking stdout from the same dependency object that `_emit` (200-210) uses. Default per D-4: a piped `--once --width` stays plain. Add `policy.color_system` to the `LiveScreen` shape tuple at line 265, so a depth change rebuilds the `Live`. Do not touch lines 67 and 70 (`QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED`) and keep the words `release-gates.md` and `Task 18` in the file (`T/test_commands.py:747-772` read the source text). |
| 1.6 | Update tests and goldens | `T/test_render.py`, `T/release1_surface.py`, `T/test_terminal.py`, `T/test_theme.py` (new), `T/test_styled_capture.py` (new), `T/live_child.py` (new), `T/test_live_screen_pty.py` (new), `T/conftest.py` | (a) `test_rendering_twice_is_byte_identical_and_no_color_changes_no_text` (test_render.py:250-259): keep determinism and the `screen_lines` equality (:257); replace :256 with `strip_sgr(colour) == nocolor`, and assert that the colour print contains ESC at 160 for the base variant and that the NO_COLOR print contains none. (b) Audit every `printed(` call (:76, :161, :181, :255-256, :277, :605, :977, :987): any that applies `cell_len` or `bad_chars` to colour output first applies `strip_sgr`. (c) `T/release1_surface.py` (`_printed`, lines 34-38, which builds `printed_*` through `make_console` and `render()` and therefore gains SGR bytes once P1 styles `render()`, since an explicit `color_system` makes Rich write SGR even to a `StringIO`): make `_printed` return `strip_sgr(buffer.getvalue())`, importing `strip_sgr` from `tests.observe.conftest` as the module already imports `FakeClock` from there, and add a docstring line that `printed_*` holds the printed text with SGR removed (release 1 wrote none, so the strip changes nothing there). Every `printed_*` value in `surface()` is then plain text, equal to the plain golden bytes, so `test_t47_...` (:611-624) is not edited, no side of the comparison is stripped asymmetrically in any phase, and the golden file bytes do not change in P1. Styled bytes are never stored in a golden; they are pinned by (a), (f) and (g). (d) `test_terminal.py`: depth cases (NO_COLOR, TERM=dumb, COLORTERM truecolor, TERM xterm-256color, none) and `make_console(...).color_system` for each; the literal-options test at :105-116 still passes. (e) `test_theme.py`: every role exists at every depth; the eight palette roles are distinct at `"standard"` (RB-09); the four state roles have four different SGR codes at `"standard"` (RB-10(e)); `STATE_ROLE` contains the tuple keys `("workerState", "running")`, `("workerState", "succeeded")`, `("workerState", "failed")`, `("dispatchStatus", "completed")` and `("liveness", "alive")`, and `FROZEN_ROLE == "state_frozen"` (RB-10(d)); no style has blink; `style_for` returns distinct objects per depth. (f) `test_styled_capture.py`: `_screen_text(styled=True)` at 160, 116, 80 contains SGR and `strip_sgr(...)` equals the `export_text()` text; NO_COLOR gives zero ESC; ASCII stays ASCII; the one-shot CLI path with a non-tty stdout still satisfies `T/test_commands.py:121`. (g) Live gate: `live_child.py` builds the fixture view, calls the real `LiveScreen` (constructor and `draw` signature to be read at commands.py:257-279 when implementing) under `pexpect.spawn` with a fixed pty size (pattern at `T/spike_child.py:64`; `pexpect` is a declared dependency, pyproject.toml:41). `test_live_screen_pty.py` asserts the stream contains `\x1b[?1049h`, SGR bytes with `38;2` when `COLORTERM=truecolor`, only 16-colour codes otherwise, no SGR under `NO_COLOR=1`, no SGR 5 or 6, and no mouse mode sequences (`\x1b[?1000h`, `?1002h`, `?1003h`, `?1006h`). If Rich emits a bare reset under `NO_COLOR`, adjust the assertion with the measured bytes and note it. |
| 1.7 | Render gate | `VP/tools/render_compare.py` | Run G1 to G6 (8.5) with the rubric rows in scope for this phase. |

**Tests and goldens that change:** `T/test_render.py` (lines 250-259, plus `strip_sgr` at the audited `printed(` calls; `test_t47_...` at 611-624 is not edited); `T/release1_surface.py` (`_printed` strips SGR); `T/test_terminal.py` (added cases). New: `T/test_theme.py`, `T/test_styled_capture.py`, `T/live_child.py`, `T/test_live_screen_pty.py`. `T/golden_release1_surface.json` and `T/golden_questions_linkoff.json` do not change.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, every `screen_lines` string (so `lines_*` in both goldens and all whole-line tests), `--once` without `--width`, the gate constant lines in commands.py.

**Rubric rows scored:** RB-01, RB-05 to RB-11, RB-23 (High and Medium must pass).

**Migration or rollback:** revert the phase commit. `color_system` defaults to `"standard"`, so a partial revert of render.py leaves unstyled output. If the `Line` refactor is too wide for one commit, land 1.1 and 1.2 first (no behaviour change), then 1.3 with `_roled` wrapping every existing builder as a single `body` line, then 1.4 builder by builder; each step keeps the suite green.

### Phase 2: Text and budget defects on the existing layouts (headings, keys, counts, title bar)

**Goal:** fix the five findings that are plain-text defects of today's layout and need no frame: missing column heading at 116 and 80, the cut 80-column key list, the split key pair and missing footer rule, the counts strip cut inside a token, and the title bar with a `READ ONLY` badge. Separate the record and snapshot guarantee from the presentation goldens before any golden is regenerated.

**Dependencies:** Phase 1. Owner decision D-2 (re-baseline the goldens; under "freeze questions-off" this phase applies to questions-on screens only) and D-3 for M-13.

**Closes:** M-10, M-11, M-13, M-15, M-16, M-17 (M-17 is optional, Low).

| Step | Action | Files | Details |
|---|---|---|---|
| 2.1 | Split the record guarantee from the presentation golden (do this first) | `T/golden_release1_records.json` (new), `T/release1_surface.py`, `T/test_render.py` | From the current `T/golden_release1_surface.json` keep, per variant (`base`, `empty`, `source-loss`, `injection`, `missing-fields`), only `header1`, `header2`, `gap_notice`, `record_text`, `snapshot_json`, and write them with `json.dumps(..., indent=1, sort_keys=True, ensure_ascii=False)` and no trailing newline (the serialisation measured in 03 section 4a). Add `test_release1_records_are_byte_identical_to_the_recorded_surface` that compares those keys from `surface()`. This file is never regenerated; it keeps "records and JSON snapshot byte-identical" enforced after the presentation golden is re-baselined. |
| 2.2 | Column heading at every width | `OBS/render.py` (`_header_lines` 246-249, gate 497, `ledger_fixed` 438-440; `reserved` 499-501 is read only, no edit) | Add `_heading_rows(view, policy) -> int` returning 2 when `view.visible_rows` else 0, and use it at the two places that today test `policy.width_class == "full"`: the `ledger_fixed` term (line 439) and the gate that appends the heading to `body` (line 497). Do not add the heading rows to `reserved` (lines 499-501): it reads `len(body)`, and the heading rows are already in `body` when it is computed, so a separate addition would count them twice and show one ledger row too few. `_columns` already names the `line` columns (203-204) and the `short` columns (218-221), so `_header_lines(columns, policy)` works for every class. The condition lives in `screen_lines`, not `render()` (FINDINGS cites the wrong function; behaviour confirmed). |
| 2.3 | Key list never cut, key pairs never split, rule above the footer | `OBS/render.py` (`_help_lines` 304-308, footer probe 423-431, footer 514-521) | Add `wrap_groups(text, width, policy) -> list[str]` next to `wrap`: split the help line on two-space separators, pack groups greedily into lines joined by two spaces, and fall back to `wrap` only for a single group wider than the width. `_help_lines` uses it in both branches, removing the `clip(...)` branch for `view.questions is None` (the cause of `e exp>` at 80, measured). Add one rule line `glyph("hrule") * width` before the footer lines and count it in `footer_height` at 423-431 and in the footer branch at 514-521. |
| 2.4 | Counts strip never cut inside a token | `OBS/render.py` (`counts_lines` 94-135, cut path 127-132) | Remove the branch that clips an unprotected token into the remaining room (127-129). A token that does not fit is dropped whole and the line ends with the existing ` >` marker (131), as RR line 20 allows for low-priority tokens; protected tokens keep their wrap path (115-121). Measured defect: `runs seen>` at 80 columns. |
| 2.5 | Title bar with a badge | `OBS/view.py` (constants near 44-114), `OBS/render.py` (head 409-414) | Add the literal `READ_ONLY_BADGE = "READ ONLY"` to view.py so render.py decides no literal (the test name at `T/test_render.py:396` says render never decides literals). In render.py add `_title_bar(lines: list[str], policy) -> list[Line]`: after `wrap(view.header1, width)`, append the badge right-aligned on the first wrapped line if `cell_len(line) + 2 + cell_len(badge) <= width`, else on the last wrapped line by the same test, else on its own right-aligned line. `view.header1` is not edited, so `record_text` (export.py:76) and `header1` in the golden are unchanged. Badge role `attention`. |
| 2.6 | Wide blank band (optional, Low) | `OBS/render.py` (`_columns` 195-196, 215) | Design choice not taken from research: give `line` and `short` the same id rule the `full` class uses (`22 + min(extra, 26)`, render.py:159-192) and let the last, elastic `flags` column take the remainder, so widths stay static (FINDINGS M-17 forbids widths that shift between refreshes). Skip if RB-22 already passes and log the skip. |
| 2.7 | Tests and goldens | `T/test_render.py`, `T/golden_release1_surface.json`, `T/golden_questions_linkoff.json` | Regenerate both presentation goldens from the current tree in the same commit. Link-off golden (command shape from 03 section 4b): `uv run python -I -c "import json,sys; sys.path.insert(0,'.'); from pathlib import Path; from tests.observe.test_linkoff_screen_reference import capture; from tests.observe.conftest import FakeClock; Path('tests/observe/golden_questions_linkoff.json').write_text(json.dumps(capture(FakeClock()), indent=1, ensure_ascii=False)+'\n', encoding='utf-8')"`. Release-1 golden (derived from 03 section 4a, not an approved procedure): the same shape with `from tests.observe.release1_surface import surface` and `json.dumps(surface(), indent=1, sort_keys=True, ensure_ascii=False)` written with no trailing newline, run from the current tree (not from `git archive 9e2608b03`). The `printed_*` values written this way are SGR-free because `_printed` strips SGR (step 1.6(c)), so the regenerated golden holds plain text and `test_t47_...` still compares like with like with no per-key stripping; add `test_presentation_goldens_hold_no_escape_bytes` (neither golden file contains `\x1b`), so a styled capture can never be written into a golden. Retitle the docstring of `test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface` (:611) to say it pins the recorded presentation, since 2.1 now holds the release-1 record guarantee. Re-run and adjust, with evidence, the tests that depend on row counts and line positions: `test_matrix_lines_fit...` (`len(lines) <= 30`, :83), `test_decision_2...` (ledger rows between 1 and 3, :660), `test_line_and_short_forms_follow_kind_id_verdict_age` (:314-326; if it searches the whole screen it must be restricted to row lines now that headings exist at 116 and 80), `test_f08` (:748; passes by construction), `T/test_inspector_scroll.py` (inspector returns earlier, no heading). Add tests: heading present at 116 and 80 when rows are visible and absent when empty; no `>` at the end of the key line at 80; `n/p question` never split across lines; no counts line ends inside a token; `READ ONLY` appears once and every line fits; footer rule precedes the footer. |
| 2.8 | Render gate | `VP/tools/render_compare.py` | Run G1 to G6 (8.5). |

**Tests and goldens that change:** `T/golden_release1_surface.json` (lines and printed keys; regenerated), `T/golden_questions_linkoff.json` (the `116` and `80` lists gain headings, all widths gain the badge; regenerated), `T/test_render.py` (docstring and the position-sensitive tests above). New: `T/golden_release1_records.json` and its test; `test_presentation_goldens_hold_no_escape_bytes`.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, `header1`, `header2`, `gap_notice` (now enforced by `golden_release1_records.json`), the gate lines in commands.py, `--once` without `--width`.

**Rubric rows scored:** RB-12, RB-13, RB-15, RB-20, RB-21, RB-22, plus every earlier row as regression.

**Migration or rollback:** step 2.1 is safe to land alone. After 2.7, rollback is a revert of the commit together with both regenerated goldens. If D-2 is "freeze questions-off", gate 2.2 to 2.6 on `view.questions is not None` and keep the release-1 golden untouched; M-10, M-11, M-13 then stay open for the questions-off screens.

### Phase 3: Frame primitive and single-column titled panes on the questions-on screens (ASCII-safe)

**Goal:** add the frame helper and box glyphs (G-1), then frame the COORDINATOR QUESTIONS list and the DECISION DESK as titled, coloured panes at every width, still one column, with every row counted in the height budget. Re-pin the Q7 hash fixture inside the 80-column frame.

**Dependencies:** Phase 2 (re-baselined goldens), Phase 1 (roles `border_*`). Owner decision D-9 (framed lines in `--once --width` output; step 3.6 assumes the default yes). Questions-off screens are not framed in this phase, so `golden_release1_surface.json` does not change here.

**Closes:** M-02 for the questions list and the desk (the ledger frame closes it in P6); Q7 fixture re-pinned (RB-19).

| Step | Action | Files | Details |
|---|---|---|---|
| 3.1 | Box glyphs with ASCII forms | `OBS/terminal.py` (`GLYPHS` 30-34) | Add, in the same unicode-and-ASCII pair shape as the existing `selected`, `truncate`, `hrule`: rounded `box_tl ╭`, `box_tr ╮`, `box_bl ╰`, `box_br ╯`, `box_h ─`, `box_v │`; heavy `hbox_tl ┏`, `hbox_tr ┓`, `hbox_bl ┗`, `hbox_br ┛`, `hbox_h ━`, `hbox_v ┃`. ASCII forms: corners `+`, horizontals `-`, verticals `\|` (RR line 25). All candidates measured one cell in Rich 15. Never write a box character as a literal in a string: `ascii_safe` (terminal.py:133-135) turns any non-ASCII character into `?`; always go through `glyph()`. |
| 3.2 | Frame helper | `OBS/render.py` (next to `_pad` 83-84) | `MARGIN = 1`, `FRAME_ROWS = 2`, `INNER_PAD = 1`. `_frame(title: str, body: list[Line], width: int, policy: TerminalPolicy, *, weight: str = "round") -> list[Line]` returns lines exactly `width` cells wide: top `tl + h + " " + title + " " + h*fill + tr`, body rows `v + " " + Line.padded(inner) + " " + v` with `inner = width - 4`, bottom `bl + h*(width-2) + br`. The title is clipped to `inner - 2` with `clip()`, so a long title cannot squeeze required body text. Border spans use `border_attention` for `weight="heavy"` and `border_secondary` for `"round"`; the title span is bold in the same colour. `Line.padded(width, policy) -> Line` pads with spaces by `cell_len`. Callers add the one-cell margin with `_indent(lines, MARGIN)`. |
| 3.3 | Thread the inner width | `OBS/render.py` (`_panel_lines` 359-387, `_question_line` 311-326, `_desk_lines` 329-356) | `pane = policy.width - 2*MARGIN`, `inner = pane - 4`. `_question_line(q, policy, inner)` and `_desk_lines(desk, policy, inner)` take the inner width in place of `policy.width`; every `wrap`, `clip` and the `room` arithmetic at lines 320-325 use `inner`. `_panel_lines` builds the body (run line, state, disclosure, counts line, caveat, question rows, cut text, `DESK_SELECTED_HIDDEN`, empty and window-full text, notes, retention) without the title and returns `_frame(panel.title, body, pane, policy, weight=...)`. Weight rule from the mockups: the list pane is heavy when there is no desk, round when a desk is shown; the desk pane is heavy. The desk is a separate frame in this phase (`DESK_TITLE` in its border). |
| 3.4 | Keep the budget exact | `OBS/render.py` (sizing 433-481, `base` 441-443, `spare` 447-457) | `base` is `len(_panel_lines(replace(panel, lines=(), empty_text=None), policy, None))` and `len(desk)` is the length of the returned list, so both include the frame rows with no new term. Keep the three `+1` terms as they are. Where the desk does not fit and `DESK_HIDDEN` replaces it, the notice goes inside the list frame body. The forced single ledger row at render.py:502 is unchanged. |
| 3.5 | Test helpers | `T/conftest.py` | `unframe(line: str) -> str` strips the margin, the left and right border glyph (rounded, heavy and ASCII forms) and one padding cell; `title_of(lines) -> list[str]` returns the text inset in top borders. Both are used only by tests. |
| 3.6 | Update tests (depends on owner decision D-9, default yes: framed lines in `--once --width` output; if D-9 is no, skip the two `T/test_commands.py` edits below and add the `frames` switch described in 8.2) | `T/test_render.py`, `T/test_commands.py`, `T/test_question_cap.py` | Whole-line checks become frame-aware: `DESK_TITLE in lines` (:900, :924, :997) becomes `DESK_TITLE in title_of(lines)`; `startswith("▸ ")` (:897), `startswith("dispatchId:")` (:964 and the desk slice :951-966), `endswith("reason unknown")` (:938, :948), `startswith("questions shown ")` (:479, :646), the exact `window full: older questions may be missing` (:547, `T/test_question_cap.py:77` and `:121`) use `unframe(l)`; `T/test_commands.py:672-675` and `:690` (`COORDINATOR QUESTIONS` and `seen, not resolved: 4 \| closed by evidence: unavailable (no source)` as whole lines of `--once --width` output) use `title_of` and `unframe`. `test_inspector...` at :118-132 is not framed and does not change. `test_decision_2` (:660-676, 8 `reason unknown` lines at height 26): two frame rows now come out of the same budget; re-pin the count from the measured value and record in the commit message that the owner's rule "the questions win on a short terminal" (comment at render.py:444-445) still holds while two fewer questions fit. `test_r3_the_desk_gives_way...` (:990, heights 8 to 60 at 116) keeps passing if every state is still reached; adjust only the height range if a state disappears. |
| 3.7 | Re-pin the Q7 fixture | `T/test_render.py` | The three tests from step 0.6 now read through `unframe`. Expected values (single column): inner width is `width - 6` (154 at 160, 110 at 116, 74 at 80). Ask text: the 64-cell hash stays whole on its own line when words precede it; the fourth desk line still ends in `...` when the ask exceeds four lines. Evidence field `resource.worktreeId` with the 64-cell hash: `label:` on one line, the value on the next line indented two cells (inner minus 2 is 72 at 80, so it fits whole); a value wider than the inner width is hard-split by `wrap()` with nothing lost and no marker (render.py:62-80). All lines at most the width. Both hash canaries (record, snapshot) stay. |
| 3.8 | Height and live checks | `T/test_height_budget.py`, `T/test_live_screen_pty.py` | Extend the height test to the framed questions-on screens at 8 (diagnostic), 12, 24, 40, 44 and the three widths: `len(lines) <= policy.height` or `policy.too_small`. In the pty test at height 24 and 40 assert the last stream row holds the `shown x/y` footer text, so a frame row that overflows (and drops the footer from the bottom, 02 section 9.2) fails the build. |
| 3.9 | Goldens | `T/golden_questions_linkoff.json` | Regenerate with the link-off command from step 2.7 (the link-off questions screen now has frames at all three widths). `T/golden_release1_surface.json` and `T/golden_release1_records.json` are untouched. |
| 3.10 | Render gate | `VP/tools/render_compare.py` | G1 to G6 with the NO_COLOR and ASCII passes mandatory (guard G-1): the ASCII pass must show `+---+` and `\|`, never `?`. |

**Tests and goldens that change:** `T/test_render.py`, `T/test_commands.py` (lines 672-690), `T/test_question_cap.py` (lines 77, 121), `T/conftest.py`, `T/test_height_budget.py`, `T/test_live_screen_pty.py`; `T/golden_questions_linkoff.json` regenerated.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, all questions-off `screen_lines` and `printed_*` (so the release-1 presentation golden), the inspector screen, the too-narrow and too-small diagnostics.

**Rubric rows scored:** RB-02 (questions, desk), RB-07, RB-19, plus all earlier rows.

**Migration or rollback:** revert the commit and the regenerated link-off golden. Frames exist only through `_frame`; the `_panel_lines` and `_desk_lines` changes are reachable only when `view.questions` is set.

### Phase 4: Two-column questions screen, count tile and RETAIN CONTEXT pane (160 and 116; 80 stays stacked)

**Goal:** the questions screen shows the question list on the left and, at widths of 116 and more, a cyan count tile over a RETAIN CONTEXT pane on the right, built only from facts the view already holds. At 80 columns the screen stays one stacked column.

**Dependencies:** Phase 3. Owner decision D-1 (O-1) must be yes; D-3 rules the severity of M-07 and M-14 (treated as Medium until then). If D-1 is no, skip this phase and P5 and keep P3.

**Closes:** M-03 (questions screen), M-05, M-07, M-14.

Target layout (character grid; widths from 8.3, margin 1):

```
 160 / 116 (left = width - 2 - 2 - 42, so 114 at 160 and 70 at 116)       80 (stacked, panes 78)
 +-- COORDINATOR QUESTIONS (heavy, amber) --+  +-- SEEN, NOT RESOLVED ---+     +-- COORDINATOR QUESTIONS --+
 | disclosure (muted)                        |  |  figure (block font)    |     | run, state, disclosure    |
 | > 1h  subject ...  reason unknown         |  |  seen, not resolved: N  |     | counts line, caveat       |
 |   2h  subject ...  reason unknown         |  +-------------------------+     | question rows             |
 | questions shown ...                       |  +-- RETAIN CONTEXT -------+     | retention line            |
 +-------------------------------------------+  | run, caveat, retention  |     +---------------------------+
                                                +-------------------------+
```

| Step | Action | Files | Details |
|---|---|---|---|
| 4.1 | One render-only field for the figure | `OBS/view.py` (panel dataclass at 246-266, `counts_line` built near 761), `T/test_view.py` | Add `count_figure: str = ""` to the panel view, set to the exact figure text already used inside `counts_line` (for example the `100+` form when the window is full), at the same place that builds `counts_line`, so the number logic has one source. The default keeps every existing construction valid. `counts_line`, `run_line` (794), `caveat_line` (798) and `retention_line` (804) are not edited. `OBS/export.py` must not read the new field; add a source-scan test next to `T/test_export.py:238-243` that `count_figure` does not appear in export.py. Read view.py:746-766 before editing. |
| 4.2 | Two-column composer | `OBS/render.py` | `_two_columns(left: list[Line], right: list[Line], wl: int, wr: int, gap: int = 2) -> list[Line]`: rows from `zip_longest(left, right, fillvalue=blank)`, each side padded by `cell_len` to its width, right-side span offsets shifted by the character length of the padded left side plus the gap (character offsets, never cell widths). Geometry constants `RIGHT_WIDTH = 42`, `COLUMN_GAP = 2`; `left = policy.width - 2*MARGIN - COLUMN_GAP - RIGHT_WIDTH` (114 at 160, 70 at 116; elastic for widths between 116 and 159 and above 160). Applies when `policy.width_class` is `full` or `line`; the `short` and `narrow` classes keep the P3 stacked layout. |
| 4.3 | Count tile | `OBS/terminal.py` (`GLYPHS`), `OBS/render.py` | Add glyph `block` (`█`, ASCII `#`). `_count_tile(panel, width, policy) -> list[Line]`: a frame with `border_count` (cyan), title `QUESTIONS_COUNT_LABEL.upper()` (view.py:70-72, no new literal); body: the figure drawn from a 3-by-5 block-glyph font `_BIG` (digits and `+`) in the `attention` role when `inner >= 4 * len(figure)`, else the figure as one bold `attention` line; then `panel.counts_line` wrapped to the inner width in `identity`, so the plain pass keeps `seen, not resolved: N \| closed by evidence: unavailable (no source)` (the text-only form FINDINGS M-05 and the NO_COLOR and ASCII passes require). |
| 4.4 | RETAIN CONTEXT pane | `OBS/view.py` (constants), `OBS/render.py` | Add `RETAIN_TITLE = "RETAIN CONTEXT"` to view.py. `_retain_pane(panel, width, policy) -> list[Line]`: a round slate frame whose body is `panel.run_line`, `panel.caveat_line` and `panel.retention_line` wrapped to the inner width in `muted`. At 160 and 116 these three lines are removed from the left body (they were scattered in three places, M-14) while the pane is drawn, and are put back there if step 4.5 drops the pane under height pressure; at 80 they stay where P3 left them. |
| 4.5 | Compose the questions screen | `OBS/render.py` (`_panel_lines` 359-387, sizing 433-481) | At `full` and `line`: `left = list frame` (disclosure, rows, cut text, `DESK_SELECTED_HIDDEN`, empty and window-full text, notes; roles from P1, rows `body_bold`, caveats `muted`); `right = tile + one blank row + retain pane`. Height rule: the left body takes `capacity` question rows as before; the right column is built against the budget `base_left + capacity`. If it is taller, drop the RETAIN pane first, then the tile, and relocate what each pane held into the left body in the same step: dropping the RETAIN pane puts `panel.run_line`, `panel.caveat_line` and `panel.retention_line` back in the left body in the P3 order (run line near the top, caveat before the rows, retention sentence last), and dropping the tile puts `panel.counts_line` back as a plain left-body line. The run line, the caveat and the retention sentence are required text (RR lines 42, 44 and 48; view.py:67, 73, 794), so a pane is never dropped without its lines being relocated and no fact disappears. The relocated lines are fixed rows of the left body: recompute `base` and `capacity` once with the relocated layout (a single retry, not a loop; the relocated layout is the P3 left body, which already fits), so `capacity` shrinks by the relocated row count and the owner's rule "the questions win on a short terminal" (render.py:444-445) still applies through the unchanged `spare` formula at 447-457. The panel height is therefore always `base_left + capacity`. The question line format `<age>  <subject>  reason unknown` and its two-space separator are not changed (`T/test_render.py:653` and the `^\s*\d+[smh]  ` checks at :930-948 pin them). |
| 4.6 | Pane-aware test helpers | `T/conftest.py` | `split_columns(line, left_width, gap) -> tuple[str, str]` slices by cell width (write it with `cell_len` if the `rich.cells` chop helper differs in 15.0.0); `panes_flat(lines, policy) -> str` returns the whitespace-collapsed left text then the right text, so phrase checks do not read across the gap. |
| 4.7 | Update tests | `T/test_render.py` | Flat checks that read phrases across a row use `panes_flat`: `test_t19...` (:437-453, the `seen, not resolved: 5 \| closed by evidence: unavailable (no source)` phrase, retention sentence, `bounded best effort; coverage unknown`), `test_decision_3_and_4` (:679-700), `test_f17_f15` (:786-805). Row checks use the left column only: the exactly-5 `reason unknown` lines (:453), `questions shown` (:479, :646), `▸ ` (:897). Add tests: figure and `counts_line` present in the plain pass at 160 and 116; no tile at 80; `2*MARGIN + left + COLUMN_GAP + RIGHT_WIDTH == width` for widths 116, 130, 159, 160, 200; degrade order at small heights (RETAIN first, then tile), and at heights 24 and 26 at 116 columns (also 160) the plain screen still contains the run line (`one Run only: <runId>`), the caveat (`no read marker in source: answered questions stay listed`) and the retention sentence (`retention reset at HH:MM; questions observed before this start are not retained`) whether the pane is drawn or dropped, with every line at most the width and at most the height (heights 24 and 26 are chosen to straddle the degrade point; measure the real trigger heights when implementing and add them); `#` block font in ASCII mode and no `?`; `count_figure` is not read by export.py. |
| 4.8 | Golden | `T/golden_questions_linkoff.json` | Regenerate with the step 2.7 command. |
| 4.9 | Render gate | `VP/tools/render_compare.py` | G1 to G6; the reviewer checks tile, pane titles, 114 plus 42 at 160 and 70 plus 42 at 116 against the attention-ledger mockups, and that no invented content (owner, requester, mapped trees) appears (AD-1 to AD-4). |

**Tests and goldens that change:** `T/test_render.py` (flat and row checks above), `T/test_view.py` (default field only), `T/test_export.py` (source scan), `T/conftest.py`; `T/golden_questions_linkoff.json` regenerated.

**Byte-identical in this phase:** `record_text` (it still writes `counts_line`), `snapshot_json`, questions-off screens and both release-1 goldens, the question line text.

**Rubric rows scored:** RB-03 (questions), RB-04, RB-16, RB-17, plus all earlier rows.

**Migration or rollback:** revert the commit and the golden. Restoring the stacked layout needs only `_panel_lines`; `count_figure` is a defaulted field and can stay.

### Phase 5: Decision Desk as question pane plus session-evidence pane (two columns at 160 and 116, three stacked panes at 80)

**Goal:** the question text leads in its own emphasised pane, the linked-session evidence is an aligned `label: value` pane, and the question list sits in its own pane, laid out as in the desk mockups. Show only the one linked session the view already holds.

**Dependencies:** Phase 4 (`_two_columns`, helpers), Phase 3 (`_frame`). Owner decisions D-1 (yes) and D-8 (the evidence pane title, below).

**Closes:** M-04, M-12; completes M-09 on the desk fields.

Target layout (widths from 8.3):

```
 160: +-- DECISION DESK (heavy) ----+  +-- <evidence title> ------------------+
      | qid  age ... / question    |  | dispatchId:           w-002          |
      +-- COORDINATOR QUESTIONS ---+  | workerState:          ...            |
      | rows ...                   |  | resource.worktreeId:  ...            |
      +----------------------------+  | notes (DESK_WORKTREE_NOTE ...)       |
        left 76                          right 80
 116: DECISION DESK (full width 114) over  [<evidence> 66] [COORDINATOR QUESTIONS 46]
  80: DECISION DESK (78) / <evidence> (78) / COORDINATOR QUESTIONS (78), stacked
```

| Step | Action | Files | Details |
|---|---|---|---|
| 5.1 | Evidence pane title | `OBS/view.py` (constants near 85-99) | Add `DESK_EVIDENCE_TITLE`. The mockup titles are `AFFECTED SESSION EVIDENCE` and `AFFECTED SESSIONS`, which claim more than the code knows (AD-4: one linked session, no requester, owner or affected list; `DESK_WORKTREE_NOTE` view.py:87-90). The default wording is `LINKED SESSION`, reusing the existing link vocabulary (`linked`, parse.py:468-472); wording is decision D-8 and a spec edit to RR line 57. The render gate accepts any title that does not claim an affected list. `DESK_TITLE` (view.py:85) stays the desk question pane title, so tests that look for it keep one literal. |
| 5.2 | Aligned field lines | `OBS/render.py` (replaces the field loop at 347-353) | `_field_lines(label: str, value: str, inner: int, label_width: int, policy) -> list[Line]`. If `cell_len(value) <= inner - label_width - 1`: one line, label `muted` padded to `label_width`, value in its role. Otherwise the label line, then the value wrapped to `inner - 2` with a two-cell indent (today's behaviour, render.py:347-353). `label_width` is the longest label plus its colon across `desk.session_fields` (`resource.worktreeId:` is 20 cells). Values of `workerState`, `dispatchStatus` and the liveness verdict use `STATE_ROLE` from P1; `nextAction.kind` stays `body` (RR line 31). Field order is the order of `session_fields` (view.py:843-853), unchanged. |
| 5.3 | Pane builders | `OBS/render.py` (`_desk_lines` 329-356) | `_desk_question_pane(desk, width, policy) -> list[Line]`: heavy frame titled `DESK_TITLE`; first body line `qid  age <age>` (age `attention` bold, as the list ages and RB-01(c) require; `attention` bold qid), then `wrap(desk.ask, inner)` limited to `DESK_TEXT_LINES` (view.py:99) with the last line cut by `...` as today, in `attention` bold. `_desk_evidence_pane(desk, width, policy)`: round slate frame titled `DESK_EVIDENCE_TITLE`, the field lines from 5.2, then `desk.notes` wrapped in `muted`. Both are pure functions of `DeskView` and never read `View` record fields; the question text is read only here and in `_question_line` (screen-only rule). |
| 5.4 | Compose and budget | `OBS/render.py` (`_panel_lines` 359-387, sizing 458-479) | At `full`: left = question pane over the list frame (round, P3 rule), right = evidence pane, joined by `_two_columns` with `RIGHT_DESK = 80` and `left = width - 4 - 80` (76 at 160). At `line`: question pane at full width, then `_two_columns(evidence, list, wl = width - 4 - 46, wr = 46)` (66 and 46 at 116). At `short`: three stacked frames. The panel height is `max(left, right)` at `full` and the sum of the parts elsewhere. When the available rows are fewer than the question pane plus one list row, or fewer than the evidence pane, use the existing `DESK_HIDDEN` notice path (view.py:97, render.py:458-471) instead of a partial desk, so a half-drawn desk never reaches the screen. `DESK_TEXT_LINES` stays 4; note that at 160 the question pane inner width is 72, so a long ask reaches the `...` cut sooner than the old full-width text (decision D-6 covers any change to the cap). |
| 5.5 | Tests | `T/test_render.py`, `T/conftest.py` | Add `pane_body(lines, title, policy) -> list[str]` that returns the unframed body of the frame whose top border contains the title. Rework the R3 tests on it: `:891` (`▸ ` row in the list pane, `DESK_TITLE` in `title_of`, flat `dispatchId: w-002` through `panes_flat`), `:919` (unlinked reasons in the evidence pane, `dispatchId:` absent), `:930` (age and `reason unknown` per row in the list pane), `:943` and `:958` (desk text bounded to four lines with `...` at 80 columns: now `pane_body(lines, DESK_TITLE)`), `:970` (hostile text inert), `:985`, `:990` (desk gives way by height at 116), `:1009`, `:1017`. New tests: label column is aligned across all fields; a value that does not fit beside its label moves to its own indented line and a value wider than the inner width is hard-split with nothing lost; the Q7 hash (RB-19) is whole in the question pane at 160 (inner 72), 116 (inner 110) and 80 (inner 74); a 64-character `resource.worktreeId` at 116 (evidence inner 62) is hard-split with nothing lost; a desk screen is never taller than `policy.height` at 8, 12, 24, 40, 44. |
| 5.6 | Golden | `T/golden_questions_linkoff.json` | Unchanged by this phase (the link-off screen has no desk). `T/golden_release1_surface.json` unchanged. |
| 5.7 | Render gate | `VP/tools/render_compare.py` | G1 to G6 with screens `desk` and `desk-planask`; the reviewer scores RB-03 (desk), RB-14, RB-10 on the desk fields, RB-19 and the earlier rows. |

**Tests and goldens that change:** `T/test_render.py` (R3 block), `T/conftest.py`. No golden changes.

**Byte-identical in this phase:** `record_text` (question lines still `q.text`, never `q.shown` or `q.ask`), `snapshot_json`, questions-off and link-off screens.

**Rubric rows scored:** RB-03 (desk), RB-10 (desk fields), RB-14, RB-19, plus all earlier rows.

**Migration or rollback:** revert the commit. `DESK_EVIDENCE_TITLE` is an unused constant after a revert. If D-8 changes the wording, only the constant and the golden-free tests that name it change.

### Phase 6: Ledger screen panes (attention slot, observation window, framed table)

**Goal:** the ledger screen (questions off) gets the same pane vocabulary: the existing gap notice in an amber attention pane, the existing freshness, counts and changes lines in an observation pane, and the worker table in a titled pane, using only data already on the screen. No owner, requester, mapped-tree or SIGNALS content (AD-1 to AD-4).

**Dependencies:** Phase 3 (`_frame`), Phase 2 (headings at every width), owner decision D-2. Under "freeze questions-off" this phase is blocked for the questions-off screens and M-06 stays open.

**Closes:** M-06; completes M-02 (all panes titled and boxed).

| Step | Action | Files | Details |
|---|---|---|---|
| 6.1 | Measure before choosing the 160-column frame | `OBS/render.py` (`_flags_text` 141, `_columns` 155-230) | The full table uses all 160 cells (render.py:159-192: 2 + 114 + 22 + 12 + 10), so a border needs 2 cells from the elastic `flags` column. Measure the longest `_flags_text` over the fixtures (`base`, `empty`, `source-loss`, `injection`, `missing-fields`, `long-identifiers`) and the `FROZEN` marker case. [UNVERIFIED: this was not measured.] If `flags` at 10 cells does not clip, use a border-only frame (no padding, no margin, inner width `width - 2`) for the table at every width; otherwise keep the 160-column table unframed under a titled rule and frame it only at 116 and 80. Record the result in the commit message. |
| 6.2 | Parameterise the columns | `OBS/render.py` (`_columns` 155-230, `_row_segments`, `_header_lines`) | `_columns(policy, avail: int)` uses `avail` instead of `policy.width` in every width sum; callers pass the pane inner width. The three layouts keep their column sets (AD-3, AD-6). Rows and heading clip to `avail`. |
| 6.3 | Compose the head | `OBS/render.py` (head 409-414, gap part 482-485, `_notes` 290-301) | Order: title bar (P2), attention pane (heavy amber, title `QUESTIONS_TITLE`, body `view.gap_notice`, or `panel.summary` when questions are on and nothing is read yet, as render.py:482-485 does today), observation pane (round slate, title `OBSERVATION WINDOW`, body `header2`, the counts lines and `changes_line`; `counts_lines` is called with the inner width, so M-16 still holds), then the ledger pane (round slate, title `view.ledger_title`, body heading and rule, rows, and the overflow line `window.text  window.more_text`). `QUESTIONS_TITLE` reuses the panel title because the gap notice is what the questions panel replaces (`panel.replaces_gap`). `OBSERVATION WINDOW` is the mockup pane title for the per-source freshness line that `header2` already carries; any other wording is a spec edit. The `/filter` input line, the one-off message and the footer stay outside the frames. |
| 6.4 | Small-height fallback | `OBS/render.py` (`_compose`) | Build the framed head; if the framed screen would leave fewer than three ledger rows at `policy.height`, use the P2 plain head instead (the height matrix includes 12, where `golden` keys `lines_*x12` must stay plain). Threshold chosen from measured row counts at heights 12, 24 and 40, and recorded; the forced single row (render.py:502) remains the last resort. Every frame row is in `top` or `body`, so `reserved` and `capacity` (499-503) account for it. |
| 6.5 | Tests | `T/test_render.py`, `T/test_commands.py`, `T/test_golden_contract.py`, `T/test_question_cap.py` | Frame-aware versions of the whole-line checks on the ledger screen: `GAP_NOTICE in lines` (:242, :490, :494, :509 and `T/test_commands.py:121`) becomes `GAP_NOTICE in [unframe(l) for l in lines]`; `no successful worker-list read yet` and the two `no observed items` lines (:352-356); `^\d+/80 shown\s+\+\d+ more` (:94, :337); row `startswith` checks (:373-375, `▸`, ` *`) through `unframe`; the header and row checks at :287-326; `collected 100 / reported 428` stays on one line (`T/test_golden_contract.py:43-58`). `T/test_inspector_scroll.py` is unaffected (the inspector returns earlier, render.py:488-493). New: at heights 12 and 8 the screen falls back to the plain head; at 24, 40, 44 the framed screen has at most `policy.height` rows; no pane holds invented content (a source scan that the pane bodies are built from `view.gap_notice`, `header2`, counts, `changes_line`, the ledger rows). |
| 6.6 | Goldens | `T/golden_release1_surface.json` | Regenerate (step 2.7 command; `printed_*` stays SGR-free through `_printed`, step 1.6(c), and the no-escape test of step 2.7 must still pass). Expected diff: `lines_{160,116,80}x40` and `printed_*` for the five variants; `lines_*x12` unchanged if 6.4 keeps the plain head at 12. `T/golden_release1_records.json` and `T/golden_questions_linkoff.json` unchanged. |
| 6.7 | Render gate | `VP/tools/render_compare.py` | G1 to G6; RB-02 (ledger), RB-18, and all earlier rows. |

**Tests and goldens that change:** the tests above; `T/golden_release1_surface.json` regenerated.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, `header1`, `header2`, `gap_notice` (enforced by `golden_release1_records.json`), the link-off golden, the inspector screen.

**Rubric rows scored:** RB-02 (ledger), RB-18, plus all earlier rows.

**Migration or rollback:** revert the commit and the regenerated golden. The fallback in 6.4 means a revert is also possible per height without touching the pane code.

### Phase 7: Spec reconciliation, final gate matrix and PR

**Goal:** make the written spec match the built screens, run the complete gate matrix once, and open the PR as the repository requires.

**Dependencies:** Phases 1 to 6 closed (or P4 and P5 skipped by D-1). Owner decision D-11 (RR 61 wording) for step 7.1.

**Closes:** no finding on its own; it records the spec changes the closed findings require.

| Step | Action | Files | Details |
|---|---|---|---|
| 7.1 | Spec edits | `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` | Lines 17 (title bar and badge), 25 (box glyph ASCII forms), 41 (RETAIN CONTEXT built), 43 and 57 (two columns, if D-1 is yes), 61 (reconcile with RR 42: the two 80-column invariant lines and "reachable only through the inspector"; the owner chooses the wording, G-H), 70 (muting implemented), 20 (token reads `POLICY FROZEN unavailable (no source)`, view.py:948), 33 (the `flags` column exists at 116 and 80). Pane titles `OBSERVATION WINDOW`, `RETAIN CONTEXT` and the D-8 desk evidence title are recorded there. |
| 7.2 | Keep the baseline capture honest | `VP/inputs/tools/render_current.py` | Update its docstring (lines 6-9 say the ANSI captures are empty of escapes). Keep `VP/inputs/current/` as the pre-fix baseline; write the post-fix harness output under the gate output directory, not over it. |
| 7.3 | Final gate matrix | `VP/tools/render_compare.py`, `T/test_live_screen_pty.py` | `render_compare.py --check --heights 44,40,24,12,8` exactly as defined in step 0.3: widths 160, 116, 80 at the mockup heights (48, 42, 42) and the text matrix at heights 44, 40, 24, 12, 8; the five passes truecolor, 256, 16-colour, NO_COLOR, ASCII; a pty run at each width; one fresh reviewer per width scores every rubric row. Every High and Medium row must pass; Low rows pass or are logged as deferred. |
| 7.4 | Optional Zellij manual check (not a gate) | `VP/zellij-note.md` (new) | Q6 is no-go as a dependency. If the owner wants it, run in a live Zellij 0.44.2 session: `zellij action dump-screen --help` first (the online docs describe a newer release, web-02 A7), then the observer in a pane and `zellij action dump-screen --ansi`; record colour, box and wide-glyph fidelity. The observer may read `ZELLIJ` as a hint, never as a requirement (web-02 A5, external context). [UNVERIFIED until run.] |
| 7.5 | Full checks | repo root | `uv run pytest tests/observe/ -v`, `make test`, `make lint`; confirm `T/test_commands.py:747-772` pass (gate lines intact); confirm `git diff` has no change to `src/superclaude/cli/observe/export.py` and no staged `.claude/` path; stage `.dev/tasks` as the repository rule requires. |
| 7.6 | Open the PR | branch | Verify `git remote get-url origin` and `gh repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner` both name `IronbellyOrg/IronClaude`; `git fetch origin` and rebase onto `origin/master` before pushing; then run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` and check that the returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N`. Never a bare `gh pr create`, never the upstream repository. |

**Tests and goldens that change:** none in code; spec and docstring only.

**Rubric rows scored:** all rows, final.

**Migration or rollback:** documentation only; revert the commit.

### 8.8 Open items, [UNVERIFIED] claims and research findings excluded from plan steps

Items below are not asserted as fact in any step. Where a step depends on one, the step says so.

| Item | Tag | Where it bites | Handling |
|---|---|---|---|
| Playwright MCP can turn Rich `export_html` into a faithful PNG offline; DejaVu Sans Mono covers the mockup glyphs | [UNVERIFIED] | Step 0.4, gate G3 | Proven once in 0.4; fallback is the text and ANSI tier |
| A reviewer subagent has no Playwright tool, only Read | assumption | G3, G4 | The session rasterises; the reviewer only Reads PNGs (both Gate 1 QA reviewers read mockup PNGs successfully) |
| Constructor and `draw` signature of the real `LiveScreen` under a pty; whether `run_interactive` accepts `--fixture` | [UNVERIFIED] | Step 1.6(g) | Read commands.py:257-279 at implementation time; the child builds `LiveScreen` itself |
| Whether Rich emits a bare reset under NO_COLOR with `Live` | [UNVERIFIED] | Step 1.6(g) | Measure, then fix the assertion |
| Mapping from real `workerState`, `dispatchStatus` and liveness words to the four state colours | [UNVERIFIED], RR 93 says no verified settled mapping | Step 1.4 | Only the minimum fixed `STATE_ROLE` table of step 1.4 is coloured (owner decision D-7, default stated); every other value is `body`; the word is always printed |
| Longest `_flags_text` versus the 10-cell `flags` column | [UNVERIFIED] | Step 6.1 | Measure first; fallback is an unframed 160-column table |
| Which of the three `+1` terms in `spare` is which (render.py:454-456) | [UNVERIFIED] | Steps 3.4, 5.4 | Read the comment at render.py:444-445 first; the terms are not edited |
| Exact `PYTHONPATH` layout and approval for regenerating the release-1 golden | [UNVERIFIED] | Step 2.7 | The plan regenerates from the current tree, not from release 1 source |
| Whether East-Asian-ambiguous box and block glyphs are one cell in the owner's terminals | [UNVERIFIED] | All frames | Rich's `cell_len` says one; carry as a caveat |
| Mockup background (dark navy) and light-terminal behaviour of the palette | [UNVERIFIED] | RB-01 | Background is not scored |
| Selected-question look (M-18) | [UNVERIFIED] (no selected row in any mockup) | Step 1.4 | Scored against RR line 50 (glyph kept) plus a bold amber role, not against a mockup |
| Plan-approval ask content (path, file list, 64-hex hash) stored as question rows | [UNVERIFIED] (`pr-591-comment.md` lines 26-31) | Q7 fixture | Fixture is synthetic; confirm with the plan-ask source |
| Zellij: floating panes, `dump-screen --ansi` fidelity, command panes, theme read at runtime, presence in CI | [UNVERIFIED] | Step 7.4 only | Not a dependency (Q6) |
| Interaction of fixtures `injection` and `long-identifiers` with styling | [UNVERIFIED] | Phase 1 gate | Include both in the harness matrix |
| Owner rulings D-1 to D-12 and OPEN-1 to OPEN-3 | open | see 8.2 | Defaults stated; effect if different stated |

Research findings that are deliberately not in a plan step:

| Finding | Rationale for exclusion |
|---|---|
| Rich `Panel`, `Table`, `Layout`, `Columns` returned from `render()` (03 option P5, 01 option 4) | Breaks `T/test_render.py:399`, adds height uncertainty, and `safe_box` does not give ASCII borders; rejected in 8.1 Q1 |
| Block digit font as a hard requirement | FINDINGS does not require it (01 section 8.2 item 6); the plan uses it when the tile is wide enough and falls back to a bold figure |
| Age gutter (fixed-width age column) from M-07 | The `<age>  <text>` two-space form is pinned (`T/test_render.py:653`, :930-948) and RR line 50 fixes the age format; not changed |
| SIGNALS bars and tiles, "8 owners / 80 sessions / 80 mapped trees", two-line register rows, requester, owner, Affected lines | Accepted divergences AD-1 to AD-4: no real data behind them |
| Three-column signal-bridge layout at 160 | The full table needs all 160 cells (render.py:159-192); AD-3 |
| `export_text(styles=True)` as the styled capture | Ignores NO_COLOR and the colour downgrade (probe, 02 section 2) |
| cairosvg, `rsvg-convert`, freeze, pyte, aha, ansi2html, Pillow | Not installed; Rich SVG needs a browser engine (external: https://github.com/Textualize/rich/issues/2153); each is a new dependency or binary needing owner approval; the plan adds none |
| Reading the Zellij theme at runtime; Zellij chrome row arithmetic | Unverified, and Zellij is not a dependency |
| Making a styled piped `--once --width` the default | Open decision D-4; the default keeps `T/test_commands.py:121` |
| Rich's own NO_COLOR (keeps bold and dim) | The project keeps `color_system=None` under NO_COLOR (G-2); changing it is a separate owner decision |

### 8.9 Integration Checklist

| # | Check | Evidence to attach | Phase |
|---|---|---|---|
| 1 | `uv run pytest tests/observe/ -v` is green at the end of every phase (baseline 766 passed; count grows with added tests) | pytest summary line | all |
| 2 | `T/golden_release1_records.json` exists, is never regenerated, and passes | test result | P2 onward |
| 3 | `record_text`, `snapshot_json` and `export.py` are untouched; `count_figure` is not read by export.py | `git diff --stat` shows no `export.py` change; source-scan test | all |
| 4 | Question text appears only on screen: both hash canaries pass (record and snapshot) | test result | P0 onward |
| 5 | Gate lines `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (commands.py:67, 70) unchanged; `release-gates.md` and `Task 18` still in commands.py | `T/test_commands.py:747-772` | P1 onward |
| 6 | No `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in render.py; no `Console(`, `NO_COLOR`, `COLUMNS` literal outside terminal.py (also not in `theme.py` comments) | `T/test_render.py:400-404`, `T/test_terminal.py:181-198` | P1 onward |
| 7 | `len(group.renderables) == len(screen_lines(...))` still holds | `T/test_render.py:399` | all |
| 8 | NO_COLOR pass has zero ESC bytes and the same text as the coloured pass after SGR removal, at 160, 116, 80 | `checks.json` | all |
| 9 | ASCII pass is pure ASCII with `+ - \|` borders and `#` block glyph; no `?` where a border or glyph belongs | `checks.json` | P3 onward |
| 10 | No SGR 5 or 6 and no mouse mode sequence in any pass or in the live pty stream | `checks.json`, pty test | all |
| 11 | Every line at most the width in cells and at most the height in rows at 8 (diagnostic), 12, 24, 40, 44, 48; the footer is the last live row | height test, pty test | P0 onward |
| 12 | The 16-colour theme has eight distinct role colours | `T/test_theme.py` | P1 |
| 13 | Both presentation goldens regenerated from the current tree with the recorded command, in the same commit as the change that moved them | commit diff | P2, P3, P4, P6 |
| 14 | One fresh reviewer per width scored the in-scope rubric rows; at most 3 iterations; all High and Medium rows pass; stop log written if not | `VP/scores/<phase>/` | all |
| 15 | OPEN-1, OPEN-2, OPEN-3 treated as Medium until the owner rules; D-1 to D-12 recorded with the owner's answer | decision record in the PR body | P2, P4, P5 |
| 16 | `make lint` and `make test` pass; no `.claude/` path staged; `.dev/tasks` staged | command output, `git status` | P7 |
| 17 | PR opened only by `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; branch rebased on `origin/master`; returned URL checked | PR URL | P7 |

### 8.10 Finding-to-phase map (M-01 to M-18)

The Severity column quotes FIND (High, Med, Low); in the Section 4 scale High = Critical, Med = Important, Low = Minor.

| ID | Finding (short) | Severity per FINDINGS | Closing phase | Steps | Rubric row |
|---|---|---|---|---|---|
| M-01 | No colour or weight | High | P1 (frame and tile colours added in P3, P4, P6 and re-scored) | 1.1 to 1.6 | RB-01, RB-09 |
| M-02 | No boxed titled panes | High | P6 (questions and desk panes in P3) | 3.1 to 3.3, 6.3 | RB-02 |
| M-03 | Questions screen has no two columns | High | P4 | 4.2, 4.5 | RB-03 |
| M-04 | Decision Desk stacked | High | P5 | 5.3, 5.4 | RB-03 |
| M-05 | Count has no weight | High | P4 | 4.1, 4.3 | RB-04 |
| M-06 | Ledger lacks attention slot, observation pane | Medium | P6 | 6.1 to 6.4 | RB-18 |
| M-07 | Caveats outweigh question rows (OPEN-1) | Medium | P4 | 4.4, 4.5 | RB-16 |
| M-08 | Absent values not muted | Medium | P1 | 1.4 | RB-11 |
| M-09 | State values uncoloured | Medium | P5 (ledger rows in P1, desk fields in P5) | 1.4, 5.2 | RB-10 |
| M-10 | No column heading at 116 and 80 | Medium | P2 | 2.2 | RB-12 |
| M-11 | 80-column key list cut | Medium | P2 | 2.3 | RB-13 |
| M-12 | Desk emphasis and alignment | Medium | P5 | 5.2, 5.3 | RB-14 |
| M-13 | Title bar and READ ONLY badge (OPEN-3) | Medium | P2 | 2.5 | RB-15 |
| M-14 | No RETAIN CONTEXT (OPEN-2) | Medium | P4 | 4.4, 4.5 | RB-17 |
| M-15 | Footer pair split, no rule | Low | P2 | 2.3 | RB-20 |
| M-16 | 80-column counts cut inside a token | Low | P2 | 2.4 | RB-21 |
| M-17 | Wide blank band after id | Low (optional) | P2 | 2.6 | RB-22 |
| M-18 | Selected question glyph only | Low | P1 | 1.4 | RB-23 |

Guards, questions and accepted items: G-1 is enforced from P3 (steps 3.1, 3.2, 3.10 and RB-07, re-run in every later gate); G-2 closes in P1 (steps 1.1, 1.2, RB-09); Q4 P1; Q5 P1 (steps 1.5, 1.6); Q7 P0 (0.6) and P3 (3.7), re-pinned in P5 (5.5); Q6 P7 step 7.4 (not a gate); AD-1 to AD-7 are respected by the "no invented content" check in the P4 and P6 gates; the spec lines changed by the closed findings (RR 17, 20, 25, 33, 41, 43, 57, 61, 70) are edited in P7.

### Summary

The plan keeps the string pipeline as the single source of text and adds, in order: a harness and baseline (P0); a theme, colour-depth detection, role spans and the styled-capture gates (P1); text and budget fixes with the record guarantee split from the presentation golden (P2); a hand-built frame primitive with ASCII glyphs on the questions-on screens (P3); two-column questions, count tile and RETAIN CONTEXT (P4) and two-column Decision Desk (P5), both gated on owner decision O-1; ledger panes (P6); and spec reconciliation, the final gate matrix and the PR (P7). Every phase ends with a render gate (render at 160, 116 and 80 including NO_COLOR and ASCII, a fresh reviewer scores the fixed rubric against the mockups, at most 3 iterations) and closes only when all in-scope High and Medium rows pass. `record_text`, `snapshot_json` and the question-text-on-screen-only rule are never touched, and the Q7 hash fixture is added before any layout change and re-pinned inside the frames.


## 9. Open Questions

Tags: [UNVERIFIED] = claim not confirmed by code or a probe; [CODE-CONTRADICTED] = the claim in a document or earlier draft is wrong and the pending fix is a document or spec change. Web findings are external context and carry their source URL. Where research files disagree, the row says which finding has the stronger evidence. Rows 1 to 4, D-7 and D-8 in 9.1 are open owner decisions (O-1, OPEN-1 to OPEN-3, and the plan decisions D-7 and D-8); the other plan decisions D-2, D-4, D-5, D-6, D-9, D-10, D-11 and D-12 are carried by the rows of 9.2 named under the 9.1 table.

### 9.1 Owner decisions (open)

| # | Question | Impact (what it blocks) | Suggested Resolution |
|---|---|---|---|
| 1 | O-1 (OPEN owner decision): adopt two-column layouts for the questions screen and the Decision Desk at 160 and 116 columns, reversing the "one stacked block at every width" choice in `rendering-rules.md` lines 43 and 57 (source: FINDINGS.md line 171; research 04). | Blocks Q1 (composition choice), findings M-03 and M-04 (both High) and, in part, M-06 and M-14; blocks the spec edits to RR 17, 41, 43, 57 and 61, which must land in the same change. Mockup column pairs needed: 160 ledger 114 + 42, 160 desk 76 + 80, 116 ledger 70 + 42, 116 desk full width over 66 + 46; 80 stays stacked (research 04 section 4). | Recommendation in FINDINGS and research 04: yes, keep 80 columns stacked, update the spec text in the same change. The owner must rule; both merged reviewers agreed it needs the owner. Until ruled, plan P4 and P5 (the two-column phases of the report plan, Section 8) as gated. |
| 2 | OPEN-1 (OPEN): severity of the question-list hierarchy, M-07. Astra High (one combined item); Opus Medium (avoids counting lost question primacy three times). | Decides phase order and gate strictness for question-row emphasis and separators. Handled as Medium (gated) today. | By Opus's own condition it is Medium because M-03 is High; keep Medium (gated) unless the owner rules otherwise. |
| 3 | OPEN-2 (OPEN): severity of RETAIN CONTEXT (M-14) and whether the pane is built at all. Opus ended Medium, Astra Low. Facts live in three places today (`run_line`, `caveat_line`, `retention_line`, view.py:794, 798, 804). | Changes RR 41 ("not built in R2") and RR 61 ("reachable only through the inspector"); decides whether `_panel_lines` (render.py:359-387) gains a retention pane and whether a late phase exists. | Treat as Medium (gated), schedule in a late phase either way; owner rules on building it. Keep it render-only: `record_text` reads the same view strings. |
| 4 | OPEN-3 (OPEN): title bar, M-13. Opus Low with the left-title and right-badge split in scope; Astra Medium for one combined identity region, badge Low, exact alignment and diamond glyph optional. | The `READ ONLY` badge is absent from all of `src/superclaude/cli/observe/`; the header contract RR line 17 has no badge and must be reconciled. `header1` is one string shared with `record_text` and the release-1 golden (view.py:914-921). | Treat as Medium (gated); the badge is required, exact alignment is the owner's or the claiming agent's call. Build the split inside render.py only so the record and goldens stay unchanged. |
| D-7 | Mapping from real `workerState`, `dispatchStatus` and liveness words to the four state colours (M-09). The code and spec state no meaning for these words and RR 93 records that no verified settled mapping exists (it concerns the SIGNALS bars, AD-2). | Decides which state words are coloured; RB-10 and SC-6 are scored against the table. | Default: the minimum fixed `STATE_ROLE` table of plan step 1.4 (running, alive, live; succeeded, completed; failed; the `FROZEN` flag); all other values neutral; the word is always printed. The owner confirms or replaces the table. |
| D-8 | Title of the Decision Desk evidence pane; the mockup titles claim an affected-session list the code does not have (AD-4). | Blocks the wording of one constant and the RR 57 edit (plan step 5.1). | Default `LINKED SESSION`; any title that does not claim an affected list is acceptable. |

The full owner-decision set of the plan is D-1 to D-12 (Section 8.2; Section 7.3 lists the same set). Where each one sits in this section: D-1 is row 1; D-3 is rows 2 to 4; D-2 is row 5; D-5 is row 6; D-12 is row 7; D-4 and D-9 are both in row 8; D-11 is row 14; D-6 is row 10; D-10 is row 15; D-7 and D-8 are the two rows above.

### 9.2 Decision-level gaps (Important in the gaps log)

| # | Question | Impact (what it blocks) | Suggested Resolution |
|---|---|---|---|
| 5 | G-A (D-2), golden re-baselining. T47 (`test_render.py:611-624`) pins questions-off `lines_*` and `printed_*` to release 1; T64 (`test_linkoff_screen_reference.py`) pins link-off questions screens. Any visual change to those screens (heading lines at 116 and 80, uncut key list at 80, borders, tile) breaks them. | Blocks every phase that changes questions-off or link-off screen text. A style-only phase changes only the 15 `printed_*` values; a layout phase changes all 30 `lines_*` plus both goldens (research 03 sections 4 and 6). Regeneration must run from the current tree, which ends the "byte-identical to release 1" meaning of T47. | Owner chooses one: re-baseline both goldens; keep the questions-off screen frozen and apply the redesign only when questions are on; or add a new golden and keep T47 for the plain screen. Issue body `.dev/issues/606/issue-body.md:84` lists these files as deliberate presentation updates. |
| 6 | G-B / Q-5 (D-5), colour depth and detection (Q4, guard G-2). `make_console` is fixed at `"standard"` (terminal.py:121); nothing detects COLORTERM or TERM. Measured downgrade table (research 04 section 3): standard base 15, muted 7, slate 8, amber 11, cyan 14, green 7, red 7, violet 7. [UNVERIFIED] capability at run time (mapping computed with Rich, not observed on a terminal). | Blocks the theme definition and state colours (M-09): at 16 colours green, red, violet and muted all collapse to index 7, so colour cannot carry state alone. Contradiction: research 01 section 7 inferred slate and muted collapse to greys and missed the state collapse; the measured 04 table (reproduced by two reviewers) has stronger evidence and is the one to use. | Owner decides target depths (16 only, or truecolor with 16-colour fallback). Define per-depth explicit roles with named ANSI colours (for example green 2/10, red 1/9, magenta 5/13) plus dim/bold and text that carries state. External context: `color_system="auto"` reads COLORTERM (truecolor or 24bit) then the last part of TERM, default standard (https://rich.readthedocs.io/en/stable/console.html); Rich gives no colour on a non-terminal file under auto (probe in research 01). |
| 7 | NO_COLOR policy for bold and dim (D-12). Code uses `color_system=None` plus `no_color=True`, which drops bold and dim as well as colour (probe, research 01 section 7). External context: Rich's own NO_COLOR keeps bold, dim, italic and underline (https://rich.readthedocs.io/en/stable/console.html; `Style.render` source at https://github.com/Textualize/rich/blob/v15.0.0/rich/style.py). | Decides whether hierarchy under NO_COLOR can use bold and dim or must live entirely in text and glyphs (finding G-1 assumes text and glyphs). | Keep `color_system=None` (strictest, matches the existing tests at `test_terminal.py:40-51` and `test_render.py:985-987`) unless the owner wants bold and dim kept; then use `no_color=True` with a colour system and rewrite those tests. Carry as an explicit decision. |
| 8 | G-C (D-4 and D-9), styled capture route (Q5). `--once --width` calls `export_text()` without styles (commands.py:242), so the nine ANSI exports hold 0 ESC bytes. Options: plain `export_text()`; `console.file.getvalue()` through `make_console`; `export_text(styles=True)` (ignores NO_COLOR and the colour downgrade, probe-verified). Also open: may a piped `--once --width` carry ANSI by default or only on a tty (no tty check exists, commands.py:238-245); may `--once --width` ever include box-drawing lines (research 03 gap 5). Research 01, 02 and 03 gave conflicting advice; 02 wins (probe on Rich 15.0.0). | Blocks the styled-capture gate, the test at `test_commands.py:121` (`"\x1b" not in out`) and the Phase 0 harness. Web-02 B8 inferred the recording console is simply not configured for NO_COLOR or 16 colours; the local probe (`export_text(styles=True)` bypasses both) has stronger evidence. | Use `console.file.getvalue()` via `make_console` for styled capture; keep plain `export_text()` for the default one-shot text; decide the tty rule (D-4, default: styled bytes only on a tty) and the box-line question (D-9, default: yes, framed lines are allowed in `--once --width` output; plan step 3.6 assumes it and 8.2 states what changes if the owner rules no). Keep the record tests (`test_commands.py:99, :105`, `test_export.py:53`) unchanged. |
| 9 | G-D / Q1 mechanism: may `render()` return multi-line Rich renderables (`Panel`, `Table`, `Columns`, `Layout`) or must it stay one `Text` per line? `test_render.py:399` pins `len(group.renderables) == len(screen_lines(...))`; `test_render.py:401-404` forbids `Console(`, `sorted(`, `.sort(`, `from_markup` in render.py. External context: web-01 recommends the line model plus a thin style layer over Panel/Table/Layout (derived from Rich source, not a documented pattern). | Decides composition for Q1 and whether phase P5 (research 03 section 6) exists. A Rich renderable cannot report its height until rendered, so the height budgets at render.py:438-457 and 499-503 would need rendered line counts. | Recommend line-model plus spans (research 01 section 8.2 options 1 to 3, web-01 H); treat Rich `Panel` as an optional, separately approved last step. Any Rich frame under `--ascii` needs an explicit `box=rich.box.ASCII` (`safe_box` does not switch it; [CODE-CONTRADICTED] claim corrected, see 9.5). |
| 10 | G-E / Q7 / Q-6 (D-6), hard-wrap rule and 64-hex hash policy. `wrap()` cuts a token wider than the width with no marker, mid-word (render.py:77); a 64-hex token fits whole at 160, 116 and 80 today (measured), long paths split mid-word. Inside a frame the inner width is 74 (mockup 78-wide frame) or less. The 4-line cap (`DESK_TEXT_LINES = 4`, view.py:99) would replace a hash trailing a long path and file list with `...`. Whether the Decision Desk must show the hash in full is undecided. External context: Rich `Text` with `overflow="crop"` clips silently, `"ellipsis"` costs one cell and marks the cut, `"fold"` splits the token (https://rich.readthedocs.io/en/stable/text.html). | Blocks the desk-frame layout phase and the named fixture test; a person cannot verify a truncated hash. No test runs a 64-hex token, a long path or wide characters through `session_fields` (render.py:347-353). | Decide a hard-wrap rule (marker or none) and a hash-in-full policy. Add (before the layout phase) the fixture test named in research 03 5d plus a second fixture with a trailing hash after a long path and file list, and a 120-character `resource.worktreeId` case. |
| 11 | G-F, the real `LiveScreen` (commands.py:257-279) has no test; only the key reader has a pty test (`test_keys_spike.py`). [UNVERIFIED] whether `run_interactive` accepts `--fixture` under a pty; the cycle-1 live measurements used a stand-in console at height 38. | Style or frame regressions on a real terminal are not caught by the 766 passing tests; blocks the "styled output verified on the live path" requirement of #606. | Plan route B (pexpect 4.9.0, pty sized to `policy.width` and `policy.height`; pattern exists at `spike_child.py:64`) or route A with a `force_terminal` seam into `LiveScreen`; rely on the render gate for the visual check. |
| 12 | G-G, frame-heavy layout at small heights is unmeasured. No final `lines[:height]` clamp on the normal screen; one ledger row is always forced (render.py:499-502); `MIN_ROWS = 8`; on the live screen rows past `policy.height` silently drop the footer key list and `shown x/y` (no ellipsis). Only height 40 and the `five` golden were run; questions-on desk screens were run only at height 70. [UNVERIFIED] heights below 40. External context agrees: under `screen=True` Rich crops rows past the height rather than ellipsising (https://github.com/Textualize/rich/blob/v15.0.0/rich/screen.py). | Blocks the height budget of every framed pane; each added frame row is one fewer ledger row, and the base fixture at 80 wide already fills all 40 rows. | Add heights 24 and 12 to the render-gate matrix; assert `len(screen_lines(...)) <= policy.height` at 8, 24, 40 and 44; count every new frame, tile and heading row inside `top`, `body` and `footer_height`; derive frame cost from research 04 pane row counts or record it as a caveat. |
| 13 | Pane height rule. Mockup panes have fixed full-frame heights (rows 6-44, frame 48 lines at 160 and 42 at 116 and 80) with blank interior; the observer content is data-dependent; RR line 13 says C's 44-row contract; code uses `policy.height` (render.py:447). Harness height is 50 (`render_current.py:38`), which matches neither mockup height (F-04). | Blocks like-for-like render-gate comparison and the vertical budget of frames. | Set harness height per width to the mockup height (48, 42, 42) or record the mismatch as accepted; state the height rule in the plan. |
| 14 | G-H (D-11), spec self-contradiction [CODE-CONTRADICTED]: RR line 61 requires the 80-column invariant lines "Questions stay until explicit resolution." and "No reply observed is not delivery failure."; current 80-column output has neither and AD-7 rejects the first as untruthful against RR 42. | Blocks the 80-column questions screen acceptance check and the spec edit that accompanies O-1. | Reword RR 61 (or RR 42) deliberately in the same spec change as O-1. |
| 15 | Q3 reviewer rubric and PNG route (D-10 for the PNG dependency). The fixed rubric is drafted in Section 8.4 (RB-01 to RB-23, each with a measurable pass or fail anchor); what stays open is the PNG route (the raw material for the rubric was eight colour roles and pane geometry, research 04 sections 2 and 4). Whether a new dev dependency for PNG rendering is justified (Q-7): nothing in `pyproject.toml` or the Makefile supports it; PIL, cairosvg, pyte, playwright, fontTools, chromium, rsvg-convert, ImageMagick, freeze, aha are all absent (research 05 section 2). External context: Rich SVG relies on `foreignObject` and a remote `@font-face`; `rsvg-convert` and ImageMagick failed on it, so it is browser-only in practice (https://github.com/Textualize/rich/issues/2153, issue from Rich 12.1.0; whether Rich 15 changed this is [UNVERIFIED]). | Blocks Phase 0 harness design and the image-to-image reviewer score. | Text and ANSI rubric works offline now; keep Rich as the only renderer and record per-case consoles (research 05 section 5, web-02 recommendation 1 and 3). If image scoring is required: open the Rich `export_html` file in the Playwright MCP browser at the mockup viewport (session only, untested here) or approve freeze or `playwright install chromium` (network at install). Use the Section 8.4 rubric unchanged and keep the same monospace font between runs. |

### 9.3 Zellij (Q6) and environment gaps

| # | Question | Impact (what it blocks) | Suggested Resolution |
|---|---|---|---|
| 16 | Q6 go or no-go. Research 05 section 7: no-go as a Phase 0 render harness or a dependency (adds no image output, behaviour unverified, install provisioned from `/etc/skel`, CI presence unknown). Web-02 recommendation 4: GO conditional (observer stays standalone, may read `ZELLIJ` as an optional hint, Zellij optional for layout and as a second manual capture method). The two agree that Zellij must not be a dependency of the render gate; they differ only on whether to adopt it as optional presentation. | Blocks the Q6 answer in the report. | Report as: no-go as a harness or observer dependency; optional manual presentation environment after a live-session experiment. Keep the 05 recommendation provisional until row 17 closes. |
| 17 | [UNVERIFIED] Needs a live Zellij session (forbidden in this task): floating-pane behaviour, `dump-screen --ansi` fidelity (colours, wide glyphs, box drawing), command panes in a layout, truecolor and 256-colour pass-through. External context: no Zellij page found that documents colour downgrade; `dump-screen -a` and `floating_panes { pane ... x y width height }` are documented (https://zellij.dev/documentation/cli-actions.html, https://zellij.dev/documentation/creating-a-layout.html). | Blocks lifting the provisional no-go and any Zellij-based capture. | One-off background-session test on 0.44.2 (`attach --create-background`, print a gradient, `dump-screen --ansi`) before relying on any of it. |
| 18 | [UNVERIFIED] Zellij docs are ahead of the installed binary: 0.46.0 was announced 2026-11-11 (https://zellij.dev/news/terminal-inbox-session-previews); local install is 0.44.2 (verified locally and the source of truth); `--pane-id` on every action and `zellij:bars` may describe newer behaviour. `zellij action --help` was read only to line 120. | A documented flag may not exist locally. | Run `zellij action dump-screen --help` and `new-pane --help` locally before any plan step cites a flag. |
| 19 | [UNVERIFIED] Layout-file syntax to start `superclaude observe` in a pane (no installed layout uses a command pane; docs show `pane command="..."`, https://zellij.dev/documentation/layout-examples); whether an application can read the active Zellij theme at runtime; lines 179-252 of `aidev02.kdl` and 180-265 of `agent.kdl` not read. | Only blocks an optional Zellij layout deliverable. | Verify with a live session if the layout deliverable is wanted; otherwise carry as a caveat. |
| 20 | Zellij chrome (tab bar 1 row, status bar 2 rows per `default.kdl:50-56`, plus the pane frame) is never converted into usable rows and columns against 160, 116, 80 and the 44-row contract (m5). | Affects the claim that 44 rows fit in a Zellij pane. | Add the arithmetic in the plan, or record it as out of scope because Zellij chrome is outside the mockups (web-02 A3: unverified whether the mockups include it). |
| 21 | [UNVERIFIED] Whether Zellij exists in CI; whether `pip`/`uv` can install Pillow, cairosvg, pyte or a Playwright browser here (network untested); whether the cairo system library is present; whether DejaVu Sans Mono (`/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf`) covers every mockup glyph; licences of freeze, pyte, aha, cairosvg are unconfirmed (web-02; ansi2html is LGPLv3+). | Blocks approval of any new tool and the font stability of image scores. | Check the CI image at plan time; confirm licence and glyph coverage before adding a dependency. |
| 22 | The Playwright MCP browser exists only inside the Claude session, not in the repository (research 05 section 5). A PNG step that depends on it cannot run in plain CI. Both Gate 1 reviewers read mockup PNGs with Read successfully, so PNG viewing is confirmed; turning a rendered SVG or HTML into a PNG offline remains untested. | Decides whether the image tier is session-only. | Keep the image tier session-only and the text/ANSI tier in CI; test the SVG/HTML to PNG path once on a real observer render. |

### 9.4 Design-evidence gaps and unverified claims

| # | Question | Impact (what it blocks) | Suggested Resolution |
|---|---|---|---|
| 23 | M-18 / F-08: no selected marker (`▸ ► › »`) appears in any of the nine mockup `.txt` files, so how a selected row or question looks has no mockup evidence [UNVERIFIED]. | Blocks scoring M-18 against the mockups. | Score M-18 against RR line 50 (glyph `▸`, `@` in ASCII, never `>` or `*`), not the mockup; owner or rubric decides any extra emphasis. |
| 24 | [UNVERIFIED] Whether the mockup PNG background (dark navy) is part of the design: the `.ansi` files set no background (no 48 code). | Decides whether a background is painted or the terminal default is kept. | Owner or rubric decision; default to no background. |
| 25 | [UNVERIFIED] The mockup palette on light terminal backgrounds is not addressed by any file; ambiguous-width glyphs (box and block characters, 1 cell in Rich) may render at another width in the owner's terminals (web-01: `cell_len` has no East-Asian-ambiguous rule, https://github.com/Textualize/rich/blob/v15.0.0/rich/cells.py). | Possible border misalignment or low contrast outside the tested setup. | Carry as a caveat; keep chrome to box drawing, plain ASCII and a short vetted symbol set; no emoji. |
| 26 | [UNVERIFIED] Content of plan-approval asks (path, file list, 64-char hash) and that they are stored as `question` rows (`pr-591-comment.md` lines 26-31, unverified in the source itself). Also [CODE-CONTRADICTED] premise of consideration 8: the 80-column Decision Desk "frame" does not exist yet (no border, render.py:329-356). | The Q7 fixture may not match a real plan ask. | Confirm with the plan-ask source before building the fixture; the premise becomes true when frames land. |
| 27 | [UNVERIFIED] Which of the three `+1` terms in `spare` (render.py:454-456) is which; read from the comment at 444-445 only. | Needed to add frame rows to the budget correctly. | Confirm when planning the height budget. |
| 28 | [UNVERIFIED] How the view fixtures `injection` and `long-identifiers` interact with styling; real `superclaude observe --questions` and `--run` screens were not measured (live source needed); `w-` ids in fixtures are 5 cells, so M-17's blank band is seen only with short ids. | Styling regressions on hostile or long data stay unseen. | Check when styling lands; carry as a caveat. |
| 29 | [UNVERIFIED] The "153 cells" full-ledger figure (FINDINGS M-06, attributed to RR line 30): not on line 30 and not reproducible; code gives exactly 160 (`_columns` 2 + 114 + 12 + 10 + 22, `FULL_WIDTH`, terminal.py:23). The conclusion (a three-column grid would not hold the full ledger) stands either way. A frame at 160 needs the elastic `flags` column to give up 2 to 4 cells. | A wrong figure could mislead the width budget. | Do not state "153 cells" as fact; use 160. |
| 30 | [UNVERIFIED] Slack figure: 01 section 8.2 item 5 computes 114+1+42 = 157 of 160 (1-cell gap); 04 mockup measurement gives 1+114+2+42+1 = 160 (1-cell margin each side, 2-cell gap). | Width arithmetic for the two-column layout. | Use 04's measured numbers (stronger evidence: measured on the mockup files). |
| 31 | Literal-by-literal break list is incomplete (F-06): `test_view.py` (60 tests, 1383 lines) and ten modules (test_keys_spike, test_adapter, test_parse, test_collector, test_session, test_questions, test_sanitize, test_cancel, test_deep_nesting, test_registration) were classified from names and docstrings. | The P2 text-phase test-change list is not exhaustive. | Enumerate at plan time; not needed for the options decision. |
| 32 | [UNVERIFIED] Exact `PYTHONPATH` layout for regenerating `golden_release1_surface.json` from release 1 source (`git archive 9e2608b03 src/superclaude` extracts `src/superclaude/...`, so `<tree>/src` is probably needed). No recorder exists for `golden_questions_linkoff.json`; the `record_golden*.py` scripts generate neither presentation golden. The derived one-liners are not an owner-approved procedure. | Blocks a safe re-baseline procedure (row 5). | Verify the layout when re-baselining; add a recorder or document the one-liner with the decision. |
| 33 | In-process Rich quirk: a `Style` caches its ANSI codes on the first colour system used, so test helpers that build consoles with different colour systems in one process can see stale codes (observed in research 01 section 7). | Flaky or misleading depth tests for row 6. | Run each depth probe in a fresh process or use fresh `Style` objects. |
| 34 | Phase 0 harness capture: `render_current.py` captures with `export_text(styles=True)` (ignores NO_COLOR and the standard downgrade) and has no `if __name__` guard (calls `main()` at import). Research 01 lines 55 and 231 and research 05 section 5 stated the `styles=True` route without that caveat. | A harness built unchanged would show truecolor that a 16-colour terminal never shows. | Capture `console.file.getvalue()` through `make_console`; add the guard when the file is next edited. |
| 35 | [UNVERIFIED] Help-string line numbers `view.py:79` and `:105` came from a grep and were not read in context; the `commands.py:63-66` comment cites an owner record file that was not opened (its existence is checked by `test_commands.py:752-755`). | Wrong citations in the plan. | Re-read at plan time. |
| 36 | Windows (`legacy_windows`) is left to Rich; `run_interactive` refuses win32 (commands.py:353-355) but `--once --width` is cross-platform and `_emit` encodes with `errors="replace"`. | Box and ASCII behaviour on legacy Windows is not designed. | Carry as a note. |
| 37 | [UNVERIFIED] Web-01 items to confirm locally: that `box.HEAVY` exists in Rich 15.0.0 (`dir(rich.box)`; `box.ASCII` is already used in a local probe); Rich docs cited are 14.1.0 for the export methods while local is 15.0.0; the matching metric for the truecolor to standard downgrade; that `export_html`/`export_svg` record the downgraded styles when the recording console has a forced colour system (inference, untested). | Possible API or behaviour surprise in the harness. | Confirm with one-line probes in the installed Rich 15.0.0 before the plan relies on them. |

### 9.5 Stale or corrected documentation (pending document fixes and corrected claims)

| # | Question | Impact (what it blocks) | Suggested Resolution |
|---|---|---|---|
| 38 | Stale spec text in `rendering-rules.md` (STALE DOC): lines 37-41 and 60-61 describe the 160/116/80 columns, the SEEN tile and RETAIN CONTEXT as the layout while line 43 says one stacked block was built; line 33 omits the `flags` column at 116 and 80 (render.py:197-212, 216-229); line 38 and the mockups still title `OPEN HUMAN QUESTIONS` (code `COORDINATOR QUESTIONS`, view.py:53); line 59 admits `observed open: n` wording is superseded; line 20 says `FROZEN unavailable (no source)` [CODE-CONTRADICTED] where code prints `POLICY FROZEN unavailable (no source)` (view.py:948). Lines 41 and 43 become stale if O-1 and M-14 are adopted. | Readers may build from design reference as if it were current behaviour. | Treat these as design reference; fix wording in the O-1 spec change; do not copy pane titles from the mockups for this one. |
| 39 | Stale review notes: `.dev/issues/409/ponytail-review-20261116/tests-and-fixtures.md:51` names commit c69ce4b3a (git log prints only cd8736199 #514); `.dev/reviews/orchestrator-tui-alignment-20261113/05-observe-built-state.md:27` says `QUESTION_GATE_PASSED = False` (code is True, commands.py:67, and `QUESTION_LINK_PASSED = True` at :70, since #592); `design-docs-and-gates.md:46` cites `test_commands.py:741-750` (now :747-760). | Wrong gate state or line cites in later documents. | Cite current code; none of these block the work. |
| 40 | `render_current.py` docstring (lines 6-9) says the `ansi-*.txt` files are "empty of escapes today" (true now, 0 ESC bytes confirmed in the nine files; false once styling lands). Related: `research-notes.md` line 24 says three width classes (code has four: full, line, short, narrow, terminal.py:63-70) and line 95 says O-1 is "recorded in the findings" while FINDINGS and 04 treat it as pending. | Misleads a reader about the baseline and the O-1 status. | Treat `current/` as the pre-fix baseline; use four width classes; treat O-1 as open (row 1). |
| 41 | Zellij provisioning headers cite phase-tasklist task IDs and a CI gate "deferred to CI"; `config.kdl` lines 30-31 and 47-48 cite upstream `default.kdl:511` and `:236-238` of Zellij v0.44.2 (upstream file not read) [UNVERIFIED]. | None for this repo (machine provisioning project). | No action. |

Corrected claims (resolved; recorded so a reader does not reuse the wrong version). These are CODE-CONTRADICTED claims whose correct form the code shows; they are not open.

| # | Claim in a document or draft | What the code shows | Where corrected |
|---|---|---|---|
| C1 | `safe_box=policy.ascii` gives Rich boxes an ASCII fallback (03 rule 3, 04 G-1 row, assumed in 01) | A Rich `Panel` prints identical Unicode borders with `safe_box` True or False (Rich 15.0.0 probe); ASCII needs an explicit `box=rich.box.ASCII`; `test_terminal.py:109, :115` pin only the attribute value | Fixed in cycle 1 (gaps log R-1) |
| C2 | Live path described from reading only (02 sections 2 and 3) | 7-hop trace measured: alternate-screen codes, width padding, silent crop at console height with no ellipsis, nothing written for a non-terminal console | 02 section 9 added in cycle 1 (gaps log R-2) |
| C3 | Three width classes full/line/narrow | Four: full, line, short, narrow | 01 corrected; row 40 |
| C4 | M-10 says `render()` prints the header only for the full class | Condition is in `screen_lines` render.py:497; `render()` is at 524-531; behaviour confirmed | Cite render.py:497 |
| C5 | 03 says the 80-column desk line is "exactly the width" (MINOR-1); a 140-character path splits in three (MINOR-2); gate-test lines 747-760 and 762-777 (F-09); `test_terminal.py:114-116` | 78 cells; 139 characters give two pieces `[80, 59]`, three need about 165; functions end at 756 and 772; cite 109 and 115 | Use the code figures |
| C6 | 04 says RR is 108 lines (MINOR-3); `ESC[0;1;` count 2 to 15 (MINOR-4); M-05 cites render.py:374 (m1) | 107 lines; 3 to 16 occurrences (160 signal-bridge 16, 80 attention-ledger 3); the line is 373 | Use the code figures |
| C7 | Grep hit counts in 03 section 2 (MINOR-6a); `research-notes.md` agent-type wording; 02 hop 4 cites `rich/live.py:127-128` | test_render 65, conftest 2, test_fixtures 2, test_export 3; about lines 125-130 | Cosmetic |
| C8 | 01 infers slate and muted collapse to greys (F-01) | Measured table in row 6 | Use 04 table |

### 9.6 Key findings carried elsewhere (excluded here with rationale)

Findings from the summaries and key takeaways of the assigned files that are answers, not open questions, are carried by the other synthesis sections and are excluded from the tables above on purpose: the string-pipeline architecture and function-level change map (01 sections 3, 4 and 8, answers Q1, owned by the problem and implementation sections); the live path and gate-constant regex pins (02 sections 4 and 9); the record and snapshot never writing question text (02 section 5; the screen-only constraint holds, with the note that stdout of `--once --width` carries question text); the phase split P0 to P5 (03 section 6, Q2); the fixture and 64-hex measurements (03 section 5, 01 section 4.9); the 8-role palette and pane geometry (04 sections 2 and 4); the offline tool inventory (05 section 2); external recommendations on Rich composition, Zellij and capture tools (web-01 and web-02, marked external context above). Open items they raised are in rows 1 to 41.

## 10. Evidence Trail

All paths are absolute. Base: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/`.

### Codebase Research

| File | Topic | Agent Type |
|---|---|---|
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/01-render-view-terminal-pipeline.md` | render.py, view.py, terminal.py and sanitize.py: string pipeline, console and colour depth, per-finding change map, 64-hex probe, height budget | Code Tracer |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/02-live-screen-commands-export.md` | commands.py, export.py, collector.py, keys.py: live screen path (section 9 trace), one-shot export, gate constants, screen-only question text | Code Tracer |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/03-tests-goldens-fixtures.md` | tests/observe: assertions at risk, goldens and regeneration, 64-hex fixture proposal, phase split P0 to P5, baseline 766 passed | Code Tracer |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/04-spec-mockups-and-findings.md` | rendering-rules.md, FINDINGS M-01 to M-18, mockup colour decode and pane geometry, 16-colour mapping, render_current.py | Doc Analyst |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/05-zellij-and-render-harness-environment.md` | Installed Zellij 0.44.2, offline render tools, pyproject and Makefile, harness options, Q6 evidence | Integration Mapper |

Supporting file (not an assigned research input): `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/research-notes.md`. This synthesis did not read it; the agent types above come from the task prompt. Its two stale lines (width classes, O-1 status) are logged in the gaps log and in row 40.

### Web Research

External context only; source URLs are inside each file.

| File | Topic |
|---|---|
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/web-01-rich-composition-and-colour.md` | Rich 15.0.0 composition (Panel, Table, Columns, Layout, box), `color_system` detection, NO_COLOR and FORCE_COLOR, export_text/html/svg, Live `screen=True`, `cell_len`, Text overflow, 16-colour downgrade |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/research/web-02-zellij-and-terminal-capture.md` | Zellij 0.44 layouts, floating panes, dump-screen, themes, detection; offline terminal-to-image tools (Rich SVG/HTML, Playwright, freeze, pyte, aha, cairosvg) |

### Gaps Log

| File | Topic |
|---|---|
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/gaps-and-questions.md` | Unified, deduplicated gaps: Section A (2 resolved blocking findings), Section B (58 open gap rows: 8 Important, 50 Minor), Section C (39 tagged-claim and stale-doc rows), Section D (7 open questions incl. O-1 and OPEN-1 to OPEN-3) |

### Synthesis Files

Directory: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/`

| File | Report content |
|---|---|
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/synth-01-problem-current-state.md` | Problem statement and current state |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/synth-02-target-gaps.md` | Target and gaps |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/synth-03-external-findings.md` | External findings |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/synth-04-options-recommendation.md` | Options and recommendation |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/synth-05-implementation-plan.md` | Implementation plan |
| `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/synth-06-questions-evidence.md` | Open Questions (section 9) and Evidence Trail (section 10); this file |

### QA Reports

The Gate 1 and task-validation QA reports are in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/qa/`. The Gate 1 reports behind the gaps log are `analyst-completeness-report.md`, `qa-research-evidence-report.md`, `qa-research-qualitative-report.md`, `qa-consolidated-findings-phase3.md`, `qa-fix-log-phase3.md`, `qa-fix-verification-phase3.md` and `qa-fix-verification-qualitative-phase3.md`; later QA reports for the synthesis and the assembled report will be added there.
