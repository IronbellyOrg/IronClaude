# ABANDONED — TASK-RF-20260403-tasklist-e2e

Closed: 2026-05-17
Status when stalled: To Do (research + QA only; never executed)

## Why never executed

The task was build-validated (research 5 files, QA 4 files including
20/20 PASS task-integrity report dated 2026-04-02) but the execution
phase never produced any `phase-outputs/` artifacts. Same April-cohort
anti-instinct gate failure context as sibling `TASK-RF-20260403-full-e2e`.

## Why superseded

Deliverable substantially exists on disk:
- `.dev/test-fixtures/results/test1-tdd-prd-v2/tasklist-index.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/phase-{1,2,3}-tasklist.md`
- `.dev/test-fixtures/results/test1-tdd-prd-v2/validation/ValidationReport.md`
  (8 findings, full TDD/PRD enrichment matrix)

Sibling tasks `TASK-RF-20260403-baseline-full-e2e` (Done) and
`TASK-RF-20260403-quality-comparison` (Done) consumed and compared
these results.

## ⚠️ Live-reference warning

`.dev/releases/current/task-sc-task-directional-merge/` names this task
as a Tier-classification Target — 30 occurrences across 5 files,
including in `roadmap/TDD_TASK_DIRECTIONAL_MERGE.md` and
`validation-spec/validation-spec.md`, with the instruction "reinstate to
H-4 if promoted to in-flight before Step 5".

When the directional-merge release next sees authoring, those refs
should be updated to point at this `.dev/tasks/done/` location. Not
done here to avoid touching an active release mid-flight.
