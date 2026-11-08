# QA Report: Gate C content verification (fix cycle 1)

**Topic:** issue-watch implementation, Gate C (Phases 6 and 7)
**Date:** 2026-11-08
**Phase:** fix-cycle (content verification, task-qualitative lens)
**Fix cycle:** 1
**Fix authorization:** false (report only; no file other than this report was written; a temporary copy under /tmp was used for probes and deleted)

---

## Overall Verdict: FAIL

12 of the 13 blocking findings are fixed as stated. All 13 stated defects are gone, but the C-1 fix moved the 120 s launch cut-off check ahead of the origin re-check, which opens a new gap: a launch can start after the cut-off (one new blocking finding, N-1 below). The two [PROPOSAL] decisions and the cycle-start exit 3 deviation are judged reasonable. No assertion was found weakened or deleted.

## Per blocking finding

| id | Result | Evidence |
|---|---|---|
| C-1 | FIXED (with the side effect in N-1) | `cycle.py:1039-1045`: `launch_allowed()` then `timeout_for(GIT_TIMEOUT_S)` None, both raise `_Skip("budget_exhausted")` before the git call; `origin_mismatch` only when `_origin_ok` returns False after a real call (`:1044-1045`). `_origin_ok(timeout)` (`:651-659`) no longer reads the deadline. Tests `test_cycle.py:4227-4305` cover a 236 s jump at cycle start, during the reserved re-read, the floor alone (cut-off patched to 1000 s), and git `failed`, `timeout`, `spawn_error` still giving exit 2. Probe: the old defect (236 s jump gives exit 2 `origin_mismatch`) no longer reproduces. |
| C-2 | FIXED | `audit.py:62-64` adds `cycle_complete` (cycle, 0); `cycle.py:1123-1133` `_cycle_reason` returns it for a clean cycle; `:805-810` the `_Stop` candidate gets no decision line (still stamped when `stop.stamp`). `check_line_kinds` (`test_cycle.py:2032-2052`) is strict: a cycle line needs `exit_for(reason) == table exit == line exit` and table kind `cycle` (or `entry` with table exit 7); a decision line must be skip, entry or skip/warning; a warning line must be warning kinds. Four negative tests (`:2069-2092`) prove it rejects a skip or entry reason on a cycle line and a warning reason on a decision line. Spot mutant "clean cycle back to `not_approved`" is killed (first failure `test_idle_cycle_makes_two_gh_calls...`). |
| C-3 | FIXED | `cli.py:121-129` catches `Exception` only; `audit.stderr_fallback("cycle_crashed", 1)` (valid: `audit.py:57`), prints only the class name, exits 1. `test_cli.py:628-687`: `RuntimeError(secret)` gives one fallback line with the five keys, secret absent, no traceback, store bytes unchanged, lock free; `build_deps` failure; `SystemExit(42)` and `KeyboardInterrupt` propagate. |
| C-4 | FIXED | New fixtures `fixtures/_assumed_shape/orca_launch_no_operation_id.json` and `orca_launch_empty_operation_id.json` carry `_assumed_shape: true`; `test_cycle.py:2992-3015` loads both through `load_fixture(...)["payload"]`; `test_launch.py:804-831` pins no id at any `OPERATION_ID_PATHS` path and `""` at path 0, with the resulting `LaunchOutcome`. |
| C-5 | FIXED | `test_slo_helper.py:257` reads "dry-run lines 13 / 18". |
| C-6 | FIXED | `test_cycle.py:4363-4413` with `conftest.py:186` `FailingStore`: pending save fails gives exit 6, `launcher.calls == []`, one save, `dispatch.json` identical, no audit line, literal fallback line; outcome-save failure gives one launch, entry `pending` with `launches` 1, two later cycles launch nothing. Mutant "`_save` swallows `OSError`" killed (first failure is the C-6 test). |
| C-7 | FIXED | `test_cycle.py:4416-4436` (idle and one-skipped-issue): exit 6, no audit line, no health stamp, store unchanged; `test_cli.py:690-704` pins `cycle: state_dir_unwritable`, `exit: 6`. |
| C-8 | FIXED | `test_cycle.py:4442-4464`: `audit.jsonl` is a directory; exit and reason unchanged, exactly one stderr line with literal `kind, ts, host, exit, reason`, store still saved (health stamp on the clean cycle). |
| C-9 | FIXED | `test_cycle.py:4467-4519`: version-0 store; real cycle rewrites at version 1 without `legacy_note`; dry-run leaves the bytes identical (`before` compared byte for byte). Spot mutant "dry-run also saves the migrated store" killed by `test_a_dry_run_migrates_in_memory_and_never_writes_the_store__df17_fr019_c9`. |
| C-10 | FIXED | `test_cycle.py:4532-4594`: five parametrized outcomes plus `spawn_error`, each with issues 9 and 10, `_touched(world) == {9}`, no entry for 10, literal `considered` list (`[]` for the cut-off). |
| C-11 | FIXED | `conftest.py:96-97` `FakeRunner.run` asserts the timeout is not None; `:951-954` teardown asserts 5.0 to 20.0 for every call of every scripted cycle; `test_cycle.py:4308-4330` pins the 12 timeouts as a literal list; the three jump tests cover cycle start, probe and second origin check. |
| C-12 | FIXED | `test_cli.py:51` captures `_REAL_BUILD_DEPS` before the autouse replacement; `:580-609` asserts config identity, `SubprocessRunner`, `FileStore` and `AuditLog` over `config.state_dir`, `SystemClock`, `shutil.which`, `socket.gethostname()`, and that the `OrcaLauncher` runs `launch_argv(...)` through the runner with `cwd=str(worktree)`. |
| C-13 | FIXED | `test_cycle.py:4602-4635`: `_MOUNTINFO == "/proc/self/mountinfo"`, real reader on `/`, tmp file text and `None` for a missing file, `load_config` refusing an `nfs4` state dir through the real reader and accepting a local one. |

