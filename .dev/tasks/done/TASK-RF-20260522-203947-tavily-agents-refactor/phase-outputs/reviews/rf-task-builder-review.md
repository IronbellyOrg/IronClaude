# rf-task-builder Refactor — Acceptance Review

**Target:** `/config/workspace/IronClaude/src/superclaude/agents/rf-task-builder.md`
**Proposal:** `.dev/releases/current/TavilyAgents/rf-task-builder-tavily-refactor.md`
**Method:** Re-Read post-edit at lines 1-30 (frontmatter), 420-480 (Extended Tools section), 520-541 (Critical Rules), plus `grep -n WebSearch` over the full file.

---

## Acceptance Criteria Checklist

1. **PASS** — Frontmatter `tools:` includes both `mcp__tavily__tavily-search` (line 13) AND `mcp__tavily__tavily-extract` (line 14); `WebFetch` (line 15) and `WebSearch` (line 16) both still present.

2. **PASS** — Tavily entries (lines 13-14) precede `WebFetch` / `WebSearch` (lines 15-16). Ordering matches proposal's precedence-as-documentation rule.

3. **PASS** — Body contains the section "### Web Search (Tavily-first)" at line 427, replacing the old "### WebSearch — External References for Task Building" header. Old section title is gone (verified via grep: no occurrences of "WebSearch — External References" remain).

4. **PASS** — All three original "Use `WebSearch` when…" triggers preserved and retargeted to Tavily at lines 434-436:
   - "Building task items for a technology, framework, or library you're not deeply familiar with"
   - "You need correct syntax, API patterns, or configuration formats to write accurate checklist items"
   - "The research notes reference external tools or services and you need more detail to write specific verification criteria"
   Heading is now "Use Tavily search when:" (line 433).

5. **PASS** — Three explicit Fallback Conditions enumerated at lines 446-448:
   1. Tavily not present at runtime (server not loaded)
   2. Tavily tool-level error (auth failure, server error, malformed response) — with single retry
   3. Tavily rate-limit / quota signal

6. **PASS** — New "Tavily-first for web fact-checking" rule appears as Critical Rule 13 at line 539. Contains the phrase "protocol violation" verbatim: "silently using WebSearch when Tavily is available is a protocol violation". Original rule 13 (Execution Context header emission) successfully renumbered to rule 14 at line 540.

7. **PASS** — The provenance contract `<!-- web-provenance: provider=WebSearch reason=<...> -->` named in BOTH venues:
   - Body section (line 450): `<!-- web-provenance: provider=WebSearch reason=<tavily-unavailable|tavily-error|tavily-rate-limit> -->`
   - Critical Rule 13 (line 539): `<!-- web-provenance: provider=WebSearch reason=<...> -->`
   Single contract, two enforcement venues.

8. **PASS** — `grep -n WebSearch` returns occurrences only in fallback contexts:
   - Line 16: frontmatter `tools:` list (fallback tool registration)
   - Line 431: "Fallback tools: `WebSearch` and `WebFetch` — use ONLY when Tavily is unavailable"
   - Line 445: "Fallback Conditions — fall back to WebSearch / WebFetch only when…"
   - Line 450: provenance annotation referencing `provider=WebSearch` (fallback audit trail)
   - Line 539: Critical Rule 13 — explicitly frames WebSearch/WebFetch as fallbacks
   No primary-use mentions remain.

9. **PASS** — No example query is presented with `WebSearch:` as the primary form. The three "Examples (use Tavily by default)" at lines 440-442 all use `mcp__tavily__tavily-search:` or `mcp__tavily__tavily-extract:` syntax. The three original example topics (Jest test file naming, Dockerfile multi-stage, SQLAlchemy migrations) are retained but rewritten with Tavily call signatures.

10. **PASS** — "Do NOT use any web tool for" guardrail preserved at line 452: "**Do NOT use any web tool for:** things already covered in the researcher's findings or the codebase. Check research notes first." (Generalized from "WebSearch" to "any web tool" to cover the broadened toolset, but the constraint is preserved and arguably strengthened.)

---

**Overall Verdict:** PASS
