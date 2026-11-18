# Reviewer 1 card

I checked the decision tables, the fold, `classify_toggles`, the resume rows and the plan tasks that implement them (3, 4, 5, 7 and 8). I read the whole plan and spec.

**What held**
- The `classify_toggles` thresholds work for a failed-on-client-but-landed draft call. `failed_mutations` gives one unit of slack, so the result is `ok`, not `foreign`.
- A second cycle after `RELEASED` reaches `ENGAGE` (engage row 11) with the right expected draft state of False.
- A resumed run cannot read its own draft as the original one, because the fold keeps `original_is_draft` from the first record.
- Resume row 2 precedence over row 3 is pinned by a Task 4 criterion.
- The `published` path (resume row 4) and the real `BRANCH_*` strings are covered by Task 4 and Task 11.
- Task 3 and Task 4 criteria are failable for the fold rows, the `guard_status` mapping and each decision row.
- Task dependencies are complete for the import chain.

**What I refute**
- I refute T1's claim that the import cycle is a risk. The base-commit facts show no cycle.

**Defects**
- F1 (confirms T1's F1): the Task 7 criteria never check the timeline count semantics.
- F2 (new): a zero-edit cycle can release a PR that still holds an earlier cycle's unpublished fix. Trace:
  1. Cycle fix-1 engages, applies edits, then ends in `HOLD(head_mismatch or push_not_completed)` (release row 9). The phase stays `HELD`.
  2. Cycle fix-2 reaches engage row 7, which returns `NOOP(already_held)`, so the guard carries over.
  3. Fix-2 applies zero edits, so release row 7 returns `RELEASE(no_edits)` before row 9 is considered. The PR goes ready with fix-1's fixes unpublished.
  4. This contradicts the spec's rule that an exit with unpublished fixes keeps the PR draft. The plan's Task 4 criterion requires exactly this release, so a correct implementation of the plan ships the behaviour.
- F3 (confirms T1's F5): the fold's return path to `RELEASE_PENDING` after a settled `not_applied` ready request is untested.

## Findings block
```findings-v2
{"id":"F1","severity":"MAJOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 7 criteria check only key presence and the null-timeline case. None feeds N events and asserts transitions==N, or asserts --paginate in the recorded call, so a one-event-type or non-paginated count passes.","refs":["FR-12","FR-14"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":111,"line_end":113,"quote":"`--read` prints one JSON line with `ok`, `state`, `isDraft`, `headRefOid`, `autoMergeRequest`, `transitions`, `complete`"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":230,"line_end":230,"quote":"gh api --paginate"}]}
{"id":"F2","severity":"MAJOR","blocking":false,"category":"data-loss","lens":"reflect-pre","claim":"After a held cycle with an unpublished fix (release row 9), the next cycle sees engage row 7 already_held. If it has zero edits, release row 7 returns RELEASE(no_edits) and marks the PR ready with the earlier unpublished fix, against the keep-draft rule.","refs":["FR-8","FR-9","FR-17"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":155,"line_end":157,"quote":"| 7 | `applied_edits == 0` | `RELEASE(cause=no_edits)` |"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":139,"line_end":139,"quote":"`NOOP(already_held)`"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":69,"line_end":69,"quote":"Any exit after engage with no confirmed push and no zero-edit proof"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":75,"line_end":75,"quote":"returns `RELEASE` with cause `no_edits`"}]}
{"id":"F3","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec fold row returns a settled not_applied ready request to RELEASE_PENDING when a failed release preceded it; Task 3 tests only the HELD outcome, so that variant can be wrong unnoticed.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":201,"line_end":201,"quote":"or `RELEASE_PENDING` when a failed release preceded it"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":60,"line_end":60,"quote":"a ready request followed by `not_applied` gives phase `HELD` with `unsettled == 0`"}]}
```
