# Variant 1 — Architect Lens

## Position

Converge the Tavily MCP installer around one source of truth and isolate command-building so transport choices are represented explicitly. Keep the default local stdio path for this upgrade, because remote HTTP requires a different Claude CLI grammar and an OAuth/browser UX that should not be bundled into a package-version correction.

## Requirements

1. `src/superclaude/cli/install_mcp.py` must stop hard-pinning `tavily-mcp@0.1.2` and use a centralized Tavily package/version token.
2. The live installer registry is the source of truth; docs must agree with it and dormant config files must not contradict it.
3. Extract or test the command-building grammar so stdio servers continue to emit `claude mcp add --transport stdio <name> [-e ...] -- <command...>` with the server name before env flags.
4. A future HTTP transport path should be modeled separately because it needs `claude mcp add --transport http <name> <url>` rather than a stdio `-- <command>` tail.
5. Existing stale `tavily` installs must be detected and reconciled rather than skipped by name-only installed checks.
6. Dry-run and real-run command echoing must not display actual API key values.

## Acceptance Criteria

- Fresh dry-run for `--servers tavily` shows local stdio with the new Tavily package token and no 0.1.x string.
- Tests fail if docs and installer disagree.
- Tests fail if dormant Tavily config artifacts remain divergent.
- Tests cover stale-install migration, command grammar ordering, and masked dry-run output.
- Post-install verification guidance includes the expected map/crawl tool surface.
