2c5848e7a7fa1b5d6ee6880bb0a327a35fe367c2
Review one task for spec compliance.

Task brief: ## Task 2: Align the rest of the worker contract with the single definition

Depends on: Task 1

Read and, where they conflict with Task 1, edit these places in src/superclaude/core/WORKER-CONTRACT.md: WC-17 (line 59, plan approval is the reply to the worker's own ask), line 190 (a coordinator never "writes or drafts a Ruling"), the resume section (lines 256-278, including check 3 item (4) that points to the Ruling eligibility rule), and the issue-pipeline bullets (lines 296-303, "Plan approval", "Completion", "Never", and the grant-row wording). Add a short pointer to the WC-3 definition where a place restates who may confirm; do not restate the full rule a second time. Leave any place that is about timing or mechanics, not about who confirms, unchanged.

Acceptance criteria:
- Each place named above has been read, and the final report of this task lists which were edited and which were left unchanged with the reason.
- Where a place says approval or confirmation is given in chat, it now either points to the WC-3 definition or names both channels; none contradicts the single definition.
- WC-17 and the plan-approval flow keep their mechanics (plan hash, check-approval, ack) unchanged.
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 2c5848e7a7fa1b5d6ee6880bb0a327a35fe367c2
Diff against the start snapshot: diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index fb6a81720..148db9614 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -61,7 +61,7 @@ These bind the top-level session that received the dispatch preamble. This secti
     - **Recording:** the agent in the session that holds the confirmation records the Ruling line, grant row or pass record from it, naming the exact scope, the person's quoted words (chat) or the answer row id (dashboard) and the date, and the person is never asked to write a file (decision D2 as amended 2026-11-17, extended to the dashboard channel by the owner on 2026-11-26).
     - A Ruling line, grant row or pass record that the coordinator or a worker records without one of these two channels for that exact scope is "executor-invented approval".
   - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6). When `ask` returns, the worker sends one heartbeat at once. When the answer arrives, the worker sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command.
