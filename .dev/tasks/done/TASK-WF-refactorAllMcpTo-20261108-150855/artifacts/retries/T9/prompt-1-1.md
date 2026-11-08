d0ef418b6003a31dc3feca208eba1af9ea4833bb
Review one task for spec compliance.

Task brief: ## Task 9: Rewrite bare `codebase-retrieval` steps in the generic skills

Design section 3.2 items 9-10. Rewrite each bare `codebase-retrieval` mention to the AUG phrase (short form inside lists) at: `src/superclaude/skills/sc-task-protocol/SKILL.md` (about lines 91, 106, 300, 315), `prd/SKILL.md` (222), `prd/refs/build-request-template.md` (100), `tdd/SKILL.md` (197, 215), `tdd/refs/build-request-template.md` (94), `task-builder/SKILL.md` (339, 1208), `roadmap/SKILL.md` (253, 491, 2537), `readme/SKILL.md` (239, 637), `tech-reference/SKILL.md` (227, 480), `tech-research/SKILL.md` (217, 454, 1621), `operational-guide/SKILL.md` (232, 610), `task/SKILL.md` (600), `confidence-check/SKILL.md` (50) and its drifted copy `plugins/superclaude/skills/confidence-check/SKILL.md` (48), `sc-crash-recovery/SKILL.md` (101, 146), `sc-crash-recovery/refs/pipelines.md` (49), `sc-crash-recovery/refs/investigators.md` (139, 141). The `sc-crash-recovery/SKILL.md:146` row "Auggie MCP unreachable" becomes "Codebase search unreachable (neither AUG nor `mcp__auggie__codebase-retrieval` answers)" with the same recovery action. Codegraph-only rows are unchanged.

Acceptance criteria:
- `grep -rn 'codebase-retrieval' <each file above>` shows every remaining mention paired with AUG on the same line.
- `uv run pytest tests/skills -v` passes; output saved to `./artifacts/t9-pytest.log`.
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
Start sha: d0ef418b6003a31dc3feca208eba1af9ea4833bb
Diff against the start snapshot: diff --git a/plugins/superclaude/skills/confidence-check/SKILL.md b/plugins/superclaude/skills/confidence-check/SKILL.md
index f45aa4d1..af9e737b 100644
--- a/plugins/superclaude/skills/confidence-check/SKILL.md
+++ b/plugins/superclaude/skills/confidence-check/SKILL.md
@@ -45,7 +45,7 @@ Full 5-check scoring is not always required. For a single specific token, verify
 - `--help` / `<cmd> --help` for CLI flags and subcommands
 - `grep` / symbol lookup for functions, config keys, identifiers
 - File read for paths and file contents
-- `codebase-retrieval` (Auggie) — fastest for project-internal identifiers
+- `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) — fastest for project-internal identifiers
 
 If verification cost is genuinely high (requires a long-running process), say so explicitly and mark the specific token `[UNVERIFIED]` with the command the user can run to confirm — do **not** ship it bare.
 
diff --git a/src/superclaude/skills/confidence-check/SKILL.md b/src/superclaude/skills/confidence-check/SKILL.md
index fbaa9721..621156ab 100644
--- a/src/superclaude/skills/confidence-check/SKILL.md
+++ b/src/superclaude/skills/confidence-check/SKILL.md
@@ -47,7 +47,7 @@ Full 5-check scoring is not always required. For a single specific token, verify
 - `--help` / `<cmd> --help` for CLI flags and subcommands
 - `grep` / symbol lookup for functions, config keys, identifiers
 - File read for paths and file contents
-- `codebase-retrieval` (Auggie) — fastest for project-internal identifiers
+- `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) — fastest for project-internal identifiers
 
 If verification cost is genuinely high (requires a long-running process), say so explicitly and mark the specific token `[UNVERIFIED]` with the command the user can run to confirm — do **not** ship it bare.
 
diff --git a/src/superclaude/skills/operational-guide/SKILL.md b/src/superclaude/skills/operational-guide/SKILL.md
index 5b35fc16..5d3484cd 100644
--- a/src/superclaude/skills/operational-guide/SKILL.md
+++ b/src/superclaude/skills/operational-guide/SKILL.md
@@ -229,7 +229,7 @@ Example: "Write a guide for the deployment process"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the procedure's problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the procedure's problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 - **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related configs and scripts, identify gaps in what the user specified.
@@ -607,7 +607,7 @@ Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
 will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 
