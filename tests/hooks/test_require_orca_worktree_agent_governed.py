"""require-orca-worktree-agent.sh next to launch-job-identity.sh.

launch-job-identity.sh (also a PreToolUse Bash hook) replaces the whole input of
a launch-level governed session through `updatedInput`, wrapping the original
command as one quoted argument, and its header says the rewrite order of other
hooks is unspecified. This pins the case where the Orca gate sees the original
command of a governed session: it must still block. Whether the live order ever
shows it the rewritten command is not verified here; see
artifacts/t2-launch-identity-interaction.md in the task package.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

HOOK = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "hooks"
    / "scripts"
    / "require-orca-worktree-agent.sh"
)
BASH = shutil.which("bash") or "/bin/bash"


def test_blocks_bare_create_in_a_governed_session(tmp_path: Path) -> None:
    sessions = tmp_path / ".claude" / "state" / "launch-level" / "sessions"
    sessions.mkdir(parents=True, mode=0o700)
    (sessions / "old").write_text("worktree\n")
    event = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "session_id": "old",
        "tool_use_id": "toolu_01ABC123",
        "cwd": "/not-binding-authority",
        "tool_input": {"command": "orca worktree create --name x"},
    }
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    result = subprocess.run(
        [BASH, str(HOOK)],
        input=json.dumps(event).encode(),
        capture_output=True,
        env=env,
        timeout=10,
    )
    assert result.returncode == 2, result.stderr.decode()
    assert result.stdout == b""
    stderr = result.stderr.decode()
    assert stderr.startswith("ORCA WORKTREE BLOCK:")
    assert '--agent claude --prompt "<task>"' in stderr
