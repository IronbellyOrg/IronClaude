89cbdcba9b3f9256b64736f71038a6778a042afd
Review one task for spec compliance.

Task brief: ## Task 4: Update the ledger Ruling line rules and examples

Depends on: Task 3

Edit src/superclaude/skills/sc-implement-protocol/refs/ledger.md: the heading and prose of "Ruling line (user-authorized, executor-recorded)" (lines 62-72), the post-ruling complete line prose (lines 74-82) only where it says who confirms, and the examples at lines 193-199. Keep the three-field grammar `T<id>: Ruling: <what> — <why> — <cost-if-wrong>` and the regular expression unchanged. Say the `<what>` field carries the provenance: the person's quoted chat words, or the dashboard answer row id. Add one example of a dashboard-provenance Ruling line that matches the regular expression.

Acceptance criteria:
- The regular expression in ledger.md is byte-identical to before.
- The new dashboard example line matches that regular expression (check by running the regular expression over the example with uv run python -c in a throwaway command; record the result in the final report).
- ledger.md names both channels and does not let a coordinator relay count.
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 89cbdcba9b3f9256b64736f71038a6778a042afd
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/ledger.md b/src/superclaude/skills/sc-implement-protocol/refs/ledger.md
index 00a4efd7b..ba2c47ce8 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/ledger.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/ledger.md
@@ -65,7 +65,7 @@ T<id>: <status> verdict=<verdict> ac=<ac-list> evidence=<ev-list> extras=lint:<l
 T<id>: Ruling: <what> — <why> — <cost-if-wrong>
 ```
 
-Em dashes as shown. Three non-empty fields. On clear user confirmation the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`.
+Em dashes as shown. Three non-empty fields. On a clear confirmation by the user through a chat message or a dashboard response (the two channels `~/.claude/WORKER-CONTRACT.md` defines in WC-3; the dashboard channel applies only once the dashboard answer path is released) the executor MUST automatically append this line; the confirmation gate is the Halt table in `refs/qa.md`. The `<what>` field carries the provenance: the user's quoted chat words, or the dashboard answer row id. A coordinator's reply or relay is never the provenance.
 
 ```
 ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$
@@ -196,6 +196,12 @@ Executor-recorded Ruling after the explained scope, reason and cost, followed by
 T2: Ruling: accept T2 missing pagination; user confirmed in current conversation "yes, accept T2 as explained" — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated
 ```
 
+The same Ruling recorded from a dashboard response (the answer row and its question id are the provenance; applies once the dashboard answer path is released):
+
+```
+T2: Ruling: accept T2 missing pagination; user confirmed by dashboard answer row ans_0000042 (question q_0000017) — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated
+```
+
 The earlier operator-written form (`T2: Ruling: drop pagination — AC-2 deferred to next spec — cost-if-wrong: list stays unpaginated`) remains valid.
 
 Retry open:

--- new untracked file .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t4-regex.log ---
MATCH T2: Ruling: accept T2 missing pagination; user confirmed in current conversation "yes, acc
MATCH T2: Ruling: accept T2 missing pagination; user confirmed by dashboard answer row ans_00000
ruling examples: 2; all match: True



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (the target is Markdown, which codegraph does not index).
Dependents not in this diff (context only): scripts/archive_workspace.py line 54 holds the Ruling regex (not edited, follow-up); tests/skills/test_implement_severity_static.py allow-list (Task 7); the plugin copy refs/ledger.md (Task 6). The regex check output is at .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t4-regex.log.

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
