# Recipe Ledger analysis

Stage 1; 60 runs; seed 20261119; bootstrap draws 2000.

## Decision (MR 5.8, RL against Z0 and K)

RL: do not adopt (failed: D1, D2, D3, D6). Blocking gate failed: D6.

## Shares of the gain, one line each

H share (Z0 - Z0raw): n/a
prompting share (K - Z0): -0.010
redesign share (RL - Z0): +0.036

## Claim wording (REQ-45)

Claim: raises the per-run found fraction; consistency is expected only for I4 and I7 (classes C4 and C8), and only for Redesign 1 at the high end of its range.

## Per arm (pooled over documents)

| arm | runs | found_fraction_mean | half_found_share | jaccard_mean | consistent_items | stable_hit_rate | wrong_blockers_per_run | found_any_mean | found_blocking_mean | nonprobe_findings_per_run | elapsed_mean | elapsed_median | tokens_per_run | kills | retries | reasks | fallbacks | invalid | check_skipped |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K | 20 | 0.213 | 0.150 | 0.402 | 4 | 0.444 | 1.400 | 0.213 | 0.029 | 7.400 | 108.729 | 117.257 | 20872.100 | 4 | 0 | 0 | 0 | 0 | 0 |
| RL | 20 | 0.259 | 0.150 | 0.356 | 6 | 0.462 | 0.500 | 0.259 | 0.053 | 3.150 | 142.091 | 141.767 | 24339.150 | 4 | 0 | 0 | 0 | 0 | 0 |
| Z0 | 20 | 0.223 | 0.150 | 0.314 | 5 | 0.455 | 0.950 | 0.223 | 0.040 | 8.350 | 100.333 | 99.762 | 21035.750 | 1 | 0 | 0 | 0 | 1 | 0 |

Elapsed time is reported as mean and median (REQ-29); re-asks are a column of their own, apart from retries.

## Per document

- K HO-2: found fraction 0.220, elapsed mean 137.5, median 147.1, p90 150.3, consistent items 2
- K HO-3: found fraction 0.117, elapsed mean 119.4, median 124.8, p90 143.1, consistent items 1
- K HX-1: found fraction 0.500, elapsed mean 81.8, median 67.1, p90 124.8, consistent items 1
- K HX-3: found fraction 0.017, elapsed mean 96.2, median 81.3, p90 124.7, consistent items 0
- RL HO-2: found fraction 0.220, elapsed mean 159.4, median 145.4, p90 185.3, consistent items 2
- RL HO-3: found fraction 0.167, elapsed mean 152.0, median 157.7, p90 182.8, consistent items 1
- RL HX-1: found fraction 0.600, elapsed mean 143.9, median 140.1, p90 192.6, consistent items 2
- RL HX-3: found fraction 0.050, elapsed mean 113.0, median 109.2, p90 130.0, consistent items 1
- Z0 HO-2: found fraction 0.260, elapsed mean 115.8, median 121.7, p90 144.9, consistent items 3
- Z0 HO-3: found fraction 0.100, elapsed mean 110.4, median 103.4, p90 138.2, consistent items 1
- Z0 HX-1: found fraction 0.500, elapsed mean 68.3, median 76.8, p90 78.2, consistent items 1
- Z0 HX-3: found fraction 0.033, elapsed mean 106.9, median 102.7, p90 132.9, consistent items 0

## Reach per class with Wilson intervals (95%)

| arm | class | hits | runs x items | rate | low | high |
|---|---|---|---|---|---|---|
| K | unassigned | 24 | 180 | 0.133 | 0.091 | 0.191 |
| RL | unassigned | 30 | 180 | 0.167 | 0.119 | 0.228 |
| Z0 | unassigned | 26 | 180 | 0.144 | 0.101 | 0.203 |

## Ledger checks and re-asks per arm (DESIGN 12.5)

