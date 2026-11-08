# QA Qualitative Fix Log (A.10.5 fix cycle 1)

**Task file:** TASK-RF-issue-watcher-20261107-150955.md (209 items before and after; no item added or removed)
**Consolidation:** qa/qa-qualitative-consolidated.md
**Method:** targeted Edit calls only; each item re-read before editing.

## Blocking findings (11)

| id | what changed | where |
|---|---|---|
| Op1-1 | 2.1 now decodes the cut stderr with `errors="ignore"` and says why; 2.5 asserts `len(result.stderr.encode("utf-8")) <= 500` for `"a"*499 + "é"*3` with expected text exactly `"a"*499` | Steps 2.1, 2.5 |
| Op1-2 | `rotate_if_needed` skips a shift whose source is missing (never raises); test cases added for "only audit.jsonl at 5 MiB" and "audit.jsonl and .1 at 5 MiB" | Steps 2.3, 2.8 |
| Op1-3 | `find_orca` and `check_origin` take `timeout: float \| None`; None starts no process (None / `origin_mismatch`); test added with no FakeRunner call; `run_cycle` steps 6 and 12 test `deadline.timeout_for(10)` for None (step 6 fails closed to exit 2; step 12 writes `budget_exhausted`, no entry, no probe) and the second origin check passes `timeout_for(10)` | Steps 5.1, 5.4, 6.2 |
| Op2-1 | Step 6.2 (12): a changed assignee set gives `assigned_other` / `unassigned` through `predicates.is_intended_owner`, not `revalidation_failed` (FR-008, spec line 140); 6.7 test text aligned | Steps 6.2, 6.7 |
| Op2-2 | Step 7.7 allows exactly one pre-existing skip (`tests/swarm/test_cli_registration.py:127`), 0 skipped for `tests/issue_watch/`; the Gate C and Final gate-command-reproduction prompts state that skip is not a finding | Steps 7.7, 7.G2, 9.F2 |
| Op2-3 | `status_report` retry `argv[0]` is bare `orca-ide` when `which` resolves none, never raises (OQ-50); AC-9 test pins PATH with a `tmp_path/bin/orca-ide` plus an empty-PATH case | Steps 6.3, 7.4; new OQ-50 |
| Op2-4 | Two-process lock test has a fixed start order (worker 1 `worker1.holding`, main starts worker 2 after, worker 2 exits 75); assertion names worker 1 and worker 2 | Step 8.5 |
| Op2-5 | `abandoned` entry with null `pending_at` takes its window floor from the current approval (marker and events reads), never raises, else skips `already_dispatched`; tombstone cases added to the 6.7 tests | Steps 6.2 (10), 6.7 |
| Op2-6 | `--repo` rule limited to repository-scoped `gh` lines; `gh auth status` and `gh auth refresh` must not carry `--repo` | Step 9.3 |
| Suf-1 | "A row marked NEEDS OWNER DECISION is an open blocking finding; verdict FAIL while any exists" appended to the four verifier prompts; 9.M8 and 9.M13 test NEEDS OWNER DECISION FIRST, before the PASS branch (9.M8 now also reads the fix report) | Steps 9.M6, 9.M7, 9.M8, 9.M11, 9.M12, 9.M13 |
| Suf-2 | Failure branch (fix and re-run until it passes, else HALT, next phase not released) added to the post-fix re-run of every gate in cycle 1 and cycle 2; Final and M4 re-runs now repeat Steps 9.4 to 9.16 (G-1 to G-11) with 9.3 first when the runbook changed; Step 10.1 marks FAIL and halts before 10.2 when the cited run or a p9 file shows a failure | Steps 3.G12, 3.G17, 5.G12, 5.G17, 7.G12, 7.G17, 8.G12, 8.G17, 9.F13, 9.F18, 9.M8, 9.M13, 10.1 |

## Minor fixes applied

| id | what changed | where |
|---|---|---|
| Suf-MINOR-4 | unique finding ids required in the consolidation items (A-, B-, C-, D-, F-, M-), kept in cycle 2 | Steps 3.G8, 5.G8, 7.G8, 8.G8, 9.F9, 9.M4 |
| Suf-MINOR-5 | cross-source agent classifies against "any decision DF-01 to DF-60" (the 29 departures still listed) | Step 9.M3 |
| Op2-M-1 | e2e event timestamps generated relative to now after `init-state` | Step 8.2 |
| Op2-M-2 | newline loop restricted to `git ls-files -co --exclude-standard` source files | Step 9.16 |
| Op2-M-3 | 10.1 cites the `-cycle2` post-fix files | Step 10.1 |
| Op2-M-4 | `re-approved` recorded as OQ-49 (no code added); OQ-49 to OQ-51 added to the M4 exemption sentence | Open Questions; the exemption sentence of the two source-fidelity prompts (task file lines 800 and 803) |
| Op2-M-5 | `test_fifty_cycles` also asserts at most one FakeLauncher call per issue | Step 6.8 |
| Struct | design range 902-935 (three places); TCS sentence refreshed: 52 Open Questions entries, TCS 1173; commit-withdrawn consistency: 10.2 records `commit withdrawn by owner`, 10.5 and 10.7 accept it in place of a commit result, new OQ-51 | Steps in Phases 2, 8, 9; Reflect Depth Derivation; Steps 10.2, 10.5, 10.7 |

## New Open Questions

OQ-49 (`re-approved` not emitted), OQ-50 (status retry argv[0] with no Orca on PATH), OQ-51 (commit withdrawn by owner). Open Questions entries: 49 before, 52 after.

## Re-verification

- `- [ ]` count 209 = `**Step` header count 209; per-phase counts unchanged (no item added or removed).
- No TBD, TODO or FIXME in the file.
- Gate agent total unchanged (34 lens agents; spawn-item counts unchanged).
- Frontmatter lines 1-64 not edited.
- Step 10.6 (POST reflect) is the penultimate item and Step 10.7 (Done) the last.
- OQ-47 and OQ-48 exemption sentence updated in both M4 fidelity prompts; every OQ-49 to OQ-51 reference resolves to an entry.

## Not fixed (notes only)

Part1 M1 to M12; part2 M-6 to M-14; sufficiency MINOR-3 (comma vs em dash in the regression string, matches rf-qa.md and rf-task-builder.md), MINOR-6, MINOR-7, MINOR-8, MINOR-9. Reason: minor findings are notes by the review severity rule and are not rechecked.
