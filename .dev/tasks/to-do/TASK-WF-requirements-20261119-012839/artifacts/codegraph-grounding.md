# Codegraph grounding

## Run state
- index_state: fresh (0 added, 0 modified, 0 removed; latest file indexed 2026-11-18T23:54:24Z; checked 2026-11-19T01:11Z for the previous plan version of the same source, no source file changed since)
- access: mcp
- worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
- tokens: none. Only Python and yaml are indexed; shell, markdown and JSON files were read with Read and Grep.

## Resolved symbols
- predicates.py: `project_check` (262 to 271), `ProjectItem` (113 to 118; holds is_archived, project_id, status_name), `approval_of` (185), `edited_after_approval` (258), approval time checks (228 to 233), `unchanged_since` (249 to 258).
- github.py: `REPO` (37), `EDITS_QUERY` (74), `PROJECT_ITEMS_QUERY` (88), `argv_discover` (180), `_argv_rest_page` (201), `argv_events` (218), `argv_comments` (223), `_argv_graphql` (228), `argv_edits` (242), `argv_project_items` (247), `argv_reread` (252), `_project_item` (764), `rate_limit_wait` (418).
- launch.py: `PROMPT_PATTERN` (33), `ORIGIN_REPO` (50), `build_claim_prompt` (84; prompt f-string at 92), `launch_argv` (95), `retry_argv` (119), `check_origin` (233).
- cycle.py: `_TOP_KEYS` (58), `Config` (97), `load_config` (195), `_examine` (915), `_revalidate` (979; reread at 1012 to 1016), `_launch` (1026; prompt built at 1054, `_revalidate` at 1058, pending saved 1091 to 1092, launch outcome 1099 to 1112), `_origin_ok` (670), `status_report` (1270), `CycleResult.launched_issue` (455).
- issue_watch/cli.py: group decorator 94, definition 95, `once_command` (118), exit constants (34 to 38).
- issue_pipeline/cli.py: `issue_pipeline_group` (about 58), `adopt-create` (108), `record-create` (134), `release-worker` (200), `stage-status` (335).
- approval_record.py: `_approval_path` (132), `_ADOPTION_KEYS` (137), `_APPROVAL_KEYS` (140), `_EVIDENCE_KEYS` (153).
- Guard: src/superclaude/hooks/scripts/launch-level-guard.sh (coordinator-only TAMPER pattern at 444; SUBMIT class denies `gh issue comment` at W, WA, F (792); GHWRITE class denies `gh api` writes at all levels (798)); tracked mirror plugins/superclaude/hooks/scripts/launch-level-guard.sh. The guard has no prompt allow-list.

## Dependents
- `build_claim_prompt`: `cycle.py` `_launch` (1054) and `status_report` (1270), `tests/issue_watch/test_launch.py`, `test_security_invariants.py`. Named in Task 6.
- `check_origin`: `cycle.py` `_origin_ok` (670) and tests. Named in Task 12.
- `github.py` readers outside the watcher: `issue_pipeline/reads.py`. Named in Tasks 1 and 11.
- The literal `--pipeline none` appears in 24 files outside `.dev`; Task 7 names them.
- `tests/issue_watch/test_security_invariants.py` lines 911 to 919 assert the old literal repo; named in Task 11.
- `CycleResult` consumers of a new `attempted_issue` field: `cli.py` `once_command`, `status_report`. Named in Task 18.

## Pre-check
- All files named by the tasks exist (Grep and find results of 2026-11-19).
- Symbols resolve at the lines quoted (read on 2026-11-19: cycle.py 1000 to 1130, approval_record.py 1 to 30 and 130 to 155, guard 64 to 74, 440 to 446, 650 to 655, 790 to 800, WORKER-CONTRACT.md 241 to 243, issue.md 43, 44, 56, test_security_invariants.py 911 to 919, predicates.py 226 to 260).
- Verified gap behind Task 9: no `item-edit` and no `updateProjectV2ItemFieldValue` exists in `src` or `docs`.
- Not yet verified: that the GraphQL type `ProjectV2Item` has an `updatedAt` field (Task 3 checks it with a read-only schema call).
