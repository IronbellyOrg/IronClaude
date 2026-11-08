# T5 before evidence: the old pairing is refused (proof a, FAIL side)

## 1. Reproduction recorded in .dev/issues/443/handoff-repro.md (2026-11-08T11:06:20Z)

Scratch test /tmp/issue443-repro/test_forced_collision.py (outside the repo) imports the unchanged test module, wraps `StandInGateway` to record its port, makes the first `_free_port()` return `gateway_port - 5` (inside shim window k=0), then runs `test_a_busy_shim_is_never_stopped_by_a_new_launch`.

Command (from the worktree root):

    timeout 180 uv run pytest /tmp/issue443-repro/test_forced_collision.py -q -s -p no:cacheprovider --rootdir /tmp/issue443-repro

Output (copied from handoff-repro.md lines 11-14):

    gateway_port=33361 forced_base=33356
    REFUSAL: [..., '  [ccsession] ERROR: http://127.0.0.1:33361/cli is a ccsession shim address (port 33361), not the gateway; refusing to start a shim that forwards to another shim']
    .
    1 passed in 0.55s

(That scratch test passes because it expects the refusal.)

## 2. Fresh run: the new test's body against the pre-fix module (2026-11-08, this task)

Setup (scratch, outside the repo): /tmp/issue443-old/tests/unit/old_tiers.py = `git show HEAD:tests/unit/test_ccsession_tiers.py` (no `_free_port_clear_of`; the shim port comes straight from `_free_port()`); /tmp/issue443-old/src is a symlink to the worktree src so REPO_ROOT resolves. /tmp/issue443-old/tests/unit/test_old_pairing.py applies the same forcing as `test_forced_in_window_shim_port_is_skipped` and does not catch the error.

Command:

    cd /tmp/issue443-old && timeout 180 env PYTHONDONTWRITEBYTECODE=1 uv run --project /home/coder/workspaces/worktrees/IronClaude/issue-443 pytest tests/unit/test_old_pairing.py -q -s -p no:cacheprovider --rootdir /tmp/issue443-old

Result: rc=1, the test FAILS with the launcher refusal:

    [old-pairing] gateway_port=42019 forced=42014
    >       assert proc.returncode == 0, proc.stderr
    E       AssertionError: [ccsession] tier2 (...): model claude-gw-tier2[1m], context 500000, auto-compact window 500000
    E       [ccsession] ERROR: http://127.0.0.1:42019/cli is a ccsession shim address (port 42019), not the gateway; refusing to start a shim that forwards to another shim
    tests/unit/old_tiers.py:1702: AssertionError
    FAILED tests/unit/test_old_pairing.py::test_forced_in_window_shim_port_is_skipped_old_pairing
    1 failed, 1 warning in 0.62s

## After (with the helper)

See ./t5-after.log: `test_forced_in_window_shim_port_is_skipped` passes (1 passed).
