# Research 03: Report and Scaffold Behavior

Status: Complete

## Findings

Evidence tags: `[CODE-VERIFIED]` means the claim is verified against repository files cited on the same bullet; `[TASK-DECISION]` means a design/task choice derived from the critiqued feature design rather than pre-existing code.

### `.dev/` is the safe artifact root for this feature

- [CODE-VERIFIED] `.dev/README.md` declares the canonical rule that workspaces, fixtures, harness code, and iteration outputs belong under `.dev/`, not under `.claude/skills/` (`/config/workspace/IronClaude/.dev/README.md:3-7`).
- [CODE-VERIFIED] The same guide says `.claude/skills/<skill>/` is reserved for distributable skill packages and that generated evaluation/debug/release workflow output belongs under `.dev/` (`/config/workspace/IronClaude/.dev/README.md:5-7`).
- [CODE-VERIFIED] Its decision table assigns research/decision artifacts to `.dev/research/`, MDTM task files to `.dev/tasks/`, and actual distributable skills to `src/superclaude/skills/<skill-name>/` synced to `.claude/skills/<skill-name>/` (`/config/workspace/IronClaude/.dev/README.md:31-40`).
- [CODE-VERIFIED] It explicitly says to stop if tempted to write sibling paths under `.claude/` and redirect to `.dev/eval-workspaces/<skill-name>/` (`/config/workspace/IronClaude/.dev/README.md:42`).

### Report writer conventions

- [CODE-VERIFIED] Existing CLI code writes generated markdown and JSON artifacts with `Path.write_text(..., encoding="utf-8")`; direct search evidence includes sprint preflight evidence writes at `src/superclaude/cli/sprint/preflight.py:73` and `src/superclaude/cli/sprint/preflight.py:221`, roadmap validation report writes at `src/superclaude/cli/roadmap/validate_executor.py:437`, eval report writes at `src/superclaude/cli/eval/run_report.py:395` through `src/superclaude/cli/eval/run_report.py:407`, and PRD executor artifact writes at `src/superclaude/cli/prd/executor.py:1164`.
- [TASK-DECISION] Existing project convention for generated/iteration artifacts is `.dev/`, not `.claude/`. For this feature, `.dev/superclaude/context-audit.md` is appropriate as an operator-facing report even though `.dev/README.md` does not currently name a `superclaude/` subdirectory (`/config/workspace/IronClaude/.dev/README.md:3-7`, `/config/workspace/IronClaude/.dev/README.md:31-42`).
- [TASK-DECISION] The implementation should call `mkdir(parents=True, exist_ok=True)` for `.dev/superclaude/` and, only with `--scaffold`, for `.dev/superclaude/project-guidance/refs/`.
- [TASK-DECISION] Default run should write only the report. `--dry-run` should render the report to stdout or return a no-write summary but must not create `.dev/superclaude/`.
- [TASK-DECISION] `--scaffold` should create only missing generated advisory files under `.dev/superclaude/project-guidance/`: `SKILL.md` and `refs/README.md`. These are examples for a target project to copy/adapt, not distributable IronClaude source files.
- [TASK-DECISION] `--force` may overwrite generated report/scaffold files, but must never overwrite `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, or any project-local `.claude/` assets.

### Context surface discovery behavior

- [TASK-DECISION] Discover only project-local startup/context surfaces: `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**/SKILL.md`, and `.claude/agents/*.md`.
- [TASK-DECISION] Use deterministic token estimate `ceil(bytes / 4)` for every discovered file. Task decision from the critiqued design: label surfaces `low` when estimate is `< 1,000`, `medium` when estimate is `1,000` through `4,000`, and `high` when estimate is `> 4,000`; these thresholds are not existing code, so tests should pin them in the new init-lite module.
- [TASK-DECISION] Preserve exact existing files: the command must read surfaces and write reports, not mutate source context. Hashing or byte comparison of `CLAUDE.md` before/after should be part of tests.
- [TASK-DECISION] Report should include manual recommendations only: biggest contributors, candidate CLAUDE.md sections to move, suggested destination under project-guidance refs, and a small copyable patch snippet. No automatic section migration.

### Edge cases

- [TASK-DECISION] If no `CLAUDE.md` exists, report that none was found and do not create one.
- [TASK-DECISION] If `.claude/` does not exist, report zero local Claude assets and do not create `.claude/`.
- [TASK-DECISION] If report output parent does not exist, create it unless `--dry-run` is active.
- [TASK-DECISION] If output exists and `--force` is false, overwrite only when the first existing report contains this exact generated marker: `<!-- generated-by: superclaude init-lite context-audit v1 -->`. If the output exists without that marker, fail with a clear Click error. With `--force`, overwrite only the report/scaffold paths owned by init-lite under `.dev/superclaude/`; never overwrite context inputs such as `CLAUDE.md`, `.mcp.json`, `.claude/settings.json`, `.claude/commands/**`, `.claude/skills/**`, or `.claude/agents/**`.

## Summary

The task should implement report/scaffold behavior under `.dev/superclaude/`, never under `.claude/` for target projects. The report is the default artifact; scaffold generation is opt-in via `--scaffold`; `CLAUDE.md` and all context inputs are read-only invariants.
