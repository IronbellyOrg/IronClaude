c38fa8fd61b1dfee3fcbec094ca813cc518d4fd0
Review one task for spec compliance.

Task brief: ## Task 3: Reword the stale primary-ladder text at lines 168 to 172 of the source retry.md

Depends on: Task 1

Lines 168 to 172 of `src/superclaude/skills/sc-implement-protocol/refs/retry.md` (the `advice-3-b.md` bullet, the bullet that starts "Every GPT adviser at any escalation is a T1 model.", and the paragraph that starts "Escalation 2 = 2 advisers on the top rung, always.") name `T1Model01` as the GPT T1 model and call an executor on `T2Model02` a Claude executor. In the workspace values listed under Constraints `T1Model01` is a Claude id, `T1Model02` is a GPT id and `T2Model02` is not a Claude model, so both statements are wrong.

First write the draft replacement wording of the changed sentences to `./artifacts/t3-wording.md` (package-relative evidence file), then apply it to `retry.md`. The rewording must follow these rules.
- Pick the GPT T1 model by the prefix rule already stated in the `advice-3-b.md` bullet (the id of `T1Model01`, else `T1Model02`, that starts with `gpt-`), and describe executors and picks by the family of the id (`claude-` or `gpt-`) and by rung position, not by a fixed variable name.
- Keep the escalation structure exactly as it is: adviser A is one rung up in the executor's own family (the top rung when the executor is on top or its tier is unknown), adviser B is from the other family, escalation 2 is two advisers on the top rung; add no spawn and no new rule.
- The reworded lines 168 to 172 contain this sentence word for word (M-1): "Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`." Task 6 embeds it as a literal; `./artifacts/t3-wording.md` is evidence only and no test reads it.
- Keep the lead-in "Worked example with the fallback ladder:" as the last words before the table, keep the four rung names reachable in the section (line 162 already holds them), and do not touch the sentence about `T2Model01` being recognized only as a match for the executor.
- The new text obeys every constraint above (no `halt`, `Ruling`, `claude-gw-tier`, no new line starting with `GPT spawn path: `).

Acceptance criteria:
- No sentence in `retry.md` lines 168 to 172 equates `T1Model01` with a GPT model or an executor on `T2Model02` with a Claude executor; the phrases "an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02`" and "adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it" no longer appear.
- The reworded example describes adviser picks by family and rung position and contains the sentence from the rules above exactly once (M-1).
- `./artifacts/t3-wording.md` exists and holds the draft text that was applied.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_model_alias_policy.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py -q` passes.
AC ids in source order (the bullets under Acceptance criteria): T3.AC1 T3.AC2 T3.AC3 T3.AC4
Global constraints: ## Constraints

- Scope: change only the files named in the tasks below (`src/superclaude/skills/sc-implement-protocol/refs/retry.md`, `src/superclaude/skills/sc-implement-protocol/SKILL.md`, their two copies under `plugins/superclaude/skills/sc-implement-protocol/`, `tests/skills/test_task_workspace_lifecycle.py` and the new `tests/skills/test_implement_launch_alias.py`). Edit nothing under `.claude/` or `.dev/issues/`.
- The rule being written: on the fallback ladder the Agent call's `model` is the rung's own alias; on the primary ladder it is `opus` for every adviser (adviser A, adviser B, the critique adviser and both escalation-2 advisers); an adviser whose picked id does not start with `claude-` is still launched on `opus` and its line 1 carries `family-fallback: <reason>`; this never STOPs and never prompts the user.
- The new text in `retry.md` must not start any line with `GPT spawn path: ` (a test requires exactly one such line, at the pinned line 183), and must keep the backticked phrase `family-fallback: <reason>` and the phrase "never STOPs and never prompts the user" (`tests/skills/test_implement_adviser_family.py`, lines 73 to 85).
- The new text must not contain the words `halt`, `Ruling` or `E-HALT-QA` outside the lines a test already allow-lists (`tests/skills/test_implement_severity_static.py`, lines 296 to 299 and 420 to 434), must not contain the string `claude-gw-tier` (`tests/skills/test_model_alias_policy.py`, lines 104 to 119), and must not put a full model id after `--model` or `--models` (same file, lines 164 to 173).
- The new text must not add a fenced block containing a line that begins with `T` and a digit and has no angle bracket (`tests/skills/test_implement_severity_static.py`, lines 225 to 250), and must not add a table row whose first cell is a backticked lowercase key and whose last cell is only the digits 2 to 5 (`tests/skills/test_workflow_archive.py`, lines 1042 to 1076).
- `retry.md` must keep the four rung names `T2bModel01`, `T2Model02`, `T1Model02` and `T1Model01`, and must not contain any `T`-digit-underscore-`Model` spelling (`tests/skills/test_model_alias_policy.py`, lines 219 to 228).
- Add no flag, no stop reason, no halt reason and no extra adviser spawn (the cap of six stays); do not change the `tier=` ledger token (its value class is letters, digits and underscore) or `src/superclaude/skills/sc-implement-protocol/refs/ledger.md`.
- In table cells and prose copied from the existing worked table, use the multiplication sign `×` and not the letter `x` (the pinned test rows use `1×`).
- Out of scope, separate defects: the executor-tier tie when `T2Model01` and `T1Model02` hold the same id, and family inference from gateway ids such as `claude-gw-tier2`.
- Decided for this work (iteration 3): nothing to decide; build what the issue asks for, within its own scope.
- Observed workspace values the wording must stay true to: `T2bModel01` is `gpt-6.1-terra`, `T2Model02` is `glm-5.3`, `T1Model02` is `gpt-6.1-sol`, `T1Model01` is `claude-opus-5-5`; the three aliases `opus`, `sonnet` and `haiku` resolve to tier ids through `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` and `ANTHROPIC_DEFAULT_HAIKU_MODEL`.
Start sha: c38fa8fd61b1dfee3fcbec094ca813cc518d4fd0
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/retry.md b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
index a66241dbd..d215f4257 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -166,10 +166,10 @@ A repair is a local, in-place fix of confirmed blockers that runs after a failed
 **Escalation rule.** Escalation 1 always spawns two advisers in one message, never one, from different model families. The family is read from the model id with any trailing `[...]` suffix stripped: a `claude-` prefix is Claude, a `gpt-` prefix is GPT.
 - `advice-3-a.md`: the executor's own model family, one rung up the active ladder; the top rung when the executor is already on the top rung or its tier is unknown.
 - `advice-3-b.md`: the other model family. Executor is Claude: adviser B is a GPT model on T1, meaning the id of `T1Model01`, else `T1Model02`, that starts with `gpt-`. Executor is GPT: adviser B is the Claude top rung (`opus` when it resolves to a `claude-` id). Executor is neither family or unknown: adviser A uses the top rung, and adviser B uses whichever of the Claude top rung and the GPT T1 model is not adviser A's family.
-- Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it, else `T1Model02`, else the same T1 model).
+- Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model: the first T1 id (the id of `T1Model01`, else `T1Model02`) that starts with `gpt-` and is not the executor's own id, else the same T1 model.
 - The pick uses the two-answer rule of procedure step 4 (a tie goes to `-a`); the critique adviser uses adviser A's model.
 
-Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claude executor): an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02` and adviser B on the GPT T1 model, then 2 on `T1Model01`; on `T1Model02`, adviser A on `T1Model01`. A GPT executor on `T2bModel01` (rung 0) gets adviser A on the GPT T1 model (`T1Model01`) and adviser B on the Claude top rung, then 2 on `T1Model01`. Worked example with the fallback ladder:
+Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example, described by the family of each id and by rung position: an executor whose id starts with neither `claude-` nor `gpt-` gets adviser A on the top rung and adviser B on whichever of the Claude top rung and the GPT T1 model is not adviser A's family; a Claude executor below the top rung gets adviser A one Claude rung up and adviser B on the GPT T1 model; a GPT executor gets adviser A on the GPT T1 model and adviser B on the Claude top rung; escalation 2 is then 2 on the top rung in each case. Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`. Worked example with the fallback ladder:
 
 | Executor tier | Escalation 1 (A3), adviser A | Escalation 1 (A3), adviser B | Escalation 2 (A4) |
 |---|---|---|---|
