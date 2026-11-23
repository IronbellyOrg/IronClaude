## internal-consistency QA Report

**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
**Lens:** internal-consistency
**Date:** 2026-11-17
**Status:** Complete (see the end of the file)

### Checklist Results

(appended incrementally below)

#### Interim notes after reading report lines 1-1290 (Sections 1-7)

- IC-A (blocking candidate): report line 753 (5.1.5) says the 64-hex token in the 80-column Decision Desk "is silently clipped today" by `render.py:528`; line 861 (5.6 Q7 row) repeats "crop clips the 64-hex token silently ... Supports render.py:528". Report lines 271-272 (2.3), 578 (3.8 Q7), 623 (4.1b), 1264 (7.2 Q7) say measured: the hash wraps whole on its own line at 160/116/80 because `wrap` runs before `render()`. Direct contradiction on the Q7 fact.
- IC-B (minor): report line 312 (2.4) says "12-column table" at ledger 160; lines 144 (2.1), 494 (3.3), 516 (3.5), 1242 (7.1) say 11 columns (10 separators).
- IC-C (minor): report line 586 says "Severity follows the scale in the header"; the report header (lines 1-6) holds no severity scale. Dangling reference. The High (FIND) to Critical mapping for M-01..M-05 is not explained (only the C8 raises are).
- IC-D (minor): verification tags for the same facts differ by section: `safe_box` no-effect and 16-colour collapse are CODE-VERIFIED/measured in 2.1, 3.2, 4.3a, 6.0 but "[UNVERIFIED in this synthesis, not re-probed]" in 5.1.3, 5.2.6 and the 5.6 roll-up (line 899); the one-renderable-per-line test is verified in 2.3 but UNVERIFIED in 5.1.2. Section 5 preamble scopes its tags to files 02 and 05, so this is explained but reads as inconsistent.
- IC-E (minor): 5.6 line 852 says "four are refinements or corrections ... (rows marked below)"; no four rows are marked.
- IC-F (minor): Q-7 (PNG dependency) is "OPEN" at line 622 (4.1b) but "closed here as no for the gate" at line 1260 (7.2).

#### Checklist results (all 1,877 lines read in 8 ranges)

**(a) IDs, labels and names match their references: FAIL (1 blocking, 5 minor)**
- M-01 to M-18: 18 rows in 1.3 (lines 46-65), 4.1a (592-609) and 8.10 (1718-1735); FIND severities in 1.3 equal the "Severity per FINDINGS" column of 8.10 for all 18. Consistent.
- Option letters: Q1 Options A/B/C (6.1), Q3 H1/H2/H3, Q4 D1/D2/D3, Q6 Z1/Z2/Z3 in Section 6 are the ones used in 7.1, 7.2 and 8.1 (Option C, H3, D2 via D1, Z2). Consistent. Section 4 uses a separate numeric list (1)-(5) and "Q1 option 2" (lines 616, 642) with no mapping to A/B/C (minor, IC-L).
- Owner decision ids: 8.2 defines D-1 to D-7 only; D-8 is used at lines 1571, 1590, 1675 ("D-1 to D-8 ... see 8.2") and 1710 but is not defined in 8.2 and is absent from 7.3 and 9.1; D-7 is absent from 7.3 (IC-G, blocking). 7.3 also lists decisions (PNG renderer, RR 61 reword, NO_COLOR bold and dim) that have no D-id in 8.2.
- Guard ids: NO_COLOR is G-2 in 1.3 (line 72) and 3.7 (552) but RB-06 (line 1356) and 8.5 (line 1388) and step 3.10 (line 1516) label the NO_COLOR pass "guard G-1" (IC-I). Gap letters G-A and G-E to G-H are used in 4.1b but G-B, G-C, G-D appear only in 9.2 (lines 1762, 1764, 1765); "C8" means a defect rule in 4.1 (line 586) and a corrected-claim row in 9.5 (line 1825) (IC-M).
- SC-1 to SC-19 (3.6) and RB-01 to RB-23 (8.4) are two id systems with no cross-map; no dangling RB or SC id found. RB scope per phase equals the "Rubric rows scored" line of each phase (P1, P2, P3, P4, P5, P6 checked).

