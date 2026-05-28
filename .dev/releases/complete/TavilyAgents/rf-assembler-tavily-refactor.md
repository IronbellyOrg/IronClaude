# Refactor: rf-assembler → Tavily-first

## Current state

`src/superclaude/agents/rf-assembler.md` declares both web tools in frontmatter (lines 13-14):

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
  - Agent
  ...
```

However, the agent body does NOT document or use web search/fetch as part of its workflow. The agent's role is strictly defined as consolidating component files into a single structured output:

- "Your job is to consolidate multiple component files... into a single structured output document" (line 35).
- The "Assembly Process" (Steps 1-6, lines 78-137) only references Read, Edit, and Write — no web operations.
- "Critical Rules" (lines 223-233) emphasize fidelity, no fabrication, evidence trace to component files — explicitly the OPPOSITE of pulling external data.
- "Output Quality Standards" (lines 197-202) state: "No fabrication — You are assembling existing content, not creating new content."

**Diagnosis:** `WebFetch` and `WebSearch` are in the tool allowlist but are dead weight. There is no documented invocation path; using them would actually violate the agent's core "no fabrication" rule.

**However**, since the tools are allowlisted, an agent under context pressure could still invoke them. Tavily-first policy should still apply *to the allowlist itself* to ensure consistency across the RF agent fleet, even though the assembler is unlikely to use web research in practice.

## Proposed refactor

There are two viable refactor directions. The reflection step (below) recommends Direction A.

### Direction A (recommended): Replace web tools with Tavily-first allowlist, codify "no web research" rule

This direction acknowledges the assembler's read-only-from-component-files nature while still making the allowlist consistent with the rest of the RF agent fleet and with project policy.

#### Frontmatter `tools:` edit (before → after)

Before (lines 6-30):

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
  - Agent
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
  - Agent
  ...
```

#### Body edits

**Add** a new subsection between "Output Quality Standards" and "Completion Protocol" (after line 203):

```markdown
---

## Web Research — Tavily-first Protocol (rare; usually NOT needed)

Your role is to assemble content from component files on disk. You should
NOT normally need to fetch anything from the web. Web research violates
your "no fabrication" rule unless explicitly authorized by the spawn
prompt or QA fix instruction.

If — and only if — your spawn prompt or an `ASSEMBLY_FIX` message
explicitly directs you to fetch external content (e.g., resolve a
linked URL whose content was already cited by a component file), use
Tavily MCP first:

- `mcp__tavily__tavily-extract` for known URLs in component files.
- `mcp__tavily__tavily-search` only if the spawn prompt directs you to
  look up a specific reference.

Fall back to `WebFetch` / `WebSearch` ONLY when Tavily is unavailable.
Tavily is considered unavailable if:

1. `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` is not
   loaded in the current session (tool not found).
2. The Tavily call returns an explicit server error (5xx / auth /
   configuration) on the first attempt AND a single retry.
3. The Tavily call returns a rate-limit error (429) and the assembly
   cannot wait.

Note any fallback in the assembled document with this marker:

`[WEB_RESEARCH_FALLBACK: tavily=<reason>; used=<WebSearch|WebFetch>;
url=<url>]`

If you find yourself wanting to fetch from the web without authorization,
STOP. Send `BLOCKED: external content needed for [section] but not
authorized by spawn prompt` to the team lead instead.
```

**Add** to the `## Critical Rules` list (after rule 9, lines 232):

```markdown
10. **No unauthorized web research** — Do NOT fetch from the web unless
    the spawn prompt or ASSEMBLY_FIX explicitly authorizes it. If
    authorized, use `mcp__tavily__tavily-search` / `-extract` first;
    fall back to WebSearch / WebFetch only when Tavily is unavailable
    (tool not loaded, server error after one retry, or rate-limited).
    Mark any fallback in the assembled document.
```

### Direction B (rejected by reflection): Remove web tools entirely

A simpler refactor would drop `WebFetch` and `WebSearch` from the frontmatter and not add Tavily tools, on the grounds that this agent has no documented web workflow.

**Reflection rejected this** because:

- The current allowlist already permits WebFetch/WebSearch and removing them is a behavioral change beyond the Tavily-first ask. Removal could break downstream skills that invoke this agent in a hybrid mode (e.g., assembling a report that includes resolving final-citation URLs).
- The Tavily-first ask is fleet-wide consistency. Even agents that rarely use web research should be aligned so that "any time the RF agent fleet hits the web, Tavily is first" is provable from frontmatter alone.

### Fallback detection condition (operational)

Same as the rf-team-lead refactor, with one additional check: before attempting any web call, the assembler MUST verify spawn-prompt authorization. If unauthorized, do not attempt the call at all — send `BLOCKED` to the team lead. The Tavily-first / fallback ladder only applies once authorization is confirmed.

## Acceptance criteria

- [ ] Frontmatter `tools:` list contains both `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract`.
- [ ] Frontmatter `tools:` list still contains `WebSearch` and `WebFetch` as fallbacks.
- [ ] Tavily tool entries appear before WebSearch/WebFetch in the frontmatter ordering.
- [ ] A new body subsection "Web Research — Tavily-first Protocol (rare; usually NOT needed)" exists.
- [ ] That subsection states explicitly that web research requires spawn-prompt authorization.
- [ ] That subsection defines the three Tavily-unavailable conditions (tool-not-loaded / server-error-after-retry / rate-limit).
- [ ] That subsection contains the `[WEB_RESEARCH_FALLBACK: ...]` marker format to be embedded in the assembled document on fallback.
- [ ] A new "Critical Rules" entry codifies Tavily-first AND the no-unauthorized-web-research constraint.
- [ ] The "no fabrication" rule (existing Output Quality Standards) is NOT weakened — the new subsection reinforces it.
- [ ] The assembler's core workflow (Steps 1-6 of Assembly Process, incremental writing protocol, contradiction handling, missing-file handling) is untouched.
- [ ] `make sync-dev` succeeds and `make verify-sync` shows no drift after edits to `src/superclaude/agents/rf-assembler.md`.

## Reflection notes

`/sc:reflect --session --analyze` surfaced the following tightenings:

1. **Original draft updated the frontmatter without acknowledging that the agent has no documented web workflow.** Reflection caught this: simply swapping tools without explaining when (or whether) to use them would invite drift — an assembler that "knows it can call Tavily" might start pulling external citations into assembled documents and silently violate the no-fabrication rule. Tightened: the body subsection explicitly states web research is "rare; usually NOT needed" and requires spawn-prompt authorization.
2. **Considered removing web tools entirely (Direction B above).** Reflection weighed this against fleet-wide consistency and the risk of breaking downstream skills that might legitimately need URL extraction during assembly (e.g., resolving a citation that arrived as a bare URL in a component file). Decided: keep tools allowlisted but gate their use behind authorization and Tavily-first. Direction A wins.
3. **Initial fallback marker was a side-channel message to team lead only.** Reflection: assembled documents are the artifact of record; any web-source fallback that produced content in the document needs to be visible *in the document itself* for audit, not only in a sidechannel team-lead message. Tightened: the `[WEB_RESEARCH_FALLBACK: ...]` marker is embedded directly in the assembled document at the point of use.
4. **Authorization gate added.** Reflection: the original Tavily-first ask was about *which tool to call when calling the web*; reflection added the prior step *whether to call the web at all*. For this agent specifically, the answer defaults to "no" unless the spawn prompt or ASSEMBLY_FIX says otherwise. This preserves the agent's core "no fabrication" identity.
5. **Verified intent preservation.** Assembly Process (Steps 1-6), Incremental Writing Protocol, Handling Issues (missing files / contradictions / empty sections), QA Handoff Protocol, Output Quality Standards, and Completion Protocol are all untouched. The refactor adds rules around web tool usage without changing the assembler's primary job.
6. **Verified fallback unambiguity.** Three conditions for "Tavily unavailable" are the same as rf-team-lead and rf-analyst proposals — fleet consistency. The authorization gate is unique to this agent and is justified by its no-fabrication mandate.
