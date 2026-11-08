# QA Report - Gate B, test-adequacy lens (Phases 4 and 5)

**Topic:** issue-watch implementation, Gate B (record.py, launch.py and their tests)
**Date:** 2026-11-07
**Phase:** task-qualitative (lens: test-adequacy)
**Fix cycle:** 1 (first review; report only, `fix_authorization: false`)
**Reviewer files read:** `gate-b-change-set.md`, `record.py`, `launch.py`, `conftest.py`, `test_record.py` (all 2002 lines), `test_launch.py`, `test_find_orca_parity.py`, `test_origin_parity.py`, `test_marker_contract.py`, research/06 Table 1.3, design sections 7.4 to 7.6 and 8.4, the originals the parity tests drive (`install_user_setup._find_orca`, `origin_repo.parse_origin_url`).

---

## Overall Verdict: FAIL

Six blocking findings (all missing or vacuous tests; no defect in the shipped behaviour that the transition rows describe). Twenty minor notes. The suite is strong on the transition rows themselves: every T-1 to T-13 row has a literal-expectation test, and the half-open windows (24 h, lease, 10 minutes) are tested exactly at, one second before and one second after. It is weak on input-validation guards, on three `record.py` helpers, on some time fields in the validation matrix, and on the dry-run file's mode guard.

