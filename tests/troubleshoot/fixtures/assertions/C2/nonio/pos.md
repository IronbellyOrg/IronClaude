---
assertion: C2
domain: nonio
polarity: pos
expected_flags: ["unproven_exclusion:retry-exhausted"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `retry-exhausted` (the producer never retries on 5xx in this deployment).
- consumer.py:41 sets the terminal status.
