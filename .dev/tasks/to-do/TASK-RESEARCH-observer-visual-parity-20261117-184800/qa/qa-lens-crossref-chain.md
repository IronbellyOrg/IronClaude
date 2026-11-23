## crossref-chain QA Report

**Report reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md
**Lens:** crossref-chain
**Date:** 2026-11-17
**Status:** Complete

### Checklist Results

**Method.** Read the report in ranges (lines 25-1878, all ten sections). Grepped `D-8` and the Q-n ids. Read `gaps-and-questions.md` rows 26-86 to check the "GAPS row n" cites. Globbed the task directory to confirm the files named in Section 10 exist. Each chain was traced by reading both ends.

**(a) Section 4 gaps to Section 8 steps or Section 9 questions: PASS with findings F-1, F-2, F-8, F-9, F-10.**
- M-01 to M-18: all 18 appear in the Section 4.1a rows and in the Section 8.10 map with closing phase, step and rubric row. Steps checked against phase bodies: M-01 1.1-1.6; M-02 3.1-3.3 and 6.3; M-03 4.2/4.5; M-04 5.3/5.4; M-05 4.1/4.3; M-06 6.1-6.4; M-07 4.4/4.5; M-08 1.4; M-09 1.4 and 5.2; M-10 2.2; M-11 2.3; M-12 5.2/5.3; M-13 2.5; M-14 4.4/4.5; M-15 2.3; M-16 2.4; M-17 2.6; M-18 1.4. All steps exist. Rubric rows RB-01 to RB-23 line up with the 8.10 "Rubric row" column.
- RN-1 to RN-3 (Section 4.2) map to steps 1.4, 2.2 and 2.3.
- G-1 maps to 3.1, 3.2, 3.10 and RB-07. G-2 maps to 1.1, 1.2 and RB-09.
- AD-1 to AD-7: all seven are present in Section 3.7 and Section 1.3. AD-1 to AD-4 recur in Section 8.8 (excluded findings) and in RB-18. AD-7 and the RR 61 reword map to 7.1. No Section 8 step is required for an AD.
- OPEN-1 to OPEN-3 map to D-3 (8.2), 7.3, Section 9.1 rows 2 to 4, and RB-15/16/17. O-1 maps to D-1, Section 9.1 row 1, and P4/P5.
- Section 4.1b gaps: Q1 composition maps to 1.3; colour depth maps to 1.1/1.2 and D-5; styled capture maps to 1.5/1.6 and D-4; LiveScreen (G-F) maps to 1.6(g); height (G-G) maps to 0.7 and 3.8; golden (G-A) maps to D-2, 2.1 and 2.7; harness maps to 0.1-0.8; Q7/G-E maps to 0.6 and 3.7; Zellij maps to 7.4; G-H maps to 7.1.
- Broken or weak links found: D-8 (F-1); box lines in `--once --width` (F-2); M-07 "separation" (F-8); 4.4 real-terminal capability (F-10); fixtures `injection` and `long-identifiers` (F-9).

**(b) Section 6 options cite Section 2 or Section 5 evidence: PASS with findings F-4, F-6.**
- 6.1 Options A, B, C: the facts table (lines 931-939) matches Section 2.1 (render.py:524-531, `test_render.py:399`, export.py imports) and Section 5.1 (5.1.1 spans, 5.1.2 Panel/Table, 5.1.3 `safe_box`). External context W01 is cited. The options are distinct (hand-built plus string pass, Rich renderables, role-recording hybrid).
- 6.2 H1, H2, H3 match Section 2.5 (tool inventory) and Section 5.5 (5.5.1 to 5.5.8). 6.3 D1, D2, D3 match Section 2.1 colour table and 5.2.1/5.2.2/5.2.5/5.2.6. 6.4 Z1, Z2 match Section 2.5 and 5.4.
- Z3 carries no evidence cell (only "n/a"); minor. The Section 4.1b and 4.5 option numbers (1) to (5), "1 to 7" and RN-1's "Q1 option 2" do not map to the A/B/C labels in Section 6 (F-4). Section 5.6 and 6.2 tag the `safe_box` probe and the 16-colour collapse differently from Sections 2.1, 3.2, 4.3a and 6.0 (F-6).

