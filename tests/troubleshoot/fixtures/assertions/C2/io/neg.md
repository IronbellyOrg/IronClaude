---
assertion: C2
domain: io
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `auth-denied` — exit statement startup.sh:663 (`return 1` after the askpass prompt).
- startup.sh:583 is the first statement of the attempt.
