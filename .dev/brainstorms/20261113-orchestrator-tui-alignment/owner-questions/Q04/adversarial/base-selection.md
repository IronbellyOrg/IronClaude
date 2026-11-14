# Base Selection: Q4

Scoring was done inline by the orchestrating worker; both rubric passes were run by the same evaluator, so they are not independent. Requirements for the coverage metric, from `../question.md`: R1 a meaning is stated; R2 a one-line reply for CO-01; R3 the effect on Q3 is stated; R4 the effect on Q18 is stated; R5 the owner's 2026-11-08 note is treated; R6 the ledger record; R7 the statement stays true through later observer releases (A-003).

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.857 (misses R7) | 1.000 | 0.857 (misses R7) | |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | 1.000 | |
| Specificity ratio (SR) | 0.15 | 0.87 | 0.87 | 0.87 | manual estimate |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| **quant_score** | | **0.938** | **0.981** | **0.938** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Deciding evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness | 4 | 5 | 4 | Criterion 1: V2 MET; V1, V3 NOT MET (an unscoped "read-only" and host statement can become false, R7). |
| Correctness | 4 | 5 | 3 | V1 criterion 5 NOT MET ("single-host gives Q3 a clear test": the ADJ condition is "stays", conceded). V3 criterion 1 NOT MET ("planned" has no owner source; the #409 Go lineage was replaced by Python plus Rich, ADJ line 187) and criterion 5 NOT MET. |
| Structure | 4 | 4 | 4 | Criterion 4 (navigation aids): NOT MET for all. |
| Clarity | 5 | 5 | 5 | All concrete. |
| Risk coverage | 3 | 4 | 1 | Criterion 1 NOT MET for all. V3 lists risks with no mitigation or recovery (criteria 2, 3 NOT MET). Criterion 5 (detection): V2 MET (re-ask trigger when R4 or a TUIBBS task is proposed); V1, V3 NOT MET. |
| Invariant and edge-case coverage | 3 | 3 | 3 | Criteria 2, 3, 5 MET for all (Q3 and Q18 interplay; guard gaps; interactions); 1 and 4 NOT MET. |
| **Total** | **23/30 = 0.767** | **26/30 = 0.867** | **20/30 = 0.667** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2, V3 | 23, 26, 20 |
| 2 | V3, V2, V1 | 20, 26, 23 |

Disagreements: 0. Same evaluator for both passes.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| Variant 1 | 0.469 | 0.383 | 0.852 |
| Variant 2 | 0.491 | 0.433 | **0.924** |
| Variant 3 | 0.469 | 0.333 | 0.802 |

Margin Variant 2 over Variant 1: 7.2 points; no tiebreaker. Variant 2 also won the most debate points (7 against 5).

## Selected Base: Variant 2 (proposal-B)

- Selection rationale: highest combined score and most debate points; its "today" scoping is the part all three advocates adopted.
- Strengths to preserve: the meaning is separated from release properties; Q3 is not pre-decided; the owner's 2026-11-08 note stays undecided.
- Strengths to incorporate:
  1. From Variant 1 (won C-001, C-005, X-003): name the built program firmly and add the two verified present facts, "single-host and read-only today" (ADJ E-01; glossary line 77); drop "provisional" (V2 advocate concession 4).
  2. From Variant 1 (won C-004): state Q18 stays at its recommended "not yet".
  3. From Variant 3 (advocate's amended line): keep a TUIBBS screen visible as "a possible later reader, not decided".
  4. From the debate on A-001 and A-002: name "the #409 dashboard" in the line; the owner sees the exact line before it is posted in another repository.
  5. From X-002 (verified): record that the owner replaced the #409 Go direction with Python plus Rich on 2026-11-08 (ADJ line 187), so the lineage does not support a TUIBBS reading.