diff --git a/src/superclaude/skills/prd/SKILL.md b/src/superclaude/skills/prd/SKILL.md
index 1a1539c5..058c0ba1 100644
--- a/src/superclaude/skills/prd/SKILL.md
+++ b/src/superclaude/skills/prd/SKILL.md
@@ -219,7 +219,7 @@ Example: "Write a PRD for pixel streaming"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the product space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the product space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 
diff --git a/src/superclaude/skills/prd/refs/build-request-template.md b/src/superclaude/skills/prd/refs/build-request-template.md
index 7342fb8a..d586bf20 100644
--- a/src/superclaude/skills/prd/refs/build-request-template.md
+++ b/src/superclaude/skills/prd/refs/build-request-template.md
@@ -97,7 +97,7 @@ will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
 
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 
diff --git a/src/superclaude/skills/readme/SKILL.md b/src/superclaude/skills/readme/SKILL.md
index f3932fa4..d1d965fa 100644
--- a/src/superclaude/skills/readme/SKILL.md
+++ b/src/superclaude/skills/readme/SKILL.md
@@ -236,7 +236,7 @@ Example: "Write a README for the backend"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the module's structure and documentation landscape. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the module's structure and documentation landscape. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 - **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, locate tech references, identify gaps in what the user specified.
@@ -634,7 +634,7 @@ Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
 will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 ```
diff --git a/src/superclaude/skills/roadmap/SKILL.md b/src/superclaude/skills/roadmap/SKILL.md
index 9593b3a5..299e8f05 100644
--- a/src/superclaude/skills/roadmap/SKILL.md
+++ b/src/superclaude/skills/roadmap/SKILL.md
@@ -250,7 +250,7 @@ Example: "Build a roadmap for the collaboration feature"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, Read, and codebase-retrieval to map the problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, Read, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 - **Scenario A**: Focused discovery — read the provided documents, verify referenced files/directories exist, scan for related code, identify gaps in what the user specified.
@@ -488,7 +488,7 @@ Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
 will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 
@@ -2534,7 +2534,7 @@ Violations compromise roadmap quality.
 
 5. **No one-shotting roadmaps.** Agents must write incrementally as they analyze and design. The orchestrator must populate the roadmap section by section. This is non-negotiable.
 
-6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.
+6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.
 
 7. **Gap-driven web research.** Do not web search everything up front. First analyze the input and codebase thoroughly, identify specific gaps, then target web research at those gaps. This keeps web research focused and efficient.
 
diff --git a/src/superclaude/skills/sc-crash-recovery/SKILL.md b/src/superclaude/skills/sc-crash-recovery/SKILL.md
index 0b80b001..6c168310 100644
--- a/src/superclaude/skills/sc-crash-recovery/SKILL.md
+++ b/src/superclaude/skills/sc-crash-recovery/SKILL.md
@@ -98,7 +98,7 @@ If the user follows up with "go ahead, run #2", do it then — but each command
 
 ## Auggie usage
 
-Auggie's `codebase-retrieval` is the primary tool for the `auggie-semantic` investigator, and also useful as a secondary check in `pipeline-artifacts` when manifest data is ambiguous. Specific queries to use:
+Codebase search is the primary tool for the `auggie-semantic` investigator, and also useful as a secondary check in `pipeline-artifacts` when manifest data is ambiguous. Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep. Specific queries to use:
 
 - *"What files contain in-progress markers (TODO-WIP, FIXME-RECENT, status fields like 🟡 InProgress) modified in the last 72 hours?"*
 - *"Where are recovery or resume instructions documented for the sprint, roadmap, or task pipelines?"*
@@ -143,7 +143,7 @@ When an investigator's tool layer fails, do not silently drop its signal — the
 | Failure | Behavior | Fallback |
 |---|---|---|
 | `bootstrap_scan.sh` exits non-zero or returns malformed JSON | Continue with the investigators that don't depend on it (git-state, claude-sessions); mark pipeline-artifacts and project-memory as `unscanned: bootstrap_failed` in the final report | Read .dev/releases/current/* directly via Glob+Read as a degraded fallback |
-| Auggie MCP unreachable / `codebase-retrieval` returns error | Skip the auggie-semantic investigator; emit `unscanned: auggie_unavailable` in the report; offer the user the option to run a Grep-based fallback for `TODO-WIP`/`status: 🟡` markers | Grep over the tree for the explicit marker strings |
+| Codebase search unreachable (neither `mcp__litellm__augment_code-augment_code_search` nor `mcp__auggie__codebase-retrieval` answers) | Skip the auggie-semantic investigator; emit `unscanned: auggie_unavailable` in the report; offer the user the option to run a Grep-based fallback for `TODO-WIP`/`status: 🟡` markers | Grep over the tree for the explicit marker strings |
 | Task subagent times out or returns empty string | Re-spawn that one investigator once with a tighter prompt (cap output, narrower scope); if still empty, emit `unscanned: subagent_failure` and continue synthesis | None — the report is honest about the gap |
 | Wave exit criterion: any investigator that returns neither a structured fragment nor an explicit "no signal" marker | Wait briefly, then treat as `unscanned`. Never let a silent-empty investigator slip through into a synthesis that looks complete | None |
 
diff --git a/src/superclaude/skills/sc-crash-recovery/refs/investigators.md b/src/superclaude/skills/sc-crash-recovery/refs/investigators.md
index e6b16256..39cc791e 100644
--- a/src/superclaude/skills/sc-crash-recovery/refs/investigators.md
+++ b/src/superclaude/skills/sc-crash-recovery/refs/investigators.md
@@ -136,9 +136,9 @@ Be brief. Tables and paths, not prose. Do NOT run any write commands.
 **Prompt skeleton:**
 
 ```
