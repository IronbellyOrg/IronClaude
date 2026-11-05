# SuperClaude Diagnostic Reference Guide

## Overview

This guide provides procedures for diagnosing issues with SuperClaude context files and configurations. Most of SuperClaude is text files that Claude Code reads, so these diagnostics focus on file verification and configuration checking.

**Important**: SuperClaude is not only text files. Its hooks run as processes on Claude Code events, the codegraph SessionStart hook (`~/.claude/hooks/codegraph-session-start.sh`) starts a background `codegraph init` for the project, and the `superclaude` CLI pipelines (sprint, roadmap, tasklist, and others) start `claude` subprocesses that call the model API over the network. This guide does not cover monitoring those processes; it checks that the installed files are present and valid.

## Quick Diagnostics

### One-Line Health Check

```bash
# Quick status check
ls ~/.claude/CLAUDE.md && echo "✅ SuperClaude installed" || echo "❌ Not installed"
```

### Basic Diagnostic Commands

```bash
# Check if SuperClaude is installed
superclaude --version

# Count context files
superclaude install --list
# Expected: every available component is also listed as installed

# Check file sizes (context files should have content)
find ~/.claude -name "*.md" -type f -size 0
# Expected: No output (no empty files)

# Verify directory structure
tree -L 2 ~/.claude/
# Or without tree command:
ls -la ~/.claude/
```

## File System Diagnostics

### Context File Verification

```bash
#!/bin/bash
# Comprehensive context file check

echo "=== SuperClaude Context File Diagnostic ==="

# Count installed files (slash commands install to ~/.claude/commands/sc/;
# mode files are not installed, so there is no modes directory to count)
ACTUAL_AGENTS=$(ls ~/.claude/agents/*.md 2>/dev/null | wc -l)
ACTUAL_COMMANDS=$(ls ~/.claude/commands/sc/*.md 2>/dev/null | wc -l)
echo "Agents installed: $ACTUAL_AGENTS"
echo "Commands installed: $ACTUAL_COMMANDS"

# Compare against what this release ships (no fixed totals: the
# shipped set changes between releases). Every shipped item should
# show "✅ installed"; installed counts can be higher than available
# if you have your own or Orca's agents or skills.
superclaude install --list
superclaude doctor

# Check core files
for file in CLAUDE.md HOW-WE-WORK.md RULES.md PRINCIPLES.md; do
    if [ -f ~/.claude/$file ]; then
        SIZE=$(wc -c < ~/.claude/$file)
        echo "$file: $SIZE bytes ✅"
    else
        echo "$file: MISSING ❌"
    fi
done
```

### Import System Check

```bash
# Verify import statements in CLAUDE.md
echo "=== Import System Check ==="
if [ -f ~/.claude/CLAUDE.md ]; then
    echo "Imports found in CLAUDE.md:"
    grep '^@' ~/.claude/CLAUDE.md

    # The installed CLAUDE.md has exactly one import line:
    # @BASH_INSPECTION_POLICY.md
    IMPORT_COUNT=$(grep -c '^@' ~/.claude/CLAUDE.md)
    echo "Total imports: $IMPORT_COUNT"

    if [ "$IMPORT_COUNT" -eq 1 ] && grep -qx '@BASH_INSPECTION_POLICY.md' ~/.claude/CLAUDE.md; then
        echo "✅ Import system configured correctly"
    else
        echo "⚠️ Expected exactly one import line: @BASH_INSPECTION_POLICY.md"
    fi
else
    echo "❌ CLAUDE.md not found"
fi
```

## Configuration Diagnostics

### MCP Server Configuration Check

```bash
# Check MCP configuration
echo "=== MCP Configuration Diagnostic ==="

CONFIG_FILE=~/.claude.json

if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Configuration file exists"
    
    # Validate JSON syntax
    if python3 -c "import json; json.load(open('$CONFIG_FILE'))" 2>/dev/null; then
        echo "✅ Valid JSON syntax"
        
        # List configured servers
        echo "Configured MCP servers:"
        python3 -c "
import json
with open('$HOME/.claude.json') as f:
    config = json.load(f)
    if 'mcpServers' in config:
        for server in config['mcpServers']:
            print(f'  - {server}')
    else:
        print('  No servers configured')
        "
    else
        echo "❌ Invalid JSON syntax in $CONFIG_FILE"
    fi
else
    echo "⚠️ No MCP configuration file found"
    echo "  This is OK if you don't use MCP servers"
fi
```

### Permission Diagnostics

```bash
# Check file permissions
echo "=== File Permission Check ==="

# Check if files are readable
UNREADABLE_COUNT=0
for file in ~/.claude/**/*.md; do
    if [ ! -r "$file" ]; then
        echo "❌ Cannot read: $file"
        ((UNREADABLE_COUNT++))
    fi
done

if [ $UNREADABLE_COUNT -eq 0 ]; then
    echo "✅ All context files are readable"
else
    echo "⚠️ Found $UNREADABLE_COUNT unreadable files"
    echo "Fix with: chmod 644 ~/.claude/**/*.md"
fi

# Check directory permissions
for dir in ~/.claude ~/.claude/agents ~/.claude/commands/sc ~/.claude/skills; do
    if [ -d "$dir" ]; then
        if [ -x "$dir" ]; then
            echo "✅ $dir is accessible"
        else
            echo "❌ $dir is not accessible"
        fi
    else
        echo "❌ $dir does not exist"
    fi
done
```

