---
variant_id: A
advocate: Agent A
blind_mode: true
---

# Variant A — Strangler-Fig Facade

## Approach

Introduce a thin canonical facade in front of all three legacy modules. Route
every call-site through the facade behind a per-call-site feature flag. Collapse
implementations one surface at a time, starting with the lowest-risk call-site.

## Required Components

1. Canonical facade module with the union of all three legacy modules' surface
   functions, dispatching internally to the legacy module by per-call-site flag.
2. Per-call-site feature flag with a documented default (initially: legacy
   module).
3. Behavioural-equivalence matrix for each surface function across the three
   modules.
4. Per-call-site cutover order ranked by risk (low-traffic, well-tested first).
5. Global kill-switch that reverts all call-sites to their legacy module.

## Risks

- Facade can become a permanent layer if cutover stalls.
- Per-call-site flag matrix can explode in cardinality.

## Mitigations

- Cutover order is a public schedule with a documented end-of-life date.
- Flag matrix is bounded by call-site count, not by surface-function count.
