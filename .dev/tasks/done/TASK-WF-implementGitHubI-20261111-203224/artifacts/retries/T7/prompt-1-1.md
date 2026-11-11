bbe2950e84824e65c9e1ba3a0411a7e6fab843fb
Review one task for spec compliance.

Task brief: 
## Task 7: Update the pins that required the stale P0 text

Depends on: Task 4

In `tests/skills/test_worker_contract.py` edit `RULE_PHRASES`: delete the `"WC-5-P0-override"` entry (lines 144-149); in `"brief-contents"` (lines 255-261) delete the phrase "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)" and keep the other phrase; in `"brief-template"` (lines 360-367) replace the two P0 phrases (`'\`--report-dir\` is marked "from P1": no command accepts it at P0'` and `"P0 only: Report file: <the command's report file under AC-0.4>."`) with phrases that exist in the rewritten contract: the heading `## 5. Coordinator brief template` stays, plus the `Command: /sc:<name> <arguments> --unattended` template prefix. Also update the pins at lines 58-78 if Task 1's wording requires adding the repair clauses as extra phrases (keep each original phrase). If any other test in this file reads the deleted text, fix it the same way. Do not change `UNATTENDED_EXPECT`, `P1_COMMANDS`, `P2_COMMANDS`, `NEVER_AS_WORKER` or the `_p2_bullet` helper.

Acceptance criteria:
- T7.AC1: `grep -n 'P0\|AC-0.4' tests/skills/test_worker_contract.py` prints no pin that requires text about P0 in the contract.
- T7.AC2: `uv run pytest tests/skills/test_worker_contract.py -q` passes after Tasks 1 to 4 and this task.

Global constraints: 
## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

Start sha: bbe2950e84824e65c9e1ba3a0411a7e6fab843fb
Diff against the start snapshot: 
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index f58212232..6b2631a9d 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -141,12 +141,6 @@ RULE_PHRASES = {
             "`--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists"
         ],
     ),
-    "WC-5-P0-override": (
-        "WC-5",
-        [
-            "a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task"
-        ],
-    ),
     "WC-7": ("WC-7", ["Run at the top level, never inside a subagent"]),
     "WC-12": (
         "WC-12",
@@ -256,7 +250,6 @@ RULE_PHRASES = {
         None,
         [
             "The contract only works if the brief carries what the command would otherwise ask a person",
-            "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)",
         ],
     ),
     "brief-layout": (None, ["so the Task text never starts with `/sc:`"]),
@@ -361,8 +354,7 @@ RULE_PHRASES = {
         None,
         [
             "## 5. Coordinator brief template",
-            '`--report-dir` is marked "from P1": no command accepts it at P0',
-            "P0 only: Report file: <the command's report file under AC-0.4>.",
+            "Command: /sc:<name> <arguments> --unattended",
         ],
     ),
     "brief-chain-line": (


Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (empty)

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
