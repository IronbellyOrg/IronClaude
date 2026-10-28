# QA Report - Numbers and Metrics (Partition a of 3)

**Topic:** Phase 2 research outputs, partition a  
**Date:** 2026-10-23  
**Phase:** phase-gate  
**Lens:** numbers-metrics (content)  
**Fix cycle:** Initial review  
**Fix authorization:** false  
**Delivery:** Text-only report. No report file or target was written.

## Overall Verdict: PASS

VERDICT: PASS

The assigned outputs preserve the relevant counting boundaries and correctly qualify the historical closure-count discrepancy. No numbers-and-metrics defect was found.

## Checked Scope

Read all five assigned targets in full:

1. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md`
2. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/02-session-a9b88895.md`
3. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-04.md`
4. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-05.md`
5. `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/scope-rules.md`

Also read the assigned acceptance paragraphs for Steps 2.4-2.8, the dispatch, governing lens checklist, standard report template, and prepared report stub.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Population arithmetic and denominators | PASS | The two screening slices each retain six manifest slots. Indexes 19-24 contain one selected planning session, one operational control, and four synthetic exclusions. Indexes 25-30 contain one selected implementation session, one unrelated operational session, one setup-only session, and three synthetic exclusions. Direct extraction from all 12 original logs confirmed their captured byte counts, physical record counts, hashes, and tool-call boundaries. Neither slice turns these dispositions into a prevalence estimate. |
| 2 | Summary counts and repair accounting | PASS | Independently counted 16 first-round planning findings and 20 numbered second-round items. The detailed next-review checklist contains 14 fixed and two partial entries. The case explicitly corrects the historical report's 13-fixed/three-partial statement rather than endorsing it. The oracle artifacts independently support four initial findings, three repaired findings, and one retained finding. |
| 3 | Numeric ranges, chronology, and revision counts | PASS | Original planning records yield 13 agent dispatches in each full review and 15 final targeted Edit calls. Historical reconstruction excludes the blocked cleanup attempt, reproduces the reported reviewed/revised hashes, and matches the live final plan. The final plan has seven phase headings and 15 task headings. Computed review intervals are 2,254.701 seconds, 2,190.241 seconds, and 84.813 seconds, consistent with the rounded durations reported. |
| 4 | Statistical claims and unsupported inference | PASS | Read every assigned section for percentage, probability, growth, cost, and prevalence claims. No unsupported population inference is made. The planning report distinguishes numbered items from independent defects and identifies both a duplicate sufficiency item and an explicit non-defect note. Mixed causal classifications are not presented as exclusive percentage buckets. |
| 5 | Test, review, and outcome metrics | PASS | Preserved execution logs support oracle totals of 67/78 before review, 74/85 after permitted repair, and 74/85 after authorized correction. The integration log records 255 default and 85 acceptance tests. Reviewer dispatches and artifacts support two failed oracle reviews followed by one passing authorized-correction review. Repeated notifications, local test failures, carry-over history, and the later archive refusal are not added to that review denominator. |
| 6 | Effort, control, and protocol-cap consistency | PASS | Reported durations are explicitly wall-clock intervals, not summed agent runtime or token costs. Nine original compliant control notifications are supported by nine reviewer dispatches in session 19. All seven source/installed protocol pairs match, with source line totals 72, 41, 175, 90, 451, 242, and 85. The retry source supports five planned reviews, while explicitly permitting additional reviewer spawns and operator-resume reviews; the rule map does not misrepresent this as a lifetime cap. |

## Summary

- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 40 | Grep: 0 | Glob: 0 | Bash: 5
- Three Read attempts returned unchanged-file notices; their earlier content responses supplied the evidence. These notices were not counted as additional verification.
- External research: None required or performed.
- Unchecked items: None.
- Unverifiable checklist items: None.

## Issues Found

None within the assigned lens and partition.

The historical 13-fixed/three-partial discrepancy is not a new defect in the finished research: the dedicated planning case expressly resolves it to 14 fixed/two partial, while the screening file accurately labels the earlier narrative as disputed.

## Actions Taken

- Recomputed metadata for the exact original logs at frozen manifest indexes 19-30 without rescanning population membership.
- Extracted bounded event metadata and relevant excerpts from the two selected case logs.
- Reconstructed the historical planning amendments in memory and compared the final result with the live plan.
- Read the original review reports, the bounded detailed closure checklist, the targeted verdict, the oracle review artifacts, and preserved execution summaries.
- Compared the original and authorized held-back fixture. Exactly one parsed field differs, and applying that field change reproduces the current serialized fixture.
- Compared all seven current source/installed protocol pairs.
- Made no writes, ran no investigated tests, launched no agents, and performed no Git operations.

### Negative Verification Results and Recovery

- An initial task-heading expression expected third-level headings and returned zero. Reading the plan showed second-level task headings; the corrected inspection enumerated Tasks 1-15.
- The guessed initial acceptance-log basename was absent. The preserved correction record identified the actual original log, which records 78 passing tests.
- An initial fixture comparison accidentally requested zero replacements and returned false. Structural comparison identified the sole changed field; changing that field and serializing reproduced the current bytes.

These were inspection errors resolved against primary evidence, not target defects.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied. This review independently checked its assigned numeric claims.

**(b) Independent semantic checks:**
- **Closure accounting:** Read `/config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/reflect/pre-designSpec-v2-20261022150856/adversarial/merged-verdict.yaml`, bounded to its original-finding closure checklist. Independently counted 14 fixed and two partial entries and checked the finished case's correction.
- **Review denominator:** Inspected actual dispatches and original result records in both selected JSONL logs. Distinguished two full planning runs plus one targeted review from the oracle task's two failed reviews plus one passing review.
- **Test-count meaning:** Checked preserved logs, not just reviewer summaries. Unchanged 74/85 totals after authorization are compatible with a strengthened existing assertion and do not imply an unchanged fixture.
- **Control boundary:** Verified the nine compliant notifications in session 19 against its nine reviewer dispatches, rather than assigning later shared-ledger events to that session.

**Claim verification:** Independently checked at least 36 primary-log metadata assertions: byte count, physical record count, and hash for each of 12 logs. Also checked seven protocol line totals and seven source/installed equalities, plus the case counts, timing intervals, review outcomes, and test totals documented above.

**Why the clean result is credible:** The review directly challenged the likely inflation points: closure arithmetic, duplicate findings, repeated notifications, blocked edits, synthetic sessions, later ledger history, passing-test totals, and retry caps. The finished targets already distinguish or correct these cases.

**Limits:** This verdict covers numbers and metrics in the five assigned outputs only. It does not certify other partitions, re-adjudicate every substantive finding, establish model effectiveness, or infer historical loaded protocol bytes from current files.

## Recommendations

Accept this partition's numbers-and-metrics review and merge it with the remaining independent partition reports. No correction is required from this lens.

## QA Complete

| Status | Result |
|---|---|
| DONE | Completed the assigned read-only review. PASS, zero issues. |
| NEXT | Parent persists this exact report at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-content-phase2-numbers-metrics-a-report.md` and verifies the saved artifact before counting delivery complete. |