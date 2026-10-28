# QA Report: Controls and Limitations (Partition a)

**Topic:** Phase 2 research on repeated planning and implementation reviews  
**Date:** 2026-10-23  
**Phase:** phase-gate  
**Lens:** controls-limitations  
**Fix cycle:** Initial review  
**Fix authorization:** false

## Overall Verdict: PASS

**VERDICT: PASS**

No issues were found within the assigned controls-and-limitations lens. This verdict covers only this partition, not the complete Phase 2 gate.

## Scope Reviewed

All five assigned targets were read completely.

| Key | Absolute target path |
|---|---|
| A | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md` |
| B | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/02-session-a9b88895.md` |
| C | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md` |
| D | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-05.md` |
| E | `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md` |

The actual acceptance paragraphs for Steps 2.4-2.8, the dispatch instructions, the governing report template, and the prepared output stub were also read.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Supporting sources outside the subset were read only to verify relevant controls and limitations. Full cross-file verification requires merging all partition reports.]

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Operational negative controls remain separate from repeated failures | PASS | C preserves the nine compliant task reviews and excludes later shared-ledger failures from that session. Independently extracted all nine original notifications and read the shared ledger. |
| 2 | Synthetic and setup-only sessions do not inflate operational cases | PASS | C and D exclude seven synthetic sessions and one setup-only session. Direct parsing confirmed zero tool calls in all eight files and literal mock-counter content in the seven synthetic sessions. |
| 3 | Successful repairs remain visible despite a later failure | PASS | B preserves three successful repairs separately from the retained frozen-fixture defect. The complete second-review artifact confirms all three corrections and exactly one remaining finding. A also preserves successful, non-recurring amendments rather than labeling every later finding a failed repair. |
| 4 | Session and source-family clustering constrain interpretation | PASS | C treats the planning revisions as one incident and separates the related implementation stage. B and D exclude opening carryover history and repeated notifications. No population-level prevalence or independent-case claim appears in the assigned conclusions. |
| 5 | Modification-time selection and live-source limits remain bounded | PASS | The frozen manifest explicitly defines selection by modification time, not event time. Assigned screens identify their fixed slots and source captures. Direct fingerprints matched preserved captures for all 11 inspected source files. Conclusions remain case-specific; no immutable membership claim is used to imply permanently immutable contents. |
| 6 | Authorization, retained defects, and unreviewed endpoints are not mislabeled repaired | PASS | Original oracle-session records distinguish the restricted repair, retained finding, later user authorization, passing correction review, and archive refusal. Original planning-session records confirm narrowed review scope and explicit disclosure that the final amendment had not been reviewed. A and B preserve these distinctions. |
| 7 | Missing history and unknown earlier-miss causes constrain causal conclusions | PASS | A explicitly leaves unobservable reviewer-miss causes unknown. B preserves the absence of a separate historical full-oracle snapshot and disclaims live-model effectiveness. Neither converts these limits into proof of reviewer psychology or universal repair impossibility. |
| 8 | Current protocol instructions are not presented as historical execution or comprehensive enforcement | PASS | E labels its analysis as current protocol-source evidence and expressly withholds historical compliance conclusions. Direct reads confirmed the current acceptance, retry, resume, single-writer, archive-review, and digest-coverage limitations. |

## Summary

- Checks passed: **8 / 8**
- Checks failed: **0**
- Critical issues: **0**
- Important issues: **0**
- Minor issues: **0**
- Issues fixed in-place: **0**
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 30 calls (27 returned content; 3 returned unchanged-file reminders) | Grep: 0 | Glob: 0 | Bash: 3
- External research: None. No web lookup or external transmission was needed.

Confidence measures completion of this focused checklist. It does not remove the historical uncertainties honestly recorded in the targets.

## Issues Found

None within this partition and lens.

## Actions Taken

- Read every assigned target and its actual task acceptance paragraphs.
- Inspected bounded original event excerpts, complete relevant oracle reviews, the targeted planning verdict, current protocol sources, and the shared progress ledger.
- Independently checked source fingerprints, synthetic-session exclusions, and the frozen-fixture correction.
- Made no target edits, report-file writes, Git operations, test runs, or external publications.

**Verification recovery:** An initial byte-comparison attempt replaced the first matching false-valued field in the fixture rather than the intended record, so that comparison returned false. A subsequent physical-line comparison found exactly one changed line, line 600. Replacing that specific field reproduced the current file byte-for-byte; structural comparison also showed exactly the stated field correction. The unsuccessful broad replacement was a verification-method error, not evidence of an additional fixture change.

## Self-Audit

**(a) Reliance list: structural PASS items skipped**

- None. No inherited structural verdict was supplied. Other reviewers’ PASS assertions were not treated as independent verification.

**(b) Independent semantic checks**

- **Negative control:** Parsed the nine original compliant notifications in `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/45eb8186-bca4-4fef-a7c8-1212ca1b7500.jsonl`. Compared them with the shared ledger to confirm that later failures must not be back-attributed.
- **Unreviewed endpoint:** Inspected original planning-session records 858, 885, 889, and 946 in `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl`. The final result expressly discloses the absence of another review.
- **Retained defect versus failed repair:** Inspected original records 383, 450, 521, 668, and 824 in `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl`. These establish the repair restriction, successful partial repair, authorization, subsequent pass, and separate archive blocker.
- **Re-frozen evidence:** Compared preserved and current fixture bytes. Exactly one physical line changed, correcting the default-path property. This supports B’s bounded correction claim without claiming an unavailable historical full-oracle comparison.
- **Protocol limits:** Read actual current sources rather than inferring behavior from E’s summary. The sources distinguish protocol obligations from executable checks and explicitly leave concurrent non-cooperating writers unsupported.

At least 22 boundary facts were independently checked: nine compliant notifications, seven synthetic exclusions, one setup-only exclusion, and five central authorization/outcome distinctions. No new runtime execution was performed.

**Why a clean result is justified:** The targets retain concrete counterexamples to universal failure claims, successful repairs, unresolved endpoints, authorization limits, and unavailable history. Primary evidence supported those boundaries. No broader generalization requiring an omitted control was found.

## Recommendations

The parent should persist this exact report into the prepared output stub at:

`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-content-phase2-controls-limitations-a-report.md`

Then verify persistence and merge this partition with the remaining independent reports. No corrective target edit is required by this review.

## QA Complete

| Status | Result |
|---|---|
| DONE | Completed the assigned controls-and-limitations review. PASS, zero findings. |
| NEXT | Parent persists and verifies this text, then combines the partition verdicts. |