**(b) Counts agree across sections: FAIL (1 minor count error, others pass)**
- Phases: 7.1 sequence and Section 8 headings list P0 to P7 (eight). 8.1 row Q2 (line 1299) says "Seven phases" (IC-H, minor).
- Golden arithmetic: 5 variants x 14 keys; 15 `printed_*` and 30 `lines_*` repeated at lines 261, 273, 573, 592, 1259; consistent. Golden-changing phases P2, P3, P4, P6 (line 573) match 7.1 steps 3-7 and Section 8 steps 2.7, 3.9, 4.8, 5.6, 6.6.
- Widths 160/116/80 and the pane arithmetic (1+114+2+42+1=160; 1+70+2+42+1=116; 1+76+2+80+1=160; 1+66+2+46+1=116; 78 wide, 74 usable at 80) agree at lines 299-306, 485, 515, 1242-1244, 1337-1338, 1537, 1578-1585. Inner width width-6 = 154/110/74 agrees at lines 1304, 1513. 4.2 left = width-4-42 and RIGHT_DESK left = width-4-80 agree.
- Q1 to Q7 answers: 3.8 (568-578), 7.2 (1258-1264) and 8.1 (1298-1304) agree on every question except the Q7 clipping statement (IC-A).
- Ledger column count: 11 at lines 144, 494, 516, 1242 but "12-column" at line 312 (IC-B, minor).
- Evidence-trail counts: 5 codebase + 2 web files (line 5) match Section 10 (lines 1839-1854); synth-01 to synth-06 match the Section 1-10 split; "58 rows, 8 Important" (line 1860) matches the eight lettered gaps G-A to G-H, but 9.2 is headed "Important in the gaps log" and holds 11 rows (5 to 15) (IC-Q, minor, cannot be reconciled from the report alone).
- Gap-to-plan coverage: every M-01 to M-18 has a closing phase in 8.10; guards G-1, G-2 and gaps G-A, G-E, G-F, G-G, G-H, colour depth, composition, harness, Zellij each map to a step (1.1, 1.5, 1.6, 2.7, 3.7, 3.8, 6.4, 7.1, 7.4). No orphan gap.

**(c) Cross-references resolve: FAIL (1 blocking, 3 minor)**
- ToC (lines 12-21) matches all ten `##` headings. "see 8.2" for D-1 to D-8 does not resolve for D-8 (IC-G). "see 7.2 Q5" (line 994), "see 9.5" (1765), "see Section 4" (540), "row 17" (1777), "step 2.1", "step 0.4", "step 1.6(c)" all resolve. "Section 4 harness row" (line 540) resolves to the Render harness row at line 622. Q-7 is OPEN at line 622 and closed at line 1260 (IC-F). SC-14 and 4.1b say the rubric is not yet written (lines 540, 622, 1771) while 8.4 gives all 23 rows (IC-O). Line 586 "scale in the header" has no target (IC-C). 5.6 "(rows marked below)" has no marked rows (IC-E). 9.5 row 39 says the guard test is "now :747-760" (line 1810) while 4.3b, 2.6, SC-16 and C5 say :747-756 (IC-K).

**(d) No contradictions within the document: FAIL (1 blocking)**
- Colour-system fact (`"standard"` at terminal.py:121, NO_COLOR gives None and drops bold, 16-colour collapse of muted/green/red/violet to 7): identical at lines 119, 171-182, 467, 481, 506, 784, 1093-1098, 1301, 1762. Pass. Only the verification tag differs (IC-D).
- One-shot export fact (`export_text()` at commands.py:242 drops styles; `export_text(styles=True)` ignores NO_COLOR and the downgrade; use `console.file.getvalue()`): identical at lines 191, 222-224, 378, 443, 576, 618, 658, 796, 920, 1262, 1302, 1398, 1764. Pass.
- Header-gate fact (heading and rule only when `width_class == "full"` and rows visible, render.py:497-498, mirror :439, in `screen_lines` not `render()`; `reserved` needs no edit): identical at lines 145, 332, 384, 601, 643, 925, 1229, 1481, 1727. Pass.
- Q7 hash fact: lines 271-272, 447, 578, 623, 1264, 1304 say the hash is wrapped whole and never clipped; lines 753 and 861 say it "is silently clipped today". Contradiction (IC-A).
- Current-state versus gap: "no READ ONLY text" (168, 604), "no RETAIN CONTEXT" (1552), "no heading at 116/80" (601) agree with Section 2. Section 2 says question text never reaches a file (229) and 3.7, 7.2, 8.9 agree.

