# Refactoring Plan: Merge into Base (Variant 2)

## Overview
- Base: Variant 2 (option B document, `variant-2-original.md`; chosen by score and by the edge-case floor, not by the debate verdict)
- Incorporating strengths from: Variant 1 (option A document), plus verified debate evidence
- Planned changes: 7
- Risk level: Medium overall (change 1 reverses the decision the base document argues for; the rest are additive)
- Output file: `D-P2-25-merged-decision.md` in the result directory (one level above `adversarial/`)
- Output shape: a decision record with these sections, in order: Decision; Why option A; Why not option B; What option A gives up; Edits required; Open points. The shared "How to judge" section is dropped from the output because it is the debate brief, not part of the decision (recorded in change 7).

## Planned Changes

### Change 1: Replace the mechanism with option A (from Variant 1)
- **Source**: Variant 1, first paragraph
- **Target**: Base, first paragraph (replace)
- **Rationale**: Debate matrix: A wins 9 of 14 points, B wins 1, 4 lean A (`debate-transcript.md`, Scoring Matrix; both advocates recommended A). Base text keeps its coverage structure but states the verdict for A: under `--unattended`, Part 3 writes `release-1-spec.md`, `release-2-spec.md` and `boundary-rationale.md` (or `release-spec-validated.md` for no split) with the Write tool and makes no nested command call; release-split's nested list stays brainstorm and adversarial. Cites `SKILL.md:281`, `release-split.md:119`, `SKILL.md:312-320`.
- **Integration point**: Section "Decision", at the top of the file
- **Risk**: Medium (restructures the base's central claim)

### Change 2: Add the reasons for A (from Variant 1, "Claimed strengths", U-001)
- **Source**: Variant 1, Claimed strengths
- **Target**: Base, new section "Why option A"
- **Rationale**: S-002 (85%), S-003 (92%): the text is already in the working tree; pinned tests already match (`test_worker_contract.py:1391`, `:1466`, `:482`); deterministic path with no choice among three commands (A-002); reuses the existing Error Handling row (`SKILL.md:439`); section 2.1 binds a command that invokes another, it does not oblige a call (`WORKER-CONTRACT.md:24`; C-004 and X-001, lean A, 55%).
- **Integration point**: After "Decision"
- **Risk**: Low (additive)

### Change 3: Add the evidence against B (from the debate, both advocates)
- **Source**: Debate transcript, points C-002, C-003, C-005, C-006, X-002
- **Target**: Base, new section "Why not option B"
- **Rationale**: Verified, with the B advocate's own concessions: `/sc:workflow` writes a plan package, not a spec (`workflow.md:80`); `/sc:tasklist` is a roadmap-to-tasklist generator (the sc-tasklist-protocol skill description), so it does not turn a split proposal into a spec, and `SKILL.md:279` says not to use it unless the proposal says so; design and workflow take `--report-dir` only (`design.md:96`, `workflow.md:71`) while release-split's idiom is `--unattended --output`; tasklist reaches `sc:task` (`tasklist.md:114`); two tasklist HALT-as-blocked gates (`tasklist.md:113`) would stop release-split after Parts 1-2 (`WORKER-CONTRACT.md:25`); the workflow package sits outside `nested/workflow-<n>/` and its staging is left to the coordinator (`workflow.md:76`).
- **Integration point**: After "Why option A"
- **Risk**: Low (additive, every line cited)

### Change 4: Correct the inaccurate staging claim (base content modified)
- **Source**: Base text "workflow and tasklist write packages under `.dev/tasks`, which a worker must not stage"; Pass 2 finding R1 on Variant 1 ("stage files")
- **Target**: Base, the staging sentence (replace)
- **Rationale**: Verified facts: workflow "does not stage `.dev/tasks`" (`workflow.md:76`); tasklist "pushes, commits and stages nothing" (`tasklist.md:115`). The accurate cost is a package written outside the nested directory that must be listed in `artifacts`, not an actual staging breach. The merged text states only that.
- **Integration point**: Inside "Why not option B"
- **Risk**: Low

### Change 5: Add what option A gives up (from Variant 2, U-002, U-003, C-001)
- **Source**: Variant 2, Claimed strengths; Variant 1, Claimed weakness
- **Target**: Base, new section "What option A gives up"
- **Rationale**: C-001 (B wins, 70%): the callees' structure and checks are lost; U-002: a separate nested contract per spec for the coordinator; U-003: design's no-architecture-change guard (`design.md:98`). The residual protection is Part 3's traceability rule (`SKILL.md:303`) and Part 4's inline fidelity verification (`SKILL.md:331`). The narrowed-B variant (design only) is recorded here as considered and not preferred, with the reasons in the debate transcript's facilitator note.
- **Integration point**: After "Why not option B"
- **Risk**: Low

### Change 6: Add the edit list (new content, edge-case coverage)
- **Source**: Rubric criteria L5, E1, E4 (Variant 1 and Variant 2 both lack them)
- **Target**: Base, new section "Edits required"
- **Rationale**: Answer to the lead's question: with A winning, no edit is needed in `SKILL.md`, `release-split.md`, `tests/skills/test_worker_contract.py` or the spec row. Optional wording polish, not recommended under scope discipline: (a) `SKILL.md:281` says "the specs" while Part 3 also writes `boundary-rationale.md` and, for no split, `release-spec-validated.md` (the Behavioral Instructions and Outputs at `SKILL.md:283-320` cover them, so the gap is wording only); (b) "the fallback of the Error Handling table" is loose because the callee is available (S-004).
- **Integration point**: After "What option A gives up"
- **Risk**: Low

### Change 7: Add the open points and drop the shared brief (new content)
- **Source**: Debate Convergence Assessment; diff-analysis Metadata
- **Target**: Base, new section "Open points"; base section "How to judge" removed
- **Rationale**: Records the 4 unresolved points (S-001, S-004, C-004, X-001), the debate's NOT_CONVERGED status at 71.4% against 80%, and the UNVERIFIED items: the interaction with D-P2-24 and D-P2-13 was not read; the claim that quality of inline output is lower is unmeasured. The shared "How to judge" text is identical in both inputs and is the debate brief, so it is not carried into the decision record.
- **Integration point**: End of file
- **Risk**: Low

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 | Keep the callees' structure and checks (base's strength) | Kept as an acknowledged cost in change 5; both advocates discount the gain (A-003): the real protection is Part 3 traceability and Part 4 |
| S-001 | B's delegation of spec authoring | Not adopted: debate lean A (55%), deliverable mismatch (C-002, 95%) |
| X-001, C-004 | "B follows section 2.1 literally" | Not adopted: `WORKER-CONTRACT.md:24` applies to a command that invokes another command; it does not require a call (lean A, 55%) |
| U-002 | Per-spec nested contracts | Not adopted: no nested Part 3 call exists under A; recorded as a cost |
| Narrowed B | Call `/sc:design` only | Not adopted: still adds a nested entry and test and spec edits, needs the Part 3 rules handed to a generic design command, and needs several calls |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | Output states the wrong verdict | Re-read the debate matrix; restore the base paragraph |
| 2 | Low | A cited line number is stale | Re-verify with Read |
| 3 | Low | A cited line number is stale | Re-verify with Read |
| 4 | Low | Staging claim misstated | Re-read `workflow.md:76`, `tasklist.md:115` |
| 5 | Low | Cost of A understated | Re-read debate C-001, U-002, U-003 |
| 6 | Low | A needed edit missed | Re-run the pinned tests listed |
| 7 | Low | Open item dropped | Re-read Convergence Assessment |

## Review Status
- [x] Auto-approved (default; `--interactive` not set)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-07