-- **WC-17. Plan approval is the reply to the worker's own ask.** A brief that carries the `Plan approval:` line makes this a different, intended wait from a WC-3 gate ask: it does not use up WC-3's one ask per Task. After writing the plan, the worker, in this order: (1) runs `superclaude issue-pipeline plan-hash <report-dir> <plan file names>`; (2) asks once with the plan path, the file list and the plan hash; (3) waits, resuming the same message ID on a timeout as WC-3 says; (4) runs `superclaude issue-pipeline check-approval <report-dir> <plan file names> --issue <N> --line <the reply text>` on the reply (`<N>` is the issue number in the brief's `Report directory` line; `--issue` makes an approval for another issue with the same plan hash refuse); (5) sends `ack <message_id> applied` or `ack <message_id> refused` (WC-12); (6) continues only on `applied`. The worker's `ask` and `send` commands carry no `--to`: Orca's default is the owning Run mailbox, the worker's own coordinator, and the launch-level guard blocks any `--to` from a bound worker. The worker never treats a bare `approved`, or any text that is not the reply to its own ask, as approval. A mismatch is refused and reported, not retried silently: the worker sends the refused ack, does not continue, and states the refusal word in its `worker_done` body.
+- **WC-17. Plan approval is the reply to the worker's own ask.** A brief that carries the `Plan approval:` line makes this a different, intended wait from a WC-3 gate ask: it does not use up WC-3's one ask per Task. After writing the plan, the worker, in this order: (1) runs `superclaude issue-pipeline plan-hash <report-dir> <plan file names>`; (2) asks once with the plan path, the file list and the plan hash; (3) waits, resuming the same message ID on a timeout as WC-3 says; (4) runs `superclaude issue-pipeline check-approval <report-dir> <plan file names> --issue <N> --line <the reply text>` on the reply (`<N>` is the issue number in the brief's `Report directory` line; `--issue` makes an approval for another issue with the same plan hash refuse); (5) sends `ack <message_id> applied` or `ack <message_id> refused` (WC-12); (6) continues only on `applied`. The worker's `ask` and `send` commands carry no `--to`: Orca's default is the owning Run mailbox, the worker's own coordinator, and the launch-level guard blocks any `--to` from a bound worker. The worker never treats a bare `approved`, or any text that is not the reply to its own ask, as approval. The approval the coordinator carries in that reply is read from GitHub evidence under the issue-pipeline rules; WC-3 defines a person's confirmation for a Ruling, a grant row or a pass record and does not change this mechanism. A mismatch is refused and reported, not retried silently: the worker sends the refused ack, does not continue, and states the refusal word in its `worker_done` body.
 - **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.
 - **WC-7. Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. A worker runs each chained `Command:` by invoking its Skill. Reading the command file and following it from memory does not satisfy WC-7.
 - **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this. When `check` returns a batch, the worker handles every message in it before acknowledging the batch. For each coordinator message that answers or directs it, the worker first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts. A message ID already applied gets only `ack <message_id> applied (duplicate)`.
@@ -271,7 +271,7 @@ Orca settles a Task on any valid `worker_done` and does not start ready Tasks it
    - No one runs a git command there that changes HEAD, the index or the working tree. The halted worktree is not merged or removed.
 
    `E-RESUME-NEEDED` alone may be re-run by the coordinator without the person, as the same command in the same worktree, and only when the ledger shows no freeze.
-2. *Lifting the freeze.* The freeze lifts only when the person's explicit hand-back is recorded in the coordinator's run notes **and** the ledger shows the matching state:
+2. *Lifting the freeze.* The freeze lifts only when the person's explicit hand-back (a confirmation as WC-3 defines it) is recorded in the coordinator's run notes **and** the ledger shows the matching state:
    - "Ruling written" requires the check in item 3 to pass.
    - "session ended" (after the person ran `/sc:implement` in their own session) requires the halted task to be `complete` and the ledger's last line to parse. The drift baseline is then re-recorded.
 
@@ -302,10 +302,10 @@ These duties apply only to an issue that the issue watcher claimed with `/sc:iss
 - **Status to command (level `none` only).** The coordinator starts a worker only for a `none` claim, and the brief it passes to `worker-start --spec` is built by `superclaude.cli.issue_pipeline.brief` with one row per Status: Research runs `/sc:research`; Spec runs `/sc:design` when `issue-summary.md` has `spec-route: design` and `/sc:brainstorm` (with `--handoff design`) when it has `spec-route: brainstorm`; Plan runs `/sc:workflow` and stops before `/sc:implement` and `/task`; Debug runs `/sc:troubleshoot` without `--fix`. Ready, Backlog, In progress, In review and Done start nothing. Claims at the other levels (`worktree`, `full`, `full submit`) launch their own agent, which runs the stage command from its launch prompt; the coordinator starts no worker for them and no brief has a level slot. After the coordinator mirrors the Status or moves it to In review, the Project values have changed, so a relaunch needs the owner to move the Status back to an allowed value, because In review fails the project check.
 - **Reserve before starting.** Create the adoption row (`adopt-create`) before `worker-start`; only a `created` result may start a worker. Mark the row `started` with the Dispatch id (`adopt-mark`) when `worker-start` returns ready, and `uncertain` when it does not. Never start again for an `uncertain` row: settle it by reading `worker-list`.
 - **Worktree, then worker.** Run the existing worktree step of the installed `sc-issue-protocol` skill (the script orca_worktree.py, subcommand worktree, with `--repo <R> --number <N> --base origin/<B> --source <the claim's issue folder>`), which creates or reuses the worktree without launching an agent of its own (it must copy the claim's issue folder in first), then run `worker-start --worktree path:<exact path it printed> --agent claude --spec <the worker brief for the issue>` straight after it, so the worker is that worktree's agent and the worktree is never left without one or used by anyone else.
-- **Plan approval.** The worker asks once with the plan path, file list and plan hash. Post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status --repo <the issue's repo>` at each gate or wake. The automatic approval record is the claim-time approval kept in `dispatch.json` plus the adoption row; it is never the plan-hash row, and `stage-status` refuses a claim-time approval dated before the plan reply (`label-before-plan`). Create the plan-hash approval row (`record-create`) only when the worker's `ask` carries the plan hash and `stage-status` reports the approval as accepted. On approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row `instructed` and then, from the worker's ack, `acked` (`record-mark`).
+- **Plan approval.** The worker asks once with the plan path, file list and plan hash. Post the plan reply with the hash and file list and mention the assignee, then read GitHub through `stage-status --repo <the issue's repo>` at each gate or wake. The automatic approval record is the claim-time approval kept in `dispatch.json` plus the adoption row; it is never the plan-hash row, and `stage-status` refuses a claim-time approval dated before the plan reply (`label-before-plan`). Create the plan-hash approval row (`record-create`) only when the worker's `ask` carries the plan hash and `stage-status` reports the approval as accepted. On approval write the row, then `reply` with `approved <record-id> plan-sha256=<hash>`, then mirror the label and Status; mark the row `instructed` and then, from the worker's ack, `acked` (`record-mark`). The approval is the GitHub evidence `stage-status` accepts, not the coordinator's own word; the WC-3 definition of a person's confirmation (a chat message or a dashboard response, nothing else) covers Rulings, grant rows and pass records and leaves this mechanism unchanged.
 - **Route B adds no exception to "never answer a person prompt".** The worker's plan boundary is crossed by the reply to its own `ask`, which is not a person prompt, so the coordinator types nothing into a worker's terminal for this flow.
 - **Completion.** After the coordinator has read a level-`none` worker's `worker_done` contract, or a launched agent's result file `.dev/issues/<N>/result.md` (noticed through the `/sc:sweep` report it already reads, WC-16), it runs `superclaude issue-pipeline complete --repo <the issue's repo> --issue <N> --project-id <the Project id from the repo's watcher config> --run <the approval event id of this run, from the issue's dispatch.json entry> --outcome <succeeded|failed|blocked|partial> [--summary <the result file>]`, only under that issue's grant row. The verb prints one closed word (a `refused:` or `failed:` word exits 1) and echoes no issue text. It posts one result comment per run; only `succeeded` moves the Status, to In review, and a failed, blocked or partial outcome never moves the Status. A worker and a launched agent never run this verb. The launch-level guard refuses it by a text pattern that is best effort; the grant-row rule is the control.
-- **Never:** tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker by itself (WC-6 and the person decide); post an issue write without that issue's grant row.
+- **Never:** tell a worker to pass its plan boundary without an approval row; act on a Status move alone; relaunch a dead worker by itself (WC-6 and the person decide); post an issue write without that issue's grant row (a grant row is recorded from the person's confirmation as WC-3 defines it).
 
 ### Worked example: gate hit, answer, new Task
 

