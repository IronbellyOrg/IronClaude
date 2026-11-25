# Base selection

Scoring was done by the orchestrator (sonnet class), which is a different class from both debaters (opus and haiku). The position-bias pass was done by the same orchestrator in both orders, so it is not an independent second judge; this is stated here instead of claiming independence.

## Quantitative Scoring (50% weight)

Source requirements for RC are the five agreed finding groups of the consensus: (g1) classification entry, (g2) failure precedence, (g3) ordering test, (g4) later-STOP reporting, (g5) wording traps and housekeeping. SR, IC and DC are estimates from reading the cards (not a mechanical count); only RC, IC and SC were counted exactly.

| Metric | Weight | Variant 1 | Variant 2 |
|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.80 (g1, g2, g4, g5; misses g3) | 0.60 (g1, g3, and Q3 in g5; misses g2, g4) |
| Internal consistency (IC) | 0.25 | 1.00 (0 contradictions found) | 1.00 (0 found) |
| Specificity ratio (SR, estimated) | 0.15 | 0.97 | 0.95 |
| Dependency completeness (DC) | 0.15 | 1.00 (every cited path:line resolved when read) | 1.00 |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 |
| **quant_score** | | **0.9355** | **0.8725** |

## Qualitative Scoring (50% weight): additive binary rubric

Each MET has a quote or finding id as evidence; no evidence defaults to NOT MET.

| Dimension | Variant 1 | Variant 2 | Evidence (shortest) |
|---|---|---|---|
| Completeness (5) | 4 | 3 | V1 covers failure and test-reader cases (A1, A2, A4 to A6); neither states what is out of scope; V2 has no edge cases beyond Q1 to Q3 |
| Correctness (5) | 5 | 4 | V1's one unverified claim (gh error output) was later verified by probe; V2's Q2 label "Blocking (Decision)" was conceded wrong in Round 1 and Round 2 |
| Structure (5) | 5 | 4 | both use id, grade, claim, evidence; V2 has no list of what was checked |
| Clarity (5) | 5 | 4 | V2's Q3 gives no concrete rows to add |
| Risk coverage (5) | 4 | 2 | neither gives probabilities; V1 covers failure modes (A2, A3) and external behaviour (gh); V2 covers none of those |
| Invariant and edge-case coverage (5) | 4 | 1 | V1: partial-page case (A2), interaction between tasks (A1, A4); V2: only the Task 1 / test interaction (Q1) |
| **qual total (of 30)** | **27** | **18** | |
| **qual_score** | **0.90** | **0.60** | |

Edge-case floor (1/5): Variant 1 = 4/5, Variant 2 = 1/5: both eligible.

## Position-Bias Mitigation

Pass 1 evaluated in order (V1, V2); pass 2 re-evaluated in reverse order (V2, V1). disagreements_found: 0; verdicts_changed: 0. Limit: same judge, so this does not remove a judge-level bias.

## Combined Scoring

| Variant | 0.50 x quant | 0.50 x qual | Final |
|---|---|---|---|
| 1 | 0.4678 | 0.4500 | **0.918** |
| 2 | 0.4363 | 0.3000 | 0.736 |

Margin: 18.2 percent. Tiebreaker applied: No (margin above 5 percent). Debate performance agrees: Variant 1 wins C-001, C-003, C-005, C-006, C-007 and S-001; Variant 2 wins C-002 and C-004.

## Selected Base: Variant 1 (reviewer 1 card, analyzer, opus class)

**Selection rationale.** Higher on every dimension except coverage of the ordering gap (Q2), and it holds the only two findings both advocates agreed are needed beyond the shared one (A2, A3).

**Strengths to preserve.** A1 (with the stale-entry and wording advice), A2 (now with the verified probe), the "what I checked and found correct" list, the Note findings.

**Strengths to incorporate from Variant 2.** Q2 (ordering test gap), graded Medium; Q3 (coverage record), graded Note; Q1's citation of the scanner assertion (test_worker_contract.py:1953-1956) merged into A1's evidence.