I did not find 15 blocking errors and do not claim them. I found 26 distinct findings (6 blocking, 20 minor). The evidence is a mutation experiment: I copied `src/superclaude` to a temporary directory, applied one small change at a time, and ran the test files against the copy with `PYTHONPATH` (the repository tree was not touched). A surviving mutant means no test fails if that behaviour breaks.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | T-1, T-2, T-3 (`fail`, `backoff_elapsed`) have tests that fail if the behaviour breaks | none | PASS | `test_record.py:951-1020` assert whole `Entry` equality against literal `blank(...)`; mutant `>=` to `>` on backoff (A7) was killed |
| 2 | T-4 `mark_pending`: field effects AND input guards | AX-3 | FAIL | Field effects pinned (`:1026-1055`). The five guards in `record.py:496-555` are untested: mutants M5 (positive ids), M7 (absolute `launch_cwd`), A11 (aware `approved_at`), A12 (`launch_login`), A13 (`launch_account_id`) all survive. See finding 1 |
| 3 | T-5, T-6, T-7 (`mark_launched`, `mark_unknown`, `mark_spawn_error`) | AX-3 | FAIL | Lease of exactly 60 min is pinned (`:1058-1067`, mutant A8 killed). `mark_launched`'s empty or non-str `operation_id` guard (`record.py:584-585`) is untested: mutant M6 survives. See finding 2 |
| 4 | T-8, T-9 (`sweep`) incl. launched-with-no-lease, unknown never moves, no save | none | PASS | `:1094-1123`, `:1609-1695`; the no-save test patches `FileStore.save` to raise |
| 5 | T-10, T-11, T-12 (`mark_claimed`) from every allowed state, incl. attempts_exhausted tombstone | none | PASS | `:1139-1216`; mutant V6 (allow `pending`) killed. The approval guard inside `mark_claimed` is covered by finding 1 |
| 6 | T-13 (`reset_entry`) removal, `consumed_log` append, prune, cap unchanged | none | PASS | `:1236-1246`, `:1525-1557`; mutants M13, M14 killed |
| 7 | Every other (state, trigger) pair raises, input unchanged | none | PASS | `:1253-1318`; `ALLOWED` is written by hand; counts 15 and 40 re-derived: 8 triggers x 7 states, minus `backoff` of no entry = 55, minus 15 allowed = 40 |
| 8 | Boundaries: exactly 24 h, exactly the lease, exactly 10 minutes, exactly 500 bytes | none | PASS | 24 h: `:1364-1389`, `:1512-1518`, `:1560-1572`; lease: `:1324-1340`; backoff: `:1343-1356`. The 500-byte cap belongs to `runner.py` (`STDERR_CAP_BYTES = 500`), not to these files; `test_runner.py:117-148` pins it (outside this change set) |
| 9 | Lock rule (`FileStore.lock`) | none | PASS (with notes) | Missing, symlink, dangling symlink, directory, foreign owner, held, nested, replaced, unlinked: `:645-748`. Two guards are untested (minor notes 1 and 2) |
| 10 | Save rule: atomic write, mode, fsync, sorted keys, ASCII, dry-run file | AX-4 | FAIL | `FileStore.save` chmod guard is pinned by `:562-575` (mutant A1 killed). The dry-run twin is not: `test_ac13_save_dry_run_forces_0600_over_a_wider_existing_file` (`:1949-1955`) passes with the `os.chmod` deleted (A2) and the directory fsync deleted (A3). See finding 6 |
| 11 | Store validation matrix (AC-22 / NFR-011) | AX-3 | FAIL | `last_completed_cycle_at` is never validated by any test (mutant V1 replaces it with `None`; 408 tests pass); `approved_at` and `pending_at` are absent from `TIME_PLACES` (`:339-347`). See finding 5 |
| 12 | Helper functions in `record.py` have a test | AX-3 | FAIL | `set_considered`, `set_next_permitted`, `set_last_completed` (`record.py:721-738`) are referenced by no test (grep over the repository). Mutants M4 and A15 survive. See finding 4 |
| 13 | Construction guards (`_new_entry`, `init_state` naive `now`) | AX-3 | FAIL | Mutants A10 and A14 survive. See finding 3 |
| 14 | DF-15: lock is free after a `SystemExit` inside the `with` block is really exercised | none | PASS | `:751-766`: raises `SystemExit(3)` inside `store.lock()`, then takes a probe `flock` from a second open file description and the lock again. Mutant M10 (remove unlock and close) is killed, so the test is not vacuous. Caveat: record level only; the crash-injection reruns arrive in P8 |
| 15 | `CrashingStore` implements C1, C3, C4, C5 as Table 1.3 states | none | PASS (by reading) | `conftest.py:157-164`: C1 raises before delegating save 1; C3 delegates save 1 then raises; C4 raises at save 2 before delegating; C5 delegates save 2 then raises; C2 is rejected by `crash_at not in CRASH_POINTS` and left to the `os.replace` patch. Matches Table 1.3 rows C1, C3, C4, C5. No test exercises the class (minor note 3) |
| 16 | Parity tests really drive the original code | none | PASS | `test_find_orca_parity.py:85-116` calls `setup._find_orca()` with `shutil.which` and `subprocess.run` faked; `test_origin_parity.py:62-71` loads `origin_repo.py` by path and calls `parse_origin_url`. Same replies go to both sides; argv lists and the 10 s timeout are compared |
| 17 | Hermeticity: wall clock, real HOME, network, paths outside `tmp_path`, xdist, markers | none | PASS (with notes) | No `datetime.now`, `time.time`, `sleep`, network or custom marker in the five files (grep). `tmp_state` moves HOME and XDG into `tmp_path`. Ran the five files under `pytest -n 4` (xdist): 686 passed. One real-HOME read remains (minor note 4) |
| 18 | Expectations written literally, not derived from the code under test | none | PASS (with notes) | Literal key lists (`:44-71`), literal `blank`/`pending` entries, hand-written `ALLOWED`. Self-referential spots are listed as minor notes 9 to 11 |
| 19 | `launch.py` tests: prompt, argv, probe, origin, outcome table, operation id, agent pin | none | PASS (with notes) | Prompt range ends 1 and 999999999 and rejects 10**9 (`test_launch.py:45-68`); 19 hostile prompts (`:116-145`); operation-id boundary 1 and 128 and 129 (`:183-190`, `:604-618`); the 12-element argv is compared literally (`:74-91`). Not mutation-run for these rows; surviving guards found by mutation are minor notes 5 to 8 |

Confidence is computed in the Self-Audit section below.

## Summary
- Checks passed: 13 / 19
- Checks failed: 6
- Critical issues: 0
- Blocking findings: 6 (all IMPORTANT, test-adequacy)
- Minor notes: 20
- Issues fixed in-place: 0 (report only)

## Issues Found (numbered findings)

