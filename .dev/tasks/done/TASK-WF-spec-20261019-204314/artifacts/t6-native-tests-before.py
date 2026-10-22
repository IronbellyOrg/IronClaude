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


@pytest.fixture
def mcp_cli(monkeypatch, isolated_home):
    from types import SimpleNamespace

    from click.testing import CliRunner

    from superclaude.cli import install_mcp
    from superclaude.cli.main import main

    config = isolated_home / "cli config"
    config.mkdir()
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(config))
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.delenv("MORPH_API_KEY", raising=False)
    state = SimpleNamespace(
        runner=CliRunner(),
        main=main,
        module=install_mcp,
        interactive=False,
        calls=[],
        processes=[],
        native_ok=True,
        gateway_ok=True,
        claude_ok=True,
        docker_ok=True,
        node_version="v20.0.0",
        auggie_version="auggie 0.36.0",
        missing_tools=set(),
        native_state="canonical",
        real_native_install=install_mcp.install_codebase_memory_mcp,
        real_native_remove=install_mcp.uninstall_codebase_memory_mcp,
        real_gateway=install_mcp.install_airis_gateway,
    )
    monkeypatch.setattr(
        install_mcp, "_is_interactive", lambda: state.interactive, raising=False
    )
    monkeypatch.setattr(
        install_mcp.shutil,
        "which",
        lambda name: None if name in state.missing_tools else f"/fixture/{name}",
    )
    monkeypatch.setattr(install_mcp, "check_mcp_server_installed", lambda name: False)
    monkeypatch.setattr(
        native,
        "discover_executable",
        lambda: native.Discovery(
            state.native_state,
            native.canonical_executable(),
            "0.12.1" if state.native_state == "canonical" else None,
        ),
    )
    monkeypatch.setattr(
        native,
        "preview_codebase_memory_removal",
        lambda: native.RemovalPreview(
            "ready", native.REMOVAL_EFFECTS, native.canonical_executable()
        ),
    )

    def command(argv, **kwargs):
        state.processes.append(argv)
        if argv == ["claude", "--version"]:
            return subprocess.CompletedProcess(
                argv, 0 if state.claude_ok else 1, "fixture", ""
            )
        if argv == ["node", "--version"]:
            return subprocess.CompletedProcess(
                argv, 0 if state.node_version else 1, state.node_version or "", ""
            )
        if argv == ["docker", "info"]:
            return subprocess.CompletedProcess(
                argv, 0 if state.docker_ok else 1, "", ""
            )
        if argv == ["auggie", "--version"]:
            return subprocess.CompletedProcess(argv, 0, state.auggie_version, "")
        if argv == ["uv", "--version"]:
            return subprocess.CompletedProcess(argv, 0, "uv fixture", "")
        if len(argv) == 2 and argv[0] in {"npx", "npm"} and argv[1] == "--version":
            return subprocess.CompletedProcess(
                argv, 1 if argv[0] in state.missing_tools else 0, "fixture version", ""
            )
        if argv[:3] == ["claude", "mcp", "add"]:
            return subprocess.CompletedProcess(argv, 0, "", "")
        if argv[:3] == ["claude", "mcp", "get"]:
            return subprocess.CompletedProcess(
                argv,
                0,
                "tavily:\n  Scope: User config\n  Command: npx\n  Args: -y tavily-mcp@0.1.2\n",
                "",
            )
        pytest.fail(f"Unexpected external command: {argv}")

    def install(*, scope, dry_run):
        state.calls.append(("native", scope, dry_run))
        return state.native_ok, "native fixture result"

    def remove(*, scope, confirmed=False, dry_run=False):
        state.calls.append(("preview" if dry_run else "remove", scope, confirmed))
        return True, ("[DRY RUN] " if dry_run else "") + native.REMOVAL_EFFECTS

    def gateway(dry_run=False):
        state.calls.append(("gateway", dry_run))
        return state.gateway_ok

    monkeypatch.setattr(install_mcp, "_run_command", command)
    monkeypatch.setattr(install_mcp, "install_codebase_memory_mcp", install)
    monkeypatch.setattr(install_mcp, "uninstall_codebase_memory_mcp", remove)
    monkeypatch.setattr(install_mcp, "install_airis_gateway", gateway)
    return state


