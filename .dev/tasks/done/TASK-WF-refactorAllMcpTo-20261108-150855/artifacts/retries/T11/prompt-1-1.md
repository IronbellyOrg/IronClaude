c846d2c9b197bb50dc940c586012759861200fb5
Review one task for spec compliance.

Task brief: ## Task 11: Update `mcp-servers:` metadata in commands

Design section 3.3 items 4-5. Apply the metadata rule to the `mcp-servers:` line of these files in `src/superclaude/commands/`: `validate-roadmap.md` (7), `brainstorm.md` (6), `recommend.md` (6), `reflect.md` (6), `troubleshoot.md` (6), `issue.md` (7), `pr-submit.md` (6), `tdd.md` (7), `review-translation.md` (6), `cleanup-audit.md` (7), `explain.md` (6), `adversarial.md` (7), `cleanup.md` (6), `cli-eval.md` (6), `cli-portify.md` (7), `improve.md` (6), `index.md` (6), `release-split.md` (7), `spec-panel.md` (6), `tasklist.md` (7), `research.md` (6), `pm.md` (6), `task.md` (7); and to the plugin copies in `plugins/superclaude/commands/`: `brainstorm.md`, `recommend.md`, `reflect.md`, `explain.md`, `cleanup.md`, `improve.md`, `index.md`, `spec-panel.md`, `research.md`, `pm.md`, `task.md`. In `research.md`, `pm.md`, `task.md` keep `playwright` and `morphllm`. `build.md` and `test.md` are unchanged. `issue.md:7` becomes `[litellm, auggie, codegraph]`; update `tests/commands/test_issue_command.py` (about line 73) to expect it.

Acceptance criteria:
- Every listed metadata line names `litellm` first where it names `auggie`, `context7` or `tavily`; `build.md` and `test.md` are unchanged.
- `uv run pytest tests/commands -v` passes; output saved to `./artifacts/t11-pytest.log`.
Global constraints: - Naming rule (design section 2): name both tools, proxy first, direct kept. Proxy names: Augment search `mcp__litellm__augment_code-augment_code_search` (called AUG below), `mcp__litellm__context7-resolve-library-id`, `mcp__litellm__context7-query-docs`, `mcp__litellm__Tavily-tavily_search`, `mcp__litellm__Tavily-tavily_extract`, `mcp__litellm__Tavily-tavily_crawl`, `mcp__litellm__Tavily-tavily_map` (capital `T`, case-sensitive). Playwright plugin names `mcp__plugin_playwright_playwright__browser_<x>`.
- AUG phrase (full form, verbatim): "Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep."
- AUG short form (inside lists and tables): "`mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)".
- Tavily phrase: "`mcp__litellm__Tavily-tavily_<x>` (else `mcp__tavily__tavily_<x>`)", keeping any existing WebSearch/WebFetch fallback tail. Context7 phrase: "`mcp__litellm__context7-<tool>` (else `mcp__context7__<tool>`)". Wildcards: "`mcp__litellm__Tavily-*` or `mcp__tavily__*`", "`mcp__litellm__context7-*` or `mcp__context7__*`".
- Allow-lists (`tools:` / `allowed-tools:`): insert each proxy name immediately before its direct twin; never remove a direct name except `mcp__auggie-mcp__codebase-retrieval`, which is replaced by AUG followed by `mcp__auggie__codebase-retrieval`. `mcp__litellm__Tavily-tavily_research` is not added anywhere.
- `mcp-servers:` metadata: add `litellm` first; replace `auggie-mcp` with `auggie`; keep the other words (`[auggie, codegraph]` becomes `[litellm, auggie, codegraph]`).
- Availability tests ("if X is not available") become "if neither <proxy name> nor <direct name> is available". Every existing degrade or fail-open path is kept verbatim (design section 4).
- Never hard-code a repository owner, name or branch; never add a `src/superclaude/...` path to an installed primitive.
- Edit `src/superclaude/**` and the hand-maintained `plugins/superclaude/**` copies only; never edit or stage `.claude/` mirrors (run `make sync-dev` instead) and never hand-edit `~/.claude`.
- Line numbers below were recorded at commit 0423fe5f; re-locate each edit by its text before editing.
- Python only through UV (`uv run pytest ...`). Never print, log or write `LITELLM_API_KEY` or any token.
- `.dev/tasks/` is always staged (`git add .dev/tasks`); `.dev/issues/` stays out of the index. No push and no PR in this run.
Start sha: c846d2c9b197bb50dc940c586012759861200fb5
Diff against the start snapshot: diff --git a/plugins/superclaude/commands/brainstorm.md b/plugins/superclaude/commands/brainstorm.md
index 60b2f572..02274499 100644
--- a/plugins/superclaude/commands/brainstorm.md
+++ b/plugins/superclaude/commands/brainstorm.md
@@ -3,7 +3,7 @@ name: brainstorm
 description: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge"
 category: orchestration
 complexity: advanced
