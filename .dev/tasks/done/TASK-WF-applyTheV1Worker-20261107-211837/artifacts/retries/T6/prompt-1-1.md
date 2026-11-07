d092fde2ee5f864f21bb35318b3f177ce6820954
Review one task for spec compliance.

Task brief: ## Task 6: Add the "Liveness supervision" subsection (C-7)

Add a `### Liveness supervision` subsection to section 4 of `src/superclaude/core/WORKER-CONTRACT.md` (after "What the coordinator owes each worker" or another place that keeps section order readable), summarising design sections 4, 6, 7 and 8:
- the wait: `check --wait` listing all nine types (`status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat`) with `--timeout-ms 300000`; `--types` only decides when a waiter wakes; a Delivery is the whole FIFO batch, replayed until `--ack` and shared by several waits on one Run inbox; every message is handled and a run-notes line is written per message ID before `--ack`; an unknown type is shown, never silently acked; lifecycle messages are checked against the current Task and Dispatch ID and a mismatch is quarantined;
- the sweep after every wake or timeout, at most once every 5 minutes: one `worker-list`, one prompt-wait listing, one `stat` per worker contract path (WC-11), costly probes only for triggered workers, the deadline W, and "after three empty waits, enumerate with `worker-list`";
- the state table (starting, progressing, long step, idle at prompt, blocked on a person prompt, blocked in `ask`, context exhausted, unreachable, exited, finished but unreported, done, unknown) with the coordinator's response for each;
- the ack timeline of owner decision (a): no blind mailbox resend; one typed copy only on a positively identified idle empty prompt after 5 minutes without an ack; report to the person at 15 minutes; never type into a busy, unknown or person-prompt session;
- the response ladder L0 to L5 with its caps and the restart budget, including the C-7 sentence from design section 10.2: "When the ladder is exhausted, the coordinator reports to the person (L5). It restarts a worker (L4) only on one of Orca's positive stall proofs (`exited`, the process exit, or a transcript whose final agent turn sent no `worker_done`), or on the person's recorded stop, and then settles it under WC-6. Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs.";
- the nudge text and the resume note placed in the new Task's brief after the guard line and before the `Command:` lines;
- the never-on-silence list (no stop, retry, release, failed mark, answer to a person-only prompt, Ruling, or lifecycle message for the worker on silence, a passed deadline, `unverifiable` or screen text alone);
- the five UNVERIFIED items from the Constraints, each labelled UNVERIFIED.

Text blocks inside fences must contain no line that starts with a number followed by "." or ")". Add pins for the subsection heading, the nine-type wait, the C-7 stall-proof sentence, the never-on-silence rule, the owner-decision ack timeline and the UNVERIFIED label.

Acceptance criteria (ids T6.AC1, T6.AC2, T6.AC3 in order):
- T6.AC1: The subsection exists in section 4 and states every item above, with each of the five unverified points marked UNVERIFIED.
- T6.AC2: The nine message types and `--timeout-ms 300000` appear on one `check --wait` line; "Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs" appears verbatim.
- T6.AC3: The new pins pass and `uv run pytest tests/skills/test_worker_contract.py -q` passes.
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
Start sha: d092fde2ee5f864f21bb35318b3f177ce6820954
Diff against the start snapshot:
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 5b5d3532..34e0e30e 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -92,6 +92,113 @@ The contract only works if the brief carries what the command would otherwise as
 
 After `worker_done`, the coordinator opens the contract, then releases or reuses the worker.
 
