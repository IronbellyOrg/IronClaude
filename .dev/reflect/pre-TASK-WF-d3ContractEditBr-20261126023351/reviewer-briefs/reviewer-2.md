# Reviewer brief 2 (persona: qa, model class: haiku)

Mode: UC-1 pre-execution. You audit a PROPOSED plan against its driving brief. Read only. Do not run commands. Do not edit files.

Repository root: /home/coder/workspaces/IronClaude (branch docs/d3-dashboard-answer-counts-as-confirmation).
Spec (brief): /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/source.md
Plan: /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-WF-d3ContractEditBr-20261126-023139/TASK-WF-d3ContractEditBr-20261126-023139.md
Coverage matrix: /home/coder/workspaces/IronClaude/.dev/reflect/pre-TASK-WF-d3ContractEditBr-20261126023351/artifacts/coverage-matrix.md

## Codegraph run state
index_state: fresh; worktree_root: /home/coder/workspaces/IronClaude; projectPath: /home/coder/workspaces/IronClaude. Targets are Markdown and pytest files; use Grep and Read.

## Grounding hunks (the qa lens: testability and wording safety)
- The spec body (source.md) is the requirement list; the plan's acceptance criteria must each be checkable by a person or a test.
- Existing pinning tests to inspect: tests/skills/test_worker_contract.py (search for "executor-invented approval" and "owner_records"), tests/skills/test_task_workspace_lifecycle.py (search for "executor-invented"), tests/skills/test_implement_severity_static.py (line 410), tests/skills/test_workflow_archive.py (line 350), tests/sweep/test_classify.py (line 744).
- Current rule text: src/superclaude/core/WORKER-CONTRACT.md line 57; src/superclaude/skills/sc-implement-protocol/refs/qa.md lines 247-259.
- Is there a test that keeps plugins/superclaude/skills/sc-implement-protocol/ equal to src/superclaude/skills/sc-implement-protocol/? (search tests/ for "plugins/superclaude" and "sc-implement-protocol").

## Your job
Find concrete defects: an acceptance criterion that cannot fail, a test the plan forgets to update (Grep tests/ for the old phrases yourself and compare with Tasks 7 and 8), a regression the new text could introduce (for example a sentence that lets a relay or a file count), or an ambiguity an implementer could resolve the wrong way. For each: file:line evidence, consequence, grade (Blocking with reason Decision, Missing or Safety; Medium; Note), and a 4-category deviation class where the plan diverges from the brief. A zero-finding answer is valid only if you state what you checked.

Return a card with: findings (id, grade, file:line, evidence, consequence), per-task verdict, confidence 0.00 to 1.00 with a one-line reason.
