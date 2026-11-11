54239f709c0c7ed5da8bd88d75e582ba9323f2b7
Review one task for spec compliance.

Task brief: ## Task 4: Carry the run state in the reviewer and final-review prompts

Edit `src/superclaude/skills/sc-implement-protocol/refs/qa.md`. Do not edit the closed reviewer template fenced block or its seven slots. In the "Slot sources" list change the `{diff}` entry so the slot content is the Q3 diff followed, when Q2b produced rows or the run state is not fresh, by a `Codegraph context` block. The block starts with the four run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath`, then the standing line `call codegraph only when index_state: fresh, never to widen scope`, then the Q2b dependents not in the diff (or the note that Q2b ran on the Grep/Read floor). State that the block is context only: a dependent becomes a finding only through the existing checklist, with its own anchor, and an unreached dependent that no AC or quoted constraint requires is not blocking. In the "Managed FINAL review (archive gate)" paragraph add that the FINAL prompt carries the same four run-state fields. State once that saved prompts keep line 1 as the start sha, that the block sits inside the `{diff}` slot content, and that the saved-prompt comparison with the template is therefore unchanged.

Acceptance criteria:
- The fenced reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` is byte-identical to before and `tests/skills/test_implement_severity_static.py::test_ac02_one_closed_reviewer_template_with_seven_slots` passes.
- The `{diff}` slot-source text names the `Codegraph context` block with `index_state`, `checked_at`, `worktree_root` and `projectPath`, the standing codegraph-only-when-fresh line, and the Q2b dependents list; it says the block is context only and adds no new blocking trigger.
- The managed FINAL paragraph states the FINAL prompt carries the four run-state fields, and the saved-prompt rule text states the comparison is unchanged because the block sits inside a slot.


AC ids, in source order of the Acceptance criteria bullets: T4.AC1 (first bullet), T4.AC2 (second bullet), T4.AC3 (third bullet).
Global constraints: ## Constraints

- Keep every flag, STOP code, ledger line format, evidence token, QA severity model (blocking, minor, note, the four checklist answers, the verdict order), retry ladder and managed-package rule of /sc:implement. Add no new `E-*` code.
- The reviewer template in `src/superclaude/skills/sc-implement-protocol/refs/qa.md` stays closed with exactly seven slots (task_brief, global_constraints, diff, start_sha, prior_findings, delta_diff, recheck_list); codegraph context reaches the reviewer only through the content of the existing `{diff}` slot.
- Graph notes never go into the ledger notes file (it would add a `notes@` token and change the inline-review rule); they go to one run file named `codegraph.md` in the ledger directory (legacy `.dev/implement/<slug>/codegraph.md`, managed `<pkg>/artifacts/codegraph.md`).
- Installed primitives never tell an agent to read a `src/superclaude/...` path; the usage guide is named only as `~/.claude/CODEGRAPH.md`.
- The tool allowlist names exact `mcp__codegraph__codegraph_<tool>` entries, never a wildcard. Never call `codegraph_explore`, `codegraph init`, `codegraph index`, `codegraph sync`, or CLI `codegraph status` while an init or index runs.
- Edit only `src/superclaude/commands/implement.md` and files under `src/superclaude/skills/sc-implement-protocol/`; do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, and do not stage `.claude/`.
Start sha: 54239f709c0c7ed5da8bd88d75e582ba9323f2b7
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/qa.md b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
index af3db5693..72cdff90e 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/qa.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/qa.md
@@ -308,7 +308,7 @@ Residual risk, stated: the FINAL is defence in depth only. Legacy N=1 runs and `
 
 ## Managed FINAL review (archive gate)
 
-Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/` and in `superseded-prompts/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. Procedure: `refs/managed-workspace.md`.
+Same isolation as above: `Do not trust the implementer's report.` One fresh subagent per archive attempt (never inline, even N=1; never reused from an earlier attempt). Input: the current full plan, the full ledger, and the current contents of every delivery file the helper's `--print-state` lists, plus the plan's `## Constraints`. Output: `pass` or `issues` with `path:line` evidence per task AC, taken from the current files and the package's `./artifacts/` logs, not copied from the ledger; reading those logs is the one exception to the Isolation rule above. A per-task `evidence=` line number is a pointer recorded when that task was reviewed, and a later task can move it, so a moved line number alone is never `issues`. `issues` when an AC is unmet at the end state, no evidence for it can be found in the current files or logs, a later change contradicts it, a plan `## Constraints` item is violated, or a log cited on a task's latest `complete` line shows a failure at its outcome line. For a user-accepted gap, verify the current outcome matches the recorded scoped acceptance, cite the unmet AC honestly, and return `issues` for any new or changed unaccepted gap. Never mark unmet AC as met. This pass never rewrites per-task verdicts and is not a code-quality ensemble; the closed per-task verdict grammar is unchanged. The FINAL also reads every brief named by a `retry … step=revert` record and every file in `<retries>/T<id>/` and in `superseded-prompts/`, and judges WHAT against the plan; the forbidden-read rule of the Subagent prompt section never applies to the FINAL. The FINAL prompt also carries the four codegraph run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath` from the Wave 0 check, with the same standing line as the `{diff}` slot block; it calls codegraph only when `index_state: fresh`. Procedure: `refs/managed-workspace.md`.
 
 ## Subagent prompt (when not inline)
 
@@ -358,6 +358,7 @@ Slot sources:
 - `{prior_findings}` holds the earlier blocking finding lines of this `start` byte for byte, never minors or notes. The reviewer marks each `resolved`, `open` or `regressed` and never cites the slot.
 - `{delta_diff}` holds `git diff <previous pinned reviewed tree> -- <touched files>` from A2 on, as context beside the full diff.
 - `{recheck_list}` holds the hit locations of re-run saved probes
+- Codegraph context. When Q2b (`SKILL.md`) produced rows, or the Wave 0 run state is not fresh, the `{diff}` slot content is the Q3 diff followed by a `Codegraph context` block: the four run-state fields `index_state`, `checked_at`, `worktree_root` and `projectPath`, the standing line `call codegraph only when index_state: fresh, never to widen scope`, then the Q2b dependents not in the diff (or the note that Q2b ran on the Grep/Read floor). The block is context only: a dependent becomes a finding only through the four-question checklist with its own anchor, and an unreached dependent that no AC or quoted constraint requires is not blocking. The template and its seven slots are unchanged; a saved prompt keeps the start sha on line 1 and the block sits inside the `{diff}` slot content, so the saved-prompt comparison with the template ("## FINAL derived test") is unchanged.
 
 These are reviewer outputs and parent-run searches, not implementer claims or adviser text; paraphrase is forbidden.
 
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