-mcp-servers: [auggie-mcp, codegraph, tavily]
+mcp-servers: [litellm, auggie, codegraph, tavily]
 personas: [architect, analyzer, scribe]
 version: 2.0.0
 spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
diff --git a/plugins/superclaude/commands/cleanup.md b/plugins/superclaude/commands/cleanup.md
index b5049b19..d597e589 100644
--- a/plugins/superclaude/commands/cleanup.md
+++ b/plugins/superclaude/commands/cleanup.md
@@ -3,7 +3,7 @@ name: cleanup
 description: "Systematically clean up code, remove dead code, and optimize project structure"
 category: workflow
 complexity: standard
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, quality, security]
 ---
 
diff --git a/plugins/superclaude/commands/explain.md b/plugins/superclaude/commands/explain.md
index c2ca1e49..7ac2e0e0 100644
--- a/plugins/superclaude/commands/explain.md
+++ b/plugins/superclaude/commands/explain.md
@@ -3,7 +3,7 @@ name: explain
 description: "Provide clear explanations of code, concepts, and system behavior with educational clarity"
 category: workflow
 complexity: standard
-mcp-servers: [context7, codegraph]
+mcp-servers: [litellm, context7, codegraph]
 personas: [educator, architect, security]
 ---
 
diff --git a/plugins/superclaude/commands/improve.md b/plugins/superclaude/commands/improve.md
index 78c2fe1d..1d521d4b 100644
--- a/plugins/superclaude/commands/improve.md
+++ b/plugins/superclaude/commands/improve.md
@@ -3,7 +3,7 @@ name: improve
 description: "Apply systematic improvements to code quality, performance, and maintainability"
 category: workflow
 complexity: standard
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, performance, quality, security]
 ---
 
diff --git a/plugins/superclaude/commands/index.md b/plugins/superclaude/commands/index.md
index 98b57525..c72df0a7 100644
--- a/plugins/superclaude/commands/index.md
+++ b/plugins/superclaude/commands/index.md
@@ -3,7 +3,7 @@ name: index
 description: "Generate comprehensive project documentation and knowledge base with intelligent organization"
 category: special
 complexity: standard
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, scribe, quality]
 ---
 
diff --git a/plugins/superclaude/commands/pm.md b/plugins/superclaude/commands/pm.md
index d36cbc11..9d4f20ba 100644
--- a/plugins/superclaude/commands/pm.md
+++ b/plugins/superclaude/commands/pm.md
@@ -3,7 +3,7 @@ name: pm
 description: "Project Manager Agent - Default orchestration agent that coordinates all sub-agents and manages workflows seamlessly"
 category: orchestration
 complexity: meta
-mcp-servers: [context7, playwright, morphllm, tavily]
+mcp-servers: [litellm, context7, playwright, morphllm, tavily]
 personas: [pm-agent]
 ---
 
diff --git a/plugins/superclaude/commands/recommend.md b/plugins/superclaude/commands/recommend.md
index bee76a3e..36c278bf 100644
--- a/plugins/superclaude/commands/recommend.md
+++ b/plugins/superclaude/commands/recommend.md
@@ -3,7 +3,7 @@ name: sc:recommend
 description: "Build a refined, paste-ready prompt that delegates the user's goal to the right local skill, command, agent, or native-tool sequence — or, with --plugin, searches the Claude plugin / community skill ecosystem instead."
 category: utility
 complexity: standard
-mcp-servers: [auggie, tavily]
+mcp-servers: [litellm, auggie, tavily]
 personas: []
 argument-hint: "<goal description> [--plugin] [--eval <mode>] [--minstar <N>]"
 ---