--- new untracked file .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t2-report.md ---
# Task 2 report: places in WORKER-CONTRACT.md checked against the WC-3 definition

Each place was Read in full before deciding.

| Place (after Task 1 line numbers) | Decision | Reason |
|---|---|---|
| WC-17 plan approval, `src/superclaude/core/WORKER-CONTRACT.md:64` | edited (one sentence added at its end) | Says the approval the coordinator carries is read from GitHub evidence under the issue-pipeline rules and that WC-3 covers Rulings, grant rows and pass records and does not change this mechanism. Plan hash, `check-approval` and ack steps unchanged. |
| "never on silence" list, line 195 ("writes or drafts a Ruling") | unchanged | About what a coordinator never does on silence; it does not state who may confirm. |
| Resume item 2 (hand-back), line 274 | edited (parenthetical added) | A person's explicit hand-back is a confirmation; it now points to the WC-3 definition. |
| Resume item 3 (the Ruling line check, items (1) to (6)), lines 279 to 285 | unchanged | Mechanical checks of the ledger line; they say nothing about the channel of confirmation. Provenance wording lives in refs/ledger.md (Task 4). |
| Issue-pipeline "Plan approval" bullet, line 305 | edited (sentence added at its end) | Says the approval is GitHub evidence accepted by `stage-status`, not the coordinator's word, and that the WC-3 definition leaves this mechanism unchanged. |
| Issue-pipeline "Completion" bullet, line 307 | unchanged | Mentions the grant row only as the control for the `complete` verb; the grant-row rule is pointed to from the "Never" bullet. |
| Issue-pipeline "Never" bullet, line 308 | edited (parenthetical added) | A grant row is recorded from the person's confirmation as WC-3 defines it. |

Open question for the owner (not changed here): whether the GitHub plan-approval path should also accept a dashboard response. It is a separate mechanism from the Ruling, grant row and pass record confirmations that WC-3 covers.



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (the target is Markdown, which codegraph does not index).
Dependents not in this diff (context only): tests/skills/test_worker_contract.py pins WC-3 text (Task 7). The task-owned report is at .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t2-report.md and lists each place as edited or unchanged with its reason (it is a package artifact, not a delivery file).

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
