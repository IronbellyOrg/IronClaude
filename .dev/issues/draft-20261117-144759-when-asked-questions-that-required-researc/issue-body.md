<!-- /sc:issue bug template (simple). -->

## Bug Summary

When a question requires documentation or online research, sessions default to WebFetch/WebSearch or manual searching instead of using the installed Context7 MCP (documentation) and Tavily MCP (web research) by default. The routing guidance exists but is advisory and is not followed at decision time, including when work is delegated to an agent whose tool list excludes the MCP servers.

Observed incident (this conversation, 2026-11-17): the user asked how to hide thinking/tool-call details in Claude Code. The orchestrator delegated the lookup to the `claude-code-guide` agent (tools: Glob, Grep, Read, WebFetch, WebSearch — no Context7/Tavily) instead of calling the available Context7/Tavily tools directly; the lookup was interrupted and the original question remains unanswered. This incident is a single observation; the broader claim that this happens "by default" is not verified beyond it.

## Environment (OS, version)

- OS: Linux 6.8.0-147-generic (dev container)
- Version: SuperClaude/IronClaude 5.0.0, branch docs/409-orca-dashboard-designs (commit 495eb96d1 at session start)

## Current Behavior

- Research-needing questions are answered via WebFetch/WebSearch or manual search rather than Context7/Tavily, even when both MCP servers are installed and available in the session.
- In the observed incident, delegation went to an agent that structurally cannot use Context7/Tavily (its tool allowlist is Glob/Grep/Read/WebFetch/WebSearch), and the orchestrator did not call the MCP tools itself before or instead of delegating.
- The MCP table in the framework context marks the Context7/Tavily routing hints as "advisory" (`src/superclaude/core/CLAUDE.md:22-26`), so nothing binds an agent or delegation decision to them.

## Expected Behavior

- Questions needing library/framework documentation default to Context7; questions needing current online information default to Tavily search (with `tavily_extract` to confirm a likely answer before searching more).
- WebFetch/WebSearch and local code search remain valid fallbacks when the MCP server is unavailable, rate-limited, or the question is out of the servers' scope — not a blanket ban on either.
- Delegation for research questions either targets an agent whose tools include the research MCP servers, or the orchestrator performs the MCP lookup itself.

## Steps to Reproduce

1. In a session with Context7 and Tavily MCP installed, ask a question that requires documentation or current online information (e.g. "how do I hide thinking/tool details in Claude Code?").
2. Observe the session (or a delegated subagent) reach for WebFetch/WebSearch or manual searching rather than Context7/Tavily.

## Impact Assessment (Severity, Blast Radius)

- Severity: medium — answers are slower, less current and less authoritative than the installed tooling provides, and a research delegation can end with the question unanswered; no data loss or correctness break in code.
- Blast Radius: every interactive session and every delegated research/lookup task in projects using the installed framework guidance.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

Quick pass (`--depth quick`), Glob/Grep/Read only (codegraph not used in this subagent run; degraded: none needed for a docs-only area).

- `src/superclaude/core/CLAUDE.md:18-26` — MCP server table names context7 ("Official library/framework docs") and tavily ("Web search, current information") but the Flag column and the note at line 26 explicitly call the routing hints "advisory … hints Claude may honour", with no default-first rule for research questions.
- `src/superclaude/core/CLAUDE.md:32-43` — the ten Core Rules contain no rule about research-tool routing; rule 8 ("Auggie first") covers pre-edit context only.
- `src/superclaude/mcp/MCP_Context7.md:13-19` — "Choose When: Over WebSearch: when you need curated, version-specific documentation", i.e. the preference exists but only as a per-call chooser doc, not a default.
- `src/superclaude/mcp/MCP_Tavily.md:19-25` — "Choose When: Over WebSearch … Over WebFetch: when you need multi-source search"; `MCP_Tavily.md:325-331` lists "Use native WebSearch" as a fallback strategy, matching the desired fallback-not-ban shape.
- `src/superclaude/core/RULES.md:194-201` — Tool Optimization says "MCP > Native > Basic" and "context7 for docs", but only as generic best-tool-selection guidance; no research-question default.
- `src/superclaude/commands/explain.md:6,36,43` — `/sc:explain` declares `mcp-servers: [context7, codegraph]`, showing the intended pattern for docs questions; there is no equivalent guarantee for ad-hoc questions or delegation.
- No agent named `claude-code-guide` exists in `src/superclaude/agents/` (Grep over the repo: no matches); the agent used in the incident is a Claude Code built-in, outside this repo's control — the fixable gap on this side is the orchestrator's routing/default, not that agent's tool list.

## Related Issues

- #512 — [FEATURE] Add MCP servers to the skills and commands that lack them (CLOSED); overlaps in theme (MCP adoption) but that issue was about equipping skills/commands, not default research routing.

## Testing Notes

After a fix, in a session with Context7/Tavily installed, ask a documentation question and a current-information question and confirm the first tool call is Context7 (docs) or Tavily (web), with WebFetch/WebSearch used only as fallback (server missing, error, or out-of-scope question). Also confirm a delegated research task either gets an agent with the MCP tools or the orchestrator performs the lookup itself.

<!-- sc:issue:create template=issue-bug-simple -->