**(c) Section 7 recommendations trace to Section 6; Q1 to Q7 have evidence in 2 or 5 and an action in 8: FAIL for the Section 6 trace of Q2, Q5, Q7 (F-3) and for the ownership of two decisions (F-1, F-2).**
- 7.1 rows Q1 (Option C), Q3 (H3), Q4 (D2 as D1 floor then detection), Q6 (Z2) each trace to a comparison table in 6.1 to 6.4 and to the Section 8 phases: Q1 to 8.1 and P1/P3, Q3 to P0 and 8.5, Q4 to 1.1/1.2, Q6 to 7.4. Consistent.
- 7.2 Q1 to Q7: evidence (R-file cites) matches Sections 2 and 5. Actions: Q1 P1/P3, Q2 P0 to P7, Q3 P0, Q4 P1, Q5 1.5/1.6, Q6 7.4, Q7 0.6/3.7/5.5. Cites to GAPS rows (1, 2, 5, 6, 7, 8, 25, 26, 32, 34-38, 39, 42) were checked against `gaps-and-questions.md` and match.
- Q2, Q5 and Q7 recommendations have no Section 6 options comparison. Section 9.2 row 8 tells the reader to decide the tty rule and the box-line question "as one options-section decision"; Section 6 has no such section (F-3).
- 7.3 lists a decision on box-drawing lines in a piped `--once --width` (line 1284) that has no D-id or default in 8.2 (F-2). 8.2 and Section 8 use D-8 that 8.2 never defines (F-1).
- 7.2 Q2 lists P2 test changes (`test_view.py`, `test_export.py`, `KEYS_LITERAL`) that Section 8 P2 does not contain (F-5).
- 7.1 Q3 says image-to-image comparison is not part of the gate; 8.5 G3/G4 and RB-01/RB-02 score a rasterised PNG against the mockup PNG (F-7).

**(d) Findings in Sections 2 and 3 that warrant action appear in Section 4 or Section 8: PASS with findings F-8, F-9, F-10, F-11.**
- Section 2.1 to 2.5 action items map: `GLYPHS` and `ascii_safe` to G-1; fixed `"standard"` to the colour-depth row; `LiveScreen` shape tuple `(width, height, ascii, no_color)` to step 1.5 (adds `color_system`); `render_current.py` import guard and `export_text(styles=True)` to steps 0.1/0.2; `+1` terms to 8.8; spec lines RR 17, 20, 25, 33, 41, 43, 57, 61, 70 to 7.1.
- Section 3.6 SC-1 to SC-19 map: SC-1 1.6(b); SC-2 RB-06; SC-3 RB-07; SC-4 RB-08; SC-5 1.6(a); SC-6 RB-09/RB-10; SC-7 8.9 row 3 and the canaries in 0.6; SC-8 RB-05; SC-9 0.7/3.8; SC-10 0.6/3.7; SC-11 RB-13; SC-12 RB-21; SC-13 RB-12; SC-14 0.5/8.4/8.5 G6; SC-15 1.6(g); SC-16 8.9 row 5; SC-17 8.9 row 6; SC-18 8.8 and existing tests; SC-19 D-2.
- Section 3.3 target "badge must not push `as of` onto its own line" has no step or rubric row (F-11). M-07 "separation" has no step (F-8). Section 4.4 "run on a real terminal at 16, 256 and truecolor" has no plan step (F-10). 8.8 promises fixtures `injection` and `long-identifiers` in the harness matrix; 0.3 and 8.5 G2 do not list them (F-9).

### Findings

