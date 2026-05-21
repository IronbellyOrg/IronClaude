# Tier 2 calibration — quality-engineer

Re-grade per refs/escalation-rubric.md.

- Evidence grounding: 1.0 (docstring, signature, return type, assertion, comment, spec all aligned)
- Symptom coverage: 0.5 (agent self-scored this honestly — 1/5 pass mystery not resolved)
- Reproducibility fit: 1.0 (test failure deterministic given new code)
- Fix directness: 1.0 (one-file test rewrite)
- Domain coherence: 1.0 (pure test/spec drift)

Calibrated confidence: (1.0+0.5+1.0+1.0+1.0)/5 = **0.90**

Verdict: strong, accepted. Agent's self-report (0.93) overestimated by ~0.03; minor calibration adjustment only.
