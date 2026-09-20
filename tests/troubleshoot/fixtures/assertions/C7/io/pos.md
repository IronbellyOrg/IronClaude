---
assertion: C7
domain: io
polarity: pos
expected_flags: [uncited]
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: /proc/uptime is served non-seekable under this runtime
## Mechanism
The shell's 1-byte read fallback fails on the non-seekable node.
