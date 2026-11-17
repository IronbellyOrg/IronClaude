# Diff Analysis: reviewer-card Comparison (UC-1 pre, design spec v3 vs plan)

## Metadata
- Generated: 2026-11-13
- Variants compared: 3 (V1 analyzer/sonnet class, V2 qa/haiku class, V3 refactorer/opus class)
- Total differences found: 21
- Categories: structural (3), content (13), contradictions (2), unique (5), shared assumptions (3)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Card organization | Prose summary, 7 bulleted findings with sub-bullets, then block | Summary, "what holds up" list, then block | 4-line summary, then block | Low |
| S-002 | Blocking policy | 0 findings blocking | 1 of 11 blocking (F1), rationale stated | 0 blocking | Medium |
| S-003 | Citation style | Spec/plan lines plus short quotes | Spec/plan lines plus quotes with markdown backticks stripped (8 flagged quote-not-found by the pre-check) | One plan line, no quote | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | guard `cycle_id` never rebound (source.md:190-206, 139, 108, 166) | F1 MAJOR: stale id after a later cycle reuses a held draft | Not raised (F3/F4/F9 touch other facets of cycle identity) | Not raised | High |
| C-002 | Task 8 narrows spec sections 4.1-4.4 to 4.1/4.5/4.6/5 (source.md:240, plan:124) | F2 MAJOR | Not raised | Not raised | High |
| C-003 | `guard_status` vs `draft_guard_unavailable` halt before any event (source.md:112,135,140) | F3 MINOR | Not raised | Not raised | Medium |
| C-004 | Failed first engage leaves RELEASE_PENDING with owned_draft false; engage row 6 never re-checks live draft (source.md:138,199) | F4 MAJOR | Not raised | Not raised | High |
| C-005 | Resume row 4 (`published`) outranks rows 5-6 (source.md:166-168) | F5 MAJOR | Not raised | Not raised | Medium |
| C-006 | `guard_status` OFF wording; resume row 6 has no phase condition | F6, F7 MINOR | Not raised | Not raised | Low |
| C-007 | Per-cycle `applied_edits` passed by protocol, not run-wide (source.md:107,366; plan:75,166) | Treats INF-021 as carried by Tasks 3, 4, 8 | F1 MAJOR blocking: no criterion checks the protocol passes the per-cycle count | Not raised | High |
| C-008 | One cycle id shared by guard events, push key, `rereview_requested` (source.md:251; plan:170) | Not raised | F3 MINOR, F9 MINOR | Not raised | Medium |
| C-009 | "Once per cycle id" has no decision-row home (source.md:133,143; plan:168) | Related to C-001, not stated | F4 MINOR | Not raised | Medium |
| C-010 | PR body release-gate statement has no producing task (source.md:326; plan:33) | Not in its slice | F5 MINOR | Not raised | Low |
| C-011 | Stated requirements with no acceptance criterion: Task 9 flag/wave-line tests, `file:NNN` rule outside Task 8, Task 10 dependency lines, `original_is_draft` never re-read, engage-failure message | Not raised | F6, F7, F8, F10, F11 | Not raised | Medium |
| C-012 | Byte-identical pin checks compare only a start-text constant (plan:154; source.md:377) | Not raised | F2 MAJOR | Not raised | Medium |
| C-013 | Task 2 grep criterion for "43" is a judgment call (plan:49) | Not raised | Not raised | F1 MINOR | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Is per-cycle `applied_edits` adequately covered by the plan? | Rows INF-021 treated as carried by Tasks 3, 4 and 8 | F1: not covered, blocking | n/a | Medium |
| X-002 | Is the plan's coverage of the assigned rows complete? | "No contradictions" in INF-017..047 apart from F1-F7 | Gaps in INF-078..083 | "Assigned rows are covered" for INF-048..063 | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Four decision-table defects in the spec's resume and engage logic (C-001, C-004, C-005, C-006) | High |
| U-002 | V1 | Task 8 narrows the spec's source sections (C-002) | High |
| U-003 | V2 | Acceptance-criterion gaps and weak pins (C-007, C-011, C-012) | High |
| U-004 | V2 | Release-gate and cycle-id sharing gaps (C-008, C-009, C-010) | Medium |
| U-005 | V3 | Task 2 grep criterion ambiguity (C-013) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|-------|-----------|------------------|----------------|--------|--------|
| A-001 | The spec's decision tables are the authoritative intended behaviour, so a table gap is a plan-or-spec defect, not an implementation choice | All three audit the plan against the spec tables | UNSTATED | High | Promoted |
| A-002 | The plan was executed once; HEAD state is evidence of execution, not a plan failure | All three follow the brief's attribution line | STATED (brief) | Medium | Documented |
| A-003 | An acceptance criterion that exists in a task body but not in its AC list does not gate the task | V2 and V3 both rely on it for "unpassable-check" findings | UNSTATED | Medium | Promoted |

## Summary
- Total structural differences: 3
- Total content differences: 13
- Total contradictions: 2
- Total unique contributions: 5
- Total shared assumptions surfaced: 3 (UNSTATED: 2 promoted, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-004, C-007
- Taxonomy tags (AD-5): L3 state mechanics: C-001, C-004, C-005, C-006, C-007, X-001, A-001; L2 structural: C-002, C-008, C-009, C-011, C-012, S-002; L1 surface: S-001, S-003, C-013, C-010, C-003.
