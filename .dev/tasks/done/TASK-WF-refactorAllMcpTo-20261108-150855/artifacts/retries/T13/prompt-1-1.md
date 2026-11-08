ac980dee6087a0dafbc2c06717fad85da8a9f454
Review one task for spec compliance.

Task brief: ## Task 13: Update comments and user docs

Design sections 3.7 item 2 and 3.9. `src/superclaude/cli/reflect/config.py` (about lines 162, 199): comment only; reword "so auggie stays indexed" to say the reviewer worktree is kept inside the repository so Grep and codegraph reach it. `docs/user-guide/mcp-servers.md`: AUG short form at about line 138; in the litellm section (about lines 148-159) add the served tool list and the AUG parameters and pushed-code-only note. `docs/user-guide/eval-pipeline.md` (about lines 263-265): add `mcp__litellm__` to the listed prefixes. `docs/user-guide/brainstorm.md` (17) and `docs/user-guide/commands.md` (784, 935): name AUG first, then `mcp__auggie__codebase-retrieval`, replacing `auggie-mcp`. `docs/guides/prd-skill-release-guide.md` (161, 434) and `docs/guides/tdd-skill-release-guide.md` (160, 441): AUG short form. Leave `docs/eval/validation-commands.md:84` (dated observed record), `docs/testing/` records and other bare-word docs unchanged.

Depends on: Task 2

Acceptance criteria:
- `git diff src/superclaude/cli/reflect/config.py` changes comment lines only.
- `uv run pytest tests -k "docs or reflect_config" -v` passes (or reports no tests selected, recorded); output saved to `./artifacts/t13-pytest.log`.
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
Start sha: ac980dee6087a0dafbc2c06717fad85da8a9f454
Diff against the start snapshot: diff --git a/docs/guides/prd-skill-release-guide.md b/docs/guides/prd-skill-release-guide.md
index 250cb663..b3285b2c 100644
--- a/docs/guides/prd-skill-release-guide.md
+++ b/docs/guides/prd-skill-release-guide.md
@@ -158,7 +158,7 @@ The PRD pipeline generates a comprehensive product requirements document through
 Stage A: Scope Discovery (orchestrator)
   A.1: Check for existing task file
   A.2: Parse & triage PRD request
-  A.3: Perform scope discovery (Glob, Grep, codebase-retrieval)
+  A.3: Perform scope discovery (Glob, Grep, `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`))
   A.4: Write research notes file
   A.5: Review research sufficiency (MANDATORY GATE)
   A.6: Template triage (01 or 02)
@@ -431,7 +431,7 @@ These rules come from the PRD template and apply to every generated PRD.
 
 1. **Check for existing task file** — looks in `.dev/tasks/to-do/` for `TASK-PRD-*/` matching this product. If found with unchecked items, resumes from there.
 2. **Parse & triage** — classifies request into Scenario A (explicit, all inputs provided) or Scenario B (vague, broad discovery needed).
-3. **Scope discovery** — uses Glob, Grep, and codebase-retrieval to map files, subsystems, integration points, and existing documentation.
+3. **Scope discovery** — uses Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map files, subsystems, integration points, and existing documentation.
 4. **Write research notes** — structured file with 7 categories: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER.
 5. **Sufficiency gate** — mandatory review of research notes quality (8-point checklist). Max 2 gap-fill rounds.
 6. **Template triage** — almost always Template 02 (Complex Task) for PRD creation.
diff --git a/docs/guides/tdd-skill-release-guide.md b/docs/guides/tdd-skill-release-guide.md
index f9164422..95ad0425 100644
--- a/docs/guides/tdd-skill-release-guide.md
+++ b/docs/guides/tdd-skill-release-guide.md
@@ -157,7 +157,7 @@ The TDD pipeline generates a comprehensive technical design document through par
 Stage A: Scope Discovery (orchestrator)
   A.1: Check for existing task file
   A.2: Parse & triage TDD request (Scenario A vs B)
-  A.3: Perform scope discovery (Glob, Grep, codebase-retrieval)
+  A.3: Perform scope discovery (Glob, Grep, `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`))
   A.4: Write research notes file (8 categories)
   A.5: Review research sufficiency (MANDATORY GATE)
   A.6: Template triage (01 or 02)
