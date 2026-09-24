"""Isolated tests for native ccsession wiring."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from superclaude.cli.install_ccsession import wire_ccsession


@pytest.fixture
def home(tmp_path):
    skill = tmp_path / ".claude/skills/ccsession-tag"
    (skill / "hooks").mkdir(parents=True)
    source = (
        Path(__file__).resolve().parents[2] / "src/superclaude/skills/ccsession-tag"
    )
    for name in (
        "ccsession",
        "hooks/session-start.sh",
        "ccsession.env.example",
        "install.sh",
    ):
        shutil.copyfile(source / name, skill / name)
    return tmp_path


def test_wire_creates_symlink_and_env(home):
    ok, msg = wire_ccsession(home)
    assert ok, msg
    skill = home / ".claude/skills/ccsession-tag"
    dest = home / ".local/bin/ccsession"
    env = home / ".claude/ccsession.env"
    assert dest.is_symlink() and dest.resolve() == (skill / "ccsession").resolve()
    assert env.read_bytes() == (skill / "ccsession.env.example").read_bytes()
    assert env.stat().st_mode & 0o777 == 0o600
    assert (skill / "ccsession").stat().st_mode & 0o111
    assert (skill / "hooks/session-start.sh").stat().st_mode & 0o111
    assert not (home / ".claude/settings.json").exists()


def test_wire_leaves_existing_env_and_settings(home):
    env = home / ".claude/ccsession.env"
    env.write_bytes(b"secret-token")
    env.chmod(0o640)
    settings = home / ".claude/settings.json"
    settings.write_bytes(b"private settings")
    assert wire_ccsession(home)[0]
    assert wire_ccsession(home)[0]
    assert env.read_bytes() == b"secret-token"
    assert env.stat().st_mode & 0o777 == 0o640
    assert settings.read_bytes() == b"private settings"
    assert b"secret-token" not in wire_ccsession(home)[1].encode()


@pytest.mark.parametrize("script", ["ccsession", "hooks/session-start.sh"])
def test_symlinked_script_cannot_expose_existing_env(home, script):
    env = home / ".claude/ccsession.env"
    env.write_bytes(b"private-token")
    env.chmod(0o600)
    target = home / ".claude/skills/ccsession-tag" / script
    target.unlink()
    target.symlink_to(env)

    ok, _ = wire_ccsession(home)
    assert not ok
    assert env.read_bytes() == b"private-token"
    assert env.stat().st_mode & 0o777 == 0o600


@pytest.mark.parametrize("component", ["skill", "hooks"])
def test_symlinked_skill_directory_cannot_chmod_external_file(home, component):
    skill = home / ".claude/skills/ccsession-tag"
    path = skill if component == "skill" else skill / "hooks"
    moved = home / f"external-{component}"
    path.rename(moved)
    path.symlink_to(moved, target_is_directory=True)
    external = moved / ("ccsession" if component == "skill" else "session-start.sh")
    mode = external.stat().st_mode & 0o777

    assert wire_ccsession(home)[0] is False
    assert external.stat().st_mode & 0o777 == mode


def test_wire_rejects_existing_env_directory(home):
    env = home / ".claude/ccsession.env"
    env.mkdir()
    ok, message = wire_ccsession(home)
    assert not ok and "not a file" in message
    assert env.is_dir()


def test_failed_env_copy_leaves_no_partial_seed(home, monkeypatch):
    env = home / ".claude/ccsession.env"

    def fail_after_partial_write(source, target):
        target.write(b"partial")
        raise OSError("interrupted copy")

    with monkeypatch.context() as patch:
        patch.setattr(shutil, "copyfileobj", fail_after_partial_write)
        ok, message = wire_ccsession(home)
    assert not ok and "interrupted copy" in message
    assert not env.exists()
    assert not list(env.parent.glob(".ccsession-env-*"))

    assert wire_ccsession(home)[0]
    assert (
        env.read_bytes()
        == (home / ".claude/skills/ccsession-tag/ccsession.env.example").read_bytes()
    )
    assert env.stat().st_mode & 0o777 == 0o600


@pytest.mark.parametrize("kind", ["file", "foreign_symlink"])
def test_wire_refuses_unmanaged_binary(home, kind):
    dest = home / ".local/bin/ccsession"
    dest.parent.mkdir(parents=True)
    if kind == "file":
        dest.write_text("my binary")
    else:
        dest.symlink_to(home / "someone-else")
    original = dest.readlink() if dest.is_symlink() else dest.read_bytes()
    ok, msg = wire_ccsession(home)
    assert ok and "warning" in msg.lower()
    assert (dest.readlink() if dest.is_symlink() else dest.read_bytes()) == original
    assert (home / ".claude/ccsession.env").exists()


def test_wire_refreshes_managed_relative_symlink(home):
    dest = home / ".local/bin/ccsession"
    dest.parent.mkdir(parents=True)
    dest.symlink_to(
        Path(
            os.path.relpath(
                home / ".claude/skills/ccsession-tag/ccsession", dest.parent
            )
        )
    )
    ok, msg = wire_ccsession(home)
    assert ok, msg
    assert dest.readlink() == home / ".claude/skills/ccsession-tag/ccsession"


def test_wire_fails_if_skill_or_example_missing(home):
    example = home / ".claude/skills/ccsession-tag/ccsession.env.example"
    example.unlink()
    assert wire_ccsession(home)[0] is False
    assert not (home / ".local/bin/ccsession").exists()
    assert wire_ccsession(home / "no-skill")[0] is False


def test_wire_symlink_runs_help(home):
    ok, msg = wire_ccsession(home)
    assert ok, msg
    result = subprocess.run(
        [str(home / ".local/bin/ccsession"), "--help"],
        env={
            **os.environ,
            "HOME": str(home),
            "PATH": str(home / ".local/bin") + os.pathsep + os.environ["PATH"],
        },
        capture_output=True,
        text=True,
        check=True,
    )
    assert "ccsession --help" in result.stdout


def test_fallback_after_native_does_not_duplicate_hook(home):
    assert wire_ccsession(home)[0]
    settings = home / ".claude/settings.json"
    canonical = "~/.claude/skills/ccsession-tag/hooks/session-start.sh"
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {
                            "matcher": "startup|resume",
                            "hooks": [{"type": "command", "command": canonical}],
                        }
                    ]
                }
            }
        )
    )
    original = settings.read_bytes()
    script = home / ".claude/skills/ccsession-tag/install.sh"
    for _ in range(2):
        subprocess.run(
            ["bash", str(script)],
            env={**os.environ, "HOME": str(home)},
            check=True,
            capture_output=True,
        )
    assert settings.read_bytes() == original
    assert not settings.with_suffix(".json.bak").exists()


def test_fallback_does_not_claim_user_hook_mentioning_script(home):
    settings = home / ".claude/settings.json"
    hook = home / ".claude/skills/ccsession-tag/hooks/session-start.sh"
    user_command = f'notify --about "{hook}"'
    settings.write_text(
        json.dumps(
            {
                "hooks": {
                    "SessionStart": [
                        {"hooks": [{"type": "command", "command": user_command}]}
                    ]
                }
            }
        )
    )
    script = home / ".claude/skills/ccsession-tag/install.sh"
    subprocess.run(
        ["bash", str(script)],
        env={**os.environ, "HOME": str(home)},
        check=True,
        capture_output=True,
    )
    commands = [
        entry["command"]
        for group in json.loads(settings.read_text())["hooks"]["SessionStart"]
        for entry in group["hooks"]
    ]
    assert commands == [user_command, f'bash "{hook}"']
