# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-18T00:47:26Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-index
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-index
- access: mcp
- tokens: none
- note: the commands and docs are markdown, which codegraph does not index; codegraph covers only the test symbols. The command and doc references come from `git grep` (see `.dev/cleanup/index/dependency-map.md`).

## Resolved symbols

Resolved with `codegraph_search` (rows are leads; each was then checked with Grep/Read):

- `_check_p1_set` (function), tests/skills/test_worker_contract.py:1399
- `_check_p2_set` (function), tests/skills/test_worker_contract.py:1598
- `test_other_operations_preserve_requested_authority_and_owned_state` (function), tests/core/test_how_we_work_routing_table.py:1011
- `_POST_REFRESH_REMOVALS` (variable), tests/recommend/test_routing_refresh.py:39
- `test_index_repo_output_format_states_where_the_files_land` (function), tests/skills/test_worker_contract.py:1267
- `_OWN_CHECK_COMMANDS` (variable), tests/skills/test_codegraph_adoption.py:279

## Dependents

Callers via `codegraph_callers` (def-line rows; the call sites are in the same test file and were read at 1501-1512 and 1611-1646 of tests/skills/test_worker_contract.py):

- `_check_p1_set` (2/2 shown): test_p1_command_set_is_complete (:1501), test_p1_set_check_fails_on_a_missing_extra_or_repeated_command (:1507). resolution: def-line
- `_check_p2_set` (3/3 shown): test_p2_command_set_is_complete (:1611), test_p2_set_check_fails_on_a_missing_extra_or_repeated_command (:1638), test_p2_set_check_fails_when_a_command_file_is_missing (:1643). resolution: def-line

No Python code outside tests names either command (codegraph search for `index-repo` returned only test symbols and `.dev` research scripts). An empty graph answer is not proof of no dependents; the file-level dependents come from `git grep` (22 tracked files outside the historical records and `.dev/`).

## Pre-check

Run 2026-11-18 after the gate, read-only: all 25 files named by tasks exist; every named test function resolves (grep of `def test_...` in the three test files); the 22 tracked non-historical files that still name the commands are exactly the 6 files Task 1 deletes plus the 16 files Tasks 2 to 13 edit; no dependent is left without a task. Unnamed dependents: none.
