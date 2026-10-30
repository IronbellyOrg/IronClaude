# MCP Server Installation Guide

SuperClaude provides a convenient CLI command for installing and managing MCP (Model Context Protocol) servers for Claude Code.

## What `superclaude install` Does With MCP

`superclaude install` installs framework files, commands, agents, skills, ccsession wiring, hooks, templates and user setup. It does **not** install any MCP server: use `superclaude mcp` for that (see below).

At the end of the run it performs one short cleanup step for old user-level MCP registrations: it removes only entries (and IronClaude's own leftover receipt files) that IronClaude can prove it wrote, keeps any entry it cannot prove and prints the reason (and, for a legacy launcher registration, the exact `claude mcp remove ... --scope user` command to remove it by hand). The step is bounded in time, never changes the exit code of `superclaude install`, and never touches binaries, indexes, caches or memories. See the [CHANGELOG](../../CHANGELOG.md) for the full list of what it covers.

- `superclaude install --list` is read-only. It reports what the cleanup step would do, one line per name, without changing anything.
- `superclaude doctor` warns (never fails) when the cleanup step still has something to remove.
- `superclaude update` keeps its existing framework behavior and never touches MCP registrations; it only prints a notice telling you to run `superclaude install` when a removable legacy entry is present.
- `superclaude install --force` reinstalls framework files only. `--target` changes only the slash-command destination, not user setup or MCP scope. There is no framework-wide dry-run option.

## Quick Start

```bash
# List available MCP servers
superclaude mcp --list

# Interactive management (terminal required)
superclaude mcp

# Install specific servers (repeat --servers for each name)
superclaude mcp --servers tavily --servers context7

# Install all individual servers (not the gateway)
superclaude mcp --servers context7 --servers playwright --servers morphllm-fast-apply --servers tavily --servers auggie
```

With no selection on a terminal, the action menu offers **1. Install MCP servers** (default) and **2. Cancel**. The install branch then offers the gateway first (default `g`); option `0` installs all individual registry servers, not the gateway.

Without a terminal, installation requires explicit `--servers` selections.

`superclaude mcp --list` lists available servers without installing or repairing them. Its installed markers are not exact ownership, scope or health proof. List mode rejects server selections, `--dry-run`, or a non-user scope rather than combining listing with lifecycle actions.

## Available MCP Servers

| Server | Description | Requires API Key |
|--------|-------------|------------------|
| **airis-mcp-gateway** | Unified gateway; separate Docker-based installation | No (some hosted tools need keys) |
| **context7** | Official library documentation and code examples | No |
| **playwright** | Cross-browser E2E testing and automation | No |
| **morphllm-fast-apply** | Fast Apply for context-aware code modifications | Yes (`MORPH_API_KEY`) |
| **tavily** | Web search and real-time information retrieval | Yes (`TAVILY_API_KEY`) |
| **auggie** | Semantic codebase search via Augment Code | No (requires `auggie login`) |

## Installation Scopes

The SuperClaude MCP command defaults to **user** scope (unlike the Claude CLI's local default):

- **local**: Project-specific, private configuration
- **project**: Team-shared via `.mcp.json` file in version control
- **user** (default): Available across all your projects

```bash
# Install for current project only
superclaude mcp --servers tavily --scope local

# Install for team (shared in version control)
superclaude mcp --servers context7 --scope project

# Install for all your projects
superclaude mcp --servers context7 --scope user
```

## API Key Management

Some MCP servers require API keys for full functionality. SuperClaude will prompt you to enter these keys during installation.

### Getting API Keys

- **Tavily**: Get your API key from [https://app.tavily.com](https://app.tavily.com)
- **Morphllm**: Get your API key from the Morphllm service
- **Auggie**: Uses session auth (run `auggie login` after install). Headless alternative: set `AUGMENT_SESSION_AUTH`. Docs: [Auggie quickstart](https://docs.augmentcode.com/context-services/mcp/quickstart-claude-code)

### Setting API Keys

During installation, you'll be prompted:

```
🔑 MCP server 'tavily' requires an API key
   Environment variable: TAVILY_API_KEY
   Description: Tavily API key for web search (get from https://app.tavily.com)
   Would you like to set TAVILY_API_KEY now? [Y/n]:
```

You can also set environment variables beforehand:

```bash
export TAVILY_API_KEY="your-api-key-here"
export MORPH_API_KEY="your-api-key-here"
```

## Prerequisites

Before installing MCP servers, ensure you have the following tools installed:

Prerequisites are checked for the selected servers, not every server in the registry.

- **Claude CLI**: Required for MCP registration.
- **npm-based servers**: Node.js 18+ and npx/npm; Auggie `0.36.0` requires Node.js 20+.
- **AIRIS Gateway**: Running Docker and curl.

Check prerequisites:

```bash
# Check Claude CLI
claude --version

# Check Node.js
node --version
```

## Installation Process

1. **Check Available Servers**

   ```bash
   superclaude mcp --list
   ```

2. **Install Servers**

   Interactive mode (recommended):

   ```bash
   superclaude mcp
   ```

   Or specify servers directly:

   ```bash
   superclaude mcp --servers tavily --servers context7
   ```

3. **Verify Installation**

   ```bash
   claude mcp list
   ```

4. **Restart Claude Code**

   After installation, restart your Claude Code session to use the new servers.

5. **Test Servers**

   In Claude Code, use `/mcp` command to check server status and authenticate.

## Advanced Usage

### Dry Run

Preview choices or a selected operation without prompts or changes:

```bash
superclaude mcp --dry-run
superclaude mcp --servers tavily --dry-run
```

No-selection dry-run prints choices and exits. A dry-run never changes registrations or files, and never asks for consent or API keys.

### Multiple Servers

Install multiple servers in one command:

```bash
superclaude mcp --servers context7 --servers tavily
```

### Custom Scope

Specify installation scope:

```bash
superclaude mcp --servers tavily --scope project
```

## Troubleshooting

### Server Not Found

If you see "Unknown MCP server selection: xxx", check the available servers:

```bash
superclaude mcp --list
```

### API Key Issues

If a server isn't working:

1. Check if the API key is set:

   ```bash
   echo $TAVILY_API_KEY
   ```

2. Verify the server is installed:

   ```bash
   claude mcp list
   ```

3. Check server status in Claude Code:

   ```
   /mcp
   ```

### Installation Fails

1. **Check prerequisites**:

   ```bash
   claude --version
   node --version
   ```

2. **Check Node.js version** (must be 18+):

   ```bash
   node --version
   ```

3. **Try with verbose output**:

   ```bash
   superclaude mcp --servers tavily 2>&1 | tee install.log
   ```

## Integration with SuperClaude Commands

MCP servers enhance SuperClaude commands with additional capabilities:

- **/sc:research** - Uses Tavily for web search and real-time information
- **/sc:implement** - Can use Context7 for official documentation
- **/sc:test** - Can use Playwright for browser automation

## Best Practices

1. **Start with essentials**: Install `context7` first
2. **Add as needed**: Install other servers based on your workflow needs
3. **Use appropriate scope**: Use `--scope project` when sharing team configuration
4. **Secure API keys**: Never commit API keys to version control

## See Also

- [MCP Server Documentation](mcp-servers.md) - Detailed server descriptions
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp) - Official MCP documentation
- [Commands Guide](commands.md) - SuperClaude commands that use MCP servers
