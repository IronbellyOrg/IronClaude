# Diff Analysis: reviewer-card comparison (pre-execution audit of the pr-submit merge-guard plan)

## Metadata
- Generated: 2026-11-13T04:19:00Z
- Variants compared: 3 (V1 = reviewer-1 analyzer/sonnet, V2 = reviewer-2 qa/haiku, V3 = reviewer-3 refactorer/opus)
- Total differences found: 40
- Categories: structural (3), content (20), contradictions (5), unique (10), shared assumptions (4 surfaced, 2 promoted)
- Plan = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`; spec = `.../source.md`. Finding ids below are `V<n>:F<m>` = variant n, finding m.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Blocking flag use | 0 of 7 findings blocking | 4 of 12 blocking (F1 to F4) | 0 of 8 blocking | Medium |
| S-002 | Finding count and spread | 7 findings, 5 MAJOR | 12 findings, 4 MAJOR + 8 MINOR | 8 findings, 1 MAJOR + 7 MINOR | Low |
| S-003 | Prose summary shape | Checked/Held/Refuted/New | Checked/Held/Refuted/Caveats | Checked/Held/Refuted/New | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | Wave 0 bullet: "at L3 with off" vs "no L3 condition" (plan 137, 140) | F1 MAJOR contradiction, "wording problem more than a logic one" | F5 MINOR contradiction, fix: reword the test to target the ref-load gate | not raised | Medium |
| C-002 | FR-16 release retry has no row or criterion (spec 315) | F2 MAJOR | F2 MAJOR blocking, adds "already_in_state is not a script output" | not raised | High |
| C-003 | Shared cycle_id across guard, push triad, rereview_requested (spec 251) | F3 MAJOR | F3 MAJOR blocking, adds off-mode invariance | not raised | High |
| C-004 | settled(draft,failed) leaves RELEASE_PENDING, engage then HOLD (spec 138, 199) | F4 MAJOR, edits may proceed on HOLD | F12 MINOR, latent because engage failure halts first | not raised | Medium |
| C-005 | Task 11 criterion strength (plan 169-173) | F5 MAJOR: names-only passes stubs, driver tests the driver | F7 MINOR: omits moved-head, unreadable-timeline, FR-17 cases | not raised | Medium |
| C-006 | Task 10 "byte-identical" compares only the start text (plan 154) | not raised | F6 MINOR | F4 MAJOR | Medium |
| C-007 | Depends-on lines incomplete (spec 363) | not raised | F10 MINOR (Task 10, Task 13) | F6 MINOR (Tasks 9, 10, 12, 13) | Low |
| C-008 | autoMergeRequest bool conversion and transitions value untested (spec 230) | not raised | F8 MINOR | not raised | Medium |
| C-009 | Wave 3 test cannot reject an unconditional engage (plan 153) | not raised | F4 MAJOR blocking | not raised | Medium |
| C-010 | resume_decision lacks target_sha and applied_edits that release_decision needs (spec 107-109, 166) | not raised | F1 MAJOR blocking | not raised | High |
| C-011 | Plan 25 calls scope limits "non-goals of ./source.md" | not raised | not raised | F1 MINOR | Low |
| C-012 | Task 13 expects git status to list ignored .claude mirrors (plan 200) | not raised | not raised | F2 MINOR | Low |
| C-013 | Phase string values undefined in Task 3, pinned lowercase in Task 5 | not raised | not raised | F3 MINOR | Low |
| C-014 | file:NNN ban has no acceptance check | not raised | not raised | F5 MINOR | Low |
| C-015 | Wave 8 test weaker than the Wave 6 test | not raised | not raised | F7 MINOR | Low |
| C-016 | Classification steps mention only gh pr / gh api, not git write verbs | not raised | not raised | F8 MINOR | Low |
| C-017 | PR body and the opening run's --merge-guard off have no task | F7 MINOR | not raised | not raised | Low |
| C-018 | not_applied of a ready request back to RELEASE_PENDING untested | F6 MINOR | not raised | not raised | Low |
| C-019 | Task 3 fold test list incomplete vs spec 4.2 | not raised | F11 MINOR | not raised | Low |
| C-020 | --merge-guard inert below monitor 3 not tested | not raised | F9 MINOR | not raised | Low |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Severity of the Wave 0 contradiction | MAJOR (V1:F1) | MINOR (V2:F5) | silent | Medium |
| X-002 | Severity of the byte-identical prefix check | silent | MINOR (V2:F6) | MAJOR (V3:F4) | Medium |
| X-003 | Severity of the failed-engage/RELEASE_PENDING path | MAJOR, edits may proceed (V1:F4) | MINOR, latent (V2:F12) | silent | Medium |
| X-004 | Does Task 11 pass on empty stubs? | yes, MAJOR (V1:F5) | only case omissions, MINOR (V2:F7) | silent | Medium |
| X-005 | Is inertness below monitor 3 untested? | silent | yes (V2:F9) | silent; V1 notes plan 73 and 172 already cover ordinal 2 and off | Low |

Evidence: each row cites the findings blocks of the named variants; the plan lines are quoted in those blocks.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V2 | resume_decision cannot call release_decision without target_sha and applied_edits (C-010) | High |
| U-002 | V2 | Wave 3 test passes an unconditional engage sentence (C-009) | Medium |
| U-003 | V2 | autoMergeRequest conversion and transitions count (C-008) | Medium |
| U-004 | V3 | plan 25 non-goals misattribution (C-011) | Low |
| U-005 | V3 | git status never lists ignored files (C-012) | Low |
| U-006 | V3 | Phase string values (C-013) | Low |
| U-007 | V3 | file:NNN ban unchecked (C-014) | Low |
| U-008 | V3 | git write verbs in classification steps (C-016) | Low |
| U-009 | V1 | PR body and off flag for the opening run have no task (C-017) | Low |
| U-010 | V1 | not_applied ready branch back to RELEASE_PENDING untested (C-018) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Classification | Status |
|---|---|---|---|---|---|
| A-001 | The right yardstick for each criterion is "a wrong implementation would fail it" (spec 366) | all three judge criteria by failability | High | UNSTATED in all three cards | Promoted |
| A-002 | Spec text is correct; plan faults are measured against it even where the spec has its own gaps (e.g. spec 241 internal tension, spec 138 and 199) | V1 and V2 flag spec-origin gaps as plan findings | High | UNSTATED | Promoted |
| A-003 | The merged-requirements FR ids (FR-1..FR-23) are valid, though that document is not in the input | V1 and V2 cite FR ids | Low | STATED by the spec header (line 4) | Not promoted |
| A-004 | The working tree already holds the feature, so grounding cannot check pre-build facts | V2 states it; V1 and V3 silent | Low | STATED in V2 and in the T1 card | Not promoted |

## Summary
- Total structural differences: 3
- Total content differences: 20
- Total contradictions: 5
- Total unique contributions: 10
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-002, C-003, C-010 (High)
- total_diff_points for convergence = S 3 + C 20 + X 5 + A 2 = 30
