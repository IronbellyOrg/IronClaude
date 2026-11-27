# Codegraph grounding

## Run state

- index_state: fresh (status: 0 added, 0 modified, 0 removed)
- checked_at: 2026-11-26T16:12:56Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-703
- projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-703
- access: mcp
- degraded: graph:stale-edges-note (status reported 93702 unresolved references from an interrupted run, so caller edges may be incomplete; every dependent below was confirmed with Grep and Read)

## Resolved symbols

- `archive` at `src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py:404` (Read)
- `_add_unresolved` at `:280`, `_contract_edit` at `:394`, `_key_idx` and `_block_end` at `:224-246` (Read)
- `place` at `:598`; guard at `:608-609` (Read)
- Test helpers `repo`, `make_pkg`, `repaired_copy`, `review_file` in `tests/skills/test_workflow_remediation.py` (Read)

## Dependents

- `archive`: one caller, `main` (`remediate.py:733`, `add("archive", ...)`), confirmed by codegraph_callers and Grep (call-site-verified); tests call `rm.archive` directly.
- `_contract_edit`: called by `archive` (`:443`) and by `mark` (`:576`); the fix must not change it.
- Documentation consumers of the recording wording: `SKILL.md`, `refs/remediation.md`, `commands/workflow.md` and their plugin mirrors.

## Pre-check

Files named by tasks exist and their symbols resolve; no unlisted dependent of the touched symbols found. The `mark`/`_contract_edit` dependent is covered by Task 1's constraint to leave `_contract_edit` unchanged.
