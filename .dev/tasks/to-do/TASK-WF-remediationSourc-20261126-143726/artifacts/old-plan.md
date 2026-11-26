---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261126-115917
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Keep the ccsession shim tests from failing with "shim failed to start" under load

Source: ./source.md
Goal: The shim tests in tests/unit/test_ccsession_tiers.py pick a launcher base port whose whole six-port window lies below the kernel's local-port range for outgoing connections, so an unrelated connection can no longer hold base + 101 and make the shim's bind fail; two regression tests pin this, and the file passes under the load harness.

## Constraints

- Only `tests/unit/test_ccsession_tiers.py` changes, plus files this plan writes under `./artifacts/`. No production file changes: `src/superclaude/skills/ccsession-tag/ccsession`, `src/superclaude/skills/ccsession-tag/models.py` and `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py` stay as they are.
- No assertion of an existing test is weakened or removed. `_free_port_clear_of` (line 832) and its #443 guard comment (line 833) are untouched. The signature `def _free_port() -> int:` stays, because `_free_port_clear_of`, the `shim` fixture (line 850), the unreachable upstream (line 1213) and the three tests that patch the module attribute `_free_port` (lines 1865, 1879, 1907) rely on it.
- The step and the attempt count are read from `models.SHIM_PORT_STEP` and `models.SHIM_PORT_ATTEMPTS`, never written as 101 and 6.
- Ruff for this repo selects E, F, I, N, W and TID with line length 88 (`pyproject.toml`, `[tool.ruff]`): every added line stays within 88 characters and imports stay sorted. `ruff check` ignores E501, so only `uv run ruff format --check` enforces the 88 columns; run `uv run ruff format` on the file so long names such as the second new test's signature are wrapped.
- Do not use `git stash`. Do not stage or commit anything under `.claude/` or `.dev/issues/`.
- Load-harness output folders go under `.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/` (untracked); only small summary files are copied into `./artifacts/`. `./artifacts/` in this plan always means this package's own `artifacts/` directory (the folder next to this plan file), while commands run from the repository root.
- Known limits to keep visible in the final report, not to hide: a below-range port can still be held by a long-lived service, and two concurrent test processes can draw overlapping windows (estimated about 11 in 22,000 per pair, unmeasured), which the pick-time bind check reduces; on a host whose local-port range starts at or below 10506 the new `_free_port()` falls back to the old behaviour; the single `port 36877 is owned by another service` failure had no identified holder and is only probably reduced; the CI runner and the original release-gate host were never observed, so the fixed-tree load runs are the real measurement.
- Out of scope (separate issues, not part of this plan): the launcher keeping the started shim's stderr and noticing an exited shim, and the macOS-only `e.errno == 48` check at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1054`.

## Phase 1: Pin the failure with tests

## Task 1: Add the two regression tests and `import random` to the test module

Edit `tests/unit/test_ccsession_tiers.py` only. Add `import random` to the import block after `import os` (line 13) so the block stays sorted (it currently has no `random` import). `import errno` is added as well, as the first line of the stdlib block (before `import gzip`, line 10 of the unmodified file, so the block stays sorted). Add two tests after `test_free_port_clear_of_fails_loudly_at_the_bound` (it ends at line 1883) and before `test_forced_in_window_shim_port_is_skipped` (line 1886). The tests use only names the module already has (`Path`, `socket`, `pytest`, `models`) plus `random`, and neither calls a helper that does not exist yet.

First test, `test_free_port_window_lies_below_the_ephemeral_range`: read `/proc/sys/net/ipv4/ip_local_port_range` itself as an independent oracle, taking the first field as `low` (skip with `pytest.skip` when the file is unreadable, or when `low - 1 - models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)` is below 10000, meaning no room); then over 20 calls assert that `_free_port() + models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1) < low`. The test must not re-bind the window ports (another process could take one between the pick and the check and make the test itself flaky).

Second test, `test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port` (takes `monkeypatch`): obtain `clear_base = _free_port()` and `held_base = _free_port()`, drawing `held_base` again until `abs(held_base - clear_base)` is larger than `models.SHIM_PORT_STEP * models.SHIM_PORT_ATTEMPTS` so the two windows cannot overlap; start a plain local listener (a `socket.socket()` bound to `("127.0.0.1", 0)` and listening); bind a second plain client socket (no `SO_REUSEADDR`) to `("127.0.0.1", held_base + models.SHIM_PORT_STEP)`, connect it to the listener and accept the connection, so that port is now the client's local port; the client bind to `held_base + models.SHIM_PORT_STEP`, the listener accept and the premise checks all sit inside one guard, and an `OSError` raised while setting up the client (bind or connect) becomes `pytest.skip`, not an error; check the premise and call `pytest.skip` if it does not hold: the premise is exact: a fresh `socket.socket()` probe's `connect_ex` to that port must equal `errno.ECONNREFUSED`, and a fresh socket with `SO_REUSEADDR` set must fail its bind of that port with `errno.EADDRINUSE` (111 and 98 on Linux); then patch `random.randrange` with `monkeypatch.setattr(random, "randrange", ...)` so that it returns `held_base` on the first call and `clear_base` on every later call, where the replacement accepts the two arguments `(start, stop)` the new `_free_port()` passes; assert `_free_port() == clear_base`. Close the accepted connection and the listener first and the client socket last, and every other socket opened, including the two probe sockets, in a `finally` block so sockets are never leaked. No sleeps.

