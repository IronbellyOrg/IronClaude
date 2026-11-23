# Research: spec, mockups and merged findings
**Investigation type:** Doc Analyst
**Scope:** the files listed above
**Status:** Complete
**Date:** 2026-11-17
---

All paths below are relative to `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`. `RR` = `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; `FIND` = `.dev/issues/409/visual-parity/merged/FINDINGS.md`; `render.py`, `terminal.py`, `view.py` = `src/superclaude/cli/observe/`.

## 1. Citation check: rendering-rules.md lines cited by FINDINGS.md

Every cited line was re-read in RR (108 lines total).

| RR line | What the line says (short) | Cited by | Verdict |
|---|---|---|---|
| 13 | Height follows C's 44-row contract; coverage/scope/PARTIAL/gap notice are minimum content; "No per-panel scrolling, no multi-pane focus" | AD-5 | [CODE-VERIFIED] consistent with render.py:390-521 (one focus: list, filter or inspector) |
| 17 | Header line 1 contract `ORCA OBSERVER  mode=...  scope=...  as of ...`; fixture reads `SYNTHETIC FIXTURE <variant>, not Orca data`; `one Run only: <runId>` | M-13 | Text verified; the contract has no READ ONLY badge, so M-13 changes this line (spec change needed) |
| 20 | COUNTS strip: numbers only, "no bars, no health name"; tokens; `>` only on low-priority tokens; wraps to second line first | AD-1, AD-2, M-16 | Verified. M-16 "legal under line 20" is accurate |
| 21 | Keys list (Up/Down, j/k, Enter, Esc, `/`, h, m, e, q; with link switch n/p); no `r` | AD-5, M-11, M-15 | Verified |
| 25 | Truncation by display cells with visible `>`; `--ascii` replaces box drawing with `+-\|` | G-1 | Verified; the only ASCII-box rule in the spec |
| 30 | Worker ledger: one row per worker, fields listed, "no `stage` column at any width" | M-06, AD-3 | Text verified. The "153 cells" figure is NOT on line 30 [UNVERIFIED]; see Gaps |
| 31 | `nextAction.kind` verbatim, never classified | M-09, M-10, AD-3 | Verified |
| 32 | Gap notice above the ledger at every width, exact strings | M-06 | Verified |
| 33 | 116 cols: `<kind> <dispatchId> <liveness.verdict> <age>`; 80 cols: kind, truncated id, age | M-10, AD-6 | [CODE-VERIFIED] matches render.py `_columns` line/short classes (render.py:193-229) |
| 38-50 | B 160 layout, RETAIN CONTEXT (41), retention (42), stacked block (43), state lines (44-49), per-question line (50) | M-03, M-07, M-14, R-3 | Verified. Line 43 is the O-1 reversal target. Line 41 says RETAIN CONTEXT is "not built in R2" |
| 57 | Decision Desk "one stacked block under the question list", unlinked-reason wording, AC-7 worktree note | M-04, M-12, AD-4 | Verified. O-1 reversal target together with line 43 |
| 61 | 80 columns single column; invariant lines; "RETAIN CONTEXT is reachable only through the inspector" | M-14, AD-7 | Text verified; internally inconsistent, see Stale Documentation |
| 70 | Absent field = literal `unknown`, muted (plain under NO_COLOR) | M-08 | Verified |
| 93 | "Fleet SIGNALS bars" left out; no verified settled mapping | AD-2 | Verified |

Other lines used by FIND: 39 (ledger titled `worker-reported, not questions`, AD-5), 41, 42 (retention in memory, AD-7), 43, 50 (age format, R-3).

Key Takeaways
- All citations in FIND resolve to the lines claimed; no line-number drift found in RR.
- Two spec lines carry the O-1 reversal: RR 43 ("One stacked block at every width ... the two-column layout above stays design reference") and RR 57 ("one stacked block under the question list").
- Spec lines that change if the fix proceeds: 17 (badge), 41 and 61 (RETAIN CONTEXT built), 43 and 57 (columns), 25 (ASCII panes), 70 (muting becomes implemented).

## 2. Mockup colour decode (all nine `.ansi` files)

Method: every `\x1b[...m` sequence in `inputs/mockups/{160,116,80}/*.ansi` was counted and each coloured text segment was grouped by colour (read-only script in /tmp, not in the repo). All sequences have the form `ESC[0;38;2;R;G;Bm` (foreground only) or `ESC[0;1;38;2;R;G;Bm` (bold) plus `ESC[0m`. There is no background (48) code, no 256-colour (38;5) code, no 16-colour code, no dim/italic/underline/reverse. [CODE-VERIFIED against the files, 15 distinct sequences in 160 signal-bridge, 8 to 11 in the others.]

| Role (name used here) | RGB | Where it is used (verified from segment text) |
|---|---|---|
| base | 225,233,238 | default body text and all padding (most frequent code in every file); owner/scope lines; list items in the ledger left pane (question text is base+bold) |
| muted | 165,182,194 | clock/freshness line (`08:00 UTC \| msgs partial ...`), `Affected:` lines, keys hint line, `7/7 lines shown`, register state lines (`not observed / not admitted \| ...`), column caption `SESSION / LIFECYCLE / PHASE; ...`, footer caveat `LOCAL FIXTURE ...` |
| slate | 82,108,128 | borders of secondary panes (rounded `╭╮╰╯─│`), the horizontal rule above the footer and between questions, pane titles of secondary panes (bold), empty SIGNALS bar fill `░` |
| amber | 250,178,25 | attention content: heavy `┏┓┗┛━┃` frame of the HUMAN QUESTION / OPEN HUMAN QUESTIONS pane, its title (bold), question text (bold), ages `45 MIN` (bold), the `SYNTHETIC · READ ONLY` badge (not bold), the large digit in the SEEN tile |
| cyan | 112,205,226 | identity and counts: screen title `◈ SIGNAL BRIDGE` / `◈ ATTENTION LEDGER` / `◈ DECISION DESK` (bold), count-tile frame and title (SEEN IS NOT RESOLVED), SIGNALS frame, running sessions (`S001 running / work`), RUN bar |
| green | 139,215,175 | settled sessions (`S007 settled / work`), `24  SETTLED` (bold) and its bar |
| red | 240,141,150 | failed session (`S009 settled / queue`; its detail line says `failed`) |
| violet | 194,173,242 | frozen: `S015 running / queue`, `1  POLICY FROZEN` (bold) |
| selected | none found | The mockups have no selected-row colour or reverse video; no `>`/`▸` selected row is drawn in any of the nine `.txt` files (checked in the three 160 files). Selection is a keys-hint only (`j/k select`). [UNVERIFIED how selection is meant to look] |
| borders | amber (heavy, attention panes), slate (rounded, secondary panes), cyan (count tile and SIGNALS frame) | |
| titles | bold in the colour of their box (amber, slate or cyan); screen title bold cyan with `◈` | |
| count tile | cyan frame and bold cyan title; digit drawn in amber block characters (`███` rows, 160 ledger lines 9-13); 160 SIGNALS counts bold in the state colour with bar `█` (state colour) over `░` (slate) | |

Bold usage found: titles, question text (amber bold in desks, base bold in the 160 ledger), ages, SIGNALS counts, `◈` screen titles. Count of `ESC[0;1;` sequences is 2 to 15 per file.

## 3. Colour depth the mockups assume, and the 16-colour mapping (Q4)

- The mockups assume 24-bit truecolor (38;2;R;G;B) at every width. No fallback ramp exists in them. [CODE-VERIFIED in the `.ansi` files]
- Current code builds the Console with `color_system=None if policy.no_color else "standard"` (`terminal.py:121`), i.e. 16 colours at best, and no module styles any text (`render.py:528`, `Text(line, no_wrap=True, overflow="crop")`). [CODE-VERIFIED] Rich therefore downgrades any truecolor style to the 16 standard colours.
- Computed with Rich's own downgrade (`Color.parse("rgb(...)").downgrade(ColorSystem.STANDARD)`, run once, read-only, in this repo's venv) the eight mockup colours map to:

| Role | Standard-16 index | 256 index |
|---|---|---|
| base | 15 (bright white) | 189 |
| slate | 8 (bright black) | 60 |
| cyan | 14 (bright cyan) | 80 |
| muted | 7 (white) | 145 |
| amber | 11 (bright yellow) | 214 |
| green | 7 (white) | 115 |
| red | 7 (white) | 210 |
| violet | 7 (white) | 147 |

- Consequence for Q4 [derived from the table above, not run on a real terminal]: at 16 colours the roles slate (8), cyan (14), amber (11) and base (15) stay distinct from each other, but muted, green, red and violet all collapse into index 7. Muted versus base is a small step (7 vs 15). So the state colours (M-09: green settled, red failed, violet frozen) are NOT distinguishable by colour alone at 16 colours when the mockup RGB values are passed through Rich's downgrade; the theme needs per-depth explicit 16-colour roles (for example green=2/10, red=1/9, magenta=5/13) or text plus colour. Slate versus muted is also the only 8 versus 7 pair on dark terminals and depends on the terminal theme.
- NO_COLOR keeps `color_system=None` (terminal.py:121) and `no_color=policy.no_color` (terminal.py:122). `resolve_policy` sets `no_color` when the env var is set and non-empty (terminal.py:83). [CODE-VERIFIED]
- Nothing in `terminal.py` detects COLORTERM or terminal capability; the depth is a fixed string "standard". [CODE-VERIFIED by reading the whole file] G-2's "the spec decides the targeted depth and detection" is therefore an open design item, not an existing mechanism.

Key Takeaways
- Mockup palette is 8 truecolor foregrounds plus bold, no backgrounds, no dim; it is a dark-theme palette.
- ANSI-styled output is the primary mode, but code is capped at "standard" (16): the cap, not Rich, is what flattens three state colours plus muted into one.
- State colour is not a safe sole carrier of meaning at 16 colours; raw state words must stay printed (they are, per RR line 31 and 71).

## 4. Mockup pane geometry (box characters, widths, heights, titles)

Measured by a read-only script over `inputs/mockups/<w>/*.txt` (column index = 0-based, left margin 1 space, so width w pane = cols 1..w-2). Heavy box `┏━┓┃┗┛` = amber attention pane; rounded `╭─╮│╰╯` = secondary pane. Frame height is 48 lines at 160 and 42 lines at 116 and 80; line width is exactly the column count (160/116/80) in all nine files. [CODE-VERIFIED]

| Screen / width | Panes (title, box type, columns, width, rows) |
|---|---|
| signal-bridge 160 | HUMAN QUESTION heavy c1-46 (46 wide, rows 6-13) over OBSERVATION WINDOW round c1-46 (rows 16-44); SESSION REGISTER round c49-122 (74 wide, rows 6-44); SIGNALS heavy c125-158 (34 wide, rows 6-44). Three columns 46/74/34 with 2-col gaps |
| signal-bridge 116 | HUMAN QUESTION heavy c1-114 (114 wide, rows 6-12); SESSION REGISTER round c1-78 (78 wide) beside OBSERVATION WINDOW round c81-114 (34 wide), rows 14-38. SIGNALS pane absent |
| signal-bridge 80 | HUMAN QUESTION heavy c1-78 (rows 6-12); SELECTED FLEET SLICE round c1-78 (rows 16-38), single column; the counts appear as one line `RUN 48  SETTLED 24  UNKNOWN 8  STALE 5` in cyan |
| attention-ledger 160 | OPEN HUMAN QUESTIONS heavy c1-114 (114 wide, rows 6-44); right column c117-158 (42 wide): SEEN IS NOT RESOLVED round cyan (rows 6-18) over RETAIN CONTEXT round slate (rows 21-38) |
| attention-ledger 116 | OPEN HUMAN QUESTIONS heavy c1-70 (70 wide, rows 6-38); right column c73-114 (42 wide): SEEN tile rows 6-18, RETAIN CONTEXT rows 21-38. Same structure as 160 with `right = 73` (matches RR line 60) |
| attention-ledger 80 | single column; one titled pane SELECTED SIGNALS round cyan c1-78 (rows 12-38); the questions are three plain base lines `Q01 45m  Choose schema...` above it (no heavy frame); no tile, no RETAIN CONTEXT pane |
| decision-desk 160 | HUMAN QUESTION heavy c1-76 (76 wide, rows 6-13) over OTHER OBSERVED QUESTIONS round c1-76 (rows 16-44); AFFECTED SESSION EVIDENCE round c79-158 (80 wide, rows 6-44). Two columns 76/80 |
| decision-desk 116 | HUMAN QUESTION heavy c1-114 (rows 6-13) full width; below it AFFECTED SESSIONS round c1-66 (66 wide) beside OTHER OBSERVED QUESTIONS round c69-114 (46 wide), rows 16-38 |
| decision-desk 80 | three stacked panes, each c1-78: HUMAN QUESTION heavy rows 6-13, AFFECTED SESSIONS round rows 16-27, OTHER OBSERVED QUESTIONS round rows 30-38 |

Common chrome in all nine: line 2 = `◈ <SCREEN NAME>` left (bold cyan) and `SYNTHETIC · READ ONLY` right-aligned (amber); line 3 `8 owners / 80 sessions / 80 mapped trees`; line 4 clock/freshness line (muted); a slate horizontal rule of `─` above the footer (line 46 at 160); footer two lines: keys hint and `LOCAL FIXTURE · source coverage is not fleet-wide assurance`. Titles are inset in the top border with the pattern `┏━ TITLE ━━━...┓` / `╭─ TITLE ───...╮`. [CODE-VERIFIED in `.txt` and `.ansi`]

Anomalies
- The two 80 and 116 mockup headings differ from the 160 ones: 116 desk pane is called AFFECTED SESSIONS (160: AFFECTED SESSION EVIDENCE); the 80 ledger pane is SELECTED SIGNALS and the 80 bridge pane SELECTED FLEET SLICE (neither exists at 160/116). The mockups at 160 title the left ledger pane OPEN HUMAN QUESTIONS, which RR line 38 retires in favour of COORDINATOR QUESTIONS (code: view.py:53 `QUESTIONS_TITLE = "COORDINATOR QUESTIONS"`). Pane titles to copy must therefore not be taken from the mockups for this one.
- 160 and 116 attention-ledger left pane are the same design; the mockup keeps a `7/7 lines shown` style overflow counter in every pane; the observer's own overflow texts are in RR line 51.

Key Takeaways
- Q1: the two-column compositions need exact column pairs: 160 ledger 114 + 42 (RR already specifies x=1 width 114 and x=117 width 42, lines 38 and 40), 160 desk 76 + 80, 116 ledger 70 + 42, 116 desk full-width question over 66 + 46, 160 bridge 46 + 74 + 34 (three columns).
- At 80 columns every mockup is a single column of 78-wide panes; the mockup's own 80 ledger has no tile and no RETAIN CONTEXT.
- 160 mockup pane heights are fixed to the full frame (rows 6-44) with blank interior; the observer's content is data-dependent, so heights need a rule (RR line 13: C's 44-row contract; code uses `policy.height`, render.py:447).

## 5. Merged findings M-01 to M-18: what each says, spec line, spec action, code location

Spec action column: CHANGE = the spec line must change for the fix; KEEP = the spec line is a guard the fix must preserve; O-1 = conflicts with the recorded stacked choice (RR 43, 57); NONE = spec silent or already requires it. Severity is as stated in FIND. Current-output evidence is from `inputs/current/<w>/*.txt`; line numbers are in those files (re-read, [CODE-VERIFIED] unless stated). Code line numbers are in `src/superclaude/cli/observe/` and were read in this session.

| ID | Says (short) | RR lines touched | Spec action | Mockup evidence | Current evidence | Code location that must change | Sev |
|---|---|---|---|---|---|---|---|
| M-01 | No colour/weight anywhere | 70 (muted), 25 | NONE (adds styling); text must stay identical for NO_COLOR/exports (AC-9 T26-T28) | all nine `.ansi` (see section 2) | 0 ESC bytes in all nine `ansi-*.txt` (rg `\x1b` found no match) [CODE-VERIFIED]; 160/ledger.txt:1 plain title | `render.py:524-531` (`render()` builds unstyled `Text`); `render.py:390-521` returns plain `list[str]`; `view.py:303-339` View carries strings only, no role tags; `terminal.py:110-125` `make_console` (theme/depth) | High |
| M-02 | No boxed titled panes | 25 (ASCII `+-\|`), 38-40 | CHANGE (25: pane glyph forms) | `mockups/160/decision-desk.txt:6-44`, `signal-bridge.txt:6-44` | 160/questions.txt:5 `COORDINATOR QUESTIONS`, :15 `worker-reported, not questions`; desk.txt:14 `DECISION DESK` | `render.py:359-387` `_panel_lines` (title at :368), `render.py:329-356` `_desk_lines` (:333), `render.py:495` ledger title; `terminal.py:30-34` GLYPHS (no box glyphs) | High |
| M-03 | Questions screen has no two columns | 38, 40, 43, 60, 61 | O-1 + CHANGE (43) | `mockups/160/agent-focus-attention-ledger.txt:6-44` (114 + 42), 116 (70 + 42), 80 single column | 160/questions.txt:5-14 one stacked block | `render.py:433-486` (panel composed as `gap_part`, `top = head + gap_part + tail` at :486) and `_panel_lines` | High |
| M-04 | Decision Desk stacked | 43, 57 | O-1 + CHANGE (43, 57) | `mockups/160/decision-desk.txt` (76 + 80), 116 (full + 66 + 46), 80 (3 stacked) | 160/desk.txt:14-26 single column, ledger repeated :28-36 | `render.py:329-356` `_desk_lines`, `render.py:458-469` desk sizing; `view.py:814-874` `_desk` | High |
| M-05 | Count has no weight | 40, 47, 61 | NONE (RR 40 already designs the big count; text forms in 47 must be kept) | `mockups/160/agent-focus-attention-ledger.txt:6-18` (tile rows 9-13, cyan frame, amber digit) | 160/questions.txt:9 | `view.py:761` (counts_line string), `view.py:263` `open_total`; `render.py:374` (`wrap(panel.counts_line)`) | High |
| M-06 | Ledger lacks attention slot, observation pane, tiles | 20, 30, 32 | KEEP 20, 32 (gap notice and counts text); line 30 column list stays | `mockups/160/signal-bridge.txt:6-44` | 160/ledger.txt:2-5 (`worker-list OK 0s  messages UNVERIFIED (not read)`; counts run-on at :3) | `render.py:409-413` (head), `:480-485` gap_part, `view.py:909-949` (header1, header2, tokens), `view.py:632-641` `_source_counts_text` | Med |
| M-07 | Caveats outweigh question rows; no row emphasis/separation | 38, 49, 50 | KEEP 49 (disclosure verbatim); RR 38 already says at 160 the title carries the disclosure | `mockups/116/agent-focus-attention-ledger.txt:9-30` | 116/questions.txt:5-14 (title, run, state, disclosure x2, counts, caveat before rows at :12-14) | `render.py:359-387`, `render.py:311-326` `_question_line`; `view.py:722-759` (lead/shown); `view.py:54-57,64,73` literals | Med (OPEN-1) |
| M-08 | Absent values not muted | 70 | NONE (RR 70 already requires muted `unknown`): DEFECT | n/a (rule, not a mockup) | 160/questions.txt:3 `source counts: unknown`; :11 `reason unknown`; 160/ledger.txt none (all fields present) | `view.py:377-385` `text_of`, `:477`, `:493`, `:635-637`, `:728`, `:744` `QUESTIONS_REASON`; `render.py:528` | Med (DEFECT) |
| M-09 | State values uncoloured | 31, 71 | KEEP 31 (`nextAction.kind` verbatim, uncoloured) | `mockups/160/signal-bridge.ansi` (cyan running, green settled, red failed, violet frozen); PNG `signal-bridge.png` | 160/ledger.txt:11 `w-002 ... blocked blocked active none review alive (terminal) 13s` | `render.py:233-243` `_row_line` joins cells into one string; `render.py:155-230` `_columns`; `view.py:481-518` `_row_view`; `view.py:843-853` desk fields | Med |
| M-10 | No column heading at 116 and 80 | 30, 33 | NONE | `mockups/116/signal-bridge.txt:15`, `mockups/80/signal-bridge.txt:17` | 116/ledger.txt:8 `   none   w-001 ...` no heading; 80/ledger.txt:9 | `render.py:497-498` (`if policy.width_class == "full" and view.visible_rows:` header only for full) [CODE-VERIFIED]; names exist at `render.py:197-204` and `:216-222` | Med (DEFECT, R-1) |
| M-11 | 80-col key list cut, `q quit` lost | 21, 22 | KEEP 21 | `mockups/80/signal-bridge.txt:41` | 80/ledger.txt:49 `... e exp>` [CODE-VERIFIED] | `render.py:304-308` `_help_lines` (`clip` when `view.questions is None`), `render.py:514-519`; `view.py:105` KEYS_LINE | Med (DEFECT) |
| M-12 | Desk: question does not lead; evidence is unaligned dump | 57 | KEEP 57 order | `mockups/160/decision-desk.txt:6-15` | 160/desk.txt:14-26 | `render.py:329-356`; `view.py:843-853` | Med |
| M-13 | No READ ONLY badge / title split | 17 | CHANGE (17) (OPEN-3) | line 2 of all nine mockups | 80/ledger.txt:1-2; 160/ledger.txt:1 | `view.py:909-921` header1; `render.py:410` | Med (OPEN-3) |
| M-14 | Supported facts scattered; no RETAIN CONTEXT | 41, 42, 61 | CHANGE (41 "not built in R2"; 61 "only through the inspector") | `mockups/160/agent-focus-attention-ledger.txt:21-38` | 160/questions.txt:6,10,14 (three places) [CODE-VERIFIED] | `view.py:794,798,804` (run_line, caveat_line, retention_line); `render.py:359-387` | Med (OPEN-2) |
| M-15 | Footer pair split, no rule/separators | 21, 22 | KEEP 21 | all mockups lines 46-47 (rule + hint line) | 116/questions.txt:23-24 `... n/p` / `question` [CODE-VERIFIED] | `render.py:304-308`, `:423-431`, `:514-519` | Low (R-2) |
| M-16 | 80-col counts cut inside a token | 20 | NONE (line 20 allows `>` on low-priority tokens) | n/a | 80/ledger.txt:5 `runs seen>`; 80/questions.txt:4 `cost un>` [CODE-VERIFIED] | `render.py:94-135` `counts_lines` (cut path at :127-132) | Low |
| M-17 | Blank band after id at 116/80 | 33 | NONE | 116 signal-bridge register line | 116/ledger.txt:9; 80/ledger.txt:10 | `render.py:195` `id_width = min(..., 60)`, `:215` | Low (optional) |
| M-18 | Selected question glyph only | 50 | KEEP 50 (glyph `▸`/`@`, never `>` or `*`) | none (mockups draw no selected row, section 2) | 160/desk.txt:11 `▸ 1h  Choose schema ...` | `render.py:311-326` (mark at :317); `render.py:145-148` `_marker` | Low |

Notes on the table
- M-01's claim "render.py builds Text(line, no_wrap=True, overflow='crop') per line with no style" is [CODE-VERIFIED] at render.py:528. M-10's text says `render()` prints the header only for full; the condition is actually inside `screen_lines()` (render.py:497-498): minor citation drift, behaviour confirmed.
- M-11's cause is [CODE-VERIFIED]: `_help_lines` returns `[clip(view.help_line, ...)]` when `view.questions is None` (render.py:306-307) and wraps otherwise (render.py:308). At 80 columns the link-off ledger footer therefore clips (80/ledger.txt:49).
- M-14 "facts exist in three places" is [CODE-VERIFIED] (160/questions.txt:6 `one Run only`, :10 `no read marker in source`, :14 `retention reset at 12:00`).
- M-09 `nextAction.kind` stays uncoloured: [CODE-VERIFIED] RR 31 and `_next_action_text` (view.py:474-478).

### Guards, accepted divergences, open items, owner decision

| ID | Says | RR lines | Status | Code evidence |
|---|---|---|---|---|
| G-1 | New panes must emit `+ - \|` under `--ascii`, never `?` borders | 25 | KEEP (guard) | [CODE-VERIFIED] `terminal.py:30-34` GLYPHS has only `selected`, `truncate`, `hrule`; `terminal.py:133-135` `ascii_safe` maps any non-ASCII to `?`; `render.py:62-80`/`clip` call `ascii_safe`. So heavy and rounded border characters in hand-built strings would render as `?` in ASCII mode unless added to GLYPHS. [CODE-CONTRADICTED] The earlier claim that `terminal.py:123` `safe_box=policy.ascii` covers Rich `Box` objects is false: `safe_box` only matters on legacy Windows, and Rich swaps in `box.ASCII` only when the output is not UTF-8 (`rich/box.py:79-83`; Rich 15.0.0 probe: `Panel("hi")` prints identical rounded Unicode borders with `safe_box` True and False, and `box=rich.box.ASCII` prints `+---+`). `test_terminal.py:114-116` pins only the attribute value. So a Rich frame under `--ascii` needs an explicit `box=rich.box.ASCII` as well, or hand-built `+ - \|` glyphs; see `01-render-view-terminal-pipeline.md` lines 204 and 229 and the re-run probe in `03-tests-goldens-fixtures.md` section 6 rule 3 |
| G-2 | Theme must stay distinct at the real colour depth; NO_COLOR stays `None` | none (spec silent: grep for truecolor/24-bit/256/colour depth in the spec folder finds only RR 70, acceptance-tests.md:17, 31 (T26), stack.md:13, 25) | KEEP (guard); depth/detection is an open design item | [CODE-VERIFIED] `terminal.py:121`; no COLORTERM or capability detection exists in `terminal.py` |
| AD-1 | "8 owners / 80 sessions / 80 mapped trees" header not built | 20 | Accepted, keep | 160/ledger.txt:3 shows the real COUNTS strip |
| AD-2 | SIGNALS bars, SETTLED/UNKNOWN/STALE tiles | 20, 93 | Accepted, keep (no bars) | `view.py:947-949` tokens `SETTLED unavailable (no source)` etc. |
| AD-3 | Two-line register rows, prose lifecycle | 30, 31 | Accepted, keep | `render.py:155-230` one row per worker, raw fields |
| AD-4 | Requester/owner/Affected/scope count | 57 (AC-7 note), 91 | Accepted, keep | `view.py:87-90` DESK_WORKTREE_NOTE; `view.py:814-874` shows one linked session only |
| AD-5 | Different key map; no `tab pane`; ledger stays under desk | 13, 21, 39 | Accepted, keep | `view.py:78-83,105` |
| AD-6 | No `workerState` column at 80 (optional at 116) | 33 | Accepted, keep | `render.py:193-229` |
| AD-7 | 80-col "Questions stay until explicit resolution." and forced focused card not adopted | 42, 61 | Accepted; but RR 61 itself lists that sentence as an invariant line, see Stale Documentation | RR 61 vs RR 42 |
| OPEN-1 | M-07 severity (Astra High vs Opus Medium) | | Open; handled as Medium (gated) | |
| OPEN-2 | M-14 severity (Opus Medium vs Astra Low) | | Open; handled as Medium (gated) | |
| OPEN-3 | M-13 severity/scope | | Open; handled as Medium (gated) | |
| O-1 | Adopt two-column layouts at 160/116, reversing the stacked choice | 43, 57 | OWNER DECISION pending (recommended yes); conflicts: M-03, M-04, and partly M-06, M-14 | RR 43 text: "One stacked block at every width of 80 columns or more ... the two-column layout above stays design reference" |

Key Takeaways
- Findings that conflict with the current spec text (need O-1 or a spec edit): M-03, M-04 (O-1); M-13 (RR 17), M-14 (RR 41, 61).
- Findings that the spec already requires and the code violates: M-08 (RR 70), M-11 (RR 21 "no key is cut" per `_help_lines` intent).
- Guards to keep: RR 20/32 (gap notice, COUNTS wording), 31 (verbatim kind), 47/49 (verbatim count and disclosure), 25 (ASCII), 50 (glyph and age format), 57 (desk line order), AC-9 T26-T28 (no SGR in NO_COLOR, no ESC in exports, no blink).
- The dominant code obstacle is architectural: `View` and `screen_lines` are string-only (view.py:303-339; render.py:390-521). Styling, tiles and panes all need role metadata or a second render path.

## 6. Mockup versus current output, per screen and width

Mockup file -> current file pairing is the one stated in `render_current.py` docstring (lines 6-9): ledger -> signal-bridge, questions -> attention-ledger, desk -> decision-desk. Data differs (mockup shows 17 of 80 sessions and three human questions with requester/Affected; current shows live-shaped synthetic data) so only structural differences are listed.

| Screen / width | Mockup (structure) | Current (structure) | Differences |
|---|---|---|---|
| ledger 160 | Title `◈ SIGNAL BRIDGE` + READ ONLY badge; HUMAN QUESTION amber pane; OBSERVATION WINDOW pane (freshness per source); SESSION REGISTER pane (two-line rows); SIGNALS tiles with bars; keys + caveat footer under a rule | 4 plain header lines, gap notice, `26 historical hidden (h)`, title line, 12-column table with header + rule rows (160/ledger.txt:8-9), `39/54 shown  +15 more`, one footer line | no colour, no panes, no tiles; table has headings (mockup rows are two-line); one footer line vs rule + two lines; mockup SIGNALS/owner lines are AD-1/AD-2 |
| ledger 116 | Heavy HUMAN QUESTION full width; SESSION REGISTER 78 + OBSERVATION WINDOW 34 side by side; caption line; no SIGNALS | 5 header lines, gap notice, 4-column line form without a heading (116/ledger.txt:8), footer wraps to two lines | no heading (M-10), no panes, wide blank band (M-17) |
| ledger 80 | Heavy HUMAN QUESTION; one-line `RUN 48  SETTLED 24 ...`; SELECTED FLEET SLICE pane; whole key hint line | header wraps (`as of 12:00:00` alone on line 2), counts cut `runs seen>`, 3-column rows no heading, key list cut `e exp>` | M-10, M-11, M-13, M-16 |
| questions 160 | OPEN HUMAN QUESTIONS heavy 114-wide pane with bold question rows separated by slate rules; SEEN IS NOT RESOLVED tile (cyan frame, amber block digit); RETAIN CONTEXT slate pane | one stacked block: title, run line, state, disclosure, counts, caveat, 3 rows, retention line, then worker table (160/questions.txt:5-23) | M-03, M-05, M-07, M-14 |
| questions 116 | Same as 160 with left pane 70 wide | disclosure wraps to two lines (116/questions.txt:8-9); footer pair split `n/p` / `question` (:23-24) | M-03, M-07, M-15 |
| questions 80 | Focused question as three plain lines, SELECTED SIGNALS pane listing Q01-Q03 with invariant sentences | stacked block, 2-line disclosure, counts cut `cost un>` | M-07, M-14, M-16, AD-7 |
| desk 160 | HUMAN QUESTION heavy 76 + OTHER OBSERVED QUESTIONS 76 beside AFFECTED SESSION EVIDENCE 80 | `DECISION DESK` bare block under the list; 9 `label: value` lines; worker table repeated below (160/desk.txt:28-36) | M-04, M-12, M-18 |
| desk 116 | HUMAN QUESTION full width over AFFECTED SESSIONS 66 + OTHER OBSERVED QUESTIONS 46 | same stacked block, note wraps at 116 | M-04, M-12 |
| desk 80 | Three stacked 78-wide panes | stacked block; note wraps to two lines (80/desk.txt:27-28) | M-04, M-12 |

Key Takeaways
- Every screen differs from its mockup in chrome (panes, colour, badge) rather than in data meaning; the data differences are AD-1 to AD-7.
- The only places where the current text is lossy relative to spec (not just mockup) are M-08 (muting), M-10 (no heading), M-11 (cut key list) and the cut tokens at 80 (M-16).

## 7. How render_current.py produces the current/ outputs (read only, not run)

[CODE-VERIFIED by reading `inputs/tools/render_current.py`, 94 lines]
- Run line (docstring lines 3-4): `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python .dev/issues/409/visual-parity/inputs/tools/render_current.py` from the repo root. Output dir `OUT = .dev/issues/409/visual-parity/inputs/current` (line 37), terminal height fixed at 50 (`HEIGHT = 50`, line 38), widths 160/116/80 (line 39).
- It imports `LiveSource`, `Collector`, `FixtureSource`, `render`, `screen_lines`, `make_console`, `resolve_policy`, `build_view`, `Session`, `apply_key`, `Key` from `superclaude.cli.observe` and test helpers from `tests.observe.conftest` (lines 19-35), so the screens are produced by the production renderer with test-fixture data. Data is synthetic.
- `ledger`: `build_view(Collector(FixtureSource("base"), clock).run_once(), Session(), clock)` (line 80): fixture mode, 80 workers, questions off.
- `questions`: `questions_result(clock)` (lines 47-65) builds 6 worker rows (`w-001`..`w-006`, worktrees `wt-1`..`wt-6`) and three question messages (`QUESTIONS`, lines 40-44: `w-001 Choose schema compatibility policy`, `w-002 Confirm deployment window`, `w-003 Name the release reviewer`) through `FakeRunner`; collector runs with `questions=True, link=True` and `run_id=QRUN` (lines 58-64). View built with a default `Session()` (nothing selected, line 83).
- `desk`: same result, then `apply_key(session, Key("text", "n"), plain, clock)` selects the first question (line 84) and the view is rebuilt (line 85).
- `emit()` (lines 68-75): `resolve_policy({}, "utf-8", {"ascii": False}, width, HEIGHT)` (empty env so colour is not disabled by NO_COLOR, UTF-8, not ASCII); writes `<name>.txt` from `screen_lines(view, policy)` and `ansi-<name>.txt` from a recording Console (`make_console(policy, file=io.StringIO(), record=True)`, `console.export_text(styles=True)`). Because `render()` applies no styles, the ansi files contain no ESC bytes (verified: no `\x1b` match in the nine files).
- Not captured: NO_COLOR, `--ascii`, live observer, error states, any hash-bearing question (QUESTIONS has no plan ask), heights other than 50. The ledger is fixture data, the other two are `live`-mode data; this explains why 160/ledger.txt:1 reads `mode=fixture` and 160/questions.txt:1 `mode=live`.

## 8. Q7 context: 64-character hex hash in the 80-column Decision Desk frame

Source: `pr-591-comment.md` consideration 8 (line 18): a plan ask carries a plan path, a file list and a 64-character hex hash; "add one fixture question with such a token and check the 80-column Decision Desk frame wraps or cuts it cleanly". Doc claims about the content of plan asks are [UNVERIFIED] (the file itself lists them under UNVERIFIED, lines 26-31); no code in `src/superclaude/cli/observe` mentions hash handling (rg `hash|[0-9a-f]{64}` found no match) and `render_current.py` has no such fixture.

What the code does with such a token (derived by reading `render.py`, not run):
- Desk question text is wrapped by `wrap()` (render.py:62-80): it breaks at the last space inside the width; a token with no space is hard-cut at `width` cells (render.py:76-78) and the cut continues on the next line. The text is limited to `DESK_TEXT_LINES = 4` lines (view.py:99; render.py:339-346), the fourth being cut with `...`.
- At 80 columns a bare desk line has 80 cells, so a 64-character token fits on one line. Inside a mockup-style pane the usable width is 74 cells (78-wide frame, `┃ ` and ` ┃`, from `mockups/80/decision-desk.txt:6-11`), so a 64-character token still fits on its own line; a label such as `plan hash (sha256): ` (20 cells) plus 64 would not fit on one line and `wrap` would move the token to the next line, where it still fits. The real risks are therefore (1) the 4-line cap cutting the hash when path + file list consume the lines, and (2) a pane implementation that clips instead of wrapping. [derived; not measured]
- The inspector/export paths show the full text untruncated (RR 26) but the Decision Desk does not.

Key Takeaways
- Q7 is not a width problem (64 < 74) but a line-budget and wrap-versus-clip problem; the fix needs a fixture with a plan-style ask.
- Open question for the owner: should the desk show the whole hash (4-line cap) or a cut hash with a visible mark, given a person cannot verify a truncated hash.

## Gaps and Questions

[UNVERIFIED]
1. The "153 cells" figure for the full ledger (FIND M-06, attributed to RR line 30) is not on RR line 30 and I could not reproduce it. The code's own full-class minimum is 160: `render.py:160-165` gives 2 + (12+12+14+14+12+16+22+12 = 114) + flags 12 + 10 separators + id 22 = 160 (= `FULL_WIDTH`, terminal.py:23). The conclusion (three-column grid would not hold the full ledger) stands either way.
2. How a selected row or selected question should look in the mockups: no selected-row styling exists in any of the nine mockups (section 2). M-18's fix direction (bold attention colour) has no mockup evidence.
3. Whether the mockup PNG background colour (dark navy) is part of the design: the `.ansi` files set no background (no 48 code), the PNGs show one. Not decided by any document.
4. Content of plan-approval asks (path, file list, 64-char hash) and that they are stored as `question` rows (`pr-591-comment.md` lines 26-31, UNVERIFIED in the source itself).
5. Terminal colour capability at run time: nothing in `terminal.py` detects it; the 16-colour mapping in section 3 is computed with Rich's downgrade, not observed on a terminal.
6. The mockup palette's behaviour on light terminal backgrounds is not addressed by any file I read.

[CODE-CONTRADICTED / drift]
7. FIND M-10 says `render()` prints a header only when `width_class == "full"`; the condition lives in `screen_lines()` (render.py:497-498), `render()` only wraps lines (render.py:524-531). Behaviour confirmed, location wrong.
8. RR line 61 requires the 80-column invariant lines "Questions stay until explicit resolution." and "No reply observed is not delivery failure."; the current 80-column output (80/questions.txt) has neither, and FIND AD-7 rejects the first as untruthful against RR 42. The spec is therefore self-contradictory (RR 61 vs RR 42) until reworded.

Questions for the owner or the next phase
- O-1 (two columns at 160 and 116): is it approved? It decides Q1 and the spec edits to RR 43 and 57.
- Which colour depths must the theme target (16 only, or truecolor with 16-colour fallback) and how is capability detected (G-2)? At 16 colours muted, green, red and violet collapse into one colour in the mockup palette (section 3), so state colours need explicit 16-colour roles.
- Should RETAIN CONTEXT be built (changes RR 41 and 61), and with which severity (OPEN-2)?
- Should the Decision Desk show a plan hash in full (Q7)?

## Stale Documentation Found

- [STALE DOC] `rendering-rules.md` line 41 says RETAIN CONTEXT is "not built in R2" and line 43 says the two-column layout "stays design reference"; both describe the current R2/R3 state and become stale if O-1 and M-14 are adopted. They match current code today (view.py/render.py have no such pane).
- [STALE DOC] `rendering-rules.md` line 61 (80 columns) says "RETAIN CONTEXT is reachable only through the inspector" and lists two invariant lines; the current output (80/questions.txt) shows neither and RETAIN CONTEXT does not exist in the inspector code path either as a pane (the inspector shows field lists, render.py:255-287). The invariant lines conflict with line 42's retention wording (AD-7).
- [STALE DOC] `rendering-rules.md` lines 38 and the mockups: the mockup title `OPEN HUMAN QUESTIONS` is retired by RR 38; code uses `COORDINATOR QUESTIONS` (view.py:53). The mockups at 160 and 116 are stale on this title.
- [STALE DOC] `rendering-rules.md` line 59 itself says some `observed open: n` wording elsewhere in the file is superseded "until the spec owner re-words them"; the file is partly stale by its own admission.
- [STALE DOC] `render_current.py` docstring (lines 6-9) calls the captured `ansi-*.txt` files "empty of escapes today"; confirmed true now (no `\x1b` in the nine files) and will be false after the fix lands. Treat the `current/` captures as a pre-fix baseline.
- Minor: `FINDINGS.md` M-10 cites `render()` for what `screen_lines()` does (drift, see Gap 7). All other line citations in FINDINGS.md matched.

## Summary

All 18 merged findings, the two guards, seven accepted divergences, three open items and O-1 were checked against `rendering-rules.md`, the nine current captures and the code in `render.py`, `view.py` and `terminal.py`; every quoted current-output line and every RR line citation matched, with one location drift (M-10) and one unreproducible figure (153 cells). The mockups are 24-bit foreground-only dark-theme designs with eight colour roles plus bold, while the code caps Rich at 16 colours (terminal.py:121) and styles nothing (render.py:528); in Rich's 16-colour downgrade the muted, green, red and violet roles collapse to one colour, so state colour cannot carry meaning alone. Panes, two-column layouts, the count tile and colour all depend on one architectural change: `View` and `screen_lines` are string-only, so role metadata or a pane renderer is needed, plus box glyphs in `GLYPHS` for ASCII mode (G-1). O-1 (reversing RR 43 and 57) and the RR 17, 41 and 61 edits are the spec changes required; Q7 (64-character hash) is a line-budget and wrap-versus-clip issue at 80 columns, not a width problem.
