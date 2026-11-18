# Round 1 Advocate Statement: Variant 1 (analyzer reviewer card)

Sources: spec = `input/TASK-WF-designSpec-20261107-075614/source.md`; plan = `input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. "L" = line in those files.

## Position summary

V1 is the only card that traces the decision tables across cycles. It shows that a faithful build of this plan releases a PR while an earlier cycle's fix is unpublished (F2), and that one Task 7 check cannot fail (F1). Its weakness is that it grades F2 non-blocking.

## Steelman: Variant 2 (qa)

Strongest version: the plan's acceptance criteria are the only mechanical gate before build, and many pass empty or wrong implementations. V2 is right on three counts. The release retry is unspecified: spec L315 names it only in the test table, no release row (L147-157) yields a retry, and the script never emits `already_in_state` (L231-232). Its F1 is real: plan L25 cites "non-goals of source.md", which has no such section, and spec L61 engages CI-fix cycles despite the plan's "not held through ... CI". Its F5 is real: plan L172 forbids `pr ready` without `--undo` only for originally draft PRs.

## Steelman: Variant 3 (refactorer)

Strongest version: a scheduler that follows `Depends on:` lines runs tasks in the order the plan declares, and spec L363 requires one line per consumed output. V3 finds that Tasks 9, 10, 12 and 13 consume Task 1's record without a Task 1 line (plan L132-135, L148, L177-193). It also finds that Task 12 edits `test_merge_guard_protocol.py` and the classification table, which Tasks 9 and 10 also edit (plan L137, L150, L180-181), with no dependency. That is a real collision risk, and V3 correctly treats the structural pins as a separate review concern.

## Strengths claimed

1. F2 (carry-over release). Spec L6: "an exit with unpublished fixes keeps the PR draft." Engage row 7 returns `NOOP(already_held)` for a second cycle while HELD (L139). Release row 7, `applied_edits == 0 → RELEASE(no_edits)` (L155), is checked before HOLD row 9 (L157), and plan L75 requires it. A zero-edit fix-2 therefore marks the PR ready while fix-1's commit is still local. This comes from the tables, not from inference about code.
2. F1 (unfailable count). Plan L111-113 asserts key names and the null-timeline case only. Spec L230 requires `gh api --paginate` and a count of `convert_to_draft` and `ready_for_review` events. A one-type or unpaginated count passes.
3. F3 (fold branch). Spec L201 returns a settled `not_applied` ready request to `RELEASE_PENDING` after a failed release. Plan L60 tests only the `HELD` result.

## Weaknesses identified in other variants

1. V2 inflates blocking status. Its F6 (plan L169, L173) says test names without bodies pass. That is a build-process check, not a design defect, yet it is rated MAJOR and blocking.
2. V2 misses the decision-table trace. None of its 12 findings follows a release path across cycles, so it misses the carry-over case the diff analysis rates High (C-004).
3. V3's F3 misreads plan L142, which bars edits to "any existing test expectation." A new `WRITE_VERB_CLASSIFICATION` key is not an existing expectation, so the claimed contradiction is weak.
4. V3 rates the Task 12 collision (its F2) MINOR, though a parallel run could clobber an edit to a shared file.
5. None of V3's four findings reaches a decision row, fold rule or script output. Its coverage is structural only.

## Concessions

1. I marked all three findings `blocking: false`. F2 should be blocking: plan L75 makes the wrong release a passing criterion, so a correct build ships it.
2. My "dependencies complete" claim covered only the import chain. Spec L363 asks for every consumed output, and V3 shows that is not met.
3. I missed V2's F3 (retry), F5 (`--undo` on the ready call) and F7 (auto-merge value). Each is a real gap I should have checked.

## Shared assumptions

- **A-001: QUALIFY.** A later fix cycle can start after a HOLD. Engage row 7 (spec L139) handles a second engage while HELD, so the design expects it. But the spec never says what a later zero-edit cycle does with earlier unpublished fixes. That gap is F2, so the assumption holds only with this qualifier.
- **A-002: ACCEPT** as the review standard. The plan sets it: Task 3 requires each fold case to "fail if the row is implemented wrongly" (plan L60). V2's F6 and my F1 apply it to criteria that name tests or keys. V3's F3 and F4 do not depend on it; they concern internal contradictions.
