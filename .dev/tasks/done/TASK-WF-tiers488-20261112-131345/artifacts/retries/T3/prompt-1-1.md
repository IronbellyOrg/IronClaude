dca2f17193e46ece36c47711719e25622243c6eb
Review one task for spec compliance.

Task brief: ## Task 3: Change rung 0 to T2bModel01 in both retry.md copies

Edit `src/superclaude/skills/sc-implement-protocol/refs/retry.md` and the tracked copy `plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` identically. On line 162 the primary ladder becomes rung 0 `T2bModel01`, rung 1 `T2Model02`, rung 2 `T1Model02`, rung 3 `T1Model01`; the sentence that the primary ladder is active only when the four rung variables are set keeps working with `T2bModel01`; add one sentence saying rung 0 is the first slot of Tier 2b, GPT-6.1 Terra (a `gpt-` model), kept on purpose so rung 0 stays a gpt-family model, while `T3Model01` is now glm-5.3 and in neither family. On line 172 replace "on `T3Model01`, adviser A on `T2Model02`" with `T2bModel01`. Search both files for any other `T3Model01` or "rung 0" statement and update it; the family wording in lines 166 to 169 must stay correct (rung 0 is a GPT-family executor, so adviser B is the Claude top rung).

Acceptance criteria:
- `grep -n 'T3Model01' src/superclaude/skills/sc-implement-protocol/refs/retry.md plugins/superclaude/skills/sc-implement-protocol/refs/retry.md` prints nothing, and both files contain `T2bModel01` on the ladder line.
- The two files differ from each other in no line that this task changed (`diff` of the two files shows only differences that existed before this task).
Global constraints: 
- Master already holds the tier layout (`ccsession-models.json` tier2b, tier3, tier4; review-tiers file; MODEL-TIERS.md rows). Do not change those lists, slots or windows, and do not edit `ccsession-models.json` (so no version bump).
- Do not touch ccsession alias code (`ccsession`, `models.py`, `local-gateway-alias-proxy.py`) or `tests/skills/test_model_alias_policy.py` lines 229-241 (the `haiku` alias stays on its current tier).
- Do not add a Terra-specific 429 rule and do not edit `docs/designs/sc-issue-command.md` or any file under `docs/testing/v5.0.0/sysop/`.
- Edit only `src/` and `plugins/` sources, tests, docs and CHANGELOG; the `.claude/` copies come from `make sync-dev` and are never staged. Installed primitives must not gain any `src/superclaude/...` path.
- Docs follow the writing rules of the repo: plain words, no em dashes.
Start sha: dca2f17193e46ece36c47711719e25622243c6eb
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md b/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md
index fab0c9e36..4f8755265 100644
--- a/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/plugins/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -159,7 +159,7 @@ A repair is a local, in-place fix of confirmed blockers that runs after a failed
 
 ### Model ladder
 
-**Ladders.** Rungs are numbered weakest to strongest. The primary ladder (environment variables) is rung 0 `T3Model01`, rung 1 `T2Model02`, rung 2 `T1Model02`, rung 3 `T1Model01`, the top rung. `T2Model01` is on par with `T2Model02`: it is recognized as rung 1 only when matching the executor's own model id and is never used as an adviser. The primary ladder is active only when the four rung variables are all set and non-empty (`T2Model01` is optional); otherwise the whole fallback ladder is active: rung 0 `haiku`, rung 1 `sonnet`, rung 2 `opus`, the top rung. The two ladders are never mixed. These are the tier slot variables exported by the workspace environment; `T1Model01` and `T1Model02` are the legacy Tier 1 slots the workspace keeps for readers such as swarm and reflect, and the fallback ladder (`haiku`, `sonnet`, `opus`) applies when they are not all set.
+**Ladders.** Rungs are numbered weakest to strongest. The primary ladder (environment variables) is rung 0 `T2bModel01`, rung 1 `T2Model02`, rung 2 `T1Model02`, rung 3 `T1Model01`, the top rung. Rung 0 is the first slot of Tier 2b, GPT-6.1 Terra (a `gpt-` model), chosen on purpose so that rung 0 stays a GPT-family model; the first Tier 3 slot is no longer used here, because it now holds glm-5.3, which is in neither the `claude-` nor the `gpt-` family. `T2Model01` is on par with `T2Model02`: it is recognized as rung 1 only when matching the executor's own model id and is never used as an adviser. The primary ladder is active only when the four rung variables are all set and non-empty (`T2Model01` is optional); otherwise the whole fallback ladder is active: rung 0 `haiku`, rung 1 `sonnet`, rung 2 `opus`, the top rung. The two ladders are never mixed. These are the tier slot variables exported by the workspace environment; `T1Model01` and `T1Model02` are the legacy Tier 1 slots the workspace keeps for readers such as swarm and reflect, and the fallback ladder (`haiku`, `sonnet`, `opus`) applies when they are not all set.
 
 **Executor tier.** A primary rung's model id is the variable's value with any trailing `[...]` suffix stripped (rung 1 also matches the value of `T2Model01`, when set); a fallback rung's id is `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` when that variable is set, else the Claude model for that alias. The executor's tier is the rung of the active ladder whose id equals the executor's own model id as its system prompt states it, both compared with any trailing `[...]` suffix stripped. No exact match → tier unknown. The tier is recorded as `tier=` (the canonical name of the executor's rung: `T2Model02` for an executor on either T2 model, otherwise the variable name or fallback alias; or `unknown`).
 
