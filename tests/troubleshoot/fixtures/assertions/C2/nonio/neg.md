---
assertion: C2
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
- Excluded: `retry-exhausted` — exit statement producer.py:88 (`raise PublishError` before any retry loop).
- consumer.py:41 sets the terminal status.
