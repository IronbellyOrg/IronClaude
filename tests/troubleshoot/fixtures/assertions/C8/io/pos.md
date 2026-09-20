---
assertion: C8
domain: io
polarity: pos
expected_flags: ["behaviour-cite: missing"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The FUSE handler returns EOF at offset>0.
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | procUptime read | returns EOF at offset>0 | handler read function | the code that implements returns EOF at offset>0 | fetched:gh-api |
