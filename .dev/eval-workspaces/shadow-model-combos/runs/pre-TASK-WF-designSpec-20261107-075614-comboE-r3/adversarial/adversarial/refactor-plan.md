# Refactoring Plan (Step 4)

## Overview
- Base: Variant 1 (reviewer-1 analyzer card). Incorporated: Variant 2 F1, F2, F3; Variant 3 F2; probe items INV-001, INV-002, INV-003, INV-005, INV-007.
- Planned changes: 8. Rejected changes: 5. Overall risk: Low (the output is a verdict list; no code is touched).
- Review status: auto-approved (non-interactive run).

## Planned Changes
| # | Change | Source | Target | Approach | Rationale (debate evidence) | Risk |
|---|--------|--------|--------|----------|----------------------------|------|
| 1 | Re-rate all of V1's blocking MAJOR findings to non-blocking | Round 2 A1, A2, A3 | V1 F1-F5, F7, F13 | modify | A1 withdrew every blocking flag under the concrete-wrong-outcome rule | Low |
| 2 | Merge V1 F2 and F13 into M-001 | A1 Round 2 | M-001 | merge | same hole filed twice | Low |
| 3 | Merge V1 F1, V3 F1, V1 F9, INV-003 into M-003 at MINOR | A1, A3 | M-003 | merge | plan:124 states reuse; AC at plan:127 is the gap | Low |
| 4 | Append V2 F1 (with INV-005), F2, F3 with corrected locators | A2 Round 2 | M-005, M-010, M-011 | append | locators corrected to plan 166-169, 111, 128 | Low |
| 5 | Append V3 F2 | A3 | M-012 | append | plan:108 vs plan:113 | Low |
| 6 | Add INV-002 as M-002 at MAJOR non-blocking | Round 2.5 resolution (3 of 3 MEDIUM) | M-002 | insert | HOLD at engage undefined | Low |
| 7 | Add INV-001 and INV-007 as M-006 and M-013 | Round 2.5 resolution | M-006, M-013 | insert | source.md:206 vs :112; plan:137 vs :140 | Low |
| 8 | Collapse V1 F8, F10, F14 into M-014 | A1 | M-014 | merge | small spec gaps | Low |

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|---|---|---|
| V1 F11 (pre-push OPEN check) | keep as MINOR | dropped 2 to 1: plan:124 and plan:150 state the check |
| V1 F12 (L2 line condition) | keep | dropped by A1 itself: plan:137 and plan:141 put the literal line in the output table |
| INV-004 | add as MEDIUM | deliberate spec design (source.md:107; plan:75) |
| INV-006 | add as LOW | dropped 2 to 1: "highest" reads as numeric |
| INV-008 | add as HIGH | meta-claim; falsifiers restate other items; no HIGH survives |

## Risk Summary
All changes are re-ratings, merges or appends of verified findings; rollback is re-reading the three variant files.

## Review Status
auto-approved
