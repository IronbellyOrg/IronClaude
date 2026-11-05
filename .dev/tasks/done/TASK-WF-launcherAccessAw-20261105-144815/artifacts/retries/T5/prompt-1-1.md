7be4d7b314048fc4de097b661e37908d4643c069
Review one task for spec compliance.

Task brief: ## Task 5: Update the CHANGELOG.md entry and run the final checks

Depends on: Task 4

Covers R-007 for the changelog.

In the "ccsession: tier mode sets the model aliases (#384 launcher follow-up)" entry under `## [Unreleased]` in `CHANGELOG.md`: change the first `#### Changed` bullet so it says the launcher exports each variable only when the owner may use its tier, and an owner limited to other tiers keeps the inherited value for the others; delete the "Known limit" bullet; change the pointer-pages bullet if it says the pages describe all three unconditionally; and in the `#### Added` bullet name the new restricted-owner tests. Then run `make lint`, `uv run ruff format --check src/ tests/`, `make sync-dev` and `make verify-sync`, and save their output to `./artifacts/t5-checks.log`.

Acceptance criteria:
- `grep -n "Known limit" CHANGELOG.md` returns nothing and the entry names the per-tier rule.
- `./artifacts/t5-checks.log` shows `make lint`, the format check and `make verify-sync` passing.

