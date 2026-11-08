# PR #447 follow-up fix record (F1, F3)

Branch `ironbelly/issue-331-review-fixes`. Nothing committed, staged or pushed. F2 and `docs/` untouched.

## Files and functions changed

| File | Function | Change |
|---|---|---|
| `src/superclaude/cli/issue_watch/cycle.py` | `validate_approvers` | F1: lstat kept only for the "missing" and "not a regular file" (symlink or directory) texts. The file is opened (`O_NOFOLLOW`), then `os.fstat(fd)` is checked: `(st_dev, st_ino)` equals the lstat result (new detail "the approvers file changed while it was being checked"), regular file, owner is `geteuid()`, no group/other write. Descriptor closed in an outer `finally` (`os.close`), read through `os.fdopen(fd, "rb", closefd=False)`. 1 MiB cap, UTF-8, id-line rules and the other details unchanged. |
| `src/superclaude/cli/issue_watch/launch.py` | `find_orca` | F3: `timeout` also accepts a zero-argument callable, called right before each probe (skipped candidates ask nothing). Its None ends the search (returns None); its number is checked with `_check_timeout` per probe. Float and None forms unchanged (float still validated up front). |
| `src/superclaude/cli/issue_watch/cycle.py` | `_Cycle._launch` | F3: early `budget_exhausted` skip kept; `find_orca` now gets `probe_allowance`, which re-reads `self.deadline.timeout_for(PROBE_TIMEOUT_S)` per probe and records whether it last answered None. A None result from `find_orca` with that flag set raises `_Skip("budget_exhausted")`; otherwise `_Stop("orca_not_found")` as before. |
| `tests/issue_watch/test_cycle.py` | new tests | see below |
| `tests/issue_watch/test_launch.py` | new tests | see below |

Design note: the flag records that the last allowance answer was None, rather than re-checking the deadline after a None return. A cycle where both probes ran and failed, the last one ending at 240 s, is still `orca_not_found` (both really failed), not a deadline skip.

## Tests

F1 (`tests/issue_watch/test_cycle.py`, helpers `_before_first_open`, `_is_closed`):
- `test_validate_approvers_refuses_a_file_swapped_between_lstat_and_open__fr027_nfr010[384|436]` (hostile file mode 0o600 and 0o664, renamed over the path inside the first `os.open`)
- `test_validate_approvers_refuses_a_mode_widened_between_lstat_and_open__fr027_nfr010` (same inode, chmod 0o666 between lstat and open)
- `test_validate_approvers_untouched_file_is_still_accepted_with_open_patched__fr027_nfr010`
- `test_validate_approvers_closes_the_descriptor_when_it_refuses__fr027_nfr010[swapped|widened]`
- `test_validate_approvers_closes_the_descriptor_when_fstat_fails__fr027_nfr010`

F3:
- `tests/issue_watch/test_launch.py`: `test_fr013_probe_timeout_callable_is_asked_before_each_probe_and_none_stops`, `..._gives_each_probe_its_own_allowance`, `..._is_not_asked_for_a_skipped_candidate`, `test_fr013_probe_timeout_callable_result_is_validated_per_probe[0|-1.0|True|5|nan]`
- `tests/issue_watch/test_cycle.py`: `test_a_deadline_crossed_by_the_first_probe_starts_no_second_probe__fr029_c11` (both CLIs resolve, entry at 235 s, first probe fails and uses 5 s)

## Pre-fix FAIL (unmodified source, tests written first)

