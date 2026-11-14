# QA Report - Determinism lens (T230)

**Date:** 2026-11-12
**Phase:** tests gate, determinism lens (adversarial, fix_authorization: false)
**Scope:** tests/sweep/ (all files), src/superclaude/cli/sweep/, result maps in phase-outputs/test-results/

## Method

Every cited line was read from disk during this review. The sweep tests were run only through
`uv run pytest tests/sweep -v` (twice, in the repository). Every perturbation (reverse and rotated
order, each test alone, time zone, locale, hash seed, shifted wall clock, stalled Budget clock,
odd temp folder, scrubbed environment, repeated runs in one process) ran from a private copy under
`/tmp/t230-work` (tests, the sweep source, `contracts/`, `pyproject.toml`, `.gitignore`) with the
repository's own `.venv/bin/pytest` and a private plugin file `t230shift.py` that lives only in
that copy. No repository file was edited and no live Orca, ccsession or Claude command ran. The
copy and its logs were deleted at the end.

Baseline: `uv run pytest tests/sweep -v` printed `559 passed` on run 1 and run 2 (1.78 s and
1.81 s, `/tmp/t230-run1.txt`, `/tmp/t230-run2.txt`, since deleted). `ruff check` and
`ruff format --check` on `src/superclaude/cli/sweep tests/sweep` both exit 0 ("All checks passed!",
"15 files already formatted").

## Experiments (private copy; every row is the full 559-test suite unless noted)

| # | Perturbation | Result |
|---|--------------|--------|
| E1 | second run, same order, in the repository | 559 passed; `git status` of `tests/sweep` and `src/superclaude/cli/sweep` unchanged |
| E2 | node ids in reverse order | 559 passed |
| E3 | node ids rotated by half | 559 passed |
| E4 | each of the 6 test files alone | 159 / 90 / 3 / 242 / 24 / 41 passed (sums to 559) |
| E5 | every one of the 559 tests alone, own process, 8 in parallel | 0 failures |
| E6 | whole suite 2x and 4x in one process (`--keep-duplicates`) | 1118 and 2236 passed |
| E7 | `TZ` = Pacific/Kiritimati (+14), America/Adak (-10), Asia/Kolkata (+5:30), UTC | 559 passed each |
| E8 | `LC_ALL`/`LANG` = C, C.utf8, en_US.utf8; `PYTHONUTF8=0`, `LANG=C` | 559 passed each |
| E9 | `PYTHONHASHSEED` = 0, 1, 2, 3, 99, 4242 | 559 passed each |
| E10 | wall clock seen by `probes._utcnow` and `commands.datetime` set to 2026-11-08T12:00:00Z, +0.5 s, 1970-01-01, 2036-01-01, now-400 d, now+3650 d, now-8.6 s | 559 passed each (control: the shift changes report names and the header, `20261112-...` to `19700101-000000`, so it is effective) |
| E11 | `Budget` default clock stalled so 5 s or 85 s of the 90 s budget are gone | 559 passed each |
| E12 | `Budget` default clock stalled so 200 s are gone (a host that freezes for more than 90 s) | 18 failed, see F1 |
| E13 | scrubbed environment (`env -i`), `ORCA_CLI_COMMAND=/bin/false`, `XDG_STATE_HOME` set, `COLUMNS=20 NO_COLOR=1 TERM=dumb`, `umask 0`, `umask 077`, cwd `/` | 559 passed each |
| E14 | run from the copy, which has no `.git` above the tests | 559 passed (the repository run, which has one, also passed) |
| E15 | `TMPDIR` containing a space | 2 failed, see F3 |
| E16 | `TMPDIR` containing non-ASCII letters (`ü ñ`, no whitespace) | 559 passed |
| E17 | `click` 8.1.8 in an isolated env: `CliRunner().invoke(...).stderr` | raises `ValueError: stderr not separately captured`, see F5 |
| E18 | `TMPDIR` is a symlink to the real folder | 559 passed |
| E19 | `TMPDIR` 286 characters long | 18 failed and 8 errors (`OSError: [Errno 36] File name too long`), see F3 |

