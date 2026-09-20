---
assertion: A7
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
RUN-SITE: startup.sh:583 @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| startup.sh:583 | aidev_seed_now \|\| return 1 | return 1 | before | yes | started-line absent | surviving=yes |
