# Diff Analysis: reviewer-card Comparison (UC-1 pre, plan vs design spec)
## Metadata
- Generated: 2026-11-13 (orchestrator-written inline; no separate analytical agent)
- Variants compared: 3 (variant-1 analyzer/sonnet class, variant-2 qa/haiku class, variant-3 refactorer/opus class)
- Total differences found: 4 structural, 12 content, 3 contradictions, 3 unique groups, 3 shared assumptions
- Findings per variant: V1 = 9 (5 MAJOR blocking, 4 MINOR), V2 = 4 (all MINOR), V3 = 2 (1 MAJOR blocking, 1 MINOR)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Finding count | 9 | 4 | 2 | Low |
| S-002 | Severity profile | 5 blocking MAJOR | 0 blocking | 1 blocking MAJOR | High |
| S-003 | Citation shape | file lines, short quotes | file lines (after one re-ask) | file lines, no quotes | Low |
| S-004 | Row coverage | INF-001..024 | all 48 | INF-025..048 | Low |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Cycle-id continuity (spec 4.6 vs Task 8/10 ACs) | F1 MAJOR blocking | not raised | not raised | High |
| C-002 | fsync-before-call ordering has no AC | F2 MAJOR blocking | not raised | not raised | Medium |
| C-003 | GuardRead mapping from --read JSON has no owner | F3 MAJOR blocking | not raised | not raised | Medium |
| C-004 | Request key builder / `a<k>` suffix has no owner | F4 MAJOR blocking | not raised | not raised | Medium |
| C-005 | resume_decision row 4 lacks release inputs | F5 MAJOR blocking | not raised | not raised | Medium |
| C-006 | next_cycle_number AC cannot tell count from highest | F6 MINOR | not raised | not raised | Low |
| C-007 | autoMergeRequest type not pinned by Task 7 AC | F7 MINOR | not raised | not raised | Low |
| C-008 | engage_decision rows read guard.phase when guard is None | F8 MINOR | not raised | not raised | Low |
| C-009 | "printed once" off line is only checked for presence | F9 MINOR | not raised | not raised | Low |
| C-010 | Task 11 ACs check test names, not behaviors | not raised | F1 MINOR | not raised | Medium |
| C-011 | "no file:NNN pointers" constraint has no AC | not raised | F2 MINOR | not raised | Low |
| C-012 | _RESOLUTION_SCRIPTS conditional step vs unconditional AC | not raised | F3 MINOR | F2 MINOR | Low |
| C-013 | Wave 0 bullet "no L3 condition" vs L3/off line | not raised | F4 MINOR | not raised | Low |
| C-014 | Byte-identical pins checked against start text only | not raised | not raised | F1 MAJOR blocking | Medium |

## Contradictions
| # | Point | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | Severity of "a stated requirement has no mechanical AC" | V1 and V3 call it MAJOR blocking (C-001..C-005, C-014) | V2 calls the same family MINOR non-blocking (C-010, C-011) | High: decides the blocking count |
| X-002 | Does any task own the cycle-id reuse (C-001)? | V1: "no task edits that wiring" | Task 8 prose (plan line 124) says the ref reuses the id for the push triad and `rereview_requested`; V1's own quote of line 127 is the AC | Medium: the gap is the AC, not the ownership |
| X-003 | engage_decision with guard None (C-008) | V1: a literal build raises | Task 4 AC: each row has its own test, including rows 10 and 11 where guard is None | Medium: the AC would catch it |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Interface-level glue gaps (C-003, C-004, C-005) from reading the spec function list against the script JSON | High |
| U-002 | V2 | AC-mechanics gaps across Tasks 7, 9, 11 | Medium |
| U-003 | V3 | Prefix-versus-byte-identical pin weakness (C-014) | Medium |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | Prose requirements with no AC do not gate execution (the executor's per-task QA does not read task prose) | All three raise "no AC checks X" as a defect | UNSTATED | Yes |
| A-002 | The spec's own pins (F12, existing tests) are complete enough that only the plan can be at fault | All three audit the plan against the spec | UNSTATED | Yes |
| A-003 | Plan text at the executed commit is what the executor saw; HEAD adds nothing relevant | All three obey the attribution note | STATED | No |

### Promoted
| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | Prose requirements with no AC do not gate | Decides whether a missing AC is blocking | Debate |
| A-002 | Spec is correct; gaps lie only in the plan | Several C-items are spec-level (C-003, C-004, C-005) | Debate |

## Summary
- Total structural differences: 4; content: 14; contradictions: 3; unique contributions: 3; shared assumptions: 3 (UNSTATED 2, STATED 1, CONTRADICTED 0)
- Highest-severity items: S-002, C-001, X-001
- total_diff_points = 4 + 14 + 3 + 2 (A) = 23
