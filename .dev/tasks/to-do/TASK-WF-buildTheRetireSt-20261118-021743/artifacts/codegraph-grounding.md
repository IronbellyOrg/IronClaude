# Codegraph grounding

## Run state
- index_state: fresh (codegraph_status: 0 added, 0 modified, 0 removed; 3418 files)
- checked_at: 2026-11-18T02:17:43Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-retire-step
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-retire-step
- access: mcp

## Resolved symbols
- install (src/superclaude/cli/main.py:46), update (main.py:340): the only production callers of the installers (read in full).
- install_commands (install_commands.py:15), install_all_skills (install_skills.py:70), install_agents (install_agents.py:15), run_retire_step (install_retired_mcp.py): read in full.
- launch-level-guard.sh:409 and plugins/superclaude/hooks/scripts/launch-level-guard.sh:409 (byte-identical copy).

## Dependents
- install_commands: callers install, update (main.py) plus tests only (codegraph_callers, 22 callers, all tests besides the two).
- install_all_skills: install, update plus tests. run_retire_step: install plus tests/cli/test_install_retired_mcp.py (def-line rows; leads only, call sites in main.py:263 read directly).
- Existing "installers never delete" tests (tests/cli/test_how_we_work_install.py:53-95) call install_core/install_commands directly and stay valid because the new step is not inside them.

## Pre-check
Gate passed (full, standard). 9 tasks in 5 phases; every named existing file exists (main.py, install modules, both guard scripts, five docs, hook and help tests); new files are created by Tasks 1, 2, 3 and 6. Dependents of install/update in main.py are covered by Tasks 4 and 7; no unnamed dependent found (production callers of install_commands, install_all_skills and run_retire_step are install and update only).
