# Remediation proposal: v3 watcher plan, findings Q-1 to Q-10 (variant 2, architect)

Source: `.dev/reflect/pre-TASK-WF-requirements-20261119-012839-20261119013121/adversarial/merged-output.md`. Plan: `.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md` (`plan:N`). Guard: `src/superclaude/hooks/scripts/launch-level-guard.sh` (`guard:N`). Every line below was re-read on 2026-11-19.
Owner decisions kept: only the coordinator comments and moves Status to In review (plan:23); an approval is void when the Project item changed after it (R31, plan:65); cron may launch all four levels (plan:25).
Scope flags: **[SCOPE+]** marks an edit that adds work beyond the finding. Net: no new code module; one new owner-action task (3a); one new guard class.

## Q-1 BLOCKING: Full Submit agents can write to issues (Tasks 10, Constraints)

Evidence: `'issue create' | 'issue edit' | 'issue comment'` share the SUBMIT line with the pr verbs (guard:653), and `SUBMIT:FS` is allowed (guard:790). plan:23 says the guard "keeps refusing issue comments" at Full Submit, which is false today; plan:158 tests only Worktree and Full. /sc:pr-submit needs no `gh issue` verb: its issue-comment traffic is `gh api` (`skills/sc-pr-submit-protocol/refs/review-retrigger.md:27`, `refs/thread-reply.md:88`), already GHWRITE at every level (guard:798).

