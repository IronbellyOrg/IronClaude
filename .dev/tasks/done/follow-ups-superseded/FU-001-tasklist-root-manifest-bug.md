---
id: "FU-001-tasklist-root-manifest-bug"
title: "Sprint runner writes .sprint-exitcode into tracked release archive path"
status: "🟡 To Do"
type: "🐛 Bug"
priority: "🔼 High"
created_date: "2026-05-18"
parent_task: "TASK-RF-20260518-181333"
tags:
- "follow-up"
- "root-cause-fix"
---

## Background

During TASK-RF-20260518-181333 Phase 1 inventory, ~80 tracked `.sprint-exitcode` files under `.dev/releases/**/` were observed. These are transient runner exitcode markers that should NOT be checked into the release archive. The `_FRESHNESS_SCRIPTS` registration mechanism plus `.gitignore` patterns guard against root-level `.sprint-exitcode`, but the existing in-archive tracked files indicate a historical pattern where the sprint runner wrote `.sprint-exitcode` into the per-release working dir and the operator-commit step swept them in.

## Symptom

`git ls-files | grep -c '\.sprint-exitcode$'` returns 40 (per Phase 3 QA report). The `TASKLIST_ROOT` logic in the sprint runner / tasklist generator writes `.sprint-exitcode` into a path that gets committed. The PR-split task's Phase 3 anchored the `.gitignore` pattern to `/` only to PRESERVE these tracked files, but the root cause is that the writer should target a non-tracked location.

## Root Cause Hypothesis

The sprint runner's `.sprint-exitcode` writer uses `TASKLIST_ROOT` as the parent dir, and `TASKLIST_ROOT` resolves to a path inside `.dev/releases/.../` instead of a `.dev/sprint-state/` or `/tmp/`-style transient location. The writer treats the tasklist working directory as the state directory, conflating two distinct concerns: archive (tracked) vs. runtime state (transient).

## Suggested Fix Direction

- Audit `src/superclaude/cli/sprint/` for `.sprint-exitcode` writes (likely `executor.py` or `commands.py`).
- Introduce a `SPRINT_STATE_DIR` env/config that defaults to a `.dev/` subdirectory listed in `.gitignore` (e.g., `.dev/sprint-state/<tasklist-id>/`).
- Migrate existing tracked `.sprint-exitcode` files to the new location and remove them from tracking with `git rm --cached`.
- Decide on archive-immutability policy: either leave historical `.sprint-exitcode` files in place (don't rewrite history) or do a single sweeping migration commit.

## Acceptance Criteria

- New `.sprint-exitcode` writes land in an untracked location.
- `git ls-files | grep '\.sprint-exitcode$'` returns 0 after migration.
- Existing in-archive `.sprint-exitcode` files preserved or moved (don't break archive immutability).
- Sprint runner tests still pass (`uv run pytest tests/sprint/`).
- `.gitignore` root-anchored pattern can remain or be relaxed without re-introducing pollution.

## References

- Phase 3 QA report: `.dev/tasks/to-do/TASK-RF-20260518-181333/qa/qa-phase-3-report.md`
- `.gitignore` patterns commit: `fe11bd8`
- Likely source: `src/superclaude/cli/sprint/executor.py`, `src/superclaude/cli/sprint/commands.py`
- Parent task: `TASK-RF-20260518-181333`
