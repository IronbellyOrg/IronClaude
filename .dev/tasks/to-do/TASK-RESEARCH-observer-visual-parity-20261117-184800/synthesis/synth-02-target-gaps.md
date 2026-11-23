# Synthesis 02: Target State and Gap Analysis (report Sections 3 and 4)

**Research question:** how to redesign the read-only Orca terminal observer (`superclaude observe`) presentation to reach theme, styling and layout parity with its design mockups, driven by merged findings M-01 to M-18, guards G-1 and G-2, accepted divergences AD-1 to AD-7, open items OPEN-1 to OPEN-3 and owner decision O-1.

**Inputs weighed:** research files 01 to 05, web-01, web-02 and `gaps-and-questions.md` (all under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/`).

**Conventions used below**
- `render.py`, `view.py`, `terminal.py`, `commands.py`, `export.py` are under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/`. `RR` is `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`. `FIND` is `.dev/issues/409/visual-parity/merged/FINDINGS.md`. Mockups are `.dev/issues/409/visual-parity/inputs/mockups/{160,116,80}/`.
- Tags: [CODE-VERIFIED] read in code or reproduced by a probe; [CODE-CONTRADICTED] a claim the code or a measurement refutes (the corrected statement is given); [UNVERIFIED] not confirmed; [STALE DOC] a document that no longer matches code. Doc-only claims are never stated as current state.
- Web findings are marked [external context] with their source URL.
- Severity scale used in Section 4: **Critical** = FINDINGS "High" or a C8 defect (spec-required behaviour that is not wired); **Important** = FINDINGS "Medium", a decision that gates other rows, or a Gate 1 "Important" gap; **Minor** = FINDINGS "Low" or a note. Gate 1 found 0 Critical research gaps; Critical here marks product gaps, not research gaps.

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
| amber | 250,178,25 | attention frame (heavy), its title, question text and ages (bold), `SYNTHETIC / READ ONLY` badge, tile digit | 11 | 214 |
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
| SC-6 | At the 16-colour depth the state roles (running, settled, failed, frozen) produce pairwise distinct SGR codes, or the state word alone carries meaning and is printed | check against the Q4 role table at `standard`; criterion derived from the 04 collapse measurement, threshold chosen with the Q4 decision | 04 section 3 |
| SC-7 | The record and JSON snapshot are byte-identical to today, and contain no question text | test_export.py:307-332, test_snapshot_schema.py:457-479, golden `record_text` and `snapshot_json` keys; add a canary that the new fixture's hash is absent from both | 02 section 5 |
| SC-8 | Required text survives: counts text, disclosure, gap notice, `reason unknown` on every question line, retention sentence, PARTIAL literal never cut | flat-text tests (test_render.py:192, :202, :437, :679) | 03 section 1 |
| SC-9 | Height: `len(screen_lines) <= policy.height` at 40, 44, 24, 12 and 8 (or the too-small diagnostic); footer stays in the last 3 or 4 lines | new matrix test; test_render.py:748, test_inspector_scroll.py:36-72 kept | 02 section 9.4 |
| SC-10 | A 64-hex hash in a Decision Desk question appears whole on one line at 160, 116 and 80 inside the framed desk; the text loses nothing when under the 4-line cap; paths longer than the inner width hard-split and lose nothing | new `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk` (03 section 5d), parametrized over widths; synthetic hash only | 03 section 5 |
| SC-11 | At 80 columns the key list is not cut: no line ends in `>` and contains `exp`; the full list is present | test_render.py:748 (test_f08) generalised to questions-off | M-11 |
| SC-12 | At 80 columns no COUNTS token is cut inside its text | new assertion on `counts_lines`; `>` only after a whole token | M-16 |
| SC-13 | A column heading line is present at 116 and 80 when at least one row is visible | new test; today only at 160 (render.py:497) | M-10 |
| SC-14 | Mockup parity score from a fixed-rubric reviewer meets a threshold | rubric and threshold are NOT yet defined; 04 sections 2 and 4 give the raw material (eight roles, pane geometry); see Section 4 harness row | Q3 |
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

### 4.1 Gap table

Severity follows the scale in the header. FINDINGS severity is kept in Notes. Rows flagged **OPEN** are undecided. Rows flagged **C8 DEFECT** are unwired in-scope capabilities: the spec names the behaviour as required, the code does not wire it at its runtime entrypoint, and no cited scope decision moves it to future work, so each is a defect with a linked remediation need (Section 4.2) and is not downgraded. Fix locations are in `render.py` unless stated.

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
| Live versus one-shot styled capture (Q5) | Live path keeps SGR; `--once --width` calls `export_text()` (styles dropped, commands.py:242); `--once` without `--width` prints `record_text`; today nothing is styled | A styled capture route that honours NO_COLOR and the colour system; gate tests for ANSI present, none under NO_COLOR, plain text equal to the golden lines, widths 160, 116, 80 and ASCII | Important | `export_text(styles=True)` bypasses NO_COLOR and down-conversion (probe) [CODE-VERIFIED]; the NO_COLOR-correct route is `console.file.getvalue()`. 02 wins over 01 and 03 on the route (Section 4.3). **OPEN**: ANSI on a piped `--once --width` (no tty check today); box-drawing in `--once --width` output; test_commands.py:121 (`"\x1b" not in out`) changes only if the styled route is chosen |
| Live screen has no test (G-F) | No test references `LiveScreen` or `run_interactive`; `FakeScreen` records calls only; `make_console` has no `force_terminal` parameter | A pty (pexpect 4.9.0) or `force_terminal` seam capture of the real `LiveScreen` | Important | Cycle-1 measurements used a stand-in console. [UNVERIFIED]: whether `run_interactive` accepts `--fixture`. `spike_child.py:64` already runs a raw `Live(screen=True)` on a pty |
| Height budget and silent bottom crop (G-G) | No final `lines[:height]` clamp; one ledger row forced (render.py:502); `Screen` cuts rows past the height; footer lost first | Every frame, tile and heading row counted in the budget; matrix test at 40, 44, 24, 12 and 8 | Important | Only the base fixture at height 40, the `five` golden and desks at height 70 were run; frames at smaller heights are [UNVERIFIED]. Which of the three `+1` terms in `spare` is which (render.py:454-456) is [UNVERIFIED] |
| Golden re-baselining (G-A) | T47 (test_render.py:611-624) pins questions-off `lines_*` and `printed_*` to release 1 (`git archive 9e2608b03`); T64 pins link-off lines (`golden_questions_linkoff.json`) | Owner decision: re-baseline both, or freeze questions-off and gate the new look to questions-on, or add a new golden and keep T47 | Important | **OPEN**. M-10 and M-11 (C8 defects) change questions-off lines at 116 and 80, so this decision gates their remediation. No recorder exists for the link-off golden; regeneration commands are derived, not owner-approved; the exact `PYTHONPATH` layout is [UNVERIFIED]. Style-only changes touch 15 `printed_*` values and no link-off values |
| Render harness (Q3) | No PIL, cairosvg, pyte, playwright, fontTools, browser, rsvg-convert, ImageMagick, freeze or aha; `pyproject.toml` and the Makefile declare nothing for images; Rich `export_svg` and `export_html` available; `render_current.py` writes text and ANSI via `export_text(styles=True)` at height 50 | A reproducible text and ANSI tier (offline) plus an image tier for the reviewer, with a fixed rubric | Important | `render_current.py` ignores NO_COLOR and the 16-colour downgrade, so a harness built on it shows truecolor a 16-colour terminal never shows (F-02); capture `console.file.getvalue()` through `make_console` instead. Rich SVG needs a browser engine: rsvg-convert and ImageMagick failed on it [external context: https://github.com/Textualize/rich/issues/2153; whether Rich 15 changed this is UNVERIFIED]. freeze is the simplest ANSI to PNG binary but is an extra install [external context: https://github.com/charmbracelet/freeze]. Playwright MCP exists only in the Claude session, so CI cannot rely on it. Claude agents can view PNGs with Read (both Gate 1 QA reviewers did). **OPEN** (Q-7: new dev dependency or text rubric plus mockup PNG). Rubric criteria are not yet written (SC-14) |
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
