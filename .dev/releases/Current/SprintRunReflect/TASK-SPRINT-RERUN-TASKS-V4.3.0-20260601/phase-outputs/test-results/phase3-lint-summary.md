# Phase 3 Lint Summary — rerun_tasks.py (+ config.py)

**Overall result:** PASSED (clean after a 1-cycle fix)

**Tool:** `ruff check` (run via worktree-absolute paths — `uv run` resolves imports to the
MAIN repo, so the edited worktree file MUST be targeted by absolute path; see Phase 3 Findings
"CRITICAL ENVIRONMENT FINDING").

**Files linted:**
- `src/superclaude/cli/sprint/rerun_tasks.py` (NEW — Sections A–G + helpers)
- `src/superclaude/cli/sprint/config.py` (R-F4 `PHASE_FILE_PATTERN` widen)

## Violations found and fixed (initial run: 3 errors)

| Rule | File:Line | Description | Fix |
|------|-----------|-------------|-----|
| F401 | rerun_tasks.py:40 | `.models.Phase` imported but unused | Removed from import (run_rerun_tasks uses `phase_obj` from `config.phases`, never constructs `Phase()`) |
| F401 | rerun_tasks.py:44 | `.recovery.RecoveryBundleRef` imported but unused | Removed from import |
| F821 | rerun_tasks.py:471 | Undefined name `verify_checkpoint_files` | **Real bug** (not just a nit): the cross-phase checkpoint check in `walk_dependencies` called it but it was never imported. Added lazy `from .checkpoints import verify_checkpoint_files` inside `_cross_phase_checkpoints_ok` (per the Step 3.1 scaffolding spec for deferred lazy imports). Re-verified the cross-phase path works post-fix. |

## Final assessment

**Clean.** `All checks passed!` on the final run. No violations remain in either file. The F821
was the most material — it would have raised `NameError` at runtime on any cross-phase dependency
walk; caught and fixed within Step 3.10. config.py is clean (the additive regex-alternative widen
introduced no violations).
