---
assertion: A7
domain: nonio
polarity: pos
expected_flags: [run_site_unresolved]
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
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| consumer.py:41 | status = "DEAD_LETTER" | return | after | yes | dlq depth | surviving=yes |
