# SuperClaude Troubleshooting Guide 🔧

Quick fixes to advanced diagnostics for SuperClaude Framework issues.

## Quick Fixes (90% of problems)

**Installation Verification:**
```bash
python3 -m SuperClaude --version    # Should show 4.1.5
SuperClaude install --list-components
```

**Command Issues:**
```bash
# Test in Claude Code:
/sc:brainstorm "test project"        # Should ask discovery questions

# If no response: Restart Claude Code session
```

**Resolution Checklist:**
- [ ] Version commands work and show 4.1.5
- [ ] `/sc:` commands respond in Claude Code  
- [ ] MCP servers listed: `SuperClaude install --list-components | grep mcp`

## Common Issues

### Installation Problems

**Package Installation Fails:**
```bash
# For pipx users
pipx uninstall SuperClaude
pipx install SuperClaude

# For pip users
pip uninstall SuperClaude
pip install --upgrade pip
pip install SuperClaude
```

**Permission Denied / PEP 668 Error:**
```bash
# Option 1: Use pipx (recommended)
pipx install SuperClaude

# Option 2: Use pip with --user flag
pip install --user SuperClaude

# Option 3: Fix permissions
sudo chown -R $USER ~/.claude

# Option 4: Force installation (use with caution)
pip install --break-system-packages SuperClaude
```

**Component Missing:**
```bash
python3 -m SuperClaude install --components core commands agents modes --force
```

### Command Issues

**Commands Not Recognized:**
1. Restart Claude Code completely
2. Verify: `python3 -m SuperClaude --version`
3. Test: `/sc:brainstorm "test"`

**Agents Not Activating:**
- Use specific keywords: `/sc:implement "secure JWT authentication"`
- Manual activation: `@agent-security "review auth code"`

**Slow Performance:**
```bash
/sc:analyze . --no-mcp               # Test without MCP servers
/sc:analyze src/ --scope file        # Limit scope
```

### MCP Server Issues

**Server Connection Fails:**
```bash
ls ~/.claude/.claude.json            # Check config exists
node --version                       # Verify Node.js 16+
SuperClaude install --components mcp --force
```

**API Key Required (Magic/Morphllm):**
```bash
export TWENTYFIRST_API_KEY="your_key"
export MORPH_API_KEY="your_key"
# Or use: /sc:command --no-mcp
```

### Freshness Hook Issues (v4.3+)

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
SuperClaude install --diagnose
cat ~/.claude/logs/superclaude.log | tail -50
```

**Component Analysis:**
```bash
ls -la ~/.claude/                    # Check installed files
grep -r "@" ~/.claude/CLAUDE.md      # Verify imports
```

**Reset Installation:**
```bash
SuperClaude backup --create          # Backup first
SuperClaude uninstall
SuperClaude install --fresh
```

## Get Help

**Documentation:**
- [Installation Guide](../getting-started/installation.md) - Setup issues
- [Commands Guide](../user-guide/commands.md) - Usage issues

**Community:**
- [GitHub Issues](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)
- Include: OS, Python version, error message, steps to reproduce