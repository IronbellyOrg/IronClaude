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
--- file: job-4711.log ---
run=invoice-4711 arm=failing command=SELECT-state-for-invoice-4711
state=dead-lettered
