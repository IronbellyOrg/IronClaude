# Base Selection: Q2

Scoring was done inline by the orchestrating worker; both rubric passes were run by the same evaluator, so they are not independent. Requirements for the coverage metric, from `../question.md`: R1 a claim level is chosen; R2 the permission acceptance is answered; R3 the acceptance is limited to the test issue (`merged-requirements.md:572`); R4 FU-1's preconditions are named as preconditions; R5 the wording of #450 edit 1 follows; R6 the effect on the #423 clause is stated; R7 downstream effects are stated.

**Important:** the base is chosen by document score, not by which answer won the debate. Variant 2 scores highest because it is the most complete on preconditions, but it lost the core debate points (C-001, C-002, X-002, X-003) to Variant 3, 3 of 3. Step 4 therefore replaces the base's core answer with Variant 3's, as the protocol's "for each base weakness" rule requires.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.857 (misses R4: no gate named) | 1.000 | 0.857 (misses R4: item 5 only as a risk) | |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | 0.933 (X-001: "FU-1 can run" against its own risk line) | |
| Specificity ratio (SR) | 0.15 | 0.87 | 0.87 | 0.87 | manual estimate |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| **quant_score** | | **0.937** | **0.981** | **0.921** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Deciding evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness | 4 | 5 | 4 | Criterion 1: V2 MET (gates named as preconditions); V1 NOT MET (no gate); V3 NOT MET (item 5 only as a risk). |
| Correctness | 5 | 4 | 3 | Criterion 4: V3 NOT MET (X-001). Criterion 5 (claims supported): V2 NOT MET ("what an approval most plausibly wants" has no source and ADJ X-001 records the default as an accident); V3 criterion 1 NOT MET ("FU-1 can run" is false while OB-H1 item 5 is "Pending, none run", `docs/designs/sc-issue-launch-level-hook.md:625`). |
| Structure | 4 | 4 | 4 | Criterion 4 (navigation aids): NOT MET for all. |
| Clarity | 5 | 5 | 5 | All concrete, with next steps. |
| Risk coverage | 3 | 4 | 4 | Criterion 1 (probability and impact): NOT MET for all. Criterion 5 (detection): V1 NOT MET (nothing runs to observe); V2, V3 MET (FU-1 record). |
| Invariant and edge-case coverage | 3 | 5 | 4 | Criterion 1 (maximum size): V2 MET ("up to 6 new sessions a day"); others NOT MET. Criterion 4 (counts): V2, V3 MET (two sessions against one); V1 NOT MET. |
| **Total** | **24/30 = 0.800** | **27/30 = 0.900** | **24/30 = 0.800** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2, V3 | 24, 27, 24 |
| 2 | V3, V2, V1 | 24, 27, 24 |

Disagreements: 0. Same evaluator for both passes.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| Variant 1 | 0.469 | 0.400 | 0.869 |
| Variant 2 | 0.491 | 0.450 | **0.941** |
| Variant 3 | 0.461 | 0.400 | 0.861 |

Margin Variant 2 over Variant 1: 7.2 points; no tiebreaker.

## Selected Base: Variant 2 (proposal-B) as the document frame

- Selection rationale: highest combined score, driven by naming FU-1's gates as explicit preconditions and stating the per-day session ceiling.
- Strengths to preserve: the explicit precondition list; the honest "FU-1 waits until the gates pass" stance (won X-001).
- Base weaknesses to fix (debate points the base lost, 3 of 3 each): the claim level (C-001), the acceptance scope (C-002, X-003), the reading of owner intent (X-002), the code-versus-design direction (C-004, C-006). All are fixed by adopting Variant 3's answer.
- Strengths to incorporate:
  1. Variant 3's core answer: `--pipeline none`, acceptance for the one test issue only, one small watcher PR.
  2. The full FU-1 precondition list agreed by all three advocates: OB-H1 item 5 (the only ship gate that binds claim-only), the live-test grant row, Orca availability, Q20.
  3. Variant 1's A-002 point: the acceptance must say it covers whatever the one session does on the test issue, not only the listed writes; the owner may write the test issue's text to shrink the untrusted-input risk.
  4. Variant 1's U-001: FU-1 also records whether a permission-on session would be feasible, as data for later, non-test decisions.
