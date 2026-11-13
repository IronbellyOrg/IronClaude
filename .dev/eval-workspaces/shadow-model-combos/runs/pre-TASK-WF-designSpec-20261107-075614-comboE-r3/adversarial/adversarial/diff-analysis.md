# Diff Analysis: reflect reviewer-card Comparison (UC-1 pre, plan vs spec for the pr-submit merge guard)

## Metadata
- Generated: 2026-11-13T05:30:00Z
- Variants compared: 3 (variant-1 = reviewer-1 analyzer card, 14 findings; variant-2 = reviewer-2 qa card, 3 findings; variant-3 = reviewer-3 refactorer card, 2 findings)
- Total differences found: 18 (structural 2, content 11, contradictions 3, unique 0 listed separately, shared assumptions 2)
- Categories: structural (2), content (11), contradictions (3), unique (see content rows marked unique), shared assumptions (2)
- Focus: correctness, coverage, deviation-classification
- Taxonomy tags: L1 surface / L2 structural / L3 state-mechanics (auto-tagged by signal terms, highest level wins)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|------|-----------|-----------|-----------|----------|-------|
| S-001 | Finding volume and depth | 14 findings (6 blocking MAJOR, 8 MINOR), 3 to 5 citations each | 3 findings, all MINOR non-blocking | 2 findings, MINOR non-blocking | Medium | L1 |
| S-002 | Citation hygiene | All lines inside the real files; refs partly spec section numbers ("4.1") | Two citations wrong (garbled path in F1, plan 517-518 in F2); refs empty | Lines correct after one re-ask | Low | L1 |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|-------|-----------|-----------|-----------|----------|-------|
| C-001 | Cycle-id continuity (spec 4.6; plan Task 8 prose vs AC) | F1 MAJOR blocking: AC names only the mint place; trace AC checks order not id equality | not raised | F1 MINOR: same gap, AC checks only where the id is minted | High | L2 |
| C-002 | Resume row 4 and RETRY_RELEASE need release_decision inputs (target_sha, applied_edits) the signature lacks (unique to V1: F2, F13) | MAJOR blocking x2 | not raised | not raised | High | L3 |
| C-003 | `not_applied` of a ready request restores `RELEASE_PENDING` (spec 4.2); Task 3 AC tests only `HELD`; no row sets `phase_before_request` (unique to V1: F3) | MAJOR blocking | not raised | not raised | High | L3 |
| C-004 | Owner of the request key `a<k>` count and of the `--read` JSON to `GuardRead` mapping; script JSON to settle outcome mapping (unique to V1: F4, F6) | MAJOR blocking (F4), MINOR (F6) | not raised | not raised | Medium | L2 |
| C-005 | Wave 0 promise "unsettled requests are reconciled before any edit" vs resume row 2 `REPORT_HELD` at ordinal < 3 or mode off (unique to V1: F5) | MAJOR blocking, category contradiction | not raised | not raised | Medium | L3 |
| C-006 | CI-fix cycle engage trigger has no severity (unique to V1: F7) | MAJOR blocking | not raised | not raised | Medium | L2 |
| C-007 | Task 11 gates three named tests by name only (no release-failure, unreadable-timeline, moved-head assertions) | not raised | F1 MINOR | not raised | Medium | L2 |
| C-008 | Task 7 AC lists `autoMergeRequest` but not its type | not raised | F2 MINOR (unpassable-check) | not raised | Low | L2 |
| C-009 | Constraint "no `file:NNN` pointers" has no AC in Task 8 | not raised | F3 MINOR | not raised | Low | L1 |
| C-010 | `_RESOLUTION_SCRIPTS` entry conditional in prose, assumed in AC (Task 7) | not raised | not raised | F2 MINOR | Low | L2 |
| C-011 | Small spec-level gaps (unique to V1): fold `cycle_id` has no effect row (F9), Phase string values undefined (F10), Wave 6 pre-push OPEN check has no function (F11), L2 line condition (F12), timeline failure exit/ok value (F14), unsettled check at engage (F8) | 6 MINOR | not raised | not raised | Low | L3 |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 3 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------------------|--------|
| X-001 | Severity and blocking status of the cycle-id continuity gap | MAJOR, blocking (source.md:251; plan:127) | MINOR, non-blocking (same citations) | silent | High |
| X-002 | Whether the plan states the reuse of one id for the push triad and `rereview_requested` | F1 says the AC only requires naming the mint place (and itself quotes plan:124 "reuses it as the `cycle_id`...") | F1 says the prose at plan:124 states the reuse but the AC does not check it | silent | Medium |
| X-003 | Overall verdict: any blocking defect at plan scope | six blocking findings (F1, F2, F3, F4, F5, F7, F13 counted as blocking) | none; "covers the reviewed requirements" | none | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Interface hole in resume row 4 and RETRY_RELEASE (C-002) | High |
| U-002 | V1 | Fold restore path for a ready `not_applied` and missing `phase_before_request` rule (C-003) | Medium |
| U-003 | V2 | Task 11 names-only gating of three scenario tests (C-007) | Medium |
| U-004 | V2 | `autoMergeRequest` type not pinned by AC (C-008) | Low |
| U-005 | V3 | `_RESOLUTION_SCRIPTS` conditional vs AC (C-010) | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | A plan acceptance criterion that names no assertion for a behaviour the task prose states is a defect (MINOR unless a wrong outcome follows), even when the prose itself covers the behaviour | All three cards file at least one "AC weaker than prose" finding | Medium | UNSTATED (promoted) |
| A-002 | The audit is a plan-text audit: spec facts F1-F13 hold at parent 0e486ab8d, and HEAD code is not evidence (stated in every brief) | All three cards | Medium | STATED (not promoted) |
| A-003 | The pure decision tables of spec 4.1 are complete enough that "a literal implementer" can build them from the plan alone | V1 attacks it (C-002, C-003), V2 and V3 rely on it | High | UNSTATED (promoted, tagged L3: state, guard, transition terms) |

## Summary
- Total structural differences: 2
- Total content differences: 11
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 3 (UNSTATED: 2 promoted as A-001 and A-003, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, X-001, X-003, A-003
- total_diff_points for convergence = 2 + 11 + 3 + 2 promoted = 18