Code change (Task 10, guard and its plugin mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh`):
1. guard:653 becomes `'pr create' | 'pr edit' | 'pr comment' | 'pr ready') LL_CLASSES+='SUBMIT ' ;;` followed by a new line `'issue '*) LL_CLASSES+='ISSUE ' ;;`. Order matters: it sits after guard:652, so `gh issue view|list|status` stay allowed (first match wins), and like the SUBMIT line it fires whether or not `gh` is in command position. It also catches `issue close|reopen|delete|transfer|lock|pin|develop`, which today are only UNKNOWN in command position (guard:654).
2. guard:786 precedence list: insert `ISSUE` after `GHWRITE`. Case table: add `ISSUE:W | ISSUE:WA | ISSUE:F | ISSUE:FS) ll_deny LL-ISSUE ;;`.
3. `ll_say`: add `LL-ISSUE` (Blocked: a GitHub issue write (gh issue create, edit, comment, close or another change). Why: only the coordinator writes to an issue; a launched session reports through `.dev/issues/<N>/result.md`. You can: write the result file; the coordinator posts the comment and moves the Status). Change LL-SUBMIT's text at guard:71 from "pull request or issue" to "pull request".
4. Coordinator-only pattern (guard:444), Task 10's addition named exactly: `*issue-pipeline*complete* | *issue_pipeline.complete* | *issue_pipeline/complete.py* | *issue_pipeline*import*complete*`. Not `*issue_pipeline*complete*`: that would refuse `uv run pytest tests/issue_pipeline/test_complete.py` in a launched session working on this repo.

Plan edits:
- plan:23 last sentence becomes: "The launch-level guard refuses every `gh issue` write (create, edit, comment, close and the rest) at every level, Full Submit included (Task 10), and every `gh api` write at every level (guard:798)."
- plan:152 (Task 10 body) adds items 1 to 4 above. plan:158 replaces "still refuse `gh issue comment` at Worktree and Full" with: "refuse `gh issue create`, `gh issue edit 5 --add-label issue-watch:approved`, `gh issue comment 5` and `gh issue close 5` with LL-ISSUE at W, WA, F and FS; `gh issue view 5` and `gh issue list` stay allowed at every level; `gh pr comment 5` still passes at FS."
- G2 must-refuse cases: `superclaude issue-pipeline complete --repo o/r --issue 5`, `uv run superclaude issue-pipeline complete ...`, `python -m superclaude.cli.issue_pipeline.complete`, `python -c "from superclaude.cli.issue_pipeline import complete"`, `python -c "from superclaude.cli.issue_pipeline.complete import run"`. Must-allow: `superclaude issue-pipeline plan-hash <dir> plan.md`, `superclaude issue-pipeline check-approval <dir> plan.md --line "approved r1 plan-sha256=<hash>"` (the two the comment at guard:442-443 names), and `uv run pytest tests/issue_pipeline/test_complete.py`. `stage-status` is a coordinator read (WORKER-CONTRACT.md:298); leave it unclassified and say so.

Tests: `tests/hooks/test_launch_level_guard.py` moves the three issue rows out of `GH_ORACLE["SUBMIT"]` (2743-2745) into a new `"ISSUE"` row with `("LL-ISSUE",) * 4`, removes them from T-GH-5 (2875-2876), adds `ISSUE` to the class list near 778 and the grid at 797; `tests/hooks/test_launch_level_guard_worker.py` takes the G2 cases above.
Risk: an older installed guard still says version 1 (guard:10) and the IR-4 preflight only checks that line (`skills/sc-issue-protocol/scripts/orca_worktree.py:839`), so a stale host guard passes and keeps allowing FS issue writes. **[SCOPE+, recommended]** bump both lines to version 2 in Task 10 and update the tests that pin it. Text matching stays a declared limit (guard:774-775): Python that shells out to `gh` is not seen.
Rejected: keep SUBMIT and add a per-verb FS exception inside the case table (two meanings for one class, and the message would still say "needs --submit").

## Q-2 OWNER DECISION: ship gate (Tasks 6, 17; plan:25)

Evidence, now read: the gate has NOT passed. `docs/designs/sc-issue-launch-level-hook.md:625` says "Pending, none run: OB-H1 items 1 to 9, OB-H2, OB-H3"; `tests/hooks/test_launch_level_observations.py:3` and `:84` keep each as a skipped test. Design :201 (U1) requires item 1 before `full` or `--submit` and item 5 before a claim at any level; `refs/claim.md:133` repeats it. If item 1 fails, a subagent of a Full Submit agent is not governed at all, and under R25 nobody is watching the launch.

- **Option A (fail-closed switch).** Task 6 adds one constant in `launch.py`, `GOVERNED_LEVELS_ALLOWED = False`, and `_examine` refuses a non-None Pipeline with a new reason `level_gated` (one row in `audit.REASON_TABLE`) before any write. Flipping it is a reviewed PR after the owner records OB-H1 items 1 and 5, OB-H2 and OB-H3 as passed. Implications: everything is built and tested now; in production only None launches until the PR; the owner decision "cron may launch all four" holds as a capability; no live observation runs inside this plan (plan:28). Cost: ~6 lines plus one reason row and two tests (Pipeline Full Submit gives `level_gated` and no launch; None launches).
- **Option B (explicit waiver).** The owner waives the gate in chat; Task 24 records it under "Open decisions" with date. Implications: unattended Full Submit launches under an approver login with subagent identity unverified; the ship-gate sentence in `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `refs/claim.md:133` and the design (:10, :201, :625) becomes false and must be rewritten **[SCOPE+: 4 more files in Task 7]**.
- Variant A2: split the switch per design §7 (item 5 + OB-H2 + OB-H3 unlock Worktree; item 1 also unlocks Full and Full Submit). Two constants instead of one.

**Recommendation: A.** It keeps both owner decisions true at once, costs a few lines, and turns an unchecked prose gate into a checked one. Plan edits: plan:102 (Task 6 body) adds the constant and refusal; plan:108 adds the two tests; Task 22 (plan:287) documents the switch.

## Q-3 OWNER DECISION: what moves when the Pipeline or Status changes (Tasks 3, 4; R31)

