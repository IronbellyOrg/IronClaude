# Option A: byte proxy over stdio (no Claude session)

Method: in a throwaway dir, verify and extract the pinned v1.6.2 tarball, `git init` a tiny repo, run a small Node stdio client twice against `codegraph serve --mcp` (env unset; env `CODEGRAPH_MCP_TOOLS=<7 tools>`). Each run records `JSON.stringify(tools/list .result.tools)` bytes plus `initialize .result.instructions` bytes. Delta = run2 - run1. Tokens estimated conservatively at 3 bytes per token: pass when delta <= 6000 bytes. Same client asserts `codegraph_explore` absent from run 2's list and that a `tools/call codegraph_explore` in run 2 returns an error (proves X-25).

Pros:
- Deterministic, offline after download, no auth, no cost; runs in any sandbox HOME.
- Same harness also proves "explore hidden and blocked".
- Fully scriptable acceptance (`jq`/`node` assertions).

Cons:
- Proxy: Claude Code may wrap or trim schemas, so the real context cost can differ from the bytes.
- The 3 bytes/token rate is a heuristic (JSON tokenises denser than prose); may fail a list that would pass a real measurement, dropping Phase 3 to the `status`-only branch.
