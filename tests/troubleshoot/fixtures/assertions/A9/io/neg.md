---
assertion: A9
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
# Discriminator: uptime-regex
Observable that differs: uptime-regex
Reference-context value: true
--- file: tier1-observation.md ---
reference arm (dind-public): uptime-regex=true
failing arm (sysbox-public): uptime-regex=false
