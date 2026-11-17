# Codegraph grounding: TASK-WF-removeScBuildPer-20261117-210056

## Run state

- index_state: unknown (the codegraph MCP server disconnected earlier in this session and its tools are not callable, so the readiness check could not classify the index)
- token: `graph:absent`
- checked_at: 2026-11-17T21:00:56Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-build
- access: none for lookups; Grep, Glob and Read floor used throughout
- note: `/sc:build` is a markdown command file with no Python symbol. No code imports or calls it; the only code that names it is a `case` list in a shell hook, so a graph lookup has nothing to add.

## Resolved symbols

No code symbol depends on the command. File-level targets, all confirmed by `git grep` and Read on 2026-11-17 (full list with lines in `.dev/cleanup/build/dependency-map.md`):

- Deleted: `src/superclaude/commands/build.md`, `plugins/superclaude/commands/build.md`, `commands/sc-build.md`
- Guide rows: `src/superclaude/core/HOW-WE-WORK.md:324,403` and its twin `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:324,403`
- Contract: `src/superclaude/core/WORKER-CONTRACT.md:329`
- Hook: `src/superclaude/hooks/scripts/launch-level-guard.sh:43,409` (identical twin `plugins/superclaude/hooks/scripts/launch-level-guard.sh`)
- Skill: `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:594`
- Tests: `tests/skills/test_worker_contract.py:473-485,583-587,1394-1399,1467-1468,1675`; `tests/core/test_how_we_work_routing_table.py:28`; `tests/hooks/test_launch_level_guard.py:81,917`; `tests/recommend/test_routing_refresh.py:35,589,599`; `tests/unit/test_cli_install.py:114,402`

## Dependents

- `tests/skills/test_worker_contract.py` `_check_p1_set` and `_check_p2_set` pin 16 and 31 command sections; both counts drop by one.
- `tests/core/test_how_we_work_routing_table.py` asserts the Other-commands table members equal `_OTHER_COMMANDS`.
- `tests/recommend/test_routing_refresh.py:648` compares the shipped commands with the frozen 43 active ones minus the post-refresh removals; `build` joins that removal set. The frozen fixture line 737 stays.
- `tests/hooks/test_launch_level_guard.py` reads the historical design table and applies removal rewrites; the design file is not edited.
- `tests/unit/test_cli_install.py` lists expected installed command files (two lists).
- Twin readers of the routing guide copy under `plugins/superclaude/skills/sc-recommend/refs/`: the two guide copies must stay byte-identical.

## Pre-check

Filled after Wave 3; see the line at the end of this file.

Pre-check result (2026-11-17): 32 file:line anchors read, 31 exact, 1 loose (a comment line one above its set); no task names a missing file or symbol; unnamed dependents noted in the reflect report (the architecture reference's "46 command files" count). Gap: no graph lookup ran (`graph:absent`).
