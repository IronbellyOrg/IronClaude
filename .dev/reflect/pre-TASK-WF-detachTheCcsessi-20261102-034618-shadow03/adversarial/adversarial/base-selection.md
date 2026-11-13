# Base Selection (Step 3)

## Quantitative Scoring (50%)

| Metric (weight) | Card 1 analyzer | Card 2 qa | Card 3 refactorer |
|---|---|---|---|
| Requirement coverage (.30) | 0.75 (missed HC1, isatty) | 0.90 (all changes + ACs + HC) | 0.50 (structural lens only) |
| Internal consistency (.25) | 0.95 | 0.85 (X-001 tension: MINOR grade vs own "fails as written" text) | 0.95 |
| Specificity (.15) | 0.90 | 0.90 | 0.85 |
| Dependency completeness (.15) | 1.0 | 1.0 | 1.0 |
| Section coverage (.15) | 1.0 | 1.0 | 1.0 |
| **quant_score** | **0.898** | **0.918** | **0.815** |

## Qualitative Scoring (50%) — 30-criterion CEV summary

| Dimension | Card 1 | Card 2 | Card 3 | Key evidence |
|---|---|---|---|---|
| Completeness | 4/5 | 5/5 | 3/5 | Card2 traced changes 1-4 + AC1-AC6 + HC; Card3 two hunks |
| Correctness | 5/5 | 4/5 | 5/5 | Card2: X-001 severity error (conceded R2), HC5 overreach (halved) |
| Structure | 5/5 | 5/5 | 4/5 | Card3 card shape lacked a checked-surface list completeness |
| Clarity | 4/5 | 4/5 | 5/5 | — |
| Risk coverage | 4/5 | 4/5 | 4/5 | none quantified the grep exclusion (INV-007 later) |
| Invariant/edge | 4/5 | 4/5 | 5/5 | Card3 probed isatty branch; others did not |
| **qual_score** | **26/30 = 0.867** | **26/30 = 0.867** | **26/30 = 0.867** |

## Combined Scoring

| Variant | quant | qual | combined |
|---|---|---|---|
| Card 1 | 0.898 | 0.867 | **0.882** |
| Card 2 | 0.918 | 0.867 | **0.892** |
| Card 3 | 0.815 | 0.867 | **0.841** |

Top two within 5% → tiebreaker. Level 1 (debate points won): Card 1 took X-001 (MEDIUM adopted unanimously) and contributed C-002/C-006; Card 2 took C-003 (halved) and C-004. Effectively 2-2. Level 2 (correctness criteria): Card 1 = 5 > Card 2 = 4.

## Selected Base: Card 1 (analyzer)

Rationale: highest correctness (no conceded severity or scope errors), its X-001 position was adopted by the full panel, its evidence pairing (plan:82 + t5-checks.log:28) was the strongest on the shared finding. Card 2's HC1 finding and grep narrowing, Card 3's isatty finding, and the Round-2.5 probe corrections are incorporated per refactor-plan.md.
