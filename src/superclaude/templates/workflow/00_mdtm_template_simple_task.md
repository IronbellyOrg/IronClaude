---
version: ""
priority: "[High | Medium | Low]"
created_date: "YYYY-MM-DD"
---

# [Implementation workflow title]

<!-- For /sc:workflow to fill in; remove this comment and unused placeholders before handing the plan to /sc:implement.
Keep task IDs stable, order dependent tasks, and add phases only when they help navigation.
Each Task heading is one implementable change; acceptance criteria describe observable outcomes, not just "tests pass".
Use plain bullets, not checkboxes or numbered steps: /sc:implement treats those as separate tasks.
Every source requirement maps to at least one task; no requirement is silently dropped.
DO NOT invent requirements, paths, or APIs not found in the Source or the repo.
Each Task must stand alone (its reviewer sees only that task and the Constraints): name every file and source section it needs.
No task that only reads/loads context; fold reading into the task that uses it.
No separate "verify X" tasks; put the check in that task's acceptance criteria.
No bulk tasks ("update all handlers"); name each file or component.
For multi-item work, list every item explicitly in the plan; do not leave discovery to the executor.
Keep outputs and acceptance criteria inside each Task; no plan-wide Outputs/Success Criteria/Verification sections.
This is not an MDTM /task checklist; /sc:implement handles per-task review and the progress ledger. -->

Source: [PRD/spec path or feature request]
Goal: [Observable result the workflow delivers]

## Constraints

- [Actual scope limit, safety requirement, or non-goal; remove this section if none]

## Phase 1: [Outcome-based phase name]

## Task 1: [Verb + concrete deliverable]

[What to change and where; cite the source requirement or relevant existing files when known.]

Acceptance criteria:
- [Observable behavior or artifact, including the relevant path/interface when known.]
- [Specific check or test that demonstrates the change, if applicable.]

## Task 2: [Next change, only if independently reviewable]

Depends on: Task 1

[What to change and where; omit the dependency line if independent.]

Acceptance criteria:
- [Observable result and how to verify it.]
