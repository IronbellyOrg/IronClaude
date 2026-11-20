# Merged reflection verdict (v2 plan)

<!-- Source: Variant 3 (base) structure; register per refactor-plan.md; corrected after the evidence-validator gate (see the last section) -->

Plan file: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-010910/TASK-WF-requirements-20261119-010910.md. `plan:N` is a line of it; `source.md:N` is a line of source.md in the same folder. Other paths are relative to the checkout root; `guard` is src/superclaude/hooks/scripts/launch-level-guard.sh.

## Verdict

FAIL as advice: 4 blocking (P-1 to P-4), 5 medium (P-5 to P-9), 2 notes (P-10, P-11). Nothing was edited.

## Confirmed fixed

The 12 earlier findings M-1 to M-12 were found fixed by all three reviewers; M-13 (the unverified minor items) was found fixed by two.

## Findings

### P-1 BLOCKING (Safety)
<!-- Source: Variant 1 N-1, Variant 2 QA-1, Variant 3 B-1 -->
- Task: Tasks 4, 8 and 9. Requirement rows: R24, R25.
- Evidence: plan:73, plan:137; guard:653 and :792; guard:798; guard:444; src/superclaude/core/WORKER-CONTRACT.md:241-243 and :300; plan:22-24.
- Finding: plan:73 and plan:137 let an agent launched at Worktree, Full or Full Submit run `issue-pipeline complete`, which posts an issue comment and a GraphQL Status change from inside Python. The guard classifies `gh issue comment` as SUBMIT and denies it at the Worktree, Worktree-approval and Full levels (guard:653, :792; allowed at Full Submit, guard:790), and denies `gh api` writes (class GHWRITE) at all levels (guard:798), but it cannot see a write made inside the verb; its TAMPER pattern names only `adopt-`, `record-`, `release-worker` and the approval-record module (guard:444). WORKER-CONTRACT.md:241-243 and :300 make GitHub writes, progress posts and Project fields coordinator actions that need the grant row, and plan:22-24 record no exception.
- Fix: the launched agent only reports (a result file and its worker_done or a sweep-visible end); the coordinator runs `complete` under the grant row. Otherwise the owner states an explicit exception, recorded in Constraints, R24 and the guard.

### P-2 BLOCKING (Decision)
<!-- Source: Variant 1 N-2 -->
- Task: Task 10 (plan:151-158).
- Evidence: tests/issue_watch/test_security_invariants.py:911-919 (:915, :918); plan:157.
- Finding: Task 10 says that test still passes, but :915 asserts the literal `repository(owner: "IronbellyOrg", name: "IronClaude")` and :918 asserts `$owner` and `$name` are absent; Task 10 turns both into variables, so the test fails by design.
- Fix: Task 10 names lines 911-919 as a test to rewrite (assert the variables and the read-only form) and drops "still passes".

### P-3 BLOCKING (Decision)
<!-- Source: Variant 2 QA-2 -->
- Task: Task 18; requirement R5 (source.md:31) and R26 (source.md:52).
- Evidence: plan:239 and plan:244 (stop only on a launched or attempted line; a child killed after 255 seconds is recorded as failed while later repos still run); cycle.py:1091-1092 (pending state saved before the launch) and :1099-1109 (launch call, then the outcome branches).
- Finding: a child killed or timed out after the launch call has printed nothing, so there is no launched or attempted line, and the loop goes on to another repo and can launch a second issue in the same sweep.
- Fix: a killed or timed-out child consumes the sweep's launch allowance unless later reconciled as no launch; add a test.

### P-4 BLOCKING (Safety, owner decision)
<!-- Source: Variant 3 B-2 -->
- Task: Task 5 and R25.
- Evidence: src/superclaude/cli/issue_watch/predicates.py:228-233 (approval compared with label and init times) and :249-258 (body, comments and renames only); plan:94.
- Finding: nothing proves who set the Pipeline field or when, so a Pipeline raised after approval and before the examine step launches a push and pull request on a label that approved a lower level.
- Fix: see "Decisions needed from the owner".

### P-5 MEDIUM
<!-- Source: Variant 1 N-1 (part) -->
- Task: Tasks 6 and 9. Requirement row: R23.
- Evidence: launch.py:33 and :92 (src/superclaude/cli/issue_watch/launch.py); a search of the guard found no `pipeline none` match; source.md:47.
- Finding: Tasks 6 and 9 say to update the guard so the new prompts are allowed, but the guard has no prompt allow-list; the prompt is pinned in launch.py (PROMPT_PATTERN at 33, the f-string at 92). source.md:47 says "the launch-level guard allows only that exact prompt"; that statement is not supported by the guard and probably means PROMPT_PATTERN.
- Fix: Task 6 changes launch.py, the command, the skill and the tests, and changes the guard only where Task 4 decides.

