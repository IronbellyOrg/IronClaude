# Base Selection: Q3

Scoring was done inline by the orchestrating worker; both rubric passes were run by the same evaluator, so they are not independent. Requirements for the coverage metric, from `../question.md`: R1 a fate for the issue is chosen; R2 the send-route stance is stated (checklist item 9); R3 the Q4 one-liner is included; R4 the posting protocol (after #450, before #409, fresh `updatedAt`, grant row); R5 text readiness and placeholders; R6 the effect on the #423 clause; R7 the nine-item checklist addressed.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 | Variant 2 | Variant 3 | Note |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.000 (7/7) | 0.571 (4/7: no Q4 line, no posting protocol, no #423 clause) | 0.714 (5/7: no #423 clause, no checklist) | |
| Internal consistency (IC) | 0.25 | 1.000 | 1.000 | 1.000 | |
| Specificity ratio (SR) | 0.15 | 0.87 | 0.87 | 0.87 | manual estimate |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | |
| **quant_score** | | **0.981** | **0.852** | **0.895** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric

| Dimension | V1 | V2 | V3 | Deciding evidence (CEV, condensed) |
|---|---|---|---|---|
| Completeness | 5 | 4 | 4 | Criterion 1: V1 MET; V2, V3 NOT MET (see RC gaps). |
| Correctness | 5 | 4 | 4 | V2 criterion 5 NOT MET ("lines up with a future orchestrator of orchestrators": "v2" has at least three meanings, ADJ line 294; conceded). V3 criterion 1 NOT MET ("text C paste-ready" while it holds a link placeholder, ADJ line 661; conceded). |
| Structure | 4 | 4 | 4 | Criterion 4 (navigation aids): NOT MET for all. |
| Clarity | 5 | 5 | 5 | All concrete. |
| Risk coverage | 4 | 4 | 3 | Criterion 1 NOT MET for all. Criterion 5 (detection): V1 MET (per-read audit and checklist tests in CO-03); V2 MET (audit); V3 NOT MET. |
| Invariant and edge-case coverage | 3 | 5 | 2 | V2 MET on collection boundaries (a listener cannot start a stopped workspace), counts (rate caps) and cross-component state (separate credentials). V1 MET on state across components (naming must match the contract note), guards, interactions; NOT MET on boundaries and counts. V3 MET on guards and interactions only. |
| **Total** | **26/30 = 0.867** | **26/30 = 0.867** | **22/30 = 0.733** | |

Edge-case floor: all eligible.

## Position-Bias Mitigation

| Pass | Order | Result |
|---|---|---|
| 1 | V1, V2, V3 | 26, 26, 22 |
| 2 | V3, V2, V1 | 22, 26, 26 |

Disagreements: 0. Same evaluator for both passes.

## Combined Scoring

| Variant | 0.5 x quant | 0.5 x qual | Combined |
|---|---|---|---|
| Variant 1 | 0.491 | 0.433 | **0.924** |
| Variant 2 | 0.426 | 0.433 | 0.859 |
| Variant 3 | 0.448 | 0.367 | 0.814 |

Margin Variant 1 over Variant 2: 6.5 points; no tiebreaker. Variant 1 also had the most outright debate wins (tied with Variant 3) and the advocates' 2-of-3 neutral recommendation.

## Selected Base: Variant 1 (proposal-A, narrow)

- Selection rationale: highest combined score; complete on requirements; 2 of 3 advocates recommended it.
- Strengths to preserve: no session-start route; answers the owner's alignment comment; CO-02 placeholders; checklist as test requirement.
- Strengths to incorporate:
  1. From Variant 3 (won X-001, X-003, A-003): a named condition under which close is the right answer instead (owner's Q4 answer states single-host is lasting and Q18 confirms no TUIBBS or remote reader planned), using text C with its reopen conditions.
  2. From the debate (V1 concession 6; A-001): say plainly that narrowing replaces the issue's problem statement, because the written body served only the watcher.
  3. From Variant 3 concession 3 and A-002: each post needs its own grant row naming each write (including a state change if closing); text C's link placeholder must be fixed before any close.
  4. From the V3 advocate's note on CO-02: reconcile text A's "writes nothing" criterion with its per-read audit line (already CO-03 (5) in the spec).
  5. From Variant 2 (U-002 via ADJ Part 6.3): text B's guards stay recorded for a future revisit; nothing is lost by not keeping routing now.
