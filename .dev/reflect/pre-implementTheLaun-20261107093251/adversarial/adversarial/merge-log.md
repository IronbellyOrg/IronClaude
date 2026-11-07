# Merge Log

Base: variant-3-original.md. Plan: refactor-plan.md. Output: ../merged-review.md. No input file was edited.

## Planned changes

1. Change 1 (reclassify V3 findings 1 and 2 as one Drift HIGH; add INV-004 and INV-002): applied. Merged into row 1 (Drift, HIGH, source V3, INV-004, INV-002); the V3 correctness gap (FakeOrca.env leakage) is folded into row 1 and cross-referenced under Advisory. The "becomes Regression if executed unchanged" flag is in row 1's text, as the plan asks; the Category stays Drift.
2. Change 2 (downgrade V3 finding 3 to an advisory note): applied. First bullet of "Advisory (non-gating)" keeps "record the consequence before implementing"; V3 row 3 is not in the table.
3. Change 3 (Task 1 gate finding, MEDIUM Drift, V1 #1 + V2 #1 + V3 #11): applied. Row 2, with the live_probe.py point from V3 #11 and the OB-H1 ordering point from V2 #1. V2's HIGH Regression is not used (see "Changes NOT made").
4. Change 4 (ownership predicate, MEDIUM Drift, escalate through INV-001): applied. Row 3 (MEDIUM, source V3, V1, V2, INV-001) with V2's negative cases and V1's marker repair; INV-001 is listed as HIGH in "Unaddressed invariants carried forward". The row stays MEDIUM as the plan says.
5. Change 5 (Task 19/20 status, MEDIUM Drift, V1 #5 + V2 #6 + V3 #5): applied. Row 4, wrong on the owned branch.
6. Change 6 (matcher-ineffective registrations and adapter prerequisites, MEDIUM): applied. Rows 5 and 6 (V2 #3, #4).
7. Change 7 (INV-005, INV-006, INV-009, INV-003 as MEDIUM rows): applied. Rows 7, 8, 9, 10. Note: row 8 also carries V1 #7 (same finding, LOW in V1, listed in base-selection.md as a V1 strength to incorporate); the plan severity MEDIUM is used and the V1 difference is stated in the row.
8. Change 8 (coverage findings V2 #2, #8, #9): applied. Rows 13, 14, 15.
9. Change 9 (V3 remaining rows, V1 LOW items, INV-007, INV-008, INV-010): partly applied. Applied: V3 enforcement_hook (row 11), Task 3 ids (row 12), scope constraint (row 18), Task 22 skips (row 19); V1 Task 12 dependency (row 21), IR-3 (row 23), issue.md (row 24), superclaude.* forms (row 25), session-id source (row 26), leaks pinned (row 27); INV-007 (row 20), INV-008 (row 22), INV-010 (row 17). Also applied: V3 #8 (IR-5 re-claim duplicates la2, row 16) as a V3 "remaining row", although the plan's parenthetical does not name it. Not applied: V1 #13 (T-REG-3 negatives), V1 #15 (Task 20 forward reference to Task 21), V1 #16 (no OB-CTX probe) and V1 #6 as a separate row, because the plan does not name them; the V1 #6 test-fallout part is covered by row 1 and its installer-list lead is kept under evidence limits. Orchestrator may want to confirm these omissions.
10. Change 10 (keep checked-and-correct, Advisory A, correctness gaps; add V1 Task 12 Necessary note and IR-7 Authorized note): applied. "Checked and correct" holds V3's list plus the two V1 notes (labelled Necessary deviation and Authorized expansion, as notes, not rows); Advisory holds Advisory A and the correctness gaps (V3 and V1).

Plan exclusions honoured (not applied): C-006 (V2 finding 7, Task 21 drops L2 on GO) withdrawn; C-001 V2 HIGH Regression not used; X-001 V3 HIGH Drift not used; S-002 "LOW-MEDIUM" replaced by LOW (row 21); A-002 V2 REJECT not used, the review states predictions as predicted.

## Post-merge check

- Heading structure intact: one H1 and six H2 sections (Verdict, Findings, Checked and correct, Advisory (non-gating), Not confirmed / evidence limits, Unaddressed invariants carried forward); two provenance comments precede the H1. Result: pass.
- Every row has a Source tag: all 27 rows carry V1, V2, V3 or INV-nnn (awk check, no row missing). Result: pass.
- Every Evidence cell non-empty: 27 of 27 rows have 8 non-empty cells (awk check). Citations were copied from the cards and the probe; two additions from debate files (PLAN:51-55 and PLAN:24 and DESIGN:506 in row 2) are marked "debate" in the cell. Result: pass.
- No row uses Regression: categories in the table are all Drift. The word appears twice in prose (the verdict's "No row is a Regression" and the row 1 flag "becomes Regression if the plan is executed unchanged"), as the plan requires. Result: pass.
- Count of rows by severity: HIGH 1, MEDIUM 14, LOW 12, total 27.
- Contradictions between rows (reported, not fixed):
  1. Row 3 is MEDIUM but cites INV-001, which the carried-forward section lists as HIGH. Deliberate in the plan (C-002 MEDIUM; INV-001 blocks convergence); the two levels are not reconciled.
  2. Row 8 is MEDIUM (plan, from the probe) while V1 rated the same finding LOW; the row states both.
  3. "Checked and correct" says "--pipeline none never reaches the launch step" (V3) while row 8 says the plan's test of it is not testable at script level; these agree on the fact and differ on whether it is a defect (the checked item is about the script, row 8 about the plan's test).
  4. INV-002 and INV-004 have probe severities MEDIUM and LOW but are folded into row 1, which is HIGH.
  5. Row 1 text says the owned-L2 migration is needed, while V3's original "no fixture adds an owned L2 hook" was conceded as too strong in Round 1; row 1 uses the weaker wording, and the Task 20 owned case is the subject of rows 3 and 4.
