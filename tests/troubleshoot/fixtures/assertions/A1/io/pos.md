---
assertion: A1
domain: io
polarity: pos
expected_flags: [deduced_headline]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.42
## Summary
Root cause: the recorded seed outcome is `clone-failed`, a fast network-level git failure.
## Diagnosis
The §8 assertion rejects any outcome other than `cloned`.
## Grounding Gaps
- `clone-failed` is deduced from source logic, not read from the artifact.
--- file: calibration.md ---
calibrated: 0.42
