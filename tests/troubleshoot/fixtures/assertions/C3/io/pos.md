---
assertion: C3
domain: io
polarity: pos
expected_flags: [control_unproven]
calibrated: 0.70
---
--- file: card.md ---
claim_class: runtime_behavior
## Evidence
The DinD control arm passed the same script, so the producer is proven passing there.
--- file: execution-locus.md ---
RUN-SITE: startup.sh:583 @ ci-runner
CONTROL-PROOF: no: startup.sh:753
