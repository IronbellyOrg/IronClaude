# n2-sonnet RESULT (Batch 3)

Row: t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t1b-1=claude-sonnet-5-5. Run fresh on 2026-11-12 (04:32-05:11 UTC), after the cooldown; 2 runs at once at most. No scoring.
Columns: findings = JSON lines in the reviewer's own findings-v1 block; blocking = those marked blocking:true. Thin = under 1000 output tokens. No "unpassable-ac" appeared, so no category normalisation was needed. Wall seconds are summed per reviewer (runs overlapped 2 at a time, so elapsed time is lower).

## TASK-WF-designSpec-20261107-075614

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking | block ok in merge |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 131 | 16315 | valid | 5 | 0 | true |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 38 | 6202 | valid | 0 | 0 | true |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 977 | 68458 | valid | 3 | 1 | true |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 259 | 34457 | valid | 6 | 0 | true |

Total: 1405 s summed wall, 125432 output tokens. Merged report: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos/n2-sonnet/TASK-WF-designSpec-20261107-075614/merged-1.md (5 ledger rows, 1 blocking).

## TASK-WF-makeTheAliasOnly-20261105-051649

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking | block ok in merge |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 147 | 16592 | valid | 5 | 3 | false |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 203 | 46436 | valid | 8 | 2 | true |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 659 | 42341 | valid | 2 | 1 | true |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 307 | 44109 | valid | 7 | 1 | true |

Total: 1316 s summed wall, 149478 output tokens. Merged report: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos/n2-sonnet/TASK-WF-makeTheAliasOnly-20261105-051649/merged-1.md (3 ledger rows, 2 blocking).

## TASK-WF-design-20261108-041415

| reviewer | model | observed model | attempts | wall s | output tokens | invalid/thin | findings | blocking | block ok in merge |
|---|---|---|---|---|---|---|---|---|---|
| t2b-1 | muse-wonder-1.0 | muse-wonder-1.0 | 1 | 63 | 9546 | valid | 5 | 2 | true |
| t4-1 | claude-haiku-5-5 | claude-haiku-5-5 | 1 | 229 | 50912 | valid | 9 | 3 | true |
| t4-2 | grok-4.7 | grok-4.7-build | 1 | 934 | 58738 | valid | 4 | 2 | true |
| t1b-1 | claude-sonnet-5-5 | claude-sonnet-5-5 | 1 | 137 | 15216 | valid | 4 | 0 | true |

Total: 1363 s summed wall, 134412 output tokens. Merged report: /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos/n2-sonnet/TASK-WF-design-20261108-041415/merged-1.md (7 ledger rows, 3 blocking).

## Notes
- The reviewer runs were started at 04:32 by an earlier launch (xargs, 2 at once) of this same row; I adopted them instead of starting duplicates. All 12 passed the observed-model check on attempt 1 (grok-4.7 observed as grok-4.7-build, accepted by the script).
- makeTheAliasOnly: the merge reports block ok false for t2b-1 (muse) but still ingested its five findings; the round was not refused, so no rerun.
- A first merge attempt left ledgers that the merge then refused as 'expects round 2'; I moved them to combos/n2-sonnet/<package>/stale-20261112/ (nothing deleted) and merged again from clean ledgers.
- Earlier outputs from batch-3 attempt 1 stay quarantined in reviews/combos/n2-sonnet-contaminated-20261111 and n2-sonnet-superseded-20261112 and were not used.
