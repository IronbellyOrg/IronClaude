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


@pytest.fixture
def owned_native(isolated_home, monkeypatch):
    # Provenance is produced by the product acquisition path, not fabricated by
    # a test-only receipt/adoption mechanism. Only bootstrap processes are mocked.
    calls, scripts, executable = setup_acquisition(monkeypatch, isolated_home)
    assert native.acquire_codebase_memory().success
    calls.clear()
    sentinels = []
    for relative in (
        ".cache/codebase-memory-mcp/project.db",
        ".claude/unrelated.json",
        ".claude/skills/keep/SKILL.md",
        ".local/bin/install.sh",
    ):
        path = isolated_home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("retained sentinel")
        sentinels.append(path)

    def run(argv, timeout, **kwargs):
        calls.append((argv, timeout, kwargs))
        if argv == [str(executable), "--version"]:
            return subprocess.CompletedProcess(
                argv, 0, "codebase-memory-mcp 0.12.1", ""
            )
        assert argv == [
            str(executable),
            "uninstall",
            "-y",
            f"--dir={executable.parent}",
        ]
        assert timeout == native.INSTALL_TIMEOUT
        executable.unlink()  # Simulate only the upstream native removal.
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr(native, "_run_bounded", run)
    return executable, calls, sentinels


def test_acquisition_records_private_binary_identity(isolated_home, monkeypatch):
    import json

    setup_acquisition(monkeypatch, isolated_home)
    result = native.acquire_codebase_memory()
    receipt = native._receipt_path()
    assert result.success and receipt.is_file()
    assert receipt.stat().st_mode & 0o777 == 0o600
    data = json.loads(receipt.read_text())
    assert data["source"] == native.INSTALL_URL
    assert data["identity"] == native._binary_identity(result.executable)
    assert len(data["identity"]["sha256"]) == 64


def test_existing_canonical_is_never_adopted(isolated_home, monkeypatch):
    binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    probe_ok(monkeypatch)
    assert native.acquire_codebase_memory().success
    assert not native._receipt_path().exists()
    preview = native.preview_codebase_memory_removal()
    assert preview.state == "ambiguous" and "receipt" in preview.message.lower()


def test_receipt_write_failure_reports_partial_acquisition(isolated_home, monkeypatch):
    calls, scripts, executable = setup_acquisition(monkeypatch, isolated_home)
    monkeypatch.setattr(
        native,
        "_write_acquisition_receipt",
        lambda *a: (_ for _ in ()).throw(PermissionError("receipt denied")),
    )
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "provenance"
    assert "partial" in result.message.lower() and executable.exists()
    assert all(not path.exists() and not path.parent.exists() for path in scripts)


def partial_upstream(monkeypatch, home, failure):
    """Upstream places the binary, then fails before completing its setup."""
    calls = []
    canonical = home / ".local/bin" / native.BINARY_NAME
    monkeypatch.setattr(native.shutil, "which", lambda name: f"/fixture/{name}")

    def run(argv, timeout, **kwargs):
        calls.append(argv)
        if argv[0] == "/fixture/curl":
            Path(argv[argv.index("--output") + 1]).write_text("fixture\n")
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[0] == "/fixture/bash":
            binary(canonical)
            if failure == "timeout":
                raise subprocess.TimeoutExpired(argv, timeout)
            if failure == "oserror":
                raise PermissionError("denied fixture")
            return subprocess.CompletedProcess(argv, 7, "", "fixture diagnostic")
        return subprocess.CompletedProcess(argv, 0, "codebase-memory-mcp 0.12.1\n", "")

    monkeypatch.setattr(native, "_run_bounded", run)
    return calls, canonical


@pytest.mark.parametrize("failure", ["nonzero", "timeout", "oserror"])
def test_retry_after_partial_upstream_reacquires(failure, isolated_home, monkeypatch):
    _, canonical = partial_upstream(monkeypatch, isolated_home, failure)
    first = native.acquire_codebase_memory()
    assert not first.success and canonical.exists()
    assert native._pending_path().is_file() and not native._receipt_path().exists()
    calls, _, _ = setup_acquisition(monkeypatch, isolated_home)
    retry = native.acquire_codebase_memory()
    assert retry.success and retry.acquired
    assert any(argv[0] == "/fixture/bash" for argv, _, _ in calls)
    assert native._receipt_path().is_file() and not native._pending_path().exists()


