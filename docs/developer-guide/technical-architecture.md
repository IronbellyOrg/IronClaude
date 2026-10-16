# SuperClaude Context Architecture Guide

## Overview

This guide documents how SuperClaude's Context-Oriented Configuration Framework is structured and how Claude Code interprets these context files to modify its behavior.

**Important**: SuperClaude is NOT standalone software with running processes, execution layers, or performance systems. It is a collection of `.md` instruction files that Claude Code reads to adopt specialized behaviors.

## Table of Contents

1. [Context File Architecture](#context-file-architecture)
2. [The Import System](#the-import-system)
3. [Agent Context Structure](#agent-context-structure)
4. [Command Context Structure](#command-context-structure)
5. [Mode Context Structure](#mode-context-structure)
6. [MCP Server Configuration](#mcp-server-configuration)
7. [How Claude Code Reads Context](#how-claude-code-reads-context)
8. [Extending the Framework](#extending-the-framework)

## Context File Architecture

### Directory Structure

```
~/.claude/ (SuperClaude Framework Files Only)
├── CLAUDE.md                       # Always loaded; imports BASH_INSPECTION_POLICY.md
├── BASH_INSPECTION_POLICY.md       # Bash inspection rules, imported by CLAUDE.md
├── HOW-WE-WORK.md                  # Routing guide, read on demand, never imported
├── RULES.md                        # Behavioral rules, read by skills
├── PRINCIPLES.md                   # Engineering principles, read by skills
├── RESEARCH_CONFIG.md              # Deep-research configuration
├── BUSINESS_SYMBOLS.md             # Business-panel symbols
├── BUSINESS_PANEL_EXAMPLES.md      # Business-panel examples
├── agents/                         # Domain specialist contexts (19 total)
│   ├── backend-architect.md        # Backend expertise
│   ├── business-panel-experts.md   # Business strategy panel
│   ├── deep-research-agent.md      # Deep research expertise
│   ├── devops-architect.md         # DevOps expertise
│   ├── frontend-architect.md       # Frontend expertise
│   ├── learning-guide.md           # Educational expertise
│   ├── performance-engineer.md     # Performance expertise
│   ├── python-expert.md            # Python expertise
│   ├── quality-engineer.md         # Quality assurance expertise
│   ├── refactoring-expert.md       # Code quality expertise
│   ├── requirements-analyst.md     # Requirements expertise
│   ├── root-cause-analyst.md       # Problem diagnosis expertise
│   ├── security-engineer.md        # Security expertise
│   ├── socratic-mentor.md          # Educational expertise
│   ├── spec-panel-experts.md       # Specification review panel
│   ├── system-architect.md         # System design expertise
│   ├── technical-writer.md         # Documentation expertise
│   ├── test-runner.md              # Test execution expertise
│   └── wave-orchestrator.md        # Wave orchestration patterns
├── hooks/                          # Shell hooks deposited by install_hooks (v4.3+)
│   ├── session-init.sh             # Pre-existing init script (legacy)
│   ├── freshness-session-start.sh  # SessionStart envelope (startup + resume branches)
│   ├── freshness-user-prompt.sh    # Per-turn <session-context> envelope injection
│   ├── freshness-pre-edit.sh       # PreToolUse gate: blocks Edit/Write against unread/stale files
│   ├── freshness-post-read.sh      # PostToolUse(Read) tracker
│   ├── freshness-subagent-start.sh # Background-agent counter increment
│   ├── freshness-subagent-stop.sh  # Background-agent counter decrement
│   └── freshness-file-changed.sh   # NOT REGISTERED in v1 — see freshness-hooks.md
├── state/                          # Per-session state populated by hooks
│   ├── reads.jsonl                 # Successful Read events (cross-session jsonl)
│   ├── turns/<sid>.txt             # Per-session turn counter
│   ├── last-prompt-ts/<sid>.txt    # Per-session last prompt timestamp
│   ├── bg-agents/<sid>.txt         # Per-session background-agent count
│   └── tool-call-counter/<sid>.txt # Per-session tool-call sequence
├── logs/                           # Hook telemetry
│   └── freshness-hook.jsonl        # PreToolUse decisions (one row per Edit attempt)
├── settings.json                   # Hook registrations merged by install_hooks
└── commands/                       # Workflow pattern contexts
    └── sc/                         # SuperClaude command namespace (25 total)
        ├── analyze.md              # Analysis patterns
        ├── brainstorm.md           # Discovery patterns
        ├── build.md                # Build patterns
        ├── business-panel.md       # Business expert panel patterns
        ├── cleanup.md              # Cleanup patterns
        ├── design.md               # Design patterns
        ├── document.md             # Documentation patterns
        ├── estimate.md             # Estimation patterns
        ├── explain.md              # Explanation patterns
        ├── git.md                  # Git workflow patterns
        ├── help.md                 # Help and command listing
        ├── implement.md            # Implementation patterns
        ├── improve.md              # Improvement patterns
        ├── index.md                # Index patterns
        ├── load.md                 # Context loading patterns
        ├── reflect.md              # Reflection patterns
        ├── research.md             # Deep research patterns
        ├── save.md                 # Session persistence patterns
        ├── select-tool.md          # Tool selection patterns
        ├── spawn.md                # Multi-agent patterns
        ├── spec-panel.md           # Specification review panel
        ├── task.md                 # Task management patterns
        ├── test.md                 # Testing patterns
        ├── troubleshoot.md         # Troubleshooting patterns
        └── workflow.md             # Workflow planning patterns

Note: Other directories (backups/, logs/, projects/, serena/, etc.) are Claude Code
operational directories, not part of SuperClaude framework content.
```

### Context File Types

| File Type | Purpose | Activation | Example |
|-----------|---------|------------|---------|
| **Commands** | Define workflow patterns | `/sc:[command]` (context trigger) | User types `/sc:implement` → reads `implement.md` |
| **Agents** | Provide domain expertise | `@agent-[name]`, a command or skill delegating, or Claude's choice by `description` | `@agent-security-engineer` → reads `security-engineer.md` |
| **Modes** | Modify interaction style | Not installed or loaded automatically; a mode flag such as `--brainstorm` is a hint Claude may honour | Mode files ship under `src/superclaude/modes/` and are not installed to `~/.claude/` |
| **Core** | Set fundamental rules | `CLAUDE.md` always loaded; the rest on demand | `CLAUDE.md` always loaded; `RULES.md`, `PRINCIPLES.md`, `HOW-WE-WORK.md` read on demand |

## The Import System

### How CLAUDE.md Works

The installed `CLAUDE.md` imports one file, `BASH_INSPECTION_POLICY.md`. Everything else (rules, principles, the routing guide `HOW-WE-WORK.md`) is read on demand by skills, commands, or people, so it costs no context until it is needed.

```markdown
# SuperClaude — Framework Context

@BASH_INSPECTION_POLICY.md
```

### Import Processing

1. Claude Code reads `CLAUDE.md`
2. Loads each `@<file>` line into context (there is one: `@BASH_INSPECTION_POLICY.md`)
3. Everything else (rules, principles, the routing guide, commands, agents, skills) is read on demand when a command, skill or person needs it

## Agent Context Structure

### Anatomy of an Agent File

Each agent `.md` file follows this structure:

```markdown
---
name: agent-name
description: Brief description
category: specialized|architecture|quality
---

# Agent Name

## Triggers
- When this agent is a good fit (guidance for whoever delegates to it;
  nothing matches these in code)

## Behavioral Mindset
Core philosophy and approach

## Focus Areas
- Domain expertise area 1
- Domain expertise area 2

## Key Actions
1. Specific behavior pattern
2. Problem-solving approach
```

### Agent Activation Logic

- **Manual**: User types `@agent-python-expert "task"`
- **Delegated**: A command or skill delegates to a named agent as one of its steps
- **Claude's choice**: Claude Code may delegate to an agent whose `description` fits the request. There is no keyword or file-type matching engine.

## Command Context Structure

### Anatomy of a Command File

```markdown
---
name: command-name
description: Command purpose
category: utility|orchestration|analysis
complexity: basic|enhanced|advanced
mcp-servers: [context7]
personas: [architect, engineer]
---

# /sc:command-name

## Triggers
- When to use this command
- Context indicators

## Usage
/sc:command-name [target] [--options]

## Workflow Pattern
1. Step 1: Initial action
2. Step 2: Processing
3. Step 3: Validation

## Examples
Practical usage examples
```

### Command Processing

When user types `/sc:implement "feature"` in Claude Code conversation:

1. Claude reads `commands/sc/implement.md`
2. Adopts implementation workflow pattern
3. Delegates to agents only where the command or its skill says to
4. Follows defined workflow steps

## Mode Context Structure

### Behavioral Modes

Modes modify Claude's interaction style. Mode files ship in the source tree under `src/superclaude/modes/` but are not installed to `~/.claude/` or loaded automatically: `CLAUDE.md` does not import them and no shipped command or skill reads them. A mode flag such as `--brainstorm` is a hint Claude may honour. The flag and keyword triggers listed inside a mode file are guidance, not automatic switches. A mode file looks like this:

```markdown
# MODE_[Name].md

## Activation Triggers
- Flag: --mode-name
- Keywords: [triggers]
- Complexity: threshold

## Behavioral Modifications
- Communication style changes
- Decision-making adjustments
- Output format modifications

## Interaction Patterns
- How to respond
- What to prioritize
```

## MCP Server Configuration

### Configuration Location

MCP servers are configured in `~/.claude.json` (NOT part of SuperClaude context):

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

### MCP Integration

- **MCP Servers**: Actual software providing tools
- **SuperClaude**: Context that tells Claude when to use them
- **Activation**: Commands and skills name the servers they use; MCP flags such as `--c7` are advisory hints

## How Claude Code Reads Context

### Context Loading Sequence

```
User Input (in Claude Code): "/sc:analyze src/ --focus security"
                    ↓
1. Parse Command: identify 'analyze' command
                    ↓
2. Load Context: read commands/sc/analyze.md
                    ↓
3. Check Flags: --focus security
                    ↓
4. Delegate if the command says so: e.g. load security-engineer.md
                    ↓
5. Apply Patterns: follow analysis workflow
                    ↓
6. Generate Output: using loaded contexts
```

### Context Priority

1. **Explicit Commands**: `/sc:` commands take precedence
2. **Manual Agents**: `@agent-<full-name>` routes directly to that agent
3. **Flags**: Modify behavior of commands/agents
4. **Delegation**: Agents a command or skill delegates to, or that Claude chooses by `description`
5. **Default Behavior**: Standard Claude Code

## Extending the Framework

### Adding New Commands

1. Create `~/.claude/commands/sc/new-command.md`
2. Define metadata, triggers, and workflow
3. No code changes needed - just context

### Adding New Agents

1. Create `~/.claude/agents/new-specialist.md`
2. Define expertise, triggers, and behaviors
3. Agent becomes available

### Adding New Modes

There is no way to add a mode that switches on by itself. Modes ship under `src/superclaude/modes/` and are not installed, and `CLAUDE.md` imports only `BASH_INSPECTION_POLICY.md`, so a new `~/.claude/MODE_*.md` file is never loaded. To change interaction style, put the behavior in the command or skill that needs it.

### Best Practices

- **Keep Context Focused**: One concept per file
- **Clear Triggers**: Define when context activates
- **Workflow Patterns**: Provide step-by-step guidance
- **Examples**: Include practical usage examples
- **Metadata**: Use frontmatter for configuration

## Important Clarifications

### What SuperClaude Is NOT

- ❌ **No Execution Engine**: No code runs, no processes execute
- ❌ **No Performance System**: No optimization possible (it's just text)
- ❌ **No Detection Engine**: Claude Code does pattern matching
- ❌ **No Orchestration Layer**: Context files guide, not control
- ❌ **No Quality Gates**: Just instructional patterns

### What SuperClaude IS

- ✅ **Context Files**: `.md` instructions for Claude Code
- ✅ **Behavioral Patterns**: Workflows and approaches
- ✅ **Domain Expertise**: Specialized knowledge contexts
- ✅ **Configuration**: Settings for actual tools (MCP)
- ✅ **Framework**: Structured prompt engineering

## Summary

SuperClaude's architecture is intentionally simple: it's a well-organized collection of context files that Claude Code reads to modify its behavior. The power comes from the careful crafting of these contexts and their systematic organization, not from any executing code or running processes.

The framework's elegance lies in its simplicity - by providing Claude Code with structured instructions through context files, we can achieve sophisticated behavioral modifications without any software complexity.
