ea648026ab2542bf96d4c47028d04f9174235f3f
Review one task for spec compliance.

Task brief: ## Task 3: Extend WC-12, WC-3, WC-5 and WC-7 (C-3a, C-3b, C-4, C-16)

In `src/superclaude/core/WORKER-CONTRACT.md` section 3, append the design section 10.2 text:
- to WC-12 (C-3a): the worker handles every message in a `check` batch before acknowledging the batch; for each coordinator message that answers or directs it, it first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts; a message ID already applied gets only `ack <message_id> applied (duplicate)`;
- to the WC-3 `ask` timeout bullet (C-3b): when `ask` returns, the worker sends one heartbeat at once, and when the answer arrives it sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command;
- to WC-5 (C-4): the closing report is never sent as `status`, `handoff` or a reply, and a coordinator may not read those as completion;
- to WC-7 (C-16): a worker runs each chained `Command:` by invoking its Skill, and reading the command file and following it from memory does not satisfy WC-7.

Add one `RULE_PHRASES` pin per rule.

Acceptance criteria (ids T3.AC1, T3.AC2 in order):
- T3.AC1: Each of the four rules ends with its new text, and the existing WC-12, WC-3, WC-5 and WC-7 pins still pass.
- T3.AC2: Four new pins exist, each carrying a key phrase from the added text (for example "applied (duplicate)", "sends one heartbeat at once", "never sent as `status`, `handoff` or a reply", "does not satisfy WC-7").
Global constraints: ## Constraints

- Edit only `src/superclaude/core/WORKER-CONTRACT.md` and `tests/skills/test_worker_contract.py`. No code beyond tests; nothing for the v2 monitor, adapters, hooks or dashboard.
- The contract has no other copy in the repo (no `plugins/superclaude/core/` copy, no level-table copy in `HOW-WE-WORK.md`), and `make sync-dev` / `make verify-sync` do not cover `core/`; both still run before the PR.
- Use the exact wording of section 10.2 of the design (read it in pieces of at most 80 lines). One adaptation: C-2's "in the preamble command's payload or phase text" becomes "in the heartbeat's subject or phase text, or a `status` body line", because the heartbeat verb takes typed flags (`--type heartbeat --subject alive --task-id --dispatch-id --phase`) and has no custom payload field.
- Every new pin is a `RULE_PHRASES` entry `"<name>": (<ident or None>, [<phrases>])` whose phrases appear verbatim in the contract; when an ident is given, one contract line must hold both the ident and the first phrase. `test_contract_states_rule` and `test_rule_check_fails_when_rule_removed` then cover it with no new test function.
- Existing pins must keep passing: WC-10 ("at the cadence its preamble sets", "split into waits of at most 4 minutes"), WC-5, WC-7, WC-12, WC-3, WC-6, heartbeats, brief-layout, brief-template, and the guard-before-`Command:` check.
- Statements the design marks unverified are written as UNVERIFIED in the contract text, never as fact: what `check --wait` wakes on without `--types`; the cause of case 5, answers not seen (lead: `orca orchestration reply` stores type `status` with subject "Re: Question", so a narrow `--types` waiter may miss it); whether a permission-prompt or compact-thrashing attention category exists; what Claude Code does with text typed while a tool call runs; whether two consumers on one mailbox both get a batch.
- Owner decisions of 2026-11-07 are binding: never resend a mailbox copy of an answer; the worker confirms an answer with an ack; with no ack after 5 minutes and a probe that positively shows an empty idle prompt, the coordinator types ONE copy into the terminal; at 15 minutes it reports to the person. A person-directed cancellation with confirmed quiescence settles a live attempt; context exhaustion alone is not proof.
- `unverifiable` liveness is absence and never authorizes stop, abandon, retry or release.
- `.dev/tasks/` is always staged (`git add .dev/tasks`), this package and its `./artifacts/` included. Never stage `.claude/` mirrors.
- Evidence logs go under `./artifacts/`.
Start sha: ea648026ab2542bf96d4c47028d04f9174235f3f
Diff against the start snapshot:
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index d99dac88..010929e6 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -55,10 +55,10 @@ These bind the top-level session that received the dispatch preamble. This secti
   - With `On a blocked gate: ask the coordinator`, at a gate that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag (any other gate is reported blocked as under the default), the worker session asks with the preamble's `ask` command, waits, then re-invokes the command in the same session with the answer as the command's argument or flag and the same report directory; the second run's contract replaces the blocked one whole.
   - The worker asks at most once per Task: if the re-invoked run blocks again, at the same gate or another, it does not ask again, keeps that second blocked contract and sends `worker_done --outcome failed`, and the coordinator continues with a new Task (WC-6).
   - A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`~/.claude/skills/sc-implement-protocol/refs/qa.md`, Halt table). The person gives the Ruling in their own session or writes the Ruling line into the ledger themselves after the worker has settled (decision D2). A Ruling line written or drafted by the coordinator or by any worker is "executor-invented approval".
