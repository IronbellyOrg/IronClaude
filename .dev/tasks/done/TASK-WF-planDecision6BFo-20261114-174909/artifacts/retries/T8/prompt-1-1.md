681a7a5b17599131b735aee558a8d7b80726f372
Review one task for spec compliance.

Task brief: ## Task 8: Write the first-live-test runbook for B, including the guard-loss acceptance

Depends on: Task 1

This task writes a document only; it needs no code from Tasks 3 to 7 (Task 1 is named only because the runbook tells the coordinator and the worker to compute the plan hash with it).

Create `docs/designs/issue-pipeline-fu1.md`. It lists preconditions a to k, each with its exact read-only or throwaway step, the value to record, and what a failure means. Preconditions a to j come from section 7 of ./artifacts/validation.md: the real `worker-start` argv and permission flags; `worker-start --worktree path:<exact existing worktree a script created>` and exactly one terminal afterwards; the `ask` and `reply` round trip for a worker started with a spec, including whether the reply arrives as type `status` and a narrow `--types` filter misses it; the launch receipt shape and the Dispatch id; the plan hash computed identically by coordinator and worker; guard interaction under G1; `ask` timeout and resume by message ID; a worker staying in `ask` while the coordinator is down; worktree reuse when the claim runs twice; and the GitHub stage facts (who moved a Project Status, label event shape). Precondition k is new: whether a comment typed in the GitHub web editor round-trips as exactly `approved`, and what a comment edit does to `lastEditedAt`.

