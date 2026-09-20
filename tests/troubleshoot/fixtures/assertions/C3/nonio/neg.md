---
assertion: C3
domain: nonio
polarity: neg
expected_flags: []
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The control run on worker-pod-a delivered every invoice exactly once with the same consumer build.
--- file: execution-locus.md ---
RUN-SITE: consumer.py:41 @ worker-pod-b
CONTROL-PROOF: yes: consumer.py:41
