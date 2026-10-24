# QA Report - Specification Review - Coverage and Fidelity

**Topic:** sc:recommend routing refresh  
**Date:** 2026-10-24  
**Phase:** Independent specification review  
**Lens:** coverage-and-fidelity  
**Fix cycle:** 1  
**fix_authorization:** false  
**Intended report destination:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/reviews/coverage-and-fidelity-1.md`

## Overall Verdict: FAIL

Command inventory coverage is complete. Specialist regression coverage is not: several appendix rows reference tests that do not exercise their claimed command outcomes.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Research snapshot and date window | PASS | HEAD is `77288289`; history queried using the inventory window. |
| 2 | Historical command set matches inventory | PASS | Mechanical comparison: 47 historical command identities, 47 inventory identities, no differences. |
| 3 | Registered analyst report coverage | PASS | Exactly 47 matching report filenames; no missing or extra command reports. |
| 4 | Active and retired counts | PASS | 43 current command files; four retired identities: estimate, sc, select-tool, task-mcp. |
| 5 | Consolidated appendix coverage and links | PASS | Exactly 47 unique command rows; all 47 analyst-report links resolve. |
| 6 | Formatting-only histories retained | PASS | Historical formatting commit covers commands whose only scoped updates were formatting; appendix distinguishes formatting from substantive changes. |
| 7 | Report sections and unfinished scaffolding | PASS | All 47 reports contain Findings, Gaps and Key Takeaways. Mechanical sentinel scan found no unfinished placeholder markers. |
| 8 | Research-only source boundary | PASS | `git diff HEAD --name-only -- src plugins tests` returned no paths. |
| 9 | Current contracts distinguished from desired policy | PASS | Specification separates existing behavior, desired workflow-first policy, contradictions and unverified dependencies. |
| 10 | Safety, mutation and output distinctions | PASS | Examined implementation planning, review posting, audit reports, specialized evaluation execution, release artifacts and memory-operation boundaries. These are contract inspections, not runtime results. |
| 11 | Sample proposed interfaces grounded in live sources | PASS | Inspected workflow, reflect, Auggie review, cleanup-audit, cli-eval and release-split contracts. |
| 12 | Future tests distinguished from executed results | PASS | Section 8 explicitly labels cases proposed and prohibits executing recommended commands during routing evaluation. |
| 13 | Specialist regression mappings exercise accepted findings | FAIL | Finding CF-01 below. |
| 14 | Exhaustive semantic verification of every assertion and proposal across all reports | UNCHECKED | Mechanical checks covered all reports; independent semantic examination was selective, not a complete assertion-by-assertion audit of all 47 reports. |

## Summary

- Checks passed: **12/14**
- Checks failed: **1**
- Checks unchecked: **1**
- Critical issues: **0**
- Important issues: **1**
- Issues fixed in-place: **N/A**

## Issues Found

### CF-01: Specialist routing regressions are missing despite claimed test mappings

**Severity:** IMPORTANT

**Primary location:**  
`/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/SPEC-sc-recommend-refresh.md:675-687`

**Traceability locations:**  
The same specification, lines **867-869**, **888**, **897** and **905**.

Appendix C claims specialist regression coverage through test identifiers whose definitions concern different outcomes:

| Command | Claimed tests | Actual test descriptions | Missing specialist verification |
|---|---|---|---|
| cleanup-audit | T14-T18/T74 | Help inventory, business/spec critique, localization, recommendation self-loop, unsupported metrics | Audit-only selection; no cleanup/commit appended; requested pass/focus preserved; excluded audit targets disclosed. |
| cli-eval | T20/T21 | Within the generic build/tasklist/mode grouping | Distinct create/run selection; suite/eval selector preservation; ambiguity clarification; real-run side effects. |
| release-split | T20/T22 | Same generic grouping | Standalone split assessment; intact-release outcome; validated-proposal continuation. |
| swarm-wizard | T20/T22/T45/T74 | Generic grouping, contract disagreement and unsupported claims | Explicit swarm/settings-help selection versus ordinary spec review or explanation. |
| validate-tests | T20/T42/T74 | Generic grouping, activation verification and unsupported claims | YAML tier-validation selection versus application testing; missing-suite handling. |

The integration matrix contains general verification/cache scenarios, not these missing command-selection cases. The behavioral matrix covers some other specialist families, but does not supply the omitted cleanup-audit, cli-eval, release-split, swarm-wizard or tier-validator scenarios.

The analyst reports explicitly proposed concrete regressions that would close this gap:

- `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/cleanup-audit.md:63-69`
- `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/cli-eval.md:73-80`

**Failure scenario:** An implementation can satisfy the currently enumerated tests while still routing “find dead code, report only” into cleanup or routing cliEval suite creation into generic implementation planning. The appendix would nevertheless appear to show regression coverage.

**Required fix:** Add explicit, uniquely identified positive and negative recommendation cases for each accepted specialist route. Map each affected appendix row to tests that actually exercise its outcome, preserved inputs and authorization boundary. Reuse shared availability/cache tests where appropriate, but do not substitute those for command-selection tests.

## Actions Taken

No fixes authorized this round; findings reported only.

No specification, analyst report, command implementation or test source was edited. No commands under review, regression suites, sync operations, Git mutations or network publication were executed.

## Recommendations

Repair CF-01 before approving the specification. Review every Appendix C test mapping against its actual Section 8 case, then add missing specialist cases without executing their target commands.

## Self-Audit

**(a) Reliance list**

- No other reviewer's PASS verdict was inherited.
- Analyst reports were treated as claims to check, not independent proof.
- Mechanical completeness was not treated as semantic completeness.

**(b) Independent falsification attempts**

- Tried to find a historical command omitted from inventory or analyst coverage: none found.
- Tried to find duplicate appendix rows, missing report links or missing current/retired identities: none found.
- Tried to find source implementation changes hidden among research artifacts: none found.
- Tried to find unfinished scaffold markers or future tests represented as executed: none found.
- Tried to falsify claimed regression coverage by following appendix test IDs back to their definitions: CF-01 confirmed.
- Checked 763 literal absolute analyst citations mechanically. Five missing current paths refer to explicitly retired command identities. Four apparent final-line overruns were trailing-newline indexing differences and were not promoted into findings.
- Did not independently verify every historical patch, aliased citation, delegated reference and semantic assertion across all 47 reports. That remains unchecked, not implicitly passed.

## Confidence Gate

- **Confidence:** “Verified: 13/14 | Unverifiable: 0 | Unchecked: 1 | Confidence: 92.86%”
- **Calculation:** `13 / (14 - 0) × 100 = 92.86%`. Verified includes the independently confirmed failed check; this is not a specification quality score.
- **Tool engagement:** “Read: 25 | Grep: 0 | Glob: 0 | Bash: 8”
- **Executed implementation/regression tests:** 0.

**Unchecked items**

- Exhaustive assertion-by-assertion semantic fidelity and individual-proposal disposition verification across all 47 analyst reports. Mechanical coverage and selected semantic verification were completed instead.

**Unverifiable items**

- None within the completed static checks.

## QA Complete

VERDICT: FAIL