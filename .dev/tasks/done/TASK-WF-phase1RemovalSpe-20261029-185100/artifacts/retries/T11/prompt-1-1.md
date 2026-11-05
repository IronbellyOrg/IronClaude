1bafb585b42d4b05bf018a1379a20c8521df05b9
Review one task for spec compliance.

Task brief: ## Task 11: Move save, load, pm and pm-agent memory to `.superclaude/memory` files

Depends on: Task 10

Implements ./source.md §5 rules M1-M4, M7, M8 and §8 T10a. Rows P1, P4, P5, P8 (root `commands/sc-load.md`, `commands/sc-pm.md`, `commands/sc-save.md`, `agents/sc-pm-agent.md`), P11, P13, P14, P17, P23 (`plugins/superclaude/agents/pm-agent.md`, `plugins/superclaude/commands/{load,pm,save}.md`, `plugins/superclaude/modes/MODE_Task_Management.md`), P27, P39, P40, P47, P57 (`src/superclaude/agents/pm-agent.md`, `src/superclaude/commands/{load,pm,save}.md`, `src/superclaude/modes/MODE_Task_Management.md`) and P73 (`src/superclaude/skills/sc-pm-protocol/SKILL.md`, kept with `/sc:pm` because `src/superclaude/commands/pm.md:52` loads it). Store `<git top-level>/.superclaude/memory/<key>.md`; tool mapping write_memory -> Write, read_memory -> Read, list_memories -> Glob, edit_memory -> Edit, no primitive deletes memories; first write creates `<project>/.superclaude/.gitignore` containing `*` when absent; single-owner keys overwritten whole, parallel-session keys written as `<key>-<session-or-timestamp>.md`; `/sc:load` reads `.serena/memories/<key>.md` only when the new file is absent, for one release, never writes there, and says it is read-only history (the one allowlisted sentence per copy). Commit `feat(memory)!: move save, load, pm and pm-agent memory to .superclaude/memory files (#323)`.

Acceptance criteria:
- T11.AC1: `make sync-dev && make verify-sync` passes and `uv run pytest tests/commands tests/skills tests/core -q -p no:cacheprovider` passes.
- T11.AC2: `rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory|think_about_|\bsummarize_changes\b|activate_project|check_onboarding_performed|prepare_for_new_conversation|get_current_config' src/superclaude/commands/save.md src/superclaude/commands/load.md src/superclaude/commands/pm.md plugins/superclaude/commands/save.md plugins/superclaude/commands/load.md plugins/superclaude/commands/pm.md commands/sc-save.md commands/sc-load.md commands/sc-pm.md src/superclaude/agents/pm-agent.md plugins/superclaude/agents/pm-agent.md agents/sc-pm-agent.md src/superclaude/modes/MODE_Task_Management.md plugins/superclaude/modes/MODE_Task_Management.md src/superclaude/skills/sc-pm-protocol/SKILL.md` prints nothing.
- T11.AC3: `rg --files-without-match '\.superclaude/\.gitignore' src/superclaude/commands/save.md src/superclaude/agents/pm-agent.md src/superclaude/skills/sc-pm-protocol/SKILL.md src/superclaude/modes/MODE_Task_Management.md` prints nothing (rule M3 in every writer).

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
Start sha: 1bafb585b42d4b05bf018a1379a20c8521df05b9
Diff against the start snapshot: Touched files: 15 tracked files (stat below), uncommitted in the working tree. Spec: $PKG/source.md section 5 rules M1-M4, M7, M8 (lines 408-423) and section 8 T10a (lines 727-735), plus the plan's Task 11 text. The rewrite was done by a helper agent; judge the files on disk. Observed by the implementer (verify yourself): the three AC rg commands (listed in the AC text) print nothing; the only 'serena' hits in the 15 files are the single M7 sentence in each of src/superclaude/commands/load.md:43, plugins/superclaude/commands/load.md:43 and commands/sc-load.md:38; make sync-dev && make verify-sync passes; uv run pytest tests/commands tests/skills tests/core gives 631 passed. Decision 5 in $PKG/decisions.md records the plan-key unification.

 agents/sc-pm-agent.md                             | 64 ++++++++++------------
 commands/sc-load.md                               | 35 ++++++------
 commands/sc-pm.md                                 | 54 +++++++++----------
 commands/sc-save.md                               | 26 ++++-----
 plugins/superclaude/agents/pm-agent.md            | 64 ++++++++++------------
 plugins/superclaude/commands/load.md              | 35 ++++++------
 plugins/superclaude/commands/pm.md                |  4 +-
 plugins/superclaude/commands/save.md              | 26 ++++-----
 plugins/superclaude/modes/MODE_Task_Management.md | 66 +++++++++++------------
 src/superclaude/agents/pm-agent.md                | 64 ++++++++++------------
 src/superclaude/commands/load.md                  | 35 ++++++------
 src/superclaude/commands/pm.md                    |  4 +-
 src/superclaude/commands/save.md                  | 26 ++++-----
 src/superclaude/modes/MODE_Task_Management.md     | 66 +++++++++++------------
 src/superclaude/skills/sc-pm-protocol/SKILL.md    | 30 ++++++-----
 15 files changed, 294 insertions(+), 305 deletions(-)

