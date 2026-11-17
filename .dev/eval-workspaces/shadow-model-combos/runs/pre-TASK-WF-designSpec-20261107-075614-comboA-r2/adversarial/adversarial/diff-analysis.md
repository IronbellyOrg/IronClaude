# Diff Analysis: reflect reviewer cards (comboA-r2)

- Generated: 2026-11-13T05:0X:00Z (Wave 4 judge adjudication prep)
- Variants compared: 3 (V1 analyzer/sonnet 4 findings; V2 qa/haiku 2 findings; V3 refactorer/opus 7 findings)
- Total differences found: 12 content points, 0 cross-variant contradictions
- Categories: structural 1, content 12, contradictions 0, unique 7, shared assumptions 1

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card shape | 4 findings, decision-table lens | 2 findings, coverage-evidence lens | 7 findings, process/convention lens, 25 citations | Low (style only; feeds base selection) |

## Content Differences (each = one candidate defect; judge verdicts in debate-transcript.md)

| # | Topic | Raised by | Overlap |
|---|---|---|---|
| C-001 | Fold type unpinned (dict prose vs attribute access; Task 5 AC subscripts) | V1 F1 | unique |
| C-002 | resume_decision row 4 re-entry lacks inputs and expected outcome | V1 F2 | unique |
| C-003 | user_override settle sets no disabled_cause; guard_status DISABLED branches unreachable | V1 F3 | unique (r1 cross-run: same defect) |
| C-004 | draft_guard_unavailable halt reports released (fold None); override unplanned | V3 F1 | unique (r1 cross-run: same defect) |
| C-005 | Byte-identical pins compare start-text only | V3 F2 | unique (r1 cross-run: MF7) |
| C-006 | ready not_applied -> RELEASE_PENDING-after-failed-release untested | V3 F3 | unique (r1 cross-run: MF12) |
| C-007 | Tasks 9/10/12/13 consume pre-build-gate.md without Depends on: Task 1 | V2 F2 + V3 F4 | SHARED (two reviewers, same defect) |
| C-008 | Task 9 classification-entry allowance contradicts its own AC exclusion list | V3 F5 | unique |
| C-009 | Gate list G4/G5 (plan L26, Task 12) vs G1live/G2live/G4/G5/G6 (plan L24, spec:326) | V3 F6 | unique |
| C-010 | no file:NNN rule stated but no AC tests it | V3 F7 | unique |
| C-011 | Resume-at-ordinal<3 reconcile (spec:58) vs row-2 REPORT_HELD precedence (spec:164) | V1 F4 | unique |
| C-012 | Inferred matrix omits 3 deliverable spans (covered by Tasks 2/10/5) | V2 F1 | unique (evidence defect, not plan defect) |

## Contradictions

None. No two reviewers assert incompatible positions; the two overlapping findings (C-007) agree in substance and scope (V3 adds Task 13).

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | C-001/C-002/C-003: the three pure-contract defects (type, re-entry, cause) | High |
| U-002 | V3 | C-004: halt-vs-released reporting defect | High |
| U-003 | V3 | C-008/C-009: two internal-consistency defects no other run caught | Medium |
| U-004 | V2 | C-012: honest coverage-evidence limitation of the Pass-2 matrix | Medium |
| U-005 | V1 | C-011: letter-level resume precedence tension | Low |
| U-006 | V3 | C-005/C-006/C-010: untested-rule and untested-fold-variant gaps | Medium |
| U-007 | V2 | C-007 co-discovery (with V3) confirms the dependency gap | Low |

## Shared Assumptions

| # | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | The plan's ACs are the only execution gate (a rule without an AC is unenforced but the rule itself still binds the implementer) | All three cards treat a missing AC as the defect, not missing prose | STATED (cards cite AC gaps explicitly) | No |

## Summary

- 1 structural, 12 content, 0 contradictions, 7 unique, 1 shared assumption (STATED, not promoted)
- Highest-severity items: C-001, C-002, C-003, C-004 (MAJOR candidates)
- Similarity check: differences > 10% of comparable items; debate proceeds.