## Common Issue Diagnostics

### Issue: Commands Not Recognized

```bash
# Diagnose command issues
COMMAND="implement"  # Change to test different commands

echo "=== Diagnosing command: $COMMAND ==="

FILE=~/.claude/commands/sc/$COMMAND.md

if [ -f "$FILE" ]; then
    echo "✅ Command file exists"
    
    # Check file size
    SIZE=$(wc -c < "$FILE")
    if [ $SIZE -gt 100 ]; then
        echo "✅ File has content ($SIZE bytes)"
    else
        echo "⚠️ File seems too small ($SIZE bytes)"
    fi
    
    # Check for metadata
    if head -10 "$FILE" | grep -q "^---"; then
        echo "✅ Has metadata header"
    else
        echo "⚠️ Missing metadata header"
    fi
    
    # Check for command pattern
    if grep -q "/sc:$COMMAND" "$FILE"; then
        echo "✅ Contains command pattern"
    else
        echo "⚠️ Missing command pattern"
    fi
else
    echo "❌ Command file not found: $FILE"
    echo "Available commands:"
    ls ~/.claude/commands/sc/ | sed 's/.md$//'
fi
```

### Issue: Agent Not Activating

```bash
# Diagnose agent issues
AGENT="python-expert"  # Change to test different agents

echo "=== Diagnosing agent: $AGENT ==="

FILE=~/.claude/agents/$AGENT.md

if [ -f "$FILE" ]; then
    echo "✅ Agent file exists"
    
    # Check for trigger keywords
    echo "Trigger keywords found:"
    grep -A 5 "## Triggers" "$FILE" | tail -n +2
    
    # Check for metadata
    if head -10 "$FILE" | grep -q "^name:"; then
        echo "✅ Has metadata"
    else
        echo "⚠️ Missing metadata"
    fi
else
    echo "❌ Agent file not found: $FILE"
    echo "Available agents:"
    ls ~/.claude/agents/ | sed 's/.md$//'
fi
```

## Installation Repair

### Quick Fix Script

```bash
#!/bin/bash
# SuperClaude Quick Fix Script

echo "=== SuperClaude Quick Fix ==="

# Check for common issues and fix them
ISSUES_FOUND=0

# Fix permissions
echo "Fixing file permissions..."
chmod 644 ~/.claude/*.md 2>/dev/null
chmod 644 ~/.claude/**/*.md 2>/dev/null
chmod 755 ~/.claude ~/.claude/agents ~/.claude/commands ~/.claude/commands/sc ~/.claude/skills 2>/dev/null

# Check for missing directories (superclaude install has no per-component flag;
# a plain install adds missing files and never replaces existing ones)
for dir in agents commands/sc skills hooks; do
    if [ ! -d ~/.claude/$dir ]; then
        echo "⚠️ Missing directory: $dir"
        echo "  Run: superclaude install   (then: superclaude doctor)"
        ((ISSUES_FOUND++))
    fi
done

# Check for empty files
EMPTY_FILES=$(find ~/.claude -name "*.md" -type f -size 0 2>/dev/null)
if [ -n "$EMPTY_FILES" ]; then
    echo "⚠️ Found empty files:"
    echo "$EMPTY_FILES"
    echo "  Run: superclaude install --force"
    ((ISSUES_FOUND++))
fi

if [ $ISSUES_FOUND -eq 0 ]; then
    echo "✅ No issues found"
else
    echo "Found $ISSUES_FOUND issues - see recommendations above"
fi
```

### Complete Reinstallation

**Warning**: never delete `~/.claude` to reinstall SuperClaude. That directory also holds Claude Code's own settings (`settings.json`), your session transcripts (`projects/`) and files written by other tools. Reinstall over the existing files instead:

```bash
# Reinstall every SuperClaude file over the existing installation
echo "=== Forced Reinstall ==="

superclaude install --force

# Verify installation
superclaude install --list
superclaude doctor
```

Restart any open Claude Code sessions afterwards so they load the reinstalled files.

## What These Diagnostics DON'T Do

### Not Applicable Concepts

These diagnostics check installed files only. They do not monitor the parts of SuperClaude that do run:

- **Hooks**: shell and Node scripts that Claude Code runs on session start and end, prompt submit, file reads and edits, and subagent start and stop
- **Codegraph**: the SessionStart hook starts a detached background `codegraph init` that indexes the project
- **CLI pipelines**: `superclaude sprint`, `superclaude roadmap` and the other pipeline commands start `claude` subprocesses, which call the model API over the network
- **MCP servers**: run as separate processes and may use the network

### Focus on What Matters

- **File Presence**: Are context files installed?
- **File Integrity**: Are files readable and complete?
- **Configuration Validity**: Is JSON syntax correct?
- **Directory Structure**: Is organization correct?
- **Permissions**: Can Claude Code read the files?

## Summary

These diagnostics are simple: verify files exist, check they're readable, and ensure configurations are valid. If a problem persists with every file present and readable, look at the running parts listed above: the hooks, the codegraph index (`/sc:graph`), and the CLI pipeline logs.
