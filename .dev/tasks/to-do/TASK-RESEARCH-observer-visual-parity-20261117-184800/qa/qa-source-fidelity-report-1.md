## Source-Document Fidelity Report

**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md (1918 lines)
**Source files checked:** 15 assigned source files totalling 7,415 lines (render.py 531, view.py 1204, terminal.py 160, sanitize.py 48, parse.py 835, adapter.py 512, test_render.py 1022, test_terminal.py 198, test_view.py 1383, golden_release1_surface.json 545, golden_questions_linkoff.json 158, test_linkoff_screen_reference.py 75, release1_surface.py 62, record_golden.py 385, record_golden_questions.py 297), plus the design inputs at widths 160 and 116 (18 mockup files, 12 current-state files; 80-column files touched incidentally). Read depth is stated under "Coverage and limits".
**Date:** 2026-11-17
**Status:** Complete (see end of file)

### Checklist results

**1 Semantic coverage: PASS.** Every component named in the checklist has an accurate counterpart in the report: `screen_lines`/`render` (2.1 call-chain table), the Text-per-line pipeline (`render.py:528`), the header gate (`render.py:497`, mirrored `:439`), `_panel_lines`/`_desk_lines`/`_question_line`/`_inspector_lines`, `wrap`/`clip`/`_pad`/`_cell`, `counts_lines`, `_columns`, the terminal policy, `GLYPHS`, `ascii_safe`, `make_console`, the view constants (`DESK_TEXT_LINES`, `QUESTIONS_*`, `KEYS_LINE`) and the golden contents. Not covered, and acknowledged by the report itself: `adapter.py` (4.5 says "not read"; it is not a presentation surface) and a literal-by-literal pass over `test_view.py` (9.4 row 31).

**2 Detail preservation: PASS.** Function signatures, line numbers, constant values, width-class names and glyph values survive. Checked exactly: `MIN_WIDTH=80`, `MIN_ROWS=8`, `FULL_WIDTH=160`, `LINE_WIDTH=116` (terminal.py:21-24); four width classes (terminal.py:63-70); `color_system=None if no_color else "standard"` at terminal.py:121; GLYPHS `▸/@`, `>/>`, `─/-` (terminal.py:30-34); `DESK_TEXT_LINES = 4` (view.py:99); `ASK_CAP = 400` (parse.py:475, applied :503); full-table arithmetic 2+114+22+12+10 = 160 recomputed from `_columns` (render.py:159-192); `line` id width `min(width-64, 60)` recomputed (render.py:195).

**3 Phantom finding detection: PASS (no phantom found).** More than 40 specific claims were traced to source or reproduced; none was untraceable (see "Claims verified").

**4 Accuracy of code characterization: PASS with minor notes.** Data flow, the budget formula (`spare = height - (len(head)+len(tail)+base+footer_height+ledger_fixed+1+1+1+selected_note)`, render.py:447-457), `reserved`/`capacity` (:499-503), desk-first sizing (:458-471), the "no final clamp" claim and the `wrap`/`clip` behaviour all match the code. Minor citation and count drift is in the findings table.

**5 No aspirational claims: PASS.** Section 2 and the "Current State" cells of Section 4 describe only what exists. New names (`theme.py`, `Line`, `Span`, `_frame`, `_two_columns`, `count_figure`, `render_compare.py`, `golden_release1_records.json`) appear only in Section 8 under "Add" or "New" and in the 8.1 "after the plan" diagram. A grep of `src/superclaude/cli/observe` for `READ ONLY`, `mouse`, `blink`, `ZELLIJ`, `COLORTERM` found nothing on-screen or in policy code, which backs the report's absence claims (M-13, 3.7, 5.4.6).

### Claims verified (tool evidence)

