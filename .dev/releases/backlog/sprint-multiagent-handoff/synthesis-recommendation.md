---
topic: "Sprint multi-agent execution model + inter-agent handoff mechanism"
type: brainstorm-synthesis
pipeline: "Agent1 (exec model) + Agent2 (handoff) -> Agent3 skeptic (sonnet) -> synthesis (opus)"
created: 2026-06-03T00:14:00+00:00
generated_by: "2-parallel-agent-groups (Group 1)"
---

# Sprint Execution Model and Handoff Mechanism — Final Recommendation

## 1. Decision

**Execution model: per-task serial execution via a pluggable StepRunner Protocol** (Agent 1 MODERATE, the only KEPT execution proposal).

**Handoff mechanism: dependency-scoped Markdown context, persisted on disk with atomic writes, injected into each per-task prompt** — built from actual completed upstream `TaskResult` objects inside the per-task loop (revised Agent 2 Lean).

These two are a **coupled pair** because the StepRunner per-task loop is the lifecycle point where completed `TaskResult` objects exist; that is exactly where dependency-scoped Markdown context can be generated and injected. Agent 3 confirmed compatibility in its "strongest combined direction": *"Agent 1 MODERATE serial StepRunner/dependency-aware per-task execution combined with a revised Agent 2 Lean handoff... persisted on disk with simple atomic writes."*

Explicitly **excluded from the build**:
- **Parallelism / swarm** (Agent 1 ROBUST → REVISE-to-later, gated behind unbuilt prerequisites).
- **Mailbox / ack handoff** (Agent 2 Robust → KILLED). The serial model has no concurrent sibling-visibility problem, so a broker adds shared-state failure modes with no speed or correctness benefit.

## 2. Why

