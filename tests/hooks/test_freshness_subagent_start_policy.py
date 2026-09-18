"""Runtime tests for SubagentStart policy injection."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
HOOK = REPO_ROOT / "src/superclaude/hooks/scripts/freshness-subagent-start.sh"
POLICY = REPO_ROOT / "src/superclaude/core/BASH_INSPECTION_POLICY.md"


def _install_policy(home: Path) -> None:
    claude_dir = home / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    (claude_dir / POLICY.name).write_text(POLICY.read_text(encoding="utf-8"))


def _run_hook(home: Path, payload: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=payload,
        text=True,
        capture_output=True,
        env=env,
        timeout=2,
        check=False,
    )


def test_subagent_start_injects_policy_and_increments_counter(tmp_path):
    _install_policy(tmp_path)
    result = _run_hook(tmp_path, json.dumps({"session_id": "sess-1"}))

    assert result.returncode == 0
    output = json.loads(result.stdout)
    hook_output = output["hookSpecificOutput"]
    assert hook_output["hookEventName"] == "SubagentStart"
    assert hook_output["additionalContext"] == POLICY.read_text(encoding="utf-8")
    counter = tmp_path / ".claude/state/bg-agents/sess-1.txt"
    assert counter.read_text().strip() == "1"


def test_subagent_start_missing_policy_fails_open(tmp_path):
    result = _run_hook(tmp_path, json.dumps({"session_id": "sess-2"}))

    assert result.returncode == 0
    assert result.stdout == ""
    counter = tmp_path / ".claude/state/bg-agents/sess-2.txt"
    assert counter.read_text().strip() == "1"


def test_subagent_start_malformed_input_still_fails_open(tmp_path):
    _install_policy(tmp_path)
    result = _run_hook(tmp_path, "{not-json")

    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["hookSpecificOutput"]["hookEventName"] == "SubagentStart"
    counter = tmp_path / ".claude/state/bg-agents/unknown.txt"
    assert counter.read_text().strip() == "1"


@pytest.mark.skipif(shutil.which("flock") is None, reason="flock utility unavailable")
def test_subagent_start_lock_contention_is_bounded(tmp_path):
    fcntl = pytest.importorskip("fcntl")
    _install_policy(tmp_path)
    lock_path = tmp_path / ".claude/state/bg-agents/sess-lock.txt.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        started = time.monotonic()
        result = _run_hook(tmp_path, json.dumps({"session_id": "sess-lock"}))
        elapsed = time.monotonic() - started

    assert result.returncode == 0
    assert elapsed < 1
    output = json.loads(result.stdout)
    assert output["hookSpecificOutput"]["hookEventName"] == "SubagentStart"


def test_subagent_start_registration_is_synchronous_without_bash_counter():
    hooks_path = REPO_ROOT / "src/superclaude/hooks/hooks.json"
    hooks = json.loads(hooks_path.read_text(encoding="utf-8"))["hooks"]

    subagent_hook = next(
        hook
        for registration in hooks["SubagentStart"]
        for hook in registration["hooks"]
        if hook["command"] == "~/.claude/hooks/freshness-subagent-start.sh"
    )
    assert "async" not in subagent_hook
    assert not any(
        registration.get("matcher") == "Bash"
        for registration in hooks.get("PreToolUse", [])
    )
