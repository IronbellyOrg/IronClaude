# Merge Log

Base: Variant 1. Plan: refactor-plan.md (6 planned changes, 3 rejected). Output: ../merged-output.md. Date: 2026-11-13.

## Changes applied
| # | Plan change | Result | Source |
|---|---|---|---|
| 1 | Replace per-finding blocking flags with Round 2 rulings (all non-blocking) | Applied: all 14 findings Blocking: no | refactor-plan.md |
| 2 | Add V2 findings as M-004, M-009, M-010, M-011, M-012 | Applied | V2 F1-F11 |
| 3 | Add V3 F1 as M-013 | Applied | V3 F1 |
| 4 | Add INV-001 as M-005 and INV-002..004 as advisory M-014 | Applied | invariant-probe.md |
| 5 | Merge V1 F1 and V2 F4 into M-001 | Applied | V1 F1, V2 F4 |
| 6 | Restate V1 F5 as M-006 with the Round 2 note | Applied | V1 F5 |

V1-only findings kept as M-002, M-003, M-007, M-008 (F6 and F7 combined in M-008), per the plan table.

## Changes not made (per plan)
V2 F1 blocking, V1 F5 blocking, V2 F4/V1 F4 blocking vote. All recorded in the output section "Changes not made".

## Validation
- Required sections present: header comments, title, Verdict, Merged findings, Unresolved, Changes not made. PASS
- 14 finding subsections M-001..M-014, in order. PASS
- Severity counts 6 MAJOR and 8 MINOR; Blocking: no on all 14. PASS
- Citation strings for all 14 findings diffed against the plan table: identical. PASS
- Provenance tags: 17 (one per section and per finding). PASS
- Heading levels: one H1, four H2, fourteen H3, no skips. PASS
- Contradiction re-scan: verdict counts, finding flags and the Unresolved section agree. PASS
- No findings or citations invented. The only additions are the citation key (full SPEC and PLAN paths from the plan table) and the INV-001 line-155 note from invariant-probe.md. PASS

Overall: PASS
