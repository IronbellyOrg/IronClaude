a2b7328856f54734c952f16ae1f7033f3882fa97
Review one task for spec compliance.

Task brief: ## Task 5: Add the live-attempt settlement bullet to WC-6 (C-15)

In `src/superclaude/core/WORKER-CONTRACT.md` section 4, subsection "WC-6. Every retry is a new Task", add the C-15 bullet from design section 10.2: a live attempt (its terminal still open) settles only when the person directs its cancellation and the coordinator has confirmed quiescence (no tool running, no input accepted, and two reads 5 minutes apart that agree); context exhaustion, heartbeats and the coordinator's own nudges are not stall proofs; a message from a settled or replaced attempt is logged and shown to the person, never applied. Add a pin.

Acceptance criteria (ids T5.AC1, T5.AC2 in order):
- T5.AC1: The WC-6 list holds the new bullet and the four existing WC-6 phrases still pass.
- T5.AC2: A pin covers "person directs its cancellation" and "never applied".
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
Start sha: a2b7328856f54734c952f16ae1f7033f3882fa97
Diff against the start snapshot:
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 83c81298..5b5d3532 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -76,6 +76,7 @@ A Task's brief cannot change after creation (Orca's `task-update` changes only `
 - No retry while the earlier attempt is not settled or reads `unverifiable`: absence never authorizes a retry.
 - A crashed or stalled attempt is settled by the coordinator: after Orca's positive stall proof it stops the worker and sets the old Task `failed --result cancelled` before creating the new Task.
 - A follow-up `send --to dispatch:<id>` is not used to carry a retry's new brief: the Dispatch ID is known only after `worker-start` returns ready, by which time a Claude worker has already received its task on the command line, so the message could arrive after the command started.
+- A live attempt (its terminal still open) settles only when the person directs its cancellation and the coordinator has confirmed quiescence: no tool running, no input accepted, and two reads 5 minutes apart that agree. Context exhaustion, heartbeats and the coordinator's own nudges are not stall proofs. A message from a settled or replaced attempt is logged and shown to the person, never applied.
 
 ### What the coordinator owes each worker
 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index 8c0c4cde..a854cf08 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -186,6 +186,15 @@ RULE_PHRASES = {
             "A crashed or stalled attempt is settled by the coordinator",
         ],
     ),
+    "wc6-live-attempt-settlement": (
+        None,
+        [
+            "settles only when the person directs its cancellation and the coordinator has confirmed quiescence",
+            "two reads 5 minutes apart that agree",
+            "Context exhaustion, heartbeats and the coordinator's own nudges are not stall proofs",
+            "is logged and shown to the person, never applied",
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
