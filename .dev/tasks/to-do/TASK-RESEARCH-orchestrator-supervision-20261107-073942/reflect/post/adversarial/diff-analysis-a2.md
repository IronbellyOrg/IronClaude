# Diff analysis (Step 1), attempt 2

Named -a2 because the freshness hook holds a stale Read record for `diff-analysis.md` from attempt 1 (TASK:457) although that file no longer exists, so a Write to it is blocked.

Variants: V1 = reviewer-1 (sonnet:analyzer, weight 0.62), V2 = reviewer-2 (haiku:qa, 0.71), V3 = reviewer-3 (opus:refactorer, 0.71). Reference: T1 card (t1-card.md). Focus: correctness, coverage, deviation-classification.

## Content differences / contradictions

| Point | V1 | V2 | V3 | T1 | Level |
|---|---|---|---|---|---|
| X-1 D-1 severity | Drift Low (ruling forced it) | - | Drift Medium (stale before ruling) | Drift Medium | L3 |
| X-2 D-4 | refuted (deliberate cross-ref to GAPS:82) | - | not checked | Drift Low | L2 |
| X-3 D-12 | - | - | Drift Low | Authorized expansion | L3 (boundary) |
| X-4 D-3 vs D-9 overlap | D-3 Drift Low | D-3 Drift Low, D-9 ND Low | D-9 ND Low | both listed | L2 |
| X-5 D-13 | - | - | Drift Low (new) | absent | L2 |
| X-6 D-8 severity | - | ND Medium | - | ND (no severity) | L1 |

## Agreement points

D-2 Drift Low (V1, V3, T1); D-5 and D-9 Necessary deviation (V2, V3, T1); Regression 0 (all); D-10, D-11 Authorized (V3, T1).

## Shared assumptions

- A-001 STATED: the owner ruling (TASK:456) freezes the report outside a gate.
- A-002 UNSTATED: the ruling's scope is only the Gaps Log count, not the "Open: 75" anchors. Promoted to X-1 debate (L3).
