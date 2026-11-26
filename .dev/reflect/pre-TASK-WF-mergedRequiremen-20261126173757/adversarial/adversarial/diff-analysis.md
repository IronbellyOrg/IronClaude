# Diff Analysis: reviewer-card comparison (UC-1 pre-execution review of the Run ledger plan)

## Metadata
- Generated: 2026-11-26T17:46:00Z
- Variants compared: 2 (V1 = reviewer 1 card, analyzer, sonnet; V2 = reviewer 2 card, qa, haiku)
- Total differences found: 23 (denominator for convergence: structural 2 + content 15 + contradictions 3 + shared assumptions 3)
- Categories: structural (2), content (15), contradictions (3), unique (5), shared assumptions (3)
- Subject under review (both cards audit the same two files): the plan `.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md` (140 lines) against its spec `.../source.md` (157 lines), same folder.
- Evidence note for line numbers: V1 cites plan lines that are 31 higher than the real file lines (it counted lines inside the brief that embedded the plan); V2 cites real lines. Both are checked by the Wave 5 evidence validator.

## Structural Differences
| # | Area | V1 | V2 | Severity |
|---|------|----|----|----------|
| S-001 | Card shape | 10 findings (F1-F10) in one table, coverage check per row, short | 7 findings (QA-1 to QA-7), coverage check grouped by row sets, candidate-finding disposition, adherence summary; about 2.4 times longer | Low |
| S-002 | Grading vocabulary | `Blocking (Decision)` / `Medium` / `Note` | `Blocking (Safety|Decision|Missing)` / `Note`, each also labelled Drift with HIGH/MEDIUM/LOW | Low |

## Content Differences
| # | Topic | V1 position | V2 position | Severity |
|---|-------|-------------|-------------|----------|
| C-001 | Task 2 check "`ledger.py` does not import `probes.py`" vs Task 3 importing `RUN_ID_RE` | F1 Blocking (Decision) | QA-4 Blocking (Decision) | Medium (both agree) |
| C-002 | Task 8 creates an undeletable scratch Run on the brief's authority; spec line 97 and 151 reserve the go for the owner | F4 Medium (authority is [INFERRED]; the brief was not in its evidence) | QA-1 Blocking (Safety) | High |
| C-003 | Task 1 `hook_entries` rule vs Task 3 `merge_hook_entries` (redundant paths, no dedupe by id) | F2 Medium, confirmed and widened | T1 F1 "not confirmed as a duplicate-row defect"; dedupe correctness unverified | Medium |
| C-004 | Task 8 when the scratch `run-create` cannot be made: which `Decision:` line? | F3 Medium: unspecified; Task 9 branches on it | not raised | Medium |
| C-005 | Task 10 check "every command and flag the doc names exists in `sweep ledger --help`" | F5 Medium | QA-5 Blocking (Decision) | Medium |
| C-006 | Staging of `.dev/tasks` absent from the plan | F8 Note | QA-6 Blocking (Missing) | Medium |
| C-007 | Task 1 stale-age fallback to the Run's `updated_at` instead of the Task's | not raised | QA-2 Blocking (Decision) | Medium |
| C-008 | Task 1 `main_checkout_only` definition ("every matched worktree is main") ignores other admission reasons | not raised | QA-3 Blocking (Decision) | Medium |
| C-009 | Task 6 with a valid ledger whose `runs` list is empty | F6 Medium (unspecified) | not raised | Medium |
| C-010 | Spec line 85 names `commands/sc/sweep.md` but the real file is `commands/sweep.md` | F10 confirms the plan is right | notes the plan uses a different path (INF-035) | Low |
| C-011 | Sweep tests placed in `tests/sweep/`, spec says `tests/run_ledger/` | F10 true and consistent | not raised | Low |
| C-012 | Is the 55-row matrix exhaustive? | not raised | QA-7 Note: it omits schema obligations | Low |
| C-013 | Citation accuracy | plan line numbers offset by +31 (brief-embedded numbering) | real line numbers | Medium |
| C-014 | Coverage verdict on the 10 matcher false negatives | all 10 covered | all covered; INF-020, INF-040, INF-041, INF-051 "not fully adherent" via QA-1/2/3/6 | Medium |
| C-015 | Confidence | self 0.80, calibrated 0.80 | self 0.92, calibrated 0.76 | Low |

## Contradictions
| # | Point of Conflict | V1 | V2 | Impact |
|---|-------------------|----|----|--------|
| X-001 | Is the hook-entry duplicate-row risk real? | F2: real, no named test catches it (plan lines for Task 1 and Task 3) | "Not confirmed ... remains unverified" | Medium |
| X-002 | Grade of the scratch-Run authority gap | Medium | Blocking (Safety) | High |
| X-003 | Grade of the missing staging step | Note | Blocking (Missing) | Medium |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | Task 8 UNVERIFIED branch leaves the `Decision:` line undefined (C-004) | Medium |
| U-002 | V1 | Empty-ledger sweep behavior unspecified (C-009) | Medium |
| U-003 | V1 | Negative checks: `integration` marker registered under `--strict-markers`; `test_readonly.py` patches only `probes.subprocess.run` | Medium |
| U-004 | V2 | Stale-age fallback to the Run's `updated_at` (C-007) | Medium |
| U-005 | V2 | `main_checkout_only` predicate overstated (C-008) | Medium |

## Shared Assumptions
| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | The owner brief (the user's own instruction to test the hook) is not in either reviewer's evidence, yet both grade the scratch-Run authority; authority can be judged from the plan and spec alone | both grade the Task 8 gap | High (the Blocking or Medium grade of C-002 depends on it) | UNSTATED [SHARED-ASSUMPTION] |
| A-002 | The spec snapshot is authoritative even where it is wrong or conflicts with a plan choice the plan justified (path on line 85, `find_orca`, test placement); a plan deviation from the spec is a plan defect | both audit "plan vs spec" | Medium | UNSTATED [SHARED-ASSUMPTION] |
| A-003 | The 55 inferred rows are a sufficient requirement universe for judging coverage | both consume the matrix | Medium | UNSTATED [SHARED-ASSUMPTION] |

## Summary
- Total structural differences: 2
- Total content differences: 15
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 3 (UNSTATED: 3, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-002, X-002, A-001
