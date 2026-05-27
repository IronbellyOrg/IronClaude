---
variant_id: D
advocate: Agent D
blind_mode: true
---

# Variant D — Shadow-and-Diff

## Approach

Run the canonical implementation in shadow mode behind every call-site for a
soak period. Diff the canonical module's auth events against the legacy
module's events on a per-call-site basis. Cut over only when divergence drops
to zero (or to documented, approved deviation) for that call-site.

## Required Components

1. Shadow-execution harness that runs the canonical module in parallel with the
   legacy module on the same auth request without affecting the response.
2. Structured-diff comparator over auth events (token claims, session state,
   audit-log entries, error codes).
3. Per-call-site divergence dashboard with a documented zero-divergence
   acceptance threshold.
4. Cutover-on-green automation: once a call-site holds zero divergence for the
   approved soak window, the flag flips automatically (with a manual override).
5. Soak-cost budget and a hard ceiling beyond which shadow execution is
   throttled.

## Risks

- Shadow execution doubles auth-path cost during the soak.
- Diff over auth events can produce false positives on non-deterministic fields
  (timestamps, nonces).

## Mitigations

- Soak is per-call-site, not global; the diff comparator excludes a documented
  set of non-deterministic fields.
- Soak length is bounded; the cost ceiling triggers throttling, not run-away
  doubling.