@@ -438,7 +438,7 @@ These rules come from the TDD template and apply to every generated TDD.
 
 1. **Check for existing task file** — looks in `.dev/tasks/to-do/` for `TASK-TDD-*/` matching this component. If found with unchecked items, resumes from there. Also checks for `research-notes.md` with partial progress.
 2. **Parse & triage** — classifies request into Scenario A (explicit, most inputs provided) or Scenario B (vague, broad discovery needed). Does NOT interrogate the user — proceeds with what it has.
-3. **Scope discovery** — uses Glob, Grep, and codebase-retrieval to map files, subsystems, integration points, and existing documentation. Optionally spawns `rf-task-researcher` for complex Scenario B discoveries.
+3. **Scope discovery** — uses Glob, Grep, and `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`) to map files, subsystems, integration points, and existing documentation. Optionally spawns `rf-task-researcher` for complex Scenario B discoveries.
 4. **Write research notes** — structured file with 8 categories: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, PRD_CONTEXT, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER.
 5. **Sufficiency gate** — mandatory review of research notes quality (8-point checklist including doc staleness verification). Max 2 gap-fill rounds.
 6. **Template triage** — almost always Template 02 (Complex Task) for TDD creation.
diff --git a/docs/user-guide/brainstorm.md b/docs/user-guide/brainstorm.md
index 9339e5af..d31ba584 100644
--- a/docs/user-guide/brainstorm.md
+++ b/docs/user-guide/brainstorm.md
@@ -14,7 +14,7 @@ For which tool to use when, see [How We Work](how-we-work.md).
 | Codebase context | Single Auggie shot | Auto-routed `/sc:analyze` or Auggie quick scan, gated by domain; falls back to codegraph, then Glob/Grep |
 | Research | Mentioned, not wired | Auto-invokes `/sc:research` (light) or `tech-research` (deep) |
 | Handoff | Text suggestion only | Flag-gated invocation of `/sc:design`, `/sc:tasklist`, or `/task-builder` |
-| MCP servers | context7, magic, playwright, morphllm, auggie-mcp | auggie-mcp, codegraph, tavily |
+| MCP servers | context7, magic, playwright, morphllm, auggie-mcp | `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`), codegraph, tavily |
 | Personas | 7-persona auto-activation soup | 3 personas auto-selected per detected domain |
 
 v2 does **not** re-implement debate, scoring, or merge logic — those are delegated to `sc-adversarial-protocol`. v2's value is orchestration.
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index c5b5c3bb..029bb55e 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -781,7 +781,7 @@ Full option list: `~/.claude/commands/sc/roadmap.md`.
 /sc:tdd --resume .dev/tasks/to-do/TASK-TDD-20260401-143022/TASK-TDD-20260401-143022.md
 ```
 
-**MCP servers:** context7, auggie-mcp
+**MCP servers:** context7, `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)
 
 ---
 
@@ -932,7 +932,7 @@ The command hands its arguments to the `sc-validate-roadmap-protocol` skill, whi
 /sc:brainstorm "improve onboarding workflow" --dry-run --strategy enterprise
 ```
 
-**MCP servers:** auggie-mcp, codegraph, tavily  
+**MCP servers:** `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`), codegraph, tavily  
 **Personas:** architect, analyzer, scribe (auto-selected per detected domain)
 
 → Full guide: [brainstorm.md](brainstorm.md)
diff --git a/docs/user-guide/eval-pipeline.md b/docs/user-guide/eval-pipeline.md
index 4de9c9d4..b23bcfce 100644
--- a/docs/user-guide/eval-pipeline.md
+++ b/docs/user-guide/eval-pipeline.md
@@ -258,11 +258,12 @@ The FR-G5 hook-matcher coverage gate enforces that **every** PostToolUse hook ma
 - `eval doctor --check-coverage [--suite <name>]` — wires the FR-G5 coverage gate marker into the doctor payload (`eval doctor --help`: "full gate lands in M4 T04.14")
 - `eval run` — implicit at the top of every run, AFTER suite parse and BEFORE any worker is dispatched (so a coverage breach short-circuits without touching any per-eval HOME)
 
-**v1 coverage scope:** the three auggie-prefix matcher families:
+**v1 coverage scope:** the four auggie-prefix matcher families:
 
 - `mcp__auggie__*`
 - `mcp__auggie-mcp__*`
 - `mcp__airis-mcp-gateway__*`
+- `mcp__litellm__*`
 
 **Failure modes:**
 
diff --git a/docs/user-guide/mcp-servers.md b/docs/user-guide/mcp-servers.md
index 2b721ada..9f393415 100644
--- a/docs/user-guide/mcp-servers.md
+++ b/docs/user-guide/mcp-servers.md
@@ -135,7 +135,7 @@ export TAVILY_API_KEY="tvly-your_api_key_here"
 **Purpose**: Augment Code semantic codebase search and retrieval
 **Triggers**: Natural-language questions about an unfamiliar codebase, architectural concepts, cross-file recall before significant edits
 **Requirements**: Node.js 20+, global `@augmentcode/auggie` install (the installer pins `@augmentcode/auggie@0.36.0`), one-time `auggie login` (or `AUGMENT_SESSION_AUTH` env var)
-**Tools**: the shipped description names `codebase-retrieval` and `ask_question`
+**Tools**: the shipped description names `codebase-retrieval` and `ask_question`. Codebase search is `mcp__litellm__augment_code-augment_code_search` (else `mcp__auggie__codebase-retrieval`)
 
 ```bash
 # Install via SuperClaude (handles npm install -g + claude mcp add)
