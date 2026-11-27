"""Regression tests for the crash-recovery bootstrap scanner."""

from __future__ import annotations

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import pytest

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


@pytest.mark.parametrize(
    "case", ["absent", "empty", "large_sessions", "large_artifacts"]
)
def test_bootstrap_scan_empty_and_large_inventories(tmp_path, case):
    project = tmp_path / "project"
    home = tmp_path / "home"
    project.mkdir()
    home.mkdir()
    env = {
        "PATH": os.environ["PATH"],
        "HOME": str(home),
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
    }
    subprocess.run(["git", "init", "-q", str(project)], env=env, check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(project),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.invalid",
            "commit",
            "--allow-empty",
            "-qm",
            "fixture",
        ],
        env=env,
        check=True,
    )
    session_dir = (
        home
        / ".claude/projects"
        / ("-" + str(project.resolve()).lstrip("/").replace("/", "-"))
    )
    if case != "absent":
        session_dir.mkdir(parents=True)
        memory = project / ".superclaude/memory/topic"
        memory.mkdir(parents=True)
        (memory / "one.md").touch()
        (memory / "two.md").touch()
        (memory / "ignored.txt").touch()
    if case == "large_sessions":
        for index in range(2000):
            (session_dir / f"session-{index:05d}.jsonl").touch()
    if case == "large_artifacts":
        for index in range(2000):
            artifact = project / ".dev/research" / f"artifact-{index:05d}"
            artifact.mkdir(parents=True)
            for name in (
                "manifest.json",
                ".roadmap-state.json",
                "execution-log.jsonl",
                ".sprint-exitcode",
            ):
                (artifact / name).touch()

    result = subprocess.run(
        ["bash", str(BOOTSTRAP_SCAN), str(project)],
        env=env,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["git"]["is_repo"] is True
    assert payload["session_log_dir_exists"] is (case != "absent")
    assert len(payload["recent_sessions"]) == (3 if case == "large_sessions" else 0)
    assert payload["has_memory"] is (case != "absent")
    assert payload["memory_count"] == (0 if case == "absent" else 2)
    if case == "large_artifacts":
        for key in (
            "recent_manifests",
            "recent_roadmap_states",
            "recent_execution_logs",
            "recent_exit_codes",
        ):
            assert len(payload[key]) == 20
        datetime.strptime(
            payload["most_recent_mtimes"]["dev_research"], "%Y-%m-%dT%H:%M:%SZ"
        )
