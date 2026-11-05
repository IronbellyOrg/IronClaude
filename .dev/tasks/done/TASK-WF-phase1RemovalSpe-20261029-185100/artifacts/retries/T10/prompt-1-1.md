2cbb78256fbea5f6fa9f77e15f85cf821d323de8
Review one task for spec compliance.

Task brief: ## Task 10: Drop decorative Serena mentions and frontmatter entries

Depends on: Task 9

Implements ./source.md §8 T9, rule G5 (frontmatter part), rule G10 (lines 21 and 90) and rule M6. Edit every ./source.md §1.2 row whose Task column is `T9`: rows P3, P7, P9, P10, P12, P16, P18, P19, P32, P34-P38, P41, P42, P44-P46, P48, P51 (lines 21 and 90 of `src/superclaude/core/CLAUDE.md` only), P53, P60, P61, P66, P67, P72, P74, P75, P88, P89 (sc-roadmap: the `<output_dir>/.session-memory.md` fallback becomes the only path), S92, S93. Also drop `serena` from the single-line `mcp-servers:` frontmatter of EVERY file in `src/superclaude`, `plugins/superclaude`, `commands` and `agents`, including files whose other rows belong to Tasks 11-15 (for example `src/superclaude/commands/troubleshoot.md:6`, `validate-roadmap.md:7`, `auggie-review.md:6`, `save.md:6`, `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:15`, `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:6`, `commands/sc-brainstorm.md:6`); rule G5 says these lists "simply drop `serena`", so the frontmatter parts of those later rows become no-ops. In tests delete `test_serena_fallback` and `test_serena_referenced` from `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py`, and delete `test_circuit_breaker_for_serena` and reword `:69-74` in `tests/sc-roadmap/integration/test_wave5_completion.py`. No body text may still point at Serena. Commit `docs(primitives): drop decorative Serena mentions and frontmatter entries (#323)`.

Acceptance criteria:
- T10.AC1: `make sync-dev && make verify-sync` passes.
- T10.AC2: `uv run pytest tests/sc-roadmap tests/commands tests/skills tests/core tests/cli/test_how_we_work_install.py -q -p no:cacheprovider` passes.
- T10.AC3: `rg -n --no-ignore 'mcp-servers:.*serena' src/superclaude plugins/superclaude commands agents` prints nothing.

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
Start sha: 2cbb78256fbea5f6fa9f77e15f85cf821d323de8
Diff against the start snapshot: Touched files: 55 tracked files (see the stat); the work is uncommitted in the working tree. Spec: $PKG/source.md section 1.2 rows whose Task column is T9 (grep them: grep -E '^\| (P|S)[0-9]+ .*\| T9 \|$' $PKG/source.md), rule G5 (frontmatter part), rule G10 (lines 21 and 90), rule M6 (section 5), and section 8 T9 (lines 717-723). Observed by the implementer (verify yourself): make sync-dev && make verify-sync passes; the Task 10 pytest command gives 860 passed, 87 skipped; the rg frontmatter check prints nothing. Notes on judgment calls: brainstorm.md line 120 in rows P12/P34 is the word 'onboarding' (a false positive, no Serena), so only the frontmatter changed there; src/superclaude/core/CLAUDE.md:111 'Symbolic queries' row is Task 15's (rule G10, line 112), not this task's; frontmatter lists that held only serena became [] (e.g. 'mcp-servers: []').

 .../progress.md                                     |  1 +
 commands/sc-brainstorm.md                           |  2 +-
 commands/sc-help.md                                 |  4 ----
 commands/sc-load.md                                 |  2 +-
 commands/sc-pm.md                                   |  2 +-
 commands/sc-reflect.md                              |  2 +-
 commands/sc-research.md                             |  3 +--
 commands/sc-save.md                                 |  2 +-
 commands/sc-task.md                                 |  5 ++---
 commands/sc-workflow.md                             |  4 +---
 plugins/superclaude/commands/brainstorm.md          |  2 +-
 plugins/superclaude/commands/load.md                |  2 +-
 plugins/superclaude/commands/pm.md                  |  2 +-
 plugins/superclaude/commands/reflect.md             |  2 +-
 plugins/superclaude/commands/research.md            |  3 +--
 plugins/superclaude/commands/save.md                |  2 +-
 plugins/superclaude/commands/task.md                |  2 +-
 plugins/superclaude/core/RESEARCH_CONFIG.md         |  5 -----
 src/superclaude/commands/adversarial.md             |  2 +-
 src/superclaude/commands/auggie-review.md           |  2 +-
 src/superclaude/commands/brainstorm.md              |  2 +-
 src/superclaude/commands/cleanup-audit.md           |  2 +-
 src/superclaude/commands/cli-eval.md                |  2 +-
 src/superclaude/commands/cli-portify.md             |  2 +-
 src/superclaude/commands/init-lite.md               |  2 +-
 src/superclaude/commands/load.md                    |  2 +-
 src/superclaude/commands/pm.md                      |  2 +-
 src/superclaude/commands/post-release.md            |  2 +-
 src/superclaude/commands/pr-submit.md               |  2 +-
 src/superclaude/commands/reflect.md                 |  2 +-
 src/superclaude/commands/release-split.md           |  2 +-
 src/superclaude/commands/research.md                |  3 +--
 src/superclaude/commands/review-translation.md      |  2 +-
 src/superclaude/commands/save.md                    |  2 +-
 src/superclaude/commands/task.md                    |  2 +-
 src/superclaude/commands/troubleshoot.md            |  2 +-
 src/superclaude/commands/validate-roadmap.md        |  2 +-
 src/superclaude/core/CLAUDE.md                      |  5 ++---
 src/superclaude/core/RESEARCH_CONFIG.md             |  3 +--
 .../skills/sc-adversarial-protocol/SKILL.md         | 19 +++----------------
 .../skills/sc-auggie-review-protocol/SKILL.md       |  2 +-
 .../skills/sc-brainstorm-protocol/SKILL.md          |  2 +-
 .../skills/sc-cleanup-audit-protocol/SKILL.md       |  2 +-
 .../skills/sc-cli-eval-protocol/SKILL.md            |  2 +-
 .../skills/sc-cli-portify-protocol/SKILL.md         |  2 +-
 .../skills/sc-init-lite-protocol/SKILL.md           |  2 +-
 .../skills/sc-post-release-protocol/SKILL.md        |  6 +++---
 .../skills/sc-pr-submit-protocol/SKILL.md           |  2 +-
 src/superclaude/skills/sc-reflect-protocol/SKILL.md |  2 +-
 .../skills/sc-release-split-protocol/SKILL.md       |  2 +-
 src/superclaude/skills/sc-roadmap-protocol/SKILL.md | 21 +++++++++------------
 .../skills/sc-troubleshoot-protocol/SKILL.md        |  2 +-
 .../skills/sc-validate-roadmap-protocol/SKILL.md    |  2 +-
 .../compliance/test_mcp_circuit_breakers.py         | 10 ----------
 .../sc-roadmap/integration/test_wave5_completion.py | 15 +++------------
 55 files changed, 68 insertions(+), 119 deletions(-)

