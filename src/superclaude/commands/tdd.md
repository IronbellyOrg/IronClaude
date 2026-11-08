---
name: tdd
description: "Create or populate a Technical Design Document (TDD) for a component, service, or system"
category: documentation
complexity: advanced
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, Agent
mcp-servers: [litellm, context7, auggie]
personas: [architect, analyzer, backend]
---

# /sc:tdd - Technical Design Document Creator

## Required Input

- **Component** (mandatory): The component, service, or system to design (positional argument or description)
- **PRD reference** (optional): A Product Requirements Document to translate into engineering specs
- **Focus areas** (optional): Specific directories, plugins, or subsystems to investigate

## Usage

```bash
# Create a TDD for a component
/sc:tdd <component> [options]

# Create a TDD from a PRD
/sc:tdd <component> --from-prd path/to/PRD.md [options]

# Resume an interrupted TDD session
/sc:tdd --resume path/to/task-file.md

# Create a heavyweight TDD with focused scope
/sc:tdd <component> --tier heavyweight --focus src/services/,src/models/ --output docs/design/
```

### Arguments

| Argument | Position | Required | Description |
|----------|----------|----------|-------------|
| `<component>` | 1 | Yes | Component, service, or system to create a TDD for |

## Options

| Flag | Short | Required | Default | Description |
|------|-------|----------|---------|-------------|
| `<component>` | | Yes | - | Component name or description to design |
| `--tier` | `-t` | No | `standard` | Design depth: lightweight, standard, heavyweight |
| `--prd` | | No | - | Alias for `--from-prd` (PRD file path) |
| `--resume` | `-r` | No | - | Resume from an existing MDTM task file |
| `--output` | `-o` | No | Auto | Output path for the final TDD document |
| `--focus` | `-f` | No | All | Comma-separated directories or files to investigate |
| `--from-prd` | | No | - | PRD file path to translate into engineering specifications |
| `--unattended` | | No | `false` | Worker mode for a coordinator; applies only as a standalone argument token. Behaviour is in `## Unattended mode`; without it nothing changes |
| `--report-dir` | | No | - | With `--unattended`: the directory that holds `return-contract.yaml` (`--output` names the TDD file, not the report directory) |

### Tier Selection Reference

Match the tier to component scope. **Default to Standard** unless the component is clearly documentable with a quick scan of <5 files.

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Bug fixes, config changes, small features (<1 sprint), <5 relevant files | 2–3 | 0–1 | 300–600 |
| **Standard** | Most features and services (1-3 sprints), 5-20 files, moderate complexity | 4–6 | 1–2 | 800–1,400 |
| **Heavyweight** | New systems, platform changes, cross-team projects, 20+ files | 6–10+ | 2–4 | 1,400–2,200 |

## Behavioral Summary

Creates comprehensive Technical Design Documents by researching the actual codebase, verifying every architectural claim through source analysis, and assembling findings into a template-conformant document. The process follows a multi-phase pipeline: scope discovery, deep codebase investigation with parallel agents, independent verification, optional web research, synthesis into template sections, quality assurance, and final assembly. When a PRD is provided, requirements are extracted and traced through to engineering specifications. Output always conforms to the project TDD template. Supports three tiers (lightweight, standard, heavyweight) to match investigation depth to component complexity.

## Examples

### Create a Standard TDD for a Service

```bash
/sc:tdd "agent orchestration system" --focus backend/app/agents/,backend/app/services/
```

### Translate a PRD into Engineering Specs

```bash
/sc:tdd "canvas roadmap" --from-prd docs/product/PRD_ROADMAP_CANVAS.md \
  --tier standard --focus frontend/app/roadmap/
```

### Heavyweight TDD for a New System

```bash
/sc:tdd "shared GPU pool infrastructure" --tier heavyweight \
  --focus ue_manager/,infrastructure/ --output docs/design/TDD_GPU_POOL.md
```

### Lightweight TDD for a Small Feature

```bash
/sc:tdd "notification service" --tier lightweight --focus src/services/notifications/
```

### Resume an Interrupted TDD Session

```bash
/sc:tdd --resume .dev/tasks/to-do/TASK-TDD-20260401-143022/TASK-TDD-20260401-143022.md
```

### TDD from PRD with Custom Output Location

