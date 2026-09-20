---
assertion: A5
domain: nonio
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
adversarial_invoked: true
--- file: candidate-fixes.md ---
| # | Fix | Proposed by | Agreement | Confidence |
|---|---|---|---|---|
| 1 | Ack before the side effect, make send idempotent | rca, backend | consensus | 0.70 |
--- file: card-rca.md ---
claim_class: environment_dependent
evidence_class: doc_static
verdict_direction: AFFIRM
