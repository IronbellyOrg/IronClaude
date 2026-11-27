# Calibration of the second Tier 1 card (saved by the orchestrator from the calibrator's returned text)

Calibrator class: sonnet alias (disjoint from the reviewer classes haiku and opus; the same class as the executor).

| Dimension | Score |
|---|---|
| Citation grounding | 0.88 |
| Coverage completeness | 0.85 |
| Deviation-classification clarity | 0.50 |
| Risk surface coverage | 0.62 |
| Recommendation actionability | 0.35 |

C = (0.88 + 0.85 + 0.50 + 0.62 + 0.35) / 5 = 0.64

Citation spot-check: every cited plan line matches (21, 22, 23, 24, 25, 104, 108, 116, 120, 134, 191, 205, 219, 222, 234), and the matrix figures match (24 parsed of 24 matched, 14 inferred, union 0.8421 = 32/38, S_dev_density 0.1579 = 6/38, six unmapped inferred rows). One mismatch: C10 cites plan line 207 for the AC6 "pending" verdict; AC6 is quoted at plan line 203 and "pending" is stated at the end of plan line 205 (line 207 is the Part three paragraph). Not cited: C7 (true by absence), C11, and the hand mapping of INF-001, 002 and 009.

Signals noted by the calibrator for the orchestrator: C < 0.85 (rubric guidance says ESCALATE), S_dev_density 0.1579 (above 0.10, at or below 0.20), 11 tasks (above S_scope 10). Orchestrator decision: section 5.3 rule 4 (domains: code, tests, docs and infra paths, at least 3) and rule 6 (C < 0.85) both route to Tier 2.
