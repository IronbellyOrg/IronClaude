dbc15d2f543daf23650db79cf5428408f37b2107
Review one task for spec compliance.

Task brief: ## Task 3: Add proxy Tavily, Context7 and Playwright names to the research agents

Design section 3.1 items 1-5. In the `tools:` lists of `src/superclaude/agents/deep-research.md`, `deep-research-agent.md`, `rf-analyst.md`, `rf-assembler.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-task-builder.md`, `rf-task-executor.md`, `rf-task-researcher.md`, `rf-team-lead.md` insert `mcp__litellm__Tavily-tavily_<x>` before each `mcp__tavily__tavily_<x>` already listed (do not add map/crawl where absent). In `deep-research.md` and `deep-research-agent.md` insert the two Context7 proxy names before their direct twins; in `deep-research-agent.md` insert `mcp__plugin_playwright_playwright__browser_navigate`, `_snapshot`, `_evaluate` before the three `mcp__playwright__browser_*` entries. Rewrite the Tavily body prose of the same ten files (change-map Agents row 4: `deep-research.md:27,35,41,43,59`, `deep-research-agent.md:145,147,148,152,154`, `rf-analyst.md:365,367,373,422-423`, `rf-assembler.md:230-231,237,288`, `rf-qa.md:119-120,125,549`, `rf-qa-qualitative.md:126-127,132,809`, `rf-task-builder.md:430,443-445,561`, `rf-task-executor.md:356`, `rf-task-researcher.md:328,353,371-376,417`, `rf-team-lead.md:307,309,315,398`) to the Tavily phrase; the tool-presence test in `deep-research.md` (about line 59) and the `tavily_unavailable` test in `deep-research-agent.md` become "neither ... nor ...". Rewrite the wildcards at `deep-research.md` (about line 37) and `rf-task-researcher.md` (about line 543). Leave `description:` lines unchanged. Widen `_TAVILY_ID` in `tests/agents/test_tavily_tool_parity.py` (about line 27) to `mcp__(?:tavily__tavily|litellm__Tavily-tavily)_[a-z]+` and add an assertion that each listed direct Tavily name has its proxy twin listed before it; update `tests/core/test_research_config.py` only if a pinned agent string changes.

Acceptance criteria:
- Every one of the ten agents lists a proxy Tavily name immediately before each direct Tavily name it lists; no direct name was removed (`git diff` shows only added list entries in `tools:` lines).
- `uv run pytest tests/agents tests/skills/test_tier2_tavily_consistency.py tests/core/test_research_config.py -v` passes; output saved to `./artifacts/t3-pytest.log`.
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
Start sha: dbc15d2f543daf23650db79cf5428408f37b2107
Diff against the start snapshot: diff --git a/src/superclaude/agents/deep-research-agent.md b/src/superclaude/agents/deep-research-agent.md
index 1db004a5..d682d0a3 100644
--- a/src/superclaude/agents/deep-research-agent.md
+++ b/src/superclaude/agents/deep-research-agent.md
@@ -3,16 +3,25 @@ name: deep-research-agent
 description: Specialist for comprehensive research with adaptive strategies and intelligent exploration. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
 category: analysis
 tools:
+  - mcp__litellm__Tavily-tavily_search
   - mcp__tavily__tavily_search
+  - mcp__litellm__Tavily-tavily_extract
   - mcp__tavily__tavily_extract
+  - mcp__litellm__Tavily-tavily_map
   - mcp__tavily__tavily_map
+  - mcp__litellm__Tavily-tavily_crawl
   - mcp__tavily__tavily_crawl
   - WebSearch
   - WebFetch
+  - mcp__litellm__context7-resolve-library-id
   - mcp__context7__resolve-library-id
+  - mcp__litellm__context7-query-docs
   - mcp__context7__query-docs
+  - mcp__plugin_playwright_playwright__browser_navigate
   - mcp__playwright__browser_navigate
+  - mcp__plugin_playwright_playwright__browser_snapshot
   - mcp__playwright__browser_snapshot
+  - mcp__plugin_playwright_playwright__browser_evaluate
   - mcp__playwright__browser_evaluate
   - Read
   - Grep
@@ -132,7 +141,7 @@ breadth) — record this loss of fidelity.
 
 `fallback_reason` enum (set whenever a non-`tavily` backend is used in place of a Tavily op):
 
-- `tavily_unavailable` — the Tavily tool was not loaded / not configured this session
+- `tavily_unavailable` — neither `mcp__litellm__Tavily-tavily_search` nor `mcp__tavily__tavily_search` was loaded / configured this session
 - `tavily_error` — Tavily returned a tool-level error after one retry
 - `tavily_rate_limited` — Tavily returned an explicit rate-limit signal
 - `map_unsupported_fallback` — `tavily-map` requested but unavailable; degraded to WebSearch discovery
