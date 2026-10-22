# MCP Server Installation Guide

SuperClaude provides a convenient CLI command for installing and managing MCP (Model Context Protocol) servers for Claude Code.

## Default Framework Setup: Codebase Memory MCP

`superclaude install` installs framework files, commands, agents, skills, ccsession wiring, hooks, templates and user setup, then runs a **required user-level Codebase Memory MCP phase**. There is no additional opt-in question. This is full upstream setup, not just MCP registration: it can configure detected clients and companion instructions, skills, agents and hooks across your account. Existing graph indexes are retained.

Automated native installation and removal support **Linux amd64/arm64 only** (`x86_64`/`aarch64` aliases are accepted). macOS, Windows and other unsupported platforms are rejected before native effects. The framework files already installed remain, but the required phase is incomplete and the command exits 1. For those platforms, consult the [official upstream installation instructions](https://github.com/DeusData/codebase-memory-mcp#installation) for separate manual setup. Manual setup is not a built-in bypass that makes the required framework phase pass on an unsupported platform.

When acquisition is needed, IronClaude downloads the **complete** official script from:

<https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh>

It requires a successful, nonempty HTTPS download into a private temporary directory before executing the script through argv-based Bash invocation, with the canonical destination `~/.local/bin/codebase-memory-mcp`. This preserves the full behavior requested by the upstream curl/Bash installation command, including release checksum verification and detected-client setup; no client filtering or configuration suppression is used. Download and installer timeouts are 60 and 300 seconds respectively, and temporary script material is cleaned up on success or failure.

The bootstrap tracks mutable `main` and fetches moving latest-release assets: **neither is pinned**. Release checksums do not authenticate the bootstrap itself. Review this trust boundary before installing. The CLI reports the verified executable version and registration outcome; it does **not** index a repository or prove a live MCP handshake. Restart clients to load integrations.

### Reuse, Updates and Previews

- A working canonical executable takes precedence over a usable PATH installation. A working binary and correct user stdio registration (absolute executable, no server arguments) are reused without download or native upgrade. A missing registration is repaired without rerunning upstream companion setup. External binaries are not silently replaced; ambiguous discovery fails closed.
- `superclaude install --list` is read-only. It reports executable availability and exact user-registration status, including unknown or stale/unverified states, rather than repairing them. This is not a live connection check.
- `superclaude install --force` reinstalls framework files only; it does not force native upgrades or index resets. `--target` changes only the slash-command destination, not native paths, user setup or MCP scope. There is no framework-wide dry-run option.
- `superclaude update` keeps its existing framework behavior: it neither upgrades nor reinstalls Codebase Memory. A later explicit `superclaude install` restores the default bundle if it was removed. There is no adopt, skip or native-upgrade lifecycle flag.
- On acquisition, executable verification or registration failure, framework installation exits 1 and keeps successful framework steps. Review the failed stage and any upstream output before retrying `superclaude install`; partial upstream effects are not rolled back. For registration-only recovery, explicit MCP installation uses the same shared path.

## Quick Start

```bash
# List available MCP servers
superclaude mcp --list

# Interactive management (terminal required)
superclaude mcp

# Explicit Codebase Memory setup or registration repair
superclaude mcp --servers codebase-memory-mcp

# Install specific servers (repeat --servers for each name)
superclaude mcp --servers tavily --servers context7

# Install all individual servers (not the gateway)
superclaude mcp --servers context7 --servers playwright --servers serena --servers morphllm-fast-apply --servers tavily --servers auggie --servers codebase-memory-mcp
```

With no selection on a terminal, the action menu offers **Install MCP servers** (default), **Uninstall Codebase Memory MCP**, and **Cancel**. The install branch still offers the gateway first (default `g`); option `0` installs all individual registry servers, including Codebase Memory, not the gateway. An explicit gateway-plus-native selection processes both and reports failures from either.

Without a terminal, installation requires explicit `--servers` selections; removal also requires `--yes`. Selecting native installation authorizes the full upstream setup described above. `--yes` never selects a server or bypasses unrelated API-key prompts.

`superclaude mcp --list` lists available servers without installing or repairing them. Its legacy installed markers are not exact native ownership/scope/health proof; use `superclaude install --list` for detailed native status. MCP list mode rejects server selections, `--uninstall`, `--yes`, `--dry-run`, or a non-user scope rather than combining listing with lifecycle actions.

## Available MCP Servers

| Server | Description | Requires API Key |
|--------|-------------|------------------|
| **codebase-memory-mcp** | Native graph memory with full upstream companion setup (Linux, user scope) | No |
| **airis-mcp-gateway** | Unified gateway; separate Docker-based installation | No (some hosted tools need keys) |
| **context7** | Official library documentation and code examples | No |
| **playwright** | Cross-browser E2E testing and automation | No |
| **serena** | Semantic code analysis and intelligent editing | No |
| **morphllm-fast-apply** | Fast Apply for context-aware code modifications | Yes (`MORPH_API_KEY`) |
| **tavily** | Web search and real-time information retrieval | Yes (`TAVILY_API_KEY`) |
| **auggie** | Semantic codebase search via Augment Code | No (requires `auggie login`) |

## Installation Scopes

The SuperClaude MCP command defaults to **user** scope (unlike the Claude CLI's local default). Individual servers other than Codebase Memory retain their existing registration scopes:

- **local**: Project-specific, private configuration
- **project**: Team-shared via `.mcp.json` file in version control
- **user** (default): Available across all your projects

Codebase Memory full native setup/removal accepts **user only**. Project/local selections fail before download or writes: the upstream lifecycle affects detected clients across the account, not just a project.

```bash
# Install for current project only
superclaude mcp --servers tavily --scope local

# Install for team (shared in version control)
superclaude mcp --servers context7 --scope project

# Install for all your projects
superclaude mcp --servers serena --scope user
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

- **Claude CLI**: Required for MCP registration and native setup.
- **Codebase Memory**: Linux amd64/arm64; **curl and Bash only when acquisition is needed**. It does not need Node/npm, Docker, an API key or a compiler. Reusing a working binary does not require curl/Bash.
- **npm-based servers**: Node.js 18+ and npx/npm; Auggie `0.36.0` requires Node.js 20+.
- **Serena**: uv.
- **AIRIS Gateway**: Running Docker and curl. Selecting it alongside Codebase Memory requires both sets of prerequisites.

Check prerequisites:

```bash
# Check Claude CLI
claude --version

# Check Node.js
node --version

# Check uv (optional)
uv --version
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
superclaude mcp --servers codebase-memory-mcp --dry-run
superclaude mcp --uninstall --servers codebase-memory-mcp --dry-run
superclaude mcp --servers tavily --dry-run
```

No-selection dry-run prints choices and exits. Native previews disclose the full source URL, destination, account-wide companion effects and retained indexes. Bounded read-only discovery may run, but dry-run never downloads or runs the upstream installer/uninstaller, changes registration/files, or asks for consent/API keys.

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

## Safe Codebase Memory Removal

The new flat-command flags are `--uninstall` and `--yes/-y`; removal accepts only `codebase-memory-mcp`, not other servers or mixed selections.

```bash
# Inspect the account-wide removal plan without changes or prompts
superclaude mcp --uninstall --servers codebase-memory-mcp --dry-run

# Terminal: show preview and ask for confirmation (default No)
superclaude mcp --uninstall --servers codebase-memory-mcp

# Explicit consent, also required without a terminal
superclaude mcp --uninstall --servers codebase-memory-mcp --yes
```

Full removal delegates detected-client/owned companion cleanup and activation shutdown to upstream and may interrupt active Codebase Memory sessions. It is not project-only deregistration. IronClaude invokes the verified canonical executable with `uninstall -y --dir=<canonical-bin-directory>`: `-y` keeps indexes without offering another index-deletion prompt. It never requests index deletion/reset or manually erases caches, project files, instructions, skills or hooks. The adjacent updater is left in place and reported; alternate PATH installations are also reported, not removed.

Automatic native removal requires the private receipt `~/.local/bin/.superclaude-codebase-memory.json`, created **only after IronClaude actually acquires and verifies the binary**. The receipt must match its canonical binary's identity and SHA-256 hash; the canonical path or filename alone is not ownership proof. Reusing a preexisting/manual/external binary does not adopt it or create a receipt. An upstream-updated/replaced binary no longer matches the old receipt. Missing/mismatched proof or symlink/ownership ambiguity stops automatic removal: use the original installation/removal mechanism, not a fabricated receipt. Successful native removal revokes IronClaude's matching receipt.

After native success, IronClaude checks binary absence and removes only a surviving **exact user-scoped** `codebase-memory-mcp` entry through the Claude CLI. IronClaude's residual cleanup does not remove project/local entries or similarly named/unrelated servers; upstream's full owned-integration cleanup remains account-wide.

| Observed state | Outcome and recovery |
|---|---|
| Binary and exact user entry absent, no alternate binary | Idempotent no-op; companion assets were not audited. Indexes/updater are retained. |
| Binary absent, exact user entry present, no alternate binary | Confirmed registration-only partial cleanup; companion assets were not audited or removed. No download just to uninstall. |
| External/custom-only installation | Report its path and stop; use its original management mechanism. |
| Ambiguous discovery, unmatched receipt or unreadable registration | Fail closed. Inspect ownership/configuration before retrying; unknown is not absence. |
| Upstream nonzero/timeout or failed absence check | Report possible partial removal. Inspect output/state before retrying the same explicit removal command; no rollback or blind second cleanup is claimed. |

## Troubleshooting

### Codebase Memory Setup or Registration Failure

Use `superclaude install --list` to distinguish missing/non-runnable/ambiguous executables from absent, unknown or stale user registration. Repair missing curl/Bash only if acquisition is required; installing Node/npm does not repair this native path. A usable external binary can be reused without overwriting it; a non-runnable external binary requires attention through its own installer.

Fix unreadable/malformed user configuration before retrying. The native path reconciles only the exact user entry; a same-named project/local entry is not user-install success. Stale user registration is captured before replacement and restored if the add fails. A restoration failure is reported separately and needs inspection, not a success assumption. Retry explicit setup with `superclaude mcp --servers codebase-memory-mcp`, or retry `superclaude install` to complete the required framework phase. Restart clients after success, then verify actual tool use separately.

### Server Not Found

If you see "Unknown server: xxx", check the available servers:

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

1. **Start with essentials**: Install `context7` and `serena` first
2. **Add as needed**: Install other servers based on your workflow needs
3. **Use appropriate scope**: For other individual servers, use `--scope project` when sharing team configuration; Codebase Memory full lifecycle is user-only
4. **Secure API keys**: Never commit API keys to version control

## Release Gate: Separately Authorized Live Smoke

**Passed on 2026-10-22** for upstream codebase-memory-mcp 0.12.1 (Linux amd64) in a disposable workspace: install only adds entries and files, removal restores the captured client configuration exactly, indexes and unrelated hooks survive, and update does not restore a removed tool. Known residuals are upstream-owned: the first install may append a PATH line to `~/.bashrc`, and may leave empty `~/.codex/AGENTS.md` and `~/.config/opencode/AGENTS.md` after removal. Re-run this procedure before relying on a materially different upstream release.

This is an operator procedure, not permission to execute it. Obtain separate approval for real downloads, native setup/removal, client processes and the live query. Mocked regression tests cannot prove released-binary behavior or upstream companion-file merge safety.

1. **Isolate the account and processes.** Use a disposable Linux amd64/arm64 VM or container with a separate account and process namespace. Do not mount the host's HOME, configuration, cache, credentials, Docker socket or project MCP files; do not share host processes. Merely changing `HOME` on the developer account is insufficient because native activation/removal can affect account-wide processes. Keep all binaries, fixtures, config, caches and evidence inside the disposable environment. Have UV, Claude CLI, curl/Bash and the approved IronClaude release wheel provided there; install the wheel into a clean, activated environment using UV. Use only separately provisioned disposable client credentials if required, never the developer's credentials. Do not build a new container harness for this check.
2. **Record a clean baseline.** Confirm no native Codebase Memory binary or acquisition receipt is present. Record the wheel identity, OS/architecture, bootstrap URL/observation time and upstream source revision inspected. Snapshot disposable user settings, instructions, hooks, client registrations and relevant file hashes. Seed an unrelated user hook and config entry, a similarly named MCP entry, and same-named project/local entries in a disposable fixture project. Retain the wheel's expected framework hook files/registrations for comparison. Place a harmless, known-content sentinel in the effective graph cache (`CBM_CACHE_DIR` if set, otherwise `~/.cache/codebase-memory-mcp`); record its path/hash. Use a retained disposable graph index as an additional sentinel if available; installation itself must not index a repository.
3. **Exercise fresh normal setup.** Inside that environment only, run `superclaude install` and retain output/exit status. Require success after full framework/user setup and native acquisition. Check the disclosed full URL and canonical destination, real checksum verification, actual installed binary version/hash, and the private acquisition receipt. Record the fetched release asset identity as well as the moving bootstrap evidence: the reviewed source revision is not a release pin, and source inspection alone is not proof of packaged-binary behavior.
4. **Inspect real companion merges.** Compare actual framework hooks/files with the wheel's expected assets and compare unrelated user hooks, instructions, settings and registrations with the baseline. Inspect all detected-client companion changes reported by upstream, not just Claude's MCP entry. Confirm unrelated hooks still function. **If upstream overwrites unrelated assets, stop, block release and revise the integration with the user. Do not quietly substitute binary-only installation.** Keep before/after evidence and any partial effects.
5. **Verify real registration and a query.** Run `claude mcp get codebase-memory-mcp` from an empty disposable directory without a project/local shadow. Confirm user scope, stdio, the selected absolute executable and no arguments; also inspect the exact user entry in the disposable configuration. Restart Claude Code, inspect `/mcp`, and request the server's read-only `list_projects` tool. Record the real MCP response (an empty project list is valid), not just registration output or a direct native CLI query. Do not index a repository to make this check pass. Verify the project/local and unrelated entries remain intact.
6. **Prove repeat-install behavior.** Snapshot binary/receipt hashes and companion files, then repeat `superclaude install` and `superclaude mcp --servers codebase-memory-mcp`. Require successful reuse without another bootstrap download, native install or upgrade. Confirm unrelated assets and index sentinels remain. Preview native install/removal with `--dry-run` and inspect `superclaude install --list`; compare snapshots to confirm no mutation or prompts.
7. **Exercise native removal.** Preview with `superclaude mcp --uninstall --servers codebase-memory-mcp --dry-run`, then run `superclaude mcp --uninstall --servers codebase-memory-mcp --yes`. Record account-wide consent/output, exit status and the actual packaged binary's `uninstall -y --dir=<canonical-bin-directory>` behavior. Require canonical binary and matching receipt absence, exact user-registration absence, unchanged index sentinel contents/hashes, preserved unrelated framework/user hooks/config and project/local entries. Record the adjacent updater's actual retained path/status and any alternate PATH binaries rather than claiming everything disappeared. Do not manually erase residual assets to turn a failed check into a pass.
8. **Check update versus restoration.** Run `superclaude update`: the removed binary/receipt/user entry must stay absent. Then run an explicit `superclaude install`: require full acquisition/registration to return with a fresh matching receipt and retained index sentinels. Remove it again through the confirmed MCP command if teardown evidence is needed, then dispose of the isolated environment.
9. **Close the gate only with evidence.** Save approval, commands/exit statuses, bootstrap and released-binary identities, redacted before/after comparisons, query response, repeat-install observations and uninstall/index/updater results under the task's artifacts directory. Any failed or unverified check leaves release blocked. Documentation completion does not authorize this smoke, release, commit or push.

## See Also

- [MCP Server Documentation](mcp-servers.md) - Detailed server descriptions
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp) - Official MCP documentation
- [Commands Guide](commands.md) - SuperClaude commands that use MCP servers
