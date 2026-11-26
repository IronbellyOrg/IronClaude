# Base selection (reflect UC-1, second run, quick depth)

## Scores

| Variant | Reviewer | Quant (50%) | Qual (50%, of 30) | Combined | Edge-case dimension (E) |
|---|---|---|---|---|---|
| V1 | reviewer 1, analyzer | 0.7010 | 0.7333 (22) | 0.7172 | 5/5 |
| V2 | reviewer 2, qa | 0.7474 | 0.9333 (28) | 0.8404 | 5/5 |
| V3 | reviewer 3, refactorer | 0.8487 | 0.8333 (25) | 0.8410 | 4/5 |

Quant inputs are in `scoring/quant.json`; qualitative cells are in `scoring/qual-pass1.md` (input order) and `scoring/qual-pass2.md` (reverse order). 24 of 30 cells agreed between passes. The 6 disagreements (C4 V1, K5 V3, S5 V1, L4 V2, R5 V1, E4 V1) were adjudicated by the orchestrator against both passes' quoted evidence (`scoring/final-scores.json`): C4 V1 = 1 (a verdict is stated, even though wrong), K5 V3 = 1 (the substance citations hold, only plan line numbers drifted, a form defect), S5 V1 = 0 (the four-class counts the reviewer format requires are absent), L4 V2 = 1 (defines `P`, `D`, `R`), R5 V1 = 1 (row 4 names the cases to add), E4 V1 = 1 (confirms the M-04 count and the nine patterns). The adjudication was made by the orchestrator, not by a fresh evaluator agent (disclosed deviation; it cannot change the base, see below).

Edge-case floor (1/5): all three variants pass.

## Tiebreak

V3 and V2 are within 5% (0.8410 against 0.8404). Level 1 (debate points won in Round 1 by majority of the three advocates, `scoring/round1-votes.json`): V3 won 8 points (C-002 to C-006, C-015 to C-017), V2 won 5 (C-001, C-018, C-019, X-001, X-002), V1 won 5 (C-007, C-009 to C-012). V3 wins on the quantitative layer and the tiebreak. Even with every disputed cell flipped against V3 and for V2, V3 keeps the quantitative lead and the debate lead.

## Selected base

**Variant 3 (reviewer 3, refactorer).** It carries the widest set of rows that name a defect with a plan line and a design line. Weaknesses of the base the refactor plan must repair: it misses the Task 28 no-key rule (C-001, from V2), four plan line numbers drifted (K5), it grades M-10 as resolved, and it omits the Task 17 cases, the `record-skipped` flag coupling and the test-first Constraint rows (C-007, C-009, C-010, from V1).

## Convergence

Round 1 only (quick depth). Agreement on the superior treatment: 25 of 26 diff points (0.96). The only split is S-001 (layout). No Round 2, no invariant probe (quick depth, disclosed in the contract).