Blocking findings (any one makes the verdict FAIL):

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT (blocking), AX-3 | `record.py:496-503` (`_check_approval`), `:549-555` (`mark_pending`), `:664-667` (`mark_claimed`); `test_record.py` has no `ValueError` assertion at all (grep `ValueError` over the file: 0 hits) | T-4, T-10, T-11 and T-12 refuse a bad approval or launch context (non-positive or non-int ids, naive `approved_at`, non-absolute `launch_cwd`, empty `launch_login`, non-positive `launch_account_id`). These values later reach audit lines and the retry command. Five mutants that delete a guard each (M5, M7, A11, A12, A13) and one that disables `_check_approval` in `mark_claimed` (A9) leave all 408 `test_record.py` tests green. | Add one parametrized test per guard that calls `mark_pending` with a bad `PendingContext` field (`0`, `-1`, `True`, `"1"`, naive datetime, `"relative"`, `""`, `None`) and asserts `ValueError` and an unchanged input document; add the same for `mark_claimed(..., approval=ApprovalResult(approver_id=0, ...))` and a naive `approved_at` |
| 2 | IMPORTANT (blocking), AX-3 | `record.py:584-585` (`mark_launched`) | T-5 requires a non-empty `str` operation id; `launch.py` already limits the id to `[A-Za-z0-9._:-]{1,128}`, and `status` prints it in a shell command. The record-side guard is untested: mutant M6 (delete it) survives. `mark_launched(doc, 7, "", now)` and `mark_launched(doc, 7, None, now)` are never called. | Add a test that `mark_launched` raises `ValueError` for `""`, `None`, `5`, `b"op"` and leaves the document and the `pending` entry unchanged |
| 3 | IMPORTANT (blocking), AX-3 | `record.py:468-471` (`_new_entry`), `:764` (`init_state` naive `now`) | `fail` and `mark_pending` create entries through `_new_entry`, which refuses an invalid issue number; `init_state` refuses a naive `now` before creating anything. Mutants A10 and A14 survive. Every test uses issue 7 or another valid number and an aware `now`. | Test `fail(doc, 0, ...)`, `fail(doc, True, ...)`, `fail(doc, "7", ...)` and `mark_pending` with `n=-1` raise `ValueError` and add no entry; test `init_state(tmp_path / "s", naive_now)` raises `ValueError` and creates no directory (the code comment promises "before anything is created") |
| 4 | IMPORTANT (blocking), AX-3 | `record.py:721-738`: `set_next_permitted`, `set_last_completed`, `set_considered` | Three public helpers have no caller in any test (repository grep finds only the definitions). `set_considered` carries FR-023 (stamp `examined` with `now`, drop every issue not in `discovered`); mutants M4 (no pruning) and A15 (no stamping) survive. `reset_rate_limit` and `prune_consumed_log` are tested; these three were left out. | Add tests: `set_considered` keeps only discovered issues, stamps only examined issues that are also discovered, leaves an unexamined discovered issue's old time, does not mutate its input; `set_next_permitted(doc, t)` and `(doc, None)`; `set_last_completed` stamps exactly `now` and changes nothing else |
| 5 | IMPORTANT (blocking), AX-3 | `test_record.py:339-347` (`TIME_PLACES`), `:246-265` (wrong top-level type) | The AC-22 matrix "a naive or non-`Z` time string is `store_invalid`" runs over 7 time places but skips `approved_at`, `pending_at` and `last_completed_cycle_at`; no wrong-type case exists for `last_completed_cycle_at`. Mutant V1 (validate ignores `last_completed_cycle_at` and stores `None`) leaves every test green, so no test ever reads that field back after `load`. | Add the three places to `TIME_PLACES`; add `{"last_completed_cycle_at": 5}` to the wrong-type list; assert `doc.last_completed_cycle_at == datetime(2026, 11, 7, 11, 30, tzinfo=timezone.utc)` in `test_valid_document_loads_with_int_keys_and_aware_times` |
| 6 | IMPORTANT (blocking), AX-4 | `test_record.py:1949-1955` (`test_ac13_save_dry_run_forces_0600_over_a_wider_existing_file__fr019`); `record.py:857-858` | The test name claims it proves `save_dry_run` forces mode 0600 over a wider existing file. It passes with the `os.chmod` deleted (mutant A2) because `write_prepared_bytes` already creates the replacement through `mkstemp` at 0600; the `FileStore.save` twin gets a real guard test (`:562-575`, which injects a wide-mode writer), the dry-run function does not. The directory fsync in `save_dry_run` (`_fsync_dir`) is also unobserved (mutant A3). | Copy the `wide()` writer-patch test for `save_dry_run`; add a `counting` fsync test that asserts the state directory is fsynced last |