def test_mcp_cli_help_documents_new_lifecycle_flags(mcp_cli):
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--help"])
    assert result.exit_code == 0
    for text in (
        "--uninstall",
        "--yes",
        "-y",
        "--servers",
        "--scope",
        "--dry-run",
        "codebase-memory-mcp",
    ):
        assert text in result.output
    assert "new" in result.output.lower() and mcp_cli.calls == []


@pytest.mark.parametrize(
    "extra",
    [
        ["--uninstall"],
        ["--yes"],
        ["--dry-run"],
        ["--servers", "codebase-memory-mcp"],
        ["--scope", "project"],
    ],
)
def test_mcp_list_rejects_incompatible_modes_before_lookup(mcp_cli, monkeypatch, extra):
    monkeypatch.setattr(
        mcp_cli.module,
        "list_available_servers",
        lambda: pytest.fail("list lookup before option validation"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list", *extra])
    assert result.exit_code != 0 and mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_list_shows_native_without_effects(mcp_cli):
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--list"])
    assert result.exit_code == 0 and "codebase-memory-mcp" in result.output
    assert mcp_cli.calls == []


@pytest.mark.parametrize(
    "extra", [[], ["--yes"], ["--uninstall"], ["--uninstall", "--yes"]]
)
def test_mcp_noninteractive_requires_selection_without_prompt(
    mcp_cli, monkeypatch, extra
):
    monkeypatch.setattr(
        mcp_cli.module.click, "prompt", lambda *a, **k: pytest.fail("non-TTY menu")
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", *extra])
    assert result.exit_code != 0 and "select" in result.output.lower()
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_no_selection_dry_run_prints_choices_and_native_disclosures(
    mcp_cli, monkeypatch
):
    monkeypatch.setattr(
        mcp_cli.module.click, "prompt", lambda *a, **k: pytest.fail("dry-run prompt")
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "--dry-run"])
    assert result.exit_code == 0
    for text in (
        "Install MCP servers",
        "Uninstall Codebase Memory",
        "Cancel",
        "airis-mcp-gateway",
        "codebase-memory-mcp",
        native.INSTALL_URL,
        "user",
        "indexes",
    ):
        assert text in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_menu_defaults_install_then_gateway(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="\n\n")
    assert result.exit_code == 0, result.output
    assert (
        "Install MCP servers" in result.output
        and "Uninstall Codebase Memory" in result.output
    )
    assert mcp_cli.calls == [("gateway", False)]


def test_mcp_menu_cancel_has_no_effects(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="3\n")
    assert result.exit_code == 0 and "cancel" in result.output.lower()
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_menu_native_uninstall_default_no(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="2\n\n")
    assert result.exit_code == 0, result.output
    assert "[y/N]" in result.output and "active sessions" in result.output
    assert mcp_cli.calls == [("preview", "user", False)]


def test_mcp_menu_install_all_includes_native(mcp_cli, monkeypatch):
    mcp_cli.interactive = True
    monkeypatch.setattr(mcp_cli.module, "prompt_for_api_key", lambda *a, **k: None)
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="1\n0\n")
    assert result.exit_code == 0, result.output
    assert ("native", "user", False) in mcp_cli.calls
    assert any("tavily-mcp@0.2.22" in cmd for cmd in mcp_cli.processes)
    assert ("gateway", False) not in mcp_cli.calls


def test_mcp_native_only_needs_no_node_docker_or_acquisition_tools_when_reused(mcp_cli):
    mcp_cli.node_version = None
    mcp_cli.docker_ok = False
    mcp_cli.missing_tools = {"curl", "bash", "npm", "node", "docker"}
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", "codebase-memory-mcp"])
    assert result.exit_code == 0, result.output
    assert mcp_cli.calls == [("native", "user", False)]
    assert mcp_cli.processes == [["claude", "--version"]]


@pytest.mark.parametrize("scope", ["project", "local"])
def test_mcp_native_scope_rejected_before_mixed_selection_effects(mcp_cli, scope):
    result = mcp_cli.runner.invoke(
        mcp_cli.main,
        [
            "mcp",
            "-s",
            "airis-mcp-gateway",
            "-s",
            "codebase-memory-mcp",
            "--scope",
            scope,
        ],
    )
    assert result.exit_code != 0 and "user" in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_native_platform_rejected_before_gateway_effects(mcp_cli, monkeypatch):
    monkeypatch.setattr(native.platform, "system", lambda: "Darwin")
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", "codebase-memory-mcp"]
    )
    assert result.exit_code != 0 and "Linux" in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


