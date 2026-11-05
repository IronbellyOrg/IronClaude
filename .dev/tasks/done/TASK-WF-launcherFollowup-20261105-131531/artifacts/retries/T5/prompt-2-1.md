af2ce147e76f70e3832c3689e17e2104819bdb57
Review one task for spec compliance.

Task brief: ## Task 5: Add the CHANGELOG.md Unreleased entry

Depends on: Task 4

In `CHANGELOG.md` under `## [Unreleased]`, add a section for this change (issue #384, launcher follow-up) with a `#### Changed` bullet that says the ccsession launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` in tier mode only, and a `#### Added` bullet for the two tests and the sonnet probe record. Edit the sentence in the earlier #384 entry that says the launcher does not set these variables yet so it points to the new entry instead of claiming the opposite.

Acceptance criteria:
- `CHANGELOG.md` has the new entry under `[Unreleased]` and no sentence that still says the launcher does not set the variables.
- `make lint`, `uv run ruff format --check src/ tests/` and `make verify-sync` pass.

AC ids (in source order):
T5.AC1: `CHANGELOG.md` has the new entry under `[Unreleased]` and no sentence that still says the launcher does not set the variables.
T5.AC2: `make lint`, `uv run ruff format --check src/ tests/` and `make verify-sync` pass.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `ccsession-orca` stays untouched.
- Re-verify every line number in the source against the code on the working branch before editing: the source numbers are at base commit 38eb3c58 and the #315 change edits the same files.
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the two probe records show: the probe record is `.dev/issues/384/analysis/probe-alias-remap.md` (opus and haiku) and `.dev/issues/384/analysis/probe-sonnet-alias.md` (sonnet).
Start sha: af2ce147e76f70e3832c3689e17e2104819bdb57
Diff against the start snapshot: diff --git a/CHANGELOG.md b/CHANGELOG.md
index a2850ce0..0c270e93 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -30,7 +30,7 @@ All notable changes to IronClaude are documented in this file.
 
 #### Added (model aliases)
 
-- New reference page `docs/reference/model-aliases.md`: what `tests/skills/test_model_alias_policy.py` checks and its allow-list (the three issue-worker agents pin picker ids on purpose), the owner decision of 2026-11-05 for a ccsession tier workspace (`opus` to `claude-gw-tier1a`, `sonnet` to `claude-gw-tier1b`, `haiku` to `claude-gw-tier2`, through `ANTHROPIC_DEFAULT_*_MODEL`), why aliases and not picker ids, and the known consequences. The launcher does not set these variables yet: that is a separate follow-up pull request after #315 merges, specified in `.dev/issues/384/launcher-followup.md` with its failing-first test. Until then the workspace defaults file exports real model ids for the three variables.
+- New reference page `docs/reference/model-aliases.md`: what `tests/skills/test_model_alias_policy.py` checks and its allow-list (the three issue-worker agents pin picker ids on purpose), the owner decision of 2026-11-05 for a ccsession tier workspace (`opus` to `claude-gw-tier1a`, `sonnet` to `claude-gw-tier1b`, `haiku` to `claude-gw-tier2`, through `ANTHROPIC_DEFAULT_*_MODEL`), why aliases and not picker ids, and the known consequences. The launcher sets these variables in tier mode through the follow-up change in the next entry (specified in `.dev/issues/384/launcher-followup.md` with its failing-first test). The workspace defaults file exports real model ids for the same three variables, and the launcher export replaces them inside a tier workspace.
 - New test file `tests/skills/test_model_alias_policy.py` (frontmatter `model:` values, `claude-gw-tier` text, full model ids in Python constants and in `--model` flags, and the fixes below) and four tests that record how the sprint alternate-model suggestion and the reflect alias count behave while the variables hold tier ids.
 
 #### Changed (model aliases)
@@ -40,6 +40,19 @@ All notable changes to IronClaude are documented in this file.
 - The cleanup-audit skill, command and report template say that the Pass 1 scanner runs on Sonnet, as `audit-scanner` already did, and drop the 50-70% cost claim that was specific to Haiku.
 - The implement retry ladder (`refs/retry.md`, `refs/ledger.md`) names the slot variables the workspace exports (`T3Model01`, `T2Model01`, `T2Model02`, `T1Model01`, `T1Model02`) instead of spellings with an underscore that no workspace exports. In a workspace that sets the four rung variables the primary ladder now replaces the alias fallback ladder, which changes which models the retry advisers use.
 
+### ccsession: tier mode sets the model aliases (#384 launcher follow-up)
+
+#### Changed (ccsession tier mode)
+
+- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (`src/superclaude/skills/ccsession-tag/ccsession`), so the plain aliases `opus`, `sonnet` and `haiku` in agent frontmatter and `--model` resolve to the tiers (the probes did not exercise the Agent-call `model` parameter). Outside tier mode the launcher sets none of them. Inside a tier workspace these values replace the real model ids that the workspace defaults file exports for the same variables.
+- Known limit: the exports do not depend on the owner's tier access. For an owner limited to other tiers, a `model: opus` or `model: sonnet` subagent is sent to a tier the shim refuses. This comes from reading the code, not from a run; see `docs/reference/model-aliases.md`.
+- The pages that said the launcher would set the variables later now say that it does: `docs/reference/model-aliases.md`, `docs/user-guide/brainstorm.md`, `docs/user-guide/commands.md`, `refs/tiers.md` and `refs/chains.md` of the `/sc:issue` protocol, a comment in `src/superclaude/cli/reflect/commands.py` and the docstring of `tests/skills/test_model_alias_policy.py`.
+
+#### Added (tier alias tests and probe)
+
+- Two tests in `tests/unit/test_ccsession_tiers.py`: `test_tier_launch_exports_the_alias_variables` (it failed before the launcher edit) and `test_non_tier_launch_leaves_the_alias_variables_unset`, with three keys added to the fake Claude of `_launch_env`.
+- Probe record `.dev/issues/384/analysis/probe-sonnet-alias.md`: `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` makes `--model sonnet` and `model: sonnet` run on that tier. In that probe a subagent whose alias is in the main session's own model family stayed on the main session's model.
+
 ### Install: harden the pinned-plugin install (#360 follow-ups)
 
 #### Fixed (plugin install)

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t5-checks.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t5-checks.log
new file mode 100644
index 00000000..22569d1a
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t5-checks.log
@@ -0,0 +1,21 @@
+$ grep -n "does not set these variables yet\|Until then the workspace defaults" CHANGELOG.md
+grep-exit=1
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
+claude-staged-grep-exit=1

Delta diff from the previous reviewed tree (empty on the first review): diff --git a/CHANGELOG.md b/CHANGELOG.md
index 559021ac..0c270e93 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -44,7 +44,7 @@ All notable changes to IronClaude are documented in this file.
 
 #### Changed (ccsession tier mode)
 
-- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (`src/superclaude/skills/ccsession-tag/ccsession`), so the plain aliases `opus`, `sonnet` and `haiku` in agent frontmatter, `--model` and the Agent call resolve to the tiers. Outside tier mode the launcher sets none of them. Inside a tier workspace these values replace the real model ids that the workspace defaults file exports for the same variables.
+- In a ccsession tier workspace the launcher now exports `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a`, `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b` and `ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2` (`src/superclaude/skills/ccsession-tag/ccsession`), so the plain aliases `opus`, `sonnet` and `haiku` in agent frontmatter and `--model` resolve to the tiers (the probes did not exercise the Agent-call `model` parameter). Outside tier mode the launcher sets none of them. Inside a tier workspace these values replace the real model ids that the workspace defaults file exports for the same variables.
 - Known limit: the exports do not depend on the owner's tier access. For an owner limited to other tiers, a `model: opus` or `model: sonnet` subagent is sent to a tier the shim refuses. This comes from reading the code, not from a run; see `docs/reference/model-aliases.md`.
 - The pages that said the launcher would set the variables later now say that it does: `docs/reference/model-aliases.md`, `docs/user-guide/brainstorm.md`, `docs/user-guide/commands.md`, `refs/tiers.md` and `refs/chains.md` of the `/sc:issue` protocol, a comment in `src/superclaude/cli/reflect/commands.py` and the docstring of `tests/skills/test_model_alias_policy.py`.
 

Earlier blocking findings of this start (empty on the first review): F1.1 sev=blocking trigger=B4 ac=scope at=CHANGELOG.md:47 anchor="Docs say only what the code and the two probe records show" chk=amiss:n,false:n,harm:n,constraint:y family=docs-overclaim fix=Drop "and the Agent call" from the sentence, or add that the Agent-call model parameter was not exercised in either probe. covers="Docs say only what the code and the two probe records show" first=A1 origin=new: The new entry says the plain aliases "in agent frontmatter, --model and the Agent call resolve to the tiers". Neither probe record exercised the Agent-call model parameter (probe-alias-remap.md:21 and probe-sonnet-alias.md:20 say so), so the claim goes beyond what the code and probe records show.

Saved-probe re-check hit locations (may be empty): src/superclaude/skills/sc-issue-protocol/refs/tiers.md:23
src/superclaude/skills/sc-issue-protocol/refs/tiers.md:24


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
