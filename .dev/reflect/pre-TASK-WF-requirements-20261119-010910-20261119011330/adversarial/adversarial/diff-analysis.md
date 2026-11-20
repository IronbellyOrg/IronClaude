# Diff Analysis: v2 plan reviewer cards (UC-1)

## Metadata
- Variants: 3 (V1 analyzer/sonnet, V2 qa/haiku, V3 refactorer/opus). All three confirm the 12 earlier findings (M-1 to M-13) are fixed in plan v2.
- Categories: structural (2), content (10), contradictions (2), unique (8), shared assumptions (2)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Severity labels | blocking/medium/note | every row Blocking, with MEDIUM or HIGH inside | blocking/medium/note | Medium |
| S-002 | Prior-fix check | per-finding list with plan lines | one line per finding | per-finding list | Low |

## Content Differences (finding points)
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 9: a launched agent calls `issue-pipeline complete`; the write happens inside Python, past the launch-level guard and WORKER-CONTRACT.md:241-243 and :300 | N-1 blocking | QA-1 blocking | B-1 blocking | High |
| C-002 | Task 10 breaks tests/issue_watch/test_security_invariants.py:911-919 (asserts the literal repo and no `$owner`) while the plan says it still passes | N-2 blocking | none | none | High |
| C-003 | Tasks 6 and 9 edit the wrong place: the guard has no prompt allow-list, PROMPT_PATTERN lives in launch.py:33 | N-1 (part) | none | none | Medium |
| C-004 | Missing Depends-on edges: Task 8 needs Task 10 and an item-id read; Task 11 vs Task 5; Task 22 vs Tasks 7 and 9 | N-3, N-4 medium | none | none | Medium |
| C-005 | Nothing proves who set the Pipeline field or when; approval compares label times only (predicates.py:228-233, 249-258) so a raised Pipeline after approval can launch Full Submit | none | none | B-2 blocking | High |
| C-006 | Task 8 marker check accepts any author; a failed Status move is never retried on a second call | none | none | M-a medium | Medium |
| C-007 | Task 4 does not decide which Status command fits which launch level, nor the end Status per pair (Debug `--fix` at Worktree then moves to In review) | none | none | M-b medium | Medium |
| C-008 | Task 18: a killed or timed-out child leaves no launched line, so the loop can launch a second issue in the same sweep | none | QA-2 blocking | none | High |
| C-009 | R23(c): no acceptance test of the Spec "well defined" judgment, its recorded reason or the high-complexity handoff | none | QA-3 blocking (MEDIUM) | none | Medium |
| C-010 | NG-2 test header and argv-builder scan miss the new read modules | none | none | N-1 note | Low |

## Contradictions
| # | Point | V1 | V2 | V3 |
|---|---|---|---|---|
| X-001 | Is the launched agent's self-call an allowed design choice? | Task 4 must decide, with guard and grant rule | it breaks the coordinator-only write rule | it breaks the guard and the contract |
| X-002 | Severity of C-008 and C-009 | not raised | blocking | not raised |

## Unique Contributions
C-002, C-003, C-004 (V1); C-008, C-009 (V2); C-005, C-006, C-007, C-010 (V3).

## Shared Assumptions
| # | Assumption | Classification |
|---|---|---|
| A-001 | The Pipeline field value is a trustworthy statement of the owner's intent | UNSTATED |
| A-002 | A launched claim agent is allowed to perform issue and Project writes that the guard forbids at its level | UNSTATED |

## Summary
Total diff points: 2 structural + 10 content + 2 contradictions + 2 shared assumptions = 16.