## Findings

No BLOCKING and no MAJOR finding. Six MINOR findings; none changes the outcome of a normal run. The
suite is deterministic on every perturbation that a host normally differs by (E1 to E11, E13, E14,
E16, E18). The findings below are the places where the suite is still tied to the host.

**F1 - MINOR - 18 tests read the real monotonic clock (E12).**
`Budget.__init__` defaults `clock=time.monotonic` (`src/superclaude/cli/sweep/probes.py:116`) and
`call_timeout()` returns None, that is "time budget reached", once less than 1 s of the 90 s total
is left (`probes.py:169-175`). `commands.run` builds `probes.Budget()` with no clock
(`src/superclaude/cli/sweep/commands.py:263`), so every `CliRunner` test uses the real clock.
Two tests build a default `Budget` themselves: `tests/sweep/test_classify.py:1743` and
`tests/sweep/test_readonly.py:120`. With a Budget clock that reports 200 s gone after its first
read (E12), these 18 tests fail: `test_classify.py::test_fr015_untracked_path_in_a_package_folder_marks_it_active`;
in `test_cli_contract.py`: `test_duplicate_run_ids_collapse_to_one_worker_list_argv`,
`test_duplicate_run_ids_keep_first_seen_order`, `test_unknown_run_then_a_second_run_reads_both_and_exits_0`,
`test_binding_1_no_run_and_first_call_failure_exits_2_with_one_argv`,
`test_binding_2_explicit_run_and_first_call_failure_publishes_and_exits_0`,
`test_binding_3_binding_then_second_call_failure_publishes_and_exits_0`,
`test_binding_4_captured_no_binding_shape_exits_2_and_reads_nothing_else`,
`test_fr005_three_workers_two_worktrees_one_person_session`, `test_fr005_summary_reconciles`,
`test_fr005_historical_rows_reconcile_with_visible_ones`, `test_golden_v1_keys_and_types_at_every_level`,
`test_waiting_lists_hold_row_ids_only`; in `test_readonly.py`:
`test_collect_makes_one_git_call_per_worktree_that_ps_reports[root-only|one-more|two-more]`,
`test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree`,
`test_a_sweep_starts_no_process_and_records_only_allowlisted_argv`. An 85 s stall (5 s left) still
passes (E11), so only a host that freezes a test for about 90 s flips them; the whole suite takes
1.8 s, so this is a latent risk, not an observed flake.
Fix (smallest): one autouse fixture in `tests/sweep/conftest.py` that replaces `probes.Budget` with
a subclass whose default `clock` is a fixed counter; keep an explicit `clock=` untouched.

**F2 - MINOR - the wall clock stamps `collected_start`/`collected_end` in every `collect` and CLI test; nothing injects it.**
`probes._utcnow` returns `datetime.now(timezone.utc)` (`probes.py:994-995`); `collect` calls it for
`started` (`probes.py:1244`) and `collected_end` (`probes.py:1313`). No test references `_utcnow`
(grep of `tests/sweep`: 0 hits). `test_cli_contract.py:92-97` patches only `commands.datetime`, so a
CLI report header reads `observed 2026-11-08T12:00:00Z . collected 2026-11-12T05:30:10Z to
2026-11-12T05:30:10Z` (header printed by `report.py:173-175`; produced by running
`test_report_name_is_the_utc_second_with_the_sweep_suffix` in the copy). The same wall-clock value
feeds the classifier: `classify._window` ends a live Dispatch window at `collected_start`
(`classify.py:548-549`) and `classify_all` passes `inp.collected_start` to the join
(`classify.py:871-873`); `_read_contracts` ages a contract against it (`probes.py:1285`, `1346`).
`test_readonly.py` is worse: its `sweep_env` (lines 303-347) patches neither clock seam, so the
observed time and the report file name come from the real clock too; the test only matches the
name with a regex (`test_readonly.py:380`).
No assertion depends on the value today: seven different clocks, including 1970-01-01 and
2036-01-01, all give 559 passed (E10). It is still a breach of "uses the fixed now or an injected
clock" and a trap for the next assertion on `collected` or on a pending Dispatch's join.
Fix (smallest): an autouse fixture that sets `probes._utcnow` to return `fixed_now`, and
`commands.datetime` to the `_Clock` of `test_cli_contract.py:92-97` (move it to `conftest.py`).

