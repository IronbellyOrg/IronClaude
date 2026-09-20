---
assertion: C8
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The broker requeues with redelivered=true when the channel closes before ack. behaviour-definition: row 1
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | broker ack | requeues with redelivered=true on channel close | broker doc Consumer acknowledgements | the clause that specifies requeues with redelivered=true on channel close | fetched:context7 |
