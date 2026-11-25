<!-- /sc:issue bug template (simple). -->

## Bug Summary

The user reports that documentation and online research questions default to WebFetch/WebSearch or manual searching instead of the available Context7 MCP (documentation) and Tavily MCP (web research). The observed incident shows a delegation decision bypassing those tools by selecting an agent whose tool list excludes them; the general frequency and root cause are not established.

Observed incident (this conversation, 2026-11-17): the user asked how to hide thinking/tool-call details in Claude Code. The orchestrator delegated the lookup to the `claude-code-guide` agent (tools: Glob, Grep, Read, WebFetch, WebSearch, no Context7/Tavily) instead of calling the available Context7/Tavily tools directly; the lookup was interrupted and the original question remains unanswered. This incident is a single observation; the broader claim that this happens "by default" is not verified beyond it.

## Environment (OS, version)

- OS: Linux 6.8.0-147-generic (dev container)
- Version: SuperClaude/IronClaude 5.0.0, branch docs/409-orca-dashboard-designs (commit 495eb96d1 at session start)

## Current Behavior

- The user reports repeated preference for WebFetch/WebSearch or manual searching despite available Context7/Tavily tools; this report has not been measured across sessions.
- In the observed incident, delegation went to an agent without Context7/Tavily in its tool allowlist (Glob/Grep/Read/WebFetch/WebSearch), and the orchestrator did not call the MCP tools itself before or instead of delegating.
- General MCP preference already exists in the framework instructions. The observed delegation did not preserve that preference. The MCP table calls its flag hints advisory, not all research-tool guidance; that wording alone does not establish the cause.

## Expected Behavior

- Questions needing library/framework documentation default to Context7; questions needing current online information default to Tavily search (with `tavily_extract` to confirm a likely answer before searching more).
- WebFetch/WebSearch and local code search remain valid fallbacks when the MCP server is unavailable, rate-limited, or the question is out of the servers' scope, not a blanket ban on either.
- Delegation for research questions either targets an agent whose tools include the research MCP servers, or the orchestrator performs the MCP lookup itself.

## Steps to Reproduce

1. In a session with Context7 and Tavily MCP installed, ask a question that requires documentation or current online information (e.g. "how do I hide thinking/tool details in Claude Code?").
2. Observe the session (or a delegated subagent) reach for WebFetch/WebSearch or manual searching rather than Context7/Tavily.

## Impact Assessment (Severity, Blast Radius)

- Severity: medium (provisional): the requested tool-selection preference was bypassed and the lookup was interrupted before an answer. Speed, freshness and accuracy differences were not measured; no data-loss incident was reported.
- Blast Radius: one observed interactive research delegation. Other documentation and online-research tasks may be affected, but wider prevalence is not verified.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

Quick pass (`--depth quick`) used Glob/Grep/Read. The issue worker's tool allowlist does not include codegraph or Auggie; this is a degraded source-text inspection, not a graph-backed analysis.

- `src/superclaude/core/CLAUDE.md:18-26`: the MCP table identifies Context7 for library/framework documentation and Tavily for web/current-information research. Its advisory note explicitly concerns the Flag column, not all tool-selection requirements.
- `src/superclaude/core/CLAUDE.md:32-43`: the ten Core Rules do not add a research-delegation rule; rule 8 ("Auggie first") covers pre-edit codebase context.
- `src/superclaude/mcp/MCP_Context7.md:13-19`: recommends Context7 over WebSearch for curated, version-specific documentation.
- `src/superclaude/mcp/MCP_Tavily.md:19-25`: recommends Tavily for structured/multi-source searching and current information, distinguishing that from single-page extraction. `src/superclaude/mcp/MCP_Tavily.md:325-331` lists native WebSearch as a fallback.
- `src/superclaude/core/RULES.md:194-201`: already requires best-tool selection with "MCP > Native > Basic" and names "context7 for docs". The issue is not a complete absence of MCP preference; preserving it across routing/delegation needs investigation.
- `src/superclaude/commands/explain.md:6,36,43`: `/sc:explain` declares Context7 integration for framework documentation.
- The worker found no repository-owned `claude-code-guide` agent definition under `src/superclaude/agents/`. The observed session supplied that agent with a restricted tool list. Changing that external definition is not established as a repository-owned fix; routing the lookup through available MCP-capable tools is a candidate.

## Related Issues

- #512: [FEATURE] Add MCP servers to the skills and commands that lack them (CLOSED); overlaps in theme (MCP adoption) but that issue was about equipping skills/commands, not default research routing.

## Testing Notes

After a fix, in a session with Context7/Tavily installed, ask a documentation question and a current-information question and confirm the first tool call is Context7 (docs) or Tavily (web), with WebFetch/WebSearch used only as fallback (server missing, error, or out-of-scope question). Also confirm a delegated research task either gets an agent with the MCP tools or the orchestrator performs the lookup itself.

<!-- sc:issue:create template=issue-bug-simple -->
