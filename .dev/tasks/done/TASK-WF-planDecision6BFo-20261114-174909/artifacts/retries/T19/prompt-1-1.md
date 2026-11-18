308fddc77748808748f87095d2c7da0e8a1bcac5
Review one task for spec compliance.

Task brief: ## Task 19: Write the change list for the merged requirements and close the open decisions

Create `./artifacts/merged-spec-change-list.md` in this package. It names, without editing the merged requirements file in the brainstorm folder: WA-01 (claim level: take the "--pipeline none" branch, now with the coordinator handoff); WA-02 (the #450 edits list gains B); WA-03 (runbook step); WA-04 (FU-1 record adds preconditions a to k and the guard-loss acceptance); WA-07 (moves from deferred to live under B, blocked-by SW-13 removed or restated); SW-13 (the supervised-worker route is now the delivery path, no longer a later redesign); OB-09 (a dashboard approval is only a message to the coordinator); section 6.3 roles (a worker row for the plan-writing worker); section 6.4 rule 10 (permission mode of every started session, now including the guard loss); section 6.8 (a per-pipeline-issue grant row shape: plan reply, marker comment, mention, label and Status writes); and new items for Tasks 1 to 16 (the adoption row of Task 3, the `pending` subcommand of Task 15 and the `Worktree:` slot change of Task 9 included). It then lists the owner decisions below, each with options, a recommended answer and the owner's answer, written for a person who has not seen the project.

Owner decisions (Q34 and Q41 were answered on 2026-11-14; Q35 to Q40 were answered on 2026-11-14 and restated by the owner on 2026-11-15, relayed by the orchestrating session; each line below records the answer, and none is open). Each is written for a person who has not seen the project:
- Q35, the claim-side change. Options: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing worktree step (recommended; no claim code changes, only the watcher prompt and tests); B2, a new claim level that creates the worktree and copies files without an agent (about six more test files, and a worktree with no agent until the coordinator starts one). ANSWERED 2026-11-15 (first 2026-11-14): B1b (the first reply said "Q53 b1b" and "2. Approved", read as Q35).
- Q36, approval latency under Q31 (no recurring timer). The coordinator reads GitHub only at gates and wakes, so an approval given on GitHub waits until the next read, which can be hours. Options: A, accept the delay and make Orca the fast path (the person approves in the coordinator session, which is immediate); B, allow a narrow timed read only for pipeline issues that are waiting for approval (reverses Q31 for that one case); C, the person types "check now" in the coordinator session after approving on GitHub. Recommended: A together with C. ANSWERED 2026-11-15 (first 2026-11-14 as "accepted delay"): option A, approve in the coordinator; the "check now" command (option C) is NOT selected and is not built.
- Q37, where the worker's plan-approval rule lives. Options: a new rule in WORKER-CONTRACT.md next to WC-3 (recommended, written once); only in each brief (no contract edit, but every brief repeats it). ANSWERED 2026-11-15 (first 2026-11-14): the rule goes in WORKER-CONTRACT.md next to WC-3.
- Q38, how a coordinator approval releases a guarded worker (G2). Options: A, the coordinator writes the session's release file after recording the approval (needs the worker's session id, UNVERIFIED); B, the guard reads a coordinator-signed approval file (more code in the guard). Recommended: A if the first live test shows the session id can be found, else B. ANSWERED 2026-11-15 (first 2026-11-14 as "default until G2"): the default. G2 is not built, so only the one G1 test issue can run; no release route is chosen now, and the route is chosen in Task 13 after the first live test.
- Q39, the scope of removing plain `approved` (Decision 9). Options: remove it for every worktree-level claim (closes the self-approval hole, but a person with no coordinator then has only `/sc:implement` typed in the session); keep it for person-run claims until G2 exists (my earlier recommendation, not taken). ANSWERED 2026-11-15: remove it now, for every worktree-level claim, with no person-run carve-out and no wait for G2 or the live test (Task 16).
- Q40, the design amendment order. #548 is merged. Options: one follow-up documentation PR for Tasks 17 and 18 (recommended); fold them into the code PR of Task 11. ANSWERED 2026-11-15 (first 2026-11-14): one follow-up documentation PR for Tasks 17 and 18, opened only after the owner reads the plan. No PR is opened from this plan, and Tasks 17 and 18 wait on Task 11.
- Q41, the worktree with no agent. The claim script creates `issue-<N>` with no agent (`orca_worktree.py:681-697`), so for a moment the worktree has none, against the project rule that every worktree gets an agent; the coordinator's `worker-start` supplies one right after. If the coordinator is down in between, the worktree sits empty. Options: A, accept it and say so in the claim text (recommended: the script closes the plain first tab, nothing runs in the empty worktree, and nothing starts while the coordinator is down anyway); B, change the script to create the worktree with an agent (more claim code, and a second agent instead of the worker); C, let `worker-start` create the worktree itself, which skips the script's copy step and reuse lookup (rejected in the design session). ANSWERED 2026-11-14: A (accept it and say so in the claim text).

