# Merge Log — case 4 rerun

## Metadata

- Base: Variant 1 (architect)
- Executor: sc:adversarial merge-executor behavior (probe rerun)
- Changes planned: 3
- Changes applied: 3
- Status: success
- Timestamp: 2026-05-27

## Anchor Preservation

| Anchor (from seed-brief.md) | Status in merged-requirements.md | Notes |
|------------------------------|------------------------------------|-------|
| pytest characterization required | Preserved | FR-1 |
| vitest as the explicit target framework | Preserved | FR-2, FR-3 |
| test suite as the migration unit | Preserved | FR-4 |
| migration must not silently drop coverage or invariants | Preserved | NFR-2, AC-2 |

## Dropped Anchors

None. All seed-brief `must_preserve` items appear in the merged output.

## Out-of-Scope Promotions

None. No `out_of_scope` items from seed-brief were promoted into merged requirements.

## Applied Changes

1. Added explicit "calendar end-date target + accountable owner" requirement (from Variant 2). Reduces indefinite-parallel-run risk identified by both advocates.
2. Added committed concept-map doc as a functional requirement (from Variant 2). Persistent artifact, useful beyond the migration.
3. Refined cutover PR to be a single config-only PR (from Variant 2). Minimizes blast radius at the cutover moment.

## Convergence

- Final convergence score: 0.82 (above 0.75 threshold)
- Status: PASS
