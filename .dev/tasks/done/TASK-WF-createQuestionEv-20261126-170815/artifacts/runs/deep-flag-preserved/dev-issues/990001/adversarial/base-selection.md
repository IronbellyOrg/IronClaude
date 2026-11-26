# Base Selection

## Quantitative Scoring (50% weight)

Source requirements (from description.md): R1 "last line", R2 "how many skills it copied".

| Metric | Weight | Variant 1 | Variant 2 | Computation |
|---|---|---|---|---|
| RC Requirement coverage | 0.30 | 0.00 | 1.00 | V1 names neither R1 nor R2; V2 names both ("a skills count as the last line") |
| IC Internal consistency | 0.25 | 1.00 | 1.00 | no intra-variant contradiction |
| SR Specificity ratio | 0.15 | 1.00 | 1.00 | all value cells concrete; no vague terms |
| DC Dependency completeness | 0.15 | 1.00 | 1.00 | no internal references (external refs excluded) |
| SC Section coverage | 0.15 | 1.00 | 1.00 | same template, same sections |
| quant_score | | 0.70 | 1.00 | |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

| Dimension | Variant 1 | Variant 2 | Key evidence |
|---|---|---|---|
| Completeness (5) | 1 | 2 | V2 covers the requirement and states current behaviour (`main.py:271-296`); neither gives out-of-scope or success criteria |
| Correctness (5) | 3 | 5 | V1's Mode lacks support (no defect, conceded in Round 1); V2's claims check out against the code |
| Structure (5) | 4 | 4 | both follow the template; no navigation aids |
| Clarity (5) | 3 | 4 | V2's reasons are concrete and actionable |
| Risk Coverage (5) | 0 | 0 | not part of a flags decision |
| Invariant & Edge Case (5) | 0 | 0 | neither addresses the A-001 / A-002 boundaries |
| qual_score | 11/30 = 0.37 | 15/30 = 0.50 | |

### Edge Case Floor Check
Both variants score 0/5. Edge case floor suspended: no variant meets minimum coverage.

## Position-Bias Mitigation
Pass 1 (V1, V2) and pass 2 (V2, V1) gave the same verdicts; disagreements found: 0; verdicts changed: 0.

## Combined Scoring

| Variant | Quant × 0.5 | Qual × 0.5 | Score |
|---|---|---|---|
| Variant 1 | 0.35 | 0.18 | 0.53 |
| Variant 2 | 0.50 | 0.25 | 0.75 |

Margin: 22 points; no tiebreaker.

## Selected Base: Variant 2 (issue-worker-t1)

- Selection rationale: it won all four contested points in Round 1 (Variant 1's advocate conceded each) and it is the only variant with code evidence.
- Strengths to preserve: the path:line reasons on the Mode and Type rows.
- Strengths to incorporate from Variant 1: the user's flag is authoritative for filing. Both advocates said a disagreement is recorded as dissent, not applied as an override (this matches `refs/create.md` Wave 2: "The issue is filed with the user's flags when the user gave them").
- Also incorporate: the A-001 and A-002 qualifications that both advocates agreed on.
