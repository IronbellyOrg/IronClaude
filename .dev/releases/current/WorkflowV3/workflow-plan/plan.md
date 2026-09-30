---
schema: workflow-plan/1.0
source: .dev/releases/current/WorkflowV3/SPEC.md
strategy: systematic
depth: standard
slug: workflow-v3
---

# Plan: implement `/sc:workflow` v3

## Goal

Replace the monolith command with command + `sc-workflow-protocol` + five refs + one grep test. Plan-only product. Sync via `make sync-dev`.

## Context

- SoT: `SPEC.md` + `merged-requirements.md` in this release dir.
- Peer shape: `src/superclaude/commands/implement.md`.
- Do not add agents, CLI, MDTM forks, MCP lists.

## Phases

### P1 — Thin command
- **Goal**: Rewrite `src/superclaude/commands/workflow.md` (80–150 lines): flags, STOP list, Activation, Related Commands. No wave steps. `mcp-servers: []`. No `**Execute**`.
- **Inputs**: SPEC.md §3; implement.md as template.
- **Outputs**: `src/superclaude/commands/workflow.md`
- **Checkpoint**: file contains `Skill sc:workflow-protocol`; usage has `quick|standard|deep`; banned flags documented.
- **Deps**: none

### P2 — Skill SKILL.md
- **Goal**: Add `src/superclaude/skills/sc-workflow-protocol/SKILL.md` with waves 0–4 (Parse, Structure, Synthesize, Gate, Contract). allowed-tools without Task. ≤500 lines.
- **Inputs**: SPEC.md §4; brainstorm-protocol SKILL as wave-table shape only.
- **Outputs**: SKILL.md
- **Checkpoint**: each wave has purpose, refs, entry, exit, STOP.
- **Deps**: P1 (Activation name must match)

### P3 — Five refs
- **Goal**: Write the five refs named in SPEC §2.
- **Inputs**: merged-requirements FR-003–013; SPEC STOP table.
- **Outputs**:
  - `refs/input-parse.md`
  - `refs/phase-templates.md`
  - `refs/overlap-routing.md`
  - `refs/quality-gates.md`
  - `refs/return-contract.md`
- **Checkpoint**: SKILL.md only names these files; STOP codes not duplicated as a sixth ref.
- **Deps**: P2

### P4 — Test + sync
- **Goal**: One pytest grepping Activation, five refs, no Execute step. `make sync-dev`.
- **Inputs**: P1–P3 files.
- **Outputs**: `tests/` file (smallest existing command-skill grep pattern); `.claude/` via sync-dev only.
- **Checkpoint**: `uv run pytest` on that file passes; `make verify-sync` clean for these paths.
- **Deps**: P3

## Execution order

P1 → P2 → P3 → P4 (serial; names must match).

## Out of scope this plan

Resume, Task fan-out, new agents, invoking tasklist on plan.md.
