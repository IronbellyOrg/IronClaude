# QA Report — Gate C test-adequacy lens (task-qualitative)

**Topic:** issue-watch Phases 6 and 7 (cycle.py, cli.py and their tests)
**Date:** 2026-11-08
**Phase:** task-qualitative (lens: test-adequacy)
**Fix cycle:** N/A (fix_authorization: false, report-only)

---

## Overall Verdict: FAIL

9 blocking findings (TA-1 to TA-9) and 16 minor notes (TA-m1 to TA-m16). Every blocking finding was proved by a surviving mutant: a one-line change to `cycle.py`, `cli.py` or `record.py`, made on a copy under `/tmp`, that leaves all 616 tests of `test_cycle.py`, `test_cli.py` and `test_slo_helper.py` green.

## Method

- Read in full: `gate-c-change-set.md`, `cycle.py` (1350 lines), `cli.py` (339), `conftest.py` (889), `test_cycle.py` (4153), `test_slo_helper.py` (416), `test_cli.py` (1443), design lines 100-166, 220-388 and 720-764, decision rows DF-01 to DF-60 and task steps 6.4 to 7.6 with the PRE-1 to PRE-12 notes (task file lines 466-512 and 960-984).
- Baseline: copied `src/`, `tests/issue_watch/`, `tests/conftest.py` and `pyproject.toml` to `/tmp/gc-mut-ta` and ran the three test files with `PYTHONPATH` pointing at the copy (import path confirmed to be the copy): 616 passed. The same files under `-n 4` (pytest-xdist, offline `--with`): 616 passed.
- Mutants: 66 one-line mutants in four batches, applied one at a time to the copy only. 35 were killed (24 of the kills were deliberate controls on behaviour the tests are meant to pin, which shows the harness detects mutants); 31 survived. Of the survivors, 4 are equivalent or no-op by construction (M22, P8, Q4, Q5) and 1 sits on dead code (Q1); the other 26 are reported below. The copy was deleted afterwards. A `find -newer` check found no file in the repo changed during the review.
- The spawn prompt carried no `## Inherited Structural Verdict`, so structural re-checking fell back to standalone behaviour (see Self-Audit).

Answers to the specific questions in the lens prompt:

| Question | Answer | Evidence |
|---|---|---|
| Is a test deriving its expectation from the code under test? | Only in minor ways (TA-m3). Almost all expectations are literals; `k = 8`, `35/3` and the 29-reason exit table are pinned by literals. | `test_cycle.py:3449-3450`, `4114`, `901-902` |
| Wall clock, real HOME, network, real subprocess, path outside `tmp_path`? | None found. `FakeClock` everywhere; autouse fixtures set HOME and XDG and replace `_read_mountinfo`; `SubprocessRunner.run` is replaced by a raiser in `test_cli.py`; `/zz-mnt` is never created. | `test_cycle.py:53-58`, `test_cli.py:51-73` |
| pytest-xdist? | Safe: 616 passed with `-n 4`. | Bash run |
| Any pytest marker? | No custom marker (matches DF-12 and design C12). The built-in `parametrize` is used 61 times and `skipif` 5 times (TA-m1). | `grep` counts 47 + 12 + 2; `test_cycle.py:728`, `test_cli.py:745,848,1036,1402,1428` |
| Can the scripted world hide an unexpected argv? | No: `gh_world` and `fake_runner` assert `not runner.unexpected` at teardown (`conftest.py:104-116`, `862-889`), `FakeLauncher` fails on an exhausted outcome list, and `test_cli.py` makes any real `SubprocessRunner.run` raise. The only unguarded runner is `make_deps`' default `FakeRunner`, and its one use asserts `calls == []` (`test_cli.py:532`). | as cited |
| Do `test_fifty_cycles` and `test_acceptance_property` truly assert at most one launch per issue and per cycle? | Yes. Per cycle: `made in (0, 1)` on launcher calls (`test_cycle.py:3989`, `4030`). Per issue: `len(numbers) == len(set(numbers))` over launcher prompts (`3999`, `4059`) plus `entry.launches <= 1` (`3994`). Mutants that break S1 (launch twice in a cycle) are killed by them (`assert 2 in (0, 1)`); a mutant that stops `mark_pending` accepting a `failed` entry is also killed by `test_fifty_cycles`. | mutants S1-no-halt-after-spawn_error, M3b, M17 |

