---
blind_mode: true
selected_base: Variant A (Agent A)
selection_method: behavioural-equivalence-matrix + risk-of-stall + per-call-site-rollback
---

# Base Selection

## Selected Base

Variant A — Strangler-Fig Facade.

## Rationale

Variant A is the only proposal that establishes a forcing function (the facade
plus per-call-site flag) without committing to a specific consolidation order
or canonical-baseline choice. Every other variant's load-bearing element
(spec-first, coverage-based baseline, shadow-and-diff, minimal-core-adapters)
composes on top of the facade rather than replacing it. Variant A therefore
acts as the structural baseline; Variants B, C, D, and E contribute hardening
layers above it.

## Composition Plan

- Variant A — structural scaffolding (facade + per-call-site flag + kill-switch).
- Variant B — canonical contract, written against the facade's observed traffic
  rather than written up front.
- Variant C — baseline-selection audit combining coverage, hardening posture,
  and behavioural-equivalence-matrix score.
- Variant D — per-call-site shadow-and-diff window at cutover time (not global
  soak).
- Variant E — explicit policy on the canonical-core module for legitimate
  per-surface divergence; no permanent adapter layer.

## Rejected Alternatives

- Variant B as base: would stall on cross-team spec disagreement without a
  forcing function.
- Variant C as base: would bake the coverage-as-proxy fallacy into the
  strategy.
- Variant D as base: shadow-and-diff is a verification mechanism, not a
  consolidation strategy; it has nothing to compare against until the canonical
  module exists.
- Variant E as base: minimal-core-adapters preserves the duplication problem in
  a new shape.
