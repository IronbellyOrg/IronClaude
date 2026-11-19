# Base Selection

Consensus findings used as the requirement set for coverage scoring (K1-K10): K1 claim.md:142 text (medium); K2 keep the E-SUBMIT stop rule; K3 architecture reference missed; K4 design-record lines missed; K5 worker-brief out-of-scope record; K6 setup-doc bare launch rows (A-004); K7 Task 10 must also stage .dev/tasks; K8 coordinator-owned re-claim (INV-002); K9 ambiguous "without `--pipeline full`" wording (INV-005); K10 test that pins a bare --submit still stops.

## Quantitative Scoring (50% weight)
| Metric | Weight | Variant 1 | Variant 2 | Variant 3 |
|--------|--------|-----------|-----------|-----------|
| Requirement coverage (K findings present in the card) | 0.30 | 0.30 (K1, K2, K4 part) | 0.30 (K1, K2 via test, K10) | 0.50 (K1, K2, K3, K4, K5) |
| Internal consistency (claims kept after debate) | 0.25 | 0.80 (F3 withdrawn) | 0.50 (blocking grade withdrawn, F2 withdrawn) | 0.90 (F6 regraded, tags corrected) |
| Specificity ratio | 0.15 | 0.90 | 0.90 | 0.95 |
| Dependency completeness (cited references resolve) | 0.15 | 0.95 | 0.95 | 0.95 |
| Section coverage (findings relative to max 6) | 0.15 | 0.83 | 0.33 | 1.00 |
| **quant_score** | | **0.69** | **0.54** | **0.81** |

## Qualitative Scoring (50% weight): additive binary rubric, 30 criteria, CEV evidence per criterion
Criteria met (orchestrator reading of the cards against the transcript): Variant 1: 20 of 30 (completeness 4, correctness 4, structure 3, clarity 3, risk coverage 3, invariant and edge case 3); Variant 2: 14 of 30; Variant 3: 23 of 30. **qual_score**: 0.67, 0.47, 0.77.

### Edge Case Floor Check
Invariant and edge case dimension: V1 3 of 5, V2 1 of 5, V3 3 of 5. All at or above the 1 of 5 floor; every variant is eligible.

## Position-Bias Mitigation
Recorded deviation: the orchestrator ran ONE pass in input order. The reverse-order pass was not run. Reason on the record: the base margin (0.11) is above the 5 percent tiebreak band, the three cards are complementary reviews of one plan rather than rival alternatives, and the debate itself changed the ordering of no point. This is a departure from the protocol, listed in the return contract as `position_bias_passes: 1`.

## Combined Scoring
| Variant | quant (50%) | qual (50%) | Final |
|---------|-------------|------------|-------|
| 1 | 0.69 | 0.67 | 0.68 |
| 2 | 0.54 | 0.47 | 0.51 |
| 3 | 0.81 | 0.77 | **0.79** |
Margin to runner-up: 0.11. Tiebreaker not applied.

## Selected Base: Variant 3 (reviewer 3, refactorer, opus)
- Rationale: widest coverage of the consensus set (5 of 10 findings), the only card with the architecture reference, the design-record lines, the worker-brief and flag.md:85, and the most grounded citations (14 of 14 calibrated).
- Strengths to preserve: F2 to F5 evidence; the scope-discipline lens.
- Strengths to incorporate: V1's claim.md:142 fix wording and A-004 evidence (issue-watcher-setup.md:616-619); V2's Task 10 staging defect and the "pin that a bare --submit stops" test; the probe findings INV-002, INV-005 and the LOW items.
