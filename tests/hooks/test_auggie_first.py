"""Behavioral tests for auggie-flag-clear.sh.

Covers the auggie-first PostToolUse path from
.dev/releases/complete/auggie-first/auggie-first-hook-proposal-v2.1.md §6 and
the §14 deferred test harness, now feasible after the fixture pattern landed
in test_freshness_pre_edit_create_case.py.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

HOOK = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "superclaude"
    / "hooks"
    / "scripts"
    / "auggie-flag-clear.sh"
)


def _run_hook(payload: dict, fake_home: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    (fake_home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    (fake_home / ".claude" / "logs").mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=5,
    )


def _sticky_path(home: Path, session_id: str) -> Path:
    return home / ".claude" / "state" / "auggie-first-pending" / f"{session_id}.txt"


def test_auggie_mcp_call_clears_sticky(tmp_path: Path) -> None:
    """mcp__auggie__codebase-retrieval clears the sticky and emits telemetry."""
    home = tmp_path / "home"
    sid = "test-clear-auggie"
    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    _sticky_path(home, sid).write_text("pending\n")
    payload = {
        "session_id": sid,
        "tool_name": "mcp__auggie__codebase-retrieval",
    }
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    assert not _sticky_path(home, sid).exists()
    telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
    assert '"event":"sticky_cleared"' in telemetry
    assert '"tool":"mcp__auggie__codebase-retrieval"' in telemetry


def test_gateway_alias_clears_sticky(tmp_path: Path) -> None:
    """mcp__airis-mcp-gateway__auggie_* (gateway alias) also clears the sticky."""
    home = tmp_path / "home"
    sid = "test-clear-gateway"
    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    _sticky_path(home, sid).write_text("pending\n")
    payload = {
        "session_id": sid,
        "tool_name": "mcp__airis-mcp-gateway__auggie_codebase_retrieval",
    }
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    assert not _sticky_path(home, sid).exists()
    telemetry = (home / ".claude" / "logs" / "auggie-first.jsonl").read_text()
    assert '"event":"sticky_cleared"' in telemetry


def test_unrelated_tool_preserves_sticky(tmp_path: Path) -> None:
    """A non-auggie tool name must not clear the sticky."""
    home = tmp_path / "home"
    sid = "test-preserve-sticky"
    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    sticky = _sticky_path(home, sid)
    sticky.write_text("pending\n")
    payload = {"session_id": sid, "tool_name": "Read"}
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    assert sticky.exists(), "sticky must survive non-auggie tool calls"


def test_unknown_session_id_is_noop(tmp_path: Path) -> None:
    """Sentinel guard: never operate on the 'unknown' session_id bucket."""
    home = tmp_path / "home"
    (home / ".claude" / "state" / "auggie-first-pending").mkdir(
        parents=True, exist_ok=True
    )
    payload = {"session_id": "unknown", "tool_name": "mcp__auggie__retrieval"}
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    log = home / ".claude" / "logs" / "auggie-first.jsonl"
    assert not log.exists() or '"event":"sticky_cleared"' not in log.read_text()


def test_missing_sticky_is_fail_open(tmp_path: Path) -> None:
    """No sticky file present — hook exits 0 without writing telemetry."""
    home = tmp_path / "home"
    payload = {
        "session_id": "test-no-sticky",
        "tool_name": "mcp__auggie__codebase-retrieval",
    }
    result = _run_hook(payload, fake_home=home)
    assert result.returncode == 0, result.stderr.decode()
    log = home / ".claude" / "logs" / "auggie-first.jsonl"
    assert not log.exists() or '"sticky_cleared"' not in log.read_text()
