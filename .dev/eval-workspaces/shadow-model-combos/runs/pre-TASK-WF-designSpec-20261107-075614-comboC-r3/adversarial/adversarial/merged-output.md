<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (reviewer-3, refactorer) -->
<!-- Merge date: 2026-11-13 -->

# Merged reflection verdict

## Summary

The task structure mostly holds up against the base commit. There is no import cycle, the event-count and key-set pins are named correctly, and the script and test-import approach follows existing code. The merged review has ten findings, none blocking. Two are MAJOR:
- M1: the resume decision cannot supply what the release decision needs, so a vacuous head check would pass every listed test.
- M6: the FR-16 release retry has no bound and no test body.

The other eight are MINOR:
- M2: the Wave 0 wording is ambiguous, and its placement is only relative to Wave 1.
- M3: the classification wording covers fewer verbs than the Constraints rule.
- M4: three test files are edited by tasks with no declared order, and four tasks rely on Task 1 without declaring it.
- M5: nothing tests that the guard, push triad and re-trigger share one cycle id.
- M7: every existing Wave bullet line is a classification key.
- M8: `guard_status` takes no halt reason.
- M9: the crash-boundary tests are narrower than spec section 7.
- M10: exit paths after engage have no held-report test.

M1 and M2 originate in the spec, so a spec amendment is recommended alongside the plan fix. Severity stays non-blocking because a failing test would later reveal the gaps.

## Findings

<!-- Source: Base (original, modified) - category changed to unpassable-check and the vacuous-head-check mechanism added from Variant 1 F1, per Change #1 -->
### M1 (MAJOR, blocking:false, unpassable-check): the resume decision cannot supply what the release decision needs

Claim: `resume_decision` row 4 must re-enter `release_decision` but has no `target_sha`, `applied_edits` or `cycle_id` input, so a vacuous head check passes every listed test.

Evidence:
- In Task 4, `resume_decision(*, mode, ordinal, guard, read, pending, dangling_branch, published)` must "re-enter `release_decision` with `push_completed=True`" for row 4 (plan:70, plan:77, spec:166).
- `release_decision` also needs `cycle_id`, `applied_edits` and `target_sha` (spec:107, spec:166). `resume_decision` (spec:109) is given none of these. Task 4's acceptance (plan:77) only asserts the outcome.
- An implementer could take `target_sha` from the live `read.head_sha`, which would make release row 8's head check always pass. Or they could pass `applied_edits=0`, which hits row 7 and releases with cause `no_edits` instead of `pushed`. Either implementation passes every listed test.

Recommended plan change: state the sources:
- `cycle_id` comes from `guard.cycle_id`;
- `target_sha` comes from the dangling `push_initiated` record when the branch is `landed`, or from the cycle's `push_completed` event when `published` is true (the head-binding bullet at base `SKILL.md:275` already takes it from the record);
- `applied_edits` is this cycle's count, which is at least 1 once a push exists.

Alternatively, row 4 returns a "re-enter release" action and the SKILL calls `release_decision` with real values. Add a test that fails when `target_sha` is taken from the live read. The defect originates in the spec (spec:107-109, spec:166), so recommend a spec amendment too.

<!-- Source: Variant 1, Finding F2 - merged per Change #2 -->
<!-- Source: Base (original, modified) - placement finding F2 combined with the Variant 1 wording ambiguity, per Change #2 -->
### M2 (MINOR, blocking:false, contradiction): the Wave 0 bullet wording is ambiguous and its placement is too loose

Claim: spec:241 requires the Wave 0 bullet to contain no L3 condition yet to print the unprotected line at L3 with `--merge-guard off`, and Task 9 places the bullet only "before Wave 1" although `dangling_branch` comes from the head-binding bullet.

Evidence:
- Spec:241 says the Wave 0 bullet "applies at every ordinal and in both modes" and "contains no L3 or `draft` condition". The same cell says "at L3 with `--merge-guard off` it prints the unprotected line once". Task 9 copies both (plan:137). Its acceptance (plan:140) fails the bullet if it "names an L3 or `draft` condition".
- The plan's narrower test description on the same Task 9 paragraph (plan:138) is "no `L3 only` or `draft` gate wording". After the spot check in the debate, the defect is ambiguous wording between plan:137, plan:140 and the acceptance bullet, not an unpassable check.
- Task 9 says the new Wave 0 bullet only has to come before the Wave 1 bullet, and its test checks only that (plan:137, plan:140). At the base commit, Wave 0 has three bullets in order: all ordinals (`SKILL.md:274`), head binding (`:275`) and conflict check (`:276`). On `--resume`, the head-binding bullet is where `resolve_crash_window` produces the branch. The guard's Resume section needs that branch as `dangling_branch`. A bullet placed right after `SKILL.md:274` would describe guard resume running before the branch exists.

