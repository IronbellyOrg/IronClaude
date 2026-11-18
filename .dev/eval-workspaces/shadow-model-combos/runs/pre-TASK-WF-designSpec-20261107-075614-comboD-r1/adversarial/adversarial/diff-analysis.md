# Diff Analysis: reviewer-card Comparison (UC-1 pre-execution audit of the pr-submit merge-guard plan)

## Metadata

- Generated: 2026-11-13 (orchestrator inline, Step 1)
- Variants compared: 3 (V1 = reviewer-1 analyzer, V2 = reviewer-2 qa, V3 = reviewer-3 refactorer)
- Total differences found: 18 (structural 2, content 12, contradictions 2, shared assumptions 2 promoted)
- Unique contributions: 8
- Subject under audit: plan `TASK-WF-designSpec-20261107-075614.md` (13 tasks) against `source.md` (design spec v3)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Body before the findings block | four bullet summary | paragraph plus scope disclosure | one sentence | Low |
| S-002 | Findings count and severity spread | 4 (1 MAJOR, 3 MINOR), none blocking | 7 (4 MAJOR, 3 MINOR), 1 blocking | 4 (2 MAJOR, 2 MINOR), 2 blocking | Medium |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 8 omits spec section 4.2 (event fields, key rules) | F1 MAJOR, not blocking | absent | F1 MAJOR, blocking | High |
| C-002 | Task 9 Wave 0 bullet: "no L3 or draft condition" vs the required "at L3 with off" text | absent | F1 MAJOR, blocking | F2 MAJOR, blocking | Medium |
| C-003 | Cycle id minted at end of Wave 3 is never asserted equal in the push triad and `rereview_requested` | absent | F2 MAJOR | F4 MINOR | Medium |
| C-004 | Fold's `cycle_id` has no advance rule or second-cycle criterion (Task 3) | F3 MINOR | absent | absent | Medium |
| C-005 | Task 4 `classify_toggles` test omits the `unsettled` slack term | F2 MINOR | absent | absent | Medium |
| C-006 | Task 5 asserts Phase string values Task 3 never fixes | F4 MINOR | absent | absent | Low |
| C-007 | Tasks 9, 10, 12 consume the pre-build record without `Depends on: Task 1` | absent | absent | F3 MINOR | Low |
| C-008 | Medium-or-higher trigger is phrase-tested only | absent | F3 MAJOR | absent | Medium |
| C-009 | "Byte-identical" pins compared against start text only | absent | F4 MAJOR | absent | Medium |
| C-010 | `autoMergeRequest` boolean conversion untested | absent | F5 MINOR | absent | Low |
| C-011 | Classification steps name `gh pr` and `gh api` but not git write verbs | absent | F6 MINOR | absent | Low |
| C-012 | Task 3 fold test "covers every row" but names four rows' cases only implicitly | absent | F7 MINOR | absent | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is the Task 8 omission blocking? | MAJOR, `blocking: false` (plan line 124, spec 182-185) | does not report it | MAJOR, `blocking: true` | High |
| X-002 | Is Task 9's L3 wording an unpassable check? | does not report it | blocking contradiction (plan 137, 140) | blocking unpassable-check (plan 137-140) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | C-004 fold `cycle_id` advance rule | Medium |
| U-002 | V1 | C-005 `unsettled` slack test gap | Medium |
| U-003 | V1 | C-006 Phase string values | Low |
| U-004 | V2 | C-008 severity trigger phrase-only | Medium |
| U-005 | V2 | C-009 start-text constants | Medium |
| U-006 | V2 | C-010 `autoMergeRequest` boolean | Low |
| U-007 | V2 | C-011 git write verb classification | Low |
| U-008 | V3 | C-007 dependency completeness | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | An executor follows the plan text literally and consults only the spec sections a task names, so anything a task omits is not built | C-001 (V1, V3) | UNSTATED | Yes |
| A-002 | Phrase-presence and static-text tests are an adequate verifier for the prose protocol files (`SKILL.md`, `refs/merge-guard.md`) | C-002, C-003, C-008 | UNSTATED | Yes |
| A-003 | All three cards audited the same plan and spec snapshot and none relied on the landed code | brief text | STATED | No |

| # | Assumption | Impact | Status |
|---|---|---|---|
| A-001 | Literal-executor model decides whether C-001 is blocking | High | open |
| A-002 | Adequacy of phrase tests decides C-003, C-008, C-009 | Medium | open |

## Taxonomy tags

L1 surface (wording, naming): C-006, X-002, S-001. L2 structural (task and file ownership, component, dependency): C-001, C-003, C-007, C-009, C-011, A-001, A-002, S-002. L3 state mechanics (state, guard, transition, validation rule): C-004, C-005, C-012, C-010, C-008.

## Summary

- Total structural differences: 2
- Total content differences: 12
- Total contradictions: 2
- Total unique contributions: 8
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 1 not promoted, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001
- Diff points for convergence: S 2 + C 12 + X 2 + A 2 = 18
