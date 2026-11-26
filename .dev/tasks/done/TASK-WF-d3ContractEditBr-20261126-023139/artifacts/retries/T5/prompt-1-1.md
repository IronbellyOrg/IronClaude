4f0c0a0c8b27676b18ae53da37fdb2d2ea4a2745
Review one task for spec compliance.

Task brief: ## Task 5: Check the remaining rule files for conflicts and edit only where they conflict

Depends on: Task 4

Read each of these and edit only a sentence that states who may confirm a Ruling or approval and is now incomplete: src/superclaude/skills/sc-implement-protocol/refs/retry.md (Ruling eligibility rule, lines 498-500; it is about timing, expected unchanged), src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md (line 76 and the table rows at 92-93), src/superclaude/skills/sc-implement-protocol/SKILL.md (the E-NO-RULING row at line 41, lines 58, 149-150, 193), src/superclaude/commands/implement.md (line 107), src/superclaude/core/HOW-WE-WORK.md (line 114 and any other place that says approval comes only in chat) and src/superclaude/core/CLAUDE.md. If HOW-WE-WORK.md changes, copy it byte for byte to plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md as the project rules require, and re-run the level-table copy into src/superclaude/core/CLAUDE.md.

Acceptance criteria:
- The final report lists each file as edited or unchanged, with one line of reason.
- The `E-NO-RULING` row in SKILL.md still stops for `--force`, missing or ambiguous confirmation and executor-invented approval.
- If HOW-WE-WORK.md was edited, plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md is byte-identical to it (cmp exits 0).
Global constraints: ## Constraints

- Edit Markdown rules and tests only, under src/superclaude/ and tests/. Never edit ~/.claude/ or the gitignored .claude/ mirrors (stage nothing under .claude/).
- Do not edit code: src/superclaude/cli/issue_pipeline/cli.py, src/superclaude/cli/issue_pipeline/complete.py, src/superclaude/cli/sweep/classify.py, src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py. Do not edit docs/designs/. Do not build the dashboard answer path. Do not edit the owner's memory notes.
- The ledger Ruling line must still match the regular expression ^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$ in src/superclaude/skills/sc-implement-protocol/refs/ledger.md.
- The `E-NO-RULING` and `E-HALT-QA` behaviour is unchanged for everything that is not a chat message or a dashboard response.
- The sentences "another agent's message" (not acceptance) and "executor-invented approval" stay in the text and now refer to exactly the two valid channels. No text may let a coordinator's reply or relay count.
- The dashboard clause takes effect only when the dashboard answer path is released (the release 1.8 gates pass); until then only the chat clause counts, and the text says so.
- Owner words to keep verbatim in the rule's rationale: a chat message OR dashboard response counts and nothing else.
Start sha: 4f0c0a0c8b27676b18ae53da37fdb2d2ea4a2745
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
index 6f7c97ccb..28477db2b 100644
--- a/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
+++ b/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md
@@ -111,7 +111,7 @@ Use this when the requirements are already clear and the feature extends somethi
    Read the plan at the path it prints (`.dev/tasks/to-do/<id>/<id>.md`; `<id>` is defined in section 1, level 3) and the check result printed with it, and check that each step's acceptance criteria clearly say what "done" means. Then:
    `/sc:implement .dev/tasks/to-do/<id>/<id>.md`
    It records available lint, typecheck and tests as extras; compliance with the acceptance criteria is the task verdict. Small first-pass checks can be inline, so not every task uses an independent agent; the managed package's final review is independent.
