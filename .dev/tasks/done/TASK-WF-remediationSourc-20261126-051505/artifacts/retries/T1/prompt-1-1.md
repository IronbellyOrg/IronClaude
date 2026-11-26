f6c9da0750a8d24b9e494050e2e1be449b8651c9
Review one task for spec compliance.

Task brief: ## Task 1: Add the Launch alias paragraph, the header grammar and the family-scope sentence to the source retry.md

In `src/superclaude/skills/sc-implement-protocol/refs/retry.md`, inside the `### Model ladder` section (it ends where `### Cost and caps` begins), make these edits and nothing else in this task.

- Keep the sentence "The adviser's effort is pinned by `effort:` in its agent file; do not rely on any per-call effort setting." and delete the sentence that follows it on the same line ("The model tier comes from the Agent call's `model` parameter."). On the next line, after a blank line, add the paragraph below. It sits after the pinned `GPT spawn path: none verified; family-fallback applies` line.
- In the paragraph that starts `**Resolving adviser B.**`, replace the words "the strongest reachable model" with `opus`, and replace "writes it on line 1 of `advice-3-b.md`: `model: <id> family: <claude|gpt> rung: <T1|top>`" with "writes it on line 1 of `advice-3-b.md` in the header form given under Launch alias below". Keep the backticked `family-fallback: <reason>` phrase, the sentence "the final summary lists every such fallback", the sentence "This never STOPs and never prompts the user: a missing model is configuration, not a finding." and the closing words "The verified spawn path for a GPT T1 model on this install:".

Text of the new paragraph (adjust only wording that would break a constraint above):

```text
**Launch alias.** The Agent call's `model` takes only `opus`, `sonnet`, `haiku` or `fable`, never a full model id or the value of a rung variable, so the rung id decides which adviser is picked and is not passed to the call. On the fallback ladder the call's `model` is the rung's own alias. On the primary ladder the call's `model` is `opus` for every adviser: adviser A, adviser B, the critique adviser and both escalation-2 advisers. An adviser whose picked id does not start with `claude-` (a GPT T1 model, any other family, or no reachable model) is still launched on `opus`, and the parent writes `family-fallback: <reason>` on that adviser's line 1. This never STOPs and never prompts the user.

The parent writes line 1 of every `advice-<n>-<x>.md` as `model: <id> family: <claude|gpt> rung: <T1|top> launch: <alias>`. The fields `model`, `family` and `rung` describe the pick the ladder chose, `launch` is the Agent `model` value actually passed, and no header states which family served the call. The id prefix decides `family-fallback` only for primary-ladder rung ids; the fallback ladder passes the rung's own alias, and the family reading of the ids above is unchanged.
```

Acceptance criteria:
- `retry.md` contains exactly one line that starts with `**Launch alias.**`, and it lies after the `GPT spawn path:` line and before the `### Cost and caps` heading.
- The paragraph states the four allowed values, the fallback-ladder rule, the primary-ladder rule for all five adviser roles, the `claude-` prefix test with the `family-fallback` note, and the header form with the `launch:` token; no sentence says which family served a call.
- The words "strongest reachable model" no longer appear in `retry.md`; exactly one line starts with `GPT spawn path: `; the backticked phrase `family-fallback: <reason>` and the phrase "never STOPs and never prompts the user" are still present.
- The new text contains none of the strings the constraints forbid (`halt`, `Ruling`, `E-HALT-QA`, `claude-gw-tier`, a fenced line starting with `T` and a digit); the four rung names are still present.
- `uv run pytest tests/skills/test_implement_adviser_family.py tests/skills/test_model_alias_policy.py tests/skills/test_implement_severity_static.py tests/skills/test_workflow_archive.py tests/skills/test_task_workspace_lifecycle.py -q` passes.
AC ids in source order (the bullets under Acceptance criteria): T1.AC1 T1.AC2 T1.AC3 T1.AC4 T1.AC5
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
Start sha: f6c9da0750a8d24b9e494050e2e1be449b8651c9
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-implement-protocol/refs/retry.md b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
index 920cc8e58..c0efa079c 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -178,11 +178,15 @@ Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claud
 | `opus` (known) | 1× `opus` (top rung) | 1× GPT T1 | 2× `opus` |
 | unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× GPT T1 | 2× `opus` |
 
-**Resolving adviser B.** Before spawning, the parent resolves adviser B's model id and writes it on line 1 of `advice-3-b.md`: `model: <id> family: <claude|gpt> rung: <T1|top>`. When no model of the other family can be reached, the parent spawns adviser B on the strongest reachable model and writes `family-fallback: <reason>` on that header line; the final summary lists every such fallback. This never STOPs and never prompts the user: a missing model is configuration, not a finding. The verified spawn path for a GPT T1 model on this install:
+**Resolving adviser B.** Before spawning, the parent resolves adviser B's model id and writes it on line 1 of `advice-3-b.md` in the header form given under Launch alias below. When no model of the other family can be reached, the parent spawns adviser B on `opus` and writes `family-fallback: <reason>` on that header line; the final summary lists every such fallback. This never STOPs and never prompts the user: a missing model is configuration, not a finding. The verified spawn path for a GPT T1 model on this install:
 
 GPT spawn path: none verified; family-fallback applies
 
-The adviser's effort is pinned by `effort:` in its agent file; do not rely on any per-call effort setting. The model tier comes from the Agent call's `model` parameter.
+The adviser's effort is pinned by `effort:` in its agent file; do not rely on any per-call effort setting.
+
+**Launch alias.** The Agent call's `model` takes only `opus`, `sonnet`, `haiku` or `fable`, never a full model id or the value of a rung variable, so the rung id decides which adviser is picked and is not passed to the call. On the fallback ladder the call's `model` is the rung's own alias. On the primary ladder the call's `model` is `opus` for every adviser: adviser A, adviser B, the critique adviser and both escalation-2 advisers. An adviser whose picked id does not start with `claude-` (a GPT T1 model, any other family, or no reachable model) is still launched on `opus`, and the parent writes `family-fallback: <reason>` on that adviser's line 1. This never STOPs and never prompts the user.
+
+The parent writes line 1 of every `advice-<n>-<x>.md` as `model: <id> family: <claude|gpt> rung: <T1|top> launch: <alias>`. The fields `model`, `family` and `rung` describe the pick the ladder chose, `launch` is the Agent `model` value actually passed, and no header states which family served the call. The id prefix decides `family-fallback` only for primary-ladder rung ids; the fallback ladder passes the rung's own alias, and the family reading of the ids above is unchanged.
 
 ### Cost and caps
 
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
