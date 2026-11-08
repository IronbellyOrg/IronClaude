import json
import os
import sys

sys.path.insert(0, "/home/coder/workspaces/worktrees/IronClaude/issue-440/tests/hooks")

import pytest

import test_launch_level_guard as t


@pytest.mark.parametrize("name", list(t.LARGE_COMMANDS))
def test_probe(tmp_path, name):
    # D5 wrapper experiment: stdin to a file once, then the guard 10 times in a row.
    env = t._spd_env(tmp_path, tmp_path / "home")
    t._bind(tmp_path, "full-submit")
    payload = tmp_path / "in.json"
    payload.write_bytes(json.dumps(t._bash(t.LARGE_COMMANDS[name])).encode())
    run = f'{t.BASH} "{t.HOOK}" < "{payload}" >/dev/null 2>&1'
    slow = tmp_path / "slow-guard.sh"
    slow.write_text(f"for _ in 1 2 3 4 5 6 7 8 9 10; do {run}; done\n")
    seconds, _ = t._spd_once(slow, b"", env, timeout=120)
    with open(os.environ["D5_OUT"], "a") as f:
        f.write(f"D5 {name}: 10x wrapper {seconds:.3f} s\n")
