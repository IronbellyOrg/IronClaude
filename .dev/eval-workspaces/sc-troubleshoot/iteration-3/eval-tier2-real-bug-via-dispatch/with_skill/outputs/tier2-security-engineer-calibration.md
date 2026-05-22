# Tier 2 Calibration — security-engineer card

**Card tier**: 2
**Agent self-score**: 0.95
**Rubric**: refs/escalation-rubric.md (re-applied independently)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| Evidence grounding | 1.0 | All cited lines verified against fixtures; the smoking-gun `output_dir=output_dir` confirmed at commands.py:1476. |
| Symptom coverage | 1.0 | Explains both halves of the asymmetry + names the threat model (operator-controlled HOMEs) that motivates OPS-002. |
| Reproducibility fit | 1.0 | Deterministic input → deterministic bypass. |
| Fix directness | 1.0 | One-line removal; touches the exact line in evidence. |
| Domain coherence | 0.7 | Mostly single-domain (security policy enforcement). Slight bleed into API-misuse but well within the security-engineer's domain. Adjusted from 0.5 in Tier 1 because the security-engineer correctly frames it as a single class of security issue. |

**Calibrated confidence**: (1.0+1.0+1.0+1.0+0.7) / 5 = **0.94**

(Agent self-reported 0.95 — calibration adjustment of -0.01, within noise.)

**Verdict**: Strong card. Tracks the threat model and the documented OPS-002 contract.
