# Refactor: rf-team-lead → Tavily-first

## Current state

`src/superclaude/agents/rf-team-lead.md` declares both web tools in frontmatter (lines 13-14):

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
  ...
```

The body explicitly documents `WebSearch` as an active capability under "Extended Tools" (lines 292-297):

> ### WebSearch — Understanding Unfamiliar Technologies
>
> Use `WebSearch` when:
> - The request involves technologies you need to understand to make good orchestration decisions
> - You need to validate whether the researcher's recommendations align with current best practices
> - Template selection depends on understanding a technology's workflow (e.g., does this framework require a build step?)

There is no documented `WebFetch` workflow in the body even though it is allowlisted. No Tavily tools are declared. No fallback policy is encoded — the agent has free choice between WebSearch/WebFetch with no priority order.

**Implication:** When the team lead needs to validate a researcher's recommendations or understand an unfamiliar framework, it will reach for `WebSearch` directly. This bypasses Tavily MCP entirely even though Tavily provides higher-quality, source-attributed search results aligned with project policy (CLAUDE.md "MCP Servers" table).

## Proposed refactor

### Frontmatter `tools:` edit (before → after)

Before (lines 6-29):

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
  - mcp__tavily__tavily-search    # PRIMARY web search
  - mcp__tavily__tavily-extract   # PRIMARY web content extraction
  - WebSearch                      # FALLBACK only — Tavily unavailable
  - WebFetch                       # FALLBACK only — Tavily unavailable
  - NotebookEdit
  - Task
  ...
```

Ordering matters: Tavily tools listed first to reinforce primacy. WebSearch/WebFetch remain in the allowlist as documented fallbacks.

### Body edits

**Replace** the "WebSearch — Understanding Unfamiliar Technologies" subsection (lines 292-297) with:

```markdown
### Web Research — Tavily-first Protocol

When you need external information (technology validation, best-practice
verification, framework workflow understanding):

**ALWAYS try Tavily MCP first:**

- `mcp__tavily__tavily-search` for queries ("how does X framework handle
  build steps", "current best practices for Y")
- `mcp__tavily__tavily-extract` when you have a specific URL whose content
  you need to read

**Fall back to WebSearch / WebFetch ONLY when Tavily is unavailable.**
Tavily is considered unavailable if any of the following holds:

1. The `mcp__tavily__tavily-search` / `mcp__tavily__tavily-extract` tool is
   not loaded in the current session (tool call returns "tool not found"
   or equivalent unknown-tool error).
2. The Tavily call returns an explicit server error (HTTP 5xx,
   authentication failure, configuration error) on the first attempt AND
   a single retry.
3. The Tavily call returns a rate-limit error (HTTP 429 or equivalent)
   and the budget for the current task does not allow waiting.

If any of (1)-(3) holds, fall back to `WebSearch` first, then `WebFetch`
for specific URLs, and note in your pipeline output:
`Tavily unavailable (<reason>); fell back to WebSearch/WebFetch.`

Do NOT use WebSearch or WebFetch as a first choice for any reason
(speed, familiarity, habit). Tavily-first is policy, not preference.

Use web research when:

- The request involves technologies you need to understand to make good
  orchestration decisions.
- You need to validate whether the researcher's recommendations align with
  current best practices.
- Template selection depends on understanding a technology's workflow
  (e.g., does this framework require a build step?).
```

**Add** to the `## Critical Rules` list (currently rules 1-10, lines 343-353):

```markdown
11. **Tavily-first for web research** — Always call `mcp__tavily__tavily-search`
    / `mcp__tavily__tavily-extract` before reaching for WebSearch / WebFetch.
    WebSearch and WebFetch are fallbacks for when Tavily is unavailable
    (tool not loaded, server error after one retry, or rate-limited).
    Note any fallback in the pipeline output.
```

### Fallback detection condition (operational)

The agent decides Tavily is unavailable using this decision tree:

