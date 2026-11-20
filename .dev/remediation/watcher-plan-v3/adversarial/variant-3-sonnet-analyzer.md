# Remediation proposal, variant 3 (analyzer): watcher plan v3 findings Q-1 to Q-10

Paths: `plan` = .dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md; `guard` = src/superclaude/hooks/scripts/launch-level-guard.sh; `merged` = .dev/reflect/pre-TASK-WF-requirements-20261119-012839-20261119013121/adversarial/merged-output.md. All paths are under /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/. I re-read the guard, the plan, predicates.py 100-280, cycle.py 905-1120, test_security_invariants.py 1-40, 700-735, 900-930, WORKER-CONTRACT.md 238-248 and the guard tests at tests/hooks/test_launch_level_guard.py 2705-2780 and 2860-2900. Owner decisions are taken as fixed.

## Ranked findings (by what changes if left unfixed)

| Rank | ID | If left unfixed | Verified |
|---|---|---|---|
| 1 | Q-1 | A Full Submit agent (running as the approver login) can post issue comments now (guard:653 SUBMIT, guard:790 allowed). This breaks the owner decision "only the coordinator comments". Label half is inference. | Yes, both lines read |
| 2 | Q-3 | If a field change does not move the item's `updatedAt`, R31 fails open and the approval-after-Project-change rule never fires. If a label apply does move it, every approval is voided and nothing launches (fail closed, total outage). | Plan only; GitHub behaviour unverified |
| 3 | Q-2 | Cron launches `full` / `full --submit` on real issues while claim.md:133 says no governed claim until OB-H1 item 1, OB-H2, OB-H3 pass. Pass state unread. | Gate text read; status unknown |
| 4 | Q-7 | Task 6's acceptance cannot pass: test_security_invariants.py:729 calls `build_claim_prompt(n)` and lines 5-6 pin the old prompt, but only Task 7 touches them. Implementer drops the test or weakens it. | Yes |
| 5 | Q-4 | Two tasks give different reasons for one event; the plan's own tests contradict (plan:71 vs plan:108). An implementer picks one and fails the other task's acceptance. | Yes (cycle.py:1007-1016, audit.py:71,80) |
| 6 | Q-5 | Status moved on the wrong Project item when an issue sits on several Projects. | Yes (predicates.py:268) |
| 7 | Q-6 | If the result marker reuses `<!-- sc:issue:claim -->` the watcher reads its own result comment as a claim marker. | Yes (predicates.py:14, github.py:63) |
| 8 | Q-8 | Task 11 as written breaks or gets bent around the DF-14 `"String!" not in query` assertion. | Yes (test line 919) |
| 9 | Q-10 | Ordering and push-sentence slips; late rework, one wording risk at WORKER-CONTRACT.md:245. | Yes |
| 10 | Q-9 | Doc gap: which sessions the guard governs. No behaviour change. | Yes (guard:7, guard:391) |

## Q-1 Move issue write verbs out of SUBMIT
- Fix: in guard H3 (line 653) split `'issue create' | 'issue edit' | 'issue comment'` off to a new class ISSUEW; keep `pr create|edit|comment|ready` as SUBMIT. Add ISSUEW to the precedence loop at line 786 (before SUBMIT), add `ISSUEW:W|WA|F|FS) ll_deny LL-ISSUE` at line 788-805, add an `LL-ISSUE` message to `ll_say` (lines 41-114) and reword LL-SUBMIT (line 71, "pull request or issue") to "pull request". Apply identically to plugins/superclaude/hooks/scripts/launch-level-guard.sh. Extend the coordinator-only TAMPER pattern (guard:444) with `*issue-pipeline*complete* | *issue_pipeline*complete*`, keeping plan-hash and check-approval allowed (guard worker tests 293-294).
- What it breaks: tests/hooks/test_launch_level_guard.py:2743-2745 and 2875-2876 expect `gh issue create/comment/edit` to be LL-SUBMIT and allowed at Full Submit; they must move to a new all-four-levels-refused group. /sc:pr-submit is not hit: its protocol files contain no `gh issue` call (grep of src/superclaude/skills/sc-pr-submit-protocol found only prose); it uses `gh pr create` and `gh api` (review-retrigger.md:27, thread-reply.md:12), and the `gh api` POSTs are already refused at every level by GHWRITE (guard:798), so pr-submit's reply/resolve steps are already blocked under a governed session; that is existing, not caused here. Owner flow (Project fields first, approval label last) runs in the owner's or coordinator's unbound session, which the guard never governs (guard:391); unaffected. A launched agent that wanted to file a follow-up issue is now refused; intended.
- Failure modes and rollback: a typo in the case row falls to `*) ll_deny LL-BROKEN` (line 804), which fails closed. Rollback: revert the one case row and the loop word; reinstall hooks. The `launch-level-guard-version: 1` stamp (guard:10) is referenced by tests/skills/test_issue_orca_worktree.py and orca_worktree.py; I did not read how it is compared, so check whether a bump is needed for installed copies to refresh.
- Tests: refused at W, WA, F, FS for `gh issue edit 5 --add-label x`, `gh -R o/r issue comment 5`, `gh issue create`; allowed: `gh issue view 5`, `gh pr create --repo o/r`, `gh pr comment 5` at FS; refused for a bound worker and a launched session: `superclaude issue-pipeline complete 12 succeeded`, `uv run superclaude issue_pipeline complete`; allowed: `issue-pipeline plan-hash`, `check-approval`. Plan:158 adds the Full Submit cases it omits.
- Alternative rejected: keep SUBMIT and rely on the grant row. SUBMIT is allowed at FS by design (guard:790), so a policy line cannot stop it.

