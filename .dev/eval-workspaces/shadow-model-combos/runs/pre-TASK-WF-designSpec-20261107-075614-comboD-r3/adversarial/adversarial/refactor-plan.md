# Refactoring Plan

## Overview
- Base variant: variant-2 (reviewer-2 card, qa lens)
- Incorporated variants: variant-1 (F1, F2), variant-3 (F1, F2); Round 2 new evidence; invariant probe INV-001, INV-002, INV-004, INV-006
- Change count: 17 planned changes, 5 rejected alternatives
- Overall risk: Low (the merged artifact is a findings list; no code is touched)
- The final merged findings list is the file `artifacts/merged-findings.checked.jsonl` (17 lines, every quote verified verbatim inside its cited line range by `artifacts/check-merged.py`). The executor copies it unchanged into the findings block of the merged output; it does not rewrite claims or citations.

## Planned Changes

| # | Change | Source | Target in base | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|
| 1 | Merge base F1 (MAJOR, blocking) with V1 F1 into M-01 at MINOR, blocking false | V1 F1, V2 F1 | base F1 | All three advocates settle MINOR in Rounds 1 and 2: plan 137 narrows the test to gate wording (X-001) | Low |
| 2 | Merge V3 F1 and base F4 into M-02 at MINOR | V3 F1, V2 F4 | base F4 | Task 1 criterion (plan 37) forces one place; the real gap is Task 10 not checking it and no cycle_id equality check (C-002) | Low |
| 3 | Add M-03 from V1 F2, strengthened with spec 240 | V1 F2 | new | Spec 240 says sections 3 and 4.1 to 4.4; Task 8 omits 4.2 and 4.4 (C-003, accepted by all three) | Low |
| 4 | Keep base F3 as M-04 with corrected citation (spec 333) | V2 F3 | base F3 | C-004 TRUE; citation fixed | Low |
| 5 | Keep base F7 as M-05 | V2 F7 | base F7 | C-004 TRUE, conceded by V1 and V3 | Low |
| 6 | Add M-06 (release-failure path) | Round 2 N2 and V2 new evidence | new | Verified TRUE by two advocates | Low |
| 7 | Keep base F10 as M-07 with corrected lines (spec 234, 232) | V2 F10 | base F10 | C-004 TRUE; citations fixed | Low |
| 8 | Keep base F12 as M-08 | V2 F12 | base F12 | C-004 TRUE | Low |
| 9 | Add M-09 (engage-failure message) | Round 2 N3 | new | Verified TRUE by two advocates | Low |
| 10 | Keep base F11 as M-10, advisory | V2 F11 | base F11 | C-008: all three call it MINOR out of build scope | Low |
| 11 | Keep base F8 as M-11, marginal | V2 F8 | base F8 | C-007 marginal true | Low |
| 12 | Add M-12 (Wave 0 second trigger, printed once) | INV-004, V2 new evidence | new | LOW probe item plus advocate 2 new evidence | Low |
| 13 | Add M-13 (Task 12 and Task 13 dependency lines) | V3 F2, Round 2 N1 | new | C-009 and X-003 MINOR hygiene, final in Round 2 | Low |
| 14 | Add M-14 (constraint with no criterion; no python fence in the ref) | Round 2 V3 new evidence | new | Verified by advocate 3 | Low |
| 15 | Add M-15 (per-cycle applied_edits source) at MAJOR, blocking false | INV-001 | new | MEDIUM probe item, UNADDRESSED, not HIGH so it does not block convergence | Medium |
| 16 | Add M-16 (fold cycle_id update rule) at MAJOR, blocking false | INV-002 | new | MEDIUM probe item, UNADDRESSED | Medium |
| 17 | Add M-17 (resume row 4 inputs) | INV-006 | new | LOW probe item | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| C-005 / base F2 | Keep "Task 11 criteria check only names" | Mostly false: plan 170-172 assert event order, real recovery windows and forbidden calls (all three advocates) |
| C-006 / base F5 | Keep "Task 12 and 13 grep checks pass without the section" | Weak and cited at a wrong line; Task 12 line 182 adds tests and Task 13 content is read; no spec line demands more |
| base F6 | Keep "RunConfig unchanged has no criterion" | Trivial; dropped as out of the debate's agreed set |
| base F9 | Keep "bullets load only at L3 with draft not asserted" | Withdrawn by its own advocate: plan 150 gates each bullet test on L3 and draft |
| V1 note | "No spec row of Tasks 3 and 4 lacks a criterion" | False (M-04, M-05) |

## Risk Summary
All changes are additive edits to a findings list with verified quotes; rollback is to use `variant-2-original.md` as is.

## Review Status
Auto-approved (non-interactive).
