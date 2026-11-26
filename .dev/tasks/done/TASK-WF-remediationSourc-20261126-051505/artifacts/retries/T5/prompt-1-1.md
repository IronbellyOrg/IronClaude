8940cfadb4652ec82c58f3c72405e433059b47e4
Review one task for spec compliance.

Task brief: ## Task 5: Copy the changed retry.md and SKILL.md into the plugins skill directory

Depends on: Task 1, Task 2, Task 3, Task 4

Copy `src/superclaude/skills/sc-implement-protocol/refs/retry.md` over `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md`, and `src/superclaude/skills/sc-implement-protocol/SKILL.md` over `plugins/superclaude/skills/sc-implement-protocol/SKILL.md`, so each pair is byte-identical. Then run `make sync-dev` (it copies `src/` into the gitignored `.claude/` dev copies) and `make verify-sync`; do not stage anything under `.claude/`.

Acceptance criteria:
- `diff -q` reports no difference for both pairs (src against plugins).
- `uv run pytest tests/commands/test_workflow_command.py -q` passes (it compares the two skill trees byte for byte).
- `make verify-sync` exits 0 after `make sync-dev`, and `git status --short` lists no path under `.claude/`.
AC ids in source order (the bullets under Acceptance criteria): T5.AC1 T5.AC2 T5.AC3
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
Start sha: 8940cfadb4652ec82c58f3c72405e433059b47e4
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md b/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md
index 920cc8e58..d215f4257 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -166,23 +166,27 @@ A repair is a local, in-place fix of confirmed blockers that runs after a failed
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
-| `haiku` | 1× `sonnet` | 1× GPT T1 | 2× `opus` |
-| `sonnet` | 1× `opus` | 1× GPT T1 | 2× `opus` |
-| `opus` (known) | 1× `opus` (top rung) | 1× GPT T1 | 2× `opus` |
-| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× GPT T1 | 2× `opus` |
+| `haiku` | 1× `sonnet` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
+| `sonnet` | 1× `opus` | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
+| `opus` (known) | 1× `opus` (top rung) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
+| unknown | 1× `opus` (top rung, so the two escalations still differ) | 1× `opus` (GPT T1 not launchable, family-fallback) | 2× `opus` |
 
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
 
diff --git a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
index 91a69a462..83bd202b3 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/SKILL.md
@@ -190,7 +190,7 @@ Extra `fail` does not change the spec verdict. A task MUST NOT be marked `compli
 
 ## Done
 
-Every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus operator Ruling). Print the ledger path. A `compliant` line may carry a `notes@` token (complete with notes, `refs/qa.md`). When no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints lines 2 to m of each task's notes file with their checklist answers, informational only, asking the user nothing. The final summary also prints every `family-fallback:` header line of an `advice-3-b.md` (`refs/retry.md`, Model ladder). Suggest `/sc:test` and `/sc:git` only as optional next steps, not gates.
+Every enumerable task has a `complete` ledger line (verdict `compliant`, or non-compliant plus operator Ruling). Print the ledger path. A `compliant` line may carry a `notes@` token (complete with notes, `refs/qa.md`). When no FINAL that can block ran (any legacy run, including N=1 and `--skip-final-review`), the final summary also prints lines 2 to m of each task's notes file with their checklist answers, informational only, asking the user nothing. The final summary also prints every `family-fallback:` header line of an `advice-<n>-<x>.md` (`refs/retry.md`, Model ladder). Suggest `/sc:test` and `/sc:git` only as optional next steps, not gates.
 
 **Follow-up print (record and print only).** At the final review step the executor prints every non-superseded minor line of every task's `<retries>/T<id>/notes.md` (lines 2 to m, the lines counted above) and runs the safety scan over each notes file with this call:
 
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