Minor notes (do not fail the review; not rechecked in later rounds):

| # | Location | Note |
|---|----------|------|
| 1 | `record.py:402`; `test_record.py:645-748` | The `not stat.S_ISREG(...)` half of the lock-safety check is untested (mutant M3 survives): the directory case dies earlier at `os.open` (`IsADirectoryError`), so a FIFO or device lock path is never tried. Add a `os.mkfifo` case expecting `lock_invalid` |
| 2 | `record.py:415-416` | `if os.fstat(fd).st_nlink == 0: raise LockHeld()` cannot be reached by any test (mutant M2 survives): an unlinked path already raises at `os.stat` on line 410. Either find a case or delete the branch |
| 3 | `conftest.py:120-230` | `CrashingStore` and `FakeLauncher` have no test of their own (repository grep: no `test_*.py` uses either). I verified `CrashingStore` against Table 1.3 by reading (item 15), but an edit that swaps C3 and C5 stays green until P8 lands. A 10-line self-test per crash point would pin it |
| 4 | `test_marker_contract.py:22-25`, `:34-39` | `Path.home() / ".claude"` is evaluated at import time, so `tmp_state`'s HOME override cannot reach it; on this host `~/.claude/skills/sc-issue-protocol/{refs/claim.md,templates/claim-comment.md}` exist and are read. A stale installed copy makes the test fail for a reason outside the repository. The plan sanctions this (DF-46, design 791, step 5.8), so it is not a deviation, but it is the one real-HOME read in the change set |
| 5 | `launch.py:244-253`; `test_launch.py` | `LaunchOutcome.__post_init__` (bad kind, bad detail, id failing the pattern, `launched` without an id) has no test; mutant A4 (disable all three checks) leaves 275 tests green. The constructor is the last guard before an operation id is stored |
| 6 | `launch.py:174`, `:223` | `_check_timeout` is exercised only through `OrcaLauncher.launch` (`test_launch.py:686-697`). `find_orca(timeout=0 / -1 / True / "10")` and `check_origin(..., timeout=0)` are untested (mutants A5, A6 survive) |
| 7 | `launch.py:205`; `test_launch.py:324-377`, `test_origin_parity.py:34-59` | The `owner in (".", "..")` guard of `parse_origin` is untested in both parsers (mutant M11 survives). The parity table has repo `.git` but no `https://github.com/../IronClaude`, `https://github.com/./x` or `https://github.com/IronbellyOrg/..` row, and no leading/trailing whitespace row although both parsers call `.strip()` |
| 8 | `launch.py:313-314`; `test_launch.py:536-540` | The `timed_out` outcome is tested only with empty output. Whether a valid id in partial stdout is kept (mutant V3 drops it) is not pinned |
| 9 | `launch.py:270-281`, `:322-324` | Probe result: `outcome_of` of exit 0 with stdout `{"error": {"operation_id": "op-9"}}` returns `launched`/`ok` (run via `uv run python -I`). The design table (D 629-634) says "operation id a non-empty str" and D 636 lists both paths as candidates, so this may be intended, but no test pins either answer. Add a case and record the decision |
| 10 | `test_record.py:1289-1291`; `test_origin_parity.py:95-110` | `test_the_pair_table_covers_every_state_and_trigger_once` and `test_ac16_parity_table_covers_every_required_shape` assert properties of tables built inside the test file itself; they guard against table edits, not against code changes |
| 11 | `test_launch.py:111-113`, `:741-746` | Two tests pin the same constant, and `assert EXPECTED_AGENT == "claude"` compares a literal with the same literal. Harmless; the live check is `ORCA_AGENT == EXPECTED_AGENT` and the `argv[4]` check |
| 12 | `test_record.py:519-527`, `:544-552` | The byte-identical test is a determinism check only, and the decimal-string-order test builds `considered` with `"10"` before `"9"`, which is also the string-sorted order, so it passes with `sort_keys` off. Sorting itself is pinned by `:530-541` (mutant M1 killed) |
| 13 | `test_record.py:530-541`; `record.py:372` | `data.decode("ascii")` cannot fail: no test stores a non-ASCII string (e.g. a `launch_login` with an accent), so `ensure_ascii=True` is unpinned (mutant M8 survives). Add one non-ASCII `launch_login` round trip |
| 14 | `test_record.py:1810-1822` | The read-only-parent test relies on `chmod 0o500` stopping writes; as uid 0 (some CI containers) the directory is writable and `pytest.raises(StoreError)` fails. It passes here (uid 1000). No marker or skip may be used here, so drop this test and keep its sibling at `:1825`, which builds the failure with a plain file as the parent and works as any user |
| 15 | `record.py:427-433`; `test_record.py:797-803` | `disabled_since()` uses `os.stat`, which follows symlinks; for a dangling `DISABLED` symlink `disabled()` is True while `disabled_since()` is None. The test asserts only `disabled()` for that case, so the divergence is unpinned |
| 16 | `test_record.py:629-639` | "keeps the old file" mocks the whole writer, so it proves nothing about atomicity. A real failure inside `write_prepared_bytes` (`os.replace` raising) is left to P8's C2 case; consider one record-level case now |
| 17 | `test_find_orca_parity.py:99-112` | The faked `subprocess.run` never raises, so the original's `except (OSError, subprocess.SubprocessError, ...)` branch (`install_user_setup.py:216-217`, timeout and spawn failure) is never driven; the launch side covers it at unit level only (`test_launch.py:296-297`) |
| 18 | `test_find_orca_parity.py:171-186` | The test requires the original to raise `AttributeError` or `TypeError`; if `_find_orca` is later fixed upstream this test fails although nothing is wrong. State that coupling in the docstring or assert only the new function's behaviour |
| 19 | `conftest.py:148-151`, `:157-164` | `CrashingStore.migrated` reads `real.migrated`, which the `Store` protocol (`record.py:316-329`) does not declare; and `saves` counts every save, so a cycle that saves for a sweep before the `pending` write shifts "save 1". Table 1.3 assumes one eligible issue and no sweep; the P8 tests must keep it that way |
| 20 | `test_record.py:1798-1807` | The exclusive-create race test patches `os.path.lexists` to False and covers `lock` only; the same race for `dispatch.json` is untested |

