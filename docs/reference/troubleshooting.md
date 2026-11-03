# SuperClaude Troubleshooting Guide 🔧

Quick fixes to advanced diagnostics for SuperClaude Framework issues.

## Quick Fixes (90% of problems)

**Installation Verification:**

```bash
superclaude --version          # Should print: SuperClaude, version 5.0.0
superclaude install --list     # List the framework components
```

**Command Issues:**

```bash
# Test in Claude Code:
/sc:brainstorm "test project"        # Should ask discovery questions

# If no response: Restart Claude Code session
```

**Resolution Checklist:**

- [ ] `superclaude --version` prints `SuperClaude, version 5.0.0`
- [ ] `/sc:` commands respond in Claude Code
- [ ] MCP servers show their install status: `superclaude mcp --list`

## Common Issues

### Installation Problems

**Package Installation Fails:**

```bash
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

Install from the IronClaude repository, not from PyPI: the PyPI `superclaude`
package is the upstream project, not this fork. To move an existing install to
5.0.0, follow [Upgrading to IronClaude 5.0.0](../getting-started/upgrading.md).

**Permission Denied / PEP 668 Error:**

```bash
# Option 1: Use pipx (recommended)
pipx install git+https://github.com/IronbellyOrg/IronClaude

# Option 2: Fix permissions on the Claude config folder
sudo chown -R $USER ~/.claude
```

**Component Missing:**

```bash
superclaude install --force    # Reinstall the framework files, overwriting existing ones
```

### Command Issues

**Commands Not Recognized:**

1. Restart Claude Code completely
2. Verify: `superclaude --version` prints `SuperClaude, version 5.0.0`
3. Test: `/sc:brainstorm "test"`

**Agents Not Activating:**

- Use specific keywords: `/sc:implement "secure JWT authentication"`
- Manual activation: `@agent-security "review auth code"`

**Slow Performance:**

```bash
/sc:analyze src/auth --depth quick   # Analyze a smaller target with a quick pass
```

To check whether MCP servers cause the slowdown, `/sc:troubleshoot` and
`/sc:reflect` accept `--no-mcp`, which runs them with native tools only.

### MCP Server Issues

**Server Connection Fails:**

```bash
claude mcp list                      # Registered servers and their connection state
superclaude mcp --list               # Servers the installer knows, with install status
node --version                       # Node.js 18+ for npm-based servers, 20+ for Auggie
superclaude mcp --servers <name>     # Install or re-register one server
```

User-scope registrations live in `~/.claude.json`.

**API Key Required (Morphllm/Tavily):**

```bash
export MORPH_API_KEY="your_key"      # morphllm-fast-apply
export TAVILY_API_KEY="your_key"     # tavily
```

### Freshness Hook Issues

The freshness hooks block `Edit`/`Write` against files Claude hasn't Read in
the last 30 minutes. See [Context Freshness Hooks](../user-guide/freshness-hooks.md)
for the full guide.

**Unexpected block: "You have not Read \`X\` in this session":**

- Expected on the first edit against a file in a fresh session — Claude will Read then retry.
- If creating a brand-new file: use a Bash heredoc (`cat > newfile <<EOF…EOF`); the gate doesn't apply to Bash.

**Hook silently not firing:**

```bash
jq -r '.hooks | keys[]' ~/.claude/settings.json    # Should list SessionStart, PreToolUse, etc.
ls ~/.claude/hooks/freshness-*.sh                  # 7 files, mode 0755
which jq                                           # jq is required; install with apt/brew
tail -F ~/.claude/logs/freshness-hook.jsonl        # Watch telemetry as you work
```

**See block decisions / why a request was halted:**

```bash
jq -c '.' ~/.claude/logs/freshness-hook.jsonl | tail -10
# decision=block + reason=no_prior_read / read_too_old explain the gate's choice
```

**Restore settings.json after a bad merge:**

```bash
ls -t ~/.claude/settings.json.bak.* | head -1 | xargs -I{} cp {} ~/.claude/settings.json
```

**Opt out (selective):** remove an event key from `~/.claude/settings.json` under `hooks`.
**Opt out (global):** remove all `freshness-*` entries from `~/.claude/settings.json` and `rm ~/.claude/hooks/freshness-*.sh`. Re-enable with `superclaude install --force`.

## Advanced Diagnostics

**System Analysis:**

```bash
superclaude doctor --verbose         # Plugin, command-to-skill and configuration checks
```

**Component Analysis:**

```bash
ls -la ~/.claude/                    # Check installed files
grep -r "@" ~/.claude/CLAUDE.md      # Verify imports
```

**Reset Installation:**

```bash
superclaude install --force          # Overwrite the installed framework files
```

`superclaude install --force` overwrites edited core files, commands and agents
in `~/.claude/` without a backup, so copy any file you changed first. There is
no backup or uninstall command.

## Get Help

**Documentation:**

- [Installation Guide](../getting-started/installation.md) - Setup issues
- [Commands Guide](../user-guide/commands.md) - Usage issues

**Community:**

- [GitHub Issues](https://github.com/IronbellyOrg/IronClaude/issues)
- Include: OS, Python version, error message, steps to reproduce
