6cb3c893b62e18ff5b3170291fff7a3eb81599d9
Review one task for spec compliance.

Task brief: ## Task 3: Update docs/reference/model-aliases.md

Depends on: Task 2

In `docs/reference/model-aliases.md`: change the sentence "Owner decision of 2026-11-05: once the launcher sets the three variables, ..." so it says that in a ccsession tier workspace the launcher sets the three variables and the aliases resolve as the table shows. Change the "Target, once the launcher change lands: ..." paragraph to a present-tense statement that outside a ccsession tier workspace the launcher sets none of the three variables. Replace the "Status on 2026-11-05 ..." paragraph (the one saying the launcher is to apply the exports after the #315 pull request merges, then describing `/etc/aidev02/aienv.d/defaults.sh`) with a status paragraph that says the launcher now exports them in tier mode only, naming `src/superclaude/skills/ccsession-tag/ccsession` and the tests `test_tier_launch_exports_the_alias_variables` and `test_non_tier_launch_leaves_the_alias_variables_unset`. Keep the facts about the defaults file only as the values that the launcher export overrides in a tier workspace, and outside one the defaults file still applies; re-read `/etc/aidev02/aienv.d/defaults.sh` lines 92-94 before restating them. In the section "Why aliases and not picker ids", correct the bullet that says the probe did not set `ANTHROPIC_DEFAULT_SONNET_MODEL` and the bullet that says the same-family case was not covered, from `.dev/issues/384/analysis/probe-sonnet-alias.md`: the sonnet variable remaps `--model sonnet` and `model: sonnet`, and a subagent whose alias is in the main session's own model family stayed on the main model in that probe. Link the new probe record next to the existing probe link.

Acceptance criteria:
- `grep -n "is to apply\|once the launcher\|did not set" docs/reference/model-aliases.md` returns no line that still describes the launcher change as pending or the sonnet variable as unprobed.
- The page links `.dev/issues/384/analysis/probe-sonnet-alias.md` with a relative path that exists.

AC ids (in source order):
T3.AC1: `grep -n "is to apply\|once the launcher\|did not set" docs/reference/model-aliases.md` returns no line that still describes the launcher change as pending or the sonnet variable as unprobed.
T3.AC2: The page links `.dev/issues/384/analysis/probe-sonnet-alias.md` with a relative path that exists.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `ccsession-orca` stays untouched.
- Re-verify every line number in the source against the code on the working branch before editing: the source numbers are at base commit 38eb3c58 and the #315 change edits the same files.
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the two probe records show: the probe record is `.dev/issues/384/analysis/probe-alias-remap.md` (opus and haiku) and `.dev/issues/384/analysis/probe-sonnet-alias.md` (sonnet).
Start sha: 6cb3c893b62e18ff5b3170291fff7a3eb81599d9
Diff against the start snapshot: diff --git a/docs/reference/model-aliases.md b/docs/reference/model-aliases.md
index 8c86e6b4..52c0c521 100644
--- a/docs/reference/model-aliases.md
+++ b/docs/reference/model-aliases.md
@@ -19,7 +19,7 @@ Checks in `tests/skills/test_model_alias_policy.py` that read model names includ
 
 ## The mapping
 
-Owner decision of 2026-11-05: once the launcher sets the three variables, inside a ccsession tier workspace the aliases resolve as follows:
+Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets the three variables, so the aliases resolve as follows:
 
 | Alias | Tier model it resolves to | Set by |
 |---|---|---|
@@ -35,10 +35,10 @@ ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b
 ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
 ```
 
-Target, once the launcher change lands: outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.
+Outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.
 
-Status on 2026-11-05: the ccsession launcher is to apply these exports in a follow-up change after the #315 pull request merges.
-Until then `/etc/aidev02/aienv.d/defaults.sh` exports real model ids for the three variables: line 92 sets `ANTHROPIC_DEFAULT_HAIKU_MODEL` from `T2Model02` (`glm-5.3`, line 37), line 93 sets `ANTHROPIC_DEFAULT_OPUS_MODEL` from `T1aModel01` (`claude-opus-5-5`, line 23) and line 94 sets `ANTHROPIC_DEFAULT_SONNET_MODEL` from `T1aModel02` (`claude-sonnet-5-5`, line 25).
+Status on 2026-11-05: the ccsession launcher (`src/superclaude/skills/ccsession-tag/ccsession`) now exports these three variables in tier mode only, in the branch that sets `USE_SHIM=1`. `test_tier_launch_exports_the_alias_variables` and `test_non_tier_launch_leaves_the_alias_variables_unset` in `tests/unit/test_ccsession_tiers.py` pin both halves.
+`/etc/aidev02/aienv.d/defaults.sh` still exports real model ids for the same three variables, and the launcher export replaces them inside a tier workspace; outside one the inherited values stay. Line 92 sets `ANTHROPIC_DEFAULT_HAIKU_MODEL` from `T2Model02` (`glm-5.3`, line 37), line 93 sets `ANTHROPIC_DEFAULT_OPUS_MODEL` from `T1aModel01` (`claude-opus-5-5`, line 23) and line 94 sets `ANTHROPIC_DEFAULT_SONNET_MODEL` from `T1aModel02` (`claude-sonnet-5-5`, line 25).
 
 ## Why aliases and not picker ids
 
@@ -46,15 +46,17 @@ Source: <https://code.claude.com/docs/en/sub-agents>, read 2026-11-05.
 
 - The sub-agents page says the Agent-call `model` parameter takes the aliases `sonnet`, `opus`, `haiku` or `fable`, and that Claude cannot pass a full model id or `inherit` on that call.
 - The page says the frontmatter `model` takes an alias, a full model id or `inherit`; it documents no environment lookup in that field, so `model: ${SOMETHING}` is not a documented option.
-- The probe found that a tier id set in `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_HAIKU_MODEL` was served and that `model: opus` and `model: haiku` resolved through it; it did not set `ANTHROPIC_DEFAULT_SONNET_MODEL`.
-- The page also describes an edge case for family aliases: when the main session runs a model of the same family, the alias can resolve to that model. The probe did not cover a main session that runs in the same family as the alias.
+- The probes found that a tier id set in `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` or `ANTHROPIC_DEFAULT_HAIKU_MODEL` was served, that `model: opus`, `model: sonnet` and `model: haiku` resolved through it, and that `--model sonnet` ran on the tier id as well.
+- The page also describes an edge case for family aliases: when the main session runs a model of the same family, the alias can resolve to that model. In the sonnet probe a `model: sonnet` subagent under a Sonnet main session ran on the main session's model, not on `claude-gw-tier1b`; that is one observation, and the rule behind it is not verified (the Claude Code source was not read). The same case was not probed for an Opus or a Haiku main session.
 
 On 2026-11-05 a probe against the workspace gateway ([probe record](../../.dev/issues/384/analysis/probe-alias-remap.md)) found that a subagent with `model: opus` ran on `claude-gw-tier1a` and one with `model: haiku` ran on `claude-gw-tier2`, while the main session kept its own model.
+A second probe ([sonnet probe record](../../.dev/issues/384/analysis/probe-sonnet-alias.md)) found the same for `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b`: `--model sonnet` and a `model: sonnet` subagent under an Opus main session ran on `claude-gw-tier1b`.
 Claude Code logs an `unrecognized_model` notice for the tier ids and serves the request.
-The probe covered the frontmatter path and `--model`; it did not exercise the Agent-call parameter.
+The probes covered the frontmatter path and `--model`; they did not exercise the Agent-call parameter.
 
 ## Known consequences
 
+- **Owners limited to some tiers.** The shim keeps only the tiers the workspace owner may use (`CCSESSION_TIER_RULES`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` lines 185-187) and answers a request for any other tier with a 400 (lines 705-714). The launcher exports the three variables whether or not the owner may use `tier1a`, `tier1b` and `tier2`, so for an owner limited to other tiers a `model: opus` or `model: sonnet` subagent is sent to a tier the shim refuses. This comes from reading the code; no limited-owner launch was run, and the export is not access-aware.
 - **Reflect reviewer diversity.** When the three variables hold the tier ids, `count_model_aliases` (`src/superclaude/cli/reflect/runner.py` lines 291-310) counts three distinct values. Tier 1a and tier 1b both list Claude Sonnet 5.5 (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` lines 38-39), so the reviewers differ less than the count suggests.
 - **Sprint alternate-model suggestion.** Given the alias `opus`, `suggest_alternate_model` returns `sonnet` when the two slots hold different ids (`src/superclaude/cli/sprint/aienv.py` lines 149-152). When the three `ANTHROPIC_DEFAULT_*_MODEL` slots hold tier ids and no slot that `_load_aliases` reads, including `T2Model01` to `T2Model0N` (lines 78-82), holds a given Claude id from a cooldown message such as `claude-opus-5-5`, it returns `None` (lines 111-128).
 - **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) and the `/sc:recommend` eval model lists (`src/superclaude/cli/recommend/eval_aggregate.py` lines 18-20) name the aliases, so this change does not rename them.

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t3-checks.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t3-checks.log
new file mode 100644
index 00000000..770a16d7
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t3-checks.log
@@ -0,0 +1,8 @@
+$ grep -n "is to apply\|once the launcher\|did not set\|did not cover\|Until then" docs/reference/model-aliases.md
+grep-exit=1
+$ link target
+-rw------- 1 coder coder 2068 Nov  5 13:12 ../../.dev/issues/384/analysis/probe-alias-remap.md
+-rw-r--r-- 1 coder coder 2757 Nov  5 13:15 ../../.dev/issues/384/analysis/probe-sonnet-alias.md
+$ pytest
+
+============================== 13 passed in 1.33s ==============================

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
