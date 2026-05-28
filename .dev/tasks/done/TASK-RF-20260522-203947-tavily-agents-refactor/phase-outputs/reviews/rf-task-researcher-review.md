# Review: rf-task-researcher Tavily Refactor

**Target:** `/config/workspace/IronClaude/src/superclaude/agents/rf-task-researcher.md`
**Proposal:** `.dev/releases/current/TavilyAgents/rf-task-researcher-tavily-refactor.md`
**Phase:** 2, Step 2.3
**Method:** Re-Read of target file (post-edit) + grep for `WebSearch`/`WebFetch`/`Tavily` occurrences.

---

## Acceptance Criteria

### 1. Frontmatter `tools:` includes both Tavily entries AND both `WebFetch`/`WebSearch` are still present

**PASS** — Lines 13-16:

```
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebFetch
  - WebSearch
```

All four entries present.

### 2. Tavily entries appear BEFORE `WebFetch`/`WebSearch`

**PASS** — Lines 13-14 (Tavily) precede lines 15-16 (WebFetch/WebSearch). Precedence-as-documentation preserved.

### 3. Body contains a section titled "Web Search (Tavily-first)" or equivalent

**PASS** — Line 342: `### Web Search (Tavily-first)` — exact title match.

### 4. At least three explicit fallback conditions enumerated

**PASS** — Lines 369-371 enumerate exactly three:

1. Tavily tool not present at runtime (server not loaded / install missing).
2. Tavily call returns tool-level error (retry once, then fall back).
3. Tavily call returns rate-limit / quota signal.

### 5. WEB SEARCH PROVENANCE in research notes schema AND fallback-condition prose

**PASS** — Two occurrences:

- Research Notes schema (line 332): `**WEB SEARCH PROVENANCE**: provider=tavily (default) or provider=WebSearch reason=<...>`
- Fallback-condition prose (line 373): `you MUST log the reason in your research notes under a WEB SEARCH PROVENANCE line: provider=WebSearch reason=<tavily-unavailable|tavily-error|tavily-rate-limit>`

### 6. All existing "Use WebSearch when…" bullets preserved retargeted to Tavily

**PASS** — All 8 original trigger bullets preserved at lines 349-356, under the new heading "Use Tavily search when:" (line 348). Verbatim comparison:

- "The project uses a library, framework, or API..." (preserved)
- "You need current syntax, configuration patterns..." (preserved)
- "The codebase references external services or tools..." (preserved)
- "You need to verify whether a pattern..." (preserved)
- "You're researching how to best accomplish a NEW implementation goal" (preserved)
- "You need to evaluate tools, libraries, or approaches..." (preserved)
- "The goal involves choosing a methodology or architecture pattern" (preserved)
- "You want to find free/open-source solutions..." (preserved)

No research-trigger guidance lost.

### 7. Escalation step 1 names Tavily not WebSearch

**PASS** — Line 400: `1. **Codebase question you can't answer** → Use Tavily (mcp__tavily__tavily-search); fall back to WebSearch only per the Fallback Conditions above`

Tavily is the primary; WebSearch named only as fallback gate.

### 8. New "Tavily-first for web" Critical Rule with "protocol violation" framing

**PASS** — Line 508 (Critical Rule 8): `**Tavily-first for web** — All web search and web fetch operations MUST use mcp__tavily__tavily-* first. WebSearch / WebFetch are fallbacks bound by the three Fallback Conditions in the "Web Search (Tavily-first)" section. Silently using WebSearch when Tavily is available is a protocol violation.`

Contains literal phrase "is a protocol violation". Rule 8 added after existing rule 7; previous rules 1-7 preserved unchanged.

### 9. No `WebSearch:` example queries as primary; WebSearch examples (if any) labeled "fallback"

**PASS** — Primary examples block (lines 358-366) uses `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` exclusively. Two `WebSearch:`/`WebFetch:` examples appear at lines 377-378 under the heading `**Fallback examples (labeled fallback — only when a Fallback Condition above fires):**`, each with inline `# fallback` comment.

### 10. grep `WebSearch` shows it ONLY in fallback contexts

**PASS** — grep verified all post-refactor `WebSearch` occurrences:

- Line 16: frontmatter tools list (allowed; listed below Tavily as fallback per criterion 2)
- Line 320: "fall back to WebSearch only per Web Search (Tavily-first) → Fallback Conditions" (fallback context)
- Line 332: provenance schema — `provider=WebSearch reason=<...>` (fallback log)
- Line 346: "Fallback tools: WebSearch and WebFetch — use ONLY when Tavily is unavailable" (fallback context)
- Line 368: "Fallback Conditions — fall back to WebSearch / WebFetch only when ANY..." (fallback context)
- Line 373: provenance log instructions for fallback events
- Line 377: example labeled `# fallback`
- Line 400: escalation "fall back to WebSearch only per the Fallback Conditions above" (fallback context)
- Line 508: Critical Rule 8 — "WebSearch / WebFetch are fallbacks" (fallback context)

Zero occurrences as recommended primary tool. All occurrences are fallback contexts, frontmatter list, or rule text governing fallback behavior.

---

## Deferred Sync/Verify Criterion

**DEFERRED** — Per task instructions, `.claude/agents/rf-task-researcher.md` was NOT edited in this step. The downstream `make sync-dev` and `make verify-sync` execution belongs to a later phase step. `src/superclaude/` is the source of truth; the `.claude/` mirror will be regenerated by sync.

---

## Anomalies

None. All six discrete-anchor edits applied via single Edit calls; no whitespace drift, no anchor ambiguity encountered. Re-Read confirms file ends at line 527 (previously 506) — net +21 lines, consistent with proposal scope (new examples block, fallback-conditions block, provenance line, new Critical Rule 8, frontmatter +2 lines).

---

**Overall Verdict:** PASS
