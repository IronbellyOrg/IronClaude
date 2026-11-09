"""FR-102: ``install_l2`` and ``l2_status`` (installer, ownership oracle, forgery, publication).

Real git under a temporary HOME (GIT_CONFIG_GLOBAL and GIT_CONFIG_SYSTEM at
/dev/null) holding copies of the packaged hook and the selector, a bare remote
and a clone. Every call runs under umask 077 with ``os.environ`` replaced by the
fixture environment, as ``tests/hooks/test_launch_level_pre_push.py`` does.
"""

import errno
import importlib.util
import os
import shutil
import stat
import subprocess
import sys
import threading
from pathlib import Path
from unittest import mock

import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / "src/superclaude/hooks/scripts/launch-level-pre-push.sh"
SELECTOR = REPO / "src/superclaude/hooks/scripts/launch-job-identity.sh"
ORCA = REPO / "src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py"


def _load():
    spec = importlib.util.spec_from_file_location("orca_worktree_l2_install", ORCA)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses need it
    spec.loader.exec_module(module)
    return module


orca = _load()
DATA = orca.L2_DATA_NAME
FOREIGN = b"#!/bin/sh\necho foreign\nexit 0\n"
REAL_LINK, REAL_WRITE = os.link, os.write


class L2:
    """Temporary HOME with the packaged hook and selector, a bare remote and a clone."""

    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.home = tmp / "home"
        self.home.mkdir(mode=0o700)
        src = self.home / ".claude/hooks"
        src.mkdir(parents=True)
        self.selector = src / "launch-job-identity.sh"
        self.packaged = src / "launch-level-pre-push.sh"
        for origin, copy in ((SELECTOR, self.selector), (HOOK, self.packaged)):
            shutil.copyfile(origin, copy)
            copy.chmod(0o755)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(
            HOME=str(self.home),
            GIT_CONFIG_GLOBAL="/dev/null",
            GIT_CONFIG_SYSTEM="/dev/null",
            GIT_CONFIG_NOSYSTEM="1",
            GIT_TERMINAL_PROMPT="0",
            GIT_CEILING_DIRECTORIES=str(tmp),
            GIT_AUTHOR_NAME="L2 fixture",
            GIT_AUTHOR_EMAIL="fixture@example.invalid",
            GIT_COMMITTER_NAME="L2 fixture",
            GIT_COMMITTER_EMAIL="fixture@example.invalid",
            UV_PYTHON=sys.executable,
            UV_PYTHON_DOWNLOADS="never",
        )
        self.work = tmp / "clone"
        self.git("init", "-q", "--bare", tmp / "remote.git", cwd=tmp)
        self.git("clone", "-q", tmp / "remote.git", self.work, cwd=tmp)
        self.hooks = self.work / ".git/hooks"
        self.entry = self.hooks / "pre-push"
        self.data = self.hooks / DATA

    def git(self, *args, cwd=None, check=True):
        return subprocess.run(
            ["git", *map(str, args)],
            env=self.env,
            cwd=cwd or self.work,
            capture_output=True,
            text=True,
            timeout=30,
            check=check,
        )

    def call(self, fn, wt=None, **extra):
        with mock.patch.dict(os.environ, {**self.env, **extra}, clear=True):
            return fn(str(wt or self.work))

    def install(self, wt=None, **extra):
        return self.call(orca.install_l2, wt, **extra)

    def status(self, wt=None, **extra):
        return self.call(orca.l2_status, wt, **extra)

    def expected_data(self) -> bytes:
        return self.call(lambda _: orca.l2_data_expected())

    def write_data(self, data=None, mode=0o644):
        self.data.write_bytes(self.expected_data() if data is None else data)
        self.data.chmod(mode)

    def remedy(self) -> str:
        return f"`rm {self.hooks}/pre-push {self.hooks}/{DATA}`"


@pytest.fixture
def l2(tmp_path):
    old = os.umask(0o077)
    try:
        yield L2(tmp_path)
    finally:
        os.umask(old)


def snap(d: Path):
    """The directory's own mtime plus (inode, mtime, mode, size) of each entry."""
    if not os.path.lexists(d):
        return None
    out = {".": d.lstat().st_mtime_ns}
    for name in os.listdir(d):
        st = (d / name).lstat()
        out[name] = (st.st_ino, st.st_mtime_ns, st.st_mode, st.st_size)
    return out


