# n2-terra RESULT (Batch 3 re-run)

Row: t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-terra. No scoring.
Provenance: muse t2b-1 (all 3 packages) and grok t4-2 (all 3) were run fresh via tools/run-reviewer.sh by a bulk driver (/tmp/b3/job.sh) with coordinator approval; haiku t4-1 and terra t2-1 were run by this worker, one at a time. Earlier stopped/contaminated outputs are kept in place (RESULT.stopped-attempt.md, _prior-stopped-attempt, n2-terra-contaminated-20261111) and not used. All 12 meta.json files have model_ok=true and findings_block=true before merging. Observed model for grok is reported as grok-4.7-build (accepted by the script). No reviewer needed the unpassable-ac fix. Muse outage no longer present: muse observed as muse-wonder-1.0.
Findings counts are from each reviewer's findings-v1 block; 'in merged' = merged-1.md cluster members from that reviewer.

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings (blocking) in report |
|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 154 | 16929 | valid | 4 (0) |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 263 | 61063 | valid | 10 (2) |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 915 | 58924 | valid | 4 (1) |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 23 | 415 | THIN (<1000 tokens) | 0 (0) |

Total wall (sum of reviewer runs) 1355 s, total output tokens 137331.

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings (blocking) in report |
|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 127 | 14932 | valid | 7 (2) |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 141 | 29966 | valid | 5 (2) |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 754 | 48614 | valid | 4 (3) |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 18 | 509 | THIN (<1000 tokens) | 0 (0) |

Total wall (sum of reviewer runs) 1040 s, total output tokens 94021.

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | flag | findings (blocking) in report |
|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 110 | 13528 | valid | 6 (1) |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 242 | 56517 | valid | 10 (1) |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 827 | 54123 | valid | 3 (1) |
| t2-1 | gpt-6.1-terra | gpt-6.1-terra | 1 | 20 | 515 | THIN (<1000 tokens) | 0 (0) |

Total wall (sum of reviewer runs) 1199 s, total output tokens 124683.

## Merge (superclaude review merge, round 1, custom resolution with this row's 4 ids/models)
| package | merged-1.md | merged clusters | blocking clusters | verdict |
|---|---|---|---|---|
| TASK-WF-designSpec-20261107-075614 | combos/n2-terra/TASK-WF-designSpec-20261107-075614/merged-1.md | 4 | 2 (L1, L2) | FAIL |
| TASK-WF-makeTheAliasOnly-20261105-051649 | combos/n2-terra/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md | 3 | 2 (L1, L2) | FAIL |
| TASK-WF-design-20261108-041415 | combos/n2-terra/TASK-WF-design-20261108-041415/merged-1.md | 4 | 1 (L1) | FAIL |

Notes:
- makeTheAliasOnly: the merge warned "t2b-1: findings block problem (1 error), anchor2 must have at most 200 characters"; block_ok=false for muse, yet its findings still appear as cluster members. Reported as is, report not edited.
- gpt-6.1-terra produced a thin report with 0 findings on all 3 packages (415-515 tokens); merged as is, as the coordinator allowed.
