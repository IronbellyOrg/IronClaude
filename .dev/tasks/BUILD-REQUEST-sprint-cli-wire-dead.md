# BUILD_REQUEST — Sprint CLI per-task execution + handoff (Stages 0–3)

## Goal

Author an **MDTM implementation tasklist** for wiring up the Sprint CLI's already-shipped-but-dead
per-task execution path plus a runner-owned typed handoff record. This is a **wiring/hardening job, not
greenfield** (the scaffolding already exists, dead). Cover **Stages 0, 1, 2, 3**. Stage 4 (agent-mail
pilot) and Stage C (coordinator+workers) are **OUT OF SCOPE** (future / deferred per the spec).

## Authoritative source (read these first)

- **Spec:** `.dev/releases/backlog/sprint-cli-architecture-brainstorm/SYNTHESIS.md`
  - §3 is the staged roadmap table. **§6 (6 HIGH resolutions, AUTHORITATIVE) and §7 (MEDIUM/LOW
    resolutions) SUPERSEDE the conflicting §3 stage-table cells.** Build tasks from §6/§7, using §3
    only for the stage skeleton.
  - Source proposals: `agent1-execution-model.md` (execution model), `agent2-handoff-mechanism.md` (handoff).
- **Pre-execution reflection report (full findings + grounding):**
  `.dev/reflect/pre-sprint-cli-arch-20260603002500/REPORT.md` and `artifacts/wave1a-grounding.md`.

## Codebase

`src/superclaude/cli/sprint/` — key symbols (NOT line numbers; see drift note):
`executor.py` (`execute_phase_tasks`, `_run_task_subprocess`, `_parse_phase_tasks`, `_subprocess_factory`,
`setup_isolation`, `IsolationLayers`, `_phase_env_vars`, `aggregate_task_results`, `TurnLedger`),
`config.py` (`_TASK_HEADING_RE`, `_DEPENDENCY_RE`, `SprintConfig`, `task_output_file`),
`process.py` (`build_prompt`, `build_task_context`, `compress_context_summary`),
`logging_.py` (`SprintLogger`, `_jsonl`, `write_task_rerun_complete`),
`checkpoints.py` (atomic temp+replace idiom: `tmp.write_text` → `tmp.replace`),
`models.py` (`TaskResult`, `TaskEntry`, `resume_command`),
`rerun_tasks.py` (`walk_dependencies` / `_dependencies_of` — existing dependency consumer),
`commands.py` (`run()` click options; `--start`/`--end`).

## HARD CONSTRAINTS (from the reflection audit — do not regress these)

1. **Anchor every task on symbol names, not line numbers.** Spec line citations have already drifted
   +4 to +55 lines in this worktree; tasks that cite literal lines will be wrong on day one.
2. **Stage 0 is NOT behavior-neutral (H1).** Wiring `setup_isolation` needs per-path merge semantics:
   Path A KEEPS its phase-scoped `CLAUDE_WORK_DIR` and only ADDS `CLAUDE_SETTINGS_DIR`/`CLAUDE_PLUGIN_DIR`;
   Path B injects the full set. `setup_isolation` likely needs per-phase/per-task parameterization.
3. **Stage 0 gate must test the real (concurrent) failure (H2)** — split into serial isolation smoke +
   a controlled concurrent-spawn corruption repro. Serial reruns alone do NOT prove the corruption fix.
4. **New ledger writer must reconcile with existing `write_task_rerun_complete` (H3)** — freeze both
   event schemas; decide `task_complete` (first-run) vs `task_rerun_complete` discriminator.
5. **Freeze the `HandoffRecord` schema (H4)** — typed, `schema_version`, derived from `TaskResult.to_dict()`
   + `produced_artifacts[]` + `consumed_upstreams[]`. The Stage-1 gate already assumes it's frozen.
6. **Resume contract (H5):** skip predicate = *validated successful* record (not mere existence);
   on-disk key = `handoff/phase-{N}-task-{task_id}.json` (bare task_id collides across phases);
   add a real `--resume <task_id>` CLI option + reconcile the dangling `resume_command()`.
7. **Stage 3 shared-state inventory beyond TurnLedger (H6)** + an `_env_capture`/`_env_builder` test seam
   (the existing `_subprocess_factory` bypasses `env_vars`, so isolation is otherwise untestable);
   **reuse `rerun_tasks.py` dependency primitive**, do not re-derive a DAG walker.
8. **MEDIUM/LOW (§7):** `_jsonl` single-writer invariant for Stages 0-2 + Stage-3 fix covers all writers
   (M2); per-task prompt composition table (M3); flag/config plumbing `--task-parallelism`/`--handoff`/
   `handoff_store` (M4); in-flight-sprint migration/back-compat (M5); heading-regex **warn-only**
   global-routing fix + ≥10-variant corpus (M6); versioned-schema gate (M7); Stage-4 rollback reword
   (L2); crash-consistency test (L3); benchmark/DAG-resume/mail-failover tests (L4); docs tasks (L5);
   reconcile Stage-0 turn-counting with existing **T02.06** (L1).

## Per-stage acceptance gates (from §6/§7)

- **Stage 0:** isolated subprocess still invokes `/sc:task` + hooks + tools + MCPs (smoke); concurrent-spawn
  repro proves isolated settings dirs prevent corruption; per-task `task_complete` events appear; correct
  turn count (not just `!= 0`).
- **Stage 1:** 100% tasks journaled on a real 3-phase sprint; `HandoffRecord` schema versioned + round-trip
  tested; heading-variant corpus passes with zero Path-A reclassification.
- **Stage 2:** mid-phase kill+resume skips only *validated-successful* tasks; back-compat degrade verified.
- **Stage 3:** ≥4 concurrent writers, zero corruption (split per-task-file vs shared-`_jsonl` gates, ≥1000
  runs); measured wall-clock win vs a fixed-duration baseline; DAG+resume correctness.

## Output

Standard MDTM tasklist location (`.dev/tasks/…`). Use UV for any Python the tasks invoke. Test framework:
`uv run pytest`. Tasks must respect the project's source-of-truth rules (edit `src/`, never `.claude/`).