def entry_state(p: Path):
    st = p.lstat()
    if stat.S_ISLNK(st.st_mode):
        body = os.readlink(p)
    elif stat.S_ISREG(st.st_mode):
        body = p.read_bytes()
    elif stat.S_ISDIR(st.st_mode):
        body = sorted(os.listdir(p))
    else:
        body = None
    return st.st_ino, st.st_mode, st.st_mtime_ns, body


def dot_names(d: Path):
    """Private staging subdirectories and temporary publication names."""
    return [n for n in os.listdir(d) if n.startswith(".")]


def write(p: Path, data: bytes, mode: int):
    p.write_bytes(data)
    p.chmod(mode)


# --- 1, 2, 16: fresh install, repeat install, version line ---------------------


@pytest.mark.parametrize(
    "drop_hooks_dir", [False, True], ids=["hooks-dir", "no-hooks-dir"]
)
def test_fresh_install_under_umask_077(l2, drop_hooks_dir):
    if drop_hooks_dir:
        shutil.rmtree(l2.hooks)
    assert l2.install() == ("installed", "")
    assert stat.S_IMODE(l2.entry.lstat().st_mode) == 0o755
    assert stat.S_IMODE(l2.data.lstat().st_mode) == 0o644
    assert l2.entry.read_bytes() == HOOK.read_bytes()
    assert l2.data.read_bytes() == l2.expected_data()
    assert (
        l2.data.read_bytes()
        == f"{l2.home}\n{os.path.dirname(shutil.which('uv'))}\n".encode()
    )
    assert l2.status() == ("owned", "")
    assert dot_names(l2.hooks) == []


def test_repeat_install_keeps_metadata(l2):
    assert l2.install() == ("installed", "")
    before = snap(l2.hooks)
    assert l2.install() == ("owned", "")
    assert snap(l2.hooks) == before  # hook and data inode and mtime unchanged
    assert l2.status() == ("owned", "")


def test_version_line_is_line_2_of_packaged_hook():
    assert HOOK.read_text().splitlines()[1] == orca.L2_VERSION_LINE


# --- 3-6 and the forgery subgroup: none reads owned, nothing changes ----------


def _symlink_to_packaged(e, l2):
    e.symlink_to(l2.packaged)


def _version_0(e, l2):
    body = HOOK.read_bytes().replace(
        orca.L2_VERSION_LINE.encode(), b"# launch-level-pre-push-version: 0"
    )
    write(e, body, 0o755)


FORGERIES = {
    "foreign": (lambda e, l2: write(e, FOREIGN, 0o755), "foreign"),
    "marker-only": (
        lambda e, l2: write(e, b"".join(HOOK.read_bytes().splitlines(True)[:2]), 0o755),
        "stale",
    ),
    "edited-body": (
        lambda e, l2: write(e, HOOK.read_bytes() + b"# edited\n", 0o755),
        "stale",
    ),
    "old-version": (_version_0, "stale"),
    "symlink-to-packaged": (_symlink_to_packaged, "symlink"),
    "dangling-symlink": (
        lambda e, l2: e.symlink_to(e.parent / "missing"),
        "symlink",
    ),
    "fifo": (lambda e, l2: os.mkfifo(e, 0o755), "conflict"),
    "directory": (lambda e, l2: e.mkdir(), "conflict"),
    "not-executable": (
        lambda e, l2: write(e, HOOK.read_bytes(), 0o644),
        "not executable",
    ),
    "group-writable": (
        lambda e, l2: write(e, HOOK.read_bytes(), 0o775),
        "group or other writable",
    ),
    "world-writable": (
        lambda e, l2: write(e, HOOK.read_bytes(), 0o777),
        "group or other writable",
    ),
}


@pytest.mark.parametrize("make,why", FORGERIES.values(), ids=list(FORGERIES))
def test_forgery_never_owned_and_never_touched(l2, make, why):
    l2.write_data()  # a valid data file, so the hook entry alone decides
    make(l2.entry, l2)
    entry_before, hooks_before = entry_state(l2.entry), snap(l2.hooks)
    state, reason = l2.status()
    assert state == "conflict"
    assert why == "conflict" or reason.startswith(why + ":")
    assert l2.remedy() in reason and "the claim never deletes them" in reason
    assert l2.install() == (state, reason)
    assert entry_state(l2.entry) == entry_before
    assert snap(l2.hooks) == hooks_before
    assert l2.status() == (state, reason)


