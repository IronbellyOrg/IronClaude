# Tier 1 reflection card (UC-1, pre-execution)

hypothesis_source: inline-orchestrator (Step 1B and 1C done by the orchestrator, no requirements-analyst agent)
spec: .dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/source.md (157 lines)
tasklist: .dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md (140 lines, 11 tasks, 5 phases)

## Coverage (Step 1B)
- Pass 1 (ID_REGEX): 0 parsed ids in spec and tasklist.
- Pass 2: 55 inferred rows, every one quote-pinned (all 55 quotes re-found in the cited spec lines, 0 dropped).
- Deterministic containment match: 45 of 55 matched (coverage_pct_union 0.8182; coverage_pct null because parsed_total is 0).
- 10 rows came back unmatched by the string rule: INF-006, INF-008, INF-010, INF-016, INF-027, INF-028, INF-032, INF-041, INF-053, INF-054. On a manual read each one is covered by a named task or by the plan's `## Constraints` section (matcher false negatives from word choice); the reviewers must re-check this.
- `coverage_degraded: parsed-sparse` (inferred 55 > parsed 0): table-wide pre-filter, forces Tier 2. S_dev_density 0.1818 (deterministic) and S_domains >= 3 (code, tests, docs and hook script) also point to Tier 2.

## Candidate findings (to be confirmed or refuted by the reviewers)
- F1 Medium: `decide()` in Task 1 takes `hook_entries` and keeps hook-added entries, and Task 3 `merge_hook_entries` also keeps hook entries under the lock. A hook entry newer than `generated_at` cannot exist in the previous ledger when `decide` runs, so Task 1's carry-over rule is redundant with Task 3, and two code paths that both add hook entries risk duplicate ledger rows unless the merge dedupes by Run id. Evidence: plan Task 1 (the sentence on `hook_entries`), plan Task 3 (`merge_hook_entries`), spec lines 51 and 75.
- F2 Note: spec line 85 names `src/superclaude/commands/sc/sweep.md`; the real file is `src/superclaude/commands/sweep.md`. The plan's Task 7 uses the real path, so the plan is right and the spec snapshot is wrong.
- F3 Medium: spec line 97 says the scratch `run-create` "needs the owner's go" and line 151 lists it as an open decision; plan Task 8 runs it on the authority of the brief. The plan says so in one clause; the executor must not read the spec line as a blocker or as a license without that clause.
- F4 Note: the spec lists the sweep-consumption tests under `tests/run_ledger/` (lines 114 and 127); plan Task 6 puts them in `tests/sweep/` because `tests/sweep/conftest.py` already fakes the Orca seams there. The plan does not call this a deviation.
- F5 Note: the spec says use `find_orca` "if its signature fits" (line 27); plan Task 2 decides it does not fit and uses `shutil.which("orca")`, with the reason. Consistent with the spec's condition.

## Self-reported confidence
0.70 (card not calibrated in this run: Tier 2 is forced by the parse-density pre-filter whatever the score, so the Tier 1 calibration could not change the route; the reviewer cards are calibrated blind).