Recommended plan change:
- Reword the Task 9 acceptance to the listed forbidden phrases (an `L3 only` or `draft` gate on the ref load), with a clause scoped to `--merge-guard off` allowed.
- Require the bullet after the "Wave 0 head binding" bullet, and have the test check that order too.
- Amend the spec wording at line 241.

<!-- Source: Base (original, modified) - F6 merged with Variant 2 F5, per Change #9 -->
<!-- Source: Variant 2, Finding F5 - merged per Change #9 -->
### M3 (MINOR, blocking:false, other): the per-task classification wording is narrower than the rule

Claim: Tasks 7, 8 and 12 classify only `gh pr` and `gh api` lines, but Constraints, spec 4.7 and `WRITE_VERB_RE` also cover git write verbs.

Evidence:
- Constraints line 22 requires a classification entry for every new line with `gh pr`, `gh api` or a git write verb (plan:22). Tasks 7, 8 and 12 say only "every line that matches `gh pr` or `gh api`" (plan:108, plan:124, plan:182). Spec 4.7 covers git write verbs (spec:255, spec:28).
- `WRITE_VERB_RE` also matches `git push`, `git add` and the other git write verbs (base `test_worker_contract.py:1098-1101`).
- Task 8 allows `git` command lines in the ref (plan:124). A `git push` line in `refs/merge-guard.md` would fail the Task 8 acceptance run without any instruction to classify it. The `git remote get-url` line the script copies is not a write verb, so the gap matters mainly for the ref and the command file.

Recommended plan change: Tasks 7, 8 and 12 should say "every line that `WRITE_VERB_RE` matches".

<!-- Source: Base (original, modified) - F4 and F5 combined into one finding; Variant 2 F4 (Task 1 dependencies as a stand-alone finding) not merged, per the plan's "Changes NOT Being Made" -->
### M4 (MINOR, blocking:false, other): same-file edits have no declared order and Task 1 dependencies are only implied

Claim: tasks that edit the same test files have no declared order, and Tasks 9, 10, 12 and 13 use the Task 1 record without declaring `Depends on: Task 1`.

Evidence:
- `tests/pr_submit/test_static_grep.py` is edited by Task 5 (`CORE_PURE_FILES`, plan:85) and Task 7 (`_RESOLUTION_SCRIPTS`, plan:108). Task 7 depends only on Task 1 (plan:106), and Task 5 only on Tasks 3 and 4 (plan:82-83).
- `tests/pr_submit/test_merge_guard_protocol.py` is extended by Tasks 9, 10 and 12. Task 12 (plan:179-180) has no order against Tasks 9 and 10 (plan:134-135, plan:148). These tasks may also add `WRITE_VERB_CLASSIFICATION` entries to `tests/skills/test_worker_contract.py`.
- The spec says a task depends on every earlier task whose output it uses, and that "the protocol tasks need the pre-build record" (spec:363). Tasks 9 (plan:137), 10 (plan:154), 12 (plan:182) and 13 (plan:195, plan:199) use `./artifacts/pre-build-gate.md` but reach Task 1 only through other tasks.
- The same-file ordering is the real hazard: a parallel or reordered executor could produce conflicting edits (debate point X-001, 90%).

Recommended plan change: add `Depends on: Task 5` to Task 7, `Depends on: Task 10` to Task 12, and `Depends on: Task 1` to Tasks 9, 10, 12 and 13.

<!-- Source: Variant 2, Finding F1 - merged per Change #4 -->
### M5 (MINOR, blocking:false, missing-requirement): nothing tests that the guard, push triad and re-trigger share one cycle id

Claim: the guard, the push triad and `rereview_requested` must use one `cycle_id` that `held_cycle_published` matches, and no task asserts id equality.

