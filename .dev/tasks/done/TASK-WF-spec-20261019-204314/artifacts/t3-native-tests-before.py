"""Isolated native acquisition tests; no upstream code is executed."""

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from superclaude.cli import install_codebase_memory as native


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    home = tmp_path / "test home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(native.platform, "system", lambda: "Linux")
    monkeypatch.setattr(native.platform, "machine", lambda: "x86_64")
    # Any accidental subprocess is a test failure, except in the local fixture.
    monkeypatch.setattr(native, "_run_bounded", lambda *a, **k: pytest.fail(str(a)))
    return home


def binary(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("benign fixture, never executed\n")
    path.chmod(0o700)
    return path


def probe_ok(monkeypatch):
    calls = []

    def run(argv, timeout, **kwargs):
        calls.append((argv, timeout, kwargs))
        return subprocess.CompletedProcess(argv, 0, "codebase-memory-mcp 0.12.1\n", "")

    monkeypatch.setattr(native, "_run_bounded", run)
    return calls


@pytest.mark.parametrize("system", ["Linux"])
@pytest.mark.parametrize("arch", ["x86_64", "amd64", "arm64", "aarch64"])
def test_supported_platform_reuses_canonical(system, arch, isolated_home, monkeypatch):
    monkeypatch.setattr(native.platform, "system", lambda: system)
    monkeypatch.setattr(native.platform, "machine", lambda: arch)
    exe = binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    calls = probe_ok(monkeypatch)
    result = native.acquire_codebase_memory()
    assert result.success and not result.acquired
    assert result.executable == exe and result.version == "codebase-memory-mcp 0.12.1"
    assert calls == [
        ([str(exe), "--version"], native.VERSION_TIMEOUT, {"capture_output": True})
    ]


@pytest.mark.parametrize(
    "system,arch",
    [
        ("Windows", "AMD64"),
        ("Darwin", "arm64"),
        ("FreeBSD", "x86_64"),
        ("Linux", "riscv64"),
    ],
)
def test_unsupported_before_discovery(system, arch, monkeypatch):
    monkeypatch.setattr(native.platform, "system", lambda: system)
    monkeypatch.setattr(native.platform, "machine", lambda: arch)
    monkeypatch.setattr(native, "discover_executable", lambda: pytest.fail("discovery"))
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "platform"
    assert "Linux" in result.message


@pytest.mark.parametrize("scope", ["project", "local", "bad"])
def test_reject_scope_before_discovery(scope):
    result = native.acquire_codebase_memory(scope=scope)
    assert not result.success and result.stage == "scope"


def test_canonical_precedes_external(isolated_home, monkeypatch):
    canonical = binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    external = binary(isolated_home / "package manager/bin" / native.BINARY_NAME)
    monkeypatch.setenv("PATH", str(external.parent))
    calls = probe_ok(monkeypatch)
    found = native.discover_executable()
    assert found.state == "canonical" and found.executable == canonical
    assert len(calls) == 1


def test_external_reuse_needs_no_curl_or_bash(isolated_home, monkeypatch):
    external = binary(isolated_home / "package manager/bin" / native.BINARY_NAME)
    monkeypatch.setenv("PATH", str(external.parent))
    probe_ok(monkeypatch)
    monkeypatch.setattr(
        native.shutil, "which", lambda _: pytest.fail("prerequisite lookup")
    )
    found = native.discover_executable()
    assert found.state == "external" and found.executable == external
    result = native.acquire_codebase_memory()
    assert result.success and result.executable == external and not result.acquired


def test_unusable_canonical_can_reuse_external(isolated_home, monkeypatch):
    canonical = binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    canonical.chmod(0o600)
    external = binary(isolated_home / "other" / native.BINARY_NAME)
    monkeypatch.setenv("PATH", str(external.parent))
    probe_ok(monkeypatch)
    assert native.discover_executable().executable == external


@pytest.mark.parametrize(
    "kind", ["binary", "parent", "dangling", "directory", "hardlink"]
)
def test_ambiguous_canonical_fails_closed(kind, isolated_home):
    canonical = isolated_home / ".local/bin" / native.BINARY_NAME
    canonical.parent.mkdir(parents=True)
    other = binary(isolated_home / "external" / native.BINARY_NAME)
    if kind == "parent":
        canonical.parent.rmdir()
        canonical.parent.symlink_to(other.parent, target_is_directory=True)
    elif kind == "directory":
        canonical.mkdir()
    elif kind == "hardlink":
        os.link(other, canonical)
    else:
        canonical.symlink_to(other if kind == "binary" else isolated_home / "absent")
    found = native.discover_executable()
    assert found.state == "ambiguous"
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "discovery"


def test_external_symlink_fails_closed(isolated_home, monkeypatch):
    external = isolated_home / "external" / native.BINARY_NAME
    external.parent.mkdir()
    external.symlink_to(isolated_home / "missing")
    monkeypatch.setenv("PATH", str(external.parent))
    assert native.discover_executable().state == "ambiguous"


def test_missing_external_under_symlink_directory_is_not_a_collision(
    isolated_home, monkeypatch
):
    actual = isolated_home / "actual bin"
    actual.mkdir()
    link = isolated_home / "linked bin"
    link.symlink_to(actual, target_is_directory=True)
    monkeypatch.setenv("PATH", str(link))
    assert native.discover_executable().state == "missing"


def test_unknown_filesystem_state_fails_closed(isolated_home, monkeypatch):
    canonical = binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    original = Path.lstat

    def lstat(path, *args, **kwargs):
        if path == canonical:
            raise PermissionError("unknown file state")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", lstat)
    assert native.discover_executable().state == "ambiguous"


def test_foreign_canonical_owner_fails_closed(isolated_home, monkeypatch):
    binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    monkeypatch.setattr(native.os, "getuid", lambda: 99999999)
    assert native.discover_executable().state == "ambiguous"


def test_nonrunnable_external_not_replaced(isolated_home, monkeypatch):
    external = binary(isolated_home / "external" / native.BINARY_NAME)
    monkeypatch.setenv("PATH", str(external.parent))
    monkeypatch.setattr(
        native,
        "_run_bounded",
        lambda *a, **k: subprocess.CompletedProcess(a[0], 2, "", "broken ABI"),
    )
    found = native.discover_executable()
    assert found.state == "non_runnable" and "broken ABI" in found.message
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "discovery"


@pytest.mark.parametrize("missing", ["curl", "bash"])
def test_acquisition_prerequisites_only(missing, monkeypatch):
    monkeypatch.setattr(
        native.shutil,
        "which",
        lambda name: None if name == missing else f"/fixture/{name}",
    )
    result = native.acquire_codebase_memory()
    assert (
        not result.success
        and result.stage == "prerequisites"
        and missing in result.message
    )


def setup_acquisition(monkeypatch, home, failure=None):
    calls, scripts = [], []
    canonical = home / ".local/bin" / native.BINARY_NAME
    monkeypatch.setattr(native.shutil, "which", lambda name: f"/fixture/{name}")

    def run(argv, timeout, **kwargs):
        calls.append((argv, timeout, kwargs))
        stage = (
            "download"
            if argv[0] == "/fixture/curl"
            else "install"
            if argv[0] == "/fixture/bash"
            else "verification"
        )
        if stage == "download":
            script = Path(argv[argv.index("--output") + 1])
            scripts.append(script)
            assert script.parent.stat().st_mode & 0o777 == 0o700
            script.write_text(
                "" if failure == "empty" else "complete bootstrap fixture\n"
            )
        if failure == stage + "_oserror":
            raise PermissionError("denied fixture")
        if failure == stage + "_timeout":
            raise subprocess.TimeoutExpired(argv, timeout)
        if failure == stage + "_nonzero":
            return subprocess.CompletedProcess(argv, 7, "", "fixture diagnostic")
        if stage == "install" and failure != "missing_postcheck":
            binary(canonical)
        if stage == "install" and failure == "postcheck_symlink":
            canonical.unlink()
            canonical.symlink_to(home / "absent")
        return subprocess.CompletedProcess(
            argv,
            0,
            "" if failure == "empty_version" else "codebase-memory-mcp 0.12.1\n",
            "",
        )

    monkeypatch.setattr(native, "_run_bounded", run)
    return calls, scripts, canonical


def test_full_acquisition_absolute_postcheck_cleanup(
    isolated_home, monkeypatch, capsys
):
    calls, scripts, canonical = setup_acquisition(monkeypatch, isolated_home)
    result = native.acquire_codebase_memory()
    assert result.success and result.acquired and result.executable == canonical
    assert result.version == "codebase-memory-mcp 0.12.1"
    download, install, verify = calls
    assert (
        download[1] == 60 and install[1] == 300 and verify[1] == native.VERSION_TIMEOUT
    )
    assert "=https" == download[0][download[0].index("--proto") + 1]
    assert "=https" == download[0][download[0].index("--proto-redir") + 1]
    assert download[0][-1] == native.INSTALL_URL and "--fail" in download[0]
    assert install[0] == ["/fixture/bash", str(scripts[0]), f"--dir={canonical.parent}"]
    assert not install[2].get("capture_output", False)
    assert verify[0] == [str(canonical), "--version"]
    assert all(not p.exists() and not p.parent.exists() for p in scripts)
    output = capsys.readouterr().out
    assert native.INSTALL_URL in output and str(canonical) in output
    assert "detected clients" in output and "companion" in output


@pytest.mark.parametrize(
    "failure,stage",
    [
        ("empty", "download"),
        ("download_nonzero", "download"),
        ("download_timeout", "download"),
        ("download_oserror", "download"),
        ("install_nonzero", "install"),
        ("install_timeout", "install"),
        ("install_oserror", "install"),
        ("missing_postcheck", "verification"),
        ("verification_nonzero", "verification"),
        ("verification_timeout", "verification"),
        ("verification_oserror", "verification"),
        ("empty_version", "verification"),
        ("postcheck_symlink", "verification"),
    ],
)
def test_stage_failures_cleanup(failure, stage, isolated_home, monkeypatch):
    calls, scripts, _ = setup_acquisition(monkeypatch, isolated_home, failure)
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == stage
    assert all(not p.exists() and not p.parent.exists() for p in scripts)
    if stage == "download":
        assert len(calls) == 1
    if stage == "install":
        assert "partial" in result.message.lower()


def test_nonrunnable_canonical_repaired(isolated_home, monkeypatch):
    canonical = binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    canonical.chmod(0o600)
    setup_acquisition(monkeypatch, isolated_home)
    result = native.acquire_codebase_memory()
    assert result.success and result.acquired


def test_tempdir_error_structured(monkeypatch):
    monkeypatch.setattr(native.shutil, "which", lambda name: f"/fixture/{name}")
    monkeypatch.setattr(
        native.tempfile,
        "TemporaryDirectory",
        lambda **kwargs: (_ for _ in ()).throw(PermissionError("temp denied")),
    )
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "download"


_REAL_RUN = native._run_bounded


def test_real_timeout_terminates_and_reaps_group(tmp_path, monkeypatch):
    """Only a benign local parent/child; no installer, network or developer HOME."""
    pid_file = tmp_path / "pids"
    code = """
import os, signal, subprocess, sys, time
child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
def stop(*args):
    child.wait(timeout=2)
    sys.exit(0)
signal.signal(signal.SIGTERM, stop)
with open(sys.argv[1], 'w') as f:
    f.write(str(os.getpid()) + ' ' + str(child.pid))
while True:
    time.sleep(.01)
"""
    with pytest.raises(subprocess.TimeoutExpired):
        _REAL_RUN([sys.executable, "-c", code, str(pid_file)], 1)
    pids = [int(pid) for pid in pid_file.read_text().split()]
    for pid in pids:
        with pytest.raises(ProcessLookupError):
            os.kill(pid, 0)
    with pytest.raises(ProcessLookupError):
        os.killpg(pids[0], 0)


@pytest.mark.parametrize("capture_output", [False, True])
@pytest.mark.parametrize("new_session", [False, True])
def test_real_leader_exits_before_term_ignoring_orphan(
    tmp_path, capture_output, new_session
):
    """Product adoption/reaping only: no test adopter and no external PID1 wait."""
    pid_file = tmp_path / "orphan"
    leader_file = tmp_path / "leader"
    code = """
import os, signal, subprocess, sys, time
from pathlib import Path
Path(sys.argv[2]).write_text(str(os.getpid()))
grandchild = '''
import os, signal, sys, time
from pathlib import Path
if sys.argv[2] == 'True':
    os.setsid()
signal.signal(signal.SIGTERM, signal.SIG_IGN)
Path(sys.argv[1]).write_text(str(os.getpid()))
while True:
    time.sleep(.01)
'''
subprocess.Popen([sys.executable, '-c', grandchild, sys.argv[1], sys.argv[3]])
while not Path(sys.argv[1]).exists():
    time.sleep(.01)
# Exit without waiting for the grandchild. The product supervisor must adopt it.
os._exit(0)
"""
    started = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired):
        _REAL_RUN(
            [
                sys.executable,
                "-c",
                code,
                str(pid_file),
                str(leader_file),
                str(new_session),
            ],
            0.5,
            capture_output=capture_output,
        )
    assert (
        time.monotonic() - started
        < 0.5 + native.TERMINATE_GRACE + native.REAP_TIMEOUT + 2
    )
    for path in (pid_file, leader_file):
        with pytest.raises(ProcessLookupError):
            os.kill(int(path.read_text()), 0)


