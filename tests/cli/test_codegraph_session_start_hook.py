"""The codegraph SessionStart hook: runs the real script against a stub ``codegraph``.

HOME, XDG_STATE_HOME and PATH point into ``tmp_path``; the stub appends one line per
argument to a file, so no test needs a real codegraph or the network.
"""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path

import pytest

HOOK = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/hooks/scripts/codegraph-session-start.sh"
)
GIT = "/usr/bin:/bin"  # the hook needs `git`; the stub dirs come first on PATH


class Box:
    def __init__(self, tmp_path):
        self.tmp = tmp_path
        self.home = tmp_path / "home"
        self.home.mkdir()
        self.state = tmp_path / "state"
        self.bin = tmp_path / "bin"
        self.bin.mkdir()
        self.argv_log = tmp_path / "argv.log"
        self.pid_file = tmp_path / "stub.pid"

    def stub(self, path: Path, name: str = "stub", sleep: int = 0) -> Path:
        """A codegraph stub: records its argv (one line per argument) and a marker."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "#!/bin/sh\n"
            f'echo "== {name}" >> "{self.argv_log}"\n'
            f'for a in "$@"; do printf \'%s\\n\' "$a" >> "{self.argv_log}"; done\n'
            + (f'echo $$ > "{self.pid_file}"\nexec sleep {sleep}\n' if sleep else "")
        )
        path.chmod(0o755)
        return path

    def repo(self, name: str = "repo") -> Path:
        top = self.tmp / name
        top.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(top)], check=True, env=self.env())
        return top

    def env(self, **extra) -> dict:
        env = {
            "HOME": str(self.home),
            "XDG_STATE_HOME": str(self.state),
            "PATH": f"{self.bin}:{GIT}",
            "GIT_CONFIG_GLOBAL": "/dev/null",
            "GIT_CONFIG_NOSYSTEM": "1",
        }
        env.update(extra)
        return env

    def run(self, cwd: Path, **extra) -> subprocess.CompletedProcess:
        done = subprocess.run(
            ["sh", str(HOOK)],
            cwd=cwd,
            env=self.env(**extra),
            input="{}",
            capture_output=True,
            text=True,
            timeout=8,
        )
        assert done.returncode == 0
        assert done.stdout == ""  # the hook never prints on stdout
        return done

    def calls(self, wait: float = 3.0, expect: int = 1) -> list:
        """The recorded runs as lists of lines, waiting for the detached child."""
        deadline = time.monotonic() + wait
        while time.monotonic() < deadline:
            if self.argv_log.exists():
                runs = self._runs()
                if len(runs) >= expect:
                    break
            time.sleep(0.05)
        return self._runs() if self.argv_log.exists() else []

    def _runs(self) -> list:
        runs: list = []
        for line in self.argv_log.read_text().splitlines():
            if line.startswith("== "):
                runs.append([line[3:]])
            elif runs:
                runs[-1].append(line)
        return runs

    def nothing_runs(self) -> None:
        time.sleep(0.4)  # a detached child would have written by now
        assert not self.argv_log.exists()


@pytest.fixture
def box(tmp_path):
    return Box(tmp_path)


def test_opt_out_exits_silently(box):
    box.stub(box.bin / "codegraph")
    top = box.repo()
    box.run(top, SUPERCLAUDE_CODEGRAPH_AUTOINIT="0")
    box.nothing_runs()


def test_no_binary_anywhere_exits_silently(box):
    top = box.repo()
    done = box.run(top)
    assert done.stderr == ""
    assert not box.state.exists()


def test_pointer_file_wins_over_a_different_codegraph_on_path(box):
    box.stub(box.bin / "codegraph", "on-path")
    pointed = box.stub(box.tmp / "registered" / "codegraph", "pointer")
    (box.home / ".codegraph").mkdir()
    (box.home / ".codegraph/.superclaude-bin").write_text(f"{pointed}\n")
    top = box.repo()
    box.run(top)
    assert box.calls() == [["pointer", "init", "--yes", str(top)]]


def test_pointer_to_a_missing_file_falls_back_to_path(box):
    box.stub(box.bin / "codegraph", "on-path")
    (box.home / ".codegraph").mkdir()
    (box.home / ".codegraph/.superclaude-bin").write_text("/nope/codegraph\n")
    top = box.repo()
    box.run(top)
    assert box.calls() == [["on-path", "init", "--yes", str(top)]]


def test_non_git_directory_runs_nothing(box):
    box.stub(box.bin / "codegraph")
    plain = box.tmp / "plain"
    plain.mkdir()
    box.run(plain)
    box.nothing_runs()


def test_home_as_git_top_runs_nothing(box):
    box.stub(box.bin / "codegraph")
    subprocess.run(["git", "init", "-q", str(box.home)], check=True, env=box.env())
    box.run(box.home)
    box.nothing_runs()


def test_existing_database_runs_nothing(box):
    box.stub(box.bin / "codegraph")
    top = box.repo()
    (top / ".codegraph").mkdir()
    (top / ".codegraph/codegraph.db").write_text("")
    box.run(top)
    box.nothing_runs()


def test_codegraph_dir_with_only_gitignore_still_runs_init_once(box):
    box.stub(box.bin / "codegraph")
    top = box.repo()
    (top / ".codegraph").mkdir()
    (top / ".codegraph/.gitignore").write_text("*\n!.gitignore\n")
    box.run(top)
    assert box.calls() == [["stub", "init", "--yes", str(top)]]


def test_a_fresh_checkout_runs_exactly_init_yes_top_once(box):
    box.stub(box.bin / "codegraph")
    top = box.repo()
    sub = top / "src" / "deep"
    sub.mkdir(parents=True)
    box.run(sub)  # a session started in a subdirectory indexes the top-level
    assert box.calls() == [["stub", "init", "--yes", str(top)]]
    assert (box.state / "superclaude/codegraph-init.log").exists()


def test_claude_project_dir_selects_the_checkout(box):
    box.stub(box.bin / "codegraph")
    top = box.repo()
    elsewhere = box.tmp / "elsewhere"
    elsewhere.mkdir()
    box.run(elsewhere, CLAUDE_PROJECT_DIR=str(top))
    assert box.calls() == [["stub", "init", "--yes", str(top)]]


def test_a_top_with_spaces_is_one_argument(box):
    box.stub(box.bin / "codegraph")
    top = box.repo("my project dir")
    box.run(top)
    assert box.calls() == [["stub", "init", "--yes", str(top)]]


def test_hook_returns_quickly_while_the_stub_sleeps_ten_seconds(box):
    box.stub(box.bin / "codegraph", sleep=10)
    top = box.repo()
    started = time.monotonic()
    box.run(top)  # capture_output would wait for the child if it were not detached
    assert time.monotonic() - started < 1.0
    deadline = time.monotonic() + 3
    while not box.pid_file.exists() and time.monotonic() < deadline:
        time.sleep(0.05)
    pid = int(box.pid_file.read_text())  # the child really started...
    os.kill(pid, 0)  # ...and is still running, detached from the hook
    os.kill(pid, 15)