SECOND_UID = 65534  # nobody


@pytest.mark.skipif(
    not hasattr(os, "geteuid") or os.geteuid() != 0,
    reason="U-7 second uid: chown of the hook or data file to another uid needs root",
)
@pytest.mark.parametrize(
    "target,why", [("pre-push", "wrong owner"), (DATA, "data-file-differs")]
)
def test_wrong_uid_never_owned(l2, target, why):
    assert l2.install() == ("installed", "")
    os.chown(l2.hooks / target, SECOND_UID, -1)
    before = snap(l2.hooks)
    state, reason = l2.status()
    assert state == "conflict" and reason.startswith(why + ":")
    assert l2.install() == (state, reason)
    assert snap(l2.hooks) == before


def test_wrong_uid_of_hook_entry_without_root(l2, monkeypatch):
    # Without root the entry check alone is reached directly; the hooks-directory
    # check would refuse first in l2_status (test_unsafe_hooks_dir_is_unsupported).
    assert l2.install() == ("installed", "")
    expected, packaged = l2.expected_data(), HOOK.read_bytes()
    uid = os.geteuid()
    monkeypatch.setattr(os, "geteuid", lambda: uid + 1)
    state, reason = orca._l2_entry_verdict(l2.hooks, expected, packaged)
    assert state == "conflict" and reason.startswith("wrong owner:")


@pytest.mark.parametrize("variant", ["group-writable", "other-content"])
def test_data_file_forgery_after_owned_install(l2, variant):
    assert l2.install() == ("installed", "")
    if variant == "group-writable":
        l2.data.chmod(0o664)
    else:
        l2.data.write_bytes(b"/elsewhere\n/usr/local/bin\n")
    before = snap(l2.hooks)
    state, reason = l2.status()
    assert state == "conflict" and reason.startswith("data-file-differs:")
    assert l2.install() == (state, reason)
    assert snap(l2.hooks) == before


def test_existing_data_file_with_other_content_conflicts(l2):
    write(l2.data, b"/elsewhere\n/usr/local/bin\n", 0o644)
    before = snap(l2.hooks)
    state, reason = l2.install()
    assert state == "conflict" and reason.startswith("data-file-differs:")
    assert l2.remedy() in reason
    # The directory mtime moves (a temporary name came and went); no entry changed.
    del before["."]
    after = snap(l2.hooks)
    del after["."]
    assert after == before
    assert not os.path.lexists(l2.entry)


# --- 7-11: preconditions, nothing written ------------------------------------


@pytest.mark.parametrize("scope", ["local", "worktree"])
def test_hookspath_is_unsupported(l2, scope):
    wt = l2.work
    if scope == "local":
        l2.git("config", "core.hooksPath", l2.tmp / "elsewhere")
    else:
        l2.git("commit", "-q", "--allow-empty", "-m", "a")
        l2.git("config", "core.repositoryformatversion", "1")
        l2.git("config", "extensions.worktreeConfig", "true")
        wt = l2.tmp / "linked"
        l2.git("worktree", "add", "-q", "-b", "side", wt)
        l2.git("config", "--worktree", "core.hooksPath", l2.tmp / "elsewhere", cwd=wt)
        # Only the linked worktree's config.worktree sets it.
        assert l2.git("config", "--get", "core.hooksPath", check=False).returncode == 1
    before = snap(l2.hooks)
    assert l2.install(wt) == ("unsupported", orca.L2_WHY_HOOKSPATH)
    assert l2.status(wt) == ("unsupported", orca.L2_WHY_HOOKSPATH)
    assert snap(l2.hooks) == before


def test_config_read_error_fails_install(l2):
    with (l2.work / ".git/config").open("a") as f:
        f.write("[broken\n")
    before = snap(l2.hooks)
    assert l2.install() == ("unsupported", orca.L2_WHY_CONFIG)
    assert l2.status() == ("absent", orca.L2_WHY_CONFIG)
    assert snap(l2.hooks) == before