-You are doing a semantic sweep of project <PROJECT_PATH> using the auggie codebase-retrieval MCP tool. The user just survived a crash and wants to find any in-progress work that structured scans (manifest.json, frontmatter) might miss.
+You are doing a semantic sweep of project <PROJECT_PATH> using codebase search. Codebase search: call `mcp__litellm__augment_code-augment_code_search` (`repo_owner`/`repo_name` from `git remote get-url origin`, `branch` = the repository's default branch; it sees pushed code only); if that tool is not available, call `mcp__auggie__codebase-retrieval`. For uncommitted or unpushed changes use codegraph or Grep. The user just survived a crash and wants to find any in-progress work that structured scans (manifest.json, frontmatter) might miss.
 
-Run the following codebase-retrieval queries IN PARALLEL where possible:
+Run the following queries with `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) IN PARALLEL where possible:
 
 1. "Files containing in-progress markers (TODO-WIP, FIXME-RECENT, XXX-RESUME, status: 🟡 InProgress, draft, WIP) that have been recently modified."
 2. "Notes or comments that say things like 'will continue', 'next step', 'left off', 'TODO next session', 'resume here', 'pause point'."
diff --git a/src/superclaude/skills/sc-crash-recovery/refs/pipelines.md b/src/superclaude/skills/sc-crash-recovery/refs/pipelines.md
index 68d2bc9d..1378a12b 100644
--- a/src/superclaude/skills/sc-crash-recovery/refs/pipelines.md
+++ b/src/superclaude/skills/sc-crash-recovery/refs/pipelines.md
@@ -46,7 +46,7 @@ mv .dev/tasks/to-do/TASK-PRD-<ts> .dev/tasks/done/
 - `.dev/research/<topic-slug>/` — multi-file research bundles, often with `00-extraction.md`, `01-...`, etc.
 - `claudedocs/` — finished tech references and analyses
 - `.dev/research/research-results/` — aggregated results
-**Status signal:** harder to read directly. Look for frontmatter, presence of a `synthesis.md` or `report.md`, and file mtimes. Auggie codebase-retrieval is useful here.
+**Status signal:** harder to read directly. Look for frontmatter, presence of a `synthesis.md` or `report.md`, and file mtimes. Codebase search (`mcp__litellm__augment_code-augment_code_search`, else `mcp__auggie__codebase-retrieval`) is useful here.
 **Recovery:** typically re-invoke the original skill with the same prompt. There's no formal resume protocol — the work is regenerable.
 
 ## Roadmap pipeline (`superclaude roadmap run`)
diff --git a/src/superclaude/skills/sc-task-protocol/SKILL.md b/src/superclaude/skills/sc-task-protocol/SKILL.md
index cf65807e..8743c56b 100644
--- a/src/superclaude/skills/sc-task-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-task-protocol/SKILL.md
@@ -88,7 +88,7 @@ Execute task according to tier requirements:
 **STRICT Execution**:
 
 1. Verify git working directory clean (git status)
-2. Load codebase context (codebase-retrieval)
+2. Load codebase context: `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)
 3. Check relevant memory files (Glob `.superclaude/memory/**/*.md`, then Read the relevant ones; skip when none exist)
 4. Identify all affected files and test files
 5. Make changes with full checklist
@@ -103,7 +103,7 @@ Execute task according to tier requirements:
 
 **STANDARD Execution**:
 