Evidence:
- Spec 4.6 (spec:251) requires one `cycle_id` across the guard, the push triad and `rereview_requested`. `held_cycle_published` matches on that id (spec:108), so a mismatch means a normal push never releases the PR.
- Plan Task 8 says the ref "reuses it as the `cycle_id` of the push triad and of `rereview_requested`" (plan:124). Task 8's acceptance asks the ref to "state" the mint place but has no test for it (plan:127-128). Task 11 does not assert id equality (plan:170-171).
- Severity is MINOR, not MAJOR: plan:124 and plan:33 assign the mint owner (the single place named by Task 1 O1), so the gap is a missing check, not a missing owner (debate point C-007, 85%).

Recommended plan change: add a Task 11 assertion that the guard `cycle_id`, the push-triad `cycle_id` and the `rereview_requested` `cycle_id` are equal in the acceptance-trace test.

<!-- Source: Variant 2, Finding F2 - merged per Change #3 -->
### M6 (MAJOR, blocking:false, missing-requirement): the FR-16 release retry has no bound and no test body

Claim: the FR-16 release retry (one retry; already-in-state counts as confirmed) has no executable criterion, and Task 11 names the test without a case body.

Evidence:
- Spec section 7 names a test for "one retry, `already_in_state` counts as confirmed, `release_pending`" (spec:315).
- Plan Task 8 states "one retry; `already in target state` counts as confirmed" in prose only (plan:124). Task 8's phrase checks omit it (plan:129). Task 11 lists the test name but no case body (plan:166-168).
- `settled(ready, failed)` returns `RELEASE_PENDING` (spec:205), and `release_decision` accepts that phase. No decision row therefore enforces the one-retry bound.

Recommended plan change: add a Task 11 case body for `test_guard_release_failure_retries_once_and_reports` that covers the first release failing, the single retry, `already in target state` counted as confirmed, and the `release_pending` report; add the retry bound to the Task 8 phrase checks.

<!-- Source: Base (original, modified) - widened from the Wave 6 line to every existing Wave bullet line, per Change #7 -->
### M7 (MINOR, blocking:false, other): whole existing Wave bullet lines are classification keys

Claim: Task 10 protects only two Wave 6 sentences, but every existing Wave bullet line, including the Wave 6 line and the head-binding bullet, is a `WRITE_VERB_CLASSIFICATION` key, so appending to it makes the entry stale.

Evidence:
- Task 10 protects only "the S5a re-trigger sentence and the Wave 6 pre-push sentence" and allows "new sentences after, never inside, the pinned sentences" (plan:150, plan:154).
- At the base commit, the entire Wave 6 bullet is one physical line (`SKILL.md:282`). That line is a `WRITE_VERB_CLASSIFICATION` key, keyed on its exact stripped text (`tests/skills/test_worker_contract.py:1199-1206`, verbs `git add+git commit+gh pr+git push+gh api`). The three Wave 0 lines are keyed the same way (`:1167-1190`).
- The key is `(path, verb, full line)` (`test_worker_contract.py:1166`), and the head-binding bullet is also pinned whole (line 1186). Appending a sentence to any such bullet makes the entry stale and fails `test_classification_table_has_no_stale_entries`. Spec 4.7 (spec:255) sets the classification rule.

Recommended plan change: Task 10 should say the Wave 3, 6 and 8 additions are separate bullet lines, and that every existing Wave bullet line stays byte-identical as a whole line. The whole-line pin is also a stronger byte-identity proof than comparing only the start text of the sentences.

<!-- Source: Variant 1, Finding F3 - merged per Change #6 -->
### M8 (MINOR, blocking:false, missing-requirement): `guard_status` takes no halt reason

Claim: the spec says a halt with reason `draft_guard_unavailable` reports `unavailable`, but `guard_status(guard, mode, ordinal)` takes no halt reason and Task 3 neither maps nor assigns it.

Evidence:
- Spec:112 ends with "A halt with reason `draft_guard_unavailable` reports `unavailable`." The signature `guard_status(guard, mode, ordinal)` (spec:110) has no halt-reason input.
- Task 3's acceptance (plan:56-61) lists every other mapping row and omits this one. An implementer cannot tell whether it belongs to the function or to the SKILL.
- A read-failed engage halt writes no guard record, so `guard` is `None` and the mapping returns `released` at ordinal 3. Task 3's "no record at ordinal 3 -> released" test would lock in the wrong value unless this is resolved.

