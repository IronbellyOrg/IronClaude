# Synthesis 04: Options Analysis and Recommendation (report Sections 6 and 7)

Research question: how to redesign the read-only Orca terminal observer (`superclaude observe`) presentation to reach theme, styling and layout parity with its design mockups (issue #606; merged findings M-01 to M-18, guards G-1 and G-2, accepted divergences AD-1 to AD-7, open items OPEN-1 to OPEN-3, owner decision O-1).

Path conventions: `R01` to `R05` = `research/01-...` to `research/05-...`; `W01`, `W02` = `research/web-01-...`, `research/web-02-...`; `GAPS` = `gaps-and-questions.md`. Code paths are relative to `src/superclaude/cli/observe/` unless they start with `tests/`. Tags: [CODE-VERIFIED] was read or probed in code; [CODE-CONTRADICTED] a doc or inference corrected by code; [UNVERIFIED] not confirmed in code (doc-only, help-text-only or not measured). Web-sourced statements are marked "external context" with their source URL.

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
| Q7 the 64-hex-character fixture in the 80-column Decision Desk frame; wrap or cut | Measured on the current code (no frame yet): `wrap` leaves a 64-cell hash whole on its own line at 160, 116 and 80; a 100-character unbroken token is hard-cut at the width with no marker; the desk text is capped at `DESK_TEXT_LINES = 4` and the list line is cut with `...` before the hash. Inside a mockup-style 78-wide frame the inner width is 74, so a 64-cell hash still fits alone but `label: <hash>` (about 84) moves the hash to its own line; the risks are the 4-line cap replacing a hash that trails a long path and file list, and a pane that clips instead of wrapping. Recommended rule: wrap the hash so it is never split when it fits the inner width (64 cells fit at every planned width), and state the exception that the 4-line cap (and the 400-character ask cap at parse.py:503) still cut a hash that falls beyond the fourth wrapped line; pin both behaviours and leave any change of the caps to the owner (D-6); add the fixture and test in P0 (name proposed: `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk`, parametrized over 160/116/80, plus the screen-only canary `HASH not in record_text(view)` and `snapshot_json(view)`); add a second fixture with a trailing hash; give hard-wrapped tokens wider than the inner width a decided, tested rule | R01:128-134; R03:160-187, 232; R04:198-209; render.py:62-80, 339-346, 347-353; view.py:99 | High for the measured current behaviour. Medium for the framed case (derived arithmetic). [UNVERIFIED]: plan-ask content (path, file list, hash) is doc-only (pr-591-comment.md lines 26-31); the hash policy is an owner decision (Q-6) |

### 7.3 What the owner must decide

| Id | Decision | Recommendation | What it unblocks |
|---|---|---|---|
| O-1 | Adopt two-column layouts for the questions screen and the Decision Desk at 160 and 116, reversing "one stacked block" in rendering-rules.md lines 43 and 57 | Yes, with 80 columns staying stacked and the spec text updated in the same change (FINDINGS recommendation; GAPS Q-1) | M-03, M-04 and the P4 and P5 phases; decides the Q1 layout scope |
| OPEN-1 | Severity of the question-list hierarchy (M-07): Astra High, Opus Medium | Treat as Medium (gated) as FINDINGS does; Medium follows from M-03 being High | Whether M-07 gates the close of P4 |
| OPEN-2 | Whether RETAIN CONTEXT is built and its severity (M-14): Opus Medium, Astra Low; changes RR lines 41 and 61 | Medium (gated); schedule late; decide with the 80-column wording | A render-only pane built from `run_line`, `caveat_line`, `retention_line` (view.py:794, 798, 804) |
| OPEN-3 | Title bar and READ ONLY badge (M-13): severity and scope; RR line 17 must be reconciled | Medium (gated): badge required, exact alignment and the diamond glyph optional | Header split inside render.py only |

Further decisions that the research surfaced and the plan depends on:

| Decision | Source | Effect |
|---|---|---|
| Golden strategy: re-baseline `golden_release1_surface.json` and `golden_questions_linkoff.json` (ends T47's release-1 meaning), or keep the questions-off screen frozen and apply the redesign only with questions on, or add a new golden | GAPS row 1; R03:227 | Whether P2 and P6 may change questions-off screens and P3 and P4 the link-off questions screens |
| Target colour depths (16 only, or truecolor with 16-colour fallback) and whether bold and dim should survive NO_COLOR | GAPS row 2, Q-5; W01 | Q4 option D1 or D2 |
| Whether the Decision Desk shows a plan hash in full, cut with a visible mark, or wrapped | GAPS row 5, Q-6 | Q7 rule and the hard-wrap rule |
| PNG renderer as a new dev dependency | GAPS Q-7 | Q3: this report recommends no for the gate |
| Reword RR line 61 (80-column invariant lines) versus RR line 42 and AD-7 | GAPS row 8 | The 80-column spec text |
| Whether a piped `--once --width` may carry ANSI and whether it may carry box lines | GAPS row 3; R03:228 | Q5 capture route and `test_commands.py:121` |

### 7.4 Coverage note

Carried into this report: the style-only phase economics and the NO_COLOR test rewrite (R03 sections 3 to 6); the `safe_box` correction (R01, R03, R04); the `export_text(styles=True)` hazard (R02); the live-path measurements, including the silent bottom crop (R02 section 9); the mockup palette, its 16-colour collapse and the pane geometry (R04 sections 2 to 4); the Zellij and harness environment (R05); the external context (W01, W02). Excluded with rationale: documentation line-number drift and cosmetic count mismatches in GAPS rows 43 to 58 (they do not change an option or an answer); the Zellij pane-frame arithmetic and the aidev02 theme lines 179-252 (not read, flagged [UNVERIFIED]); licence confirmation for freeze, pyte, aha and cairosvg (H2 is not recommended).
