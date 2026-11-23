# Diff Analysis: reviewer card comparison (UC-1 audit of the executeNowBrief plan)
## Metadata
- Variants compared: 3 (variant-1 analyzer/sonnet, variant-2 qa/haiku, variant-3 refactorer/opus)
- Focus: correctness, coverage, deviation-classification
- Categories: structural (2), content (12), contradictions (3), unique (5), shared assumptions (3)

## Structural Differences
| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Finding record shape | one block per finding, 9 findings, "Checked, no defect" paragraph | two findings plus a Notes paragraph and an adherence summary | 11 findings, same record shape as variant 1 | Low |
| S-002 | Scope covered | Tasks 1-7 plus whole package | constraints, package acceptance, Tasks 10-12 only; says Tasks 1-9 not audited | Tasks 8, 9 and plan structure, plus confirmation of T1 findings | Medium |

## Content Differences
| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Task 4 acceptance grep cannot pass (test names contain closure_evidence, never_read) | F1 blocking | not covered | not covered | High |
| C-002 | Task 5 acceptance grep cannot pass (renamed test contains question_fixture; hyphen code does not match) | F2 blocking | not covered | F1 blocking | High |
| C-003 | Whole-package acceptance (source.md:49-53) dropped | F3: three checks, non-blocking | F1, F2: run-use and git status, blocking; INF-021 covered | F2: run-use and git status, non-blocking; count survives via gate | Medium |
| C-004 | commands.py:177-178 shifts after Task 4 | F4 | not covered | F7 (adds: Task 12 has no dependency on Task 4 or 10) | Medium |
| C-005 | Orphan comments terminal.py:41 and collector.py:102 | F5, F6 (also docstring :131) | not covered | F8, F9 | Low |
| C-006 | test_snapshot_schema.py:1 docstring after Task 12 | F7 (false) | not covered | F10 (arguably still true) | Low |
| C-007 | Task 8 import instructions | F8: drops snapshot_json | not covered | F3: also unused resources import, isort | Low |
| C-008 | Task 3 helper needs apply_frozen import | F9 | not covered | not covered | Low |
| C-009 | Golden scan test names after Task 9 T7 cut | not covered | not covered | F5 | Low |
| C-010 | Stale line numbers in Tasks 6, 8, 9 after Task 3 | not covered | not covered | F6 | Low |
| C-011 | ARCHITECTURE-SPINE.md:142 stale after Task 8 | not covered | not covered | F4 (noted only) | Low |
| C-012 | Label collision T5/T7/T8/T9 (rows vs spec tests) | not adopted | not covered | F11 | Low |

## Contradictions
| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is INF-021 (final count) a dropped requirement? | part of F3: final count never stated | "not a separate dropped requirement": per-task gate covers it | count survives through the gate | Medium |
| X-002 | Is the dropped package acceptance blocking? | blocking=false | blocking=true | blocking=false | Medium |
| X-003 | Does plan:65 forbid renaming the Task 4 test? | F1: it does not forbid a rename (refines T1 card) | n/a | n/a | Low |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | C-001 Task 4 grep finding | High |
| U-002 | 1 | C-008 apply_frozen import | Low |
| U-003 | 3 | C-009 golden test names | Low |
| U-004 | 3 | C-011 spine drift and Task 12 ordering | Medium |
| U-005 | 2 | Owner pass record, owner decisions and Tasks 10-12 targets checked and found accurate | Medium |

## Shared Assumptions
| # | Agreement source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | all variants confirm the 9-case and 684 arithmetic | the 694 baseline and Task 9's len(overflow) == 1 hold, though no one ran tests | UNSTATED | yes |
| A-002 | all variants flag grep criteria | an executor reads grep criteria literally, not as identifier searches | UNSTATED | yes |
| A-003 | all variants treat line numbers as leads | the plan's re-grep constraint (plan:22) makes shifted line numbers harmless | STATED | no |

## Summary
- Structural 2, content 12, contradictions 3, unique 5, shared assumptions 3 (UNSTATED 2, STATED 1, CONTRADICTED 0)
- Highest severity: C-001, C-002
- Debate diff points: S 2 + C 12 + X 3 + A 2 promoted = 19
