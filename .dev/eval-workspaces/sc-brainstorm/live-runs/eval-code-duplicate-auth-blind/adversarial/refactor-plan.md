---
blind_mode: true
---

# Refactor Plan

## Phase 1 — Scaffolding (Variant A core)

1. Introduce canonical facade module exposing the union of the three modules'
   surface functions.
2. Add a per-call-site feature flag with the legacy module as the initial
   default.
3. Add a global kill-switch that reverts every call-site to its legacy module.
4. Route the lowest-risk call-site through the facade in pass-through mode
   (still dispatches to legacy).

## Phase 2 — Audit and Contract (Variants B, C core)

5. Run coverage and hardening audits on each of the three legacy modules.
6. Produce the behavioural-equivalence matrix across surface functions.
7. Select the canonical baseline implementation using the matrix plus audit
   data (not coverage alone).
8. Codify the canonical contract as a typed interface plus property-based test
   suite, written against the facade's observed traffic.

## Phase 3 — Canonicalisation (Variants C, E core)

9. Implement the canonical module against the contract.
10. Model legitimate per-surface divergence as explicit policy on the canonical
    module (configurable per call-site).
11. Stand up transitional adapters where a surface's quirk cannot yet be
    expressed as canonical policy; mark each with an end-of-life date.

## Phase 4 — Cutover (Variants A, D core)

12. For each call-site in cutover order, enable shadow-and-diff mode (canonical
    runs in parallel with legacy; response still served by legacy).
13. Soak per the configured window. When divergence holds at zero (or at
    documented approved deviation), flip the flag to canonical.
14. After all call-sites for a given legacy module are cut over, retire that
    legacy module.

## Phase 5 — Cleanup

15. Remove every transitional adapter whose end-of-life date has passed.
16. Remove the legacy modules.
17. Document the explicit-divergence-policy registry as the canonical record of
    legitimate per-surface differences.

## Rollback

- Per-call-site: flip the per-call-site flag back to legacy. MTTR target: under
  5 minutes.
- Global: flip the kill-switch. MTTR target: under 2 minutes.
- Post-cleanup: requires a re-introduction of the legacy module from version
  control; covered by the rollback runbook.
