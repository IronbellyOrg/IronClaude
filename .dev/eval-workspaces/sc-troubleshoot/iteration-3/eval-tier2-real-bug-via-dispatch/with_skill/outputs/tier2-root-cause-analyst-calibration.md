# Tier 2 Calibration — root-cause-analyst card

**Card tier**: 2
**Agent self-score**: 0.94
**Rubric**: refs/escalation-rubric.md (re-applied independently)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | All citations verified; particularly the contrast between layers (1473 vs 1490-1499) is a real, on-disk distinction. |
| Symptom coverage | 1.0 | Same as security-engineer: explains both halves. Adds a useful framing (kwarg misuse) that didn't appear in Tier 1. |
| Reproducibility fit | 1.0 | Deterministic. |
| Fix directness | 0.9 | FIX-A is direct (one-line). The proposed FIX-B (remove the kwarg entirely) is broader and the agent correctly defers it to a refactor — small uncertainty premium. |
| Domain coherence | 0.8 | Frames as API-misuse, which is single-domain (correctness). Higher than security-engineer's framing because it removes the security ambiguity by treating the security impact as a consequence rather than the root. |

**Calibrated confidence**: (1.0+1.0+1.0+0.9+0.8) / 5 = **0.94**

(Agent self-reported 0.94 — matches.)

**Verdict**: Strong card. Provides the critical second framing (correct downstream pattern at 1490-1499 vs. incorrect upstream usage at 1476).