+### Liveness supervision
+
+These are the v1 liveness rules. Every time and cap below is a starting value, not a measured one: the coordinator keeps the values it uses in its run notes, a brief may override them, and a worker may not.
+
+**The wait.** The coordinator waits with every type listed:
+
+`orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000`
+
+- `--types` only decides when a waiter wakes. A returned Delivery is the whole FIFO batch, replayed until `--ack`, and shared by every wait on one Run inbox.
+- The coordinator handles every message in the batch and writes one run-notes line per message ID before it sends `--ack`. If the notes write fails, the batch is not acked.
+- An unknown type puts its sender in S11 and is shown to the person, never silently acked.
+- `worker_done`, `question`, `escalation`, `handoff` and `merge_ready` are checked against the sender's current Task ID and Dispatch ID; a mismatch is quarantined: logged and shown to the person, never applied.
+- After three empty waits in a row, the coordinator enumerates its workers with `worker-list`.
+- Per type: `heartbeat` updates the worker's heartbeat record and is never a stall proof; a `status` carrying an ack line goes to the ack rules below, one naming a report path or saying the work is complete sets S9, any other is logged; `worker_done` opens the contract, and a second one for the same dispatch is logged and ignored; a `question` is answered with `reply --id` or forwarded to the person, and starts the ack clock; an `escalation` gets L1, then L5; a `decision_gate` goes to the person; a `handoff` leaves any new work to the coordinator's decision (WC-13); a `merge_ready` merges only on the person's instruction; a `dispatch` is logged as unexpected. The coordinator never sends or synthesizes `worker_done` for a worker.
+
+**The sweep.** After every wake or timeout, at most once every 5 minutes, the coordinator runs one sweep: one `worker-list`, one prompt-wait listing (`worktree ps --agent-wait`) and one `stat` per worker contract path (WC-11), updating each worker's heartbeat record (arrival time, progress token, declared window). Costly probes (transcript tail, screen read) run only for workers a trigger fired for in this sweep.
+
+- Deadline W is `max(10 min, 2 x the observed median heartbeat interval)`, or the worker's declared `expect_silence_min`, capped at 45 minutes.
+- A semantic change is a substantive change of the progress token, the contract file or the transcript content. A message arrival or a repeated identical read is not one.
+- Starting values: startup grace 10 minutes; a read-only probe after 10 minutes with no semantic change; a named state or an L5 report by 15 minutes after the last semantic change; an unreachable report after 10 minutes of continuous `unverifiable`.
+
+| State | Trigger | Response |
+|---|---|---|
+| S0 starting | No progress token or transcript 10 minutes after start | L1, then L2 "begin your brief", then L5 by 15 minutes |
+| S1 progressing | Token changed within W and a semantic change within 10 minutes | L0 |
+| S2 long step | A declared window, or transcript activity under 5 minutes old | L1 at 10 minutes even inside the window (the window defers only nudges and typed text); past the window, L1, L3, then L5 by 15 minutes |
+| S3 idle at prompt | No token change for W, and all of: the last transcript entry is 5 minutes old or older with no `worker_done` in the final turn; the screen shows an empty prompt with no tool running; no pending ask | L1, L2, L3; L4 only with a stall proof; a third idle episode goes to L5 |
+| S4 blocked on a person prompt | `agentWait` is non-null | Capture the screen; L5 at 5 minutes plus Orca's own delay, re-reported every 15 minutes; never answer the prompt |
+| S5 blocked in ask | An open `question` | Answer it, then the ack timeline |
+| S6 context exhausted | Token unchanged for W while heartbeats arrive, and screen text such as `Autocompact is thrashing` confirmed by a second read 5 minutes later | Interrupt with "write your handoff file now, then end your turn"; if the turn ends without `worker_done`, L4 within the budget, otherwise L5 and ask the person for a recorded stop |
+| S7 unreachable | Liveness `unverifiable` | L5 after 10 minutes; never L4 |
+| S8 exited | Liveness `exited` | Settle under WC-6, then L4 or L5 |
+| S9 finished but unreported | Contract present and no `worker_done` within one sweep | L1 (read the contract), then L2 "send `worker_done` per WC-5 with `--report-path <path>`", then L5 by 10 minutes after the nudge |
+| S10 settled | `worker_done` received | None |
+| S11 unknown | The deciding evidence is stale or unknown | L1, then as the resulting state; no typed input while S11 |
+
+**Answers and acks.** The coordinator never resends a mailbox copy of an answer; the worker confirms each answer with an ack line (WC-12). The ack timeline, from the moment the answer is sent:
+
+- A1, at 0: record the answer as pending_ack.
+- A2, at 5 minutes with no ack and no heartbeat showing the ask returned: L1 probe of `agentWait`, the transcript tail and the screen.
+- A3, at 5 minutes, only when the probe positively shows an idle, empty prompt: type ONE copy into the terminal with `orca terminal send --text "<copy>" --enter --wait-submit <s>`, at most one per message ID.
+- A4, at 15 minutes: L5 report to the person with the message ID, the answer, the receipt fields and the probe results.
+- Input veto: never interrupt; never type into a busy, S11 or S4 session; never answer a person prompt. Without a positive idle identification, skip to A4. A worker with no terminal skips A3.
+- A duplicate ack is a no-op. An ack does not prove the answer was right: the outcome is still read from the contract after `worker_done`. At settlement, a pending ack closes as `unacked-at-settlement`.
+
+The typed copy is one line:
+
+```text
+[coordinator] Answer to your message <message_id> (reply <R-task-n>): <answer>. If you already applied <message_id>, only send: ack <message_id> applied (duplicate). Otherwise send the ack first, then continue.
+```
+
+**The ladder.** A lineage is the original Task plus every replacement; caps count per lineage.
+
+| Rung | Action | When | Cap |
+|---|---|---|---|
+| L0 observe | Watch only | Always | None |
+| L1 probe | Read-only: `worker-show`, `worker-read --source transcript`, a screen read, the contract `stat` | A trigger fired | None |
+| L2 nudge | Typed with `--wait-submit`; the S6 variant is an interrupt plus a handoff request | L1 confirms S3, S9 or S6 at an identified prompt | 1 per incident, 2 per lineage; a nudge with no turn start still counts |
+| L3 ask | Typed: "Reply with `status`: current step, what you are waiting for" | L2 failed once and the state is still ambiguous | 1 per incident |
+| L4 restart with resume note | Reconcile, stop the worker, settle it, set the old Task `failed --result cancelled`, create a new Task | Only with an Orca stall proof, or a person-directed cancellation with confirmed quiescence (WC-6), and only within the restart budget | 1 per rolling 60 minutes, 2 per lineage; WC-6's three-failed-starts rule also applies, whichever is stricter |
+| L5 report to the person | Report the state, its evidence and what was tried | Any person-only state, or any cap reached | S4 is re-reported every 15 minutes |
+
+When the ladder is exhausted, the coordinator reports to the person (L5). It restarts a worker (L4) only on one of Orca's positive stall proofs (`exited`, the process exit, or a transcript whose final agent turn sent no `worker_done`), or on the person's recorded stop, and then settles it under WC-6. Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs.
+
+- Restart budget: per lineage, 1 restart per rolling 60 minutes and 2 in total. The cause classes are `idle`, `context-exhausted`, `exited` and `unreachable-then-exited`; the same class twice means no plain restart. For `context-exhausted`, the next Task reduces the load (splits the `Command:` lines or narrows the inputs), or the coordinator goes to L5.
+
+The nudge, typed with `--wait-submit` and its receipt logged:
+
+```text
+[coordinator liveness check <UTC time>] If a step is running, ignore this and continue. If your turn ended before worker_done, continue with your next Command: line now. If all Command: lines are done, send worker_done per WC-5. Do not restart finished steps.
+```
+
+**The resume note.** An L4 restart puts this note in the new Task's brief, after the guard line and before the `Command:` lines. The new Task gets its own report directory; the old one is read-only input. For `/sc:implement`, its own `E-RESUME-NEEDED` re-run takes priority.
+
+```text
+Resume: replaces Task <old task id> (cause: <class>, evidence: <source>@<time>).
+Lineage: <lineage id>, attempt <n>.
+Task ID / Dispatch ID of the replaced attempt: <ids>.
+Completed Command: lines: <n of m>, contracts: <paths>.
+Last progress token: <step>/<counter>.
+Handoff file: <old report-dir>/handoff/<latest>.md (read this first, at most 80 lines at a time).
+Answered message IDs already applied: <ids>.
+Uncertain effects: <actions started but not confirmed, e.g. a push or a message send>; verify before redoing.
+Load rule: read reports and logs in pieces of at most 80 lines; do not reread whole prior reports.
+Start at: Command: line <k>.
+```
+
+**Never on silence.** On silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never:
+
+- stops a worker;
+- creates a retry Task;
+- releases a worker or a worktree;
+- marks a Task failed;
+- answers a permission or person-only prompt;
+- writes or drafts a Ruling;
+- sends a lifecycle message for the worker.
+
+Silence authorizes only L1, L2 and L3.
+
+**Not yet verified.** These points are open; the rules above do not depend on them being true:
+
+- UNVERIFIED: what `check --wait` wakes on when `--types` is not given. The coordinator always lists every type.
+- UNVERIFIED: the cause of case 5, answers a worker did not see. Lead: `orca orchestration reply` stores type `status` with subject "Re: Question", so a waiter with a narrow `--types` list may miss it.
+- UNVERIFIED: whether Orca has an attention category for a permission prompt or for compact thrashing; until it is confirmed, S4 rests on `agentWait` and S6 on screen text read twice. The delay Orca adds before `agentWait` shows a prompt is also unmeasured.
+- UNVERIFIED: what Claude Code does with text typed while a tool call runs; this is why typed text goes only to a positively idle prompt.
+- UNVERIFIED: whether two consumers on one mailbox both get a batch; the coordinator runs one wait per Run inbox.
+
 ### Brief layout
 
 The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. Guard line:
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index a854cf08..1410fc7e 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -195,6 +195,60 @@ RULE_PHRASES = {
             "is logged and shown to the person, never applied",
         ],
     ),
