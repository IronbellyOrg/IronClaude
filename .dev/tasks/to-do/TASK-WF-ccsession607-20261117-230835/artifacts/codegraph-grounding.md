# Codegraph grounding (TASK-WF-ccsession607-20261117-230835)

## Run state

- index_state: fresh (codegraph_status: 0 added, 0 modified, 0 removed; 3831 files indexed)
- checked_at: 2026-11-17T23:08:46Z
- worktree_root / projectPath: /home/coder/workspaces/worktrees/IronClaude/ccsession-list-speed-607
- access: mcp (lookup tools listed)
- tokens: graph:empty for the bash script. The index holds python, yaml, javascript, typescript and liquid files only; `src/superclaude/skills/ccsession-tag/ccsession` (a bash script without extension) is "not an indexed file", so every lookup in it ran on the floor (Grep and Read). The Python test file `tests/unit/test_ccsession_tag.py` is indexed (284 symbols, no other indexed file depends on it).

## Resolved symbols (floor: Grep and Read of the live file)

All in `src/superclaude/skills/ccsession-tag/ccsession` (2072 lines, byte-identical to the installed copy and to origin/master c00caea93):

- `set -e` at line 132; `PROJECTS_DIR="$HOME/.claude/projects"` at 144; `CCSESSION_DIR` resolved at 159.
- `session_home` 1377-1399, `session_branch` 1401-1408, `load_worktrees` 1417-1428, `session_place` 1430-1478.
- `session_transcript` 1480-1483, `get_btime` 1488-1512, `get_mtime` 1514-1531, `format_epoch` 1533-1537, `format_duration` 1539-1552.
- `list_sessions` 1554-1663 (row loop 1580-1638), `retention_warning` 1665-1678 (calls the python3 helper retention.py at 1675: the precedent for scan_sessions.py), `ask_session_name` 1680-, `show_saved` 1715-1731 (captures list_sessions at 1718).
- Dispatch: `--list` 1881-1886, `--here` 1887-1896, `--ask` 1897-1900.
- Resume path: `session_transcript` 2054, `session_home` 2055, `session_place` 2057.

## Dependents (floor: Grep, each site read)

- `list_sessions`: called at 1719 (show_saved, worktree view, from `--ask`), 1883 (`--list`), 1890 (`--here --all`), 1892 (`--here`). `ccsession-orca:204` runs `ccsession --ask` (named by the issue, not re-read here).
- `session_transcript`: 1599 (list_sessions) and 2054 (resume path). Both stay on the existing function; only list_sessions gets the index.
- `session_home`: 1607 (list_sessions) and 2055 (resume path). The grep/awk locale prefix reaches both.
- `session_branch`: 1455 (inside `session_place`, only for a deleted folder).
- `get_btime`, `get_mtime`, `format_epoch`: only list_sessions (1610, 1611, 1616, 1617). They stay defined.
- Tests: `tests/unit/test_ccsession_tag.py` `_listed` (line 4059) and `_ccs` (line 4000) run the real entry points `--here`, `--here --all`, `--list`; pinned-format tests use them.
- Installers: `src/superclaude/skills/ccsession-tag/install.sh:40` (`cp -R` of the whole folder) and `src/superclaude/cli/install_skill.py:52` (`copytree`) copy the skill folder wholesale, so a new `scan_sessions.py` needs no manifest edit. `src/superclaude/cli/install_ccsession.py:105` and `tests/unit/test_install_ccsession.py:339,357,373` reference `retention.py` by name; they are not touched.

## Pre-check

All 13 tasks: every file named exists (ccsession, retention.py, install.sh, install_skill.py, the test file, the scale-store script); the test helpers `_named_repo` (3963), `_transcript` (3982) and `_ccs` (4000) exist; `ccsession-orca:204` calls `ccsession --ask` as the source says. Dependents of the touched functions that no task names: `ccsession-orca` (reaches the list only through `--ask`, covered by Task 11 acceptance) and the README line "Listing never writes any file" (a constraint, covered by Task 9). Floor used (graph:empty for the unindexed bash script).
