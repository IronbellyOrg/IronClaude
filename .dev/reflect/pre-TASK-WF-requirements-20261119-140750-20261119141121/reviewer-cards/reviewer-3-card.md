persona: refactorer
model_class: opus

(Persisted by the orchestrator from the reviewer's returned text; the reviewer agent has no Write tool. Plan = `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md` (`plan:N` is a line of it). `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`.)

## Summary
Plan v4 carries every finding (Q-1 to Q-10) and every owner decision of the remediation proposal into a named task with a test that fails when the item is missing. Q-6 and Q-10 are only partly fixed. Every requirement R1 to R33 maps to a task, and no task is orphaned. Three new blocking defects: a coordinator for any repo other than IronClaude would read plan approvals from the wrong repo; the approval-void rule may refuse every issue with an empty Pipeline (the only level the closed gate lets launch); Task 11 tests the work brief at levels that never use it. The 28-task split mostly holds. Two same-file pairs are missing from the ordering constraint.

## Q-1..Q-10 and decisions
- Q-1 FIXED: Task 13 (plan:200-207) covers the ISSUE class, the class list, the deny row, the message and the version bump. Guard lines verified: guard:10, :444, :652-654, :764, :786 and :798; LL-SUBMIT text at guard:70-71.
- Q-2 / Decision 1 FIXED: Task 8 (plan:137-143), Task 21 report (plan:290), Task 26 (plan:346). `_PENDING` at tests/hooks/test_launch_level_observations.py:79.
- Q-3 / Decision 2 FIXED: Tasks 3, 4 and 5 (plan:61-89). New defect B-2 below.
- Q-4 FIXED: reason order at plan:123, tested at plan:129.
- Q-5 FIXED: Task 12 (plan:188, :191).
- Q-6 PARTIAL: per-run marker and run id are in (plan:188, :214); no test that `marker_comments` ignores a result comment, which the proposal's Q-6 tests require.
- Q-7 FIXED: plan:125, :130. Q-8 FIXED: plan:227, :231. Q-9 FIXED: plan:25; test at plan:206.
- Q-10 PARTIAL: same-file ordering line exists (plan:30) but is incomplete (M-1).
- Decisions 3 to 6 FIXED: Task 9, Task 13 (tamper token), Task 12 (end-status table), Task 13 refusals; Task 28 records the answers.

## Findings

B-1 | Blocking (Safety) | Tasks 11, 14, 15, 23 | affected action: the coordinator's plan-approval gate for any repo other than IronClaude.
  Evidence: `stage-status` calls `gh.reread(runner, budget, issue, _timeout)` with no repo (src/superclaude/cli/issue_pipeline/cli.py:279) and loads `~/.config/superclaude/issue-watch.json` by default (cli.py:347). `reads.py` calls `gh.events` / `gh.edits` with no repo (reads.py:142, :148). github.py hard-wires `REPO = "IronbellyOrg/IronClaude"` (github.py:37). Task 15 keeps REPO as the default "so reads.py and its tests keep working unchanged" (plan:227). WORKER-CONTRACT.md:298 tells the coordinator to "read GitHub through stage-status at each gate". Task 23 enables every repo of an allowed owner (plan:313). Result: COORD-X checking X#N reads the approval label, approvers and edits of IronClaude#N. Live even with the gate closed, because level None starts plan workers. WORKER-CONTRACT.md:242 ("Every such action targets IronbellyOrg/IronClaude") also contradicts `complete --repo` for other repos, and no task edits that line.
  Fix: thread `--repo` (and the per-repo `issue-watch.d` config) into `stage-status` and `reads.py` and test that a second repo never reads IronClaude; or limit the dispatcher to IronClaude until that is done. Reword WORKER-CONTRACT.md:242 in Task 11.

B-2 | Blocking (Decision) | Tasks 3, 5 | affected action: the void rule for an empty Pipeline, the only level the closed gate lets launch.
  Evidence: Task 3 says an absent Pipeline value is Python None and gives `pipeline_changed_at: datetime | None` (plan:61). Task 5 says "an unreadable time also refuses" (plan:84). Absent and unreadable are the same value, and no acceptance case covers an empty Pipeline (plan:87-88). Read literally, every issue with an empty Pipeline ends `edited_after_approval`.
  Fix: tell "no value" from "unreadable value" in the parse; state that an absent Pipeline uses only the Status time; add tests: empty Pipeline passes, Pipeline cleared after approval passes, a malformed time refuses.

B-3 | Blocking (Decision) | Tasks 6, 11 | affected action: Task 11's brief acceptance check, and Debug at level None.
  Evidence: Task 6 decides the brief is used only at `none`; at the other levels the launched agent runs the command from its launch prompt (plan:102). Task 11's test asks for the limited `/sc:troubleshoot` form at Worktree and the `--fix` form at Full and Full Submit in the brief (plan:177) and has no None row. The brief today is a plan-writing worker whose rows "stop before /sc:implement" (worker-brief.txt:5). Whether Debug at None runs `--fix` (code edits before plan approval) is untested.
  Fix: test the brief's None rows, including what Debug does at None; move the Worktree/Full/Full Submit troubleshoot checks to the launch-prompt tests of Task 10.

M-1 | Medium | Constraints, Tasks 2, 10, 11 | same-file edits that can run in parallel. Task 10 edits WORKER-CONTRACT.md (plan:161) but plan:30 lists only Tasks 11 and 14 for that file; Tasks 10 and 11 have the same dependencies (6, 7) and no order. Task 2 (depends on Task 1) and Task 10 both edit docs/designs/issue-watcher.md and issue-watcher-setup.md (plan:48, :161) with no edge. Fix: add both pairs to plan:30 or add edges (Task 10 depends on Task 2, Task 11 on Task 10).

M-2 | Medium | Task 7 | `status_report` rebuilds the retry prompt from dispatch.json only (cycle.py:1286, :1310-1313), and the store holds no Status or Pipeline. Task 7 requires a valid retry command per Status (plan:123, :131) but changes neither record.py nor the store schema. Fix: store the launched prompt or level in the entry (add record.py to Task 7 and plan:30) or print no retry command for a governed level.

M-3 | Medium | Constraints, Task 6 | Full Submit "runs /sc:pr-submit --monitor 3" (plan:27), but that skill posts with `gh api --method POST` and `gh api graphql` (sc-pr-submit-protocol/refs/review-retrigger.md:27; scripts/reply-resolve-thread.sh:73, :131). The guard refuses both at Full Submit (guard:579, :581, :798). The remediation flagged this as a residual risk; the plan drops it. Fix: record it in Task 6 and Task 26 as a known limit before the gate flips, or scope Full Submit's pr-submit to no monitor.

M-4 | Medium | Task 13 | The body allows "record the over-match as accepted and tested" for `*issue-pipeline*complete*` (plan:202), but the acceptance requires `plan-hash` with a path containing "completed" to stay allowed (plan:207), and that pattern refuses it. Only the anchored option can pass. Fix: delete the second option and anchor on the verb word.

M-5 | Medium | Goal | plan:15 "A launched agent can never write to an issue, a label or a Project at any level" is false at level None and contradicts the plan's constraints (plan:25: the claim session is ungoverned and posts two comments; plan:24: the check is text-only). Fix: narrow it to "an agent launched at Worktree, Full or Full Submit is refused gh issue, label and project writes by text check".

N-1 | Note | Task 9 | cites `self.account_id` (cycle.py:767), a runtime value from `gh api user`; `check-config` has only the config's `owner_account_id` (cycle.py:768). Name the config field.
N-2 | Note | Task 5 | "one-second resolution, line 257": `unchanged_since` compares raw datetimes (predicates.py:257); only `approval_of` truncates (predicates.py:181-182, :205).
N-3 | Note | Task 13 | SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1070 and :1443 also mention guard version 1 and are not in the bump list.
N-4 | Note | Task 13 | ISSUE fires on any `gh issue|label|project` word outside command position too (guard:626-646), so at Full / Full Submit a commit message or `grep "gh issue comment"` is refused. Not listed as an accepted over-match.
N-5 | Note | Task 19 | says its argv builders "are covered by the scan Task 12 extends" (plan:275), but test_security_invariants.py is not among Task 19's files (plan:30). The scan must find modules generically or Task 19 must edit the test.
N-6 | Note | split | Tasks 7 and 13 are large (Task 7: prompt, reordering and seven test files; Task 13: guard, mirror and five version pins). Both are kept whole because splitting either would leave the test suite red between tasks. The other 26 tasks have a single purpose.

Checked: the plan in full; source.md R1-R33; the remediation proposal in full; guard :10, :70-71, :444, :548-587, :595-808; cycle.py :41, :58, :455, :760-771, :940-1064, :1270-1324; predicates.py :110-271; launch.py :33, :50, :84-127, :233, :249; github.py REPO usages; issue_pipeline/cli.py :195-364; reads.py imports; brief.py; worker-brief.txt; WORKER-CONTRACT.md :238-300; version pins; the `--pipeline none` hit list; test_launch_level_observations.py :70-85.
Not checked: audit.py :26/:71-80; test line numbers in test_launch_level_guard.py :2743-2745 and :2875-2876; test_security_invariants.py :911-919; approval_record.py; DF-14 text; whether bound workers carry a level in the store; check-config (cli.py :185-198).
