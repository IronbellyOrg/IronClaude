# Diff Analysis: reflect reviewer-card Comparison

## Metadata

- Generated: 2026-11-13T05:33:00Z
- Variants compared: 3 (variant-1 reviewer-1 analyzer/sonnet; variant-2 reviewer-2 qa/haiku; variant-3 reviewer-3 refactorer/opus)
- Total differences found: 22 (structural 2, content 9, contradictions 1, unique 7, promoted shared assumptions 3; unique items overlap content rows C-001, C-006 to C-009)
- Total diff points for convergence: S 2 + C 9 + X 1 + A 3 = 15
- Categories: structural (2), content (9), contradictions (1), unique (7), shared assumptions (4)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card layout (L1) | Summary, Findings (F1-F3), "Rows verified" list, findings block | Summary, numbered findings, "Verified rows", "Not checked", findings block | Summary, Findings (F1-F6), "Rows checked and found sound", findings block, "Not checked" after block | Low |
| S-002 | Category labels (L1) | 2 specific categories (unpassable-check, contradiction) + 1 missing-requirement | 3 missing-requirement, 1 unpassable-check, 1 other | 3 of 6 findings labelled `other` | Low |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|-------|--------------------|--------------------|--------------------|----------|
| C-001 | resume_decision row 4 cannot call release_decision (L3) | F1 MAJOR: inputs missing; vacuous head check passes; proposes a "re-enter" action or extra inputs | not raised | F1 MAJOR: same defect; names concrete sources (guard.cycle_id, push record or push_completed target_sha, applied_edits >= 1) and a failing test | High |
| C-002 | Wave 0 bullet (L2) | F2 MAJOR: spec/plan require both "no L3 condition" and an L3 off-print; Task 9 test cannot pass | not raised | F2 MINOR: bullet only placed "before Wave 1"; must follow the head-binding bullet | Medium |
| C-003 | git write verbs in classification wording (L2) | not raised | F5 MINOR | F6 MINOR | Low |
| C-004 | Task 1 dependency declarations (L2) | not raised | F4 MINOR | F5 MINOR | Low |
| C-005 | Same-file task ordering (L2) | not raised | not raised | F4 MINOR: Tasks 5/7 and 9/10/12 | Medium |
| C-006 | guard_status halt reason (L3: guard) | F3 MINOR | not raised | not raised | Low |
| C-007 | cycle_id sharing between guard, push triad and rereview (L3: state) | not raised | F1 MAJOR | not raised | High |
| C-008 | FR-16 release retry and bound (L3: transition) | not raised | F2 MAJOR | not raised | Medium |
| C-009 | Whole-line classification pin of SKILL.md Wave bullets (L2) | not raised | not raised | F3 MINOR | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Whether missing `Depends on: Task 1` lines matter | V2 F4: "Ordering still holds transitively through Task 8" (MINOR) | V3 F4/F5: unordered same-file edits and implied dependencies "could produce conflicting edits" (MINOR) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V3 | Names the sources for the release inputs in resume (guard.cycle_id, record or push_completed target_sha) | High |
| U-002 | V2 | Cycle-id equality has no mechanical check; held_cycle_published matches on it | High |
| U-003 | V2 | FR-16 one-retry bound has no decision row and no test body | Medium |
| U-004 | V2 | Crash-before/after-each-request-and-settle coverage narrower than spec section 7 | Low |
| U-005 | V3 | Whole Wave 6 line is a WRITE_VERB_CLASSIFICATION key; append makes entry stale | Medium |
| U-006 | V3 | Unordered edits of test_static_grep.py and test_merge_guard_protocol.py | Medium |
| U-007 | V1 | guard_status takes no halt reason although spec maps `draft_guard_unavailable` | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | Every plan defect found is non-blocking (blocking:false on all 14 findings) because a wrong implementation would surface later as a failing test | All variants set blocking false | High: severity calibration | UNSTATED (promoted) |
| A-002 | The spec text is itself correct wherever the plan copies it faithfully (defects are attributed to plan wording, not spec design), although C-001 and C-002 originate in the spec | V1, V3 trace C-001/C-002 to spec lines; none recommends a spec change | Medium | UNSTATED (promoted) |
| A-003 | The repository base commit e8db2fe66 copy is the right evidence (stated in the briefs) | All variants cite base paths | Low | STATED |
| A-004 | The plan's acceptance commands (make, uv run pytest) are runnable in the executor's environment as written | None checks it | Medium | UNSTATED (promoted) |

## Summary

- Total structural differences: 2
- Total content differences: 9
- Total contradictions: 1
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-007
