---
topic: "Thin CLI wrapper for the post-execution /sc:reflect gate (run reflect Tier-2 as a top-level claude -p subprocess from a tasklist's final item, capture the return-contract, write the verdict back)"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-08T18:25:53Z
source_brief: .dev/handoffs/reflect-cli-wrapper-brainstorm-brief.md
---

# Seed Brief: reflect-cli-wrapper

## Problem Statement

Task-builder-generated MDTM tasklists end with a "post-execution reflection gate" (`src/superclaude/skills/task-builder/SKILL.md`, Phase N). Two existing designs both fall short: the **subagent** approach (executor spawns an Agent-tool subagent running `/sc:reflect`) **cannot run Tier 2** because Agent-tool subagents can't nest a skill that itself fans out subagents (memory `reference_subagent_cannot_nest_skill_fanout`) — and Tier 2 (heterogeneous-model reviewers + adversarial merge) is mandatory for medium/complex tasklists; the **HALT** approach (current master #142) is correct and executor-disjoint but fully manual (a human runs `/sc:reflect` in a fresh session). We want the strong Tier-2 audit WITHOUT the manual step: a thin wrapper the final tasklist item shells out to (in a bash window) that runs the full reflect skill as a **top-level `claude -p` subprocess** (escaping the nesting limit), captures the verdict, and writes it back so the tasklist can gate on it.

## Known Context

- Reflect emits a versioned `return-contract.yaml` + `REPORT.md` + `metrics.json` (`sc-reflect-protocol/SKILL.md` §9, §15.1). The wrapper CONSUMES the contract; it does not re-implement reflect.
- Per-process model is supported: `ClaudeProcess` passes `--model` to the `claude` CLI (`src/superclaude/cli/pipeline/process.py:92`).
- Top-level `claude --model` subprocess + window launch is precedented: `src/superclaude/cli/sprint/process.py:162`, `src/superclaude/cli/sprint/tmux.py:193`.
- A CLI subprocess (not an Agent-tool subagent) does NOT hit the nesting limit — this is the whole reason the wrapper works.
- Reflect depth for the gate is derived deterministically from a Tasklist Complexity Score (`task-builder/SKILL.md` "Reflect Depth (Deterministic TCS)"); Tier 2 required for medium/complex.
- The gate item the wrapper plugs into is the master HALT version of `task-builder/SKILL.md` Phase-N reflect gate.
- Env model aliases here are multi-vendor (opus→claude-opus-4-8, sonnet→gpt-5.5, haiku→qwen3.6-plus), so reflect's Tier-2 ensemble is genuinely heterogeneous when those reach the subprocess.

## Constraints

- Thin, NOT a `sc:cli-portify` of reflect: do NOT reimplement reflect's waves/tiers/deviation-taxonomy/promotion-gate in Python. The skill stays the single source of truth.
- Must NOT run reflect inside an Agent-tool subagent (the failure mode being avoided).
- Must NOT auto-commit; default audit-only (`--no-promote`) unless explicitly designed otherwise.
- Must avoid a second behavioral copy of reflect logic that would drift from the skill.
- Reuse existing pipeline/sprint primitives where they fit (process launch, tmux, isolation) rather than inventing new machinery.
- CLAUDE.md rules apply: source-of-truth `src/superclaude/`; never commit `.claude/` mirrors; fork-only PRs.

## Success Criteria

- The final tasklist item triggers a full reflect run (including Tier 2 for medium/complex) with zero human intervention in the common path.
- The reflect run is executor-disjoint (fresh top-level process), not a nested subagent → Tier-2 fan-out actually executes.
- The verdict (`reflect_post: {verdict, run_id, report}`) is written back to the task frontmatter and the tasklist completion-gate consumes it (exit code and/or contract parse).
- Deviations (regressions/grounding-gaps) still HALT for human review; no silent auto-proceed; no auto-commit.
- The wrapper is small, reversible, and keeps the reflect skill as the single source of truth (no logic duplication).

## Open Questions

1. Window mechanic: how does the final tasklist item "open a bash window" — tmux pane (sprint pattern), detached process polled for completion, or a printed single-line command the operator launches? blocking vs detached-and-poll?
2. Wrapper home: new `superclaude reflect` Click subcommand under `src/superclaude/cli/reflect/`, vs a standalone `scripts/` entrypoint — trade-offs for install/discoverability/testing.
3. Input derivation: how to compute `<BASE>..HEAD` (frontmatter `start_commit` / `git merge-base`), `--tasklist`, `--depth` (from TCS), `--executor-model`.
4. Verdict write-back + gate consumption: exit-code contract vs parsing `return-contract.yaml`; how the completion-gate reads `reflect_post` and how deviations route (HALT to Open Questions vs proceed).
5. Headless env: ensuring the `claude -p` subprocess carries Serena/auggie MCP + `ANTHROPIC_DEFAULT_*_MODEL` aliases so Tier-2 + grounding aren't degraded (sprint 4-layer isolation as reference).
6. Runtime/budget: T2 reflect can take 8-15 min; timeout, budget guard, resume.
7. Template integration: does the wrapper REPLACE the master HALT item text in `task-builder/SKILL.md` Phase N, or is it an opt-in alternative (flag/config)? minimal reversible template change.
8. Promotion: default `--no-promote` (audit-only) or wire Wave-7 promotion?
