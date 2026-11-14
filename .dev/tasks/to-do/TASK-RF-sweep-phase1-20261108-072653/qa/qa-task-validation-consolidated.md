# A.10 Task file structural validation, consolidated (cycle 1)

Date: 2026-11-08
Task file: TASK-RF-sweep-phase1-20261108-072653.md (2479 lines, 14 phases, 297 items)

## Items Reviewed

| Report | Lens | Partition | Verdict | Blocking | Minor |
|---|---|---|---|---|---|
| qa-task-validation-b2-report-p1.md | b2-self-containment | Phases 1-7 | FAIL | 9 IMPORTANT | 8 |
| qa-task-validation-b2-report-p2.md | b2-self-containment | Phases 8-14 | FAIL | 9 IMPORTANT | 10 |
| qa-task-validation-structure-report-p1.md | phase-structure | front matter + Phases 1-7 | FAIL | 5 IMPORTANT | 12 |
| qa-task-validation-structure-report-p2.md | phase-structure | Phases 8-14 + Task Log | FAIL | 2 IMPORTANT | 10 |

Combined: 25 blocking (all IMPORTANT, 0 CRITICAL), 40 minor. Overlaps between partitions are resolved by the fix agent.

## Blocking findings to fix (summary; full text and item numbers in each report)

- B2-p1: about 60 repeated QA gate items cross-reference earlier items ("Same inputs as 2.8", "Apply the item 2.21 procedure") instead of restating inputs and rules; items 2.1-2.6 cite research/04 lines off by 2; item 7.16 runs `worker-show` before the `worker-list` call that supplies Dispatch ids and omits the `orca-tabs/` path; plus the other IMPORTANT items in the report.
- B2-p2: `${TASK_DIR}` is used in shell commands but never set (items 14.8, 14.43 and others write to the wrong folders); plus the other IMPORTANT items in the report.
- Structure-p1: R5 has no QA gate or `qa/r5/` folder; the decisions gate has 5 agents (floor is 6); gates cannot build the PASS set that the regression halt needs; no lens batch is marked parallel; the sprint/swarm Execution Context source area appears in no item.
- Structure-p2: the Task Log has no Follow-Up Items section; Phases 11 and 12 have no QA gate although QA_GATE_REQUIREMENTS is PER_PHASE.
- Orchestrator addition (graded blocking here, minor in structure-p2): routing row R5 (`_POST_REFRESH_ADDITIONS` in `tests/recommend/test_routing_refresh.py`) lands three items after `sweep.md` is created; research/03 shows creating `sweep.md` trips that test, so R5 must land in the same item as, or before, any test run after `sweep.md` exists. Move it next to the `sweep.md` creation item.

## Minor findings

Recorded in the four reports as notes; not fixed in this cycle unless a blocking fix covers them.
