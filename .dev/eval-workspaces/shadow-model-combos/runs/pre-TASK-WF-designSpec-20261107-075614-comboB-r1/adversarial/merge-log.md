# Merge Log

Date: 2026-11-13. Base: variant-3-original.md. Plan: refactor-plan.md (changes 1-9). Output: merged-findings.md.

| Plan # | Change | Result in merged-findings.md | Source | Status |
|---|---|---|---|---|
| 1 | V3 F1 severity MAJOR to MEDIUM; merge V1 F1 | M1 MEDIUM; sources V3 F1, V1 F1; added the unreadable-path bound at spec:117 | V1 F1, V3 F1 | Applied |
| 2 | V3 F2 MAJOR to MEDIUM; reframe as spec defect copied by plan; add unspecified resume `target_sha`; mark HEAD REBIND HEAD-only | M2 MEDIUM, reframed; resume `target_sha` gap and HEAD-only note added | V3 F2, INV-006 | Applied |
| 3 | New finding: zero-edit release can release a guard holding an earlier cycle's unpublished fix | M3 MEDIUM, probe-only, cites spec:155-156, :69, plan:75, :166 | INV-001 | Applied |
| 4 | New finding: engage row 8 before row 10 | M11 LOW, cites spec:140, :142, plan:70, :73-74 | INV-002 | Applied |
| 5 | Merge V1 F2 into V3 F3 | M4 LOW, sources V3 F3, V1 F2 | V1 F2, V3 F3 | Applied |
| 6 | New finding: Tasks 9, 10, 12, 13 omit Task 1 edges; withdraw "all complete" | M7 LOW; withdrawal listed under Refuted or dropped | V2 F1 | Applied |
| 7 | New finding: Task 13 gives flags.md only a row | M8 LOW | V2 F2 | Applied |
| 8 | Keep V3 F4, F5, F6, F7 at MINOR (LOW) | M5, M9, M10, M6 at LOW | V3 | Applied |
| 9 | Drop V2 F3 | Listed under Refuted or dropped | Round 2 | Applied |

## Notes
- Id order follows the requested list: M5 is V3 F4, M6 is V3 F7, M9 is V3 F5, M10 is V3 F6.
- "Changes NOT Being Made" in the plan were honored (V3 "all complete" claim, V1/V2 MINOR for the adapter, INV-003..005).
- Not re-read: spec:299 (cited by V1/V3 for M4); kept as given in the variant blocks.
- Severity values in the table use LOW where the variants said MINOR, per the final findings list.
- No escalations; no plan item was skipped.
