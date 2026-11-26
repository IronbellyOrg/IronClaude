# Diff Analysis: reviewer-card comparison (second review, regenerated Run ledger plan)

## Metadata
- Generated: 2026-11-26T18:20:00Z
- Variants compared: 2 (V1 = reviewer 1, analyzer, sonnet; V2 = reviewer 2, qa, haiku)
- Total differences found: 13 (convergence denominator: structural 1 + content 7 + contradictions 1 + shared assumptions 2 = 11; unique 3 not counted)
- Categories: structural (1), content (7), contradictions (1), unique (3), shared assumptions (2)
- Subject: plan /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md against its spec source.md in the same folder. Both cards cite real line numbers.
- Depth: quick, by the circuit breaker of the adversarial skill (standard reduced to quick): the cards agree on five of six prior blockers and differ on one; the first review already ran the full standard pipeline on the same material.

## Structural Differences
| # | Area | V1 | V2 | Severity |
|---|------|----|----|----------|
| S-001 | Card shape | short: verdict, prior blockers, 6 findings, coverage list | long: verdict, prior blockers, 1 finding, grouped coverage table with an adherence summary | Low |

## Content Differences
| # | Topic | V1 | V2 | Severity |
|---|-------|----|----|----------|
| C-001 | Prior blocker B-6 (time parsing): resolved? | open (partial): only `decide` is required to parse times; Task 2 guard 4, Task 3 merge and Task 6 stale test do not say so | resolved: Task 1 states that every time comparison parses through `parse_time` and a mixed-form test exists | High |
| C-002 | Prior blockers B-1 to B-5 | all resolved, with citations | all resolved, with citations | Low (agree) |
| C-003 | Import-allowlist test could miss relative imports (`from .probes import X`) | F2 Medium | not raised | Medium |
| C-004 | Exact hint text for the two exact-match tests is left to the implementer | F3 Medium | not raised | Medium |
| C-005 | Wording notes: fake-runner access in Task 4 (F4), report file not in the artifacts list (F5), `fcntl` import at module top (F6) | Notes | not raised | Low |
| C-006 | Is the 69-row matrix exhaustive? | not raised | N-1 Note: it is an index, not an inventory | Low |
| C-007 | Verdict | FAIL (1 Blocking) | PASS with notes | High |

## Contradictions
| # | Point of Conflict | V1 | V2 | Impact |
|---|-------------------|----|----|--------|
| X-001 | Does the plan require `parse_time` in every time comparison? | No: only inside `decide` (plan lines 30 and 33); Tasks 2, 3 and 6 are silent (plan lines 40, 50, 82) | Yes: "every time comparison parses both sides into UTC datetimes" | High |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | F2 import-test relative-import gap | Medium |
| U-002 | V1 | F3 hint text not pinned | Medium |
| U-003 | V2 | N-1 matrix completeness | Low |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | A general sentence inside Task 1 about "every comparison" governs other tasks' code | V2 relies on it; V1 treats it as local to `decide` | High | UNSTATED [SHARED-ASSUMPTION] |
| A-002 | The first review's findings are the complete list of what could still be wrong | both check B-1 to B-6 first | Medium | UNSTATED [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 1
- Total content differences: 7
- Total contradictions: 1
- Total unique contributions: 3
- Total shared assumptions surfaced: 2 (UNSTATED: 2)
- Highest-severity items: C-001, C-007, X-001, A-001
