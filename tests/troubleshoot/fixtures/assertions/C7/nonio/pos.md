---
assertion: C7
domain: nonio
polarity: pos
expected_flags: [uncited]
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
environment-property: the broker requeues with redelivered=true when the channel closes before ack
## Mechanism
A crash between send and ack requeues the message.
