# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Concrete incident (2026-11-17): user asked how to hide thinking/tool details in Claude Code; the orchestrator delegated to the `claude-code-guide` agent (tools Glob/Grep/Read/WebFetch/WebSearch, no Context7/Tavily) and did not call Context7/Tavily directly; the lookup was interrupted and the question is still unanswered. Source: this conversation's task brief.
- The routing hints in the framework MCP table are explicitly "advisory" with no default-first rule for research questions. Source: src/superclaude/core/CLAUDE.md:22-26.
- No Core Rule covers research-tool routing (rule 8 "Auggie first" is pre-edit context only). Source: src/superclaude/core/CLAUDE.md:32-43.
- Context7 and Tavily already document "Choose When: Over WebSearch/WebFetch" preferences, and Tavily lists native WebSearch as a fallback — the intended default-vs-fallback shape exists but only as per-call chooser docs. Source: src/superclaude/mcp/MCP_Context7.md:13-19, src/superclaude/mcp/MCP_Tavily.md:19-25,325-331.
- RULES.md Tool Optimization says "MCP > Native > Basic" and "context7 for docs", but as generic guidance without a research default. Source: src/superclaude/core/RULES.md:194-201.
- `/sc:explain` declares `mcp-servers: [context7, codegraph]`, an existing pattern for docs questions. Source: src/superclaude/commands/explain.md:6,36,43.
- No agent named `claude-code-guide` exists in this repo (`src/superclaude/agents/`, Grep: no matches); it is a Claude Code built-in, so the fixable gap here is orchestrator routing, not that agent's tool list.
- Related issue #512 found via duplicate search (gh issue list --repo IronbellyOrg/IronClaude --state all --search ...), CLOSED, thematic overlap only.
- Version/environment details (SuperClaude 5.0.0, branch, OS) taken from session context, not the description.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
