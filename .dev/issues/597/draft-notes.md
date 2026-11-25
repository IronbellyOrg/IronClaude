# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Concrete incident (2026-11-17): user asked how to hide thinking/tool details in Claude Code; the orchestrator delegated to the `claude-code-guide` agent (tools Glob/Grep/Read/WebFetch/WebSearch, no Context7/Tavily) and did not call Context7/Tavily directly; the lookup was interrupted and the question is still unanswered. Source: this conversation's task brief.
- The framework MCP table names documentation/web use cases; its advisory wording concerns flag hints only, not all tool-selection requirements. Source: src/superclaude/core/CLAUDE.md:18-26. The initial draft's inference that all routing guidance is advisory was removed after source verification.
- The Core Rules do not add a research-delegation rule (rule 8 "Auggie first" concerns pre-edit context). Source: src/superclaude/core/CLAUDE.md:32-43.
- Context7 and Tavily already document preferences over native web tools for suitable tasks, and Tavily documents native WebSearch fallback. Source: src/superclaude/mcp/MCP_Context7.md:13-19, src/superclaude/mcp/MCP_Tavily.md:19-25,325-331.
- General MCP preference already exists: "MCP > Native > Basic" and "context7 for docs". The draft therefore does not claim a complete absence of guidance or an established root cause. Source: src/superclaude/core/RULES.md:194-201.
- `/sc:explain` declares Context7 integration for framework documentation. Source: src/superclaude/commands/explain.md:6,36,43.
- The worker found no repository-owned `claude-code-guide` definition under src/superclaude/agents/. The observed session supplied that restricted agent. Ownership of its definition is not established; repository-side routing is a candidate rather than a proven fix.
- Wider prevalence, performance/freshness/accuracy differences and a definitive cause are not verified. The issue distinguishes the user report from one observed delegation and treats medium severity as provisional.
- Expected behavior and testing notes describe MCP-capable delegation or an orchestrator lookup, preserve justified native-web fallback and do not ban local code inspection. These are proposed confirmation checks derived from the user's requested default.
- Related issue #512 found via duplicate search (gh issue list --repo IronbellyOrg/IronClaude --state all --search ...), CLOSED, thematic overlap only.
- Version/environment details (SuperClaude 5.0.0, branch, OS) taken from session context, not the description.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
