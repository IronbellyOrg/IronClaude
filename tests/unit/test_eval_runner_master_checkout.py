"""Regression tests for the temporary master checkout in scripts/eval_runner.py.

The eval runner used to create a permanent sibling checkout next to the
repository and never remove it. It now creates its master checkout in a
temporary directory and removes it on exit, so it works without Orca.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "eval_runner.py"


def _git(cwd: Path, *args: str) -> str:
    """Run git in a fixture repo, isolated from the caller's git config."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    env["GIT_CONFIG_NOSYSTEM"] = "1"
    proc = subprocess.run(
        ["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=True
    )
    return proc.stdout


def _make_repo(path: Path, branch: str) -> Path:
    path.mkdir()
    _git(path, "init", "-q", "-b", branch)
    _git(
        path,
        "-c",
        "user.name=eval-test",
        "-c",
        "user.email=eval-test@example.com",
        "commit",
        "-q",
        "--allow-empty",
        "-m",
        "init",
    )
    return path


def _worktree_paths(repo: Path) -> set[str]:
    out = _git(repo, "worktree", "list", "--porcelain")
    return {
        os.path.realpath(line.split(" ", 1)[1])
        for line in out.splitlines()
        if line.startswith("worktree ")
    }


@pytest.fixture
def eval_runner(monkeypatch):
    """Load scripts/eval_runner.py as a module (pattern of test_bare_review_golden_regen.py).

    The module is registered in sys.modules before exec_module: its @dataclass
    with string annotations looks the module up there.
    """
    spec = importlib.util.spec_from_file_location("eval_runner_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def temp_root(tmp_path, monkeypatch):
    """Send tempfile.mkdtemp into a known folder so leftovers can be checked."""
    root = tmp_path / "tmp"
    root.mkdir()
    monkeypatch.setattr(tempfile, "tempdir", str(root))
    return root


def test_checkout_exists_inside_and_is_removed_after(
    eval_runner, tmp_path, temp_root, monkeypatch
):
    repo = _make_repo(tmp_path / "repo", "master")
    monkeypatch.setattr(eval_runner, "REPO_ROOT", repo)

    with eval_runner.master_checkout() as checkout:
        assert checkout.is_dir()
        assert os.path.realpath(checkout) in _worktree_paths(repo)

    assert not checkout.exists()
    assert os.path.realpath(checkout) not in _worktree_paths(repo)
    assert list(temp_root.iterdir()) == []


def test_checkout_is_removed_when_body_raises(
    eval_runner, tmp_path, temp_root, monkeypatch
):
    repo = _make_repo(tmp_path / "repo", "master")
    monkeypatch.setattr(eval_runner, "REPO_ROOT", repo)

    seen: list[Path] = []
    with pytest.raises(RuntimeError, match="boom"):
        with eval_runner.master_checkout() as checkout:
            seen.append(checkout)
            raise RuntimeError("boom")

    assert seen and not seen[0].exists()
    assert os.path.realpath(seen[0]) not in _worktree_paths(repo)
    assert list(temp_root.iterdir()) == []


def test_missing_master_raises_with_git_stderr(
    eval_runner, tmp_path, temp_root, monkeypatch
):
    repo = _make_repo(tmp_path / "repo", "trunk")
    monkeypatch.setattr(eval_runner, "REPO_ROOT", repo)

    with pytest.raises(eval_runner.MasterCheckoutError) as excinfo:
        with eval_runner.master_checkout():
            pytest.fail("the body must not run without a master branch")

    message = str(excinfo.value)
    assert "master" in message
    assert "fatal" in message.lower()
    assert list(temp_root.iterdir()) == []
    assert _worktree_paths(repo) == {os.path.realpath(repo)}


def test_script_has_no_fixed_sibling_checkout():
    assert "IronClaude-eval-master" not in SCRIPT.read_text(encoding="utf-8")
