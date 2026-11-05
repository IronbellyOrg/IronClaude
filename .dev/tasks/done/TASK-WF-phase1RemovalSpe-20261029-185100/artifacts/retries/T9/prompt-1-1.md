0dd559495f95edb68d2cc4e6e4956c7d8e9b5fc0
Review one task for spec compliance.

Task brief: ## Task 9: Remove the Serena registry entry and MCP package assets

Depends on: Task 8

Implements ./source.md §8 T8 and rows S32-S36, S41, S46-S51, S88, S100. Delete the Serena registry block and uv advisory in `src/superclaude/cli/install_mcp.py` (`:55-61`, `:561-570`); delete `src/superclaude/mcp/MCP_Serena.md`, `src/superclaude/mcp/configs/serena.json`, `src/superclaude/mcp/configs/serena-docker.json` and the same three under `plugins/superclaude/mcp/`; delete the Serena lines in `src/superclaude/mcp/MCP_Auggie.md`, `MCP_Morphllm.md`, `MCP_Tavily.md` and `plugins/superclaude/mcp/MCP_Morphllm.md`, `MCP_Tavily.md`; delete the Serena entries in `tests/cli/test_install_mcp_registry.py` (both dicts) and add `"serena"` to the `test_removed_mcp_servers_are_not_in_registry` tuple; remove the three names from `tests/unit/test_cli_install.py:150-153` and `:423-425` in the same commit as the deletions. Commit `feat(mcp)!: remove Serena from the MCP registry and package assets (#323)`, then post the G2 issue-#323 comment.

Acceptance criteria:
- T9.AC1: `uv run pytest tests/cli/test_install_mcp_registry.py tests/cli/test_install_mcp_tavily.py tests/cli/test_install_mcp_cli.py tests/unit/test_cli_install.py tests/cli/test_update_command.py -q -p no:cacheprovider` passes.
- T9.AC2: `rg -n -i serena src/superclaude/cli/install_mcp.py src/superclaude/mcp plugins/superclaude/mcp tests/unit/test_cli_install.py` prints nothing.
- T9.AC3: `uv run superclaude mcp --servers serena --dry-run 2>&1 | grep -q 'Unknown MCP server selection: serena'` succeeds.
- T9.AC4: The G2 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

`$PKG` = /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100 (repo root: the git top-level of that directory). The source spec for anything the brief says is in `$PKG/source.md`; the plan is `$PKG/TASK-WF-phase1RemovalSpe-20261029-185100.md`.

