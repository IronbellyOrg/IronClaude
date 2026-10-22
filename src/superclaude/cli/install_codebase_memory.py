"""Bounded full upstream acquisition, independent of MCP registration.

A canonical location is not proof of upstream ownership. Discovery is suitable
for reuse/preview, not authorization to uninstall an arbitrary executable.
"""

import ctypes
import hashlib
import json
import os
import platform
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

BINARY_NAME = "codebase-memory-mcp"
INSTALL_URL = (
    "https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh"
)
DOWNLOAD_TIMEOUT = 60
INSTALL_TIMEOUT = 300
VERSION_TIMEOUT = 10
TERMINATE_GRACE = 1
REAP_TIMEOUT = 3


@dataclass(frozen=True)
class Discovery:
    """Read-only observation; canonical/external states have a verified version."""

    state: Literal["missing", "canonical", "external", "non_runnable", "ambiguous"]
    executable: Path | None = None
    version: str | None = None
    message: str = ""


@dataclass(frozen=True)
class AcquisitionResult:
    success: bool
    stage: str
    message: str
    executable: Path | None = None
    version: str | None = None
    acquired: bool = False


def canonical_executable() -> Path:
    return Path.home().absolute() / ".local" / "bin" / BINARY_NAME


@dataclass(frozen=True)
class RemovalPreview:
    state: Literal["ready", "missing", "external", "ambiguous", "unsupported"]
    message: str
    executable: Path | None = None
    remaining: tuple[Path, ...] = ()


@dataclass(frozen=True)
class RemovalResult:
    success: bool
    stage: str
    message: str
    remaining: tuple[Path, ...] = ()


REMOVAL_EFFECTS = (
    "Full user-level removal affects detected clients and companion integrations, "
    "may interrupt active sessions, and retains graph indexes. "
    "The adjacent updater is left in place; IronClaude does not erase companion/cache files."
)


def _receipt_path() -> Path:
    return canonical_executable().parent / ".superclaude-codebase-memory.json"


def _pending_path() -> Path:
    return canonical_executable().parent / ".superclaude-codebase-memory.pending"


def _acquisition_pending() -> bool:
    """True if our own upstream run started and never reached a written receipt."""
    try:
        info = _pending_path().lstat()
    except FileNotFoundError:
        return False
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != os.getuid()
        or info.st_nlink != 1
        or info.st_mode & 0o077
    ):
        raise ValueError(
            "Acquisition pending marker is not a private owned regular file"
        )
    return True


def _mark_acquisition_pending() -> None:
    """Record, before upstream runs, that an acquisition is in progress."""
    canonical = canonical_executable()
    for directory in (canonical.parent.parent, canonical.parent):
        directory.mkdir(mode=0o755, exist_ok=True)
    _check_install_directory()
    try:
        os.close(
            os.open(
                _pending_path(),
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                0o600,
            )
        )
    except FileExistsError:
        _acquisition_pending()  # An existing marker must still be our private file.


def _check_install_directory() -> None:
    canonical = canonical_executable()
    for directory in (canonical.parent.parent, canonical.parent):
        if directory.resolve() != directory:
            raise ValueError("Symlinked canonical directory")
        if directory.exists():
            info = directory.stat()
            if (
                not stat.S_ISDIR(info.st_mode)
                or info.st_uid != os.getuid()
                or info.st_mode & 0o022
            ):
                raise ValueError(
                    "Canonical directory ownership/permissions are uncertain"
                )


def _binary_identity(path: Path) -> dict:
    _check_install_directory()
    if path.resolve() != path:
        raise ValueError("Symlinked canonical executable")
    with os.fdopen(
        os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK), "rb"
    ) as source:
        info = os.fstat(source.fileno())
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_nlink != 1
            or info.st_mode & 0o022
        ):
            raise ValueError("Canonical executable identity is uncertain")
        digest = hashlib.sha256()
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(source.fileno())
        current = path.lstat()
        if (
            info.st_dev,
            info.st_ino,
            info.st_size,
            info.st_mtime_ns,
            info.st_ctime_ns,
        ) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_ctime_ns,
        ) or (info.st_dev, info.st_ino) != (current.st_dev, current.st_ino):
            raise ValueError("Canonical executable changed during identity check")
        return {
            "path": str(path),
            "device": info.st_dev,
            "inode": info.st_ino,
            "size": info.st_size,
            "mtime_ns": info.st_mtime_ns,
            "ctime_ns": info.st_ctime_ns,
            "sha256": digest.hexdigest(),
        }


