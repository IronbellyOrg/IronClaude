"""
Unit tests for install_hooks.py — the atomic additive-merge installer for
hook scripts and settings.json hook registrations.

Acceptance criteria (T04.01, freshness-system tasklist):
  Minimum 8 test cases covering:
    1. Empty target settings.json
    2. Existing top-level hooks key with unrelated events
    3. Existing same-event with different matcher
    4. Existing same-event+same-matcher (collision case)
    5. Malformed target JSON (graceful refuse)
    6. Missing target file (creates)
    7. Permission denied (clear error message)
    8. Atomic write rollback on crash

These tests use tempdir fixtures so they never touch a user's real
~/.claude/settings.json.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.install_hooks import (
    _backup_path,
    _atomic_write_json,
    install_hooks,
    validate_session_id,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def fake_source_hooks(tmp_path, monkeypatch):
    """
    Stand up a fake src/superclaude/hooks/ tree (hooks.json + scripts/) and
    point install_hooks's source-locator functions at it.

    Returns (package_root, hooks_json_path, scripts_dir).
    """
    pkg_root = tmp_path / "pkg"
    hooks_pkg = pkg_root / "hooks"
    scripts_pkg = hooks_pkg / "scripts"
    legacy_scripts_pkg = pkg_root / "scripts"
    scripts_pkg.mkdir(parents=True)
    legacy_scripts_pkg.mkdir(parents=True)

    hooks_json = {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "*",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "~/.claude/hooks/freshness-session-start.sh",
                            "timeout": 5,
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Edit|Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "~/.claude/hooks/freshness-pre-edit.sh",
                            "timeout": 1,
                        }
                    ],
                }
            ],
        }
    }
    (hooks_pkg / "hooks.json").write_text(json.dumps(hooks_json, indent=2))

    for name in [
        "freshness-session-start.sh",
        "freshness-user-prompt.sh",
        "freshness-pre-edit.sh",
        "freshness-post-read.sh",
        "freshness-file-changed.sh",
        "freshness-subagent-start.sh",
        "freshness-subagent-stop.sh",
    ]:
        (scripts_pkg / name).write_text("#!/usr/bin/env bash\nexit 0\n")
    (legacy_scripts_pkg / "session-init.sh").write_text("#!/usr/bin/env bash\nexit 0\n")

    monkeypatch.setattr(
        "superclaude.cli.install_hooks._get_hooks_source",
        lambda: hooks_pkg / "hooks.json",
    )
    monkeypatch.setattr(
        "superclaude.cli.install_hooks._get_hooks_scripts_source",
        lambda: scripts_pkg,
    )
    monkeypatch.setattr(
        "superclaude.cli.install_hooks._get_legacy_scripts_source",
        lambda: legacy_scripts_pkg,
    )

    return pkg_root


@pytest.fixture
def target_settings(tmp_path):
    """Return a Path pointing to a fresh, non-existent settings.json target."""
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    return home / ".claude" / "settings.json"


# ---------------------------------------------------------------------------
# Case 1: missing target file (creates)
# ---------------------------------------------------------------------------


def test_case_1_missing_target_creates(fake_source_hooks, target_settings):
    assert not target_settings.exists()

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert ok, msg
    assert target_settings.exists()

    data = json.loads(target_settings.read_text())
    assert "hooks" in data
    assert set(data["hooks"].keys()) == {"SessionStart", "PreToolUse"}
    # Scripts copied
    hooks_dir = target_settings.parent / "hooks"
    assert (hooks_dir / "freshness-pre-edit.sh").exists()
    assert (hooks_dir / "freshness-pre-edit.sh").stat().st_mode & 0o111


# ---------------------------------------------------------------------------
# Case 2: empty target file (parses as {}, gets merged)
# ---------------------------------------------------------------------------


def test_case_2_empty_target_settings(fake_source_hooks, target_settings):
    target_settings.write_text("{}\n")

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert ok, msg

    data = json.loads(target_settings.read_text())
    assert "hooks" in data and len(data["hooks"]) == 2


# ---------------------------------------------------------------------------
# Case 3: existing top-level hooks with unrelated events — preserved
# ---------------------------------------------------------------------------


def test_case_3_unrelated_events_preserved(fake_source_hooks, target_settings):
    target_settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "Stop": [
                        {
                            "hooks": [
                                {"type": "command", "command": "~/my-stop.sh", "timeout": 1}
                            ]
                        }
                    ]
                },
                "unrelated_key": {"foo": "bar"},
            },
            indent=2,
        )
    )

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert ok, msg

    data = json.loads(target_settings.read_text())
    # Unrelated event preserved
    assert "Stop" in data["hooks"]
    assert data["hooks"]["Stop"][0]["hooks"][0]["command"] == "~/my-stop.sh"
    # Unrelated top-level key preserved
    assert data["unrelated_key"] == {"foo": "bar"}
    # New events added
    assert "SessionStart" in data["hooks"]
    assert "PreToolUse" in data["hooks"]


# ---------------------------------------------------------------------------
# Case 4a: existing same-event, DIFFERENT matcher — both kept
# ---------------------------------------------------------------------------


def test_case_4a_same_event_different_matcher(fake_source_hooks, target_settings):
    target_settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "PreToolUse": [
                        {
                            "matcher": "Bash",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": "~/my-bash-prehook.sh",
                                    "timeout": 1,
                                }
                            ],
                        }
                    ]
                }
            },
            indent=2,
        )
    )

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert ok, msg

    data = json.loads(target_settings.read_text())
    matchers = [r.get("matcher") for r in data["hooks"]["PreToolUse"]]
    assert "Bash" in matchers  # user's existing hook preserved
    assert "Edit|Write" in matchers  # freshness hook added


# ---------------------------------------------------------------------------
# Case 4b: existing same-event, SAME matcher — skipped without force
# ---------------------------------------------------------------------------


def test_case_4b_collision_skipped_without_force(fake_source_hooks, target_settings):
    user_reg = {
        "matcher": "Edit|Write",
        "hooks": [
            {"type": "command", "command": "~/my-edit-hook.sh", "timeout": 2}
        ],
    }
    target_settings.write_text(
        json.dumps({"hooks": {"PreToolUse": [user_reg]}}, indent=2)
    )

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert ok, msg

    data = json.loads(target_settings.read_text())
    # Only one registration (user's), freshness skipped
    assert len(data["hooks"]["PreToolUse"]) == 1
    assert data["hooks"]["PreToolUse"][0]["hooks"][0]["command"] == "~/my-edit-hook.sh"
    assert "skipped-collision=1" in msg


def test_case_4c_collision_replaced_with_force(fake_source_hooks, target_settings):
    user_reg = {
        "matcher": "Edit|Write",
        "hooks": [
            {"type": "command", "command": "~/my-edit-hook.sh", "timeout": 2}
        ],
    }
    target_settings.write_text(
        json.dumps({"hooks": {"PreToolUse": [user_reg]}}, indent=2)
    )

    ok, msg = install_hooks(target_path=target_settings, force=True)
    assert ok, msg

    data = json.loads(target_settings.read_text())
    assert len(data["hooks"]["PreToolUse"]) == 1
    assert (
        data["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        == "~/.claude/hooks/freshness-pre-edit.sh"
    )
    assert "replaced=1" in msg


# ---------------------------------------------------------------------------
# Case 5: malformed target JSON — graceful refuse, target untouched
# ---------------------------------------------------------------------------


def test_case_5_malformed_target_refused(fake_source_hooks, target_settings):
    target_settings.write_text("{not valid json...")

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert not ok
    assert "malformed" in msg.lower()
    # Backup was created BEFORE the refuse → preserves the bad file for the user
    backup_files = list(target_settings.parent.glob(f"{target_settings.name}.bak.*"))
    assert backup_files, "Backup should exist for malformed-target refusal"
    # Target itself is unchanged
    assert target_settings.read_text() == "{not valid json..."


# ---------------------------------------------------------------------------
# Case 6: permission denied (clear error message)
# ---------------------------------------------------------------------------


def test_case_6_permission_denied(fake_source_hooks, target_settings):
    target_settings.write_text(json.dumps({"hooks": {}}, indent=2))
    # Make parent dir read-only to fail the atomic write
    parent = target_settings.parent
    os.chmod(parent, 0o555)

    try:
        ok, msg = install_hooks(target_path=target_settings, force=False)
        assert not ok
        # Permission error should be in the message
        assert (
            "permission" in msg.lower()
            or "denied" in msg.lower()
            or "atomic write" in msg.lower()
            or "could not" in msg.lower()
        ), msg
    finally:
        os.chmod(parent, 0o755)


# ---------------------------------------------------------------------------
# Case 7: backup is created before any write to existing file
# ---------------------------------------------------------------------------


def test_case_7_backup_before_write(fake_source_hooks, target_settings):
    original_content = json.dumps({"hooks": {"Stop": []}, "marker": "user-value"})
    target_settings.write_text(original_content)

    ok, msg = install_hooks(target_path=target_settings, force=False)
    assert ok, msg

    backup_files = list(target_settings.parent.glob(f"{target_settings.name}.bak.*"))
    assert len(backup_files) == 1
    assert backup_files[0].read_text() == original_content


# ---------------------------------------------------------------------------
# Case 8: atomic write — no partial-write window on crash
# ---------------------------------------------------------------------------


def test_case_8_atomic_write_no_partial(tmp_path):
    target = tmp_path / "settings.json"
    target.write_text(json.dumps({"version": 1}))
    original = target.read_text()

    # Simulate a crash mid-write: patch os.replace to raise BEFORE rename.
    # The temp file should NOT have replaced the target.
    with patch(
        "superclaude.cli.install_hooks.os.replace",
        side_effect=OSError("simulated crash"),
    ):
        with pytest.raises(OSError):
            _atomic_write_json(target, {"version": 2})

    # Target still has the original (atomic guarantee)
    assert target.read_text() == original
    # Temp file cleaned up
    tmp_files = list(tmp_path.glob(f".{target.name}.tmp.*"))
    assert not tmp_files


# ---------------------------------------------------------------------------
# Bonus: backup-path helper produces unique, sortable names
# ---------------------------------------------------------------------------


def test_backup_path_format(tmp_path):
    target = tmp_path / "settings.json"
    target.touch()
    b1 = _backup_path(target)
    # Has the .bak. prefix and a Zulu timestamp suffix
    assert ".bak." in b1.name
    assert b1.name.endswith("Z")


# ---------------------------------------------------------------------------
# Bonus: session_id sanitization helper
# ---------------------------------------------------------------------------


def test_session_id_validator():
    assert validate_session_id("abc123")
    assert validate_session_id("session_id-42")
    assert not validate_session_id("../etc/passwd")
    assert not validate_session_id("a b")
    assert not validate_session_id("")
    assert not validate_session_id(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# End-to-end smoke: fresh + existing + force chain
# ---------------------------------------------------------------------------


def test_smoke_install_then_reinstall_force(fake_source_hooks, target_settings):
    ok1, msg1 = install_hooks(target_path=target_settings, force=False)
    assert ok1, msg1

    # Second run without force: same-matcher collisions → all skipped
    ok2, msg2 = install_hooks(target_path=target_settings, force=False)
    assert ok2, msg2
    assert "skipped-collision" in msg2

    # Third run with force: replaces in place
    ok3, msg3 = install_hooks(target_path=target_settings, force=True)
    assert ok3, msg3
    assert "replaced=" in msg3

    data = json.loads(target_settings.read_text())
    assert set(data["hooks"].keys()) == {"SessionStart", "PreToolUse"}