Acceptance criteria:
- `import errno` and `import random` each appear once in the import block, in their sorted places, and `uv run ruff check tests/unit/test_ccsession_tiers.py` reports no new finding (no I001 or F401).
- Both new tests exist with exactly these names, in this file, placed after `test_free_port_clear_of_fails_loudly_at_the_bound` and before `test_forced_in_window_shim_port_is_skipped`.
- Run on the unchanged `_free_port` (the old three-line body): `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= -k "free_port_window or free_port_skips"` shows both tests FAILED by an `AssertionError` on the assertions described above, not by an `ImportError`, `NameError`, `TypeError` or a skip; the command output is saved to `./artifacts/t1-red.log`. If either new test is skipped instead of failing in that red run, repeat the red run once and save both outputs; if it skips again, stop and report the premise failure instead of continuing.
- The rest of the file is unchanged: `git diff --stat -- tests/unit/test_ccsession_tiers.py` shows only added lines (the two imports and the two tests), and the existing tests still pass with the two new tests deselected: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= --deselect tests/unit/test_ccsession_tiers.py::test_free_port_window_lies_below_the_ephemeral_range --deselect tests/unit/test_ccsession_tiers.py::test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port` (record the pass line in `./artifacts/t1-rest.log`).

## Phase 2: Add the window helpers

## Task 2: Add the constants and the two helpers above `_free_port()`

Depends on: Task 1

Edit `tests/unit/test_ccsession_tiers.py` only. Insert, directly above `def _free_port() -> int:` (line 823 of the unmodified file; it moves down after Task 1), these module-level names, with one-line comments in the style of the file:
- `_FREE_PORT_FLOOR = 10000` and `_FREE_PORT_TRIES = 50`.
- `_ephemeral_low() -> int`: returns the first whitespace-separated field of `/proc/sys/net/ipv4/ip_local_port_range` as an int; returns `32768` on `OSError`, `ValueError` or `IndexError` (32768 is also below the macOS range).
- `_window_binds(base: int) -> bool`: for each `port = base + models.SHIM_PORT_STEP * k` with `k in range(models.SHIM_PORT_ATTEMPTS)`, create a `socket.socket()`, set `SO_REUSEADDR`, bind `("127.0.0.1", port)` and close it (use `with`); return `False` on the first `OSError`, else `True`. This is the same bind the shim makes (`allow_reuse_address = True` at `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:1030`, bind at line 1052).

Do not change `_free_port()` in this task: the helpers stay unused until Task 3.

Acceptance criteria:
- The two helpers and the two constants exist with exactly these names and signatures, directly above `_free_port`, and `_free_port()` is byte-for-byte unchanged.
- The helpers work on a window that is known to be free (output in `./artifacts/t2-helpers.log`): an ad-hoc run prints `t._ephemeral_low()` (`32768` on this host); then steps through bases from 10000 upward until it can bind all six window ports `base + models.SHIM_PORT_STEP * k` (k from 0 to `models.SHIM_PORT_ATTEMPTS` minus 1) with `SO_REUSEADDR` set, not listening, and keeps those six sockets open; while they are held, `t._window_binds(base)` returns `True`, and a plain socket without `SO_REUSEADDR` fails to bind `base` (so a helper that left `SO_REUSEADDR` out would print `False`); the six sockets are then closed. This check does not use the old `_free_port()` and does not print `_window_binds(0)`.
- A held window port is detected: in an ad-hoc run (output in `./artifacts/t2-helpers.log`), bind a plain socket to `base + models.SHIM_PORT_STEP` for a free `base`, call `_window_binds(base)` while it is held without `SO_REUSEADDR` and listening, and record `False`.
- `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` report nothing new for the added hunk, and the two new tests from Task 1 still fail on their assertions.

## Phase 3: Move the base port out of the ephemeral range

## Task 3: Replace the body of `_free_port()` with the window-aware draw

Depends on: Task 2

Edit `tests/unit/test_ccsession_tiers.py` only. Keep `def _free_port() -> int:` and replace its body with: compute `top = _ephemeral_low() - 1 - models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)`; if `top >= _FREE_PORT_FLOOR`, loop up to `_FREE_PORT_TRIES` times, draw `base = random.randrange(_FREE_PORT_FLOOR, top + 1)` (call it through the `random` module attribute so a test can patch it) and return `base` when `_window_binds(base)` is true; after the loop, or when `top < _FREE_PORT_FLOOR`, fall back to the original body (`bind(("127.0.0.1", 0))` and return the port). Add a docstring or comment saying why: a `bind(0)` base is in the range the kernel uses for outgoing connections and base + 101 then collides with other processes' connections (issue 352).

Acceptance criteria:
- `_free_port()` keeps its signature and returns an `int`; on this host (range start 32768) every call returns a base with `base + models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1) < 32768`; the three tests that patch the module attribute `_free_port` (`test_free_port_clear_of_skips_a_port_in_the_shim_window`, `test_free_port_clear_of_fails_loudly_at_the_bound`, `test_forced_in_window_shim_port_is_skipped`) pass unchanged.
- Both new tests now pass: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= -k "free_port_window or free_port_skips"` (output in `./artifacts/t3-green.log`).
- The whole file passes: `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts=` (output in `./artifacts/t3-whole-file.log`), including the six launcher tests that call `_free_port_clear_of` (their calls are at lines 1920, 2006, 2282, 2328, 2355 and 2491 of the unmodified file), `test_a_busy_shim_is_never_stopped_by_a_new_launch`, `test_tiers_off_launch_never_takes_over_a_tier_shim`, `test_upgraded_code_starts_a_new_shim_and_keeps_the_old` and `test_relative_defaults_path_keeps_each_directory_on_its_own_shim`.
- Load check, seven shim tests: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed --tests --rounds 4 --parallel 8 --burners 16 --timeout 700 --tag fixed` ends with 0 failed process-runs of 32 and no `shim failed to start` in any log (the unfixed rate was 8 to 19 percent of process-runs); copy `summary-fixed.json` from that folder to `./artifacts/t3-load-summary.json`. Any process log that shows "shim failed to start" is recorded in the final report with the port it names and whether that port is below the kernel's local-port range start (32768 on this host); such a failure counts against the claim that the fix is sufficient and is reported as it is; the run is never repeated until it passes.
- Load check, whole file: this is the issue's own criterion, 20 consecutive whole-file runs under the same load.
  - First check that no leftover shim or burner process is running (`pgrep -af "local-gateway-alias-proxy.py"` and `pgrep -af "while True: pass"` print nothing; kill any leftover before going on).
  - Then time one loaded whole-file run: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed-whole-timing --tests --whole-file --rounds 1 --parallel 1 --burners 16 --timeout 1800 --tag timing`, and read its `secs` (with `--parallel 1` that is the true duration).
  - Run the 20 runs: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed-whole --tests --whole-file --rounds 20 --parallel 1 --burners 16 --timeout <the larger of 600 and twice the timing run's secs> --tag wholefile`; the check passes only when all 20 results have `rc` 0. A result with `rc: "timeout"` fails the check; after any timeout or other abort, kill the leftover shim and burner processes before doing anything else.
  - A passed run must not show more skipped tests than the unloaded whole-file run in `./artifacts/t3-whole-file.log`: compare the last line of each process log (a skipped test returns exit code 0 and the summary JSON does not count skips). Copy `summary-wholefile.json` to `./artifacts/t3-wholefile-summary.json`.
  - The earlier shape of 5 rounds of 4 parallel processes (`--rounds 5 --parallel 4 --tag wholefile4`, output folder `.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/fixed-whole4`) may be run as an extra and is not counted toward the criterion; it can share a hash-derived port between processes in `test_show_all_launch_runs_its_own_shim`.
  - A failure of a test that has nothing to do with shims is recorded by name; run that single test alone and unloaded (`uv run pytest <its node id> -q -p no:cacheprovider -o addopts=`); one that passes alone, or fails alone too, is reported and does not count against this change; a shim-related failure counts. The wall-clock tests that can fail under load without any port involvement are `test_cooldown_expires_and_repeats` (near lines 1177-1189 of the unmodified test file) and the tests that set `CCSESSION_FIRST_BYTE_TIMEOUT` to 1 (near lines 1204, 1244, 1554 and 1752); the final report lists any of them that failed.
- `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` report nothing new for the changed hunks.
- `git diff --stat` shows only `tests/unit/test_ccsession_tiers.py` changed apart from the files this plan writes under `.dev/tasks/`; no path under `.claude/` or `.dev/issues/` is changed.
