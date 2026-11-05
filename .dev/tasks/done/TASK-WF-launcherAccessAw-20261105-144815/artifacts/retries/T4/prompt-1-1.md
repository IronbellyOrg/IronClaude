e206be639e4ffce144de8514b7ea33a8f241e93e
Review one task for spec compliance.

Task brief: ## Task 4: Update the pages and comments that say the launcher sets all three variables

Depends on: Task 3

Covers R-007 for the pointer pages.

Where each of these now says that in a ccsession tier workspace the launcher sets the variables, say that it sets each variable for a tier the owner may use (the alias of a tier the owner may not use keeps its inherited value): `docs/user-guide/brainstorm.md` (the `--models` row), `docs/user-guide/commands.md` (the `--agents` spec line near line 860), `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` (item 4 about the `haiku` alias: the launcher sets it to `claude-gw-tier2` when the owner may use tier2), `src/superclaude/skills/sc-issue-protocol/refs/chains.md` (the brainstorm model list bullet), the comment above `_DEFAULT_MODEL` in `src/superclaude/cli/reflect/commands.py` (comment text only, and it must not contain the text `claude-gw-tier`), and the docstring of `tests/skills/test_model_alias_policy.py` (docstring only, no assertion change). Use `grep -rn "launcher sets" src docs tests` to find them and report any other line that still says the launcher sets all three unconditionally.

Acceptance criteria:
- The grep above lists no line that says the launcher sets all three variables without the owner-access condition.
- `uv run pytest tests/skills/test_model_alias_policy.py tests/skills/test_issue_protocol.py` passes and `git diff` of `src/superclaude/cli/reflect/commands.py` shows comment lines only.

