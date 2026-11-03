<div align="center">

# 📦 SuperClaude Installation Guide

### **Transform Claude Code with commands, agents, skills, and MCP integrations**

<p align="center">
  <img src="https://img.shields.io/badge/version-5.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Platform-Linux%20|%20macOS%20|%20Windows-orange?style=for-the-badge" alt="Platform">
</p>

<p align="center">
  <a href="#-quick-installation">Quick Install</a> •
  <a href="#-requirements">Requirements</a> •
  <a href="#-installation-methods">Methods</a> •
  <a href="#-verification">Verify</a> •
  <a href="#-troubleshooting">Troubleshoot</a>
</p>

</div>

---

## ⚡ **Quick Installation**

<div align="center">

### **Choose Your Preferred Method**

| Method | Command | Platform | Best For |
|:------:|---------|:--------:|----------|
| **🐍 pipx** | `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` | Linux/macOS | **✅ Recommended** - Isolated environment |
| **📦 pip** | `pip install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` | Linux/macOS | Traditional Python setups |
| **🔧 Dev** | `git clone ... && uv venv && make install && uv run superclaude install` | Linux/macOS | Contributors & developers |

</div>

**Platforms.** `superclaude install` always installs codegraph (see
[codegraph](#codegraph)). Its automatic install supports Linux and macOS on x64
or arm64 only. On any other platform, including Windows, `superclaude install`
exits 1 unless a `codegraph` that prints `1.6.2` for `codegraph --version` is
already on `PATH` or in `~/.local/bin`. Most installed hooks are bash scripts.

> **IronClaude vs. the PyPI package.** IronClaude is a fork that still ships under the
> Python package name `superclaude`. The `superclaude` package on PyPI
> (`pipx install superclaude`) is the upstream SuperClaude Framework, not IronClaude: it
> does not include `HOW-WE-WORK.md` or this fork's commands. Install IronClaude from the
> repository (`https://github.com/IronbellyOrg/IronClaude`) as shown below. Installing
> from the repository URL needs read access to it.

### Global policy activation

`superclaude install` deploys IronClaude's core instructions, Bash inspection
batching policy, skills, agents, and hooks under `~/.claude/`. The policy is
therefore active in every project that loads normal user configuration—not only
inside the IronClaude repository.

Existing installations upgrade with:

```bash
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

See [Upgrading](upgrading.md) for the full steps. Do not use `superclaude update`
for this: it refreshes the files but never installs codegraph or retires old MCP
registrations.

The refresh preserves unrelated user hook registrations, refreshes
framework-owned hooks by command identity, and makes SubagentStart policy
injection synchronous. Start a new Claude Code session after installing or
upgrading; an already-running session does not reload its initial instructions.
No hard Bash counter is installed—the policy is advisory and keeps mutations or
adaptive diagnostics as separate calls.

---

## 📋 **Requirements**

<div align="center">

<table>
<tr>
<td align="center" width="50%">

### ✅ **Required**

| Component | Version | Check Command |
|-----------|---------|---------------|
| **Python** | 3.10+ | `python3 --version` |
| **Git** | Any | `git --version` |
| **pipx** (recommended) or **pip** | Latest | `pipx --version` |
| **Claude Code CLI** (`claude` on `PATH`) | Latest | `claude --version` |
| **Network access to GitHub** | - | Needed to install from the repository and to download codegraph |
| **Disk Space** | 50MB | `df -h` |

`superclaude install` exits 1 when `claude --version` fails: the codegraph
phase does not start without it.

</td>
<td align="center" width="50%">

### 💡 **Optional**

| Component | Purpose | Check Command |
|-----------|---------|---------------|
| **Node.js** | MCP Servers | `node --version` |
| **RAM** | Performance | 1GB recommended |

</td>
</tr>
</table>

</div>

<details>
<summary><b>🔍 Quick System Check</b></summary>

```bash
# Run this to check all requirements at once
python3 --version && echo "✅ Python OK" || echo "❌ Python missing"
git --version && echo "✅ Git OK" || echo "❌ Git missing"
pipx --version && echo "✅ pipx OK" || echo "⚠️ pipx missing (pip works too)"
claude --version && echo "✅ Claude Code OK" || echo "❌ Claude Code missing"
node --version 2>/dev/null && echo "✅ Node.js OK (optional)" || echo "⚠️ Node.js missing (optional)"
```

</details>

---

## 🚀 **Installation Methods**

<div align="center">

### **Detailed Installation Instructions**

</div>

### **Method 1: pipx (Recommended)**

<table>
<tr>
<td width="60%">

```bash
# Install pipx if not present. On systems that block pip installs
# (PEP 668 "externally-managed-environment"), use uv or the distro package
# instead of `python3 -m pip install --user pipx`:
uv tool install pipx          # or: sudo apt install pipx / brew install pipx
pipx ensurepath

# Install IronClaude from the fork (the PyPI "superclaude" package is upstream)
pipx install git+https://github.com/IronbellyOrg/IronClaude

# Run the installer
superclaude install
```

</td>
<td width="40%">

**✅ Advantages:**

- Isolated environment
- No dependency conflicts
- Clean uninstall
- Automatic PATH setup

**📍 Best for:**

- Linux/macOS users
- Clean system installs
- Multiple Python projects

</td>
</tr>
</table>

### **Method 2: pip (Traditional)**

<table>
<tr>
<td width="60%">

```bash
# Standard installation (from the fork, not PyPI).
# On PEP 668 systems ("externally-managed-environment") these pip commands
# fail outside a virtual environment: use Method 1 (pipx) instead, installing
# pipx with `uv tool install pipx` or the distro pipx package.
pip install git+https://github.com/IronbellyOrg/IronClaude

# Or user installation
pip install --user git+https://github.com/IronbellyOrg/IronClaude

# Run the installer
superclaude install
```

</td>
<td width="40%">

**✅ Advantages:**

- Familiar to Python users
- Direct installation

**📍 Best for:**

- Virtual environments
- Quick setup

**⚠️ Platforms:** Linux and macOS (x64 or arm64); see the platform note under Quick Installation.

</td>
</tr>
</table>

### **Method 3: Development Installation**

<table>
<tr>
<td width="60%">

```bash
# Clone repository
git clone https://github.com/IronbellyOrg/IronClaude
cd IronClaude

# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create the virtual environment that `make install` installs into
# (`make install` runs `uv pip install -e ".[dev]"`, which needs an environment)
uv venv

# Install in development mode (editable package + dev dependencies)
make install

# Copy commands, agents, skills, hooks and core files into ~/.claude/
uv run superclaude install

# Verify installation
make verify
```

From a source checkout, `superclaude` lives in `.venv`. Prefix it with `uv run`
(for example `uv run superclaude doctor`) or activate the environment with
`source .venv/bin/activate`.

</td>
<td width="40%">

**✅ Advantages:**

- Latest features
- Contribute to project
- Full source access
- Fast installation (uv)

**📍 Best for:**

- Contributors
- Custom modifications
- Testing new features

</td>
</tr>
</table>

---

## 🎛️ **Installation Options**

<div align="center">

### **Customize Your Installation**

| Option | Command | Description |
|--------|---------|-------------|
| `--target <dir>` | `superclaude install --target <dir>` | Where to install commands (default: `~/.claude/commands/sc`) |
| `--force` | `superclaude install --force` | Overwrite existing files |
| `--list` | `superclaude install --list` | List available and installed components |

</div>

---

## ✅ **Verification**

<div align="center">

### **Confirm Successful Installation**

</div>

### **Step 1: Check Installation**

```bash
# Verify the installed version (prints: SuperClaude, version 5.0.0)
superclaude --version

# List what is installed (read-only)
superclaude install --list

# Run the health check with details
superclaude doctor --verbose
```

Check that:

- `superclaude install --list` shows a `codegraph MCP` block whose
  `User registration:` line reads `matches` and whose last line reads
  `Ready for Serena retirement: yes`.
- `superclaude doctor --verbose` ends with `✅ SuperClaude is healthy` and prints
  no `no codegraph registration` line.

Use `--verbose`: plain `superclaude doctor` passes even when codegraph is not
registered, and only the verbose output shows that line.

### **Step 2: Test in Claude Code**

```bash
# Open Claude Code and try these commands:
/sc:brainstorm "test project"     # Should trigger discovery questions
/sc:analyze README.md              # Should provide structured analysis
@agent-security-engineer "review code"  # Should activate security specialist
```

### **Step 3: What's Installed**

<div align="center">

| Contents | Location |
|----------|----------|
| Core files, including the routing guide `HOW-WE-WORK.md` | `~/.claude/` |
| Slash commands | `~/.claude/commands/sc/` |
| Agents | `~/.claude/agents/` |
| Skills | `~/.claude/skills/` |
| Hooks | `~/.claude/hooks/` |
| Document and workflow templates | `~/.claude/templates/` |
| Rules (read on demand, excluded from auto-loading) | `~/.claude/rules/` |
| Output styles | `~/.claude/output-styles/` |
| Hook registrations and settings defaults (only keys you have not set), merged into your settings; a backup `settings.json.bak.<timestamp>` is written first | `~/.claude/settings.json` |
| ccsession launchers (links into the `ccsession-tag` skill) | `~/.local/bin/ccsession`, `~/.local/bin/ccsession-orca` |
| ccsession settings file (created from the example only when missing) | `~/.claude/ccsession.env` |
| codegraph 1.6.2 (downloaded, SHA-256 verified) | `~/.codegraph/`, link `~/.local/bin/codegraph` |
| codegraph user-scope MCP registration | the `codegraph` entry under `mcpServers` in `~/.claude.json` |

</div>

`superclaude install` also installs the default Claude Code plugins listed in
its settings defaults (six plugins, including `playwright` and `frontend-design`)
with `claude plugin install <plugin> --scope user`, skipping any you disabled in
`enabledPlugins`. This step downloads over the network within a shared 30-second
budget (with the Orca skills step); a plugin that fails or runs out of time is
reported, and the step never makes `superclaude install` fail. Rerun
`superclaude install` to retry. When the Orca CLI is installed, the same step
asks it to install its own skills (`computer-use`, `orca-cli`, `orchestration`).

> **`CLAUDE_CONFIG_DIR`.** The installer always writes its files under
> `$HOME/.claude/`. If you set `CLAUDE_CONFIG_DIR`, it is used only to find
> `.claude.json` when reading MCP registrations. An empty
> `CLAUDE_CONFIG_DIR` makes that lookup fail, so the codegraph phase stops and
> `superclaude install` exits 1.

---

## codegraph

codegraph is a code-graph MCP server (symbols, callers, impact, file outlines).
Installing it is a required phase of every `superclaude install`, with or
without `--force`:

- It reuses a `codegraph` that prints `1.6.2` (on `PATH` or in `~/.local/bin`);
  otherwise it downloads the pinned v1.6.2 release for your platform from
  GitHub, checks its SHA-256 and extracts it under `~/.codegraph/`.
- It registers codegraph as a user-scope MCP server in `~/.claude.json`.
- It needs the `claude` CLI and, for the download, network access. If the
  phase fails, everything else is still installed, the failed stage is
  printed and `superclaude install` exits 1. Fix the cause and run it again.
- A cleanup step then runs. It removes old `serena` and `codebase-memory-mcp`
  user registrations that IronClaude can prove it wrote and, once codegraph is
  ready, other uncustomised Serena launchers (any name except `serena-local`).
  It prints `<name>: kept: <reason>` for a `serena` or `codebase-memory-mcp`
  entry it keeps; see [Upgrading](upgrading.md#what-stays-on-purpose) for the
  removal commands.

Restart Claude Code afterwards: MCP servers load at session start. For the
failure table, indexing, removal and the Serena cleanup, see the
[MCP Installation Guide](../user-guide/mcp-installation.md).

---

## 🛠️ **Management**

<div align="center">

<table>
<tr>
<th>📦 Update</th>
<th>🗑️ Uninstall</th>
</tr>
<tr>
<td>

```bash
# Update to latest (pipx). --force reinstalls from the repository:
# `pipx upgrade` skips the reinstall while the version number is unchanged
pipx install --force git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force

# Update to latest (pip). --force-reinstall for the same reason
pip install --force-reinstall git+https://github.com/IronbellyOrg/IronClaude
superclaude install --force
```

</td>
<td>

```bash
# Uninstall package (pipx)
pipx uninstall superclaude

# Uninstall package (pip)
pip uninstall superclaude
```

</td>
</tr>
</table>

</div>

There is no `superclaude uninstall` command. Uninstalling the package removes only the Python package and the `superclaude` command. Everything `superclaude install` copied into your home folder stays where it is:

- core files such as `~/.claude/CLAUDE.md`, `~/.claude/RULES.md` and `~/.claude/HOW-WE-WORK.md`
- `~/.claude/commands/sc/`, `~/.claude/agents/`, `~/.claude/skills/`, `~/.claude/hooks/` and `~/.claude/templates/`
- `~/.claude/rules/` and `~/.claude/output-styles/`
- the `~/.local/bin/ccsession` and `~/.local/bin/ccsession-orca` links and `~/.claude/ccsession.env`
- the hook entries and settings defaults merged into `~/.claude/settings.json` (a backup named `settings.json.bak.<timestamp>` is written before the hook merge)
- codegraph: its user-scope registration and the files `superclaude install --list` prints as owned (under `~/.codegraph/`, plus the `~/.local/bin/codegraph` link)

Remove those by hand if you want them gone. Run `superclaude install --list` before uninstalling to see which core files, commands, agents, skills and templates are installed, and which codegraph paths are owned. To remove codegraph, run:

```bash
claude mcp remove codegraph --scope user
```

then delete the owned paths `superclaude install --list` printed; see [Removing codegraph](../user-guide/mcp-installation.md#removing-codegraph).

A plain `superclaude install` keeps framework files you already have (it still runs the codegraph phase and the cleanup step); run `superclaude install --force` to refresh them, for example to get the new `~/.claude/CLAUDE.md` and the latest `~/.claude/HOW-WE-WORK.md`. Unlike `superclaude update`, it also installs codegraph and retires old MCP registrations.

> **Warning:** `superclaude install --force` overwrites every file it ships, the same files `superclaude update` overwrites, including `~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, and keeps no backup of them. It also deletes and re-copies each shipped skill folder in `~/.claude/skills/`, so any file you added inside one is lost. If you edited or added any of these files, copy them first (for example `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`), then re-apply your changes after the upgrade. After refreshing the files it also runs the codegraph phase and the cleanup step; if the codegraph phase fails, the command exits 1 even though the files were already refreshed. Fix the cause and run it again.

---

## 🔧 **Troubleshooting**

<details>
<summary><b>❌ PEP 668 Error (Python Package Management)</b></summary>

This error occurs on systems with externally managed Python environments.

**Solutions (in order of preference):**

```bash
# Option 1: Use pipx (Recommended)
pipx install git+https://github.com/IronbellyOrg/IronClaude

# Option 2: User installation
pip install --user git+https://github.com/IronbellyOrg/IronClaude

# Option 3: Virtual environment
python3 -m venv superclaude-env
source superclaude-env/bin/activate  # Linux/macOS
# or
superclaude-env\Scripts\activate  # Windows
pip install git+https://github.com/IronbellyOrg/IronClaude

# Option 4: Force (use with caution)
pip install --break-system-packages git+https://github.com/IronbellyOrg/IronClaude
```

</details>

<details>
<summary><b>❌ Command Not Found</b></summary>

If the `superclaude` command is not found after installation:

```bash
# Check if package is installed
python3 -m pip show superclaude

# Run the installer
superclaude install

# Add to PATH (if using --user)
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc  # Linux
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc   # macOS
```

</details>

<details>
<summary><b>❌ Claude Code Not Found</b></summary>

If Claude Code is not installed or not in PATH:

1. Download from [https://claude.ai/code](https://claude.ai/code)
2. Install following platform instructions
3. Verify with: `claude --version`
4. Restart terminal after installation

</details>

<details>
<summary><b>❌ Permission Denied</b></summary>

For permission errors during installation:

```bash
# Use user installation
pip install --user git+https://github.com/IronbellyOrg/IronClaude

# Or use sudo (not recommended)
sudo pip install git+https://github.com/IronbellyOrg/IronClaude

# Better: use pipx
pipx install git+https://github.com/IronbellyOrg/IronClaude
```

</details>

<details>
<summary><b>❌ Missing Python or pip</b></summary>

**Linux (Ubuntu/Debian):**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**macOS:**

```bash
# Install Homebrew first if needed
brew install python3
```

**Windows:**

- Download from [python.org](https://python.org)
- Check "Add Python to PATH" during installation
- Restart terminal after installation

</details>

---

## 📚 **Next Steps**

<div align="center">

### **Your Learning Journey**

<table>
<tr>
<th>🌱 Start Here</th>
<th>🌿 Expand Skills</th>
<th>🌲 Master Framework</th>
</tr>
<tr>
<td valign="top">

**First Week:**

- [Quick Start Guide](quick-start.md)
- [Commands Reference](../user-guide/commands.md)
- Try `/sc:brainstorm`

</td>
<td valign="top">

**Week 2-3:**

- [Behavioral Modes](../user-guide/modes.md)
- [Agents Guide](../user-guide/agents.md)
- [How We Work](../user-guide/how-we-work.md)

</td>
<td valign="top">

**Advanced:**

- [MCP Servers](../user-guide/mcp-servers.md)
- [Context Freshness Hooks](../user-guide/freshness-hooks.md) (v4.3+)
- [Technical Architecture](../developer-guide/technical-architecture.md)
- [Contributing Code](../developer-guide/contributing-code.md)

</td>
</tr>
</table>

</div>

---

<div align="center">

### **🎉 Installation Complete!**

You now have access to:

<p align="center">
  <b>Commands</b> • <b>AI Agents</b> • <b>Skills</b> • <b>MCP Integrations</b>
</p>

**Ready to start?** Try `/sc:brainstorm` in Claude Code for your first SuperClaude experience!

<p align="center">
  <a href="quick-start.md">
    <img src="https://img.shields.io/badge/📖_Continue_to-Quick_Start_Guide-blue?style=for-the-badge" alt="Quick Start">
  </a>
</p>

</div>