@pytest.mark.parametrize("variant", ["group-writable", "foreign-owned"])
def test_unsafe_hooks_dir_is_unsupported(l2, monkeypatch, variant):
    if variant == "group-writable":
        l2.hooks.chmod(0o775)
    else:  # a foreign owner cannot be made without root; geteuid is shifted instead
        uid = os.geteuid()
        monkeypatch.setattr(os, "geteuid", lambda: uid + 1)
    before = snap(l2.hooks)
    assert l2.install() == ("unsupported", orca.L2_WHY_HOOKS_DIR)
    # FR-041 names `absent` here; the code answers `unsupported`. Either way, not owned.
    assert l2.status()[1] == orca.L2_WHY_HOOKS_DIR
    assert snap(l2.hooks) == before


@pytest.mark.parametrize("variant", ["not-a-repo", "rev-parse-fails"])
def test_git_failure(l2, monkeypatch, variant):
    wt = l2.work
    if variant == "not-a-repo":
        wt = l2.tmp / "plain"
        wt.mkdir()
    else:
        real_run = orca.run

        def run(argv, *a, **kw):
            if "rev-parse" in argv:
                return orca.Result(rc=128, err="fatal: injected")
            return real_run(argv, *a, **kw)

        monkeypatch.setattr(orca, "run", run)
    before = snap(l2.hooks)
    assert l2.status(wt) == ("absent", orca.L2_WHY_GIT)
    assert l2.install(wt) == ("unsupported", orca.L2_WHY_GIT)
    assert snap(l2.hooks) == before


@pytest.mark.parametrize("variant", ["missing", "no-version-line", "symlink"])
def test_packaged_hook_not_installed(l2, variant):
    l2.packaged.unlink()
    if variant == "no-version-line":
        write(l2.packaged, b"#!/bin/sh\nexit 0\n", 0o755)
    elif variant == "symlink":
        l2.packaged.symlink_to(HOOK)
    before = snap(l2.hooks)
    assert l2.install() == ("unavailable", orca.L2_WHY_NOT_INSTALLED)
    assert snap(l2.hooks) == before
    assert l2.status() == ("absent", orca.L2_WHY_NO_HOOK)


# --- 12: self-test failures leave no hook and no private subdirectory --------


def _no_uv_path(l2):
    path = os.pathsep.join(
        d
        for d in l2.env["PATH"].split(os.pathsep)
        if d and not (Path(d) / "uv").exists()
    )
    assert shutil.which("git", path=path) and not shutil.which("uv", path=path)
    return {"PATH": path}


def _broken_uv(l2):
    # shortcut: "a uv directory without uv" cannot be produced, because the data
    # file names the directory where which() found uv; a uv there that exits 1
    # is the nearest case the self-test must catch.
    fake = l2.tmp / "fake-uv"
    fake.mkdir()
    write(fake / "uv", b"#!/bin/sh\nexit 1\n", 0o755)
    return {"PATH": f"{fake}{os.pathsep}{l2.env['PATH']}"}


def _failing_selector(l2):
    write(l2.selector, b"#!/bin/sh\nexit 1\n", 0o755)
    return {}


def _never_refusing_hook(l2):
    write(l2.packaged, f"#!/bin/sh\n{orca.L2_VERSION_LINE}\nexit 0\n".encode(), 0o755)
    return {}


SELFTEST = {
    "uv-not-on-path": (_no_uv_path, orca.L2_WHY_NO_UV),
    "broken-uv": (_broken_uv, "the hook self-test failed at step "),
    "selector-fails": (
        _failing_selector,
        "the hook self-test failed at step selector-env",
    ),
    "no-refusal": (
        _never_refusing_hook,
        "the hook self-test failed at step no-data-refusal",
    ),
}


@pytest.mark.parametrize("setup,why", SELFTEST.values(), ids=list(SELFTEST))
def test_selftest_failure_links_nothing(l2, setup, why):
    extra = setup(l2)
    names = set(os.listdir(l2.hooks))
    state, reason = l2.install(**extra)
    assert state == "unavailable" and reason.startswith(why), reason
    assert not os.path.lexists(l2.entry)
    assert dot_names(l2.hooks) == []
    assert set(os.listdir(l2.hooks)) - names <= {DATA}  # the inert data file may stay
    assert l2.status(**extra)[0] == "absent"


