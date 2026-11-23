# QA fix log, Phase 5 synthesis gate (Gate 2), cycle 1

One line per fix: finding number, file, change.

- F4 | synth-05 step 2.2 | `_heading_rows` now used at two places (ledger_fixed :439, gate :497); explicit "do not add to `reserved`" because `reserved` reads `len(body)` which already holds the heading rows (render.py:495-501 re-read).
- F4 | synth-02 RN-2 | removed `reserved` from the "add 2 heading rows" instruction; explains the double count.
- F4 | synth-01 M-10 mapping row | `reserved` :499-501 noted as needing no separate edit.
- F3 | synth-05 8.1 Q7 row | rule restated per surface (desk text whole inside first 4 wrapped lines, cut by `...` beyond; ASK_CAP 400 at parse.py:503; evidence field hard-split rule with 116 evidence inner 62). Re-read render.py:62-80, 329-356, view.py:99, parse.py:475/503.
- F3 | synth-05 8.2 D-6 | default now "today's rule, no cap changed"; effect-if-different lists the code places and the test/spec edits.
- F3 | synth-05 step 0.6 and RB-19 | second test named as the one stated exception; RB-19 scoped to the PLAN_ASK fixture, trailing-hash fixture keeps `...`.
- F5 | synth-05 step 4.5 | dropping the RETAIN pane now relocates run line, caveat and retention sentence to the left body (P3 order), dropping the tile relocates `counts_line`; single recompute of `base`/`capacity`; literals checked against view.py:67, 73, 794 and rendering-rules.md lines 42-48.
- F5 | synth-05 step 4.7 tests | added a test at heights 24 and 26 at 116 (and 160) that the three required lines are present whether or not the pane is drawn, lines fit width and height; trigger heights to be measured at implementation.
- F2 | synth-05 step 1.6(c) and file list, P1 "tests and goldens that change" | replaced one-sided strip in T47 by `release1_surface.py::_printed` returning `strip_sgr(...)`; T47 unedited; golden bytes unchanged in P1. Re-read release1_surface.py:34-38, 60, test_render.py:45-52, 611-624 and terminal.py:110-125 (explicit color_system makes Rich write SGR to a StringIO).
- F2 | synth-05 step 2.7, P2 list, step 6.6 | regenerated goldens hold SGR-free `printed_*` by construction; new `test_presentation_goldens_hold_no_escape_bytes`; 6.6 states the same.
- F2 | synth-02 M-01 note and RN-1 cell | "regenerate 15 printed_* values" corrected to the strip-in-surface route (consistent with synth-05).
- F1 | synth-04 7.1 sequence | rewritten to P0 to P7 of synth-05 with its golden-per-phase assignments; width split kept as a note inside P4/P5; states that Section 8 is the plan of record. (also corrected the old `reserved` mention in step 4)
- F1 | synth-04 7.2 Q2 row | rewritten to the P0 to P7 scheme and golden assignments (P1 no golden, P2 both presentation goldens, P3 link-off, P4 link-off, P5 none, P6 release-1, P7 none); 6.x options table cell for golden churn notes the strip route.
- F1 | synth-02 3.8 Q2 row | labelled research 03's own grouping, then gives the P0 to P7 scheme of Section 8.
- F1 | synth-05 Section 8 opening | added the sentence that P0 to P7 is authoritative and Sections 3.8 and 7 mirror it.
- F1 | synth-04 7.3 tables, synth-06 row 1 (line 13), synth-04:70 | stale old-scheme labels (P3 phase for two-column, "P2 and P4", "P2 to P4", "P3/P4 gated") relabelled to P4 and P5 / P2, P3, P4, P6; research-03 labels kept but marked as research labels. Grep for `\bP[0-9]\b` over synth-01 to 06 re-run after editing.
- F4/F5 | synth-05 step 2.2 file column and step 4.4 | `reserved` marked read only; 4.4 notes lines return to the left body when 4.5 drops the pane (consistency).
- F3 | synth-04 Q7 answer | "wrap, never cut, the hash" replaced by the same per-surface rule with the cap exception and D-6 reference.

