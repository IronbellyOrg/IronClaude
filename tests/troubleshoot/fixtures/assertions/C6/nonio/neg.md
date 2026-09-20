---
assertion: C6
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: environment_dependent
## Claim
Root cause: the consumer stalls above 512 in-flight messages.
2x2 row: prefetch-exact=1 prefetch-ref=0 (failing) / 0,0 (passing)
--- file: bracket.md ---
bracket=[510,512] width=2
