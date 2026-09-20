---
assertion: A9
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
# Discriminator: redelivered
Observable that differs: redelivered
Reference-context value: false
--- file: tier1-observation.md ---
control consumer (known-good, worker-pod-a): redelivered=false
failing consumer (worker-pod-b): redelivered=true