@pytest.mark.parametrize(
    "native_ok,gateway_ok", [(True, True), (True, False), (False, True), (False, False)]
)
def test_mcp_mixed_gateway_native_executes_both_and_aggregates(
    mcp_cli, native_ok, gateway_ok
):
    mcp_cli.native_ok, mcp_cli.gateway_ok = native_ok, gateway_ok
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", "codebase-memory-mcp"]
    )
    assert result.exit_code == (0 if native_ok and gateway_ok else 1), result.output
    assert mcp_cli.calls == [("gateway", False), ("native", "user", False)]
    if not native_ok:
        assert "codebase-memory-mcp" in result.output
    if not gateway_ok:
        assert "airis-mcp-gateway" in result.output


def test_mcp_unknown_mixed_selection_rejected_before_any_prerequisites(mcp_cli):
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "codebase-memory-mcp", "-s", "unknown"]
    )
    assert result.exit_code != 0 and "unknown" in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


@pytest.mark.parametrize(
    "selection,version,minimum",
    [("context7", "v17.0.0", "18"), ("auggie", "v19.0.0", "20")],
)
def test_mcp_selected_npm_node_minimum_before_any_install(
    mcp_cli, selection, version, minimum
):
    mcp_cli.node_version = version
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", selection]
    )
    assert result.exit_code != 0 and minimum in result.output
    assert mcp_cli.calls == []


def test_mcp_missing_acquisition_prerequisite_prevents_gateway_effects(mcp_cli):
    mcp_cli.native_state = "missing"
    mcp_cli.missing_tools = {"curl"}
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", "codebase-memory-mcp"]
    )
    assert result.exit_code != 0 and "curl" in result.output
    assert mcp_cli.calls == []


@pytest.mark.parametrize(
    "servers", [["tavily"], ["codebase-memory-mcp", "tavily"], ["unknown"]]
)
def test_mcp_uninstall_rejects_unsupported_or_mixed_selection(mcp_cli, servers):
    args = ["mcp", "--uninstall", "--yes"]
    for server in servers:
        args.extend(["--servers", server])
    result = mcp_cli.runner.invoke(mcp_cli.main, args)
    assert result.exit_code != 0 and mcp_cli.calls == [] and mcp_cli.processes == []


def test_mcp_noninteractive_uninstall_requires_yes(mcp_cli):
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "--uninstall", "-s", "codebase-memory-mcp"]
    )
    assert result.exit_code != 0 and "--yes" in result.output
    assert mcp_cli.calls == []


def test_mcp_explicit_yes_uninstall_previews_then_calls_confirmed(mcp_cli):
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "--uninstall", "-s", "codebase-memory-mcp", "-y"]
    )
    assert result.exit_code == 0, result.output
    assert "detected clients" in result.output and "indexes" in result.output
    assert mcp_cli.calls == [("preview", "user", False), ("remove", "user", True)]


