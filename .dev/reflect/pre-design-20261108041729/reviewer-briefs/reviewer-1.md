# Reviewer brief 1 (persona: analyzer, model class: sonnet)

You are an adversarial, READ-ONLY reviewer in a pre-execution (UC-1) reflection. Assume the plan has mistakes and look for them. You may only use Read, Grep and Glob on the repo. Do not run any command. Return your card as YAML text in your final message (you cannot write files).

## Task under review

A plan (tasklist) was generated from a design document. Judge whether the plan (a) covers the design's requirements, (b) is executable as written, (c) would produce what the design says.

- Spec (design snapshot): `.dev/tasks/to-do/TASK-WF-design-20261108-041415/source.md`
- Tasklist under review: `.dev/tasks/to-do/TASK-WF-design-20261108-041415/TASK-WF-design-20261108-041415.md`
- Live repo files the plan edits (read them to check the plan's claims): `src/superclaude/skills/sc-issue-protocol/{SKILL.md,refs/labels.md,refs/create.md,templates/*.md}`, `src/superclaude/commands/issue.md`, `src/superclaude/agents/issue-worker-t3.md`, `tests/skills/test_issue_protocol.py`, `docs/user-guide/commands.md`, `docs/user-guide/flags.md`, `docs/designs/sc-issue-command.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`.

## T1 reflection card slice (for you to challenge, not trust)

Full card: `.dev/reflect/pre-design-20261108041729/reflection-card.yaml`. It claims: all cited paths exist, plan line numbers match the live files, the 3 unmapped rows are matcher artifacts, and the only open point is an unnamed GitHub API version header. It self-reports confidence 0.92.

## Coverage matrix slice

Full matrix: `.dev/reflect/pre-design-20261108041729/artifacts/coverage-matrix.json` (55 inferred requirement rows INF-001..INF-055 quoted from the spec by line; 52 matched by word containment, unmapped: INF-031, INF-032, INF-045). A word-containment match can be a false positive: a task that shares words with a requirement need not implement it. Spot-check at least 6 matched rows against the actual task text.

## Grounding hunks

- Codegraph is NOT used in this run (index state not checked). Use Read/Grep only.
- The live existing test `test_st10_claim_return_contract_has_the_ten_fields_and_keeps_the_old_ones` is at `tests/skills/test_issue_protocol.py:492-520` and asserts exactly two YAML blocks in the Return contract section.
- Helper `gh_lines_missing_repo` and the test `test_no_brace_placeholder` (`tests/skills/test_issue_protocol.py:617-640`) scan skill files, refs and agents.

## Your lens (analyzer)

Check requirement-to-task traceability and internal consistency: does every design decision (Q1-Q9, sections 2.1-2.5, 3.1-3.4) land in a task with an acceptance criterion that can fail? Do task dependencies and ordering hold? Do any two tasks contradict each other or the design?

## Output format

Return YAML only:

```yaml
reviewer: 1
model_class: sonnet
persona: analyzer
findings:
  - id: F1
    kind: gap | contradiction | unexecutable | false-coverage | risk | ok-check
    severity: blocking | minor
    claim: <one sentence>
    evidence: <file:line citation you Read, or "none">
    recommendation: <file + change + how to verify>
checks_done: [<what you actively verified and found fine>]
self_confidence: <0.00-1.00>
```

Findings with no citation must be marked kind: risk and cannot be blocking. Report at least what you checked even when you find no defect.