diff --git a/plugins/superclaude/commands/reflect.md b/plugins/superclaude/commands/reflect.md
index a4c48c1e..0b0d8ebe 100644
--- a/plugins/superclaude/commands/reflect.md
+++ b/plugins/superclaude/commands/reflect.md
@@ -3,7 +3,7 @@ name: reflect
 description: "Tiered reflection protocol — UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate"
 category: analysis
 complexity: advanced
-mcp-servers: [auggie, codegraph, context7, tavily]
+mcp-servers: [litellm, auggie, codegraph, context7, tavily]
 personas: [analyzer, qa, refactorer]
 version: 2.0.0
 supersedes: .dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md
diff --git a/plugins/superclaude/commands/research.md b/plugins/superclaude/commands/research.md
index 9e57d48a..5cd3bc18 100644
--- a/plugins/superclaude/commands/research.md
+++ b/plugins/superclaude/commands/research.md
@@ -3,7 +3,7 @@ name: research
 description: Deep web research with adaptive planning and intelligent search
 category: command
 complexity: advanced
-mcp-servers: [tavily, playwright]
+mcp-servers: [litellm, tavily, playwright]
 personas: [deep-research-agent]
 ---
 
diff --git a/plugins/superclaude/commands/spec-panel.md b/plugins/superclaude/commands/spec-panel.md
index ac3a932a..8b8ed8dd 100644
--- a/plugins/superclaude/commands/spec-panel.md
+++ b/plugins/superclaude/commands/spec-panel.md
@@ -3,7 +3,7 @@ name: spec-panel
 description: "Multi-expert specification review and improvement using renowned specification and software engineering experts"
 category: analysis
 complexity: enhanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [technical-writer, system-architect, quality-engineer]
 ---
 
diff --git a/plugins/superclaude/commands/task.md b/plugins/superclaude/commands/task.md
index 838214f6..26732d5b 100644
--- a/plugins/superclaude/commands/task.md
+++ b/plugins/superclaude/commands/task.md
@@ -4,7 +4,7 @@ description: "Unified task execution with intelligent workflow management, MCP c
 category: special
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7, playwright, morphllm]
+mcp-servers: [litellm, context7, playwright, morphllm]
 personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]
 version: "2.0.0"
 ---
diff --git a/src/superclaude/commands/adversarial.md b/src/superclaude/commands/adversarial.md
index 3fbb17b8..38e9b163 100644
--- a/src/superclaude/commands/adversarial.md
+++ b/src/superclaude/commands/adversarial.md
@@ -4,7 +4,7 @@ description: "Structured adversarial debate, comparison, and merge pipeline for
 category: analysis
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, scribe]
 ---
 
diff --git a/src/superclaude/commands/brainstorm.md b/src/superclaude/commands/brainstorm.md
index 5e1e4680..0bdbb2d6 100644
--- a/src/superclaude/commands/brainstorm.md
+++ b/src/superclaude/commands/brainstorm.md
@@ -3,7 +3,7 @@ name: brainstorm
 description: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge"
 category: orchestration
 complexity: advanced
-mcp-servers: [auggie-mcp, codegraph, tavily]
+mcp-servers: [litellm, auggie, codegraph, tavily]
 personas: [architect, analyzer, scribe]
 version: 2.0.0
 spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
diff --git a/src/superclaude/commands/cleanup-audit.md b/src/superclaude/commands/cleanup-audit.md
index dd3276b3..c3f373bf 100644
--- a/src/superclaude/commands/cleanup-audit.md
+++ b/src/superclaude/commands/cleanup-audit.md
@@ -4,7 +4,7 @@ description: "Multi-pass read-only repository audit producing evidence-backed cl
 category: utility
 complexity: high
 allowed-tools: Read, Glob, Grep, Bash, TodoWrite, Task, Write, Skill
-mcp-servers: [codegraph, context7]
+mcp-servers: [litellm, codegraph, context7]
 personas: [analyzer, architect, devops, qa, refactorer]
 ---
 
diff --git a/src/superclaude/commands/cleanup.md b/src/superclaude/commands/cleanup.md
index 62f03fde..8ef10f19 100644
--- a/src/superclaude/commands/cleanup.md
+++ b/src/superclaude/commands/cleanup.md
@@ -3,7 +3,7 @@ name: cleanup
 description: "Systematically clean up code, remove dead code, and optimize project structure"
 category: workflow
 complexity: standard
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, quality, security]
 ---
 