Grounded in the verified STEP-0 finding (Agent 3's corrected reading of the source):

- Current execution is **content-gated, not "per-phase default"**: when a phase file contains `### T<PP>.<TT>` headings, `_parse_phase_tasks()` delegates to `execute_phase_tasks()` and the per-task loop runs; the per-phase `ClaudeProcess` path is only reached when no tasks parse (`executor.py:1259-1268`, `1301-1325`). A per-task seam already exists in production.
- That per-task path is **real but unsafe to lean on**: `_run_task_subprocess()` hardcodes `turns_consumed=0`, skips `build_prompt`'s sprint-context header, and skips the `IsolationLayers` env vars (`executor.py:1076-1115`). Worse, the **join point flattens results**: the branch ignores the `remaining` list and collapses task outcomes into phase PASS/ERROR, never calling the modeled `build_resume_output()` (`executor.py:1277-1301`; `models.py:779-813`).
- The richer handoff helpers (`build_task_context`, `get_git_diff_context`, `compress_context_summary`) are **defined but dead in production** — only tests call them (`process.py:257-385`). Production `build_prompt()` injects directory **path references** only (`process.py:147-167`).
- A **swarm is unsafe today**: one in-memory global `TurnLedger` (`executor.py:1198-1203`) and an explicitly single-threaded preliminary-result writer (`executor.py:1969-1972`) mean parallelism requires process-safe accounting, atomic writes, and worktree isolation — i.e., it *is* the product, not optional hardening. Building it now violates scope discipline.

Therefore the highest-ROI, source-safe move is to make per-task execution a first-class, properly-wired StepRunner with a correct resume/budget/observability contract, and to enrich handoff at the one lifecycle point where the data actually exists.

## 3. Surviving Roadmap

Only KEEP/REVISE phases below. All KILLs honored (no mailbox phase appears).

### Phase 1 — Harden the per-task path + define the resume contract (REVISE of Agent 1 LEAN)
**Effort: M (~2-3 days).** Make `_run_task_subprocess()` a first-class peer of the per-phase path: per-task sprint-context prompt, pass `IsolationLayers.env_vars`, parse **real** turn counts from stream-json (replace hardcoded `turns_consumed=0`). **Critically (Agent 3's revision):** change the post-loop contract so `execute_phase_tasks()`'s `remaining` list is consumed and `build_resume_output()` is emitted on partial failure — do not flatten to phase PASS/ERROR.
**Per-phase test strategy:** Unit — assert `(exit_code, turns>0, output_bytes)` parsed from a fixture stream-json; assert isolation env vars present in spawned env. Partial-failure — kill task 3 of 5, assert tasks 1-2 durable, 4-5 in `remaining_task_ids`, and `build_resume_output()` emits correct `--resume {task_id}`. Token-cost — golden test: per-task turns sum == ledger consumed delta.

### Phase 2 — Extract the StepRunner Protocol with golden parity (KEEP, Agent 1 MODERATE P1)
**Effort: M (~3-4 days).** Replace the private `_subprocess_factory` hook with a `StepRunner` Protocol (`run(task, config, phase) -> TaskResult`) and two impls: `PerPhaseRunner`, `PerTaskRunner`; `execute_sprint` selects via the existing `_parse_phase_tasks` gate.
**Per-phase test strategy:** **Golden parity is the gate** (Agent 3's KEEP condition) — assert the per-phase path is byte-for-byte equivalent to today across prompt (`build_prompt`), result-file convention, isolation env vars, monitor state, and ledger accounting. Config-race — assert runners never mutate `SprintConfig`. Protocol conformance for both runners.

### Phase 3 — Dependency-scoped Markdown handoff in the per-task prompt (REVISE of Agent 2 Lean)
**Effort: M (~2-3 days).** Inside the `PerTaskRunner` loop, generate context from **completed upstream `TaskResult` objects** (not the per-phase `build_prompt`, where no task results exist yet). Use `build_task_context` / `compress_context_summary` scoped to that task's transitive dependencies; persist to disk with **atomic write/rename** and inject the path/content into the per-task prompt.
**Per-phase test strategy:** Context-correctness — injected context contains only transitive-dependency `TaskResult`s. Token-cost — golden injected-Markdown size under a hard cap for a 20-task phase; `compress_context_summary` keeps recent N full, older compressed. Atomicity — interrupted write leaves no partial file (rename-after-fsync).

### Phase 4 — Dependency DAG (serial topo) + per-task budget caps (KEEP, Agent 1 MODERATE P2-P3 merged)
**Effort: L (~4-5 days).** Build a DAG from `TaskEntry.dependencies` and execute in **topological order, still one subprocess at a time** (no parallelism). Add per-task budget caps drawn from the global ledger to prevent early-task starvation.
**Per-phase test strategy:** Unit — cycle detection raises; topo order respects deps. Partial-failure — upstream dep FAIL → dependents SKIPPED (not attempted), reported in `remaining`, no wasted launch. Budget — runaway task hits per-task cap, terminated (124) without eating phase budget; ledger solvent for later tasks.

### Phase 5 — E2E + observability parity (KEEP, Agent 1 MODERATE P4)
**Effort: M (~2-3 days).** Wire per-task `OutputMonitor` + tmux tail (closing the real observability gap Agent 3 identified — the per-task path already does minimal TUI updates at `executor.py:993-1000`/`1065-1071`, but not stream monitoring). Per-task entries in `gate-kpi-report.md` and `execution-log.jsonl`.
**Per-phase test strategy:** E2E — mixed tasklist (one per-phase, one per-task) under fake-claude; KPI attributes turns/gate-outcome per task. Observability — one JSONL event per task transition. Regression — suite green, `verify-sync` clean.

**Total effort: ~13-18 days, fully serial.** No swarm, no mailbox, no parallel infrastructure.

## 4. Open Risks (must resolve before build)

1. **Partial-failure recovery contract (blocking Phase 1).** The current per-task branch ignores `remaining` and never emits `build_resume_output()`; phase status is flattened at `executor.py:1277-1301`. If Phase 1 ships subprocess wiring without changing this join-point contract, "per-task recovery" is cosmetic. Define the resume semantics first.
2. **Cost accounting and prompt growth.** Per-task cold starts + repeated dependency-context injection may *increase* tokens, not save them. Require measured before/after budgets and a **hard prompt-size cap** (Phase 3) rather than assuming savings. Per-task context injection can itself trigger prompt-too-long.
3. **State authority across surfaces.** Decide which artifact is authoritative among result files, NDJSON output, and context Markdown **before** Phase 5, or debugging regresses as state fragments. This must be settled as the golden-parity baseline in Phase 2.
4. **Golden-parity coverage (gates Phase 2 KEEP).** The per-phase path has implicit contracts in adjacent code (prompt headers, result-file conventions, isolation env, monitor/tmux). Without golden parity tests, the StepRunner refactor relocates complexity instead of removing it.

## 5. Human-Decision-Required

1. **Stop-after gate.** This roadmap deliberately ends at serial per-task execution. Building swarm/parallelism (the REVISE-to-later Agent 1 ROBUST) requires explicit human authorization **and** a demonstrated wide-independent-phase workload that justifies the process-safe ledger, O_EXCL writes, per-agent worktrees, and multiplexed monitor rewrite. Do not start it speculatively.
2. **Authoritative-state choice (Risk 3).** Which surface is the single source of truth — result files, NDJSON, or context Markdown — is a design call a human should ratify before Phase 5, since it shapes all downstream debugging and KPI reporting.
3. **Prompt-size cap value (Risk 2).** The hard cap on injected dependency-context Markdown is a token-budget/quality tradeoff that needs a human-set threshold, informed by the Phase 3 before/after measurements.
