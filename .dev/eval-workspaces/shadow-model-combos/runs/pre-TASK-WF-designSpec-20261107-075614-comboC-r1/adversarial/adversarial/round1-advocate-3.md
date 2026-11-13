# Round 1 statement: advocate for Variant 3 (refactorer card)

## Position summary

V3 is a narrow but accurate card. It checks plan structure (task order, `Depends on:` lines, shared-file edit order, the stale-classification rule) against spec sections 4.7, 6 and 10. Its four MINOR findings are each grounded in a spec rule or a plan contradiction. V3 is weak on behavioural coverage, and I concede that below. I argue its severities are the best calibrated of the three cards.

## Steelman

**V1.** Its strongest form is the F2 trace. After a release HOLD (row 9), a later zero-edit cycle meets engage row 7 (`NOOP(already_held)`). Release row 7 then returns `RELEASE(no_edits)` before row 9 is reached. The PR goes ready while an earlier cycle's fix is unpublished, which conflicts with spec line 69 ("Any exit after engage with no confirmed push ... PR stays draft"). Task 4 turns this into a criterion. V1 also has a real, failable gap in F1 (Task 7 never checks timeline count or `--paginate`). My critique is below.

**V2.** Its strongest form is that it audits the criteria themselves, which is what a pre-execution audit is for. The `--undo` gap is real: spec line 231 requires it, and Task 7's criteria assert only `--repo`. The auto-merge `notes` gap is real: spec line 143 against plan lines 73 and 111. The unpassable Wave 0 criterion is real. V3 missed the first two.

## Strengths claimed

1. F1 is a direct spec requirement. Spec line 363 says a task "depends on every earlier task whose output it imports or consumes", and names "the protocol tasks need the pre-build record". Tasks 9, 12 and 13 declare no `Depends on: Task 1`, although each cites `./artifacts/pre-build-gate.md` (plan 137, 182, 195). V1 calls dependencies "complete for the import chain", but the spec rule is wider than imports.
2. F2 is a real race on shared files. Task 12 (plan 177-182) extends `test_merge_guard_protocol.py` and the classification table, as Tasks 9 and 10 do, yet depends only on Tasks 6 and 8.
3. F4 is an internal contradiction. Plan 108 makes `_RESOLUTION_SCRIPTS` conditional on O2. Plan 113 requires the script to pass those tests unconditionally.
4. The "what held" list is evidence a reader can use. It confirms the stale-entry ordering, with the entries added last in Tasks 7 and 8, as spec 4.7 requires. It confirms byte-identical pins checked against constants, as spec 377 requires. It confirms the import-cycle check in Task 5. No other card covers these.
5. V3 does not duplicate T1 F2 and F4. It confirms them without inflating the count.

## Weaknesses in other variants

1. V2 F1 (blocking) overstates. Spec has no "non-goals" heading, so the plan's attribution at line 25 is loose. But spec Wave 8 (line 241) releases "after `push_completed` before the CI re-poll", so "not held through CI" matches the spec. This is a labelling slip, not a blocking contradiction.
2. V2 F3 (blocking) says FR-16 has "no mechanism". The mechanism exists: `RETRY_RELEASE` (engage row 5, resume row 7), `settled(ready, failed)` returning to `RELEASE_PENDING` (spec 205), and `confirmed, not changed` (spec 202, 204). Plan line 124 says "one retry; `already in target state` counts as confirmed". At most this is a MINOR criterion gap.
3. V2 F6 (blocking) overstates. Task 11 criterion 1 names the tests. Criteria 2-4 (plan 170-172) assert event order, real `detect_crash_window` output and forbidden gh calls, so empty stubs would fail them.
4. V2 sets blocking=true on seven findings; several are MINOR-grade criterion tightening. That makes the verdict "not ready", but the plan has no inverted or missing task.
5. V1 F2 is a spec defect, not a plan defect. Spec 107 states "a zero-edit cycle after a fixing cycle still releases with `no_edits`". The plan copies it faithfully. In a plan-against-spec audit it belongs under "spec gap", not data-loss in the plan.

## Concessions

- V3 has no behavioural findings. It misses V1 F2, V2 F5 and F7, and the Task 7 count gap. Its "no drift" scope verdict missed the loose line 25.
- V3 F3 is arguable. Adding a classification entry may not count as editing "an existing test expectation".
- V3 confirms T1 F2 (Wave 0 wording) but raises no card entry. Its severity is therefore unrecorded, and V2's MAJOR is the only recorded one.
- All four V3 findings are covered transitively, so MINOR is right but they carry little weight.

## Shared assumptions

**A-001: QUALIFY.** Engage row 7 (`NOOP(already_held)`) shows the spec expects a second cycle to start in phase `HELD`. The spec never says a run continues to a new cycle after a release-row-9 HOLD specifically. If it does, the flaw sits in the spec's own `applied_edits` rule (spec 107), not in the plan.

**A-002: QUALIFY.** It holds for a criterion whose only content is test names (Task 11 criterion 1). It fails where the criterion also runs the tests and the task body names the cases (Task 11 criteria 2-4, Task 3 criteria). Failability must be judged on body plus criteria together.
