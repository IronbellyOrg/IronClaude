# Phase 1 Baseline Status — FR-RH1 UC-2 Contracted-Sink Reachability Gate

Captured: 2026-06-20 (Phase 1, item C-003). Read-only baseline; no working-tree mutations made by this item.

## Git baseline

- **Current branch:** `ReflectHardening-3`
- **Start commit (frontmatter `start_commit`):** `63f1a8153d2375e48369059c253dc2a76f73c063`
- **Current HEAD:** `63f1a8153d2375e48369059c253dc2a76f73c063` (matches frontmatter — clean baseline, no commits since task creation)
- **`git status --short` (all untracked `.dev/` workspaces; zero tracked-file modifications):**

```
?? .dev/brainstorms/20260620-040444-reflect-uc2-reachability-gate/
?? .dev/reflect-hardening/
?? .dev/reflect/pre-fr-rh1-uc2-reachability-20260620-053500/
?? .dev/reflect/pre-fr-rh2-headless-ensemble-20260620-040811/
?? .dev/reflect/pre-reflect-t2-swarm-tdd-20260620020835/
?? .dev/reflect/pre-uc2-reachability-20260620-044943/
?? .dev/reflect/pre-uc2-reachability-gate-20260620-041729/
?? .dev/reflect/pre-uc2-reachability-tdd-20260620000727/
?? .dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/
?? .dev/tasks/to-do/TASK-RF-uc2-reachability-20260620-025931/
?? .dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/
?? .dev/tasks/to-do/TASK-TDD-20260619-235400/
```

## Source-of-truth, sync, UV, and `.claude/` rules (from CLAUDE.md + research 05)

- **Source of truth = `src/superclaude/`.** All implementation edits to skills, commands, and agents MUST land under `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/` FIRST, then run `make sync-dev` to regenerate `.claude/` mirrors.
- **`.claude/` mirrors are generated sync-dev output and MUST NEVER be staged** — `.claude/{skills,commands,agents,hooks,templates}` are gitignored; the ONLY tracked `.claude/` file is `.claude/settings.json`. Never `git add -f` any `.claude/` path. If staging requires `-f` on a `.claude/` path, STOP and move the change to `src/superclaude/`.
- **Non-mirrorable code** (`src/superclaude/cli/reflect/*.py`, `tests/`, `docs/`) is edited directly and is NOT subject to `make sync-dev` (it is not mirrored into `.claude/`). Only `skills/`, `commands/`, `agents/` content mirrors.
- **UV only** for all Python: `uv run pytest`, `uv run ruff format --check src/ tests/`. Never bare `python -m`, `pip`, or `python script.py`.
- **PR target** (if/when reached) = fork `IronbellyOrg/IronClaude`, never upstream — but this task does NOT perform git commits/PRs; staging is limited to the POST-reflect wrapper's `git add -A` in Phase 7.
- **Cross-task note (adversarial decision, 2026-06-20):** this task (C) is the canonical UC-2 reachability GATE and legitimately owns `contract_version: "1.6.0"` and registers its `uc2-reachability-*` eval ids FIRST. The sibling FR-RSR task (B) must rebase off 1.6.0; do NOT copy FR-RSR `runtime_surface_*`/UNREACHED semantics (per research 05 §"MUST NOT be copied").