# --- 13, publication: competing installers, races, injected failures ---------


def test_concurrent_installs_converge_on_one_pair(l2):
    barrier, results = threading.Barrier(2), []

    def claim():
        barrier.wait()
        results.append(orca.install_l2(str(l2.work)))

    with mock.patch.dict(os.environ, l2.env, clear=True):
        threads = [threading.Thread(target=claim) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(120)
    # Exactly one link wins; the other reads the winner's hook as owned.
    assert sorted(results) == [("installed", ""), ("owned", "")]
    assert l2.status() == ("owned", "")
    assert sorted(n for n in os.listdir(l2.hooks) if not n.endswith(".sample")) == [
        "pre-push",
        DATA,
    ]


def test_foreign_entry_created_before_link_survives(l2, monkeypatch):
    def racing_link(src, dst, *a, **kw):
        if "src_dir_fd" not in kw:  # the final S5 link, not publish_no_replace
            write(Path(dst), FOREIGN, 0o755)
            raise FileExistsError(errno.EEXIST, "File exists", str(dst))
        return REAL_LINK(src, dst, *a, **kw)

    monkeypatch.setattr(os, "link", racing_link)
    state, reason = l2.install()
    assert state == "conflict" and reason.startswith("foreign:")
    assert l2.entry.read_bytes() == FOREIGN
    assert dot_names(l2.hooks) == []


def _short_write_then_fail(monkeypatch):
    calls = []

    def write_(fd, data):
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return REAL_WRITE(fd, data)
        calls.append(fd)
        if len(calls) == 1:
            return REAL_WRITE(fd, bytes(data[:1]))  # a partial write
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(os, "write", write_)


def _fsync_fails(monkeypatch):
    def fsync(fd):
        raise OSError(errno.EIO, "Input/output error")

    monkeypatch.setattr(os, "fsync", fsync)


def _link_fails(final_only):
    def patch(monkeypatch):
        def link(src, dst, *a, **kw):
            if final_only and "src_dir_fd" in kw:
                return REAL_LINK(src, dst, *a, **kw)
            raise OSError(errno.EPERM, "Operation not permitted")

        monkeypatch.setattr(os, "link", link)

    return patch


FAULTS = {
    "partial-write": _short_write_then_fail,
    "fsync": _fsync_fails,
    "link-every": _link_fails(False),
    "link-final": _link_fails(True),
}


@pytest.mark.parametrize("inject", FAULTS.values(), ids=list(FAULTS))
def test_injected_write_failure_never_owned(l2, monkeypatch, inject):
    inject(monkeypatch)
    state, reason = l2.install()
    monkeypatch.undo()
    assert state == "unavailable" and reason.startswith("write failed:"), reason
    assert not os.path.lexists(l2.entry)
    assert dot_names(l2.hooks) == []
    assert l2.status()[0] == "absent"


# --- 14: the claim environment does not redirect git --------------------------

INJECTED_ENV = {
    "parameters": {"GIT_CONFIG_PARAMETERS": "'core.hookspath'='/tmp/l2-elsewhere'"},
    "count": {
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": "core.hooksPath",
        "GIT_CONFIG_VALUE_0": "/tmp/l2-elsewhere",
    },
    "git-dir": {"GIT_DIR": "/nonexistent/l2.git", "GIT_WORK_TREE": "/nonexistent"},
}


@pytest.mark.parametrize("extra", INJECTED_ENV.values(), ids=list(INJECTED_ENV))
def test_git_redirecting_environment_is_ignored(l2, extra):
    assert l2.status(**extra) == ("absent", orca.L2_WHY_NO_HOOK)
    assert l2.install(**extra) == ("installed", "")
    assert l2.status(**extra) == ("owned", "")
    assert l2.install(**extra) == ("owned", "")


# --- 15: l2_status never writes -----------------------------------------------


def _owned(l2):
    assert l2.install() == ("installed", "")


STATUS_STATES = {
    "absent": (lambda l2: None, "absent"),
    "no-hooks-dir": (lambda l2: shutil.rmtree(l2.hooks), "absent"),
    "owned": (_owned, "owned"),
    "conflict": (lambda l2: write(l2.entry, FOREIGN, 0o755), "conflict"),
}


@pytest.mark.parametrize("setup,state", STATUS_STATES.values(), ids=list(STATUS_STATES))
def test_l2_status_never_writes(l2, setup, state):
    setup(l2)
    git_dir = l2.work / ".git"
    before = snap(l2.hooks), snap(git_dir)
    for _ in range(2):
        assert l2.status()[0] == state
    assert (snap(l2.hooks), snap(git_dir)) == before


# Reuse the launch scene and its isolated HOME, git and Orca fixtures.
from tests.skills import test_issue_orca_worktree as launch_tests  # noqa: E402

home = launch_tests.home
fake_orca = launch_tests.fake_orca
git_repo = launch_tests.git_repo
issue_dir = launch_tests.issue_dir


@pytest.mark.parametrize("refuse,owned", [(False, False), (True, False), (True, True)])
def test_ir7_l2_switch(
    refuse, owned, fake_orca, git_repo, issue_dir, monkeypatch, capsys
):
    import argparse
    import json

    wt = launch_tests.launch_scene(fake_orca, git_repo, issue_dir)
    module = _load()
    for key, value in fake_orca.env(SC_ORCA_SHIM_INTERVAL="0").items():
        monkeypatch.setenv(key, value)
    monkeypatch.chdir(git_repo)
    monkeypatch.setattr(module, "IR7_REFUSE", refuse)
    if owned:
        # The launch fixture's uv is a no-op; the installer needs the real selector.
        (fake_orca.tools / "uv").unlink()
        monkeypatch.setenv("UV_PYTHON", sys.executable)
        monkeypatch.setenv("UV_PYTHON_DOWNLOADS", "never")
        for origin in (HOOK, SELECTOR):
            target = fake_orca.home / ".claude/hooks" / origin.name
            shutil.copyfile(origin, target)
            target.chmod(0o755)
        assert module.install_l2(str(wt))[0] == "installed"
    assert module.l2_status(wt)[0] == ("owned" if owned else "absent")
    args = argparse.Namespace(
        source=str(issue_dir), number=launch_tests.NUMBER, level="full", submit=False
    )
    assert module.cmd_launch(args) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["warning"] == (None if owned else "W-L2-ABSENT")
    if refuse and not owned:
        assert data["status"] == "failed"
        assert data["enforcement_hook"] == "installed"
        assert module.IR7_REFUSAL in data["detail"]
        assert not launch_tests.launch_calls(fake_orca)
        assert not launch_tests.pending_dir(fake_orca).exists()
        assert "launch" not in json.loads((issue_dir / "worktree.json").read_text())
    else:
        assert data["status"] == "launched"
        assert len(launch_tests.launch_calls(fake_orca)) == 1
        if not owned:
            assert module.REMEDY["W-L2-ABSENT"] in data["detail"]
        else:
            assert "W-L2-ABSENT" not in data["detail"]


def test_ir7_shipped_switch_is_off():
    assert _load().IR7_REFUSE is False


@pytest.mark.parametrize("operation", ["install_l2", "l2_status"])
def test_fifo_data_conflict_returns_without_waiting(l2, operation):
    import json

    if operation == "l2_status":
        assert l2.install() == ("installed", "")
        l2.data.unlink()
    os.mkfifo(l2.data, 0o600)
    before = snap(l2.hooks)
    # Bound the process, not a thread: a blocking open must fail instead of
    # leaving a hung test runner or requiring a writer to unblock the FIFO.
    code = """
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("fifo_orca", sys.argv[1])
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
print(json.dumps(getattr(module, sys.argv[2])(sys.argv[3])))
"""
    proc = subprocess.run(
        [sys.executable, "-c", code, str(ORCA), operation, str(l2.work)],
        env=l2.env,
        capture_output=True,
        text=True,
        timeout=5,
        check=True,
    )
    state, reason = json.loads(proc.stdout)
    assert state == "conflict"
    assert "data-file-differs" in reason
    after = snap(l2.hooks)
    if operation == "install_l2":
        # Publishing a temporary file changes the directory mtime, not its entries.
        before.pop(".")
        after.pop(".")
    assert after == before
    assert stat.S_ISFIFO(l2.data.lstat().st_mode)
