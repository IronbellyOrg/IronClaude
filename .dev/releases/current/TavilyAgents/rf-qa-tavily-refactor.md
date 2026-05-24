# Refactor: rf-qa → Tavily-first

## Current state

**File:** `/config/workspace/IronClaude/src/superclaude/agents/rf-qa.md`

**Frontmatter `tools:` (lines 6-30)** — web tools currently registered:

```yaml
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch          # line 13 — generic web fetch
  - WebSearch         # line 14 — generic web search
  - NotebookEdit
  - Agent
  - Task
  - ...
```

**Body web-research usage:** rf-qa's verification checklists are overwhelmingly source-grounded (Read, Grep, Glob, Bash). The agent's stated philosophy at line 37 ("Source truth is king") and Principle 6 (`Source truth is king: Verify against actual files, not just agent claims`, line 92) explicitly prioritise local-file verification. The web tools currently in the `tools:` list are **legacy/inherited capacity** — no checklist item under any QA phase (Research Gate, Synthesis Gate, Report Validation, Task Integrity, Fix Cycle) instructs the agent to perform a web search or fetch. The closest the body gets to external lookup is checklist item 5 of Report Validation (line 234: `External Research Findings include source URLs for every finding`), but this is **validating that upstream research files cite URLs**, not performing fresh web research.

**Current "pattern":** WebFetch/WebSearch are declared-but-unused. There is no documented order, no fallback logic, and no detection condition because the agent never invokes them in normal operation.

## Proposed refactor

### Frontmatter edits (lines 6-30)

**Before:**
```yaml
  - WebFetch
  - WebSearch
```

**After:**
```yaml
  - mcp__tavily__tavily-search    # PRIMARY web search (Tavily MCP first)
  - mcp__tavily__tavily-extract   # PRIMARY web fetch (Tavily MCP first)
  - WebFetch                      # FALLBACK only — when Tavily MCP unavailable
  - WebSearch                     # FALLBACK only — when Tavily MCP unavailable
```

Keep relative ordering (Tavily lines BEFORE WebFetch/WebSearch) so the agent inventory visibly encodes precedence.

### Body edits

**Insert a new `## Web Research Tooling (Tavily-first)` section between line 81 ("---" closing the Parallel Partitioning section) and line 84 ("Verification Principles") OR equivalently between line 97 ("---") and line 99 (Research Gate). Suggested location: after Verification Principles (~line 97 fence), as a sibling subsection so it governs every QA phase below it.**

Suggested wording:

> ## Web Research Tooling (Tavily-first)
>
> When any QA verification step legitimately requires fetching external information — e.g., confirming an external API surface cited in a synthesis file, verifying that an external standard (RFC, OWASP entry, library version) said what a research file claims it said — you MUST use Tavily MCP first.
>
> **Precedence:**
> 1. `mcp__tavily__tavily-search` — for queries / discovery.
> 2. `mcp__tavily__tavily-extract` — for fetching a specific URL's content.
> 3. **Fallback only:** `WebSearch` / `WebFetch` — and only when Tavily MCP is unavailable (see detection condition below).
>
> **Detection condition for "Tavily unavailable"** (any of):
> - The `mcp__tavily__tavily-search` or `mcp__tavily__tavily-extract` tool is not present in your runtime tool list this session (server not loaded).
> - The Tavily call returns a structured server error (e.g., 5xx, connection refused, "server not configured").
> - The Tavily call returns a rate-limit / quota error (HTTP 429 or equivalent payload).
>
> If any of these fire on a single call, record the failure mode in your QA report's `Tool engagement:` line (e.g., `tavily_search: 1 attempt, fell back to WebSearch (rate-limit)`), then issue the equivalent WebSearch/WebFetch call. Do NOT fall back silently — the fallback MUST be auditable in the report.
>
> **What this does NOT change:** rf-qa remains source-truth-first (Principle 6). Web research is only ever a supplement when verifying a claim that is intrinsically external (URL-bound, standards-bound, third-party-API-bound). Local Read/Grep/Glob/Bash remain the primary verification surface; the Tavily-first rule governs the residual external-lookup case.

**Add to "Tool Engagement Minimum" (line 448-449) — append:**