## Items Reviewed

Adapted to the lens: each row is a behaviour group the prompt lists, answered by "does a test exist that would FAIL if it broke". Result PASS means every mutant I tried on that group was killed (or survived only as a minor note).

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Cycle step 1: platform, config, `enabled`, approvers, worktree | none | PASS | `test_cycle.py:91-378` (`INVALID_CONFIGS`: one case per rule, literal fragments), `589-796` (approvers table), `1434-1482` (`not_enabled`, exit 2 with zero gh calls). Minor: TA-m5, TA-m6. |
| 2 | Step 1 network-FS check reader (`_read_mountinfo`, `_MOUNTINFO`) | AX-3 | FAIL | Autouse fixture replaces the reader in every test (`test_cycle.py:58`, `test_cli.py:61`); mutant M7 (`_MOUNTINFO` set to `/proc/self/mountstats`) survived. See TA-8. |
| 3 | Steps 2 and 3: lock held, lock missing or invalid, `DISABLED` | none | PASS | `test_cycle.py:1373-1431`, `1502-1551`; mutant P5 (rotate while lock held) killed. Minor: TA-m7. |
| 4 | Step 4: store load, migration, `next_permitted_at` | AX-3 | FAIL | Rate-limit window tests pass (`1734-1780`), but the migrated-store branch `cycle.py:720-721` has no test; mutants M2a, M2b survived. See TA-4. |
| 5 | Step 5: login, `owner_account_id`, login regex, skew 60 and 61 s | none | PASS | `1302-1365`, `1689-1726`; mutants M20, N-login-logged-when-invalid, P9 killed. |
| 6 | Step 6: origin check at cycle start and re-check before `pending` | none | PASS | `1485-1499`, `3410-3432`; mutant P10 killed. The deadline guard on these calls is row 18. |
| 7 | Steps 7 to 9: sweep, discovery (79/80, 99/100/101, duplicate), candidate order | none | PASS | `1613-1686`, `3530-3558`, `3649-3672`; mutants N-cap-candidates-11, P2 killed. Minor: TA-m8. |
| 8 | Steps 10 and 11: every skip reason, claimed paths, tombstones, `in_backoff`, `day_cap` | none | PASS | 22 `SKIP_CASES` (`2267-2441`), `2496-2878`; mutants M16, Q7, C3 killed. Minor: TA-m9, TA-m10. |
| 9 | Step 12 order and durability: probe, prompt, re-read with 3 reserved calls, `pending` saved before launch | none | PASS | Literal `_LAUNCH_TRACE` and literal `dispatch.json` entry at launch time (`2884-2942`), `4111-4153`; mutants C1, P10, Q2, Q3, Q6 killed. |
| 10 | Step 12 / S1: after one launch-step outcome later candidates are neither read nor stamped | AX-3 | FAIL | Tested only for `launched`, `launch_unknown`, `revalidation_transient`, `disabled_mid_cycle`, `origin_mismatch`; mutants for `revalidation_failed` (M3a), `prompt_invalid`, the 120 s cut-off `budget_exhausted` (M3c) and the re-read assignee skips survived. See TA-5. |
| 11 | FR-016 case (a) and (b) | none | PASS | `3441-3510` (k = 8, cycle 2 starts with the 7 unexamined; 15 eligible launch exactly 1); mutants S1-no-halt-after-launched, N-cap killed. |
| 12 | Step 13: final save and exit 6 `state_dir_unwritable` (also the `pending` save) | AX-3 | FAIL | No `OSError` is injected anywhere in `test_cycle.py`; mutants M1 and M1b survived. See TA-1, TA-2. |
| 13 | Step 14: health stamp only for a clean, real, non-disabled cycle | none | PASS | `1298`, `1430`, `1446`, `3010`, `3392`; mutants N-health-stamp-on-exit-nonzero killed. |
| 14 | Step 15: decision lines then cycle line, rotation, stderr fallback when the audit write fails | AX-3 | FAIL | Order and rotation are pinned (`1405-1415`, `2008`; P5, P6 killed) but the `except OSError` fallback (`cycle.py:1145-1146`) has no test; mutant M1c survived. See TA-3. |
| 15 | Exit codes 0, 2, 3, 4, 5, 6, 7, 75 and precedence | none | PASS | `806-864` (every subset of `{2,3,4,5,6,7,75}`), `1982-2011`, `901-902` literal 29-row table. Exit 6 by write failure is in row 12. |
| 16 | Dry-run rules: no `dispatch.json` write, shadow file, would-launch decision, probe skipped, no rate-limit persistence | none | PASS | `3587-3806`; mutants N-dry-run-writes-store, N-shadow-reset-no-warning, M21 killed. Minor: TA-m8. |
| 17 | Rate-limit rule: persistence, 3600 s clamp, 119/120 s window, per-call clamp | none | PASS | `1734-1872`, `3222-3235`; mutant N-rate-clamp-reread-removed killed. Minor: TA-m13. |
| 18 | Deadline rule: 240 s total, 5 s floor, 236 s, 120/121 s cut-off, no `None` timeout reaching a Runner | AX-3 | FAIL | Arithmetic and gh calls are well tested (`920-1036`, `1880-1975`), but the `None` guards on the git origin check and the Orca probe are not (M4a, M4b survived). See TA-6. |
| 19 | Config table and approvers table rows | none | PASS | Every row of design 4.2 and its five approvers rules has a literal case; see row 1. |
| 20 | Commands: five names, exit codes, `status` read-only and field set, `check-config`, `init-state` | none | PASS | `test_cli.py:266-836`, `991-1088`; mutants M19, P3, P7 killed; M6 (status takes the lock) killed only by a side effect (TA-m11). |
| 21 | Production wiring: `cli.build_deps` | AX-3 | FAIL | Replaced by a raiser in an autouse fixture (`test_cli.py:68-72`) and by fakes in every test; mutants M5a, M5b, M5c survived. See TA-7. |
| 22 | `reset`: every exit, exactly one audit line, never a cycle line | none | PASS | `test_cli.py:1094-1443` (exact-dict `one_line` checks); mutants M18 killed. Minor: TA-m14. |
| 23 | SLO helper (a) p95, (b) 7-day exit-0 share, (c) claimed within lease, (d) stale count | AX-3 | FAIL | (a), (d) and the lease end are pinned with hand-worked literals; the negative case "claim earlier than the launch" is missing (M11 survived). See TA-9. |
| 24 | Isolation: wall clock, real HOME, network, real subprocess, paths outside `tmp_path`, xdist, markers | none | PASS | See the question table; xdist run 616 passed. Minor: TA-m1. |
| 25 | Scripted world cannot hide an unexpected argv | none | PASS | `conftest.py:104-116`, `862-889`. |
| 26 | Vacuous assertions and expectations derived from the code under test | none | PASS | Two weak assertions and three derived expectations, all minor: TA-m3, TA-m4. |
| 27 | `test_fifty_cycles` and `test_acceptance_property` assert at most one launch per issue and per cycle | none | PASS | See the question table. |