Blocking = Important (no Critical). Minor findings are notes only.

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| F-1 | IMPORTANT (blocking) | 8.2, 7.3, 9.1 versus 5.1, 7.1 (spec edits), 8.8, 8.9 row 15 | Decision D-8 (title of the Decision Desk evidence pane) is used in P5 step 5.1 (line 1590: "wording is decision D-8 and a spec edit to RR line 57"), P5 dependencies (1571), P5 rollback (1604), step 7.1 (1642), 8.8 (1675: "Owner rulings D-1 to D-8 ... see 8.2") and 8.9 row 15 (1710: "D-1 to D-8 recorded with the owner's answer"). The 8.2 table (lines 1323-1331) defines only D-1 to D-7. D-8 is also absent from 7.3 and from Section 9.1. The owner-facing decision lists never show it, so the decision can go unasked, and the 8.2 pointer in 8.8 is false. | Add a D-8 row to 8.2 (decision: evidence-pane title; default `LINKED SESSION`; if different: only `DESK_EVIDENCE_TITLE` and the RR 57 wording change). Add it to the 7.3 further-decisions table and to Section 9.1. |
| F-2 | IMPORTANT (blocking) | 4.1b (Live versus one-shot row), 7.3 line 1284, 9.2 row 8, 8.2, P3 3.6 | The question "may `--once --width` output include box-drawing lines" is flagged OPEN in four places (4.1b: "box-drawing in `--once --width` output"; 7.3 last row; Section 9.2 row 8; gaps log row 3, which says to carry it as one decision in the options section). Section 6 has no such comparison and 8.2 has no D-id or default for it (D-4 covers ANSI on a pipe only). P3 step 3.6 silently decides yes: it rewrites `test_commands.py:672-675` and `:690` with `title_of` and `unframe` because `--once --width` stdout now carries frames. An open owner question has a plan step that assumes its answer. | Add a decision row to 8.2 (for example D-9: box-drawing lines in `--once --width` output; default yes with ASCII forms under `--ascii`; if no, P3 3.6 and 3.9 change). List it in 7.3 against that id, and state the default in 6 or 7.2 Q5. |
| F-3 | MINOR | 6, 7.1, 7.2 | Q2, Q5 and Q7 are recommended in 7.2 but have no comparison in Section 6 (6.1 to 6.4 cover Q1, Q3, Q4, Q6). 9.2 row 8 refers to "one options-section decision" that does not exist. The Q5 route options are in 4.3a, 5.3 and 9.2 row 8 only. | Add short option tables for Q5 (capture route), Q7 (hash rule) and Q2 (phase scheme) to Section 6, or state in 7.1 that these three are decided from 4.3a and 5.3. |
| F-4 | MINOR | 4.1b, 4.2 RN-1, 4.5 versus 6.1 | Options are numbered (1) to (5) in 4.1b, "options 1 to 7" in 4.5, and "Q1 option 2" in RN-1, while Section 6.1 uses A, B, C. No table maps one set to the other. Z3 in 6.4 has no evidence cell. | Add a one-line map (for example 1-3 and 5 = A/C, 4 = B) or relabel RN-1 as "Option C". |
| F-5 | MINOR | 7.2 Q2 versus 8 P2 | 7.2 Q2 says the P2 text phase changes literals in `test_view.py`, `test_export.py` and `KEYS_LITERAL`, and states that it mirrors Section 8. Section 8 P2 (2.1 to 2.8) changes `test_render.py`, `test_inspector_scroll.py` and both goldens, and does not touch the other three. 4.2 RN-3 says `KEYS_LITERAL` changes only if the key text changes, and 2.3 does not change the key text. | Align the 7.2 Q2 P2 list with the "Tests and goldens that change" line of P2. |
| F-6 | MINOR | 5.1.3, 5.2.6, 5.6 roll-up versus 2.1, 3.2, 4.3a, 6.0 | The same two facts carry different tags. The `safe_box` no-effect probe and the 16-colour collapse are [UNVERIFIED in this synthesis, not re-probed] in 5.1.3, 5.2.6 and the 5.6 roll-up (line 899). In 2.1, 3.2, 4.3a and 6.0 they are [CODE-VERIFIED] and "reproduced by two reviewers". | Add to the 5.6 roll-up that these are verified by the codebase files 01 and 04 (the 5.x tags are relative to files 02 and 05 only), or retag. |
| F-7 | MINOR | 7.1 Q3 versus 8.5 G3/G4, 8.4 RB-01/RB-02 | 7.1 says "Image-to-image comparison is not part of the gate" and H1 is an extra "after one end-to-end trial". 8.5 makes rasterising (G3) and a reviewer scoring the rendered PNG against the mockup PNG (G4) a step of every phase, with a text fallback only if step 0.4 fails. | State in 7.1 that after step 0.4 passes the PNG tier is part of the in-session gate, with H3 as the offline floor. |
| F-8 | MINOR | 4.1a M-07 versus 8.10, 8.8, P4 | M-07 target is "row emphasis and separation". Row emphasis is built (1.4); only the age gutter is excluded (8.8). No step builds row separation, and RB-16 tests only "rows lead; caveats lighter". | Add a separation step or list "row separation" in 8.8's excluded findings with a reason. |
| F-9 | MINOR | 4.4, 8.8 versus 0.3, 8.5 G2 | 8.8 handles "fixtures `injection` and `long-identifiers` with styling" by "Include both in the harness matrix". The harness screens in 0.3 and 8.5 G2 are only `ledger`, `questions`, `desk`, `desk-planask`. SC-18 is still covered by the existing `test_render.py` injection tests. | Add the two fixtures to the 0.3 output set, or change the 8.8 handling to name the existing tests. |
| F-10 | MINOR | 4.4 row 1 versus 8.8 | 4.4 says colour capability and the 16-colour mapping need "a run on a real terminal at 16, 256 and truecolor". No step or 8.8 row schedules it; the pty test (1.6(g)) checks bytes, not a real terminal. | Add an 8.8 row or a 7.4-style optional manual check. |
| F-11 | MINOR | 3.3 title-bar row versus 2.5 and RB-15 | 3.3 target at 80 columns: the badge must not put `as of <time>` on its own line "as header1 does today". Step 2.5 leaves `header1` unedited, so the same wrap remains and RB-15 does not test it. | Reword the 3.3 target, or add an RB-15 clause for the 80-column wrap. |
| F-12 | MINOR | 8.9 row 13 versus 3.9, 4.8, 6.6 | 8.9 row 13 says "Both presentation goldens regenerated" in P2, P3, P4, P6. Steps 3.9 and 4.8 regenerate only the link-off golden; 6.6 only the release-1 golden. | Reword the row per phase. |
| F-13 | MINOR | 3.6 SC-14, 4.1b harness row, 9.2 row 15 versus 8.4/8.5 | These say the rubric and threshold are "not yet defined / not drafted". Section 8.4 writes 23 rubric rows and 8.5 G6 sets the pass rule. The open question is stale. | Mark SC-14 and row 15 as answered by 8.4/8.5 G6. |
| F-14 | MINOR | 4.1a (M-08, M-10, M-11 Critical) versus 8.4/8.10 (Medium) | Section 4 says these C8 defects are raised to Critical and "not downgraded". RB-11, RB-12, RB-13 and 8.10 label them Medium. Gating is the same (High and Medium rows block close), but the labels disagree and 8.4 has no map to the Section 4 scale. | Add a severity-scale note to 8.4. |
| F-15 | MINOR | 7.3 and 9.1 versus 8.2 | Owner decisions without a D-id in 8.2: bold and dim under NO_COLOR, RR 61 wording, PNG dependency (defaulted "no" in 7.2 Q3). D-7 (state-word colour mapping) is in 8.2 but not in 7.3 or Section 9. | Give each a D-id, or note in 8.2 which 7.3 row each D-id covers. |

### Summary

- Total findings: 15
- Critical: 0
- Important (blocking): 2 (F-1, F-2)
- Minor (notes): 13 (F-3 to F-15)
- Chains traced clean: M-01 to M-18 (Section 4 to 8.10 to phase steps), RN-1 to RN-3, G-1, G-2, AD-1 to AD-7, OPEN-1 to OPEN-3, O-1, SC-1 to SC-19, Section 5.6 subsection cites (5.1.x to 5.5.x), GAPS row cites in 7.2.
- Verification: Read 15 ranges of the report, 2 ranges of `gaps-and-questions.md`, 1 Grep for D-8/Q-n, 1 Glob of the task directory. Section 4.4 and Section 9 items were each followed to a Section 8 step or 8.8 row.
- Verdict: FAIL. Two open owner decisions are missing from the decision tables and one is assumed by a plan step (F-1, F-2). Fix those two and re-review; the minor notes need no recheck.