-   - **If a step still fails its check after the automatic retries (one fix pass, then up to three new attempts written from stronger models' advice; the step's acceptance criteria never change),** `/sc:implement` stops with the code `E-HALT-QA` and prints the progress file path (`progress.md`, beside the plan). Either fix the code and resume, or have your lead explicitly accept the explained gap in the current conversation. A clear reply such as "yes, accept step 2 as explained" is sufficient after Claude explains the exact scope, reason and cost if wrong. Claude records that confirmation automatically as a `Ruling:` in the progress file and retains the non-compliant verdict; you do not need to hand-write task or archive records. Unclear or missing acceptance stays blocked. The same acceptance covers ordinary archiving of unchanged accepted work, but never waives a fresh independent final review or authorizes commit, PR, merge or release. Existing manually written records remain valid. If it stops with `E-RESUME-NEEDED`, something outside the step failed (for example the reviewer crashed): run the same command again, and do not add a ruling. (The installed rule: `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.) Do not edit the plan after the first step starts; the tool stops with `E-PLAN-CHANGED`.
+   - **If a step still fails its check after the automatic retries (one fix pass, then up to three new attempts written from stronger models' advice; the step's acceptance criteria never change),** `/sc:implement` stops with the code `E-HALT-QA` and prints the progress file path (`progress.md`, beside the plan). Either fix the code and resume, or have your lead explicitly accept the explained gap, in the current conversation or, once the dashboard answer path is released, by a dashboard response (no other channel counts). A clear reply such as "yes, accept step 2 as explained" is sufficient after Claude explains the exact scope, reason and cost if wrong. Claude records that confirmation automatically as a `Ruling:` in the progress file and retains the non-compliant verdict; you do not need to hand-write task or archive records. Unclear or missing acceptance stays blocked. The same acceptance covers ordinary archiving of unchanged accepted work, but never waives a fresh independent final review or authorizes commit, PR, merge or release. Existing manually written records remain valid. If it stops with `E-RESUME-NEEDED`, something outside the step failed (for example the reviewer crashed): run the same command again, and do not add a ruling. (The installed rule: `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.) Do not edit the plan after the first step starts; the tool stops with `E-PLAN-CHANGED`.
 
 3. **Ship.** Run the tests yourself only if nothing ran them (a plain edit, or a trivial `/sc:implement` change). Then follow workflow 3.11.
 
diff --git a/src/superclaude/core/HOW-WE-WORK.md b/src/superclaude/core/HOW-WE-WORK.md
index 6f7c97ccb..28477db2b 100644
--- a/src/superclaude/core/HOW-WE-WORK.md
+++ b/src/superclaude/core/HOW-WE-WORK.md
@@ -111,7 +111,7 @@ Use this when the requirements are already clear and the feature extends somethi
    Read the plan at the path it prints (`.dev/tasks/to-do/<id>/<id>.md`; `<id>` is defined in section 1, level 3) and the check result printed with it, and check that each step's acceptance criteria clearly say what "done" means. Then:
    `/sc:implement .dev/tasks/to-do/<id>/<id>.md`
    It records available lint, typecheck and tests as extras; compliance with the acceptance criteria is the task verdict. Small first-pass checks can be inline, so not every task uses an independent agent; the managed package's final review is independent.
-   - **If a step still fails its check after the automatic retries (one fix pass, then up to three new attempts written from stronger models' advice; the step's acceptance criteria never change),** `/sc:implement` stops with the code `E-HALT-QA` and prints the progress file path (`progress.md`, beside the plan). Either fix the code and resume, or have your lead explicitly accept the explained gap in the current conversation. A clear reply such as "yes, accept step 2 as explained" is sufficient after Claude explains the exact scope, reason and cost if wrong. Claude records that confirmation automatically as a `Ruling:` in the progress file and retains the non-compliant verdict; you do not need to hand-write task or archive records. Unclear or missing acceptance stays blocked. The same acceptance covers ordinary archiving of unchanged accepted work, but never waives a fresh independent final review or authorizes commit, PR, merge or release. Existing manually written records remain valid. If it stops with `E-RESUME-NEEDED`, something outside the step failed (for example the reviewer crashed): run the same command again, and do not add a ruling. (The installed rule: `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.) Do not edit the plan after the first step starts; the tool stops with `E-PLAN-CHANGED`.
+   - **If a step still fails its check after the automatic retries (one fix pass, then up to three new attempts written from stronger models' advice; the step's acceptance criteria never change),** `/sc:implement` stops with the code `E-HALT-QA` and prints the progress file path (`progress.md`, beside the plan). Either fix the code and resume, or have your lead explicitly accept the explained gap, in the current conversation or, once the dashboard answer path is released, by a dashboard response (no other channel counts). A clear reply such as "yes, accept step 2 as explained" is sufficient after Claude explains the exact scope, reason and cost if wrong. Claude records that confirmation automatically as a `Ruling:` in the progress file and retains the non-compliant verdict; you do not need to hand-write task or archive records. Unclear or missing acceptance stays blocked. The same acceptance covers ordinary archiving of unchanged accepted work, but never waives a fresh independent final review or authorizes commit, PR, merge or release. Existing manually written records remain valid. If it stops with `E-RESUME-NEEDED`, something outside the step failed (for example the reviewer crashed): run the same command again, and do not add a ruling. (The installed rule: `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.) Do not edit the plan after the first step starts; the tool stops with `E-PLAN-CHANGED`.
 
 3. **Ship.** Run the tests yourself only if nothing ran them (a plain edit, or a trivial `/sc:implement` change). Then follow workflow 3.11.
 