def test_retry_after_receipt_write_failure_reacquires(isolated_home, monkeypatch):
    setup_acquisition(monkeypatch, isolated_home)
    write_receipt = native._write_acquisition_receipt
    monkeypatch.setattr(
        native,
        "_write_acquisition_receipt",
        lambda *a: (_ for _ in ()).throw(PermissionError("receipt denied")),
    )
    assert native.acquire_codebase_memory().stage == "provenance"
    assert native._pending_path().is_file()
    monkeypatch.setattr(native, "_write_acquisition_receipt", write_receipt)
    retry = native.acquire_codebase_memory()
    assert retry.success and retry.acquired and native._receipt_path().is_file()
    assert not native._pending_path().exists()


@pytest.mark.parametrize("kind", ["symlink", "shared"])
def test_untrusted_pending_marker_fails_closed(kind, isolated_home, monkeypatch):
    binary(isolated_home / ".local/bin" / native.BINARY_NAME)
    calls = probe_ok(monkeypatch)
    marker = native._pending_path()
    target = isolated_home / "do-not-touch"
    target.write_text("keep\n")
    if kind == "symlink":
        marker.symlink_to(target)
    else:
        marker.write_text("")
        marker.chmod(0o644)
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "discovery"
    assert all(argv[0] != "/fixture/bash" for argv, _, _ in calls)
    assert target.read_text() == "keep\n"


def test_pending_marker_does_not_block_external_reuse(isolated_home, monkeypatch):
    external = binary(isolated_home / "package manager/bin" / native.BINARY_NAME)
    monkeypatch.setenv("PATH", str(external.parent))
    probe_ok(monkeypatch)
    monkeypatch.setattr(
        native.shutil, "which", lambda _: pytest.fail("prerequisite lookup")
    )
    marker = native._pending_path()
    marker.parent.mkdir(parents=True)
    marker.write_text("")
    marker.chmod(0o600)
    result = native.acquire_codebase_memory()
    assert result.success and result.executable == external and not result.acquired
    assert marker.is_file()


def test_marker_failure_stops_before_upstream(isolated_home, monkeypatch):
    calls, _, _ = setup_acquisition(monkeypatch, isolated_home)
    monkeypatch.setattr(
        native,
        "_mark_acquisition_pending",
        lambda: (_ for _ in ()).throw(PermissionError("marker denied")),
    )
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "prerequisites"
    assert all(argv[0] != "/fixture/bash" for argv, _, _ in calls)


def test_successful_acquisition_clears_pending_marker(isolated_home, monkeypatch):
    setup_acquisition(monkeypatch, isolated_home)
    assert native.acquire_codebase_memory().acquired
    assert not native._pending_path().exists()


def test_receipt_symlink_is_not_overwritten(isolated_home, monkeypatch):
    setup_acquisition(monkeypatch, isolated_home)
    receipt = native._receipt_path()
    receipt.parent.mkdir(parents=True)
    target = isolated_home / "do-not-overwrite"
    target.write_text("keep")
    receipt.symlink_to(target)
    result = native.acquire_codebase_memory()
    assert not result.success and result.stage == "provenance"
    assert receipt.is_symlink() and target.read_text() == "keep"


def test_owned_removal_uses_upstream_and_preserves_sentinels(owned_native):
    executable, calls, sentinels = owned_native
    preview = native.preview_codebase_memory_removal()
    assert preview.state == "ready" and preview.executable == executable
    for phrase in (
        "detected clients",
        "companion",
        "active sessions",
        "indexes",
        "updater",
    ):
        assert phrase in preview.message.lower()
    result = native.uninstall_codebase_memory(confirmed=True)
    assert result.success and not executable.exists()
    assert not native._receipt_path().exists()
    removals = [call for call in calls if "uninstall" in call[0]]
    assert len(removals) == 1
    assert removals[0][0] == [
        str(executable),
        "uninstall",
        "-y",
        f"--dir={executable.parent}",
    ]
    assert not removals[0][2].get("capture_output", False)
    assert all(path.read_text() == "retained sentinel" for path in sentinels)
    assert "updater" in result.message.lower() and "indexes" in result.message.lower()