Recommended plan change: say in Task 3 that the `unavailable` report on a `draft_guard_unavailable` halt is a SKILL-level override, and add a test or phrase check for it.

<!-- Source: Variant 2, Finding F3 - merged per Change #5 -->
### M9 (MINOR, blocking:false, missing-requirement): the crash boundaries are narrower than spec section 7

Claim: the spec test requires a crash before and after each request and settle, but Task 11 cases cover only the crash between request and settle plus the branch and publish cases.

Evidence:
- Spec section 7 requires "crash before and after each request and settle" (spec:318).
- Task 11 covers only the crash between request and settle (plan:166), plus the branch and publish cases (plan:171).

Recommended plan change: extend the Task 11 crash cases to the four boundaries: before request, between request and settle, after settle, and the matching resume outcome for each.

<!-- Source: Invariant probe INV-012/INV-013 - merged per Change #8 (MEDIUM advisory) -->
### M10 (MINOR, blocking:false, missing-requirement): exit paths after engage need a held-report test

Claim: no task enumerates the exits after engage or asserts that each reaches the report step with the guard folded, so a halt that skips the report would leave a draft PR with no clear command.

Evidence:
- The spec says any exit after engage with no confirmed push and no zero-edit proof leaves the PR draft and reports `held` with the clear command (spec:69), and a validation failure after engage reports `merge_guard: held` plus the clear command (spec:275). The spec test is "each exit of D7 reports `held` and the clear command (FR-17)" (spec:313).
- The base SKILL has several post-engage halts (`fix_commit_failed`, `pr_head_mismatch`, `push_range_mismatch`, plus max-rounds and validation exits). The probe found that none appears in a card finding (invariant probe INV-012, INV-013).
- Task 11's case list (plan:166) names no exit list, and its acceptance (plan:169) only lists the test name `test_guard_holds_on_unpublished_or_uncertain_exits`. Task 8's acceptance only checks that a phrase is present.

Recommended plan change: Task 11 should enumerate the exits (the spec D7 exits plus the base SKILL halts above) and assert that each reaches the report step with `merge_guard: held` and the clear command.

## Rows checked and found sound

- No import cycle. The package `__init__` imports `classifier`, `conflicts`, `detection`, `fsm`, `models`, `reviewers` and `severity_router`, but not `run_log` (`__init__.py:22-96`). `recovery` imports `run_log` (`recovery.py:37`), which is why `merge_guard` must not import `recovery`.
- `_NEW_KEY_DEFAULTS` and the exact key-set asserts (`test_run_log.py:312-317`, `:403-404`) match what Task 5 describes.
- `test_allowed_tools_cover_every_program` scans only `NEW_REFS`, and scripts are not granted one by one in `allowed-tools` (`test_conflict_sync_protocol.py:35`, `:587-611`; `SKILL.md:4`). So Task 8's own "the `scripts/` path exists" check is the right proof.
- `_RESOLUTION_SCRIPTS` requires the origin `sed` line and origin before `gh repo view` (`test_static_grep.py:479-549`). The model script `retrigger-review.sh` satisfies both.
- One test module importing from another has a precedent (`test_conflict_sync_protocol.py:21`).
- The cycle ids `fix-<n>` and `ci-<n>` do not collide with the reserved prefixes (`conflicts.py:1242-1244`).

## Findings block

