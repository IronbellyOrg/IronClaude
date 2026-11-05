e719a20a36404668d78b4c7236e1adcf5b19283b
Review one task for spec compliance.

Task brief: ## Task 4: Update the pages and comments that say "once the launcher sets"

Depends on: Task 3

Change the future-tense wording to present tense (the launcher sets the variables in a ccsession tier workspace) in these places, and nowhere else: `src/superclaude/skills/sc-issue-protocol/refs/tiers.md` (item 4 of the list about the `haiku` alias: drop "once the launcher sets that variable" and "until then it follows the value in the workspace defaults file"; outside a tier workspace it follows the inherited `ANTHROPIC_DEFAULT_HAIKU_MODEL`), `src/superclaude/skills/sc-issue-protocol/refs/chains.md` (the brainstorm model list bullet), `docs/user-guide/brainstorm.md` (the `--models` row), `docs/user-guide/commands.md` (the `--agents` spec line near line 849), the comment above `_DEFAULT_MODEL` in `src/superclaude/cli/reflect/commands.py` (comment text only, no code change) and the module docstring of `tests/skills/test_model_alias_policy.py` (docstring only, no assertion change). Run `grep -rn "launcher sets\|once the launcher" src docs tests` afterwards and fix any other hit that describes the launcher change as pending, except in `.dev/`.

Acceptance criteria:
- The grep above returns no line that describes the launcher export as future work.
- `uv run pytest tests/skills/test_model_alias_policy.py` still passes and `git diff` of `src/superclaude/cli/reflect/commands.py` shows comment lines only.

AC ids (in source order):
T4.AC1: The grep above returns no line that describes the launcher export as future work.
T4.AC2: `uv run pytest tests/skills/test_model_alias_policy.py` still passes and `git diff` of `src/superclaude/cli/reflect/commands.py` shows comment lines only.
Global constraints: ## Constraints

