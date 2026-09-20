---
assertion: A8
domain: nonio
polarity: neg
expected_flags: []
files_present: [REPORT.md, execution-locus.md, job-7781.log]
---
--- file: REPORT.md ---
## Diagnosis
The job log's last marker reads `RESULT: FAIL`.
--- file: execution-locus.md ---
PRINT-SITE: scheduler job log, job smoke-consumer
RUN-SITE: consumer.py:41 @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: artifact-file