diff --git a/src/superclaude/commands/cli-eval.md b/src/superclaude/commands/cli-eval.md
index cd4059d9..cabb844b 100644
--- a/src/superclaude/commands/cli-eval.md
+++ b/src/superclaude/commands/cli-eval.md
@@ -3,7 +3,7 @@ name: cli-eval
 description: "Manage the cliEval pipeline lifecycle — author a new eval suite (propose→critique→debate→author→validate→document) or interactively select and supervise a run of an existing suite."
 category: testing
 complexity: advanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, qa, scribe]
 ---
 
diff --git a/src/superclaude/commands/cli-portify.md b/src/superclaude/commands/cli-portify.md
index bcd63d19..90e07363 100644
--- a/src/superclaude/commands/cli-portify.md
+++ b/src/superclaude/commands/cli-portify.md
@@ -4,7 +4,7 @@ description: "Port inference-based SuperClaude workflows into programmatic CLI p
 category: development
 complexity: high
 allowed-tools: Read, Glob, Grep, Write, Bash, TodoWrite, Skill
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, backend]
 version: "1.0.0"
 ---
diff --git a/src/superclaude/commands/explain.md b/src/superclaude/commands/explain.md
index 5b1cef90..c79892e9 100644
--- a/src/superclaude/commands/explain.md
+++ b/src/superclaude/commands/explain.md
@@ -3,7 +3,7 @@ name: explain
 description: "Provide clear explanations of code, concepts, and system behavior with educational clarity"
 category: workflow
 complexity: standard
-mcp-servers: [context7, codegraph]
+mcp-servers: [litellm, context7, codegraph]
 personas: [educator, architect, security]
 ---
 
diff --git a/src/superclaude/commands/improve.md b/src/superclaude/commands/improve.md
index adc55d74..b43a55ad 100644
--- a/src/superclaude/commands/improve.md
+++ b/src/superclaude/commands/improve.md
@@ -3,7 +3,7 @@ name: improve
 description: "Apply systematic improvements to code quality, performance, and maintainability"
 category: workflow
 complexity: standard
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, performance, quality, security]
 ---
 
diff --git a/src/superclaude/commands/index.md b/src/superclaude/commands/index.md
index 2f539541..bda7f6ec 100644
--- a/src/superclaude/commands/index.md
+++ b/src/superclaude/commands/index.md
@@ -3,7 +3,7 @@ name: index
 description: "Generate comprehensive project documentation and knowledge base with intelligent organization"
 category: special
 complexity: standard
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, scribe, quality]
 ---
 
diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index d8c7141b..3eeb3016 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -4,7 +4,7 @@ version: "1.1.0"
 description: "Claim a GitHub issue on the origin repo (assign it, check its accuracy, write a summary and a next-step prompt, then create an Orca worktree and launch an agent in it) or create a templated issue with labels from a fixed set"
 category: workflow
 complexity: advanced
-mcp-servers: [auggie, codegraph]
+mcp-servers: [litellm, auggie, codegraph]
 personas: [analyzer]
 argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit] | --create \"<description>\" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]"
 ---
diff --git a/src/superclaude/commands/pm.md b/src/superclaude/commands/pm.md
index d36cbc11..9d4f20ba 100644
--- a/src/superclaude/commands/pm.md
+++ b/src/superclaude/commands/pm.md
@@ -3,7 +3,7 @@ name: pm
 description: "Project Manager Agent - Default orchestration agent that coordinates all sub-agents and manages workflows seamlessly"
 category: orchestration
 complexity: meta
-mcp-servers: [context7, playwright, morphllm, tavily]
+mcp-servers: [litellm, context7, playwright, morphllm, tavily]
 personas: [pm-agent]
 ---
 
diff --git a/src/superclaude/commands/pr-submit.md b/src/superclaude/commands/pr-submit.md
index b82995af..c6cc6232 100644
--- a/src/superclaude/commands/pr-submit.md
+++ b/src/superclaude/commands/pr-submit.md
@@ -3,7 +3,7 @@ name: pr-submit
 description: "Open a PR on the fork and arm an in-session PR-review auto-remediation monitor — poll for the Augment and Codex reviews, re-grade + verify findings, dispatch verified ones to /sc:troubleshoot, then (at higher --monitor ordinals) fix, validate, push, reply, and resolve under a capped monotonic round counter."
 category: quality
 complexity: advanced
