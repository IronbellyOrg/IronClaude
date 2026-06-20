---
name: brainstorm
description: "Orchestrated multi-agent brainstorm: Socratic dialogue + parallel proposals + adversarial merge"
category: orchestration
complexity: advanced
mcp-servers: [sequential, serena, auggie-mcp, tavily]
personas: [architect, analyzer, scribe]
version: 2.0.0
spec: .dev/eval-workspaces/sc-brainstorm/SPEC.md
---

# /sc:brainstorm — Orchestrated Multi-Agent Brainstorm

## Triggers

- Ambiguous project ideas requiring structured exploration with multiple perspectives
- Requirements discovery where adversarial debate would surface blind spots
- Concept validation needing parallel proposals merged into a unified spec
- Cross-session brainstorming with reproducible artifacts (not just chat output)

## Required Input

A topic string (free-form text). File references via `@<path>` are supported.

```bash
/sc:brainstorm "<topic>"
```

**STOP** on empty topic.

## Usage

```bash
/sc:brainstorm "<topic>" [--proposals N] [--depth quick|standard|deep] \
  [--strategy systematic|agile|enterprise|auto] \
  [--codebase|--no-codebase] [--research light|deep|none|--no-research] \
  [--personas p1,p2,...] [--models opus,sonnet,haiku] \
  [--blind] [--convergence FLOAT] [--interactive] \
  [--handoff none|design|tasklist|task] [--output DIR] \
  [--dry-run] [--resume-from PATH] [--force-stale]
```

## Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `<topic>` | | — (required) | Brainstorm topic (free text or `@file` reference) |
| `--proposals` | `-p` | `3` | Number of parallel proposal variants (2-7). Clamped by depth. |
| `--depth` | `-d` | `standard` | Dialogue + debate depth: `quick`, `standard`, `deep`. Pass-through to `/sc:adversarial --depth`. |
| `--strategy` | `-s` | `auto` | `systematic`, `agile`, `enterprise`, `auto` (heuristic-detected) |
| `--codebase` | | auto | Force codebase context enrichment |
| `--no-codebase` | | `false` | Skip codebase enrichment even if code-related |
| `--research` | | auto | `light`, `deep`, `none` |
| `--no-research` | | `false` | Skip research enrichment |
| `--personas` | | auto | Comma-separated persona list overriding auto-detection |
| `--models` | | `opus,sonnet,haiku` | Model alias list rotated across proposals |
| `--blind` | | `false` | Pass-through to `/sc:adversarial --blind` |
| `--convergence` | | `0.75` | Pass-through to `/sc:adversarial --convergence` |
| `--interactive` | `-i` | `false` | Pause for user input at Socratic + adversarial decision points |
| `--handoff` | | `none` | Post-merge action: `none`, `design`, `tasklist`, `task` |
| `--output` | `-o` | auto | Output directory (default: `.dev/brainstorms/<ts>-<slug>/`) |
| `--dry-run` | | `false` | Execute Waves 0–2B, skip 3-4, print agent-spec preview |
| `--resume-from` | | — | Resume from a saved seed-brief, skipping Socratic dialogue |
| `--force-stale` | | `false` | Allow `--resume-from` even if domain re-classification differs |

**Flag interactions** (enforced in Wave 0):

- `--strategy enterprise` implies `--depth deep` unless overridden
- `--depth quick` caps `--proposals` at 2 (cost guardrail)
- `--depth deep` allows up to 7 proposals
- `--handoff task` requires the task-builder skill installed; `--handoff tasklist` requires sc-tasklist-protocol

## Examples

### Codebase feature discovery

```bash
/sc:brainstorm "add rate limiting to public API endpoints" --depth standard
```

Auto: codebase enrichment via Auggie; 3 proposals across opus/sonnet/haiku with architect/refactorer/backend personas; adversarial debate + merge.

### Deep incident post-mortem

```bash
/sc:brainstorm "deployment broke staging at 3am" --depth deep --strategy systematic
```

Analyzer/devops personas; 5+ proposals; merge emphasizes observability + rollback strategies.

### Product feature with light research

```bash
/sc:brainstorm "AI-powered changelog summarizer" --strategy agile
```

Tavily research enrichment; architect/frontend/scribe personas; product-style requirements output.

### Cross-domain redesign with full handoff

