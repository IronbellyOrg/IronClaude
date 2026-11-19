# Reviewer brief (UC-1, pre-execution audit)
You audit a PROPOSED plan against its driving requirements. Read-only. Do not run commands.
Spec (requirements): /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/source.md
Plan: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/TASK-WF-requirements-20261118-233559.md
Coverage matrix from Tier 1: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/reflect/pre-TASK-WF-requirements-20261118-233559-20261118234500/artifacts/coverage-matrix.md
Codegraph grounding: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261118-233559/artifacts/codegraph-grounding.md (index_state: fresh, projectPath: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb; only Python and yaml are indexed)
Source code under audit lives in /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/cli/issue_watch/ (read it to check line numbers and symbols the plan names).
Tier 1 findings to confirm or refute: (a) R20 only recorded, not verified; (b) lock/restart test automation (source.md:62) unmapped; (c) source.md:60 conflicts with R18; (d) Task 18 lacks Depends-on Task 4/6.
Report every finding as: id, severity (blocking|medium|note), plan task and source row, evidence as file:line you actually Read, and what changes if corrected. Tag anything you did not Read as [INFERRED]. A zero-finding result is valid if you state what you checked.
Deviation taxonomy for UC-1 is not needed; classify as coverage-gap, wrong-reference, ordering, safety, or contradiction.

Persona: analyzer. Focus: does every plan task name real files, lines and symbols that exist (verify at least 12 of the line numbers and symbols the plan cites) and are the Depends-on edges correct?
