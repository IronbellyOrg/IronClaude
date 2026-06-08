---
topic: "Design `superclaude sprint rerun-tasks` — granular per-task rerun within a phase"
domain: architecture
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-01T00:00:00Z
---

# Seed Brief: superclaude sprint rerun-tasks (Granular Phase Resume)

## Problem Statement

The sprint executor's recovery surface is currently phase-level: when one or two tasks in a phase fail (transient API outage, proxy down, retry-storm bloat), the only recovery path is `superclaude sprint run --start N --end N`, which re-runs ALL tasks in that phase from scratch.

This was triggered by the MultiModelSwarm sprint (~14h, 7 phases). Phase 7 had 21 tasks; T07.11 produced partial/bloated output (1.03MB transcript indicating retry-storm) and T07.12 produced zero work (14KB transcript: SessionStart hook + 10 `api_retry` events + `ConnectionRefused` + `is_error: true, output_tokens: 0`). The mid-phase checkpoint deliverable `phase-7-cp2.md` was never produced. T07.13–T07.21 all completed cleanly after the proxy recovered. To recover the 2 truly-failed tasks today, the operator must re-execute 19 already-successful tasks.

We need a granular recovery verb that re-runs only the specified failed tasks within a phase, merges the new results back into the canonical results directory and tasklist, and integrates cleanly with the existing `verify-checkpoints --recover` and (planned) `/sc:reflect --mode post` machinery.

## Known Context

**Failure forensics (verified, not trusted from inline summary)**

- Tasklist root: `/config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/tasklist/`
- Phase 7 = 17 regular tasks + 4 checkpoints (T07.01..T07.21)
- T07.10 finished 15:58:41 clean. T07.11 ran 15:58→16:05 with transcript 1.03MB (median ~400KB) — retry-storm bloat, deliverable `commands.py::run_cmd --detached` partially wired, status undetermined. T07.12 ran 16:05:39→16:09:02, transcript 14KB, zero real work, was the cp2 checkpoint. 19m32s transcript gap (proxy down). T07.13 resumed clean.
- Phase 7 aggregate flipped to `ERROR` because `all_passed = all(r.status == TaskStatus.PASS for r in task_results)`.

**Current CLI surface (verified via `--help` and `commands.py` Read)**

| Capability | Surface | Granularity |
|---|---|---|
| Phase-range resume | `sprint run --start N --end M` | Phase-level (rebuilds all tasks in range) |
| Checkpoint-report recovery | `sprint verify-checkpoints --recover` | Markdown-stub regeneration from existing artifacts (no work re-run) |
| Per-task rerun | — | **DOES NOT EXIST** |

**Current data model (verified at `src/superclaude/cli/sprint/models.py`)**

- `TaskStatus` enum at line 39 (PASS/FAIL/INCOMPLETE/SKIPPED).
- `TaskResult` at line 159 (per-task data, in-memory).
- `PhaseStatus` at line 211 (PENDING/SUCCESS/ERROR/HALT).
- `PhaseResult` at line 523 — phase aggregate, persisted to disk.
- **`task_results: list[TaskResult]` exists in `PhaseReport` (line 209) — computed during phase execution, aggregated to `PhaseResult` totals, but NOT persisted to disk in a form the next invocation could read.**

**Reusable infrastructure**

- `checkpoints.py` (408 LOC): `extract_checkpoint_paths()`, `verify_checkpoint_files()`, `build_manifest()`, `recover_missing_checkpoints()` — proves the "parse the tasklist, find specific structural items, manipulate them" pattern already exists.
- Per-task transcripts already written to `results/phase-N-task-T<PP>.<TT>-output.txt` and `-errors.txt`.
- MDTM tasklist files use `### T<PP>.<TT> -- <Title>` heading convention.
- MDTM checkbox semantics: `- [ ]` vs `- [x]`. F1 executor re-reads file to find first unchecked item.

**Composition context**

- `SprintRunReflect` brainstorm (`.dev/releases/backlog/SprintRunReflect/merged-requirements.md`, convergence 0.85) proposes `/sc:reflect --mode post --depth deep` as a native after-phase sidecar with a `reflect_fleet.py` helper. Reflect can identify specific T-IDs with Regression/Drift findings — granular rerun is the recovery vehicle for those findings.
- `TaskQAComparison` (synthesized) established that out-of-context `/sc:reflect --mode post` catches blindspots inline rf-qa misses. Recovery cost today: rerun entire phase. With this feature: rerun named T-IDs.

**Operational constraints (memory-bound)**