-1. Load context via codebase-retrieval
+1. Load context via `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)
 2. Search downstream impacts: `codegraph_callers` / `codegraph_impact` on the changed symbol when codegraph is usable (`~/.claude/CODEGRAPH.md`; rows are leads, Read before relying on them), OR Grep with a word-boundary pattern for the changed symbol, then Read the call sites
 3. Make changes
 4. Run affected tests OR document manual verification
@@ -297,7 +297,7 @@ After completion, collect implicit feedback:
 
 **Required Servers by Tier**:
 
-- STRICT: None required (native Read, Grep, Glob, Bash and codebase-retrieval cover the prerequisites); codegraph preferred for the "files that import changed code" step; Grep fallback allowed and recorded
+- STRICT: None required (native Read, Grep, Glob, Bash and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) cover the prerequisites); codegraph preferred for the "files that import changed code" step; Grep fallback allowed and recorded
 - STANDARD: Context7 (fallback allowed)
 - LIGHT: None required (fallback allowed)
 - EXEMPT: None required
@@ -312,7 +312,7 @@ After completion, collect implicit feedback:
 **Planning Phase**:
 
 1. TodoWrite: Create task breakdown
-2. codebase-retrieval: Load context
+2. `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`): Load context
 3. Glob / Read: Check project state in `.superclaude/memory/**/*.md`
 
 **Execution Phase**:
diff --git a/src/superclaude/skills/task-builder/SKILL.md b/src/superclaude/skills/task-builder/SKILL.md
index 417daa64..48a29147 100644
--- a/src/superclaude/skills/task-builder/SKILL.md
+++ b/src/superclaude/skills/task-builder/SKILL.md
@@ -336,7 +336,7 @@ Independent means ALL of these are true:
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the problem space. This must happen BEFORE spawning researchers so each researcher gets a focused assignment from the scope map.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the problem space. This must happen BEFORE spawning researchers so each researcher gets a focused assignment from the scope map.
 
 **Adjust depth by scenario:**
 
@@ -1205,7 +1205,7 @@ Agent:
     overrides your agent definition's Critical Rule 6 ("ALWAYS broadcast
     TASK_READY") and Step 6 (TaskCreate + broadcast). Instead, return the
     task file path as your final output.
-    - **Codebase questions** → use WebSearch or codebase-retrieval
+    - **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)
     - **External docs/syntax** → use WebSearch
     - **If blocked** → create the best task file you can and note gaps
       in the Task Log section. The skill will review and iterate.
diff --git a/src/superclaude/skills/task/SKILL.md b/src/superclaude/skills/task/SKILL.md
index b2578d72..86e230ce 100644
--- a/src/superclaude/skills/task/SKILL.md
+++ b/src/superclaude/skills/task/SKILL.md
@@ -597,7 +597,7 @@ These rules apply across ALL task file executions. Violations compromise executi
 
 5. **Evidence-based completion only.** An item is only complete when there is evidence — a file was written, a command produced output, a verification passed. Never mark an item `- [x]` based on "I think I did that" or "that should be fine."
 
-6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations. Use Edit for file modifications, not `sed` or `awk`.
+6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations. Use Edit for file modifications, not `sed` or `awk`.
 
 7. **One item at a time (with parallel exception).** The default is strictly sequential — complete one item fully before starting the next. The ONLY exception is parallel agent spawning of independent items within the same phase. Even then, each agent's completion is tracked individually.
 
diff --git a/src/superclaude/skills/tdd/SKILL.md b/src/superclaude/skills/tdd/SKILL.md
index 47c4cd8c..02b460a8 100644
--- a/src/superclaude/skills/tdd/SKILL.md
+++ b/src/superclaude/skills/tdd/SKILL.md
@@ -194,7 +194,7 @@ Example: "Create a TDD for the wizard"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the component's architecture. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the component's architecture. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 
@@ -212,7 +212,7 @@ Use Glob, Grep, and codebase-retrieval to map the component's architecture. This
    - External integration points (imports from outside the component)
    - **If PRD_REF is provided**, read the PRD and extract: relevant epics, user stories, acceptance criteria, technical requirements, technology stack, success metrics/KPIs, scope definition (in/out/deferred), performance/security/scalability requirements.
 
-2a. **Reuse-neighbour search (orchestrator-level — NOT a nested research subagent)** — for each proposed new component / helper / pipeline-step, delegate to the `reuse-auditor` agent: `Task(reuse-auditor, candidates=<proposed components>, stage=pre, repo_root, output_path=${TASK_DIR}research/reuse-audit.yaml)`. Run this **here, at orchestrator level during scope discovery** — explicitly NOT inside a spawned Phase-2 research subagent (avoids subagent→agent nesting; see `mem:reference_subagent_cannot_nest_skill_fanout`). The agent returns, per proposed component, a name-agnostic capability fingerprint, grounded neighbours (`file:line`), composite scores, similarity tier, and a verdict (`reuse-by-import | mirror-shape | extract-shared | distinct`). Record the findings for A.4 `## REUSE_AUDIT`. Pre-stage is **always advisory** (no code has shipped). Fallback: agent unavailable → inline capability-keyed `codebase-retrieval` + grep-skeleton sweep, findings advisory-only; never STOP.
+2a. **Reuse-neighbour search (orchestrator-level — NOT a nested research subagent)** — for each proposed new component / helper / pipeline-step, delegate to the `reuse-auditor` agent: `Task(reuse-auditor, candidates=<proposed components>, stage=pre, repo_root, output_path=${TASK_DIR}research/reuse-audit.yaml)`. Run this **here, at orchestrator level during scope discovery** — explicitly NOT inside a spawned Phase-2 research subagent (avoids subagent→agent nesting; see `mem:reference_subagent_cannot_nest_skill_fanout`). The agent returns, per proposed component, a name-agnostic capability fingerprint, grounded neighbours (`file:line`), composite scores, similarity tier, and a verdict (`reuse-by-import | mirror-shape | extract-shared | distinct`). Record the findings for A.4 `## REUSE_AUDIT`. Pre-stage is **always advisory** (no code has shipped). Fallback: agent unavailable → inline capability-keyed `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) + grep-skeleton sweep, findings advisory-only; never STOP.
 
 3. **Plan research assignments** — divide the component into specific investigation topics, each becoming a subagent assignment. Common topics for TDDs:
    - Architecture and system design patterns
diff --git a/src/superclaude/skills/tdd/refs/build-request-template.md b/src/superclaude/skills/tdd/refs/build-request-template.md
index e4b822df..2229ffb0 100644
--- a/src/superclaude/skills/tdd/refs/build-request-template.md
+++ b/src/superclaude/skills/tdd/refs/build-request-template.md
@@ -91,7 +91,7 @@ will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
 
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 
diff --git a/src/superclaude/skills/tech-reference/SKILL.md b/src/superclaude/skills/tech-reference/SKILL.md
index ba17aa9f..42c39edb 100644
--- a/src/superclaude/skills/tech-reference/SKILL.md
+++ b/src/superclaude/skills/tech-reference/SKILL.md
@@ -224,7 +224,7 @@ Example: "Document the agent system"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the feature's shape. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the feature's shape. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 - **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
@@ -477,7 +477,7 @@ Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
 will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 
diff --git a/src/superclaude/skills/tech-research/SKILL.md b/src/superclaude/skills/tech-research/SKILL.md
index d33efdf6..47418499 100644
--- a/src/superclaude/skills/tech-research/SKILL.md
+++ b/src/superclaude/skills/tech-research/SKILL.md
@@ -214,7 +214,7 @@ Example: "Research the agent system"
 
 ### A.3: Perform Scope Discovery
 
-Use Glob, Grep, and codebase-retrieval to map the problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
+Use Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map the problem space. This must happen BEFORE building the task file so the builder can enumerate specific investigation assignments.
 
 **Adjust depth by scenario:**
 - **Scenario A**: Focused discovery — verify the files/directories the user mentioned exist, scan for related code, identify gaps in what the user specified.
@@ -451,7 +451,7 @@ Do NOT broadcast TASK_READY, use TaskCreate, or use SendMessage — these tools
 will fail because there is no team. This overrides your agent definition's
 Critical Rule 6 ("ALWAYS broadcast TASK_READY") and Step 6 (TaskCreate + broadcast).
 Instead, return the task file path as your final output.
-- **Codebase questions** → use WebSearch or codebase-retrieval (you have access)
+- **Codebase questions** → use WebSearch or `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`); you have access
 - **External docs/syntax** → use WebSearch
 - **If blocked** → create the best task file you can and note gaps in the Task Log section. The skill will review and iterate.
 
@@ -1618,7 +1618,7 @@ Violations compromise research quality.
 
 5. **No one-shotting reports.** Agents must write incrementally as they discover information. The orchestrator must write the final report section by section. This is non-negotiable.
 
-6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, codebase-retrieval for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.
+6. **Use dedicated tools.** Use Glob for file search, Grep for content search, Read for file reading, `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) for semantic code search. Do NOT use bash `find`, `grep`, `cat`, `head`, `tail`, `rg`, or `awk` commands for these operations.
 
 7. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps. This keeps web research focused and efficient.
 
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
