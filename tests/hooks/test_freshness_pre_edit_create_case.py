"""Behavioral tests for freshness-pre-edit.sh.

Covers the create-vs-edit distinction added to resolve F10 from
.dev/releases/complete/freshness-system/checkpoints/CP-P05-T05.01.md.
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
    / "freshness-pre-edit.sh"
)


def _run_hook(payload: dict, fake_home: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["HOME"] = str(fake_home)
    (fake_home / ".claude" / "state").mkdir(parents=True, exist_ok=True)
    (fake_home / ".claude" / "logs").mkdir(parents=True, exist_ok=True)
    return subprocess.run(
        ["bash", str(HOOK)],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=5,
    )


def test_write_to_nonexistent_file_allows(tmp_path: Path) -> None:
    """Create-case: Write to a path that does not exist is allowed."""
    target = tmp_path / "brand-new-file.md"
    assert not target.exists()
    payload = {
        "session_id": "test-create-case",
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 0, result.stderr.decode()
    telemetry = (
        tmp_path / "home" / ".claude" / "logs" / "freshness-hook.jsonl"
    ).read_text()
    assert '"reason":"create_allowed"' in telemetry
    assert '"decision":"allow"' in telemetry


def test_edit_to_existing_unread_file_still_blocks(tmp_path: Path) -> None:
    """Edit-case: existing file without prior Read still blocks (no regression)."""
    target = tmp_path / "existing.md"
    target.write_text("seeded\n")
    payload = {
        "session_id": "test-edit-case",
        "tool_name": "Edit",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 2
    assert b"You have not Read" in result.stderr
    telemetry = (
        tmp_path / "home" / ".claude" / "logs" / "freshness-hook.jsonl"
    ).read_text()
    assert '"reason":"no_prior_read"' in telemetry


def test_write_to_existing_unread_file_still_blocks(tmp_path: Path) -> None:
    """Write to an EXISTING file is an edit, not a create — gate must hold."""
    target = tmp_path / "existing.md"
    target.write_text("seeded\n")
    payload = {
        "session_id": "test-write-edit-case",
        "tool_name": "Write",
        "tool_input": {"file_path": str(target)},
        "cwd": str(tmp_path),
    }
    result = _run_hook(payload, fake_home=tmp_path / "home")
    assert result.returncode == 2
    assert b"You have not Read" in result.stderr
