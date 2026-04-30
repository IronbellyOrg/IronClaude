# Auggie MCP Server

**Purpose**: Augment Code semantic codebase search with real-time indexing and proprietary embedding models

## Triggers
- "Where is X defined / used / referenced?" across an unfamiliar codebase
- High-level questions about architecture, integration patterns, or domain concepts
- Need for semantic (natural-language) code search rather than literal pattern matching
- Loading codebase context before significant edits or design work
- Cross-language retrieval where grep/glob is insufficient

## Choose When
- **Over Grep/Glob**: When the query is conceptual ("the auth subsystem") rather than literal (a known symbol or path)
- **Over Serena**: When you need broad codebase recall, not symbol-level navigation
- **Over WebSearch**: When the answer lives in this repository, not on the open web
- **For onboarding**: First-pass orientation in a large or unfamiliar codebase
- **Not for**: Exact symbol lookups, file path resolution, or version-controlled history (use Grep/Glob/git)

## Works Best With
- **Sequential**: Auggie surfaces relevant code → Sequential reasons over the architecture
- **Serena**: Auggie locates concepts → Serena performs precise symbol-level edits
- **Context7**: Auggie shows in-repo usage → Context7 supplies upstream library docs

## Tools
- **codebase-retrieval** — Natural-language semantic search across the indexed codebase
- **ask_question** — Q&A over the repository using Auggie's context engine
- **implement** — Apply a change in the repo (optional commit)

## Examples
```
"where do we handle JWT refresh?" → Auggie (semantic, cross-file)
"how does the wizard system orchestrate sub-agents?" → Auggie (architectural concept)
"find all references to UserService.login" → Serena (symbol-level)
"open the file at src/auth/jwt.ts" → Read (exact path known)
"what's the latest stable Next.js version?" → Context7 / WebSearch
```

## Installation

```bash
superclaude mcp --servers auggie
# Installs @augmentcode/auggie globally and registers the server with Claude Code.
# After install, run: auggie login   (one-time browser OAuth)
```

Manual three-step alternative:
```bash
npm install -g @augmentcode/auggie@latest
auggie login
claude mcp add --transport stdio --scope user auggie -- auggie --mcp --mcp-auto-workspace
```

Headless environments may set `AUGMENT_SESSION_AUTH` instead of running `auggie login`.

## Links
- [Auggie Quickstart for Claude Code](https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code)
- [@augmentcode/auggie on npm](https://www.npmjs.com/package/@augmentcode/auggie)