diff --git a/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/progress.md b/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/progress.md
--- a/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/progress.md
+++ b/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/progress.md
@@ -18,3 +18,4 @@ T8: start sha=d556b81ccbc2aaa3c5edfac88041f7985033c46d
 T8: complete verdict=compliant ac=T8.AC1,T8.AC2 evidence=T8.AC1@tests/cli/test_install_hooks.py:682-684,T8.AC2@src/superclaude/hooks/hooks.json:47,notes@./artifacts/retries/T8/notes.md:1-2 extras=lint:pass,typecheck:skip,test:pass files=src/superclaude/hooks/hooks.json,plugins/superclaude/hooks/hooks.json,src/superclaude/hooks/scripts/freshness-pre-edit.sh,plugins/superclaude/hooks/scripts/freshness-pre-edit.sh,tests/cli/test_install_hooks.py,src/superclaude/cli/eval/suites/real.yaml,src/superclaude/cli/eval/coverage.py,src/superclaude/cli/eval/suites/README.md,tests/cli/eval/test_coverage_gate.py
 T9: start sha=0dd559495f95edb68d2cc4e6e4956c7d8e9b5fc0
 T9: complete verdict=compliant ac=T9.AC1,T9.AC2,T9.AC3,T9.AC4 evidence=T9.AC1@tests/cli/test_install_mcp_registry.py:37-45,T9.AC2@src/superclaude/cli/install_mcp.py:1,T9.AC3@src/superclaude/cli/install_mcp.py:1,T9.AC4@./artifacts/issue-comments.md:5,https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6511002768 extras=lint:pass,typecheck:skip,test:pass files=src/superclaude/cli/install_mcp.py,tests/cli/test_install_mcp_registry.py,tests/unit/test_cli_install.py,src/superclaude/mcp/MCP_Auggie.md,src/superclaude/mcp/MCP_Morphllm.md,src/superclaude/mcp/MCP_Tavily.md,plugins/superclaude/mcp/MCP_Morphllm.md,plugins/superclaude/mcp/MCP_Tavily.md
+T10: start sha=2cbb78256fbea5f6fa9f77e15f85cf821d323de8
diff --git a/commands/sc-brainstorm.md b/commands/sc-brainstorm.md
--- a/commands/sc-brainstorm.md
+++ b/commands/sc-brainstorm.md
@@ -3,7 +3,7 @@ name: brainstorm
 description: "Interactive requirements discovery through Socratic dialogue and systematic exploration"
 category: orchestration
 complexity: advanced
-mcp-servers: [context7, magic, playwright, morphllm, serena]
+mcp-servers: [context7, magic, playwright, morphllm]
 personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
 ---
 
diff --git a/commands/sc-help.md b/commands/sc-help.md
--- a/commands/sc-help.md
+++ b/commands/sc-help.md
@@ -40,9 +40,6 @@ Here is a complete list of all available SuperClaude (`/sc:sc`) commands.
 | `/sc:sc:implement` | Feature and code implementation with intelligent persona activation and MCP integration |
 | `/sc:sc:improve` | Apply systematic improvements to code quality, performance, and maintainability |
 | `/sc:sc:index` | Generate comprehensive project documentation and knowledge base with intelligent organization |
-| `/sc:sc:load` | Session lifecycle management with Serena MCP integration for project context loading |
-| `/sc:sc:reflect` | Task reflection and validation using Serena MCP analysis capabilities |
-| `/sc:sc:save` | Session lifecycle management with Serena MCP integration for session context persistence |
 | `/sc:sc:select-tool` | Intelligent MCP tool selection based on complexity scoring and operation analysis |
 | `/sc:sc:spawn` | Meta-system task orchestration with intelligent breakdown and delegation |
 | `/sc:sc:spec-panel` | Multi-expert specification review and improvement using renowned specification and software engineering experts |
@@ -72,7 +69,6 @@ SuperClaude supports behavioral flags to enable specific execution modes and too
 | `--c7` / `--context7` | Library imports, framework questions | Enable Context7 for curated documentation lookup |
 | `--magic` | UI component requests (/ui, /sc:21) | Enable Magic for modern UI generation from 21st.dev |
 | `--morph` / `--morphllm` | Bulk code transformations | Enable Morphllm for efficient multi-file pattern application |