+    "liveness-wait": (
+        None,
+        [
+            "### Liveness supervision",
+            "orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000",
+            "A returned Delivery is the whole FIFO batch, replayed until `--ack`",
+            "writes one run-notes line per message ID before it sends `--ack`",
+            "After three empty waits in a row, the coordinator enumerates its workers with `worker-list`",
+        ],
+    ),
+    "liveness-sweep-and-states": (
+        None,
+        [
+            "at most once every 5 minutes, the coordinator runs one sweep",
+            "A message arrival or a repeated identical read is not one",
+            "| S9 finished but unreported |",
+            "| S10 settled |",
+            "| S11 unknown |",
+        ],
+    ),
+    "liveness-acks": (
+        None,
+        [
+            "The coordinator never resends a mailbox copy of an answer",
+            "type ONE copy into the terminal",
+            "A4, at 15 minutes: L5 report to the person",
+        ],
+    ),
+    "liveness-ladder-and-restart": (
+        None,
+        [
+            "1 per rolling 60 minutes, 2 per lineage",
+            "Nudges, asks, heartbeats, repeated identical reads and context exhaustion are never stall proofs",
+            "the same class twice means no plain restart",
+            "An L4 restart puts this note in the new Task's brief, after the guard line and before the `Command:` lines",
+        ],
+    ),
+    "liveness-never-on-silence": (
+        None,
+        [
+            "On silence, a passed deadline, `unverifiable` liveness or screen text alone, the coordinator never:",
+            "Silence authorizes only L1, L2 and L3.",
+        ],
+    ),
+    "liveness-unverified": (
+        None,
+        [
+            "UNVERIFIED: what `check --wait` wakes on when `--types` is not given",
+            "UNVERIFIED: the cause of case 5, answers a worker did not see",
+            "UNVERIFIED: whether Orca has an attention category for a permission prompt or for compact thrashing",
+            "UNVERIFIED: what Claude Code does with text typed while a tool call runs",
+            "UNVERIFIED: whether two consumers on one mailbox both get a batch",
+        ],
+    ),
     "brief-contents": (
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
