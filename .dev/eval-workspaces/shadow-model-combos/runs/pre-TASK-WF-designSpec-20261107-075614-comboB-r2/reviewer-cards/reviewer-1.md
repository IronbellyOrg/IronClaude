persona: analyzer
model_class: sonnet
model: claude-sonnet-5-5
model_observed: claude-gw-tier1b (self-report; alias for the sonnet class)

## Verdict

The plan covers the spec well, and I found no missing deliverable or dependency-order error in Tasks 2 to 5. Three T1 findings are real defects in the acceptance criteria: F1 (an unpassable check), F2 (an under-specified signature) and F3 (a report gap). I confirm F4 to F7 as stated. I add two more findings: one MINOR defect (F8) and one MINOR over-claim in a Task 5 criterion (F9).

## Findings (prose)

- **F1 (confirmed, blocking).** Task 7 requires the static scan to assert "every `gh` line carries `--repo` or a `repos/` path" (plan:113). It also requires the script to join `_RESOLUTION_SCRIPTS` and pass those tests (plan:108, 113).
  - `test_repo_resolution_prefers_origin_over_gh_default` runs `next(...)` for a line starting `REPO=` or `[ -n` that contains `gh repo view --json nameWithOwner` (tests/pr_submit/test_static_grep.py:545-550). That line carries neither `--repo` nor `repos/`.
  - A script without it raises StopIteration. A script with it breaks the plan's stricter scan.
  - The same strict scan would also catch the `command -v gh` check needed for exit 127, and any `die "gh ..."` message.
  - The existing `_repo_scoped` predicate already accepts the resolution idiom (test_static_grep.py:107-132, `_REPO_RESOLVE` at :35). The plan should say to reuse it and to limit the scan to real `gh` invocations.

- **F2 (confirmed, blocking).** `resume_decision` row 4 is "re-enter `release_decision` with `push_completed=True`" (source.md:166).
  - Its signature (source.md:109, plan:157) has no `cycle_id`, `applied_edits` or `target_sha`.
  - `GuardAction` has no re-enter value (source.md:43-47).
  - Plan:160 requires each row's test to assert `action`, `reason` and `cause`, and plan:164 demands a row-4 result. Neither says what row 4 returns.
  - The spec or plan must name the action (for example `RELEASE_AFTER_PUSH`) or state that the SKILL calls `release_decision` itself. The head proof must also stay mandatory, because release needs a confirmed head.

- **F3 (confirmed).** The spec says a halt with reason `draft_guard_unavailable` reports `unavailable` (source.md:73, :68). `guard_status(guard, mode, ordinal)` has no halt input.
  - Plan:148 pins "no record at ordinal 3 gives `released`", and an engage that halts before any guard event leaves no record. That halt is therefore reported as `released`.
  - Source.md:274 shows that `requested(draft)` followed by `settled(failed)` leaves `RELEASE_PENDING` with `owned_draft` false, which reports `unavailable`. Only a read or timeline failure at engage (rows 3 and 8) writes no event. Those cases are the gap.
  - Neither Task 8's Exit report (plan:124) nor Task 11 (plan:169) owns the override or tests it.

- **F4 (confirmed, MINOR).** The fold row `settled(any, skipped, user_override)` (source.md:206) does not say it sets `disabled_cause`, but `guard_status` needs it (source.md:73).
  - Plan:147 tests only `already_draft`. A fold that leaves the cause empty passes Task 3 and mis-reports.

- **F5 (confirmed, MINOR).** Task 1 records the base failures before any `make sync-dev` (plan:33).
  - The repo note says to record the baseline after `make install` and `make sync-dev` (docs/memory/reflect/deviation-patterns-post-release-v5.0.0.md:7).
  - Task 13 passes on "no failing id absent from the base record" (plan:199). A feature-caused mirror failure that is also in a stale baseline would be hidden.

- **F6 (confirmed, MINOR).** `GuardRead` uses `is_draft`, `head_sha` and `auto_merge_armed` (source.md:49-51). The script emits `isDraft`, `headRefOid` and `autoMergeRequest` (source.md:230). No task converts one to the other, and the SKILL has no python fence to do it.
  - A `merge_guard` helper or a documented SKILL step is needed.

- **F7 (confirmed, MINOR).** Task 9's Wave 0 bullet must say "no draft call is made" (plan:137), but its test must fail on `draft` gate wording (plan:140). The bullet's own text trips the test unless the test targets a condition phrase rather than the bare word.