def _read_acquisition_receipt() -> dict | None:
    path = _receipt_path()
    try:
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except FileNotFoundError:
        return None
    with os.fdopen(descriptor, "r", encoding="utf-8") as source:
        info = os.fstat(source.fileno())
        if (
            not stat.S_ISREG(info.st_mode)
            or info.st_uid != os.getuid()
            or info.st_nlink != 1
            or info.st_mode & 0o077
            or info.st_size > 16384
        ):
            raise ValueError("Acquisition receipt is not a private owned regular file")
        receipt = json.load(source)
    if (
        not isinstance(receipt, dict)
        or receipt.get("source") != INSTALL_URL
        or not isinstance(receipt.get("identity"), dict)
    ):
        raise ValueError("Acquisition receipt is malformed")
    return receipt


def _write_acquisition_receipt(path: Path) -> None:
    """Only called after this integration actually completes upstream acquisition."""
    receipt = {"source": INSTALL_URL, "identity": _binary_identity(path)}
    previous = _read_acquisition_receipt()
    staged_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".cbm-receipt-",
            delete=False,
        ) as staged:
            staged_path = Path(staged.name)
            os.fchmod(staged.fileno(), 0o600)
            json.dump(receipt, staged)
            staged.flush()
            os.fsync(staged.fileno())
        if previous is None:
            os.link(
                staged_path, _receipt_path()
            )  # Never clobber a racing first receipt.
        else:
            if _read_acquisition_receipt() != previous:
                raise ValueError("Acquisition receipt changed concurrently")
            os.replace(staged_path, _receipt_path())
    finally:
        if staged_path is not None:
            staged_path.unlink(missing_ok=True)


def _alternate_path_entries() -> tuple[Path, ...]:
    result = []
    canonical = canonical_executable()
    for directory in os.get_exec_path():
        path = Path(directory).absolute() / BINARY_NAME
        if path == canonical or path in result:
            continue
        try:
            info = path.lstat()
        except FileNotFoundError:
            continue
        if (
            path.resolve() != path
            or not stat.S_ISREG(info.st_mode)
            or info.st_nlink != 1
        ):
            raise ValueError(f"Ambiguous alternate PATH entry: {path}")
        result.append(path)
    return tuple(result)


def preview_codebase_memory_removal() -> RemovalPreview:
    """Read-only preview; only a matching acquisition receipt authorizes removal."""
    if platform.system() != "Linux" or platform.machine().lower() not in {
        "amd64",
        "x86_64",
        "arm64",
        "aarch64",
    }:
        return RemovalPreview(
            "unsupported",
            "Automated removal requires Linux amd64/arm64. Use the official manual mechanism on other platforms.",
        )
    try:
        _check_install_directory()
        canonical = canonical_executable()
        remaining = _alternate_path_entries()
        try:
            canonical.lstat()
        except FileNotFoundError:
            if remaining:
                return RemovalPreview(
                    "external",
                    "External/custom PATH entries found: "
                    + ", ".join(map(str, remaining))
                    + ". Use their own installation mechanism; no automatic removal.",
                    remaining=remaining,
                )
            return RemovalPreview(
                "missing",
                "Canonical native executable is absent. Companion assets were not audited. "
                + REMOVAL_EFFECTS,
            )
        receipt = _read_acquisition_receipt()
        if receipt is None or receipt["identity"] != _binary_identity(canonical):
            return RemovalPreview(
                "ambiguous",
                f"No matching acquisition receipt for {canonical}; use its original installation/removal mechanism.",
                canonical,
                remaining,
            )
        found = _inspect_executable(canonical, canonical=True)
        if found.state != "canonical":
            return RemovalPreview(
                "ambiguous",
                f"Canonical executable verification failed: {found.message}",
                canonical,
                remaining,
            )
        return RemovalPreview(
            "ready",
            f"Remove canonical {canonical} ({found.version}). " + REMOVAL_EFFECTS,
            canonical,
            remaining,
        )
    except (OSError, ValueError, RuntimeError) as exc:
        return RemovalPreview("ambiguous", f"Removal discovery failed: {exc}")