> If web research was performed during this QA phase, the tool-engagement line MUST also report `tavily_search: N | tavily_extract: N | web_search_fallback: N | web_fetch_fallback: N` with a one-line reason for any non-zero fallback count.

**Add a new Critical Rule (after rule 11, line 465):**

> 12. **Tavily-first for any external lookup** — When verifying a claim that requires fetching from the open web, you MUST attempt `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` before falling back to `WebSearch` / `WebFetch`. Silent fallback is a process violation; the fallback condition and reason MUST appear in your QA report.

### Fallback decision flow

```
need external lookup?
  └── tavily tool available in this session?
        ├── NO  → record "tavily-not-loaded" in report, use WebSearch/WebFetch
        └── YES → call mcp__tavily__tavily-search (or -extract)
              ├── success → use result
              ├── 5xx / connection error → record reason, fall back to WebSearch/WebFetch
              ├── 429 rate-limit → record reason, fall back to WebSearch/WebFetch
              └── auth/config error → record reason, fall back to WebSearch/WebFetch
```

## Acceptance criteria

- [ ] Frontmatter `tools:` block lists `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` BEFORE `WebFetch` and `WebSearch`.
- [ ] `WebFetch` and `WebSearch` remain in the `tools:` list (not removed — they are the fallback).
- [ ] A new `## Web Research Tooling (Tavily-first)` body section exists, sited so it governs every QA phase (Research Gate, Synthesis Gate, Report Validation, Task Integrity, Fix Cycle).
- [ ] The detection condition for "Tavily unavailable" enumerates: (1) tool not present in runtime tool list, (2) server error / connection refused, (3) rate-limit / quota error.
- [ ] The "Tool Engagement Minimum" section requires reporting `tavily_*` and `*_fallback` counts when any web research was performed.
- [ ] A new Critical Rule (rule 12) codifies the Tavily-first requirement and bans silent fallback.
- [ ] Source-truth primacy (Principle 6) is preserved verbatim — web research remains supplementary, not primary.
- [ ] No existing QA checklist item is weakened or removed.
- [ ] `make verify-sync` passes after editing `src/superclaude/agents/rf-qa.md` and running `make sync-dev`.

## Reflection notes

**Adversarial validation against original intent:**

1. **Does Tavily-first contradict rf-qa's zero-trust philosophy?** No — Tavily-first applies only to the residual cases where external verification is legitimately required. rf-qa's primary verification surface (Read / Grep / Glob / Bash against local source files) is untouched. The refactor narrows external-lookup tool choice; it does not introduce new external-lookup obligations.

2. **Risk of dead-letter web tools.** rf-qa's body does not currently require web research in any phase. After the refactor, both Tavily and WebSearch/WebFetch may remain unused for the lifetime of most QA passes. This is the right outcome — declaring tools that are never invoked is normal in agent definitions (it's capacity, not mandate). The Tavily-first rule fires only when web research IS performed, governing how, not whether.

3. **Audit-trail strengthening.** The mandated `tavily_*` / `*_fallback` reporting in the Tool Engagement line is a genuine improvement to rf-qa's existing audit discipline (Principle 9 "Self-audit"). It catches the failure mode where an agent silently downgrades from MCP-backed search to generic WebSearch without noting why.

4. **Partition-instance compatibility.** Parallel rf-qa partitions (lines 50-77) each get their own tool list; Tavily-first applies per-instance identically. No cross-partition coordination is needed for tool selection.

5. **Gap surfaced by reflection:** the original intent of rf-qa did NOT include external research at all (it's a verifier, not a researcher). One could argue the cleaner refactor is to **remove** WebFetch/WebSearch entirely rather than add Tavily-first. **Decision:** keep the tools because (a) Report Validation item 5 verifies that upstream research files cite source URLs — a verifier may legitimately want to spot-check those URLs resolve, and (b) the constraint from the parent prompt is "Tavily first, fall back to Web*", not "remove web tools". The refactor honours the constraint as given.

6. **No interaction with fix-cycle monotonicity protocol (FR-CONV.5 / PR-02 at lines 337-345).** The Tavily-first rule is purely a tool-selection precedence; it does not alter halt-guard semantics, regression detection, or `|F_n|` accounting.