Global constraints (plan `## Constraints`, verbatim):
- Work on branch `ironbelly/feat-codememory-codegraph-init`, base commit `55d40308`. Do not open a pull request to `master` for Phase 1 alone and do not push to `upstream`; Phases 1 and 2 merge as one unit (./source.md §2.2, D9).
- `$PKG` in every command below means this package's directory as the executor resolves it at run time (the folder that holds this plan); never hardcode it. Evidence goes under `$PKG/artifacts/`; handoff notes for other repos go under `$PKG/handoffs/`.
- One commit per task, conventional commit message as given in each task, ending with the attribution line the executor's session requires. Every commit stages the task package with `git add .dev/tasks` (package, `progress.md` and `artifacts/` included). Never stage or commit `.claude/` content (only `.claude/settings.json` is tracked, and Phase 1 does not touch it). Never use `git add -f` on a `.claude/` path.
- Every edit to a `src/superclaude/...` primitive is mirrored by hand, in the same commit, in its `plugins/superclaude/...` twin and its root `commands/sc-*.md` / `agents/sc-*.md` copy where ./source.md §1.2 lists one (D15).
- After editing `src/superclaude/core/HOW-WE-WORK.md`, copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md`.
- Use `uv run` for Python; standalone scripts run with `uv run --no-project python -I`. Every pytest run uses `-p no:cacheprovider`. Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` is not rewritten. After every test run, `git status --short` must list only files the task intends to change; restore any tracked file a test changed.
- Test baseline: the full suite already has failures at the base (W1 saw 27 failed and 16 errors). "Passes" for a targeted command means no failing test id that is not in `$PKG/artifacts/baseline/full.txt` (compare with the `comm -13` form in Task 18); never assume a clean suite.
- Never run the real `./update.sh`, `superclaude install` (including `--list`) or `claude mcp add/remove` against the real `HOME`; every environment check runs in a sandbox `HOME` made with `mktemp -d` (./source.md §10, D8). Never delete user data (`~/.serena`, project `.serena/` folders outside this repo, `~/.cache/codebase-memory-mcp`). Never edit another repository.
- Progress reporting (./source.md §9): at the end of each task group (Phases 1-6 below, i.e. groups G0-G5) post exactly one comment on issue #323 of the fork, and only there. First run `gh repo view --json nameWithOwner -q .nameWithOwner` (must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude`), then `gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result>. Decisions logged: <count, path in task package>. Next: <next group>."`. Never use a bare `gh issue comment` and never `--repo SuperClaude-Org/...`. If `gh` is unauthenticated or fails, record the exact error and the intended body in `$PKG/progress.md` and continue (not a blocker).
- Decision rules (./source.md §10), never stop to ask the user: a simple decision (one obvious option, or one the source already constrains) is made by the executor and logged as one line in `$PKG/decisions.md` (decision, options, method `self`, rationale). A mid-level decision (two or more viable options with real trade-offs inside one task) writes each option to `$PKG/decisions/<task>-<slug>/option-<x>.md`, spawns an agent that runs `/sc:adversarial --compare <option files> --depth quick`, follows its recommendation and logs method `adversarial quick` with the merged-recommendation path. A complex decision (an architectural change to the source's design: retire-step scope, memory store layout, merge order, deleting a file the source keeps) does the same with `/sc:adversarial --compare <option files>` (standard depth) and logs method `adversarial full`.
- A blocked task stays blocked with its reason in `$PKG/progress.md`; continue with tasks that do not depend on it. If a task's acceptance fails, fix it within the task's files; if the fix needs a file another task owns, pull that edit forward and log it in `$PKG/decisions.md`. A task may not need a later task to go green.
- Scope limits (./source.md §2.1, §2.3): existing `.dev/` files outside `$PKG` are never edited; the only other `.dev/` writes are the new files `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` and `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`, and each task that writes one stages that exact file (`git add <path>`, never the folder). No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh`; those are handed off, not removed by Phase 1.
- This plan was corrected after an advisory `/sc:reflect --mode pre` review (`.dev/codegraph-migration/review/F1-result.md`). Where a task's text here differs from `./source.md`, the task text wins.
- Human actions the executor must not attempt: merging Phases 1 and 2 to `master` (Phase 2's PR via `/sc:pr-submit`) and running the real `./update.sh` on a live workspace after that merge (Phase 2 owns that live check).
Start sha: 0dd559495f95edb68d2cc4e6e4956c7d8e9b5fc0
Diff against the start snapshot: Work is already committed as HEAD 09a7ed64 (git show --stat HEAD). Touched files: src/superclaude/cli/install_mcp.py, src/superclaude/mcp/{MCP_Auggie,MCP_Morphllm,MCP_Tavily}.md, plugins/superclaude/mcp/{MCP_Morphllm,MCP_Tavily}.md, tests/cli/test_install_mcp_registry.py, tests/unit/test_cli_install.py, and six deleted files (MCP_Serena.md, configs/serena.json, configs/serena-docker.json under src/superclaude/mcp and plugins/superclaude/mcp). Spec: $PKG/source.md section 8 T8 (lines 710-715). Observed by the implementer (verify yourself): the Task 9 pytest command gives 155 passed, 1 skipped; the rg check prints nothing; 'uv run superclaude mcp --servers serena --dry-run' prints 'Unknown MCP server selection: serena' (this is read-only: dry-run with an unknown server name). The G2 comment is https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6511002768, recorded at $PKG/artifacts/issue-comments.md:5. PENDING LEDGER WRITE appended to $PKG/progress.md only if this review passes (the ledger is append-only): a 'T9: complete verdict=compliant ac=T9.AC1,T9.AC2,T9.AC3,T9.AC4 evidence=...,https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6511002768,T9.AC4@./artifacts/issue-comments.md:5 ...' line (the ledger accepts no free text, so the URL goes into the complete line evidence; decision 1 in $PKG/decisions.md).


    feat(mcp)!: remove Serena from the MCP registry and package assets (#323)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 .../artifacts/retries/T9/q0-head                   |  1 +
 .../progress.md                                    |  1 +
 plugins/superclaude/mcp/MCP_Morphllm.md            |  3 --
 plugins/superclaude/mcp/MCP_Serena.md              | 36 ----------------------
 plugins/superclaude/mcp/MCP_Tavily.md              |  2 --
 plugins/superclaude/mcp/configs/serena-docker.json | 14 ---------
 plugins/superclaude/mcp/configs/serena.json        | 18 -----------
 src/superclaude/cli/install_mcp.py                 | 17 ----------
 src/superclaude/mcp/MCP_Auggie.md                  |  3 --
 src/superclaude/mcp/MCP_Morphllm.md                |  6 ----
 src/superclaude/mcp/MCP_Serena.md                  | 35 ---------------------
 src/superclaude/mcp/MCP_Tavily.md                  |  2 --
 src/superclaude/mcp/configs/serena-docker.json     | 14 ---------
 src/superclaude/mcp/configs/serena.json            | 18 -----------
 tests/cli/test_install_mcp_registry.py             | 20 +-----------
 tests/unit/test_cli_install.py                     |  7 ++---
 16 files changed, 6 insertions(+), 191 deletions(-)
commit 09a7ed64b8928f3aef509493cbe262a34950a6e4
Author: coder <coder@coder.local>
Date:   Thu Oct 29 23:31:59 2026 +0000

    feat(mcp)!: remove Serena from the MCP registry and package assets (#323)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/src/superclaude/cli/install_mcp.py b/src/superclaude/cli/install_mcp.py
index 750bd395..0cb8569b 100644
--- a/src/superclaude/cli/install_mcp.py
+++ b/src/superclaude/cli/install_mcp.py
@@ -52,13 +52,6 @@ MCP_SERVERS = {
         "command": "npx -y @playwright/mcp@latest",
         "required": False,
     },
-    "serena": {
-        "name": "serena",
-        "description": "Semantic code analysis and intelligent editing",
-        "transport": "stdio",
-        "command": "uvx --from serena-agent==1.7.0 serena start-mcp-server --context claude-code --project-from-cwd --enable-web-dashboard false --enable-gui-log-window false",
-        "required": False,
-    },
     "morphllm-fast-apply": {
         "name": "morphllm-fast-apply",
         "description": "Fast Apply capability for context-aware code modifications",
@@ -530,16 +523,6 @@ def check_prerequisites(
                 )
         except (OSError, subprocess.SubprocessError):
             errors.append("Docker readiness failed for AIRIS MCP Gateway")
-    if "serena" in selected:
-        # Retain the existing optional uv advisory, but only for its consumer.
-        try:
-            result = _run_command(
-                ["uv", "--version"], capture_output=True, text=True, timeout=10
-            )
-            if result is None or result.returncode != 0:
-                click.echo("uv not found - required to run Serena MCP server", err=True)
-        except (OSError, subprocess.SubprocessError):
-            click.echo("uv not found - required to run Serena MCP server", err=True)
     return not errors, errors
 
 
diff --git a/tests/cli/test_install_mcp_registry.py b/tests/cli/test_install_mcp_registry.py
index 242713fa..84a6c33f 100644
--- a/tests/cli/test_install_mcp_registry.py
+++ b/tests/cli/test_install_mcp_registry.py
@@ -10,11 +10,6 @@ from superclaude.cli import install_mcp
 
 def test_updated_mcp_registry_commands_are_pinned_and_stable():
     expected = {
-        "serena": (
-            "uvx --from serena-agent==1.7.0 serena start-mcp-server "
-            "--context claude-code --project-from-cwd "
-            "--enable-web-dashboard false --enable-gui-log-window false"
-        ),
         "morphllm-fast-apply": "npx -y @morphllm/morphmcp",
         "auggie": "auggie --mcp --mcp-auto-workspace",
     }
@@ -40,6 +35,7 @@ def test_removed_mcp_servers_are_not_in_registry():
         "magic",
         "chrome-devtools",
         "codebase-memory-mcp",
+        "serena",
     ):
         assert name not in install_mcp.MCP_SERVERS
 
@@ -47,23 +43,9 @@ def test_removed_mcp_servers_are_not_in_registry():
 def test_distributable_mcp_templates_match_pinned_registry_commands():
     root = Path(__file__).resolve().parents[2]
     expected = {
-        "serena.json": [
-            "--from",
-            "serena-agent==1.7.0",
-            "serena",
-            "start-mcp-server",
-            "--context",
-            "claude-code",
-            "--project-from-cwd",
-            "--enable-web-dashboard",
-            "false",
-            "--enable-gui-log-window",
-            "false",
-        ],
         "morphllm.json": ["-y", "@morphllm/morphmcp"],
     }
     server_names = {
-        "serena.json": "serena",
         "morphllm.json": "morphllm-fast-apply",
     }
 
diff --git a/tests/unit/test_cli_install.py b/tests/unit/test_cli_install.py
index 0e2f41ba..94d2e7b7 100644
--- a/tests/unit/test_cli_install.py
+++ b/tests/unit/test_cli_install.py
@@ -147,10 +147,9 @@ scripts/sc-recommend-phase0.sh
     "mcp": _names(
         """
 MCP_Airis-Agent.md MCP_Auggie.md MCP_Context7.md MCP_Mindbase.md MCP_Morphllm.md
-MCP_Playwright.md MCP_Serena.md MCP_Tavily.md __init__.py configs/__init__.py
+MCP_Playwright.md MCP_Tavily.md __init__.py configs/__init__.py
 configs/airis-agent.json configs/auggie.json configs/context7.json
 configs/mindbase.json configs/morphllm.json configs/playwright.json
-configs/serena-docker.json configs/serena.json
 """
     ),
     "modes": _names(
@@ -420,9 +419,9 @@ scripts/freshness-user-prompt.sh
     ),
     "mcp": _names(
         """
-MCP_Context7.md MCP_Morphllm.md MCP_Playwright.md MCP_Serena.md MCP_Tavily.md
+MCP_Context7.md MCP_Morphllm.md MCP_Playwright.md MCP_Tavily.md
 __init__.py configs/__init__.py configs/context7.json configs/morphllm.json
-configs/playwright.json configs/serena-docker.json configs/serena.json
+configs/playwright.json
 """
     ),
     "modes": _names(
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

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
