---
blind_mode: true
convergence_score: 0.82
adversarial_status: pass
---

# Merged Output — Canonical Auth Consolidation Plan

This is the adversarial-merge consensus across Agent A through Agent E. It is
the source for the project-level merged-requirements.md.

## Strategy Statement

Consolidate the three duplicate auth modules to a single canonical module via
a strangler-fig facade. Drive the consolidation with a behavioural-equivalence
matrix and an executable canonical contract. Verify equivalence per-call-site
via shadow-and-diff at cutover time. Model legitimate per-surface divergence
as explicit policy on the canonical module, not as permanent adapter logic.

## Load-Bearing Elements

1. Canonical facade with per-call-site flag and global kill-switch.
2. Multi-criteria baseline-selection audit (coverage, hardening posture,
   behavioural-equivalence-matrix score) — coverage alone does not pick the
   baseline.
3. Canonical contract as typed interface plus property-based test suite,
   written against the facade's observed traffic.
4. Per-call-site shadow-and-diff window at cutover time.
5. Explicit per-surface divergence policy on the canonical module; transitional
   adapters carry end-of-life dates.

## Acceptance Criteria

- Single canonical module owns every production auth code path post-cutover.
- Per-call-site rollback MTTR under 5 minutes; global kill-switch MTTR under
  2 minutes.
- Test coverage on the canonical module meets or exceeds the union of legacy
  modules' coverage; every drift-derived incident has a regression test.
- Zero P0/P1 incidents attributable to the migration.
- Legacy modules retired (or quarantined behind a clear deprecation marker) by
  end of migration.

## Open Implementation-Tier Parameters

- Soak length for per-call-site shadow window (range under debate: 24 hours to
  7 days).
- Canonical-contract format (typed interface plus property tests, or
  OpenAPI-style plus contract tests).