**F3 - MINOR - two tests, and under a very long folder 26, depend on the shape of the temp folder.**
(a) `_CONTRACT_PATH_RE` stops at whitespace, quotes, backticks, `<`, `>` and parentheses
(`probes.py:1014`). `_stock_contract_run` writes the pytest `tmp_path` into a Task spec
(`test_probes_allowlist.py:1444`). A temp path with any of those characters (the folder name comes
from `TMPDIR` and from `pytest-of-<user>`) makes the contract "outside root" and fails
`test_a_contract_over_1_mib_is_unscanned_with_a_reason` (`test_probes_allowlist.py:1349-1359`) and
`test_a_contract_that_changes_on_every_read_is_an_inconsistent_observation` (`:1666-1687`) (E15).
(b) `SweepRoot.transcript` names a folder after the whole worktree path with every non-alphanumeric
character as `-` (`tests/sweep/conftest.py:288-291`); a name over 255 bytes raises `ENAMETOOLONG`.
With a 286-character `TMPDIR` that fails 18 tests and errors 8 (E19). A `TMPDIR` with non-ASCII
letters or a symlink is fine (E16, E18).
Fix (smallest): in the fixtures, `pytest.skip` with a reason when the path holds one of the regex's
stop characters or the key is longer than 255 bytes; or run with a short `--basetemp`.

**F4 - MINOR - the one integration test depends on the host's git.**
`test_real_git_lock_free_status_and_gitignore` is skipped only when git is missing
(`test_readonly.py:472`) but runs `git init -q -b main` (`:488`), which needs git 2.28 or newer, and
reads the repository's own `.gitignore` (`:489`; the rule is at `.gitignore:255-256`). The host has
git 2.47.3, so it passes here (and in the copy, E1 to E14).
Fix: skip below git 2.28 with a reason, or `git init` then `git symbolic-ref HEAD refs/heads/main`.

**F5 - MINOR - the CLI tests need click 8.2 or newer, the dependency range allows 8.0.**
The tests call `CliRunner()` with no `mix_stderr` and read `result.stderr`
(`test_cli_contract.py:176`, `181-182`, `192`, `1226`). `pyproject.toml:36` declares `click>=8.0.0`;
`uv.lock:108-109` pins 8.5.1, which is why the suite passes. With click 8.1.8 `.stderr` raises
`ValueError: stderr not separately captured` (E17), so every test that reads it would fail the same
way, every time (not a flake).
Fix: raise the floor to `click>=8.2` in `pyproject.toml`.

**F6 - MINOR - two statements in the result maps are looser than the evidence.**
`test-probes-allowlist.txt:263` says "No test starts a process or waits on a real clock ... Budget
tests use FakeClock." No test waits, but 18 tests read the real clock (F1) and none fixes
`_utcnow` (F2). `test-cli-registration.txt:27` says "reverse file order with -p no:randomly: 469
passed"; pytest-randomly is not installed (`phase10-validation.md:79` lists the plugins:
`superclaude-5.0.0, anyio-4.16.0`), so the flag does nothing, and 469 is the old count (559 now).
Fix: reword both lines.