## Summary
- Checks passed: 19 / 27
- Checks failed: 8 (covering 9 blocking findings)
- Critical issues: 0 CRITICAL, 9 IMPORTANT (all blocking), 16 MINOR
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status: drift-axis-inactive (no BUILD_REQUEST.GOAL verbatim was in the spawn prompt or in the change-set file, so AX-1 was disabled; AX-2 to AX-5 were applied)

## Issues Found

### Blocking findings

Severity IMPORTANT = blocking (wrong behaviour or a safety rule left unproven by any test). "Mutant" means the one-line change named in Method, applied to a copy in `/tmp`; the three test files still passed (616 passed).

| id | severity | file | evidence | expected versus actual |
|---|---|---|---|---|
| TA-1 | IMPORTANT (blocking) | `src/superclaude/cli/issue_watch/cycle.py:582-587` (`_save`); `tests/issue_watch/test_cycle.py` | Mutant M1 replaced `except OSError: raise _Stop("state_dir_unwritable") from None` with `except OSError: pass`: 616 passed. No test injects an `OSError` into `store.save`; `OSError` appears in `test_cycle.py` only inside a reason-table row (line 890). `CrashingStore` (`conftest.py:124-180`) raises `SystemExit`, not `OSError`, and no Phase 6 or 7 test uses it. | Expected: a test where the `pending` save raises `OSError` and asserts `launcher.calls == []`, exit 6 `state_dir_unwritable` and no `launched` line (FR-010; security rule "no cycle path launches without first saving a pending entry"). Actual: the guard that stops a launch when the durable write fails is unproven. A swallowed error would launch with nothing recorded, and the same issue could launch again (NFR-005). |
| TA-2 | IMPORTANT (blocking) | `cycle.py:1060-1088` (`_commit`, `_commit_store`); `test_cycle.py` | Mutant M1b replaced `except OSError: self._stopped("state_dir_unwritable")` with `pass`: survived. Exit 6 `state_dir_unwritable` is reached in tests only through `exit_for` (`test_cycle.py:890`) and, for `init-state` and `reset`, through chmod tests that are skipped under root (TA-m1). | Expected: a cycle-level test where the final save fails: exit 6, reason `state_dir_unwritable`, no cycle line in `audit.jsonl` (stderr fallback only, `cycle.py:1139-1140`), no health stamp, and `once` printing `exit: 6`. Actual: the exit-6 write-failure row of design 4.3 and step 13 has no cycle-level test. |
| TA-3 | IMPORTANT (blocking) | `cycle.py:1138-1146` (`_conclude`); `test_cycle.py` | Mutant M1c replaced the `except OSError: audit.stderr_fallback(...)` body with `raise`: survived. The task file (line 975, PRE-3) asked for this case in Step 6.6; `grep OSError test_cycle.py` finds none. | Expected: with `audit.jsonl` unwritable (for example a directory in its place) `run_cycle` returns the same exit code, writes one stderr line with exactly the keys `kind, ts, host, exit, reason`, and still saves the store (FR-020, AC-14). Actual: the fallback wiring is unproven (`test_audit.py` tests the line builders, not this call site). |
| TA-4 | IMPORTANT (blocking) | `cycle.py:720-721` (`_load`); `test_record.py:532-571`; `test_cycle.py` | Mutants M2a (`if False:`) and M2b (drop `not self.dry_run`) both survived. DF-17 says a real cycle saves a migrated store and a dry-run migrates in memory and never saves (FR-019 byte-identity). The decision row names `test_record.py` for "v0 fixture + dry-run: bytes unchanged", but those tests only exercise `FileStore.migrated`; `grep migrated tests/issue_watch` finds only `test_record.py` and the `CrashingStore` property in `conftest.py`. No test calls `run_cycle` on a store whose `migrated` is true. | Expected: two cycle tests over `FileStore(dir, migrations={0: v0_to_v1})` and a version-0 file: the real cycle rewrites it at version 1, the dry-run leaves the bytes unchanged. Actual: neither exists; a dry-run that rewrites the store would break FR-019 unnoticed. |
| TA-5 | IMPORTANT (blocking) | `cycle.py:806-807` (S1 halt); `test_cycle.py:1947-1962`, `3070-3090`, `3129-3311` | Four mutants survived: no halt after `revalidation_failed` (M3a); no halt after `prompt_invalid`; no halt after `budget_exhausted` at the 120 s cut-off (M3c); no halt after a re-read `assigned_other` or `unassigned`. The multi-candidate S1 checks cover only `launched` (`3480`), `launch_unknown` (`3093`), `revalidation_transient` (`3178`), `disabled_mid_cycle` (`3362`) and `origin_mismatch` (`3410`). Every `revalidation_failed`, `prompt_invalid`, 121 s and re-read-assignee test uses `world.issue(9)` alone. (`spawn_error` is killed only incidentally, by `test_fifty_cycles`.) | Expected (design 6.3, FR-016): after any launch-step outcome later candidates are neither read nor stamped; each of these outcomes with issues 9 and 10 should assert `_touched(world) == {9}` and `considered == {9: ...}`. Actual: a regression would read and stamp issue 10 in the same cycle (extra gh calls, and a second launch attempt in one cycle) with no failing test. |
| TA-6 | IMPORTANT (blocking) | `cycle.py:651-657` (`_origin_ok`), `1009-1012` (probe); `test_cycle.py` | Mutants M4a (origin `None` guard removed) and M4b (probe `None` guard removed) survived. `FakeRunner` accepts a `None` timeout and only four assertions look at the timeouts that reach it (`test_cycle.py:1887`, `1897`, `1931`, `2928`). No case brings the clock under 5 s left before the origin check, the probe or the second origin check. | Expected (FR-029, design 8.5: "the caller must test for None before it calls a Runner"): a case that advances the clock past 235 s before each of those calls, plus an invariant checked for every scripted cycle that no recorded timeout is `None` or above the time left. Actual: untested; in production `SubprocessRunner.run(timeout=None)` would wait without limit past the 240 s budget. |
| TA-7 | IMPORTANT (blocking) | `cli.py:61-73` (`build_deps`); `test_cli.py:68-72`, `453`, `477`, `490`, `527`, `552` | Mutants M5a (`which` replaced by `lambda name: None`), M5b (audit log pointed at another directory) and M5c (store pointed at another directory) all survived. An autouse fixture replaces `cli.build_deps` with a raiser and each `once` test replaces it again, so the real function never runs. | Expected: one test that calls the real `cli.build_deps(config)` (with `SubprocessRunner.run` still guarded) and asserts the store and audit log use `config.state_dir`, the launcher is an `OrcaLauncher` over the same runner, `which` is `shutil.which`, the clock is `SystemClock` and `host` is `socket.gethostname()`. Actual: the only production assembly of `Deps` (DF-45) is never executed by a test. |
| TA-8 | IMPORTANT (blocking) | `cycle.py:77`, `178-184` (`_MOUNTINFO`, `_read_mountinfo`); `test_cycle.py:58`, `test_cli.py:61` | Mutant M7 (`_MOUNTINFO = "/proc/self/mountstats"`) survived. An autouse fixture replaces `_read_mountinfo` in every test, so the real reader and the path constant are never run. | Expected: a test that points `cycle._MOUNTINFO` at a tmp file holding an `nfs4` line and one at a missing file, and checks `_read_mountinfo()` returns the text and `None`. Actual: with a wrong path the network-filesystem check (design 4.2, DF-23, DF-52) would silently never run (fail open) and the suite stays green. |
| TA-9 | IMPORTANT (blocking) | `cycle.py:1341` (`slo_numbers`); `test_slo_helper.py:274-312` | Mutant M11 (`at <= c < end` changed to `c < end`) survived. Every claim in the tests is at or after its launch. | Expected: a case with a `claimed` line one second before the `launched` line of the same issue and a due lease, giving share `0.0` (the rule is "reached `claimed` before `lease_expires_at`" for that launch). Actual: a claim from an earlier launch of the same issue (realistic after `reset N` and a second launch) would count for the later launch and inflate NFR-013 number (c) with no failing test. |

