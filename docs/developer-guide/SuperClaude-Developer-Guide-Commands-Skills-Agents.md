# SuperClaude Developer Guide: Commands, Skills, and Agents

> **Version**: 1.0.0 | **Last Updated**: 2026-11-12
> **Audience**: Developers creating, extending, or maintaining SuperClaude framework components
> **Source of Truth**: `src/superclaude/` -- all component source files live here

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Quick Start](#2-quick-start)
3. [Commands Deep Dive](#3-commands-deep-dive)
4. [Agents Deep Dive](#4-agents-deep-dive)
5. [Skills Deep Dive](#5-skills-deep-dive)
6. [Multi-Phase Architecture](#6-multi-phase-architecture)
7. [Integration Patterns](#7-integration-patterns)
   - [7.7 Orca Orchestration: Commands as Workers](#77-orca-orchestration-commands-as-workers)
8. [Development Workflow](#8-development-workflow)
9. [Best Practices](#9-best-practices)
10. [Complete Examples](#10-complete-examples)

---

## 1. Introduction

### What SuperClaude Is

SuperClaude is a **Context-Oriented Configuration Framework** for Claude Code. It consists entirely of Markdown instruction files (`.md`) that Claude Code reads at session start and on demand to modify its behavior. SuperClaude is NOT standalone software, a runtime, or an executable. It shapes how Claude Code reasons, plans, and acts by injecting structured context.

The framework provides:

- **Specialized personas** that activate domain-specific reasoning (security, architecture, frontend, etc.)
- **Slash commands** (`/sc:*`) that trigger structured workflows with defined inputs, outputs, and quality gates
- **Skills** that package domain knowledge with lazy-loading token efficiency
- **Agents** that define specialist executor roles with explicit behavioral boundaries
- **MCP integration** that connects Claude Code to external tools (documentation servers, browser automation, semantic search)

### The Three-Tier Architecture

SuperClaude components are organized into three tiers that work together:

```text
Commands (Workflow Triggers — thin dispatch layer)
    invoke via Activation section
Skills (Domain Knowledge Packages — behavioral protocol + refs/)
    delegate to
Agents (Specialist Executors)
```

| Tier | What It Is | File Location | Invocation | Typical Size |
|------|-----------|---------------|------------|--------------|
| **Command** | Thin dispatch stub: flags, usage, examples, boundaries, Activation handoff | `src/superclaude/commands/<name>.md` | `/sc:<name>` | ~80-150 lines |
| **Skill** | Domain knowledge package with behavioral protocol and optional reference files | `src/superclaude/skills/<name>/SKILL.md` | Invoked by commands via Activation section | ~200-500 lines |
| **Agent** | Specialist executor with behavioral constraints | `src/superclaude/agents/<name>.md` | `@agent-<name>` or delegated by skills | ~40-120 lines |

**How they compose**: A command like `/sc:adversarial` defines the user-facing interface (flags, usage, examples, boundaries) and nothing else — it contains zero protocol logic. Its `## Activation` section hands off to the `sc-adversarial` skill which contains the detailed protocol. The skill delegates work to agents like `debate-orchestrator` and `merge-executor`.

**Every skill MUST have a command in front of it.** The command is the user-facing entry point; the skill is the behavioral engine. A skill without a command is an architectural violation — it forces the skill to handle both interface concerns (flags, usage, examples) and protocol concerns (execution logic), creating a monolith. When refactoring an existing skill, creating its thin command layer is part of the refactoring scope.

### The Activation Pattern

Every command that backs a skill MUST include an `## Activation` section as the handoff mechanism:

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill <skill-name>

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification is in the protocol skill.
```

This pattern enforces separation of concerns: the command owns the interface, the skill owns the protocol. The command never contains execution logic; the skill never contains usage examples or flag definitions.

### Installation Locations

```text
Source of truth (development):     src/superclaude/
  commands/                        Command .md files
  skills/                          Skill directories (SKILL.md + refs/)
  agents/                          Agent .md files
  core/                            Core framework files (CLAUDE.md, HOW-WE-WORK.md, WORKER-CONTRACT.md, ...)

Installation target (user):        ~/.claude/
  *.md                             Installed core files, including WORKER-CONTRACT.md (worker rules, section 7.7)
  commands/sc/                     Installed commands
  skills/                          Installed skills
  agents/                          Installed agents

Dev convenience copies:            .claude/
  commands/sc/                     Synced from src/ via make sync-dev
  skills/                          Synced from src/ via make sync-dev
  agents/                          Synced from src/ via make sync-dev
```

### Path rules for primitives

A command, skill or agent runs from `~/.claude/` in whatever project the user is in, where `src/superclaude/` does not exist. So when a primitive tells an agent to read, verify or invoke another primitive, it must not use a `src/superclaude/...` path.

| To refer to | Write |
|---|---|
| a skill or its refs | `~/.claude/skills/<name>/SKILL.md`, `~/.claude/skills/<name>/refs/...` |
| an agent | `~/.claude/agents/<name>.md` |
| a command | `~/.claude/commands/sc/<name>.md` |
| a core doc | `~/.claude/<FILE>.md` (e.g. `~/.claude/HOW-WE-WORK.md`) |

Rules:

1. **Accept the project copy too.** In a dev checkout `make sync-dev` creates `.claude/skills/` and `.claude/agents/`, and the installed copy may be missing or older. An existence check should name both (`~/.claude/skills/<name>/SKILL.md` or `.claude/skills/<name>/SKILL.md`; either satisfies it) and STOP only when neither exists.
2. **When one file must be read, follow Claude Code's precedence**, which differs by type: same-name agents resolve project `.claude/agents/` over `~/.claude/agents/`; same-name skills resolve `~/.claude/skills/` over `.claude/skills/`. Read the winning copy first and say so in the text.
3. **Do not point at what is not installed.** Package code (`src/superclaude/cli/`, `pm_agent/`, `contracts/`) and `src/superclaude/examples/` are not copied to `~/.claude/`. Reach package behavior through the `superclaude` CLI instead of a file path.
4. **`src/superclaude/...` is fine only** in maintainer instructions ("edit `src/superclaude/...`, then `make sync-dev`"), in commands that work on this repo's own source by design (such as `/sc:cli-portify`), and as an in-checkout fallback listed after the global path.
5. **Before committing**, run `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify every remaining hit against rule 4.

### Context Loading Sequence

When Claude Code starts a session, it loads context in this priority order:

1. **Core file** (always loaded): `~/.claude/CLAUDE.md`, which imports only `BASH_INSPECTION_POLICY.md`. The routing guide `~/.claude/HOW-WE-WORK.md` is installed beside it but is read on demand (by `/sc:help`, `/sc:recommend`, or a person); it is never `@`-imported.
   The worker contract `~/.claude/WORKER-CONTRACT.md` is installed beside `CLAUDE.md` too. It is read on demand by an Orca coordinator and, from P1, by a worker applying the brief guard, and it is never `@`-imported ([section 7.7](#77-orca-orchestration-commands-as-workers)).
2. **Explicit commands**: User types `/sc:<command>` -- loads the command file
3. **Manual agents**: User references `@agent-<name>` -- loads the agent file
4. **Flag-triggered**: per-command flags (each command file lists its own); `--c7`, `--play` and similar are behavioural hints, see `docs/user-guide/flags.md`
5. **Skills**: Load only name and description at session start (~50 tokens). Full content loads on invocation (~2000 tokens)

---

## 2. Quick Start

### 2.1 Create a Minimal Command

Create a file at `src/superclaude/commands/hello.md`:

````markdown
---
name: hello
description: "A minimal example command"
category: utility
complexity: simple
mcp-servers: []
personas: []
---

# /sc:hello - Hello World Command

## Triggers
- User invokes `/sc:hello`
- User asks for a greeting or demo

## Usage

```bash
/sc:hello [name]
```

## Behavioral Flow
1. Greet the user by name (or "World" if no name provided)
2. Display a summary of available SuperClaude commands

## Examples

```bash
/sc:hello              # "Hello, World!"
/sc:hello Alice        # "Hello, Alice!"
```

## Boundaries

**Will:**
- Greet the user and list available commands

**Will Not:**
- Execute any code or modify files
- Access external services
````

### 2.2 Create a Minimal Agent

Create a file at `src/superclaude/agents/greeter.md`:

```markdown
---
name: greeter
description: Friendly greeting specialist for demonstration purposes
category: utility
---

# Greeter Agent

## Triggers
- Invoked by `/sc:hello` command
- User requests a personalized greeting

## Behavioral Mindset
Be warm, concise, and informative. Focus on helping users discover
SuperClaude capabilities.

## Tools
- **Read**: Access command files for listing
- **Glob**: Discover available commands

## Outputs
- Greeting message with user's name
- List of available `/sc:*` commands

## Boundaries

**Will:**
- Generate greetings and list commands

**Will Not:**
- Modify any files
- Execute shell commands
```

### 2.3 Create a Minimal Skill

Create a directory and file at `src/superclaude/skills/hello/SKILL.md`:

```markdown
---
name: hello
description: Minimal greeting skill for demonstration
allowed-tools: Read, Glob
---

# Hello Skill

## Purpose
Demonstrate the minimal structure required for a SuperClaude skill.

## Protocol

1. Accept optional `name` argument
2. Read available commands from `src/superclaude/commands/`
3. Return greeting and command list

## Will Do
- Greet the user
- List available commands

## Will Not Do
- Modify files
- Access external services
```

### 2.4 Sync and Test

```bash
# Copy new components from src/ to .claude/
make sync-dev

# Verify sync succeeded
make verify-sync

# Test the command in Claude Code
# Type: /sc:hello
```

---

## 3. Commands Deep Dive

### 3.1 Anatomy of a Command File

Every command is a single Markdown file with two parts: YAML frontmatter and a Markdown body.

**YAML Frontmatter** (required fields):

```yaml
---
name: <command-name>           # Identifier, maps to /sc:<name>
description: "<summary>"       # One-line user-facing description
category: <category>           # One of: development, planning, analysis, quality,
                               #   testing, documentation, version-control, meta, special
complexity: <level>            # One of: simple, moderate, advanced, high
mcp-servers: [<servers>]       # MCP servers used: context7,
                               #   playwright, magic, morphllm (or empty [])
personas: [<personas>]         # Descriptive labels only (nothing auto-activates them): architect,
                               #   analyzer, frontend, backend, security, qa, etc. (or empty [])
---
```

**Optional frontmatter fields** (seen in advanced commands):

```yaml
version: "2.0.0"              # Explicit spec version (used in /sc:task)
```

**Markdown Body** (standard sections):

| Section | Purpose | Required |
|---------|---------|----------|
| `# /sc:<name> - Title` | Human-readable title | Yes |
| `## Required Input` or `## Triggers` | What activates the command and what it needs | Yes |
| `## Usage` | Code-fenced invocation examples | Yes |
| `## Options` or `## Arguments` | Flag/argument table | If flags exist |
| `## Behavioral Flow` | Step-by-step protocol | Yes |
| `## MCP Integration` | Which MCP servers and how | If MCP used |
| `## Tool Coordination` | Which tools and when | Recommended |
| `## Examples` | Copy-paste invocation samples | Yes |
| `## Boundaries` | Will / Will Not lists | Yes |
| `## Related Commands` | Links to related `/sc:*` commands | Recommended |
| `## Unattended mode` | This command's gate resolutions, report file, report directory flag and nested invocations under `--unattended` ([section 7.7](#77-orca-orchestration-commands-as-workers)) | Only when the command accepts `--unattended`, which no command does at P0 |

A command that accepts `--unattended` lists it in `## Options` (this guide's convention). It takes `--report-dir` when it has no directory-valued `--output` or `--output-dir` of its own, or when the brief does not pass that flag; passing both, or neither, is refused before any work (WC-4, [section 7.7](#77-orca-orchestration-commands-as-workers)).

### 3.2 Command Archetypes

Commands fall into three recurring patterns:

#### Archetype 1: Analysis Pipeline

Commands that read, analyze, and report without modifying files.

- **Examples**: `/sc:analyze`, `/sc:cleanup-audit`, `/sc:explain`
- **Characteristics**: Read-heavy tools, native reasoning for deep analysis, produces reports
- **Worker fit**: `/sc:cleanup-audit` is in the contract's ready-with-brief-constraints table; one of `/sc:explain`'s flags is refused under `--unattended` (section 7.7); a command gets `--unattended` only after each of its gates has an unattended resolution (WC-2). See [section 7.7](#77-orca-orchestration-commands-as-workers).
- **Typical frontmatter**:

```yaml
category: analysis
mcp-servers: [context7]
personas: [analyzer, architect]
```

#### Archetype 2: Meta-Orchestrator

Commands that decompose work and delegate to sub-agents without directly executing.

- **Examples**: `/sc:spawn`, `/sc:adversarial`
- **Characteristics**: Task tool for delegation, defines stop conditions, produces task hierarchies or coordination artifacts
- **Key pattern**: Explicit "STOP AFTER" boundary preventing the command from executing what it plans
- **Worker fit**: `/sc:spawn` is a never-as-worker command (section 7.7); `/sc:adversarial` is in the contract's ready-with-brief-constraints table. Such a command may fan out with the Agent tool (WC-7) but never calls `worker-start`, `dispatch` or `task-create` (WC-8). See [section 7.7](#77-orca-orchestration-commands-as-workers).

Example from `/sc:spawn`:

```text
## CRITICAL BOUNDARIES
- STOP AFTER TASK DECOMPOSITION
- Output is task hierarchy only
- Will NOT execute tasks or modify code
```

#### Archetype 3: Unified Executor

Commands that handle the full lifecycle from classification through execution to verification.

- **Examples**: `/sc:task`, `/sc:implement`, `/sc:build`
- **Characteristics**: Multiple MCP servers, many personas, tiered compliance, sub-agent delegation
- **Worker fit**: outward actions and the command's own commit step are off under `--unattended` (WC-9); per the rollout plan, `/sc:implement` is converted in P4. See [section 7.7](#77-orca-orchestration-commands-as-workers).
- **Typical frontmatter**:

```yaml
category: special
version: "2.0.0"
mcp-servers: [context7, playwright, morphllm]
personas: [architect, analyzer, frontend, backend, security, qa, devops,
           refactorer, performance, mentor, scribe]
```

### 3.3 Command Processing Pipeline

When a user invokes a command, it passes through five stages:

```text
1. Input Parsing    →  Parse $ARGUMENTS with @<path>, !<command>, --<flags>
2. Context Resolution  →  Read the command file and its skill; select MCP servers
3. Phase Planning      →  Follow the skill's own waves or phases, if it defines any
4. Execution Strategy  →  Orchestrate tools and resources
5. Quality Gates       →  Validate output and verify completion
```

### 3.4 Performance Profiles

Each command declares a performance profile that affects resource allocation:

| Profile | Description | Token Budget | Use Case |
|---------|-------------|-------------|----------|
| `optimization` | High-performance with caching and parallel execution | 5K | Simple commands |
| `standard` | Balanced performance with moderate resource usage | 15K | Most commands |
| `complex` | Resource-intensive with comprehensive analysis | 30K+ | Audits, architecture |

### 3.5 Wave-Enabled Commands

Some commands declare `wave-enabled: true` in their frontmatter, and many protocol skills run their own waves or phases. No complexity score, file count or operation count switches wave execution on automatically: a command runs in waves only when its own command file or skill says so.

### 3.6 Registering a New Command

After creating a command file, register it in `src/superclaude/core/HOW-WE-WORK.md`. Routing-table rows are per job, not per command: if a workflow should use the new command, add it to that job's row in the routing table (its steps and mandatory flags), or add a new job row; if no workflow uses it, add one row to the "Other commands" table instead. Then copy the guide byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (and, if you edited the level table, re-copy it into `src/superclaude/core/CLAUDE.md`), run `make sync-dev` and `make verify-sync`, and run `uv run pytest tests/core tests/commands` (these tests check the routing table and the plugin copy). No other framework file needs registering: `/sc:help` lists installed commands live.

A command that accepts `--unattended` needs no entry in any worker list, because the coordinator decides from whether the command file has an `## Unattended mode` section (the "Orca coordination" section of `~/.claude/HOW-WE-WORK.md`). The one registration step it does need is in a test file: the maintainer adds its name to `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py`, as section 8.4 describes. The never-as-worker list changes only through the maintainer edit that [section 7.7](#77-orca-orchestration-commands-as-workers) describes.

---

## 4. Agents Deep Dive

### 4.1 Anatomy of an Agent File

Every agent is a single Markdown file with YAML frontmatter and a Markdown body.

**YAML Frontmatter** (required fields):

```yaml
---
name: <agent-name>             # Identifier, used in @agent-<name> references
description: <summary>         # One-line description of the agent's role
category: <category>           # Functional grouping: analysis, meta, utility, etc.
---
```

**Optional frontmatter fields** (for constrained agents):

```yaml
tools: [Read, Write, Glob]     # Explicit tool allowlist
model: opus                    # Model preference
maxTurns: 10                   # Maximum conversation turns
permissionMode: restricted     # Permission level
```

The optional `model:` field is read by Claude Code as an alias (`sonnet`, `opus`, `haiku`, `fable`), a full model ID or `inherit`. For the agent files under `src/superclaude/agents/`, `tests/skills/test_model_alias_policy.py` requires `opus`, `sonnet`, `haiku` or `inherit`, except for the allow-listed issue workers, which pin a picker ID such as `claude-gw-tier3` (see [model-aliases](../reference/model-aliases.md)). The Agent call's `model` parameter accepts aliases only and overrides the frontmatter. So a skill that needs a pinned tier spawns the agent by `subagent_type` and must not pass `model`.

**Markdown Body** (standard sections):

| Section | Purpose | Required |
|---------|---------|----------|
| `# <Agent Title>` | Human-readable name | Yes |
| `## Triggers` | When this agent activates | Yes |
| `## Behavioral Mindset` | Role framing and behavioral constraints | Yes |
| `## Model Preference` | Which model works best | Recommended |
| `## Tools` | Which tools and why | Recommended |
| `## Responsibilities` | Numbered list of what the agent does | Yes |
| `## Focus Areas` | Key quality dimensions | Recommended |
| `## Outputs` | Concrete artifacts produced | Yes |
| `## Does NOT` | Explicit negative constraints | Yes |
| `## Boundaries` | Will / Will Not lists | Yes |

### 4.2 Agent Patterns

"Worker" has two meanings in this guide. A pattern such as Constrained Worker below is an Agent-tool subagent inside one session. An Orca worker is a whole top-level session that a coordinator starts to run one command ([section 7.7](#77-orca-orchestration-commands-as-workers)).

Agents follow four recurring patterns:

#### Pattern 1: Constrained Worker

An agent with a narrow scope and explicit tool restrictions. Receives specific instructions and produces a single artifact type.

- **Example**: `merge-executor` -- follows a refactoring plan to produce merged output
- **Characteristics**: Small tool set, single responsibility, receives plan from orchestrator
- **Typical size**: 40-60 lines

#### Pattern 2: Specialist Investigator

An agent focused on deep analysis within a specific domain. Produces reports, findings, or recommendations.

- **Example**: `deep-research-agent` -- systematic investigation with evidence management
- **Characteristics**: Read-heavy tools, multi-phase workflow, evidence-based output, quality standards
- **Typical size**: 80-120 lines

#### Pattern 3: Process Orchestrator

An agent that coordinates other agents without doing the work itself. Manages sequencing, scoring, and handoffs.

- **Example**: `debate-orchestrator` -- coordinates adversarial debate without participating
- **Characteristics**: Task tool for delegation, strict neutrality, process integrity focus, return contracts
- **Key constraint**: "Does NOT participate in debates or advocate for any variant"
- **Orca boundary**: an orchestrating agent coordinates subagents inside its own session only; it never calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8)
- **Typical size**: 60-100 lines

#### Pattern 4: Meta-Layer Agent

An agent that operates across sessions and manages knowledge, learning, and documentation.

- **Example**: `pm-agent` -- documents implementations, analyzes mistakes, maintains knowledge base
- **Characteristics**: `.superclaude/memory/` files for session persistence, PDCA self-evaluation, mandatory session start activation
- **Typical size**: 100-150 lines

When an Orca coordinator runs the command as a worker, these rules hold for every agent under it ([section 7.7](#77-orca-orchestration-commands-as-workers)):

- Only the top-level worker session sends lifecycle messages (heartbeat, ask, check, `worker_done`), never a subagent (WC-7).
- No agent calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8).
- Under `--unattended` nothing asks the person, so an agent resolves a gate the way its command's `## Unattended mode` section says (this guide's convention); only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).

### 4.3 Agent Spec Format (Dynamic Instantiation)

Skills can dynamically create agents using the agent spec mini-language:

```text
<model>[:persona[:"instruction"]]
```

The `<model>` in an agent spec is an alias (for example `opus`, `sonnet` or `haiku`), not a full model ID or picker ID.

**Examples**:

| Spec | Meaning |
|------|---------|
| `opus` | Opus model, no persona or custom instruction |
| `opus:architect` | Opus with architect persona |
| `opus:security:"Focus on OWASP Top 10"` | Opus with security persona and custom instruction |
| `sonnet:analyzer` | Sonnet with analyzer persona |

This format is used in the `--agents` flag of `/sc:adversarial` to specify advocate agents for variant generation.

### 4.4 Agent Activation Methods

Agents activate through three mechanisms:

| Method | Syntax | When |
|--------|--------|------|
| **Manual reference** | `@agent-<name>` | User explicitly invokes |
| **Skill delegation** | Task tool in SKILL.md | Skill protocol delegates to agent |
| **Claude's choice** | Agent `description` match | Claude Code may delegate to an agent whose description fits the request; there is no keyword or file-type scoring in code |

---

## 5. Skills Deep Dive

### 5.1 Anatomy of a Skill

A skill is a **directory** containing a `SKILL.md` manifest and optional subdirectories:

```text
src/superclaude/skills/<skill-name>/
  SKILL.md              # Manifest (required) -- behavioral intent
  refs/                 # Reference files (optional) -- algorithms, formulas, templates
    scoring-protocol.md
    agent-specs.md
  rules/                # Rule files (optional) -- validation rules
  templates/            # Template files (optional) -- output templates
  scripts/              # Script files (optional) -- shell preprocessing
```

### 5.2 SKILL.md Frontmatter

**Minimum required fields**:

```yaml
---
name: <skill-name>
description: "<what this skill does>"
allowed-tools: Read, Glob, Grep
---
```

**Full field set** (for complex skills):

```yaml
---
name: sc-cleanup-audit
description: "Multi-pass read-only repository audit producing evidence-backed cleanup recommendations"
category: utility
complexity: high
mcp-servers: [context7]
personas: [analyzer, architect, devops, qa, refactorer]
allowed-tools: Read, Grep, Glob, Bash(git *), Bash(wc *), Bash(find *), Bash(du *), TodoWrite, Task, Write
argument-hint: "[target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]"
---
```

**Key fields explained**:

| Field | Purpose | Notes |
|-------|---------|-------|
| `name` | Skill identifier | Skills prefixed `sc-` map to `/sc:<name>` commands |
| `description` | User-facing summary | Loaded at session start (~50 tokens) |
| `allowed-tools` | Tool allowlist | Primary safety boundary for the skill |
| `category` | Functional grouping | Optional, aids discoverability |
| `complexity` | Complexity level | Optional, affects resource allocation |
| `mcp-servers` | MCP server declarations | Optional, documents orchestration intent |
| `personas` | Persona activations | Optional, documents persona involvement |
| `argument-hint` | CLI usage hint | Optional, improves invocation ergonomics |

### 5.3 Extended Metadata Comment

For documentation purposes, skills can include an unparsed HTML comment with additional metadata:

```markdown
<!-- Extended metadata (for documentation, not parsed):
category: analysis
complexity: advanced
mcp-servers: [context7]
personas: [architect, analyzer, scribe]
-->
```

This is NOT parsed by the framework but helps developers and documentation tools understand the skill's orchestration context.

### 5.4 Tool Allowlisting

The `allowed-tools` field is the **primary safety boundary** for skills. It restricts which tools Claude Code can use when executing the skill.

**Patterns**:

| Pattern | Meaning | Example |
|---------|---------|---------|
| `Read, Glob, Grep` | Standard read-only tools | Analysis skills |
| `Bash(git *)` | Bash restricted to git commands only | Audit skills |
| `Bash(wc *), Bash(find *)` | Bash restricted to specific command families | Report skills |
| Omit `Edit` | Prevent file modification | Read-only skills |
| Full tool list | All tools available | Implementation skills |

**Safety principle**: For audit or report-only skills, omit `Edit` and scope `Write` output to a dedicated directory. For safety-critical skills, restrict Bash to specific command families.

### 5.5 Skill Complexity Tiers

Skills fall into three complexity tiers:

#### Tier 1: Simple (SKILL.md only)

A single `SKILL.md` file with no subdirectories. Suitable for lightweight checks, assessments, or simple protocols.

**Example**: `confidence-check`

```text
src/superclaude/skills/confidence-check/
  SKILL.md              # ~100 lines, no refs/ or rules/
```

```yaml
---
name: Confidence Check
description: Pre-implementation confidence assessment (>=90% required).
---
```

The skill defines a scoring rubric (5 checks), a threshold (>= 90% to proceed), and explicit action ranges (70-89% present alternatives, < 70% ask questions). No external references needed.

#### Tier 2: Medium (SKILL.md + allowed-tools + compliance logic)

A `SKILL.md` with tool allowlisting and structured execution flows. May include tiered compliance or delegation.

**Example**: `sc-task-protocol` (backs `/sc:task`)

```text
src/superclaude/skills/sc-task-protocol/
  SKILL.md              # ~400 lines: execution flow for STANDARD and STRICT tiers
```

```yaml
---
name: sc:task-protocol
description: Unified task execution with intelligent workflow management,
  MCP compliance enforcement, and multi-agent delegation.
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill,
  mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
---
```

Key features: Four compliance tiers (STRICT/STANDARD/LIGHT/EXEMPT). The `/sc:task` command file classifies the tier (keyword and compound-phrase rules) and emits the machine-readable header; the skill then runs the execution flow for STANDARD and STRICT tasks.

#### Tier 3: Complex (SKILL.md + refs/ + agents + multi-phase)

A full skill directory with reference files, agent delegation, and multi-phase protocols.

**Example**: `sc-adversarial-protocol` (backs `/sc:adversarial`)

```text
src/superclaude/skills/sc-adversarial-protocol/
  SKILL.md                # ~3,000 lines, behavioral protocol
  refs/
    scoring-protocol.md   # Hybrid scoring algorithm details
    agent-specs.md        # Agent specification format and templates
    debate-protocol.md    # The 5-step debate protocol
    artifact-templates.md # Output artifact templates
```

```yaml
---
name: sc:adversarial-protocol
description: Structured adversarial debate, comparison, and merge pipeline
  for 2-10 artifacts
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill
---
```

Key features: Dual input modes, 5-step adversarial protocol, hybrid scoring with position-bias mitigation, dynamic agent instantiation, return contracts, error handling matrix, 6 output artifacts.

### 5.6 The refs/ Pattern (Lazy Loading)

The `refs/` directory contains detailed reference material that is loaded **on demand per wave**, not pre-loaded at session start. This is critical for token efficiency.

**Design rules**:

- `SKILL.md` contains behavioral intent (WHAT and WHEN) -- max ~400-500 lines
- `refs/` contains algorithms, formulas, prompts, templates (HOW) -- loaded per wave
- At any point, a skill should have at most 2-3 refs loaded
- The SKILL.md explicitly declares when to load each ref:

```markdown
## Wave 2: Analysis
Load `refs/scoring-protocol.md` before executing scoring.
Do NOT pre-load refs from later waves.
```

**Token budget**:

| Component | Tokens | When Loaded |
|-----------|--------|-------------|
| Skill name + description | ~50 | Session start |
| Full SKILL.md | ~2000 | On invocation |
| Each ref file | ~500-1500 | Per wave, on demand |

### 5.7 The sc- Prefix Convention

Skills prefixed with `sc-` have a special relationship with commands:

- `sc-adversarial-protocol` skill backs the `/sc:adversarial` command
- `sc-task-protocol` skill backs the `/sc:task` command
- `sc-cleanup-audit-protocol` skill backs the `/sc:cleanup-audit` command

These protocol skills are installed to `~/.claude/skills/` like any other skill; the command activates its skill by name (`Skill sc:<command>-protocol`). The installer skips only a bare `sc-<name>` skill whose `commands/<name>.md` exists; it does not strip the `-protocol` suffix, so protocol skills are never skipped (`src/superclaude/cli/install_skills.py`).

Skills without the `sc-` prefix (like `confidence-check`) are standalone utilities invocable by any command or agent.

### 5.8 Machine-Readable Headers

Complex skills require machine-readable output headers for telemetry and automation. These are HTML comment blocks emitted as the first output:

```markdown
<!-- SC:TASK-UNIFIED:CLASSIFICATION
tier: STRICT
confidence: 0.92
keyword_matches: ["refactor", "database"]
context_boosters: ["security_path:+0.4"]
override: none
-->
```

**Why**: Enables automated testing, telemetry dashboards, and inter-command composition.

### 5.9 Input and Output Contracts

#### Input Contracts

Skills define mandatory input validation with STOP/WARN rules:

```markdown
## Required Input (STOP if missing)

### Mode A: Compare existing artifacts
- `--compare file1,file2[,...,fileN]`: 2-10 existing file paths

### Mode B: Generate variants from source
- `--source <file>`: Source file path (STOP if not found)
- `--generate <type>`: Artifact type to generate
- `--agents <spec>[,...]`: Agent specifications

**STOP**: If neither mode's required inputs are provided.
**WARN**: If file count < 2 or > 10 in Mode A.
```

#### Output / Return Contracts

Skills return structured data for inter-command composition:

```markdown
## Return Contract

The skill returns these fields to the calling command:

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial`, `failed` |
| `merged_output_path` | string | Path to merged artifact |
| `convergence_score` | float | 0.0-1.0 agreement level |
| `artifacts_dir` | string | Path to artifacts directory |
| `unresolved_conflicts` | list | Items that could not be resolved |
```

#### Worker contract (under `--unattended`)

Under `--unattended` the worker contract file is `<report-dir>/return-contract.yaml`. Its status field is `worker_status`, not `status`, because existing skills' contracts already use `status` with other values (WC-4). The WC-4 two-case rule decides where the worker fields go:

- A command that already writes `return-contract.yaml` in the report directory itself keeps every existing field, including its own `status`, and adds the worker fields beside them.
- A command whose own contract lives elsewhere leaves that file unchanged, and the worker contract at `<report-dir>/return-contract.yaml` lists it in `artifacts`.

For example, a skill's own `success` becomes `succeeded`. The full mapping is WC-4 in `~/.claude/WORKER-CONTRACT.md`; see [section 7.7](#77-orca-orchestration-commands-as-workers).

### 5.10 Skill-Authoring Checklist

Use this checklist when creating or refactoring a skill:

- [ ] **Thin command layer exists** — a command file at `src/superclaude/commands/<name>.md` (~80-150 lines) with flags, usage, examples, boundaries, and an `## Activation` section that invokes `Skill <skill-name>`. The command contains zero protocol logic.
- [ ] SKILL.md has YAML frontmatter with `name`, `description`, `allowed-tools`
- [ ] SKILL.md contains only behavioral protocol (WHAT/WHEN) — under 500 lines
- [ ] `allowed-tools` is scoped to minimum required (no unnecessary `Edit` or `Bash`)
- [ ] Purpose section clearly states what the skill does and does not do
- [ ] Will Do / Will Not Do boundaries are explicit
- [ ] If complex: refs/ directory contains algorithm and template details (HOW content)
- [ ] SKILL.md declares when each ref should be loaded (per-wave)
- [ ] Input contract defines STOP/WARN conditions for missing inputs
- [ ] Output contract defines return fields for composability
- [ ] If the skill uses agents: agent delegation is explicit with Task tool
- [ ] Routing row added to the guide (`src/superclaude/core/HOW-WE-WORK.md`)
- [ ] **No hardcoded `src/superclaude/...` paths** in SKILL.md, refs/ or scripts that tell an agent to read or verify another primitive; use the installed `~/.claude/...` path and accept the project `.claude/` copy too (see "Path rules for primitives")
- [ ] **Worker eligibility decided**: the command is either worker-capable or a never-as-worker command ([section 7.7](#77-orca-orchestration-commands-as-workers))
- [ ] **Every blocking step has an unattended resolution**: each step that waits for a human has a default, a caller flag or a blocked outcome listed in the command's `## Unattended mode` section, which the skill follows as this guide's convention (WC-2, [section 7.7](#77-orca-orchestration-commands-as-workers))
- [ ] **Worker contract on every outcome**: the worker contract is written on every outcome, and the skill's own contract file follows the WC-4 two-case rule as this guide's convention ([section 7.7](#77-orca-orchestration-commands-as-workers))
- [ ] **No Orca dispatch**: no call to `worker-start`, `dispatch` or `task-create` in the skill, its refs or scripts (WC-8, [section 7.7](#77-orca-orchestration-commands-as-workers)), and, per the rollout plan (SA-2), no `orca` or `orca-ide` command at all
- [ ] **Outward defaults off**: outward defaults and the skill's own commit or `.dev/tasks` staging step are off under `--unattended` (WC-9, [section 7.7](#77-orca-orchestration-commands-as-workers))
- [ ] **Short blocking waits**: no single blocking Bash wait exceeds the WC-10 limit ([section 7.7](#77-orca-orchestration-commands-as-workers))
- [ ] **Parallel-safe writes**: default write paths carry a timestamp or the caller's slug, and no single-owner shared file is written under `--unattended` (WC-11, [section 7.7](#77-orca-orchestration-commands-as-workers))
- [ ] **Nested invocations propagate**: nested `/sc:` invocations follow the nested propagation rule ([section 7.7](#77-orca-orchestration-commands-as-workers))

---

## 6. Multi-Phase Architecture

### 6.1 Wave System

The wave system enables multi-stage command execution for complex operations. Waves are defined by each command's skill and run when that skill runs; no complexity score, file count or operation count turns them on automatically.

**5-Wave Standard Pattern**:

```text
Wave 0: Prerequisites
  - Validate inputs, check dependencies, create artifact directory
  - Load: SKILL.md only

Wave 1: Analysis
  - Read files, collect evidence, identify patterns
  - Load: refs/analysis-criteria.md (if exists)

Wave 2: Planning
  - Score findings, prioritize actions, create execution plan
  - Load: refs/scoring-protocol.md (if exists)

Wave 3: Generation / Execution
  - Produce artifacts, execute plan, delegate to agents
  - Load: refs/templates.md (if exists)

Wave 4: Validation
  - Verify artifacts, run quality gates, compile return contract
  - Load: refs/validation-rules.md (if exists)
```

**Wave entry/exit criteria**: Each wave has explicit preconditions (what must be ready) and postconditions (what must be produced) before the next wave can begin.

**Wave checkpoint pattern**: Save progress at wave boundaries to the `.superclaude/memory/` files for session resumability.

### 6.2 Compliance Tiers

The `/sc:task` command implements tiered compliance enforcement:

| Tier | When | Steps | Verification | Token Cost |
|------|------|-------|-------------|------------|
| **STRICT** | Security, auth, database, refactor, multi-file | 11 steps | Sub-agent (quality-engineer) | 3-5K |
| **STANDARD** | Add, implement, fix, update | 5 steps | Direct test execution | 300-500 |
| **LIGHT** | Typo, comment, formatting, minor | 4 steps | Skip verification | 0 |
| **EXEMPT** | Explain, search, git status, brainstorm | 2 steps | Skip verification | 0 |

**Priority order**: STRICT > EXEMPT > LIGHT > STANDARD

**Auto-detection algorithm**:

```text
1. Check for user override (--compliance flag)
2. Detect compound phrases (highest priority)
   - "fix security" -> STRICT (security always wins)
   - "quick fix" -> LIGHT (overrides "fix" -> STANDARD)
   - "minor auth change" -> STRICT (auth changes never minor)
3. Score keywords by tier weight
4. Apply context boosters:
   - estimated_files > 2 -> STRICT +0.3
   - security path detected -> STRICT +0.4
   - all doc files -> EXEMPT +0.5
5. Resolve conflicts using priority ordering
6. If confidence < 0.7 -> prompt user for confirmation
```

---

## 7. Integration Patterns

### 7.1 Command + Skill + Agent Composition

The canonical composition pattern (using `/sc:adversarial` as example):

```text
User invokes:  /sc:adversarial --compare file1.md,file2.md --depth deep

Command file:  src/superclaude/commands/adversarial.md
  - Parses flags, validates inputs
  - Activates personas: architect, analyzer, scribe
  - Selects MCP servers: context7

Skill:         src/superclaude/skills/sc-adversarial-protocol/SKILL.md
  - Loads behavioral protocol
  - Loads refs/scoring-protocol.md for Wave 2
  - Loads refs/agent-specs.md for Wave 3

Agents:
  debate-orchestrator  ->  Coordinates 5-step pipeline
    delegates to:
      advocate agents   ->  Dynamic agents per --agents spec
      merge-executor    ->  Follows refactoring plan for final merge

Output:        artifacts/ directory with 6 files + return contract
```

### 7.2 MCP Server Integration

Commands and skills name the MCP servers they use in their own frontmatter, for example `mcp-servers: [auggie, codegraph, context7, tavily]` in `/sc:troubleshoot` and `/sc:reflect`. A skill that needs an MCP tool also lists its exact tool names in `allowed-tools` (for example `mcp__codegraph__codegraph_callers`). There is no framework-wide MCP router, failure counter or fallback table: each primitive says in its own text what it does when a server is missing.

The pattern the 5.0.0 primitives follow:

- **Native floor.** `Grep`, `Glob` and `Read` are always available and stay in place as the floor for definition, caller and file lookups.
- **Tiers above the floor.** codegraph and Auggie are lookup steps placed before the floor step, never instead of it; when either is missing the primitive continues on the floor. Context7 (library docs) and Tavily (web search) are optional steps a primitive uses when its text calls for outside knowledge.
- **Per-command switches only.** MCP flags exist only where a command defines them. `/sc:troubleshoot` and `/sc:reflect` accept `--no-mcp` (native tools only). The `--c7`, `--play` and `--tavily` hints in `~/.claude/CLAUDE.md` are advisory; they are not options every command accepts.

### 7.3 Codegraph in Commands, Skills and Agents

5.0.0 adds codegraph (a local code graph of symbols, callers and files) to commands, skills and agents. Every primitive that uses it follows `~/.claude/CODEGRAPH.md`; read that file before adding a codegraph step. Its rules, in short:

- **Readiness check once per run.** Before the first lookup, check the switch, the session's tool list, the CLI version against the pin and the index state (CODEGRAPH.md section 2). Guard every CLI `codegraph status` with `pgrep -f 'codegraph\.js (init|index)'`; the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead (up to 60 s while an index build runs, where the primitive's Bash allowlist permits `pgrep`).
- **Closed `graph:*` tokens.** When codegraph cannot be used, add exactly one token from the closed list (`graph:absent`, `graph:unlisted`, `graph:disabled`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`, `graph:telemetry_on`) to the primitive's existing `degraded` list and continue on the floor. Invent no new tokens; no token stops a run.
- **Read before cite or edit.** Re-Read a `file:line` range before quoting it or editing it. An empty graph result is not proof of absence ("no callers", "no tests").
- **Exact tool names.** Allowlists name each tool exactly (`mcp__codegraph__codegraph_<tool>`, `Bash(codegraph callers *)`), never a wildcard, and no skill or agent runs a mutating verb. Among primitives, only the user-typed `/sc:graph init` runs `codegraph init`; the session-start hook indexes new checkouts on its own.
- **Switch-off.** `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` turns off codegraph use in primitives (token `graph:disabled`); `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` turns off only the session-start index hook.

### 7.4 Persona Integration

Personas are labels, not switches. They appear in command frontmatter (`personas:`) and in debate agent specs such as `/sc:adversarial --agents opus:architect,sonnet:security`. Nothing activates them automatically and there are no `--persona-*` flags.

| Persona | Typical focus | Primary MCP |
|---------|---------------|-------------|
| architect | "architecture", "design", "scalability" | Context7 |
| frontend | "component", "responsive", "accessibility" | Playwright |
| backend | "API", "database", "service" | Context7 |
| security | "vulnerability", "threat", "compliance" | — |
| analyzer | "analyze", "investigate", "root cause" | Context7 |
| qa | "test", "quality", "validation" | Playwright |
| performance | "optimize", "performance", "bottleneck" | Playwright |
| refactorer | "refactor", "cleanup", "technical debt" | — |
| devops | "deploy", "infrastructure", "automation" | — |
| mentor | "explain", "learn", "understand" | Context7 |
| scribe | "document", "write", "guide" | Context7 |

**Cross-persona collaboration patterns**:

- `architect + performance`: System design with performance budgets
- `security + backend`: Secure server-side development with threat modeling
- `frontend + qa`: User-focused development with accessibility testing
- `analyzer + refactorer`: Root cause analysis with systematic code improvement

### 7.5 Thinking Depth Flags (advisory)

These flags are advisory hints only. No installed core file defines them in 5.0.0 (the file that did was removed), so no command parses them or enforces a token budget or MCP choice; `/sc:business-panel` only notes that it works alongside them. The table records the conventional meaning, not installed behavior:

| Flag | Token Budget (hint) | When to Use | MCP (hint) |
|------|-------------|-------------|-----|
| `--think` | ~4K | Module-level analysis | native |
| `--think-hard` | ~10K | System-wide analysis, architectural | Context7 |
| `--ultrathink` | ~32K | Critical system redesign, legacy modernization | All MCP servers |

### 7.6 Dynamic Context Injection

Skills can use shell preprocessing to inject runtime context:

```markdown
## Repository Context

`!git log --oneline -10`
`!wc -l $(find . -name "*.py" -not -path "*/node_modules/*")`
```

The `!command` syntax executes shell commands and injects their output into the skill context. This enables skills to adapt to the current repository state.

### 7.7 Orca Orchestration: Commands as Workers

Orca can run IronClaude commands as workers under an Orca coordinator (the `/orchestration` skill). The rules live in one installed core file, `~/.claude/WORKER-CONTRACT.md`. This subsection says what they mean for someone writing a command, skill or agent; it summarizes the contract and does not replace it, so read the contract before you rely on a worker rule.

#### How the pieces fit

- A coordinator is a session someone opened by hand, never one that Orca started as a worker. It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report (`~/.claude/WORKER-CONTRACT.md`, opening and section 4).
- A worker is a top-level Claude session that runs one `/sc:` command and reports it with `worker_done`: one command per worker.
- Commands contain no Orca calls (the contract's opening). Per the rollout plan (SA-2), no command, skill or agent runs an `orca` or `orca-ide` command, and none needs Orca to be installed or running.
- The `/orchestration` skill (`~/.claude/skills/orchestration/SKILL.md`) is a discovery stub that loads Orca's version-matched guide from the Orca binary. The IronClaude coordinator rules are in section 4 of `~/.claude/WORKER-CONTRACT.md`. The "Orca coordination" section of `~/.claude/HOW-WE-WORK.md` gives the short routing view.

#### Rollout state

- All 31 converted commands have an `## Unattended mode` section (16 from phase 1, 15 from phase 2), and `UNATTENDED_EXPECT` in `tests/skills/test_worker_contract.py` holds exactly those 31 entries.
- A coordinator puts `--unattended` and one report directory on the 16 phase 1 commands by default; the phase 2 commands join that default after a phase 2 live check passes. It decides by the two-copy test in `~/.claude/WORKER-CONTRACT.md` ("Before the first task-create for a command"), not by a list in this guide. A command gains `--unattended` and its section in the phase that converts its gates, so no command accepts the flag while it can still stop for a human.
- Per the rollout plan (SA-1), without `--unattended` every command behaves exactly as it does today: the same prompts, approval gates, default values, output paths and outward defaults.

#### Deciding whether a new command can be a worker

- The never-as-worker list (`~/.claude/WORKER-CONTRACT.md`, section 1): `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while decision D3 keeps it off workers. These commands are never dispatched as workers and get no `--unattended` mode.
- Per the rollout plan, these are commands whose purpose is orchestration, a conversation with a human, or an outward action that must be authorized, so making them workers would remove their purpose.
- Adding a command to the list is a maintainer edit of `src/superclaude/core/WORKER-CONTRACT.md` and of `NEVER_AS_WORKER` in `tests/skills/test_worker_contract.py`.
- Any other command gets `--unattended` only after each of its gates has an unattended resolution (WC-2).

#### Supervising a Run: `/sc:sweep` (Phase 1)

- **What it is.** `superclaude sweep run` (`src/superclaude/cli/sweep/`) collects, classifies and publishes one read-only report; the `/sc:sweep` command and the `sc-sweep-protocol` skill run it and print the counts and the report path. The coordinator runs it beside its liveness sweep (rule WC-16 in `WORKER-CONTRACT.md`, at most once every 5 minutes). The design is `docs/designs/orchestrator-mode.md`.
- **Package layout.** `probes.py` is the only module that starts a process or reads Orca, git, transcript and contract data: it holds the fixed allowlist of Orca read commands (`ALLOWED_ORCA`, 10 templates) and git read commands, the size limits and the time budget. `classify.py` and `report.py` are pure functions over a `SweepInput` (an import test bans `subprocess`, `click`, `os` and `shutil` in them). `models.py` holds the data shapes and `commands.py` the click command, the argument checks, the publish step and the exit codes.
- **Read-only rule.** Nothing in the package grows a write verb. A later phase that closes or removes things (`/sc:close`) gets its own package, seam and allowlist. `tests/sweep/test_readonly.py` checks, with snapshot diffs, that a run adds no file except the report.
- **Extending the report.** `SECTIONS` in `report.py` is a tuple of 12 functions; a later phase appends a function and does not edit the existing ones. The `Next inspection` text comes from a fixed map keyed by rule name.
- **Tests.** `tests/sweep/` (classification, probes and allowlist, report, command contract, read-only guard, registration), `tests/commands/test_sweep_command.py` (command and skill text, including the narrow chat-summary exception) and the contract pins in `tests/skills/test_worker_contract.py`. The sweep tests never start a process: `tests/sweep/conftest.py` blocks `subprocess.run`, `subprocess.Popen` and `os.system` except for the one `integration` test.
- **Known limits.** See the `Known limits (sweep, Phase 1)` entry in `CHANGELOG.md`.

#### What a command does under `--unattended`

- **Flag parse rule.** `--unattended` counts only as a standalone argument token outside any quoted argument. The same text inside a quoted prompt or topic never switches the mode.
- **Person-mode refusal.** Under `--unattended` every command refuses the flags that exist to involve a human: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test) and `--monitor 1` (pr-submit). The refusal is a stop before any work: the command writes its worker contract with `worker_status: failed` and the refused flag in `reason`, or, when no report directory is known, prints the refusal in chat only (WC-4).
- **WC-2, no waiting for a human.** Under `--unattended` nothing asks the person: the command never calls `AskUserQuestion`, never ends its turn on a chat question or a `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: a documented default, a value the caller passed as a flag, or blocked, where the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question`, then stops.
- **WC-4, the report directory.** The brief passes exactly one report directory. A command uses its own directory-valued `--output` or `--output-dir` as the report directory; `--report-dir <dir>` is for a command without such a flag, or for a brief that does not pass that flag. Passing both, or neither, is refused before any work (WC-4): the command does no work, writes nothing, and prints one fixed error message in chat that names both ways to pass a report directory. With no contract written, the worker reports the run as failed (WC-5).
- **WC-4, the worker contract.** The command writes `<report-dir>/return-contract.yaml` on every outcome (succeeded, failed, blocked and partial), including stops before any other output exists. Its top-level fields are `worker_contract_version` (`"1"`), `worker_status`, `command` (the exact command line), `report_path` (the main human-readable deliverable, if any) and `artifacts` (every other file written), plus `blocked_question` when blocked and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code). `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. `worker_status` is one of `succeeded`, `partial`, `failed` or `blocked`. It is not named `status`, because existing contracts already use `status` with other values.
- **WC-4, the two-case rule.** A command that already writes `return-contract.yaml` in the report directory itself keeps every existing field, including its own `status`, and adds the worker fields beside them. A command whose own contract lives elsewhere leaves that file unchanged, and the worker contract at `<report-dir>/return-contract.yaml` lists it in `artifacts`.
- **WC-4, the status mapping.** A command's own status maps to `worker_status` in five cases: `success` to `succeeded`, `partial` to `partial`, `failed` to `failed`, `stopped-precondition` to `failed` with the precondition in `reason`, and the flag-STOP `blocked` of impact and graph to `failed` with the STOP in `reason`.
- **WC-8, no dispatch from a command.** A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator.
- **WC-9, no outward action.** Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on. The command's own commit step is off too, and the skills that stage `.dev/tasks` themselves defer that staging.
- **WC-10, long waits.** A single blocking Bash call lasts at most 4 minutes. A longer wait (a poll, a long eval) is split into waits of at most 4 minutes so the worker session can heartbeat between the parts.
- **WC-11, parallel-safe writes.** Default output paths carry a timestamp or the slug the coordinator passes, so two workers never write the same file. Single-owner shared files (for example memory keys overwritten whole) are not written under `--unattended`.
- **Nested propagation rule.** When the command invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, it passes `--unattended` and the report directory `<caller report-dir>/nested/<command>-<n>/` if the invoked command accepts the flag at this phase, and lists the nested contract in its `artifacts`. Otherwise that step must be gate-free, or the caller skips it under `--unattended` and records the skip in its contract.

#### The worker session, not the command (WC-7)

WC-7 is a duty of the worker session. The worker runs the command at its own top level, never inside an Agent-tool subagent. Only that session sends lifecycle messages (heartbeat, ask, check, `worker_done`). A command's own Agent-tool fan-out stays as it is (WC-7).

#### The `## Unattended mode` section of a converted command

A converted command carries a short `## Unattended mode` section. Per the contract it lists that command's own gate resolutions and report file and names its nested invocations; as this guide's template convention (Appendix B), it also names its report directory flag and its resume input, if any. It points to `~/.claude/WORKER-CONTRACT.md` and does not restate the shared rules.

From P1, the worker's brief guard checks every copy of the command file it can see (the project `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`) for this section, and copies that disagree make the worker refuse.

#### Skills and agents under a command

- As this guide's authoring convention, skills and agents that run under a command follow that command's `## Unattended mode` section (WC-2), and a skill follows the WC-4 two-case rule for its own contract file.
- Only the top-level worker session sends lifecycle messages, never a subagent (WC-7).
- No agent calls `worker-start`, `dispatch` or `task-create`, because the command it runs under never does (WC-8).
- Under `--unattended` nothing asks the person. Only the worker session may put a blocked question to the coordinator, and only when its brief allows it (WC-2, WC-3).

---

## 8. Development Workflow

### 8.1 Source of Truth

All component source files live in `src/superclaude/`:

```text
src/superclaude/
  commands/           # Command .md files (source of truth)
  skills/             # Skill directories with SKILL.md (source of truth)
  agents/             # Agent .md files (source of truth)
```

The `.claude/` directory in the repo root contains **convenience copies** that Claude Code reads during development. These are synced from `src/superclaude/` and must never diverge.

### 8.2 Sync Workflow

**When editing in `src/superclaude/`** (preferred):

```bash
# 1. Make your changes in src/superclaude/
# 2. Sync to .claude/
make sync-dev

# 3. Verify sync succeeded
make verify-sync
```

**When editing in `.claude/` directly** (iterating with Claude Code):

```bash
# 1. Copy changes back to src/superclaude/ manually
# 2. Verify both sides match
make verify-sync
```

**Always run `make verify-sync` before committing.** CI will catch desync.

### 8.3 Creating a New Component: Full Workflow

```bash
# 1. Scaffold the component
#    Command:
touch src/superclaude/commands/my-command.md

#    Agent:
touch src/superclaude/agents/my-agent.md

#    Skill (simple):
mkdir -p src/superclaude/skills/my-skill
touch src/superclaude/skills/my-skill/SKILL.md

#    Skill (complex with refs):
mkdir -p src/superclaude/skills/sc-my-skill/refs
touch src/superclaude/skills/sc-my-skill/SKILL.md
touch src/superclaude/skills/sc-my-skill/refs/scoring.md

# 2. Write the component (see templates in Section 10)

# 2a. Decide worker eligibility (WC-2, section 7.7)
#    If the command will accept --unattended, write its ## Unattended mode section
#    and add its name to UNATTENDED_COMMANDS in tests/skills/test_worker_contract.py

# 3. Sync to .claude/ for testing
make sync-dev

# 4. Verify sync
make verify-sync

# 5. Test in Claude Code
#    - Invoke the command/agent/skill
#    - Verify triggers activate correctly
#    - Validate output matches expected behavior
#    - Test edge cases and error conditions

# 6. Register the component (commands only)
#    Register it in src/superclaude/core/HOW-WE-WORK.md (a job row, or the Other commands table; see 3.6)

# 7. Commit
git add src/superclaude/commands/my-command.md
git add src/superclaude/agents/my-agent.md  # if applicable
git add src/superclaude/skills/sc-my-skill/  # if applicable
git commit -m "feat: add /sc:my-command with agent and skill"
```

### 8.4 Testing Components

**Manual validation process**:

1. **Install**: Run `make sync-dev` to copy to `.claude/`
2. **Test invocation**: Run the command with its documented arguments (commands run only when invoked; there is no keyword activation)
3. **Verify behavior**: Execute the command and check output matches protocol
4. **Validate structure**: Confirm all expected artifacts are produced
5. **Test edge cases**: Missing inputs, invalid arguments, boundary conditions
6. **Test boundaries**: Verify "Will Not" constraints are respected

**Automated testing expectations** (for complex skills):

- Golden file tests: Compare output against known-good artifacts
- Frontmatter validation: Parse YAML and verify required fields exist
- Adversarial integration tests: End-to-end with real variant files
- Edge case tests: Empty inputs, single file, maximum file count

**Orca readiness checks** (for a command that will run as an Orca worker). These checks relate to WC-2, WC-4 and WC-9 ([section 7.7](#77-orca-orchestration-commands-as-workers)):

- Run `uv run pytest tests/skills/test_worker_contract.py`.
- Its write-verb audit scans the skills, commands and agents under `src/superclaude/` (`AUDIT_ROOTS`) for `git add`, `git commit`, `git push`, `git merge`, `git stash`, `git update-ref`, `git worktree add` and `git worktree remove` (also written as `git -C <path> <verb>`), and for every `gh pr` and `gh api` line, reads included.
- Each matching line needs an entry in `WRITE_VERB_CLASSIFICATION` with a category and a reason. An entry whose line was edited or removed fails `test_classification_table_has_no_stale_entries`.
- A command given an `## Unattended mode` section must be added to `UNATTENDED_COMMANDS`, or `test_no_command_has_unattended_mode_section_after_p0` fails.
- Someone runs the command once without `--unattended` to confirm that its prompts, outputs and outward defaults are unchanged.

### 8.5 Plugin Build Workflow (Future)

The plugin system is planned for v5.0. When available:

```bash
# Build plugin artifacts
make build-plugin        # Validate + assemble into dist/

# Sync to plugin repository
make sync-plugin-repo    # rsync artifacts to ../SuperClaude_Plugin
```

The plugin repo is a **build output**, not a primary editing location. Always edit in `src/superclaude/`.

---

## 9. Best Practices

### 9.1 Command Design

**Do**:

- Start with clear "Required Input" or "Triggers" section
- Define explicit "Will / Will Not" boundaries
- Include 3-5 copy-paste examples covering common use cases
- Declare MCP servers and personas in frontmatter even if empty (`[]`)
- Use the existing command archetypes as starting points
- Decide worker eligibility up front ([section 7.7](#77-orca-orchestration-commands-as-workers))
- When the command accepts `--unattended`, list each gate's resolution, the report file and the report directory flag in `## Unattended mode`, and point to `~/.claude/WORKER-CONTRACT.md` (WC-2, [section 7.7](#77-orca-orchestration-commands-as-workers))

**Do not**:

- Create commands that do everything (single responsibility principle)
- Skip the Boundaries section (leads to scope creep)
- Hardcode file paths (use arguments and `@<path>` references)
- Forget to register the command in the guide (a job row or the Other commands table, see 3.6)
- Call Orca from a command: commands contain no Orca calls (the contract's opening), and WC-8 bars `worker-start`, `dispatch` and `task-create` ([section 7.7](#77-orca-orchestration-commands-as-workers))
- Copy shared contract rules into the command; point to `~/.claude/WORKER-CONTRACT.md` instead ([section 7.7](#77-orca-orchestration-commands-as-workers))
- Leave an outward default on under `--unattended` (WC-9, [section 7.7](#77-orca-orchestration-commands-as-workers))

### 9.2 Agent Design

**Do**:

- Write a concise Behavioral Mindset (1-3 sentences)
- List tools with explanations of WHY each tool is needed
- Include explicit "Does NOT" constraints
- Define concrete output artifact names and formats

**Do not**:

- Create agents that can do anything (constrain the scope)
- Skip the Triggers / when-to-use guidance (delegators and Claude, which choose agents by `description`, then pick the wrong agent)
- Allow agents to both orchestrate AND execute (pick one role)
- Omit the Boundaries section

### 9.3 Skill Design

**Do**:

- **Create a thin command layer** (`commands/<name>.md`, ~80-150 lines) for every skill — flags, usage, examples, boundaries, and an `## Activation` section that invokes the skill. No exceptions, including when refactoring existing skills.
- Keep SKILL.md under 500 lines (behavioral intent only)
- Move algorithms and templates to `refs/` for lazy loading
- Use `allowed-tools` as the primary safety boundary
- Define input contracts with STOP/WARN conditions
- Define return contracts for composability
- Declare per-wave ref loading instructions
- Write the worker contract on every outcome (WC-4, [section 7.7](#77-orca-orchestration-commands-as-workers))
- Follow the WC-4 two-case rule for the skill's own contract file, as this guide's convention ([section 7.7](#77-orca-orchestration-commands-as-workers))
- Split long blocking Bash waits (WC-10, [section 7.7](#77-orca-orchestration-commands-as-workers))

**Do not**:

- Ship a skill without a command in front of it (the command is the user-facing interface; the skill is the behavioral engine)
- Put flags, usage examples, or CLI interface concerns in SKILL.md (belongs in the command)
- Pre-load all refs at skill invocation (violates lazy loading)
- Put implementation details in SKILL.md (belongs in refs/)
- Use unrestricted `Bash` when specific commands suffice
- Create skills without tool allowlisting
- Skip the Will Do / Will Not Do boundaries
- Call `AskUserQuestion` or end on a question under `--unattended` (WC-2, [section 7.7](#77-orca-orchestration-commands-as-workers))
- Write a fixed shared output path or a single-owner shared file under `--unattended` (WC-11, [section 7.7](#77-orca-orchestration-commands-as-workers))

### 9.4 Token Management

- Simple skill (confidence-check): ~50 tokens at session start, ~100 tokens on invocation
- Medium skill (sc-task-protocol): ~50 tokens at start, ~2000 on invocation
- Complex skill (sc-adversarial-protocol): ~50 tokens at start, ~2000 for SKILL.md + ~500-1500 per ref loaded per wave
- Commands: ~80-150 lines loaded on invocation

**Optimization strategies**:

- Use `--uc` (ultra-compressed) mode when context pressure is high
- Skills with refs/ should never load more than 2-3 refs at a time
- Use the progressive disclosure pattern: name/description first, full content on demand
- Consider splitting large skills into multiple focused skills

### 9.5 Error Handling

Skills should define an error handling matrix:

```markdown
## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Missing required input | STOP with clear error message | None |
| File not found | WARN, continue with available files | Skip missing |
| Agent delegation fails | Retry once, then proceed with N-1 agents | Log and continue |
| MCP server unavailable | Continue on the native floor, record it as degraded | Grep / Glob / Read |
| Convergence not reached | REVISE loop (max 2 iterations) | PASS_WITH_WARNINGS |
```

### 9.6 Community Tips (from Research)

These patterns emerged from real-world Claude Code usage:

1. **Keep agents focused**: The most effective agents have a single, well-defined responsibility. Agents that try to do too much produce inconsistent results.

2. **Test with real data**: Use actual project files when testing commands and skills, not synthetic examples. Edge cases in real codebases reveal boundary issues.

3. **Version your specs**: Use the `version` field in frontmatter to track breaking changes to command interfaces.

4. **Use the STOP pattern**: When a command must not proceed without required inputs, use explicit "STOP if missing" language. Claude Code respects these boundaries consistently.

5. **Leverage composition over complexity**: Instead of building one massive skill, compose multiple focused skills through command orchestration. This improves reusability and testability.

6. **Document the "why" in Behavioral Mindset**: The most effective agent definitions explain not just what to do, but the reasoning philosophy. "Coordinate with strict neutrality" is more effective than "manage the pipeline."

7. **Use return contracts for pipeline composition**: When skills need to feed into each other, define explicit return contracts with typed fields. This makes inter-skill composition predictable.

### 9.7 Anti-Patterns

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| Skill without command layer | Skill handles both interface and protocol concerns, creating a monolith; no standardized user-facing entry point | Create a thin command file (~80-150 lines) with flags, usage, examples, boundaries, and `## Activation` handoff to the skill |
| Monolithic SKILL.md | Exceeds token budget, slow loading | Split into SKILL.md + refs/ |
| Unrestricted `Bash` in allowed-tools | Safety risk, unbounded execution | Use `Bash(git *)`, `Bash(wc *)` patterns |
| Agent that orchestrates AND executes | Role confusion, inconsistent behavior | Separate into orchestrator + worker |
| Command without Boundaries | Scope creep, unpredictable behavior | Always include Will / Will Not |
| Pre-loading all refs | Token waste, slow invocation | Load refs per-wave on demand |
| Hardcoded file paths in skills | Breaks portability | Use arguments and relative paths |
| Skipping the routing-table row | /sc:recommend never gets a matched-row answer for the command; it can only find it through live enumeration (slower, with no mandatory flags) | Add the command to a job row in the routing table, or to the "Other commands" table, in src/superclaude/core/HOW-WE-WORK.md |
| No error handling matrix | Silent failures, confusing behavior | Define scenario/behavior/fallback table |
| A step that waits for a human under `--unattended` | WC-2 forbids the question, so the step has no allowed outcome and the worker cannot finish it | Resolve each gate by a documented default, a caller flag or blocked (WC-2, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
| An Orca call inside a command or skill | Per the rollout plan (SA-2), commands run where Orca is absent; per the rollout plan, two controllers compete, which is why orchestrating commands stay with the coordinator | Leave fan-out to the coordinator, which splits the work into separate Tasks; WC-8 bars `worker-start`, `dispatch` and `task-create` ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| A worker contract written only on success | A stop with no contract reads as a failure with no report (WC-5) | Write it on every outcome (WC-4, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
| Reusing `status` for the worker outcome | It clashes with the values existing contracts already give `status` | Use `worker_status` under the WC-4 two-case rule ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| One long blocking Bash wait | The worker session cannot heartbeat during it | Split it into waits within the WC-10 limit ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| A fixed shared output path | Two workers in one worktree overwrite each other's files | Use a timestamp or the slug the coordinator passes, plus the Task's own report directory (WC-11, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
| Copying the contract into a command | The copies drift from the contract | Point to `~/.claude/WORKER-CONTRACT.md` ([section 7.7](#77-orca-orchestration-commands-as-workers)) |

---

## 10. Complete Examples

### Example 1: Simple Command + Agent (Beginner)

A command that generates a project summary report.

**File**: `src/superclaude/commands/summary.md`

````markdown
---
name: summary
description: "Generate a concise project summary with file counts and key metrics"
category: analysis
complexity: simple
mcp-servers: []
personas: [analyzer]
---

# /sc:summary - Project Summary Generator

## Triggers
- User invokes `/sc:summary`
- User asks "summarize this project" or "project overview"

## Usage

```bash
/sc:summary [path]          # Summarize project at path (default: current directory)
/sc:summary --format brief  # One-paragraph summary
/sc:summary --format full   # Detailed summary with metrics
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--format` | `brief` | Output format: `brief` or `full` |
| `--path` | `.` | Project root to analyze |

## Behavioral Flow

1. Scan project directory structure
2. Count files by type (source, test, docs, config)
3. Identify primary language and framework
4. Read README.md and package.json/pyproject.toml if present
5. Generate summary report

## Examples

```bash
/sc:summary                    # Brief summary of current project
/sc:summary --format full      # Detailed summary with metrics
/sc:summary --path ./backend   # Summarize backend subdirectory
```

## Boundaries

**Will:**
- Read project files to generate summary statistics
- Identify languages, frameworks, and project structure

**Will Not:**
- Modify any files
- Access external services or APIs
- Execute project code or tests
````

**File**: `src/superclaude/agents/summary-reporter.md`

```markdown
---
name: summary-reporter
description: Generates structured project summary reports from file analysis
category: analysis
---

# Summary Reporter

## Triggers
- Invoked by `/sc:summary` command
- Project overview or metrics requests

## Behavioral Mindset
Be factual and concise. Report only what can be verified from the file system.
Never speculate about project purpose beyond what README and config files state.

## Tools
- **Read**: Access README, config files, and source files
- **Glob**: Discover files by pattern for counting
- **Bash**: Run `wc -l` for line counts, `find` for file discovery

## Outputs
- Project summary report with:
  - File type breakdown (count and line count)
  - Primary language and framework identification
  - Project structure overview
  - Key configuration details

## Does NOT
- Modify any files
- Execute project code
- Make qualitative judgments about code quality

## Boundaries

**Will:**
- Analyze file structure and generate factual reports

**Will Not:**
- Assess code quality or make recommendations
- Access external services
```

---

### Example 2: Medium Command + Skill with Compliance (Intermediate)

A command that reviews pull request changes with compliance-tiered analysis.

**File**: `src/superclaude/commands/pr-review.md`

````markdown
---
name: pr-review
description: "Review pull request changes with compliance-tiered analysis depth"
category: quality
complexity: moderate
mcp-servers: [context7]
personas: [analyzer, qa, security]
---

# /sc:pr-review - Pull Request Review

## Triggers
- User invokes `/sc:pr-review`
- User asks to "review PR", "review changes", "code review"

## Usage

```bash
/sc:pr-review                           # Review current branch changes
/sc:pr-review --compliance strict       # Force deep security review
/sc:pr-review --focus security,quality  # Focus on specific areas
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--compliance` | `auto` | Review depth: `strict`, `standard`, `light`, `auto` |
| `--focus` | `all` | Review focus: `security`, `quality`, `performance`, `all` |
| `--base` | `main` | Base branch for diff comparison |

## Behavioral Flow

1. Run `git diff <base>...HEAD` to collect changes
2. Classify compliance tier (auto-detect or user override)
3. Activate appropriate personas based on changed file types
4. Execute tier-appropriate review:
   - STRICT: Full security scan + quality analysis + test coverage check
   - STANDARD: Quality analysis + basic security check
   - LIGHT: Syntax and style review only
5. Generate review report with findings and recommendations

## MCP Integration
- **Native reasoning**: Multi-step analysis for STRICT tier
- **Context7**: Framework best practices for pattern validation

## Examples

```bash
/sc:pr-review                                    # Auto-detect tier
/sc:pr-review --compliance strict --focus security  # Deep security review
/sc:pr-review --base integration                  # Compare against integration branch
```

## Boundaries

**Will:**
- Analyze code changes and identify potential issues
- Provide actionable review comments with evidence
- Scale review depth based on compliance tier

**Will Not:**
- Modify any code or auto-fix issues
- Approve or reject the PR (advisory only)
- Access external PR systems or APIs
````

**File**: `src/superclaude/skills/sc-pr-review/SKILL.md`

````markdown
---
name: sc-pr-review
description: "Pull request review with compliance-tiered analysis and multi-persona evaluation"
allowed-tools: Read, Glob, Grep, Bash(git *), TodoWrite, Write
---

<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: moderate
mcp-servers: [context7]
personas: [analyzer, qa, security]
-->

# PR Review Skill

## Purpose
Provide structured, evidence-based pull request reviews with analysis depth
scaled to the risk level of changes. Advisory only -- never modifies code.

## Compliance Tier Classification

### Auto-Detection

<!-- SC:PR-REVIEW:CLASSIFICATION
tier: <detected_tier>
confidence: <score>
changed_files: <count>
security_paths: <boolean>
-->

| Signal | Tier Boost | Amount |
|--------|-----------|--------|
| Changed files > 5 | STRICT | +0.3 |
| Security path detected (auth/, crypto/) | STRICT | +0.4 |
| Test files only | LIGHT | +0.3 |
| Documentation only | LIGHT | +0.5 |
| Single file change | STANDARD | +0.1 |

### Tier Workflows

**STRICT** (11-step):
1. Collect diff
2. Classify changed files by domain
3. Activate security persona
4. Scan for vulnerability patterns (OWASP Top 10)
5. Activate qa persona
6. Analyze test coverage for changed code
7. Activate analyzer persona
8. Review code quality and maintainability
9. Cross-reference with Context7 patterns
10. Compile findings with severity ratings
11. Generate review report

**STANDARD** (5-step):
1. Collect diff
2. Analyze code quality
3. Check for common issues
4. Verify test presence
5. Generate review report

**LIGHT** (3-step):
1. Collect diff
2. Check style and syntax
3. Generate brief report

## Output Format

```markdown
# PR Review: <branch-name>

## Classification
- Tier: <tier>
- Confidence: <score>
- Changed files: <count>

## Findings

### Critical (must fix)
- [ ] <finding with evidence>

### Warning (should fix)
- [ ] <finding with evidence>

### Info (consider)
- [ ] <finding with evidence>

## Summary
<1-3 sentence summary>
```

## Will Do
- Analyze code changes for security, quality, and style issues
- Scale analysis depth to risk level of changes
- Provide evidence-based findings with file:line references

## Will Not Do
- Modify any code or apply fixes
- Access external PR platforms
- Make approval/rejection decisions
````

---

### Example 3: Complex Command + Skill + Agents with Refs (Advanced)

This example shows the full `/sc:adversarial` implementation as it exists in the codebase. This is the canonical reference for building complex multi-agent skills.

**File**: `src/superclaude/commands/adversarial.md`

````markdown
---
name: adversarial
description: "Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts"
category: analysis
complexity: advanced
mcp-servers: [context7]
personas: [architect, analyzer, scribe]
---

# /sc:adversarial - Adversarial Debate & Merge Pipeline

## Required Input
- Mode A: `--compare file1,file2[,...,fileN]` (2-10 existing files)
- Mode B: `--source <file> --generate <type> --agents <spec>[,...]` (generate + compare)

## Usage

```bash
# Mode A: Compare existing files
/sc:adversarial --compare file1.md,file2.md[,...,fileN.md] [options]

# Mode B: Generate variants from source + compare
/sc:adversarial --source source.md --generate <type> --agents <agent-spec>[,...] [options]
```

## Options

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `--compare` | `-c` | Mode A | - | Comma-separated file paths (2-10) |
| `--source` | `-s` | Mode B | - | Source file for variant generation |
| `--generate` | `-g` | Mode B | - | Type of artifact to generate |
| `--agents` | `-a` | Mode B | - | Agent specs: `model[:persona[:"instruction"]]` |
| `--depth` | `-d` | No | `standard` | Debate depth: `quick`, `standard`, `deep` |
| `--convergence` | - | No | `0.8` | Convergence threshold (0.0-1.0) |
| `--interactive` | `-i` | No | `false` | Pause at each step for review |
| `--focus` | `-f` | No | `all` | Focus areas: comma-separated |

## Behavioral Summary

Executes a 5-step protocol producing 6 artifacts:
1. **Diff Analysis**: Structural and content comparison across all variants
2. **Adversarial Debate**: Steelman debate with per-point scoring
3. **Base Selection**: Hybrid quantitative-qualitative scoring with position-bias mitigation
4. **Refactoring Plan**: Actionable merge plan with integration points
5. **Merge Execution**: Produce final merged artifact

## Boundaries

**Will:**
- Compare 2-10 artifacts through structured adversarial debate
- Apply hybrid scoring with position-bias mitigation
- Produce documented merge with full provenance

**Will Not:**
- Participate in debates (delegates to advocate agents)
- Override scoring without documented justification
- Skip protocol steps
````

**File**: `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`

```markdown
---
name: sc:adversarial
description: Structured adversarial debate, comparison, and merge pipeline for 2-10 artifacts
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task
---

<!-- Extended metadata (for documentation, not parsed):
category: analysis
complexity: advanced
mcp-servers: [context7]
personas: [architect, analyzer, scribe]
-->

# Adversarial Debate & Merge Pipeline

## Purpose
Generic, reusable command implementing a structured adversarial debate,
comparison, and merge pipeline.

**Core Objective**: Verify and validate accuracy of statements in generated
artifacts, weeding out hallucinations and sycophantic agreement through
structured adversarial pressure using steelman debate strategy.

## Input Contract

### Mode A: Compare existing artifacts (STOP if invalid)
- `--compare file1,file2[,...,fileN]`: 2-10 existing file paths
- STOP if: fewer than 2 files, more than 10 files, any file not found

### Mode B: Generate + compare (STOP if invalid)
- `--source <file>`: Source file (STOP if not found)
- `--generate <type>`: Artifact type
- `--agents <spec>[,...]`: Agent specifications
- STOP if: source file not found, no agents specified

## 5-Step Protocol

### Step 1: Diff Analysis
Load variants, produce structural comparison.
Output: `artifacts/diff-analysis.md`

### Step 2: Adversarial Debate
Load `refs/agent-specs.md` for advocate prompt template.
Instantiate advocate agents per variant using Task tool.
Execute steelman debate with per-point scoring.
Output: `artifacts/debate-transcript.md`

### Step 3: Base Selection
Load `refs/scoring-protocol.md` for hybrid scoring algorithm.
Execute quantitative metrics (deterministic).
Execute qualitative rubric (LLM with CEV protocol).
Apply position-bias mitigation (dual-pass: forward + reverse).
Output: `artifacts/base-selection.md`

### Step 4: Refactoring Plan
Produce actionable merge plan from debate findings.
Output: `artifacts/refactor-plan.md`

### Step 5: Merge Execution
Delegate to merge-executor agent.
Validate merged output.
Output: `artifacts/merged-output.md`, `artifacts/merge-log.md`

## Delegation Pattern

| Agent | Role | Instantiation |
|-------|------|--------------|
| debate-orchestrator | Coordinates pipeline, does NOT participate | Permanent agent |
| merge-executor | Follows refactoring plan, produces merge | Permanent agent |
| advocate-N | Argues for variant N with steelman evidence | Dynamic per Task |

## Return Contract

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial`, `failed` |
| `merged_output_path` | string | Path to merged artifact |
| `convergence_score` | float | 0.0-1.0 agreement level |
| `artifacts_dir` | string | Path to artifacts directory |
| `unresolved_conflicts` | list | Items not resolved |

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| File not found | STOP with clear error | None |
| Agent delegation fails | Retry once | Proceed with N-1 agents |
| Convergence not reached | REVISE loop (max 2) | PASS_WITH_WARNINGS |
| MCP unavailable | Circuit breaker | Native tools |
| Scoring tie | Tiebreaker protocol | Alphabetical order |

## Output Collision Protocol
If artifact directory exists, append `-N` suffix. Never overwrite.

## Will Do
- Compare 2-10 artifacts through structured adversarial debate
- Apply hybrid scoring with position-bias mitigation (dual-pass)
- Produce documented merge with full provenance annotations

## Will Not Do
- Work with more than 10 variants
- Skip any protocol step
- Override scoring without documented justification
- Participate in debates (strict process management only)
```

**File**: `src/superclaude/skills/sc-adversarial-protocol/refs/scoring-protocol.md`

```markdown
# Scoring Protocol Reference

## Hybrid Scoring Algorithm

Combined score = 50% Quantitative + 50% Qualitative

### Quantitative Metrics (Deterministic)
- Requirement coverage: count(requirements_met) / count(total_requirements)
- Structural completeness: count(sections_present) / count(expected_sections)
- Internal consistency: 1 - (count(contradictions) / count(assertions))
- Unique contributions: count(unique_points) / count(total_points)

### Qualitative Rubric (LLM with CEV Protocol)
Each dimension scored using Claim-Evidence-Verdict format:
- **Claim**: What is being assessed
- **Evidence**: Specific quotes or references from the variant
- **Verdict**: Score (1-5) with justification

Dimensions:
1. Clarity and readability
2. Technical accuracy
3. Actionability
4. Completeness of reasoning

### Position-Bias Mitigation
Execute scoring in TWO passes:
- Pass 1: Variants in original order (A, B, C, ...)
- Pass 2: Variants in reverse order (..., C, B, A)
- Final score: Average of both passes
- Flag any variant with > 15% score variance between passes

### Tiebreaker Protocol
If top variants score within 5% of each other:
1. Prefer the variant with higher unique contribution count
2. If still tied, prefer the variant with fewer contradictions
3. If still tied, prefer alphabetical order (deterministic)
```

**File**: `src/superclaude/skills/sc-adversarial-protocol/refs/agent-specs.md`

````markdown
# Agent Specification Reference

## Agent Spec Format

```
<model>[:persona[:"instruction"]]
```

### Examples
- `opus` -> Opus model, default behavior
- `opus:architect` -> Opus with architect persona
- `opus:security:"Focus on OWASP Top 10"` -> Opus with persona and custom instruction

## Advocate Prompt Template

When instantiating an advocate agent for variant N:

```
You are Advocate for Variant {N}: "{variant_name}"

Your role: Argue FOR this variant using steelman strategy.

Rules:
1. Present the STRONGEST possible case for your variant
2. Address weaknesses honestly but show how they can be mitigated
3. Use specific evidence (quotes, section references) from the variant
4. Never fabricate evidence or misrepresent the variant's content

Output format:
## Strengths (with evidence)
## Weaknesses (with mitigation)
## Unique Contributions
## Response to Opposing Arguments
```

## Advocate Output Format

Each advocate produces a structured argument:

```markdown
## Advocate Report: Variant {N}

### Strengths
- [Strength 1]: "[quote from variant]" (section: X)
- [Strength 2]: "[quote from variant]" (section: Y)

### Weaknesses (with mitigation)
- [Weakness 1]: Can be mitigated by [approach]

### Unique Contributions
- [Point not found in any other variant]

### Response to Opposing Arguments
- Re: [opposing point]: [steelman response]
```
````

**File**: `src/superclaude/agents/debate-orchestrator.md`

```markdown
---
name: debate-orchestrator
description: Coordinate adversarial debate pipeline without participating in debates
category: analysis
---

# Debate Orchestrator

## Triggers
- Invoked by `/sc:adversarial` command to coordinate the 5-step pipeline
- Multi-variant comparison requiring structured debate coordination

## Behavioral Mindset
Coordinate the adversarial pipeline with strict neutrality. Never participate
in debates or advocate for any variant. Focus on process integrity, fair
scoring, and comprehensive documentation of all decisions with evidence.

## Model Preference
Highest-capability model available (opus preferred).

## Tools
- **Task**: Delegate to advocate agents and merge-executor
- **Read**: Load variant files, diff analysis, debate transcripts
- **Write**: Produce scoring artifacts, base-selection report, refactoring plan
- **Glob**: Discover variant files and artifact structure
- **Grep**: Pattern matching for requirement coverage and contradiction detection
- **Bash**: File operations, directory creation

## Responsibilities

1. Parse input mode and validate parameters
2. Dispatch variant generation (Mode B)
3. Coordinate the 5-step protocol with proper data flow
4. Track convergence scoring across debate rounds
5. Execute base selection using scoring algorithm
6. Hand off to merge-executor for Step 5
7. Compile final return contract

## Outputs
- diff-analysis.md
- debate-transcript.md
- base-selection.md
- refactor-plan.md
- Return contract (status, paths, convergence, unresolved conflicts)

## Does NOT
- Generate variants (delegates to specified agents)
- Participate in debates (delegates to advocate agents)
- Execute merges (delegates to merge-executor)

## Boundaries

**Will:**
- Coordinate multi-agent adversarial debate with strict process adherence
- Execute hybrid scoring algorithms with full evidence documentation

**Will Not:**
- Advocate for any variant or inject opinion
- Override scoring results without documented justification
- Skip protocol steps or produce artifacts without required evidence
```

**File**: `src/superclaude/agents/merge-executor.md`

```markdown
---
name: merge-executor
description: Execute merge operations following a refactoring plan produced by debate-orchestrator
category: analysis
---

# Merge Executor

## Triggers
- Delegated by debate-orchestrator after base selection and refactoring plan
- Step 5 of the adversarial pipeline

## Behavioral Mindset
Follow the refactoring plan precisely. Integrate sections from non-base
variants as specified. Document every merge decision with provenance
annotations. Never deviate from the plan without explicit justification.

## Tools
- **Read**: Load base variant, non-base variants, refactoring plan
- **Write**: Produce merged output and merge log
- **Grep**: Verify section integration and reference integrity

## Responsibilities

1. Load the base variant and refactoring plan
2. Apply each integration point from the plan
3. Add provenance annotations to merged sections
4. Verify internal references and cross-section consistency
5. Produce merge log documenting all decisions
6. Return merged output path to orchestrator

## Outputs
- merged-output.md: Final merged artifact with provenance annotations
- merge-log.md: Decision log for every merge action

## Does NOT
- Deviate from the refactoring plan
- Make independent editorial decisions
- Skip provenance annotations

## Boundaries

**Will:**
- Execute merge operations following the refactoring plan exactly
- Document all merge decisions with provenance

**Will Not:**
- Make independent content decisions
- Skip any integration point in the plan
- Produce output without provenance annotations
```

---

## Appendix A: SKILL.md Skeleton Template

Use this template as a starting point for new skills:

```markdown
---
name: <skill-name>
description: "<one-line description>"
allowed-tools: <comma-separated tool list>
---

<!-- Extended metadata (for documentation, not parsed):
category: <category>
complexity: <simple|moderate|advanced|high>
mcp-servers: [<servers>]
personas: [<personas>]
-->

# <Skill Title>

## Purpose
<What this skill does and why it exists.>

## Input Contract

### Required Input (STOP if missing)
- <required-arg>: <description> (STOP if <condition>)

### Optional Input
- <optional-arg>: <description> (default: <value>)

## Protocol

<When the run has --unattended, each step that waits for a human applies the resolution its command's ## Unattended mode section names (WC-2, section 7.7; this guide's convention).>

### Step 1: <Name>
<What happens, what refs to load, what output produced.>
Output: `artifacts/<filename>`

### Step 2: <Name>
<Continue for each step.>

## Delegation Pattern

| Agent | Role | Instantiation |
|-------|------|---------------|
| <agent> | <role> | <permanent or dynamic> |

## Return Contract

<Under --unattended a worker contract is written too; see section 5.9.>

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `success`, `partial`, `failed` |
| <field> | <type> | <description> |

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| <error> | <behavior> | <fallback> |

## Will Do
- <capability 1>
- <capability 2>

## Will Not Do
- <constraint 1>
- <constraint 2>
```

## Appendix B: Command Template

````markdown
---
name: <command-name>
description: "<one-line description>"
category: <category>
complexity: <simple|moderate|advanced|high>
mcp-servers: [<servers>]
personas: [<personas>]
---

# /sc:<name> - <Title>

## Triggers
- User invokes `/sc:<name>`
- <additional trigger conditions>

## Usage

```bash
/sc:<name> [arguments] [options]
```

## Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--flag` | `-f` | `value` | <description> |
| `--unattended` | | off | <Optional row: only if this command accepts unattended mode (WC-2, section 7.7)> |
| `--report-dir` | | none | <Optional row: only if this command has no directory-valued `--output` or `--output-dir`, or the brief does not pass it; both or neither is refused before any work (WC-4, section 7.7)> |

## Behavioral Flow
1. <Step 1>
2. <Step 2>
3. <Step 3>

## MCP Integration
- **<Server>**: <How it is used>

## Examples

```bash
/sc:<name>                    # Basic usage
/sc:<name> --flag value       # With options
```

## Unattended mode
<Optional section: delete it if this command does not accept --unattended.>

Under `--unattended`:
- <Gate name>: <resolution: default <value> | flag <--flag> | blocked with the question>
- Report file: <path of the main deliverable>
- Report directory flag: <--output <dir> | --output-dir <dir> | --report-dir <dir>>
- Nested invocations: <each nested /sc: command and its nested report directory, or none>
- Resume input: <the input a resumed run takes, or none>

Shared rules (WC-4, section 7.7): see `~/.claude/WORKER-CONTRACT.md`.

## Boundaries

**Will:**
- <capability>

**Will Not:**
- <constraint>
````

## Appendix C: Agent Template

```markdown
---
name: <agent-name>
description: <one-line description>
category: <category>
---

# <Agent Title>

## Triggers
- <trigger condition 1>
- <trigger condition 2>

## Behavioral Mindset
<1-3 sentences describing the agent's role, philosophy, and constraints.>

## Model Preference
<model recommendation and why>

## Tools
- **<Tool>**: <Why this tool is needed>

## Responsibilities
1. <responsibility 1>
2. <responsibility 2>

## Outputs
- <artifact 1>: <description>
- <artifact 2>: <description>

## Does NOT
- <negative constraint 1>
- <negative constraint 2>

## Boundaries

**Will:**
- <capability>

**Will Not:**
- <constraint>
```

## Appendix D: File Path Reference

All paths are relative to the SuperClaude Framework repository root:

| Component | Source Location | Installation Target |
|-----------|---------------|-------------------|
| Commands | `src/superclaude/commands/*.md` | `~/.claude/commands/sc/*.md` |
| Agents | `src/superclaude/agents/*.md` | `~/.claude/agents/*.md` |
| Skills | `src/superclaude/skills/*/SKILL.md` | `~/.claude/skills/*/SKILL.md` |
| Core files | `src/superclaude/core/*.md` | `~/.claude/*.md` |
| Worker contract | `src/superclaude/core/WORKER-CONTRACT.md` | `~/.claude/WORKER-CONTRACT.md` |
| Worker contract tests | `tests/skills/test_worker_contract.py` | N/A (not installed) |
| Dev copies | `.claude/commands/sc/`, `.claude/agents/`, `.claude/skills/` | N/A (dev only) |

## Appendix E: Glossary

| Term | Definition |
|------|-----------|
| **Agent spec** | Mini-language format `model[:persona[:"instruction"]]` for dynamic agent creation |
| **Brief guard** | The worker session's check, from P1, that each `Command:` line of its brief matches the `## Unattended mode` state of the command file copies it can see ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **CEV protocol** | Claim-Evidence-Verdict format for qualitative scoring |
| **Compliance tier** | STRICT/STANDARD/LIGHT/EXEMPT classification for task execution depth |
| **Context-Oriented Configuration** | SuperClaude's architecture: .md files that shape Claude Code behavior |
| **Coordinator** | The session, opened by hand, that plans Orca work, creates one Task per unit of work and starts one worker per Task ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **Frontmatter** | YAML metadata block at the top of .md files, delimited by `---` |
| **Lazy loading** | Skills load name/description (~50 tokens) at start; full content on invocation |
| **Lifecycle messages** | The Orca messages that only the top-level worker session sends, never a subagent (WC-7, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **MCP** | Model Context Protocol -- servers that extend Claude Code capabilities |
| **Nested propagation rule** | How a command run with `--unattended` passes the flag and a nested report directory to a nested `/sc:` command ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **Never-as-worker list** | The commands that are never dispatched as Orca workers and get no `--unattended` mode ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **Persona** | Specialized behavior profile (architect, security, qa, etc.) |
| **Position-bias mitigation** | Dual-pass scoring (forward + reverse) to eliminate order effects |
| **Progressive disclosure** | Information loaded incrementally as needed, not all at once |
| **refs/** | Reference files in a skill directory, loaded on-demand per wave |
| **Report directory** | The one directory the brief passes for the worker contract: either the command's own directory-valued `--output` or `--output-dir`, or `--report-dir` for a command without one or a brief that does not pass it; both or neither is refused before any work (WC-4, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **Return contract** | Structured data a skill returns for inter-command composition |
| **REVISE loop** | Max 2 iteration retry for scores in 70-84% range |
| **sc- prefix** | Skill prefix indicating it backs a `/sc:` command |
| **Steelman** | Debate strategy: present the strongest version of each argument |
| **STOP pattern** | Explicit halt condition when required inputs are missing |
| **Unattended mode** | The behaviour a command switches to when its caller passes `--unattended`, with no step that waits for a human (WC-2, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **Wave** | One stage in multi-phase command execution |
| **Worker (Orca)** | A top-level Claude session that an Orca coordinator starts to run one `/sc:` command; not an Agent-tool subagent ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **Worker contract** | The `return-contract.yaml` a command writes in its report directory on every outcome under `--unattended`, following the WC-4 two-case rule ([section 7.7](#77-orca-orchestration-commands-as-workers)) |
| **`worker_status`** | The worker contract's outcome field, kept separate from a command's own `status` (WC-4, [section 7.7](#77-orca-orchestration-commands-as-workers)) |
