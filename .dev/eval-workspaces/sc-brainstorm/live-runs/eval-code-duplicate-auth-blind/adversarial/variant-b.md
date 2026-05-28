---
variant_id: B
advocate: Agent B
blind_mode: true
---

# Variant B — Specification-First

## Approach

Write the canonical auth contract as an executable specification — typed
interface plus property-based tests — before any code consolidation. Implement
the canonical module against the spec. Migrate call-sites only after the spec
is signed off.

## Required Components

1. Typed canonical-auth interface document.
2. Property-based test suite codifying required behaviours (idempotency of
   token validation under replay, lockout monotonicity, session-extension
   rules, etc.).
3. Three-way audit of the legacy modules against the spec to surface every
   accidental divergence.
4. Implementation of the canonical module that passes the property suite.
5. Migration plan that lands only after spec sign-off.

## Risks

- Spec-design phase can stall on cross-team disagreement.
- Property suite may miss behaviours that exist only in operational quirks.

## Mitigations

- Use the facade scaffolding (from Variant A) as the forcing function to break
  cross-team deadlock.
- Add observation-derived tests from production traffic as the spec ages.
