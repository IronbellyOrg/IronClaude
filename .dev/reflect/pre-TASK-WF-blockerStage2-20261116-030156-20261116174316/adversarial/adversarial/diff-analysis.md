# Diff Analysis: reviewer-card comparison (stage 2 plan, UC-1)

## Metadata
- Generated: 2026-11-16 (orchestrator, inline analytical step)
- Variants compared: 3 (variant-1 analyzer/sonnet, variant-2 qa/haiku, variant-3 refactorer/opus; each a reviewer card with findings, refuted T1 items, follow-ups, verdict)
- Total differences found: 2 structural, 14 content, 3 contradictions, 5 unique, 3 shared assumptions
- Categories: structural (2), content (14), contradictions (3), unique (5), shared assumptions (3)
- Note: the variants are review cards on the same plan; "approach" below means which findings a card raises and how it grades them. The merge target is one merged finding register.

## Structural Differences
| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Card scope | carrier edits and tests (Tasks 2, 3, 5) | acceptance lines and spec coverage (Tasks 1, 6, 7, 8) | interfaces, tech-research, cross-stage (Tasks 2, 4) | Low | L1 |
| S-002 | Disposition of the earlier single-agent card (T1) | confirms F1, F2, F6; none refuted | refutes F5, F7, parts of F3, F4 | confirms F3, F4, F6; none refuted | Medium | L2 |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | /sc:implement sweep has no ledger to read | blocking R1-1 | absent | follow-up candidate (stage 3 adds --promote to a call with no input) | High | L2 |
| C-002 | GR12 safety row must make a contract `partial` (spec 6.4:438) | blocking R1-2 | says Task 5 meets REQ-12 | absent | High | L3 |
| C-003 | Safety-miss confirmation file holds only run-scoped row ids | absent | blocking R2-1 | absent | High | L3 |
| C-004 | Task 7 agents see only the blind table, so code-supplied inputs cannot reach their answers | absent | blocking R2-2 | absent | High | L3 |
| C-005 | `protected-risk-dispute` tag never written by `write` or `safety` | absent | absent | blocking R3-1 | High | L3 |
| C-006 | tech-research tier mapping and report-table format undefined for `write` | follow-up (rf-qa format fixed) | follow-up (producer to parser fixture) | blocking R3-2 | High | L2 |
| C-007 | rf-analyst reports carry no `rests_on` fields (template not among the five edited) | follow-up (reviewers omitting fields) | absent | blocking R3-3 | High | L2 |
| C-008 | Task 1 entry check narrower than Constraints | absent | follow-up | minor R3-4 | Medium | L2 |
| C-009 | Sweep call must be on its own line for AC3, Task 6 and stage 3 | minor R1-3 | absent | minor R3-5 | Low | L1 |
| C-010 | tech-research has no unattended mode to choose `--unattended` | minor R1-5 | absent | minor R3-7 | Low | L2 |
| C-011 | Printed list has no named producer (sweep prints flagged rows only) | minor R1-4 | absent | absent | Medium | L2 |
| C-012 | Coverage matrix omits requirement-bearing spans | absent | minor R2-3 | absent | Low | L1 |
| C-013 | Constraints say "two more files" mention follow_ups; three will | absent | absent | minor R3-6 | Low | L1 |
| C-014 | `--judge-answers` vs "no subcommand calls a judge" | absent | absent | minor R3-8 | Low | L1 |

## Contradictions
| # | Point of conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Does Task 5 satisfy REQ-12/6.4? | no: GR12 to partial missing | yes: "exactly three keys, incomplete maps to partial" | silent | High |
| X-002 | Is the tech-research report-to-`write` gap blocking? | follow-up only | "every run partial" not established; weakness only | blocking (tier undefined, no format) | High |
| X-003 | Is a short entry check (Task 1) a defect? | silent | follow-up | minor, loud late failure | Medium |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Archive digest and record-file placement; legacy runs have no final review step | Medium |
| U-002 | V2 | Run-scoped ids make Task 8 safety-miss counting ambiguous (C-003) | High |
| U-003 | V2 | Task 7 blind-only input conflicts with the code-supplied-input evaluation (C-004) | High |
| U-004 | V3 | `protected-risk-dispute` tag is never persisted (C-005) | High |
| U-005 | V3 | Edited LEGACY templates vs active Phase 6 reviewers; rf-analyst gap (C-007) | High |

## Shared Assumptions
| A-NNN | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | The plan runs as a managed package under /sc:implement, Tasks 1 to 8 in order, so a failure at Task 4/6/7 occurs after earlier edits | all three cards treat Task 1 entry check and later failures as sequential | UNSTATED | yes |
| A-002 | Stage 1 will deliver functions and files exactly as its plan describes (function names are not pinned there) | all three read stage 1 text as the interface | UNSTATED | yes |
| A-003 | "Blocking" means consequence-graded (cannot be met, wrong or missing result, data loss), not label-graded | all three apply the lead's rule | STATED | no |

## Summary
- Total structural differences: 2
- Total content differences: 14
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 3 (UNSTATED 2, STATED 1, CONTRADICTED 0)
- Highest-severity items: C-001, C-002, C-003, C-004, C-005, C-006, C-007, X-001, X-002
- total_diff_points (denominator) = 2 + 14 + 3 + 2 (promoted A-NNN) = 21
