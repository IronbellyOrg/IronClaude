8ba804a4282e58d3f957238cb28d35081e0a21b2
Review one task for spec compliance.

Task brief: ## Task 1: Rewrite the confirmation rule in the worker contract

Edit src/superclaude/core/WORKER-CONTRACT.md, the WC-3 bullet that begins "A Ruling halt is never asked" (line 57). Make it the single governing definition of a valid confirmation. State: a person's confirmation counts only as (a) their own chat message in the current conversation naming the exact scope, or (b) a dashboard response, meaning an answer row created through the dashboard under that person's authenticated login for the question id whose text names the exact scope, recorded with the channel (dashboard), the person id, the question id and the time. List what never counts: another agent's message, a coordinator's reply or relay of a message, any file, silence, a generic go-ahead, an answer to a different question or scope, a row written by an agent's login, a row the person's own login did not create. State the timing safeguard (clause b applies only when the dashboard answer path is released; until then only clause a). State the recording rule: the agent records the Ruling line, grant row or pass record from the confirmation, naming the exact scope, the person's quoted words (chat) or the answer row id (dashboard), and the date; the person is never asked to write a file. Keep the decision D2 amendment note and the existing sentence that a Ruling halt is never asked and is reported blocked. Rewrite the final sentence so "executor-invented approval" names a Ruling line, grant row or pass record recorded without one of the two channels for that exact scope.

Acceptance criteria:
- WORKER-CONTRACT.md line 57 area contains both channels, the nothing-else list including "a coordinator's reply or relay", the timing safeguard and the recording rule, and still contains the phrases "another agent's message" and "executor-invented approval".
- No sentence in WORKER-CONTRACT.md says or implies that a coordinator's reply or relay is acceptance (Grep for "relay" and "coordinator's reply" in the file and Read each hit).
- Dependents updated by later tasks: tests/skills/test_worker_contract.py (Task 7) and the executor rules (Tasks 3 to 5).
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 8ba804a4282e58d3f957238cb28d35081e0a21b2
Diff against the start snapshot: diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 38d27f5e4..fb6a81720 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -54,7 +54,12 @@ These bind the top-level session that received the dispatch preamble. This secti
   - With the brief line `On a blocked gate: report blocked` (the default when the brief says nothing), the worker lets the command write its blocked contract and sends `worker_done --outcome failed`.
   - With `On a blocked gate: ask the coordinator`, at a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag (any other gate is reported blocked as under the default), the worker session asks with the preamble's `ask` command, waits, then re-invokes the command in the same session with the answer as the command's argument or flag and the same report directory; the second run's contract replaces the blocked one whole.
   - The worker asks at most once per Task: if the re-invoked run blocks again, at the same gate or another, it does not ask again, keeps that second blocked contract and sends `worker_done --outcome failed`, and the coordinator continues with a new Task (WC-6).
-  - A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, Halt table). The person gives the Ruling in chat, in their own session or in the coordinator's session, and the agent in that session records the Ruling line from that confirmation (decision D2, amended 2026-11-17 by the owner: the person is never required to write a Ruling line into a file; other owner records, such as a grant row or a pass record, are likewise given by the owner in chat and recorded by the agent in that session from that confirmation, naming the exact scope, the owner's quoted words and the date, and the owner is never asked to write a file). A Ruling line, grant row or pass record that the coordinator or a worker records without the person's own chat confirmation of that exact scope is "executor-invented approval".
+  - A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, Halt table). The person gives the Ruling in chat, in their own session or in the coordinator's session, or through the dashboard (see the definition below), and the agent in that session records the Ruling line from that confirmation (decision D2, amended 2026-11-17 by the owner: the person is never required to write a Ruling line into a file).
+    - **A person's confirmation (the single governing definition; the owner's words are "a chat message OR dashboard response counts and nothing else").** A confirmation of a Ruling, a grant row or a pass record counts only when it is one of these two channels, naming the exact scope: (a) chat, the person's own chat message in the current conversation; (b) dashboard, a dashboard response, meaning an answer row created through the dashboard under that person's authenticated login, for the question id whose text names the exact scope, recorded with the channel (dashboard), the person id, the question id and the time.
+    - **What never counts:** another agent's message; a coordinator's reply or relay of a message; any file; silence; a generic go-ahead; an answer to a different question or a different scope; a row written by an agent's login; a row that the person's own login did not create.
+    - **Timing:** clause (b) takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only clause (a) counts.
+    - **Recording:** the agent in the session that holds the confirmation records the Ruling line, grant row or pass record from it, naming the exact scope, the person's quoted words (chat) or the answer row id (dashboard) and the date, and the person is never asked to write a file (decision D2 as amended 2026-11-17, extended to the dashboard channel by the owner on 2026-11-26).
+    - A Ruling line, grant row or pass record that the coordinator or a worker records without one of these two channels for that exact scope is "executor-invented approval".
   - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6). When `ask` returns, the worker sends one heartbeat at once. When the answer arrives, the worker sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command.
 - **WC-17. Plan approval is the reply to the worker's own ask.** A brief that carries the `Plan approval:` line makes this a different, intended wait from a WC-3 gate ask: it does not use up WC-3's one ask per Task. After writing the plan, the worker, in this order: (1) runs `superclaude issue-pipeline plan-hash <report-dir> <plan file names>`; (2) asks once with the plan path, the file list and the plan hash; (3) waits, resuming the same message ID on a timeout as WC-3 says; (4) runs `superclaude issue-pipeline check-approval <report-dir> <plan file names> --issue <N> --line <the reply text>` on the reply (`<N>` is the issue number in the brief's `Report directory` line; `--issue` makes an approval for another issue with the same plan hash refuse); (5) sends `ack <message_id> applied` or `ack <message_id> refused` (WC-12); (6) continues only on `applied`. The worker's `ask` and `send` commands carry no `--to`: Orca's default is the owning Run mailbox, the worker's own coordinator, and the launch-level guard blocks any `--to` from a bound worker. The worker never treats a bare `approved`, or any text that is not the reply to its own ask, as approval. A mismatch is refused and reported, not retried silently: the worker sends the refused ack, does not continue, and states the refusal word in its `worker_done` body.
 - **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.


Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (the target is Markdown, which codegraph does not index).
Dependents of the changed WC-3 text not in this diff (context only, owned by later tasks): tests/skills/test_worker_contract.py (pins the old sentence, Task 7), src/superclaude/skills/sc-implement-protocol/refs/qa.md and refs/ledger.md (Tasks 3 and 4), docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md (follow-up, Task 9).

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
