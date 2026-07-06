---
source: codebase
quality_tier: primary
created: 2026-06-22T23:31:36Z
---

# Codebase Context: Tavily MCP Upgrade

## Relevant entry points

- `src/superclaude/cli/main.py` exposes the `superclaude mcp` command and delegates to `install_mcp_servers()` / `list_available_servers()` from `src/superclaude/cli/install_mcp.py`.
- `src/superclaude/cli/install_mcp.py` contains the live `MCP_SERVERS` registry used by `superclaude mcp --servers tavily`.
- `install_mcp_server()` builds a Claude Code command of the form `claude mcp add --transport <transport> [--scope <scope>] <name> [-e KEY=VALUE]... -- <command...>` for stdio servers.
- `prompt_for_api_key()` returns `os.getenv(api_key_env)` when present, otherwise prompts and returns a value that becomes `-e TAVILY_API_KEY=<value>` for local stdio installs.
- Existing installed-server detection is coarse: `check_mcp_server_installed(server_name)` only checks whether the server name appears in `claude mcp list`; it does not detect whether an existing Tavily server was installed with stale `tavily-mcp@0.1.2`.

## Current Tavily divergence

- Live installer: `MCP_SERVERS["tavily"]` uses `transport: "stdio"`, `command: "npx -y tavily-mcp@0.1.2"`, `api_key_env: "TAVILY_API_KEY"`.
- Docs: `docs/user-guide/mcp-servers.md` documents `args: ["-y", "tavily-mcp@latest"]` for Tavily.
- Config artifacts: `src/superclaude/mcp/configs/tavily.json` and `plugins/superclaude/mcp/configs/tavily.json` both use `mcp-remote https://mcp.tavily.com/mcp/?tavilyApiKey=${TAVILY_API_KEY}`.
- Repository search found no Python loader references to `src/superclaude/mcp/configs/tavily.json` or `plugins/superclaude/mcp/configs/tavily.json`; the live path is `MCP_SERVERS` in `install_mcp.py`.

## Test surfaces discovered

- No direct test file for `install_mcp.py` was found in the active test tree by the codebase sweep.
- `.dev/releases/complete/v1.0-mcp-installer/test-strategy.md` sketches historical MCP installer test categories including npm servers, API keys, installation flow, and no direct CLI calls, but it is an archived strategy artifact rather than an active test.

## Constraints from implementation shape

- The current command builder always appends `--` and then splits `server_info["command"]` with `shlex.split()`. Native HTTP transport likely needs a URL positional argument instead of a stdio command behind `--`; this is a real installer abstraction change, not just changing Tavily's command string.
- Local stdio API-key handling is already supported via `api_key_env` and `-e KEY=VALUE`.
- Remote HTTP OAuth does not require putting the API key in the URL, but API-key query/header forms are also documented by Tavily. The installer needs an explicit auth strategy if remote becomes an option.
- Back-compat must account for users with an existing installed Tavily server name: current detection would skip upgrade entirely.
