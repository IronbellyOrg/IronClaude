# Codegraph grounding

## Run state

- index_state: stale (107407 pending references; `graph:stale`)
- checked_at: 2026-11-23T23:35:45Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-751
- Codegraph was not used for citations; Grep and Read were (permanent floor).

## Resolved symbols

- run_sweep: src/superclaude/cli/issue_watch/dispatch.py:348 (read in full)
- first_run: src/superclaude/cli/issue_watch/first_run.py:125 (read in full); `_report_dir` :78, `_write_report` :86, report-name rule :141-145
- ensure_config: src/superclaude/cli/issue_watch/generate.py:196

## Dependents

- run_sweep: run_all_command (src/superclaude/cli/issue_watch/cli.py:470; call at :508, :511), tests/issue_watch/test_dispatch.py:141 (`sweep`, call at :152). Signature unchanged.
- first_run: dispatch.py:427 (only production call), tests/issue_watch/test_first_run.py:125 and :347.

## Pre-check

Checked by Grep and Read (no codegraph): every file the plan names exists (dispatch.py, first_run.py, test_dispatch.py, test_first_run.py, test_cli.py, test_security_invariants.py); symbols resolve at the cited lines; dependents of run_sweep and first_run are listed above and are either named by Tasks 4 and 5 or unaffected (signatures unchanged). Task 2 needed a `timedelta` import, now in the task. `graph:stale`.