Source copies diff (twins in plugins/ and commands/ agents/ carry the equivalent edits; read them with git diff):
diff --git a/src/superclaude/commands/load.md b/src/superclaude/commands/load.md
--- a/src/superclaude/commands/load.md
+++ b/src/superclaude/commands/load.md
@@ -1,6 +1,6 @@
 ---
 name: load
-description: "Session lifecycle management with Serena MCP integration for project context loading"
+description: "Session lifecycle management with memory files for project context loading"
 category: session
 complexity: standard
 mcp-servers: []
@@ -13,7 +13,7 @@ personas: []
 
 - Session initialization and project context loading requests
 - Cross-session persistence and memory retrieval needs
-- Project activation and context management requirements
+- Project context and memory management requirements
 - Session lifecycle management and checkpoint loading scenarios
 
 ## Usage
@@ -24,35 +24,36 @@ personas: []
 
 ## Behavioral Flow
 
-1. **Initialize**: Establish Serena MCP connection and session context management
+1. **Initialize**: Resolve the project root and locate the `.superclaude/memory/` store
 2. **Discover**: Analyze project structure and identify context loading requirements
-3. **Load**: Retrieve project memories, checkpoints, and cross-session persistence data
-4. **Activate**: Establish project context and prepare for development workflow
+3. **Load**: Retrieve project memories, checkpoints, and cross-session persistence data from the memory files
+4. **Establish**: Establish project context and prepare for development workflow
 5. **Validate**: Ensure loaded context integrity and session readiness
 
 Key behaviors:
 
-- Serena MCP integration for memory management and cross-session persistence
-- Project activation with comprehensive context loading and validation
+- Markdown memory files under `.superclaude/memory/` for cross-session persistence
+- Project context loading with comprehensive validation
 - Performance-critical operation with <500ms initialization target
 - Session lifecycle management with checkpoint and memory coordination
 
-## MCP Integration
+## Memory Store
 
-- **Serena MCP**: Mandatory integration for project activation, memory retrieval, and session management
+- **Location**: `<project>/.superclaude/memory/<key>.md`, flat markdown with subfolders for topics. `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree
+- **Legacy fallback**: For one release, `/sc:load` reads `.serena/memories/<key>.md` only when `.superclaude/memory/<key>.md` is absent, never writes there, and tells the user that folder is read-only history
 - **Memory Operations**: Cross-session persistence, checkpoint loading, and context restoration
 - **Performance Critical**: <200ms for core operations, <1s for checkpoint creation
 
 ## Tool Coordination
 
-- **activate_project**: Core project activation and context establishment
-- **list_memories/read_memory**: Memory retrieval and session context loading
+- **Glob** `.superclaude/memory/**/*.md`: List the available memories
+- **Read**: Memory retrieval and session context loading from `.superclaude/memory/<key>.md`
 - **Read/Grep/Glob**: Project structure analysis and configuration discovery
 - **Write**: Session context documentation and checkpoint creation
 
 ## Key Patterns
 
-- **Project Activation**: Directory analysis → memory retrieval → context establishment
+- **Project Context Loading**: Directory analysis → memory retrieval → context establishment
 - **Session Restoration**: Checkpoint loading → context validation → workflow preparation
 - **Memory Management**: Cross-session persistence → context continuity → development efficiency
 - **Performance Critical**: Fast initialization → immediate productivity → session readiness
@@ -63,7 +64,7 @@ Key behaviors:
 
 ```
 /sc:load