@@ -142,16 +151,16 @@ breadth) — record this loss of fidelity.
 
 **Search Strategy**
 
-1. Broad initial searches via `mcp__tavily__tavily_search`
+1. Broad initial searches via `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`)
 2. Identify key sources
-3. Deep extraction via `mcp__tavily__tavily_extract` as needed
-4. Follow interesting leads (re-issuing `mcp__tavily__tavily_search` with refined queries)
+3. Deep extraction via `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) as needed
+4. Follow interesting leads (re-issuing `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) with refined queries)
 
 **Discovery Routing** (map/crawl — research engine only)
 
-- `mcp__tavily__tavily_map` — site-structure discovery: enumerate a site's URL graph before
+- `mcp__litellm__Tavily-tavily_map` (else `mcp__tavily__tavily_map`) — site-structure discovery: enumerate a site's URL graph before
   targeted extraction. Enabled at the **deep** profile and above; cap `maps=2` per run.
-- `mcp__tavily__tavily_crawl` — deep domain traversal: follow links across a domain to gather
+- `mcp__litellm__Tavily-tavily_crawl` (else `mcp__tavily__tavily_crawl`) — deep domain traversal: follow links across a domain to gather
   many pages. Enabled at the **exhaustive** profile only; cap `crawls=1` per run, and the
   result set is truncated to a maximum of **50 URLs**.
 - Typical flow: `map` a domain → `extract` the high-value URLs; escalate to `crawl` only when
diff --git a/src/superclaude/agents/deep-research.md b/src/superclaude/agents/deep-research.md
index 02fbc750..a81fb60e 100644
--- a/src/superclaude/agents/deep-research.md
+++ b/src/superclaude/agents/deep-research.md
@@ -3,13 +3,19 @@ name: deep-research
 description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
 category: analysis
 tools:
+  - mcp__litellm__Tavily-tavily_search
   - mcp__tavily__tavily_search
+  - mcp__litellm__Tavily-tavily_extract
   - mcp__tavily__tavily_extract
+  - mcp__litellm__Tavily-tavily_map
   - mcp__tavily__tavily_map
+  - mcp__litellm__Tavily-tavily_crawl
   - mcp__tavily__tavily_crawl
   - WebSearch
   - WebFetch
+  - mcp__litellm__context7-resolve-library-id
   - mcp__context7__resolve-library-id
+  - mcp__litellm__context7-query-docs
   - mcp__context7__query-docs
   - Read
   - Grep
@@ -24,7 +30,7 @@ Deploy this agent whenever the SuperClaude Agent needs authoritative information
 
 - Clarify the research question, depth (`quick`, `standard`, `deep`, `exhaustive`), and deadlines.
 - Draft a lightweight plan (goals, search pivots, likely sources).
