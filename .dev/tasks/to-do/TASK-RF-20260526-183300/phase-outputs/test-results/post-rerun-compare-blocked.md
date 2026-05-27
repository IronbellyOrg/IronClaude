---
phase: 6
step: 6.2
verdict: BLOCKED
created_date: 2026-05-26
---

# Post-Rerun Comparison — BLOCKED (Awaiting Operator-Driven Rerun)

## Status

BLOCKED. Cases 4-11 rerun artifacts that reflect the Phase 2-3 protocol remediation are NOT yet present under `.dev/eval-workspaces/sc-brainstorm/live-runs/eval-<case-name>/`.

The existing `live-runs/eval-*` artifacts were produced by a prior session BEFORE Phase 2-3 source edits propagated to `.claude/` (and before `make sync-dev` ran in Phase 5.2). Running `compare_live_runs.py` against them produces the pre-remediation regression baseline (live 81.69% vs baseline 100%) already captured by Phase 5 Step 5.5 — it does NOT measure the effect of this task's remediation.

## Why Comparison Was Not Re-run At This Step

Re-running `compare_live_runs.py` here would regenerate the same pre-remediation comparison Step 5.5 already produced. That would inflate the appearance of post-remediation acceptance without measuring it. Per Phase 6 Step 6.2 ("run only when rerun artifacts are present"), the correct action is to mark this BLOCKED and surface the dependency.

## Resolution Path

1. Execute the rerun procedure documented in `.dev/tasks/to-do/TASK-RF-20260526-183300/phase-outputs/plans/cases-4-11-rerun-instructions.md` (8 cases, fresh sessions each).
2. Confirm all required artifacts (`seed-brief.md`, `merged-requirements.md`, `return-contract.yaml`, adversarial outputs, handoff outputs where applicable) exist under each `live-runs/eval-<case-name>/`.
3. Run `uv run python .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py` from project root.
4. Resume this task at Step 6.3 (acceptance matrix).

## Discipline

- No comparison metrics are fabricated by this BLOCKED status. Step 5.5 captured the pre-rerun baseline honestly; this step does NOT pretend that a post-rerun comparison has occurred.
- UV-only Python is required when the rerun comparison eventually executes.
- Case 12 remains intentionally excluded from rerun and comparison until registry compatibility is brought into scope.