def test_host_subreaper_flag_and_unrelated_child_unchanged():
    import ctypes

    flag = ctypes.c_int()
    libc = ctypes.CDLL(None, use_errno=True)
    assert (
        libc.prctl(37, ctypes.byref(flag), 0, 0, 0) == 0
    )  # PR_GET_CHILD_SUBREAPER only
    before = flag.value
    unrelated = subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(.1); raise SystemExit(23)"]
    )
    try:
        result = _REAL_RUN(
            [sys.executable, "-c", "print('benign')"], 2, capture_output=True
        )
        assert result.returncode == 0
        assert unrelated.wait(timeout=2) == 23
        assert libc.prctl(37, ctypes.byref(flag), 0, 0, 0) == 0
        assert flag.value == before
    finally:
        if unrelated.poll() is None:
            unrelated.kill()
        unrelated.wait(timeout=2)


def test_real_uncooperative_process_is_killed_and_reaped(tmp_path):
    pid_file = tmp_path / "pid"
    code = """
import os, signal, sys, time
signal.signal(signal.SIGTERM, signal.SIG_IGN)
with open(sys.argv[1], 'w') as f:
    f.write(str(os.getpid()))
while True:
    time.sleep(.01)
"""
    with pytest.raises(subprocess.TimeoutExpired):
        _REAL_RUN([sys.executable, "-c", code, str(pid_file)], 1, capture_output=True)
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_file.read_text()), 0)