AC ids (in source order):
T4.AC1: The grep above lists no line that says the launcher sets all three variables without the owner-access condition.
T4.AC2: `uv run pytest tests/skills/test_model_alias_policy.py tests/skills/test_issue_protocol.py` passes and `git diff` of `src/superclaude/cli/reflect/commands.py` shows comment lines only.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `models.py`, `local-gateway-alias-proxy.py` and `ccsession-orca` stay untouched (R-002).
- The three unconditional export lines from the first follow-up already sit right after `USE_SHIM=1` in the tier-mode branch of `src/superclaude/skills/ccsession-tag/ccsession` (about lines 867-870); re-read the file before editing and change only those lines (R-001).
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the probe records show; no probe exercised the Agent-call `model` parameter.
- R-008 (the pull request body) changes no file and has no task; it is written when the pull request is opened. R-004 has no launcher-level test because a broken access entry makes the launcher exit before Claude starts (`apply_tier_selection`, `|| exit 2`).
Start sha: e206be639e4ffce144de8514b7ea33a8f241e93e
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
index ca2c8bac..0fe11631 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
@@ -23,7 +23,7 @@ Verified against the Claude Code subagent docs (`https://code.claude.com/docs/en
 1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main session's model.
 2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the frontmatter.
 3. Frontmatter `model:` accepts an alias, a full model ID (the same values as the `--model` flag) or `inherit`.
-4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace the launcher sets that variable to `claude-gw-tier2` (`docs/reference/model-aliases.md`); outside one it follows the inherited `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Either way, "spawn with haiku" does not guarantee the T3 tier.
+4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace the launcher sets that variable to `claude-gw-tier2` when the owner may use tier2 (`docs/reference/model-aliases.md`); otherwise, and outside a tier workspace, it follows the inherited `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Either way, "spawn with haiku" does not guarantee the T3 tier.
 
 So each tier has its own agent file whose `model:` is the picker ID, and the spawn passes only `subagent_type`.
 

diff --git a/src/superclaude/skills/sc-issue-protocol/refs/chains.md b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
index c4eca776..09127580 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/chains.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
@@ -18,7 +18,7 @@ These are the default rows passed to `/sc:recommend` as the suggested route. `/s
 Notes:
 - `--depth quick` with `--fix` is a STOP in `/sc:troubleshoot`, so the simple bug row has no `--fix` and hands the report to `/sc:implement` (issue body: "Hand the output directly off ... /sc:implement").
 - `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
-- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. In a ccsession tier workspace the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`, so the aliases map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; outside one they keep Claude Code's meaning (`docs/reference/model-aliases.md`). The session tier itself is pinned by the `/model` line (default D25).
+- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. In a ccsession tier workspace the launcher sets each `ANTHROPIC_DEFAULT_*_MODEL` for a tier the owner may use, so those aliases map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; an alias for a tier the owner may not use keeps its inherited value, and outside a tier workspace the aliases keep Claude Code's meaning (`docs/reference/model-aliases.md`). The session tier itself is pinned by the `/model` line (default D25).
 - `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.
 
 No brainstorm step carries a handoff flag: the tasklist handoff feeds `/sc:tasklist`, not `/sc:workflow`, and the design handoff only prints a suggestion (B11), so `/sc:workflow` and `/sc:design` run as their own steps.

diff --git a/docs/user-guide/brainstorm.md b/docs/user-guide/brainstorm.md
index e5b49299..9339e5af 100644
--- a/docs/user-guide/brainstorm.md
+++ b/docs/user-guide/brainstorm.md
@@ -49,7 +49,7 @@ A topic string. File references via `@<path>` are supported. Empty topic STOPs t
 | `--codebase` / `--no-codebase` | auto | Force or skip codebase enrichment. Auto-detects for `code`/`architecture`/`incident` domains. |
 | `--research` | auto | `light` (Tavily), `deep` (`tech-research` skill), `none`. |
 | `--personas` | auto | Override domain-aware persona selection with a literal comma list. |
-| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (`ANTHROPIC_DEFAULT_*_MODEL` env vars override them; unset ones use Claude Code's built-in models). In a ccsession tier workspace the launcher sets those variables, so `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; see [model-aliases](../reference/model-aliases.md). |
+| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (`ANTHROPIC_DEFAULT_*_MODEL` env vars override them; unset ones use Claude Code's built-in models). In a ccsession tier workspace the launcher sets each of those variables for a tier the owner may use, so the matching aliases `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`, and an alias for a tier the owner may not use keeps its inherited value; see [model-aliases](../reference/model-aliases.md). |
 | `--blind` | `false` | Strip model identity before scoring (prevents model bias). |
 | `--convergence` | `0.75` | Adversarial convergence threshold for PASS routing. |
 | `--interactive` | `false` | Pause for user input at Socratic + adversarial decision points. |

diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index b3d41b6c..e5dec5b8 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -857,7 +857,7 @@ The command hands its arguments to the `sc-validate-roadmap-protocol` skill, whi
 
 - Runs a depth-tiered Socratic dialogue → `seed-brief.md`
 - Auto-routes codebase + research enrichment (`/sc:analyze`, `/sc:research`, `tech-research`)
-- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`, so `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; see [model-aliases](../reference/model-aliases.md))
+- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace the launcher sets each `ANTHROPIC_DEFAULT_*_MODEL` for a tier the owner may use, so the matching aliases `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; see [model-aliases](../reference/model-aliases.md))
 - Delegates to `/sc:adversarial` for N parallel proposals + debate + merge → `merged-requirements.md`
 - Optionally hands off to `/sc:design`, `/sc:tasklist`, or `/task-builder`
 

diff --git a/src/superclaude/cli/reflect/commands.py b/src/superclaude/cli/reflect/commands.py
index 97986743..faa31357 100644
--- a/src/superclaude/cli/reflect/commands.py
+++ b/src/superclaude/cli/reflect/commands.py
@@ -30,8 +30,9 @@ import click
 # this value. (Flagged decision -- see Task Log.)
 # The default is the plain alias ``opus``, not a dated model id: Claude Code
 # resolves it, and inside a ccsession tier workspace the launcher sets
-# ``ANTHROPIC_DEFAULT_OPUS_MODEL``, which maps it to a tier model
-# (see docs/reference/model-aliases.md). ``ANTHROPIC_MODEL`` still takes
+# ``ANTHROPIC_DEFAULT_OPUS_MODEL`` when the owner may use that tier, which
+# maps it to a tier model (see docs/reference/model-aliases.md).
+# ``ANTHROPIC_MODEL`` still takes
 # precedence in the ``reflect run`` command when it is set.
 _DEFAULT_MODEL = "opus"
 

diff --git a/tests/skills/test_model_alias_policy.py b/tests/skills/test_model_alias_policy.py
index 4b50a1de..5d8c31b2 100644
--- a/tests/skills/test_model_alias_policy.py
+++ b/tests/skills/test_model_alias_policy.py
@@ -3,10 +3,10 @@
 These tests check, at the points each test names, that the agent, command and
 skill files and the Python package under ``src/superclaude`` use the plain aliases
 ``opus``, ``sonnet`` and ``haiku`` (or ``inherit`` in frontmatter), apart from the
-allow-lists below. In tier mode the launcher sets ``ANTHROPIC_DEFAULT_*_MODEL``,
-so the aliases map to tier models inside a ccsession tier workspace; outside one
-the workspace defaults file exports real model ids for them. See
-``docs/reference/model-aliases.md``.
+allow-lists below. In tier mode the launcher sets each ``ANTHROPIC_DEFAULT_*_MODEL``
+for a tier the owner may use, so those aliases map to tier models inside a
+ccsession tier workspace; otherwise the workspace defaults file's real model ids
+apply. See ``docs/reference/model-aliases.md``.
 
 Enforcement type: STATIC (file text and ast). The allow-lists below are the
 documented exceptions; every entry carries its reason.

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t4-checks.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t4-checks.log
new file mode 100644
index 00000000..1a320b2e
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t4-checks.log
@@ -0,0 +1,22 @@
+$ grep -rn "launcher sets" src docs tests (excluding docs/generated, docs/swarm, docs/testing)
+src/superclaude/cli/reflect/commands.py:32:# resolves it, and inside a ccsession tier workspace the launcher sets
+src/superclaude/skills/sc-issue-protocol/refs/tiers.md:26:4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace the launcher sets that variable to `claude-gw-tier2` whe
+src/superclaude/skills/sc-issue-protocol/refs/chains.md:21:- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. 
+docs/user-guide/commands.md:860:- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace the launcher sets each `ANTHROPIC_DEFAULT_*_MODEL` for a tier the
+docs/user-guide/brainstorm.md:52:| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (`ANTHROPIC_DEFAULT_*_MODEL` env vars override them; unset ones use Claude Code's built-in models). I
+docs/reference/model-aliases.md:22:Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets each variable only when the workspace owner may use its tier, so for an owner who may use all
+docs/reference/model-aliases.md:38:Outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's meaning.
+tests/skills/test_model_alias_policy.py:6:allow-lists below. In tier mode the launcher sets each ``ANTHROPIC_DEFAULT_*_MODEL``
+--- unconditional wording check (expect none): lines that say the launcher sets all three / the variables without the owner condition
+unconditional-grep-exit=1
+$ git diff -U0 $start -- src/superclaude/cli/reflect/commands.py (changed lines)
+--- a/src/superclaude/cli/reflect/commands.py
++++ b/src/superclaude/cli/reflect/commands.py
+-# ``ANTHROPIC_DEFAULT_OPUS_MODEL``, which maps it to a tier model
+-# (see docs/reference/model-aliases.md). ``ANTHROPIC_MODEL`` still takes
++# ``ANTHROPIC_DEFAULT_OPUS_MODEL`` when the owner may use that tier, which
++# maps it to a tier model (see docs/reference/model-aliases.md).
++# ``ANTHROPIC_MODEL`` still takes
+$ ruff
+All checks passed!
+2 files already formatted

diff --git a/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t4-tests.log b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t4-tests.log
new file mode 100644
index 00000000..a43bb90d
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherAccessAw-20261105-144815/artifacts/t4-tests.log
@@ -0,0 +1,78 @@
+============================= test session starts ==============================
+platform linux -- Python 3.11.15, pytest-9.2.0, pluggy-1.7.0
+SuperClaude: 5.0.0
+benchmark: 5.3.1 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
+rootdir: /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases
+configfile: pyproject.toml
+plugins: superclaude-5.0.0, benchmark-5.3.1, anyio-4.16.0, cov-7.1.0
+collected 680 items
+
+tests/skills/test_model_alias_policy.py .............                    [  1%]
+tests/skills/test_issue_protocol.py .................................... [  7%]
+..........................................                               [ 13%]
+tests/skills/test_issue_worker_agents.py ............................... [ 17%]
+......................................                                   [ 23%]
+tests/skills/test_worker_contract.py ................................... [ 28%]
+........................................................................ [ 39%]
+........................................................................ [ 49%]
+......................................................................   [ 60%]
+tests/cli/reflect/test_base_precedence.py ......                         [ 61%]
+tests/cli/reflect/test_classify_fix.py ...........                       [ 62%]
+tests/cli/reflect/test_claudeprocess_reflect_children_restricted.py .... [ 63%]
+.                                                                        [ 63%]
+tests/cli/reflect/test_cli_smoke.py ............                         [ 65%]
+tests/cli/reflect/test_contract_fallback_metadata.py ........            [ 66%]
+tests/cli/reflect/test_contract_status_cli.py ........                   [ 67%]
+tests/cli/reflect/test_docs_cli_parity.py ..                             [ 67%]
+tests/cli/reflect/test_ensemble_fallback_engage.py ...                   [ 68%]
+tests/cli/reflect/test_ensemble_fallback_stub.py ............            [ 70%]
+tests/cli/reflect/test_ensemble_stub_integration.py ...............      [ 72%]
+tests/cli/reflect/test_ensemble_unit.py ..........................       [ 76%]
+tests/cli/reflect/test_fallback_classify.py ......                       [ 76%]
+tests/cli/reflect/test_fallback_config.py .....                          [ 77%]
+tests/cli/reflect/test_fallback_plan.py .............                    [ 79%]
+tests/cli/reflect/test_fallback_select.py ..........                     [ 81%]
+tests/cli/reflect/test_fallback_slot_factory.py ..                       [ 81%]
+tests/cli/reflect/test_fix_loop.py .........                             [ 82%]
+tests/cli/reflect/test_grader_yaml_root.py .                             [ 82%]
+tests/cli/reflect/test_isolate_reviewers_cli.py .......                  [ 83%]
+tests/cli/reflect/test_marker_suppression.py ......                      [ 84%]
+tests/cli/reflect/test_no_nesting_guard.py X.....                        [ 85%]
+tests/cli/reflect/test_preflight_phase_complete.py ........              [ 86%]
+tests/cli/reflect/test_promote_plumbing.py .........                     [ 88%]
+tests/cli/reflect/test_remediation_route_table.py ....                   [ 88%]
+tests/cli/reflect/test_remediation_source_template.py .....              [ 89%]
+tests/cli/reflect/test_reviewer_brief_constraints.py ...                 [ 89%]
+tests/cli/reflect/test_reviewer_finding_parity.py .....                  [ 90%]
+tests/cli/reflect/test_reviewer_isolation_gate.py ....                   [ 91%]
+tests/cli/reflect/test_reviewer_readonly_tools.py .....                  [ 91%]
+tests/cli/reflect/test_reviewer_swarm_target_grounding.py ..             [ 92%]
+tests/cli/reflect/test_runner_e2e.py ..........                          [ 93%]
+tests/cli/reflect/test_verdict_mapping.py .............................. [ 98%]
+......                                                                   [ 98%]
+tests/cli/reflect/test_verify_denylist_git_mutations.py ...              [ 99%]
+tests/cli/reflect/test_writeback.py ....                                 [100%]
+
+=============================== warnings summary ===============================
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_runs_without_tasklist
+  /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/tests/cli/reflect/test_contract_status_cli.py:90: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem():
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_does_not_launch_reflect_audit_machinery
+  /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/tests/cli/reflect/test_contract_status_cli.py:109: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem():
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_validate_does_not_write_lock_by_default
+  /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/tests/cli/reflect/test_contract_status_cli.py:133: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem() as fs:
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_output_is_metadata_only
+  /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/tests/cli/reflect/test_contract_status_cli.py:157: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem():
+
+tests/cli/reflect/test_contract_status_cli.py::test_contract_status_validate_output_redacts_raw_payload_body
+  /home/coder/workspaces/worktrees/IronClaude/issue-384-launcher-tier-aliases/tests/cli/reflect/test_contract_status_cli.py:259: DeprecationWarning: 'isolated_filesystem' is deprecated and will be removed in Click 9.0. Use 'tempfile.TemporaryDirectory' or pytest's 'tmp_path' fixture with absolute paths instead.
+    with cli_runner.isolated_filesystem() as fs:
+
+-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
+================== 679 passed, 1 xpassed, 5 warnings in 3.78s ==================

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
