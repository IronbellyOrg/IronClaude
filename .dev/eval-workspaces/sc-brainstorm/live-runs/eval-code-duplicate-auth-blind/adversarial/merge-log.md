---
blind_mode: true
convergence_score: 0.82
---

# Merge Log

## Inputs

- Variants A, B, C, D, E (5 anonymized advocates: Agent A through Agent E).
- Base: Variant A.

## Merged Elements

| From | Element | Form in Merge |
|---|---|---|
| Variant A | Canonical facade + per-call-site flag + kill-switch | Phase 1 + Phase 4 |
| Variant B | Canonical contract (typed interface + property tests) | Phase 2, written against observed traffic |
| Variant C | Coverage + hardening audit | Phase 2, as input to baseline selection |
| Variant C | Behavioural-equivalence matrix | Phase 2, as primary baseline-selection criterion |
| Variant D | Shadow-and-diff | Phase 4, per-call-site at cutover only |
| Variant E | Explicit-divergence policy on canonical module | Phase 3, replacing permanent adapters |
| Variant E | Transitional adapters | Phase 3, end-of-life dated |

## Rejected Elements

- Variant C "highest-coverage-wins" framing — replaced by multi-criteria audit.
- Variant D global soak — replaced by per-call-site soak at cutover.
- Variant E permanent adapters — replaced by canonical-policy module plus
  end-of-life transitional adapters.
- Variant B "no implementation before spec sign-off" sequencing — replaced by
  facade-first-then-spec because the facade is the forcing function that breaks
  cross-team deadlock.

## Convergence Indicators

- All five variants agreed on per-call-site rollback granularity.
- All five variants agreed that legacy modules must be retired (none proposed
  permanent coexistence).
- Four of five variants explicitly required a behavioural-equivalence
  artefact in some form; the fifth (Variant D) provided it implicitly via the
  diff comparator.

## Convergence Score

0.82 — strong agreement on the five load-bearing elements; remaining tensions
(soak length, contract format) are implementation-tier parameters.
