<!-- TEMPLATE (agent 1). BMAD-conformant story record, written by the IronClaude coordinator ONLY, when a story is implemented and reviewed (event E7 in IRONCLAUDE-SIDE.md 5.2).
Path: {implementation_artifacts}/<story_key>.md  (BMAD's own name for a story file; e.g. _bmad-output/implementation-artifacts/12-3-decision-cards.md).
Why it exists: bmad-retrospective reads "the complete story file" of every story of the epic (skill line 241) and looks for sections named Dev Notes / Implementation Notes / Challenges, Review / Code Review, Lessons Learned, Technical Debt / Known Issues; bmad-create-story reads the previous story's Dev Agent Record. A story that exists only as an IronClaude plan package is invisible to both.
Everything below is copied from machine-written files (ledger progress.md, return-contract.yaml, review output); the coordinator adds no opinion. Never invent: write "Not recorded". The Status line follows the write-back mapping (review at PR open, done at closeout). -->

# Story <N>.<M>: <title>

Status: <ready-for-dev | in-progress | review | done>

## Story

As a <user>, I want <capability>, so that <benefit>.

## Acceptance Criteria

| Id | Criterion (verbatim from the story file) | Result | Evidence |
|---|---|---|---|
| S<N>.<M>-AC1 | Given ... When ... Then ... | pass / fail / not checked | ledger line or test name, with path |

## Tasks / Subtasks

(From the plan's tasks and the ledger: `T<id>: complete verdict=compliant ... ac=...`. One checkbox per task, marked from the ledger only.)

- [ ] T1 (AC: S<N>.<M>-AC1) <task title>

## Dev Notes

(Architecture decisions that bound the story, as copied into the story file, plus what the implementer found in the code. Section name kept because the retrospective searches for it.)

### Challenges

(Halts, retries, `E-HALT-QA` stops with the STOP code and how each was settled; "None recorded" if none.)

## Review

(Per-task QA verdicts and the final independent review result `FINAL: pass|issues`; PR review findings that were fixed, from the PR monitor's record. Section name kept because the retrospective searches for it.)

## Lessons Learned

(Only what the ledger, a review or a Ruling states explicitly. Otherwise "None recorded".)

## Technical Debt

(Gaps accepted by a Ruling, Medium findings not fixed, follow-up issues filed, each with its link. Otherwise "None recorded".)

## Dev Agent Record

### Agent Model Used

(As recorded by the commands, per step: panel, workflow, implement, review. "Not recorded" where the contract does not carry it.)

### Debug Log References

(Paths: plan package, ledger, return contracts.)

### Completion Notes List

### File List

(From the ledger `files=` fields, paths relative to the repository root.)

## Change Log

(Date, event, who wrote it: coordinator session.)