new file .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/t3-wording.md (full contents):
+++ b/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-051505/artifacts/t3-wording.md
@@ -0,0 +1,25 @@
+# Task 3 draft wording (evidence only; no test reads this file)
+
+Applied to `src/superclaude/skills/sc-implement-protocol/refs/retry.md`, lines 168 to 172 of the pre-change file. The `advice-3-b.md` bullet (line 168) already states the prefix rule correctly and is left as it is. Two blocks change: the "Every GPT adviser" bullet (line 169) and the "Escalation 2" paragraph (line 172).
+
+## Replacement for the bullet at line 169
+
+- Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model: the first T1 id (the id of `T1Model01`, else `T1Model02`) that starts with `gpt-` and is not the executor's own id, else the same T1 model.
+
+Why this wording: the old bullet gave "`T1Model01` when the executor is not already on it, else `T1Model02`, else the same T1 model", which equates `T1Model01` with a GPT model. In the observed workspace `T1Model01` is a Claude id and `T1Model02` is the GPT id. The new bullet keeps the same selection order and the same fallback to the same model, but picks by the `gpt-` prefix rule of the `advice-3-b.md` bullet instead of by variable name.
+
+## Replacement for the paragraph at line 172
+
+Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example, described by the family of each id and by rung position: an executor whose id starts with neither `claude-` nor `gpt-` gets adviser A on the top rung and adviser B on whichever of the Claude top rung and the GPT T1 model is not adviser A's family; a Claude executor below the top rung gets adviser A one Claude rung up and adviser B on the GPT T1 model; a GPT executor gets adviser A on the GPT T1 model and adviser B on the Claude top rung; escalation 2 is then 2 on the top rung in each case. Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`. Worked example with the fallback ladder:
+
+Why this wording: the old example called an executor on `T2Model02` a Claude executor and named `T1Model01` as the GPT T1 model. In the observed workspace `T2Model02` is neither family and `T1Model01` is a Claude id. The new example follows the escalation structure of lines 167 and 168 unchanged (adviser A one rung up in the executor's family, or the top rung when the executor is on top, neither-family or unknown; adviser B from the other family; escalation 2 on the top rung), adds no spawn and no rule, and states the launch rule once with the exact sentence the plan requires.
+
+## Rules check
+
+| Rule | Where met |
+|---|---|
+| GPT T1 model picked by the prefix rule; executors and picks described by family and rung position, not a fixed variable name | bullet at line 169 (prefix rule, no variable named as the executor's rung); paragraph at line 172 (no executor named by variable) |
+| Escalation structure unchanged; no new spawn or rule | paragraph keeps A one rung up in the executor's family (top rung when on top, neither-family or unknown), B from the other family, escalation 2 on the top rung |
+| The exact sentence, once | paragraph at line 172: "Every adviser on the primary ladder is launched on `opus`, and a pick whose id does not start with `claude-` carries `family-fallback`." |
+| Lead-in kept as the last words before the table; the four rung names reachable; the `T2Model01` sentence untouched | paragraph ends "Worked example with the fallback ladder:"; line 162 untouched |
+| No `halt`, `Ruling`, `claude-gw-tier`, no new line starting `GPT spawn path: `, no model-id literal | none present in the new text |
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
