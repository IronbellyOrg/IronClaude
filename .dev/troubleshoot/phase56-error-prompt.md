# Paste-ready prompt — troubleshoot the phase 5/6 error root cause

Run this in a FRESH Claude Code session at the IronClaude repo root (it diagnoses the
sprint runner code, which lives in this repo; the failing run was against TUIBBS-scp).

---

/sc:troubleshoot "Sprint run phases error without running their tasks — a per-task scheduler/dependency-resolution or phase-aggregation bug, NOT the (already-fixed) concurrency segfault. Evidence from an EXCLUSIVE `superclaude sprint run <index> --start 4 --resume T04.05` against /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/e2eTests/ : Phase 4 fully PASSED (T04.01–05). Phase 5 (Reporting & Registers) started, ran ONLY T05.01 which PASSED (67 turns, 28m, 915KB output), then the phase immediately aggregated to status=error / exit_code=1 WITHOUT ever running T05.02+. Phase 6 (Results→Patch-Release-Spec Pipeline) then phase_completed in 0.0006s with status=error and ZERO task_complete events — no task ran at all. Dependency edges: T05.01 depends_on [T04.01,T04.02,T04.03]; T06.01 depends_on [T05.02, T06.02]. Hypothesis to investigate (do not assume): the per-task scheduler marks a phase 'error' and stops scheduling once a task's dependencies can't be satisfied from the passed-set, and a phase whose tasks are all dependency-blocked aggregates to error in ~0s (phase 6). Possibly interacts with the --start/--resume partial-resume state (cross-phase dependency like T06.01→T05.02 where T05.02 was never scheduled). The phase_complete fields output_bytes=0 / files_changed=0 are a red herring — per-task output files exist on disk. Evidence files: .dev/releases/current/v1-MVP/e2eTests/execution-log.jsonl (phase 5/6 events), results/phase-5-result.json and results/phase-6-result.json (task_results + statuses), results/phase-5-task-T05.01-output.txt (915KB, proves the task ran). Find the root cause of why phase 5 stops after one task and phase 6 runs zero tasks." --type bug --scope src/superclaude/cli/sprint/

---

Notes for the troubleshooter (auggie/serena grounding targets):
- `execute_phase_tasks` and `aggregate_task_results` in src/superclaude/cli/sprint/executor.py (per-task path; how `remaining_task_ids` / unattempted tasks flip a phase to ERROR).
- The dependency walk / scheduler in src/superclaude/cli/sprint/scheduler.py (how a task's depends_on is resolved against the passed-set; what happens when a dependency lives in a prior phase or was skipped by --resume).
- The --start/--resume partial-state handling in src/superclaude/cli/sprint/commands.py + resume/planner.py — whether resuming mid-phase-4 leaves later-phase cross-task dependencies (T06.01→T05.02) unsatisfiable.
- Whether a phase with all-tasks-dependency-blocked SHOULD error in 0s (phase 6) or should be reported differently.
