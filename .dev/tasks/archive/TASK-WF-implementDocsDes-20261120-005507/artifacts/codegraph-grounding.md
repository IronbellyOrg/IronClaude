# Codegraph grounding

## Run state

- index_state: fresh
- checked_at: 2026-11-20T00:55:11Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-624
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-624
- access: mcp (codegraph_status, codegraph_node listed)
- tokens: none (markdown targets are not indexed; Grep and Read grounded them)

## Resolved symbols

- `src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py`: `rename_noreplace` (:88), `archive` (:477), `validate` (:278), `ID_RE` (:42); no other indexed file depends on it.
- `src/superclaude/cli/reflect/panel_lint.py`: `STABLE_FIELDS_1_8_0` (:33), `CONTRACT_VERSION` (:185), `lint_panel_contract` (:302); used by `scripts/reflect_shadow_exit.py` and `tests/cli/reflect/test_panel_contract_lint.py`.
- `src/superclaude/cli/reflect/runner.py:765` reads `result.remediation_plan_path`; `_apply_remediation` (:582) runs `/sc:implement <path>` and a non-zero rc stops the loop (:772-782).

## Dependents

- Files holding "1.8.0": `scripts/reflect_consumer_inventory.py`, `scripts/reflect_shadow_exit.py`, `scripts/reflect_verdict_replay.py`, `src/superclaude/cli/reflect/contract.py`, `models.py`, `panel_lint.py`, reflect `SKILL.md`, `refs/grader-extensions.md`, `refs/remediation-handoff.md`, `refs/report-template.md`, `tests/cli/reflect/test_panel_contract_lint.py`, `test_shadow_skill_contract.py`, `test_shadow_exit_script.py`, `test_verdict_replay_script.py`, `tests/review/test_reflect_consumer_inventory.py`, three fixtures under `tests/cli/reflect/fixtures/`.
- Workflow contract "1.1" pins: `managed-workspace.md:10`, `archive_workspace.py:327`, `refs/return-contract.md:6`; tests `tests/skills/test_workflow_archive.py`, `test_task_workspace_lifecycle.py`, `test_task_workspace_smoke.py`, `test_worker_contract.py`.
- Plugin mirrors that exist and were byte-identical when planned: `plugins/superclaude/skills/sc-workflow-protocol/`, `plugins/superclaude/skills/sc-implement-protocol/`; the reflect protocol has no mirror.
- Superseded packages in `to-do/` by contract text: seven own-contract hits plus two that are not migrated (see Task 13).

## Pre-check

13 tasks checked. Every existing file a task names exists (spot-checked: review-loop prompts, reviewer-spec.md, reflect tests and fixtures, plugin HOW-WE-WORK copy, archive folder). New files by design: `scripts/remediate.py`, `refs/remediation.md`, `tests/skills/test_workflow_remediation.py`. The workflow skill has no `scripts/` folder yet. Dependents no task names (found later by the reflect reviewers, see REPORT.md): `tests/commands/test_workflow_command.py` and `plugins/superclaude/commands/workflow.md`, the git-HEAD tests in `tests/cli/reflect/test_shadow_skill_contract.py`, `scripts/reflect_shadow_exit.py`, `sc-implement-protocol/refs/qa.md` STOP list.
