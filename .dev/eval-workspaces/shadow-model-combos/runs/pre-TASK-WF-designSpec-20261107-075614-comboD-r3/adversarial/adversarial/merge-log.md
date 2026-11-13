# Merge Log

## Metadata

- Base: Variant 2 (reviewer-2 card, qa lens), variant-2-original.md
- Executor: merge-executor (model claude-gw-tier1b)
- Plan: refactor-plan.md (17 planned changes, 5 rejected alternatives)
- Changes applied: 17 of 17
- Status: COMPLETE
- Timestamp: see the Merge date comment in merged-output.md (UTC, generated at merge time)
- Method: the findings block was produced by concatenating the pre-verified jsonl file (`artifacts/merged-findings.checked.jsonl`) into the fence, so no claim, id or citation was retyped.

## Changes Applied

| # | Change | Result id | Status |
|---|---|---|---|
| 1 | Merge base F1 with V1 F1 at MINOR, blocking false | M-01 | applied |
| 2 | Merge V3 F1 and base F4 at MINOR | M-02 | applied |
| 3 | Add V1 F2 strengthened with spec 240 | M-03 | applied |
| 4 | Keep base F3, corrected citation (spec 333) | M-04 | applied |
| 5 | Keep base F7 | M-05 | applied |
| 6 | Add release-failure path | M-06 | applied |
| 7 | Keep base F10, corrected lines (spec 234, 232) | M-07 | applied |
| 8 | Keep base F12 | M-08 | applied |
| 9 | Add engage-failure message | M-09 | applied |
| 10 | Keep base F11, advisory | M-10 | applied |
| 11 | Keep base F8, marginal | M-11 | applied |
| 12 | Add Wave 0 second trigger, printed once | M-12 | applied |
| 13 | Add Task 12 and Task 13 dependency lines | M-13 | applied |
| 14 | Add constraint with no criterion | M-14 | applied |
| 15 | Add per-cycle applied_edits source, MAJOR, blocking false | M-15 | applied |
| 16 | Add fold cycle_id update rule, MAJOR, blocking false | M-16 | applied |
| 17 | Add resume row 4 inputs | M-17 | applied |

## Post-Merge Validation

- Findings block byte identity: the 17 lines inside the `findings-v2` fence of merged-output.md were extracted and compared with `artifacts/merged-findings.checked.jsonl`. Line count 17; `diff` output empty (DIFF_EMPTY).
- JSON parse: all 17 lines parsed with `json.loads` (PARSED 17).
- Structural integrity: PASS. Headings in order: title (H1), Merged verdict, Merged findings (with H3 Findings block), Dissent and resolution, Invariant probe carry-over, Provenance table. Provenance header comments present before the title.
- Internal references: PASS. Every M id mentioned (M-01 to M-17) resolves to a finding in the block; INF ids appear only inside the unchanged findings lines as refs. INV-001 to INV-007 match invariant-probe.md.
- Contradiction re-scan: new contradictions introduced: 0. Severity counts in the verdict (0 blocking, 2 MAJOR, 15 MINOR) match the jsonl (M-15 and M-16 MAJOR, all blocking false).
- Note: the plan carries INV-003 into no finding; the card lists it as UNADDRESSED LOW with that remark, adding no new finding.

## Summary

- Planned changes: 17
- Applied: 17
- Failed: 0
- Skipped: 0
