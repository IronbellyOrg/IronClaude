# Reviewer brief (UC-1, pre-execution audit; read-only, run nothing)
You audit a PROPOSED plan against its driving requirements.
Spec: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-010910/source.md  (requirements R1-R30; R24-R30 are new)
Plan: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-010910/TASK-WF-requirements-20261119-010910.md
Grounding: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-010910/artifacts/codegraph-grounding.md (index fresh; only Python and yaml are indexed)
Code under audit: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/src/superclaude/ and tests/ in the same checkout.
Prior review of an EARLIER plan version (same requirements, 12 findings M-1..M-13) is at /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/reflect/pre-TASK-WF-requirements-20261118-233559-20261118234500/adversarial/merged-output.md . This plan version claims to fix them. Check each fix really is in the plan (cite plan line), then look for NEW defects, especially in Tasks 4-9 (launch levels, completion update, Full Submit push rule) and in anything the fixes introduced.
Report each finding as: id, severity (blocking|medium|note), plan task and source row, evidence as file:line you actually Read, what changes if corrected. Blocking means correcting it changes a named decision/behaviour, or a required item is missing, or following the text would break a safety boundary. Tag anything unread [INFERRED]. A zero-finding result is valid if you say what you checked. Under 60 lines.

Persona: analyzer. Focus: do the files, lines and symbols the plan names exist (check at least 15), are Depends-on edges right, did the 12 earlier findings get fixed?