F1, `uv run pytest tests/issue_watch/test_cycle.py -k validate_approvers -rA`:
```
E   Failed: DID NOT RAISE ConfigError      (x6)
FAILED ...test_validate_approvers_refuses_a_file_swapped_between_lstat_and_open__fr027_nfr010[384]
FAILED ...test_validate_approvers_refuses_a_file_swapped_between_lstat_and_open__fr027_nfr010[436]
FAILED ...test_validate_approvers_refuses_a_mode_widened_between_lstat_and_open__fr027_nfr010
FAILED ...test_validate_approvers_closes_the_descriptor_when_it_refuses__fr027_nfr010[swapped]
FAILED ...test_validate_approvers_closes_the_descriptor_when_it_refuses__fr027_nfr010[widened]
FAILED ...test_validate_approvers_closes_the_descriptor_when_fstat_fails__fr027_nfr010
PASSED ...test_validate_approvers_untouched_file_is_still_accepted_with_open_patched__fr027_nfr010
================= 6 failed, 51 passed, 492 deselected in 1.56s =================
```
(The current code returns the swapped file's ids instead of raising.)

F3, `-k "timeout_callable or first_probe_starts_no_second"`:
```
E   ValueError: timeout must be a positive number of seconds      (x3, test_launch.py callable tests)
E   AssertionError: assert 2 == 1
E    +  where 2 = <built-in method count of list object ...>('probe')       (test_cycle.py)
FAILED ...test_fr013_probe_timeout_callable_is_asked_before_each_probe_and_none_stops
FAILED ...test_fr013_probe_timeout_callable_gives_each_probe_its_own_allowance
FAILED ...test_fr013_probe_timeout_callable_is_not_asked_for_a_skipped_candidate
FAILED ...test_a_deadline_crossed_by_the_first_probe_starts_no_second_probe__fr029_c11
================= 4 failed, 5 passed, 719 deselected in 2.51s =================
```
The cycle test shows the real defect: the second probe is started (2 probes, not 1). The 5 passing tests are the `_validated_per_probe` cases: they pass before the fix only because the old code rejects any callable with that same ValueError, so they pin behaviour after the fix but are not failing-first.

## Post-fix PASS

F1: `64 passed, 485 deselected` for `-k "validate_approvers or approvers_summary or validate_setup"`; all 7 new F1 tests PASSED.
F3: `9 passed, 719 deselected`; all 9 new F3 tests PASSED.

## Final command results (real output)

| Command | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` | `2653 passed in 17.46s` |
| `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -q` | `2653 passed in 6.84s` |
| `make lint` | architecture policy PASS (5 warnings, pre-existing); `uv run ruff check .` All checks passed |
| `uvx --offline ruff@0.15.20 check src/ tests/` | All checks passed |
| `uvx --offline ruff@0.15.20 format --check src/ tests/` | `1246 files already formatted` (after formatting `tests/issue_watch/test_launch.py` once) |
| `make sync-dev` then `make verify-sync` | `All components in sync.` (rc 0) |
| detect-secrets-hook on the 4 changed files (baseline version 1.5.0 copy) | rc 0, no findings |

## Unverified

- The swap race is simulated by renaming inside a wrapped `os.open`; no real concurrent attacker was run.
- No foreign-owner fstat test was added (needs root); the existing monkeypatched-`geteuid` test now exercises the fstat owner check.
- `make lint` architecture warnings (5) were not compared against master.

## FIFO finding (PR 448 round 1)

Finding (Augment, Medium): `validate_approvers` opened the approvers file `O_RDONLY | O_NOFOLLOW | O_CLOEXEC`. A parent-directory writer who swaps the file for a FIFO after the lstat makes the blocking open wait for a writer, so the fstat checks never run and the poller hangs.

Fix: `src/superclaude/cli/issue_watch/cycle.py` adds `os.O_NONBLOCK` to the open flags (one-line comment gives the reason). The existing inode compare then rejects the swapped FIFO with `ConfigError("approvers_invalid")`; the existing `finally` still closes the descriptor.

Tests added in `tests/issue_watch/test_cycle.py` (written first):
- `test_validate_approvers_refuses_a_file_swapped_for_a_fifo_without_hanging__fr027_nfr010` (unlink + mkfifo between lstat and open; call runs in a daemon thread, `join(timeout=2)`; stuck thread released in `finally` by an `O_RDWR | O_NONBLOCK` open of the FIFO).
- `test_validate_approvers_fifo_from_the_start_is_refused_without_hanging__fr027_nfr010` (FIFO from the start; lstat rejects with "not a regular file"; guard test, passes before and after).

Pre-fix (unmodified source):

```
FAILED tests/issue_watch/test_cycle.py::test_validate_approvers_refuses_a_file_swapped_for_a_fifo_without_hanging__fr027_nfr010
E   AssertionError: validate_approvers hung opening a FIFO
E   assert not True
E    +  where True = is_alive()
================= 1 failed, 1 passed, 550 deselected in 4.98s ==================
```

Post-fix:

```
tests/issue_watch/test_cycle.py ..                                       [100%]
====================== 2 passed, 550 deselected in 0.16s =======================
```

| Command | Result |
|---|---|
| `uv run pytest tests/issue_watch/ -q` | `2655 passed in 17.06s` (was 2653) |
| `uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/ -q` | `2655 passed in 6.78s` |
| `make lint` | architecture policy PASS; `ruff check .` All checks passed |
| `uvx --offline ruff@0.15.20 check src/ tests/` | All checks passed |
| `uvx --offline ruff@0.15.20 format --check src/ tests/` | `1246 files already formatted` (after one `ruff format` of `cycle.py` to join the wrapped `os.open` call) |
| `make sync-dev` then `make verify-sync` | `All components in sync.` |
| detect-secrets-hook on `cycle.py` and `test_cycle.py` | rc 0 |

Unverified: the swap is simulated through the `_before_first_open` wrapper, not a real concurrent attacker; the FIFO-from-the-start test did not fail before the fix (lstat already rejects it), so it is a guard, not a failing-first proof.
