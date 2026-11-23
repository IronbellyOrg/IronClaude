# QA Report - Phase 5 synthesis-gate fix verification (cycle 1)

**Topic:** observer visual parity
**Date:** 2026-11-18
**Phase:** fix-cycle (synthesis gate)
**Fix cycle:** 1
**Fix authorization:** false (report only)

Scope: the five blocking findings F1-F5 of qa-consolidated-findings-phase5.md, against the six synth files.

## Per-finding checks

| # | Blocking finding | Result | Evidence (source re-read, not the fix log) |
|---|---|---|---|
| F1 | Three incompatible phase schemes | FIXED | synth-05 Section 8 opening (line 3) now states P0 to P7 is authoritative and Sections 3.8 and 7 mirror it. synth-04 7.1 (lines 321-330) lists P0 to P7 with golden-per-phase: P1 none, P2 both presentation goldens, P3 and P4 link-off, P5 none, P6 release-1. synth-04 7.2 Q2 row (line 355) gives the same. synth-02 3.8 Q2 row (line 132) labels research 03 as its own grouping and gives the P0 to P7 scheme. All agree with synth-05 8.9 row 13 (P2, P3, P4, P6) and the per-phase "goldens that change" lines in synth-05. synth-06 row 1 (line 13) uses "P4 and P5". |
| F2 | Suite not green after P2 (T47 vs styled `printed_*`) | FIXED | `tests/observe/release1_surface.py:34-38` builds `printed_*` through `make_console` and `render()`, so the defect was real. synth-05 step 1.6(c) makes `_printed` return `strip_sgr(...)`, so T47 (`test_render.py:611-624`, which compares `surface()` to the golden key by key) is unedited and neither side is stripped one-sidedly. Steps 2.7 and 6.6 state the regenerated golden holds SGR-free `printed_*`, and add `test_presentation_goldens_hold_no_escape_bytes`. `strip_sgr` is created in P0 step 0.7 in `tests/observe/conftest.py`, which `release1_surface.py:23` already imports from, so the order is valid. I grepped for every other reader of a styled console stream (`getvalue()`): test_render.py:52 (audited by step 1.6(b)), test_terminal.py:34 (step 1.6(d)), test_commands.py:65 (plain `run_once` stdout). `test_linkoff_screen_reference.py` uses `screen_lines` only, so the link-off golden is unaffected in P1. |
| F3 | Q7 hash "never cut" vs the 4-line cap | FIXED | Code facts re-read: `view.py:99` `DESK_TEXT_LINES = 4`; `parse.py:475` and `:503` `ASK_CAP = 400` cut with `...`; `render.py:339-346` cuts the fourth desk line with `...`; `render.py:62-80` `wrap` keeps a token whole unless it is wider than the width. synth-05 8.1 Q7 row, D-6, RB-19, step 0.6 (second test is the one stated exception), step 3.7 and step 5.5, synth-04 Q7 answer (line 360), and synth-06 row 10 (line 27) now all state the same per-surface rule. The widths 154/110/74 and 72/110/74 recompute correctly from 8.3. |
| F4 | False "add heading rows to `reserved`" instruction | FIXED | `render.py:495-501` re-read: `body` takes the heading rows at :497-498 before `reserved = len(top)+len(body)+footer_height+1`, so a separate addition would double count. synth-05 step 2.2 says explicitly not to add them to `reserved` and to use `_heading_rows` at :439 and :497 only. synth-02 RN-2 (line 202) and synth-01 M-10 row (line 312) say the same. The remaining mention at synth-02:77 ("counted inside ... `reserved`") describes frame rows that enter `body` and is true. |
| F5 | Step 4.5 drops required text with the RETAIN pane | FIXED | synth-05 step 4.5 now relocates `run_line`, `caveat_line` and `retention_line` to the left body when the pane is dropped (and `counts_line` when the tile is dropped), and step 4.4 says the same. Literals checked against `view.py:67` (retention), `:73` (caveat), `:794` (run line); the strings in step 4.7 match them. Step 4.7 adds a test at heights 24 and 26 at 116 and 160 that the three lines are present whether or not the pane is drawn. |

## Structure and new-issue checks

- Headings of synth-01 to synth-06 listed by grep: all section headers present in order; synth-05 keeps 8.1 to 8.10 plus Phase 0 to 7 and Summary.
- Table column counts checked with a script over all six files: no row edited by the fix cycle is malformed. The only deviations are unescaped `|` inside code spans in synth-05 lines 65, 68, 106 and synth-03 lines 47, 63, 86, none touched by this cycle (see minor notes).
- No new blocking inconsistency found between synth-05 steps 1.6, 2.1, 2.7, 3.9, 6.6 and the "tests and goldens that change" lists.

## Minor notes (not blocking, not rechecked later)

1. synth-05 lines 65, 68, 106 and synth-03 lines 47, 63, 86: raw `|` inside code spans splits the table cell in strict renderers. Escape as `\|`. Pre-existing.
2. synth-06 row 5 (line 22) still says "A style-only phase changes only the 15 `printed_*` values", which is research 03's route; the plan keeps them plain by the strip.
3. synth-04 line 375 says P3 and P4 change the link-off screens; P2 also regenerates the link-off golden (synth-05 step 2.7).
4. synth-05 8.1 Q7 row: "62 at 116 in P5" is the evidence pane inner width; "inner width minus 2" would be 60. A 64-cell value splits either way.
5. synth-05 step 4.5: "single retry" of the base/capacity recompute is ambiguous when both the pane and the tile are dropped; decide the surviving panes first, then compute once.
6. synth-05 8.1 Q2 says "Seven phases" for P0 to P7 (eight).
7. synth-06 line 90 still says "phase split P0 to P5 (03 section 6)"; it is research 03's own label.

## Overall Verdict: PASS (with notes)

- Blocking findings from cycle 1: 5. Fixed: 5. Still open: 0. New blocking issues introduced: 0.
- Remaining blocking count: 0.

## Confidence

Verified: 5/5 blocking findings plus structure check | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 17 | Grep: 8 | Glob: 1 | Bash: 1 (read-only table-shape script)
Limits: I did not re-read research files 01 and 03 in full; the code facts the fixes rely on (render.py, view.py, parse.py, release1_surface.py, test_render.py T47) were read directly from source.

## QA Complete