## Q-3 Observe `updatedAt` behaviour before relying on R31
- Fix: Task 3 splits in two. (a) the agent runs the read-only schema query (already in plan:55) and a read-only script that prints a given item's `updatedAt`; (b) the owner, on a throwaway issue in a test Project, records `updatedAt`, changes Pipeline, re-reads, applies the approval label, re-reads, and pastes the four values into `./artifacts/t3-updatedat-observation.txt`. Decision table in the plan: field moves it and label does not = R31 as written; field does not move it = R31 fails open, stop and return the fallback (level-specific approval label); label moves it = every approval voids, same stop.
- What it breaks: Tasks 4, 6 and 9 gain a dependency on the owner artifact (Task 4 already depends on Task 3). The observation is an owner write; the agent never runs it (plan:21 forbids real-GitHub writes).
- Failure modes: GitHub timestamps are whole seconds, and `unchanged_since` treats an equal time as changed (predicates.py:257, OQ-37). The owner flow (fields first, label last) works when seconds apart; a script doing `item-edit` then `--add-label` within one second is refused with `edited_after_approval`, which is fail-closed and fixed by removing and re-adding the label. Rollback: the predicate in Task 4 is one function and two call sites; revert them and the Project check alone remains.
- Tests: plan:70 cases plus a case where the approval and item times fall in the same second (refuse) and a case with the item an hour older (pass).
- Alternative rejected: a tolerance window (`updatedAt` allowed up to N seconds after approval). It reopens exactly the window R31 closes.

## Q-2 Ship gate (owner decision stays open)
- Fix, recommended: Option A, fail closed. Add one config key `launch_levels_gate` (default `closed`) in the generated config; while closed, the cycle treats any Pipeline other than None/empty as a skip with a new audit reason `launch_gate_closed` (`("skip", 0)`, `audit.py` REASON_TABLE near lines 71-80). The owner flips the key after OB-H1 item 1, OB-H2, OB-H3 pass, or writes in chat that the gate is waived (Option B), and the plan Constraints (plan:25) cite the answer.
- What it breaks: Task 6 tests that cross every Pipeline value need the gate open in their fixtures; REASON_TABLE count tests; Task 12 config keys; Task 15 generator writes `closed`. Cron then launches only None until the owner acts.
- Failure modes: a forgotten flip leaves the watcher at level None (safe, noisy: reports one reason). Rollback: remove the key check; default `open` restores plan behaviour.
- Tests: closed gate with Worktree/Full/Full Submit = `launch_gate_closed`, no launch call; None launches; open gate launches all four.
- Alternative rejected: only document the gate. Task 17 enables repos automatically, so a document cannot stop a launch.

