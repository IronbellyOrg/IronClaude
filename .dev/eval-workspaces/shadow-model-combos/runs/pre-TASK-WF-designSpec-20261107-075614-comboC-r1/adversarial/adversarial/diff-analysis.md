# Diff Analysis: reviewer-card comparison (UC-1 pre-execution audit of the pr-submit merge guard plan)

Variants: V1 = reviewer-1 card (analyzer), V2 = reviewer-2 card (qa), V3 = reviewer-3 card (refactorer). Source files for every claim:
- spec: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md
- plan: .dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md

## Metadata
- Generated: 2026-11-13
- Variants compared: 3
- Categories: structural (3), content (12), contradictions (3), unique (4), shared assumptions (3)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Findings count and severity mix | 3 findings (2 MAJOR, 1 MINOR), none blocking | 12 findings (7 MAJOR all blocking=true, 5 MINOR) | 4 findings, all MINOR, none blocking | High |
| S-002 | Prose section | "What held / What I refute / Defects" list | "Checked / Held / Refuted / New gaps" | "What held / On the T1 excerpt / MINOR list" | Low |
| S-003 | Scope of lens | decision tables, fold, classifier, resume | acceptance criteria and matrix rows | task order, dependencies, shared files | Medium |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 9 Wave 0 bullet "no L3 condition" vs "at L3 with off" | silent | F2 MAJOR blocking (unpassable-check) | confirms the T1 finding, no new finding | Medium |
| C-002 | Task 7 timeline count and `--paginate` have no failable criterion | F1 MAJOR | silent | silent | Medium |
| C-003 | Auto-merge signal (`notes`, `autoMergeRequest` value) has no failable criterion | silent | F7 MAJOR blocking | silent | Medium |
| C-004 | Zero-edit cycle can release a PR that holds an earlier cycle's unpublished fix | F2 MAJOR data-loss | silent | silent | High |
| C-005 | Release retry once / `already_in_state` / `release_pending` | silent | F3 MAJOR blocking: "no mechanism" | silent | Medium |
| C-006 | Plan line 25 scope limits attributed to the spec as "non-goals" | silent | F1 MAJOR blocking contradiction | silent | Low |
| C-007 | Guard, push triad and `rereview_requested` share one cycle id | silent | F4 MAJOR blocking | silent | Medium |
| C-008 | `--undo` on the draft call and absence on the ready call | silent | F5 MAJOR blocking | silent | Medium |
| C-009 | Task 11 criterion passes on empty test stubs | silent | F6 MAJOR blocking | silent | Medium |
| C-010 | `Depends on:` lines (Task 1 consumers, Task 12 shared files) | "dependencies complete for the import chain" | silent | F1, F2 MINOR | Low |
| C-011 | Fold `not_applied` ready request returning to `RELEASE_PENDING` untested | F3 MINOR | silent | silent | Low |
| C-012 | Criteria that name an exception path (Task 9 classification entry; Task 7 `_RESOLUTION_SCRIPTS`) | silent | silent | F3, F4 MINOR | Low |

## Contradictions
| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Blocking posture: five findings V2 marks blocking true are not raised or are MINOR in V1 and V3 (same plan) | no blocking | 7 blocking | no blocking | High |
| X-002 | Does the plan specify the release retry? | n/a | F3 says no mechanism; plan line 124 text reads "one retry; `already in target state` counts as confirmed" | n/a | Medium |
| X-003 | Dependencies: V1 says complete; V3 says Tasks 9, 10, 12, 13 miss `Depends on: Task 1` | complete | n/a | incomplete | Low |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Traced scenario for C-004 (HOLD, then zero-edit cycle, then RELEASE) | High |
| U-002 | V2 | Six acceptance-criterion gaps (C-005, C-007, C-008, C-009, C-003, C-001) | Medium |
| U-003 | V2 | Matrix completeness note (F12): the 45 inferred rows omit table rows and gates G1-G6 | Low |
| U-004 | V3 | Plan structure checks: shared-file ordering, stale-entry order, pinned sentences | Medium |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | A later fix cycle can start after a held cycle (release HOLD) | V1 F2 relies on it; V2 and V3 silent | UNSTATED | Yes |
| A-002 | An acceptance criterion that names a test or an artifact is "failable" only when its body asserts the behaviour | V2 F6, V3 F3/F4 | UNSTATED | Yes |
| A-003 | The plan is judged as authored on 2026-11-07, not against shipped HEAD code | all three | STATED (brief attribution) | No |

Promoted: A-001, A-002 (taxonomy L3 and L2).

## Summary
- Total structural differences: 3
- Total content differences: 12
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-001, C-004, X-001
