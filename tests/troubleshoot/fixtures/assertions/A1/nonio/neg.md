---
assertion: A1
domain: nonio
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
**Confidence**: 0.72
## Summary
Root cause: the invoice message ends `dead-lettered` after the consumer crashes between send and ack.
## Diagnosis
The consumer acks after the side effect.
## Grounding Gaps
- none for the headline token.
--- file: calibration.md ---
calibrated: 0.72
--- file: tier1-observation.md ---
SELECT state FROM consumed_log WHERE invoice_id=4711; -- dead-lettered
