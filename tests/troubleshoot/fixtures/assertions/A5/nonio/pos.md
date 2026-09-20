---
assertion: A5
domain: nonio
polarity: pos
expected_flags: [consensus_on_unobserved]
---
--- file: REPORT.md ---
adversarial_invoked: false
--- file: candidate-fixes.md ---
| # | Fix | Proposed by | Agreement | Confidence |
|---|---|---|---|---|
| 1 | Ack before the side effect, make send idempotent | rca, backend | consensus | 0.70 |
--- file: card-rca.md ---
claim_class: environment_dependent
evidence_class: doc_static
verdict_direction: AFFIRM
