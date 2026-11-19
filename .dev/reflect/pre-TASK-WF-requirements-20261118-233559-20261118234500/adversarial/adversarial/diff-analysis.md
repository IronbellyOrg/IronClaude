# Diff Analysis: reviewer cards for the zero-setup watcher plan (UC-1)

## Metadata
- Variants compared: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus)
- Categories: structural (3), content (14), contradictions (2), unique (9), shared assumptions (2)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Severity vocabulary | blocking/medium/note | every row called Blocking, then MEDIUM/HIGH | blocking/medium/note | Medium |
| S-002 | Verdict | none | FAIL | FAIL | Low |
| S-003 | Checked-and-clean list | 30+ cites listed | none | short list | Low |

## Content Differences (finding points)
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Lock and restart tests missing from Task 13 (R18, source.md:44, 62) | F3 medium | QA-1 | F3 blocking | High |
| C-002 | R18 auto-enable vs source.md:60 owner-only switch-on | F1 blocking | QA-6 (no precedence) | F4 medium | High |
| C-003 | R20 only recorded, not verified | F2 medium | QA-5 | F5 note, correct handling | Medium |
| C-004 | R23 confirmations still open; Full Submit maps to push and PR | none | QA-2 | F2 blocking | High |
| C-005 | Automatic approval record has no plan hash (Task 6, R19) | none | none | F1 blocking | High |
| C-006 | One launch per sweep fails when a launch outcome is unknown (Tasks 14-15) | none | QA-3 | none | High |
| C-007 | Prompt uses Status and Pipeline read at examine time, not at launch (Task 5) | none | QA-4 | none | High |
| C-008 | Task 18 and Task 20 dependency gaps | F4 medium | note | F6 note | Medium |
| C-009 | Task 16 creates labels from the loop; R14 says report | none | none | F7 medium | Medium |
| C-010 | New modules hard-code real home paths; test isolation | none | none | F8 medium | Medium |
| C-011 | Task 2 may miss issue-watcher.md line 15 | F5 medium | none | none | Low |
| C-012 | Task 6 omits files holding the old fixed prompt | F6 medium | none | none | Medium |
| C-013 | Task 7 omits argv_events and argv_comments | F7 note | none | none | Medium |
| C-014 | Task 11 REST reads need `--method GET` | none | none | F9 note | Low |

## Contradictions
| # | Point | V1 | V2 | V3 |
|---|---|---|---|---|
| X-001 | Is R20 a plan gap? | yes (medium) | yes (blocking) | no, Coder row, open question is right |
| X-002 | Who wins, R18 or source.md:60? | R18 should be stated as superseding | no precedence is established | R18 wins, line 60 is stale |

## Unique Contributions
C-005, C-006, C-007 (High); C-009, C-010, C-012, C-013 (Medium); C-011, C-014 (Low).

## Shared Assumptions
| # | Assumption | Classification |
|---|---|---|
| A-001 | The plan's Task 4 design note is allowed to settle R23 points that the source lists as open | UNSTATED |
| A-002 | `dispatch.json` approval fields are what R19 calls the approval record | UNSTATED |

## Summary
Total diff points: 3 structural + 14 content + 2 contradictions + 2 shared assumptions = 21.
