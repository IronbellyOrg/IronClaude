# Remediation source: make the ccsession shim tests stop failing with "shim failed to start" under load

Issue: https://github.com/IronbellyOrg/IronClaude/issues/352 (branch clayphi/issue-352, base integration). Diagnosis: `.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/REPORT.md` (status success, Tier 2, calibrated confidence 0.83, consensus of four cards). This is a test-only fix; no production file changes.

## Summary

The shim tests in `tests/unit/test_ccsession_tiers.py` take the launcher's base port from `_free_port()` (lines 823-826), which does `bind(("127.0.0.1", 0))`. The kernel gives `bind(0)` an odd port inside its local-port range for outgoing connections (32768-60999 here). The launcher then starts a second shim at base + 101 (`SHIM_PORT_STEP = 101`, `models.py:821`), which is always an even port, the class the kernel hands to outgoing `connect()`. When an unrelated connection holds that port as its local port (established, or in TIME_WAIT on the client side), the shim's `SO_REUSEADDR` bind fails with errno 98, the shim exits, the launcher's connect probe keeps reporting "no listener" for about 4.5 s, and `ccsession:1264` prints `shim failed to start`. Measured failure rate with parallel pytest processes on 4 pinned cores and 16 CPU burners: 1 of 12, 6 of 32 and 2 of 24 process-runs; one process alone: 0 of 8 (low power).

## Files to change