@@ -158,6 +158,14 @@ superclaude mcp --servers litellm
 
 The registration stores the literal text `Bearer ${LITELLM_API_KEY}` in the `x-litellm-api-key` header, never the key itself. Claude Code reads the variable when it connects, so rotating the key needs no reinstall. Check with `claude mcp list`: litellm should show Connected (a 401 means the variable was empty when Claude Code started).
 
+**Tools served** (each named `mcp__litellm__<tool>`):
+
+- `augment_code-augment_code_search`: Augment codebase search. Pass `repo_owner` and `repo_name` from `git remote get-url origin` and `branch` = the default branch. It searches pushed code only; for uncommitted or unpushed changes use codegraph or Grep.
+- `Tavily-tavily_search`, `Tavily-tavily_extract`, `Tavily-tavily_map`, `Tavily-tavily_crawl`, `Tavily-tavily_research`: Tavily web search and extraction.
+- `context7-resolve-library-id`, `context7-query-docs`: Context7 library documentation.
+
+Commands and agents name the proxy tool first and the direct tool second (for example `mcp__litellm__augment_code-augment_code_search` else `mcp__auggie__codebase-retrieval`), so both direct installs and the proxy work.
+
 ## Unified MCP Gateway (Alternative Setup)
 
 For users who want a simpler, unified setup that manages many MCP servers through a single endpoint, **AIRIS MCP Gateway** provides:
diff --git a/src/superclaude/cli/reflect/config.py b/src/superclaude/cli/reflect/config.py
index 5e9938b2..51ccb1aa 100644
--- a/src/superclaude/cli/reflect/config.py
+++ b/src/superclaude/cli/reflect/config.py
@@ -159,7 +159,8 @@ def create_review_snapshot(config) -> tuple[Path | None, str | None]:
     free of any raw ``subprocess`` import (NFR-1 thinness guard). Returns
     ``(snapshot_path, None)`` on success, or ``(None, stop_reason)`` on a
     precondition STOP. NEVER falls back to the live tree. Uses a REAL worktree
-    checkout (NOT an archive) so auggie stays indexed (A-2).
+    checkout (NOT an archive), kept inside the repository so Grep and codegraph
+    reach it (A-2).
 
     Lifecycle:
       1. PRE-CLEAN a leftover ``<output>/_review-snapshot`` via ``git worktree
@@ -196,7 +197,8 @@ def create_review_snapshot(config) -> tuple[Path | None, str | None]:
         return (None, "no-committable-ref")
     if current_head != config.head:
         return (None, "head-moved-precondition")
-    # (3) Real worktree checkout (NOT archive) so auggie stays indexed.
+    # (3) Real worktree checkout (NOT archive), kept inside the repository so Grep
+    # and codegraph reach it.
     config.output_dir.mkdir(parents=True, exist_ok=True)
     try:
         _git(git_cwd, "worktree", "add", "--detach", str(snapshot), current_head)
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