@@ -169,7 +169,7 @@ A repair is a local, in-place fix of confirmed blockers that runs after a failed
 - Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it, else `T1Model02`, else the same T1 model).
 - The pick uses the two-answer rule of procedure step 4 (a tie goes to `-a`); the critique adviser uses adviser A's model.
 
-Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claude executor): an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02` and adviser B on the GPT T1 model, then 2 on `T1Model01`; on `T3Model01`, adviser A on `T2Model02`; on `T1Model02`, adviser A on `T1Model01`. Worked example with the fallback ladder:
+Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claude executor): an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02` and adviser B on the GPT T1 model, then 2 on `T1Model01`; on `T2bModel01`, adviser A on `T2Model02`; on `T1Model02`, adviser A on `T1Model01`. Worked example with the fallback ladder:
 
 | Executor tier | Escalation 1 (A3), adviser A | Escalation 1 (A3), adviser B | Escalation 2 (A4) |
 |---|---|---|---|
diff --git a/src/superclaude/skills/sc-implement-protocol/refs/retry.md b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
index fab0c9e36..4f8755265 100644
--- a/src/superclaude/skills/sc-implement-protocol/refs/retry.md
+++ b/src/superclaude/skills/sc-implement-protocol/refs/retry.md
@@ -159,7 +159,7 @@ A repair is a local, in-place fix of confirmed blockers that runs after a failed
 
 ### Model ladder
 
-**Ladders.** Rungs are numbered weakest to strongest. The primary ladder (environment variables) is rung 0 `T3Model01`, rung 1 `T2Model02`, rung 2 `T1Model02`, rung 3 `T1Model01`, the top rung. `T2Model01` is on par with `T2Model02`: it is recognized as rung 1 only when matching the executor's own model id and is never used as an adviser. The primary ladder is active only when the four rung variables are all set and non-empty (`T2Model01` is optional); otherwise the whole fallback ladder is active: rung 0 `haiku`, rung 1 `sonnet`, rung 2 `opus`, the top rung. The two ladders are never mixed. These are the tier slot variables exported by the workspace environment; `T1Model01` and `T1Model02` are the legacy Tier 1 slots the workspace keeps for readers such as swarm and reflect, and the fallback ladder (`haiku`, `sonnet`, `opus`) applies when they are not all set.
+**Ladders.** Rungs are numbered weakest to strongest. The primary ladder (environment variables) is rung 0 `T2bModel01`, rung 1 `T2Model02`, rung 2 `T1Model02`, rung 3 `T1Model01`, the top rung. Rung 0 is the first slot of Tier 2b, GPT-6.1 Terra (a `gpt-` model), chosen on purpose so that rung 0 stays a GPT-family model; the first Tier 3 slot is no longer used here, because it now holds glm-5.3, which is in neither the `claude-` nor the `gpt-` family. `T2Model01` is on par with `T2Model02`: it is recognized as rung 1 only when matching the executor's own model id and is never used as an adviser. The primary ladder is active only when the four rung variables are all set and non-empty (`T2Model01` is optional); otherwise the whole fallback ladder is active: rung 0 `haiku`, rung 1 `sonnet`, rung 2 `opus`, the top rung. The two ladders are never mixed. These are the tier slot variables exported by the workspace environment; `T1Model01` and `T1Model02` are the legacy Tier 1 slots the workspace keeps for readers such as swarm and reflect, and the fallback ladder (`haiku`, `sonnet`, `opus`) applies when they are not all set.
 
 **Executor tier.** A primary rung's model id is the variable's value with any trailing `[...]` suffix stripped (rung 1 also matches the value of `T2Model01`, when set); a fallback rung's id is `ANTHROPIC_DEFAULT_<ALIAS>_MODEL` when that variable is set, else the Claude model for that alias. The executor's tier is the rung of the active ladder whose id equals the executor's own model id as its system prompt states it, both compared with any trailing `[...]` suffix stripped. No exact match → tier unknown. The tier is recorded as `tier=` (the canonical name of the executor's rung: `T2Model02` for an executor on either T2 model, otherwise the variable name or fallback alias; or `unknown`).
 
@@ -169,7 +169,7 @@ A repair is a local, in-place fix of confirmed blockers that runs after a failed
 - Every GPT adviser at any escalation is a T1 model. When the executor is GPT, adviser A is the GPT T1 model (`T1Model01` when the executor is not already on it, else `T1Model02`, else the same T1 model).
 - The pick uses the two-answer rule of procedure step 4 (a tie goes to `-a`); the critique adviser uses adviser A's model.
 
-Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claude executor): an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02` and adviser B on the GPT T1 model, then 2 on `T1Model01`; on `T3Model01`, adviser A on `T2Model02`; on `T1Model02`, adviser A on `T1Model01`. Worked example with the fallback ladder:
+Escalation 2 = 2 advisers on the top rung, always. Primary-ladder example (Claude executor): an executor on `T2Model02` or `T2Model01` gets adviser A on `T1Model02` and adviser B on the GPT T1 model, then 2 on `T1Model01`; on `T2bModel01`, adviser A on `T2Model02`; on `T1Model02`, adviser A on `T1Model01`. Worked example with the fallback ladder:
 
 | Executor tier | Escalation 1 (A3), adviser A | Escalation 1 (A3), adviser B | Escalation 2 (A4) |
 |---|---|---|---|
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