Notes (not findings): (1) Seven tests read the sweep source by `Path(__file__).resolve().parents[2]`
(for example `test_classify.py:1844-1847`); they fail when `tests/` is copied without `src/` (the
first pass of my copy, 7 failures, then 1 until `contracts/` was added). They do not depend on the
current folder (E13, cwd `/`). (2) `_temp_path` uses `os.getpid()` (`test_cli_contract.py:211`) and
matches `commands.py:168` only because `CliRunner` runs in the same process; a forked runner would
break it, but nothing forks. (3) The three monkeypatches of `os.link`, `os.unlink`, `os.write` act on
the shared `os` module and answer only a call made from `commands` (`test_cli_contract.py:232-245`),
so they leak nothing to other tests (E2 to E6).

## Not covered

I did not run the suite on macOS or Windows, on Python 3.10 or 3.12, under pytest-xdist, with git
older than 2.28, or on a folder that refuses hard links. The last one matters: the real `_publish`
publishes with `os.link` (`commands.py:186`), and `test_exit_code_0_means_the_report_was_published`
asserts `st_nlink == 1` (`test_cli_contract.py:1122`), so a temp folder on a file system without
hard links (some network or container mounts) would fail every publish test. That is a property of
the product design (the link is the commit point), so I list it here and not as a finding. A click
version below 8.2 was checked only with a 6-line probe (E17), not with the suite.

## Self-Audit

1. Independent verifications (counts are approximate): the 19 experiments (E1 to E19, 559 tests
   each, E5 as 559 separate runs), about 25 source citations re-read (`commands.py`, `probes.py`,
   `classify.py`, `report.py`), about 14 test-file regions re-read (`conftest.py`,
   `test_cli_contract.py`, `test_cli_registration.py`, `test_probes_allowlist.py`,
   `test_readonly.py`, `test_classify.py`, `test_report.py`), and about 12 whole-tree greps (clock,
   sleep, thread, random, tempfile, ordering, environment, mtime, chmod, symlink, `_utcnow`,
   `Budget(`).
2. Files read: `tests/sweep/conftest.py` (all 334 lines), `test_cli_registration.py` (all),
   `test_readonly.py` (all 528 lines), `test_cli_contract.py` lines 1-1409 (all, 150 at a time),
   `test_probes_allowlist.py` lines 100-290, 1100-1260, 1320-1380, 1436-1470, 1555-1700,
   `test_classify.py` lines 90-240 and 1700-1850, `test_report.py` lines 570-630;
   `src/superclaude/cli/sweep/{__init__,commands,probes,classify,report}.py` in the ranges cited;
   `phase-outputs/test-results/phase10-validation.md` (all) and the heads, tails and determinism
   lines of the six result maps; `tests/conftest.py` by grep; `pyproject.toml`, `.gitignore`,
   `uv.lock` by grep. The rest of the six test files (about 4,000 lines of case bodies) was covered
   by whole-tree grep and by the experiments, not by a line-by-line read; an outcome that depends on
   the host would have shown in one of the experiments, which ran every test.
3. This is not a 0-issue report: it has six MINOR findings, each with a reproduction (F1 by E12, F2 by
   the header printed from a real test run, F3 by E15 and E19, F5 by E17). The clean results are backed
   by raw counts, not by reading: every full-suite run that was not a deliberate stress (E12, E15,
   E19) ended `559 passed`, and all 559 single-test runs passed. The first runs in my copy showed 7
   and then 1 failure; both were my copy missing `src/` and `contracts/` (note 1), not the suite.
4. Web research: none. The only network use was `uv run --isolated --with click==8.1.8` for E17
   (a package download, not a search); Tavily was not needed.

Reliance audit: this review received no inherited structural verdict, so there is nothing relied on
and no category (a) entry. Category (b), independent semantic checks: E12 shows by experiment which
tests change outcome when the monotonic clock stalls; the header run shows that a CLI report mixes the
fixed observed time with the real collected time; E15 and E19 show which tests depend on the temp
folder.