- Only `src/superclaude/skills/ccsession-tag/ccsession` changes under `src/superclaude/skills/ccsession-tag/`; `ccsession-orca` stays untouched.
- Re-verify every line number in the source against the code on the working branch before editing: the source numbers are at base commit 38eb3c58 and the #315 change edits the same files.
- Do not stage `.claude/`. Edit only under `src/`, `tests/`, `docs/` and `CHANGELOG.md`.
- Docs say only what the code and the two probe records show: the probe record is `.dev/issues/384/analysis/probe-alias-remap.md` (opus and haiku) and `.dev/issues/384/analysis/probe-sonnet-alias.md` (sonnet).
Start sha: e719a20a36404668d78b4c7236e1adcf5b19283b
Diff against the start snapshot: diff --git a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
index 1ea25d58..ca2c8bac 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/tiers.md
@@ -23,7 +23,7 @@ Verified against the Claude Code subagent docs (`https://code.claude.com/docs/en
 1. Claude Code resolves a subagent's model in this order: the Agent call's `model` parameter, then the agent file's `model:` frontmatter, then `CLAUDE_CODE_SUBAGENT_MODEL`, then the main session's model.
 2. The Agent call's `model` parameter accepts only the aliases `sonnet`, `opus`, `haiku`, `fable`. It cannot carry a picker ID, and if passed it overrides the frontmatter.
 3. Frontmatter `model:` accepts an alias, a full model ID (the same values as the `--model` flag) or `inherit`.
-4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace it resolves to `claude-gw-tier2` once the launcher sets that variable (`docs/reference/model-aliases.md`); until then it follows the value in the workspace defaults file. Either way, "spawn with haiku" does not guarantee the T3 tier.
+4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace the launcher sets that variable to `claude-gw-tier2` (`docs/reference/model-aliases.md`); outside one it follows the inherited `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Either way, "spawn with haiku" does not guarantee the T3 tier.
 
 So each tier has its own agent file whose `model:` is the picker ID, and the spawn passes only `subagent_type`.
 

diff --git a/src/superclaude/skills/sc-issue-protocol/refs/chains.md b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
index 0e118443..c4eca776 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/chains.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/chains.md
@@ -18,7 +18,7 @@ These are the default rows passed to `/sc:recommend` as the suggested route. `/s
 Notes:
 - `--depth quick` with `--fix` is a STOP in `/sc:troubleshoot`, so the simple bug row has no `--fix` and hands the report to `/sc:implement` (issue body: "Hand the output directly off ... /sc:implement").
 - `/sc:troubleshoot --depth deep` STOPs on a description under 10 words without `--scope`; the rows always pass `--scope`.
-- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. In a ccsession tier workspace the aliases map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2` once the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`; outside one they keep Claude Code's meaning (`docs/reference/model-aliases.md`). The session tier itself is pinned by the `/model` line (default D25).
+- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; the brainstorm rows use these defaults. In a ccsession tier workspace the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`, so the aliases map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; outside one they keep Claude Code's meaning (`docs/reference/model-aliases.md`). The session tier itself is pinned by the `/model` line (default D25).
 - `/sc:design --type` is chosen per issue by `/sc:recommend` from the four values the command accepts.
 
 No brainstorm step carries a handoff flag: the tasklist handoff feeds `/sc:tasklist`, not `/sc:workflow`, and the design handoff only prints a suggestion (B11), so `/sc:workflow` and `/sc:design` run as their own steps.

diff --git a/docs/user-guide/brainstorm.md b/docs/user-guide/brainstorm.md
index d4dab8cb..e5b49299 100644
--- a/docs/user-guide/brainstorm.md
+++ b/docs/user-guide/brainstorm.md
@@ -49,7 +49,7 @@ A topic string. File references via `@<path>` are supported. Empty topic STOPs t
 | `--codebase` / `--no-codebase` | auto | Force or skip codebase enrichment. Auto-detects for `code`/`architecture`/`incident` domains. |
 | `--research` | auto | `light` (Tavily), `deep` (`tech-research` skill), `none`. |
 | `--personas` | auto | Override domain-aware persona selection with a literal comma list. |
-| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (`ANTHROPIC_DEFAULT_*_MODEL` env vars override them; unset ones use Claude Code's built-in models). In a ccsession tier workspace `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2` once the launcher sets those variables; see [model-aliases](../reference/model-aliases.md). |
+| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (`ANTHROPIC_DEFAULT_*_MODEL` env vars override them; unset ones use Claude Code's built-in models). In a ccsession tier workspace the launcher sets those variables, so `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; see [model-aliases](../reference/model-aliases.md). |
 | `--blind` | `false` | Strip model identity before scoring (prevents model bias). |
 | `--convergence` | `0.75` | Adversarial convergence threshold for PASS routing. |
 | `--interactive` | `false` | Pause for user input at Socratic + adversarial decision points. |

diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index a0d00b97..b3d41b6c 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -857,7 +857,7 @@ The command hands its arguments to the `sc-validate-roadmap-protocol` skill, whi
 
 - Runs a depth-tiered Socratic dialogue → `seed-brief.md`
 - Auto-routes codebase + research enrichment (`/sc:analyze`, `/sc:research`, `tech-research`)
-- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2` once the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`; see [model-aliases](../reference/model-aliases.md))
+- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace the launcher sets `ANTHROPIC_DEFAULT_*_MODEL`, so `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; see [model-aliases](../reference/model-aliases.md))
 - Delegates to `/sc:adversarial` for N parallel proposals + debate + merge → `merged-requirements.md`
 - Optionally hands off to `/sc:design`, `/sc:tasklist`, or `/task-builder`
 

diff --git a/src/superclaude/cli/reflect/commands.py b/src/superclaude/cli/reflect/commands.py
index c3cea35c..97986743 100644
--- a/src/superclaude/cli/reflect/commands.py
+++ b/src/superclaude/cli/reflect/commands.py
@@ -29,8 +29,8 @@ import click
 # Tier-2 reviewer diversity comes from the ``ANTHROPIC_DEFAULT_*`` aliases, not
 # this value. (Flagged decision -- see Task Log.)
 # The default is the plain alias ``opus``, not a dated model id: Claude Code
-# resolves it, and inside a ccsession tier workspace it maps to a tier model once
-# the launcher sets ``ANTHROPIC_DEFAULT_OPUS_MODEL``
+# resolves it, and inside a ccsession tier workspace the launcher sets
+# ``ANTHROPIC_DEFAULT_OPUS_MODEL``, which maps it to a tier model
 # (see docs/reference/model-aliases.md). ``ANTHROPIC_MODEL`` still takes
 # precedence in the ``reflect run`` command when it is set.
 _DEFAULT_MODEL = "opus"

diff --git a/tests/skills/test_model_alias_policy.py b/tests/skills/test_model_alias_policy.py
index bff9c481..4b50a1de 100644
--- a/tests/skills/test_model_alias_policy.py
+++ b/tests/skills/test_model_alias_policy.py
@@ -3,10 +3,10 @@
 These tests check, at the points each test names, that the agent, command and
 skill files and the Python package under ``src/superclaude`` use the plain aliases
 ``opus``, ``sonnet`` and ``haiku`` (or ``inherit`` in frontmatter), apart from the
-allow-lists below. Once the launcher sets ``ANTHROPIC_DEFAULT_*_MODEL`` in tier
-mode (a follow-up change after the #315 pull request), the aliases map to tier
-models inside a ccsession tier workspace; today the workspace defaults file
-exports real model ids for them. See ``docs/reference/model-aliases.md``.
+allow-lists below. In tier mode the launcher sets ``ANTHROPIC_DEFAULT_*_MODEL``,
+so the aliases map to tier models inside a ccsession tier workspace; outside one
+the workspace defaults file exports real model ids for them. See
+``docs/reference/model-aliases.md``.
 
 Enforcement type: STATIC (file text and ast). The allow-lists below are the
 documented exceptions; every entry carries its reason.

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t4-checks.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t4-checks.log
new file mode 100644
index 00000000..1e6190ed
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t4-checks.log
@@ -0,0 +1,21 @@
+$ grep -rn "launcher sets\|once the launcher" src docs tests (excluding .dev)
+src/superclaude/cli/reflect/commands.py:32:# resolves it, and inside a ccsession tier workspace the launcher sets
+src/superclaude/skills/sc-issue-protocol/refs/tiers.md:26:4. The `haiku` alias follows `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Inside a ccsession tier workspace the launcher set
+src/superclaude/skills/sc-issue-protocol/refs/chains.md:21:- The brainstorm model list defaults to `opus,sonnet,haiku`, rotated across proposals, and takes aliases only; 
+docs/user-guide/commands.md:860:- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace the launcher sets `ANTHRO
+docs/user-guide/brainstorm.md:52:| `--models` | `opus,sonnet,haiku` | Model aliases rotated across proposals (`ANTHROPIC_DEFAULT_*_MODEL` env vars override them; unset on
+docs/reference/model-aliases.md:22:Owner decision of 2026-11-05: inside a ccsession tier workspace the launcher sets the three variables, so the aliases resolve as follow
+docs/reference/model-aliases.md:38:Outside a ccsession tier workspace the launcher sets none of the three variables, so `opus`, `sonnet` and `haiku` keep Claude Code's me
+tests/skills/test_model_alias_policy.py:6:allow-lists below. In tier mode the launcher sets ``ANTHROPIC_DEFAULT_*_MODEL``,
+--- future-tense check (expect none):
+future-grep-exit=1
+$ git diff src/superclaude/cli/reflect/commands.py (added/removed lines)
+--- a/src/superclaude/cli/reflect/commands.py
++++ b/src/superclaude/cli/reflect/commands.py
+-# resolves it, and inside a ccsession tier workspace it maps to a tier model once
+-# the launcher sets ``ANTHROPIC_DEFAULT_OPUS_MODEL``
++# resolves it, and inside a ccsession tier workspace the launcher sets
++# ``ANTHROPIC_DEFAULT_OPUS_MODEL``, which maps it to a tier model
+$ ruff
+All checks passed!
+2 files already formatted

diff --git a/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t4-tests.log b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t4-tests.log
new file mode 100644
index 00000000..f49af550
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-launcherFollowup-20261105-131531/artifacts/t4-tests.log
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
+================== 679 passed, 1 xpassed, 5 warnings in 4.01s ==================

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