- **F8 (new, MINOR).** The row 3 `RECONCILE` reasons are ambiguous at the edges. Plan:163 copies source.md:165 ("live state not matching settles `not_applied`; anything else is `ambiguous`").
  - A live state that mismatches the request while `observed == run_toggles + 1` is a foreign toggle, yet it settles `not_applied`, which the fold treats as "no toggle landed".
  - An unreadable timeline under `classify_toggles` has no stated reason either.
  - The order of the three checks should be pinned.
  - I found no data loss. The result is a possible wrong `not_applied` settle that clears a pending key.

- **F9 (new, MINOR).** Plan:175 says the Task 5 command exercises "the exact key-set assertions that use `_NEW_KEY_DEFAULTS`" in all three files. In `tests/pr_submit` only `test_run_log.py` references `_NEW_KEY_DEFAULTS` (:326, :418-419). `test_idempotency.py` and `test_static_grep.py` add nothing to that check. This is harmless but over-claims.

**Checked and found fine.**
- Task 4 criteria against the three decision tables (source.md:90-132): rows and parameters match.
- Task 3 `guard_status` mapping against source.md:73.
- The import graph for a cycle: `run_log` to `merge_guard` to `conflicts` to `fsm` and `models` has none (run_log.py:24, conflicts.py:34-35, fsm.py:26-28).
- The prefixes `sync-` and `conflict-` (conflicts.py:46).
- The `BRANCH_*` string equality with `BRANCH_A_LANDED`, `BRANCH_B_NOT_LANDED` and `BRANCH_C_AMBIGUOUS` (recovery.py:40-42).
- Task order and dependencies.

## Findings block

```findings-v2
{"id":"F1","severity":"MAJOR","blocking":true,"category":"unpassable-check","lens":"reflect-pre","claim":"Task 7 requires every gh line to carry --repo or repos/, but the required _RESOLUTION_SCRIPTS tests need a `gh repo view --json nameWithOwner` line (no --repo); `command -v gh` lines also break the scan. Reuse _repo_scoped.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":108,"line_end":113,"quote":"asserts every `gh` line carries `--repo` or a `repos/` path"},{"role":"plan","path":"tests/pr_submit/test_static_grep.py","line_start":545,"line_end":550,"quote":"gh repo view --json nameWithOwner"},{"role":"plan","path":"tests/pr_submit/test_static_grep.py","line_start":107,"line_end":132}]}
{"id":"F2","severity":"MAJOR","blocking":true,"category":"contradiction","lens":"reflect-pre","claim":"resume_decision row 4 re-enters release_decision, but its signature lacks cycle_id, applied_edits and target_sha and GuardAction has no re-enter value; the Task 4 row-4 criterion cannot be written, and omitting the head proof would release without confirming the head.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":109,"line_end":109},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":166,"line_end":166,"quote":"re-enter `release_decision` with `push_completed=True`"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":157,"line_end":164}]}
{"id":"F3","severity":"MAJOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"A halt with reason draft_guard_unavailable must report `unavailable` (spec), but guard_status has no halt input and a no-record engage halt at ordinal 3 maps to `released`; no task assigns or tests the override.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":73,"line_end":73,"quote":"A halt with reason `draft_guard_unavailable` reports `unavailable`."},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":148,"line_end":148},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":124,"line_end":129}]}
{"id":"F4","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"The fold row for settled(any, skipped, user_override) does not set disabled_cause, yet guard_status needs it; Task 3's fold criterion tests only already_draft.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":206,"line_end":206},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":147,"line_end":147}]}
{"id":"F5","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Task 1 records the baseline before make sync-dev, so the Task 13 comparison with the stale baseline can hide feature-caused mirror failures.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":33,"line_end":33},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":199,"line_end":199}]}
{"id":"F6","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"GuardRead field names differ from the script JSON keys (isDraft, headRefOid, autoMergeRequest) and no task owns the conversion.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":49,"line_end":51},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":230,"line_end":230}]}
{"id":"F7","severity":"MINOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"The Wave 0 bullet must say no draft call is made, yet its test must fail on `draft` gate wording; the test needs a narrower pattern.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":137,"line_end":140}]}
{"id":"F8","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Resume row 3 leaves the check order undefined: a live state that mismatches the request while observed==run_toggles+1 (foreign toggle) would settle not_applied, and unreadable-timeline handling has no stated reason.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":165,"line_end":165},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":163,"line_end":163}]}
{"id":"F9","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Task 5 says the pytest command covers the exact key-set assertions using _NEW_KEY_DEFAULTS in three files; only test_run_log.py uses that constant.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":175,"line_end":175},{"role":"plan","path":"tests/pr_submit/test_run_log.py","line_start":418,"line_end":419}]}
```

reviewer_model_self_report: claude-gw-tier1b (Claude, run as the analyzer reviewer persona)
