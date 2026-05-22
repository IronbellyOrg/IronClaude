# Tier 2 Calibration — quality-engineer card

**Card tier**: 2
**Agent self-score**: 0.91
**Rubric**: refs/escalation-rubric.md (re-applied independently)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 0.9 | Citations to scratch-roots.md verified. The claim "no parity test exists" is grounded in absence-of-evidence; we did not actually search the test tree, so this score is slightly discounted. The on-disk fixture does not include the test directory. |
| Symptom coverage | 0.8 | Covers the meta-question ("why did this ship?") rather than the immediate bug. Useful as a sibling lens; lower for the bug-explanation dimension. |
| Reproducibility fit | 1.0 | The proposed parity test is concrete and would reproduce the bypass before the fix. |
| Fix directness | 0.9 | Same FIX-A as other agents + an additive test. Direct primary, additive secondary. |
| Domain coherence | 0.9 | Test gaps + process — single domain (quality / coverage). |

**Calibrated confidence**: (0.9+0.8+1.0+0.9+0.9) / 5 = **0.90**

(Agent self-reported 0.91 — within noise.)

**Verdict**: Useful complementary card. Surfaces a real test gap that would otherwise be missed and is essential for the long-term recurrence story even though it doesn't change the core fix.