def test_local_process_output_captured_or_preserved(capfd):
    result = _REAL_RUN(
        [sys.executable, "-c", "print('version fixture')"], 2, capture_output=True
    )
    assert result.returncode == 0 and result.stdout == "version fixture\n"
    assert capfd.readouterr().out == ""
    result = _REAL_RUN([sys.executable, "-c", "print('native output fixture')"], 2)
    assert result.returncode == 0 and result.stdout is None
    assert capfd.readouterr().out == "native output fixture\n"


def test_real_native_nonzero_preserved():
    result = _REAL_RUN(
        [sys.executable, "-c", "raise SystemExit(17)"], 2, capture_output=True
    )
    assert result.returncode == 17


def test_real_native_exec_failure_reported(tmp_path):
    with pytest.raises(subprocess.SubprocessError, match="Native supervision failed"):
        _REAL_RUN([str(tmp_path / "missing-executable")], 2, capture_output=True)


def test_home_discovery_error_is_structured(monkeypatch):
    monkeypatch.setattr(
        Path, "home", lambda: (_ for _ in ()).throw(RuntimeError("no home"))
    )
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "discovery"
    assert "no home" in result.message


def test_canonical_foreign_file_owner(isolated_home, monkeypatch):
    canonical = binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    # Test file ownership separately from the directory guard, without chown.
    original = Path.lstat

    def lstat(path, *args, **kwargs):
        info = original(path, *args, **kwargs)
        if path == canonical:
            values = list(info)
            values[4] = 99999999
            return os.stat_result(values)
        return info

    monkeypatch.setattr(Path, "lstat", lstat)
    assert native.discover_executable().state == "ambiguous"


def test_missing_canonical_on_path_skipped(isolated_home, monkeypatch):
    monkeypatch.setenv("PATH", str(isolated_home / ".local/bin"))
    assert native.discover_executable().state == "missing"


def test_path_lookup_error_is_ambiguous(monkeypatch):
    monkeypatch.setattr(
        native.os,
        "get_exec_path",
        lambda: (_ for _ in ()).throw(OSError("path unavailable")),
    )
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "discovery"
