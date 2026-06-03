---
topic: "Feasibility study + high-level roadmap for porting/recreating the SuperClaude CLI orchestration pipeline (sprint run, roadmap run, pipeline, tasklist) onto Mastra + Backlog.md + Beads (Stack D), as a multi-tenant orchestration layer for the company, maximizing reuse of skills/agents/harness components."
domain: architecture
strategy: enterprise
depth: deep
proposals_target: 4
handoff_target: none
created: 2026-06-02T21:31:00+00:00
---

# Seed Brief: mastra-beads-port-feasibility

## Problem Statement

SuperClaude/IronClaude currently ships a ~65K-LOC Python orchestration layer (`src/superclaude/cli/`) that drives Claude Code as a worker. The flagship surfaces are:

- **`superclaude sprint run <tasklist-index.md>`** — executes MDTM task phases by spawning `claude --print --verbose --output-format stream-json` subprocesses, with checkpoints, tmux session management, KPI/retrospective capture, diagnostics, and recoverable per-task reruns.
- **`superclaude roadmap run <spec.md>`** — the largest subsystem (~16.7K LOC): spec parsing, adversarial generation, convergence scoring, fidelity/structural/semantic gates, obligation scanning, cosmetic + semantic remediation, certification.
- **`superclaude pipeline`** — FMEA classification, dataflow graphs, invariant passes, guard analysis, conflict detection, verification emission (~6.7K LOC).
- **`tasklist` / `task_builder` / `audit` / `eval` / `prd`** — supporting generators and validators.

The execution substrate is a **subprocess driver over the `claude` CLI** (`pipeline/process.py::ClaudeProcess`, extended per-domain), parsing `stream-json`, enforcing `max_turns`, model selection, and permission flags. The *intelligence* lives in on-disk **skills** (`src/superclaude/skills/*/SKILL.md`), **agents** (`src/superclaude/agents/*.md`), **commands** (`/sc:*`), and **hooks** — a portable knowledge harness — while the *orchestration* (gates, waves, checkpoints, convergence) is portable Python coupled to the Claude Code CLI as its only runtime.

The goal is to evaluate porting/recreating this pipeline onto **Stack D = Mastra (agent/workflow runtime) + Backlog.md (markdown task-of-record + MCP) + Beads (issue/dependency graph)** to obtain a **multi-tenant, multi-user, multi-tool orchestration layer** for the whole company — not a like-for-like rewrite, but a deliberate replatforming that preserves the harness IP (skills/agents/gates) where possible.

## Known Context

- **Coupling point**: orchestration ↔ runtime is the `ClaudeProcess` subprocess boundary (`['claude','--print','--verbose']`, `output_format="stream-json"`, `max_turns`, `model`, `permission_flag`). This is the single seam a Mastra port must replace.
- **Portable IP** (runtime-agnostic, mostly Markdown/YAML + pure-Python logic): skills, agents, commands, hooks, gate logic (convergence/fidelity/FMEA/invariants), MDTM task format, checkpoint/retrospective models.
- **Claude-Code-specific** (must be re-homed): CLI subprocess lifecycle, stream-json parsing, tmux session driver, `/sc:*` slash-command dispatch, permission-mode flags, Claude-Code hook events.
- **Stack D component facts (to verify in research)**: Mastra 1.0.0 (Jan 2026, Apache-2.0 core + EE license for `ee/` incl. Studio auth/RBAC); Backlog.md (MIT, MCP alignment via BACK-407); Beads v1.0.0 (Apr 2026, MIT, `bd` CLI w/ JSON, SQLite or Dolt server-mode). Multi-tenant auth/RBAC is the EE-licensed surface of Mastra Studio.
- **Functional overlap risk**: Backlog.md (markdown task tree) and Beads (issue/dependency graph) overlap; one must be primary work-of-record, the other memory.
- Current model aliases in this env: opus=`claude-opus-4-8`, sonnet=`gpt-5.5`, haiku=`qwen3.6-plus` (heterogeneous — relevant because a multi-tool layer must drive non-Claude models, which the current `claude`-CLI driver cannot).

## Constraints

- This is a feasibility study + high-level roadmap, **not** an implementation. Output is requirements/analysis only.
- Treat as a **major replatforming**, not an incremental upgrade — do not assume it is simple or even net-positive; "do not port" must remain a live option.
- Must explicitly assess **reuse vs. rewrite** for each harness component class (skills, agents, commands, hooks, gates, task format).
- Must address **multi-tenancy / multi-user / RBAC** as a first-class requirement (the strategic driver), including Mastra EE licensing implications.
- Must drive **multiple agent CLIs/models** (Claude Code, Cursor, Codex, Gemini, Copilot), not just `claude` — the current single-CLI driver is a hard limit.
- Verify version/maturity/licensing claims against current (June 2026) sources; flag stale or unverifiable claims.

## Success Criteria

- A defensible **go / no-go / hybrid** recommendation with V/C/L/R-style scoring and explicit risk register.
- A **component-by-component port matrix**: reuse-as-is / adapt / rewrite / drop, for each orchestration subsystem and each harness class.
- A **phased high-level roadmap** (strangler-fig-style) with milestones, sequencing, dependencies, and rough complexity/effort bands — not story-point estimates.
- Explicit treatment of the **runtime seam** (replacing `ClaudeProcess`/stream-json with Mastra workflows/agents) and the **task-of-record** decision (Backlog.md vs Beads vs both).
- A **risk register** covering license drift (Mastra EE), Backlog/Beads overlap, loss of Claude-Code-native features (hooks, slash commands, permission modes), and multi-tenant security.

## Open Questions

- Does Mastra's workflow/step model express the sprint **wave → checkpoint → wave** and roadmap **gate/convergence** loops natively, or must they be rebuilt as Mastra control flow?
- Can skills/agents (Markdown knowledge artifacts) be consumed by Mastra agents without a Claude-Code runtime, or do they need translation to Mastra agent/instruction format?
- Is the multi-tenant requirement satisfiable on Mastra OSS, or does it force the EE license (and what does that cost/lock-in look like)?
- Backlog.md vs Beads as primary work-of-record — which maps better to MDTM tasklists + the dependency edges the roadmap/pipeline gates need?
- What is irreducibly lost by leaving Claude Code (hooks, `/sc:*` dispatch, permission modes, freshness enforcement) and what is the mitigation?