- `tests/unit/test_ccsession_tiers.py` only.
  1. Add `import random` to the imports (lines 10-27 have none).
  2. Replace `_free_port()` (lines 823-826) with the helpers and the new `_free_port()` below. Keep the signature `def _free_port() -> int:` so `_free_port_clear_of` (line 832, with its #443 guard), the `shim` fixture (line 850), the unreachable upstream (line 1213) and the three tests that monkeypatch the module attribute `_free_port` (lines 1856-1910) keep working unchanged.
  3. Add two regression tests after `test_free_port_clear_of_fails_loudly_at_the_bound` (ends at line 1883).

Helpers and behaviour of the new `_free_port()`:
- `_FREE_PORT_FLOOR = 10000` and `_FREE_PORT_TRIES = 50` (module constants).
- `_ephemeral_low() -> int`: the first field of `/proc/sys/net/ipv4/ip_local_port_range`; fallback `32768` on `OSError`, `ValueError` or `IndexError` (32768 is also below the macOS range).
- `_window_binds(base: int) -> bool`: for each `base + models.SHIM_PORT_STEP * k`, `k in range(models.SHIM_PORT_ATTEMPTS)`, bind `127.0.0.1:<port>` with `SO_REUSEADDR` set (the bind the shim makes), close it, and return False at the first failure. Read the step and the attempt count from `models`, never hard-code 101 and 6.
- `_free_port()`: `top = _ephemeral_low() - 1 - models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1)`. Draw `random.randrange(_FREE_PORT_FLOOR, top + 1)` up to `_FREE_PORT_TRIES` times and return the first base for which `_window_binds(base)` is true. If `top < _FREE_PORT_FLOOR` or every draw fails, return today's `bind(0)` port.
- Use `random.randrange` (a module attribute lookup at call time) so a test can monkeypatch it.

Regression tests (test file):
- `test_free_port_window_lies_below_the_ephemeral_range`: read `/proc/sys/net/ipv4/ip_local_port_range` itself as an independent oracle; skip when the file is absent or no room exists below it; over 20 calls assert `base + models.SHIM_PORT_STEP * (models.SHIM_PORT_ATTEMPTS - 1) < low`. Do not re-bind the window inside the test (another process could take a port between the pick and the check and make the test itself flaky). It fails on the current code because `bind(0)` returns a port at or above `low`.
- `test_free_port_skips_a_window_whose_attempt_port_is_a_client_local_port`: obtain a clear base `clear_base` from `_free_port()` and a second base `held_base`; bind a plain client socket (no `SO_REUSEADDR`) to `held_base + models.SHIM_PORT_STEP` and connect it to a local listener, so that port is the client's local port; assert the premise (a connect probe to that port gives `connect_ex` 111 and a `SO_REUSEADDR` bind on it fails with errno 98, else `pytest.skip`); monkeypatch `random.randrange` to return `held_base` first and `clear_base` afterwards; assert `_free_port() == clear_base`. Cleanup: close the listener side first, then the client. Deterministic, no sleeps. It does not call `_window_binds`, so it fails on the current code by its final assertion: the old `_free_port` ignores the patched draw and returns a `bind(0)` port that is not `clear_base`.

## Must not change

- `src/superclaude/skills/ccsession-tag/ccsession`: the tests assert the second shim is at exactly `port + 101` (test lines 1935, 2289, 2334); a launcher that skips a dead port lands on +202; its contracts (never stop another shim `ccsession:1210`, detached start `:1249`, attach only on a matching health answer `:1267`, the message at `:1264`) stay.
- `src/superclaude/skills/ccsession-tag/models.py` (`SHIM_PORT_ATTEMPTS`, `SHIM_PORT_STEP`) and `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`.
- No assertion of any existing test is weakened or removed; `_free_port_clear_of` and its #443 guard (test line 833) are untouched.

## Acceptance criteria

1. The two new tests exist and pass on the fixed tree, and the range test is shown to fail first: write the two new tests before the helpers exist, run them (`uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts= -k "free_port_window or free_port_skips"`) and record that both tests fail on the old `_free_port` by an assertion (not by an import or name error), then add the helpers and the new `_free_port` and record that both pass. Do not use `git stash`.
2. `uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider -o addopts=` passes (the whole file), including the six launcher tests that call `_free_port_clear_of` (test lines 1920, 2006, 2282, 2328, 2355, 2491), `test_free_port_clear_of_skips_a_port_in_the_shim_window`, `test_free_port_clear_of_fails_loudly_at_the_bound` and `test_forced_in_window_shim_port_is_skipped`.
3. Load check on the fixed tree: `taskset -c 0-3 uv run python .dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/repro/load_repro.py --repo . --out <new folder under .dev/troubleshoot/...> --tests --rounds 4 --parallel 8 --burners 16 --timeout 700 --tag fixed` gives 0 failed process-runs of 32 (the old rate was 8-19% per process-run). This runs the real tree, with no `--tree` option, so it needs no scratch copy; its output stays untracked.
4. The issue's own criterion: 20 consecutive whole-file runs of `tests/unit/test_ccsession_tiers.py` under the same load (the harness with `--rounds 20 --parallel 1`) all pass.
5. `uv run ruff check tests/unit/test_ccsession_tiers.py` and `uv run ruff format --check tests/unit/test_ccsession_tiers.py` report nothing new for the changed hunks.
6. `git diff --stat` shows only `tests/unit/test_ccsession_tiers.py` changed (plus `.dev/tasks` plan files); nothing under `.claude/` or `.dev/issues/`.

## Risks and limits to keep in the plan

- A below-range port can still be held by a long-lived service, or two concurrent test processes can draw overlapping windows (estimated about 11 in 22,000 per pair, unmeasured); the pick-time bind screening reduces this.
- On a host whose local-port range starts at or below 10506 the helper falls back to today's behaviour.
- The single `port 36877 is owned by another service` failure had no identified holder; this fix probably reduces it (inference only).
- The CI runner and the original release-gate host were not observed; the fixed-tree load run is the real measurement.

## Follow-up (not part of this plan)

- Launcher: keep the started shim's stderr in a start log and notice an exited shim, moving to the next candidate port in the existing six-attempt loop (production change, separate issue).
- `local-gateway-alias-proxy.py:1054` tests `e.errno == 48` (macOS); Linux uses 98.

## References

- Report: /home/coder/workspaces/worktrees/IronClaude/issue-352/.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/REPORT.md
- Impact report: /home/coder/workspaces/worktrees/IronClaude/issue-352/.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/impact/impact.md
- Candidate-fix index: /home/coder/workspaces/worktrees/IronClaude/issue-352/.dev/troubleshoot/test-ccsession-shim-tests-in-tests-20261126031906/candidate-fixes.md
- Issue summary and decisions: /home/coder/workspaces/worktrees/IronClaude/issue-352/.dev/issues/352/issue-summary.md

## Pipeline Hardening

Pipeline hardening not applicable: test-only change; no gate, review or audit signs off on the launcher from a substituted proof (boundary scan in the report).
