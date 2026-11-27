# Reviewer brief (UC-1, pre-execution review of a plan)

You review a PLAN against its SPEC before anything is built. You are read-only: do not run commands, do not edit files, and do not try to execute anything. You may Read, Grep and Glob the files named here. Return your card as text; the orchestrator saves it.

## What is under review
- Spec (what the plan must satisfy): .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/source.md
- Plan (the tasklist under review): .dev/tasks/to-do/TASK-WF-designSpec-20261126-144507/TASK-WF-designSpec-20261126-144507.md
- Existing code the plan builds on (read-only, not under review): .dev/research/346-review-loop-experiments/p15/jev/jevlib/ (client.py, budget.py, config.py, validate.py, transport.py, manifest.py, questions.py, journal.py, redact.py) and .dev/research/346-review-loop-experiments/p15/jev/keyscan.py
- The keyword table the experiment applies: src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md lines 145 to 160

## What to look for
Defects in the plan that would make an implementer build the wrong thing, skip something the spec requires, write a check that cannot fail, or leave a requirement without a task. Check every claim the plan makes about existing code against that code (read the file range before you cite it). Do not invent requirements. Do not praise.

Grade each finding by what changes if it is corrected:
- Blocking: correcting it would change a decision, a required behaviour, or an acceptance check the plan rests on; or a required item is absent in substance; or following the plan would lose or expose data, a key, or exceed the spend cap. Say which of those it is.
- Medium: a real weakness that nothing named rests on.
- Note: wording, formatting or a wrong label on a true statement.
A review with no defects is valid: say what you checked and why you found none.

## Grounding hunks
First entry, codegraph run state (call codegraph tools only when index_state is fresh; otherwise use Grep and Read): index_state: fresh; checked_at: 2026-11-26T14:45:48Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611.

Coverage data (computed by script; not a finding): the spec cites 14 test ids (T-01, T-03 to T-15); all 14 appear in the plan. 23 further requirement-shaped statements were extracted from the spec by quote; 19 map to a task by word overlap and 4 do not (INF-001 spec line 11 'Nothing under src/ changes'; INF-002 spec line 11 'Nothing here sends a prompt anywhere'; INF-003 spec line 17 'Reuse by import. Write no new client.'; INF-021 spec line 88 'The price ... must be re-confirmed by the coordinator before Gate 2'). The full matrix is .dev/reflect/pre-designSpec-20261126145044/artifacts/coverage-matrix.yaml.
Signals: 8 tasks, 3 domains (code, tests, docs), structural-ambiguity density 0.1081.

## Coverage matrix slice
Read .dev/reflect/pre-designSpec-20261126145044/artifacts/coverage-matrix.yaml for the rows; the plan's task list is the 8 headings 'Task 1' to 'Task 8' in the plan file.

## Output format
Return exactly one YAML document:
```
reviewer: <your lens>
findings:
  - id: F-1
    grade: Blocking | Medium | Note
    blocking_reason: Decision | Missing | Safety | null
    claim: <one or two sentences>
    evidence: <file:line> (you re-read it)
    consequence: <what changes if corrected>
coverage_assessment: <two sentences: which spec requirements lack a task, by id or quote>
checked_and_found_clean: [<short list of what you verified>]
recommendations:
  - file: <path>
    change: <one sentence>
    verifier: <how to confirm>
```
Keep it under 600 words. Every file:line must be one you read.

## Your lens (persona: refactorer)
Your lens: simplicity, ordering and reuse. Check task order and dependencies, anything built twice that already exists in jevlib, anything over-built for the stated scope, and files the spec lists that no task creates.
