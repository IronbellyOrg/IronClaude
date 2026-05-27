---
phase: merge
base_variant: 3
convergence_score: 0.82
status: PASS
created: 2026-05-27T00:00:00Z
---

# Merge Log

## Source Variants

- Variant 1: `variant-1-scribe.md` (opus:scribe — docs-first)
- Variant 2: `variant-2-pm.md` (sonnet:pm — process-first)
- Variant 3: `variant-3-architect.md` (haiku:architect — tooling-first) [BASE]

## Convergence

- Quantitative score: **0.82** (above 0.75 target)
- High agreement on tooling + docs as foundation; low-stakes disagreement on cohort cadence timing.
- Status: **PASS** — proceed to merged-output.

## Merge Operations

| Element | Origin | Action | Notes |
|---------|--------|--------|-------|
| `make onboard` target | V3 | INCLUDE | Foundation |
| Smoke-test marker | V3 | INCLUDE | Foundation |
| Hook `--explain` mode | V3 | INCLUDE | Highest-leverage single fix |
| `superclaude doctor --contributor` | V3 | INCLUDE | Sprint 1 |
| `QUICKSTART.md` | V1 | INCLUDE | Sprint 1; references V3's `make onboard` |
| Glossary doc | V1 | INCLUDE | Sprint 1 |
| Failure-mode appendix in CONTRIBUTING | V1 | INCLUDE | Sprint 1; cross-referenced with V3 `--explain` |
| PR template "first PR" checkbox | V2 | INCLUDE | Sprint 1 |
| Auto-comment Action | V2 | INCLUDE | Sprint 1; references V1 docs |
| Shepherd-available list (no rotation) | V2 | INCLUDE (DOWNGRADED) | Sprint 1; formal rotation deferred |
| Worked-example skill PR | V1 | DEFER | Sprint 2 |
| 2-week cohort threads | V2 | DEFER | Sprint 2 conditional on volume |
| Sprint retro on contributors | V2 | DEFER | Sprint 2 |
| Codespaces / devcontainer | V3 | DEFER | Sprint 2 |
| Maintainer-of-the-week rotation | V2 | DROP | Insufficient maintainer pool signal |
| Three-doc reading rule | V1 | DROP | Replaced by simpler auto-comment 3-link |

## Conflict Resolutions

1. **Cohort cadence (V2 vs V3 critique)** — RESOLVED by deferring to Sprint 2 with explicit volume threshold (4+ first-PRs per 2-week window).
2. **Worked-example PR (V1 vs V2/V3 critique on maintenance burden)** — RESOLVED by deferring to Sprint 2; documented update-trigger ("when skill template changes").
3. **Docs vs hooks (V1 vs V3 critique)** — RESOLVED by composing: hooks self-explain at point of failure, docs catch the rare residual case. Both, not either.
4. **Codespaces only vs local-only (V2 vs V3 critique)** — RESOLVED by keeping `make onboard` local-first in Sprint 1; devcontainer additive in Sprint 2.

## Unresolved Conflicts (acknowledged for downstream)

None blocking. All conflicts resolved via scope sequencing.

## Provenance

- Base = V3 (highest base-selection score 22/25).
- 6 elements from V3 included.
- 3 elements from V1 included (QUICKSTART, glossary, failure-mode appendix).
- 3 elements from V2 included (PR template, auto-comment, shepherd list).
- 4 elements deferred to Sprint 2.
- 2 elements dropped.
- Total merged feature set: 12 sprint-1 items + 4 sprint-2 items.