-| `--serena` | Symbol operations, project memory | Enable Serena for semantic understanding and session persistence |
 | `--play` / `--playwright` | Browser testing, E2E scenarios | Enable Playwright for real browser automation and testing |
 | `--all-mcp` | Maximum complexity scenarios | Enable all MCP servers for comprehensive capability |
 | `--no-mcp` | Native-only execution needs | Disable all MCP servers, use native tools |
diff --git a/commands/sc-load.md b/commands/sc-load.md
--- a/commands/sc-load.md
+++ b/commands/sc-load.md
@@ -3,7 +3,7 @@ name: load
 description: "Session lifecycle management with Serena MCP integration for project context loading"
 category: session
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/commands/sc-pm.md b/commands/sc-pm.md
--- a/commands/sc-pm.md
+++ b/commands/sc-pm.md
@@ -3,7 +3,7 @@ name: pm
 description: "Project Manager Agent - Default orchestration agent that coordinates all sub-agents and manages workflows seamlessly"
 category: orchestration
 complexity: meta
-mcp-servers: [context7, magic, playwright, morphllm, serena, tavily, chrome-devtools]
+mcp-servers: [context7, magic, playwright, morphllm, tavily, chrome-devtools]
 personas: [pm-agent]
 ---
 
diff --git a/commands/sc-reflect.md b/commands/sc-reflect.md
--- a/commands/sc-reflect.md
+++ b/commands/sc-reflect.md
@@ -3,7 +3,7 @@ name: reflect
 description: "Task reflection and validation using Serena MCP analysis capabilities"
 category: special
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/commands/sc-research.md b/commands/sc-research.md
--- a/commands/sc-research.md
+++ b/commands/sc-research.md
@@ -3,7 +3,7 @@ name: research
 description: Deep web research with adaptive planning and intelligent search
 category: command
 complexity: advanced
-mcp-servers: [tavily, playwright, serena]
+mcp-servers: [tavily, playwright]
 personas: [deep-research-agent]
 ---
 
@@ -82,7 +82,6 @@ personas: [deep-research-agent]
 ## MCP Integration
 - **Tavily**: Primary search and extraction engine
 - **Playwright**: JavaScript-heavy content extraction
-- **Serena**: Research session persistence
 
 ## Output Standards
 - Save reports to `claudedocs/research_[topic]_[timestamp].md`
diff --git a/commands/sc-save.md b/commands/sc-save.md
--- a/commands/sc-save.md
+++ b/commands/sc-save.md
@@ -3,7 +3,7 @@ name: save
 description: "Session lifecycle management with Serena MCP integration for session context persistence"
 category: session
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/commands/sc-task.md b/commands/sc-task.md
--- a/commands/sc-task.md
+++ b/commands/sc-task.md
@@ -3,7 +3,7 @@ name: task
 description: "Execute complex tasks with intelligent workflow management and delegation"
 category: special
 complexity: advanced
-mcp-servers: [context7, magic, playwright, morphllm, serena]
+mcp-servers: [context7, magic, playwright, morphllm]
 personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
 ---
 