def test_mcp_yes_does_not_bypass_other_api_key_prompt(mcp_cli):
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "tavily", "--yes"], input="y\ncli-test-key\n"
    )
    assert result.exit_code == 0, result.output
    assert "Would you like to set TAVILY_API_KEY" in result.output
    assert any("TAVILY_API_KEY=cli-test-key" in cmd for cmd in mcp_cli.processes)
    assert "cli-test-key" not in result.output


def test_mcp_yes_does_not_bypass_auggie_binary_consent(mcp_cli):
    mcp_cli.auggie_version = "auggie 0.35.0"
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "auggie", "--yes"], input="n\n"
    )
    assert result.exit_code != 0 and "globally" in result.output
    assert not any(cmd[:2] == ["npm", "install"] for cmd in mcp_cli.processes)


@pytest.mark.parametrize("server", ["tavily", "auggie"])
def test_mcp_dry_run_api_key_and_binary_paths_never_prompt_or_mutate(
    mcp_cli, monkeypatch, server
):
    monkeypatch.setattr(
        mcp_cli.module.click,
        "confirm",
        lambda *a, **k: pytest.fail("dry-run confirmation"),
    )
    monkeypatch.setattr(
        mcp_cli.module.click,
        "prompt",
        lambda *a, **k: pytest.fail("dry-run key prompt"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", server, "--dry-run"])
    assert result.exit_code == 0, result.output
    assert not any(
        cmd[:3] in (["claude", "mcp", "add"], ["claude", "mcp", "remove"])
        or cmd[0] in {"npm", "curl"}
        for cmd in mcp_cli.processes
    )


def test_mcp_dry_run_stale_registration_does_not_remove(mcp_cli, monkeypatch):
    monkeypatch.setattr(mcp_cli.module, "check_mcp_server_installed", lambda name: True)
    monkeypatch.setattr(
        mcp_cli.module.click,
        "confirm",
        lambda *a, **k: pytest.fail("dry-run confirmation"),
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp", "-s", "tavily", "--dry-run"])
    assert result.exit_code == 0 and "re-register" in result.output
    assert mcp_cli.processes == [["claude", "mcp", "get", "tavily"]]


def test_mcp_gateway_dry_run_needs_no_docker_and_writes_nothing(
    mcp_cli, monkeypatch, isolated_home
):
    mcp_cli.docker_ok = False
    monkeypatch.setattr(mcp_cli.module, "install_airis_gateway", mcp_cli.real_gateway)
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "--dry-run"]
    )
    assert result.exit_code == 0, result.output
    assert mcp_cli.processes == [] and not (isolated_home / ".superclaude").exists()


@pytest.mark.parametrize("uninstall", [False, True])
def test_mcp_native_dry_run_positive_disclosures_and_no_lifecycle(
    mcp_cli, monkeypatch, uninstall
):
    monkeypatch.setattr(
        mcp_cli.module, "install_codebase_memory_mcp", mcp_cli.real_native_install
    )
    monkeypatch.setattr(
        mcp_cli.module, "uninstall_codebase_memory_mcp", mcp_cli.real_native_remove
    )
    monkeypatch.setattr(
        mcp_cli.module.click,
        "confirm",
        lambda *a, **k: pytest.fail("dry-run confirmation"),
    )
    args = ["mcp", "-s", "codebase-memory-mcp", "--dry-run"] + (
        ["--uninstall"] if uninstall else []
    )
    result = mcp_cli.runner.invoke(mcp_cli.main, args)
    assert result.exit_code == 0, result.output
    for phrase in (
        native.INSTALL_URL,
        "user",
        "detected clients",
        "companion",
        "indexes",
        "retained",
    ):
        assert phrase in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


@pytest.mark.parametrize("server,tool", [("context7", "npx"), ("auggie", "npm")])
def test_mcp_missing_selected_package_tool_prevents_all_effects(mcp_cli, server, tool):
    mcp_cli.missing_tools = {tool}
    mcp_cli.auggie_version = "auggie 0.35.0"
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "airis-mcp-gateway", "-s", server]
    )
    assert result.exit_code != 0 and tool in result.output
    assert mcp_cli.calls == []


