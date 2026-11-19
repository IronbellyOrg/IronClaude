# Codegraph grounding

## Run state
- index_state: fresh (0 added, 0 modified, 0 removed; latest file indexed 2026-11-18T23:54:24Z)
- access: mcp
- checked_at: 2026-11-19T01:11:00Z
- worktree_root and projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb
- tokens: none. Only Python and yaml are indexed; shell, markdown and JSON files were read with Read and Grep.

## Resolved symbols
- predicates.py: `project_check` (262 to 271), `ProjectItem` (113 to 118), `approval_of` (185), `edited_after_approval` (258).
- github.py: `REPO` (37), `EDITS_QUERY` (74), `PROJECT_ITEMS_QUERY` (88), `argv_discover` (180), `_argv_rest_page` (201), `argv_events` (218), `argv_comments` (223), `_argv_graphql` (228), `argv_edits` (242), `argv_project_items` (247), `argv_reread` (252), `_project_item` (764), `rate_limit_wait` (418).
- launch.py: `PROMPT_PATTERN` (33), `ORIGIN_REPO` (50), `build_claim_prompt` (84), `launch_argv` (95), `retry_argv` (119), `check_origin` (233).
- cycle.py: `_TOP_KEYS` (58), `Config` (97), `load_config` (195), `_examine` (915), `_revalidate` (979; reread at 1012 to 1016), `_launch` (1026; prompt built at 1054, `_revalidate` called at 1058, launch outcome at 1099 to 1112), `_origin_ok` (670), `status_report` (1270), `CycleResult.launched_issue` (455).
- cli.py (issue_watch): group decorator 94, definition 95, `once_command` (118), exit constants (34 to 38).
- issue_pipeline/cli.py: `issue_pipeline_group` (about 58), verbs `release-worker` (decorator 200), `stage-status` (decorator 335), `record-create` (134), `adopt-create` (108).
- issue_pipeline/approval_record.py: `_approval_path` (132), `_ADOPTION_KEYS` (137), `_APPROVAL_KEYS` (140), `_EVIDENCE_KEYS` (153).
- issue_pipeline/brief.py: `build`, templates/worker-brief.txt sections `[head]`, `[marker]`, `[simple]`, `[medium]`, `[complex]`.
- Guard: src/superclaude/hooks/scripts/launch-level-guard.sh with tracked mirror plugins/superclaude/hooks/scripts/launch-level-guard.sh; `.claude/hooks/launch-level-guard.sh` is sync output and is not edited.

## Dependents
- `build_claim_prompt`: `cycle.py` `_launch` (1054) and `status_report` (1270), `tests/issue_watch/test_launch.py`, `test_security_invariants.py`. Named in Task 5.
- `check_origin`: `cycle.py` `_origin_ok` (670), `tests/issue_watch/conftest.py`, `test_launch.py`, `test_origin_parity.py`, `test_security_invariants.py`. Named in Task 11.
- `github.py` readers outside the watcher: `src/superclaude/cli/issue_pipeline/reads.py` (imports `github as gh`, `_argv_rest_page`). Named in Tasks 1 and 10.
- The literal `--pipeline none` appears in 24 files outside `.dev` (listed by Grep on 2026-11-19); Task 6 names them all.
- `CycleResult` consumers of a new `attempted_issue` field: `cli.py` `once_command`, `status_report`. Named in Task 17.

## Pre-check
- All files named by the tasks exist (checked with the Grep and find results of 2026-11-19), including `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` and the plugin guard mirror.
- Symbols resolve at the lines quoted (cycle.py lines read 1000 to 1130 on 2026-11-19; approval_record.py 1 to 30 and 130 to 155; issue.md 43, 44, 56).
- Verified gap behind Task 8: no `item-edit` and no `updateProjectV2ItemFieldValue` exists in `src` or `docs`.
- New modules are pure additions: `defaults.py`, `repos.py`, `generate.py`, `repo_init.py`, `first_run.py`, `dispatch.py`, `issue_pipeline/complete.py`, with the boundary test `tests/issue_watch/test_module_boundaries.py` to be satisfied.