@@ -29,7 +29,7 @@ personas: [architect, analyzer, frontend, backend, security, devops, project-man
 
 Key behaviors:
 - Multi-persona coordination across architect, frontend, backend, security, devops domains
-- Intelligent MCP server routing (Context7, Magic, Playwright, Morphllm, Serena)
+- Intelligent MCP server routing (Context7, Magic, Playwright, Morphllm)
 - Systematic execution with progressive task enhancement and cross-session persistence
 - Advanced task delegation with hierarchical breakdown and dependency management
 
@@ -38,7 +38,6 @@ Key behaviors:
 - **Magic MCP**: UI/UX task coordination and design system integration
 - **Playwright MCP**: Testing workflow integration and validation automation
 - **Morphllm MCP**: Large-scale task transformation and pattern-based optimization
-- **Serena MCP**: Cross-session task persistence and project memory management
 - **Availability fallback**: The MCP servers named here are preferred tooling, not hard requirements — when one is not installed, degrade gracefully (native reasoning, official docs via web lookup in place of Context7, native tools otherwise) instead of routing work to absent servers.
 
 ## Tool Coordination
diff --git a/commands/sc-workflow.md b/commands/sc-workflow.md
--- a/commands/sc-workflow.md
+++ b/commands/sc-workflow.md
@@ -3,7 +3,7 @@ name: workflow
 description: "Generate structured implementation workflows from PRDs and feature requirements"
 category: orchestration
 complexity: advanced
-mcp-servers: [context7, magic, playwright, morphllm, serena]
+mcp-servers: [context7, magic, playwright, morphllm]
 personas: [architect, analyzer, frontend, backend, security, devops, project-manager]
 ---
 
@@ -38,7 +38,6 @@ Key behaviors:
 - **Magic MCP**: UI/UX workflow generation and design system integration strategies
 - **Playwright MCP**: Testing workflow integration and quality assurance automation
 - **Morphllm MCP**: Large-scale workflow transformation and pattern-based optimization
-- **Serena MCP**: Cross-session workflow persistence, memory management, and project context
 - **Availability fallback**: The MCP servers named here are preferred tooling, not hard requirements — when one is not installed, degrade gracefully (native reasoning, official docs via web lookup in place of Context7, native tools otherwise) instead of routing work to absent servers.
 
 ## Tool Coordination
@@ -79,7 +78,6 @@ Key behaviors:
 ### Cross-Session Workflow Management
 ```
 /sc:sc:workflow project-brief.md --depth normal
-# Serena MCP manages cross-session workflow context and persistence
 # Progressive workflow enhancement with memory-driven insights
 ```
 
diff --git a/plugins/superclaude/commands/brainstorm.md b/plugins/superclaude/commands/brainstorm.md
--- a/plugins/superclaude/commands/brainstorm.md
+++ b/plugins/superclaude/commands/brainstorm.md
@@ -3,7 +3,7 @@ name: brainstorm
 description: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge"
 category: orchestration
 complexity: advanced
-mcp-servers: [serena, auggie-mcp, tavily]
+mcp-servers: [auggie-mcp, tavily]
 personas: [architect, analyzer, scribe]
 version: 2.0.0
 spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
diff --git a/plugins/superclaude/commands/load.md b/plugins/superclaude/commands/load.md
--- a/plugins/superclaude/commands/load.md
+++ b/plugins/superclaude/commands/load.md
@@ -3,7 +3,7 @@ name: load
 description: "Session lifecycle management with Serena MCP integration for project context loading"
 category: session
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/plugins/superclaude/commands/pm.md b/plugins/superclaude/commands/pm.md
--- a/plugins/superclaude/commands/pm.md
+++ b/plugins/superclaude/commands/pm.md
@@ -3,7 +3,7 @@ name: pm
 description: "Project Manager Agent - Default orchestration agent that coordinates all sub-agents and manages workflows seamlessly"
 category: orchestration
 complexity: meta
-mcp-servers: [context7, playwright, morphllm, serena, tavily]
+mcp-servers: [context7, playwright, morphllm, tavily]
 personas: [pm-agent]
 ---
 
diff --git a/plugins/superclaude/commands/reflect.md b/plugins/superclaude/commands/reflect.md
--- a/plugins/superclaude/commands/reflect.md
+++ b/plugins/superclaude/commands/reflect.md
@@ -3,7 +3,7 @@ name: reflect
 description: "Tiered reflection protocol — UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate"
 category: analysis
 complexity: advanced
-mcp-servers: [auggie, serena, context7, tavily]
+mcp-servers: [auggie, context7, tavily]
 personas: [analyzer, qa, refactorer]
 version: 2.0.0
 supersedes: .dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md
diff --git a/plugins/superclaude/commands/research.md b/plugins/superclaude/commands/research.md
--- a/plugins/superclaude/commands/research.md
+++ b/plugins/superclaude/commands/research.md
@@ -3,7 +3,7 @@ name: research
 description: Deep web research with adaptive planning and intelligent search
 category: command
 complexity: advanced
-mcp-servers: [tavily, playwright, serena]
+mcp-servers: [tavily, playwright]
 personas: [deep-research-agent]
 ---
 
@@ -97,7 +97,6 @@ Per-tier `search_depth`/`extract_depth` and map/crawl selection are defined by t
 - **Tavily**: Primary search, extraction, site-mapping (`tavily-map`) and domain-crawl (`tavily-crawl`) engine — see deep-research-agent / RESEARCH_CONFIG.md for routing
 - **Sequential**: Complex reasoning and synthesis
 - **Playwright**: JavaScript-heavy content extraction
-- **Serena**: Research session persistence
 
 ## Output Standards
 
diff --git a/plugins/superclaude/commands/save.md b/plugins/superclaude/commands/save.md
--- a/plugins/superclaude/commands/save.md
+++ b/plugins/superclaude/commands/save.md
@@ -3,7 +3,7 @@ name: save
 description: "Session lifecycle management with Serena MCP integration for session context persistence"
 category: session
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/plugins/superclaude/commands/task.md b/plugins/superclaude/commands/task.md
--- a/plugins/superclaude/commands/task.md
+++ b/plugins/superclaude/commands/task.md
@@ -4,7 +4,7 @@ description: "Unified task execution with intelligent workflow management, MCP c
 category: special
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7, serena, playwright, morphllm]
+mcp-servers: [context7, playwright, morphllm]
 personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]
 version: "2.0.0"
 ---
diff --git a/plugins/superclaude/core/RESEARCH_CONFIG.md b/plugins/superclaude/core/RESEARCH_CONFIG.md
--- a/plugins/superclaude/core/RESEARCH_CONFIG.md
+++ b/plugins/superclaude/core/RESEARCH_CONFIG.md
@@ -95,7 +95,6 @@ tool_coordination:
   discovery_primary: tavily
   extraction_smart_routing: true
   reasoning_engine: sequential
-  memory_backend: serena
   parallel_tool_calls: true
 
 quality_gates:
@@ -411,10 +410,6 @@ mcp_integration:
   context7:
     role: technical_docs
     fallback: tavily_search
