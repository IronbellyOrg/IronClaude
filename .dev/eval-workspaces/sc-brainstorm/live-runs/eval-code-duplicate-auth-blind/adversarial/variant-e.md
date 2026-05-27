---
variant_id: E
advocate: Agent E
blind_mode: true
---

# Variant E — Minimal-Canonical-Plus-Adapters

## Approach

Extract the truly shared core — token issuance, session lookup, password
verification primitives — into a canonical library. Keep three thin adapter
layers that translate each surface's legitimate quirks into the canonical core.
Do not attempt to flatten legitimate per-surface divergence.

## Required Components

1. Canonical-core library with a small, stable surface (issue token, validate
   token, hash password, verify password, lookup session).
2. Three adapter layers — one per current surface — that map surface-specific
   request and claim shapes onto the canonical core.
3. Adapter-divergence policy: any divergence in adapter behaviour beyond
   request and claim translation requires explicit, signed-off rationale.
4. Migration plan that converts each legacy module into its adapter,
   incrementally.
5. Drift-detection mechanism that surfaces adapter behaviour drifting beyond
   the policy.

## Risks

- Three adapters with three subtly different translation rules can re-create
  the duplication problem at a smaller scale.
- Distinction between "legitimate divergence" and "accidental divergence" is a
  judgement call.

## Mitigations

- Legitimate divergence is modelled as explicit policy on the canonical-core
  module (per Variant D's critique), not as adapter logic, wherever possible.
- Adapters are subject to a documented policy ceiling on what they may diverge
  on.
