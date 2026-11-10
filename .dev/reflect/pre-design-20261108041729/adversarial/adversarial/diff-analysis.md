# Diff Analysis: reviewer-card comparison (reflect Tier 2, UC-1 pre)

## Metadata
- Generated: 2026-11-08T04:26:00Z
- Variants compared: 3 (variant-1 = reviewer 1 sonnet/analyzer, variant-2 = reviewer 2 haiku/qa, variant-3 = reviewer 3 opus/refactorer)
- Subject of all variants: the plan `TASK-WF-design-20261108-041415.md` against its design `source.md`
- Total differences found: 17
- Categories: structural (2), content (10), contradictions (1), unique (4), shared assumptions (4, of which 2 promoted)
- Focus: correctness, coverage, deviation-classification

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Card shape | 7 findings + ok-check finding + 4 checks_done | 4 findings + 10 checks_done | 7 findings + 4 checks_done | Low |
| S-002 | Citation form | repo `file:line` | plan and design `file:line` plus repo test lines | repo `file:line` | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| C-001 | `tests/skills/test_worker_contract.py` exact-line classification table breaks when Tasks 2, 3, 5 rewrite `gh api` lines | blocking (R1-F1) | not raised | blocking (R3-F1) | High |
| C-002 | Strength of Task 8's new tests (exact output formats, Q7 and Q8 pairs; `orgs/` regex) | regex only, minor (R1-F4); "revert Tasks 1-5 turns a test red" is false for Task 4, minor (R1-F6) | two blocking: prefix checks instead of exact formats (R2-F1), names present instead of Q7/Q8 rules (R2-F2) | regex and spelling, minor (R3-F6) | High |
| C-003 | Plan's test runs miss `tests/commands/test_issue_command.py` and `tests/skills/test_issue_worker_agents.py` | minor (R1-F2) | says Task 6 `-k command` selects existing tests; not raised as a gap | minor (R3-F2) | Medium |
| C-004 | `complexity-field.json` has no template and is not in the Outputs row or the "every file starts from a template" rule | minor (R1-F3) | not raised | minor (R3-F3) | Medium |
| C-005 | Constraint "writes exactly two things" vs mode label and pushback comment | minor (R1-F5) | minor (R2-F4, comment only) | not raised | Low |
| C-006 | `create.md:34,36` wording and the flags row left stale | minor (R1-F6) | not raised | minor (R3-F4) | Low |
| C-007 | Task 10 omits `docs/designs/sc-issue-command.md` lines 34, 330, 331 | not raised | not raised | minor (R3-F5) | Medium |
| C-008 | `SKILL.md:107` "Print this block last" and the narrowed meaning of `labels_*` | not raised | not raised | minor (R3-F7) | Low |
| C-009 | The Will / Will Not test never reads the command file, so Task 7's "keep unchanged" proves no agreement | OK (R1 check) | minor (R2-F3) | not raised | Low |
| C-010 | Reliability of the coverage matrix's per-row task ids | minor note (R1-F7) | not raised | agrees INF-005/006/025 spread over Tasks 2, 3, 5 | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is the new test set able to catch a revert of the earlier tasks? | R1-F6: reverting any of Tasks 1-5 would not turn a new test red for the flags row or review wording (partial) | R2-F1/F2: Task 8 tests are too weak to fail on broken content | Task 8 test 5 asserts the scout headings Task 4 adds (implied by R3 not flagging) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 2 | Exact-format and Q7/Q8 assertion strength in Task 8 (R2-F1, R2-F2) | High |
| U-002 | 3 | Doc lines 34, 330, 331 missing from Task 10 (R3-F5) | Medium |
| U-003 | 3 | Return-contract wording at `SKILL.md:107` (R3-F7) | Low |
| U-004 | 1 | Prose-vs-path ambiguity in the `orgs/` scanner, with a self-check test design (R1-F4) | Medium |

## Shared Assumptions

| # | Agreement source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | C-001, C-003 | CI runs the whole `tests/` tree, so unrun test files are a real risk | STATED (R1 names `make test`, CI) | No |
| A-002 | All variants cite plan and repo line numbers | The live files do not change between this review and execution, so the cited lines still hold | UNSTATED | Yes |
| A-003 | No variant raised lint | `make lint` (lint-architecture) accepts the planned wording and frontmatter changes | UNSTATED | Yes |
| A-004 | All variants leave GitHub behaviour to the plan | The GitHub `--type` flag, POST body and silent-drop behaviour work as documented | STATED (plan marks it UNVERIFIED) | No |

Promoted shared-assumption diff points: A-002, A-003.

## Taxonomy tags (AD-5)

| Point | Level |
|---|---|
| S-001, S-002, C-005, C-006, C-008 | L1 (wording / formatting) |
| C-001, C-003, C-004, C-007, C-010, X-001, A-003 | L2 (structural default) |
| C-002, C-009, A-002 | L3 (guard conditions / state) |

## Summary
- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 1
- Total unique contributions: 4
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002
- total_diff_points for convergence: 2 + 10 + 1 + 2 = 15
