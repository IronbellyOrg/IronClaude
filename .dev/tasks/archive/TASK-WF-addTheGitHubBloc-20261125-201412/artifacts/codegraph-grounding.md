# Codegraph grounding for TASK-WF-addTheGitHubBloc-20261125-201412

## Run state

- index_state: fresh
- checked_at: 2026-11-25T20:14:20Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-848
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-848
- access: mcp
- tokens: none (Markdown files are not indexed, so the four Markdown targets were read directly; this is normal evidence, not a failure)

## Resolved symbols

- tests/skills/test_issue_protocol.py (outline via codegraph_node symbolsOnly): helpers `_text`, `_wave`, `plan_section_problems`, constants `ROOT`, `SKILL`, `REFS`, `COMMANDS`; last test `test_stage_claim_skips_recommend_and_plain_claim_keeps_it` (line 1162); pinned tests `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones`, `test_the_coordinator_handoff_is_the_same_paragraph_in_all_three_files`, `test_st11_no_source_tree_path_in_the_command_file`, `test_skill_frontmatter_and_size`, `test_no_source_tree_path_in_skill_files`.
- Read directly: refs/claim.md Wave 2 (lines 36 to 44), Wave 3 (46 to 51), Final output (138 to 150); SKILL.md Claim mode item 3 (line 86) and Error handling table (lines 154 to 177); commands/issue.md `--claim` bullet (line 16); HOW-WE-WORK.md `/sc:issue` row (line 296); plugin guide copy is byte-identical (cmp).

## Dependents

- tests/skills/test_issue_protocol.py (reads claim.md, SKILL.md, commands/issue.md)
- tests/commands/test_routing_plugin_parity.py (guide copy parity)
- tests/commands/test_issue_command.py (line 245 reads `refs/claim.md`)
- tests/issue_pipeline/test_brief.py (line 19 reads claim.md)
- tests/issue_watch/test_marker_contract.py (line 20 reads claim.md)
- tests/skills/test_issue_orca_worktree.py (lines 1789, 2184 read claim.md, including `## Final output`)
- tests/skills/test_worker_contract.py (lines 2954 to 2986 name claim.md)
- tests/core/test_how_we_work_routing_table.py and tests/cli/test_how_we_work_install.py (read HOW-WE-WORK.md)

## Pre-check

- Files named by the plan exist: 8 of 8 (claim.md, SKILL.md, commands/issue.md, HOW-WE-WORK.md, plugin guide copy, test_issue_protocol.py, test_issue_command.py, test_routing_plugin_parity.py).
- Symbols named by the plan resolve: yes (list under Resolved symbols).
- Dependents the plan did not name before this check: tests/issue_pipeline/test_brief.py, tests/issue_watch/test_marker_contract.py, tests/skills/test_issue_orca_worktree.py, tests/skills/test_worker_contract.py, tests/core/test_how_we_work_routing_table.py, tests/cli/test_how_we_work_install.py. Task 6 now lists them in its acceptance criteria.