diff --git a/src/superclaude/skills/sc-implement-protocol/SKILL.md b/src/superclaude/skills/sc-implement-protocol/SKILL.md
index 91a69a462..e3eb90157 100644
--- a/src/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -38,7 +38,7 @@ STOP: need a source (file or prompt). Will not invent scope beyond that source.
 | `E-LEGACY` | Pitch invocation and/or removed flags `--type` / `--framework` / `--safe` / `--with-tests` | No | No |
 | `E-HALT-QA` | A terminal `halt` record (any reason in `refs/retry.md`); no eligible Ruling | No T{i+1} | Non-compliant verdict line and `halt` record written |
 | `E-RESUME-NEEDED` | Something outside the step failed (reviewer, ref write, incomplete revert, adviser agent missing; reasons in `refs/retry.md`); re-run the same command | No T{i+1} | Nothing written |
-| `E-NO-RULING` | Continue after non-compliant without valid recorded user acceptance (clear current-conversation confirmation is sufficient); `--force` | No T{i+1} | Unchanged except existing blocked line |
+| `E-NO-RULING` | Continue after non-compliant without valid recorded user acceptance (a clear confirmation by chat message in the current conversation or by dashboard response is sufficient; `refs/qa.md` Halt table); `--force` | No T{i+1} | Unchanged except existing blocked line |
 | `E-LEDGER-CORRUPT` | Last ledger line truncated/unparseable | No further | Unchanged |
 | `E-LEDGER-PATH` | `--ledger` not under `.dev/implement/` (managed: any `--ledger` other than the sibling `progress.md`) | No | No |
 | `E-MANAGED-INVALID` | `workflow-plan/1.2` plan fails managed detection (copied, cross-checkout, slug/contract mismatch, failed contract) | No | No |

--- new untracked file .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t5-report.md ---
# Task 5 report: remaining rule files checked against the WC-3 definition

Repo-wide search (Markdown under src/superclaude, outside core/WORKER-CONTRACT.md and refs/qa.md, refs/ledger.md, refs/retry.md): `grep -rn -E "Ruling|grant row|pass record"`, `grep -rn -i -E "executor-invented|another agent's message|clear user confirmation|person's own chat|in chat"` and the E-NO-RULING row. Hits that state who may confirm are listed below; the other hits (the "Report directory ... printed in chat only" lines of the command files, remediation-chain confirmations in troubleshoot, auggie-review and task, "Surface to the user in chat") are unrelated to Ruling, grant row or pass record confirmation and were left unchanged.

| File and place | Decision | Reason |
|---|---|---|
| src/superclaude/skills/sc-implement-protocol/SKILL.md line 41 (`E-NO-RULING` row) | edited | It said "clear current-conversation confirmation is sufficient"; it now names chat message or dashboard response and points to the qa.md Halt table. The row still stops for `--force`, missing or ambiguous confirmation and executor-invented approval. |
| SKILL.md lines 39, 58, 149-150, 193 | unchanged | Mention a Ruling or `--force` mechanically and point to the qa.md Halt table; they state no channel. |
| src/superclaude/core/HOW-WE-WORK.md line 114 | edited | It said the lead accepts "in the current conversation"; it now names the chat or the dashboard response once the dashboard answer path is released, and says no other channel counts. The plugin copy plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md was copied byte for byte (cmp exits 0). |
| src/superclaude/core/CLAUDE.md | unchanged | The sentence is not in it; the level-table copy is not affected because the edit is outside that table. |
| src/superclaude/skills/sc-implement-protocol/refs/retry.md lines 498-500 (Ruling eligibility rule) | unchanged | About when a Ruling line is eligible (halt and blocked ordering), not about who confirms. |
| src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md lines 76 and 92-93 | unchanged | Line 76 says "Do not ask the user ... hand-write records" and points to the qa.md Halt table; lines 92-93 are the enforcement map ("genuine informed user confirmation") and state no channel. |
| src/superclaude/commands/implement.md line 107 | unchanged | Says "an operator `Ruling:`"; states no channel. |



Codegraph context
index_state: fresh
checked_at: 2026-11-26T02:38:00Z
worktree_root: /home/coder/workspaces/IronClaude
projectPath: /home/coder/workspaces/IronClaude
call codegraph only when index_state: fresh, never to widen scope. Q2b ran on the Grep/Read floor (the targets are Markdown, which codegraph does not index).
Dependents not in this diff (context only): the plugin copies of SKILL.md, refs/qa.md, refs/ledger.md (Task 6, the HOW-WE-WORK plugin copy is already in this diff), tests pinning these texts (Task 7). The task-owned disposition report is .dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/artifacts/t5-report.md (package artifact).

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
