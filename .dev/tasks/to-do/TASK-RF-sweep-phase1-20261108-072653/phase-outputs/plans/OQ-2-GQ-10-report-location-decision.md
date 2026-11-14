---
needs_human_decision: true
status: RESOLVED
---

# Sweep report location decision

## Question

> "G7 / AMBIGUITY 3: where the sweep report is written"

Question identifier: OQ-2 / GQ-10. Source: research package `gaps-and-questions.md:33`, with options in `research/research-notes.md:305`. Task items 7.1 and 7.2 require an explicit owner decision; an existing design default is not approval.

## Options

> "under `.dev/tasks/` (always staged by rule) or another `.dev/` folder; dated file name format."

- Option 1: "under `.dev/tasks/` (always staged by rule)". Reports become part of the staged task records.
- Option 2: "another `.dev/` folder". The proposed location is `<root>/.dev/sweeps/`, gitignored, with UTC file name `<YYYYMMDD-HHMMSS>-sweep.md`. This is the design/specification working default, not an owner decision.

## Recommendation

`<root>/.dev/sweeps/`, gitignored, file name `<YYYYMMDD-HHMMSS>-sweep.md`, as DESIGN and SPEC already state. This recommendation does NOT authorize adoption.

## Blocked work

Task item 9.1, step 1.6: the `--output` default.

Task item 7.2 must halt while this record is PENDING or Chosen is empty. Choosing a different location requires revising DESIGN sections 1, 3, 10 and 12 before implementation continues; item 7.2 defines that separate stop.

## Operator decision

OPERATOR DECISION: Approve the recommended report location and naming scheme.
Chosen: `<root>/.dev/sweeps/`, gitignored, UTC file name `<YYYYMMDD-HHMMSS>-sweep.md`.
Decided by: Ryan Wiancko, owner, 2026-11-09.
Decision source: In this session's report-folder question, the owner selected ".dev/sweeps/ (Recommended)". The selected option explicitly approved gitignored UTC reports and continuation. This resolves OQ-2/GQ-10 only; it is not a grant for unrelated decisions.