## Mutation evidence (temporary copies; repository untouched)

| Mutant | Change | Result |
|---|---|---|
| M1 | `sort_keys=False` in `FileStore.save` | killed (1 failed) |
| M2 | delete `st_nlink == 0` branch | survives |
| M3 | delete `S_ISREG` half of lock check | survives |
| M4 | `set_considered` stops pruning | survives |
| M5 | delete positive-id guard in `_check_approval` | survives |
| M6 | delete empty-id guard in `mark_launched` | survives |
| M7 | delete absolute-`launch_cwd` guard | survives |
| M8 | `ensure_ascii=False` | survives |
| M10 | lock: remove unlock and close (DF-15) | killed |
| M11 | delete `.`/`..` owner guard in `parse_origin` | survives |
| M13 | day-cap window loses `<= now` | killed |
| M14 | allow `failed` in `_RESETTABLE` | killed |
| M15 | `init_state` drops `chmod 0o700` | killed |
| M16 | `validate` drops the `pending_at` rule | killed |
| A1 | `FileStore.save` drops `chmod 0o600` | killed |
| A2 | `save_dry_run` drops `chmod 0o600` | survives |
| A3 | `save_dry_run` drops directory fsync | survives |
| A4 | `LaunchOutcome.__post_init__` checks disabled | survives |
| A5, A6 | `_check_timeout` bypassed in `check_origin`, `find_orca` | survive |
| A7 | backoff `>=` to `>` | killed |
| A8 | lease 60 min plus one second | killed |
| A9 | `_check_approval` disabled in `mark_claimed` | survives |
| A10 | `_new_entry` issue-number guard removed | survives |
| A11, A12, A13 | naive `approved_at`, empty `launch_login`, bad `launch_account_id` guards removed | survive |
| A14 | `init_state` naive-`now` pre-check removed | survives |
| A15 | `set_considered` stops stamping | survives |
| A17 | `load_dry_run` stops catching `ValueError` | killed |
| A18 | `migrated` flag always False | killed |
| V1 | `validate` ignores `last_completed_cycle_at` | survives |
| V3 | timed-out outcome drops the id | survives |
| V6 | `mark_claimed` also allows `pending` | killed |

