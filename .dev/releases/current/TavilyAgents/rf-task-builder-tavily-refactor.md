# Refactor: rf-task-builder → Tavily-first

## Current state

**Frontmatter `tools:` (lines 6-25)** lists `WebFetch` (line 13) and `WebSearch` (line 14). **Tavily MCP tools are NOT in the list** — the builder has no path to Tavily today.

**Body workflow references** to web operations are narrower than in `rf-task-researcher` but still load-bearing:

- "Extended Tools → WebSearch — External References for Task Building" (lines 425-439) — full prescriptive block with "Use `WebSearch` when…" bullets, three worked example queries, and a "Do NOT use WebSearch for" guardrail. This is the canonical web-search-from-builder entry point.

WebFetch is in the tools list but is never referenced anywhere in the body — latent capability with no workflow.

There is no fallback logic, no Tavily mention, and no provenance/audit-trail requirement for web-sourced facts that end up in task checklist items. **This is operationally important** because builder uses web findings to write checklist-item Context fields and verification criteria — if a wrong fact leaks in from a web search, it propagates into every executor item built off it.

**Current pattern**: `WebSearch` first (and only when builder steps outside researcher findings); `WebFetch` available but undocumented; no fallback, no Tavily, no provenance tag in generated task files.

## Proposed refactor

### Frontmatter `tools:` edit

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

Same precedence-as-documentation ordering as the researcher refactor: Tavily entries immediately before WebFetch/WebSearch.

### Body edits

**1. Rewrite "Extended Tools → WebSearch" section (lines 423-439)** to "Extended Tools → Web Search (Tavily-first)". New canonical block:

> ### Web Search (Tavily-first)
>
> **Primary tool:** `mcp__tavily__tavily-search` for verifying library/framework syntax and patterns referenced in checklist items; `mcp__tavily__tavily-extract` when you need the full content of a specific docs URL (e.g., to copy an API signature verbatim into a Context field).
>
> **Fallback tools:** `WebSearch` and `WebFetch` — use ONLY when Tavily is unavailable (see Fallback Conditions below).
>
> Use Tavily search when:
> - Building task items for a technology, framework, or library you're not deeply familiar with
> - You need correct syntax, API patterns, or configuration formats to write accurate checklist items
> - The research notes reference external tools or services and you need more detail to write specific verification criteria
>
> **Examples (use Tavily by default):**
> ```
> mcp__tavily__tavily-search: query="Jest test file naming conventions and structure"
> mcp__tavily__tavily-search: query="Dockerfile multi-stage build syntax"
> mcp__tavily__tavily-extract: urls=["https://docs.sqlalchemy.org/en/20/core/migrations.html"]
> ```
>
> **Fallback Conditions — fall back to WebSearch / WebFetch only when ANY of these are true:**
> 1. The Tavily tool is not present in your available tools at runtime (server not loaded).
> 2. A Tavily call returns a tool-level error (auth failure, server error, malformed response) — retry once with a simplified query; if the retry also errors, fall back.
> 3. A Tavily call returns an explicit rate-limit / quota signal — fall back for the remainder of this build.
>
> When you fall back, annotate the affected checklist item's Context field with an HTML comment: `<!-- web-provenance: provider=WebSearch reason=<tavily-unavailable|tavily-error|tavily-rate-limit> -->`. This preserves the executor's ability to audit which facts came from a fallback path.
>
> **Do NOT use any web tool for:** things already covered in the researcher's findings or the codebase. Check research notes first.

**2. Add a new Critical Rule (after current rule 12, before rule 13 — fits naturally between MALFORMED-output rules and the Execution Context emission rule):**

> 13. **Tavily-first for web fact-checking** — When the builder consults the web to verify library/framework syntax or patterns for checklist-item Context fields, the call MUST go through `mcp__tavily__tavily-search` or `mcp__tavily__tavily-extract` first. `WebSearch` / `WebFetch` are fallbacks bound by the three Fallback Conditions in the "Web Search (Tavily-first)" section. When a fallback fires, the affected checklist item MUST carry the `<!-- web-provenance: provider=WebSearch reason=<...> -->` annotation in its Context field. Web-sourced facts in checklist items without provenance annotation MUST be assumed to have been Tavily-sourced; silently using WebSearch when Tavily is available is a protocol violation and a downstream rf-qa risk because the verdict's evidence trail becomes ambiguous.

