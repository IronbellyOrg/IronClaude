---
assertion: A1
domain: nonio
polarity: pos
expected_flags: [deduced_headline]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.42
## Summary
Root cause: the invoice message ends `dead-lettered` after the consumer crashes between send and ack.
## Diagnosis
The consumer acks after the side effect.
## Grounding Gaps
- `dead-lettered` is pending observation; the DLQ was not queried in this run.
--- file: calibration.md ---
calibrated: 0.42
