# Base Selection Report (Q30)

Scored by the orchestrating worker in-context. Requirements used for coverage (6): (1) meets OB-04 (1) (`merged-requirements.md:252`); (2) produces the record OB-06 (c) links; (3) puts no real question at risk; (4) the read happens while a question is pending (diagnostic); (5) names a loss-detection method that does not itself consume; (6) no `run-use`.

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (proposal-A) | V2 (proposal-B) | V3 (proposal-C) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.667 (4/6; no record, not diagnostic) | 0.333 (2/6) | 0.667 (4/6; read after the cycle, no detection method) |
| internal_consistency | 0.25 | 1.00 | 0.90 ("quiet moment" removes the pending question its own detection step needs) | 1.00 |
| specificity_ratio | 0.15 | 0.85 | 0.85 | 0.85 |
| dependency_completeness | 0.15 | 1.00 | 1.00 | 1.00 |
| section_coverage | 0.15 | 1.00 | 1.00 | 1.00 |
| **quant_score** | | **0.878** | **0.753** | **0.878** |

## Qualitative Scoring (50% weight)

| Dimension | V1 | V2 | V3 | Decisive evidence |
|---|---|---|---|---|
| Completeness | 3/5 | 3/5 | 4/5 | V3 alone covers setup, acceptance, record and teardown |
| Correctness | 5/5 | 3/5 | 4/5 | V2 conflicts with OB-04 (1); V3's step order makes the read non-diagnostic |
| Structure | 5/5 | 5/5 | 5/5 | identical |
| Clarity | 4/5 | 4/5 | 4/5 | ids glossed only partly |
| Risk coverage | 2/5 | 2/5 | 4/5 | V3 names setup, representativeness and person-opened limits |
| Invariants and edge cases | 2/5 | 2/5 | 3/5 | V3 handles the listener and acknowledgement cycle |
| **qual_score** | **21/30 = 0.700** | **19/30 = 0.633** | **24/30 = 0.800** | |

## Position-Bias Mitigation
Pass 1 (V1, V2, V3) and pass 2 (V3, V2, V1) by the same in-context scorer, not independent. Re-checked V3 correctness (kept 4/5, step-order gap conceded by its own advocate). Disagreements: 0.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final** | Debate points |
|---|---|---|---|---|
| V1 | 0.439 | 0.350 | **0.789** | 1 |
| V2 | 0.376 | 0.317 | **0.693** | 1 |
| V3 | 0.439 | 0.400 | **0.839** | 5 |

Margin V3 over V1: 6.3% (above 5%). Tiebreaker: no.

## Selected Base: Variant 3 (proposal-C)

### Selection Rationale
Highest score, 5 debate points, and all three advocates' overall pick.

### Strengths to Preserve
1. A disposable Run opened by the owner, never the program's own; written acceptance; `GRANT(OB-04,live-read)`; teardown.

### Strengths to Incorporate
1. From V2 and V3 advocates: read while the test question is still pending.
2. From V2: before-and-after comparison, grounded in the known planted question and the coordinator's `--wait` delivery, never a plain `check`.
3. From V1: a holder-terminal preflight, and hold (V1) as the written fallback if OB-03 fails, the preflight fails or Orca does not answer.