### Findings

Line numbers are lines of the report reviewed.

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| 1 | IMPORTANT (blocking) | 5.1.5 (line 753), 5.6 Q7 row (line 861) vs 2.3 (271-272), 3.8 (578), 4.1b (623), 7.2 (1264), 8.1 (1304) | 5.1.5 says "the 64-hex-character token in the 80-column Decision Desk is silently clipped today" because `render.py:528` uses `overflow="crop"`, and 5.6 repeats "crop clips the 64-hex token silently ... Supports render.py:528". Every other section reports the measured fact: `screen_lines` wraps first, so the hash is whole on its own line at 160, 116 and 80 and no line exceeds the width, so crop never fires. | Reword both rows to say crop is the generic Rich behaviour and that today `wrap()` runs before `render()`, so the hash is not clipped; keep the "ellipsis costs one cell" point as external context only. |
| 2 | IMPORTANT (blocking) | 8.2 (1323-1331) vs 5.1 (1571, 1590), 8.8 (1675), 8.9 #15 (1710), 7.3 (1266-1284) | Owner decision D-8 (desk evidence pane title) is cited as defined in 8.2 ("D-1 to D-8 ... see 8.2") but 8.2 lists D-1 to D-7 only; D-8 is defined only inline in step 5.1. 7.3 ("What the owner must decide") omits both D-7 and D-8, and 8.2 omits the PNG, RR 61 and NO_COLOR bold/dim decisions that 7.3 and 9.2 list. The register the PR body must record (8.9 #15) therefore has no single consistent list. | Add a D-8 row (default `LINKED SESSION`, effect: only the constant and a spec edit to RR 57) to 8.2; add D-7 and D-8 to 7.3, or state which list is authoritative and give the PNG, RR 61 and NO_COLOR decisions D-ids. |
| 3 | MINOR | 2.4 (line 312) | "12-column table" for ledger 160; 2.1, 3.3, 3.5 and 7.1 say 11 columns with 10 separators. | Change 12 to 11. |
| 4 | MINOR | 4.1 (line 586), 4.1a | "Severity follows the scale in the header": the report header has no scale. High (FINDINGS) maps to Critical for M-01 to M-05 without explanation; C8 defects M-08, M-10, M-11 are Critical in 4.1a (and "not downgraded") but Medium in 8.4 (RB-11 to RB-13) and 8.10. | Define the scale in 4.1 and state the High-to-Critical rule and that the rubric uses its own High/Medium/Low gating scale. |
| 5 | MINOR | 5.1.2, 5.1.3, 5.2.6, 5.6 roll-up (lines 750, 751, 785, 899) vs 2.1, 2.6, 3.2, 4.3a, 6.0 | Same facts carry different tags: `safe_box` no-effect probe and the 16-colour collapse are verified/measured (reproduced by two reviewers) in Sections 2-4 and 6 but "[UNVERIFIED in this synthesis, not re-probed]" in Section 5; the one-renderable-per-line test is verified in 2.3 but UNVERIFIED in 5.1.2. Section 5's preamble scopes its tags to files 02 and 05, which explains but does not remove the apparent conflict. | Add a sentence in 5 that the facts are verified in Sections 2-4 by files 01 and 04, or re-tag. |
| 6 | MINOR | 5.6 (line 852) | "four are refinements or corrections ... (rows marked below)": no four rows are marked; the contradictions table below has six rows and the roll-up two. | Remove the count or mark the rows. |
| 7 | MINOR | 4.1b Render harness (line 622) vs 7.2 Q3 (line 1260) | Q-7 (PNG dependency) is "OPEN" in 4.1b and "closed here as no for the gate" in 7.2. | Say "open for the owner; recommended no" in both places. |
| 8 | MINOR | 8.1 row Q2 (line 1299) | "Seven phases" but the same row and 7.1 list P0 to P7 (eight). | Change to "Eight phases (P0 to P7)". |
| 9 | MINOR | 8.4 RB-06 (line 1356), 8.5 (line 1388), step 3.10 (line 1516) vs 1.3 (72), 3.7 (551-552) | The NO_COLOR pass is attributed to guard G-1; G-1 is the ASCII-pane guard and NO_COLOR belongs to G-2. | Label RB-06 and the NO_COLOR half of 8.5/3.10 as G-2. |
| 10 | MINOR | 2.4 (line 335), 4.1a M-13 (604), 7.3 OPEN-3 (1273), 9.1 row 4 (1755) vs step 2.5 (1484), steps 4.1 and 4.4 (1549, 1552) | The report says the M-13 split is "inside render.py only" and M-05/M-14 are "render-only", but the plan edits `OBS/view.py` (adds `READ_ONLY_BADGE`, `count_figure`, `RETAIN_TITLE`). The intent (no change to `header1`, `counts_line` or the record) holds. | Reword to "no change to view strings that the record reads; constants and one defaulted field are added in view.py". |
| 11 | MINOR | 9.5 row 39 (line 1810) | Says the guard test is "now :747-760"; 2.6 (385), 4.3a (668), SC-16 (542) and C5 (1822) say the range is :747-756 and :747-760 is the earlier error. | Change to :747-756. |
| 12 | MINOR | 4.1b composition row (616), 4.2 (642), 4.5 (727) vs Section 6.1 | Section 4 numbers options (1) to (5) and says "Q1 option 2"; Section 6 to 8 call them Options A, B, C. No mapping is given. | Add the mapping (A = 1+3+5, B = 4, C = 2+3+5) in 4.1b. |
| 13 | MINOR | 4.1b vs 9.2; 4.1 (586) vs 9.5 (1825) | Gap letters G-A, G-E, G-F, G-G, G-H are used in 4.1b but G-B, G-C, G-D are not, though 9.2 uses them; "C8" names a defect rule in 4.1 and a corrected-claim row in 9.5. | Add G-B, G-C, G-D to the matching 4.1b rows; rename one "C8". |
| 14 | MINOR | 9.2 row 8 (line 1764) vs 4.3a (658), 6.0 row 4 (920), 8.6 (1398) | Row 8 says "Research 01, 02 and 03 gave conflicting advice" on the styled-export route; the other three place name 01 and 05 (and `render_current.py`). | Use one attribution (01 and 05). |
| 15 | MINOR | 3.6 SC-14 (540), 4.1b harness row (622), 9.2 row 15 (1771) vs 8.4 (1347-1373), 8.5 | Sections 3, 4 and 9 say the rubric and threshold are "NOT yet defined"; 8.4 and 8.5 define 23 rows and the pass rule. | Say the rubric is defined in 8.4 and is written to a file in P0. |
| 16 | MINOR | 9.2 heading (line 1757) vs 10 (line 1860) | 9.2 is headed "Important in the gaps log" and holds 11 rows (5 to 15); Section 10 says the gaps log has 8 Important rows. | Reconcile the count or retitle 9.2. |

### Summary

- Total findings: 16
- Critical: 0
- Important (blocking): 2
- Minor (notes): 14
- Checklist items: 4 reviewed (a, b, c, d); all four contain at least one finding. The three named facts (colour system, one-shot export, header gate) are stated identically in every place they appear.
- Confidence: Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (lens-scoped; source-code truth was out of this lens)
- Tool engagement: Read: 12 (task line 281, 8 ranges of the report, 2 reads of this file, plus this report's own state) | Grep: 0 | Glob: 0 | Bash: 1 (line count and heading list). Report was read in full by ranges, so Grep was not needed for coverage.
- Verdict: FAIL (2 blocking findings: #1 contradiction on the Q7 hash behaviour, #2 owner-decision register inconsistent with D-8). The 14 minor findings are notes.

**Status:** Complete

