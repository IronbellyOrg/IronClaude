---
assertion: A9
domain: nonio
polarity: pos
expected_flags: [probe_suspect]
---
--- file: REPORT.md ---
# Discriminator: redelivered
Observable that differs: redelivered
Reference-context value: false
--- file: tier1-observation.md ---
control consumer (known-good, worker-pod-a): redelivered=true
failing consumer (worker-pod-b): redelivered=true
