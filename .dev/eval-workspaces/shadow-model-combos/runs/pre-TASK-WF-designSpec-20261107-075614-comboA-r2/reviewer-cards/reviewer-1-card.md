# Reviewer 1 card (analyzer): pre-execution audit, merge-guard plan vs spec

I audited the frozen spec (`.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`, "spec") and plan (`.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`, "plan"). I did not read the done/ history and did not use HEAD source.

## Analysis

The plan carries the spec's enumerations faithfully: 11 engage rows, 9 release rows, 9 resume rows, the 43 to 45 event count, the three RECONCILE reasons and the guard_status first-match mapping. The import chain at the pin closes no cycle, and Task 3's "imports only enum, dataclasses, re, is_conflict_cycle" is satisfiable if event types are compared by string literal.

The plan does carry four contract-level defects inherited from the spec. Three would make acceptance criteria unimplementable or silently wrong.

1. **Guard type mismatch (dict vs attribute).**
   - The fold returns "None or this dict" (spec 187-192).
   - Spec 114-125 (`classify_toggles`), 129-143 and 145-157 (the decision tables) access it by attribute: `guard.baseline`, `guard.phase`, `guard.owned_draft`.
   - Plan Task 5 asserts `state["draft_guard"]["phase"] == "held"` (plan 90), which is dict subscripting with a string value.
   - Plan Task 3 (plan 56) never says what type the fold returns or what string value `Phase.HELD` has.
   - Task 4 (plan 70) passes the guard into the decision functions by attribute.
   - An implementer must pick dict or dataclass, and Task 5's criterion fails under the dataclass choice (and vice versa) unless Phase is `str, Enum` with value `"held"`. The plan should pin one representation and the Phase string values.

2. **`resume_decision` cannot call `release_decision`.**
   - Spec row 4 (spec 166) and plan Task 4 (plan 77) have `resume_decision` "re-enter `release_decision` with `push_completed=True`".
   - `resume_decision`'s signature (spec 109, plan 70) has no `cycle_id`, `applied_edits` or `target_sha`.
   - `release_decision` row 8 (spec 156) needs `target_sha` to compare with `read.head_sha`.
   - The plan's acceptance (plan 77) says only "re-enter", with no expected `action` or `cause`, so a test can't tell RELEASE from HOLD.
   - It is unclear whether row 4 returns a RELEASE decision directly or a marker for the SKILL to call `release_decision`.

3. **`disabled_cause` is never set for `user_override`.**
   - The fold effect table (spec 206) sets `phase = DISABLED, owned_draft = False` for a user_override settle, but not `disabled_cause`.
   - Only the already_draft row sets it (spec 200).
   - `guard_status` (spec 112) distinguishes `DISABLED` + `user_override` from `DISABLED` + `already_draft` through that field.
   - Plan Task 3 acceptance (plan 60-61) tests the fold rows and the status mapping separately, so a fold that leaves `disabled_cause=None` for user_override still passes, and a real foreign-toggle run reports the wrong `merge_guard` value.
   - No fold-to-status test covers it.

4. **Resume at ordinal below 3 contradicts reconcile-before-edit.**
   - Spec section 3 (spec 58) says that on `--resume` at any ordinal and in either mode, "unsettled requests are reconciled before any edit".
   - `resume_decision` row 2 (spec 164) returns `REPORT_HELD` first, with no mutation, for `ordinal < 3` or `mode == OFF`, before row 3 reconciles.
   - Plan Task 4 (plan 76) pins row 2 winning over row 3.
   - A guard stuck in `ENGAGE_PENDING` or `RELEASE_PENDING` at ordinal below 3 is never settled.
   - This is low impact because ordinals below 3 never mutate, but the two statements disagree, and the plan neither notes nor resolves it.

Verified without findings: Task 2's count edits, the Task 3 `fix_cycle_id` / `next_cycle_number` / `pending_requests` / `held_cycle_published` contracts, the Task 3 `BRANCH_*` equality test, Task 4's `classify_toggles` slack arithmetic and failed-on-client-but-landed case, Task 5's import safety, Task 6's flag shape, and Task 7's script exit-code and repo-scope contract.

## Findings block

```findings-v2
{"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Fold returns a dict (subscripted in Task 5 acceptance) but decision functions read guard.phase/.baseline by attribute; plan never fixes the type or Phase string values, so Task 4 and Task 5 criteria can conflict.","refs":["INF-014","INF-017"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":187,"line_end":192,"quote":"returns `None` or this dict"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":118,"line_end":119,"quote":"observed = read.transitions - guard.baseline"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":90,"line_end":90,"quote":"state[\"draft_guard\"][\"phase\"] == \"held\""}]}
{"id":"F2","severity":"MAJOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"resume_decision row 4 must re-enter release_decision but has no cycle_id/target_sha/applied_edits inputs; Task 4 criterion gives no expected action/cause for row 4, so the contract is unimplementable as stated.","refs":["INF-015","INF-016"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":109,"line_end":109,"quote":"resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)"},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":166,"line_end":166},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":77,"line_end":77,"quote":"each re-enter `release_decision` with `push_completed=True`"}]}
{"id":"F3","severity":"MAJOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Fold row for settled(any, skipped, user_override) does not set disabled_cause, yet guard_status keys user_override off it; plan tests fold and status separately so a wrong report of off/unavailable would pass.","refs":["INF-018"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":206,"line_end":206},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":112,"line_end":112},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":60,"line_end":61}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Spec section 3 says resume reconciles unsettled requests at any ordinal, but resume row 2 returns REPORT_HELD first below ordinal 3 or in off mode; plan pins row-2 precedence without noting that pending requests stay unreconciled.","refs":["INF-016"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":58,"line_end":58},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":164,"line_end":165},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":76,"line_end":76}]}
```

reviewer_model_self_report: claude-gw-tier1b (Claude, Anthropic)

coverage_rows_observed: INF-003, INF-004, INF-005, INF-006, INF-007, INF-008, INF-009, INF-010, INF-011, INF-012, INF-013, INF-014, INF-015, INF-016, INF-017, INF-018, INF-019, INF-020, INF-021
