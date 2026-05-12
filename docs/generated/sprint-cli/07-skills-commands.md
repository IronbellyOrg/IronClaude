---
title: Sprint CLI - Skill & Command Integration
generated: 2026-04-03
scope: .claude/commands/sc/, .claude/skills/, cli/sprint/process.py
---

# Skill & Command Integration

## Hybrid Architecture

The Sprint CLI is a hybrid system with two distinct layers:

```
+--------------------------------------------------+
|           INFERENCE LAYER (Claude Runtime)        |
|  Slash commands -> Skills -> Agent definitions    |
|  Loaded by Claude Code, executed at inference     |
+--------------------------------------------------+
                    ^
                    | /sc:task-unified prompt
                    |
+--------------------------------------------------+
|       DETERMINISTIC EXECUTOR (Python CLI)         |
|  superclaude sprint run -> subprocess management  |
|  Gate validation, logging, status classification  |
+--------------------------------------------------+
```

**Bridge mechanism**: Sprint CLI spawns Claude subprocesses with prompts that invoke `/sc:task-unified`, causing the inference layer to load and execute the task-unified skill protocol.

## The Critical Bridge: Process -> Prompt -> Skill

**`src/superclaude/cli/sprint/process.py:170-204`**:

```python
def build_prompt(self):
    return f"/sc:task-unified Execute all tasks in @{phase_file} --compliance strict --strategy systematic"
```

This prompt is passed to `claude --print -p <prompt>` via `pipeline/process.py:71-91`, causing:

1. Claude Code loads `/sc:task-unified` command
2. Command activates `sc:task-unified-protocol` skill
3. Skill protocol executes tasks with tier classification
4. Results written to phase output files
5. Sprint executor classifies results via exit code + file parsing

## Sprint-Related Slash Commands

### `/sc:task-unified` (Primary Sprint Command)

**File**: `.claude/commands/sc/task-unified.md`
**Purpose**: Unified task execution with tier classification
**Activation**: `> Skill sc:task-unified-protocol`
**Sprint role**: Injected into every Claude-mode phase subprocess prompt

### `/sc:tasklist` (Upstream: Generates Sprint Input)

**File**: `.claude/commands/sc/tasklist.md`
**Purpose**: Roadmap-to-tasklist bundle generation
**Activation**: `> Skill sc:tasklist-protocol`
**Sprint role**: Produces `tasklist-index.md` + `phase-N-tasklist.md` files consumed by sprint runner

### `/sc:roadmap` (Upstream: Generates Tasklist Input)

**File**: `.claude/commands/sc/roadmap.md`
**Purpose**: Comprehensive roadmap generation
**Activation**: `> Skill sc:roadmap-protocol`
**Sprint role**: Produces roadmap artifacts consumed by tasklist generation

### `/sc:pm` (Orchestration Layer)

**File**: `.claude/commands/sc/pm.md`
**Purpose**: Project Manager agent orchestration
**Activation**: `> Skill sc:pm-protocol`
**Sprint role**: High-level orchestration that may invoke sprint-related commands

### Other Related Commands

| Command | File | Purpose |
|---------|------|---------|
| `/sc:validate-roadmap` | `validate-roadmap.md` | Validate roadmap artifacts |
| `/sc:release-split` | `release-split.md` | Split release into phases |

## Sprint-Coupled Skills

### `sc-task-unified-protocol`

**File**: `.claude/skills/sc-task-unified-protocol/SKILL.md`
**Source**: `src/superclaude/skills/sc-task-unified-protocol/SKILL.md`

- Executes classified tasks (STANDARD/STRICT tiers)
- STRICT path can spawn `quality-engineer` verification agent
- Defines verification routing and escalation behavior
- This is what sprint-invoked Claude sessions execute

### `sc-tasklist-protocol`

**File**: `.claude/skills/sc-tasklist-protocol/SKILL.md`
**Source**: `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`

