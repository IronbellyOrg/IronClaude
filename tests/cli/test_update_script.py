"""Regression tests for the repository update wrapper."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
UPDATE_SCRIPT = REPO_ROOT / "update.sh"
EXPECTED_COMMANDS = [
    "pipx install --force ./",
    "superclaude install --force",
    "make sync-dev",
    "superclaude doctor",
]

_STUB = """#!/usr/bin/env bash
set -u
name="$(basename "$0")"
printf '%s|%s|%s\n' "$name" "$PWD" "$*" >> "$UPDATE_LOG"
if [[ "$name $*" == "${FAIL_COMMAND:-}" ]]; then
    exit 23
fi
"""


def _logged_command(line: str) -> str:
    name, _cwd, arguments = line.split("|", 2)
    return f"{name} {arguments}".strip()


def _run_update(tmp_path: Path, failing_command: str = ""):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name in ("pipx", "superclaude", "make"):
        stub = bin_dir / name
        stub.write_text(_STUB, encoding="utf-8")
        stub.chmod(0o755)

    log_path = tmp_path / "update.log"
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
            "UPDATE_LOG": str(log_path),
            "FAIL_COMMAND": failing_command,
        }
    )
    result = subprocess.run(
        [str(UPDATE_SCRIPT)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    lines = log_path.read_text(encoding="utf-8").splitlines()
    return result, lines


def test_update_runs_from_repository_root_and_verifies_global_install(tmp_path):
    result, lines = _run_update(tmp_path)

    assert result.returncode == 0, result.stderr
    assert [_logged_command(line) for line in lines] == EXPECTED_COMMANDS
    assert {line.split("|", 2)[1] for line in lines} == {str(REPO_ROOT)}


@pytest.mark.parametrize(
    ("failing_command", "expected_call_count"),
    [
        ("pipx install --force ./", 1),
        ("superclaude install --force", 2),
        ("make sync-dev", 3),
        ("superclaude doctor", 4),
    ],
)
def test_update_stops_and_propagates_each_stage_failure(
    tmp_path, failing_command, expected_call_count
):
    result, lines = _run_update(tmp_path, failing_command=failing_command)

    assert result.returncode == 23
    assert len(lines) == expected_call_count
    assert _logged_command(lines[-1]) == failing_command
