# Codegraph grounding

## Run state
- index_state: fresh (0 added, 0 modified, 0 removed; latest file indexed 2026-11-18T17:15:00Z)
- access: mcp
- checked_at: 2026-11-18T23:36:30Z
- worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
- tokens: none. Only python and yaml are indexed: shell, markdown and JSON files were read with Read and Grep.

## Resolved symbols
- predicates.py: `project_check` (lines 262 to 271), `ProjectItem` (113 to 118), `approval_of` (185).
- github.py: `REPO` (37), `EDITS_QUERY` (74), `PROJECT_ITEMS_QUERY` (88), `argv_discover` (180), `argv_edits` (242), `argv_project_items` (247), `argv_reread` (252), `_project_item` (764), public reads `discover`, `events`, `marker_comments`, `edits`, `project_items`, `reread`.
- launch.py: `PROMPT_PATTERN` (33), `ORIGIN_REPO` (50), `build_claim_prompt` (84), `launch_argv` (95), `retry_argv` (119), `check_origin` (233).
- cycle.py: `_TOP_KEYS` (58), `Config` (97), `load_config` (195), `_examine` (915), `_revalidate` (979), `_launch` (1026), `_origin_ok` (670), `status_report` (1270), `CycleResult.launched_issue` (455).
- cli.py: `issue_watch_group` (95), `once_command` (118), exit constants (34 to 38).

## Dependents
- `check_origin`: `cycle.py` `_origin_ok` (670), `tests/issue_watch/conftest.py` `_register_shared` (719), `test_launch.py`, `test_origin_parity.py`, `test_security_invariants.py`. Named in Task 8.
- `build_claim_prompt`: `cycle.py` `_launch` (1026) and `status_report` (1270, builds the retry command), `test_launch.py`, `test_security_invariants.py`. Task 5 names `_launch`; `status_report` is added here: it must keep printing a valid retry command (Task 5 acceptance covers `retry_argv`).
- `github.py` readers outside the watcher: `src/superclaude/cli/issue_pipeline/reads.py` (imports `github as gh`). Named in Tasks 1 and 7.
- The literal `--pipeline none` also appears in `src/superclaude/skills/sc-issue-protocol/templates/next-steps.md`, `tests/issue_watch/test_no_text.py`, `test_cli.py` and `test_crash_injection.py`: Task 6 names a Grep for every hit, so these are covered by its search rather than by name.

## Pre-check
- All files named by the tasks exist (checked with test -e on 2026-11-18).
- Symbols resolve at the lines quoted.
- Unnamed dependents to watch: `status_report` (cycle.py), `templates/next-steps.md`, `tests/issue_watch/test_crash_injection.py`, `test_no_text.py`, `test_cli.py`.
- New modules are pure additions: `defaults.py`, `repos.py`, `generate.py`, `repo_init.py`, `first_run.py`, `dispatch.py`, with the boundary test `tests/issue_watch/test_module_boundaries.py` to be satisfied.