```findings-v2
{"id":"M1","severity":"MAJOR","blocking":false,"category":"unpassable-check","lens":"reflect-pre","claim":"resume_decision row 4 must re-enter release_decision but has no target_sha, applied_edits or cycle_id input, so a vacuous head check (target_sha=read.head_sha) passes every test; state the sources and test that a live-read target_sha fails.","refs":["FR-21","FR-10","INF-010"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":70,"line_end":70},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":77,"line_end":77},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":107,"line_end":109},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":166,"line_end":166,"quote":"re-enter `release_decision` with `push_completed=True`"}]}
{"id":"M2","severity":"MINOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Wave 0 bullet: spec 241 forbids any L3 condition yet requires the L3 --merge-guard off line, so Task 9's wording is ambiguous; also place the bullet after the head-binding bullet (dangling_branch comes from it) and test that order.","refs":["FR-21","INF-029"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":137,"line_end":137},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":140,"line_end":140},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":241,"line_end":241,"quote":"at L3 with `--merge-guard off` it prints the unprotected line once"}]}
{"id":"M3","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Tasks 7, 8 and 12 classify only gh pr and gh api lines, but Constraints, spec 4.7 and WRITE_VERB_RE (base test_worker_contract.py:1098-1101) also cover git write verbs; say every line WRITE_VERB_RE matches.","refs":["SPEC-4.7"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":22,"line_end":22},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":108,"line_end":108},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":124,"line_end":124},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":182,"line_end":182},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":28,"line_end":28},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":255,"line_end":255}]}
{"id":"M4","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Unordered tasks edit the same test files (Tasks 5 and 7; Tasks 9, 10, 12), and Tasks 9, 10, 12, 13 use the Task 1 record without declaring it; add Depends on: Task 5 to Task 7, Task 10 to Task 12, and Task 1 to 9, 10, 12, 13.","refs":["INF-032"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":82,"line_end":85},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":106,"line_end":108},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":179,"line_end":182},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":134,"line_end":137},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":148,"line_end":148},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":190,"line_end":195},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":363,"line_end":363}]}
{"id":"M5","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Guard, push triad and rereview must share one cycle_id that held_cycle_published matches; plan:124 names a mint owner but no test asserts id equality (Task 8 only states the mint place, Task 11 does not compare ids).","refs":["SPEC-4.6","SPEC-4.1-held_cycle_published"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":124,"line_end":124,"quote":"reuses it as the `cycle_id` of the push triad and of `rereview_requested`"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":127,"line_end":128},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":170,"line_end":171},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":251,"line_end":251},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":108,"line_end":108}]}
{"id":"M6","severity":"MAJOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"FR-16 release retry (one retry; already-in-state counts as confirmed) has no executable criterion; no release decision row bounds the retry, and Task 11 names the test without a case body.","refs":["FR-16"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":124,"line_end":124,"quote":"one retry; `already in target state` counts as confirmed"},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":129,"line_end":129},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":166,"line_end":168},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":205,"line_end":205},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":315,"line_end":315}]}
{"id":"M7","severity":"MINOR","blocking":false,"category":"other","lens":"reflect-pre","claim":"Task 10 protects only two Wave 6 sentences, but every existing Wave bullet line (Wave 6 and the head-binding bullet included) is a WRITE_VERB_CLASSIFICATION key; appending to one stales it. Require separate bullet lines and whole existing lines unchanged.","refs":[],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":150,"line_end":150},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":154,"line_end":154},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":255,"line_end":255}]}
{"id":"M8","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec says a halt with reason draft_guard_unavailable reports unavailable, but guard_status(guard, mode, ordinal) takes no halt reason and Task 3 neither maps nor assigns it to the SKILL.","refs":[],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":112,"line_end":112},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":56,"line_end":61}]}
{"id":"M9","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"Spec test requires crash before and after each request and settle; Task 11 cases cover only the crash between request and settle plus branch and publish cases.","refs":["FR-7"],"citations":[{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":166,"line_end":166},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":171,"line_end":171},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":318,"line_end":318}]}
{"id":"M10","severity":"MINOR","blocking":false,"category":"missing-requirement","lens":"reflect-pre","claim":"No task enumerates the exits after engage (base SKILL halts fix_commit_failed, pr_head_mismatch, push_range_mismatch, max-rounds, validation) or asserts each reaches the report with merge_guard held and the clear command (FR-17, D7).","refs":["FR-17","D7"],"citations":[{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":69,"line_end":69},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":275,"line_end":275},{"role":"spec","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md","line_start":313,"line_end":313},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":166,"line_end":166},{"role":"plan","path":".dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md","line_start":169,"line_end":169}]}
```

merge_note: Base is Variant 3 (reviewer-3). Merged per the refactor plan: M1 keeps the base MAJOR and takes the category unpassable-check from Variant 1; M2 combines the base placement finding with Variant 1's wording ambiguity; M3 merges Variant 2 F5 with base F6; M4 folds base F4 and F5 (Variant 2 F4 not kept as a stand-alone finding); M5, M6, M9, M8 come from Variant 2 F1, F2, F3 and Variant 1 F3; M7 widens base F3; M10 comes from the invariant probe (INV-012, INV-013). The Variant 2 layout (S-001) was not adopted. Not merged: INV-001 and INV-009 (probe only).
