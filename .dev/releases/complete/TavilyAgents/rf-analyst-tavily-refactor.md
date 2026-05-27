# Refactor: rf-analyst → Tavily-first

## Current state

`src/superclaude/agents/rf-analyst.md` declares both web tools in frontmatter (lines 13-14):

```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - NotebookEdit
  - Task
  ...
```

However, the agent body does NOT document any web search or fetch workflow:

- The agent's purpose is "data extraction, cross-validation, and synthesis across research and output files" (line 3 description; line 30 body).
- Five analysis types are defined — completeness-verification, cross-validation, synthesis-review, gap-analysis, coverage-audit — and all five operate exclusively over files on disk in `${TASK_DIR}research/` or `${TASK_DIR}synthesis/`.
- "Quality Standards" (lines 333-340) include: "Do not invent data — if you can't verify something, mark it as unverified" and "Fix nothing yourself — report issues for the appropriate agent to fix. You are read-only on research/synthesis files."
- "Critical Rules" (lines 357-366) include rule 7: "Zero tolerance for fabrication — if a research file contains invented claims, flag the entire file."
- Cross-Validation analysis (lines 206-231) explicitly compares claims against "actual code" — not against external/web sources.

**Diagnosis:** Like rf-assembler, `WebFetch` and `WebSearch` are in the allowlist but are dead weight relative to the agent's documented analysis types. Using them would risk introducing unverified external claims into reports that are supposed to flag exactly that kind of fabrication.

**However**, fleet-wide Tavily-first policy still applies: if the analyst ever does call the web (e.g., a future analysis type, or a `[CODE-VERIFIED]` cross-check that requires resolving an external reference), Tavily must be the primary path. The allowlist is the right place to encode this.

## Proposed refactor

### Frontmatter `tools:` edit (before → after)

Before (lines 6-25):

```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - NotebookEdit
  - Task
  ...
```

After:

```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - mcp__tavily__tavily-search    # PRIMARY web search (rare use; see body)
  - mcp__tavily__tavily-extract   # PRIMARY web content extraction (rare use)
  - WebSearch                      # FALLBACK only — Tavily unavailable
  - WebFetch                       # FALLBACK only — Tavily unavailable
  - NotebookEdit
  - Task
  ...
```

### Body edits

**Add** a new subsection between "Quality Standards" (ends line 340) and "Completion Protocol" (line 342):

```markdown
---

## Web Research — Tavily-first Protocol (rare; usually NOT needed)

Your analysis types (completeness verification, cross-validation,
synthesis review, gap analysis, coverage audit) operate over files on
disk. You should NOT normally need to fetch anything from the web.
Introducing unverified external claims directly contradicts your
zero-tolerance-for-fabrication rule.

If — and only if — your spawn prompt explicitly directs you to validate
a doc-sourced claim against an external reference (URL cited in a
research file, official documentation URL referenced in a verification
tag), use Tavily MCP first:

- `mcp__tavily__tavily-extract` for known URLs cited in research files
  when you must verify a claim's source.
- `mcp__tavily__tavily-search` only when the spawn prompt directs you to
  look up a specific external reference.

**Fall back to `WebFetch` / `WebSearch` ONLY when Tavily is unavailable.**
Tavily is considered unavailable if any of:

1. `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` is not
   loaded in the current session (tool not found).
2. The Tavily call returns an explicit server error (5xx / auth /
   configuration) on the first attempt AND a single retry.
3. The Tavily call returns a rate-limit error (429) and the analysis
   cannot wait.

When falling back, record this directly in your analysis report under
the Quality Standards / Methodology section using this marker:

`[WEB_RESEARCH_FALLBACK: tavily=<reason>; used=<WebSearch|WebFetch>;
url=<url>; claim=<claim being verified>]`

If you find yourself wanting to fetch from the web without explicit
direction from the spawn prompt, STOP. Mark the relevant claim as
`[UNVERIFIED]` in your report (consistent with your existing
cross-validation tagging) and continue. Do NOT introduce external
content unilaterally — that is fabrication-by-import and violates
Critical Rule 7.
```

**Add** to the `## Critical Rules` list (after rule 8, lines 366):

```markdown
9. **No unauthorized web research** — Do NOT fetch from the web unless
   the spawn prompt explicitly directs you to verify a referenced URL or
   external claim. If authorized, use `mcp__tavily__tavily-search` /
   `-extract` first; fall back to WebSearch / WebFetch only when Tavily
   is unavailable (tool not loaded, server error after one retry, or
   rate-limited). Mark any fallback in the analysis report. Treat
   unauthorized external content as fabrication-by-import (Rule 7).
```

