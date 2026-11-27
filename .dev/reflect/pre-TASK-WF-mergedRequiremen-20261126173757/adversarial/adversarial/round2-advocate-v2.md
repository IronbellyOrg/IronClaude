**Response to remaining criticisms of my card**

- **C-008 / U-005 (`main_checkout_only`): conceded, Medium.** I re-read plan line 30 and 60 and spec line 59.
  - Plan line 30 defines the flag as "every matched worktree has `isMainWorktree` true". That is vacuously true for a Run with no matched worktree, so it is a real imprecision.
  - Plan line 60 says the summary counts "the number of Runs admitted only through the main checkout". Spec line 59 says the same, and adds that these figures "change no rule".
  - So the intent is stated twice and matches the spec, an executor can proceed, and the figure is informational. In my Round 1 and in the debate I conceded the same-shaped stale-age fallback (C-007) to Medium for the same reason. Keeping C-008 at Blocking (Decision) would be inconsistent with that.
  - One point I do keep: the flag is pinned by the named test `test_main_checkout_only_and_stale_flags` (plan line 33). A literal reading of line 30 would make that test pass on a wrong predicate, so the fix is still worth making: "admitted only through a main-checkout worktree", with the empty case excluded.
- **S-002 (grading vocabulary): agree with V1's withdrawal. Note.** My card has no Medium tier, and that is why conditional findings (QA-2, QA-3) landed at Blocking. V1 has a Medium tier but no Missing or Safety label. Neither is a plan finding.
- **A-001 (scratch-Run authority): both cards now say QUALIFY. Note.** I conceded QA-1 already. The plan and spec show only that plan line 102 gives no quote or file for the brief. They cannot show the action is unauthorised.
  - V1's new point is that Task 11's owner-decision list (plan `:136`, as V1 reports it) omits Open decision 2, the scratch Run. I did not re-read `:136` for this reply, so I take it from V1 and treat it as consistent with that gap.
- **C-005 (Task 10 check) and C-006 / X-003 (staging): V1 now concedes both, so they are no longer disputed.** I keep Blocking (Decision) and Blocking (Missing).
- **F2's fix hole: accepted.** `counts.hook_added` is defined only as a build-time value (spec lines 34-36). The fix should say to dedupe by id and leave `counts` as built.
- **F10 / test placement: agreed Note.** I withdraw my Round 1 claim that it is a real deviation. The plan puts Tasks 1-4 in `tests/run_ledger/`, and only Task 6's tests sit in `tests/sweep/`.
- **QA-7 (matrix omits schema obligations): Note.** V1 is right that it concerns the review input, not a plan defect.
- **F1's Task 1 dead branch (`decide(..., hook_entries)` can never fire), the Task 8 `Decision:` gap, the empty ledger and the hook-entry duplicate row: all conceded in Round 1.** I have nothing to add on them.

**Updated assessment of the opposing card**

V1 is more accurate on unspecified behaviour and on authority calibration. V2 is more accurate on spec-versus-plan drift, on the missing staging step, on the unsatisfiable Task 10 check and on citations. V1's plan line numbers are all +31 off, which is a form defect only. V1 conceded its F5 and F8 grades honestly. V1's final table is sound, and I find nothing to dispute in it.

**New evidence**

None beyond the line 30, 60 and spec 59 reading above. That reading supports V1's point and cuts against my Round 1 grade.

**Final table (still-open item only)**

| Point | Final grade | Evidence |
|---|---|---|
| C-008 / U-005 (`main_checkout_only`) | Medium | Plan `:30` is vacuous for a Run with no matched worktree, but plan `:60` and spec `:59` state the intended count, and the figure changes no rule. |

Agreed with V1 and not open: S-002 Note, A-001 Note (QUALIFY), C-005 Blocking (Decision), C-006 / X-003 Blocking (Missing).

Files re-read (all under `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/`):
- `tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md` (lines 28-63)
- `tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/source.md` (lines 52-61)
