---
assertion: C7
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: the broker requeues with redelivered=true when the channel closes before ack
## Mechanism
A crash between send and ack requeues the message.
2x2 row: redelivered-exact=1 redelivered-ref=0 (failing) / 0,0 (passing)
