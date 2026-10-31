# MCP Server Installation Guide

SuperClaude provides a convenient CLI command for installing and managing MCP (Model Context Protocol) servers for Claude Code.

## Default setup: codegraph

`superclaude install` (and so `./update.sh`) installs **codegraph**, a code-graph server (symbols, callers, impact, file outlines), as a required user-level phase. Everything else is opt-in through `superclaude mcp`.

- **Pinned and verified.** The phase uses codegraph `v1.6.2` only. It first looks for a copy that already prints `1.6.2` (`codegraph` on `PATH`, then `~/.local/bin/codegraph`; a copy baked into an image is reused with no network). Otherwise it downloads the release tarball for your platform (Linux or macOS, x64 or arm64), checks its SHA-256 against the value pinned in the source, and only then extracts it to `~/.codegraph/versions/v1.6.2/`. It never runs upstream's `install.sh` or `codegraph install`.
- **Registered at user scope**, equivalent to:

  ```text
  claude mcp add-json codegraph '{"type":"stdio","command":"<absolute path>","args":["serve","--mcp"],"alwaysLoad":true,"env":{"CODEGRAPH_TELEMETRY":"0","CODEGRAPH_NO_UPDATE_CHECK":"1","CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"}}' --scope user
  ```

  Telemetry and update checks are off. `superclaude install` repairs an entry it wrote itself (old path, missing field) and never replaces an entry you changed: a user-managed `codegraph` entry whose command runs is kept, with the command to hand it back.
- **Tool list.** Upstream lists only `codegraph_explore` by default. `CODEGRAPH_MCP_TOOLS` replaces that with seven narrower tools (`codegraph_node`, `_search`, `_callers`, `_callees`, `_impact`, `_files`, `_status`); `codegraph_explore` is hidden and a call to it fails. The seven schemas add about 1,861 tokens to a session (measured with four headless runs; the 2,000-token limit is a proposal, not yet confirmed by the maintainers).
- **Run it again any time.** A second `superclaude install` makes no download and no registry change. `superclaude install --list` prints what is installed (`Executable`, `Owner`, `User registration`, `Ready for Serena retirement`) without changing anything; `superclaude doctor` fails only when the registered command no longer exists.
- **No Windows install.** On an unsupported platform the phase stops with the manual steps unless a matching copy is already on `PATH`.

### If the codegraph phase fails

`superclaude install` still installs everything else, prints the failed stage and exits 1 (so `./update.sh` stops).

| Stage | Typical cause | What to do |
|---|---|---|
| prerequisites | `claude` missing or `claude --version` fails | Install Claude Code, rerun `superclaude install` |
| platform | not Linux or macOS on x64 or arm64 | Install codegraph yourself so `codegraph --version` prints `1.6.2`, rerun |
| download | network error, proxy, timeout | Fix the network (`https_proxy` is honoured), rerun |
| checksum | the file does not match the pinned SHA-256 | Do not retry blindly: report it |
| extract | bad archive, or the extracted copy is not `1.6.2` | Rerun; report if it repeats |
| registration | `~/.claude.json` unreadable or `claude mcp` failed | Fix the file or run the printed command, rerun |

### Removing codegraph

```bash
claude mcp remove codegraph --scope user
```

Then delete the paths `superclaude install --list` prints as owned (the version directory under `~/.codegraph/versions/`, the `~/.local/bin/codegraph` and `~/.codegraph/current` links, then the receipt `~/.codegraph/.superclaude-receipt.json`). Copies you or an image installed are never listed. Remove a project's index with `codegraph uninit` in that project.

### Indexing: one index per checkout

A session-start hook (`~/.claude/hooks/codegraph-session-start.sh`, event `SessionStart`, matcher `startup`) starts one background `codegraph init --yes` in the git top-level of a checkout that has no `.codegraph/codegraph.db`. Clones, sibling worktrees and new projects each get their own index on their first session. It never runs in `$HOME`, `/` or a directory outside git, never touches an existing index, prints nothing and cannot fail a session. While a session is open codegraph keeps the index fresh; edits made with no session open are caught when the next session connects.