-  - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6).
-- **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. Before P1, when no command writes a contract, a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task. The worker takes `--outcome` and `--report-path` from that rule. The body's first sentence then states the command's own status, or that its report file has none, instead of `worker_status`.
-- **WC-7. Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is.
-- **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this.
+  - On an `ask` timeout the worker resumes the same message ID and never creates a duplicate. No heartbeat is sent while blocked in `ask`. An answer that arrives after the worker has settled is carried by a new Task (WC-6). When `ask` returns, the worker sends one heartbeat at once. When the answer arrives, the worker sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command.
+- **WC-5. Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. `--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists; `--outcome succeeded` when it is `succeeded` or `partial`, including an audit whose verdict is FAIL (the audit itself succeeded). The worker never reads the command's own `status` field for this; any other `worker_status` value is treated as `failed`. The first sentence of the body states `worker_status` and the verdict. If an authorized commit (WC-9) is refused or fails, the worker sends `--outcome failed`, and the body's first sentence reads `worker_status: succeeded; commit not made` followed by the reason. Before P1, when no command writes a contract, a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task. The worker takes `--outcome` and `--report-path` from that rule. The body's first sentence then states the command's own status, or that its report file has none, instead of `worker_status`. The closing report is never sent as `status`, `handoff` or a reply; a coordinator may not read those as completion.
+- **WC-7. Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. Lifecycle messages (heartbeat, ask, check, `worker_done`) are sent only by that top-level session, never by a subagent. A command's own Agent-tool fan-out stays as it is. A worker runs each chained `Command:` by invoking its Skill. Reading the command file and following it from memory does not satisfy WC-7.
+- **WC-12. Coordinator follow-ups are pulled, not pushed.** The worker runs the preamble's `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. Commands need no change for this. When `check` returns a batch, the worker handles every message in it before acknowledging the batch. For each coordinator message that answers or directs it, the worker first sends `status` with a body starting `ack <message_id> applied|queued|refused`, then acts. A message ID already applied gets only `ack <message_id> applied (duplicate)`.
 - **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).
 - **Heartbeats.** The worker session sends heartbeats at the cadence its preamble sets, using the preamble's own command; it sends none while blocked in `ask` or `check --wait`, and a subagent never sends one (WC-7). Each heartbeat carries a progress token, in the heartbeat's subject or phase text, or a `status` body line: the current `Command:` line index and a count that rises only when on-disk progress rises (WC-15), plus `expect_silence_min` before a step expected to outlast the cadence. A heartbeat whose token has not changed is evidence that the process exists, not that the work is progressing. Command steps keep each blocking wait short enough for this (WC-10).
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index e31dd8b1..612e1603 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -247,6 +247,34 @@ RULE_PHRASES = {
             "evidence that the process exists, not that the work is progressing",
         ],
     ),
+    "wc12-ack-batch": (
+        None,
+        [
+            "the worker handles every message in it before acknowledging the batch",
+            "ack <message_id> applied|queued|refused",
+            "applied (duplicate)",
+        ],
+    ),
+    "wc3-ask-return-heartbeat": (
+        None,
+        [
+            "When `ask` returns, the worker sends one heartbeat at once",
+            "sends the WC-12 ack for that message ID at the first legal opportunity, before re-invoking the command",
+        ],
+    ),
+    "wc5-closing-report-type": (
+        None,
+        [
+            "The closing report is never sent as `status`, `handoff` or a reply",
+        ],
+    ),
+    "wc7-skill-invocation": (
+        None,
+        [
+            "A worker runs each chained `Command:` by invoking its Skill",
+            "Reading the command file and following it from memory does not satisfy WC-7",
+        ],
+    ),
     "brief-template": (
         None,
         [
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
