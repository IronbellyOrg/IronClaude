# Merge Log

Base: V3 (reviewer 3 card). Merge method: adversarial. Plan executed: adversarial/refactor-plan.md (20 changes, one per merged id). Output: adversarial/merged-review-card.md.

## Applied changes

| MF id | Severity | Source ids | Source variant | Action | Notes |
|---|---|---|---|---|---|
| MF-01 | blocking | R1-01 + R3-03 | V3 base + V1 | merged | V1 blocking label and impact sub-claim dropped; V1 flag-table, G-O, step 10, write-scope edits added to V3's R3-03 |
| MF-02 | blocking | R1-13 | V1 | added-from-V1 | skill STOP row wording per V3 Round 2 |
| MF-03 | blocking | R3-02 + R1-02 + R3-09 + INV-3 | V3 base + V1 + probe | merged | R3-09 and INV-3 (init-lite.md:94) folded in |
| MF-04 | blocking | R3-01 + R1-05 | V3 base + V1 | merged | both fix options kept |
| MF-05 | blocking | R3-04 + R1-03 | V3 base + V1 | merged | V3 data-field fix used; V1's two explicit tests recorded as the workflow case |
| MF-06 | blocking | INV-1 | probe | added-from-probe | |
| MF-07 | blocking | INV-2 | probe | added-from-probe | |
| MF-08 | blocking | INV-5 | probe | added-from-probe | probe MEDIUM; blocking per refactor plan |
| MF-09 | minor | INV-4 + INV-6 | probe | added-from-probe | probe MEDIUM; applied with MF-06 |
| MF-10 | minor | R3-10 + R1-04 | V3 base + V1 | merged | |
| MF-11 | minor | R3-08 + R2-03 | V3 base + V2 | merged | stays minor |
| MF-12 | minor | R3-06 + R2-04 | V3 base + V2 | merged | count corrected to six; V2 fix not used |
| MF-13 | minor | R1-07 + R2-05 | V1 + V2 | merged | also listed under Open owner questions |
| MF-14 | minor | R3-05 + R1-12 | V3 base + V1 | merged | |
| MF-15 | minor | R1-10 | V1 | added-from-V1 | |
| MF-16 | minor | R3-07 | V3 base | kept-from-base | |
| MF-17 | minor | R2-06 | V2 | added-from-V2 | |
| MF-18 | minor | R2-07 | V2 | added-from-V2 | |
| MF-19 | minor | R2-01 + calibrator | V2 | added-from-V2 | R2-01 "no fix needed" rejected; trailing-space correction from debate Round 2 |
| MF-20 | minor | R1-11 | V1 | note-only | outside this plan's files |

## Rejected or not merged (recorded, no card block)

R1-06 (owner question D-P1-4), R1-09, R1-01 impact sub-claim, R2-01 "no fix needed", R3-06 "seven" count, R3-08 as should-fix, "bad flags blocked" wording. Open owner questions D-P1-1 and D-P1-4 are in the card.

## Provenance counts

Counted from the table: kept-from-base 1 (MF-16); merged 9 (MF-01, 03, 04, 05, 10, 11, 12, 13, 14); added-from-V1 2 (MF-02, 15); added-from-V2 3 (MF-17, 18, 19); added-from-probe 4 (MF-06, 07, 08, 09); note-only 1 (MF-20). Total 20.

## Post-merge validation

Every finding MF-01..MF-20 has an id, severity, evidence, and plan edit (MF-20 plan edit is "none, note only" by the refactor plan); no duplicate ids; severities unchanged from the refactor plan; counts match the header (blocking 8: MF-01..MF-08; minor 12: MF-09..MF-20; total 20). Evidence citations are copied from the reviewer cards, the debate transcript (including the probe table) or the plan lines those sources cite; none were added by the merge. Two plan-line cites not in a card (Task numbers for MF-08 and the Task 11 location of `/sc:test`) come from the plan's own task headings.