@pytest.mark.parametrize("scope", ["project", "local"])
def test_mcp_other_servers_retain_requested_scope(mcp_cli, monkeypatch, scope):
    monkeypatch.setattr(mcp_cli.module, "prompt_for_api_key", lambda *a, **k: None)
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "tavily", "--scope", scope]
    )
    assert result.exit_code == 0, result.output
    add = next(cmd for cmd in mcp_cli.processes if cmd[:3] == ["claude", "mcp", "add"])
    if scope == "project":
        assert add[add.index("--scope") + 1] == "project"
    else:
        assert "--scope" not in add  # Legacy local default remains unchanged.


def test_mcp_invalid_menu_number_does_not_install_partial_valid_selection(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(mcp_cli.main, ["mcp"], input="1\n1,999\n")
    assert result.exit_code != 0 and "Invalid selection" in result.output
    assert mcp_cli.calls == [] and mcp_cli.processes == []


@pytest.mark.parametrize("missing", ["claude", "docker"])
def test_mcp_readiness_failure_prevents_all_mixed_install_effects(mcp_cli, missing):
    mcp_cli.claude_ok = missing != "claude"
    mcp_cli.docker_ok = missing != "docker"
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "-s", "codebase-memory-mcp", "-s", "airis-mcp-gateway"]
    )
    assert result.exit_code != 0 and mcp_cli.calls == []


def test_mcp_interactive_explicit_removal_requires_and_obeys_confirmation(mcp_cli):
    mcp_cli.interactive = True
    result = mcp_cli.runner.invoke(
        mcp_cli.main, ["mcp", "--uninstall", "-s", "codebase-memory-mcp"], input="y\n"
    )
    assert result.exit_code == 0, result.output
    assert "[y/N]" in result.output
    assert mcp_cli.calls == [("preview", "user", False), ("remove", "user", True)]


@pytest.mark.parametrize(
    "selection",
    [
        ["airis-mcp-gateway"],
        ["airis-mcp-gateway", "codebase-memory-mcp"],
        ["codebase-memory-mcp", "airis-mcp-gateway"],
    ],
)
@pytest.mark.parametrize("dry_run", [False, True])
def test_mcp_gateway_curl_preflight_before_any_selected_effects(
    mcp_cli, isolated_home, monkeypatch, selection, dry_run
):
    mcp_cli.missing_tools = {"curl"}
    mcp_cli.native_state = "canonical"  # Reuse must not hide the gateway's curl need.
    monkeypatch.setattr(mcp_cli.module, "install_airis_gateway", mcp_cli.real_gateway)
    original = mcp_cli.module._run_command

    def command(argv, **kwargs):
        if argv[0] == "curl":
            mcp_cli.processes.append(argv)
            return subprocess.CompletedProcess(argv, 127, "", "curl not found")
        return original(argv, **kwargs)

    monkeypatch.setattr(mcp_cli.module, "_run_command", command)
    before = sorted(
        str(path.relative_to(isolated_home)) for path in isolated_home.rglob("*")
    )
    args = ["mcp"]
    for server in selection:
        args.extend(["--servers", server])
    if dry_run:
        args.append("--dry-run")
    result = mcp_cli.runner.invoke(mcp_cli.main, args)
    assert result.exit_code == (0 if dry_run else 1), result.output
    if not dry_run:
        assert "curl" in result.output and mcp_cli.calls == []
    else:
        assert "DRY RUN" in result.output
    assert not any(
        cmd[0] == "curl"
        or cmd[:3]
        in (
            ["claude", "mcp", "add"],
            ["claude", "mcp", "add-json"],
            ["claude", "mcp", "remove"],
        )
        for cmd in mcp_cli.processes
    )
    assert not (isolated_home / ".superclaude").exists()
    assert (
        sorted(
            str(path.relative_to(isolated_home)) for path in isolated_home.rglob("*")
        )
        == before
    )