- Deterministic generation of `tasklist-index.md` + `phase-N-tasklist.md`
- Enforces Sprint CLI compatibility checks
- Post-generation validation/patching stages
- Output structure explicitly designed for `superclaude sprint run`

### `sc-roadmap-protocol`

**File**: `.claude/skills/sc-roadmap-protocol/SKILL.md`
**Source**: `src/superclaude/skills/sc-roadmap-protocol/SKILL.md`

- Produces roadmap artifacts
- References downstream tasklist/sprint flow
- Writes stateful outputs consumed by later pipeline stages

### `sc-pm-protocol`

**File**: `.claude/skills/sc-pm-protocol/SKILL.md`
**Source**: `src/superclaude/skills/sc-pm-protocol/SKILL.md`

- Orchestration layer above sprint
- May invoke sprint-related commands in sequence

## Agent Definitions

### Indirect Usage via Skills

Agent `.md` files in `.claude/agents/` are **not directly imported** by sprint Python code. They are consumed at inference time when skills spawn sub-agents:

- `quality-engineer.md`: Spawned by `sc-task-unified-protocol` for STRICT verification
- RF team agents (`rf-task-builder`, `rf-task-executor`, etc.): Separate orchestration system, not used by sprint runtime

## Data Flow: Upstream -> Sprint -> Downstream

```
Specification Document (PRD/TDD/spec)
  |
  +-> /sc:roadmap (or superclaude roadmap run)
  |     -> extraction.md, roadmap-*.md, ...
  |     -> roadmap.md (merged)
  |     -> .roadmap-state.json
  |
  +-> /sc:tasklist (or superclaude tasklist validate)
  |     -> tasklist-index.md
  |     -> phase-01-tasklist.md, phase-02-tasklist.md, ...
  |
  +-> superclaude sprint run tasklist-index.md
  |     -> discover_phases() reads index
  |     -> parse_tasklist() reads each phase file
  |     -> FOR EACH phase:
  |     |   spawn claude -p "/sc:task-unified Execute tasks in @phase-N..."
  |     |     -> sc-task-unified-protocol SKILL activates
  |     |     -> tasks executed, results written
  |     |   executor classifies results
  |     |   gates validate output quality
  |     |
  |     -> execution-log.{jsonl,md}
  |     -> phase results, diagnostics, KPI report
  |
  +-> .roadmap-state.json influences:
        - Fidelity blocking (force_fidelity_fail option)
        - Auto-wiring of TDD/PRD context in tasklist validate
```

## Installation & Namespace Routing

### Component Installation (`src/superclaude/cli/`)

| Installer | Target | Source |
|-----------|--------|--------|
| `install_commands.py` | `~/.claude/commands/sc/` | `src/superclaude/commands/` |
| `install_agents.py` | `~/.claude/agents/` | `src/superclaude/agents/` |
| `install_skills.py` | `~/.claude/skills/` | `src/superclaude/skills/` |

### Skill Dedup Rule (`install_skills.py`)

If a skill name starts with `sc-` and a matching slash command exists in `commands/sc/`, the skill is marked as "served by /sc: command" and **skipped** during standalone install to avoid duplicate entries.

### Command-Skill Link Resolution

**`src/superclaude/cli/cli_portify/resolution.py`**:
- Parses command activation sections (`> Skill sc:<name>`)
- Resolves command-to-skill links
- Uses command-first policy when ambiguous

## Trigger Model Summary

| Component | Trigger | Automatic? |
|-----------|---------|------------|
| `/sc:task-unified` | Sprint subprocess prompt | Yes (injected by sprint runner) |
| `sc-task-unified-protocol` | Command activation block | Yes (loaded by command) |
| `/sc:tasklist` | User invocation | No (manual, upstream) |
| `/sc:roadmap` | User invocation | No (manual, upstream) |
| `quality-engineer` agent | STRICT task verification | Yes (spawned by skill) |
| Gate validation | Post-step in executor | Yes (automatic) |
