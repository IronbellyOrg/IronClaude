# Refactor: rf-task-researcher → Tavily-first

## Current state

**Frontmatter `tools:` (lines 6-25)** lists `WebFetch` (line 13) and `WebSearch` (line 14). **Tavily MCP tools (`mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract`) are NOT in the list.** The agent therefore cannot call Tavily today — it has no path to it even if it wanted one.

**Body workflow references** to web operations are concentrated and prescriptive (not incidental):

- "Solution Research" section (lines 297-332) — explicit decision framework for when to research externally; closes with "use WebSearch to investigate" (line 318).
- "Extended Research Tools → WebSearch — External Documentation & Best Practices" (lines 339-361) — full bullet list of triggers ("Use `WebSearch` when…"), six worked example queries, and a "Do NOT use WebSearch for" guardrail. Web search is positioned as the canonical extra-codebase tool.
- "Escalation: When to Ask for Help" (lines 378-383) — step 1 of the escalation ladder is literally "Use WebSearch for external context".
- "Research Notes Structure" (lines 326-332) — `SOLUTION_RESEARCH` section schema asks for "source URL" per approach evaluated, implying web-sourced citations.

WebFetch is in the tools list but is never named in the body — currently a latent capability with no workflow that invokes it.

**Current pattern**: `WebSearch` first (and only); `WebFetch` available but undocumented; no fallback logic, no Tavily mention anywhere. Net effect: every external research action today flows through Anthropic's first-party WebSearch.

## Proposed refactor

### Frontmatter `tools:` edit (insert two lines, keep existing two as fallback)

```diff
 tools:
   - Read
   - Write
   - Edit
   - Bash
   - Glob
   - Grep
+  - mcp__tavily__tavily-search
+  - mcp__tavily__tavily-extract
   - WebFetch
   - WebSearch
   - NotebookEdit
   ...
```

Order matters as documentation: Tavily entries appear immediately before WebFetch/WebSearch to signal precedence at the tools-list level. Both fallback tools are retained — do not remove them.

### Body edits

**1. Rename and rewrite the "Extended Research Tools → WebSearch" section (lines 339-361)** to "Extended Research Tools → Web Search (Tavily-first)". New canonical block:

> ### Web Search (Tavily-first)
>
> **Primary tool:** `mcp__tavily__tavily-search` for general web search; `mcp__tavily__tavily-extract` when you need full content of a known URL.
>
> **Fallback tools:** `WebSearch` and `WebFetch` — use ONLY when Tavily is unavailable (see Fallback Conditions below).
>
> Use Tavily search when:
> - [keep all existing "Use WebSearch when" bullets, retargeted to Tavily]
>
> **Examples (use Tavily by default):**
> ```
> mcp__tavily__tavily-search: query="Express.js middleware error handling pattern 2026"
> mcp__tavily__tavily-search: query="PostgreSQL JSONB index best practices"
> mcp__tavily__tavily-extract: urls=["https://nodejs.org/api/fs.html"]
> ```
>
> **Fallback Conditions — fall back to WebSearch / WebFetch only when ANY of these are true:**
> 1. The Tavily tool is not present in your available tools at runtime (server not loaded / install missing).
> 2. A Tavily call returns a tool-level error (auth failure, server error, malformed response) — retry once with a simplified query; if the retry also errors, fall back.
> 3. A Tavily call returns an explicit rate-limit / quota signal — fall back for the remainder of this research task.
>
> When you fall back, you MUST log the reason in your research notes under a `WEB SEARCH PROVENANCE` line: `provider=WebSearch reason=<tavily-unavailable|tavily-error|tavily-rate-limit>`. Default research notes assume `provider=tavily` and the line may be omitted.
>
> **Do NOT use any web tool for:** things you can find in the codebase. Always check locally first.

**2. Update "Escalation: When to Ask for Help" (lines 378-383)** — replace step 1:

```diff
-1. **Codebase question you can't answer** → Use WebSearch for external context
+1. **Codebase question you can't answer** → Use Tavily (`mcp__tavily__tavily-search`); fall back to WebSearch only per the Fallback Conditions above
```