def uninstall_codebase_memory(
    *, scope: str = "user", confirmed: bool = False
) -> RemovalResult:
    """Run canonical upstream removal only; scoped registration is the caller's job."""
    if scope != "user":
        return RemovalResult(
            False, "scope", "Full native removal supports user scope only."
        )
    if not confirmed:
        return RemovalResult(
            False,
            "consent",
            "Explicit confirmation is required; no removal was performed.",
        )
    preview = preview_codebase_memory_removal()
    if preview.state == "missing":
        return RemovalResult(True, "absent", preview.message)
    if preview.state != "ready" or preview.executable is None:
        return RemovalResult(False, "discovery", preview.message, preview.remaining)
    executable = preview.executable
    try:
        # Revalidate proof immediately before handing the exact canonical path to upstream.
        receipt = _read_acquisition_receipt()
        if receipt is None or receipt["identity"] != _binary_identity(executable):
            return RemovalResult(
                False,
                "discovery",
                "Acquisition identity changed; no removal was performed.",
            )
        result = _run_bounded(
            [str(executable), "uninstall", "-y", f"--dir={executable.parent}"],
            INSTALL_TIMEOUT,
        )
        if result.returncode != 0:
            return RemovalResult(
                False,
                "uninstall",
                f"Upstream removal exited {result.returncode}; possible partial removal. Inspect upstream output and retry; no blind cleanup was attempted.",
            )
        try:
            executable.lstat()
        except FileNotFoundError:
            if _read_acquisition_receipt() != receipt:
                raise ValueError(
                    "Acquisition receipt changed; private proof was not cleared"
                )
            _receipt_path().unlink()  # Revoke only our verified private proof, not upstream assets.
            remaining = _alternate_path_entries()
            message = "Canonical native executable removed; indexes retained and adjacent updater left untouched."
            if remaining:
                message += (
                    " Alternate PATH entries remain: "
                    + ", ".join(map(str, remaining))
                    + "."
                )
            return RemovalResult(True, "verification", message, remaining)
        return RemovalResult(
            False,
            "verification",
            "Canonical executable still exists; possible partial removal. Inspect upstream output before retrying.",
        )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        return RemovalResult(
            False,
            "uninstall",
            f"Native removal failed: {exc}. Possible partial removal; inspect upstream output and retry. No blind cleanup was attempted.",
        )


def _signal_group(pid: int, sig: int) -> None:
    try:
        os.killpg(pid, sig)
    except ProcessLookupError:
        pass


def _supervise_native(argv: list[str], timeout: float) -> tuple[int, bool]:
    """Run ONLY in the dedicated helper, which owns no unrelated children.

    Linux adoption also covers double-forks/setsid. ECHILD, not an empty procfs
    snapshot, proves collection is complete. A finite, killable tree is required;
    an uninterruptible kernel task produces an explicit cleanup failure.
    """
    if sys.platform != "linux":
        raise OSError("Native supervision requires Linux")
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER, helper only
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    children_file = Path(f"/proc/self/task/{os.getpid()}/children")
    children_file.read_text()  # Fail before acquisition if procfs is unavailable.
    cancelled = False

    def cancel(signum, frame):
        nonlocal cancelled
        cancelled = True

    signal.signal(signal.SIGTERM, cancel)
    signal.signal(signal.SIGINT, cancel)
    process = subprocess.Popen(argv, shell=False, start_new_session=True)
    deadline = time.monotonic() + timeout
    terminating: float | None = None
    leader_code: int | None = None
    term_sent: set[int] = set()
    kill_sent: set[int] = set()
    while True:
        try:
            while True:
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    break
                if pid == process.pid:
                    leader_code = os.waitstatus_to_exitcode(status)
                    process.returncode = leader_code
        except ChildProcessError:
            if leader_code is None:
                raise subprocess.SubprocessError(
                    "Native leader status was not collected"
                )
            return leader_code, terminating is not None
        now = time.monotonic()
        if terminating is None and (cancelled or now >= deadline):
            terminating = now
            if leader_code is None:
                _signal_group(process.pid, signal.SIGTERM)
        if terminating is not None:
            force = now >= terminating + TERMINATE_GRACE
            if now >= terminating + TERMINATE_GRACE + REAP_TIMEOUT:
                raise subprocess.SubprocessError(
                    "Native descendant cleanup incomplete: kill/reap deadline exceeded"
                )
            if force and leader_code is None:
                _signal_group(process.pid, signal.SIGKILL)
            # Only our direct children are signalled. When a parent dies, its
            # descendants become ours; repeat until waitpid reports ECHILD.
            sent = kill_sent if force else term_sent
            for pid in map(int, children_file.read_text().split()):
                if pid not in sent:
                    try:
                        os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    sent.add(pid)
        time.sleep(0.01)


