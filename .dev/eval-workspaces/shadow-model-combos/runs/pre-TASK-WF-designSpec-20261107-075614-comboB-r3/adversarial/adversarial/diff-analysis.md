# Diff Analysis: reviewer-card Comparison (UC-1 pre, spec vs plan, merge-guard)

## Metadata
- Generated: 2026-11-13T05:24:00Z
- Variants compared: 3 (variant-1 analyzer/sonnet-class, variant-2 qa/haiku-class, variant-3 refactorer/opus-class)
- Total differences found: 4 structural, 9 content, 2 contradictions, 5 unique, 2 shared assumptions
- Categories: structural (4), content (9), contradictions (2), unique (5), shared assumptions (2)

## Structural Differences
| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Finding count | 5 findings (1 MAJOR, 4 MINOR) | 2 findings (2 MINOR) | 4 findings (2 MAJOR, 2 MINOR) | Low |
| S-002 | Verification narrative | confirms/refutes each T1 finding | lists rows only | lists covered rows and not-satisfied rows | Low |
| S-003 | Severity of the cycle-id finding | not reported | MINOR | MAJOR | Medium |
| S-004 | Row coverage claim | 25 rows verified, overturns UNMATCHED labels | 25 rows verified, no per-row evidence | 25 rows verified, overturns 4 UNMATCHED labels | Low |

## Content Differences
| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | resume_decision row 4 re-entry (T1-F1) | MAJOR: signature lacks cycle_id, applied_edits, target_sha; GuardAction has no re-enter member; AC names no action/reason | not reported | MAJOR: signature lacks applied_edits and target_sha; release rows 7-8 need both | High |
| C-002 | One cycle id across guard, push and rereview_requested | "no missed defects" | MINOR: only minting place and event order are checked | MAJOR: no AC checks equality; held_cycle_published depends on it | Medium |
| C-003 | Task 12 grep vs heading "Merge guard" | MINOR unpassable-check | not reported | not reported | Low |
| C-004 | autoMergeRequest boolean conversion | MINOR missing-requirement | not reported | not reported | Low |
| C-005 | _RESOLUTION_SCRIPTS criterion vacuous | MINOR | not reported | not reported | Low |
| C-006 | Phase string values unstated | MINOR, "very low risk" | not reported | not reported | Low |
| C-007 | Event-field contracts (section 4.2) not enforced writer-side | not reported | MINOR | not reported | Low |
| C-008 | Depends on: Task 1 missing on Tasks 9, 10, 12, 13 | not reported (says dependencies consistent) | not reported | MINOR | Low |
| C-009 | file:NNN pointer ban has no criterion | not reported | not reported | MINOR | Low |

## Contradictions
| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Variant 3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | Are the plan's dependencies complete? | "Dependencies and the twelve scenario test names are consistent" (variant-1-original.md, narrative) | silent | Tasks 9, 10, 12, 13 read pre-build-gate.md but do not list Task 1 (variant-3-original.md F3) | Low |
| X-002 | Is the cycle-id equality gap real and how severe? | "Missed defects: none worth raising" | MINOR | MAJOR | Medium |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | Rebuttal of the "SKILL does the re-entry" reading of resume row 4 (spec 280) | High |
| U-002 | 1 | Narrowing of T1-F5 (already_draft is stated in spec 112, 200; only Phase values unstated) | Medium |
| U-003 | 2 | Event-field contract gap (attempt-scoped keys, first-request-only baseline) | Low |
| U-004 | 3 | Dependency-line gap against spec section 10 | Low |
| U-005 | 3 | file:NNN pointer ban unenforced by any criterion | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | HEAD source is not evidence of what the plan could know; base-commit excerpts are authoritative | all three cards cite only spec and plan lines | A reviewer that never opened base-grounding.md (variant 1) may miss base-commit facts | UNSTATED (promoted) |
| A-002 | The 25-row slices each reviewer "verified" were checked against the plan, not only against the matrix labels | all three list rows without per-row evidence | Coverage claims are not independently checkable | UNSTATED (promoted) |

## Summary
- Total structural differences: 4
- Total content differences: 9
- Total contradictions: 2
- Total unique contributions: 5
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001