-# Loads current directory project context with Serena memory integration
+# Loads current directory project context from .superclaude/memory/
 # Establishes session context and prepares for development workflow
 ```
 
@@ -72,7 +73,7 @@ Key behaviors:
 ```
 /sc:load /path/to/project --type project --analyze
 # Loads specific project with comprehensive analysis
-# Activates project context and retrieves cross-session memories
+# Establishes project context and retrieves cross-session memories
 ```
 
 ### Checkpoint Restoration
@@ -95,12 +96,12 @@ Key behaviors:
 
 **Will:**
 
-- Load project context using Serena MCP integration for memory management
+- Load project context from the `.superclaude/memory/` markdown files
 - Provide session lifecycle management with cross-session persistence
-- Establish project activation with comprehensive context loading
+- Establish project context with comprehensive context loading
 
 **Will Not:**
 
 - Modify project structure or configuration without explicit permission
-- Load context without proper Serena MCP integration and validation
+- Load context without validation
 - Override existing session context without checkpoint preservation
diff --git a/src/superclaude/commands/pm.md b/src/superclaude/commands/pm.md
--- a/src/superclaude/commands/pm.md
+++ b/src/superclaude/commands/pm.md
@@ -13,7 +13,7 @@ personas: [pm-agent]
 
 ## Triggers
 
-- **Session Start (MANDATORY)**: ALWAYS activates to restore context via Serena MCP memory
+- **Session Start (MANDATORY)**: ALWAYS activates to restore context from the `.superclaude/memory/` files
 - **All User Requests**: Default entry point for all interactions unless explicit sub-agent override
 - **State Questions**: Progress and status inquiries trigger context report
 - **Vague Requests**: Discovery-mode triggers for underspecified goals
@@ -44,7 +44,7 @@ personas: [pm-agent]
 
 ## Behavioral Summary
 
-PM Agent is the always-active orchestration layer that auto-delegates user requests to domain specialists (backend, frontend, security, etc.) without requiring manual agent selection. It maintains continuous context across sessions via Serena MCP memory, follows a PDCA (Plan-Do-Check-Act) cycle for self-improvement, and dynamically loads/unloads MCP tools per execution phase for zero-token baseline efficiency. All implementations, mistakes, and patterns are automatically documented for continuous learning.
+PM Agent is the always-active orchestration layer that auto-delegates user requests to domain specialists (backend, frontend, security, etc.) without requiring manual agent selection. It maintains continuous context across sessions via memory files under `.superclaude/memory/`, follows a PDCA (Plan-Do-Check-Act) cycle for self-improvement, and dynamically loads/unloads MCP tools per execution phase for zero-token baseline efficiency. All implementations, mistakes, and patterns are automatically documented for continuous learning.
 
 ## Activation
 
diff --git a/src/superclaude/commands/save.md b/src/superclaude/commands/save.md
--- a/src/superclaude/commands/save.md
+++ b/src/superclaude/commands/save.md
@@ -1,6 +1,6 @@
 ---
 name: save
-description: "Session lifecycle management with Serena MCP integration for session context persistence"
+description: "Session lifecycle management with memory files for session context persistence"
 category: session
 complexity: standard
 mcp-servers: []
@@ -25,29 +25,31 @@ personas: []
 ## Behavioral Flow
 
 1. **Analyze**: Examine session progress and identify discoveries worth preserving
-2. **Persist**: Save session context and learnings using Serena MCP memory management
+2. **Persist**: Save session context and learnings as markdown memory files under `.superclaude/memory/`
 3. **Checkpoint**: Create recovery points for complex sessions and progress tracking
 4. **Validate**: Ensure session data integrity and cross-session compatibility
 5. **Prepare**: Ready session context for seamless continuation in future sessions
 
 Key behaviors:
 
-- Serena MCP integration for memory management and cross-session persistence
+- Markdown memory files under `.superclaude/memory/` for cross-session persistence
 - Automatic checkpoint creation based on session progress and critical tasks
 - Session context preservation with comprehensive discovery and pattern archival
 - Cross-session learning with accumulated project insights and technical decisions
 
-## MCP Integration
+## Memory Store
 
-- **Serena MCP**: Mandatory integration for session management, memory operations, and cross-session persistence
-- **Memory Operations**: Session context storage, checkpoint creation, and discovery archival
+- **Location**: `<project>/.superclaude/memory/<key>.md`, flat markdown with subfolders for topics. `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree
+- **First write**: if `<project>/.superclaude/.gitignore` is absent, create it with the single line `*`
+- **Single-owner keys** (`pm_context`, `last_session`, `next_actions`): overwritten whole on each save
+- **Keys parallel sessions may write** (`checkpoint`, `decision`, handoffs): written as `<key>-<session-or-timestamp>.md` and never edited in place
 - **Performance Critical**: <200ms for memory operations, <1s for checkpoint creation
 
 ## Tool Coordination
 