## Q-4 One reason for the same reread
- Fix: in `_revalidate` (cycle.py:1012-1016) every failure, including the new item-updated check and the Status/Pipeline-changed check, raises `revalidation_failed` (the function's existing rule: all reread failures collapse, lines 1007-1016). `edited_after_approval` is returned only at `_examine` (after line 957). Edit plan:71 to say that between examine and launch the reason is `revalidation_failed`.
- What it breaks: nothing in tests today; both reasons are `("skip", 0)` (audit.py:71, 80), so exit code and store effects are identical. The next cycle re-examines and reports `edited_after_approval`.
- Tests: Pipeline raised after approval, between examine and launch = `revalidation_failed`; same change before examine = `edited_after_approval`; the Task 6 lowered-Pipeline case yields the same single reason whichever check fires first.
- Rollback: revert the plan wording; no code outside the two call sites. Alternative rejected: return `edited_after_approval` from `_revalidate`; it needs a new branch in `_rv`/`_Skip` for one label and still disagrees with plan:108.

## Q-5 Target the exact Project item in `complete`
- Fix: Task 9 takes the configured Project id (from the repo config, Task 12) and reuses the "one live item" helper Task 6 adds (plan:102); the Status and `In review` option ids are read for that Project's item; zero or several live matches = closed refusal word before any mutation.
- What it breaks: the `complete` verb (Task 10) needs `--config` or a repo name to find the Project id; Task 10 depends on Task 12 then. Tests in plan:146 gain two-Project, zero-item and archived-item cases.
- Failure modes: stale config id = refusal, comment still posted per its own rule; rollback = remove the id parameter (not recommended).
- Alternative rejected: select the first item of the issue. predicates.py:268 shows the real selection is by project id.

## Q-6 Distinct result marker
- Fix: the design note (Task 5) fixes the result marker text, e.g. `<!-- sc:issue:result -->`, never `CLAIM_MARKER` (predicates.py:14, selected by github.py:63 `contains(CLAIM_MARKER)`). State that coordinator and watcher share one login on this host, so idempotency keys on the marker text, not the author.
- What it breaks: nothing; `unchanged_since` already ignores comments by `own_login` (predicates.py:254), so the comment does not void the approval. The Status move does bump the item (intended: a retry needs a fresh approval, see Q-10).
- Test: `marker_comments` evidence does not match a comment with the result marker; a second `complete` call finds only the result marker.
- Rollback: change the constant. Alternative rejected: reuse the claim marker with a suffix; the jq `contains` would still match.

## Q-7 Task 6 acceptance versus test_security_invariants.py
- Fix: Task 6 rewrites the prompt-pinning parts of test_security_invariants.py (docstring lines 5-6; the scan call `build_claim_prompt(n)` at line 729 and any pin on `PROMPT_PATTERN`) in the same task; Task 7 keeps the documents and the other test files. test_no_shell.py stays in Task 6's acceptance.
- What it breaks: Task 7's list of files shrinks by one; its grep rerun still covers it.
- Failure mode: a half-edited test passes vacuously; keep the "scan is not vacuous" assertion (around line 901). Rollback: restore the file.
- Alternative rejected: drop the file from Task 6's acceptance; the invariant is then unchecked at the moment the prompt changes.

## Q-8 Task 11 and the `String!` assertion
- Fix: the plan states the restated test: `$owner` and `$name` appear in the query; `repository(owner: $owner, name: $name)` appears; the literal `"IronbellyOrg"` does not; lines 916-917 stay; line 919 is restated so `String!` is not forbidden for `$owner`/`$name` only (or the variables use a default, `$owner: String = "IronbellyOrg"`, which keeps nullable form; per the GraphQL spec a defaulted nullable variable fits a non-null position, unverified against GitHub). The DF-14 rationale was not read; confirm it before choosing.
- What it breaks: any other test reading these constants by literal; scan at 905-908 stays.
- Rollback: Task 11 is one module; revert. Alternative rejected: delete assertion 919; it guards the pagination cursor typing.

## Q-9 Which sessions are governed
- Fix: Task 10 text and the design note state: sessions bound by the launch marker (levels worktree, full, full-submit; guard:7, guard:254-273) are governed; a level-none claim session and an ordinary session are never blocked (guard:391); workers are covered only by the TAMPER class (guard:441-444). So for level None the coordinator-only rule is by contract (WORKER-CONTRACT.md:241-243), not by guard.
- What it breaks: nothing. Test: an unbound session running `issue-pipeline complete` is allowed by the guard (documents the declared limit).

## Q-10 Ordering, retry, push sentence
- Fix: add Task 1 to Task 4's dependencies if it edits predicates.py; state the cycle.py edit order Task 4, 6, 12, 18 (Task 6 and 12 already chain); add Task 9 to Task 15's dependencies (plan:216 extends the argv scan Task 9 owns); say a retry after the coordinator mirrors a Status needs a fresh approval (the move bumps `updatedAt`); write the replacement for WORKER-CONTRACT.md:245 so the coordinator pushes nothing and shows commits to the person, while at Full Submit the launched agent pushes only its own feature branch (what the guard allows, guard:719-723).
- What it breaks: Task 24 ordering; none in code. Rollback: edit the plan text.

## Residual risks
- The guard classifies text, not intent: `gh` out of command position (`flock x gh project item-edit ...`, tests/hooks/test_launch_level_guard.py:2736 "Residual R17") is not UNKNOWN, so "never changes a Project field" at launched levels is policy, not enforcement; `gh issue edit` still hits H3 at any position.
- pr-submit's `gh api` POST steps are blocked at every level by the existing guard; Full Submit therefore may not complete review replies. Not a regression; the owner should know.
- A Full Submit agent runs under the approver login; after Q-1 the label vector needs `gh issue edit` or `gh api`, both refused, but a non-gh route (curl, python) depends on the guard's other classes (GHWRITE `api.github.com`, guard:552, 623).
- Unverified: updatedAt semantics (Q-3); OB-H gate pass state (Q-2); version-stamp handling (Q-1); DF-14 rationale (Q-8); docs/designs/sc-issue-launch-level-hook.md was not read, and its grid must be updated with Q-1.
