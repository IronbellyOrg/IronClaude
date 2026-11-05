# Option B: real session token measurement

Method: two headless runs with the executor's real login but no user MCP servers: `claude -p "reply ok" --output-format json --strict-mcp-config --mcp-config <cfg>` where `<cfg>` registers only the extracted codegraph (`serve --mcp`, `alwaysLoad`), once without and once with `CODEGRAPH_MCP_TOOLS`. Delta = difference in reported input tokens (input + cache creation + cache read). Pass when delta <= 2000 tokens.

Pros:
- Measures the real quantity the 2K threshold is about (session context tokens).
- Uses the exact Claude Code version that will load the server.

Cons:
- Needs a logged-in `claude` and network to Anthropic; an unattended executor without auth stops (human item).
- Uses the real HOME (`--strict-mcp-config` keeps `mcpServers` untouched, but sessions rewrite other parts of `~/.claude.json`).
- JSON `usage` field names and whether `--strict-mcp-config` with `alwaysLoad` lists the tools are UNVERIFIED; small run-to-run noise.
- Does not by itself prove explore is blocked (needs the stdio client anyway).