@pytest.mark.parametrize(
    "tamper", ["bytes", "inode", "receipt", "permissions", "symlink"]
)
def test_removal_refuses_identity_or_receipt_ambiguity(
    owned_native, isolated_home, tamper
):
    executable, calls, _ = owned_native
    if tamper == "bytes":
        executable.write_text("modified executable")
    elif tamper == "inode":
        contents = executable.read_bytes()
        executable.unlink()
        executable.write_bytes(contents)
        executable.chmod(0o700)
    elif tamper == "receipt":
        native._receipt_path().write_text("not-json")
    elif tamper == "permissions":
        native._receipt_path().chmod(0o644)
    else:
        executable.unlink()
        executable.symlink_to(isolated_home / "missing")
    result = native.uninstall_codebase_memory(confirmed=True)
    assert not result.success and result.stage == "discovery"
    assert not any("uninstall" in call[0] for call in calls)


@pytest.mark.parametrize("failure", ["nonzero", "timeout", "oserror", "survives"])
def test_native_removal_failures_no_blind_second_pass(
    owned_native, monkeypatch, failure
):
    executable, calls, sentinels = owned_native
    original = native._run_bounded

    def run(argv, timeout, **kwargs):
        if "uninstall" not in argv:
            return original(argv, timeout, **kwargs)
        calls.append((argv, timeout, kwargs))
        if failure == "timeout":
            raise subprocess.TimeoutExpired(argv, timeout)
        if failure == "oserror":
            raise PermissionError("fixture denied")
        return subprocess.CompletedProcess(
            argv, 7 if failure == "nonzero" else 0, "", ""
        )

    monkeypatch.setattr(native, "_run_bounded", run)
    result = native.uninstall_codebase_memory(confirmed=True)
    assert not result.success and "partial" in result.message.lower()
    assert "retry" in result.message.lower()
    assert sum("uninstall" in call[0] for call in calls) == 1
    assert executable.exists() and all(
        path.read_text() == "retained sentinel" for path in sentinels
    )


def test_removal_reports_all_remaining_path_entries(
    owned_native, isolated_home, monkeypatch
):
    executable, _, _ = owned_native
    alternates = [
        binary(isolated_home / name / native.BINARY_NAME)
        for name in ("external one", "external two")
    ]
    monkeypatch.setenv("PATH", os.pathsep.join(str(path.parent) for path in alternates))
    result = native.uninstall_codebase_memory(confirmed=True)
    assert result.success and not executable.exists()
    assert result.remaining == tuple(alternates)
    assert all(str(path) in result.message and path.exists() for path in alternates)


def test_external_only_removal_refuses_with_resolved_paths(isolated_home, monkeypatch):
    external = binary(isolated_home / "package managed" / native.BINARY_NAME)
    monkeypatch.setenv("PATH", str(external.parent))
    preview = native.preview_codebase_memory_removal()
    assert preview.state == "external" and str(external.resolve()) in preview.message
    result = native.uninstall_codebase_memory(confirmed=True)
    assert not result.success and external.exists()


def test_missing_native_is_idempotent_without_acquisition(monkeypatch):
    monkeypatch.setattr(
        native,
        "acquire_codebase_memory",
        lambda **k: pytest.fail("acquisition on removal"),
    )
    assert native.preview_codebase_memory_removal().state == "missing"
    assert native.uninstall_codebase_memory(confirmed=True).success


def test_removal_requires_explicit_confirmation(owned_native):
    executable, calls, _ = owned_native
    result = native.uninstall_codebase_memory()
    assert not result.success and result.stage == "consent"
    assert executable.exists() and calls == []


@pytest.mark.parametrize("scope", ["project", "local"])
def test_removal_rejects_other_scopes_before_processes(scope):
    result = native.uninstall_codebase_memory(scope=scope, confirmed=True)
    assert not result.success and result.stage == "scope"


def test_removal_unsupported_platform_before_processes(monkeypatch):
    monkeypatch.setattr(native.platform, "system", lambda: "Darwin")
    assert native.preview_codebase_memory_removal().state == "unsupported"
    result = native.uninstall_codebase_memory(confirmed=True)
    assert not result.success and result.stage == "discovery"
