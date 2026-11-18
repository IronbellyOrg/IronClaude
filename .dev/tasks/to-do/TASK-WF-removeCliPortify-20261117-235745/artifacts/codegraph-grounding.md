# Codegraph grounding: TASK-WF-removeCliPortify-20261117-235745

## Run state

- index_state: fresh (codegraph_status: 3801 files, 0 added / 0 modified / 0 removed since index, 2026-11-17T23:54Z)
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-cli-portify
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-cli-portify
- access mode: codegraph MCP tools
- graph tokens: none

## Resolved symbols

- `cli_portify_group` (src/superclaude/cli/cli_portify/commands.py): only importer in src is src/superclaude/cli/main.py:537,539 (codegraph_callers; the other 16 callers are tests/cli_portify/test_cli.py).
- `PortifyProcess` (src/superclaude/cli/cli_portify/process.py:121): used inside cli_portify, tests/cli_portify and tests/pipeline/test_process_stdin.py. Rows for scripts/eval_workflow_vs_task_builder.py, tests/cli/eval/test_workflow_vs_task_builder_companion.py and roadmap/semantic_layer.py are same-name `run`/`build_command` collisions; `git grep PortifyProcess` finds no use there (confirmed by Grep).

## Dependents

Full list with path:line is in .dev/cleanup/cli-portify/dependency-map.md (sections A to E). No kept src module imports cli_portify (git grep over src/**/*.py).

## Pre-check

All files named by Tasks 1 to 18 exist (checked with test -f). Dependents no task names: tests/roadmap/test_retry_contract.py reads the retry_loop_no_terminal_case fixture that Task 17 rewords; it asserts only `failure_class`, `contract` and `source_authority`, not the incident text, so the reword is safe. Rest of the dependent set matches the dependency map. No graph:* note.
