---
assertion: A1
domain: io
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.72
## Summary
Root cause: the recorded seed outcome is `clone-failed`, read from the seed artifact.
## Diagnosis
The §8 assertion rejects any outcome other than `cloned`.
## Grounding Gaps
- none for the headline token.
--- file: calibration.md ---
calibrated: 0.72
--- file: job-105704643590.log ---
seed-outcome-observed=clone-failed
RESULT: FAIL