Not counted: M0 (no-op control, passed), M9 (same as A2, it only reached the dry-run chmod), M12 and V4 (equivalent changes), M17 (pattern matched nothing), V2 (syntax error in the copy), V5 (pattern matched nothing).

## Actions Taken

None. `fix_authorization: false`. The only file written is this report; temporary mutation copies lived under a private `/tmp/ironclaude-batch.*` directory and were removed by an exit trap.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

The spawn prompt carried no `## Inherited Structural Verdict` section, so this review ran standalone (no structural reliance).

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was supplied. The Gate B change-set file `gate-b-change-set.md` lists gate runs (G-1 1094 and 1372 passed, G-4, G-5); I treated those as context only and re-ran the five test files myself (686 passed; 686 passed again under `pytest -n 4` with `pytest-xdist` resolved offline).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Do the tests fail when behaviour breaks? Verified by 34 informative mutants run against temporary copies of `src/superclaude` (table above); 12 were killed and 22 survived.
- Is the DF-15 test real? Mutant M10 (no unlock, no close) fails `test_ac22_lock_is_free_again_after_an_exit_inside_the_with__nfr005`.
- Does `CrashingStore` match Table 1.3? Read `conftest.py:120-176` against research/06 lines 58-68: C1, C3, C4, C5 match; C2 is correctly excluded.
- Do the parity tests drive the originals? Read `install_user_setup.py:198-218` (`_find_orca`) and `origin_repo.py:60-72` (`parse_origin_url`) and compared the faked call signature (`capture_output`, `text`, `timeout=10`, `stdin`) with the real call.
- Is there a real-HOME or wall-clock dependency? Grep for `datetime.now|time.time|utcnow|Path.home|expanduser|os.environ|sleep(|skip|xfail|pytest.mark` over the five files; confirmed the installed `~/.claude` copies exist on this host and are read by `test_marker_contract.py`.
- Probed an untested behaviour directly: `outcome_of` with an error-path id at exit 0 (minor note 9).

Answers to the self-audit questions:
1. Factual claims independently checked against code: about 70 (every row of items 1 to 19, 34 mutation runs, 2 probe runs, 3 suite runs).
2. Files read: `record.py` (858 lines), `launch.py` (348), `conftest.py` (230), `test_record.py` (2002), `test_launch.py` (746), `test_find_orca_parity.py` (286), `test_origin_parity.py` (176), `test_marker_contract.py` (53), `install_user_setup.py` lines 25-45 and 195-235, `origin_repo.py` lines 55-110, research/06 lines 30-120, design lines 470-540 and 604-640, `gate-b-change-set.md`, the Step 4.1c, 4.3, 4.4, 4.5 and 5.8 items of the task file, both `_assumed_shape` Orca fixtures.
3. This report found issues, so the zero-issue question does not apply; the evidence for each blocking finding is a surviving mutant, reproducible by the sed expressions summarized in the table.
4. No web research was performed; Tavily was not needed.

**Confidence:** Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 15 | Grep: 12 | Glob: 1 | Bash: 16 (3 suite runs, 3 mutation batches, 1 probe, file and design excerpts)
Tool calls (Read + Grep + Glob = 28) exceed the 19 checklist rows, so the minimum-engagement rule is met.

Axis lens status: drift was applicable (BUILD-REQUEST GOAL line 9 was read from the build request); no AX-1 finding.

## Recommendations
- Resolve findings 1 to 6 (all are additions of tests; no production change is needed). Findings 1 to 3 and 5 can be one parametrized block each; finding 4 needs about six small tests; finding 6 copies an existing test.
- Take minor notes 1, 3, 5, 6, 7, 13 and 14 in the same pass if cheap; none is required to clear the gate.
- After the fix, re-run the same mutants (the table lists them) and expect M3, M4, M5, M6, M7, M8, A2, A3, A9 to A15 and V1 to be killed; that is the cheapest re-verification.

## QA Complete