### Minor notes (never fail the review; not rechecked)

| id | file | note |
|---|---|---|
| TA-m1 | `test_cycle.py:728`; `test_cli.py:745`, `848`, `1036`, `1402`, `1428` | No custom marker is used (DF-12, design C12). The built-in `parametrize` is used 61 times, which is not a new marker. Five tests carry `skipif(os.geteuid() == 0)`. Under root (common in container CI) they skip silently, and they are the only tests of the `init-state` and `reset` write-failure exits. A deterministic `OSError` injection would not need `skipif`. |
| TA-m2 | `test_cli.py:1114` | `assert (fb["ts"], fb["host"]) != ("", "")` is almost always true. Assert the literal `ts` and host as the other reset tests do. |
| TA-m3 | `test_cycle.py:1049`; `test_cli.py:1245` | The rotation size is taken from `audit.ROTATE_BYTES` instead of a literal (`_PADDING`), so these tests would still pass if the constant changed. `check_line_kinds` and `test_exit_and_kind_follow_reason_table` use `audit.REASON_TABLE`, but a literal 29-row table backs them (`test_cycle.py:867-902`). Scripted argv come from `github.argv_*`; `test_github.py` pins argv literally (15 hits). |
| TA-m4 | `test_cycle.py:1292`, `2022-2060`; `cycle.py:1115-1118` | The rule "a clean cycle's reason is the last decision's reason, or `not_approved` when nothing was examined" is pinned by a literal, but no spec or design text defines it (the code comment calls it an open question). Fine as a record of today's behaviour; revisit if the owner decides otherwise. |
| TA-m5 | `cli.py:117-128`; `test_cli.py` | Mutant M14 (`once` loads the config with `platform=False`) survived. Platform refusal is tested for `check-config`, `init-state` and `reset` only. |
| TA-m6 | `cycle.py:664-669` | Mutant M10 (validate setup before the `enabled` check) survived. No test has `enabled: false` with an invalid approvers file. |
| TA-m7 | `cycle.py:691` | Mutant M15 (`DISABLED` ignored in a dry-run) survived. No dry-run test has `DISABLED` present. |
| TA-m8 | `cycle.py:751-766` | Mutant P4 (a dry-run does not keep the sweep result in memory) survived. No dry-run test has an orphaned `pending` entry for an issue that is also discovered. |
| TA-m9 | `test_cycle.py:1172-1175`, `1558-1587` | The `project_read_failed` stop is asserted for exit and reason only; the decision line and the "not stamped" rule are not (mutant N-scope-missing-stamps survived). |
| TA-m10 | `cycle.py:922-927`; `test_cycle.py:2351` | Mutant M8 (`unchanged_since` called with `own_login=""`) survived. Only a foreign comment is tested; an own-login comment after the approval, which must not block, is not. |
| TA-m11 | `cli.py:155-173`; `test_cli.py:730-734` | Mutant M6 (`status` takes the lock) is killed only by a side effect (`test_status_exits_6_for_a_missing_store` has no lock file). No test runs `status` while the lock is held. |
| TA-m12 | `cycle.py:1086`, `1023-1024` | Mutant P1 (no `consumed_log` prune at commit) survived. The second `_day_cap_reached()` check (mutant Q1) cannot fire, because the in-memory document cannot gain launches between the two checks; it is dead code and cannot be tested. |
| TA-m13 | `conftest.py:703-720`; `github.py:418-431` | `GhWorld` can only set `Retry-After` and `Date` on the G1 reply, so the `x-ratelimit-reset` branch of `rate_limit_wait` is not reachable from a cycle test. |
| TA-m14 | `test_cli.py:1203-1240`; `record.py:706-720` | `reset` is tested with `consumed_at` 5 h old only. `reset_entry` appends `consumed_at` and then prunes at once, so an entry consumed 24 h or more ago leaves no `consumed_log` evidence; no test pins that. |
| TA-m15 | `test_slo_helper.py:254-258`, `303-312` | Mutants M12 (lease end exactly `now`) and M13 (a cycle line exactly 7 days old) survived; the tests use 50 minutes of open lease and 167 h and 7 d 1 h. |
| TA-m16 | `cycle.py:635-641`; task file lines 474, 507, 960 | (a) `note: "re-approved"` is emitted but never asserted (mutant M9 survived), while open question OQ-49 says no code emits it. (b) Step 6.6 asks for "a `failed` entry written earlier in the same cycle stands"; the test uses a swept `pending_orphan` entry (`test_cycle.py:1846-1872`), because S1 halts after a `failed` write, so exit 7 together with 5 cannot happen in `run_cycle` although design 4.3 says it can. (c) Step 7.4 says the AC-9 `argv[0]` equals the resolved path; the test pins the bare name `orca-ide` (`test_cli.py:813`), which matches the code. |

