# Base Selection: Q8 owner-answer proposals

Scored by the orchestrating session (not an advocate). Variant 1 = A, 2 = B, 3 = C.

## Quantitative Scoring (50% weight)

Requirement set (question.md and the gate on master): R1 names the staged direction; R2 gives the owner's "production integration" reading; R3 names the command; R4 owner-written (`release-gates.md:22`); R5 handles BC-18 (the #409 status line for criterion 1); R6 unblocks OB-02 for release 3; R7 covers the gate's field list (`acceptance-tests.md:70`).

| Metric | Weight | A | B | C | Computation note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.43 | 0.43 | 0.86 | A: R4, R5, R7 (later); B: R1, R5, R6; C: all but R7 |
| Internal consistency (IC) | 0.25 | 1.00 | 1.00 | 0.92 | C: "met by the owner's record" against "documents rather than precedes the decision" |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.90 | 0.90 | Estimated; all cite lines and files |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All references resolve |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | Five of five |
| **quant_score** | | **0.814** | **0.814** | **0.923** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (condensed CEV)

| Dimension | A | B | C | Evidence (short) |
|---|---|---|---|---|
| Completeness | 3 | 4 | 4 | A leaves the reading and direction unconfirmed; B and C miss parts of the gate field list (C admits it) |
| Correctness | 4 | 3 | 4 | B treats the 2026-11-08 record as owner evidence, but its line 3 says it was "Recorded by an Orca worker"; and amending the issue text leaves `release-gates.md:22` and `acceptance-tests.md:70` unmet |
| Structure | 4 | 4 | 4 | Same template |
| Clarity | 4 | 4 | 5 | C's next step is one paragraph in the owner's words |
| Risk | 3 | 4 | 4 | A: no mitigation for an undated deferral |
| Invariant and edge cases | 2 | 3 | 3 | B and C name the gate-field gap; A names the reading-dependent status line only implicitly |
| **Total of 30** | **20** | **22** | **24** | |
| **qual_score** | **0.667** | **0.733** | **0.800** | |

Edge-case floor: A 2, B 3, C 3; all eligible.

## Position-Bias Mitigation

Pass 1 order A, B, C; pass 2 order C, B, A. One disagreement: B, Completeness "dependencies" (pass 1: 1, it names Q7; pass 2: 0, it does not plan the gate-file change). Re-evaluated: 1 (the dependency on Q7 is named; the gate change is scored under Correctness). Verdicts changed: 0.

## Combined Scoring

| Variant | quant x 0.5 | qual x 0.5 | Score |
|---|---|---|---|
| A | 0.407 | 0.333 | 0.740 |
| B | 0.407 | 0.367 | 0.774 |
| C | 0.462 | 0.400 | 0.862 |

Margin C over B: 0.088 (more than 5%); tiebreaker not applied.

## Selected Base: Variant 3 (proposal C)

- Selection rationale: highest combined score, won 8 of 10 points, chosen by all three advocates.
- Strengths to preserve: an owner-written dated record; criterion 1 unchanged; the owner's own reading of "production integration".
- Strengths to incorporate: from A, the explicit deferral of release-3 fields and the honest interim BC-18 line; from B, citing the 2026-11-08 and 2026-11-11 decisions as background; from C's own advocate, an honest status line that says the record was written after releases 1 and 2 shipped.