-    
-  serena:
-    role: memory_management
-    fallback: session_only
 ```
 
 ## Monitoring Metrics
diff --git a/src/superclaude/commands/adversarial.md b/src/superclaude/commands/adversarial.md
--- a/src/superclaude/commands/adversarial.md
+++ b/src/superclaude/commands/adversarial.md
@@ -4,7 +4,7 @@ description: "Structured adversarial debate, comparison, and merge pipeline for
 category: analysis
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7, serena]
+mcp-servers: [context7]
 personas: [architect, analyzer, scribe]
 ---
 
diff --git a/src/superclaude/commands/auggie-review.md b/src/superclaude/commands/auggie-review.md
--- a/src/superclaude/commands/auggie-review.md
+++ b/src/superclaude/commands/auggie-review.md
@@ -3,7 +3,7 @@ name: auggie-review
 description: "Auggie-powered code review for PRs, local diffs, or file snapshots — narrow bugs + architectural risks + anti-patterns, with auto-posted PR review and optional remediation handoff"
 category: quality
 complexity: advanced
-mcp-servers: [serena]
+mcp-servers: []
 personas: [analyzer, architect, security, qa, refactorer]
 argument-hint: "[<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus security,architecture,quality,performance,all] [--depth quick|standard|deep] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer] [--revagent opus|sonnet|haiku|fable]"
 ---
diff --git a/src/superclaude/commands/brainstorm.md b/src/superclaude/commands/brainstorm.md
--- a/src/superclaude/commands/brainstorm.md
+++ b/src/superclaude/commands/brainstorm.md
@@ -3,7 +3,7 @@ name: brainstorm
 description: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge"
 category: orchestration
 complexity: advanced
-mcp-servers: [serena, auggie-mcp, tavily]
+mcp-servers: [auggie-mcp, tavily]
 personas: [architect, analyzer, scribe]
 version: 2.0.0
 spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
diff --git a/src/superclaude/commands/cleanup-audit.md b/src/superclaude/commands/cleanup-audit.md
--- a/src/superclaude/commands/cleanup-audit.md
+++ b/src/superclaude/commands/cleanup-audit.md
@@ -4,7 +4,7 @@ description: "Multi-pass read-only repository audit producing evidence-backed cl
 category: utility
 complexity: high
 allowed-tools: Read, Glob, Grep, Bash, TodoWrite, Task, Write, Skill
-mcp-servers: [serena, context7]
+mcp-servers: [context7]
 personas: [analyzer, architect, devops, qa, refactorer]
 ---
 
diff --git a/src/superclaude/commands/cli-eval.md b/src/superclaude/commands/cli-eval.md
--- a/src/superclaude/commands/cli-eval.md
+++ b/src/superclaude/commands/cli-eval.md
@@ -3,7 +3,7 @@ name: cli-eval
 description: "Manage the cliEval pipeline lifecycle — author a new eval suite (propose→critique→debate→author→validate→document) or interactively select and supervise a run of an existing suite."
 category: testing
 complexity: advanced
-mcp-servers: [context7, serena]
+mcp-servers: [context7]
 personas: [architect, analyzer, qa, scribe]
 ---
 
diff --git a/src/superclaude/commands/cli-portify.md b/src/superclaude/commands/cli-portify.md
--- a/src/superclaude/commands/cli-portify.md
+++ b/src/superclaude/commands/cli-portify.md
@@ -4,7 +4,7 @@ description: "Port inference-based SuperClaude workflows into programmatic CLI p
 category: development
 complexity: high
 allowed-tools: Read, Glob, Grep, Write, Bash, TodoWrite, Skill
-mcp-servers: [serena, context7]
+mcp-servers: [context7]
 personas: [architect, analyzer, backend]
 version: "1.0.0"
 ---
diff --git a/src/superclaude/commands/init-lite.md b/src/superclaude/commands/init-lite.md
--- a/src/superclaude/commands/init-lite.md
+++ b/src/superclaude/commands/init-lite.md
@@ -4,7 +4,7 @@ description: "Safely audit project-local SuperClaude context surfaces and write
 category: utility
 complexity: low
 allowed-tools: Read, Glob, Grep, Bash, Skill
-mcp-servers: [serena]
+mcp-servers: []
 personas: [analyzer]
 version: "1.0.0"
 ---
diff --git a/src/superclaude/commands/load.md b/src/superclaude/commands/load.md
--- a/src/superclaude/commands/load.md
+++ b/src/superclaude/commands/load.md
@@ -3,7 +3,7 @@ name: load
 description: "Session lifecycle management with Serena MCP integration for project context loading"
 category: session
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/src/superclaude/commands/pm.md b/src/superclaude/commands/pm.md
--- a/src/superclaude/commands/pm.md
+++ b/src/superclaude/commands/pm.md
@@ -3,7 +3,7 @@ name: pm
 description: "Project Manager Agent - Default orchestration agent that coordinates all sub-agents and manages workflows seamlessly"
 category: orchestration
 complexity: meta
-mcp-servers: [context7, playwright, morphllm, serena, tavily]
+mcp-servers: [context7, playwright, morphllm, tavily]
 personas: [pm-agent]
 ---
 
diff --git a/src/superclaude/commands/post-release.md b/src/superclaude/commands/post-release.md
--- a/src/superclaude/commands/post-release.md
+++ b/src/superclaude/commands/post-release.md
@@ -4,7 +4,7 @@ description: "Post-release follow-through: synchronize and create a shipped vers
 category: documentation
 complexity: high
 allowed-tools: Read, Glob, Grep, Skill
-mcp-servers: [serena]
+mcp-servers: []
 personas: [scribe, devops, qa, analyzer]
 ---
 
diff --git a/src/superclaude/commands/pr-submit.md b/src/superclaude/commands/pr-submit.md
--- a/src/superclaude/commands/pr-submit.md
+++ b/src/superclaude/commands/pr-submit.md
@@ -3,7 +3,7 @@ name: pr-submit
 description: "Open a PR on the fork and arm an in-session PR-review auto-remediation monitor — poll for the Augment review, re-grade + verify findings, dispatch verified ones to /sc:troubleshoot, then (at higher --monitor ordinals) fix, validate, push, reply, and resolve under a capped monotonic round counter."
 category: quality
 complexity: advanced
-mcp-servers: [serena, auggie]
+mcp-servers: [auggie]
 personas: [analyzer, architect, security, qa, devops]
 argument-hint: "[--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--output-dir <dir>] [--resume <run-log.jsonl>]"
 version: "1.0"
diff --git a/src/superclaude/commands/reflect.md b/src/superclaude/commands/reflect.md
--- a/src/superclaude/commands/reflect.md
+++ b/src/superclaude/commands/reflect.md
@@ -3,7 +3,7 @@ name: reflect
 description: "Tiered reflection protocol — UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate"
 category: analysis
 complexity: advanced
-mcp-servers: [auggie, serena, context7, tavily]
+mcp-servers: [auggie, context7, tavily]
 personas: [analyzer, qa, refactorer]
 version: 2.0.0
 supersedes: .dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md
diff --git a/src/superclaude/commands/release-split.md b/src/superclaude/commands/release-split.md
--- a/src/superclaude/commands/release-split.md
+++ b/src/superclaude/commands/release-split.md
@@ -4,7 +4,7 @@ description: "Neutral two-phase release split analysis with adversarial validati
 category: planning
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7, serena]
+mcp-servers: [context7]
 personas: [architect, analyzer, scribe]
 ---
 
diff --git a/src/superclaude/commands/research.md b/src/superclaude/commands/research.md
--- a/src/superclaude/commands/research.md
+++ b/src/superclaude/commands/research.md
@@ -3,7 +3,7 @@ name: research
 description: Deep web research with adaptive planning and intelligent search
 category: command
 complexity: advanced
-mcp-servers: [tavily, playwright, serena]
+mcp-servers: [tavily, playwright]
 personas: [deep-research-agent]
 ---
 
@@ -97,7 +97,6 @@ Per-tier `search_depth`/`extract_depth` and map/crawl selection are defined by t
 - **Tavily**: Primary search, extraction, site-mapping (`tavily-map`) and domain-crawl (`tavily-crawl`) engine — see deep-research-agent / RESEARCH_CONFIG.md for routing
 - **Native reasoning**: Complex reasoning and synthesis
 - **Playwright**: JavaScript-heavy content extraction
-- **Serena**: Research session persistence
 
 ## Output Standards
 
diff --git a/src/superclaude/commands/review-translation.md b/src/superclaude/commands/review-translation.md
--- a/src/superclaude/commands/review-translation.md
+++ b/src/superclaude/commands/review-translation.md
@@ -3,7 +3,7 @@ name: review-translation
 description: "Systematic localization review with adversarial validation, real-world evidence search, and comprehensive quality scoring"
 category: orchestration
 complexity: advanced
-mcp-servers: [tavily, context7, serena]
+mcp-servers: [tavily, context7]
 personas: [localization-reviewer, linguistic-validator, cultural-consultant, research-analyst]
 ---
 
diff --git a/src/superclaude/commands/save.md b/src/superclaude/commands/save.md
--- a/src/superclaude/commands/save.md
+++ b/src/superclaude/commands/save.md
@@ -3,7 +3,7 @@ name: save
 description: "Session lifecycle management with Serena MCP integration for session context persistence"
 category: session
 complexity: standard
-mcp-servers: [serena]
+mcp-servers: []
 personas: []
 ---
 
diff --git a/src/superclaude/commands/task.md b/src/superclaude/commands/task.md
--- a/src/superclaude/commands/task.md
+++ b/src/superclaude/commands/task.md
@@ -4,7 +4,7 @@ description: "Unified task execution with intelligent workflow management, MCP c
 category: special
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7, serena, playwright, morphllm]
+mcp-servers: [context7, playwright, morphllm]
 personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]
 version: "2.0.0"
 ---
diff --git a/src/superclaude/commands/troubleshoot.md b/src/superclaude/commands/troubleshoot.md
--- a/src/superclaude/commands/troubleshoot.md
+++ b/src/superclaude/commands/troubleshoot.md
@@ -3,7 +3,7 @@ name: troubleshoot
 description: "Tiered debugging — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in remediation chain (sc:workflow → sc:implement; task-builder → /task with --depth deep)"
 category: analysis
 complexity: advanced
-mcp-servers: [auggie, serena, context7, tavily]
+mcp-servers: [auggie, context7, tavily]
 personas: [analyzer, performance, security, qa, refactorer, devops]
 argument-hint: "[<issue description>] [--type bug|build|performance|deployment|security|test] [--depth quick|standard|deep] [--scope <path|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-doc-discovery] [--no-mcp] [--context <path>] [--caller <name>]"
 ---
diff --git a/src/superclaude/commands/validate-roadmap.md b/src/superclaude/commands/validate-roadmap.md
--- a/src/superclaude/commands/validate-roadmap.md
+++ b/src/superclaude/commands/validate-roadmap.md
@@ -4,7 +4,7 @@ description: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, e
 category: analysis
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern, mcp__serena__activate_project
-mcp-servers: [auggie, serena]
+mcp-servers: [auggie]
 personas: [analyzer, architect, qa]
 ---
 
diff --git a/src/superclaude/core/CLAUDE.md b/src/superclaude/core/CLAUDE.md
--- a/src/superclaude/core/CLAUDE.md
+++ b/src/superclaude/core/CLAUDE.md
@@ -18,7 +18,6 @@ uv run python script.py          # execute scripts
 | Server         | Primary Use                                  | Flag (advisory) |
 |----------------|----------------------------------------------|-----------------|
 | auggie         | Codebase search — call before significant edits | (auto)  |
-| serena         | Symbol navigation, project memory            | --serena   |
 | context7       | Official library/framework docs              | --c7       |
 | tavily         | Web search, current information              | --tavily   |
 | playwright     | Browser automation, E2E testing              | --play     |
@@ -87,8 +86,8 @@ Treat the following as **mandatory re-verification triggers** before
 output:
 
 - **S1.** About to cite `file:line` or "at line N" of a specific file.
-- **S2.** About to issue an Edit / Write / replace_content / replace_symbol_body
-  / insert_*_symbol against a file. (Hook enforces; mention here for completeness.)
+- **S2.** About to issue an Edit / Write against a file. (Hook enforces; mention
+  here for completeness.)
 - **S3.** About to assert that file A agrees or disagrees with file B.
 - **S4.** About to quote an IP, hostname, credential ID, port, path, or
   config value tied to a specific source file.
diff --git a/src/superclaude/core/RESEARCH_CONFIG.md b/src/superclaude/core/RESEARCH_CONFIG.md
--- a/src/superclaude/core/RESEARCH_CONFIG.md
+++ b/src/superclaude/core/RESEARCH_CONFIG.md
@@ -23,7 +23,7 @@ hop_configuration: {max_depth: 5, timeout: 60s, parallel: true, loop_detection:
 confidence_scoring: {relevance: 0.5, completeness: 0.5, min: 0.6, target: 0.8}
 self_reflection: {frequency: after_each_hop, triggers: [low_confidence, contradictions, 80%_time, user_intervention]}
 memory: {case_reasoning: true, pattern_learning: true, session_persistence: true, retention: 30d}
-tools: {discovery: tavily, routing: smart, memory: serena, parallel: true}
+tools: {discovery: tavily, routing: smart, parallel: true}
 quality_gates: {planning: [objectives, strategy, criteria], execution: min_confidence=0.6, synthesis: coherence+clarity}
 extraction: {strategy: selective, screenshots: contextual, js_rendering: auto, timeout: 15s}
 ```
