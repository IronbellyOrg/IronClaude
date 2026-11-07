a0713762a27cf0b35604e1f64d0fad708570aeff
Review one task for spec compliance.

Task brief: ## Task 7: Add the Chain line to the brief layout and template (C-8), then record the checks

In `src/superclaude/core/WORKER-CONTRACT.md`, add the C-8 line from design section 10.2 to the "Brief layout" subsection right after the guard line fence, and to the section 5 brief template between the guard line and the first `Command:` line:

```text
Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
```

Add a pin for the Chain line. Then run `make sync-dev`, `make verify-sync`, `make lint`, `uv run ruff format --check tests/skills/test_worker_contract.py`, `uv run pytest tests/skills -q` and `uv run pytest tests -q -x` (or the widest suite that runs here), and save each output to `./artifacts/`.

Acceptance criteria (ids T7.AC1, T7.AC2, T7.AC3, T7.AC4 in order):
- T7.AC1: The Chain line appears in "Brief layout" and in the section 5 template, after the guard line and before any `Command:` line, and `_check_guard_before_command` and the brief-layout and brief-template pins still pass.
- T7.AC2: A Chain-line pin passes.
- T7.AC3: `./artifacts/` holds the sync-dev, verify-sync, lint, ruff format, `tests/skills` and wider-suite logs, each ending in a pass; any pre-existing failure outside the two edited files is named in `./artifacts/wider-tests.log` with evidence that it also fails on `master`.
- T7.AC4: A grep for other copies of `WORKER-CONTRACT.md` text under `plugins/` and `src/superclaude/core/HOW-WE-WORK.md` is saved to `./artifacts/copies-check.log` and shows none to update.
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
Start sha: a0713762a27cf0b35604e1f64d0fad708570aeff
Diff against the start snapshot:
diff --git a/src/superclaude/core/WORKER-CONTRACT.md b/src/superclaude/core/WORKER-CONTRACT.md
index 31dabf61..8af2518d 100644
--- a/src/superclaude/core/WORKER-CONTRACT.md
+++ b/src/superclaude/core/WORKER-CONTRACT.md
@@ -207,6 +207,12 @@ The brief puts the preamble-facing instructions and the guard line before the co
 Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
 ```
 
+Chain line, right after the guard line and before the first `Command:` line (C-8):
+
+```text
+Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
+```
+
 The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test, run on the copies the worker will see (the target worktree's project `.claude/commands/sc/` copy and `~/.claude/commands/sc/`), not on its own copy. A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer.
 
 ### Feature worktree and child worktrees
@@ -280,6 +286,7 @@ Copy this template into each Task's spec, one brief per Task, and fill every ang
 
 ```text
 Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".
+Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).
 On a blocked gate: report blocked
 Local commit: not authorized
 Report directory: <directory unique to this Task>
diff --git a/tests/skills/test_worker_contract.py b/tests/skills/test_worker_contract.py
index a4d79d88..3f96684d 100644
--- a/tests/skills/test_worker_contract.py
+++ b/tests/skills/test_worker_contract.py
@@ -363,6 +363,12 @@ RULE_PHRASES = {
             "P0 only: Report file: <the command's report file under AC-0.4>.",
         ],
     ),
+    "brief-chain-line": (
+        None,
+        [
+            "Chain: run every Command: line in one turn without stopping between them (WC-14); write a handoff file after each (WC-15); send ack lines for coordinator answers (WC-12).",
+        ],
+    ),
 }
 
 GUARD_LINE = (
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
