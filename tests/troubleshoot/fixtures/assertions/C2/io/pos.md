---
assertion: C2
domain: io
polarity: pos
expected_flags: ["unproven_exclusion:auth-denied"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `auth-denied` (unreachable for an anonymous public clone).
- startup.sh:583 is the first statement of the attempt.
