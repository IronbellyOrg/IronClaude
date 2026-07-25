"""Regression tests for the crash-recovery bootstrap scanner."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP_SCAN = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-crash-recovery"
    / "scripts"
    / "bootstrap_scan.sh"
)


def test_bootstrap_scan_resolves_session_logs_from_home(tmp_path):
    project = tmp_path / "project"
    home = tmp_path / "home"
    project.mkdir()

    encoded_cwd = "-" + str(project.resolve()).lstrip("/").replace("/", "-")
    session_dir = home / ".claude" / "projects" / encoded_cwd
    session_dir.mkdir(parents=True)
    session_log = session_dir / "session.jsonl"
    session_log.write_text("{}\n", encoding="utf-8")

    env = os.environ.copy()
    env["HOME"] = str(home)
    result = subprocess.run(
        [str(BOOTSTRAP_SCAN), str(project)],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["session_log_dir"] == str(session_dir)
    assert payload["session_log_dir_exists"] is True
    assert payload["recent_sessions"] == [str(session_log)]
