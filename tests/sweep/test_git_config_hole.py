"""Issue 547: a sweep ``git status`` must not run a program that repository configuration
or the inherited environment names.

Each test plants a command that writes a marker file, proves with a plain ``git status``
that the plant works (the positive control), then runs the sweep's own reader
(``probes.read_worktree``, real git, no fake) and asserts the marker never appears.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from superclaude.cli.sweep import probes

integration = pytest.mark.integration
pytestmark = integration
# The autouse guard in conftest.py reads only a test function's own marks, so every
# test also carries ``@integration``.

PLAIN_STATUS = ["status", "--porcelain=v1", "-z", "--branch", "--untracked-files=all"]
FILTER_REASON = "git filter could run a program"


@pytest.fixture(autouse=True)
def _isolated_git(monkeypatch):
    """No host config, no inherited GIT_CONFIG_* keys, a fixed identity."""
    for key in ("GIT_CONFIG_COUNT", "GIT_CONFIG_PARAMETERS"):
        monkeypatch.delenv(key, raising=False)
    for n in range(8):
        monkeypatch.delenv(f"GIT_CONFIG_KEY_{n}", raising=False)
        monkeypatch.delenv(f"GIT_CONFIG_VALUE_{n}", raising=False)
    for key, value in {
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Sweep Test",
        "GIT_AUTHOR_EMAIL": "sweep-test@example.com",
        "GIT_COMMITTER_NAME": "Sweep Test",
        "GIT_COMMITTER_EMAIL": "sweep-test@example.com",
        "GIT_TERMINAL_PROMPT": "0",
        "LC_ALL": "C",
    }.items():
        monkeypatch.setenv(key, value)


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
    return proc.stdout


def make_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    """A main repository with one commit, a linked worktree and a marker path."""
    main = tmp_path / "main"
    main.mkdir()
    git(main, "init", "-q", "-b", "main")
    (main / "f.txt").write_text("aaaa\n")
    git(main, "add", "f.txt")
    git(main, "commit", "-q", "-m", "seed")
    wt = tmp_path / "wt"
    git(main, "worktree", "add", "-q", str(wt), "-b", "wtb")
    return main, wt, tmp_path / "marker"


def make_stat_dirty(path: Path) -> None:
    """Same bytes, newer mtime: git must re-read the file (and run a clean filter)."""
    st = path.stat()
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))


def hook(marker: Path) -> str:
    return f"touch {marker}; echo"


def plain_status(wt: Path) -> None:
    subprocess.run(
        ["git", "-C", str(wt), *PLAIN_STATUS],
        capture_output=True,
        timeout=60,
        check=False,
    )


def assert_plant_works(wt: Path, marker: Path) -> None:
    """Positive control: an unguarded status does run the planted command."""
    plain_status(wt)
    assert marker.exists(), "control failed: the plant did not run on a plain status"
    marker.unlink()


def sweep_read(wt: Path):
    return probes.read_worktree(wt, probes.Budget())


@integration
def test_fsmonitor_in_shared_config_does_not_run(tmp_path):
    """Route 1: core.fsmonitor in the shared .git/config."""
    main, wt, marker = make_repo(tmp_path)
    git(main, "config", "core.fsmonitor", hook(marker))
    assert_plant_works(wt, marker)

    sweep_read(wt)

    assert not marker.exists()


@integration
def test_fsmonitor_through_include_path_does_not_run(tmp_path):
    """Route 4: include.path pulls in a file that sets core.fsmonitor."""
    main, wt, marker = make_repo(tmp_path)
    inc = tmp_path / "inc.cfg"
    inc.write_text(f"[core]\n\tfsmonitor = {hook(marker)}\n")
    git(main, "config", "include.path", str(inc))
    assert_plant_works(wt, marker)

    sweep_read(wt)

    assert not marker.exists()


@integration
def test_per_worktree_fsmonitor_does_not_run(tmp_path):
    """Route 5: per-worktree config (extensions.worktreeConfig)."""
    main, wt, marker = make_repo(tmp_path)
    git(main, "config", "extensions.worktreeConfig", "true")
    git(wt, "config", "--worktree", "core.fsmonitor", hook(marker))
    assert_plant_works(wt, marker)

    sweep_read(wt)

    assert not marker.exists()


@integration
def test_fsmonitor_from_git_config_count_env_does_not_run(tmp_path, monkeypatch):
    """Route 6: GIT_CONFIG_COUNT / KEY_0 / VALUE_0 name core.fsmonitor."""
    _main, wt, marker = make_repo(tmp_path)
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.fsmonitor")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", hook(marker))
    assert_plant_works(wt, marker)

    sweep_read(wt)

    assert not marker.exists()


@integration
def test_fsmonitor_from_git_config_parameters_env_does_not_run(tmp_path, monkeypatch):
    """Route 6b: the GIT_CONFIG_PARAMETERS form of the environment route."""
    _main, wt, marker = make_repo(tmp_path)
    monkeypatch.setenv("GIT_CONFIG_PARAMETERS", f"'core.fsmonitor={hook(marker)}'")
    assert_plant_works(wt, marker)

    sweep_read(wt)

    assert not marker.exists()


def _select_filter(main: Path, wt: Path, name: str) -> None:
    """Track a file and a .gitattributes that selects driver ``name``; no config yet."""
    (wt / ".gitattributes").write_text(f"* filter={name}\n")
    git(wt, "add", ".gitattributes")
    git(wt, "commit", "-q", "-m", "select filter")


@integration
def test_filter_clean_selected_by_a_tracked_path_does_not_run(tmp_path):
    """Route 2: filter.<d>.clean selected by a tracked path; the worktree is unscanned."""
    main, wt, marker = make_repo(tmp_path)
    _select_filter(main, wt, "x")
    git(main, "config", "filter.x.clean", f"sh -c 'touch {marker}; cat'")
    make_stat_dirty(wt / "f.txt")
    assert_plant_works(wt, marker)
    make_stat_dirty(wt / "f.txt")

    _state, row = sweep_read(wt)

    assert not marker.exists()
    assert row.coverage == "unscanned"
    assert row.unscanned == FILTER_REASON


@integration
def test_filter_process_selected_by_a_tracked_path_does_not_run(tmp_path):
    """Route 3: filter.<d>.process selected by a tracked path; the worktree is unscanned."""
    main, wt, marker = make_repo(tmp_path)
    _select_filter(main, wt, "x")
    git(main, "config", "filter.x.process", f"touch {marker}")
    make_stat_dirty(wt / "f.txt")
    assert_plant_works(wt, marker)
    make_stat_dirty(wt / "f.txt")

    _state, row = sweep_read(wt)

    assert not marker.exists()
    assert row.coverage == "unscanned"
    assert row.unscanned == FILTER_REASON


@integration
def test_filter_defined_but_selected_by_no_path_is_still_read(tmp_path):
    """Control: a filter defined (as /etc/gitconfig defines lfs) but selected by nothing."""
    main, wt, marker = make_repo(tmp_path)
    git(main, "config", "filter.lfs.clean", f"sh -c 'touch {marker}; cat'")
    git(main, "config", "filter.lfs.process", f"touch {marker}")
    make_stat_dirty(wt / "f.txt")

    state, row = sweep_read(wt)

    assert not marker.exists()
    assert row.coverage == "read"
    assert row.unscanned is None
    assert state.status_read is True  # the status was read, so the branch was parsed


def _add_submodule(main: Path, wt: Path, tmp_path: Path) -> Path:
    src = tmp_path / "subsrc"
    src.mkdir()
    git(src, "init", "-q", "-b", "main")
    (src / "s.txt").write_text("s\n")
    git(src, "add", "s.txt")
    git(src, "commit", "-q", "-m", "s")
    git(
        main,
        "-c",
        "protocol.file.allow=always",
        "submodule",
        "add",
        "-q",
        str(src),
        "sub",
    )
    git(main, "commit", "-q", "-m", "add sub")
    git(wt, "merge", "-q", "main")
    git(wt, "-c", "protocol.file.allow=always", "submodule", "update", "--init", "-q")
    return wt / "sub"


@integration
def test_submodule_fsmonitor_does_not_run(tmp_path):
    """Route 8: a submodule's own core.fsmonitor (the outer status starts a child status)."""
    main, wt, marker = make_repo(tmp_path)
    sub = _add_submodule(main, wt, tmp_path)
    git(sub, "config", "core.fsmonitor", hook(marker))
    (sub / "s.txt").write_text("changed\n")
    assert_plant_works(wt, marker)

    sweep_read(wt)

    assert not marker.exists()


@integration
def test_submodule_local_filter_does_not_run(tmp_path):
    """Route 9: a filter named only in the submodule's own config."""
    main, wt, marker = make_repo(tmp_path)
    sub = _add_submodule(main, wt, tmp_path)
    (sub / ".gitattributes").write_text("* filter=y\n")
    git(sub, "config", "filter.y.clean", f"sh -c 'touch {marker}; cat'")
    (sub / "s.txt").write_text("t\n")
    make_stat_dirty(sub / "s.txt")
    assert_plant_works(wt, marker)
    make_stat_dirty(sub / "s.txt")

    sweep_read(wt)

    assert not marker.exists()
