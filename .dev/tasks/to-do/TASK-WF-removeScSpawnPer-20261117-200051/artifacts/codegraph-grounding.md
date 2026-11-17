# Codegraph grounding: TASK-WF-removeScSpawnPer-20261117-200051

## Run state

- index_state: unknown (the `codegraph_status` MCP tool is not in this session's tool list, so the readiness check could not classify the index)
- token: `graph:unlisted`
- checked_at: 2026-11-17T20:01:04Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-spawn
- access: none for lookups; Grep, Glob and Read floor used throughout
- CLI: `codegraph --version` prints 1.6.2 (matches the pin); not used for lookups
- note: `/sc:spawn` is a markdown command file with no Python symbol. An earlier `codegraph_search "spawn"` returned only unrelated `spawn` methods in `cli/eval`, so a graph lookup has nothing to add here.

## Resolved symbols

No code symbol depends on the command. File-level targets, all confirmed by Grep and Read on 2026-11-17 (full list with lines in `.dev/cleanup/spawn/dependency-map.md`):

- Deleted: `src/superclaude/commands/spawn.md`, `plugins/superclaude/commands/spawn.md`, `commands/sc-spawn.md`
- Guide rows: `src/superclaude/core/HOW-WE-WORK.md:270,334` and its twin `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:270,334`
- Contract: `src/superclaude/core/WORKER-CONTRACT.md:23`
- Hook: `src/superclaude/hooks/scripts/launch-level-guard.sh:43,409` (byte-identical twin `plugins/superclaude/hooks/scripts/launch-level-guard.sh`)
- Tests: `tests/skills/test_worker_contract.py:89,468,1455`; `tests/core/test_how_we_work_routing_table.py:33`; `tests/recommend/fixtures/routing_refresh_cases.json:610-629`; `tests/recommend/test_routing_refresh.py:135,645-648`; `tests/hooks/test_launch_level_guard.py:907`; `tests/unit/test_cli_install.py:118,405`

## Dependents

- Guide twin tests: `tests/skills/test_review_prompt_overrides.py:26`, `tests/skills/test_review_brief_placement.py:19`, `tests/skills/test_spec_panel_review_loop.py:25` read the plugin twin of the guide; both copies must stay byte-identical.
- `tests/core/test_how_we_work_routing_table.py:298` asserts the Other-commands table members equal `_OTHER_COMMANDS`.
- `tests/recommend/test_routing_refresh.py` reads case S27 through `_route` (the `/sc:spawn` guide line) and compares shipped commands with the frozen 43 active ones (line 648).
- `tests/skills/test_worker_contract.py:848-851,1193` iterate `NEVER_AS_WORKER` against the contract line.
- `tests/hooks/test_launch_level_guard.py:916` iterates `IMPL_SPELLINGS`.
- `tests/unit/test_cli_install.py` lists expected installed command files (two lists).
- `make verify-sync` compares `src/superclaude`, `.claude/` and `plugins/superclaude`.

## Pre-check

Read-only check by Grep and Read (codegraph not used, `graph:unlisted`), 2026-11-17:

- All 12 tasks name files that exist (three to delete, the rest to edit), and the cited line numbers still hold the `spawn` text (re-read for the architecture reference, the adversarial skill, the user guide, the flags page and the install test).
- Dependents not named by a task: none found. The "45 commands" counts in `docs/getting-started/upgrading.md:85` and `docs/developer-guide/technical-architecture.md:43` were already wrong before this change (47 command files ship) and are left alone on purpose.
- Mirror facts: the two guide copies and the two hook copies are byte-identical today; the plugin and source copies of the command differ, but both are deleted.
- Gate result: 12 tasks in 5 phases (cap 8), every task has acceptance criteria, no checkbox or numbered lines, no placeholders.