## Actions Taken
None. `fix_authorization` was false. The only files written are this report and scratch files under `/tmp/gc-mut-ta`, which were removed. A `find -newer` check showed no file in the repository changed during the review.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
The spawn prompt carried no `## Inherited Structural Verdict` section, so no rf-qa PASS was relied on. The Gate A and Gate B results and the Phase 6 and 7 gate results in `gate-c-change-set.md` (2098 and 2224 passed) were not taken as evidence either: I re-ran the three test files myself on a copy (616 passed) and then mutated that copy.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was supplied; standalone behaviour applied.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Does any test fail if the `pending` save, the final save or the audit write fails? -- tried mutants M1, M1b, M1c on a `/tmp` copy of `cycle.py`; all survived (TA-1 to TA-3).
- Does the S1 halt hold for every launch-step outcome? -- tried 9 mutants of `cycle.py:806-807` (one or more per outcome); the ones for `revalidation_failed`, `prompt_invalid`, 120 s `budget_exhausted` and re-read assignee skips survived, the other five (`launched`, `launch_unknown`, `revalidation_transient`, `spawn_error`, and the combined `prompt_invalid` plus `spawn_error`) were killed (TA-5).
- Is the migrated-store rule (DF-17) tested at cycle level? -- `grep migrated` over `tests/issue_watch` and mutants M2a, M2b; nothing calls `run_cycle` on a migrated store (TA-4).
- Is the real `build_deps` and the real mountinfo reader run? -- `grep build_deps` in `test_cli.py` (always replaced) and mutants M5a to M5c, M7 (TA-7, TA-8).
- Do the controls work? -- 24 deliberate mutants on behaviour the tests claim to pin (for example `elapsed() <= 120` to `< 120`, `used >= DAY_CAP` to `>`, no `pending` save) were all killed, so the surviving mutants are real gaps and not harness failures.
- Is the suite safe under pytest-xdist and free of wall-clock, HOME, network and subprocess use? -- ran the three files with `-n 4` (616 passed) and read the autouse fixtures (`test_cycle.py:53-58`, `test_cli.py:51-73`).
- If you told the user the review found 0 issues, would they believe it? -- not applicable: 9 blocking findings, each with a failing-to-fail mutant they can re-run.
- Web research: none was needed, so no Tavily or fallback call was made.

