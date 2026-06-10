---
topic: "reflect-wrapper AUTO-FIX evolution (audit-only → audit→fix→verify→promote)"
domain: architecture
strategy: systematic
depth: standard
proposals_target: 1
handoff_target: none
created: 2026-06-10T05:30:00+00:00
adversarial_status: skipped-by-design
adversarial_skip_reason: >
  The 7 driving decisions are pre-decided and grounded (a /sc:reflect --mode pre
  flagged them load-bearing; the brief instructs "do NOT re-litigate"). A
  multi-model adversarial variant-debate exists to converge DIVERGENT ideation;
  here the design is already converged, so the heavy Wave-3 fan-out is skipped
  and merged-requirements is synthesized directly from the grounded brief.
---

# Seed Brief: reflect-wrapper AUTO-FIX evolution

## Problem Statement

The shipped `superclaude reflect run` wrapper is an **audit-only** fail-closed POST
gate: it launches `/sc:reflect --mode post` as a top-level `claude --print`
subprocess (so Tier-2 heterogeneous fan-out works — the entire reason the wrapper
exists, per `reference_subagent_cannot_nest_skill_fanout`), parses
`return-contract.yaml`, derives a 4-state verdict, and writes it back. It HALTs on
any deviation and never repairs.

Two gate sites will consume this engine:

- **O1** — every task-builder tasklist ends with a task running
  `superclaude reflect run <tasklist> --depth deep`.
- **O2** — every sc:tasklist PHASE ends with the same against the phase's file.

The objective is to evolve the wrapper from *audit-only* to
**validate → review → AUTO-FIX/AUTO-APPLY → PROMOTE**, with zero human
intervention on the clean/auto-fixed path, while preserving fail-closed HALT for
anything a human must decide.

## Known Context

- Reflect is **read-only SoT**: its Waves 0–6 never mutate; "Will Not:
  Auto-execute a Tier 3 remediation task — task-builder produces a file, the user
  runs `/task <path>`" (`sc-reflect-protocol/SKILL.md` §Will-Not). The fix layer
  MUST live in the wrapper.
- `--remediate` makes reflect's Wave 6 spawn `rf-task-builder` to *author* a
  corrective MDTM file (`refs/remediation-handoff.md` BUILD_REQUEST).
- Contract v1.3.0 exposes `deviation_count_by_class{authorized,necessary,drift,
  regression}`, `regression_present`, `needs_human_decision` (= grounding-gaps
  non-empty), `user_decision_required`, `remediation_offered`,
  `grounding_gaps_path`, `report_path`, `deviation_register_path`. It does NOT
  yet expose the **path of the authored remediation file** (`remediation_task_path`).
- Promotion adapters are exactly two — `task` (`.dev/tasks/to-do/TASK-*` →
  `done/`) and `sprint-release` (`.dev/releases/current/` → `complete/`). There
  is **no per-phase adapter**.
- The verdict map in `contract.py` already HALTs on `regression`,
  `needs_human_decision`, `user_decision_required`, `drift>0`,
  `unauthorized_deviation`, and routes `degraded`/`blocked` correctly.

## Constraints

- **Thin wrapper.** No reflect-logic duplication (waves/tiers/taxonomy/promotion
  mechanics stay in the skill). No imports from `cli.sprint`/`cli.roadmap`. Zero
  `async`. Only launch path is `ClaudeProcess`.
- **Must land BEFORE the generators' gates go live** (else every generated
  tasklist breaks at "superclaude: no such command"). Mergeable +
  `pipx install --force`-able.
- **Recursion is structural:** an auto-run remediation tasklist carries its OWN
  terminal gate (O1) → infinite wrapper→reflect→remediation→wrapper loop without
  a hard breaker.
- Honors `feedback_human_decision_items_must_halt`: never auto-apply a default
  that ships a change for a human-decision item.

## Success Criteria

- A clean Tier-2 pass auto-promotes (O1) with no human step.
- A purely mechanical deviation set (drift/necessary-only) is auto-repaired,
  re-verified, and then promoted — bounded by N iterations.
- Any regression / needs_human_decision / user_decision / grounding-gap /
  degraded / blocked verdict HALTs (no promote), surfaced to the operator.
- The recursion breaker provably terminates the nested-gate loop.
- A single contract artifact lets the generator worktree wire gates without
  re-deriving any of this.

## Open Questions (resolved in merged-requirements)

- Fix-loop iteration bound N → resolved: default 2 (`--max-fix-iterations`).
- O2 promotion with no per-phase adapter → resolved: O2 forces `--no-promote`;
  promotion is tasklist/release-level only.
- Locating the authored remediation file → resolved: reflect emits
  `remediation_task_path`; wrapper reads it (no newest-dir guessing).
- Recursion breaker mechanism → resolved: `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1`
  self-suppress in the wrapper + generator gate-emission skip.

## Enrichment Context

Grounded directly against the canonical base in worktree `wrapper-onto-master`
(`src/superclaude/cli/reflect/*.py`, `main.py` registration) and the reflect
skill (`sc-reflect-protocol/SKILL.md` §9.1 contract, §Will-Not,
`refs/promotion-adapters.md`, `refs/remediation-handoff.md`). No external research
required; all hard anchors are in-repo and cited in merged-requirements.
