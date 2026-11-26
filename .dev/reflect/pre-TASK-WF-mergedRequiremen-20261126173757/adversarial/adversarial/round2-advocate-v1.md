## Response to V2's criticisms of the V1 card

I re-read the plan lines 1-141 and `source.md` lines 22-155 before relying on any line number below.

| V2 criticism | Response |
|---|---|
| Missed QA-2 and QA-3 | Conceded. V1 did not find the stale-age fallback or the `main_checkout_only` definition. The disagreement left is the grade of QA-3. |
| F5 graded Medium | Conceded, and I keep my Round 1 concession (Blocking (Decision)). Plan `:128` ("every command and flag the doc names exists in `sweep ledger --help`") cannot pass against `:124`, which requires the doc to name `flock -n`, `env -i`, `command -v` and a crontab. I graded the same kind of defect Blocking (Decision) in F1, so the same grade applies here. |
| F8 graded Note | Conceded. A grep of the plan for "stage" finds only `:20` and `:96`, both about `.claude/`. No step stages `.dev/tasks`, though `source.md:133` requires it. The package is untracked in the git status. |
| Line numbers offset by 31 | Conceded. This is a form defect. The quotes are exact, so a validator can re-locate them. |
| F10 is a catch-all | Partly right. The `find_orca` and path points are fine as Notes. On test placement, Tasks 1-4 use `tests/run_ledger/` as the spec says (`source.md:114`). Only Task 6's `tests/sweep/test_ledger_input.py` and the autouse fixture in `tests/sweep/conftest.py` sit outside it. The autouse fixture there is the reason for the split. I keep it as a Note. |
| F2's fix has a hole | Small and conceded. `source.md:34-36` defines `counts.hook_added` only as a build-time value, and `source.md:75` is silent on it after the merge. The fix should say to leave `counts` as built and dedupe the entries by id. This does not change the grade of F2. |
| Missed QA-7 | Not a plan defect. It is a point about the review matrix. I leave it at Note. |

## Assessment of the V2 card

- **Where V2 is stronger:** definition drift against the spec (stale-age fallback, `main_checkout_only`), the absent staging step, the unsatisfiable Task 10 check, and exact citations.
- **Where V2 is weaker:**
  - It missed three unspecified-behaviour gaps: the Task 8 `Decision:` line, the empty ledger, and the hook-entry duplicate row.
  - Its "not confirmed" on the duplicate row did not address the overlap between `new` and the hook rule. Their advocate has conceded this.
  - It has no Medium tier, so conditional findings land in Blocking.
- **Overgrades:** QA-1 is conceded as overgraded by their advocate. QA-2 is conditional on the Task timestamp field being absent, and their advocate agrees. That leaves QA-3 as the one open overgrade.

## New evidence

1. **A-001.** Plan `:136` lists the owner decisions that Task 11 must report. They are the age cutoff, and that the schedule and hook registration are left to Coder#545. It omits Open decision 2 (`source.md:151`, the scratch Run). That fits the plan treating the scratch Run as already answered by the brief ("the brief orders this test", `:102`). It does not prove it, because the plan never quotes or locates the brief.
2. **C-008 resolved by `:60`.** Task 4 says the summary counts "the number of Runs admitted only through the main checkout". That is the spec's reading at `source.md:59`. The flag definition at `:30` is imprecise, but the count's intent is stated twice and agrees with the spec.
3. **C-008 is a real defect, and I concede that.**
   - `all(wt.isMainWorktree for wt in matched)` is true for an empty list. A natural implementation would flag every Task-only or `new`-only Run.
   - On the 10 admitted Runs (`source.md:54`: 3 by worktree, 9 by Task, 2 by both), that could inflate the figure.
   - It is still a reported count. It changes no rule, and `source.md:59` says the figures "change no rule".

## Final table for the open items

| Point | Final grade | Evidence |
|---|---|---|
| C-008 / U-005 (`main_checkout_only`) | Medium | Plan `:30` is vacuous for a Run with no matched worktree and says nothing about other admission reasons. The intent is clear from `source.md:59` and plan `:60`, so an executor can proceed. The figure is informational and changes no rule. V2 graded the same-shaped stale-age fallback (QA-2) Medium. |
| S-002 (grading vocabulary) | Note | Neither card is the winner. V1 has Medium but no Missing or Safety label, which is why it left a missing item at Note. V2 has the labels but no Medium, which is why it put a conditional finding at Blocking. Both are subsets of the debate vocabulary, so I withdraw V1 as the named winner. |
| A-001 (wording) | Note (QUALIFY) | I withdraw REJECT. The plan and spec can show that the plan does not carry its own authority (`:102` has no quote or file). They cannot show that the action is unauthorised, because that needs the brief. V2's QUALIFY is more accurate. |
| C-005 (Task 10 check) | Blocking (Decision) | Plan `:128` cannot pass when `:124` requires `flock -n`, `env -i`, `command -v` and a crontab. Same kind of defect as C-001. |
| C-006 / X-003 (staging) | Blocking (Missing) | `source.md:133` says to stage `.dev/tasks`. The plan has no staging step (grep: only `:20` and `:96`, both about `.claude/`), and the acceptance checks can pass without it. The global rule mitigates this but is not a plan step. |

Files read:
- `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/round1-advocate-v1.md`
- `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/round1-advocate-v2.md`
- `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md`
- `/home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/source.md`

I did not re-read `variant-1-original.md` or `variant-2-original.md`.
