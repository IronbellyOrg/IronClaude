# Base Selection (hybrid scoring)

Inputs: three review cards (V1 reviewer-1 analyzer/sonnet, V2 reviewer-2 qa/haiku, V3 reviewer-3 refactorer/opus), the debate (Round 1, Round 2) and the per-criterion passes in `scoring/`. All numbers below come from `scoring/quant.json`, `scoring/qual-pass1.md`, `scoring/qual-pass2.md`, `scoring/qual-reeval.md` and `scoring/final-scores.json`.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 | V2 | V3 | How computed |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.6667 | 0.5833 | 0.6667 | share of the 24 content topics (C-001..C-024) the card raised (`-` cells of the diff analysis count as not raised) |
| Internal consistency (IC) | 0.25 | 0.8125 | 0.7000 | 0.8125 | 1 - (claims shown false or contradicted by the calibrators and the debate / table rows); false-claim counts V1 3 (row 6 line number, row 14 `hooks_path`, Regression count in the summary), V2 3 (40-line cap "no instruction", FR-109 "covered", NFR-014 "covered"), V3 3 (Task 27 listed under a test failure, row 9 label, NFR-014 "covered") |
| Specificity ratio (SR) | 0.15 | 1.0000 | 0.9960 | 1.0000 | concrete indicators (file:line, ids, symbols) over concrete plus vague words |
| Dependency completeness (DC) | 0.15 | 1.0 | 1.0 | 1.0 | every "row N" reference resolves inside the card |
| Section coverage (SC) | 0.15 | 0.6 | 1.0 | 0.8 | H2 sections over the maximum (5) |
| **quant_score** | | **0.7931** | **0.7994** | **0.8231** | |

## Qualitative Scoring (50% weight): 30-criterion additive binary rubric

Two independent passes (forward order V1, V2, V3 and reverse order V3, V2, V1), each criterion MET or NOT MET with evidence (full cell evidence: `scoring/qual-pass1.md`, `scoring/qual-pass2.md`). Totals: pass 1 = 25 / 19 / 25, pass 2 = 23 / 22 / 26. The passes disagreed on 9 of 90 cells (C3 V2, C4 V1, K4 V3, K5 V2, L1 V3, L5 V1, R3 V2, R5 V2, E4 V2); a third evaluation with both pieces of evidence settled them (`scoring/qual-reeval.md`): finals 1, 1, 0, 1, 0, 1, 1, 1, 1.

| Dimension (5 criteria each) | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5 | 5 | 4 |
| Correctness | 2 | 2 | 3 |
| Structure | 5 | 5 | 5 |
| Clarity | 4 | 2 | 3 |
| Risk coverage | 4 | 4 | 5 |
| Invariant and edge-case coverage | 5 | 5 | 5 |
| **Total (of 30)** | **25** | **23** | **25** |
| qual_score | 0.8333 | 0.7667 | 0.8333 |

Edge-case floor (at least 1 of 5 on the invariant dimension): all three variants pass.
Position-bias log: 9 disagreements (10 percent of cells), 4 verdicts changed from pass 1 (all on V2: K5, R3, R5, E4 moved from 0 to 1).

## Combined Scoring

| Variant | quant (x0.50) | qual (x0.50) | variant_score |
|---|---|---|---|
| V1 | 0.7931 | 0.8333 | 0.8132 |
| V2 | 0.7994 | 0.7667 | 0.7830 |
| V3 | 0.8231 | 0.8333 | **0.8282** |

Margin V3 over V1: 0.0150 (within the 5 percent band), so the tiebreaker applies.

Tiebreaker level 1, debate performance (points won in the final per-point tally, `scoring/round2-votes.json`, 37 of 37 agreed): V3 11 (S-002, C-002, C-003, C-008, C-009, C-010, C-014, C-016, C-017, X-003, X-004), V1 9 (S-003, C-011, C-013, C-015, C-018, C-019, C-024, X-001, X-002 and the A-points do not count), V2 6 (S-001, C-012, C-020, C-021, C-022, C-023); 11 against 9 is a clear win for V3. (Level 2, correctness criteria met, also favors V3: 3 against 2.) Tiebreaker applied: yes, level 1.

## Selected Base: Variant 3 (opus:refactorer, reviewer-3 card)

Selection rationale: highest combined score (0.8282) and the most debate points won (11); its blocking defects are the ones the debate confirmed as halting the executor (plugin-copy timing, the `_TRANSIENT` reason pin, the ledger header and archive lines, the unconditional reconcile).

Strengths to preserve: executability lens (which existing test fails and where), the repair list of 13 fixes (Round 2, advocate 3), the advisory correctness gap about the allow-list.

Strengths to incorporate from the non-base variants:
- From V1: the `skipped` settlement with no action (C-011, Blocking), NFR-014 stop-on-prompt half (C-013, Medium), seven-vs-five refusal tokens (C-018), `origin/integration` fragility with a merge-base fix (C-019), the SKILL.md growth budget (C-017).
- From V2: the missing T-04 and T-21 executor-side cases (C-012, Blocking by majority), person-only commit authority assertion (C-021, Medium), the test-first order (C-020, Medium), field-level helper assertions (C-022, Note), 40-line refusal-log assertion (C-023, Note).
- From the debate (all three advocates): the Constraint 24 versus Task 38 contradiction resolved as "each task copies its own plugin files, Task 38 only verifies" (X-006), and the DD-8 / T-16 conflicts with needed fixes recorded as explicit overrides (A-003).

Calibration weights carried into the merge: card 1 C = 0.82, card 2 C = 0.79, card 3 C = 0.84.