-- Execute web searches using Tavily MCP (`mcp__tavily__tavily_search`) as the primary tool. Use `mcp__tavily__tavily_extract` for page content extraction. Only fall back to WebSearch / WebFetch when Tavily MCP is unavailable (see Fallback Policy below). Use Context7 for official library/framework docs and native reasoning for multi-step synthesis.
+- Execute web searches using Tavily MCP (`mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`)) as the primary tool. Use `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) for page content extraction. Only fall back to WebSearch / WebFetch when Tavily MCP is unavailable (see Fallback Policy below). Use Context7 for official library/framework docs and native reasoning for multi-step synthesis.
 - Track sources with credibility notes and timestamps.
 - Deliver a concise synthesis plus a citation table.
 
@@ -32,15 +38,15 @@ Deploy this agent whenever the SuperClaude Agent needs authoritative information
 
 ### Tavily-first rule (web search / extraction)
 
-1. **Primary**: `mcp__tavily__tavily_search` for all web search queries; `mcp__tavily__tavily_extract` for fetching specific URLs / page content.
+1. **Primary**: `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) for all web search queries; `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) for fetching specific URLs / page content.
 2. **Fallback**: `WebSearch` (search) and `WebFetch` (single-URL fetch) are used **only** when Tavily MCP is unavailable.
-3. **Library docs**: `mcp__context7__*` remains primary for library/framework/SDK documentation (not subject to the Tavily-first rule — Context7 is a separate axis).
+3. **Library docs**: `mcp__litellm__context7-*` or `mcp__context7__*` remains primary for library/framework/SDK documentation (not subject to the Tavily-first rule — Context7 is a separate axis).
 
 ### Discovery Routing (map/crawl — research engine only)
 
-- `mcp__tavily__tavily_map` — site-structure discovery: enumerate a site's URL graph before
+- `mcp__litellm__Tavily-tavily_map` (else `mcp__tavily__tavily_map`) — site-structure discovery: enumerate a site's URL graph before
   targeted extraction. Enabled at the **deep** profile and above; cap `maps=2` per run.
-- `mcp__tavily__tavily_crawl` — deep domain traversal: follow links across a domain to gather
+- `mcp__litellm__Tavily-tavily_crawl` (else `mcp__tavily__tavily_crawl`) — deep domain traversal: follow links across a domain to gather
   many pages. Enabled at the **exhaustive** profile only; cap `crawls=1` per run, result set
   truncated to a maximum of **50 URLs**.
 - Typical flow: `map` a domain → `extract` the high-value URLs; escalate to `crawl` only when
@@ -56,7 +62,7 @@ Deploy this agent whenever the SuperClaude Agent needs authoritative information
 
 Treat Tavily MCP as unavailable, and fall back to WebSearch/WebFetch, when **any** of the following holds:
 
-- The `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` tools are not present in the available tool surface for this session (not loaded / not configured).
+- Neither the `mcp__litellm__Tavily-tavily_search` / `mcp__litellm__Tavily-tavily_extract` tools nor the `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` tools are present in the available tool surface for this session (not loaded / not configured).
 - A Tavily call returns a transport-level error (timeout, connection refused, 5xx) **twice in a row** for the same query.
 - A Tavily call returns an explicit rate-limit / quota-exceeded error.
 - A Tavily call returns an authentication error (missing/invalid API key).
diff --git a/src/superclaude/agents/rf-analyst.md b/src/superclaude/agents/rf-analyst.md
index 3d6a0b95..79195f44 100644
--- a/src/superclaude/agents/rf-analyst.md
+++ b/src/superclaude/agents/rf-analyst.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search    # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_search    # PRIMARY web search (rare use; see body)
+  - mcp__litellm__Tavily-tavily_extract   # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_extract   # PRIMARY web content extraction (rare use)
   - WebSearch                      # FALLBACK only - Tavily unavailable
   - WebFetch                       # FALLBACK only - Tavily unavailable
@@ -362,15 +364,15 @@ a doc-sourced claim against an external reference (URL cited in a
 research file, official documentation URL referenced in a verification
 tag), use Tavily MCP first:
 
-- `mcp__tavily__tavily_extract` for known URLs cited in research files
+- `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) for known URLs cited in research files
   when you must verify a claim's source.
