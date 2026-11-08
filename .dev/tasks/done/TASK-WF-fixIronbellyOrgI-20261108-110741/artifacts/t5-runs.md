# T5 run evidence (proof c)

Setup: `uv pip install "pytest-xdist>=3.5,<4"` (installed pytest-xdist 3.8.0 and execnet 2.1.2 into the venv only; pyproject.toml and uv.lock unchanged). xdist created 28 workers.

Script: /tmp/issue443-runs.sh (scratch). Each run: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/unit/test_ccsession_tiers.py -q -p no:cacheprovider [-n auto]`. Durations are pytest's own (the script's wall-clock column came out empty because `bc` is not installed). Logs: /tmp/issue443-runs/run-<n>.log.

| Run | Mode | Passed | Failed | Skipped | Duration | rc |
|---|---|---|---|---|---|---|
| 1 | -n auto | 176 | 0 | 0 | 20.75s | 0 |
| 2 | -n auto | 176 | 0 | 0 | 13.00s | 0 |
| 3 | -n auto | 175 | 1 | 0 | 15.69s | 1 |
| 4 | -n auto | 176 | 0 | 0 | 20.67s | 0 |
| 5 | -n auto | 176 | 0 | 0 | 16.01s | 0 |
| serial | serial | 176 | 0 | 0 | 164.84s | 0 |

Result: 5 of 6 runs fully green; the criterion "all pass" is NOT met as written (run 3).

## Run 3 failure: not the #443 collision

`FAILED tests/unit/test_ccsession_tiers.py::test_forced_in_window_shim_port_is_skipped` (worker gw4), raised from the second `_real_launch` inside `test_a_busy_shim_is_never_stopped_by_a_new_launch`:

    AssertionError: gateway_port=40363 shim_base_port=34015 upstream=http://127.0.0.1:40363/cli
    [ccsession] A shim with other settings or older code is on 127.0.0.1:34015; leaving it running for its sessions
    [ccsession] Starting model-alias shim on 127.0.0.1:34116
    [ccsession] ERROR: shim failed to start (try: python3 .../shim-under-test.py)

- No refusal: 40363 is not 0..97 above any of 34015 + 101k (k = 0..5), so the helper's pairing worked; the forced in-window port had already been skipped.
- The launcher waits 3 seconds (10 x 0.3s, src/superclaude/skills/ccsession-tag/ccsession:1040-1045) for the shim on base+101 (34116) to listen. It did not. Two mechanisms fit and the log cannot tell them apart (UNVERIFIED which): another parallel worker held 34116, or the shim's python3 start took over 3s under 28-worker load.
- Both are the parallel-worker flake class the coordinator assigned to #352 ("report them; do not fix them"). Not fixed here. The same launch flow passed in the other 5 runs, including the plain `test_a_busy_shim_is_never_stopped_by_a_new_launch` in all 6.

## Set 2 (same code, no changes; re-run after the T5 review)

Script: /tmp/issue443-runs2.sh (set 1's script with the output directory changed to /tmp/issue443-runs2 and the empty wall-clock field removed). Logs: /tmp/issue443-runs2/run-<n>.log.

| Run | Mode | Passed | Failed | Skipped | Duration | rc |
|---|---|---|---|---|---|---|
| 1 | -n auto | 176 | 0 | 0 | 13.31s | 0 |
| 2 | -n auto | 176 | 0 | 0 | 14.18s | 0 |
| 3 | -n auto | 176 | 0 | 0 | 12.97s | 0 |
| 4 | -n auto | 176 | 0 | 0 | 13.54s | 0 |
| 5 | -n auto | 176 | 0 | 0 | 14.07s | 0 |
| serial | serial | 176 | 0 | 0 | 164.89s | 0 |

Set 2 result: 6 of 6 runs fully green. Set 1 run 3 stays on record above; set 2 does not replace it.

## Coordinator ruling (msg_7ce89f6e15c5)

175/176 once, class #352, UNVERIFIED port-taken vs slow start. Proof (c) is treated as met for #443 by coordinator ruling msg_7ce89f6e15c5: every failure in the runs is the #352 class and none is the "ccsession shim address" refusal. No retries, longer waits or launcher changes were added. The T5 review's unmet "all pass" (T5.AC2) is carried as a gap with this ruling as the reason.
