---
version: ""
priority: "High"
created_date: "2026-11-11"
---

# Make the launch-level guard and the worktree hook recognize every Orca CLI name

Source: DEFECT recorded by the supervised-orchestration technical reference run (`.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239/`). Evidence: `research/gap-P3-G02.md` (29 probes, sections 3.5 and 3.6), `qa/phase-3-verification-content.md` (17 independent probes), `qa/phase-3-fix-report-cycle-1.md`. Owner authorization to open this task: recorded in the technical-reference run on 2026-11-11 (answer "Record as DEFECT, create task"). Capability declared in scope by `docs/designs/sc-issue-launch-level-hook.md:193` ("Why the agent cannot fake it: ... terminal and messaging tools are ESCAPE"; names `orca` only at `:119,:175,:247,:288`).
Goal: A session governed by the launch-level guard gets the same ESCAPE classification and the same worktree-agent block whether the Orca CLI is typed as `orca`, `orca-ide`, `orca-dev` or by a path ending in one of those names.

This plan is a draft written by a documentation run: it has not been reviewed by `/sc:workflow` or `/sc:implement`. Re-check every path and line against the repo before executing.

## Constraints

- Defect, not a new feature: the guard (`src/superclaude/hooks/scripts/launch-level-guard.sh`) and the hook (`src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`) already work for the literal name `orca`; that behavior must not change.
- Edit `src/superclaude/hooks/scripts/` and the `plugins/superclaude/hooks/scripts/` mirror only through the repo's sync flow (`make sync-dev`, `make verify-sync`); never stage `.claude/` copies.
- No live Orca is needed or allowed for verification: use fixed-JSON hook probes and the existing hook tests.
- Do not claim a fix is deployed: installed hooks under `~/.claude/hooks/` change only through `superclaude install`/`update`.

## Phase 1: Close the name gap

## Task 1: Recognize alternate Orca CLI names in the launch-level guard

In `src/superclaude/hooks/scripts/launch-level-guard.sh`, the `orca)` arm (around `:455-458`, allow-list at `:475-477`) is entered only when the executable basename is exactly `orca`. Make the arm also apply to `orca-ide` and `orca-dev` (the names the repo tries first in `_ORCA_CLIS` at `src/superclaude/cli/install_user_setup.py:35`, and the names Orca's dispatch preamble prints for workers, see `research/gap-P3-G01.md` S1 and `research/gap-P3-G02.md` section 3.1) and decide explicitly whether `orca.cmd` (probed by the research as also returning 0 from the guard, `research/gap-P3-G02.md` probe table) is in or out, recording the reason; include absolute-path forms such as `/opt/Orca/bin/orca-ide`. Decide in the task whether to match an explicit list or a pattern, and record the choice with the reason; do not widen to unrelated command names.

Acceptance criteria:
- Fixed-JSON probes (stdin payload format of `tests/hooks/test_launch_level_guard.py`, bound session at levels worktree and full-submit) return exit code 2 for `orca-ide terminal send --terminal t1 --text approved`, `orca-ide agent launch ...` and `orca-ide orchestration worker-start ...`, matching the results for `orca`, and the read-only allow-list (for example `orca terminal show`) still returns 0 under the alternate names.
- New parametrised cases in `tests/hooks/test_launch_level_guard.py` cover the alternate names for at least those three verbs and one allow-listed verb, and fail on the unfixed script.
- The existing tests in `tests/hooks/test_launch_level_guard.py` still pass and the speed pins (`LARGE_LIMIT_S`, T-SPD tests) still hold.

## Task 2: Recognize alternate Orca CLI names in the worktree-agent hook

Depends on: Task 1

In `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, the orca-word test at `:145` (`b == "orca" || b ~ /^\$/`) recognizes only the literal name. Apply the same decision as Task 1 so `orca-ide worktree create --name x` (without `--agent`) exits 2 with the existing block message, and keep the documented fail-open cases unchanged. Mirror the change in `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh` via the sync flow.

Acceptance criteria:
- Probes: `orca-ide worktree create --name x` and `orca-dev worktree create --name x` exit 2; the same commands with `--agent claude` exit 0; `orca worktree create --name x` still exits 2.
- New cases in `tests/hooks/test_require_orca_worktree_agent.py` cover the alternate names and fail on the unfixed script; the existing tests pass.
- `make verify-sync` passes.

## Task 3: Correct the documented ceilings and the design claim

Depends on: Task 1, Task 2

Update the known-ceilings list in the header of `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (`:39-61`) and `docs/designs/sc-issue-launch-level-hook.md` (`:119,:175,:193,:247,:288`) so each statement names the recognized CLI names (or states the remaining limit, such as obfuscated names via variables) instead of the literal `orca` alone.

Acceptance criteria:
- No statement in those two files claims coverage the scripts do not provide; the remaining accepted limits (obfuscated or built names, a hostile agent) are stated.
- `tests/core/test_orca_session_launch_guidance.py` and the hook tests that pin the block message still pass.
