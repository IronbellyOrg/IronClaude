# Diff Analysis — case 4 rerun (pytest → vitest)

## Metadata

- Generated: 2026-05-27
- Variants compared: 2 (architect, refactorer)
- Total differences found: 4
- Categories: structural (1), content (2), contradictions (0), unique (1), shared assumptions (3)

## Structural Differences

| # | Area | Variant 1 (architect) | Variant 2 (refactorer) | Severity |
|---|------|------------------------|--------------------------|----------|
| S-001 | Migration cadence | Per-suite PRs over an extended parallel-run window | Batched PRs in a short, time-boxed window ending with a single config-only cutover PR | Medium |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | Dual-runner duration | Long (until parity + one release cycle) | Short (target ≤ 4 weeks) | Medium |
| C-002 | pytest deps removal timing | Final PR after one release of vitest-only | Immediately at cutover + post-cutover dep-prune PR | Low |

## Shared Assumptions (no diff)

| # | Assumption |
|---|------------|
| A-001 | pytest must be characterized before any rewrite |
| A-002 | Coverage must not regress at any point |
| A-003 | The underlying code under test must be JS/TS — otherwise the migration is invalid |

## Unique Items

| # | Variant | Item |
|---|---------|------|
| U-001 | Variant 2 | Persistent concept-map doc (pytest → vitest equivalents) that lives on after migration |

## Contradictions

None. Both proposals share the same invariants (characterization, coverage non-regression, defined cutover criterion). They differ on cadence/duration policy, not principle.