def _run_bounded(
    argv: list[str], timeout: float, *, capture_output: bool = False
) -> subprocess.CompletedProcess:
    """Isolate Linux adoption; never change the hosting CLI's child ownership."""
    cleanup_time = TERMINATE_GRACE + REAP_TIMEOUT + 2
    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as result_file:
        process = subprocess.Popen(
            [
                sys.executable,
                "-I",
                "-S",
                str(Path(__file__).resolve()),
                str(result_file.fileno()),
                str(timeout),
                *argv,
            ],
            shell=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
            errors="replace",
            start_new_session=True,
            pass_fds=(result_file.fileno(),),
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout + cleanup_time)
        except BaseException:
            # Request the helper's own bounded cleanup before reaping it.
            process.terminate()
            try:
                process.communicate(timeout=cleanup_time)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=REAP_TIMEOUT)
                raise subprocess.SubprocessError(
                    "Native supervisor stopped responding; descendant cleanup not confirmed"
                )
            raise
        result_file.seek(0)
        try:
            result = json.load(result_file)
        except (ValueError, OSError) as exc:
            raise subprocess.SubprocessError(
                "Native supervisor failed; descendant cleanup not confirmed"
            ) from exc
        if "error" in result:
            raise subprocess.SubprocessError(result["error"])
        if result["timed_out"]:
            raise subprocess.TimeoutExpired(argv, timeout, stdout, stderr)
        return subprocess.CompletedProcess(argv, result["returncode"], stdout, stderr)


def _inspect_executable(path: Path, *, canonical: bool) -> Discovery:
    """Refuse uncertain paths; do not infer package-manager or upstream ownership."""
    try:
        try:
            info = path.lstat()
        except FileNotFoundError:
            return Discovery("missing", path)
        if path.resolve() != path:
            return Discovery(
                "ambiguous", path, message=f"Symlinked executable/directory: {path}"
            )
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            return Discovery(
                "ambiguous", path, message=f"Not an unambiguous regular file: {path}"
            )
        if canonical and info.st_uid != os.getuid():
            return Discovery(
                "ambiguous",
                path,
                message=f"Canonical executable has a different owner: {path}",
            )
    except (OSError, RuntimeError) as exc:
        return Discovery(
            "ambiguous",
            path,
            message=f"Cannot establish executable identity for {path}: {exc}",
        )
    if not os.access(path, os.X_OK):
        return Discovery("non_runnable", path, message=f"Not executable: {path}")
    try:
        result = _run_bounded(
            [str(path), "--version"], VERSION_TIMEOUT, capture_output=True
        )
        version = (result.stdout or result.stderr or "").strip()
        if result.returncode != 0 or not version:
            return Discovery(
                "non_runnable",
                path,
                message=f"Version check failed for {path}: {result.stderr or result.stdout or 'empty output'}",
            )
        return Discovery("canonical" if canonical else "external", path, version)
    except (OSError, subprocess.SubprocessError) as exc:
        return Discovery(
            "non_runnable", path, message=f"Executable check failed for {path}: {exc}"
        )


def discover_executable() -> Discovery:
    """Prefer canonical, then the first usable PATH file; never modify anything.

    Symlinks/hardlinks and unknown canonical ownership fail closed. External
    files may be reused but are never candidates for automatic replacement.
    """
    canonical = None
    try:
        canonical = canonical_executable()
        for directory in (canonical.parent.parent, canonical.parent):
            if directory.resolve() != directory:
                return Discovery(
                    "ambiguous",
                    canonical,
                    message=f"Symlinked canonical directory: {directory}",
                )
            if directory.exists() and (
                not directory.is_dir() or directory.stat().st_uid != os.getuid()
            ):
                return Discovery(
                    "ambiguous",
                    canonical,
                    message=f"Canonical directory type/ownership is uncertain: {directory}",
                )
        found = _inspect_executable(canonical, canonical=True)
        if found.state in {"canonical", "ambiguous"}:
            return found
        unusable = None
        for path_entry in os.get_exec_path():
            candidate = Path(path_entry).absolute() / BINARY_NAME
            if candidate == canonical:
                continue
            external = _inspect_executable(candidate, canonical=False)
            if external.state in {"external", "ambiguous"}:
                return external
            if external.state == "non_runnable" and unusable is None:
                unusable = external
        return unusable or found
    except (OSError, RuntimeError) as exc:
        return Discovery("ambiguous", canonical, message=f"Discovery failed: {exc}")


