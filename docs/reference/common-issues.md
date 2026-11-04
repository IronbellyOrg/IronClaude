# SuperClaude Common Issues - Quick Reference 🚀

**Problem Solving Guide**: Most frequent issues with practical solutions.

## Top 5 Quick Fixes (90% of Issues)

### 1. Commands Not Working in Claude Code ⚡

```text
Problem: /sc:brainstorm doesn't work
Solution: Restart Claude Code completely
Test: /sc:brainstorm "test" should ask questions
```

### 2. Installation Verification

```bash
superclaude --version    # Should print: SuperClaude, version 5.0.0
```

If it prints an older version, or the command is missing, upgrade the package
and the installed files:

```bash
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

From an IronClaude clone, check out the release and run `./update.sh` instead.
Restart your Claude sessions afterwards. The full procedure is in
[Upgrading to IronClaude 5.0.0](../getting-started/upgrading.md).

`superclaude update` only re-copies files from the package that is already
installed. It does not install a newer package, install codegraph or remove
old MCP registrations, so use `superclaude install --force` for an upgrade.

### 3. Permission Issues

```bash
# Permission denied / PEP 668 errors:
# Option 1: Use pipx (recommended)
pipx install git+https://github.com/IronbellyOrg/IronClaude

# Option 2: Fix permissions on the Claude config folder
sudo chown -R $USER ~/.claude
```

Install from the IronClaude repository, not from PyPI: the PyPI `superclaude`
package is the upstream project, not this fork.

### 4. MCP Server Issues

```bash
superclaude mcp --list    # List the MCP servers the installer knows about
node --version            # Node.js 18+ for npm-based servers, 20+ for Auggie
```

To check whether a problem comes from MCP servers, `/sc:troubleshoot` and
`/sc:reflect` accept `--no-mcp`, which runs them with native tools only.

### 5. Component Missing

```bash
superclaude install --list     # List the framework components
superclaude install --force    # Reinstall them, overwriting existing files
superclaude doctor             # Check the installation
```

## Platform-Specific Issues

**Windows:**

Windows support is not verified. `superclaude install` has no option to choose
the Claude config folder: `--target` only sets the commands folder (default
`~/.claude/commands/sc`). The automatic codegraph download covers Linux and
macOS on x64 or arm64 only; on any other platform `superclaude install` exits 1
unless a `codegraph` that prints `1.6.2` is already on `PATH` or in
`~/.local/bin`.

**macOS:**

```bash
brew install python pipx node
pipx install git+https://github.com/IronbellyOrg/IronClaude
superclaude install
```

**Linux:**

Install Python 3.10 or newer, `pipx` and Node.js 18 or newer with your package
manager (distribution `nodejs` packages can be older than 18), then:

```bash
pipx install git+https://github.com/IronbellyOrg/IronClaude
superclaude install
```

## Verification Checklist

- [ ] `superclaude --version` prints `SuperClaude, version 5.0.0`
- [ ] `/sc:brainstorm "test"` works in Claude Code
- [ ] `superclaude install --list` shows components

## When Quick Fixes Don't Work

See [Troubleshooting Guide](troubleshooting.md) for advanced diagnostics.
