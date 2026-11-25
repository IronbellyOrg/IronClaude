# Merge Log

## Metadata
- Base: Variant 2 (`variant-2-original.md`, reviewer 2, qa lens, opus class), score 0.8193 against 0.7023.
- Plan: `refactor-plan.md` (this folder). Output: `../merged-review-card.md`.
- Executor: merge-executor (sc:adversarial Mode A, Step 5).
- Changes applied: 17 of 17 (Change #1 header; Changes #2-#14 the 13 rows; Change #15 adherence summary; Change #16 notes; Change #17 provenance list).
- Status: success (all post-merge checks pass; see Post-Merge Validation).
- Timestamp: 2026-11-25T19:25:00Z.
- Plan discrepancy recorded, not repaired: the plan's Overview says "Change count: 20 planned", but the plan body defines Changes #1-#17. This log counts the 17 defined changes.

## Changes Applied

### Change #1: header and path key
- Status: applied.
- Done: wrote the four provenance comments and the H1; header line with persona "merged: analyzer (V1, haiku class) and qa (V2, opus class)" and total deviations 13; kept V2's path key sentence (PLAN, SPEC, "Every other path is under ...").
- Not carried: V2's reviewer self-claim "I re-read every line number cited below", which describes the first reviewer and not the merged card. The plan said to keep V2's path key sentence only.
- Provenance: V2 header (lines 1-5 of `variant-2-original.md`), replaced per plan.

### Change #2: Row 1 (full suite and lint gate not run)
- Status: applied. Grade Blocking (Missing), HIGH. Location `PLAN:76-77, PLAN:89`. Text and evidence copied from the plan.
- Provenance: base V2 row 1, V1 row 4, C-001, U-001, INV-016, A-001.

### Change #3: Row 2 (changed launcher not on the live route)
- Status: applied. Grade Blocking (Missing), HIGH. Location `PLAN:98, PLAN:101, PLAN:22`.
- Provenance: base V2 row 2, V1 row 1, C-002, U-002, INV-014, INV-015, A-003.

### Change #4: Row 3 (Task 6 check not tied to the coordinator PID)
- Status: applied. Grade Blocking (Decision), HIGH. Location `PLAN:98, PLAN:101-102`.
- Provenance: base V2 row 3, C-005, INV-002, INV-003.

### Change #5: Row 4 (wrapper fake records more than the one switch)
- Status: applied. Grade Blocking (Decision), HIGH. Location `PLAN:60, PLAN:66, PLAN:26`.
- Provenance: base V2 row 5, U-003, INV-018.

### Change #6: Row 5 (raw-resume cases missing)
- Status: applied. Grade Blocking (Missing), HIGH. Location `PLAN:60, PLAN:63`.
- Provenance: V1 row 3, V2 rows 12-13, C-004, U-006, INV-008, INV-011, INV-012.

### Change #7: Row 6 (help header line placed where `--help` never prints it)
- Status: applied. Grade Medium, MEDIUM. Location `PLAN:46, PLAN:51-52`. Judge ruling text kept.
- Provenance: V1 row 2, V2 row 4, C-003, X-001, INV-017; judge ruling.

### Change #8: Row 7 (tab-reopen execs missing from the route trace)
- Status: applied. Grade Medium, MEDIUM. Location `PLAN:33`.
- Provenance: V2 row 11, U-007.

### Change #9: Row 8 (line numbers go stale after Task 2)
- Status: applied. Grade Medium, MEDIUM. Location `PLAN:33, PLAN:38, PLAN:46`.
- Provenance: probe INV-009.

### Change #10: Row 9 (`verify-sync` needs `uv` and `jq`)
- Status: applied. Grade Medium, MEDIUM. Location `PLAN:89`.
- Provenance: probe INV-004.

### Change #11: Row 10 (Ruff wording says two files, commands are repo-wide)
- Status: applied. Grade Medium, MEDIUM. Location `PLAN:77`.
- Provenance: probe INV-016.

### Change #12: Row 11 (`git status` check cannot see ignored mirror files)
- Status: applied. Grade Note, LOW. Location `PLAN:89`.
- Provenance: V2 row 7, U-005.

### Change #13: Row 12 (spec relative links unresolved in the package)
- Status: applied. Grade Note, LOW. Location `SPEC:37-38`.
- Provenance: V1 Notes, U-011.

### Change #14: Row 13 (count correction: 21 or 24 test files, not 16)
- Status: applied. Grade Note, LOW. Location `reviewer-2-card.md row 1`.
- Provenance: V2 row 1, U-010, INV-007; correction.

Notes for Changes #2-#14: each row uses the plan's text with the grade prefix in bold added at the start of "What diverged" (the plan gives the grade in the row header). The plan's quote-escaping `\"` in Row 9 was written as a plain `"` inside the backticks. No cell contains a pipe character, so no `\|` escape was needed. Evidence cells and "What diverged" texts were compared by script with the plan's Evidence and What diverged lines: all 13 evidence cells identical; all 13 texts identical apart from the added grade prefix.

### Change #15: Adherence summary
- Status: applied. Units 42; 7 rows not counted; of the other 35, 29 adherent and 6 not (INF-041 row 1; INF-002, INF-004, INF-009 rows 2 and 3; INF-023 row 5; `SPEC:25` row 4); category counts with Drift 13 rows (5 Blocking, 5 Medium, 3 Note); statement that unit counts are not finding counts. Laid out as a bullet list.
- Provenance: replaces V2's summary, recounted per plan.

### Change #16: Notes
- Status: applied. Verdict FAIL (rows 1-5 Blocking), confidence 0.80, judge ruling, confirmed correct (with "16 test files" removed), not verified, probe warnings carried, dismissals kept, reviewer metadata, coverage. The judge-ruling bullet adds a short parenthetical with the reason from row 6 (the plan says "reason above").
- Provenance: V2 Notes rewritten per plan; V1 Notes (dismissals, metadata); debate; invariant probe.

### Change #17: Provenance list
- Status: applied. Four provenance comments at the top; section `## Provenance of rows` with one bullet per row (13 bullets). Rows 8, 9 and 10 have no base row (probe-sourced); row 12 has no V2 row (V1 Notes).
- Provenance: new section.

## Post-Merge Validation
Run by Reading the merged card back and by script counts.

1. Heading hierarchy: PASS. One H1 (`# Reflect Reviewer — Merged Deviation Findings`), then four H2 sections (Deviations, Adherence summary, Notes, Provenance of rows). No H3 or deeper, no skipped level.
2. Table shape: PASS. 13 data rows numbered 1-13, each with 6 cells (7 pipe separators per line, none escaped, none inside a cell).
3. Row references: PASS. References inside the card are "fix to row 1" (row 9), "evidence for row 1" (row 13), and in Notes and the adherence summary rows 1-6, 8, 9, 10, 13 and "rows 2 and 3", all existing rows. Two items are not card-row references and were left as copied: Row 13's Location `reviewer-2-card.md row 1` (a row of the other card) and Notes "V2 row 6" (a row of variant 2, labelled as such).
4. Grade counts: PASS. 5 rows start with `**Blocking` (rows 1-5: rows 1, 2 and 5 are Missing, rows 3 and 4 are Decision), 5 with `**Medium:**` (rows 6-10), 3 with `**Note:**` (rows 11-13). The adherence summary states 5 Blocking, 5 Medium, 3 Note; Notes state "rows 1-5 are Blocking" and row 6 Medium. Same counts.
5. Verdict against rows: PASS. Verdict FAIL is consistent with five Blocking rows; no row or note says pass or conditional pass.
6. Evidence cites: PASS. All 13 Evidence cells are identical to the plan's Evidence lines (script comparison, no differences).

Result: pass, no failures.

## Summary
- Planned: 17
- Applied: 17
- Failed: 0
- Skipped: 0
- Plan discrepancy noted (Overview says 20 changes, body defines 17); no plan content was altered.
