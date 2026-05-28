---
blind_mode: true
---

# Diff Analysis

## Pairwise Element Overlap

| Element | Variant A | Variant B | Variant C | Variant D | Variant E |
|---|---|---|---|---|---|
| Canonical facade | Yes (core) | Implied | No | No | Partial (core lib) |
| Canonical contract | No | Yes (core) | Partial | No | Partial |
| Baseline-selection audit | No | Yes (audit pass) | Yes (core) | No | No |
| Shadow-and-diff | No | No | No | Yes (core) | No |
| Explicit divergence policy | No | No | No | Partial | Yes (core) |
| Per-call-site rollback | Yes | Implied | Implied | Yes | Implied |
| Global kill-switch | Yes | Implied | Implied | Yes | Implied |

## Non-Conflicting Composition

The five core elements (facade, contract, audit, shadow-and-diff, divergence
policy) are orthogonal — each addresses a different failure mode:

- Facade addresses cutover blast radius.
- Contract addresses accidental-divergence inheritance.
- Audit addresses baseline-selection bias.
- Shadow-and-diff addresses unverified behavioural equivalence.
- Divergence policy addresses legitimate per-surface differences.

## Conflicts to Resolve

- Variant E adapter layers vs. Variant D and the merged plan: rejected in favour
  of explicit canonical-policy on the canonical module. Adapters retained only
  as a transitional shim during migration.
- Variant C "highest-coverage-wins" simplification vs. Variant B audit
  requirement: resolved in favour of the audit. Coverage is one input, not the
  sole input.
- Variant D global soak vs. Variant C cost concern: resolved in favour of
  per-call-site soak at cutover time.