**3. Update "Solution Research → What to Research" (line 318)** — replace the prose "use WebSearch to investigate":

```diff
-When external research IS warranted, use WebSearch to investigate:
+When external research IS warranted, use Tavily (`mcp__tavily__tavily-search`) to investigate (fall back to WebSearch only per Web Search (Tavily-first) → Fallback Conditions):
```

**4. Update "Research Notes Structure" (lines 326-332)** — add provenance line:

```diff
 - **APPROACHES EVALUATED**: Each approach with pros, cons, and source URL
+- **WEB SEARCH PROVENANCE**: `provider=tavily` (default) or `provider=WebSearch reason=<...>` if a fallback fired during this research
```

**5. Add a new entry to "Critical Rules" (after current rule 7, lines 487):**

> 8. **Tavily-first for web** — All web search and web fetch operations MUST use `mcp__tavily__tavily-*` first. `WebSearch` / `WebFetch` are fallbacks bound by the three Fallback Conditions in the "Web Search (Tavily-first)" section. Silently using WebSearch when Tavily is available is a protocol violation.

(Renumber existing rule 7 → 7, current rules continue; final list grows by one.)

## Acceptance criteria

A reviewer / task-builder can verify the refactor landed correctly by checking:

- [ ] Frontmatter `tools:` includes `mcp__tavily__tavily-search` AND `mcp__tavily__tavily-extract`, AND both `WebFetch` and `WebSearch` are still present.
- [ ] Tavily entries appear in the list BEFORE `WebFetch` / `WebSearch` (precedence-as-documentation).
- [ ] Body contains a section titled "Web Search (Tavily-first)" (or equivalent) with explicit Tavily-primary / WebSearch-fallback framing.
- [ ] At least three explicit fallback conditions are enumerated (tool-missing, tool-error, rate-limit).
- [ ] The "WEB SEARCH PROVENANCE" requirement appears in the research notes schema AND in the fallback-condition prose.
- [ ] All existing "Use WebSearch when…" bullets are preserved (retargeted to Tavily) — no research-trigger guidance was lost in the rename.
- [ ] The escalation ladder step 1 names Tavily, not WebSearch.
- [ ] A new "Tavily-first for web" rule is added to "Critical Rules" with the phrase "is a protocol violation" or equivalent strong enforcement.
- [ ] No `WebSearch:` example queries remain in the document as the *primary* example — Tavily examples appear first; WebSearch examples (if retained at all) are explicitly labeled "fallback".
- [ ] grep for `WebSearch` in the post-refactor file shows it ONLY in fallback / "fall back to" contexts, never as the recommended primary tool.

## Reflection notes

`/sc:reflect --session --analyze` flagged three gaps in the initial proposal that I tightened:

1. **Original draft did not address WebFetch separately.** WebFetch is in the tools list but never referenced in the body — easy to overlook. Tightened: the new "Web Search (Tavily-first)" block names `mcp__tavily__tavily-extract` as the WebFetch counterpart and the Fallback Conditions cover both Tavily tools, so WebFetch falls back symmetrically with WebSearch rather than being orphaned.

2. **Original draft's fallback condition was vague ("if Tavily fails").** Reflection: "fails" is under-specified — does a slow response count? a partial result? Tightened to three concrete, observable conditions (tool-missing, tool-level error with one retry budget, explicit rate-limit signal) so the agent's decision logic is deterministic and a reviewer can audit it.

3. **Original draft had no audit trail.** If Tavily is the default and WebSearch is the fallback, downstream consumers (builder, QA gates) cannot tell from the research notes which provider was used unless the agent says so. Tightened: added the `WEB SEARCH PROVENANCE` line to the `SOLUTION_RESEARCH` schema, with a sensible default (`provider=tavily` may be omitted) so the line only appears when something noteworthy happened — minimizes noise, preserves auditability.

Reflection also confirmed the refactor preserves the agent's core responsibility (codebase-first exploration, web only when locally impossible). The "Do NOT use any web tool for: things you can find in the codebase" guardrail is retained and strengthened by being lifted out of the WebSearch-specific section into the new tool-agnostic block.
