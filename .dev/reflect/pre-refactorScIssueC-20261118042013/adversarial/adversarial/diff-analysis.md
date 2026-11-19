# Diff Analysis: reviewer-card comparison (reflect UC-1, plan TASK-WF-refactorScIssueC-20261118-041634)

## Metadata
- Generated: 2026-11-18T04:31:00Z
- Variants compared: 3 (variant-1 = reviewer 1 analyzer/sonnet, variant-2 = reviewer 2 qa/haiku, variant-3 = reviewer 3 refactorer/opus)
- Focus: correctness, coverage, deviation-classification
- Total differences found: 15 debate points (structural 2, content 6, contradictions 3, shared assumptions 4) plus 5 unique contributions
- Variant files: adversarial/variant-N-original.md (copies of the cards)

## Structural Differences
| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Verdict | pass-with-findings | fail | pass-with-findings | High |
| S-002 | Severity labels | 3 medium + 2 note, no blocking | 1 blocking + 1 medium | 2 medium + 4 note, no blocking | Medium |

## Content Differences
| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | claim.md:142 launched-agent text is wrong for default full | F2 medium wrong-claim | F1 blocking | F6 note, wording older than the plan | High |
| C-002 | Task 3 relaxes the E-SUBMIT-NEEDS-FULL stop rule (bare --submit runs at full) | F1 medium scope-drift, owner not asked | F2 medium: the test does not protect the new behaviour | F1 medium scope-creep, owner choice needed before Task 3; design record flag.md:85 requires STOP | High |
| C-003 | Ship-gate sentence while full becomes default | F3 medium INFERRED: bare claim now under the stricter gate | not raised | rejected: the sentence names both governed levels, so it stays true | Medium |
| C-004 | Sites that still state the old default or old rule and have no task | F5 note: sc-issue-command.md:238, issue-watcher.md:41 | not raised | F2 medium: docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1557,:1635; F3 note: flag.md:66,:78,:85,:87; F4 note: sc-issue-command.md:238 | Medium |
| C-005 | Worker brief for the coordinator path still starts the simple chain with /sc:brainstorm | not raised | not raised | F5 note, INFERRED: worker-brief.txt:17-19 | Low |
| C-006 | test_launch.py is named in the spec but not edited | F4 note, correct | covered in assessment | assessment: correct, already pinned | Low |

## Contradictions
| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Severity of the claim.md:142 text | medium | blocking (changes the user's next action) | note (predates the plan) | High |
| X-002 | Is the bare --submit relaxation a defect or an acceptable consequence of the new default | scope-drift, ask owner | accepted as written; asks only for a test | scope-creep, narrower edit is to leave the STOP rule | High |
| X-003 | Does the ship-gate need attention | yes (F3) | silent | no (C-2 rejected) | Medium |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 3 | Architecture reference docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1557,:1635 is a missed site | High |
| U-002 | 3 | worker-brief.txt:17-19 keeps brainstorm for simple work on the coordinator path | Medium |
| U-003 | 2 | Missing assertion that a bare --submit is accepted when --pipeline is omitted | Medium |
| U-004 | 1 | The default bare claim now falls under the stricter full-level precondition (U1) | Medium |
| U-005 | 3 | Design-record lines flag.md:66,:78,:85,:87 and sc-issue-command.md:238/:248 | Low |

## Shared Assumptions
| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | all three accept the plan's task order and dependencies | Task order 1,2 then 3,4 then 5,6 then 7,8 then 9,10 is executable as written | STATED (V3) | no |
| A-002 | all three treat the default as a Markdown edit | The default level is resolved only by the model from Markdown text; no code path parses `--pipeline` or supplies a default (orca_worktree.py `--level` is required) | UNSTATED | yes |
| A-003 | all three accept leaving the watcher untouched | The watcher's explicit `--pipeline none` is the only guard that keeps handoff claims off `full`, and tests pin it | STATED (V1, V2, V3 cite test_launch.py) | no |
| A-004 | all three treat the watcher as the only automated caller | No other automated or documented caller issues a bare `/sc:issue --claim N` that would silently become `full` (a grep of src/superclaude finds only the watcher and descriptions of it; docs/, plugins/ and README not searched) | UNSTATED | yes |

## Summary
- Total structural differences: 2
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED 2: A-002, A-004; STATED 2; CONTRADICTED 0)
- Highest-severity items: S-001, C-001, C-002, X-001, X-002
- Taxonomy tags: L1 surface: S-002; L2 structural: S-001, C-001, C-003, C-004, C-005, C-006, X-001, X-003, A-001, A-002, A-003; L3 state-mechanics: C-002, X-002, A-004 (guard and validation-rule signals)