Evidence: Task 3 (plan:55) proves only that `ProjectV2Item.updatedAt` exists. Item-level `updatedAt` may move on things that are not Project changes (labels, the claim's own comments, assignment), which would void good approvals, and nothing proves it moves on a field change (fail-open).

- **Option A (owner observation).** New **Task 3a** (owner action, no code): on a test issue the owner changes Pipeline, then Status, then applies the approval label; between each step the agent runs the read-only query and saves the times to `./artifacts/t3a-updatedat-observation.md`. Task 4 depends on Task 3a. Implication: one owner action blocks Phase 1's last task.
- **Option B (fallback label).** If A shows a fail-open or false voids, R31 falls back to a level-specific approval label. Implications: Tasks 4, 5, 13 and 16 change; a level label alone does not cover a Status change (Research to Debug switches to `/sc:troubleshoot --fix`), so it would need Status-by-level labels; owner decision again.
- **Option C (field-value times).** Read `createdAt` and `updatedAt` of the Status and Pipeline `ProjectV2ItemFieldSingleSelectValue` objects (both are fields of that type and of `ProjectV2ItemFieldValueCommon` in GitHub's GraphQL reference) through the two `fieldValueByName` aliases Task 3 already adds. Void when either value's later time is at or after the approval. A label or comment touches neither object, so no false voids; a cleared Pipeline reads as None (lower, safe) and a cleared Status fails `project_check` (predicates.py:262-271).

**Recommendation: C, confirmed once by A; B only if A fails.** C targets exactly the two fields R31 names and is the same query size. Plan edits: plan:55 replaces "the Project item's `updatedAt`" with "`createdAt` and `updatedAt` of the Status and Pipeline values", the dataclass gets `status_changed_at` and `pipeline_changed_at` (predicates.py:113-118), and the schema check also reads `__type(name: "ProjectV2ItemFieldSingleSelectValue")`; plan:58 checks both names; plan:65 compares the later of the two times; plan:67 becomes "Depends on: Task 1, Task 3, Task 3a". **[SCOPE+]** Task 3a (owner action only).
Rejected: keep item `updatedAt` unobserved (fail-open risk stays and is unbounded).

## Q-4 BLOCKING: two reasons for one reread (Tasks 4, 6)

Evidence: Task 4 (plan:71) expects `edited_after_approval` between examine and launch; Task 6 (plan:108) expects `revalidation_failed`; `_revalidate` raises `revalidation_failed` for every failure (cycle.py:1007-1016). Both are `_Skip`s with no store write (cycle.py:822-823, 833-834), so only the audit line differs.
Plan edit, plan:102 adds: "In `_revalidate`, after the items reread (cycle.py:1012-1014), the Task 4 time check runs first and raises `edited_after_approval`; only when it passes does `project_check` and the examined-versus-reread Status and Pipeline comparison run, each raising `revalidation_failed`." plan:108 adds a case: Pipeline raised with a value time after approval gives `edited_after_approval`; a reread Status differing with every time before approval gives `revalidation_failed`.
Rejected: one reason for both (makes plan:71 false and hides the provenance refusal in the audit).

## Q-5 MEDIUM: Status move can hit the wrong Project item (Task 9)

Evidence: plan:141 passes repo and issue only; the watcher selects by Project id (predicates.py:268).
Plan edit, plan:141: the function also takes `project_id` (validated `^PVT_[A-Za-z0-9_-]+$`); for `succeeded`, before any write (the comment included) it reads the issue's items and selects the one non-archived item of that Project with the helper Task 6 adds next to `project_check`; zero gives `refused:project_missing`, more than one `refused:project_ambiguous`, a Status field without an `In review` option `refused:status_option_missing`. Other outcomes do no Project read. Task 10's verb takes `--project-id`; the coordinator copies it from the repo's watcher config. plan:143 becomes "Depends on: Task 3, Task 5, Task 6". plan:146 adds the three refusals with zero calls after the read.
Rejected: look up the Project from the repository (`projectsV2`), which repeats Task 15's ambiguity in a writer.

## Q-6 MEDIUM: the marker login is shared (Task 9, design note)

Plan edit, plan:87 (Task 5) and plan:141: the result marker is a new literal, `<!-- sc:issue:result -->`, never `CLAIM_MARKER` (`<!-- sc:issue:claim -->`, predicates.py:14), so the watcher's marker read (`github.py` `MARKER_JQ`) never mistakes a result comment for a claim. The design note states that the counted login is the workspace's single `gh` login, shared by the watcher, the coordinator and any launched agent, so a hand-posted comment under it carrying the marker suppresses the result post. Test (plan:146): the result marker does not contain `CLAIM_MARKER`. Own-login comments are already ignored by `unchanged_since` (predicates.py:254), so the post does not void anything.
Rejected: a separate bot login for the coordinator (Coder template work, out of scope).

## Q-7 MEDIUM: Task 6 cannot pass its own acceptance (Tasks 6, 7)

Evidence: `test_security_invariants.py:5-6` pins `--pipeline none`; `--pipeline none` appears 45 times in 7 `tests/issue_watch` files (test_cli 3, test_cli_e2e 2, test_crash_injection 1, test_cycle 6, test_launch 14, test_no_text 4, test_security_invariants 15). Task 6 changes `PROMPT_PATTERN`, so all of them go red until Task 7 (plan:114).
Plan edit: move those 7 files from Task 7's list (plan:114) into Task 6, whose acceptance (plan:109) then includes `uv run pytest tests/issue_watch -q`. Task 7 keeps commands, skills, `WORKER-CONTRACT.md` and docs.
Rejected: drop the two files from Task 6's acceptance (leaves the tree red between tasks; `/sc:implement` QA grades each task on its own).

## Q-8 NOTE: restating DF-14 (Task 11)

`repository(owner:, name:)` takes non-null arguments, so `$owner` and `$name` must be `String!`, which breaks `"String!" not in query` (test_security_invariants.py:919). Plan edit, plan:166: "Line 919 becomes: `$after: String)` stays nullable, and the only `String!` declarations are `$owner` and `$name` (regex `\$(\w+): String!` gives exactly {owner, name})." The DF-14 rationale was not read; Task 11 reads it first and stops if it forbids non-null variables outright.

## Q-9 NOTE: which sessions the guard governs (Task 10, plan:23)

Plan edit, plan:23 adds: "The guard governs only a session with a record in the launch-level store (guard:257-258): the agent the claim launches at worktree, full or full-submit (an unrecognised record reads as worktree, guard:264-268) and a bound worker (G2 pattern, guard:441-444). The watcher-launched `--pipeline none` claim session has no record (refs/claim.md:118) and the coordinator has none, so neither is governed; the claim session's two marked comments are allowed by design."

## Q-10 NOTE: dependency edges and ordering

- plan:67 Task 4: add Task 1 (and Task 3a per Q-3). plan:211 Task 15: add Task 9 (its argv scan, plan:216).
- Constraints, new line: "Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (4, 6, 12, 18), `launch.py` (6, 12), `github.py` (3, 11), `predicates.py` (1, 3, 4, 6), `WORKER-CONTRACT.md` (8, 10), `test_security_invariants.py` (3, 6, 9, 11). Task 1 leaves `cycle.py` unchanged (plan:34)."
- plan:87 and Task 8 duties: "After the coordinator mirrors the Status (WORKER-CONTRACT.md:298) or moves it to In review, the Project values have changed, so any relaunch needs a fresh approval label."
- plan:88: the replacement for WORKER-CONTRACT.md:245 keeps "the coordinator never pushes worker commits on the Pipeline setting"; at Full Submit only the launched agent pushes its own feature branch.

## Residual risks

1. The guard is text-based (guard:774-775): Python or another wrapper that shells out to `gh` or calls `complete.py` by an unusual spelling is not seen. The launched agent runs under an approver login, so Q-1 narrows but does not close self-approval of another issue.
2. Already true today: at Full Submit, `/sc:pr-submit`'s review re-trigger and thread replies use `gh api --method POST` (review-retrigger.md:27, thread-reply.md:88), which GHWRITE refuses at every level, so `--monitor 3` cannot reply or re-trigger from a launched agent. Out of scope; flag to the owner.
3. Q-3 Option C rests on GitHub's documented field-value timestamps; Task 3a confirms the behaviour once, and nothing keeps checking it afterwards.
4. Without Q-2 Option A, plan:25 and refs/claim.md:133 contradict each other in production.
5. The `complete` verb does not itself check the issue's grant row; that stays a rule in WORKER-CONTRACT.md:300. A code check would be **[SCOPE+]** and is not proposed.