- **Cost.** About 70 KB on disk per indexed file and up to about 1 GB of memory while the first `init` runs; seconds for a small repository, around 100 seconds for 27,000 files. The first answers in a brand-new checkout can be incomplete until the init finishes.
- **Opt out.** Set `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` in the environment (or in the `env` block of `~/.claude/settings.json`). It disables **only** this session-start hook: not the MCP server, not the installer phase, not any command or skill. Use it for CI and for headless pipelines (`claude -p` also fires `startup`). Every IronClaude codegraph switch starts with `SUPERCLAUDE_CODEGRAPH_`. To exclude files from one project, add excludes to its `codegraph.json`.
- **Progress log.** `${XDG_STATE_HOME:-~/.local/state}/superclaude/codegraph-init.log`.
- **Git ignore.** codegraph's `.codegraph/` folder shows up as untracked. Add `.codegraph/` to your global git ignore file (the file named by `core.excludesFile`, by default `~/.config/git/ignore`) so it never shows up in `git status` or `git add -A`.
- **Optional `post-checkout` recipe** (not installed; IronClaude writes no git config and installs no git hooks). In a repository's `.git/hooks/post-checkout`: `[ -e .codegraph/codegraph.db ] || (nohup codegraph init --yes "$PWD" </dev/null >/dev/null 2>&1 &) ; exit 0`. Use `init`, never `sync` or `index`, which can empty an index that is being built.

### Serena is removed once codegraph is ready

In the first `superclaude install` where codegraph is registered and usable (`Ready for Serena retirement: yes` in `install --list`), the cleanup step also removes every user-scope MCP entry other than `serena-local` that launches Serena (arguments contain `start-mcp-server`, `env` and `headers` absent or empty), whatever its name, and the `~/.local/bin/codebase-memory-mcp` registration. Until then the current-pin `serena` entry is kept and the removal command is printed. A launcher entry with non-empty `env` or `headers` is kept; the cleanup step reports that ("customised registration") only for an entry named `serena`, and says nothing about a renamed one. To keep Serena, register it yourself as `serena-local`; the installer never removes that name.

Kept by policy: `~/.serena`, project `.serena/` folders, `~/.cache/codebase-memory-mcp`, the uv cache and, outside Coder, a `serena-agent` uv tool you installed (the removal command is printed). Local-scope (`projects.*.mcpServers`) and `.mcp.json` entries are never read or removed by the installer; if a project still registers `serena` or `codebase-memory-mcp` that way, run `claude mcp remove <name> --scope local` (or `--scope project` for `.mcp.json`) in that project. The root-owned `/usr/local/bin/codebase-memory-mcp` in the Coder image goes only with a new image, and a `~/.local/bin/codebase-memory-mcp` binary with its client companions stays, with its `uninstall -y` command printed.

### Commands and skills that use codegraph

IronClaude's commands, skills and agents use codegraph above a Grep/Read fallback, following the shared guide `~/.claude/CODEGRAPH.md` (installed with the core files). Two commands expose it directly: `/sc:graph` (or `/sc:graph status`) reports whether this worktree's index is ready, and `/sc:graph init` builds it by hand when the session-start hook did not; `/sc:impact <symbol>...` or `/sc:impact --diff <base>` lists production and test dependents, and `--tests` adds an advisory test list. Two switches, each with its own scope: `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` stops commands, skills and agents from using codegraph (they use Grep/Read only), and `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` turns off only the session-start index hook. Neither touches the MCP registration.

## What `superclaude install` Does With MCP

`superclaude install` installs framework files, commands, agents, skills, ccsession wiring, hooks, templates and user setup, then the codegraph phase above. It installs no other MCP server: use `superclaude mcp` for those (see below).

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
| **codegraph** | Code graph: symbols, callers, impact, file outlines; installed by `superclaude install` (see Default setup above) | No |
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