```bash
/sc:brainstorm "redesign error handling across worker pool" \
  --depth deep --proposals 5 --handoff tasklist
```

Codebase + research enrichment; 5 proposals × 3 models; deep debate; merged requirements feed sc:tasklist invocation.

### Blind multi-model comparison

```bash
/sc:brainstorm "consolidate three duplicate auth modules" \
  --depth deep --blind --proposals 4
```

Strips model identity before adversarial scoring to prevent model-bias.

### Dry-run agent-spec preview

```bash
/sc:brainstorm "improve onboarding workflow" --dry-run --strategy enterprise
```

Executes dialogue + enrichment + agent-spec composition; prints the composed --agents string and token-budget estimate; does NOT invoke adversarial.

## Behavioral Summary

5-wave protocol:

1. Wave 0: prerequisites + skill compatibility check
2. Wave 1: Socratic dialogue → seed-brief
3. Wave 2A: parallel enrichment via `/sc:analyze` + `/sc:research`
4. Wave 2B: agent-spec composition + token-budget pre-flight
5. Wave 3: delegate to `Skill sc-adversarial-protocol` with `--generate spec`
6. Wave 4: flag-gated handoff to `/sc:design`, `/sc:tasklist`, or `/sc:task-builder`

Produces a versioned return contract with stable + telemetry blocks.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:brainstorm-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification is in the protocol skill at `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`.

## Boundaries

**Will:**

- Transform ambiguous topics into structured seed briefs via Socratic dialogue
- Orchestrate parallel proposal generation via `/sc:adversarial` (Mode B)
- Auto-detect and invoke codebase + research enrichment when valuable
- Compose model × persona agent-specs across 3 active aliases (opus/sonnet/haiku)
- Hand off merged requirements to `/sc:design`, `/sc:tasklist`, or `/sc:task-builder` (flag-gated)
- Produce a versioned return contract for composability with downstream commands

**Will Not:**

- Re-implement adversarial debate, scoring, or merge logic (delegated to `sc-adversarial-protocol`)
- Auto-invoke `/sc:design` (text recommendation only — design is dialogue-heavy)
- Modify source code or implement features (produces requirements only)
- Activate ANTHROPIC_DEFAULT_* env var swapping (uses 3 active aliases as-is)
- Silently downgrade on missing handoff skills (STOPs and asks user to choose)
- Route empty/malformed adversarial responses to PARTIAL success (FAILs instead)

## Related Commands

| Command | Integration | Usage |
|---------|-------------|-------|
| `/sc:adversarial` | Core delegate — Wave 3 invokes via `Skill sc-adversarial-protocol` | Parallel proposal generation + debate + merge |
| `/sc:analyze` | Enrichment — Wave 2A invokes for codebase context | `--codebase` or auto for code-related topics |
| `/sc:research` | Enrichment — Wave 2A invokes for light research | `--research light` or auto when topic mentions external frameworks |
| `tech-research` (skill) | Enrichment — Wave 2A invokes for deep research | `--research deep` or auto for enterprise/novel topics |
| `/sc:design` | Handoff (text-only) | `--handoff design` prints recommendation; user runs separately |
| `/sc:tasklist` | Handoff (invoked) | `--handoff tasklist` invokes `Skill sc-tasklist-protocol` |
| `/sc:task-builder` | Handoff (invoked) | `--handoff task` invokes `Skill task-builder` with domain-detected template |

## CRITICAL BOUNDARIES

### Stop after merged requirements

This command produces a REQUIREMENTS SPECIFICATION (spec-style format) plus optional downstream artifacts via `--handoff`.

**Explicitly Will NOT**:

- Generate implementation code (use `/sc:implement`)
- Make low-level architectural decisions outside the merged spec (use `/sc:design`)
- Execute tests or deployments

**Output**:

- `merged-requirements.md` — unified specification with frontmatter + structured sections
- `seed-brief.md` — Socratic dialogue output
- `adversarial/` — 6 standard adversarial artifacts (debate-transcript, diff-analysis, etc.)
- `enrichment/` — codebase + research artifacts (if any)
- Return contract (stable + telemetry) for downstream composition

**Next Step**: After brainstorm completes, the merged requirements feed into:

- `/sc:design` for architecture
- `/sc:tasklist` for sprint planning
- `/sc:implement` for direct execution