AC ids (in source order):
T5.AC1: `grep -n "Known limit" CHANGELOG.md` returns nothing and the entry names the per-tier rule.
T5.AC2: `./artifacts/t5-checks.log` shows `make lint`, the format check and `make verify-sync` passing.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `models.py`, `local-gateway-alias-proxy.py` and `ccsession-orca` stay untouched (R-002).
- The three unconditional export lines from the first follow-up already sit right after `USE_SHIM=1` in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession` (about lines 867-870); re-read the file before editing and change only those lines (R-001).
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the probe records show; no probe exercised the Agent-call `model` parameter.
- R-008 (the pull request body) changes no file and has no task; it is written when the pull request is opened. R-004 has no launcher-level test because a broken access entry makes the launcher exit before Claude starts (`apply_tier_selection`, `|| exit 2`).
Start sha: 7be4d7b314048fc4de097b661e37908d4643c069
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index 0c270e93..823dfd6e 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -30,7 +30,7 @@ All notable changes to IronClaude are documented in this file.
 
 #### Added (model aliases)
 
-- New reference page `docs/reference/model-aliases.md`: what `tests/skills/test_model_alias_policy.py` checks and its allow-list (the three issue-worker agents pin picker ids on purpose), the owner decision of 2026-11-05 for a ccsession tier workspace (`opus` to `claude-gw-tier1a`, `sonnet` to `claude-gw-tier1b`, `haiku` to `claude-gw-tier2`, through `ANTHROPIC_DEFAULT_*_MODEL`), why aliases and not picker ids, and the known consequences. The launcher sets these variables in tier mode through the follow-up change in the next entry (specified in `.dev/issues/384/launcher-followup.md` with its failing-first test). The workspace defaults file exports real model ids for the same three variables, and the launcher export replaces them inside a tier workspace.
+- New reference page `docs/reference/model-aliases.md`: what `tests/skills/test_model_alias_policy.py` checks and its allow-list (the three issue-worker agents pin picker ids on purpose), the owner decision of 2026-11-05 for a ccsession tier workspace (`opus` to `claude-gw-tier1a`, `sonnet` to `claude-gw-tier1b`, `haiku` to `claude-gw-tier2`, through `ANTHROPIC_DEFAULT_*_MODEL`), why aliases and not picker ids, and the known consequences. The launcher sets these variables in tier mode through the follow-up change in the next entry (specified in `.dev/issues/384/launcher-followup.md` with its failing-first test). The workspace defaults file exports real model ids for the same three variables, and the launcher export replaces the ones for tiers the owner may use inside a tier workspace.
 - New test file `tests/skills/test_model_alias_policy.py` (frontmatter `model:` values, `claude-gw-tier` text, full model ids in Python constants and in `--model` flags, and the fixes below) and four tests that record how the sprint alternate-model suggestion and the reflect alias count behave while the variables hold tier ids.
 
 #### Changed (model aliases)
@@ -44,13 +44,12 @@ All notable changes to IronClaude are documented in this file.
 
 #### Changed (ccsession tier mode)
 
-- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (`src/superclaude/skills/ccsession-tag/ccsession`), so the plain aliases `opus`, `sonnet` and `haiku` in agent frontmatter and `--model` resolve to the tiers (the probes did not exercise the Agent-call `model` parameter). Outside tier mode the launcher sets none of them. Inside a tier workspace these values replace the real model ids that the workspace defaults file exports for the same variables.
-- Known limit: the exports do not depend on the owner's tier access. For an owner limited to other tiers, a `model: opus` or `model: sonnet` subagent is sent to a tier the shim refuses. This comes from reading the code, not from a run; see `docs/reference/model-aliases.md`.
+- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (`src/superclaude/skills/ccsession-tag/ccsession`), each one only when the workspace owner may use its tier, so the plain aliases `opus`, `sonnet` and `haiku` in agent frontmatter and `--model` resolve to the tiers (the probes did not exercise the Agent-call `model` parameter). "May use" is read with the `tiers` command of `models.py`, the rule the shim applies, without running the shim. A variable whose tier the owner may not use, or every variable when the list cannot be read, keeps its inherited value: an owner limited to tier2 and tier3 gets only the haiku variable and keeps the inherited opus and sonnet values. Outside tier mode the launcher sets none of them. Inside a tier workspace the exported values replace the real model ids that the workspace defaults file exports for the same variables.
 - The pages that said the launcher would set the variables later now say that it does: `docs/reference/model-aliases.md`, `docs/user-guide/brainstorm.md`, `docs/user-guide/commands.md`, `refs/tiers.md` and `refs/chains.md` of the `/sc:issue` protocol, a comment in `src/superclaude/cli/reflect/commands.py` and the docstring of `tests/skills/test_model_alias_policy.py`.
 
 #### Added (tier alias tests and probe)
 
-- Two tests in `tests/unit/test_ccsession_tiers.py`: `test_tier_launch_exports_the_alias_variables` (it failed before the launcher edit) and `test_non_tier_launch_leaves_the_alias_variables_unset`, with three keys added to the fake Claude of `_launch_env`.
+- Five tests in `tests/unit/test_ccsession_tiers.py`: `test_tier_launch_exports_the_alias_variables` (an unrestricted owner gets all three; it failed before the launcher edit), `test_non_tier_launch_leaves_the_alias_variables_unset`, `test_limited_owner_gets_only_the_haiku_alias_variable`, `test_limited_owner_keeps_inherited_alias_values` and `test_workspace_without_tier1a_and_tier1b_exports_only_its_tiers`, with three keys added to the fake Claude of `_launch_env`.
 - Probe record `.dev/issues/384/analysis/probe-sonnet-alias.md`: `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` makes `--model sonnet` and `model: sonnet` run on that tier. In that probe a subagent whose alias is in the main session's own model family stayed on the main session's model.
 
 ### Install: harden the pinned-plugin install (#360 follow-ups)

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t5-checks.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t5-checks.log
new file mode 100644
index 00000000..9f0c4424
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t5-checks.log
@@ -0,0 +1,26 @@
+$ grep -n "Known limit" CHANGELOG.md   (literal AC command)
+70:- Known limits, commands it does not catch: string arguments to another interpreter (`bash -c "python3 x"`,
+note: the only hit is the "Known limits, commands it does not catch" bullet of the unrelated UV-only Bash hook entry (#357); the follow-up entry has no such line
+$ grep -n "Known limit:" CHANGELOG.md   (the removed bullet)
+known-limit-colon-exit=1
+$ sed -n "/ccsession: tier mode sets the model aliases/,/^### Install/p" CHANGELOG.md | grep -c "per-tier\|each one only when\|may use"
+1
+$ make lint
+  ✅ PASS — architecture policy compliant (5 warning(s))
+Running linter...
+uv run ruff check .
+All checks passed!
+lint-exit=0
+$ uv run ruff format --check src/ tests/
+1199 files already formatted
+format-exit=0
+$ make sync-dev (writes only gitignored .claude/ copies)
+   Templates: 52 files
+$ make verify-sync
+=== Hooks Cross-Consistency ===
+  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes
+
+✅ All components in sync.
+verify-exit=0
+$ git status --short | grep .claude
+claude-grep-exit=1

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