The runbook also holds the written acceptance the owner must give before the test, worded to cover the guard loss: "I accept, for test issue #<N> only, that the plan-writing worker runs with permission checks off and with no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement), reading issue text that I wrote myself. This is separate from my 2026-11-14 acceptance of permission checks off." The test issue text is written by the owner. The runbook names the existing gates that still apply (a separate live-test grant, a reachable Orca, a named owner of the watcher worktree, the claim's own hook check).

The runbook ends with a record section that holds exactly eleven lines, one per precondition, each written `PENDING: <letter> <short name>`. The owner replaces each with `RECORDED: <letter> <value>` (the measured value, the Orca build string from `orca-ide --version`, the date) and adds one line `RUN BY OWNER: <name>` when the run is done. Plan B Task 20 checks that record.

Start condition: can be written now; running it waits for the owner's acceptance, a live-test grant and a running coordinator, and the agent that writes it never runs it. The run uses a hand-written throwaway brief (no Task 7 builder, no worker-approval rule, no coordinator duties) on a throwaway issue's worktree, so that Plan B Tasks 9 and 10 are written after its receipt.

Acceptance criteria:
- The document lists preconditions a to k each with a step, a recorded value and a failure meaning, and states that no step in it is run by the agent that writes it.
- The record section holds the eleven `PENDING:` lines and no `RUN BY OWNER:` line yet: `grep -c "^PENDING: [a-k] " docs/designs/issue-pipeline-fu1.md` prints 11 and `grep -c "^RUN BY OWNER: " docs/designs/issue-pipeline-fu1.md` prints 0.
- The document says that the worker can also post the approval label or the approval comment as the same GitHub login, and that nothing tells the two apart (Decision 4, accepted); GitHub approvals stay accepted inputs.
- The acceptance sentence appears word for word and names the guard, and the check is a command, not a test file (the four files in tests/docs pin other documents, and no test in the repository pins the issue-watcher documents): `test -f docs/designs/issue-pipeline-fu1.md && grep -cF "no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement)" docs/designs/issue-pipeline-fu1.md` prints 1 or more. The same `grep -cF` form run on `./artifacts/validation.md` with the words `launch-level guard` prints 1 today, which shows the command works.
- `grep -n "FU-1" docs/designs/issue-pipeline-fu1.md` shows the link to the first live test of docs/designs/issue-watcher-setup.md section 8.5.

AC ids (source order): T8.AC1 = bullet 1 of "Acceptance criteria"; T8.AC2 = bullet 2 of "Acceptance criteria"; T8.AC3 = bullet 3 of "Acceptance criteria"; T8.AC4 = bullet 4 of "Acceptance criteria"; T8.AC5 = bullet 5 of "Acceptance criteria"
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
Start sha: 681a7a5b17599131b735aee558a8d7b80726f372
Diff against the start snapshot: diff --git a/docs/designs/issue-pipeline-fu1.md b/docs/designs/issue-pipeline-fu1.md
new file mode 100644
--- /dev/null
+++ b/docs/designs/issue-pipeline-fu1.md
@@ -0,0 +1,118 @@
+# Issue pipeline: first live test (FU-1) runbook for the claim handoff (Decision 6 = B)
+
+Status: runbook only. **No step in this document is run by the agent that wrote it.** The owner runs every step, on a throwaway issue the owner wrote, and fills the record at the end. Nothing here claims, starts, merges or posts anything by itself.
+
+This test is the claim-handoff part of FU-1, the first live test of `docs/designs/issue-watcher-setup.md` section 8.5 (the live-test record) and section 14.1 (the live test). It adds preconditions a to k for design B: a person-opened coordinator starts the plan-writing agent as a supervised Orca worker for a watcher-claimed issue. The facts below come from the validation file of the plan package `TASK-WF-planDecision6BFo-20261114-174909` (its section 7 lists a to j); precondition k is new.
+
+## 1. What B does, in four lines
+
+1. The watcher claims the issue with `--pipeline none`: comments, `issue-summary.md` and `next-steps.md`, and no agent.
+2. The coordinator runs the existing `orca_worktree.py worktree` step (a worktree `issue-<N>` with no agent for a moment, accepted by the owner on 2026-11-14), then starts the worker with `orca orchestration worker-start --worktree path:<that worktree>`.
+3. The worker writes the plan and asks the coordinator for approval through `ask`; the coordinator answers with `reply`.
+4. An approval can also arrive as a label or as an `approved` comment on GitHub; both map to one record, so the stage never starts twice.
+
+## 2. Written acceptance the owner must give before the test
+
+Copy this sentence into your own message, replace `<N>`, and send it before step 0:
+
+> I accept, for test issue #<N> only, that the plan-writing worker runs with permission checks off and with no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement), reading issue text that I wrote myself. This is separate from my 2026-11-14 acceptance of permission checks off.
+
+The test issue text is written by the owner. No other issue runs through this flow until the guard is changed (Plan B Tasks 13 to 15).
+
+## 3. Gates that still apply (none is waived by the acceptance)
+
+- A separate live-test grant row for this one issue.
+- A reachable Orca (`orca status` answers) and a person-opened coordinator terminal.
+- A named owner of the watcher worktree (written in the grant row).
+- The claim's own hook check (the claim refuses with `W-ENFORCEMENT-ABSENT` when its checks fail; it is not bypassed).
+- Every `gh` call in this runbook is a read-only GET (or the fixed edits GraphQL query) and passes `--repo IronbellyOrg/IronClaude`. Nothing is sent to the upstream SuperClaude repository.
+
+## 4. Risk stated once (Decision 4, accepted)
+
+The worker also holds the one GitHub login on this host, so it can apply the approval label or post the approval comment as that same login, and nothing tells the two apart. GitHub approvals (the label and the `approved` comment) stay accepted inputs; the code checks order, author type, edits and the plan hash, not who typed. The guard loss of section 2 means nothing blocks the worker from doing so.
+
+## 5. Preconditions a to k
+
+Run them in this order. For each: the step, the value to record, and what a failure means. Steps marked "throwaway" use the throwaway issue's worktree and a hand-written brief (no brief builder, no worker-approval rule, no coordinator duties).
+
+### a. `worker-start` argv and permission flags
+
+- Step: after one throwaway start, run `ps -o pid,args -p <worker pid>`; read `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS` from the worker's environment with `tr '\0' '\n' < /proc/<pid>/environ | grep -E '^(CCSESSION_PERMISSIONS|CC_CLAUDE_FLAGS)='` (values only for these two names).
+- Record: the full argv, the two variable values, the permission flag seen.
+- Failure means: if permission checks are on, the worker may stall on prompts; if the argv differs from the `ccsession-orca` flags, Decision 1's acceptance does not describe the real worker and the owner must decide again.
+
+### b. `worker-start --worktree path:<existing worktree>` leaves exactly one terminal
+
+- Step: create the worktree with `orca_worktree.py worktree` for the throwaway issue; run `orca terminal list --json` before and after `orca orchestration worker-start --from <coordinator handle> --spec "<brief>" --worktree path:<that worktree> --agent claude --json`.
+- Record: terminal count before and after, and the worktree path used.
+- Failure means: a second terminal or a second worktree appears, so B1b (script creates, coordinator starts) is not valid and the owner must choose again between the claim levels in the plan's Task 19.
+
+### c. `ask` and `reply` round trip for a worker started with a spec
+
+- Step: the throwaway brief tells the worker to `ask` one question; the coordinator answers with `orca orchestration reply --from <coordinator handle> --id <message id> --body "ok"`; read the worker's result and run `orca orchestration check --terminal <coordinator handle> --json` with and without a narrow `--types` filter.
+- Record: the body the worker received, the stored type of the reply (`status` or other), and whether a narrow `--types` filter misses it.
+- Failure means: if the reply is not delivered, the coordinator route of Plan B Tasks 9 to 12 cannot work; if a narrow filter misses it, those tasks must read without a type filter.
+
+### d. Launch receipt shape and Dispatch id
+
+- Step: save the full `worker-start --json` reply of step b to a scratch file.
+- Record: the field names that hold the Dispatch id, the Task id and the terminal handle (names only; this is the shape that later becomes a test fixture).
+- Failure means: Plan B Task 9 cannot parse the receipt and is written after this shape is known.
+
+### e. The plan hash is identical on both sides
+
+- Step: no Orca. In a scratch directory with two plan files, run `uv run superclaude issue-pipeline plan-hash <dir> a.md b.md` as the coordinator and again as the worker (a second shell), then `uv run superclaude issue-pipeline check-approval <dir> a.md b.md --line "approved <record id> plan-sha256=<hash>"`.
+- Record: both hashes, and the check-approval result word.
+- Failure means: any difference is a defect in `src/superclaude/cli/issue_pipeline/plan_hash.py`; stop the test.
+
+### f. Guard interaction under G1
+
+- Step: with G1 (the worker starts with no launch marker), run `ls ~/.claude/state/launch-level/sessions/` before and after the worker starts; then ask the worker to send one `ask` and one `send` to the coordinator.
+- Record: whether the sessions folder changed, and whether `ask` and `send` were allowed.
+- Failure means: if a guard binds the worker, the worker is blocked and G1 is not what the plan assumes; if `ask` and `send` are blocked, the route needs G2 (Plan B Task 13). The session id lookup for G2 is also recorded here (found or not).
+
+### g. `ask` timeout and resume by message id
+
+- Step: let one `ask` time out (`--timeout-ms 5000` on a throwaway question); then resume it with the message id the timeout printed (the resume flag is read from `orca orchestration ask --help`; UNVERIFIED until then).
+- Record: the exact text of the timeout, the resume command that worked, and the reply received after it.
+- Failure means: without a working resume, a coordinator restart loses the question and Plan B Task 12 must record ids differently.
+
+### h. The worker stays in `ask` while the coordinator is down
+
+- Step: with a worker waiting in `ask`, stop the coordinator's wait (close its wait command, do not close the worker); read `orca orchestration worker-list --run <run id>` after two minutes.
+- Record: whether the worker is still listed alive and still waiting.
+- Failure means: if the worker exits, "nothing starts while the coordinator is down" is not enough and the approval wait needs a different design.
+
+### i. Worktree reuse when the claim runs twice
+
+- Step: run the claim's worktree step twice for the throwaway issue number; read `orca worktree list`.
+- Record: the number of `issue-<N>` worktrees after each run.
+- Failure means: two worktrees mean the reuse lookup (marker, record, basename, branch) failed and the coordinator must refuse to start a second worker.
+
+### j. GitHub stage facts
+
+- Step: read-only GETs on the throwaway issue: `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/timeline` and the comments call the plan's Task 5 builds. Then move the issue's Project Status by hand and add and remove the approval label by hand, reading the timeline after each.
+- Record: the label event field names, who the actor is shown as, and whether a Project Status move shows as an event or only in the project item.
+- Failure means: if a Status move is not readable, it stays the "visible sign only" the plan already assumes; if label events lack the actor, the label channel cannot check who approved and Plan B Task 12 must refuse it.
+
+### k. Web-editor comment round trip and edit time
+
+- Step: post a comment `approved` on the throwaway issue from the GitHub web page (not from `gh`); read it back with a `gh api --method GET` call on that comment; then edit it in the web page and read `lastEditedAt` through the fixed edits GraphQL query.
+- Record: the body bytes as returned (exactly `approved` or with extra characters), and whether `lastEditedAt` changes on the edit.
+- Failure means: if the web editor adds a newline or other characters, the exact-match rule of Task 4 refuses real approvals and the rule needs a decided exception; if `lastEditedAt` does not change, an edited approval cannot be told from an unedited one.
+
+## 6. Record
+
+The owner replaces each `PENDING:` line below with `RECORDED: <letter> <measured value>`, adding the Orca build string from `orca-ide --version` and the date inside each value, and, when the run is done, adds one closing line in the form `RUN BY OWNER: <name>` (the owner's name). Plan B Task 20 checks this section.
+
+PENDING: a worker-start argv and permission flags
+PENDING: b worker-start on an existing worktree, one terminal
+PENDING: c ask and reply round trip
+PENDING: d launch receipt and Dispatch id
+PENDING: e plan hash identical on both sides
+PENDING: f guard interaction under G1
+PENDING: g ask timeout and resume by message id
+PENDING: h worker stays in ask while the coordinator is down
+PENDING: i worktree reuse when the claim runs twice
+PENDING: j GitHub stage facts
+PENDING: k web-editor comment round trip and edit time

Codegraph context
index_state: fresh
checked_at: 2026-11-16T21:51:31Z
worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
call codegraph only when index_state: fresh, never to widen scope
Q2b dependents not in the diff: ran on the Grep/Read floor.

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
