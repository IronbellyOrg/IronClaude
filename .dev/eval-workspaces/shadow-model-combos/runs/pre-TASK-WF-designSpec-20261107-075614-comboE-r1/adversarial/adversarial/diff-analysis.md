# Diff Analysis: reviewer-card comparison (UC-1 pre-execution audit of the pr-submit merge guard plan)

## Metadata
- Generated: 2026-11-13
- Variants compared: 3 (variant-1 analyzer: 11 findings; variant-2 qa: 5 findings; variant-3 refactorer: 7 findings)
- Total differences found: 16 (structural 1, content 14, contradictions 2... see tables), unique 9, shared assumptions 3
- Categories: structural (1), content (14), contradictions (2), unique (9), shared assumptions (3)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card layout | Audit summary + 11 findings + coverage line | Short summary + 5 findings | Short summary + 7 findings | Low |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 11 ACs check test names, not behaviour | F1 MAJOR blocking | F1 MAJOR blocking | F1 MAJOR non-blocking | Medium |
| C-002 | One cycle_id shared by guard, push, rereview (spec 4.6) has no AC | F2 MAJOR blocking | F2 MAJOR blocking | F2 MAJOR non-blocking | Medium |
| C-003 | "no file:NNN pointers" rule has no AC | F9 MINOR | F4 MINOR | F3 MINOR | Low |
| C-004 | Task 7 `gh api --paginate` not exercised by a multi-page fake | F8 MAJOR non-blocking | F3 MINOR | F4 MINOR | Low |
| C-005 | Task 2 AC "grep 43" is judgment, not mechanical | F10 MINOR | F5 MINOR | absent | Low |
| C-006 | guard_status cannot return `unavailable` for a pre-request halt | F3 MAJOR blocking | absent | absent | High |
| C-007 | fold row for user_override sets no disabled_cause | F4 MAJOR blocking | absent | absent | Medium |
| C-008 | resume_decision row 4 lacks target_sha, applied_edits | F5 MAJOR blocking | absent | absent | Medium |
| C-009 | Section 3 "reconciled at any ordinal" vs resume row 2 REPORT_HELD | F6 MAJOR blocking | absent | absent | Medium |
| C-010 | Pre-push halt lives only in ref prose | F7 MAJOR non-blocking | absent | absent | Medium |
| C-011 | Task 9 Wave 0 bullet: "no L3 condition" vs off line at L3 | F11 MINOR | absent | absent | Low |
| C-012 | Task 6 AC does not check RunConfig/run_skill unchanged | absent | absent | F5 MINOR | Low |
| C-013 | Task 7 idempotency tested only for already-draft | absent | absent | F6 MINOR | Low |
| C-014 | Held report must carry a reason; Task 8 AC omits it | absent | absent | F7 MINOR | Low |

## Contradictions
| # | Point of Conflict | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | Is the pre-push halt checked by an AC? | V1 F7: Task 8 and Task 10 ACs "check other phrases" | Task 10 AC (plan line 153) says "the Wave 6 test asserts the Pre-push sentence" | Medium |
| X-002 | Citation validity | V2 F4 cites spec line 420 (file has 378 lines); V3 F7 cites a doubled path; V1 F4 cites spec line 151 for the user_override fold row (it is at line 206) | the pre-check flagged these | Low |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | C-006 guard_status / halt mapping gap | High |
| U-002 | V1 | C-007 disabled_cause for user_override | Medium |
| U-003 | V1 | C-008 resume_decision inputs | Medium |
| U-004 | V1 | C-009 section 3 vs row 2 | Medium |
| U-005 | V1 | C-010 pre-push halt AC | Medium |
| U-006 | V1 | C-011 Wave 0 bullet wording | Low |
| U-007 | V3 | C-012 RunConfig invariant | Low |
| U-008 | V3 | C-013 idempotent both directions | Low |
| U-009 | V3 | C-014 held reason | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | An AC is only a gate if a wrong implementation would fail it (a name-only or phrase-only AC does not count) | C-001..C-004 | UNSTATED | yes |
| A-002 | The package already shipped; the plan is judged against the spec text, not against the shipped code | all | STATED (brief) | no |
| A-003 | Task prose that describes a scenario but whose ACs only list test names is "not asserted" | C-001 | UNSTATED | yes |

## Summary
- Total structural 1, content 14, contradictions 2, unique 9, shared assumptions 3 (UNSTATED 2, STATED 1, CONTRADICTED 0)
- Highest-severity items: C-006
