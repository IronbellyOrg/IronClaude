# Base Selection

Scoring was done inline by the orchestrator (no separate judge agent). Source requirements for RC are the 62 inferred rows of `artifacts/coverage-matrix.json`; a card "matches" a row when it lists the row in `rows_observed`.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) | Computation |
|---|---|---|---|---|---|
| RC requirement coverage | 0.30 | 0.32 | 0.37 | 0.29 | rows_observed / 62 (20, 23, 18) |
| IC internal consistency | 0.25 | 0.80 | 0.70 | 0.80 | 1 - contradicted claims / claims: V1 one false claim ("no Tasks 3 and 4 row lacks a criterion"); V2 an overstated MAJOR, a mostly false F2 and F9 withdrawn; V3 an overstated MAJOR |
| SR specificity ratio | 0.15 | 0.95 | 0.95 | 0.95 | all findings carry line ranges and quotes |
| DC dependency completeness | 0.15 | 1.00 | 0.87 | 1.00 | resolved citations / citations: precheck flagged 4 `quote-not-found` citations, all in V2 (spec 369, 280, 270, 268) |
| SC section coverage | 0.15 | 1.00 | 1.00 | 1.00 | same sections in all three cards |
| **quant_score** | | **0.7385** | **0.7090** | **0.7295** | RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15 |

## Qualitative Scoring (50% weight): 30-criterion additive binary rubric

Criteria were adapted to an audit card (a card is the artifact under comparison). MET needs a quoted evidence line; no evidence means NOT MET.

| Dimension (5 criteria each) | V1 | V2 | V3 | Evidence for the differences |
|---|---|---|---|---|
| Completeness | 2 | 4 | 2 | V2 covers acceptance gaps across Tasks 3, 4, 6, 7, 9 to 12; V1 and V3 hold two findings each |
| Correctness | 4 | 3 | 4 | V2 has four wrong spec lines and an overstated blocker; V1 one false note; V3 an overstated blocker |
| Structure | 5 | 5 | 5 | header, findings block, self-report, notes in each |
| Clarity | 4 | 4 | 4 | |
| Risk coverage | 2 | 3 | 2 | V2 lists consequences per gap (auto-merge not surfaced, PR-body gate may not reach the PR) |
| Invariant and edge-case coverage | 1 | 3 | 1 | V2 F7, F10, F12 probe first-skip state, idempotency in both directions and the CI cycle |
| **Total / 30** | **18** | **22** | **18** | |
| **qual_score** | **0.600** | **0.733** | **0.600** | |

### Edge Case Floor Check
All three variants score at least 1 of 5 on Invariant and Edge Case Coverage, so all are eligible as base.

## Position-Bias Mitigation
Pass 1 (order V1, V2, V3) and pass 2 (order V3, V2, V1) were both run inline by the orchestrator, not by independent agents. No criterion changed between passes (disagreements found: 0, verdicts changed: 0).

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Final |
|---|---|---|---|
| V1 | 0.3693 | 0.3000 | 0.6693 |
| V2 | 0.3545 | 0.3667 | 0.7212 |
| V3 | 0.3648 | 0.3000 | 0.6648 |

Margin between the top two: 0.0519 (above the 0.05 tiebreaker band); tiebreaker applied: No.

## Selected Base: Variant 2 (reviewer-2 card, qa lens, Haiku class)

- **Rationale:** the highest combined score (0.7212) comes from breadth: 12 findings that read plan criteria against spec rows. Its lower quantitative score comes from four mis-lined spec citations, which the merge corrects.
- **Strengths to preserve:** F3, F4, F7, F8, F10, F11, F12 (verified TRUE as MINOR gaps in the debate); the per-criterion method.
- **Strengths to incorporate from non-base variants:** V1 F2 (Task 8 omits spec 4.2 and 4.4) and V1's severity call on the Wave 0 bullet; V3 F1 (cycle-id minting) at MINOR and V3 F2 (dependency of Task 12); Round 2 and probe items listed in `refactor-plan.md`.
- **Weaknesses of the base to fix:** F1 severity MAJOR blocking (all three advocates and the debate settle on MINOR); F2, F5 and F9 (mostly false, weak, withdrawn); four wrong spec line numbers (333, 234, 232 replace 369, 270, 268; F5 is dropped).