```bash
/sc:tdd "wizard state management" --prd docs/product/PRD_WIZARD.md \
  --tier heavyweight --output docs/wizard/TDD_WIZARD_STATE.md
```

### Prompt Quality Guide

The quality of your prompt directly affects output quality. Providing all four inputs (component, PRD, focus areas, output) produces the most focused, actionable TDD.

**Strong — all four pieces present:**

```bash
/sc:tdd "agent orchestration system" \
  --from-prd docs/docs-product/tech/agents/PRD_AGENT_SYSTEM.md \
  --focus backend/app/agents/,backend/app/services/agent_service.py,backend/app/workers/ \
  --output docs/agents/TDD_AGENT_ORCHESTRATION.md
```

**Strong — clear scope + PRD + output type:**

```bash
/sc:tdd "canvas roadmap" \
  --from-prd docs/docs-product/tech/canvas/PRD_ROADMAP_CANVAS.md \
  --tier standard --focus frontend/app/roadmap/
```

**Strong — design from scratch with clear scope:**

```bash
/sc:tdd "shared GPU pool" --tier heavyweight \
  --focus ue_manager/,infrastructure/,backend/app/services/streaming_service.py
```

**Weak — topic only (will work but produces broader, less focused results):**

```bash
/sc:tdd "wizard"
```

**Weak — no context (agents won't know what to focus on):**

```bash
/sc:tdd
```

## Skill Invocation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill tdd

Do NOT proceed with protocol execution using only this command file.
The full behavioral specification, tier logic, and execution pipeline are defined in the skill.

(Heading uses `Skill Invocation` rather than `Activation` because the paired skill directory is named `tdd` — predating the `sc-<name>-protocol` naming convention enforced by `make lint-architecture` Check 1. Renaming the skill would break tests at `tests/cli/test_tdd_extract_prompt.py`, `tests/roadmap/test_prd_prompts.py`, and downstream task files; the runtime directive still works.)

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:tdd` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (the component is a quoted argument); otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` names the TDD file). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` TDD file. `artifacts` lists the MDTM task folder files the run wrote; paths git ignores are left out (WC-4).
- **Person-mode flags.** None is refused. `--resume <task-file>` resumes as today.
- **Gates.** Under `--unattended` a bare topic resolves as blocked (a topic or vague request with no component detail), with the clarification template in `blocked_question`; a TDD that is already complete resolves as blocked, with the update-or-re-run question in `blocked_question`. The nested `/task` call receives `--unattended` after the task file path, and its two ask-the-user points come back as a question that tdd writes as a blocked contract. The build request's cleanup question defaults to keeping the sources, and the archive confirmation defaults to not archiving. The task builder, told the caller is unattended, leaves `.dev/tasks` staging to the coordinator and skips its CLI-mode reflect gate, recording `reflect gate skipped (unattended)` in the task log. There is no other gate.
- **Nested invocations.** None with a report directory: the `task` skill and the builder agent write no worker contract, so no nested directory is created.
- **Outward actions.** It pushes and commits nothing and does not stage `.dev/tasks`; the coordinator stages it (WC-9).

## Boundaries

**Will:**

- Research actual codebase to produce evidence-based technical designs
- Translate PRD requirements into traceable engineering specifications
- Create template-conformant TDD documents at three depth tiers
- Spawn parallel investigation agents for thorough coverage
- Resume interrupted sessions from persisted task files
- Verify architectural claims through source code analysis

**Will Not:**

- Implement the designed system (use `/sc:implement` for implementation)
- Create product requirements (use `/sc:prd` for PRD creation)
- Make architectural decisions without codebase evidence
- Produce TDDs from memory or speculation without source verification
- Skip investigation phases to produce faster but shallower output
- Modify existing source code during the design process

## Related Commands

| Command | Integration | Usage |
|---------|-------------|-------|
| `/sc:prd` | PRD feeds TDD requirements | `/sc:tdd "component" --from-prd PRD.md` |
| `/sc:design` | Complementary system design | Use for architecture diagrams and API specs |
| `/sc:workflow` | Post-TDD implementation planning | Generate implementation workflow from TDD |
| `/sc:brainstorm` | Pre-TDD requirements discovery | Clarify requirements before writing a TDD |
