# Codegraph grounding: TASK-WF-stage1Request-20261116-221852

## Run state

- index_state: fresh (`codegraph_status`: 3668 files, "Changes since index: 0 added, 0 modified, 0 removed")
- access: mcp
- checked_at: 2026-11-16T22:19:30Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- projectPath: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel
- tokens: none

## Resolved symbols

Read from the live files on 2026-11-16 (Read/Grep confirmed; graph rows are leads only).

| Named by the source | Resolved to |
|---|---|
| `src/superclaude/cli/review/__init__.py` | `review_group` (click group `review`) and the loop over the module-name tuple (`panel_cmd`, `merge_cmd`, `ledger_cmd`, `telemetry_cmd`, `lint_cmd`, `estimate_cmd`, `cluster_cmd`, `verify_cmd`, `manifest_cmd`); a missing module is skipped only when the missing name is the module itself; each module must export `command` |
| `superclaude review` subcommand names today | `panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations`, `manifest`; `lint_cmd` and `estimate_cmd` have no module |
| `safety_route.py`, `safety_cmd.py`, `tests/review/test_review_safety_route.py`, `tests/review/test_review_safety_cmd.py` | none exists yet (new files) |
| `sc-implement-protocol` `SKILL.md` | "### Whole-list review" and "## Done" sections present; the plugin twin under `plugins/superclaude/skills/sc-implement-protocol/` is byte-equal today for `SKILL.md`, `refs/managed-workspace.md` and `refs/qa.md` |
| `refs/managed-workspace.md` | the code block holding `FINAL: <pass\|issues> evidence=<ev-list> state=<sha256>` is followed by the line beginning "6. `pass`"; step 2 ("`--skip-final-review`") and step 5 ("Re-run step 3.") are present |
| `refs/qa.md` | SHA-256 `93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004` in both the source and the plugin twin on 2026-11-16 |
| `test_h_implement_protocol_plugin_twins_byte_equal` | `tests/skills/test_review_severity_rule.py` line 371 |
| the pinned tests of the plan's Task 2 | all 11 files named there exist, plus `tests/review/test_review_cli.py` |

## Dependents

- `review_group`: imported by `src/superclaude/cli/main.py` (adds it as `review`); the package is used by 28 files (codegraph, rows are leads). Task 1 changes only the tuple, so no caller changes.
- `SKILL.md` and `refs/managed-workspace.md` of `sc-implement-protocol`: read by the tests named in Task 2 (static pin scans, byte-equal twin test, lifecycle and smoke tests, archive and saved-prompt tests, install file lists). Three more tests mention the skill and are added to the Task 2 run: `tests/skills/test_implement_retry_revert.py`, `tests/skills/test_implement_retry_citation.py`, `tests/skills/test_implement_adviser_family.py`.

## Pre-check

Run on 2026-11-16 with the fresh index of the run state above; Grep and Read confirmed each row.

- Task 1: the three existing paths it names resolve (`src/superclaude/cli/review/__init__.py` and the seven subcommand names; the tuple holds the optional `lint_cmd` and `estimate_cmd` with no module). The four new files do not exist yet, as the task expects. `tests/review/test_review_cli.py` exists (its `test_review_help_lists_the_subcommands` is the help-listing test the new command must keep green). `make lint` and `make verify-sync` are Makefile targets.
- Task 2: `SKILL.md` has "### Whole-list review" and "## Done"; `refs/managed-workspace.md` has the `FINAL:` code block, step 5 and step 6 as the task quotes them; both plugin twins and `refs/qa.md` are byte-equal to their sources (SHA-256 `93e232f5...af004`); `test_h_implement_protocol_plugin_twins_byte_equal` exists. All 14 test files named in the task exist.
- Dependents of the touched files that no task names: `tests/hooks/test_launch_level_guard.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/commands/test_workflow_command.py` and `tests/skills/test_model_alias_policy.py` mention `sc-implement-protocol`; they are not run by Task 2 and may read the edited files. Not added to the plan's test list because the paragraph adds no model alias, routing row or hook text; a failure in one of them after Task 2 is a defect of the edit.
- Nothing in the plan names a file that is absent, and no symbol it names fails to resolve.