1. Attempt `mcp__tavily__tavily-search` (or `-extract`) with the query.
2. If the tool call errors with "unknown tool" / "tool not available" → Tavily unavailable → use WebSearch/WebFetch.
3. If the tool call errors with a 5xx / auth / config error → retry once with the same arguments. If the retry also fails → Tavily unavailable → use WebSearch/WebFetch.
4. If the tool call errors with a 429 / rate-limit → check whether the current task can afford to wait (default: no). If no → Tavily unavailable for this query → use WebSearch/WebFetch. Record the rate-limit event.
5. If the tool succeeds, use the result. Do not call WebSearch/WebFetch for the same query.

In every fallback case, the agent must include a single line in the pipeline output (or relayed status message) of the form:
`web_research_fallback: tavily=<reason>; used=<WebSearch|WebFetch>`.

## Acceptance criteria

A reviewer / task-builder can verify the refactor with this checklist:

- [ ] Frontmatter `tools:` list contains both `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract`.
- [ ] Frontmatter `tools:` list still contains `WebSearch` and `WebFetch` (as documented fallbacks; not removed).
- [ ] Tavily tool entries appear ordered before WebSearch/WebFetch in the frontmatter list (visual reinforcement of primacy).
- [ ] The "WebSearch — Understanding Unfamiliar Technologies" subsection no longer exists.
- [ ] A new subsection titled "Web Research — Tavily-first Protocol" (or equivalent) exists under "Extended Tools".
- [ ] The new subsection explicitly names `mcp__tavily__tavily-search` and `mcp__tavily__tavily-extract` as PRIMARY.
- [ ] The new subsection explicitly defines the three Tavily-unavailable conditions (tool not loaded; server/auth error after one retry; rate-limit).
- [ ] The new subsection contains the literal phrase "Do NOT use WebSearch or WebFetch as a first choice" (or stricter equivalent).
- [ ] A new rule is added to `## Critical Rules` covering Tavily-first; the rule is numbered after the existing rules (does not displace rule 1's emphasis on three-teammate spawning).
- [ ] The fallback observability requirement is present (the `web_research_fallback: ...` line in pipeline output).
- [ ] No existing responsibilities (team spawning, template selection, parallel tracks, AskUserQuestion, /rf:opinion, Phase 1-7 workflow) are removed or weakened by the edit.
- [ ] `make sync-dev` succeeds and `make verify-sync` shows no drift after edits to `src/superclaude/agents/rf-team-lead.md`.

## Reflection notes

`/sc:reflect --session --analyze` against the original agent's intent surfaced the following tightenings (applied above):

1. **Initial draft only updated the "WebSearch" subsection.** Reflection flagged that the frontmatter ordering of tools sends an implicit signal — leaving WebSearch/WebFetch listed before the new Tavily tools would partially undercut the body change. Tightened: Tavily tools listed first in the proposed frontmatter, and the acceptance criteria check the ordering explicitly.
2. **Fallback condition was originally vague ("if Tavily fails").** Reflection: this leaves the agent room to claim Tavily "felt slow" and skip to WebSearch. Tightened into a three-condition decision tree (unknown-tool error / server error after retry / rate-limit) so the fallback is observable and auditable.
3. **No observability hook in the first draft.** Reflection: without a logged fallback marker, pipelines that silently fall back to WebSearch look identical to compliant runs, defeating the policy. Added the `web_research_fallback: ...` output requirement and an acceptance-criterion bullet.
4. **Original "Critical Rules" list was untouched.** Reflection: this agent reads its critical rules at every spawn; a rule added there has higher behavioral weight than prose under "Extended Tools" alone. Added rule 11.
5. **Verified intent preservation.** The team lead's core responsibilities — scope discovery, parallel tracks, research review protocol, template selection (01 vs 02), error handling, project mode — are untouched. The refactor only replaces the existing WebSearch guidance and supplements the critical rules. No phase (1-7) loses capability.
6. **Verified the fallback path remains usable.** Reflection considered the case where Tavily is reliably unavailable (e.g., no API key configured in a dev environment). The three-condition tree resolves to "use WebSearch/WebFetch" on the first attempt, so the agent is not bricked — it just logs the reason.
