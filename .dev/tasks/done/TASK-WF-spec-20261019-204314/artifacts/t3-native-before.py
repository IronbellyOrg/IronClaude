"""Bounded full upstream acquisition, independent of MCP registration.

A canonical location is not proof of upstream ownership. Discovery is suitable
for reuse/preview, not authorization to uninstall an arbitrary executable.
"""

import ctypes
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
    if found.state in {"canonical", "external"}:
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
            return AcquisitionResult(
                True,
                stage,
                f"Verified {verified.version} at {canonical}. Restart clients to load integrations; no indexing or MCP handshake was performed.",
                canonical,
                verified.version,
                True,
            )
    except (OSError, subprocess.SubprocessError) as exc:
        partial = (
            " Partial upstream changes may remain; review output and retry."
            if stage in {"install", "verification"}
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
