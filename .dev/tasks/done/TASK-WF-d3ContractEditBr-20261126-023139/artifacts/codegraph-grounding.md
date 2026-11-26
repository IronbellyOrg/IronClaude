# Codegraph grounding

## Run state

- index_state: fresh (codegraph_status earlier in this run: 0 changed files)
- checked_at: 2026-11-26 (UTC)
- worktree_root: /home/coder/workspaces/IronClaude
- projectPath: /home/coder/workspaces/IronClaude
- access mode: MCP tools
- token: graph:markdown-targets (every target file is Markdown or a pytest file that quotes Markdown; codegraph indexes symbols, so Grep and Read are the evidence here)

## Resolved symbols

No code symbol is changed. The rule text lives in these Markdown files (all under src/superclaude/):

- core/WORKER-CONTRACT.md: WC-3 Ruling-halt bullet (line 57), WC-17 (line 59), line 190 (what a coordinator never does: "writes or drafts a Ruling"), lines 256-278 (resume after a Ruling), lines 296-303 (issue pipeline: plan approval, completion, "Never").
- skills/sc-implement-protocol/refs/qa.md: lines 215-220 (accepted-minor versus Ruling table), 247-259 (Halt table rows and the paragraph "A Ruling counts only when...").
- skills/sc-implement-protocol/refs/ledger.md: lines 62-82 (Ruling line grammar and regex `^T([0-9A-Za-z.-]+): Ruling: .+ — .+ — .+$`), 193-199 (examples).
- skills/sc-implement-protocol/refs/retry.md: lines 498-500 (Ruling eligibility rule; about timing of the line, not who confirms).
- skills/sc-implement-protocol/refs/managed-workspace.md line 76; SKILL.md lines 41, 58, 149-150, 193; commands/implement.md line 107; core/HOW-WE-WORK.md line 114.

## Dependents

Tests that pin the current text (they must change with it):

- tests/skills/test_worker_contract.py around lines 3340-3356 (test_owner_records_are_given_in_chat_and_recorded_by_the_agent)
- tests/skills/test_task_workspace_lifecycle.py lines 338-349, 485, 878
- tests/skills/test_implement_severity_static.py line 410
- tests/skills/test_workflow_archive.py line 350
- tests/sweep/test_classify.py line 744

Code that checks approvals (not edited; follow-up list only): src/superclaude/cli/issue_pipeline/cli.py (line 252 text: run only under the issue's grant row), src/superclaude/cli/issue_pipeline/complete.py (docstring line 3), src/superclaude/cli/sweep/classify.py (lines 176, 182: Ruling halt classification), src/superclaude/skills/sc-implement-protocol/scripts/archive_workspace.py (line 54 Ruling regex, line 381 archive check "without matching user-authorized Ruling").

## Pre-check

(filled in at the Wave 4 pre-check)
