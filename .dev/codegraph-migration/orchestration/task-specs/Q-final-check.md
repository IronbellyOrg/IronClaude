Task Q: independent final check of the three phase plans and assembly of the decisions log.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding). You did not produce any of this work; review it adversarially.

Target: `.dev/codegraph-migration/review/F1-result.md`, `F2-result.md`, `F3-result.md`, the task packages they name under `.dev/tasks/to-do/`, the three specs under `.dev/codegraph-migration/specs/`, the handoff under `.dev/codegraph-migration/handoff/`, and `.dev/codegraph-migration/review/review.md`.

Change: write `.dev/codegraph-migration/FINAL-SUMMARY.md` with:
1. A table: phase, spec path, tasklist package path, number of tasks, verdict PASS/FAIL.
2. Checks per tasklist: every review finding resolved (applied or rejected with evidence); every task has a runnable acceptance command and commit point; tests run after each task group; issue #323 comment steps present; decision rules present; cross-phase ordering consistent (Phase 1 then 2 then 3, plus Coder pin ordering); no task edits `.claude/` mirrors directly (only via `make sync-dev`); no primitive references `src/superclaude/...` paths; no task would stage `.claude/` paths.
3. Coverage: re-run the codebase-memory and Serena rg commands from the inventories (outside `.dev/`) and confirm every hit file maps to a Phase 1 or Phase 3 task; list any orphans.
4. Consolidated autonomous-decisions log: collect every `## Decisions` entry from inventories, research, specs, F-results and `.dev/codegraph-migration/decisions/`; one row each: decision, choice, method, source file.
5. Human-intervention points that remain, with why each is unavoidable.
6. Defects found: id, severity, file, fix. You may fix MINOR defects in the tasklists or specs directly and record them; list IMPORTANT/CRITICAL ones without fixing.
Verdict is binary per phase; any unfixed finding is FAIL. On zero findings for a phase, include a Self-Audit.

Constraints: no source edits; no commits.

Ownership: `.dev/codegraph-migration/FINAL-SUMMARY.md`, and MINOR fixes in the specs/tasklists recorded in that file.

Observable acceptance: FINAL-SUMMARY.md exists with all six sections and the rg re-run commands with hit counts.
