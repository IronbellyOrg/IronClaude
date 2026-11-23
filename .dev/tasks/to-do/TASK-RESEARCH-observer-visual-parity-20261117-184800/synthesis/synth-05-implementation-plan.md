## 8. Implementation Plan

This is a plan for a later implementation of the observer redesign (issue #606); nothing here is an instruction to implement now. The phase scheme P0 to P7 in this Section 8 is the authoritative one for the whole report; the phase labels in Sections 3.8 and 7 mirror it and, where a wording differs, this Section 8 governs. All paths are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`. `OBS` means `src/superclaude/cli/observe/`; `T` means `tests/observe/`; `VP` means `.dev/issues/409/visual-parity/`; `RR` means `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`. Every plan step rests on a source-code read or probe recorded in research files 01, 02, 03 and 05. Mockup and spec facts (04, RR, FINDINGS) are used only as the design target, never as a statement of current architecture. Items that are `[UNVERIFIED]` appear in 8.8 and are not asserted as fact in any step.

### 8.1 Planning decisions (answers to Q1 to Q7 that every phase relies on)

| Q | Decision used by this plan | Evidence | Status |
|---|---|---|---|
| Q1 composition | Keep the line model. Introduce a `Line` (plain string plus role spans) layer in `OBS/render.py`; `screen_lines()` becomes `[l.plain for l in _compose(...)]` so every plain-string test and golden keeps its meaning. Frames and two columns are hand-built from `Line` objects using new `GLYPHS` entries. `render()` still returns one `Text` per line. No Rich `Panel`, `Table`, `Layout` or `Columns` in `render()`. | `render()` is one `Text(no_wrap=True, overflow="crop")` per string (render.py:524-531); `T/test_render.py:399` pins `len(group.renderables) == len(screen_lines(...))`; `wrap`/`clip` own the `>` and `...` markers; height budgets count `list[str]` lengths (render.py:438-457, 499-503); `safe_box` does not ASCII-ize a Panel (probe, Rich 15.0.0). [CODE-VERIFIED] | Decided |
| Q2 phases | Seven phases, ordered by golden impact: P0 tests and harness only; P1 style only; P2 text and budget fixes; P3 single-column frames; P4 and P5 two-column layouts (need O-1); P6 ledger frames; P7 spec reconciliation and final gate. | 03 section 6 (P0 to P5 grouping), with P2 and P6 added for the findings it does not cover. | Decided |
| Q3 harness | Standalone script `VP/tools/render_compare.py` built on `render_current.py`; no new dependency. Text and ANSI tier is machine-checked; PNG tier is made in the Claude session by opening Rich `export_html` output in the Playwright MCP browser; a fresh reviewer subagent scores a fixed rubric (8.3) against the mockup PNGs. | 05 sections 2, 4, 5, 6; web-02 B1, B2, B7 (external context). PNG route is untested. | Decided; PNG route [UNVERIFIED] until step 0.4 |
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
| D-7 | Mapping from real state words to colour roles (M-09) | Only values whose meaning the code or spec states are coloured; all others use the body role; the state word is always printed | Owner supplies the table; step 1.4 table is replaced |

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
| RB-01 | The eight mockup roles are used: amber for attention content, ages and the selected question; cyan for titles, counts and identity; slate for secondary borders and rules; base for body text; muted for secondary text and absent values (palette in 04 section 2) | High | M-01 | Reviewer, truecolor PNG | P1 |
| RB-02 | Every pane the mockup frames has a titled border with the title inset in the top border: heavy amber for the attention pane, rounded slate for secondary panes, cyan for the count tile | High | M-02 | Reviewer | P3 (questions, desk), P6 (ledger) |
| RB-03 | Column structure matches 8.3 at each width (two columns at 160 and 116, stacked at 80) | High | M-03, M-04 | Reviewer | P4 (questions), P5 (desk) |
| RB-04 | Count tile: a visually dominant figure in a cyan frame; the plain pass still contains `seen, not resolved: N | closed by evidence: unavailable (no source)` | High | M-05 | Reviewer plus script | P4 |
| RB-05 | Required literals intact and uncut: gap notice, counts tokens without a mid-token cut, `PARTIAL (...)` text, the disclosure, `reason unknown`, desk title, retention line, `nextAction.kind` verbatim | High | guards RR 20, 31, 32, 47, 49 | Script (substring list) | every phase |
| RB-06 | NO_COLOR pass: zero ESC bytes; text equals the coloured pass after SGR removal; hierarchy is carried by text and glyphs | High | G-1 | Script | every phase |
| RB-07 | ASCII pass: output is pure ASCII; borders are `+ - |`; no `?` where a border should be | High | G-1 | Script | P3, and every phase for the ASCII text part |
| RB-08 | Fit: every line at most the width in cells; rows at most the height; the footer keys are the last lines; no SGR 5 or 6 (blink); no mouse sequences | High | AD-5, standing constraints | Script | every phase |
| RB-09 | 16-colour pass: the eight roles map to eight distinct ANSI colours (no two roles share an index) | High | G-2 | Script (theme table test plus SGR read) | P1 |
| RB-10 | State words are coloured by the D-7 table and never by colour alone; at 16 colours green, red and violet states are distinguishable | Medium | M-09 | Reviewer | P1 |
| RB-11 | Absent values (`unknown`, `unavailable (no source)`, `reason unknown`) are muted; plain under NO_COLOR | Medium | M-08 | Reviewer | P1 |
| RB-12 | A column heading and rule appear at 116 and 80 whenever rows are visible | Medium | M-10 | Reviewer plus script | P2 |
| RB-13 | The 80-column key list is not cut and no key pair is split across lines | Medium | M-11 | Script | P2 |
| RB-14 | Desk: the question text leads and is emphasised; `label: value` evidence is aligned; long values wrap on their own line | Medium | M-12 | Reviewer | P5 |
| RB-15 | Title bar: the left title and a right `READ ONLY` badge (OPEN-3, gating until ruled) | Medium | M-13 | Reviewer | P2 |
| RB-16 | Question list hierarchy: rows lead; caveat lines carry less weight than rows (OPEN-1, gating until ruled) | Medium | M-07 | Reviewer | P4 |
| RB-17 | Run scope, caveat and retention facts are grouped in one RETAIN CONTEXT pane at 160 and 116 (OPEN-2, gating until ruled) | Medium | M-14 | Reviewer | P4 |
| RB-18 | Ledger screen: observation and attention content is in titled panes, with no invented owner, requester, mapped-tree or SIGNALS content (AD-1 to AD-4) | Medium | M-06 | Reviewer | P6 |
| RB-19 | Q7: for the `PLAN_ASK` fixture (hash inside the first four wrapped lines) the 64-hex hash is whole on one line in the 80-column desk, nothing is lost, no line exceeds 80 cells; the trailing-hash fixture still ends its fourth line with `...` (D-6) | Medium | Q7 | Script | P3 |
| RB-20 | A rule line precedes the footer and the key pair `n/p question` is intact | Low | M-15 | Script | P2 |
| RB-21 | The 80-column counts strip is not cut inside a token | Low | M-16 | Script | P2 |
| RB-22 | No wide blank band after the id column at 116 and 80 | Low | M-17 | Reviewer | P2 |
| RB-23 | The selected question has a role style in addition to the glyph | Low | M-18 | Reviewer | P1 |

A phase closes only when every High and Medium row that is in scope for it passes; Low rows are recorded and may be deferred with a log line. A reviewer scores only the rows in scope for the phase, and marks later rows `N/A (scheduled P<n>)`.

### 8.5 Render gate protocol (the last step of every phase, written once)

| Step | Action | Details |
|---|---|---|
| G1 | Implement | Phase steps are done; `uv run pytest tests/observe/ -v` is green (baseline 766 passed in 25.70 s on 2026-11-17, plus tests added by earlier phases). |
| G2 | Render | `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <out>/<phase>/iter-<n>` renders widths 160, 116 and 80 for screens `ledger`, `questions`, `desk` and `desk-planask`, in four passes: truecolor, 16-colour, NO_COLOR and ASCII, plus the text-only height matrix. It writes `checks.json` with the script-checked rows (RB-05 to RB-09, RB-13, RB-19 to RB-21). |
| G3 | Rasterise | In the Claude session, open each truecolor and 16-colour `.html` through the Playwright MCP browser at a fixed viewport and save `.png` next to it (route proven in step 0.4). If 0.4 fails, the text and ANSI tier is used and the reviewer compares `.txt`/`.ansi` files with the mockup `.txt`/`.ansi` files, with the mockup PNG as the visual reference. |
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

**Dependencies:** none. Baseline run: `uv run pytest tests/observe/ -q` gives 766 passed.

**Closes:** no finding. It prepares the gate for all of M-01 to M-18.

| Step | Action | Files | Details |
|---|---|---|---|
| 0.1 | Make `render_current.py` importable | `VP/inputs/tools/render_current.py` | Line 93 calls `main()` at import time with no guard. Wrap it in `if __name__ == "__main__":`. Outputs of a direct run stay identical. |
| 0.2 | Add the harness | `VP/tools/render_compare.py` (new) | Loads `render_current.py` by path (`importlib.util.spec_from_file_location`) to reuse its view builders (`questions_result`, `QUESTIONS`, the three views). Interface: `render_case(view, width: int, height: int, *, env: dict, ascii: bool) -> CaseOutput` where `CaseOutput` holds `plain` (`screen_lines`), `stream` (the string written by `make_console(policy, file=io.StringIO(), record=True)` printing `render(view, policy)`, read with `console.file.getvalue()`), and `html` (`console.export_html(inline_styles=True)`). Policy comes from `resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)`. It must not use `export_text(styles=True)`. |
| 0.3 | Define the output set | `VP/tools/render_compare.py` | For widths 160, 116, 80 and screens `ledger`, `questions`, `desk`, `desk-planask` (Q7 fixture, built in 0.6): write `<out>/<width>/<screen>.txt` (plain), `.ansi` (stream), `.nocolor.txt` (env `{"NO_COLOR": "1"}`), `.ascii.txt` (`ascii=True`), `.html`, and, per width, `manifest.json` with line counts and cell widths. Heights: 48 at 160 and 42 at 116 and 80 (mockup frame heights, 04 section 4; `render_current.py:38` uses 50, which is not like for like); `--heights 44,40,24,12,8` adds a text-only matrix. Flag `--check` writes `checks.json` (RB-05 to RB-09, RB-13, RB-19 to RB-21): width fit by `rich.cells.cell_len`, no ESC in the NO_COLOR file, `isascii()` on the ASCII file, SGR 5 and 6 absent, required literal list present, `strip_sgr(stream) == plain + newlines`. |
| 0.4 | Prove the PNG route once | `VP/png-route.md` (new) | In the Claude session, open one `.html` via `mcp__plugin_playwright_playwright__browser_navigate` (`file://`), set the page to `font-family: "DejaVu Sans Mono"` and a width of `<cols>ch`, take a screenshot with `browser_take_screenshot`, and Read the PNG back. Record viewport, font and result. [UNVERIFIED until run; DejaVu Sans Mono is the only mono font confirmed installed, and its coverage of the mockup glyphs is untested.] If it fails, record that the text and ANSI tier is the gate and that a PNG tool (freeze or Playwright) needs a separate owner approval; no dependency is added by this plan. |
| 0.5 | Write the rubric and reviewer prompt | `VP/rubric/rubric.md`, `VP/rubric/reviewer-prompt.md` (new) | `rubric.md` is the 8.4 table verbatim plus the palette from 04 section 2 and the geometry from 8.3. The reviewer prompt names the inputs (mockup `.png`/`.txt`/`.ansi` for the width, rendered `.png`/`.txt`/`.ansi`, `checks.json`), the pairing ledger to signal-bridge, questions to attention-ledger, desk to decision-desk, the PASS or FAIL JSON shape, and forbids edits. The screen pairing and the mockup titles that the spec retires (`OPEN HUMAN QUESTIONS`) are noted so the reviewer does not score the title text. |
| 0.6 | Add the Q7 fixture and tests | `T/test_render.py` (R3 block, after line 958) | New `PLAN_ASK` constant: a synthetic ask with a plan path, two file paths and `"0123456789abcdef" * 4`, under `ASK_CAP = 400` characters (parse.py:475) and under four desk lines at 80 columns. Test `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk(width)` over `WIDTHS`: built with `r3_rows([("w-001", PLAN_ASK)])` and `r3_screen(fake_clock, rows, 0, width, height=70)`; asserts every line `cell_len <= width`; the hash is whole on one desk line; the ask with spaces removed equals the desk text with spaces removed when not cut. Second test with a hash after a long path and file list that fills the four-line cap, pinning today's `...` cut: the hash is not shown, and this is the one stated exception to "the hash is whole" (rule D-6). The first test's fixture keeps the hash inside the first four lines. Third test: a worker with a 120-character `resource.worktreeId` (pattern from `T/test_view.py` `r3_workers(worktree=...)`) pins the 2-cell continuation indent at render.py:347-353. Canary: `HASH not in record_text(view)` and `HASH not in snapshot_json(view)`. |
| 0.7 | Add helpers and a height test | `T/conftest.py`, `T/test_height_budget.py` (new) | `strip_sgr(text) -> str` using `re.sub(r"\x1b\[[0-9;]*m", "", text)` and `sgr_params(text) -> set[str]`, with a self-test. `test_questions_on_screen_fits_the_height(width, height)` for heights 24, 40, 44. Run it first: if a height fails on today's code, record the failing heights in `VP/scores/baseline.md` and pin only the passing set (the forced single ledger row at render.py:502 can overflow; 02 section 9.4). |
| 0.8 | Baseline score | `VP/scores/baseline.json` (new) | Run the harness at the current commit, rasterise per 0.4, spawn one fresh reviewer per width (8.5 G4), store the scores. Expected: RB-01 to RB-04 and RB-10 to RB-18 FAIL; script rows pass. A baseline that passes any High rubric row is a sign the rubric is not discriminating; revise `rubric.md` once, then freeze. |

**Tests and goldens that change:** none change; tests are added. Golden files and `printed_*` bytes are untouched.

**Byte-identical in this phase:** everything under `src/`; `record_text`; `snapshot_json`; both goldens.

**Rubric rows scored (baseline only):** all, as a baseline; no pass is required.

**Migration or rollback:** delete the new files; no source depends on them. If 0.7 shows an existing overflow, it is a finding for P3, not a P0 fix.

**Render gate:** the baseline run in step 0.8 replaces the gate for this phase; the phase closes when `uv run pytest tests/observe/ -v` is green with the new tests and the baseline file exists.

### Phase 1: Colour depth, theme, role spans and the styled-capture gates (style only, no text change)

**Goal:** add colour and weight to every existing screen without changing one plain character; fix colour depth (Q4, G-2); make styled output capturable and tested on the one-shot path and the live path (Q5).

**Dependencies:** Phase 0 (harness, helpers `strip_sgr`, rubric, baseline). Owner decisions D-4, D-5, D-7 (defaults in 8.2 apply if not ruled).

**Closes:** M-01 (colour and weight on the current screens; frame and tile colours follow in P3 and P4), M-08, M-18; M-09 on the ledger rows (desk fields complete it in P5); guard G-2.

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Resolve the colour system in the policy | `OBS/terminal.py` (`TerminalPolicy` 37-51, `resolve_policy` 73-92, `make_console` 110-125) | Add field `color_system: str \| None = "standard"` last in the frozen dataclass so existing constructions keep working. In `resolve_policy`: `None` when `no_color`; `None` when `env.get("TERM")` is `dumb` or `unknown`; `"truecolor"` when `env.get("COLORTERM", "").lower()` is `truecolor` or `24bit`; `"256"` when `env.get("TERM", "")` ends with `256color`; otherwise `"standard"`. In `make_console` replace line 121 with `color_system=policy.color_system`; keep `no_color=policy.no_color`. NO_COLOR therefore still gives `color_system=None` and drops bold as well as colour (project behaviour, 01 section 7). `NO_COLOR` literal stays only in terminal.py (source scan `T/test_terminal.py:181-198`). Tests call `resolve_policy({}, ...)` with an empty env, so they stay at `"standard"`. |
| 1.2 | Add the theme module | `OBS/theme.py` (new) | `ROLES: tuple[str, ...]` (semantic roles: `title`, `attention`, `attention_title`, `identity`, `secondary`, `body`, `body_bold`, `muted`, `selected`, `border_attention`, `border_secondary`, `border_count`, `state_running`, `state_settled`, `state_failed`, `state_frozen`); `style_for(role: str, depth: str) -> rich.style.Style \| None` (returns `None` for depth `None`); one table per depth. Truecolor RGB from the mockups: base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242 (04 section 2). 256-colour indexes: base 189, slate 60, cyan 80, muted 145, amber 214, green 115, red 210, violet 147. 16-colour table with named colours: base `bright_white`, muted `white`, slate `bright_black`, cyan `bright_cyan`, amber `bright_yellow`, green `green`, red `red`, violet `magenta`. No role sets blink, dim or reverse. `Style` objects are cached per `(role, depth)` so an earlier depth in the same process cannot leave stale codes on a later one (Rich caches ANSI codes on a Style, 01 section 7). The file must not contain the literals `Console(`, `NO_COLOR`, `COLUMNS`, `stdout.encoding` or `getpreferredencoding` (also not in comments). |
| 1.3 | Add the `Line` layer | `OBS/render.py` (imports 12-14, `render` 524-531, `screen_lines` 390-521) | New frozen `Span(start: int, end: int, role: str)` (character offsets) and `Line(plain: str, spans: tuple[Span, ...] = ())` with construction helpers `seg(text, role=None) -> Line` and `join(*parts: Line) -> Line` that build in order, so offsets never come from cell widths (wide characters are 2 cells but 1 character, 01 section 8.2). `Line.clipped(width, policy) -> Line` calls `clip()` on `plain` and trims spans to the new length; `ascii_safe` replaces one character with one `?`, so offsets stay valid. `_roled(strings: list[str], role: str) -> list[Line]` wraps existing `wrap(...)` output with one whole-line role. Rename the body of `screen_lines` to `_compose(view, policy, message=None) -> list[Line]` and define `screen_lines(...) = [l.plain for l in _compose(...)]`, so the public signature and every string result are unchanged. `render()` builds `Text(l.plain, no_wrap=True, overflow="crop")` per line and calls `text.stylize(style, span.start, span.end)` only when `policy.color_system` is not `None`. Keep render.py free of `Console(`, `from_markup`, `sorted(`, `.sort(` and of `observe.adapter\|collector\|parse` (`T/test_render.py:400-404`). |
| 1.4 | Assign roles at the builders (no text edits) | `OBS/render.py` (`counts_lines` 94-135, `_row_line` 233-243, `_header_lines` 246-249, `_inspector_lines` 255-287, `_question_line` 311-326, `_desk_lines` 329-356, `_panel_lines` 359-387, footer 514-521) | `header1` `title`; `header2`, `changes_line`, `gap_notice`, `_notes`, `ledger_empty` text and the footer `muted` (the mockups draw the clock and freshness line and the keys hint in muted, 04 section 2); counts tokens: protected tokens `identity`, and the suffix span of a token ending in `UNAVAILABLE` (view.py:100) `muted`; panel title `attention_title`; run, state, disclosure, caveat and retention lines `muted`; `counts_line` `identity`; ledger title `secondary` bold; the question line is built as segments: age `attention` bold, subject `body_bold`, `QUESTIONS_REASON` tail `muted`, and the selected question marker and line `selected` (M-18; the glyph stays `glyph("selected")`, RR line 50); `DESK_TITLE` `attention_title`, desk question text `attention`, field labels `muted`, values `body`. `_row_line` is rebuilt as `_row_segments(row, columns, policy) -> Line`: it appends each `_cell(...)` in order and tags cells; the `nextAction.kind` cell stays `body` (RR line 31, never classified); a cell whose stripped text equals the bare `unknown` is `muted` (a real value `"unknown"` is quoted by `text_of`, view.py:377-385, so the bare word means absent); `workerState`, `dispatchStatus` (full layout only, `_columns` 166-191) and the liveness verdict (`_verdict`, all layouts) take the D-7 mapping `STATE_ROLE: dict[str, str]` in theme.py; a flags cell containing `FROZEN_MARKER` (view.py:106) is `state_frozen`. Before filling `STATE_ROLE`, read `RowView` construction (view.py:481-518) and the closed value sets in parse.py; values with no stated meaning stay `body`, and the state word is always printed. No regex runs over worker-controlled text; roles are attached where the builder already knows the field. |
| 1.5 | Make the one-shot path styled-capable | `OBS/commands.py` (`run_once` 225-247, `LiveScreen` 257-279) | Add `_screen_text(view, policy, *, styled: bool) -> str` that builds `make_console(policy, file=io.StringIO(), record=True)`, prints `render(view, policy)` and returns `console.file.getvalue()` when `styled`, else `console.export_text()`. `run_once` sets `styled = (policy.color_system is not None) and stdout_is_tty`, taking stdout from the same dependency object that `_emit` (200-210) uses. Default per D-4: a piped `--once --width` stays plain. Add `policy.color_system` to the `LiveScreen` shape tuple at line 265, so a depth change rebuilds the `Live`. Do not touch lines 67 and 70 (`QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED`) and keep the words `release-gates.md` and `Task 18` in the file (`T/test_commands.py:747-772` read the source text). |
| 1.6 | Update tests and goldens | `T/test_render.py`, `T/release1_surface.py`, `T/test_terminal.py`, `T/test_theme.py` (new), `T/test_styled_capture.py` (new), `T/live_child.py` (new), `T/test_live_screen_pty.py` (new), `T/conftest.py` | (a) `test_rendering_twice_is_byte_identical_and_no_color_changes_no_text` (test_render.py:250-259): keep determinism and the `screen_lines` equality (:257); replace :256 with `strip_sgr(colour) == nocolor`, and assert that the colour print contains ESC at 160 for the base variant and that the NO_COLOR print contains none. (b) Audit every `printed(` call (:76, :161, :181, :255-256, :277, :605, :977, :987): any that applies `cell_len` or `bad_chars` to colour output first applies `strip_sgr`. (c) `T/release1_surface.py` (`_printed`, lines 34-38, which builds `printed_*` through `make_console` and `render()` and therefore gains SGR bytes once P1 styles `render()`, since an explicit `color_system` makes Rich write SGR even to a `StringIO`): make `_printed` return `strip_sgr(buffer.getvalue())`, importing `strip_sgr` from `tests.observe.conftest` as the module already imports `FakeClock` from there, and add a docstring line that `printed_*` holds the printed text with SGR removed (release 1 wrote none, so the strip changes nothing there). Every `printed_*` value in `surface()` is then plain text, equal to the plain golden bytes, so `test_t47_...` (:611-624) is not edited, no side of the comparison is stripped asymmetrically in any phase, and the golden file bytes do not change in P1. Styled bytes are never stored in a golden; they are pinned by (a), (f) and (g). (d) `test_terminal.py`: depth cases (NO_COLOR, TERM=dumb, COLORTERM truecolor, TERM xterm-256color, none) and `make_console(...).color_system` for each; the literal-options test at :105-116 still passes. (e) `test_theme.py`: every role exists at every depth; the eight palette roles are distinct at `"standard"` (RB-09); no style has blink; `style_for` returns distinct objects per depth. (f) `test_styled_capture.py`: `_screen_text(styled=True)` at 160, 116, 80 contains SGR and `strip_sgr(...)` equals the `export_text()` text; NO_COLOR gives zero ESC; ASCII stays ASCII; the one-shot CLI path with a non-tty stdout still satisfies `T/test_commands.py:121`. (g) Live gate: `live_child.py` builds the fixture view, calls the real `LiveScreen` (constructor and `draw` signature to be read at commands.py:257-279 when implementing) under `pexpect.spawn` with a fixed pty size (pattern at `T/spike_child.py:64`; `pexpect` is a declared dependency, pyproject.toml:41). `test_live_screen_pty.py` asserts the stream contains `\x1b[?1049h`, SGR bytes with `38;2` when `COLORTERM=truecolor`, only 16-colour codes otherwise, no SGR under `NO_COLOR=1`, no SGR 5 or 6, and no mouse mode sequences (`\x1b[?1000h`, `?1002h`, `?1003h`, `?1006h`). If Rich emits a bare reset under `NO_COLOR`, adjust the assertion with the measured bytes and note it. |
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

**Dependencies:** Phase 2 (re-baselined goldens), Phase 1 (roles `border_*`). Questions-off screens are not framed in this phase, so `golden_release1_surface.json` does not change here.

**Closes:** M-02 for the questions list and the desk (the ledger frame closes it in P6); Q7 fixture re-pinned (RB-19).

| Step | Action | Files | Details |
|---|---|---|---|
| 3.1 | Box glyphs with ASCII forms | `OBS/terminal.py` (`GLYPHS` 30-34) | Add, in the same unicode-and-ASCII pair shape as the existing `selected`, `truncate`, `hrule`: rounded `box_tl ╭`, `box_tr ╮`, `box_bl ╰`, `box_br ╯`, `box_h ─`, `box_v │`; heavy `hbox_tl ┏`, `hbox_tr ┓`, `hbox_bl ┗`, `hbox_br ┛`, `hbox_h ━`, `hbox_v ┃`. ASCII forms: corners `+`, horizontals `-`, verticals `\|` (RR line 25). All candidates measured one cell in Rich 15. Never write a box character as a literal in a string: `ascii_safe` (terminal.py:133-135) turns any non-ASCII character into `?`; always go through `glyph()`. |
| 3.2 | Frame helper | `OBS/render.py` (next to `_pad` 83-84) | `MARGIN = 1`, `FRAME_ROWS = 2`, `INNER_PAD = 1`. `_frame(title: str, body: list[Line], width: int, policy: TerminalPolicy, *, weight: str = "round") -> list[Line]` returns lines exactly `width` cells wide: top `tl + h + " " + title + " " + h*fill + tr`, body rows `v + " " + Line.padded(inner) + " " + v` with `inner = width - 4`, bottom `bl + h*(width-2) + br`. The title is clipped to `inner - 2` with `clip()`, so a long title cannot squeeze required body text. Border spans use `border_attention` for `weight="heavy"` and `border_secondary` for `"round"`; the title span is bold in the same colour. `Line.padded(width, policy) -> Line` pads with spaces by `cell_len`. Callers add the one-cell margin with `_indent(lines, MARGIN)`. |
| 3.3 | Thread the inner width | `OBS/render.py` (`_panel_lines` 359-387, `_question_line` 311-326, `_desk_lines` 329-356) | `pane = policy.width - 2*MARGIN`, `inner = pane - 4`. `_question_line(q, policy, inner)` and `_desk_lines(desk, policy, inner)` take the inner width in place of `policy.width`; every `wrap`, `clip` and the `room` arithmetic at lines 320-325 use `inner`. `_panel_lines` builds the body (run line, state, disclosure, counts line, caveat, question rows, cut text, `DESK_SELECTED_HIDDEN`, empty and window-full text, notes, retention) without the title and returns `_frame(panel.title, body, pane, policy, weight=...)`. Weight rule from the mockups: the list pane is heavy when there is no desk, round when a desk is shown; the desk pane is heavy. The desk is a separate frame in this phase (`DESK_TITLE` in its border). |
| 3.4 | Keep the budget exact | `OBS/render.py` (sizing 433-481, `base` 441-443, `spare` 447-457) | `base` is `len(_panel_lines(replace(panel, lines=(), empty_text=None), policy, None))` and `len(desk)` is the length of the returned list, so both include the frame rows with no new term. Keep the three `+1` terms as they are. Where the desk does not fit and `DESK_HIDDEN` replaces it, the notice goes inside the list frame body. The forced single ledger row at render.py:502 is unchanged. |
| 3.5 | Test helpers | `T/conftest.py` | `unframe(line: str) -> str` strips the margin, the left and right border glyph (rounded, heavy and ASCII forms) and one padding cell; `title_of(lines) -> list[str]` returns the text inset in top borders. Both are used only by tests. |
| 3.6 | Update tests | `T/test_render.py`, `T/test_commands.py`, `T/test_question_cap.py` | Whole-line checks become frame-aware: `DESK_TITLE in lines` (:900, :924, :997) becomes `DESK_TITLE in title_of(lines)`; `startswith("▸ ")` (:897), `startswith("dispatchId:")` (:964 and the desk slice :951-966), `endswith("reason unknown")` (:938, :948), `startswith("questions shown ")` (:479, :646), the exact `window full: older questions may be missing` (:547, `T/test_question_cap.py:77` and `:121`) use `unframe(l)`; `T/test_commands.py:672-675` and `:690` (`COORDINATOR QUESTIONS` and `seen, not resolved: 4 \| closed by evidence: unavailable (no source)` as whole lines of `--once --width` output) use `title_of` and `unframe`. `test_inspector...` at :118-132 is not framed and does not change. `test_decision_2` (:660-676, 8 `reason unknown` lines at height 26): two frame rows now come out of the same budget; re-pin the count from the measured value and record in the commit message that the owner's rule "the questions win on a short terminal" (comment at render.py:444-445) still holds while two fewer questions fit. `test_r3_the_desk_gives_way...` (:990, heights 8 to 60 at 116) keeps passing if every state is still reached; adjust only the height range if a state disappears. |
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

**Dependencies:** Phases 1 to 6 closed (or P4 and P5 skipped by D-1).

**Closes:** no finding on its own; it records the spec changes the closed findings require.

| Step | Action | Files | Details |
|---|---|---|---|
| 7.1 | Spec edits | `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` | Lines 17 (title bar and badge), 25 (box glyph ASCII forms), 41 (RETAIN CONTEXT built), 43 and 57 (two columns, if D-1 is yes), 61 (reconcile with RR 42: the two 80-column invariant lines and "reachable only through the inspector"; the owner chooses the wording, G-H), 70 (muting implemented), 20 (token reads `POLICY FROZEN unavailable (no source)`, view.py:948), 33 (the `flags` column exists at 116 and 80). Pane titles `OBSERVATION WINDOW`, `RETAIN CONTEXT` and the D-8 desk evidence title are recorded there. |
| 7.2 | Keep the baseline capture honest | `VP/inputs/tools/render_current.py` | Update its docstring (lines 6-9 say the ANSI captures are empty of escapes). Keep `VP/inputs/current/` as the pre-fix baseline; write the post-fix harness output under the gate output directory, not over it. |
| 7.3 | Final gate matrix | `VP/tools/render_compare.py`, `T/test_live_screen_pty.py` | Widths 160, 116, 80 at the mockup heights (48, 42, 42) and the text matrix at heights 44, 40, 24, 12, 8; passes truecolor, 256, 16-colour, NO_COLOR, ASCII; a pty run at each width; one fresh reviewer per width scores every rubric row. Every High and Medium row must pass; Low rows pass or are logged as deferred. |
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
| Mapping from real `workerState`, `dispatchStatus` and liveness words to the four state colours | [UNVERIFIED], RR 93 says no verified settled mapping | Step 1.4 | Only values with a stated meaning are coloured (D-7); the word is always printed |
| Longest `_flags_text` versus the 10-cell `flags` column | [UNVERIFIED] | Step 6.1 | Measure first; fallback is an unframed 160-column table |
| Which of the three `+1` terms in `spare` is which (render.py:454-456) | [UNVERIFIED] | Steps 3.4, 5.4 | Read the comment at render.py:444-445 first; the terms are not edited |
| Exact `PYTHONPATH` layout and approval for regenerating the release-1 golden | [UNVERIFIED] | Step 2.7 | The plan regenerates from the current tree, not from release 1 source |
| Whether East-Asian-ambiguous box and block glyphs are one cell in the owner's terminals | [UNVERIFIED] | All frames | Rich's `cell_len` says one; carry as a caveat |
| Mockup background (dark navy) and light-terminal behaviour of the palette | [UNVERIFIED] | RB-01 | Background is not scored |
| Selected-question look (M-18) | [UNVERIFIED] (no selected row in any mockup) | Step 1.4 | Scored against RR line 50 (glyph kept) plus a bold amber role, not against a mockup |
| Plan-approval ask content (path, file list, 64-hex hash) stored as question rows | [UNVERIFIED] (`pr-591-comment.md` lines 26-31) | Q7 fixture | Fixture is synthetic; confirm with the plan-ask source |
| Zellij: floating panes, `dump-screen --ansi` fidelity, command panes, theme read at runtime, presence in CI | [UNVERIFIED] | Step 7.4 only | Not a dependency (Q6) |
| Interaction of fixtures `injection` and `long-identifiers` with styling | [UNVERIFIED] | Phase 1 gate | Include both in the harness matrix |
| Owner rulings D-1 to D-8 and OPEN-1 to OPEN-3 | open | see 8.2 | Defaults stated; effect if different stated |

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
| 15 | OPEN-1, OPEN-2, OPEN-3 treated as Medium until the owner rules; D-1 to D-8 recorded with the owner's answer | decision record in the PR body | P2, P4, P5 |
| 16 | `make lint` and `make test` pass; no `.claude/` path staged; `.dev/tasks` staged | command output, `git status` | P7 |
| 17 | PR opened only by `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; branch rebased on `origin/master`; returned URL checked | PR URL | P7 |

### 8.10 Finding-to-phase map (M-01 to M-18)

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

