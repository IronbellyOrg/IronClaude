# Reviewer brief (UC-1, pre-execution review of a plan)

You review a PLAN against its SPEC before anything is built. You are read-only: do not run commands, do not edit files, and do not try to execute anything. You may Read, Grep and Glob the files named here. Return your card as text; the orchestrator saves it.

## What is under review
- Spec (what the plan must satisfy; its section 'Revision 1' at the end wins over sections 3 to 8 where they differ): .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/source.md
- Plan (the tasklist under review): .dev/tasks/to-do/TASK-WF-designSpec-20261126-152817/TASK-WF-designSpec-20261126-152817.md
- Existing code the plan builds on (read-only, not under review): .dev/research/346-review-loop-experiments/p15/jev/jevlib/ (client.py, budget.py, config.py, validate.py, transport.py, manifest.py, questions.py, journal.py) and .dev/research/346-review-loop-experiments/p15/jev/keyscan.py
- The keyword table the experiment applies: src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md lines 150 to 160 (the cue rows are lines 153 to 158)

## What to look for
Defects in the plan that would make an implementer build the wrong thing, skip something the spec requires, write a check that cannot fail, or leave a requirement without a task. Check every claim the plan makes about existing code against that code (read the file range before you cite it). Do not invent requirements. Do not praise.

Grade each finding by what changes if it is corrected:
- Blocking: correcting it would change a decision, a required behaviour, or an acceptance check the plan rests on; or a required item is absent in substance; or following the plan would lose or expose data, a key, or exceed the spend cap. Say which of those it is.
- Medium: a real weakness that nothing named rests on.
- Note: wording, formatting or a wrong label on a true statement.
A review with no defects is valid: say what you checked and why you found none.

## T1 card excerpt
The first-pass reviewer's findings relevant to your lens (a lead to confirm or reject by reading the file yourself, not a verdict):
- F-1 (Medium): Gate 2's `spend_bound` check needs the text of every frozen prompt to estimate the whole-run tokens, but the plan also says `gate1` and `gate2` hash files only and never call the corpus loader. The plan does not say how the gate gets the prompts.
- F-3 (Medium): Gate 2 refuses when any `run_end` event exists, and `execute` writes `run_end` also when the whole-run reservation is refused before any post. So a run that sent nothing blocks every later Gate 2.
- F-5 (Note): The `run` subcommand does not say what happens when `TYPESAFE_API_KEY` is unset after both gates pass: the exit code, and whether a `run_end` event is written.

## Grounding hunks
First entry, codegraph run state (call codegraph tools only when index_state is fresh; otherwise use Grep and Read): index_state: fresh; checked_at: 2026-11-26T14:45:48Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-611; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-611.

Coverage data (computed by script; not a finding): the spec cites 14 test ids (T-01, T-03 to T-15); all 14 appear in the plan. 44 further requirement-shaped statements were extracted from the spec by quote; 35 map to a task by word overlap and 9 do not (INF-001, INF-002, INF-003, INF-005, INF-006, INF-014, INF-018, INF-021, INF-027); the plan's Constraints and Tasks 3, 4 and 6 carry most of them in different words. The full matrix is .dev/reflect/pre-designSpec-20261126153331/artifacts/coverage-matrix.yaml.
Signals: 8 tasks, 3 domains (code, tests, docs), structural-ambiguity density 0.1552.

## Coverage matrix slice
Read .dev/reflect/pre-designSpec-20261126153331/artifacts/coverage-matrix.yaml for the rows; the plan's task list is the 8 headings 'Task 1' to 'Task 8' in the plan file.

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

## Your lens (persona: analyzer)
Your lens: root-cause and evidence. Test whether each plan claim about existing code (what a function returns, raises, reads, or defaults to) is true by reading that code, and whether acceptance checks could fail for the reason they state.
