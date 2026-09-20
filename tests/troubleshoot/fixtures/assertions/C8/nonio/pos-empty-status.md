---
assertion: C8
domain: nonio
polarity: pos
expected_flags: ["behaviour-cite: missing"]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The broker requeues with redelivered=true when the channel closes before ack. behaviour-definition: row 2
--- file: behaviour-definitions.md ---
| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | broker ack | requeues with redelivered=true on channel close | broker doc Consumer acknowledgements | the clause that specifies requeues with redelivered=true on channel close | fetched:context7 |
| 2 | producer retry | publishes again on HTTP 5xx | producer client retry policy | the code that implements publishes again on HTTP 5xx | |
