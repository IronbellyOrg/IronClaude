---
topic: "Brainstorm consolidating three duplicate auth modules"
domain: code
strategy: systematic
depth: deep
proposal_count: 5
handoff_target: none
adversarial_status: pass
convergence_score: 0.82
blind_mode: true
created: 2026-05-27T00:00:00Z
---

# Merged Requirements: Canonical Auth Consolidation

## Problem Statement

Three duplicate authentication modules exist across the codebase, with
overlapping but subtly divergent flows (session handling, token validation,
password checks, MFA, role lookup). The duplication drives correctness drift,
doubles the attack surface, and slows feature work that touches auth. The
consolidation must produce a single canonical auth module that preserves every
behaviour the three current modules legitimately provide, with a clear
migration path, per-call-site rollback, and a documented end-state.

## Goals

- Replace three duplicate auth modules with one canonical module.
- Eliminate drift-derived correctness incidents.
- Reduce auth attack surface to one implementation.
- Preserve legitimate per-surface differences as explicit policy, not as
  silently divergent code.
- Land the consolidation without auth-related security regressions and without
  user-visible session invalidation outside an explicit comms event.

## Requirements

### Structural

1. A canonical auth facade is introduced first, exposing the union of the
   three legacy modules' surface functions and dispatching internally via a
   per-call-site feature flag (default: legacy module).
2. A global kill-switch reverts every call-site to its legacy module in under
   2 minutes.
3. Per-call-site rollback (flag flip back to legacy) completes in under
   5 minutes.

### Selection and Contract

4. Baseline selection uses a multi-criteria audit: coverage, hardening posture
   (password hash algorithm and parameters, MFA enforcement, session timeout,
   audit-log completeness), and behavioural-equivalence-matrix score. Coverage
   alone is not sufficient.
5. A canonical-auth contract is codified as a typed interface plus a
   property-based test suite, written against the facade's observed traffic
   rather than written up front. Every drift-derived incident yields a
   regression case in the suite.
6. A behavioural-equivalence matrix documents every surface function across
   the three legacy modules. Each cell is one of: identical, intentionally
   divergent (with policy rationale), accidentally divergent (with resolution).

### Divergence Policy

7. Legitimate per-surface divergence is expressed as explicit policy on the
   canonical module, configurable per call-site. Transitional adapters are
   permitted only with a documented end-of-life date.
8. Adapter-divergence policy: any adapter behaviour beyond request and claim
   translation requires explicit signed-off rationale.

### Cutover

9. Per-call-site cutover order is ranked by risk (low-traffic, well-tested
   first), published as a schedule, and held to.
10. At each call-site cutover, the canonical module runs in shadow mode in
    parallel with the legacy module for a configured soak window. The auth-event
    structured-diff comparator excludes a documented set of non-deterministic
    fields.
11. The flag flips to canonical only when divergence holds at zero (or at
    documented approved deviation) for the soak window.
12. Shadow-execution cost is bounded by a budget. Exceeding the budget
    triggers throttling, not run-away doubling.

### Observability and Audit

13. Canonical-module observability is at least as strong as the strongest of
    the three legacy modules, with structured auth events, per-call-site
    divergence metrics during shadow mode, and rollback telemetry.
14. Audit-log completeness on the canonical module meets or exceeds the union
    of the three legacy modules' audit fields.

### End State

15. After all call-sites for a given legacy module are cut over, that legacy
    module is retired (removed or quarantined behind a clear deprecation
    marker).
16. After end-of-life dates pass, transitional adapters are removed.
17. The explicit-divergence-policy registry remains as the canonical record of
    legitimate per-surface differences.

## Acceptance Criteria

- Single canonical auth module owns 100 percent of production auth code paths
  at end-state.
- Behavioural-equivalence matrix is complete: every surface function across the
  three legacy modules is classified as identical, intentionally divergent (with
  documented policy rationale), or accidentally divergent (with documented
  resolution).
- Per-call-site rollback MTTR demonstrated under 5 minutes in a dry-run prior
  to first production cutover; global kill-switch MTTR demonstrated under
  2 minutes.
- Canonical-module test coverage meets or exceeds the union of the three
  legacy modules' coverage; every drift-derived incident has a regression test.
- During cutover, every call-site holds zero divergence (or documented approved
  deviation) across the configured soak window before its flag is flipped.
- At least 95 percent of auth traffic runs on the canonical module within the
  planned cutover window.
- Zero P0/P1 incidents attributable to the consolidation.
- Audit-log completeness on the canonical module meets or exceeds the union of
  the three legacy modules' audit fields.
- Legacy modules retired (or quarantined behind a clear deprecation marker) by
  end of migration; transitional adapters removed after their end-of-life
  dates pass.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Facade becomes permanent (cutover stalls) | Published cutover schedule with end-of-life date; quarterly review |
| Baseline-selection bias (coverage as proxy) | Multi-criteria audit including behavioural-equivalence matrix |
| Spec-design phase stalls cross-team | Facade introduced first as forcing function; spec written against observed traffic |
| Shadow-execution doubles auth cost | Per-call-site soak only; cost budget with throttling |
| Diff false positives on non-deterministic fields | Documented exclusion list in comparator |
| Adapters re-create duplication at smaller scale | End-of-life dates; adapter-divergence policy ceiling |
| Legitimate divergence silently flattened | Explicit policy module on canonical; per-call-site config |
| In-flight session policy across cutover | Documented in cutover runbook (silent upgrade, forced re-auth, or grace-window dual-read) per call-site |

## Provenance

This merged specification is the adversarial-merge consensus across five
anonymized variants (Agent A through Agent E) produced under BLIND MODE. The
five variants contributed orthogonal load-bearing elements:

- Agent A contributed the strangler-fig facade scaffolding plus per-call-site
  flag and kill-switch (structural baseline).
- Agent B contributed the canonical-contract requirement (typed interface plus
  property-based test suite), hardened by Variant A's facade-first sequencing.
- Agent C contributed the multi-criteria baseline-selection audit, hardened
  by Variant B's critique against coverage-as-sole-proxy.
- Agent D contributed shadow-and-diff verification, scoped down by Variant C's
  cost critique to per-call-site at cutover time.
- Agent E contributed the explicit-divergence-policy model on the canonical
  module, hardened by Variant D's critique against permanent adapter layers.

Base variant: Variant A. Convergence score: 0.82. Mode: B (parallel variants
with adversarial debate). Depth: deep. Rounds: 3. Open implementation-tier
parameters: per-call-site soak length (24h to 7d) and canonical-contract
format (typed interface vs. OpenAPI-style). Both are scoped to implementation,
not strategy.

Supporting artefacts:

- `seed-brief.md` (Wave 1 output)
- `adversarial/variant-a.md` through `adversarial/variant-e.md`
- `adversarial/debate-transcript.md` (3 rounds, anonymized)
- `adversarial/base-selection.md`
- `adversarial/diff-analysis.md`
- `adversarial/refactor-plan.md`
- `adversarial/merge-log.md`
- `adversarial/merged-output.md`