(Renumber existing rule 13 → 14.)

**3. Update Granularity Requirements (lines 254-268) — no edit required.** Web-sourced facts already feed into items via Step 4 (Synthesize Requirements); the provenance annotation in rule 13 attaches at item-emission time, not at synthesis time.

**4. No edit to QA / VALIDATION / TESTING encoding sections.** Web search is orthogonal to these; the new rule does not interact with QA gate fix-cycle limits or MALFORMED retry counters.

## Acceptance criteria

- [ ] Frontmatter `tools:` includes `mcp__tavily__tavily-search` AND `mcp__tavily__tavily-extract`, AND both `WebFetch` and `WebSearch` are still present.
- [ ] Tavily entries precede `WebFetch` / `WebSearch` in the list.
- [ ] Body contains a section titled "Web Search (Tavily-first)" (or equivalent) replacing the old "WebSearch — External References for Task Building" section.
- [ ] All three original "Use `WebSearch` when…" triggers are preserved (retargeted to Tavily) — no builder-side research-trigger guidance was lost.
- [ ] At least three explicit Fallback Conditions are enumerated (tool-missing, tool-error, rate-limit).
- [ ] A new "Tavily-first for web fact-checking" rule appears in "Critical Rules" with the phrase "protocol violation" or equivalent strong enforcement.
- [ ] The provenance annotation contract (`<!-- web-provenance: provider=WebSearch reason=<...> -->`) is named in BOTH the body section AND the new Critical Rule (single contract, two enforcement venues).
- [ ] grep for `WebSearch` in the post-refactor file shows it ONLY in fallback / "fall back to" / "WebSearch fallback" contexts.
- [ ] No example query is presented with `WebSearch:` as the primary form; WebSearch examples (if retained) are explicitly labeled "fallback".
- [ ] The "Do NOT use any web tool for…" guardrail is preserved.

## Reflection notes

`/sc:reflect --session --analyze` flagged three issues that I tightened:

1. **Original draft proposed a *generic* WEB SEARCH PROVENANCE line at task-file top-level**, mirroring the researcher refactor. Reflection: builder doesn't produce a research-notes document — builder produces a task file made of checklist items. A top-level provenance line on a task file would be invisible to F1 executor, which reads items one-by-one. Tightened: provenance annotation attaches **per checklist item** as an HTML comment in the item's Context field, so it travels with the fact into executor's reading scope, and rf-qa can see it during gate verification.

2. **Original draft did not specify what happens if researcher already supplied web-sourced findings.** Reflection: builder's primary input is researcher findings, which (post-researcher-refactor) carry a `WEB SEARCH PROVENANCE: provider=tavily|WebSearch …` line. Builder should propagate this into the item annotation. Decided NOT to add this as a separate rule — the existing "evidence-based items" rule (Critical Rule 9: "Every task item must reference specific file paths from the research. No assumed or fabricated paths") already binds builder to research-sourced facts; adding "and carry provenance through" would be a natural extension but is out of scope for the Tavily-first refactor specifically. Flagged as a follow-up: once both refactors land, consider tightening Rule 9 to "…and carry web-source provenance through to item Context fields."

3. **Original draft positioned the new Critical Rule with vague phrasing ("prefer Tavily").** Reflection: builder's Critical Rules use absolute language (NEVER, ALWAYS, MUST) — a soft "prefer" rule is inconsistent and easy to ignore under context pressure. Tightened to "MUST go through Tavily first" + "silently using WebSearch when Tavily is available is a protocol violation" to match the existing rule register (e.g., rule 1's "NEVER one-shot" framing).

Reflection confirmed the refactor preserves builder's existing responsibilities — template-first, granularity, incremental writing, QA-gate encoding, Execution Context header emission — and only narrows the web-tool decision space. No interaction with MALFORMED retry counters, fix-cycle limits, or hidden-input determinism rules.
