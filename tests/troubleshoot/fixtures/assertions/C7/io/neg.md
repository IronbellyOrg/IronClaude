---
assertion: C7
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: /proc/uptime is served non-seekable under this runtime
## Mechanism
The shell's 1-byte read fallback fails on the non-seekable node.
2x2 row: uptime-exact=1 uptime-ref=0 (failing) / 0,0 (passing)