-mcp-servers: [auggie]
+mcp-servers: [litellm, auggie]
 personas: [analyzer, architect, security, qa, devops]
 argument-hint: "[--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--merge-guard {draft,off}] [--output-dir <dir>] [--resume <run-log.jsonl>]"
 version: "1.0"
diff --git a/src/superclaude/commands/recommend.md b/src/superclaude/commands/recommend.md
index bee76a3e..36c278bf 100644
--- a/src/superclaude/commands/recommend.md
+++ b/src/superclaude/commands/recommend.md
@@ -3,7 +3,7 @@ name: sc:recommend
 description: "Build a refined, paste-ready prompt that delegates the user's goal to the right local skill, command, agent, or native-tool sequence — or, with --plugin, searches the Claude plugin / community skill ecosystem instead."
 category: utility
 complexity: standard
-mcp-servers: [auggie, tavily]
+mcp-servers: [litellm, auggie, tavily]
 personas: []
 argument-hint: "<goal description> [--plugin] [--eval <mode>] [--minstar <N>]"
 ---
diff --git a/src/superclaude/commands/reflect.md b/src/superclaude/commands/reflect.md
index 3788a085..4ee2be08 100644
--- a/src/superclaude/commands/reflect.md
+++ b/src/superclaude/commands/reflect.md
@@ -3,7 +3,7 @@ name: reflect
 description: "Tiered reflection protocol — UC-1 pre-execution coverage/gap audit and UC-2 post-execution deviation audit with heterogeneous reviewer ensemble, blind calibration, and mandatory evidence-validator gate"
 category: analysis
 complexity: advanced
-mcp-servers: [auggie, codegraph, context7, tavily]
+mcp-servers: [litellm, auggie, codegraph, context7, tavily]
 personas: [analyzer, qa, refactorer]
 version: 2.0.0
 supersedes: .dev/eval-workspaces/sc-reflect/skill-snapshot/reflect-v1.md
diff --git a/src/superclaude/commands/release-split.md b/src/superclaude/commands/release-split.md
index 303ea03f..cf64c0ea 100644
--- a/src/superclaude/commands/release-split.md
+++ b/src/superclaude/commands/release-split.md
@@ -4,7 +4,7 @@ description: "Neutral two-phase release split analysis with adversarial validati
 category: planning
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [architect, analyzer, scribe]
 ---
 
diff --git a/src/superclaude/commands/research.md b/src/superclaude/commands/research.md
index b09f38ff..8e2ca4ac 100644
--- a/src/superclaude/commands/research.md
+++ b/src/superclaude/commands/research.md
@@ -3,7 +3,7 @@ name: research
 description: Deep web research with adaptive planning and intelligent search
 category: command
 complexity: advanced
-mcp-servers: [tavily, playwright]
+mcp-servers: [litellm, tavily, playwright]
 personas: [deep-research-agent]
 ---
 
diff --git a/src/superclaude/commands/review-translation.md b/src/superclaude/commands/review-translation.md
index cb8f10d2..a2a5f8e0 100644
--- a/src/superclaude/commands/review-translation.md
+++ b/src/superclaude/commands/review-translation.md
@@ -3,7 +3,7 @@ name: review-translation
 description: "Systematic localization review with adversarial validation, real-world evidence search, and comprehensive quality scoring"
 category: orchestration
 complexity: advanced
-mcp-servers: [tavily, context7]
+mcp-servers: [litellm, tavily, context7]
 personas: [localization-reviewer, linguistic-validator, cultural-consultant, research-analyst]
 ---
 
diff --git a/src/superclaude/commands/spec-panel.md b/src/superclaude/commands/spec-panel.md
index fa1ed3f3..20b0c756 100644
--- a/src/superclaude/commands/spec-panel.md
+++ b/src/superclaude/commands/spec-panel.md
@@ -3,7 +3,7 @@ name: spec-panel
 description: "Multi-expert specification review and improvement using renowned specification and software engineering experts"
 category: analysis
 complexity: enhanced
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [technical-writer, system-architect, quality-engineer]
 ---
 