-- `mcp__tavily__tavily_search` only when the spawn prompt directs you to
+- `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) only when the spawn prompt directs you to
   look up a specific external reference.
 
 **Fall back to `WebFetch` / `WebSearch` ONLY when Tavily is unavailable.**
 Tavily is considered unavailable if any of:
 
-1. `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` is not
+1. Neither `mcp__litellm__Tavily-tavily_search` / `mcp__litellm__Tavily-tavily_extract` nor `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` is
    loaded in the current session (tool not found).
 2. The Tavily call returns an explicit server error (5xx / auth /
    configuration) on the first attempt AND a single retry.
@@ -419,8 +421,8 @@ After writing your output file:
 8. **Contradictions are important** — always surface them, never resolve them silently
 9. **No unauthorized web research** -- Do NOT fetch from the web unless
    the spawn prompt explicitly directs you to verify a referenced URL or
-   external claim. If authorized, use `mcp__tavily__tavily_search` /
-   `mcp__tavily__tavily_extract` first; fall back to WebSearch / WebFetch only when Tavily
+   external claim. If authorized, use `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) /
+   `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) first; fall back to WebSearch / WebFetch only when Tavily
    is unavailable (tool not loaded, server error after one retry, or
    rate-limited). Mark any fallback in the analysis report. Treat
    unauthorized external content as fabrication-by-import (Rule 7).
diff --git a/src/superclaude/agents/rf-assembler.md b/src/superclaude/agents/rf-assembler.md
index 8a400e1d..1384c3ec 100644
--- a/src/superclaude/agents/rf-assembler.md
+++ b/src/superclaude/agents/rf-assembler.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search    # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_search    # PRIMARY web search (rare use; see body)
+  - mcp__litellm__Tavily-tavily_extract   # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_extract   # PRIMARY web content extraction (rare use)
   - WebSearch                      # FALLBACK only - Tavily unavailable
   - WebFetch                       # FALLBACK only - Tavily unavailable
@@ -227,14 +229,14 @@ explicitly directs you to fetch external content (e.g., resolve a
 linked URL whose content was already cited by a component file), use
 Tavily MCP first:
 
-- `mcp__tavily__tavily_extract` for known URLs in component files.
-- `mcp__tavily__tavily_search` only if the spawn prompt directs you to
+- `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) for known URLs in component files.
+- `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) only if the spawn prompt directs you to
   look up a specific reference.
 
 Fall back to `WebFetch` / `WebSearch` ONLY when Tavily is unavailable.
 Tavily is considered unavailable if:
 
-1. `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` is not
+1. Neither `mcp__litellm__Tavily-tavily_search` / `mcp__litellm__Tavily-tavily_extract` nor `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` is
    loaded in the current session (tool not found).
 2. The Tavily call returns an explicit server error (5xx / auth /
    configuration) on the first attempt AND a single retry.
@@ -285,7 +287,7 @@ After writing the output document:
 7. **Report missing content** — If a section has no source material, mark it explicitly
 8. **Cross-check consistency** — Verify internal references, completeness, and coherence
 9. **Evidence-based assembly** — Every claim in the output must trace to a component file
-10. **No unauthorized web research** - Do NOT fetch from the web unless the spawn prompt or ASSEMBLY_FIX explicitly authorizes it. If authorized, use `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` first; fall back to WebSearch / WebFetch only when Tavily is unavailable (tool not loaded, server error after one retry, or rate-limited). Mark any fallback in the assembled document.
+10. **No unauthorized web research** - Do NOT fetch from the web unless the spawn prompt or ASSEMBLY_FIX explicitly authorizes it. If authorized, use `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) / `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) first; fall back to WebSearch / WebFetch only when Tavily is unavailable (tool not loaded, server error after one retry, or rate-limited). Mark any fallback in the assembled document.
 
 ## Agent Memory
 
diff --git a/src/superclaude/agents/rf-qa-qualitative.md b/src/superclaude/agents/rf-qa-qualitative.md
index 846b57a1..a9981b91 100644
--- a/src/superclaude/agents/rf-qa-qualitative.md
+++ b/src/superclaude/agents/rf-qa-qualitative.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search    # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_search    # PRIMARY web search (Tavily MCP first)
+  - mcp__litellm__Tavily-tavily_extract   # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_extract   # PRIMARY web fetch (Tavily MCP first)
   - WebFetch                      # FALLBACK only -- when Tavily MCP unavailable
   - WebSearch                     # FALLBACK only -- when Tavily MCP unavailable
@@ -123,13 +125,13 @@ When such external lookup is required, you MUST use Tavily MCP first.
 
 **Precedence:**
 
-1. `mcp__tavily__tavily_search` -- for queries / discovery.
-2. `mcp__tavily__tavily_extract` -- for fetching a specific URL's content.
+1. `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) -- for queries / discovery.
+2. `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) -- for fetching a specific URL's content.
 3. **Fallback only:** `WebSearch` / `WebFetch` -- and only when Tavily MCP is unavailable (see detection condition below).
 
 **Detection condition for "Tavily unavailable"** (any of):
 
-- The `mcp__tavily__tavily_search` or `mcp__tavily__tavily_extract` tool is not present in your runtime tool list this session (server not loaded).
+- Neither `mcp__litellm__Tavily-tavily_search` nor `mcp__tavily__tavily_search` (or neither `mcp__litellm__Tavily-tavily_extract` nor `mcp__tavily__tavily_extract`) is present in your runtime tool list this session (server not loaded).
 - The Tavily call returns a structured server error (e.g., 5xx, connection refused, "server not configured").
 - The Tavily call returns a rate-limit / quota error (HTTP 429 or equivalent payload).
 
@@ -806,7 +808,7 @@ Before issuing your verdict, answer these questions in your report:
 
 - Maximum 2 fix cycles. After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. Do NOT convert unfixed findings to Open Questions. All blocking findings must be resolved; minor findings are recorded as notes.
 - Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.
-- **Tavily-first for any external lookup** -- When verifying a claim that requires fetching from the open web (a vendor doc page, an external standard, a third-party API surface, an external link in the document under review), you MUST attempt `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.
+- **Tavily-first for any external lookup** -- When verifying a claim that requires fetching from the open web (a vendor doc page, an external standard, a third-party API surface, an external link in the document under review), you MUST attempt `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) / `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.
 
 ### Fixing Issues (When Authorized)
 
diff --git a/src/superclaude/agents/rf-qa.md b/src/superclaude/agents/rf-qa.md
index b5643b5b..eafbf85f 100644
--- a/src/superclaude/agents/rf-qa.md
+++ b/src/superclaude/agents/rf-qa.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search    # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_search    # PRIMARY web search (Tavily MCP first)
+  - mcp__litellm__Tavily-tavily_extract   # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_extract   # PRIMARY web fetch (Tavily MCP first)
   - WebFetch                      # FALLBACK only -- when Tavily MCP unavailable
   - WebSearch                     # FALLBACK only -- when Tavily MCP unavailable
@@ -116,13 +118,13 @@ When any QA verification step legitimately requires fetching external informatio
 
 **Precedence:**
 
-1. `mcp__tavily__tavily_search` -- for queries / discovery.
-2. `mcp__tavily__tavily_extract` -- for fetching a specific URL's content.
+1. `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) -- for queries / discovery.
+2. `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) -- for fetching a specific URL's content.
 3. **Fallback only:** `WebSearch` / `WebFetch` -- and only when Tavily MCP is unavailable (see detection condition below).
 
 **Detection condition for "Tavily unavailable"** (any of):
 
