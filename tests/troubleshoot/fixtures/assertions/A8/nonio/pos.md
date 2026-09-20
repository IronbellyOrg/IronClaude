---
assertion: A8
domain: nonio
polarity: pos
expected_flags: [ci_verdict_unobserved]
files_present: [REPORT.md, execution-locus.md]
---
--- file: REPORT.md ---
## Diagnosis
The nightly consumer smoke job was reported green by the scheduler.
--- file: execution-locus.md ---
PRINT-SITE: scheduler job log, failing CI job smoke-consumer
RUN-SITE: consumer.py:41 @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: artifact-file
