# Evidence Validation Report

Verdict: PASS. Independent validator returned complete full-reread result, persisted by parent before downstream consumption. No commands, sampling or structural assertions.

## Counts
| Group | Total | Revalidated | Dropped |
|---|---:|---:|---:|
| Source and plan | 17 | 17 | 0 |
| INF quotes | 8 | 8 | 0 |
| Machine/receipts | 4 | 4 | 0 |
| All | 29 | 29 | 0 |

## Retained checks
- refactor_find.py:53 and settings49,51,58 match.
- commands.py:2129-2157 success list, existing-review prefix, caller template/substitutions match.
- adversarial.md:39 existing-file comma list2-10.
- Plan19-26 constraints,37-39 red,67-71 green/real capture,79-86 docs; MRB1 plan79-84 and81 false scope claim exist.
- Wizard refs cli-contract44 and interview65 both stale follow-up; command swarm-wizard94 and wizard-guide216 broader stale list.
- Source1 matching-documentation obligation exists.
- All8 INF quotes exact substrings; no recompute, package ../../source.md resolves correctly.
- coverage-matrix fields/ratios match exactly; machine union0.5 retained with lexical unmatched003/005/007/008.
- Initial calibration0.70 and final card receipts0.73/0.73/0.87 match. Base3, labelHIGH present in card3.
- Actual merged contract statuspartial/convergence1/fallbacktrue/conflicts0 and31/31 record checked; model identity unverified.
- Counts blocking1,medium4,note3 with Low3 separate agree with merged receipt. Upstream dropped false resume claim is not a final-report drop.

## Tail
MR-B1 supported: plan79-84 limits three docs and81 denies skill/command changes; two wizard tables literally match missing follow-up, command94 lists it too. REPORT correctly rejects merge's no-sync advice against CLAUDE.md. Precision notes, no drops: wizard-guide216 says /code-review (a built-in per help85), not the namespaced string, so its stale-lens association is debated inference, not literal match. Blocker does not depend on it. command94 lacks --apply but REPORT only says includes missing command, accurate. Resume source ranges not directly re-read: only upstream drop cited in REPORT, not underlying code assertion. Fill header29/29/0; inferred report-claim counter remains0 because eight INF rows are quotes, not speculative claims. No structural assertions, no reexecution. Citation grounding PASS does not override partial merge status or FAIL plan verdict. No new finding or repair authorization.