@@ -139,4 +139,3 @@ Server fallbacks are in the table below. Research-specific: low_confidence → r
 | tavily | primary search | native websearch |
 | playwright | complex extraction | tavily extraction |
 | context7 | technical docs | tavily search |
-| serena | memory management | session only |
diff --git a/src/superclaude/skills/sc-adversarial-protocol/SKILL.md b/src/superclaude/skills/sc-adversarial-protocol/SKILL.md
--- a/src/superclaude/skills/sc-adversarial-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-adversarial-protocol/SKILL.md
@@ -9,7 +9,7 @@ allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
 <!-- Extended metadata (for documentation, not parsed):
 category: analysis
 complexity: advanced
-mcp-servers: [context7, serena]
+mcp-servers: [context7]
 personas: [architect, analyzer, scribe]
 -->
 
@@ -488,7 +488,6 @@ return_contract:
 | Server | Usage | Steps |
 |--------|-------|-------|
 | Native reasoning | Debate scoring, convergence analysis, refactoring plan logic | Steps 2-4 |
-| Serena | Memory persistence of adversarial outcomes | Step 5 |
 | Context7 | Domain pattern validation during merge | Step 5 |
 
 **Circuit breaker**: Use native Claude reasoning with depth reduction (deep → standard, standard → quick) if analysis depth exceeds budget.