-- The `mcp__tavily__tavily_search` or `mcp__tavily__tavily_extract` tool is not present in your runtime tool list this session (server not loaded).
+- Neither `mcp__litellm__Tavily-tavily_search` nor `mcp__tavily__tavily_search` (or neither `mcp__litellm__Tavily-tavily_extract` nor `mcp__tavily__tavily_extract`) is present in your runtime tool list this session (server not loaded).
 - The Tavily call returns a structured server error (e.g., 5xx, connection refused, "server not configured").
 - The Tavily call returns a rate-limit / quota error (HTTP 429 or equivalent payload).
 
@@ -546,4 +548,4 @@ If your total (Read + Grep + Glob) calls < TOTAL checklist items, the review is
 9. **Report honestly** — A false PASS is worse than a false FAIL. When in doubt, fail it and explain why.
 10. **Maximum 2 fix cycles** — After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings. All blocking findings must be resolved; minor findings are recorded as notes.
 11. **You are the last line of defense** — If you miss something, it goes into the final report as fact. Take this seriously.
-12. **Tavily-first for any external lookup** -- When verifying a claim that requires fetching from the open web, you MUST attempt `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.
+12. **Tavily-first for any external lookup** -- When verifying a claim that requires fetching from the open web, you MUST attempt `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) / `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.
diff --git a/src/superclaude/agents/rf-task-builder.md b/src/superclaude/agents/rf-task-builder.md
index 898efc44..5fabd530 100644
--- a/src/superclaude/agents/rf-task-builder.md
+++ b/src/superclaude/agents/rf-task-builder.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search
   - mcp__tavily__tavily_search
+  - mcp__litellm__Tavily-tavily_extract
   - mcp__tavily__tavily_extract
   - WebFetch
   - WebSearch
@@ -427,7 +429,7 @@ See SKILL.md "Retry Monotonicity Protocol" for full specification.
 
 ### Web Search (Tavily-first)
 
-**Primary tool:** `mcp__tavily__tavily_search` for verifying library/framework syntax and patterns referenced in checklist items; `mcp__tavily__tavily_extract` when you need the full content of a specific docs URL (e.g., to copy an API signature verbatim into a Context field).
+**Primary tool:** `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) for verifying library/framework syntax and patterns referenced in checklist items; `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) when you need the full content of a specific docs URL (e.g., to copy an API signature verbatim into a Context field).
 
 **Fallback tools:** `WebSearch` and `WebFetch` -- use ONLY when Tavily is unavailable (see Fallback Conditions below).
 
@@ -440,9 +442,10 @@ Use Tavily search when:
 **Examples:**
 
 ```text
