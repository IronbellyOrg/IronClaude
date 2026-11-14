"""Read-only guarantees of the sweep (NFR-001, NFR-002, NFR-013, FR-025; DESIGN section 11).

The recorded-argv and env tests patch ``probes.subprocess.run``. The snapshot-diff tests
run ``superclaude sweep run`` through ``CliRunner`` with ``patch_orca`` and ``patch_git``.
The one real-git test carries the ``integration`` marker, so the autouse guard in
``conftest.py`` lets it start git; it is the only test here that does.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import warnings
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from click.testing import CliRunner

from superclaude.cli.sweep import commands, probes, sweep_group
from superclaude.cli.sweep.models import SweepContext

REPO_ROOT = Path(__file__).resolve().parents[2]
STATUS_ARGS = probes.ALLOWED_GIT[0]

GIT = shutil.which("git")

RUN = "run_000000000001"
WORKER_LIST = ("orchestration", "worker-list", "--run", RUN, "--json")
TASKS_READY = ("orchestration", "task-list", "--ready", "--run", RUN, "--json")
TASKS_ALL = ("orchestration", "task-list", "--run", RUN, "--json")
WORKTREE_PS = ("worktree", "ps", "--json")

_FIXED_IDENTITY = {
    "GIT_CONFIG_GLOBAL": "/dev/null",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Sweep Test",
    "GIT_AUTHOR_EMAIL": "sweep-test@example.com",
    "GIT_COMMITTER_NAME": "Sweep Test",
    "GIT_COMMITTER_EMAIL": "sweep-test@example.com",
    "GIT_TERMINAL_PROMPT": "0",
    "LC_ALL": "C",
}


class _RunRecorder:
    """Stands in for ``subprocess.run``; keeps each argv, keyword set and env."""

    def __init__(self) -> None:
        self.calls: list[dict] = []

    def __call__(self, argv, **kwargs):
        self.calls.append(
            {"argv": list(argv), "kwargs": kwargs, "env": kwargs.get("env")}
        )
        # Only status prints a branch header; the inspections before it (issue 547) see none.
        stdout = b"## main\0" if argv[6] == "status" else b""
        return SimpleNamespace(returncode=0, stdout=stdout, stderr=b"")


@pytest.fixture
def recorder(monkeypatch) -> _RunRecorder:
    rec = _RunRecorder()
    # Patched inside the test, after the autouse guard has patched the same attribute.
    monkeypatch.setattr(probes.subprocess, "run", rec)
    return rec


def test_git_argv_and_env_are_lock_free(recorder, monkeypatch):
    monkeypatch.setenv(
        "GIT_OPTIONAL_LOCKS", "1"
    )  # a caller's value must not leak through
    worktree = Path("/work/tree-a")

    out = probes._git(worktree, *STATUS_ARGS, timeout=5.0)

    assert out == "## main\0"
    (call,) = recorder.calls
    argv = call["argv"]
    assert argv[0] == "git"
    assert argv[1] == "--no-optional-locks"
    assert argv[2] == "-C"
    assert argv[3] == str(worktree)
    assert argv[4:6] == ["-c", "core.fsmonitor=false"]
    assert argv[6:] == list(STATUS_ARGS)
    assert call["env"]["GIT_OPTIONAL_LOCKS"] == "0"
    assert call["kwargs"]["timeout"] == 5.0
    assert call["kwargs"]["check"] is False


def test_check_git_args_allows_only_the_listed_call(recorder):
    probes.check_git_args(STATUS_ARGS)  # the one allowed call passes

    with pytest.raises(ValueError):
        probes.check_git_args(("rev-parse",))
    with pytest.raises(ValueError):
        probes._git(Path("/work/tree-a"), "rev-parse", timeout=5.0)
    assert recorder.calls == []  # a rejected call never reaches a subprocess


# --- One git argv per discovered worktree (FR-025, NFR-002) -------------------------------


def _canned_orca(patch_orca, worktrees: list[Path]) -> None:
    """Answer the four reads of a one-Run sweep; ``worktree ps`` lists ``worktrees``."""
    patch_orca.respond(WORKER_LIST, {"workers": []})
    patch_orca.respond(TASKS_READY, {"tasks": []})
    patch_orca.respond(TASKS_ALL, {"tasks": []})
    patch_orca.respond(
        WORKTREE_PS, {"worktrees": [{"path": str(path)} for path in worktrees]}
    )


def _collect(sweep_root, fixed_now) -> None:
    window = timedelta(hours=6)
    ctx = SweepContext(fixed_now, window, fixed_now - window, sweep_root.root, (RUN,))
    probes.collect(ctx, (RUN,), sweep_root.root, probes.Budget())


@pytest.fixture
def no_orca_version_file(monkeypatch):
    """``collect`` reads Orca's package.json; a test must not depend on the host's copy."""
    monkeypatch.setattr(probes, "read_orca_version", lambda: None)


@pytest.mark.parametrize("extra", [0, 1, 2], ids=["root-only", "one-more", "two-more"])
def test_collect_makes_one_git_call_per_worktree_that_ps_reports(
    sweep_root, patch_orca, patch_git, fixed_now, no_orca_version_file, extra
):
    others = [sweep_root.worktree(f"wt-{n}") for n in range(extra)]
    _canned_orca(patch_orca, others)

    _collect(sweep_root, fixed_now)

    expected = [sweep_root.root.resolve(), *(p.resolve() for p in others)]
    assert [c["cwd"] for c in patch_git.calls] == expected
    assert all(c["args"] == STATUS_ARGS for c in patch_git.calls)
    assert len(patch_git.calls) == extra + 1


def test_collect_reaches_git_with_a_lock_free_argv_for_each_worktree(
    sweep_root, patch_orca, recorder, fixed_now, no_orca_version_file
):
    # The same path through ``collect``, with the real ``_git`` over a recorded ``run``.
    others = [sweep_root.worktree("wt-a"), sweep_root.worktree("wt-b")]
    _canned_orca(patch_orca, others)

    _collect(sweep_root, fixed_now)

    expected = [sweep_root.root.resolve(), *(p.resolve() for p in others)]
    git_calls = [c for c in recorder.calls if c["argv"][0] == "git"]
    status_calls = [c for c in git_calls if c["argv"][6] == "status"]
    assert [c["argv"][3] for c in status_calls] == [str(p) for p in expected]
    # Every worktree is inspected (config) before its one status; no driver, no more calls.
    assert [c["argv"][6] for c in git_calls] == ["config", "status"] * len(expected)
    for call in status_calls:
        assert call["argv"][:3] == ["git", "--no-optional-locks", "-C"]
        assert call["argv"][4:6] == ["-c", "core.fsmonitor=false"]
        assert call["argv"][6:] == list(STATUS_ARGS)
        assert call["env"]["GIT_OPTIONAL_LOCKS"] == "0"


# --- The snapshot helper (NFR-001) -------------------------------------------------------


def _record(seen: dict[str, tuple], path: Path) -> None:
    """One entry per path: ``(kind, size, st_mtime_ns, sha256)``.

    A folder records its kind only: its own mtime moves whenever a child is added, which
    the diff already reports as the child. A symlink is recorded by its target and never
    followed.
    """
    st = os.lstat(path)
    if stat.S_ISLNK(st.st_mode):
        entry = ("link", None, None, os.readlink(path))
    elif stat.S_ISDIR(st.st_mode):
        entry = ("dir", None, None, None)
    elif stat.S_ISREG(st.st_mode):
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 16), b""):
                digest.update(chunk)
        entry = ("file", st.st_size, st.st_mtime_ns, digest.hexdigest())
    else:  # a socket or fifo is never opened
        entry = ("other", st.st_size, st.st_mtime_ns, None)
    seen[str(path)] = entry


def snapshot(paths) -> dict[str, tuple]:
    """Walk each path with ``os.walk``; record path, size, ``st_mtime_ns`` and SHA-256.

    Paths may overlap (``HOME`` holds the state dir): a path is recorded once.
    """
    seen: dict[str, tuple] = {}
    for top in map(Path, paths):
        if not os.path.lexists(top):
            continue
        _record(seen, top)
        for folder, dirs, files in os.walk(top):  # followlinks stays False
            for name in (*dirs, *files):
                _record(seen, Path(folder) / name)
    return seen


def diff(before: dict[str, tuple], after: dict[str, tuple]):
    """``(added, removed, modified)`` as three sets of paths."""
    added = set(after) - set(before)
    removed = set(before) - set(after)
    modified = {p for p in set(before) & set(after) if before[p] != after[p]}
    return added, removed, modified


def assert_only_added(before, after, expected: set[Path]) -> None:
    added, removed, modified = diff(before, after)
    assert not removed, f"removed: {sorted(removed)}"
    assert not modified, f"modified: {sorted(modified)}"
    assert added == {str(p) for p in expected}, f"added: {sorted(added)}"


def _tree(base: Path) -> Path:
    top = base / "tree"
    (top / "sub").mkdir(parents=True)
    (top / "a.txt").write_text("alpha\n")
    (top / "sub" / "b.txt").write_text("bravo\n")
    return top


def _add_file(top: Path) -> None:
    (top / "sub" / "new.txt").write_text("new\n")


def _add_folder(top: Path) -> None:
    (top / "newdir").mkdir()


def _remove_file(top: Path) -> None:
    (top / "a.txt").unlink()


def _rewrite_same_size(top: Path) -> None:
    target = top / "a.txt"
    stamp = target.stat()
    target.write_text("ALPHA\n")  # same size
    os.utime(target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))  # same mtime


def _touch_only(top: Path) -> None:
    target = top / "a.txt"
    stamp = target.stat()
    os.utime(target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns + 1_000_000_000))


def _grow(top: Path) -> None:
    target = top / "a.txt"
    stamp = target.stat()
    target.write_text("alpha, longer\n")
    os.utime(
        target, ns=(stamp.st_atime_ns, stamp.st_mtime_ns)
    )  # only size and hash move


def _link(top: Path) -> None:
    (top / "ln").symlink_to("a.txt")


@pytest.mark.parametrize(
    ("change", "bucket"),
    [
        pytest.param(_add_file, "added", id="new-file"),
        pytest.param(_add_folder, "added", id="new-folder"),
        pytest.param(_link, "added", id="new-symlink"),
        pytest.param(_remove_file, "removed", id="removed-file"),
        pytest.param(_rewrite_same_size, "modified", id="same-size-same-mtime-content"),
        pytest.param(_touch_only, "modified", id="mtime-only"),
        pytest.param(_grow, "modified", id="size-and-content"),
    ],
)
def test_snapshot_diff_detects_each_kind_of_change(tmp_path, change, bucket):
    top = _tree(tmp_path)
    before = snapshot([top])
    assert diff(before, snapshot([top])) == (
        set(),
        set(),
        set(),
    )  # a quiet tree is clean

    change(top)
    result = dict(zip(("added", "removed", "modified"), diff(before, snapshot([top]))))

    assert result[bucket], f"{change.__name__} was not reported as {bucket}"
    assert [k for k, v in result.items() if v] == [bucket]


def test_snapshot_records_overlapping_paths_once(tmp_path):
    top = _tree(tmp_path)

    both = snapshot([top, top / "sub"])

    assert both == snapshot([top])


# --- NFR-001: a sweep adds exactly one report file --------------------------------------


@pytest.fixture
def sweep_env(
    sweep_root,
    patch_orca,
    patch_git,
    monkeypatch,
    tmp_path,
    fixed_now,
    no_orca_version_file,
):
    """A root, a second worktree, ``HOME`` and the XDG dirs, with the seams faked.

    Every source the sweep reads has a real file: a package ledger, a transcript and a
    ccsession tab entry. ``paths`` lists what the snapshot covers.
    """
    xdg = []
    for var, sub in (
        ("XDG_CONFIG_HOME", "config"),
        ("XDG_DATA_HOME", "data"),
        ("XDG_CACHE_HOME", "cache"),
    ):
        folder = tmp_path / "xdg" / sub
        folder.mkdir(parents=True)
        monkeypatch.setenv(var, str(folder))
        xdg.append(folder)
    other = sweep_root.worktree("wt-a")
    sweep_root.package("pkg-a", worktree=other, ledger="ledger\n")
    sweep_root.transcript(stamps=(fixed_now,), worktree=other)
    sweep_root.tab_entry("tab1+leaf1", "session-0001", other, "term_abc")
    _canned_orca(patch_orca, [other])
    patch_git.default = "## main\0"
    return SimpleNamespace(
        sweep_root=sweep_root,
        root=sweep_root.root,
        orca=patch_orca,
        git=patch_git,
        sweeps=sweep_root.root / ".dev" / "sweeps",
        paths=(
            sweep_root.root,
            sweep_root.home,
            sweep_root.state,
            *xdg,
            sweep_root.base / "worktrees",
        ),
    )


def _invoke(env):
    return CliRunner().invoke(
        sweep_group, ["run", "--run", RUN, "--root", str(env.root)]
    )


def _prepare(env, existing: str) -> None:
    """Make ``.dev`` or ``.dev/sweeps`` exist before the sweep, as the case asks."""
    if existing in ("dev", "sweeps"):
        env.sweep_root.package("pkg-root", ledger="ledger\n")
    if existing == "sweeps":
        env.sweeps.mkdir(parents=True)


EXISTING = pytest.mark.parametrize("existing", ["nothing", "dev", "sweeps"])


@EXISTING
def test_sweep_run_adds_exactly_one_report_and_changes_nothing_else(
    sweep_env, existing
):
    _prepare(sweep_env, existing)
    before = snapshot(sweep_env.paths)

    result = _invoke(sweep_env)

    after = snapshot(sweep_env.paths)
    assert result.exit_code == 0, result.output
    report = Path(json.loads(result.stdout)["report_path"])
    assert report.parent == sweep_env.sweeps
    assert re.fullmatch(r"\d{8}-\d{6}-sweep\.md", report.name)
    new_folders = {
        "nothing": [sweep_env.root / ".dev", sweep_env.sweeps],
        "dev": [sweep_env.sweeps],
        "sweeps": [],
    }[existing]
    # Exactly the report, plus the folders that were new; nothing modified or removed.
    assert_only_added(before, after, {report, *new_folders})
    kind, size, _, _ = after[str(report)]
    assert (kind, size > 0) == ("file", True)  # a real, non-empty file


@EXISTING
def test_no_temp_file_and_no_second_name_remain_after_exit_0(sweep_env, existing):
    _prepare(sweep_env, existing)

    result = _invoke(sweep_env)

    assert result.exit_code == 0, result.output
    report = Path(json.loads(result.stdout)["report_path"])
    assert sorted(p.name for p in sweep_env.sweeps.iterdir()) == [report.name]
    # The temp file was a second hard-linked name; one name left means link count 1.
    assert os.stat(report).st_nlink == 1
    everywhere = snapshot(sweep_env.paths)
    assert [p for p in everywhere if p.endswith(".tmp")] == []


def test_the_snapshot_check_catches_a_stray_write_made_during_the_run(
    sweep_env, monkeypatch
):
    real_publish = commands._publish

    def publish_and_stray_write(text, output_dir, now):
        (sweep_env.sweep_root.home / "stray.txt").write_text("not allowed\n")
        return real_publish(text, output_dir, now)

    monkeypatch.setattr(commands, "_publish", publish_and_stray_write)
    before = snapshot(sweep_env.paths)

    result = _invoke(sweep_env)

    assert result.exit_code == 0, result.output
    report = Path(json.loads(result.stdout)["report_path"])
    with pytest.raises(AssertionError, match="stray.txt"):
        assert_only_added(
            before,
            snapshot(sweep_env.paths),
            {report, sweep_env.root / ".dev", sweep_env.sweeps},
        )


# --- NFR-013: no live Orca, ccsession or Claude launch -----------------------------------


def test_the_subprocess_guard_is_live_in_this_module():
    for start in (subprocess.run, subprocess.Popen, os.system):
        with pytest.raises(AssertionError, match="must not start a process"):
            start(["true"])


def test_a_sweep_starts_no_process_and_records_only_allowlisted_argv(sweep_env):
    result = _invoke(sweep_env)

    assert result.exit_code == 0, result.output  # a process start would exit 1 here
    orca_calls = [call["args"] for call in sweep_env.orca.calls]
    assert orca_calls, "the sweep made no Orca read at all"
    assert set(orca_calls) == {WORKER_LIST, TASKS_READY, TASKS_ALL, WORKTREE_PS}
    git_calls = sweep_env.git.calls
    assert [c["cwd"] for c in git_calls] == [
        sweep_env.root.resolve(),
        sweep_env.sweep_root.base.joinpath("worktrees", "wt-a").resolve(),
    ]
    assert all(c["args"] == STATUS_ARGS for c in git_calls)
    assert all(c["argv"][:3] == ["git", "--no-optional-locks", "-C"] for c in git_calls)
    for (
        args
    ) in orca_calls:  # each one is an allowlisted template (no ccsession, claude)
        probes.check_orca_argv(args)
        assert args[0] in {"orchestration", "worktree"}


# --- The real-git test (FR-025) ----------------------------------------------------------


def _git_env(home: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(_FIXED_IDENTITY)
    env["HOME"] = str(home)
    return env


@pytest.mark.integration
@pytest.mark.skipif(GIT is None, reason="git is not installed")
def test_real_git_lock_free_status_and_gitignore(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    env = _git_env(tmp_path / "home")

    def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(
            [GIT, "-C", str(repo), *args],
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
            check=check,
        )

    git("init", "-q", "-b", "main")
    shutil.copyfile(REPO_ROOT / ".gitignore", repo / ".gitignore")
    tracked = repo / "tracked.txt"
    tracked.write_text("one\n")
    git("add", ".gitignore", "tracked.txt")
    git("commit", "-q", "-m", "seed")

    # (2) a report under .dev/sweeps/ is ignored.
    assert git("check-ignore", ".dev/sweeps/x.md", check=False).returncode == 0
    # (3) task packages under .dev/tasks/ are not.
    assert git("check-ignore", ".dev/tasks/to-do/x.md", check=False).returncode == 1

    # (4) writing a file under .dev/sweeps/ leaves the status output unchanged.
    before = git("status", "--porcelain").stdout
    (repo / ".dev" / "sweeps").mkdir(parents=True)
    (repo / ".dev" / "sweeps" / "x.md").write_text("report\n")
    assert git("status", "--porcelain").stdout == before == ""

    # (1) control: make the index entry stat-dirty (same bytes, new mtime). The sweep's
    # lock-free call must leave the index file alone; a plain status rewrites it.
    index = repo / ".git" / "index"
    st = tracked.stat()
    os.utime(tracked, ns=(st.st_atime_ns, st.st_mtime_ns + 5_000_000_000))
    index_before = index.read_bytes()

    lock_free = subprocess.run(
        [GIT, "--no-optional-locks", "-C", str(repo), *STATUS_ARGS],
        env={**env, "GIT_OPTIONAL_LOCKS": "0"},
        capture_output=True,
        timeout=30,
        check=True,
    )
    assert lock_free.returncode == 0
    assert index.read_bytes() == index_before, "lock-free status rewrote the index"

    git("status", "--porcelain")  # the plain call
    if index.read_bytes() == index_before:
        warnings.warn(
            "control inconclusive: a plain git status did not rewrite the index here",
            stacklevel=1,
        )