-- **write_memory/read_memory**: Core session context persistence and retrieval
-- **think_about_collected_information**: Session analysis and discovery identification
-- **summarize_changes**: Session summary generation and progress documentation
+- **Write/Read**: Core session context persistence and retrieval of `.superclaude/memory/` files
+- **Glob** `.superclaude/memory/**/*.md`: Listing existing memories before a save
+- **Session analysis and summary**: Done in the session itself; the discovery analysis and summary are written into the memory files
 - **TodoRead**: Task completion tracking for automatic checkpoint triggers
 
 ## Key Patterns
@@ -63,7 +65,7 @@ Key behaviors:
 
 ```
 /sc:save
-# Saves current session discoveries and context to Serena MCP
+# Saves current session discoveries and context to .superclaude/memory/
 # Automatically creates checkpoint if session exceeds 30 minutes
 ```
 
@@ -95,12 +97,12 @@ Key behaviors:
 
 **Will:**
 
-- Save session context using Serena MCP integration for cross-session persistence
+- Save session context as markdown files under `.superclaude/memory/` for cross-session persistence
 - Create automatic checkpoints based on session progress and task completion
 - Preserve discoveries and patterns for enhanced project understanding
 
 **Will Not:**
 
-- Operate without proper Serena MCP integration and memory access
+- Operate without write access to the `.superclaude/memory/` store
 - Save session data without validation and integrity verification
 - Override existing session context without proper checkpoint preservation
diff --git a/src/superclaude/skills/sc-pm-protocol/SKILL.md b/src/superclaude/skills/sc-pm-protocol/SKILL.md
--- a/src/superclaude/skills/sc-pm-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-pm-protocol/SKILL.md
@@ -18,16 +18,18 @@ Activation conditions:
 
 Do NOT invoke this skill directly. Use the `sc:pm` command.
 
-## Session Lifecycle (Serena MCP Memory Integration)
+## Session Lifecycle (Memory Files Under `.superclaude/memory/`)
+
+Memory is plain markdown in `<project>/.superclaude/memory/<key>.md`, with subfolders for topics. `<project>` is the git top-level of the current directory (`git rev-parse --show-toplevel`), or the current directory outside git: one store per worktree. On the first write, if `<project>/.superclaude/.gitignore` is absent, create it with the single line `*`. Single-owner keys (`pm_context`, `last_session`, `next_actions`, `current_plan`) are overwritten whole; keys parallel sessions may write (`checkpoint`, `decision`, handoffs) are written as `<key>-<session-or-timestamp>.md` and never edited in place.
 
 ### Session Start Protocol (Auto-Executes Every Time)
 
 1. Context Restoration:
-   - list_memories() → Check for existing PM Agent state
-   - read_memory("pm_context") → Restore overall context
-   - read_memory("current_plan") → What are we working on
-   - read_memory("last_session") → What was done previously
-   - read_memory("next_actions") → What to do next
+   - Glob `.superclaude/memory/**/*.md` → Check for existing PM Agent state
+   - Read `.superclaude/memory/pm_context.md` → Restore overall context
+   - Read `.superclaude/memory/current_plan.md` → What are we working on
+   - Read `.superclaude/memory/last_session.md` → What was done previously
+   - Read `.superclaude/memory/next_actions.md` → What to do next
 
 2. Report to User:
    "Previous: [last session summary]
@@ -40,16 +42,16 @@ Do NOT invoke this skill directly. Use the `sc:pm` command.
 
 ### During Work (Continuous PDCA Cycle)
 
-1. Plan: write_memory("plan", goal_statement); define what to implement and why
-2. Do: TodoWrite for task tracking; write_memory("checkpoint", progress) every 30min; record experiments
+1. Plan: Write goal_statement to `.superclaude/memory/current_plan.md`; define what to implement and why
+2. Do: TodoWrite for task tracking; Write progress to `.superclaude/memory/checkpoint-<timestamp>.md` every 30min; record experiments
 3. Check: Self-evaluation against goals; assess what worked and what failed
 4. Act: Success → docs/patterns/[name].md; Failure → docs/mistakes/[name].md; update CLAUDE.md if global
 
 ### Session End Protocol
 
-1. Final Checkpoint: write_memory("last_session", summary); write_memory("next_actions", todo_list)
+1. Final Checkpoint: Write summary to `.superclaude/memory/last_session.md`; Write todo_list to `.superclaude/memory/next_actions.md`
 2. Documentation Cleanup: Move temp docs to patterns or mistakes
-3. State Preservation: write_memory("pm_context", complete_state)
+3. State Preservation: Write complete_state to `.superclaude/memory/pm_context.md`
 
 ## Sub-Agent Orchestration Patterns
 
@@ -110,7 +112,7 @@ Never retry the same approach without understanding WHY it failed.
 3. Hypothesis Formation: Create hypothesis document with evidence
 4. Solution Design (MUST BE DIFFERENT from failed approach)
 5. Execute New Approach: Implement based on root cause understanding
-6. Learning Capture: Success → write_memory; Failure → Return to Step 2
+6. Learning Capture: Success → Write the solution to `.superclaude/memory/learning/solutions/[error_type].md`; Failure → Return to Step 2
 
 ### Anti-Patterns
 
@@ -127,7 +129,7 @@ Never retry the same approach without understanding WHY it failed.
 
 ## Memory Key Schema (Standardized)
 
-Pattern: `[category]/[subcategory]/[identifier]`
+Pattern: `[category]/[subcategory]/[identifier]`, stored as the file `.superclaude/memory/[category]/[subcategory]/[identifier].md`
 
 - `session/`: context, last, checkpoint
 - `plan/[feature]/`: hypothesis, architecture, rationale
@@ -154,7 +156,7 @@ After each successful implementation:
 - Create docs/patterns/[feature-name].md
 - Document architecture decisions in ADR format
 - Update CLAUDE.md with new best practices
-- write_memory("learning/patterns/[name]", reusable_pattern)
+- Write reusable_pattern to `.superclaude/memory/learning/patterns/[name].md`
 
 ### Mistake Recording
 
@@ -163,7 +165,7 @@ When errors occur:
 - Create docs/mistakes/[feature]-YYYY-MM-DD.md
 - Document root cause analysis
 - Create prevention checklist
-- write_memory("learning/mistakes/[timestamp]", failure_analysis)
+- Write failure_analysis to `.superclaude/memory/learning/mistakes/[timestamp].md`
 
 ### Monthly Maintenance
 
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
