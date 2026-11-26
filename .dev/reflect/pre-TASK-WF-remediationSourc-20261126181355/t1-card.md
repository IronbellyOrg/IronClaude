# Tier 1 card (UC-1, second review, regenerated package)

hypothesis_source: inline-orchestrator
## Coverage
- Pass 1 ids: 0. Pass 2 inferred rows: 69 (55 from the earlier spec text plus 14 from the appended Reflect Verdict State section); all quotes re-found in the cited lines, 0 dropped.
- Deterministic containment match: 60 of 69 (coverage_pct_union 0.8696; coverage_pct null); S_dev_density 0.1304.
- Unmatched by the string rule: INF-006, INF-008, INF-016, INF-027, INF-032, INF-053, INF-054, INF-055, INF-061; on a manual read each is covered by a task or the Constraints (word-choice misses).
- coverage_degraded parsed-sparse: Tier 2 forced.
## Candidate prior-blocker status (to be confirmed by the reviewers)
- B-1 import rule: Task 2 and the Constraints now allow exactly RUN_ID_RE and parse_time, with test_ledger_imports_only_allowed_probes_names.
- B-2 Task 10 check limited to `superclaude` commands and flags.
- B-3 Task 11 ends with `git add .dev/tasks`.
- B-4 Task 6 updates the exact-text cases in tests/sweep/test_cli_contract.py.
- B-5 Task 9 updates the install test seed list.
- B-6 Tasks 1 and 3 parse times with probes.parse_time; test_time_forms_compare_correctly.
## Self-reported confidence
0.70 (uncalibrated; Tier 2 forced).
