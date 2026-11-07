# Diff Analysis: reviewer-card comparison (plan TASK-WF-planTheRealBound-20261107-080351)

## Metadata
- Generated: 2026-11-07
- Variants compared: 3 (variant-1 = reviewer 1 analyzer/sonnet, variant-2 = reviewer 2 qa/haiku, variant-3 = reviewer 3 refactorer/opus)
- Calibrated confidence of each card: V1 0.79, V2 0.70, V3 0.81
- Total differences found: structural 3, content 18, contradictions 3, unique 8, shared assumptions 3
- Categories: structural (3), content (18), contradictions (3), unique (8), shared assumptions (3)

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Finding id scheme and count | R1-01..12 (12) | QA-1..6 (6) | R3-F1..13 (13) | Low |
| S-002 | Card sections | `verified_true_claims` block then findings | findings only | findings only | Low |
| S-003 | Finding `type` vocabulary | infeasible-task, coverage-gap, other | contradiction, fabricable-evidence, other | missed-requirement, ordering, boundary, scope-creep, other | Medium (none uses the 4-class deviation taxonomy) |

## Content Differences
| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | PASS unreachable by construction (Task 5 controlled vs Task 8 observed-only) | R1-04 medium | QA-1 medium | R3-F1 high | High (all agree on substance; severity differs) |
| C-002 | Old governed child cannot outlive the first process (supervisor waits for descendants) | R1-03 medium (reaping) and R1-01 high (Task 4) | QA-3 high (evidence can be faked) | R3-F4 medium | High |
| C-003 | Task 7 ordering/data source | R1-05 (no depth data, depends on Task 5 only) | QA-6 (tree coverage) | R3-F2 (ordering only) | Medium |
| C-004 | Task 7 exhaustion branch is dead; bound belongs to historical probe | R1-06 medium | - | R3-F9 low | Medium |
| C-005 | Task 5 boot-identity branch is dead; merged helper compares boot at :234 | R1-07 low | - | R3-F10 low | Low |
| C-006 | Twelve-run budget unallocated | R1-08 medium | QA-2 (extra launch) | R3-F12 low | Medium |
| C-007 | Task 4 "ordinary" call is itself governed | - | QA-2 medium | R3-F11 low | Low |
| C-008 | Task 4 reparent shape cannot be observed from a later call (supervisor drains first) | R1-01 high | - | - | High |
| C-009 | Unavailable branch missing in Tasks 2 and 7 | - | QA-4 medium | - | Medium |
| C-010 | Selector results not linked to captured output | - | QA-5 medium | - | Medium |
| C-011 | Resume/fork needs session persistence; live_probe disables it | R1-02 medium | - | - | Medium |
| C-012 | Subagent/Monitor runs need the tools offered | R1-09 medium | - | - | Medium |
| C-013 | Task 6 governed pusher and "human" shell labelling | R1-10 low | - | R3-F7 medium | Medium |
| C-014 | No baseline for "git status unchanged"; blocked package already modified | R1-11 low | - | R3-F6 medium | Medium |
| C-015 | Orphan/setsid cleanup mechanism | R1-12 low | - | - | Low |
| C-016 | Global-settings checksum only checked once | - | - | R3-F5 medium | Medium |
| C-017 | Task 8 case list omits launch wrapper, hook/Git trees, auto mode, decisive row | - | QA-6 medium | R3-F3 medium | Medium |
| C-018 | Tasks 5 and 6 repeat existing controlled tests | - | - | R3-F8 low | Low |

## Contradictions
| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|---|---|---|---|---|
| X-001 | Severity of the PASS-unreachable defect | medium (R1-04) | medium (QA-1) | high (R3-F1) | Medium (same finding, different severity) |
| X-002 | Whether Task 3's decisive-case criteria are already adequate | R1-03: the survival check is missing, criteria not otherwise challenged | QA-3 (high): criteria can be met by two sequential snapshots | R3-F4: how the child stays alive is unspecified | Medium (plan line 59 already says the child "stays alive while" the new session starts; the calibrator noted QA-3 overstates the wording gap) |
| X-003 | What Task 4's second call is | R1-01: a later call finds the descendant dead | QA-2: a later call is governed, not ordinary | R3-F11: same as QA-2, wording only | Medium (R1 attacks feasibility, QA/R3 attack labelling; both can hold) |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | Resume/fork needs persistence flags (R1-02) | High (it would make resume unavailable by the plan's own doing) |
| U-002 | V1 | Subagent/Monitor tool list (R1-09) | High |
| U-003 | V1 | Orphan cleanup sweep (R1-12) | Low |
| U-004 | V2 | Selector-output linkage (QA-5) | High |
| U-005 | V2 | Unavailable branch missing (QA-4) | High |
| U-006 | V3 | Settings checksum per run (R3-F5) | Medium |
| U-007 | V3 | Existing controlled tests already cover Tasks 5/6 (R3-F8) | Medium |
| U-008 | V3 | Controlled closure does not count toward PASS (R3-F13) | Medium |

## Shared Assumptions
| # | Assumption | Source Agreement | Classification | Promoted | Impact |
|---|---|---|---|---|---|
| A-001 | A prompt-driven `claude --print` run reliably executes the exact Bash command requested, so a captured selector line is produced | All variants assume Tasks 2-4 yield one selector line per run | UNSTATED | Yes | High (a non-literal run silently loses the observation) |
| A-002 | The executor can start a nested real Claude run from inside a Claude session with working authentication in the throwaway HOME | V1 notes it; V2 QA-4 depends on it; V3 R3-F12 counts runs | STATED (V1 notes, QA-4) | No | High |
| A-003 | The merged helper's behavior in design 19.7 is the specification the plan observes against (so "closed by" judgments in Task 8 refer to the merged selector, not the historical probe) | V1 R1-06/07 and V3 R3-F9/F10 agree | STATED | No | Medium |

## Summary
- Total structural differences: 3
- Total content differences: 18
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 3 (UNSTATED: 1, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-008
