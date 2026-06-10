# Brainstorm brief — thin CLI wrapper for the post-execution `/sc:reflect` gate

Design the spec for a **thin CLI wrapper** that lets a task-builder MDTM tasklist fire its final post-execution `/sc:reflect --mode post` gate **autonomously** — by opening a bash window that shells out to the wrapper, which runs the FULL reflect skill (including Tier 2) as a **top-level `claude -p` subprocess**. This is deliberately NOT a full `sc:cli-portify` of the reflect logic.

## Problem statement

Task-builder-generated tasklists end with a "post-execution reflection gate" item (`src/superclaude/skills/task-builder/SKILL.md`, "Phase N … Independent post-execution reflection gate"). Two existing designs both fall short:

- **Subagent design (rejected):** have the executor spawn an Agent-tool subagent that runs `/sc:reflect`. This **cannot run Tier 2** — Agent-tool subagents can't nest a skill that itself fans out subagents (project memory `reference_subagent_cannot_nest_skill_fanout`). For medium/complex tasklists we REQUIRE Tier 2 (heterogeneous-model reviewer ensemble + adversarial merge), so this is a non-starter.
- **HALT design (current master, #142):** the executor writes `reflect_post: PENDING`, STOPs, and surfaces a paste-ready `/sc:reflect` command for a human to run in a NEW Claude session. Correct and disjoint, but fully manual.

**Goal:** keep the strong, executor-disjoint Tier-2 audit but remove the human-in-the-loop step — by having the final tasklist item open a bash window that calls a thin wrapper, which runs reflect as a fresh top-level OS process (no Agent-tool nesting → full Tier 2 works), captures the verdict, and writes it back so the tasklist can gate on it.

## The concept (what to spec)

A thin wrapper — e.g. a `superclaude reflect run` Click subcommand (or a `scripts/` shell/python entrypoint) — that:

1. Resolves inputs (diff range, tasklist path, depth, executor-model) from the task file / git.
2. Invokes `claude -p "/sc:reflect --mode post …"` as a **single top-level subprocess** (NOT an Agent-tool subagent), so the reflect skill's own Tier-2 fan-out runs normally.
3. Reads reflect's emitted `return-contract.yaml` (+ REPORT.md / metrics.json) from the reflect `--output` dir.
4. Writes the verdict back to the task frontmatter `reflect_post: {verdict, run_id, report}` and exits with a status the tasklist completion-gate can consume.
5. Preserves reflect's HALT-on-deviation behavior (regressions/grounding-gaps still surface for human review; no auto-commit).

## Hard anchors (grounded — brainstorm codebase-enrichment should confirm these)

- Reflect emits a versioned `return-contract.yaml` + `REPORT.md` + `metrics.json` (`src/superclaude/skills/sc-reflect-protocol/SKILL.md` §9 output contract, §15.1 metrics). The wrapper consumes the contract; it does NOT re-implement reflect.
- Per-process model is already supported: `ClaudeProcess` passes `--model` to the `claude` CLI (`src/superclaude/cli/pipeline/process.py:92`). Precedent for a headless reflect subprocess.
- Top-level `claude --model` subprocess + window launch is precedented: `src/superclaude/cli/sprint/process.py:162` and `src/superclaude/cli/sprint/tmux.py:193`.
- The nesting limitation that kills the subagent design — and why a CLI subprocess escapes it — is project memory `reference_subagent_cannot_nest_skill_fanout` ("CLI subprocesses (sprint run) work fine in a subagent").
- Reflect depth for the gate is derived deterministically from a Tasklist Complexity Score (`task-builder/SKILL.md` "Reflect Depth (Deterministic TCS)") — Tier 2 is required for medium/complex.
- The gate item the wrapper plugs into is the master HALT version of `task-builder/SKILL.md` Phase-N reflect gate.

## Scope boundaries (NON-goals — keep it thin)

- NOT a `sc:cli-portify` of reflect: do NOT reimplement reflect's waves/tiers/deviation-taxonomy/promotion-gate in Python. The skill stays the single source of truth.
- Do NOT run reflect inside an Agent-tool subagent (the failure mode being avoided).
- Do NOT auto-commit, and do NOT auto-promote unless explicitly designed (default audit-only / `--no-promote`).
- Avoid creating a second behavioral copy of reflect logic that would drift from the skill.

## Open questions for the brainstorm to resolve

1. **Window mechanic:** how does the final tasklist item "open a bash window" — a tmux pane (sprint pattern), a detached background process polled for completion, or a printed single-line command the operator launches? Detached-and-poll vs blocking?
2. **Wrapper home:** new `superclaude reflect` Click subcommand under `src/superclaude/cli/reflect/`, vs a standalone `scripts/` entrypoint. Trade-offs for install/discoverability.
3. **Input derivation:** how to compute `<BASE>..HEAD` (frontmatter `start_commit` / `git merge-base`), `--tasklist`, `--depth` (from TCS), and `--executor-model` for the subprocess.
4. **Verdict write-back + gate consumption:** exit-code contract vs parsing `return-contract.yaml`; how the tasklist completion-gate reads `reflect_post` and how deviations route (HALT to Open Questions vs proceed).
5. **Headless env:** ensuring the `claude -p` subprocess has Serena/auggie MCP + the `ANTHROPIC_DEFAULT_*_MODEL` aliases so Tier-2 fan-out and grounding aren't degraded (sprint's 4-layer subprocess isolation as a reference).
6. **Runtime/budget:** T2 reflect can take 8-15 min; timeout, budget guard, and resume behavior.
7. **Template integration:** does the wrapper REPLACE the master HALT item text in `task-builder/SKILL.md` Phase N, or is it an opt-in alternative path (e.g. a flag/config)? What's the minimal, reversible template change?
8. **Promotion:** run with `--no-promote` (audit-only) by default, or wire Wave-7 promotion?

## Desired output

`merged-requirements.md` — a unified spec for the thin wrapper (problem, FRs/NFRs, the window-mechanic + write-back design, scope boundaries, resolved open questions, integration plan into the task-builder Phase-N gate), ready to feed `sc:roadmap` or `sc:implement`. Stop at the merged requirements (`--handoff none`).
