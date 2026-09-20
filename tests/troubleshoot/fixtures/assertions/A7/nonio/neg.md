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
RUN-SITE: consumer.py:41 @ worker-pod-b
SAME-ENV: no
OBSERVE-VIA: remote-command
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| consumer.py:41 | status = "DEAD_LETTER" | return | after | yes | dlq depth | surviving=yes |
