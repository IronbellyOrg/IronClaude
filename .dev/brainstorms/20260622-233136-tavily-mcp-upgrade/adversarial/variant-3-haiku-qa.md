# Variant 3 — QA Lens

## Position

The upgrade is only complete if it is observable in tests and dry-run output. Since the user-facing target is `tavily-mcp@latest`, test for that token, for no regression to 0.1.x, for migration behavior, and for map/crawl verification.

## Requirements

1. Set the installer package spec to `tavily-mcp@latest`, preferably via a named constant such as `TAVILY_MCP_PACKAGE = "tavily-mcp@latest"`.
2. Add tests for fresh install, stale 0.1.x upgrade, non-stale skip, dry-run behavior, API key env behavior, API key redaction, docs parity, config cleanup, transport shape, and command positional ordering.
3. Mark any live tool-surface check as integration/optional because it needs Node, Claude CLI, and a Tavily API key; unit tests should mock subprocess calls.
4. Ensure docs explicitly mention `tavily-map` and `tavily-crawl` as expected 0.2.x capabilities and explain how to verify them after install.
5. Keep stdio default and leave remote HTTP as a separately tested future path.

## Acceptance Criteria

- `uv run pytest` on the new Tavily installer tests passes.
- A dry-run with a stale mocked install prints both the removal/reinstall intent and the `@latest` add command, with secrets masked.
- Docs-installer parity test catches any mismatch.
- Optional integration test enumerates tools and requires map/crawl when live credentials are available.
