# Diff Analysis: reviewer-card comparison (UC-1 pre review of the pr-submit merge-guard plan)

## Metadata
- Generated: 2026-11-13
- Variants compared: 3 (variant-1 = reviewer-1 analyzer/sonnet-class card; variant-2 = reviewer-2 qa/haiku-class card; variant-3 = reviewer-3 refactorer/opus-class card)
- Inputs under review: spec `source.md`, plan `TASK-WF-designSpec-20261107-075614.md` (both under `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`)
- Categories: structural (1), content (11), contradictions (3), unique (8), shared assumptions (3)

## Structural Differences
| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Card layout | prose + "candidates not reported" list, 2 findings | deviation table + coverage audit, 3 findings | deviation table + refuted list + notes, 7 findings | Low |

## Content Differences
| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | No task builds the `--read` JSON to `GuardRead` conversion (source.md:88-90, :230; plan Task 3) | F1 MINOR | absent | F1 MAJOR | Medium |
| C-002 | Task 7 criterion 3 requires `_RESOLUTION_SCRIPTS` tests, while adding the script to that list is conditional (plan:108,113) | F2 MINOR | absent | F3 MINOR | Low |
| C-003 | Held guard keeps the earlier cycle's `cycle_id`; resume then releases on the earlier push (source.md:108,139,166) | absent | absent | F2 MAJOR | High |
| C-004 | Source of the per-cycle applied-edit count for release (source.md:107) | absent | absent | F4 MINOR | Low |
| C-005 | Scenario tests run a Task 11 driver, not the SKILL/ref prose (plan:166,129) | declined (no named wrong outcome) | absent | F5 MINOR | Low |
| C-006 | PR-body gate and `--merge-guard off` for the PR-opening run only recorded in Task 1 (source.md:326) | declined (no quote) | absent | F6 MINOR | Low |
| C-007 | Fold returns a dict (`["phase"]`) but decision rules use attribute access (`guard.phase`) (source.md:118-122,187) | absent | absent | F7 MINOR | Low |
| C-008 | Tasks 9 and 12 consume the pre-build record without `Depends on: Task 1` (plan:134-137,179-182; source.md:363) | absent | F1 MINOR | states "dependency lines all complete" | Low |
| C-009 | Task 13 gives flags.md only a row; spec 245 asks both guides for a paragraph | absent | F2 MINOR | absent | Low |
| C-010 | Coverage matrix omits event-payload spans (source.md:184-185) and the dependency rule (:363) | absent | F3 MINOR | absent | Low |
| C-011 | T1 candidates 5 (`guard is None` rows) and 6 (`from __future__` import) | refuted/declined | not examined | refuted | Low |

## Contradictions
| # | Point of Conflict | Variant 1 | Variant 3 | Variant 2 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Severity of the missing `GuardRead` adapter | MINOR (mapping is mechanical) | MAJOR (two unchecked inventions) | not raised | Medium |
| X-002 | Are the plan's dependency declarations complete? | not examined | "Dependency lines checked against spec:363; all complete" | Tasks 9 and 12 omit Task 1 | Low |
| X-003 | Does a test-driver-only scenario suite / unowned PR-body gate name a wrong outcome? | no (declined) | yes (MINOR findings) | not raised | Low |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | 3 | C-003 held-guard stale cycle_id with a concrete crash sequence | High |
| U-002 | 3 | C-007 dict versus attribute access | Medium |
| U-003 | 3 | C-004 applied-edit count source | Medium |
| U-004 | 3 | C-005, C-006 | Low |
| U-005 | 2 | C-008 dependency edges | Low |
| U-006 | 2 | C-009 flags guide paragraph | Low |
| U-007 | 2 | C-010 coverage-matrix completeness, plus per-row check of the 10 unmatched rows | Medium |
| U-008 | 1 | Explicit rows-checked statement and candidate-by-candidate disposition | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The plan is judged against the spec and base-commit e8db2fe6 facts, not against HEAD code that already holds the merged feature | all three cards | High | UNSTATED in variant 2 |
| A-002 | Open live-GitHub gates (G1, G2, G4, G5, G6) are out of scope for a pre-execution review | all three | Medium | STATED in the plan |
| A-003 | The spec's guard state-machine rules (fold, decision tables, resume rows) are themselves correct, so a plan that copies them is correct | all three except variant 3 F2 (state guard condition) | High | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 11
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-003, X-001
- Taxonomy tags: L1 = S-001, C-009; L2 = C-001, C-002, C-004, C-005, C-006, C-007, C-008, C-010, C-011; L3 = C-003, A-003, A-001 is L2