Confidence: Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (of the 20 checks
below; the "Not covered" list is outside them).
Tool engagement (approximate): Read: 45 | Grep: 22 | Glob: 0 | Bash: 17.
Tool calls (Read + Grep + Glob = 67) exceed the 20 checks.

## Checks

| Id | Check | Result |
|----|-------|--------|
| C1 | Tests that build a `SweepContext` or a classified input pass a fixed `now` (`conftest.py:139-142`, `test_probes_allowlist.py:45`, `test_classify.py:102-104`) | PASS |
| C2 | No test code reads the wall clock, sleeps, starts a thread, or uses random, uuid or tempfile (grep of `tests/sweep`: 0 hits) | PASS |
| C3 | The wall-clock seams of the code under test (`probes._utcnow`, `commands.datetime`) are fixed in every test that reaches them | FAIL (MINOR, F2) |
| C4 | The monotonic `Budget` clock is injected in every test that reaches it | FAIL (MINOR, F1) |
| C5 | No dependence on test order: reverse, rotated, per file, each test alone (E2 to E5) | PASS |
| C6 | The suite passes twice in a row, also inside one process, and writes no repository file (E1, E6) | PASS |
| C7 | Module state is restored after `test_import_is_lazy_and_runs_no_seam` (`test_cli_registration.py:48-69`; E2, E3, E5) | PASS |
| C8 | No dependence on the host time zone (E7; every `datetime(` in the tests is aware, `probes.parse_time` reads zone-less times as UTC, `probes.py:385-388`) | PASS |
| C9 | No dependence on the host locale (E8; `strftime` is numeric only, `commands.py:155`, `conftest.py:162-169`; string sorts) | PASS |
| C10 | No dependence on hash seed or set order (E9; sets are sorted before they are output, `classify.py:438`, `:823`) | PASS |
| C11 | No dependence on file system listing order (every `iterdir`, `listdir`, `rglob`, `os.walk` in the tests is sorted, set-compared or has one entry; the code sorts its scans, `probes.py:636`, `:858`, `:1372`) | PASS |
| C12 | No dependence on host environment variables or host files (E13; `read_orca_version` is patched in all three modules that collect, `test_probes_allowlist.py:211`, `test_cli_contract.py:88`, `test_readonly.py:126`; `ORCA_CLI_COMMAND` set on the host is harmless) | PASS |
| C13 | No dependence on the shape of the temp folder (E15, E16, E18, E19) | FAIL (MINOR, F3) |
| C14 | No dependence on the current folder (E13 cwd `/`, E14 no `.git` above; `chdir` goes through `monkeypatch`, `test_cli_contract.py:714`, `:726`, `:747`) | PASS |
| C15 | No dependence on file time granularity (stability tests change the size, `probes.py:558-570`, `test_probes_allowlist.py:1649-1687`; mtime tests set nanoseconds, `test_readonly.py:238-258`) | PASS |
| C16 | No dependence on a host tool beyond what the test marks (one `integration` test; git version, F4) | FAIL (MINOR, F4) |
| C17 | The declared dependency range is enough for the tests (`pyproject.toml:36` vs `result.stderr`; E17) | FAIL (MINOR, F5) |
| C18 | The result maps agree with what a run shows (559 passed, 1 integration test selected, `phase10-validation.md:62`, `:80`; wording of two lines, F6) | FAIL (MINOR, F6) |
| C19 | `ruff check` and `ruff format --check` on the sweep source and tests exit 0 | PASS |
| C20 | No test starts a process or touches Orca, ccsession or Claude (guard `conftest.py:22-42`; `test_a_sweep_starts_no_process_and_records_only_allowlisted_argv`; my runs started none) | PASS |

Checks C3, C4, C13, C16, C17 and C18 FAIL only through MINOR findings, which never fail the gate.

Verdict: PASS
Blocking count: 0

