---
assertion: A9
domain: io
polarity: pos
expected_flags: [probe_suspect]
---
--- file: REPORT.md ---
# Discriminator: uptime-regex
Observable that differs: uptime-regex
Reference-context value: true
--- file: tier1-observation.md ---
reference arm (dind-public): uptime-regex=false
failing arm (sysbox-public): uptime-regex=false
