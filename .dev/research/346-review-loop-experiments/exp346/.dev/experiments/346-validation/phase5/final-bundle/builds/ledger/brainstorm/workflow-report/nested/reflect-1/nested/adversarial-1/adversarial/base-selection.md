# Base Selection

## Quantitative Scoring (50% weight)

Requirement set for RC = the 12 confirmed in-scope defect topics of diff-analysis.md (C-001 to C-011 and C-013; C-012 excluded as refuted). Values for SR are orchestrator estimates from reading every claim line (both cards are almost entirely concrete); the other four are counted.

| Metric | Weight | Variant A | Variant B | Computation |
|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.833 | 0.333 | A: C-001..C-006, C-009, C-010, C-011, C-013 = 10/12; B: C-001, C-002, C-007, C-008 = 4/12 |
| Internal consistency (IC) | 0.25 | 1.000 | 0.900 | A: 0 contradictions in 15 claims (11 findings, D1-D4); B: 1 (self_audit "INF-032 falsely covered" vs true_gaps INF-134 only) in 10 claims |
| Specificity ratio (SR) | 0.15 | 0.95 | 0.93 | estimate; both cite file:line on nearly every claim |
| Dependency completeness (DC) | 0.15 | 1.000 | 0.900 | A: D1/D4 refs to R1-F10/R1-F11 resolve; B: INF-032 unresolved in-card (1 of ~10 refs) |
| Section coverage (SC) | 0.15 | 0.900 | 1.000 | top-level keys: A 9, B 10 |
| **quant_score** | | **0.928** | **0.750** | (RC×0.30)+(IC×0.25)+(SR×0.15)+(DC×0.15)+(SC×0.15) |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Full Claim-Evidence-Verdict tables are in the two pass reports summarised below (pass 1 input order A,B; pass 2 reverse order B,A; independent opus evaluators).

| Dimension | A pass 1 | A pass 2 | A final | B pass 1 | B pass 2 | B final |
|---|---|---|---|---|---|---|
| Completeness (5) | 3 | 3 | 3 | 3 | 2 | 2 |
| Correctness (5) | 3 | 3 | 3 | 2 | 3 | 2 |
| Structure (5) | 5 | 5 | 5 | 5 | 5 | 5 |
| Clarity (5) | 4 | 4 | 4 | 4 | 3 | 3 |
| Risk Coverage (5) | 4 | 4 | 4 | 4 | 4 | 4 |
| Invariant & Edge Case (5) | 5 | 5 | 5 | 3 | 4 | 3 |
| **Total (30)** | 24 | 24 | **24** | 21 | 21 | **19** |

Key verdicts: both NOT MET on Completeness #1 (A missed C-007 and the Task 6/Task 1 conflict and carries refuted A-F10; B missed C-004, C-005, C-006). A NOT MET on Correctness #1-2 (refuted A-F10; unsafe first remedy in A-F1). B NOT MET on Correctness #1, #3, #4 (regression misclassification; INF-032 self-contradiction). Both NOT MET on Risk #1 (no per-risk probability) and Clarity #4 (terms undefined).

### Edge Case Floor Check
- Variant A: 5/5, eligible.
- Variant B: 3/5, eligible.

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness #3 | B | MET | NOT MET | no | NOT MET (re-evaluated) |
| Correctness #3 | B | NOT MET | MET | no | NOT MET (re-evaluated) |
| Clarity #1 | B | MET | NOT MET | no | NOT MET (re-evaluated) |
| Invariant #1 | B | NOT MET | MET | no | NOT MET (re-evaluated) |
| all 30 criteria | A | — | — | yes (identical) | as passes |

- disagreements_found: 4 (all Variant B)
- verdicts_changed: 4 relative to one pass each (two from pass 1, two from pass 2); B total moves from 21 to 19 in both passes.

## Combined Scoring

| Variant | quant × 0.50 | qual × 0.50 | Combined |
|---|---|---|---|
| A | 0.464 | 0.400 (24/30) | **0.864** |
| B | 0.375 | 0.317 (19/30) | **0.692** |

- Margin: 0.172 (17.2 points); tiebreaker not applied.
- Debate points (scoring matrix): A wins 13, B wins 4, split 2, equal or agreed 4 (see debate-transcript.md).

## Selected Base: Variant A (opus advocate; card by reviewer 1, analyzer, sonnet)

**Selection rationale.** Variant A covers 10 of the 12 confirmed defect topics, including the three high-severity test-mechanics defects (C-004 severity scan of tracked files only, C-005 routing-refresh command set, C-006 Task 2/Task 3 ordering) that B missed and conceded; its classes match the taxonomy and its self-confidence matches calibration (0.80 vs 0.78).

**Strengths to preserve (A):** A-F1 class `necessary`; A-F2, A-F3, A-F4 (reworded as ordering), A-F5, A-F6, A-F7, A-F8 (minor, verified), A-F9, A-F11; t1 deviation agreement D1, D2, D4 and the D3 reclassification.

**Strengths to incorporate from B:**
- B-F3 heartbeat condition (C-007), reclassified `drift`, blocking; plan never mentions the heartbeat.
- B-F2 cross-task conflict (Task 1 :44 vs Task 6 :125) and the single skip predicate (review 1, loop PASS, live hash equals snapshot), class `drift`.
- B-F1 remedy for C-001: keep the whole-file no-path pin; rewrite spec-panel.md:220 in the variant under a recorded owner decision (installed template differs from the examples copy), add that line to the drift exclusions.
- B coverage map, relabelled "referenced" (INF-005/058/104 moved to true gaps, matching A-F7).
- B-F4 bytes per claim as a minor owner note (spec-internal gap, source.md:72 vs :157).
- Debate new evidence: E-CAP vs E-TERMINAL order on a fourth `begin`; spec premise "(that test scans all of `src/`)" is false.
