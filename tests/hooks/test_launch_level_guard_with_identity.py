"""The launch-level guard and the job identity hook on the same PreToolUse payload (plan Task 14, F3).

Each case runs src/superclaude/hooks/scripts/launch-level-guard.sh and
src/superclaude/hooks/scripts/launch-job-identity.sh one after the other on the
same Bash payload, with HOME inside tmp_path, CLAUDE_CONFIG_DIR unset, a PATH
holding only a temporary bin directory, and the UV environment of
tests/hooks/test_launch_job_identity.py (UV_PYTHON set to sys.executable,
UV_PYTHON_DOWNLOADS never). Both hooks read the same store,
~/.claude/state/launch-level/sessions/<session_id>.

Not observed here: the order in which Claude Code runs two matching PreToolUse
hooks and how it combines a block with an updatedInput. That needs a live
session (see artifacts/hook-order.md of the plan package).
"""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "src" / "superclaude" / "hooks" / "scripts"
GUARD = SCRIPTS / "launch-level-guard.sh"
IDENTITY = SCRIPTS / "launch-job-identity.sh"
BASH = "/bin/bash"
SID = "sess-abc_123"
TOOL_ID = "toolu_01ABC123"
HEADER = "Launch-level guard: this session was started by /sc:issue --claim at level {level}."
STATE_NOTE = (
    "Note: the launch record was invalid or unreadable, so the strictest level "
    "(worktree) applies."
)
IDENTITY_BLOCK = "launch job: governed Bash call cannot be wrapped safely\n"

pytestmark = pytest.mark.skipif(
    sys.platform != "linux", reason="the identity hook supports Linux only"
)


@pytest.fixture
def scene(tmp_path):
    home = tmp_path / "home"
    home.mkdir(mode=0o700)
    bindir = tmp_path / "bin"
    bindir.mkdir()
    for tool in ("cat", "sed", "tr", "mkdir", "mv", "ln", "rm", "jq", "uv"):
        found = shutil.which(tool)
        assert found, tool
        (bindir / tool).symlink_to(found)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    env.update(
        HOME=str(home),
        PATH=str(bindir),
        UV_PYTHON=sys.executable,
        UV_PYTHON_DOWNLOADS="never",
    )
    return home, env


def _bind(home: Path, word: str, sid: str = SID) -> None:
    sessions = home / ".claude" / "state" / "launch-level" / "sessions"
    sessions.mkdir(parents=True, exist_ok=True, mode=0o700)
    for part in (
        sessions.parent,
        sessions.parent.parent,
        sessions.parent.parent.parent,
    ):
        part.chmod(0o700)
    path = sessions / sid
    path.write_text(word)
    path.chmod(0o600)


def _payload(command: str, sid: str = SID) -> dict:
    return {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "session_id": sid,
        "tool_use_id": TOOL_ID,
        "cwd": "/not-binding-authority",
        "tool_input": {"command": command, "description": "keep exactly"},
    }


def _hook(script: Path, payload: dict, env: dict):
    return subprocess.run(
        [BASH, str(script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        timeout=20,
    )


def _both(payload: dict, env: dict):
    return _hook(GUARD, payload, env), _hook(IDENTITY, payload, env)


def _updated_input(result) -> dict:
    assert result.returncode == 0, result.stderr
    specific = json.loads(result.stdout)["hookSpecificOutput"]
    assert specific["hookEventName"] == "PreToolUse"
    assert "permissionDecision" not in specific
    return specific["updatedInput"]


def test_full_submit_allowed_command_guard_allows_identity_rewrites_only_command(scene):
    home, env = scene
    _bind(home, "full-submit")
    original = "git status"
    payload = _payload(original)
    guard, identity = _both(payload, env)
    # The guard reads the original payload and allows it silently.
    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
    updated = _updated_input(identity)
    assert identity.stderr == ""
    # Only the command changes; every other tool_input field is kept.
    assert {k: v for k, v in updated.items() if k != "command"} == {
        k: v for k, v in payload["tool_input"].items() if k != "command"
    }
    wrapped = shlex.split(updated["command"])
    assert wrapped[0] == BASH and wrapped[1].endswith("launch-job-identity.sh")
    assert wrapped[2:] == ["execute", SID, TOOL_ID, original]
    assert updated["command"] != original


def test_guard_must_see_the_original_command_not_the_installed_rewrite(scene):
    # Installed, the identity hook lives at ~/.claude/hooks/ and writes its own
    # real path into the rewrite. Were that rewrite handed to the guard, the
    # guard would see a .claude/hooks path and block as LL-TAMPER at any level.
    home, env = scene
    _bind(home, "full-submit")
    installed = home / ".claude" / "hooks" / IDENTITY.name
    installed.parent.mkdir(mode=0o700)
    shutil.copy2(IDENTITY, installed)
    payload = _payload("git status")
    guard = _hook(GUARD, payload, env)
    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
    updated = _updated_input(_hook(installed, payload, env))
    assert shlex.split(updated["command"])[1] == str(installed)
    chained = _hook(GUARD, {**payload, "tool_input": updated}, env)
    assert chained.returncode == 2
    assert chained.stderr.splitlines()[0] == HEADER.format(level="full --submit")
    assert chained.stderr.splitlines()[1].startswith(
        "Blocked: touching the launch-level state"
    )


def test_worktree_blocked_command_guard_blocks_identity_still_rewrites(scene):
    home, env = scene
    _bind(home, "worktree")
    guard, identity = _both(_payload("git commit -m wip"), env)
    assert guard.returncode == 2
    assert guard.stdout == ""
    lines = guard.stderr.splitlines()
    assert lines[0] == HEADER.format(level="worktree")
    assert lines[1].startswith("Blocked: creating a commit")
    assert STATE_NOTE not in guard.stderr
    # Recorded, not part of the decision: the identity hook rewrites the call
    # as for any governed session; the guard's exit 2 is what blocks it.
    updated = _updated_input(identity)
    assert shlex.split(updated["command"])[2:] == [
        "execute",
        SID,
        TOOL_ID,
        "git commit -m wip",
    ]


def test_ordinary_session_both_hooks_silent(scene):
    home, env = scene
    _bind(home, "full-submit", sid="another-session")  # a nonempty store
    guard, identity = _both(_payload("git commit -m wip", sid="ordinary-1"), env)
    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
    assert (identity.returncode, identity.stdout, identity.stderr) == (0, "", "")


@pytest.mark.parametrize("word", ["degraded", "degraded\n"])
def test_degraded_word_guard_worktree_with_state_note_identity_blocks_all(scene, word):
    home, env = scene
    _bind(home, word)
    # A command the guard blocks: level worktree with the LL-STATE note.
    guard, identity = _both(_payload("git commit -m wip"), env)
    assert guard.returncode == 2
    lines = guard.stderr.splitlines()
    assert lines[0] == HEADER.format(level="worktree")
    assert lines[1].startswith("Blocked: creating a commit")
    assert STATE_NOTE in lines
    # The identity hook treats the word as outside worktree, full, full-submit
    # and blocks every Bash call of the session.
    assert (identity.returncode, identity.stdout, identity.stderr) == (
        2,
        "",
        IDENTITY_BLOCK,
    )
    # Mismatch: a command the guard allows at worktree is still blocked by the
    # identity hook, so a degraded session cannot run Bash at all.
    guard, identity = _both(_payload("git status"), env)
    assert (guard.returncode, guard.stdout, guard.stderr) == (0, "", "")
    assert (identity.returncode, identity.stdout, identity.stderr) == (
        2,
        "",
        IDENTITY_BLOCK,
    )
