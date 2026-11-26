---
mode: pre
tier: 1
claim_class: static_defect
evidence_class: source_static
verdict_direction: AFFIRM
self_reported_confidence: 0.75
spec: .dev/tasks/to-do/TASK-WF-design-20261126-180705/source.md
tasklist: .dev/tasks/to-do/TASK-WF-design-20261126-180705/TASK-WF-design-20261126-180705.md
---

# T1 reflection card (UC-1, re-review of the regenerated plan)

## Scope and what was read

This plan replaces the plan reviewed in the first run (`.dev/tasks/archive/TASK-WF-design-20261126-162939/TASK-WF-design-20261126-162939.md`, 11 blocking, 14 medium, 10 note findings; its report is `.dev/reflect/pre-TASK-WF-design-20261126-162939-20261126164050/REPORT.md`, finding ids M-01 to M-35). The new plan has 8 phases and 38 tasks (`TASK-WF-design-20261126-180705.md:34` onward, Task 1 at line 36). Read in full: the diff between the two plans (`artifacts/plan-diff.txt`, 71 hunks, 247 lines), the new Constraints (lines 17 to 32) and the tasks the diff touches (Tasks 1 to 6, 8, 9, 12 to 15, 17 to 22, 24 to 32, 34, 36 to 38). Not re-read line by line: the unchanged tasks (7, 10, 11, 16, 23, 33, 35); they were reviewed in the first run and the diff shows no change to them.

## Coverage map

`ID_REGEX` Pass 1 matches only the design's test ids T-01 to T-27 (unchanged from the first run: 25 of 27 named in the plan, T-14 and T-18 not named, both covered by named tasks). Pass 2 (inferred rows, the design's FR, NFR, DD and AC ids with plan ranges expanded on both sides): 199 ids, 173 named in the plan text (`coverage_pct_union` 0.8693, was 0.8543), 26 not named (`artifacts/coverage.json`): FR-015, FR-016, FR-024 to FR-029, FR-037, FR-068, FR-069, FR-083 to FR-089, FR-119, NFR-004, NFR-011, NFR-013, NFR-015, NFR-016, T-14, T-18. Disposition is the one of the first run (16 are not active requirements, the rest are covered by a named task). `inferred_count` (172) is larger than `parsed_count` (27), so `coverage_degraded: parsed-sparse` forbids a Tier-1 stop.

## Candidate findings (to verify; none is yet a conclusion)

F1. Prior blockers M-01 to M-11 look repaired in the plan text: Constraint line 30 reworded (M-01); the S23 edit and the routing-test run moved from Task 19 to Task 20 (M-02); Task 24 scope limited to files this work adds (M-03); Task 25 uses `test ! -e` (M-04); Tasks 26 to 32 copy their plugin twins and Task 38 verifies (M-05); the two transient reasons are listed in `refs/commit-step.md` only (M-06); the `_ALLOW` entry and the override are in Tasks 26 and 32 (M-07); Task 9 copies nine patterns (M-08); Task 12 has `record-skipped` (M-09); T-04 and T-21 cases are in Tasks 15, 18, 28, 29, 34 (M-10); Task 13 has the `.dev/implement/` rule (M-11). Whether each repair is complete and correct is for the reviewers to decide.
F2. New text can hide new defects: Task 3's rule on `add -A` (allowed only in the runner's private-index calls) against `FORBIDDEN_FLAGS`; Task 4's from-scratch child environment; Task 30 now edits `refs/retry.md` too and re-keys `wc9-allowed` rows; Task 31 now depends on Task 30; Task 32's conditional `vcs reconcile` call; the Constraint that new tests are written first.
F3. The recorded base commit (Task 1) replaces `origin/integration` in the "unchanged" checks; the merge-base printed at pre-check time is 862384852faebe3255c2876527103696cfd3cf3b, equal to HEAD.

## Risk surface

The plan's size grew from 72 to 88 KiB; Tasks 26 to 32 now carry plugin-copy steps, which adds work to each and makes each task's acceptance run more suites. Existing pins touched by the plan are now named in the Constraints (STOP table, `_TRANSIENT`, `_ALLOW`, classification rows, parity tests).

## Recommendations

1. Decide each prior blocker M-01 to M-11 as resolved, open or regressed by reading the changed tasks against the diff, and grade new findings by the review severity rule.
2. Check the changed acceptance criteria can pass in task order against the real tests.