@@ -2240,18 +2239,6 @@ mcp_integration:
     steps: "Steps 2-4"
     depth_reduction: "deep → standard, standard → quick"
 
-  serena:
-    usage: "Memory persistence of adversarial outcomes"
-    steps: "Step 5 (post-merge)"
-    data_persisted:
-      - "Pipeline configuration and outcome summary"
-      - "Scoring results for cross-session learning"
-      - "Error patterns for improvement"
-    circuit_breaker:
-      failure_threshold: 4
-      timeout: "45s"
-      fallback: "Skip persistence, log warning"
-
   context7:
     usage: "Domain pattern validation during merge"
     steps: "Step 5 (merge validation)"
@@ -2274,7 +2261,7 @@ framework_registration:
     entry: |
       **`/sc:adversarial [options]`** — Structured adversarial debate, comparison, and merge pipeline (wave-enabled, complex profile)
       - **Auto-Persona**: Architect, Analyzer, Scribe
-      - **MCP**: Serena (persistence), Context7 (validation); native reasoning for debate scoring
+      - **MCP**: Context7 (validation); native reasoning for debate scoring
       - **Tools**: [Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task]
 
   orchestrator_md:
@@ -2282,7 +2269,7 @@ framework_registration:
       pattern: "adversarial debate"
       complexity: "complex"
       domain: "analysis"
-      auto_activates: "architect + analyzer personas, --ultrathink, Serena"
+      auto_activates: "architect + analyzer personas, --ultrathink"
       confidence: "95%"
 
     additional_entries:
diff --git a/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md b/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
--- a/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-auggie-review-protocol/SKILL.md
@@ -7,7 +7,7 @@ allowed-tools: Read, Grep, Glob, Bash(auggie *), Bash(gh *), Bash(git *), Bash(j
 <!-- Extended metadata (for documentation, not parsed):
 category: quality
 complexity: advanced
-mcp-servers: [serena, auggie]
+mcp-servers: [auggie]
 personas: [analyzer, architect, security, qa, refactorer]
 -->
 
diff --git a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
--- a/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
@@ -12,7 +12,7 @@ argument-hint: "<topic> [--proposals N] [--depth quick|standard|deep] [--strateg
 <!-- Extended metadata (for documentation, not parsed):
 category: orchestration
 complexity: advanced
-mcp-servers: [serena, auggie-mcp, tavily]
+mcp-servers: [auggie-mcp, tavily]
 personas: [architect, analyzer, scribe]
 version: 2.0.0
 spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
diff --git a/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md b/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
--- a/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md
@@ -3,7 +3,7 @@ name: sc:cleanup-audit-protocol
 description: "Multi-pass read-only repository audit producing evidence-backed cleanup recommendations"
 category: utility
 complexity: high
-mcp-servers: [serena, context7]
+mcp-servers: [context7]
 personas: [analyzer, architect, devops, qa, refactorer]
 allowed-tools: Read, Grep, Glob, Bash(git *), Bash(wc *), Bash(find *), Bash(du *), TodoWrite, Task, Write
 argument-hint: "[target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]"
diff --git a/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md b/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
--- a/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cli-eval-protocol/SKILL.md
@@ -8,7 +8,7 @@ argument-hint: "create|run [--name <stem>] [--from @<spec>] [--suite <name>] [--
 <!-- Extended metadata (for documentation, not parsed):
 category: testing
 complexity: advanced
-mcp-servers: [context7, serena]
+mcp-servers: [context7]
 personas: [architect, analyzer, qa, scribe]
 version: 1.0.0
 -->
diff --git a/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md b/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md
--- a/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md
@@ -4,7 +4,7 @@ description: "Full behavioral protocol for sc:cli-portify — port inference-bas
 category: development
 complexity: high
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task
-mcp-servers: [serena, context7, auggie-mcp]
+mcp-servers: [context7, auggie-mcp]
 personas: [architect, analyzer, backend]
 argument-hint: "--workflow <skill-name-or-path> [--name <cli-name>] [--output <dir>] [--dry-run]"
 ---
diff --git a/src/superclaude/skills/sc-init-lite-protocol/SKILL.md b/src/superclaude/skills/sc-init-lite-protocol/SKILL.md
--- a/src/superclaude/skills/sc-init-lite-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-init-lite-protocol/SKILL.md
@@ -10,7 +10,7 @@ argument-hint: "--context-optimized [--project-root <dir>] [--output <path>] [--
 <!-- Extended metadata (for documentation, not parsed):
 category: utility
 complexity: low
-mcp-servers: [serena]
+mcp-servers: []
 personas: [analyzer]
 version: 1.0.0
 -->
diff --git a/src/superclaude/skills/sc-post-release-protocol/SKILL.md b/src/superclaude/skills/sc-post-release-protocol/SKILL.md
--- a/src/superclaude/skills/sc-post-release-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-post-release-protocol/SKILL.md
@@ -8,7 +8,7 @@ argument-hint: "<version> — an existing release tag (e.g. v1.4.1). Optional: -
 <!-- Extended metadata (for documentation, not parsed):
 category: documentation
 complexity: high
-mcp-servers: [serena]
+mcp-servers: []
 personas: [scribe, devops, qa, analyzer]
 -->
 
@@ -241,7 +241,7 @@ This protocol emits two HTML-comment header blocks (style follows `sc-auggie-rev
 **Field sources.**
 
 - `caller` — the slash command that invoked this skill: `/sc:post-release` if invoked directly; the parent skill name if invoked from another skill; `none` if invoked interactively without a slash command.

diff --git a/tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py b/tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py
index 5ca72b2d..c9e8f5ac 100644
--- a/tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py
+++ b/tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py
@@ -30,12 +30,6 @@ class TestCircuitBreakerConfiguration:
 class TestFallbackBehavior:
     """Verify fallback behavior for MCP operations."""
 
-    def test_serena_fallback(self, skill_md_content):
-        """Serena memory persistence should have fallback."""
-        # SKILL.md should define what happens if Serena is unavailable
-        lower = skill_md_content.lower()
-        assert "fallback" in lower or "circuit" in lower
-
     def test_template_fallback_to_inline(self, skill_md_content):
         """Template discovery should fallback to inline generation."""
         assert "inline" in skill_md_content.lower()
@@ -74,10 +68,6 @@ class TestMCPServerReferences:
         """SKILL.md should reference Context7 MCP server."""
         assert "Context7" in skill_md_content or "context7" in skill_md_content
 
-    def test_serena_referenced(self, skill_md_content):
-        """SKILL.md should reference Serena MCP server."""
-        assert "Serena" in skill_md_content or "serena" in skill_md_content
-
     def test_mcp_integration_section(self, skill_md_content):
         """SKILL.md should have an MCP Integration section."""
         assert "MCP Integration" in skill_md_content or "## MCP" in skill_md_content
diff --git a/tests/sc-roadmap/integration/test_wave5_completion.py b/tests/sc-roadmap/integration/test_wave5_completion.py
index f1b8dd83..c01a6883 100644
--- a/tests/sc-roadmap/integration/test_wave5_completion.py
+++ b/tests/sc-roadmap/integration/test_wave5_completion.py
@@ -66,20 +66,11 @@ class TestValidationStatusFlow:
 
 
 class TestMemoryPersistence:
-    """Test Serena memory persistence from SKILL.md T5.5."""
+    """Test session-memory persistence from SKILL.md T5.5."""
 
     def test_memory_persistence_in_skill_md(self, skill_md_content):
-        """SKILL.md should define memory persistence behavior."""
-        assert (
-            "write_memory" in skill_md_content or "memory" in skill_md_content.lower()
-        )
-
-    def test_circuit_breaker_for_serena(self, skill_md_content):
-        """SKILL.md should define circuit breaker for Serena."""
-        assert (
-            "circuit" in skill_md_content.lower()
-            or "fallback" in skill_md_content.lower()
-        )
+        """SKILL.md should define session-memory persistence behavior."""
+        assert ".session-memory.md" in skill_md_content
 
 
 class TestGitOperations:
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
