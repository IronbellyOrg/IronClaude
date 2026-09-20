---
assertion: A7
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: consumer pod stdout, worker-pod-b
RUN-SITE: pending-producers @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: remote-command
--- file: producers.md ---
observation-kind: categorical
producer-count: 0
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
