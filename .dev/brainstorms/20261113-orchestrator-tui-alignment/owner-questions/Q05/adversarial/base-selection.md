# Base Selection: Q5

Scoring was done inline by the orchestrating worker; both rubric passes were run by the same evaluator, so they are not independent. Requirements for the coverage metric, from `../question.md`: R1 the relationship is stated; R2 the draft step (XC-05); R3 the landing step (XC-07); R4 the effect on Q9 and Q17; R5 the treatment of the #409 "one shared set of facts" proposal; R6 the join-basis handling; R7 the dependency on PR #539.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.857 (misses R3: the note's landing) | 1.000 | 1.000 | |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | 0.933 (X-002: "moving target" against "the draft could have been written now at low cost") | |
| Specificity ratio (SR) | 0.15 | 0.87 | 0.87 | 0.87 | manual estimate |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| **quant_score** | | **0.938** | **0.981** | **0.964** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Deciding evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness | 4 | 5 | 4 | Criterion 1: V2 MET; V1 NOT MET (landing of the note); V3 NOT MET (no fallback if the trigger never fires). |
| Correctness | 4 | 5 | 3 | V1 criterion 5 NOT MET (its gain, one definition on screen, does not apply in version 1 because the observer shows no sweep classes, E-06; conceded). V3 criterion 4 NOT MET (X-002) and criterion 5 NOT MET ("saves the cost if the owner prefers a panel or merge": every surviving option keeps the note; conceded). |
| Structure | 4 | 4 | 4 | Criterion 4 (navigation aids): NOT MET for all. |
| Clarity | 5 | 5 | 5 | All concrete. |
| Risk coverage | 3 | 4 | 2 | Criterion 1 NOT MET for all. Criterion 5 (detection): V2 MET (the comparison test); V1, V3 NOT MET. V3 criterion 2 (mitigation) NOT MET. |
| Invariant and edge-case coverage | 4 | 4 | 2 | V1, V2 MET on state across components, guards (age rule; candidate join basis), counts (45 seconds against 6 hours named in V2; empty panel without a coordinator in V1), interactions. V3 MET on interactions and guards only. |
| **Total** | **24/30 = 0.800** | **27/30 = 0.900** | **20/30 = 0.667** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2, V3 | 24, 27, 20 |
| 2 | V3, V2, V1 | 20, 27, 24 |

Disagreements: 0. Same evaluator for both passes.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| Variant 1 | 0.469 | 0.400 | 0.869 |
| Variant 2 | 0.491 | 0.450 | **0.941** |
| Variant 3 | 0.482 | 0.333 | 0.815 |

Margin Variant 2 over Variant 1: 7.2 points; no tiebreaker. Variant 2 also won all 12 decided debate points and was every advocate's neutral recommendation.

## Selected Base: Variant 2 (proposal-B)

- Selection rationale: highest score; unanimous debate outcome.
- Strengths to preserve: no runtime link in version 1; draft now, land after #539 and the real-id comparison; the comparison test; Q9 and Q17 at "not now".
- Strengths to incorporate:
  1. From Variant 3 (U-003): re-ask Q17 once the real-id comparison is recorded, before the note lands.
  2. From Variant 1 (U-001): if Q17 later becomes "yes", the panel reads a caller-side captured copy from the coordinator's pass and never runs the sweep.
  3. From the Variant 1 advocate: the #409 correction pass records this choice so the #409 body does not keep proposing the opposite.
  4. From Variants 1 and 2 advocates: the mapping table states each program's stale threshold, because the test guards words only.
  5. From the Variant 2 and 3 advocates: the draft may need revising if the Q1 fix or the open #539 threads change any constant it cites; the Q1 ruling is expected to change the git allow-list, not the note's contents.
