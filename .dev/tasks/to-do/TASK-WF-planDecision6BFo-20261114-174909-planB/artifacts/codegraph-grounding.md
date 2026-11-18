# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status: 3196 files, 0 added, 0 modified, 0 removed since index at 2026-11-14T16:05:30Z)
- checked_at: 2026-11-14T17:49:09Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-b
- access: mcp (codegraph_status, codegraph_search, codegraph_node, codegraph_callers listed)
- tokens: none
- note: the checkout is at 0406ef5b0. origin/master is now d4d1662a8 (PR #539 sweep and PR #548 design amendment merged after the base). Rows below describe 0406ef5b0; the plan's first constraint says to rebase before editing.

## Resolved symbols

- src/superclaude/cli/issue_watch/launch.py: PROMPT_PATTERN (:33), build_claim_prompt (:84), launch_argv (:95), retry_argv (:119), OrcaLauncher.launch (:358)
- src/superclaude/cli/issue_watch/predicates.py: approval_of (:185), unchanged_since (:237), LabelEvent (:90), EditEvidence (:143), CommentEdit (:133), ApprovalResult (:152)
- src/superclaude/cli/issue_watch/record.py: FileStore (:334), FileStore.lock (:381), FileStore.save (:370), _fsync_dir (:310), STORE_FILE (:281), mark_pending (:538), mark_launched (:580)
- src/superclaude/cli/issue_watch/github.py: EVENTS_JQ (:54), MARKER_JQ (:61), EDITS_QUERY (:74), argv_events (:218), argv_comments (:223), argv_edits (:242)
- src/superclaude/cli/issue_watch/cli.py: issue_watch_group (:94); registered in src/superclaude/cli/main.py:563-565
- src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py: cmd_worktree (:622), cmd_launch (:1682), cmd_prompt (:761), copy_issue_dir (:436)
- src/superclaude/hooks/scripts/launch-level-guard.sh: approval regex (:347-364), orca allow-list (:458-478), binding by marker (:314-388)

## Dependents

- build_claim_prompt callers: cycle.py:1026 (_launch), cycle.py:1270 (status_report), tests/issue_watch/test_launch.py:41,47,54,67, tests/issue_watch/test_security_invariants.py:451,697 (codegraph: 11 callers, 2 are files)
- launch_argv callers: retry_argv (launch.py:119), OrcaLauncher.launch (launch.py:358), tests/issue_watch/test_launch.py:75,95,102,141,805,817,841,913, tests/issue_watch/test_security_invariants.py:451,697,921, tests/issue_watch/test_no_text.py:464, tests/issue_watch/test_cli.py:582, tests/issue_watch/conftest.py:279 (20 callers; the list is at the limit)
- record.py is imported by cli.py and cycle.py, and by tests/issue_watch/{conftest,test_cli,test_concurrency,test_crash_injection,test_cycle,test_record}.py
- predicates.py is imported by cycle.py and record.py
- Import boundary: tests/issue_watch/test_module_boundaries.py pins what each issue_watch module may import, so new code goes in a sibling package, not in issue_watch
- tests/issue_watch/test_no_text.py forbids a gh argv that asks for comment text; the new reads turn the body into a boolean inside jq, as MARKER_JQ does
- tests/skills/test_worker_contract.py pins WORKER-CONTRACT.md wording; src/superclaude/cli/install_core.py installs it

## Pre-check

Pre-check run after the gate (read-only; the plan was not edited).

- Files named by tasks: every existing file exists (main.py, test_worker_contract.py, test_issue_orca_worktree.py, test_issue_protocol.py, the guard tests, chains.md, launch-level-pre-push.sh, swarm/atomic.py with write_prepared_bytes at :14). New files (issue_pipeline package and tests, two design notes, templates) do not exist yet, as intended.
- Symbols named by tasks resolve at the cited lines (read at base 0406ef5b0).
- Dependents no task names (leads, not proof):
  - docs/designs/sc-issue-claim-pipeline-flag.md, sc-issue-command.md and sc-issue-launch-level-hook.md describe the `--pipeline` levels and the guard; Tasks 12, 13, 15 and 16 should check them.
  - tests/docs has no test that pins docs/designs/issue-watcher*.md, so Task 8 and Task 16 wording about "existing docs-pin tests" is wrong (recorded, not fixed: Wave 4 never edits the plan).
  - No plugin mirror of WORKER-CONTRACT.md was found under plugins/.
- Result: 0 missing files, 3 unnamed doc dependents, 1 wrong test reference.
