# Diff Analysis: reviewer-card comparison (sc:reflect Wave 4)

## Metadata
- Generated: 2026-10-31T19:00:00Z
- Variants compared: 3 (variant-1 = reviewer-1 sonnet/analyzer, variant-2 = reviewer-2 glm-via-haiku/qa, variant-3 = reviewer-3 opus/refactorer)
- Subject under review: plan .dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md against design .dev/pr-submit-codex/design/pr-submit-codex-design.md
- Focus: correctness, coverage, deviation-classification
- Total differences found: 19
- Categories: structural (2), content (9), contradictions (4), unique (11), shared assumptions (2)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Finding granularity | 10 findings, mixed code/plan gaps | 14 findings, 9 are design-section gaps | 11 findings, code-anchored | Low |
| S-002 | Class vocabulary | gap/drift/refinement/aligned | gap/refinement/aligned (no drift) | gap/drift/refinement/aligned | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 9 dependency on Tasks 4/7/8 | R1-1 gap, medium | not raised | R3-F2 drift, medium | Medium |
| C-002 | Codex completion time hand-off to _thread_findings | R1-4 gap, medium | not raised | R3-F1 gap, medium | High |
| C-003 | Crash between Augment and Codex re-trigger posts | R1-3 gap, medium (recovery.py change or test) | not raised | R3-F4 gap, medium (SKILL resume calls pending_retriggers) | High |
| C-004 | Missing Codex gate rows in Task 7 acceptance | R1-8 low | not raised | R3-F8 low | Low |
| C-005 | Stale event-count texts | R1-5 loop-guard.md 37 | R2-10 run_log.py 37 | R3-F5 models.py + run_log.py | Low |
| C-006 | reviewer field on events | not raised | R2-05 medium (all Wave 1/6 events) | R3-F9 low | Medium |
| C-007 | Augment presence predicate divergence | R1-6 drift low | R2-12 refinement low | R3-F7 refinement low (weak per calibrator) | Low |
| C-008 | Dedup group handling in later waves | not raised | R2-01 high (reply/resolve fan-out), R2-03 max tier, R2-04 fix_applied per member, R2-09 flagged-by | not raised | High |
| C-009 | S5 re-review semantics | not raised | R2-02 subset wait + attribution, R2-07 reviewer_incomplete phase rereview | not raised | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | What a local override WITHOUT Codex fields should mean | R1-7: accept "Codex disabled", record the choice and document it (refinement, low) | R2-11: accept resolution toward empty, record it (refinement, low) | R3-F3: wrong; from_yaml must fall back to shipped Codex identities, only explicit empty disables (drift, medium) | High |
| X-002 | Class of the Task 9 dependency defect | gap | (silent) | drift | Low |
| X-003 | Class of the activity-predicate divergence | drift | refinement | refinement | Low |
| X-004 | Fix location for the crash-resume hole | recovery.py change + test_crash_recovery.py case | (silent) | SKILL.md/review-retrigger.md resume text + Task 10 test | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | R1-2: Tasks 7-9 have no in-task tests; Task 7 dry check depends on live PR 336 with no fallback | Medium |
| U-002 | 1 | R1-9: pr-submit.md --silence-timeout row still says No-Augment-activity | Low |
| U-003 | 2 | R2-01: verified group members each need reply + resolve in Wave 6 | High |
| U-004 | 2 | R2-03/R2-04: group max-tier routing and per-member fix_applied | Medium |
| U-005 | 2 | R2-02/R2-07: S5 waits only for re-triggered reviewers; at-least-one attribution; reviewer_incomplete{phase: rereview} | Medium |
| U-006 | 2 | R2-06: Codex findings join the S5b decline fallback re-entry | Medium |
| U-007 | 2 | R2-08: resume path reads absent_reviewers | Low |
| U-008 | 2 | R2-13: Task 15 grep omits the two release guides | Low |
| U-009 | 3 | R3-F6: SKILL Output Contract rereview_request_count wording | Low |
| U-010 | 3 | R3-F10: poll script advisory state is not a Codex completion signal | Low |
| U-011 | 3 | R3-F11: seed absent_reviewers in the initial rebuild_state dict | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The plan may not be edited from reflect findings (workflow Wave 4 is advisory), so every finding must be absorbed by the executor inside the existing tasks' scope ("per design sections 4-13") rather than by new tasks | All three phrase recommendations as "extend Task N" | High: if executors only follow acceptance criteria literally, design-only requirements are dropped | UNSTATED |
| A-002 | Design section text is binding on tasks that cite "per design sections X-Y" even where the task body does not restate a rule | All three treat unrestated design rules as gaps rather than as covered-by-reference | Medium | UNSTATED |

## Summary
- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 4
- Total unique contributions: 11
- Total shared assumptions surfaced: 2 (UNSTATED: 2, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-002, C-003, C-008, X-001, U-003
- Taxonomy auto-tags: L3 (state/guard/boundary): C-002, C-003, X-001, X-004, C-009, A-001; L2: C-001, C-006, C-008, U-*; L1: S-001, S-002, X-002, X-003, C-005