## New blocking finding

| id | Severity | File | Evidence | Expected versus actual |
|---|---|---|---|---|
| N-1 | blocking (wrong behaviour against a stated design rule, regression introduced by the C-1 fix) | `src/superclaude/cli/issue_watch/cycle.py:1039-1058` (`_launch`) | The only `launch_allowed()` call (`grep`: `cycle.py:1039`) now runs before the origin re-check, which may take up to 10 s, and nothing re-tests the cut-off between the git call, the pending write and `d.launcher.launch(...)`. Probe on a temporary copy of the tree (code identical, one added test): a clock advance of 115 s during the reserved `items` re-read (elapsed 115, cut-off passes), then 10 s inside the second `origin` call (elapsed 125) produced exit 0, `launched_issue` 9, one launcher call with the 120 s timeout. Before the fix the check stood after the git call. | Design 8.5 line 647: Orca launch "not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line"; line 649 says the launch ends at 240 s at worst (with the gap it can end at 250 s). Expected: no launch, no entry, decision `budget_exhausted`. Actual: launch starts at 125 s. No test covers a clock advance inside the origin call (`test_no_launch_starts_at_121_s_elapsed` and the 120 s boundary test move the clock only at the re-read). Required fix: keep the `timeout_for(GIT_TIMEOUT_S)` None guard before the git call and test `launch_allowed()` after the origin check (or both before and after), and add a case with the clock advancing inside the second `origin` call that expects exit 0, a `budget_exhausted` decision and no entry. Note the C-1 tests that assert "origin called once" after a 236 s jump at the re-read must then be adjusted deliberately: either keep the pre-check as well (then they stay valid) or expect the second git call. |

## Judgement of the executor decisions

