# Current read-only CLI contract observations

These are completed documentation inspections, not instructions to execute commands and not a fresh product test run.

- Installed Claude CLI add-json help exposes explicit local/user/project scope and a JSON payload.
- Installed remove help exposes explicit local/user/project scope; omitting scope removes whichever scope is selected by the CLI.
- Installed get help exposes no scope or JSON option and warns that approved server lookups may perform health checks. No get/list lookup or connection was performed; only help text was inspected.
- Context7 official Claude Code documentation confirms user entries are top-level mcpServers in HOME/.claude.json; CLAUDE_CONFIG_DIR relocates that .claude.json inside the configured directory. Local entries live under project blocks; project configuration uses .mcp.json.
- Official documentation also demonstrates add-json with user scope. This closes the Tier-1 card's unverified layout/grammar note at the documentation level, not the still-pending released-binary/live integration gate.

Source: https://code.claude.com/docs/en/mcp-quickstart and https://code.claude.com/docs/en/self-hosted-environments-configuration (Context7 query during this audit), plus current installed CLI help captured by the orchestrator. No configuration mutation, server connection, native bootstrap, or upstream removal was executed.
