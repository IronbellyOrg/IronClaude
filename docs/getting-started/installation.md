<div align="center">

# 📦 SuperClaude Installation Guide

### **Transform Claude Code with commands, agents, skills, and MCP integrations**

<p align="center">
  <img src="https://img.shields.io/badge/version-4.3.5-blue?style=for-the-badge" alt="Version">
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
| **📦 pip** | `pip install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` | All | Traditional Python setups |
| **🔧 Dev** | `git clone ... && uv venv && make install && uv run superclaude install` | All | Contributors & developers |

</div>

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

Existing installations receive refreshed core files and hook registrations with:

```bash
superclaude update
```

The update preserves unrelated user hook registrations, refreshes
framework-owned hooks by command identity, and makes SubagentStart policy
injection synchronous. Start a new Claude Code session after installing or
updating; an already-running session does not reload its initial instructions.
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
| **pip** | Latest | `pip --version` |
| **Claude Code** | Latest | `claude --version` |
| **Disk Space** | 50MB | `df -h` |

</td>
<td align="center" width="50%">

### 💡 **Optional**

| Component | Purpose | Check Command |
|-----------|---------|---------------|
| **Node.js** | MCP Servers | `node --version` |
| **Git** | Version Control | `git --version` |
| **pipx** | Isolated Install | `pipx --version` |
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
claude --version && echo "✅ Claude Code OK" || echo "❌ Claude Code missing"
node --version 2>/dev/null && echo "✅ Node.js OK (optional)" || echo "⚠️ Node.js missing (optional)"
git --version 2>/dev/null && echo "✅ Git OK (optional)" || echo "⚠️ Git missing (optional)"
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
# Install pipx if not present
python3 -m pip install --user pipx
python3 -m pipx ensurepath

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
# Standard installation (from the fork, not PyPI)
pip install git+https://github.com/IronbellyOrg/IronClaude

# Or user installation
pip install --user git+https://github.com/IronbellyOrg/IronClaude

# Run the installer
superclaude install
```

</td>
<td width="40%">

**✅ Advantages:**

- Works everywhere
- Familiar to Python users
- Direct installation

**📍 Best for:**

- Windows users
- Virtual environments
- Quick setup

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
# Verify the installed version
superclaude --version

# Run the health check
superclaude doctor
```

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

</div>

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
superclaude update

# Update to latest (pip). --force-reinstall for the same reason
pip install --force-reinstall git+https://github.com/IronbellyOrg/IronClaude
superclaude update
```

</td>
<td>

```bash
# Uninstall package (pipx)
pipx uninstall superclaude

# Uninstall package (pip)
pip uninstall superclaude

# Remove the old Claude Code plugin install
make uninstall-legacy
```

</td>
</tr>
</table>

</div>

There is no `superclaude uninstall` command. Uninstalling the package removes only the Python package and the `superclaude` command. Everything `superclaude install` copied into your home folder stays where it is:

- core files such as `~/.claude/CLAUDE.md`, `~/.claude/RULES.md` and `~/.claude/HOW-WE-WORK.md`
- `~/.claude/commands/sc/`, `~/.claude/agents/`, `~/.claude/skills/`, `~/.claude/hooks/` and `~/.claude/templates/`
- `~/.claude/rules/` and `~/.claude/output-styles/`
- the `~/.local/bin/ccsession` link and `~/.claude/ccsession.env`
- the hook entries and settings defaults merged into `~/.claude/settings.json` (a backup named `settings.json.bak.<timestamp>` is written before the hook merge)

Remove those by hand if you want them gone. Run `superclaude install --list` before uninstalling to see which core files, commands, agents, skills and templates are installed.

`make uninstall-legacy` (run from a repository checkout) runs `scripts/uninstall_legacy.sh`. It removes only the old Claude Code plugin install: `~/.claude/plugins/superclaude@superclaude`, `~/.claude/superclaude.json`, `~/.claude/superclaude_config.json`, and the `superclaude@superclaude` entry in `enabledPlugins` in `~/.claude/settings.json`. It backs these up to `~/.claude-superclaude-backup-<timestamp>` first. It does not remove anything `superclaude install` put in `~/.claude/`.

A plain `superclaude install` never replaces files you already have; run `superclaude update` to get the new `~/.claude/CLAUDE.md` and the latest `~/.claude/HOW-WE-WORK.md`.

> **Warning:** `superclaude update` overwrites every file it ships, including `~/.claude/CLAUDE.md` and `~/.claude/RULES.md`, and keeps no backup of them. It also deletes and re-copies each shipped skill folder in `~/.claude/skills/`, so any file you added inside one is lost. `superclaude install --force` does the same. If you edited or added any of these files, copy them first (for example `cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`), then re-apply your changes after the update.

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