diff --git a/src/superclaude/commands/task.md b/src/superclaude/commands/task.md
index d12ff76e..3d5548e1 100644
--- a/src/superclaude/commands/task.md
+++ b/src/superclaude/commands/task.md
@@ -4,7 +4,7 @@ description: "Unified task execution with intelligent workflow management, MCP c
 category: special
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
-mcp-servers: [context7, playwright, morphllm]
+mcp-servers: [litellm, context7, playwright, morphllm]
 personas: [architect, analyzer, qa, refactorer, frontend, backend, security, devops, python-expert, quality-engineer]
 version: "2.0.0"
 ---
diff --git a/src/superclaude/commands/tasklist.md b/src/superclaude/commands/tasklist.md
index 6882f419..3cd02b62 100644
--- a/src/superclaude/commands/tasklist.md
+++ b/src/superclaude/commands/tasklist.md
@@ -4,7 +4,7 @@ description: "Generate deterministic, Sprint CLI-compatible tasklist bundles fro
 category: utility
 complexity: high
 allowed-tools: Read, Glob, Grep, Write, Bash, TaskCreate, TaskUpdate, TaskList, TaskGet, Task, Skill
-mcp-servers: [context7]
+mcp-servers: [litellm, context7]
 personas: [analyzer, architect]
 version: "2.0.0"
 ---
diff --git a/src/superclaude/commands/tdd.md b/src/superclaude/commands/tdd.md
index 4143c2fa..9391d504 100644
--- a/src/superclaude/commands/tdd.md
+++ b/src/superclaude/commands/tdd.md
@@ -4,7 +4,7 @@ description: "Create or populate a Technical Design Document (TDD) for a compone
 category: documentation
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, Agent
-mcp-servers: [context7, auggie-mcp]
+mcp-servers: [litellm, context7, auggie]
 personas: [architect, analyzer, backend]
 ---
 
diff --git a/src/superclaude/commands/troubleshoot.md b/src/superclaude/commands/troubleshoot.md
index 97593352..5afbcabc 100644
--- a/src/superclaude/commands/troubleshoot.md
+++ b/src/superclaude/commands/troubleshoot.md
@@ -3,7 +3,7 @@ name: troubleshoot
 description: "Tiered debugging — fast Tier 1 triage with auggie + codegraph grounding and a native Grep/Read floor, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in remediation chain (sc:workflow → sc:implement; task-builder → /task with --depth deep)"
 category: analysis
 complexity: advanced
-mcp-servers: [auggie, codegraph, context7, tavily]
+mcp-servers: [litellm, auggie, codegraph, context7, tavily]
 personas: [analyzer, performance, security, qa, refactorer, devops]
 argument-hint: "[<issue description>] [--type bug|build|performance|deployment|security|test] [--depth quick|standard|deep] [--scope <path|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-doc-discovery] [--no-mcp] [--context <path>] [--caller <name>]"
 ---
diff --git a/src/superclaude/commands/validate-roadmap.md b/src/superclaude/commands/validate-roadmap.md
index 455b2dd8..79c424d5 100644
--- a/src/superclaude/commands/validate-roadmap.md
+++ b/src/superclaude/commands/validate-roadmap.md
@@ -4,7 +4,7 @@ description: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, e
 category: analysis
 complexity: advanced
 allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__litellm__augment_code-augment_code_search, mcp__auggie__codebase-retrieval, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node
-mcp-servers: [auggie, codegraph]
+mcp-servers: [litellm, auggie, codegraph]
 personas: [analyzer, architect, qa]
 ---
 
diff --git a/tests/commands/test_issue_command.py b/tests/commands/test_issue_command.py
index 735e3684..7604e08d 100644
--- a/tests/commands/test_issue_command.py
+++ b/tests/commands/test_issue_command.py
@@ -70,7 +70,7 @@ def test_frontmatter_fields():
     assert fields["description"]
     assert fields["category"] == "workflow"
     assert fields["complexity"] == "advanced"
-    assert fields["mcp-servers"] == "[auggie, codegraph]"
+    assert fields["mcp-servers"] == "[litellm, auggie, codegraph]"
     assert fields["personas"] == "[analyzer]"
     assert fields["argument-hint"]
     assert "--pipeline worktree|full|none" in fields["argument-hint"]
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
