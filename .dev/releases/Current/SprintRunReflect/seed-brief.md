---
topic: "Integrate /sc:reflect --mode post --depth deep as a native parallel post-phase hook in superclaude sprint run pipeline"
domain: architecture
strategy: enterprise
depth: deep
proposals_target: 3
handoff_target: tasklist
created: 2026-06-01T00:00:00Z
---

# Seed Brief: Sprint Run Reflect Integration

## Problem Statement

Today, `superclaude sprint run` (src/superclaude/cli/sprint/executor.py) runs a phase loop with three native post-phase hooks: `run_post_phase_wiring_hook` (line 748), `_verify_checkpoints` (line 1811), and `notify_phase_complete` (line 1605). There is also a single end-of-sprint Haiku-driven retrospective at `src/superclaude/cli/sprint/retrospective.py`. Critically, **no `/sc:reflect` invocation exists anywhere in `cli/sprint/`**, so phase-level adherence/regression auditing only happens when an operator manually runs `sc:reflect` from a second terminal driven by a Monitor watching `execution-log.jsonl` for `phase_complete` events.

The operator wants this externalized pattern baked into the executor as a native parallel/background hook firing `/sc:reflect --mode post --depth deep` after each phase, with configurable gate semantics. The reflect run should either (a) appear as a sidecar report with no gate effect or (b) gate the next phase's start. The integration must compose cleanly with existing wiring/checkpoint/notify hooks and with `retrospective.py`.

## Known Context

- **Current pipeline shape** — Single-phase loop in `executor.py` near line 1264; multi-phase loop near line 1329. Both end in `_verify_checkpoints` → `notify_phase_complete` → `run_post_phase_wiring_hook`. No sub-skill spawning today.
- **sc-reflect surface** — `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (1585 lines). UC-1 (pre-execution) and UC-2 (post-execution) modes. T1 (fast single-agent), T2 (parallel heterogeneous reviewers + adversarial merge via `sc-adversarial-protocol`), T3 (task-builder remediation chain). Flags: `--mode post`, `--tier 1|2|auto`, `--depth quick|standard|deep`, `--tasklist`, `--diff`, `--commit-range`, `--task-log`, `--output`, `--budget-remaining N`.
- **Manual orchestration pattern (in flight)** — Terminal A runs `sprint run`. Terminal B runs Claude Code with a Monitor on `execution-log.jsonl`. Each `phase_complete` event triggers an Agent that (a) inventories phase artifacts via `find -newermt`, (b) reads tasklist + roadmap milestone N + result transcripts, (c) executes sc-reflect UC-2 T1 logic, (d) writes `tasklist/validation/sc-reflect-post-phase-N-report.md`.
- **Cost envelope** — T1 reflect ≈ 5-12k tokens/phase; T2 reflect ≈ 35-70k tokens/phase. A 9-phase sprint at T2-deep is 315-630k Claude tokens. A 9-phase sprint at T1-quick is 45-108k tokens.
- **Existing overlap surfaces** — `run_post_phase_wiring_hook` (static wiring check), `_verify_checkpoints` (cp-file adherence check), `retrospective.py` (single end-of-sprint Haiku narrative), `monitor.py`/`tui.py` (display layer), `kpi.py` (metrics surface). All are content-orthogonal or partially-overlapping with what sc-reflect UC-2 verifies.
- **Existing sc-reflect features to leverage** — §14.5 Wave 7 promotion mutation (default-on UC-2 strict-gate), §4.1c auto-wire of `tdd_file`/`prd_file` from `.roadmap-state.json`, §15.1 `metrics.json` + `.dev/reflect/runs.jsonl` cross-run aggregation, §11.5 sampled citation budget, §11.3 calibrator disjoint-set rule, §4 Wave 0 step 0.9 budget pre-flight via `--budget-remaining N`.
- **Asymmetric cost rule (sc-reflect §10.4)** — regression-present should always halt rather than proceed; this is the natural gate signal.

## Constraints

- Brainstorm only — no code changes, no executor.py edits, no skill edits. All artifacts must land under `.dev/releases/backlog/SprintRunReflect/`.
- The integration must not break in-flight sprints (the operator has one running right now).
- The integration must respect the existing token-budget envelope; nested reflect spawns must not be allowed to runaway.
- Background subprocess must be cleanable on sprint Ctrl-C / SIGTERM (no zombie reflect processes).
- The hook MUST be opt-in initially (default state must preserve current behavior) with a clear migration path to opt-out default.
- Compatibility with `--dry-run`, `--resume`, `--profile`, and other existing sprint flags.

## Success Criteria

- Design covers all 7 user-specified topics (T1-T7) with explicit option-set selections.
- Each topic decision is justified against the asymmetric-cost rule (cost of false halt vs. cost of missed regression).
- Migration path is explicit: shipping order (flag → opt-in → opt-out default → mandatory) with rollback story.
- Implementation cost estimated in (files changed, LOC delta, dependency additions, est. dev hours).
- Open questions surfaced and tagged as "needs user resolution before coding" vs. "can be decided at implementation time".
- Output artifacts saved correctly under the user-specified directory.

## Open Questions

- Should the reflect subprocess run as a **separate `claude` invocation** (matching the manual pattern, full skill access, expensive) or as an **in-process Python module call** (cheaper, but requires reflect logic to be Python-callable, which it isn't today)?
- Does the operator want **per-phase fanout for all phases** or **only for phases above a complexity threshold** (e.g., phases that touched > N files, phases with high-tier tasks)?
- If reflect runs in parallel with the next phase, **what happens to the report when phase N+1 modifies files that reflect-N was auditing?** Snapshot-at-launch via git stash? Read-only file references? Accept the race as a known limitation?
- Should reflect findings feed into the **end-of-sprint retrospective.py** as cross-phase trend input, or remain phase-local only?

## Enrichment Context

Evidence verified from local source:

- `executor.py` is 2148 LOC; the phase loop spans roughly L1260-L1620 with hooks at L1289 (single-phase wiring), L1519 (`_verify_checkpoints`), L1596 (`phase_complete` jsonl write), L1605 (`notify_phase_complete`).
- `executor.py:38` imports `notify_phase_complete, notify_sprint_complete` from `.notify` — the existing notification surface is the natural cut-line for reflect dispatch.
- `retrospective.py` is 366 LOC, runs ONCE post-sprint, Haiku-driven — confirmed by user spec.
- `sc-reflect-protocol/SKILL.md` is 1585 lines (user spec said ~1400 — within rounding). Has §4.0 Wave 0 with `--budget-remaining` pre-flight (user spec §T5).