## Recommendations
- Fix cycle 1 (tests only, no change to `cycle.py` or `cli.py` is needed): add the nine missing tests, in this order of value: TA-1 and TA-2 (a `Store` wrapper whose `save` raises `OSError` on call 1 and on the final call), TA-3 (audit log path is a directory), TA-5 (issues 9 and 10 for `revalidation_failed`, `prompt_invalid`, the 121 s cut-off and the re-read assignee skips), TA-4 (version-0 store, real and dry-run), TA-6 (clock past 235 s before the origin check and the probe, and a `timeouts` invariant in `GhWorld`), TA-7 (real `build_deps`), TA-8 (`_MOUNTINFO` pointed at a tmp file), TA-9 (claim before launch).
- Replace the root-dependent `skipif` write-failure tests with the same `OSError` injection (TA-m1) so exit 6 is covered when the suite runs as root.
- Re-run the mutants of this report after the fix (the scripts are not kept; each mutant is the one-line change named in the finding) and expect every blocking mutant to be killed.
- Minor notes need no action for the gate to pass.

## Confidence Gate

- **Confidence:** Verified: 27/27 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 25 | Grep: 26 | Glob: 3 | Bash: 8 (Read + Grep + Glob = 54, above the 27 checks)
- Unchecked items: none. Unverifiable items: none.
- Verdict rule: confidence is at least 95% with nothing unchecked, so a PASS would have been allowed; the verdict is FAIL because of the nine blocking findings, not because of coverage of the review.

## QA Complete