| arm | over_budget recipe | over_budget lens | recipe_missing | unknown_item | classes_lost | re-asks asked | re-asks accepted | yield with re-ask (runs) | yield without re-ask (runs) |
|---|---|---|---|---|---|---|---|---|---|
| K | 0 | 0 | {} | 0 | {} | 0 | 0 | n/a (0) | 0.213 (20) |
| RL | 0 | 8 | {'C1': 1, 'C2': 2, 'C3': 1, 'C4': 1, 'C7': 1} | 3 | {'C1': 1, 'C3': 1, 'C7': 3} | 0 | 0 | n/a (0) | 0.259 (20) |
| Z0 | 0 | 0 | {} | 0 | {} | 0 | 0 | n/a (0) | 0.223 (20) |

none_found share: reviewer-runs with a NONE FOUND row of the class over reviewer-runs with a row of the class.

| arm | class | none_found | ran | share |
|---|---|---|---|---|
| RL | C1 | 0 | 18 | 0.000 |
| RL | C2 | 3 | 34 | 0.088 |
| RL | C3 | 0 | 18 | 0.000 |
| RL | C4 | 0 | 36 | 0.000 |
| RL | C5 | 0 | 20 | 0.000 |
| RL | C6 | 0 | 20 | 0.000 |
| RL | C7 | 0 | 16 | 0.000 |
| RL | C8 | 0 | 20 | 0.000 |

## Rows per lens (mean rows of a ledger, by reviewer id)

| arm | reviewer id | mean rows |
|---|---|---|
| RL | t2b-1 | 12.450 |
| RL | t3-1 | 9.353 |
| RL | t4-1 | 10.579 |

## Reach per class per reviewer id

| arm | class | reviewer id | rows | ledger rows | selection | act | merge survival |
|---|---|---|---|---|---|---|---|
| K | unassigned | t2b-1 | 180 | 0 | 0 | 0 | 69 |
| K | unassigned | t3-1 | 180 | 0 | 0 | 0 | 24 |
| K | unassigned | t4-1 | 180 | 0 | 0 | 0 | 34 |
| RL | unassigned | t2b-1 | 180 | 180 | 87 | 18 | 30 |
| RL | unassigned | t3-1 | 180 | 180 | 94 | 14 | 16 |
| RL | unassigned | t4-1 | 180 | 180 | 85 | 17 | 22 |
| Z0 | unassigned | t2b-1 | 180 | 0 | 0 | 0 | 77 |
| Z0 | unassigned | t3-1 | 180 | 0 | 0 | 0 | 20 |
| Z0 | unassigned | t4-1 | 180 | 0 | 0 | 0 | 21 |

## Gates

- RL D1: FAIL HO-2: median ratio 1.195, mean ratio 1.377, p90 ratio 1.279; HO-3: median ratio 1.525, mean ratio 1.377, p90 ratio 1.323; HX-1: median ratio 1.824, mean ratio 2.109, p90 ratio 2.463; HX-3: median ratio 1.063, mean ratio 1.057, p90 ratio 0.978; kills 4 (0.067)
- RL D2: FAIL difference 0.036, lower bound -0.090
- RL D3: FAIL candidate 6, control 5
- RL D4: pass wrong blockers difference -0.450, clean twins n/a
- RL D5: not run no planted documents in --sets
- RL D6: FAIL regressed items: HO-2/GT2, HO-2/GT3 (blocking gate)
- RL D7: pass gain over K 0.046

## Time: planned and measured (REQ-31)

| quantity | planned | measured |
|---|---|---|
| b, smallest Z0 median of the slowest reviewer (s) | 100.0 | 76.5 |
| break-even row cost, 14 rows (s) | 2.07 | 1.48 |
| luna cost per row c (s) | 2.00 | 2.43 |
| luna row cap (rows) | 14 | 8 |

## Stages (REQ-41)

Per-row detail is in stages.jsonl (extraction is null for RL: there is no extractor).

## Definitions

- found fraction: covered items over items of the document (judge's `gt_covered_any`); pooled means are over runs.
- consistent: an item reached in at least 60% of the runs of an arm; stable-hit rate is consistent items over items reached at all.
- non-probe findings: findings lines that reach the merge without `probe` and without `src: ledger`.
- bootstrap: documents first, then runs; the lower bound is the 5th percentile of the difference.
