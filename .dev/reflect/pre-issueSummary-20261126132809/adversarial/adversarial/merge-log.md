# Merge Execution Log

## Metadata
- Base: Variant 2 (opus:qa)
- Executor: merge-executor
- Changes applied: 8 of 8
- Status: success
- Timestamp: 2026-11-26

## Changes Applied

### Change 1: Re-grade every Variant B row by the caller's rule
- Status: Applied
- Applied: the merged table carries the final grades from the plan's Target text (rows M-01 and M-04 to M-13 as given there; M-14 to M-18 Note; V2 rows 17-18 appear only in the Dropped section).
- Provenance: Variant 2 rows 1-18, per the plan's Target text.

### Change 2: Merge the overlapping findings
- Status: Applied
- Applied: M-01, M-02 and M-07 carry the combined source cells naming V1 finding 1, 2 and 3 with V2 rows 4, 5 and 8 (copied verbatim).
- Provenance: Variant 1 findings 1-3 merged into Variant 2 rows 4, 5, 8.

### Change 3: Fold V1's unique observation into M-01 and M-04
- Status: Applied
- Applied: the PLAN:81 admission appears in M-01; the unresolved SPEC:32-33 links appear in M-04 (verbatim target text).
- Provenance: Variant 1 observation.

### Change 4: Merge V2 row 6 halves into one open Safety item (M-03)
- Status: Applied
- Applied: M-03 is one row graded "Blocking (Safety), open: unverified" with the widened fix.
- Provenance: Variant 2 row 6; Round 2.5 INV-003, INV-004.

### Change 5: Widen the fixes for M-01 and M-02
- Status: Applied
- Applied: the widened fix cells of M-01 and M-02 are present as given in the Target text.
- Provenance: Round 2.5 INV-005, 006, 007, 012.

### Change 6: Add M-13 and M-18
- Status: Applied
- Applied: rows M-13 (Medium) and M-18 (Note) are present.
- Provenance: Round 2.5 INV-008 and INV-018.

### Change 7: Keep V2 row 9 at Medium (M-09)
- Status: Applied
- Applied: M-09 is graded Medium.
- Provenance: Variant 2 row 9; Round 2.5 INV-017.

### Change 8: Add the Dropped or downgraded findings section and the counts line
- Status: Applied
- Applied: the "## Dropped or downgraded findings" section (11 bullets) and the line `finding_counts: blocking 3, medium 10, note 5` are present.
- Provenance: plan Target text.

## Post-Merge Validation

### Structural integrity
- Verbatim check: lines 63-101 of the plan and lines 13-51 of the merged file compared with diff: identical.
- Heading hierarchy: one H1 (line 5) and one H2 ("Dropped or downgraded findings", line 36); no skipped levels. The three provenance comments are lines 1-3.
- Table: 18 data rows (M-01 to M-18), each with exactly 9 cells (checked by counting `|` separators per row; the plan's own rows show the same count of 9). Result: pass.

### Internal references
- M-nn ids mentioned outside the id column: 10 in the Dropped section (M-01, M-03, M-04 x2, M-05 x2, M-06, M-07, M-09, M-15) and 3 inside other rows (M-01 x2, M-02 x1).
- Total: 13; resolved: 13; broken: 0.

### Contradiction re-scan
- Counts line says blocking 3, medium 10, note 5. Grades counted in the table: Blocking 3 (M-01, M-02, M-03), Medium 10 (M-04 to M-13), Note 5 (M-14 to M-18). Match: yes.
- No contradiction found between the table and the Dropped section on grades (M-07 Medium, M-04 to M-06 Medium, M-03 Blocking, M-09 Medium all agree).

## Summary
All 8 planned changes are in the merged card at `/home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/reflect/pre-issueSummary-20261126132809/adversarial/merged-reviewer-card.md`. The Target text was copied byte for byte (diff identical). No validation failure. Nothing was added, removed or reworded.
