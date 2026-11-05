# SuperClaude Verification and Troubleshooting Guide

## Overview

This guide covers how to verify your SuperClaude installation and troubleshoot common issues with context files and configurations.

**Important**: SuperClaude installs context files (commands, agents, skills, core files) into `~/.claude/`, and it also ships the `superclaude` Python CLI, which has executable pipelines (`sprint`, `roadmap`, `reflect`, `swarm`, `eval` and more) and a pytest suite. This guide focuses on verifying the installed files and the codegraph MCP registration; see [Running the test suite](#running-the-test-suite) for the code tests.

## Table of Contents

1. [Installation Verification](#installation-verification)
2. [Context File Verification](#context-file-verification)
3. [MCP Server Verification](#mcp-server-verification)
4. [Common Issues](#common-issues)
5. [Troubleshooting Commands](#troubleshooting-commands)

## Installation Verification

### Check Installation Status

```bash
# Verify the superclaude CLI is available (from a source checkout: uv run superclaude --version)
superclaude --version
# Expected: SuperClaude, version <x.y.z>

# Verify Claude Code CLI integration
claude --version
# Expected: Claude Code version info

# Check if context files were installed
ls ~/.claude/
# Expected: CLAUDE.md, HOW-WE-WORK.md, RULES.md, PRINCIPLES.md, agents/, commands/, skills/

# Verify main context file
head ~/.claude/CLAUDE.md
# Expected: Should show import statements
```

### Verify Directory Structure

```bash
# Check all directories exist
for dir in agents commands/sc skills; do
    if [ -d ~/.claude/$dir ]; then
        echo "✅ $dir directory exists"
        ls ~/.claude/$dir | wc -l
    else
        echo "❌ $dir directory missing"
    fi
done
```

### Count Installed Components

```bash
# Compare what is available with what is installed (counts change between releases,
# so do not check against a fixed number)
superclaude install --list
# Each section ends with "<N> available, <M> installed". Every shipped item should show
# "✅ installed"; M can be higher than N if you have your own or Orca's skills or agents,
# so installed is at least the available set, not necessarily equal to it

# Health check (exits non-zero if any check fails)
superclaude doctor --verbose

# Raw counts, if you want them (commands install to ~/.claude/commands/sc/)
ls ~/.claude/agents/*.md | wc -l
ls ~/.claude/commands/sc/*.md | wc -l
ls -d ~/.claude/skills/*/ | wc -l
```

## Context File Verification

### Verify Core Files

```bash
# Check core context files exist
for file in CLAUDE.md HOW-WE-WORK.md RULES.md PRINCIPLES.md; do
    if [ -f ~/.claude/$file ]; then
        echo "✅ $file exists ($(wc -l < ~/.claude/$file) lines)"
    else
        echo "❌ $file missing"
    fi
done
```

### Verify Import System

```bash
# CLAUDE.md imports exactly one file
grep '^@' ~/.claude/CLAUDE.md
# Expected output:
# @BASH_INSPECTION_POLICY.md
```

### Check File Integrity

```bash
# Verify files are readable text files
file ~/.claude/CLAUDE.md
# Expected: ASCII text or UTF-8 text

# Check for corruption
for file in ~/.claude/**/*.md; do
    if file "$file" | grep -q "text"; then
        echo "✅ $file is valid text"
    else
        echo "❌ $file may be corrupted"
    fi
done
```

## MCP Server Verification

### Check MCP Configuration

```bash
# Verify .claude.json exists
if [ -f ~/.claude.json ]; then
    echo "✅ MCP configuration file exists"
    # Check which servers are configured
    grep -o '"[^"]*":' ~/.claude.json | grep -v mcpServers
else
    echo "❌ No MCP configuration found"
fi
```

### Verify the codegraph MCP Registration

`superclaude install` downloads the pinned codegraph binary and registers it as a user-scope MCP server. Two read-only commands show its state:

```bash
# The codegraph block comes just before the "Retired MCP registrations (user scope)" block
# (no download, no claude mcp call)
superclaude install --list
# Expected, near the end:
# codegraph MCP (pinned v1.6.2; user scope):
#    Executable: <your home>/.codegraph/versions/v1.6.2/bin/codegraph (1.6.2)
#    Owner: owned (receipt) ...
#    User registration: matches
#    Ready for Serena retirement: yes

# The health check includes a codegraph check
superclaude doctor --verbose
# Expected lines:
# ✅ codegraph MCP registration
#     Ready for Serena retirement: yes
```

If `User registration` shows `absent` or `owned but stale`, or the doctor check fails because the registered command is not an executable while `User registration` is not `user-managed`, run `superclaude install --force` and check again.

`user-managed` means the `codegraph` entry was registered by you, not by IronClaude. The installer never replaces it: it keeps a working entry as it is, and it refuses an entry whose command does not run. To let IronClaude manage it, or to repair an entry whose command does not run, remove it with `claude mcp remove codegraph --scope user` and run `superclaude install` again.

### Test MCP Server Availability

```bash
# Check if Node.js is available (required for MCP)
node --version
# Expected: v18.0.0 or higher (superclaude mcp requires Node.js 18+ for npm-based servers)

# Check if npx is available
npx --version
# Expected: Version number

# Test Context7 MCP (if configured)
npx -y @upstash/context7-mcp@latest --help 2>/dev/null && echo "✅ Context7 available" || echo "❌ Context7 not available"
```

## Common Issues

### Issue: Commands Not Working

**Symptom**: `/sc:` context triggers don't produce expected Claude Code behavior

**Verification**:

```bash
# Check if command file exists (commands install to ~/.claude/commands/sc/)
ls ~/.claude/commands/sc/implement.md
# If missing, reinstall SuperClaude

# Verify file content
head -20 ~/.claude/commands/sc/implement.md
# Should show command metadata and instructions
```

**Solution**:

```bash
# Reinstall (install has no per-component option; --force overwrites existing files)
superclaude install --force
```

### Issue: Agents Not Activating

**Symptom**: `@agent-` invocations don't work in Claude Code

**Verification**:

```bash
# List all agents
ls ~/.claude/agents/

# Check specific agent
cat ~/.claude/agents/python-expert.md | head -20
```

**Solution**:

```bash
# Reinstall (install has no per-component option; --force overwrites existing files)
superclaude install --force
```

### Issue: Context Not Loading

**Symptom**: Claude Code doesn't seem to read SuperClaude context

**Verification**:

```bash
# Check CLAUDE.md is in correct location
ls -la ~/.claude/CLAUDE.md

# Verify Claude Code can access the directory
# In Claude Code, check if context is loading properly
```

**Solution**:

1. Restart Claude Code
2. Ensure you're in a project directory
3. Check file permissions: `chmod 644 ~/.claude/*.md`

### Issue: MCP Servers Not Working

**Symptom**: MCP features unavailable

**Verification**:

```bash
# Check Node.js installation
which node

# Verify .claude.json syntax
python3 -c "import json; json.load(open('$HOME/.claude.json'))" && echo "✅ Valid JSON" || echo "❌ Invalid JSON"
```

**Solution**:

```bash
# Install Node.js if missing
# Ubuntu: sudo apt install nodejs npm
# macOS: brew install node
# Windows: Download from nodejs.org

# Fix JSON syntax if invalid, then re-add the MCP servers you need
superclaude mcp --list
superclaude mcp --servers <name>
```

## Troubleshooting Commands

### Quick Diagnostic

```bash
#!/bin/bash
# SuperClaude Quick Diagnostic Script

echo "=== SuperClaude Diagnostic ==="
echo ""

# Check installation system
echo "1. Installation System:"
if command -v superclaude &> /dev/null; then
    echo "   ✅ superclaude CLI available"
    superclaude --version
else
    echo "   ❌ superclaude not found - install IronClaude with: pipx install git+https://github.com/IronbellyOrg/IronClaude"
    echo "      (or pip install git+https://github.com/IronbellyOrg/IronClaude; the PyPI 'superclaude' package is upstream)"
fi

# Check context files
echo ""
echo "2. Context Files:"
if [ -d ~/.claude ]; then
    echo "   ✅ ~/.claude directory exists"
    echo "   - Agents: $(ls ~/.claude/agents/*.md 2>/dev/null | wc -l)"
    echo "   - Commands: $(ls ~/.claude/commands/sc/*.md 2>/dev/null | wc -l)"
    echo "   - Skills: $(ls -d ~/.claude/skills/*/ 2>/dev/null | wc -l)"
else
    echo "   ❌ ~/.claude directory not found"
fi

# Check MCP
echo ""
echo "3. MCP Configuration:"
if [ -f ~/.claude.json ]; then
    echo "   ✅ MCP configuration exists"
else
    echo "   ❌ No MCP configuration"
fi

# Check Node.js
echo ""
echo "4. Node.js (for MCP):"
if command -v node &> /dev/null; then
    echo "   ✅ Node.js installed: $(node --version)"
else
    echo "   ⚠️  Node.js not installed (optional, needed for MCP)"
fi

echo ""
echo "=== Diagnostic Complete ==="
```

### File Permission Fix

```bash
# Fix permissions on all context files
chmod 644 ~/.claude/*.md
chmod 644 ~/.claude/**/*.md
chmod 755 ~/.claude ~/.claude/agents ~/.claude/commands ~/.claude/commands/sc ~/.claude/skills
```

### Complete Reinstall

```bash
# Backup existing configuration
cp -r ~/.claude ~/.claude.backup.$(date +%Y%m%d)

# Reinstall everything, overwriting the installed files
superclaude install --force

# Restore any customizations from backup if needed
```

Do not delete `~/.claude/`: it also holds your Claude Code settings, project memory and session history, which `superclaude install` does not recreate.

## Important Notes

### Running the Test Suite

The context files themselves do not execute, but the repository has a pytest suite for the `superclaude` CLI, its pipelines, hooks and skill structure. From a source checkout:

```bash
make test                      # runs uv run pytest
uv run pytest tests/sprint/ -v # one area
make verify-sync               # src/superclaude/ and .claude/ are in sync
```

### What This Guide Verifies

- **File Presence**: Context files exist in correct locations
- **File Integrity**: Files are valid text and readable
- **Directory Structure**: Proper organization maintained
- **Configuration Validity**: JSON files are syntactically correct
- **Dependencies Available**: Node.js for MCP servers (optional)
- **Behavioral Testing**: Context files produce expected Claude Code behavior

## Summary

Installation verification for SuperClaude focuses on ensuring context files are properly installed and accessible to Claude Code and that the codegraph MCP registration is ready (`superclaude install --list`, `superclaude doctor --verbose`). The `superclaude` CLI code is covered by the pytest suite (`make test`).
