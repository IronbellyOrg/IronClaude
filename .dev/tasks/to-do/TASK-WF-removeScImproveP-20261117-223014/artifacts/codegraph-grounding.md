# Codegraph grounding: remove /sc:improve

## Run state

- index_state: fresh (CLI `status`: "Index is up to date"; 3,795 files, 57,477 nodes)
- checked_at: 2026-11-17T22:30Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-improve
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-improve
- access: cli (`/opt/codegraph/v1.6.2/bin/codegraph`, version 1.6.2; the codegraph MCP server disconnected mid-session, so lookup tools were not listed)
- tokens: graph:empty (the command is a markdown file; the graph indexes Python and YAML only, so it has no caller rows for `/sc:improve`). Index note: "built by an earlier version"; not re-indexed (read-only run).

## Resolved symbols

Found with `codegraph query`: `P2_COMMANDS` (tests/skills/test_worker_contract.py:495), `UNATTENDED_EXPECT` (:516), `P2_GATES` (:1753), `_REMOVED_COMMAND_TEXT` (tests/hooks/test_launch_level_guard.py:80), `IMPL_SPELLINGS` (:909), `_POST_REFRESH_REMOVALS` (tests/recommend/test_routing_refresh.py:39).
Not indexed (markdown, shell, JSON, HTML): the command files, `launch-level-guard.sh`, `HOW-WE-WORK.md`, the fixture, the docs. Floor: `git grep` and Read, recorded in `.dev/cleanup/improve/dependency-map.md`.

## Dependents

- `P2_COMMANDS` users: test_worker_contract.py lines 1013, 1053, 1435, 1551, 1630-1635 (counts 14 and 29 must follow).
- `UNATTENDED_EXPECT` users: lines 806, 950-953, 1104-1118, 1433-1436, 1533-1553, 1601-1622, 1637.
- No Python or shell code imports or calls the command; `cli/recommend/prompts.py:195` holds one sentence naming it.

## Pre-check

Floor (git grep, Read; codegraph has no rows for markdown): all repo paths named by the 12 tasks exist (0 missing). Tracked files naming the command that no task names: `tests/sc-roadmap/compliance/test_critical_corrections.py` (kept on purpose: a self-contained list of the old roadmap's 7 wave-enabled commands, reads no file, and `/build` is still in it too). The plugin copy of `delegation-vs-native-heuristics.md` is covered by Task 2 ("and its plugin copy"). 1 note, no plan edit.