| Decision | Verdict | Reasoning |
|---|---|---|
| [PROPOSAL] `cycle_complete` (cycle, exit 0) | Reasonable | The spec reason table (spec lines 330-358) has no cycle-kind reason for a clean cycle, and DF-41 plus Step 6.6 forbid a skip reason on a cycle line. A new closed name is the minimal way to keep the invariant; it is added to `REASON_TABLE`, marked [PROPOSAL] in a comment, and the name-count pin was updated (59). SLO helper exclusions (`disabled`, `not_enabled`) are unaffected. |
| [PROPOSAL] `cycle_crashed` (cycle, exit 1) | Reasonable | Spec exit table (spec 315-326) has no crash code; exit 1 is already the `status` unhealthy code but for a different command. FR-020 asks for a one-line stderr fallback; only the exception class name is printed, so no issue text can leak. |
| No decision line for the stopping candidate | Reasonable | It is the only way to keep "a cycle reason never on a decision line" while the stop reasons (`rate_limit_clamped`, `project_read_failed`, `orca_not_found`, `disabled_mid_cycle`, `origin_mismatch`) are cycle-kind in the spec table. The candidate is still stamped where `stamp=True`, so S1 and FR-023 behaviour is unchanged. |
| Cycle-start origin check with no time ends exit 3 `gh_timeout` | Correct | Design 8.5 line 646: the git origin call is "as `gh`", and the `gh` row (line 644) gives "exit 3 `gh_timeout` when shared". The step-6 origin check (design 6.2 row 6) is a shared call, not a per-issue read, so `budget_exhausted` (a skip reason, forbidden on a cycle line under strict DF-41) cannot apply. `origin_mismatch` stays reserved for a completed failed comparison (row 6). The per-issue re-check correctly uses `budget_exhausted` (line 647). Test `test_cycle.py:4227-4238` pins exit 3, only the `user` gh call, no git call. |

## Assertion weakening check

- The tree is untracked, so no diff exists; I compared the rewritten code and tests with the strict invariant and the spec.
- `check_line_kinds` is stricter than the "accept both" form the finding described: it ties the cycle line exit to the table exit and rejects skip, entry (except table exit 7) and warning reasons on a cycle line. The one allowance (entry reasons with table exit 7 on an exit-7 cycle line) follows from the spec table: exit 7 has no cycle-kind reason, so the cycle line must name the failed entry's reason.
- Changed expectations (`EXIT_TABLE` row 5 now `[(8, "assigned_other")]`, clean cycles expect `cycle_complete`, skip reasons asserted on decision lines) are literals, not derived from the code under test.
- No `xfail`, no weakened `in`/`or` reason checks found (`grep`). All 2242 tests pass (`uv run pytest tests/issue_watch/ -q`: 2242 passed in 8.6 s).

## Minor notes (not rechecked later)

- M-1: `test_cycle.py:4606-4608` uses `pytest.skip("/proc/self/mountinfo exists on Linux only")`; the task's test rule says no test uses `pytest.skip`, `skipif` or `xfail`. The package is Linux-only (platform check), so the skip never fires here. Replace by an unconditional assertion.
- M-2: The fix report's remark that the `timeout_for(GIT_TIMEOUT_S)` None guard in `_launch` is reachable only with a patched cut-off is true today; if N-1 is fixed by checking the cut-off after the git call, that guard can be reached again with the real constants.

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was provided in the prompt; none relied on (standalone behaviour).

**(b) Independent semantic checks:**
- Read the design 8.5 rows (lines 638-649), spec reason table (330-358), DF-41 and the Step 6.6 text, then the fixed `_launch`, `_steps`, `_cycle_reason`, `_candidates`, `_commit` code.
- Ran the full suite (2242 passed) and four mutants on a /tmp copy through a monkeypatch fixture: `_save` swallowing `OSError` (killed), dry-run saving the migrated store (killed), clean cycle reason back to `not_approved` (killed), cut-off skip as `origin_mismatch` (killed by the Deadline unit test).
- Wrote a probe test on the temporary copy that advances the clock 115 s at the re-read and 10 s inside the second origin call: the launch started at 125 s (basis of N-1). The copy was deleted afterwards.

**Confidence:** Verified: 18/18 (13 finding ids, 4 executor decisions, 1 sweep for new issues and weakened assertions) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Not run by me: the pinned ruff check (structural verifier's scope) and the full set of the fix agent's 23 mutants (4 re-run).
**Tool engagement:** Read: 13 | Grep: 13 | Glob: 0 | Bash: 12

## Recommendations

- Cycle 2: fix N-1 only (re-test `launch_allowed()` after the origin re-check, add the clock-inside-origin test). The 13 other findings need no further work.

## QA Complete