| # | Report claim | Check | Result |
|---|---|---|---|
| 1 | 2.1: Rich 15 probe, `bold #ff8800` at standard / 256 / truecolor | Re-ran one process per depth (`uv run python -I -B`) | `\x1b[1;91mx`, `\x1b[1;38;5;208mx`, `\x1b[1;38;2;255;136;0mx` exactly as stated |
| 2 | 2.1 / 3.2: mockup palette at 16 colours: base 15, muted 7, slate 8, amber 11, cyan 14, green/red/violet 7; 256 indexes 189/145/60/214/80/115/210/147 | Recomputed with `rich.color.Color.downgrade` | All sixteen numbers match |
| 3 | 2.1: `safe_box` True/False print identical rounded borders; `export_text(styles=True)` keeps SGR under NO_COLOR | Re-ran probes | Both reproduce |
| 4 | 2.3: golden_release1 = 5 variants x 14 keys; `indent=1, sort_keys=True, ensure_ascii=False`, no trailing newline; no ESC | Loaded and re-serialised | Byte-equal; 14 keys each; 0 `u001b` in either golden |
| 5 | 2.3: link-off golden scenarios `five`/`long_subject`, 24/24/25 and 22/22/23 lines; `indent=1, ensure_ascii=False` + newline | Loaded and re-serialised | Match |
| 6 | 2.3: the two `record_golden*.py` scripts do not produce the goldens | Grepped both | They write `fixtures/golden-*.json` only |
| 7 | 2.3 / Q7: 222-char fixture; desk text lines 157+64 (160), 85+71+64 (116), 78+78+64 (80); hash whole on the last line | Rebuilt with `r3_rows`/`r3_screen`, height 70 | Identical numbers |
| 8 | 2.1 measured screens (`--once --width W --fixture base`): 40 lines each, footer 132 cells at 160, `shown 28/54`, `29/54`, `28/54`, `runs seen>` and `as of` alone at 80 | Ran the CLI at 160/116/80 | All match; row sums 40/40/40 |
| 9 | 2.4: nine mockup `.ansi` files, 8 truecolor roles, no background code; `ESC[0;1;` counts 3 to 16; 48/42 ESC lines | grep over the .ansi files | Match (160 signal-bridge 16, 80 attention-ledger 3) |
| 10 | 2.4 / 3.2: role use (ages amber bold, ledger question text base bold, desk question text amber bold, titles cyan bold, badge amber, tile digit amber) | Decoded segments per line | Match |
| 11 | 2.4: pane geometry at 160/116/80 for all three screens | Measured box-corner spans in the `.txt` files | All match; frames 48/42 lines |
| 12 | 2.4 / 3.1: current-state captures have 0 ESC bytes | `grep -c` over `current/{160,116,80}` | 0 |
| 13 | 2.4: PNGs show a dark navy background; tile digit drawn as block glyphs | Viewed 160 attention-ledger and 116 decision-desk PNGs | Confirmed |
| 14 | 2.4 current structure (disclosure wraps at 116/80; `n/p`/`question` split at 116; `cost un>` at 80; desk 9 `label: value` lines then repeated table) | Read `current/*/questions.txt`, `desk.txt`, `ledger.txt` | Match |
| 15 | 2.3 test_render.py pins at :68-77, :83, :177-185, :242, :250-259, :263, :393, :396-404, :437-453, :591, :611-624, :660-676, :748-757, :853-887, :891-967, :970-987, :990 | Read the ranges | All exist as described |
| 16 | 2.3 test_terminal.py :41-51, :105-116 (`safe_box` at :109, :115), :181-198 | Read | Match |
| 17 | 9.4 row 31: test_view.py has 60 tests, 1383 lines | `wc -l`, `grep -c '^def test_'` | 1383 / 60 |
| 18 | 2.3 test_linkoff_screen_reference.py :34-37, :50-64, :67-69 (107 chars), :72-75 | Read | Match |
| 19 | 2.3 release1_surface.py `surface()` :41-62, `_printed` :34-38, docstring `git archive 9e2608b03` | Read; `git cat-file -t` | Match; commit exists |
| 20 | 2.3 history: `cd8736199` (#514) and `3206bdb9c` (#592); `.dev/issues/606/issue-body.md:84` lists the four files | `git log --oneline -- <file>`, `sed -n 84p` | Match |
| 21 | 2.2: `ASK_CAP = 400` with `...` at parse.py:499-503; link vocabulary :468-472; `parse_questions` :512-607 | Read parse.py 462-610 | Match |
| 22 | 2.1/3.7: no `mouse`/`blink`; keys.py cbreak :61; `_HANDLED` = INT/TERM/HUP/TSTP/CONT | Grep, Read keys.py | Match |
| 23 | 2.2: commands.py :58, :67/:70, :240-245, :264-274, :353 | Grepped | Match |
| 24 | Step 1.4: fixture state words (workerState 9 values, dispatchStatus 5, liveness verdicts alive/live/ended/exited/unverifiable) | Counted values in `fixtures/*.json` | Match exactly |
| 25 | 2.4: rendering-rules.md lines 17, 20, 25, 31, 33, 41, 43, 50, 57, 61, 70, 93; file is 107 lines | `sed -n`, `wc -l` | Match |
| 26 | Change map: render.py :368, :333, :373, :317, :319, :369, :387, :127-132, :195, :215; view.py :761, :794, :798, :804, :914-921, :948, :509 | Read render.py and view.py in full | Match (:373, not :374, is `counts_line`, as the report corrects) |
| 27 | Coordinator fix (desk age bold amber): step 1.4, step 5.3, RB-01(c), 3.2 table all agree | Read the four places | Consistent with each other (but see finding 5) |

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|---|---|---|---|---|
| 1 | Inaccurate | /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/render.py | 4.1a M-10 ("`_columns` (:203-204, 218-221)") and step 2.2 ("`_columns` already names the `line` columns (203-204)") | In the `line` branch the named columns `kind, dispatchId, liveness, age` are at render.py:199-202 (`flags` at :203, the closing bracket at :204). The `short` cite 218-221 is correct. True claim, wrong lines. | MINOR |
| 2 | Inaccurate | /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/current/116/ledger.txt | 2.4 "Spec versus code" ledger 116 row ("5 header lines") | The capture has 4 header lines (title, freshness, two counts lines) followed by the gap notice, the same as the 160 row, which lists "4 header lines, gap notice" separately. Counting the gap notice here makes the two rows inconsistent. The 2.1 measured table (counts 2, gap 1) is correct. | MINOR |
| 3 | Inaccurate | /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py | 2.3 pins table, whole-line equality row ("`GAP_NOTICE in lines` (:242, :454, :490)") | :242 and :490 are `GAP_NOTICE in lines`; :454 is `GAP_NOTICE not in lines` (negated). It is still a whole-line pin, but the wording "in" is wrong for that line. | MINOR |
| 4 | Distorted (confidence tag) | /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/terminal.py | 5.1.3, 5.1.4, 5.2.6, 5.6 table, 5.6 roll-up, 6.1 Option B cons, 9.4 row 37 | Section 5 and parts of 6 and 9 tag the `safe_box` no-effect probe, the 16-colour collapse mapping and the existence of `rich.box.HEAVY`/`ASCII` as `[UNVERIFIED ... not re-probed]`, while Sections 2, 3, 4, 8 tag the first two `[CODE-VERIFIED]`. I reproduced all three today (`safe_box` True/False identical; downgrade table identical; `hasattr(rich.box, "HEAVY")` and `"ASCII"` both True). The understatement is conservative and harms nothing, but a reader of Section 5 alone is told these are unconfirmed. | MINOR |
| 5 | Inaccurate (attribution) | /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/160/decision-desk.ansi (also 116, 80) | 3.2 palette table (amber "Used for (verified from segment text)": "ages"), RB-01(c), step 1.4, step 5.3 | Amber ages are verified only for the list rows in the attention-ledger mockup ("45 MIN", bold amber). In all three decision-desk mockups the only amber text is the badge, the `HUMAN QUESTION` title and the question lines; the desk age reads "observed 45m ago" in base colour (and "20m observed" in muted). Making the desk `qid  age` line bold amber (the coordinator fix) and requiring it in RB-01(c) is a design extension, not mockup evidence, and is not labelled as one. A reviewer scoring against the desk mockup would see no amber age there. | MINOR |
| 6 | Inaccurate (cosmetic) | /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py | 2.1 ("test_render.py:396-403"), 2.3 ("396-399" and "400-404"), 3.7/6.1 ("401-404"), SC-17 ("396-404") | The source-guard test spans :396-404 (renderables equality :399, regex :401-404). The report quotes four different ranges for it. No claim is false. | MINOR |

### Coverage and limits

- Read in full: render.py, view.py, terminal.py, sanitize.py, release1_surface.py, test_linkoff_screen_reference.py, test_terminal.py (lines 25-198), parse.py lines 462-610, and the report (1918 lines).
- Read in ranges: test_render.py (lines 60-189, 236-265, 280-380, 385-404, 437-511, 575-630, 640-762, 845-1022).
- Checked by grep, count or read-only probe only: adapter.py (not opened, no report claim depends on its body), record_golden.py and record_golden_questions.py (grep for what they write), test_view.py (line and test counts, `r3_workers` signature), golden JSON files (loaded and re-serialised, never read whole), the nine current-state and nine mockup `.txt`/`.ansi` files at 160 and 116 (decoded by script), two PNGs viewed (160 attention-ledger, 116 decision-desk); the other four 160/116 PNGs were not viewed.
- Not verified because outside the assigned set: Zellij facts (Section 2.5), the web findings (Section 5.4, 5.5 URLs), commands.py hop-by-hop live trace (only the cited line anchors), test_commands.py and test_export.py line cites, and the gaps-and-questions log.

### Summary

- Files checked: 15 assigned source files (7,415 lines) plus the 160 and 116 design inputs (see "Coverage and limits" for read depth).
- Claims verified: 27 verification groups covering about 120 individual claims (line anchors, constants, measured screens, probes, golden contents, palette, geometry, test pins, git history, spec lines). Tool engagement: Read 22, Grep 9, Bash/probe 14 (including 8 `uv run python -I -B` re-measurements and 3 CLI runs), no Glob.
- Fidelity issues: 6, all MINOR (citation or count drift, an understated confidence tag, one unlabelled design extension). Blocking (CRITICAL/IMPORTANT): 0. No phantom findings, no distorted code behaviour, no aspirational claims.
- Confidence: Verified 5/5 checklist items with tool evidence | Unverifiable 0 | Unchecked 0 | Confidence 100% for the assigned scope; residual risk is limited to the unread parts listed under "Coverage and limits".
- Verdict: **PASS** (with 6 minor notes; none triggers a fix pass).

**Status:** Complete

## QA Complete
