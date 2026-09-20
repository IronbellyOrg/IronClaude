---
assertion: A7
domain: io
polarity: pos
expected_flags: [run_site_unresolved]
---
--- file: REPORT.md ---
status: partial
--- file: execution-locus.md ---
PRINT-SITE: GitHub Actions job log, step "Seed checkout"
RUN-SITE: pending-producers @ ci-runner
SAME-ENV: no
OBSERVE-VIA: artifact-file
--- file: producers.md ---
observation-kind: categorical
## Producers
| line | statement | exit statement | marker | wall-time | observable | surviving |
|---|---|---|---|---|---|---|
| startup.sh:583 | aidev_seed_now \|\| return 1 | return 1 | before | yes | started-line absent | surviving=yes |