-mcp__tavily__tavily_search: "Jest test file naming conventions and structure"
-mcp__tavily__tavily_search: "Dockerfile multi-stage build syntax"
-mcp__tavily__tavily_search: "SQLAlchemy migration file structure"
+mcp__litellm__Tavily-tavily_search: "Jest test file naming conventions and structure"
+mcp__litellm__Tavily-tavily_search: "Dockerfile multi-stage build syntax"
+mcp__litellm__Tavily-tavily_search: "SQLAlchemy migration file structure"
+# else mcp__tavily__tavily_search with the same query
 ```
 
 **Fallback Conditions -- fall back to WebSearch / WebFetch only when ANY of these are true:**
@@ -558,7 +561,7 @@ Use current date/time for the timestamp.
 10. **QA gates are checklist items, not prose.** When QA_GATE_REQUIREMENTS is FINAL_ONLY or PER_PHASE, you MUST encode QA gate checklist items in the generated task file. QA gates described only in prose or comments are invisible to the F1 executor and will be skipped. A generated task file that omits required QA gates is a MALFORMED output. When QA_INTENSITY is lite or standard, generate FEWER QA items per gate (matching the I22 agent counts), combining lens focuses into single agents as specified by the calling skill's QA Intensity Adaptation table in its Agent Prompt Templates section.
 11. **Validation items are mandatory when specified.** When VALIDATION_REQUIREMENTS is non-empty, you MUST encode corresponding validation checklist items. A task file with implementation items but no validation items (when VALIDATION_REQUIREMENTS is specified) is a MALFORMED output.
 12. **Testing items are mandatory when specified.** When TESTING_REQUIREMENTS is not NONE or N/A, you MUST encode testing checklist items with test file paths, commands, and pass criteria. A generated task file that requires testing items but omits them is a MALFORMED output.
-13. **Tavily-first for web fact-checking** -- When the builder consults the web to verify library/framework syntax or patterns for checklist-item Context fields, the call MUST go through `mcp__tavily__tavily_search` or `mcp__tavily__tavily_extract` first.
+13. **Tavily-first for web fact-checking** -- When the builder consults the web to verify library/framework syntax or patterns for checklist-item Context fields, the call MUST go through `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) or `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) first.
     `WebSearch` / `WebFetch` are fallbacks bound by the three Fallback Conditions in the "Web Search (Tavily-first)" section.
     When a fallback fires, the affected checklist item MUST carry the `<!-- web-provenance: provider=WebSearch reason=<...> -->` annotation in its Context field.
     Web-sourced facts in checklist items without provenance annotation MUST be assumed to have been Tavily-sourced; silently using WebSearch when Tavily is available is a protocol violation and a downstream rf-qa risk because the verdict's evidence trail becomes ambiguous.
diff --git a/src/superclaude/agents/rf-task-executor.md b/src/superclaude/agents/rf-task-executor.md
index 911b71b7..6fe2fd6c 100644
--- a/src/superclaude/agents/rf-task-executor.md
+++ b/src/superclaude/agents/rf-task-executor.md
@@ -12,7 +12,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search
   - mcp__tavily__tavily_search
+  - mcp__litellm__Tavily-tavily_extract
   - mcp__tavily__tavily_extract
   - WebFetch
   - WebSearch
@@ -353,7 +355,7 @@ Confirm they have content and match expectations.
 4. **REPORT PROGRESS** - Message the team with status updates
 5. **CLAIM TASKS** - Update task list when starting
 6. **BROADCAST COMPLETION** - So team knows when done
-7. **Tavily-first for any web operation** - Web search and web fetch are NOT part of your documented workflow. If a recovery scenario forces you to consult the web (e.g., investigating an obscure `automated_qa_workflow.sh` error before reporting `EXECUTION_ERROR`), the call MUST go through `mcp__tavily__tavily_search` or `mcp__tavily__tavily_extract` first. `WebSearch` / `WebFetch` are fallbacks; fall back ONLY when (a) the Tavily tool is not loaded / unavailable, (b) Tavily returns a tool-level error after one retry, or (c) Tavily returns an explicit rate-limit signal. Log the provider in your `EXECUTION_PROGRESS` or `EXECUTION_ERROR` message using the format: `web-lookup: provider=<tavily|WebSearch reason=...>`. Silently using `WebSearch` / `WebFetch` when Tavily is available is a protocol violation.
+7. **Tavily-first for any web operation** - Web search and web fetch are NOT part of your documented workflow. If a recovery scenario forces you to consult the web (e.g., investigating an obscure `automated_qa_workflow.sh` error before reporting `EXECUTION_ERROR`), the call MUST go through `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) or `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) first. `WebSearch` / `WebFetch` are fallbacks; fall back ONLY when (a) the Tavily tool is not loaded / unavailable, (b) Tavily returns a tool-level error after one retry, or (c) Tavily returns an explicit rate-limit signal. Log the provider in your `EXECUTION_PROGRESS` or `EXECUTION_ERROR` message using the format: `web-lookup: provider=<tavily|WebSearch reason=...>`. Silently using `WebSearch` / `WebFetch` when Tavily is available is a protocol violation.
 
 ## What NOT To Do
 
diff --git a/src/superclaude/agents/rf-task-researcher.md b/src/superclaude/agents/rf-task-researcher.md
index 8483d0ce..623c9845 100644
--- a/src/superclaude/agents/rf-task-researcher.md
+++ b/src/superclaude/agents/rf-task-researcher.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search
   - mcp__tavily__tavily_search
+  - mcp__litellm__Tavily-tavily_extract
   - mcp__tavily__tavily_extract
   - WebFetch
   - WebSearch
@@ -325,7 +327,7 @@ Not every task needs external research. Use this decision guide:
 
 ### What to Research
 
-When external research IS warranted, use Tavily (`mcp__tavily__tavily_search`) to investigate (fall back to WebSearch only per Web Search (Tavily-first) -> Fallback Conditions):
+When external research IS warranted, use Tavily (`mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`)) to investigate (fall back to WebSearch only per Web Search (Tavily-first) -> Fallback Conditions):
 
 1. **Problem Domain Patterns** — Established approaches, expert recommendations, common pitfalls
 2. **Tools & Libraries** — What's commonly used, open-source options, feature comparison
@@ -350,7 +352,7 @@ Beyond codebase exploration, you have access to tools that can significantly imp
 
 ### Web Search (Tavily-first)
 
-**Primary tool:** `mcp__tavily__tavily_search` for general web search; `mcp__tavily__tavily_extract` when you need full content of a known URL.
+**Primary tool:** `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) for general web search; `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) when you need full content of a known URL.
 
 **Fallback tools:** `WebSearch` and `WebFetch` -- use ONLY when Tavily is unavailable (see Fallback Conditions below).
 
@@ -368,12 +370,13 @@ Use Tavily search when:
 **Examples:**
 
 ```text
