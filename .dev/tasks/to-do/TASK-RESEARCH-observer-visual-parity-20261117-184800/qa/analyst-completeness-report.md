# Research Completeness Verification

**Topic:** observer visual-parity redesign (issue #606)
**Date:** 2026-11-17
**Status:** Complete
**Depth tier:** Standard
**Files analyzed:** 5 codebase research files (01 to 05); web files out of scope

---

Method: read research-notes.md and all five research files in full; then spot-checked cited claims against source, tests, mockups and the installed tools (Rich 15.0.0 probes, `superclaude observe --once --width {160,116,80} --fixture base`, golden JSON loads, test and spec line reads). Per I16 each finding is graded BLOCKING or MINOR (notes). Findings are numbered F-01 onward and defined in the Findings Register at the end.

## 1. Coverage Audit (checklist item 1)

| Scope item (EXISTING_FILES) | Covered by | Status |
|---|---|---|
| `render.py` (531 lines) | 01 (sections 3-4, 8), 04 (section 5) | COVERED; line cites spot-checked (497, 528, 304-308, 359-387, 447-457, 155-230) all match |
| `view.py` | 01 (section 5), 02 (sections 5-6), 04 | COVERED; view.py:948, 64, 99, 761 literals match |
| `terminal.py` | 01 (sections 1, 7) | COVERED; read lines 18-137, all claims match |
| `commands.py` | 02 (sections 1-4, 8) | COVERED; 225-279 matches |
| `collector.py`, `export.py`, `questions.py`, `keys.py` | 02 (sections 5-7) | COVERED |
| `parse.py`, `adapter.py`, `sanitize.py` | 01 (sanitize), 02/03 (parse cites) | COVERED as context (not expected to change) |
| `tests/observe/` (28 py + 2 goldens) | 03 (sections 1-4, 6) | COVERED; 10 of 22 test modules classified only from names and docstrings (F-06) |
| `rendering-rules.md` | 04 (section 1), 01 (stale-doc list) | COVERED; RR 20, 25, 30, 41, 43, 61 spot-checked |
| `visual-parity/inputs/` (mockups, current, render_current.py) | 04 (sections 2-4, 6-7), 05 (section 4) | COVERED |
| `.dev/issues/409/attachments/` | 04 (PNG cites) | COVERED in effect: `cmp` shows the three attachment PNGs are byte-identical to `mockups/160/{signal-bridge,agent-focus-attention-ledger,decision-desk}.png` |
| `FINDINGS.md` | 04 (section 5), 01 (section 8.1) | COVERED |
| Zellij config, themes, layouts, 0.44.2 CLI | 05 (section 1) | COVERED, help-text only; partial reads (F-07) |
| `pr-591-comment.md` | 03 (5), 04 (8) | COVERED; line 18 matches |

Questions and findings coverage:

| Item | Evidence behind it | Status |
|---|---|---|
| Q1 composition in line pipeline | 01 section 8.2 (7 candidates with width arithmetic), 04 section 4 (pane geometry) | COVERED |
| Q2 tests and goldens per phase | 03 section 6 (phase table P0-P5), section 4 | COVERED; P2 literal list incomplete (F-06) |
| Q3 render harness and rubric | 05 sections 2, 4-6 | PARTIAL; rubric not drafted, PNG route unverified; web-02 and synthesis close this (not blocking) |
| Q4 ANSI colour depth | 01 section 7, 04 section 3, 02 section 2 | COVERED; 01 vs 04 inconsistency (F-01) |
| Q5 live vs one-shot | 02 sections 1-3, 8; 03 section 3 | COVERED; the two files recommend different one-shot routes (F-03) |
| Q6 Zellij go or no-go | 05 sections 1.6, 7 | PARTIAL (no session run); web-02 closes it (not blocking) |
| Q7 64-hex at 80 columns | 01 section 4.9, 03 section 5, 04 section 8 | COVERED with measurements; three files agree |
| M-01 to M-18 | 04 section 5 (all 18, with spec line, code location, severity); 01 section 8.1 (all 18 plus G-1, G-2) | COVERED, 18 of 18 |
| G-1, G-2, AD-1 to AD-7, OPEN-1 to OPEN-3, O-1 | 04 section 5 (second table) | COVERED |

## 2. Evidence Quality (checklist item 2)

Every research file cites file:line, function names and measured probe output throughout. I did not count every claim; I re-verified the following independently and found 0 mismatches of fact (only the line-range and wording notes in F-09 and F-10).

| Research file | Claims I re-verified | Mismatches | Quality rating |
|---|---|---|---|
| 01 render/view/terminal | terminal.py:121 `"standard"`; GLYPHS has 3 names (30-34); 4 width classes (63-70); `safe_box=True` Panel still draws `╭─╮` (probe); render.py:528 unstyled `Text`; `_columns` arithmetic (160 table = 160 cells; 116 id = 52; 80 id = 38); header gate 497; `_help_lines` 304-308; `_panel_lines` order 368-387; `spare` formula 447-457; live screens at 160/116/80 (40 lines each, heading only at 160, `runs seen>` and wrapped `as of` at 80); golden_questions row counts 24/24/25 and max widths 160/113/80; view.py:948, 64, 99, 761 | 0 | Strong |
| 02 live/commands/export | commands.py:238-245 and 257-279 (`export_text()` without styles; `LiveScreen.draw`); `export_text(styles=True)` under NO_COLOR returns ANSI (probe: `'\x1b[1;31mhello\x1b[0m\n'` while the stream is plain); `TTY_COMPATIBLE` and `FORCE_COLOR` exist in Rich 15 `console.py` (955, 964); gate tests test_commands.py:747-772; `"\x1b" not in` at test_commands.py:99, 105, 121 | 0 | Strong |
| 03 tests/goldens | test_render.py:396-404 (renderables count and source regex), 250-259, 958-967; test_terminal.py:109, 115, 185-186; golden key set (14 per variant, 5 variants), no ESC in golden; no test references `LiveScreen` (grep: no match); test counts per module (36, 19, 13, 60, 54 `def test_` in commands, export, terminal, view, render) | 0 | Strong |
| 04 spec/mockups/findings | Rich downgrade table reproduced exactly (base 15, muted 7, slate 8, amber 11, cyan 14, green 7, red 7, violet 7); mockup frame heights (48 at 160, 42 at 116 and 80); no `▸ ► › »` in any of the nine mockup `.txt` (04 had checked only the 160 files); no 256-colour, dim, italic, underline or reverse codes in the nine `.ansi`; RR 20, 25, 30, 41, 43, 61 text; FINDINGS "153 cells" at line 64 and the `render()` wording at line 91; M-01..M-18, G-1, G-2, OPEN-1..3, O-1 all present | 0 | Strong |
| 05 Zellij/harness | `zellij 0.44.2` and `zellij setup --check` "Well defined"; node present; unzip, chromium, convert absent; render_current.py `HEIGHT = 50`, `main()` at import time (line 93), `export_text(styles=True)` at emit; 0 ESC bytes in `current/160/ansi-ledger.txt` vs 48 lines in the mockup `.ansi`; 160 PNG sizes 79851, 91078, 171981 | 0 | Adequate (Zellij evidence is help text only, F-07) |

## 3. Documentation Staleness (checklist item 3)

| Claim | Source doc | Verification tag | Status |
|---|---|---|---|
| `FROZEN unavailable` vs code `POLICY FROZEN unavailable` | rendering-rules.md:20 | 01: CODE-CONTRADICTED (view.py:948 confirmed by me) | OK |
| Two-column layout "stays design reference"; RETAIN CONTEXT "not built in R2" | rendering-rules.md:41, 43 | 01 and 04: STALE DOC, match current code | OK |
| RR 61 lists invariant lines and says RETAIN CONTEXT is reachable only through the inspector | rendering-rules.md:61 | 04: STALE DOC and self-contradiction with RR 42 (text confirmed at RR 61) | OK |
| "153 cells" for the full ledger | FINDINGS.md:64 (cites RR 30) | 01 and 04: UNVERIFIED (RR 30 has no number; code gives 160) | OK |
| M-10 says `render()` prints the header | FINDINGS.md:91 | 01 and 04: misattribution, condition is at `screen_lines` render.py:497 (confirmed) | OK |
| Mockup title `OPEN HUMAN QUESTIONS` | mockups 160/116 | 04: STALE DOC (code uses `COORDINATOR QUESTIONS`, view.py:53 confirmed) | OK |
| Commit c69ce4b3a for the golden | ponytail-review tests-and-fixtures.md:51 | 03: STALE DOC (git log prints cd8736199) | OK |
| `QUESTION_GATE_PASSED = False` on master | orchestrator-tui-alignment review | 03: STALE DOC (code is True, commands.py:67) | OK |
| render_current.py "empty of escapes today" | render_current.py:8-9 | 04, 05: true today, stale after styling | OK |
| Plan asks carry path, file list, 64-hex hash | pr-591-comment.md:18, 26-31 | 04: UNVERIFIED (the file itself lists it under UNVERIFIED) | OK |
| Task prompt says width classes full/line/narrow | task prompt (g) | 01: CODE-CONTRADICTED (4 classes, confirmed terminal.py:63-70) | OK |

No doc-sourced claim is untagged and no `[CODE-CONTRADICTED]` claim is reported as current fact. Zero FLAGs.

## 4. Completeness (checklist item 4)

| Research file | Status | Summary | Gaps section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-render-view-terminal-pipeline.md | Complete | Y | Y (13 items) | Y (per section) | Complete |
| 02-live-screen-commands-export.md | Complete | Y | Y | Y (per section) | Complete; header "Scope: the files listed above" has no list (F-10) |
| 03-tests-goldens-fixtures.md | Complete | Y | Y (9 items) | Y (per section) | Complete; same dangling Scope line (F-10) |
| 04-spec-mockups-and-findings.md | Complete | Y | Y | Y (per section) | Complete; same dangling Scope line (F-10) |
| 05-zellij-and-render-harness-environment.md | Complete | Y | Y | Y (per section) | Complete; same dangling Scope line (F-10) |

All five files meet the structural bar. The Key Takeaways are per section rather than one closing block, which still satisfies the check.

## 5. Cross-Reference Check (checklist item 5)

| Cross-cutting concern | Files | Cross-referenced? |
|---|---|---|
| `export_text()` drops styles; `styles=True` bypasses NO_COLOR and the 16-colour downgrade | 01 sec 3, 02 sec 2, 03 sec 3, 05 sec 4 | 01 and 03 agree with 02 on the default call. The harness consequence is missing: render_current.py (04 sec 7, 05 sec 4) uses `export_text(styles=True)`, so its ANSI captures would not show the `standard` downgrade or NO_COLOR. 05 sec 5 recommends ANSI assertions without that caveat. See F-02 |
| Colour depth and role collapse | 01 sec 7, 04 sec 3, 02 sec 2 | Partial. 04 measures the collapse, 01 infers a different one. See F-01 |
| T47 and T64 golden re-baselining and the 15 `printed_*` values | 01 sec 6, 03 sec 4 and 6 | Yes, consistent (15 `printed_*`, 30 `lines_*`) |
| 64-hex token | 01 sec 4.9, 03 sec 5c, 04 sec 8 | Yes, consistent; 03 and 01 measured whole-line wrap, 04 predicted by reading (consistent) |
| Source guards (render.py regex; terminal.py-only `Console(` and `NO_COLOR`) | 01 sec 3, 03 sec 1 and 6 | Yes (03 adds the test_terminal.py:181-198 scan that 01 omits) |
| `len(renderables) == len(screen_lines)` (test_render.py:399) | 03 only | Not echoed in 01 sec 8.2 option 4 (Rich `Panel`/`Layout`), which does list the regex guard but not this one. Minor; synthesis should join them (covered by F-03 note) |
| Gate constants pinned by regex | 02 sec 4, 03 sec 4d | Yes, consistent (line ranges differ, F-09) |
| M-09 only exists at full width and in the desk | 01 sec 8.1, 04 sec 5 | Yes, consistent |
| Harness frame height vs mockup frame height | 04 sec 4 (48/42), 05 sec 4 (`HEIGHT = 50`) | No file compares them. See F-04 |

## 6. Contradiction Detection (checklist item 6)

No factual contradiction between files about the same code fact. Surfaced items, none resolved silently:

1. Colour roles at 16 colours. 01 sec 7 (labelled inference): "slate and muted both land on greys ... these two roles can collapse"; amber has "no standard colour (nearest yellow/bright_red)". 04 sec 3 (measured, and reproduced by me): slate = 8, muted = 7 (distinct), amber = 11 (bright yellow), and muted, green, red, violet all = 7. The measured table supersedes the inference; 01 also misses the larger problem (state colours collapse). F-01.
2. One-shot width path. 03 sec 3 and sec 6 (P1 row) keep `export_text()` unstyled so `"\x1b" not in out` at test_commands.py:121 still holds ("keep it"). 02 sec 2 and sec 8 recommend a styled route through `console.file.getvalue()` and say :121 "would need changing". Both are internally correct and conditional on the same unmade decision (Q5). F-03.
3. Spec self-contradiction. RR 61 lists invariant lines ("Questions stay until explicit resolution.") that RR 42 and AD-7 reject (04 gap 8). Already surfaced by 04; I confirmed the RR 61 text. Carried into the gaps below.
4. Task prompt vs code: width classes full/line/narrow in the prompt, full/line/short/narrow in code. Surfaced by 01; confirmed at terminal.py:63-70.

## 7. Compiled Gaps (checklist item 7)

Severity scale: Critical (blocks synthesis), Important (affects quality or needs a decision in the report), Minor (note only).

### Critical Gaps (block synthesis)
- None. Every claim the synthesis needs about current behaviour has a source read or a probe behind it, and my spot-checks found no factual error.

### Important Gaps (affect quality; the synthesis must carry them as decisions or caveats)
- G-A. Golden re-baselining (T47, `test_render.py:611-624`; T64): any questions-off or link-off screen change breaks the release-1 meaning of `golden_release1_surface.json`; needs an owner decision to re-baseline or a gated look. Sources: 01 gap 7, 03 gap 4. Decision item, not a research gap.
- G-B. Colour depth and detection (Q4 / G-2): fixed `"standard"`; at 16 colours the mockup roles muted, green, red and violet collapse to index 7. Needs per-depth explicit roles or text carrying state. Sources: 01 gap 6, 04 sec 3. Carry the 04 table, not the 01 inference (F-01).
- G-C. Styled capture route (Q5): `export_text()` plain vs `file.getvalue()` vs `styles=True` (bypasses NO_COLOR). Sources: 01 gap 5, 02 gaps, 03 gap 5. Tension F-03; harness consequence F-02.
- G-D. O-1 (two columns at 160 and 116) and the spec edits to RR 17, 41, 43, 57, 61 (04 sec 5). Owner decision; recommended yes.
- G-E. Hard-wrap rule for tokens wider than the inner frame width (no marker, mid-word cut of long paths) and whether a hash may be shown cut. Sources: 01 gap 13, 03 sec 5c, 04 sec 8.
- G-F. No automated test covers the real `LiveScreen` (commands.py:257-279); only text and bytes are pinned. Source: 03 gap 6. The render gate has to supply the visual check.
- G-G. Frame-heavy layout at small heights is unmeasured; no final `lines[:height]` clamp exists. Sources: 01 gap 8, F-04, F-05.
- G-H. Spec contradiction RR 61 vs RR 42 / AD-7. Source: 04 gap 8.

### Minor Gaps (notes)
- "153 cells" unverifiable (01 gap 1, 04 gap 1); code says 160.
- Selected-row look has no mockup evidence (04 gap 2; I confirmed none of the nine `.txt` mockups draws a selected marker). F-08.
- Mockup PNG background (dark navy) vs `.ansi` with no background code (04 gap 3).
- Light-terminal behaviour of the palette not addressed (04 gap 6).
- Zellij: floating panes, `dump-screen` fidelity, command panes in layouts, theme read-back, CI presence, all need a live session (05 gaps). F-07.
- Pillow, cairosvg, pyte, Playwright browser install feasibility and cairo system library untested (05 gaps); web-02 scope.
- East-Asian-ambiguous glyph width in the owner's terminals (01 gap 9); which `+1` is which in `spare` (01 gap 10); fixtures `injection` and `long-identifiers` under styling (01 gap 11).
- Windows `legacy_windows` left to Rich; `--once --width` is cross-platform (02 gaps).
- Test modules classified from docstrings only; `test_view.py` literals not enumerated (03 gaps 2-3). F-06.

## 8. Depth Assessment (checklist item 8)

**Expected depth:** Standard (file-level understanding with key function documentation).
**Actual depth achieved:** Above Standard for code. The code files carry function-level and line-level traces, width arithmetic for all three layouts, measured screens at 160/116/80, probe-verified Rich behaviour (colour system, `safe_box`, `export_text`), a per-finding change map (M-01 to M-18, G-1, G-2), a seven-option insertion analysis, a phase-by-phase test and golden impact table and a baseline run (766 passed). The environment file is at Standard depth.
**Missing depth elements:** none that block synthesis. Open items are the ones listed under F-02 to F-07 below.

## Findings Register

Grading follows I16: BLOCKING means synthesis cannot proceed or a claim would mislead it; MINOR is a note for the synthesis or a later phase. No finding is blocking.

| ID | Grade | File(s) | Finding | Evidence | Suggested action (for the synthesis or a later phase; no research file was changed) |
|---|---|---|---|---|---|
| F-01 | MINOR | 01 sec 7 vs 04 sec 3 | 01's inference that slate and muted collapse, and that amber has no standard colour, is wrong. Measured: slate 8, muted 7, amber 11, and green, red, violet, muted all 7. 01 misses the state-colour collapse. | My probe with Rich 15.0.0 `Color.downgrade(ColorSystem.STANDARD)` reproduces 04's table exactly | Synthesis uses the 04 table and drops the 01 inference |
| F-02 | MINOR | 04 sec 7, 05 sec 4-5 vs 02 sec 2 | `render_current.py` emits ANSI with `export_text(styles=True)`, which ignores NO_COLOR and the `standard` downgrade. A Phase 0 harness built on it would show truecolor that a 16-colour terminal never shows. Not noted in 05's harness table. | My probe: with `color_system=None, no_color=True` the stream is plain and `export_text(styles=True)` returns `'\x1b[1;31mhello\x1b[0m\n'`; render_current.py emit uses `styles=True` (05 sec 4) | Phase 0 harness should capture `console.file.getvalue()` through `make_console` |
| F-03 | MINOR | 02 sec 2, 8 vs 03 sec 3, 6 | Two different one-shot routes recommended (styled `getvalue()` vs keep plain `export_text()`); the latter keeps test_commands.py:121 unchanged, the former changes it. Not flagged as one open decision. | test_commands.py:121 `"\x1b" not in out`; commands.py:242 | Present as the Q5 decision in the options section |
| F-04 | MINOR | 04 sec 4, 05 sec 4 | Harness height 50 (`render_current.py:38`) vs mockup frames 48 rows (160) and 42 rows (116, 80). The render gate compares like with like only if the heights match; nobody noted it. | `wc -l` of the nine mockup `.txt`: 48, 42, 42; HEIGHT = 50 | Set harness height per width to the mockup height, or record the mismatch as accepted |
| F-05 | MINOR | 01 gap 8, 03 | Frame-heavy behaviour at 24 rows and at `MIN_ROWS = 8` is unmeasured; the questions-on desk screen was run only in 03 (height 70). | 01 gap 8; render.py:499-502 forces one ledger row, no final clamp | Add heights 24 and 12 to the render-gate matrix |
| F-06 | MINOR | 03 gaps 2-3 | `test_view.py` (60 tests, 1383 lines) and ten modules were classified from names and docstrings, so the literal-by-literal P2 break list is incomplete. | 03 gaps 2-3 | Enumerate at plan time; not needed for the options decision |
| F-07 | MINOR | 05 sec 1.6, gaps | Zellij evidence is help text only; `zellij action --help` was read to line 120 and the theme and layout files to about two thirds. Q6 is allowed to stay partial at Gate 1. | 05 gaps | web-02 and the synthesis close it; keep "no-go as harness dependency" worded as provisional |
| F-08 | MINOR | 04 gap 2 | The selected row and selected question have no mockup reference, so M-18 has no visual target. 04 checked only the 160 files; I checked all nine `.txt` (no `▸ ► › »` found). | grep count 0 over `mockups/**/*.txt` | Rubric should score M-18 against the spec text (RR 50), not the mockup |
| F-09 | MINOR | 03 sec 4d | Gate test line ranges given as 747-760 and 762-777; the functions end at 756 and 772 (02 has them right). | test_commands.py:747-756, 762-772 | Cite 02's ranges |
| F-10 | MINOR | 02, 03, 04, 05 headers | "Scope: the files listed above" points at nothing; the scope list was not carried into the file. | file headers | Cosmetic; no action needed for synthesis |

## Verdict: PASS (0 blocking, 10 minor)

## Summary

| Measure | Value |
|---|---|
| Research files analyzed | 5 (01 to 05) |
| Files with Status: Complete, Summary, Gaps and Key Takeaways | 5 of 5 |
| M-01 to M-18 covered with research evidence | 18 of 18 |
| Q1, Q2, Q4, Q5, Q7 covered | 5 of 7 (Q3 and Q6 partial by design; web research closes them) |
| Factual mismatches found in spot-checks | 0 |
| Blocking findings | 0 |
| Minor findings | 10 (F-01 to F-10) |
| Critical gaps | 0 |
| Important gaps (decisions or caveats for the synthesis) | 8 (G-A to G-H) |
| Verdict | PASS |

Every research claim I re-checked held, including the quantitative ones (width arithmetic, golden row counts, Rich colour downgrade, NO_COLOR behaviour, live screens at three widths). The ten minor findings are inconsistencies or omissions between files, not errors in any one file. The two worth carrying into the synthesis are F-01 (use 04's colour table, not 01's inference) and F-02 (the harness must capture through `make_console` output, not `export_text(styles=True)`). No research file was modified.