### P-6 MEDIUM
<!-- Source: Variant 1 N-3, N-4 -->
- Task: Tasks 8, 10, 11, 5, 22, 7 and 9.
- Evidence: predicates.py:113-118 (ProjectItem holds is_archived, project_id and status_name only); plan:164 (Task 11 depends on Task 10 only); plan:284 (Task 22 depends on Task 20 only); cycle.py:915 and :979 (_examine and _revalidate, rewritten by Task 5 and again by Task 11).
- Finding: Task 8 needs a read for the Project item id and the Status field and option ids, and needs Task 10 for the repo parameter; Task 11 edits the same cycle functions as Task 5 without depending on it; Task 22 writes the completion text and push rule decided in Tasks 7 and 9 without depending on them.
- Fix: record these dependencies and the new read.

### P-7 MEDIUM
<!-- Source: Variant 3 M-a -->
- Task: Task 8. Requirement row: R24.
- Evidence: plan:126 and plan:131.
- Finding: the marker check names no author, so any commenter could post the marker line and suppress the result comment; the plan does not say whether a failed Status move is retried on a second call.
- Fix: count only the watcher's own marker comments, and retry the Status move on a second call.

### P-8 MEDIUM
<!-- Source: Variant 3 M-b -->
- Task: Task 4. Requirement rows: R23, R24.
- Evidence: plan:69 and plan:73; source.md:47.
- Finding: plan:68 and plan:78 already give prompt text per Status and Pipeline pair, but Task 4 does not decide whether each Status command suits each launch level (Debug runs `/sc:troubleshoot --fix`, which edits code, at Worktree, whose meaning is "propose next steps, halt"), nor the end Status per pair; the end-Status table is keyed by Status only.
- Fix: Task 4 decides per pair: run, limit or refuse, and the end Status.

### P-9 MEDIUM
<!-- Source: Variant 2 QA-3 -->
- Task: Task 4 and Tasks 5 to 7. Requirement row: R23(c) (source.md:47).
- Evidence: plan:71 and plan:77-80 (the Spec judgment is a Task 4 design decision with a document-only acceptance); absence claim for the later tasks.
- Finding: no acceptance test covers the Spec well-defined judgment, its recorded reason or the high-complexity handoff. The judgment is an agent's, so a unit test may cover only the recording and the handoff, not the judgment.
- Fix: add an acceptance check for the two Spec branches' prompts, the recorded reason and the handoff.

### P-10 NOTE
<!-- Source: Variant 3 N-1 -->
- Task: Task 8.
- Evidence: tests/issue_watch/test_security_invariants.py:10 (a generic NG-2 line), :712-730 (the argv scan covers only `github.*` builders and `launch_argv`); plan:132.
- Finding: the scan does not cover the new read modules (generate.py, repos.py, dispatch.py).
- Fix: add those builders to the scan.

### P-11 NOTE (found by the evidence check)
<!-- Source: evidence-validator -->
- Task: Task 20 and Task 18.
- Evidence: plan:259 (`run-all --dry-run` leaves the directory unchanged), plan:239 (a rotation file) and the loop lock file.
- Finding: a dry run that takes the loop lock or reads the rotation file may write a file, so "directory unchanged" could fail.
- Fix: say whether the dry run takes the lock and writes nothing, or exempt the lock file.

## Decisions needed from the owner

### P-1 (BLOCKING, Safety): who writes the completion update when an agent launched at Worktree, Full or Full Submit finishes
Options:
- A launched agent only reports; the coordinator posts the comment and moves the Status under the grant row.
- The owner states an explicit exception for these writes, recorded in Constraints, R24 and the guard.

### P-4 (BLOCKING, Safety): how the Pipeline setting is proven to be the owner's
Options:
- Level-specific approval.
- Void the approval when the Project item changed after it (recommended, if the item's updatedAt is readable; Task 3 verifies).

## No finding

<!-- Source: Variant 3 card, citations corrected by the evidence check -->
- github.py stays read-only (plan:22, 54, 157).
- Approval label, Status allow-list and edited-after-approval stay the gate (plan:23).
- The plan-hash row is never made from claim-time data (plan:117).
- Task 14 sends REST reads with `--method GET` (plan:201).
- Task 22's `gh auth status` check is read-only (plan:282).
- The level mapping matches src/superclaude/commands/issue.md:43-44 and :56-57.
- Launch order and unknown case as stated (cycle.py:1054-1058, 1106-1109).

## Not checked

- Tasks 10 to 22 in depth; tests/hooks bodies; conftest.py.

## Corrections after the gate

The evidence-validator found: P-3's evidence now cites plan:239 and :244 and cycle.py:1091-1092 instead of lines that say nothing about a killed child; P-1's wording on guard:798 (GHWRITE covers `gh api` writes, SUBMIT covers `gh issue comment`) was corrected; P-5's guard lines were replaced by the search result and the conflict with source.md:47 is stated; P-6 now cites plan:164 and :284; P-7's "never retried" was reworded; P-8 dropped guard:409 and the claim that prompts per pair are undecided; P-9 cites plan:71 and :77-80; P-10 states that line 10 is generic; the "run-all dry-run writes nothing" no-finding item became P-11; the plan:151 citation was replaced.