### Fallback detection condition (operational)

The analyst decides Tavily is unavailable using the same three-condition tree as the rf-team-lead and rf-assembler proposals, with one analyst-specific addition:

1. Before any web call, verify the spawn prompt authorizes external verification of a specific claim/URL. If not authorized, mark the claim `[UNVERIFIED]` and do NOT call the web at all.
2. If authorized, attempt `mcp__tavily__tavily-extract` (or `-search`) with the URL/query.
3. Unknown-tool error → Tavily unavailable → fall back to WebFetch/WebSearch.
4. 5xx / auth / config error → retry once. If retry also fails → Tavily unavailable → fall back.
5. 429 rate-limit → mark Tavily unavailable for this query → fall back. (Analyst reports already note timing — record the rate-limit event in the report.)
6. Success → use the Tavily result. Tag the claim `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` per the existing Cross-Validation analysis convention. Note in the report that verification used Tavily (no fallback marker needed for the success case).

## Acceptance criteria

- [ ] Frontmatter `tools:` list contains both `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract`.
- [ ] Frontmatter `tools:` list still contains `WebSearch` and `WebFetch` as fallbacks.
- [ ] Tavily tool entries appear before WebSearch/WebFetch in the frontmatter ordering.
- [ ] A new body subsection "Web Research — Tavily-first Protocol (rare; usually NOT needed)" exists, placed between "Quality Standards" and "Completion Protocol".
- [ ] That subsection explicitly says web research requires spawn-prompt authorization, and that unauthorized external content is "fabrication-by-import".
- [ ] That subsection defines the three Tavily-unavailable conditions (tool-not-loaded / server-error-after-retry / rate-limit).
- [ ] That subsection contains the `[WEB_RESEARCH_FALLBACK: ...]` marker format for use in analysis reports.
- [ ] The new Critical Rules entry (rule 9, since current list is 1-8) codifies Tavily-first AND links it back to existing Rule 7 (zero tolerance for fabrication).
- [ ] The existing five analysis types (completeness-verification, cross-validation, synthesis-review, gap-analysis, coverage-audit), the Synthetic-DNSP Finding behavior, the Parallel Partitioning behavior, the General Process, and all existing Quality Standards / Critical Rules are untouched.
- [ ] Cross-Validation analysis's existing `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tagging is preserved unchanged (the refactor reuses it for the un-authorized case).
- [ ] `make sync-dev` succeeds and `make verify-sync` shows no drift after edits to `src/superclaude/agents/rf-analyst.md`.

## Reflection notes

`/sc:reflect --session --analyze` surfaced the following tightenings:

1. **First draft did not connect the new rule to existing Rule 7 (zero tolerance for fabrication).** Reflection: the analyst's core identity is finding fabrication, not introducing it. Calling the web without spawn-prompt authorization is itself a form of fabrication — the analyst would be importing claims that aren't traceable to the research/synthesis files it was asked to audit. Tightened: the new Critical Rule explicitly names this as "fabrication-by-import" and links to Rule 7.
2. **First draft introduced a new tagging system for fallback events.** Reflection: the analyst already has `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` from the Cross-Validation analysis type. Reusing those (with `[UNVERIFIED]` for unauthorized calls) is cleaner than inventing parallel tags. Tightened: the proposal explicitly reuses the existing tagging and adds only the `[WEB_RESEARCH_FALLBACK: ...]` marker for the *Tavily-failed-but-fallback-succeeded* case, which is genuinely new.
3. **Partition-instance implications considered.** Reflection: this agent supports parallel partitioning (multiple analyst instances each handling a subset of files). A web-research fallback by one partition must be visible in the merged report. Resolved: the `[WEB_RESEARCH_FALLBACK: ...]` marker is embedded in each partition's report under Methodology, and the orchestrator's existing merge logic (union of findings) carries it through.
4. **Synthetic-DNSP unaffected.** Reflection: the existing PR-03 synthetic-finding behavior (lines 70-86) is about partition agent failures, not web-research failures. The refactor does not touch it. Confirmed in acceptance criteria: "Synthetic-DNSP Finding behavior ... untouched".
5. **Verified intent preservation.** All five analysis types, the Synthetic-DNSP behavior, Parallel Partitioning, the read-only-on-research/synthesis-files rule, the Quality Standards, the Completion Protocol, and Critical Rules 1-8 are untouched. The refactor adds one Critical Rule and one body subsection.
6. **Verified fallback path is unambiguous.** Three conditions for "Tavily unavailable" are identical to the rf-team-lead and rf-assembler proposals — fleet consistency. The authorization-gate prefix is shared with rf-assembler but justified independently here by Rule 7.