def acquire_codebase_memory(*, scope: str = "user") -> AcquisitionResult:
    """Reuse an executable or run the complete official bootstrap once.

    The caller must check Claude CLI readiness and obtain installation consent.
    This function does not register MCP, index code, upgrade working binaries,
    or roll back upstream mutations. curl/Bash are acquisition-only prerequisites.
    """
    if scope != "user":
        return AcquisitionResult(
            False, "scope", "Full native setup supports user scope only."
        )
    system, arch = platform.system().lower(), platform.machine().lower()
    architectures = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }
    normalized_arch = architectures.get(arch)
    if system != "linux" or normalized_arch is None:
        return AcquisitionResult(
            False,
            "platform",
            f"Automated native setup supports Linux amd64/arm64, not {system}/{arch}. macOS/Windows require the official manual installer; Linux supervision is required for descendant cleanup.",
        )

    found = discover_executable()
    try:
        # A canonical binary left by our own interrupted run is re-acquired, not reused.
        pending = found.state == "canonical" and _acquisition_pending()
    except (OSError, ValueError) as exc:
        return AcquisitionResult(False, "discovery", str(exc), found.executable)
    if found.state == "external" or (found.state == "canonical" and not pending):
        return AcquisitionResult(
            True,
            "verification",
            f"Reusing {found.executable} ({found.version}).",
            found.executable,
            found.version,
        )
    if found.state == "ambiguous":
        return AcquisitionResult(False, "discovery", found.message, found.executable)
    canonical = canonical_executable()
    if found.state == "non_runnable" and found.executable != canonical:
        return AcquisitionResult(False, "discovery", found.message, found.executable)

    stage = "prerequisites"
    try:
        curl, bash = shutil.which("curl"), shutil.which("bash")
        if not curl or not bash:
            missing = ", ".join(
                name for name, value in (("curl", curl), ("bash", bash)) if not value
            )
            return AcquisitionResult(
                False, stage, f"Acquisition requires {missing}; install it and retry."
            )
        print(
            f"Acquiring full upstream setup from {INSTALL_URL}\nDestination: {canonical}\nUpstream configures detected clients and companion instructions, skills, agents and hooks; existing graph indexes are retained.",
            flush=True,
        )
        stage = "download"
        with tempfile.TemporaryDirectory(
            prefix="codebase-memory-install-"
        ) as directory:
            script = Path(directory) / "install.sh"
            result = _run_bounded(
                [
                    str(Path(curl).absolute()),
                    "--fail",
                    "--silent",
                    "--show-error",
                    "--location",
                    "--max-redirs",
                    "5",
                    "--proto",
                    "=https",
                    "--proto-redir",
                    "=https",
                    "--max-time",
                    str(DOWNLOAD_TIMEOUT),
                    "--output",
                    str(script),
                    INSTALL_URL,
                ],
                DOWNLOAD_TIMEOUT,
            )
            if (
                result.returncode != 0
                or not script.is_file()
                or script.stat().st_size == 0
            ):
                return AcquisitionResult(
                    False,
                    stage,
                    f"Bootstrap download failed or was empty (exit {result.returncode}); script was not executed.",
                )
            stage = "prerequisites"
            _mark_acquisition_pending()
            stage = "install"
            result = _run_bounded(
                [str(Path(bash).absolute()), str(script), f"--dir={canonical.parent}"],
                INSTALL_TIMEOUT,
            )
            if result.returncode != 0:
                return AcquisitionResult(
                    False,
                    stage,
                    f"Upstream install exited {result.returncode}; partial upstream changes may remain. Review its output and retry.",
                )
            stage = "verification"
            verified = _inspect_executable(canonical, canonical=True)
            if verified.state != "canonical":
                return AcquisitionResult(
                    False,
                    stage,
                    f"Upstream completed but executable verification failed: {verified.message or verified.state}. Partial upstream changes may remain.",
                    canonical,
                )
            stage = "provenance"
            _write_acquisition_receipt(canonical)
            _pending_path().unlink(missing_ok=True)
            stage = "verification"
            return AcquisitionResult(
                True,
                stage,
                f"Verified {verified.version} at {canonical}. Restart clients to load integrations; no indexing or MCP handshake was performed.",
                canonical,
                verified.version,
                True,
            )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        partial = (
            " Partial upstream changes may remain; review output and retry."
            if stage in {"install", "verification", "provenance"}
            else " Retry acquisition after resolving the error."
        )
        return AcquisitionResult(
            False, stage, f"{stage.capitalize()} failed: {exc}.{partial}"
        )


if __name__ == "__main__":
    # Private same-module helper entry; status FD never reaches the native tool.
    with os.fdopen(int(sys.argv[1]), "w", encoding="utf-8") as status_file:
        try:
            returncode, timed_out = _supervise_native(sys.argv[3:], float(sys.argv[2]))
            json.dump({"returncode": returncode, "timed_out": timed_out}, status_file)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            json.dump({"error": f"Native supervision failed: {error}"}, status_file)
