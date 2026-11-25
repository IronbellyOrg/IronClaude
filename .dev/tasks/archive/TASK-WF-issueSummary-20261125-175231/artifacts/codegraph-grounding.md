# Codegraph grounding: TASK-WF-issueSummary-20261125-175231

## Run state

- index_state: fresh (MCP `codegraph_status`: "Changes since index: 0 added, 0 modified, 0 removed")
- checked_at: 2026-11-25T17:52:59Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-765
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-765
- access: mcp (status tool called; lookup tools were not needed, see below)
- codegraph CLI version: 1.6.2 (matches the pin)
- degraded: graph:truncated (status reported "39329 references from an interrupted index run": caller and impact edges may be missing, so no "no callers" or "no dependents" conclusion was drawn from the graph)

## Resolved symbols

The launcher `ccsession` and its wrapper `ccsession-orca` are extensionless bash files. The index lists only javascript, liquid, python, typescript and yaml, so neither file has symbols in the graph. Every claim below was confirmed by Grep and Read of the live file (the permanent floor), not by a graph row.

- `src/superclaude/skills/ccsession-tag/ccsession`: env file sourced at 1082-1086; `CCSESSION_ORIGIN` exported at 2438; six `exec "$CLAUDE_BIN"` sites at 2448, 2450, 2509, 2511, 2516, 2518; `orca_terminal_title` (2394-2404) is the precedent for exporting a Claude Code switch (`CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1`, only in an Orca terminal).
- `src/superclaude/skills/ccsession-tag/ccsession-orca`: ends in `exec "$CCSESSION" --name "$name" --shim --claude-args "$@"` (261) or `exec "$CCSESSION" --shim --claude-args "$@"` (263).
- `src/superclaude/skills/ccsession-tag/README.md`: Orca section 392-426, "Tab title in Orca" 592-609 (precedent for documenting a Claude Code env switch).
- `src/superclaude/scripts/ic`: `exec claude ...` at 128 and 130, bypasses ccsession.
- `src/superclaude/core/WORKER-CONTRACT.md`: coordinator wait at 100-102.
- Test harnesses: `_label_run`/`_label_launch` (test_ccsession_tag.py 1333-1384), `_LAUNCH_CASES` (1465-1472), `_orca_env` (1820+, fake claude records `env_names`), autouse fixture `_offline_model_data` (39-97), `_launch_env`/`_launch` (test_ccsession_tiers.py 368-453), `home` fixture (test_install_ccsession.py 28-44).
- `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP`: no match anywhere in the repo outside `.dev/` (Grep).

## Dependents

- Every Claude Code process started by `ccsession` or `ccsession-orca` (the six exec sites) and everything it spawns: its Bash tool commands, background commands and nested `claude` runs inherit the exported variable.
- Tests that capture the launch environment and must stay green: tests/unit/test_ccsession_tag.py, tests/unit/test_ccsession_tiers.py, tests/unit/test_install_ccsession.py.
- Not reached: `src/superclaude/scripts/ic` (direct `exec claude`) and a bare `claude` start.
- Installer: `wire_ccsession` copies the launcher unchanged (test_install_ccsession.py 47-62); no installer change.

## Pre-check

Checked by Grep, Glob and Read (no new readiness check). Result: 6 tasks, 0 failures.

- Files named by tasks all exist: `ccsession`, `ccsession-orca`, `README.md`, `SKILL.md` (so `make sync-dev` copies the skill), `tests/unit/test_ccsession_tag.py`, `tests/unit/test_ccsession_tiers.py`, `tests/unit/test_install_ccsession.py`, `src/superclaude/scripts/ic`, `src/superclaude/core/WORKER-CONTRACT.md`.
- Helpers and tests named by tasks resolve: `_label_run` (1333), `_orca_env` (1820), `_orca_tty` (1950), `_orca_no_tty` (1977), `_offline_model_data` (39), `_LAUNCH_CASES` (1465), `_launch` (368), `_launch_env` (389), `test_default_tier_sets_model_and_tier_window` (467), `test_tier_flag_and_named_model` (592, uses `--tier tier0` and `--model gpt-6-astra`).
- Line ranges cited by tasks were read in this run: `ccsession` 1080-1093, 2365-2520; `ccsession-orca` 1-30, 240-263; README 385-439, 580-609; `ic` 115-131; WORKER-CONTRACT 92-111.
- Dependents of the touched launcher not named by a task: none found. `ccsession.env.example` is not edited (the switch is forced by the launcher, not set in the env file). The `.venv/lib/python3.10/site-packages/superclaude/_src/...` copy of the launcher is an installed package copy, not a source, and is not edited.
- Graph caveat: the interrupted-index warning means graph rows could be incomplete; none was used as evidence.
