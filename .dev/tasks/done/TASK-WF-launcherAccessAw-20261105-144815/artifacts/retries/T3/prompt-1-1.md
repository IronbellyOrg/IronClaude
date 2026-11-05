4358770d07add6d8de88fea202234b42262bcde1
Review one task for spec compliance.

Task brief: ## Task 3: Update docs/reference/model-aliases.md

Depends on: Task 2

Covers R-007 for the reference page.

In `docs/reference/model-aliases.md`: change the sentence under "The mapping" that says the launcher sets the three variables so that it says the launcher sets each variable only for a tier the workspace owner may use. Rewrite the "Status on 2026-11-05" paragraph so that it says: the launcher (`src/superclaude/skills/ccsession-tag/ccsession`) exports each variable in tier mode only, when the tier is on the owner's list of usable tiers; the list is the output of the `tiers` command of `src/superclaude/skills/ccsession-tag/models.py` (the same `tier_access` rule the shim applies, `CCSESSION_ACCESS` and the tier list), read without running the shim; a tier that is not on the list, or a list that cannot be read, leaves the inherited value; so an owner limited to tier2 and tier3 gets only `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` and keeps the inherited opus and sonnet values (for example the real model ids from `/etc/aidev02/aienv.d/defaults.sh`, whose lines 92-94 you re-read first); and name the tests of Task 1 and `test_tier_launch_exports_the_alias_variables`. Delete the "Owners limited to some tiers" bullet under "Known consequences", since the status paragraph now states what such an owner gets. Keep the table rows and the exports code block unchanged.

Acceptance criteria:
- `grep -n "Owners limited to some tiers" docs/reference/model-aliases.md` returns nothing, and the page contains the words "each variable" or "per tier" and the command name `tiers`.
- `uv run pytest tests/skills/test_model_alias_policy.py` passes.

AC ids (in source order):
T3.AC1: `grep -n "Owners limited to some tiers" docs/reference/model-aliases.md` returns nothing, and the page contains the words "each variable" or "per tier" and the command name `tiers`.
T3.AC2: `uv run pytest tests/skills/test_model_alias_policy.py` passes.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `models.py`, `local-gateway-alias-proxy.py` and `ccsession-orca` stay untouched (R-002).
- The three unconditional export lines from the first follow-up already sit right after `USE_SHIM=1` in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession` (about lines 867-870); re-read the file before editing and change only those lines (R-001).
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the probe records show; no probe exercised the Agent-call `model` parameter.
- R-008 (the pull request body) changes no file and has no task; it is written when the pull request is opened. R-004 has no launcher-level test because a broken access entry makes the launcher exit before Claude starts (`apply_tier_selection`, `|| exit 2`).
Start sha: 4358770d07add6d8de88fea202234b42262bcde1
Diff against the start snapshot: diff --git a/docs/reference/model-aliases.md b/docs/reference/model-aliases.md
index 52c0c521..a87928ec 100644
--- a/docs/reference/model-aliases.md
+++ b/docs/reference/model-aliases.md
@@ -19,7 +19,7 @@ Checks in `tests/skills/test_model_alias_policy.py` that read model names includ
 
 ## The mapping
 
-Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets the three variables, so the aliases resolve as follows:
+Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets each variable only when the workspace owner may use its tier, so for an owner who may use all three tiers the aliases resolve as follows:
 
 | Alias | Tier model it resolves to | Set by |
 |---|---|---|
@@ -27,7 +27,7 @@ Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher set
 | `sonnet` | `claude-gw-tier1b` | `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` |
 | `haiku` | `claude-gw-tier2` | `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` |
 
-The exports are:
+When the owner may use the tier, the launcher exports:
 
 ```text
 ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a
@@ -37,8 +37,9 @@ ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2
 
 Outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.
 
