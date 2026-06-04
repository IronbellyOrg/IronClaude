# Base Selection: Eval+Incorporation Release Plan

## Scoring (combined quantitative 0.50 + qualitative 0.50)

| Dimension | V1 architect | V2 analyzer | V3 devops |
|-----------|:-----------:|:-----------:|:---------:|
| Completeness (structure) | 0.95 | 0.80 | 0.70 |
| Eval/measurement rigor | 0.45 | 0.98 | 0.55 |
| Cost/operational realism | 0.55 | 0.65 | 0.95 |
| Reversibility / safety | 0.95 | 0.75 | 0.80 |
| Reusability of skeleton | 0.95 | 0.70 | 0.60 |
| Clarity / actionability | 0.85 | 0.80 | 0.90 |
| Risk coverage | 0.85 | 0.90 | 0.85 |
| **Weighted combined** | **0.79** | **0.80** | **0.77** |

Scores are near-identical (within 5%) — triggers tiebreaker.

## Tiebreaker → Base = V1 (opus/architect)

V1 and V2 are within 5% (0.79 vs 0.80). Tiebreaker Level 1 (debate performance):
V1's structural skeleton **won every architecture point uncontested** and is the only
variant that produces a *reusable container* both other variants explicitly defer to
("the other variants must cover that gap" — V3; "V1's state machine is the right
container" — V2). V2 and V3 are content-rich but architecturally dependent.

**Base = V1** (the 5-stage state machine + gates + integration map + rollback skeleton).
**Graft sources:**
- **V2** supplies the *measurement substance* poured into every S1 (shadow) and S2 (gate): scenario matrix, 30-metric catalog, ground-truth tiering, blind adjudication, statistical-validity guards, vendor-claim hypotheses, scorecard templates.
- **V3** supplies the *cost instrumentation* hung on every gate: 5-domain cost taxonomy, latency harness, install matrix, multi-vendor token economics, TCO scorecard, usage monitoring, sem-collision neutralization, maintenance matrix.

This is a **union merge**, not a compromise: each variant owns a non-overlapping pillar,
and the base provides the frame that holds all three.

## Edge-case floor check
All three score ≥1/5 on invariant/edge-case coverage (V1: weave auto-KILL + CP checkpoints; V2: Simpson's-paradox + recall@60; V3: O(n²) ceiling + dead-weight detection). Floor satisfied; no variant ineligible.
