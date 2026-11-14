# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-14T15:20:23Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/sweep-git-fix
- projectPath: /home/coder/workspaces/worktrees/IronClaude/sweep-git-fix
- access: mcp
- tokens: none

## Resolved symbols

- `_git`, `check_git_args`, `ALLOWED_GIT`, `GitCallFailed`: src/superclaude/cli/sweep/probes.py (read in full before citing)
- `_read_worktree` (probes.py:921), `read_worktree` (:948), `_failed_worktree` (:954), `_worktree_paths` (:1203), `collect` (:1217), `_orca_reads` (:1011)

## Dependents

- `_git` callers: `_read_worktree` (call-site-verified at probes.py:938); tests: tests/sweep/test_readonly.py (`test_git_argv_and_env_are_lock_free`, `test_check_git_args_allows_only_the_listed_call`), tests/sweep/test_probes_allowlist.py (`test_git_negatives_raise_value_error_before_a_subprocess`, `test_the_one_git_call_is_accepted`, `test_subprocess_output_boundary_for_git`). Other `_git` hits in tests/cli/reflect are a different module (`superclaude.cli.reflect.config._git`), not touched.
- `_read_worktree` callers: `read_worktree` (probes.py:948), `collect` (probes.py:1217).
- Fake seam: `GitFake` and `patch_git` in tests/sweep/conftest.py (calls list, one canned response per worktree path).

## Pre-check

Checked 2026-11-14 (Grep/Read on the files below; codegraph rows were leads only):
- Files the tasks name exist: src/superclaude/cli/sweep/probes.py, tests/sweep/test_probes_allowlist.py, tests/sweep/test_readonly.py, tests/sweep/conftest.py, docs/designs/orchestrator-mode.md. tests/sweep/test_git_config_hole.py is new (created by Task 1).
- Symbols resolve: `_git`, `check_git_args`, `ALLOWED_GIT`, `_read_worktree`, `_failed_worktree`, `_orca_reads`, `GitFake`, `patch_git`, `GIT_STATUS`, `STATUS_ARGS`, `test_collect_worker_list_source_rows_and_truncated`.
- Dependents of the touched symbols not named by any task: `tests/sweep/test_readonly.py::test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree` (lines 144 to 158) records every real `_git` subprocess call per worktree through `recorder`; with the new inspection calls it sees more than one call per worktree and its `[c["argv"][3] ...] == expected` assertion must be restricted to status calls (the executor handles this in Task 4; see the reflect report).
