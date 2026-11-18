persona: analyzer
model_class: sonnet
model: claude-sonnet-5-5

## Findings block
```findings-v2
{"id":"F1","severity":"MAJOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 7 criteria check only key presence and the null-timeline case. None feeds N events and asserts transitions==N, or asserts --paginate in the recorded call, so a one-event-type or non-paginated count passes.","refs":["FR-12","FR-14"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":111,"line_end":113,"quote":"`--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":230,"line_end":230,"quote":"gh api --paginate"}]}
{"id":"F2","severity":"MAJOR","blocking":false,"category":"data-loss","lens":"reflect-pre","claim":"After a held cycle with an unpublished fix (release row 9), the next cycle sees engage row 7 already_held. If it has zero edits, release row 7 returns RELEASE(no_edits) and marks the PR ready with the earlier unpublished fix, against the keep-draft rule.","refs":["FR-8","FR-9","FR-17"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":155,"line_end":157,"quote":"| 7 | `applied_edits == 0` | `RELEASE(cause=no_edits)` |"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":139,"line_end":139,"quote":"`NOOP(already_held)`"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":69,"line_end":69,"quote":"Any exit after engage with no confirmed push and no zero-edit proof"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":75,"line_end":75,"quote":"returns `RELEASE` with cause `no_edits`"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec fold row returns a settled not_applied ready request to RELEASE_PENDING when a failed release preceded it; Task 3 tests only the HELD outcome, so that variant can be wrong unnoticed.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":201,"line_end":201,"quote":"or `RELEASE_PENDING` when a failed release preceded it"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":60,"line_end":60,"quote":"a ready request followed by `not_applied` gives phase `HELD` with `unsettled == 0`"}]}
```

calibration:
  per_finding:
    F1: 0.8
    F2: 0.55
    F3: 0.75

reviewer_model_self_report: claude-gw-tier1b
