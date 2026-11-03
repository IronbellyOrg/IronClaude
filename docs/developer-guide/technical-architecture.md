# SuperClaude Context Architecture Guide

## Overview

This guide documents how SuperClaude's Context-Oriented Configuration Framework is structured and how Claude Code interprets these context files to modify its behavior.

**Important**: Most of SuperClaude is `.md` instruction files (core files, commands, agents, skills) that Claude Code reads to adopt specialized behaviors. Two parts do run code: the `superclaude` Python CLI (installer, `doctor`, and the `sprint`, `roadmap`, `tasklist`, `eval`, `swarm` and other pipelines) and the hook scripts Claude Code runs on session and tool events. See [What Runs Code](#what-runs-code).

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

The lists below give counts rather than every file name. Run `superclaude install --list` to see each installed core file, command, agent, skill and template by name.

```text
~/.claude/ (SuperClaude Framework Files Only)
├── CLAUDE.md                       # Always loaded; imports BASH_INSPECTION_POLICY.md
├── BASH_INSPECTION_POLICY.md       # Bash inspection rules, imported by CLAUDE.md
├── HOW-WE-WORK.md                  # Routing guide, read on demand, never imported
├── RULES.md                        # Behavioral rules, read by skills
├── PRINCIPLES.md                   # Engineering principles, read by skills
├── CODEGRAPH.md                    # Codegraph usage guide, read by skills and agents (5.0.0)
├── ISSUE-HANDOFF.md                # Issue template for work handed to someone else (5.0.0)
├── ISSUE-BACKLOG.md                # Issue template for parked work (5.0.0)
├── RESEARCH_CONFIG.md              # Deep-research configuration
├── BUSINESS_SYMBOLS.md             # Business-panel symbols
├── BUSINESS_PANEL_EXAMPLES.md      # Business-panel examples
│                                   # (11 core files in all)
├── agents/                         # 45 agent files, e.g. backend-architect.md,
│                                   # pm-agent.md, rf-qa.md, technical-writer.md
├── commands/
│   └── sc/                         # 45 slash commands (/sc:<name>), e.g. implement.md,
│                                   # workflow.md, impact.md (/sc:impact), graph.md (/sc:graph)
├── skills/                         # 38 skill folders (SKILL.md plus refs/, rules/,
│                                   # templates/, scripts/), e.g. sc-implement-protocol/,
│                                   # sc-graph-protocol/, sc-impact-protocol/, ccsession-tag/
│   └── ccsession-tag/
│       ├── ccsession, ccsession-orca  # Launchers, linked from ~/.local/bin/
│       └── hooks/
│           ├── session-start.sh    # SessionStart (startup|resume)
│           └── session-name.sh     # UserPromptSubmit and SessionEnd: keeps session names in step
├── templates/                      # 53 document and workflow templates (documents/,
│                                   # workflow/, modularization-template-review/)
├── rules/                          # Rule groups core/, contextual/, prompts/; listed in
│                                   # settings.json claudeMdExcludes, read on demand
├── output-styles/
│   └── pragmatic.md                # Injected into subagents by pragmatic-subagent.js
├── hooks/                          # Hook scripts deposited by install_hooks
│   ├── session-init.sh             # Pre-existing init script (legacy)
│   ├── freshness-session-start.sh  # SessionStart envelope (startup + resume branches)
│   ├── freshness-user-prompt.sh    # Per-turn <session-context> envelope injection
│   ├── freshness-pre-edit.sh       # PreToolUse gate: blocks Edit/Write against unread/stale files
│   ├── freshness-post-read.sh      # PostToolUse(Read) tracker
│   ├── freshness-subagent-start.sh # Background-agent counter increment
│   ├── freshness-subagent-stop.sh  # Background-agent counter decrement
│   ├── freshness-file-changed.sh   # Copied but NOT registered — see freshness-hooks.md
│   ├── codegraph-session-start.sh  # SessionStart (startup): one detached `codegraph init --yes`
│   │                               # in a git checkout with no .codegraph/codegraph.db (5.0.0)
│   ├── auggie-flag-clear.sh        # PostToolUse after an auggie MCP call
│   ├── pragmatic-subagent.js       # SubagentStart: injects output-styles/pragmatic.md (needs node)
│   ├── reject-workspace-writes.sh  # Copied; registered only by this repo's .claude/settings.json
│   └── sc-recommend-phase0.sh      # Copied; registered only by this repo's .claude/settings.json
├── state/                          # Per-session state populated by hooks
│   ├── reads.jsonl                 # Successful Read events (cross-session jsonl)
│   ├── turns/<sid>.txt             # Per-session turn counter
│   ├── last-prompt-ts/<sid>.txt    # Per-session last prompt timestamp
│   ├── bg-agents/<sid>.txt         # Per-session background-agent count
│   └── tool-call-counter/<sid>.txt # Per-session tool-call sequence
├── logs/                           # Hook telemetry
│   └── freshness-hook.jsonl        # PreToolUse decisions (one row per Edit attempt)
├── ccsession.env                   # ccsession settings, seeded once from ccsession.env.example
└── settings.json                   # Hook registrations merged by install_hooks

Note: Other directories (backups/, projects/, etc.) are Claude Code
operational directories, not part of SuperClaude framework content.
```

`superclaude install` also writes outside `~/.claude/`. The `versions/`, `current` and `~/.local/bin/codegraph` entries appear only when the installer downloads the pinned codegraph itself, because none was found on `PATH` or in `~/.local/bin`:

```text
~/.codegraph/                       # codegraph, pinned version
├── versions/<tag>/bin/codegraph    # Downloaded binary
├── current                         # Link to the active version
├── .superclaude-receipt.json       # What the installer downloaded and linked
└── .superclaude-bin                # Path of the binary the installer registered
~/.local/bin/
├── codegraph                       # Link to ~/.codegraph/versions/<tag>/bin/codegraph
├── ccsession                       # Link to ~/.claude/skills/ccsession-tag/ccsession
└── ccsession-orca                  # Link to ~/.claude/skills/ccsession-tag/ccsession-orca
```

The hook registrations themselves come from `hooks.json` in the package and are merged into `~/.claude/settings.json`. The 5.0.0 release dropped the core files `ORCHESTRATOR.md`, `COMMANDS.md`, `PERSONAS.md`, `MODES.md`, `FLAGS.md` and `MCP.md`; their routing content now lives in `HOW-WE-WORK.md`. Copies left in an older `~/.claude/` are not loaded by anything.

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

```text
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

### What Runs Code

- **The `superclaude` Python CLI**: `install`, `update`, `doctor` and `mcp` set up and check the installation. The `sprint`, `roadmap`, `tasklist`, `eval`, `swarm`, `reflect`, `prd`, `cli-portify` and `cleanup-audit` commands are multi-step pipelines: most start Claude Code as a subprocess for each step and check its output in code; `swarm` fans one prompt out to several OpenAI-compatible model workers. Run `superclaude --help` for the full list.
- **Hook scripts**: Claude Code runs the scripts in `~/.claude/hooks/` and `~/.claude/skills/ccsession-tag/hooks/` on the events registered in `settings.json`. They track reads, block edits to unread or stale files (`freshness-pre-edit.sh`), and start a background `codegraph init` on the first session in a new checkout (`codegraph-session-start.sh`; opt out with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`).
- **MCP servers**: Separate software (codegraph, Context7, Tavily and others) that `superclaude mcp` and `superclaude install` register with Claude Code.

### What Is Only Context

- **Core files, commands, agents and skills**: `.md` instructions Claude Code reads. A `/sc:` command or skill describes a workflow; Claude follows it, nothing enforces it in code unless the workflow calls a CLI pipeline or a hook applies.
- **No detection engine**: Claude Code chooses agents by their `description`; there is no keyword or file-type matcher.
- **Flags**: Flags typed after a `/sc:` command (`--c7`, `--tavily`, `--brainstorm`) are hints Claude may honour, not options parsed by code. CLI options of `superclaude <command>` are parsed normally.

## Summary

SuperClaude is mostly a well-organized collection of context files that Claude Code reads to modify its behavior, plus a Python CLI and a set of hook scripts that do run. The context files carry the workflows and expertise; the CLI installs and checks them and runs the long multi-step pipelines; the hooks keep sessions honest about what has been read and keep the code graph indexed.