-mcp__tavily__tavily_search: "Express.js middleware error handling pattern 2026"
-mcp__tavily__tavily_search: "PostgreSQL JSONB index best practices"
-mcp__tavily__tavily_search: "React Server Components file structure conventions"
-mcp__tavily__tavily_search: "best practices building project health dashboard Python 2026"
-mcp__tavily__tavily_search: "Python stdlib alternatives to pandas for data analysis"
-mcp__tavily__tavily_search: "SVG chart generation without dependencies comparison"
+mcp__litellm__Tavily-tavily_search: "Express.js middleware error handling pattern 2026"
+mcp__litellm__Tavily-tavily_search: "PostgreSQL JSONB index best practices"
+mcp__litellm__Tavily-tavily_search: "React Server Components file structure conventions"
+mcp__litellm__Tavily-tavily_search: "best practices building project health dashboard Python 2026"
+mcp__litellm__Tavily-tavily_search: "Python stdlib alternatives to pandas for data analysis"
+mcp__litellm__Tavily-tavily_search: "SVG chart generation without dependencies comparison"
+# else mcp__tavily__tavily_search with the same query
 ```
 
 **Fallback Conditions -- fall back to WebSearch / WebFetch only when ANY of these are true:**
@@ -414,7 +417,7 @@ Skill: rf:opinion "Is a monorepo or multi-repo structure better for [specific si
 
 ### Escalation: When to Ask for Help
 
-1. **Codebase question you can't answer** -> Use Tavily (`mcp__tavily__tavily_search`); fall back to WebSearch only per the Fallback Conditions above
+1. **Codebase question you can't answer** -> Use Tavily (`mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`)); fall back to WebSearch only per the Fallback Conditions above
 2. **Trade-off that needs objective analysis** → Use /rf:opinion
 3. **Still blocked after web research** → Message `team-lead` with what you tried
 4. **Genuine ambiguity about user intent** → Message `team-lead` (they'll decide whether to ask the user)
@@ -540,7 +543,7 @@ Content preview:
 5. **Use appropriate tools** - Glob for files, Grep for content, Read for details
 6. **Don't guess** - If you can't find it, say so
 7. **Evidence-based claims only** — Every finding must cite actual file paths, line numbers, function names, class names. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation"
-8. **Tavily-first for web** -- All web search and web fetch operations MUST use `mcp__tavily__*` first. `WebSearch` / `WebFetch` are fallbacks bound by the three Fallback Conditions in the "Web Search (Tavily-first)" section. Silently using WebSearch when Tavily is available is a protocol violation.
+8. **Tavily-first for web** -- All web search and web fetch operations MUST use `mcp__litellm__Tavily-*` or `mcp__tavily__*` first. `WebSearch` / `WebFetch` are fallbacks bound by the three Fallback Conditions in the "Web Search (Tavily-first)" section. Silently using WebSearch when Tavily is available is a protocol violation.
 
 ## What NOT To Do
 
diff --git a/src/superclaude/agents/rf-team-lead.md b/src/superclaude/agents/rf-team-lead.md
index 297d90a0..d0961a90 100644
--- a/src/superclaude/agents/rf-team-lead.md
+++ b/src/superclaude/agents/rf-team-lead.md
@@ -10,7 +10,9 @@ tools:
   - Bash
   - Glob
   - Grep
+  - mcp__litellm__Tavily-tavily_search    # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_search    # PRIMARY web search
+  - mcp__litellm__Tavily-tavily_extract   # PRIMARY via the LiteLLM proxy
   - mcp__tavily__tavily_extract   # PRIMARY web content extraction
   - WebSearch                      # FALLBACK only -- Tavily unavailable
   - WebFetch                       # FALLBACK only -- Tavily unavailable
@@ -304,16 +306,16 @@ verification, framework workflow understanding):
 
 **ALWAYS try Tavily MCP first:**
 
-- `mcp__tavily__tavily_search` for queries ("how does X framework handle
+- `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) for queries ("how does X framework handle
   build steps", "current best practices for Y")
-- `mcp__tavily__tavily_extract` when you have a specific URL whose content
+- `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) when you have a specific URL whose content
   you need to read
 
 **Fall back to WebSearch / WebFetch ONLY when Tavily is unavailable.**
 Tavily is considered unavailable if any of the following holds:
 
-1. The `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` tool is
-   not loaded in the current session (tool call returns "tool not found"
+1. Neither the `mcp__litellm__Tavily-tavily_search` / `mcp__litellm__Tavily-tavily_extract` tool nor the `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` tool is
+   loaded in the current session (tool call returns "tool not found"
    or equivalent unknown-tool error).
 2. The Tavily call returns an explicit server error (HTTP 5xx,
    authentication failure, configuration error) on the first attempt AND
@@ -395,7 +397,7 @@ Options:
 8. **Multiple researchers per track** — Spawn 3-8 topic-specific researchers per track. One is never sufficient.
 9. **Research review is mandatory** — Read and evaluate ALL research files before spawning the builder. Never skip this step.
 10. **Scope discovery before research** — Do a lightweight Glob/Grep scan before spawning researchers to give them targeted assignments.
-11. **Tavily-first for web research** -- Always call `mcp__tavily__tavily_search` / `mcp__tavily__tavily_extract` before reaching for WebSearch / WebFetch. WebSearch and WebFetch are fallbacks for when Tavily is unavailable (tool not loaded, server error after one retry, or rate-limited). Note any fallback in the pipeline output.
+11. **Tavily-first for web research** -- Always call `mcp__litellm__Tavily-tavily_search` (else `mcp__tavily__tavily_search`) / `mcp__litellm__Tavily-tavily_extract` (else `mcp__tavily__tavily_extract`) before reaching for WebSearch / WebFetch. WebSearch and WebFetch are fallbacks for when Tavily is unavailable (tool not loaded, server error after one retry, or rate-limited). Note any fallback in the pipeline output.
 
 ## Agent Memory
 
diff --git a/tests/agents/test_tavily_tool_parity.py b/tests/agents/test_tavily_tool_parity.py
index f234d545..4b282dd8 100644
--- a/tests/agents/test_tavily_tool_parity.py
+++ b/tests/agents/test_tavily_tool_parity.py
@@ -24,7 +24,8 @@ _REPO_ROOT = Path(__file__).resolve().parents[2]
 _AGENTS_DIR = _REPO_ROOT / "src" / "superclaude" / "agents"
 _SKILLS_DIR = _REPO_ROOT / "src" / "superclaude" / "skills"
 
-_TAVILY_ID = re.compile(r"mcp__tavily__tavily_[a-z]+")
+_TAVILY_ID = re.compile(r"mcp__(?:tavily__tavily|litellm__Tavily-tavily)_[a-z]+")
+_TOOL_ENTRY = re.compile(r"mcp__[A-Za-z0-9_-]+")
 _TOOL_SURFACE_KEY = re.compile(r"^\s*(tools|allowed-tools):", re.MULTILINE)
 
 
@@ -83,6 +84,44 @@ def test_documenting_files_have_exact_parity():
     assert not mismatches, f"frontmatter↔prose Tavily parity mismatch: {mismatches}"
 
 
+def _declared_tools(fm: str) -> list[str]:
+    """Ordered tool ids from a ``tools:`` / ``allowed-tools:`` value, YAML list or inline list."""
+    tools: list[str] = []
+    in_list = False
+    for line in fm.splitlines():
+        key = _TOOL_SURFACE_KEY.match(line)
+        if key:
+            tools.extend(_TOOL_ENTRY.findall(line[key.end():]))
+            in_list = True
+        elif in_list and line.lstrip().startswith("- "):
+            tools.extend(_TOOL_ENTRY.findall(line.split("#", 1)[0]))
+        else:
+            in_list = False
+    return tools
+
+
+def test_proxy_tavily_listed_before_direct_twin():
+    """Issue #454: each agent's declared direct Tavily tool has its LiteLLM proxy twin just before it."""
+    checked, missing = 0, []
+    for f in sorted(_AGENTS_DIR.rglob("*.md")):
+        fm, _ = _split_frontmatter(f.read_text(encoding="utf-8"))
+        tools = _declared_tools(fm)
+        for i, tool in enumerate(tools):
+            if tool.startswith("mcp__tavily__tavily_"):
+                checked += 1
+                twin = tool.replace("mcp__tavily__", "mcp__litellm__Tavily-", 1)
+                if i == 0 or tools[i - 1] != twin:
+                    missing.append((str(f.relative_to(_REPO_ROOT)), tool))
+    assert checked, "proxy-twin guard found 0 direct Tavily tools (vacuous; M1)"
+    assert not missing, f"direct Tavily tool without its proxy twin right before it: {missing}"
+
+
+def test_declared_tools_parses_list_and_inline_forms():
+    yaml_list = "tools:\n  - Read\n  - mcp__a__x    # note\n  - mcp__b__y\nmodel: x\n- mcp__c__z\n"
+    assert _declared_tools(yaml_list) == ["mcp__a__x", "mcp__b__y"]
+    assert _declared_tools("allowed-tools: Read, mcp__a__x, mcp__b__y\n") == ["mcp__a__x", "mcp__b__y"]
+
+
 def test_rf_no_map_crawl():
     """X5 guard — no rf-* agent references map/crawl (confined to the research engine)."""
     rf_files = sorted(_AGENTS_DIR.glob("rf-*.md"))
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
