# Tier 2 calibration — root-cause-analyst

- Evidence grounding: 1.0 (primary diagnosis); secondary intermittency hypothesis weakly grounded but correctly flagged as
  inferential.
- Symptom coverage: 1.0 — covers BOTH the primary failure AND offers a credible (if unverified) story for the 1/5 pass rate
  via SQLAlchemy thread-safety.
- Reproducibility fit: 1.0 — primary deterministic; secondary intermittency hypothesis aligns with a well-known concurrency
  hazard.
- Fix directness: 1.0 — fix-of-record is single test file.
- Domain coherence: 0.5 (agent self-scored — surfaces threading + ORM concern alongside test fix)

Calibrated confidence: (1.0+1.0+1.0+1.0+0.5)/5 = **0.90**

Verdict: strongest card of the three. Highest symptom coverage because it attempts an explanation for the residual
intermittency without contaminating the primary fix.