- Single-line bash only (terminal can't paste heredocs / multi-line). All paste-ready commands MUST fit one line.
- SoT: edits land in `src/superclaude/cli/sprint/` first, then `make sync-dev`. New module candidate: `rerun_tasks.py`.
- Never stage `.claude/` skill/command output — sync-dev artifact only.

## Constraints

- **Backwards compatible**: existing `sprint run --start --end` semantics unchanged. New verb is additive.
- **No data-model break in v1**: if extending `PhaseResult` with persisted `task_results`, must be additive (new fields with defaults) so older sprint logs still load. Optional path: transcript-inspection only, no schema change.
- **MDTM tasklist preservation**: never silently mutate `phase-N-tasklist.md` without explicit operator opt-in (`--mutate-source` or `--merge-back`).
- **Atomic results**: rerun bundle must be inspectable BEFORE merge-back; `--dry-run` and `--no-merge-back` are first-class.
- **Composition with verify-checkpoints**: rerun re-runs WORK; verify-checkpoints regenerates REPORT stubs. They are orthogonal but must not collide.
- **Single-line CLI invocations**.
- **Token budget envelope**: rerun must NOT silently re-execute already-passed tasks. Filtering is the whole point.
- **Failure-mode honesty**: if the rerun also fails, the operator should not be worse off than before.

## Success Criteria

- **SC1**: `superclaude sprint rerun-tasks <index> --phase 7 --tasks T07.11,T07.12` re-executes ONLY those 2 tasks and produces fresh transcripts + checkpoint report `phase-7-cp2.md` without re-running T07.01..T07.10 or T07.13..T07.21.
- **SC2**: After successful rerun + merge-back, `phase-7-tasklist.md` checkboxes for T07.11/T07.12 read `[x]`, `execution-log.jsonl` records the rerun event, and `verify-checkpoints` reports zero missing artifacts for phase 7.
- **SC3**: `--dry-run` prints the extraction plan (target task IDs, sub-tasklist preview, dependency analysis, deliverable overwrite list) without executing.
- **SC4**: `/sc:reflect --mode post` deviation register can mechanically nominate task IDs for rerun — either by emitting a paste-ready command OR by `rerun-tasks` reading the reflect report directly via `--from-reflect-report <path>`.
- **SC5**: Rerun-of-rerun is bounded. Failure modes (retry already failed, partial deliverable preservation, source tasklist edited mid-flight) have explicit documented behavior — no silent corruption.
- **SC6**: Implementation cost ≤ ~600 LOC delta in `src/superclaude/cli/sprint/` (one new module + minimal edits to `commands.py` and `executor.py`). No new top-level dependencies.
- **SC7**: Round-trip safe — a sprint that ran cleanly and a sprint that ran → failed → rerun-tasks → succeeded must produce equivalent on-disk artifacts (modulo timestamps and a `rerun_history` marker).

## Open Questions (Topics for Adversarial Debate)

The parent prompt enumerates 9 design topics T1–T9. Restated here for the adversarial round:

- **T1 — Task extraction semantics**: how does the verb slice tasks out of `phase-N-tasklist.md`? Regex-parse `### T<PP>.<TT>` headings (A), rebuild synthetic phase from definitions (B), or MDTM template re-render (C).
- **T2 — Index construction**: new sub-index file (A), append virtual phase to original (B), or in-process pass to executor (C).
- **T3 — Dependency handling**: leave deps as-is (A), walk graph and warn (B), or transitive auto-include (C).
- **T4 — Checkbox state mutation**: uncheck-then-recheck originals (A), leave originals untouched and only flip on `--merge-back` (B), or never mutate source (C).
- **T5 — Results merge-back**: where do rerun transcripts/checkpoint reports land, and how is `execution-log.jsonl` updated?
- **T6 — Per-task persistence**: extend `PhaseResult` with persisted `task_results` (A) or operate via transcript-inspection on `results/phase-N-task-*.txt` (B)?
- **T7 — /sc:reflect integration**: reflect emits paste-ready commands (A), or `--from-reflect-report` flag auto-extracts T-IDs from deviation register (B)?
- **T8 — Failure modes**: retry-of-retry semantics; partial-deliverable preservation vs overwrite; original-tasklist-edited-between-runs detection.
- **T9 — Composition with `verify-checkpoints --recover`**: auto-invoke after success (A), or umbrella `sprint repair` verb (B), or keep strictly orthogonal (C)?

## Enrichment Context

**Codebase grounding (verified Reads, primary tier)**

- `src/superclaude/cli/sprint/commands.py` line 16 has `sprint_group` Click group; `run` subcommand starts line 72. Adding `rerun-tasks` requires registering a new `@sprint_group.command("rerun-tasks")` block in the same file (~80-120 LOC).
- `src/superclaude/cli/sprint/executor.py` line 1605-area emits `notify_phase_complete()`; line 296 has `aggregate_task_results()`; line 757 has synthetic-TaskEntry/TaskResult fabrication (already proves we can build a phase pipeline from a subset). Re-using the existing executor entry points for a synthetic single-phase rerun is the right pattern.
- `src/superclaude/cli/sprint/checkpoints.py` already proves "parse tasklist, find specific structural items, manipulate them." Mirror its style for the new module.
- `src/superclaude/cli/sprint/models.py` line 159 `TaskResult`: persistence path-of-least-resistance is extending `PhaseResult` with `task_results: list[TaskResult] = field(default_factory=list)` and a YAML/JSON dump in the phase log. ~30 LOC.

**Sibling brainstorm (SprintRunReflect, convergence 0.85)** proposes `reflect_fleet.py` helper firing after `notify_phase_complete()`. Natural composition: reflect's deviation register identifies T-IDs → rerun-tasks consumes them. Either via paste-ready command output (T7-A, no coupling) or `--from-reflect-report` (T7-B, tight coupling).

**Quality tier**: primary (direct Read of source files + sibling brainstorm artifacts).
