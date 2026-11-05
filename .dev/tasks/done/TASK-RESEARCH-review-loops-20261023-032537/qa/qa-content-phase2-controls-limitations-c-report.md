# QA Report: Controls and Limitations (Partition c of 3)

**Topic:** Phase 2 research on repeated review failures  
**Date:** 2026-10-23  
**Phase:** phase-gate  
**Lens:** controls-limitations  
**Fix cycle:** N/A  
**Fix authorization:** false

## Overall Verdict: PASS

**VERDICT: PASS**  
**Issue count: 0**

This partition preserves successful repairs, negative controls, sampling limits, changing source contents, unknown earlier-miss causes and policy-change confounding. It does not treat accepted defects as repaired defects.

## Checked Scope

Read all four assigned targets in full:

- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/05-session-e002bed2.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/06-session-0690ee9f.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-03.md`
- `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md`

Read the actual acceptance paragraphs for Steps 2.3, 2.11, 2.12 and 2.13, the review dispatch, governing report template and assigned report stub.

[PARTITION NOTE: Cross-file checks cover the assigned targets and supporting evidence needed for this lens. This verdict does not replace the other partitions or other review lenses.]

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Successful one-repair cases remain visible | PASS | Independently extracted monitor records 267/319 and 496/540. They show unsuccessful reviews followed by compliant rechecks. The monitor case retains both controls and notes the helper’s later-discovered integration defect. |
| 2 | Credential control remains separate from repeated failure | PASS | Credential parent records 390, 411 and 435 establish issues, restored durable lint proof and pass/archive for the initial package. The case, screening summary and deck keep this separate from the follow-up package’s repeated final failures. |
| 3 | Other screening controls are not converted into repeated failures | PASS | Original nested reviewer conclusions confirm session 17’s Task 8 unsuccessful/compliant pair and FINAL issues/pass pair. Original session 13 record 435 explicitly says no semantic re-review followed its corrections. Session 14 record 371 retains the earlier report as historical. The screening summary and deck preserve these boundaries. |
| 4 | Modification-time selection and source-family clustering limit generalization | PASS | Read the frozen manifest’s selection rule and membership paths. The deck explicitly identifies modification-time selection, synthetic exclusions and clustering in few work families. Its conclusions reject fleet-wide rates and controlled model/protocol comparisons. |
| 5 | Membership freeze is not represented as immutable source contents | PASS | The manifest fixes membership without per-file content snapshots. The monitor supplement distinguishes its original prefix from a later observation and labels its prefix hash retrospective. Independent extraction found further live growth, which was not back-attributed into the declared historical windows. |
| 6 | Unknown earlier-miss causes remain unknown | PASS | Both dedicated cases explicitly separate implementation mechanisms from reviewer cognition. The deck preserves unknown causes rather than asserting context exhaustion, model weakness or inattention. |
| 7 | Policy change remains a confounder | PASS | Independently read historical tool-result record 18 from consecutive credential FINAL reviewers. After removing reader-added line numbers, both original contents match the preserved historical-rule capture. The old and revised evidence rules differ. The case and deck correctly decline to isolate policy effects from evidence corrections or identify an unknown updater. |
| 8 | Acceptance closure is not mislabeled repair | PASS | Monitor records 1250/1261 show human acceptance followed by completion with unchanged `misunderstood`. The live ledger independently retains the ruling and noncompliant completion. The case and deck do not invent an eighth review or repaired outcome. Credential acceptance likewise remains an unmet literal lint criterion, not universal compliance. |
| 9 | Missing history and verification boundaries constrain conclusions | PASS | Targets acknowledge unavailable historical proof, incomplete ledgers, local rather than production reproductions, fixture-dependent size thresholds and current-instruction versus historical-execution differences. Missing archived paths encountered during this review were checked through surviving original transcript outputs rather than reconstructed files. |

## Summary

- Checks passed: **9 / 9**
- Checks failed: **0**
- Critical issues: **0**
- Important issues: **0**
- Minor issues: **0**
- Issues fixed in-place: **0**
- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 21 | Grep: 0 | Glob: 0 | Bash: 5

Read engagement includes 17 content returns, three missing-path results and one unchanged-file response. Missing-path checks were not counted as successful verification. Relevant historical facts were recovered from original transcript evidence.

Confidence measures completion of this focused checklist, not certainty about unavailable historical events or coverage outside this partition.

## Issues Found

None within the assigned controls-and-limitations lens.

## Actions Taken

- Read all assigned targets without modifying them.
- Used bounded, read-only transcript extraction through UV.
- Checked original review outcomes, acceptance events and historical policy contents.
- Did not run investigated plans, tests, production workflows, Git operations, external lookups or additional agents.
- Did not write a report file. This final text is the report for parent persistence.

## Self-Audit

**(a) Reliance list:**

- No inherited structural PASS table was supplied. No structural verdict was substituted for independent semantic verification.
- Screening captures were used for navigation and historical context, not as substitutes for the original reviewer conclusions checked above.

**(b) Independent semantic checks:**

- Independently checked **24 discrete event/content claims**: four monitor control outcomes, four monitor compliance/migration/acceptance events, six credential evidence/closure events, two historical policy contents, four session-17 reviewer outcomes, two planning endpoints and two population-selection facts.
- Original monitor evidence came from `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl`.
- Original credential evidence came from `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl` and its cited nested reviewer transcripts.
- Checked that the summaries retain the decision-changing qualifications: successful review does not prove exhaustive correctness; acceptance does not prove repair; changed evidence and changed policy cannot be experimentally separated; later discovery does not establish introduction.
- Zero findings resulted because these qualifications survive into the assigned summaries and deck conclusions, not merely because a limitations section exists.

### Verification limitations and recovery

Three attempted direct reads were unavailable:

- The credential follow-up archived `progress.md`.
- The initial credential package’s archived `artifacts/t3-markdownlint.log`.
- The credential follow-up’s archived `artifacts/t6-owner-acceptance.md`.

Surviving original parent tool outputs and nested reviewer records independently support the relevant historical control, lint-proof and acceptance conclusions. This review does not certify those archived files’ present availability.

An initial monitor extraction exceeded the inline output limit. A narrower extraction subsequently returned the required control and closure evidence directly. An initial raw policy-content comparison differed because original reader output included line-number prefixes; comparison after removing those prefixes matched both captured contents.

No web research was needed or performed.

## Recommendations

Merge this zero-finding report with the other Phase 2 reviews. No target correction is required by this lens. This partition PASS does not establish that the complete Phase 2 gate has passed.

| Status | Result |
|---|---|
| DONE | Reviewed all four assigned targets and independently checked their controls and limitations. |
| NEXT | Parent persists this report and includes it in the full Phase 2 review merge. |

## QA Complete