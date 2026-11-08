# QA Qualitative Consolidated Findings (A.10.5 fix cycle 1)

**Task file:** TASK-RF-issue-watcher-20261107-150955.md
**Sources:** qa-qualitative-operational-report-part1.md (IMP-1..IMP-3, here Op1-1..Op1-3), qa-qualitative-operational-report-part2.md (I-1..I-6, here Op2-1..Op2-6), qa-qualitative-sufficiency-report.md (IMPORTANT-1, IMPORTANT-2, here Suf-1, Suf-2)
**Blocking findings:** 11 (each listed once). Minor fixes applied: 5 one-line minors plus structure notes. Other minors stay notes.

## Blocking findings

| id | source | items | fix |
|---|---|---|---|
| Op1-1 | part1 Issue 1 | 2.1, 2.5 | 2.1: decode with `errors="ignore"` (not "replace"); 2.5: assert `len(result.stderr.encode("utf-8")) <= 500` for `"a"*499 + "é"*3`, expected text exactly `"a"*499`. |
| Op1-2 | part1 Issue 2 | 2.3, 2.8 | `rotate_if_needed` skips a shift whose source does not exist; 2.8 adds the first-rotation case (only `audit.jsonl`) and the `audit.jsonl` + `.1` case. |
| Op1-3 | part1 Issue 3 | 5.1, 5.4, 6.2 | `find_orca` and `check_origin` take `timeout: float \| None`; None starts no process (`find_orca` returns None, `check_origin` returns `origin_mismatch`); 5.4 asserts no FakeRunner call on None; 6.2 tests `timeout_for` for None before steps 6 and 12 and writes `budget_exhausted`. |
| Op2-1 | part2 I-1 | 6.2 (12), 6.7 | Changed assignee set gives `assigned_other` / `unassigned` via `predicates.is_intended_owner`, not `revalidation_failed` (FR-008, spec line 140). |
| Op2-2 | part2 I-2 | 7.7, 7.G2, 9.F2 | Allow the single pre-existing skip `tests/swarm/test_cli_registration.py:127`; lens prompts state it is not a finding. |
| Op2-3 | part2 I-3 | 6.3, 7.1, 7.4 | `status_report` retry `argv[0]` is the bare `orca-ide` when no `_ORCA_CLIS` name resolves; AC-9 test pins PATH; Open Question recorded. |
| Op2-4 | part2 I-4 | 8.5 | Two-process lock test gets a deterministic start order (worker 1 holding marker, then worker 2). |
| Op2-5 | part2 I-5 | 6.2 (10), 6.7 | `abandoned` entry with null `pending_at` (tombstone) takes its window floor from the current approval; never raises; 6.7 case. |
| Op2-6 | part2 I-6 | 9.3 | `--repo` rule applies to repository-scoped `gh` commands only; `gh auth status` / `gh auth refresh` must not carry `--repo`. |
| Suf-1 | sufficiency IMPORTANT-1 | 9.M6, 9.M7, 9.M8, 9.M11, 9.M12, 9.M13 | NEEDS OWNER DECISION is an open blocking finding: verdict FAIL while any exists; 9.M8 and 9.M13 test it first, before the PASS branch. |
| Suf-2 | sufficiency IMPORTANT-2 | 3.G12, 3.G17, 5.G12, 5.G17, 7.G12, 7.G17, 8.G12, 8.G17, 9.F13, 9.F18, 9.M8, 9.M13, 10.1 | Post-fix re-run gets a failure branch (fix and re-run, else HALT); Final and M4 re-runs repeat Steps 9.4 to 9.16 (G-1 to G-11); 10.1 marks FAIL and halts before 10.2 on a failure. |

## Minor fixes applied in this round

| id | source | item | fix |
|---|---|---|---|
| Suf-MINOR-4 | sufficiency | 3.G8, 5.G8, 7.G8, 8.G8, 9.F9, 9.M4 | Unique finding ids in consolidation items. |
| Suf-MINOR-5 | sufficiency | 9.M3 | "covered by any decision DF-01 to DF-60". |
| Op2-M-1 | part2 | 8.2 | Event timestamps generated relative to now after `init-state`. |
| Op2-M-2 | part2 | 9.16 | Newline loop restricted to `git ls-files -co --exclude-standard`. |
| Op2-M-3 | part2 | 10.1 | Also cites the `-cycle2` post-fix files. |
| Op2-M-4 | part2 | Open Questions | `re-approved` recorded as an Open Question (no P6 item emits it); no code added. |
| Op2-M-5 | part2 | 6.8 | `test_fifty_cycles` also asserts at most one FakeLauncher call per issue. |
| Struct-1 | verification report | design range | 902-935. |
| Struct-2 | verification report | TCS sentence | Stale sentence updated to the 49-entry count (plus new entries). |
| Struct-3 | verification report | 10.2 vs 10.7 | Commit withdrawn by owner: 10.7 records "commit withdrawn by owner" instead of commit-result.md; POST reflect runs on the working-tree diff, documented as an Open Question. |

## Notes (not fixed, not rechecked)

Part1 M1..M12; part2 M-6..M-14; sufficiency MINOR-3 (comma vs em dash in regression string), MINOR-6 (mutation check scratch copy), MINOR-7 (M4 agent split), MINOR-8 (qa_intensity), MINOR-9 (gate-less phase headers).