Open points that remain (facts, not owner decisions; the first live test of Task 8 must measure each): the real `worker-start` argv and permission flags; whether `worker-start` accepts an exact existing worktree that the script created and leaves exactly one terminal; the `ask` and `reply` round trip, including whether the reply is stored as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; how a worker's session id can be found (it decides the G2 release route in Task 13); `ask` timeout and resume by message ID; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; the GitHub label event shape; whether a comment typed in the GitHub web editor arrives as exactly `approved`; and what a comment edit does to `lastEditedAt`.

Start condition: can be written now.

Acceptance criteria:
- The artifact lists every merged-requirements item named above with the change in one sentence, and lists Q35 to Q41 each with options, a recommended answer, and the owner's answer or a default.
- A grep of the merged requirements file shows no modification (`git status` of the brainstorm folder is clean for that file).

AC ids (source order): T19.AC1 = bullet 1 of "Acceptance criteria"; T19.AC2 = bullet 2 of "Acceptance criteria"
Global constraints: ## Constraints

- Plan only. The owner approved this plan with fixes on 2026-11-15 and asked for the review changes on the same day; every owner decision in Task 19 is answered, and what stays open are facts the first live test must measure (Task 8), not decisions. Running `/sc:implement` from this plan still needs the owner's separate go. No push, PR, GitHub write or Orca write verb is authorized by this plan.
- This is Plan A of two. It holds only work that can run now, in this file order: Task 16 first (its own branch from origin/master, its own pull request later), then Tasks 1, 2, 8 (a document only), 3, 4, 5, 6, 7 and 19. Task numbers are stable across both plans, so they are not contiguous here. `/sc:implement` runs items in file order and ignores `Depends on` and `Start condition` text, so the order of the items is the gate. A `Depends on` line names only a task that appears earlier in this file. Plan B lives in its own package folder, `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909-planB/plan-b-gated-tasks.md` (Tasks 20, 9, 10, 11, 12, 13, 14, 15, 17, 18). It opens with an owner-run gate item, the first live test recorded in docs/designs/issue-pipeline-fu1.md, and is not run from this file.
- Archive. Plan B sits in its own package folder, so archiving this plan's folder when it completes does not move Plan B.
- Owner input O-1 (not chosen by this plan): the number of one GitHub issue that the owner wrote, which Task 4 records real GitHub responses for. It is written by the owner into `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md` as one line `ISSUE: <number>`. An executor that finds no such line stops at Task 4 and never picks an issue.
- Rebase first. This plan was written on base 0406ef5b0. origin/master is now d4d1662a8 and already holds PR #539 (sweep) and PR #548 (the D2 "claim-only" superseded note in docs/designs/issue-watcher.md). Every task below starts from a worktree based on current origin/master.
- Evidence for every factual claim is in ./artifacts/validation.md (read-only measurements, file and line citations, and what is UNVERIFIED). Real code locations are in ./artifacts/codegraph-grounding.md.
- Chosen claim-side change: B1b, the watcher claims with `--pipeline none` and the coordinator runs the existing `orca_worktree.py worktree` step, then `worker-start --worktree path:<that worktree>`. The owner confirmed it on 2026-11-14 and again on 2026-11-15 (Q35 = B1b; the first reply wrote "Q53 b1b" next to "2. Approved", read as Q35). B2, a new claim level, is not built.
- Owner answers: see Task 19.
- Owner decision Q34 (2026-11-14): the plan-writing worker runs without the launch-level guard (G1) for ONE test issue only. The written acceptance must cover the loss of the guard itself (no block on commit, push, merge, GitHub writes or /sc:implement), the owner writes that issue's text, and it is not stretched from the Decision 1 acceptance of permission checks off. Before any other issue runs through this flow, the guard is changed (G2, Plan B Tasks 13 to 15).
- Accepted earlier and carried here: only the coordinator tells the worker to proceed; one person-opened coordinator owns all watcher-claimed issues on this host with a lock per issue; nothing starts while the coordinator is down; one grant row per pipeline issue; one GitHub login on this host means an agent could apply the approval label or post the approval comment (Decision 4, accepted).
- New code goes in a new package `src/superclaude/cli/issue_pipeline/` and tests in `tests/issue_pipeline/`. The tests in tests/issue_watch/test_module_boundaries.py pin what each issue_watch module may import, and tests/issue_watch/test_no_text.py forbids a gh call that asks for comment text, so issue_pipeline imports from issue_watch and never the reverse.
- Never edit `.claude/` mirrors; edit `src/superclaude/` and run `make sync-dev`. Always stage `.dev/tasks` and the `src/` changes, never `.claude/`; commit only when the owner asks.
- The merged requirements file in the brainstorm folder is not edited by any task; Task 19 writes the change list for it inside this package.
- Every command is run with `uv run`.
Start sha: 308fddc77748808748f87095d2c7da0e8a1bcac5
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/artifacts/merged-spec-change-list.md b/.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/artifacts/merged-spec-change-list.md
new file mode 100644
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/artifacts/merged-spec-change-list.md
@@ -0,0 +1,53 @@
+# Change list for the merged requirements (issue watcher claim handoff, Decision 6 = B)
+
+Target file, not edited by this plan: `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` (row ids below are that file's). This list says what each named item must become once design B (a person-opened coordinator starts the plan-writing agent as a supervised Orca worker for a watcher-claimed issue) is built. The owner applies it later; nothing here changes the file.
+
+Written for a person who has not seen the project. Plain words: the *watcher* is the timer job that notices an approved GitHub issue and starts a *claim* session for it; the *coordinator* is a session a person opened, which starts and answers *workers*; design B lets the claim session stop at "claimed, files written, no agent" and lets the coordinator start the agent that writes the plan.
+
+## 1. Item changes (one sentence each)
+
+| Item | Change |
+|---|---|
+| WA-01 (claim level) | Take the `--pipeline none` branch, now with the coordinator handoff: `launch.PROMPT_PATTERN` and `build_claim_prompt` emit `--pipeline none`, and the claim no longer creates a worktree or an agent (the coordinator does both steps afterwards). |
+| WA-02 (#450 edits) | The #450 edits list gains edit B: the issue text states that the watcher claims with `--pipeline none` and a coordinator, not the claim session, starts the plan-writing agent. |
+| WA-03 (runbook step) | The runbook step 1.3a also names who runs the coordinator that owns watcher-claimed issues on this host (one person-opened coordinator, one lock per issue) and says nothing starts while it is down. |
+| WA-04 (FU-1 record) | The FU-1 record adds preconditions a to k of `docs/designs/issue-pipeline-fu1.md` (a to j from the validation file, k = web-editor comment round trip) and the owner's written guard-loss acceptance for the one test issue. |
+| WA-07 | Moves from DEFERRED to live under B, and its "blocked by SW-13" is removed (SW-13 is now the delivery path, see below); its condition (4) is restated to cover the guard loss of the one G1 test issue, and (5) stays: no free text from the issue reaches a prompt. |
+| SW-13 | The supervised-worker route (`worker-start` by the coordinator, `ask` and `reply` for plan approval) is now the delivery path of the handoff, no longer a later sub-orchestrator redesign. |
+| OB-09 | A dashboard approval is only a message to the coordinator (WC-12): the human answer travels through the coordinator, which records it and tells the worker; the dashboard never approves by itself. |
+| Section 6.3 (roles) | Gains a worker row for the plan-writing worker: it writes the plan, asks the coordinator for approval and never pushes, comments, commits or creates worktrees. |
+| Section 6.4 rule 10 | Permission mode of every started session is accepted in writing, now including the guard loss: the one G1 test issue runs with permission checks off and no launch-level guard until G2 exists. |
+| Section 6.8 (grant table) | Gains a per-pipeline-issue grant row shape: one row per issue holding the plan reply, the marker comment, the mention, and the label and Status writes the coordinator may make. |
+
+## 2. New items, one per plan task
+
+| Task | New item (one sentence) |
+|---|---|
+| 16 | Remove the plain `approved` release from the launch-level guard and the launch prompt for every worktree-level claim; only a first line starting `/sc:implement`, `/sc:task` or `/task` releases (own branch, own pull request later). |
+| 1 | `issue_pipeline` package with `issue-pipeline plan-hash`: a SHA-256 over a named list of plan files (name, length and bytes each), shared by coordinator and worker. |
+| 2 | The approval line module and `check-approval`: only `approved` and `approved <record id> plan-sha256=<64 hex>` are accepted, whole text, no trimming. |
+| 8 | The first-live-test runbook `docs/designs/issue-pipeline-fu1.md` (document only), with the guard-loss acceptance and eleven `PENDING:` record lines. |
+| 3 | A locked, write-ahead approval record helper with an adoption row per (issue, stage) (`reserved`, `started`, `uncertain`) and an approval row per (issue, stage, plan hash), so a start and a continuation happen at most once. |
+| 4 | Stage predicates for the approval label and the `approved` comment (order after the plan reply, author type, assignee or approver, edits, plan hash), plus recorded real GitHub responses for the owner's issue. |
+| 5 | GitHub reads that turn comment text into booleans and fixed-pattern ids inside jq, under the watcher's call budget. |
+| 6 | The read-only `issue-pipeline stage-status` command. |
+| 7 | The worker brief builder from fixed templates for the three Feature rows (type `bug` refused), in the layout of `WORKER-CONTRACT.md` section 5. |
+| 9 | The brief's `Worktree:` slot changes from the contract's `shared feature worktree` or `child worktree` forms to `path:<existing worktree>`, the worktree the claim script made (Plan B). |
+| 15 | The `pending` subcommand of Plan B Task 15 (a new verb that belongs to the guard change G2, Tasks 13 to 15); what it prints is defined in Plan B, which this run did not read, so this row only records that the verb is a new item. |
+| 10 to 14 | Plan B items: the coordinator route (Tasks 9 to 12) and the guard change G2 (Tasks 13 to 15); this run did not read Plan B, so these rows name them only as the plan's own text refers to them and leave each task's wording to Plan B. |
+
+## 3. Owner decisions (Q35 to Q41), none open
+
+| Q | Question in plain words | Options | Recommended | Owner's answer |
+|---|---|---|---|---|
+| Q35 | How does the claim hand over: what does the watcher's claim do before the coordinator takes over? | **B1b**: the watcher claims with `--pipeline none` and the coordinator runs the existing worktree step (no claim code changes, only the watcher prompt and tests). **B2**: a new claim level that creates the worktree and copies files without an agent (about six more test files, and a worktree with no agent until the coordinator starts one). | B1b | **B1b**, 2026-11-15 (first 2026-11-14; the first reply wrote "Q53 b1b" and "2. Approved", read as Q35). |
+| Q36 | How fast is approval when no timer re-reads GitHub (decision Q31, no recurring timer)? | **A**: accept the delay and make Orca the fast path (approve in the coordinator session, immediate). **B**: a narrow timed read only for issues waiting for approval (reverses Q31 for that case). **C**: the person types "check now" after approving on GitHub. | A together with C | **Option A**, 2026-11-15 (first 2026-11-14 as "accepted delay"). Option C ("check now") is not selected and not built. |
+| Q37 | Where does the worker's plan-approval rule live? | A new rule in `WORKER-CONTRACT.md` next to WC-3 (written once). Only in each brief (no contract edit, every brief repeats it). | In the contract, next to WC-3 | **In `WORKER-CONTRACT.md` next to WC-3**, 2026-11-15 (first 2026-11-14). |
+| Q38 | How does a coordinator approval release a guarded worker (the later guard change G2)? | **A**: the coordinator writes the session's release file after recording the approval (needs the worker's session id, UNVERIFIED). **B**: the guard reads a coordinator-signed approval file (more guard code). | A if the first live test shows the session id can be found, else B | **The default until G2**, 2026-11-15 (first 2026-11-14): G2 is not built, so only the one G1 test issue can run; the route is chosen in Task 13 after the first live test. |
+| Q39 | How far does removing the plain `approved` release reach? | Remove it for every worktree-level claim (closes the self-approval hole; a person with no coordinator then types `/sc:implement` in the session). Keep it for person-run claims until G2 exists. | Keep for person-run claims (the earlier recommendation, not taken) | **Remove it now for every worktree-level claim**, with no person-run carve-out and no wait for G2 or the live test, 2026-11-15 (Task 16; built on branch `ironbelly/remove-approved-route`). |
+| Q40 | In what order do the design documents change? | One follow-up documentation PR for Tasks 17 and 18 (after #548). Fold them into the code PR of Task 11. | One follow-up documentation PR | **One follow-up documentation PR**, 2026-11-15 (first 2026-11-14), opened only after the owner reads the plan; no PR is opened from this plan, and Tasks 17 and 18 wait on Task 11. |
+| Q41 | What about the worktree with no agent, for the moment between the claim script and the coordinator's `worker-start`? | **A**: accept it and say so in the claim text (the script closes the plain first tab, nothing runs in the empty worktree, nothing starts while the coordinator is down). **B**: change the script to create the worktree with an agent (more claim code, a second agent instead of the worker). **C**: let `worker-start` create the worktree itself (skips the script's copy step and reuse lookup; rejected in the design session). | A | **A**, 2026-11-14: accept it and say so in the claim text. |
+
+## 4. Facts the first live test must measure (not decisions)
+
+The real `worker-start` argv and permission flags; whether `worker-start` accepts an exact existing worktree that the script created and leaves exactly one terminal; the `ask` and `reply` round trip, including whether the reply is stored as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; how a worker's session id can be found (it decides the G2 release route in Task 13); `ask` timeout and resume by message id; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; the GitHub label event shape; whether a comment typed in the GitHub web editor arrives as exactly `approved`; and what a comment edit does to `lastEditedAt`. Each is a precondition (a to k) of `docs/designs/issue-pipeline-fu1.md`.

Codegraph context
index_state: fresh
checked_at: 2026-11-16T21:51:31Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: ran on the Grep/Read floor.

Note for the reviewer: the only deliverable is .dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/artifacts/merged-spec-change-list.md (read the live file). Plan B was deliberately not read by the executor. The merged requirements file is at .dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md and may be read to verify the item ids.
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
