# Reviewer brief 1 (persona: analyzer, model class: sonnet)

Mode: UC-1 pre-execution. You audit a PROPOSED plan against its driving brief. Read only. Do not run commands. Do not edit files.

Repository root: /home/coder/workspaces/IronClaude (branch docs/d3-dashboard-answer-counts-as-confirmation).
Spec (brief): /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/source.md
Plan: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/TASK-WF-d3ContractEditBr-20261126-023139.md
Coverage matrix: /home/coder/workspaces/IronClaude/.dev/reflect/pre-TASK-WF-d3ContractEditBr-20261126023351/artifacts/coverage-matrix.md

## Codegraph run state
index_state: fresh; worktree_root: /home/coder/workspaces/IronClaude; projectPath: /home/coder/workspaces/IronClaude. Every file under audit is Markdown or a pytest file, so Grep and Read are the evidence.

## Grounding hunks
The plan names these existing places; verify each one exists and says what the plan says it says (cite file:line you re-Read):
- src/superclaude/core/WORKER-CONTRACT.md line 57 (WC-3 Ruling halt bullet), line 59 (WC-17), line 190, lines 256-278, lines 296-303
- src/superclaude/skills/sc-implement-protocol/refs/qa.md lines 215-220 and 247-259
- src/superclaude/skills/sc-implement-protocol/refs/ledger.md lines 62-82 and 193-199 (the regular expression at about line 71)
- tests/skills/test_worker_contract.py around line 3340; tests/skills/test_task_workspace_lifecycle.py lines 338-349
- plugins/superclaude/skills/sc-implement-protocol/refs/ (tracked mirror of the skill refs)

## Your job
Find concrete defects of the PLAN against the brief: a source requirement the plan misses or contradicts, a task whose acceptance criteria cannot show the change worked, a wrong file or line claim, a task order that breaks (Depends on), a task that would make an edit the brief forbids, or a case where following the plan would let a coordinator relay count as confirmation. For each defect give: file:line evidence, the consequence if left uncorrected, and a grade (Blocking with the reason: Decision, Missing or Safety; Medium; or Note). Classify any divergence of the plan from the brief under the 4-category taxonomy (Authorized expansion, Necessary deviation, Drift, Regression). A zero-finding answer is valid only if you state what you checked.

Return a card with: findings (id, grade, file:line, evidence, consequence), per-task verdict, confidence 0.00 to 1.00 with a one-line reason.