-Status on 2026-11-05: the ccsession launcher (`src/superclaude/skills/ccsession-tag/ccsession`) now exports these three variables in tier mode only, in the branch that sets `USE_SHIM=1`. `test_tier_launch_exports_the_alias_variables` and `test_non_tier_launch_leaves_the_alias_variables_unset` in `tests/unit/test_ccsession_tiers.py` pin both halves.
-`/etc/aidev02/aienv.d/defaults.sh` still exports real model ids for the same three variables, and the launcher export replaces them inside a tier workspace; outside one the inherited values stay. Line 92 sets `ANTHROPIC_DEFAULT_HAIKU_MODEL` from `T2Model02` (`glm-5.3`, line 37), line 93 sets `ANTHROPIC_DEFAULT_OPUS_MODEL` from `T1aModel01` (`claude-opus-5-5`, line 23) and line 94 sets `ANTHROPIC_DEFAULT_SONNET_MODEL` from `T1aModel02` (`claude-sonnet-5-5`, line 25).
+Status on 2026-11-05: the ccsession launcher (`src/superclaude/skills/ccsession-tag/ccsession`) exports each of these variables in tier mode only, in the branch that sets `USE_SHIM=1`, and only when the tier is on the workspace owner's list of usable tiers. That list is the output of the `tiers` command of `src/superclaude/skills/ccsession-tag/models.py` (lines 923-935). The command applies `tier_access`, the rule the shim uses (`CCSESSION_ACCESS`, `CCSESSION_TIER_RULES` and the tier list), so the launcher reads the rule without running the shim and adds no second rule. A variable whose tier is not on the list is left exactly as inherited, and when the list cannot be read no variable is exported.
+So an owner limited to tier2 and tier3 gets only `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` and keeps the inherited opus and sonnet values, for example the real model ids from the workspace defaults file; a workspace whose model list has no tier1a and tier1b behaves the same. The list is read when the launcher starts, before that launch's model-data refresh, so a list changed by the refresh applies from the next launch. The five tests `test_tier_launch_exports_the_alias_variables`, `test_limited_owner_gets_only_the_haiku_alias_variable`, `test_limited_owner_keeps_inherited_alias_values`, `test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers` and `test_non_tier_launch_leaves_the_alias_variables_unset` in `tests/unit/test_ccsession_tiers.py` pin these cases.
+`/etc/aidev02/aienv.d/defaults.sh` still exports real model ids for the same three variables; inside a tier workspace the launcher export replaces the ones for tiers the owner may use and the others stay, and outside one the inherited values stay. Line 92 sets `ANTHROPIC_DEFAULT_HAIKU_MODEL` from `T2Model02` (`glm-5.3`, line 37), line 93 sets `ANTHROPIC_DEFAULT_OPUS_MODEL` from `T1aModel01` (`claude-opus-5-5`, line 23) and line 94 sets `ANTHROPIC_DEFAULT_SONNET_MODEL` from `T1aModel02` (`claude-sonnet-5-5`, line 25).
 
 ## Why aliases and not picker ids
 
@@ -56,7 +57,6 @@ The probes covered the frontmatter path and `--model`; they did not exercise the
 
 ## Known consequences
 
-- **Owners limited to some tiers.** The shim keeps only the tiers the workspace owner may use (`CCSESSION_TIER_RULES`, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` lines 185-187) and answers a request for any other tier with a 400 (lines 705-714). The launcher exports the three variables whether or not the owner may use `tier1a`, `tier1b` and `tier2`, so for an owner limited to other tiers a `model: opus` or `model: sonnet` subagent is sent to a tier the shim refuses. This comes from reading the code; no limited-owner launch was run, and the export is not access-aware.
 - **Reflect reviewer diversity.** When the three variables hold the tier ids, `count_model_aliases` (`src/superclaude/cli/reflect/runner.py` lines 291-310) counts three distinct values. Tier 1a and tier 1b both list Claude Sonnet 5.5 (`src/superclaude/skills/ccsession-tag/MODEL-TIERS.md` lines 38-39), so the reviewers differ less than the count suggests.
 - **Sprint alternate-model suggestion.** Given the alias `opus`, `suggest_alternate_model` returns `sonnet` when the two slots hold different ids (`src/superclaude/cli/sprint/aienv.py` lines 149-152). When the three `ANTHROPIC_DEFAULT_*_MODEL` slots hold tier ids and no slot that `_load_aliases` reads, including `T2Model01` to `T2Model0N` (lines 78-82), holds a given Claude id from a cooldown message such as `claude-opus-5-5`, it returns `None` (lines 111-128).
 - **Roadmap names.** Step ids such as `generate-opus-architect` (`src/superclaude/skills/sc-roadmap-protocol/SKILL.md` line 114) and the `/sc:recommend` eval model lists (`src/superclaude/cli/recommend/eval_aggregate.py` lines 18-20) name the aliases, so this change does not rename them.

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t3-checks.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t3-checks.log
new file mode 100644
index 00000000..7d5f1537
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t3-checks.log
@@ -0,0 +1,8 @@
+$ grep -n "Owners limited to some tiers" docs/reference/model-aliases.md
+grep-exit=1
+$ grep -n "each variable\|`tiers` command" docs/reference/model-aliases.md
+22:Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets each variable only when the workspace owner may use its
+40:Status on 2026-11-05: the ccsession launcher (`src/superclaude/skills/ccsession-tag/ccsession`) exports each of these variables in tier m
+$ pytest tests/skills/test_model_alias_policy.py
+
+============================== 13 passed in 1.26s ==============================

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
