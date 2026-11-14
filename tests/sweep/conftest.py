"""Shared fixtures for the ``superclaude sweep`` test suite (DESIGN section 11).

Every test runs with the seams patched; none starts Orca, ccsession or Claude
(NFR-013). The autouse guard blocks ``subprocess.run``, ``subprocess.Popen`` and
``os.system`` unless the test function itself carries the ``integration`` marker.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture(autouse=True)
def no_subprocess(request, monkeypatch):
    """Raise AssertionError on any process start, except for an ``integration`` test.

    Only the test function's own decorator marks are read. The superclaude pytest
    plugin adds ``integration`` to every test whose path contains ``/integration/``,
    so ``request.node``'s closest-marker lookup would let those tests through.
    """
    marks = getattr(request.function, "pytestmark", [])  # own decorator marks only
    if any(m.name == "integration" for m in marks):
        return

    def _blocked(*args, **kwargs):
        raise AssertionError(
            "sweep tests must not start a process (subprocess.run, subprocess.Popen, "
            "os.system); patch the probes seam instead"
        )

    monkeypatch.setattr(subprocess, "run", _blocked)
    monkeypatch.setattr(subprocess, "Popen", _blocked)
    monkeypatch.setattr(os, "system", _blocked)


@dataclass
class GitFake:
    """Recording fake for ``probes._git``.

    ``calls`` holds one dict per call: ``cwd``, ``args``, ``timeout``, the ``argv`` and
    the ``env`` that the real ``_git`` would build. ``responses`` maps a worktree path
    (``str``) to canned porcelain output (``str`` or ``bytes``) or to an exception
    instance that is raised for that worktree (for example ``GitCallFailed``).

    The read-only inspection calls (``config``, ``ls-files``, ``check-attr``) that decide
    whether a git filter could run are recorded in ``precheck_calls``, not ``calls``, so
    ``calls`` still holds one status call per worktree. They answer empty output unless
    ``responses`` holds an entry for the key ``(str(cwd), <verb>)`` (``respond_inspect``).
    """

    calls: list[dict] = field(default_factory=list)
    precheck_calls: list[dict] = field(default_factory=list)
    responses: dict[object, object] = field(default_factory=dict)
    default: object = ""

    def respond(self, cwd: Path | str, output: object) -> None:
        self.responses[str(cwd)] = output

    def respond_inspect(self, cwd: Path | str, verb: str, output: object) -> None:
        self.responses[(str(cwd), verb)] = output

    def __call__(self, cwd, *args, timeout=10.0, stdin=None, binary=False):
        from superclaude.cli.sweep import probes

        probes.check_git_args(args)  # the real seam rejects anything else first
        record = {
            "cwd": Path(cwd),
            "args": tuple(args),
            "timeout": timeout,
            "stdin": stdin,
            "argv": [
                "git",
                "--no-optional-locks",
                "-C",
                str(cwd),
                "-c",
                "core.fsmonitor=false",
                *args,
            ],
            "env": {**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        }
        if args[0] == "status":
            self.calls.append(record)
            out = self.responses.get(str(cwd), self.default)
        else:
            self.precheck_calls.append(record)
            out = self.responses.get((str(cwd), args[0]), b"")
        if isinstance(out, BaseException):
            raise out
        if binary:
            return out.encode() if isinstance(out, str) else out
        return out.decode("utf-8", "replace") if isinstance(out, bytes) else out


@pytest.fixture
def patch_git(monkeypatch) -> GitFake:
    """Replace ``probes._git`` with a recording fake that returns canned porcelain."""
    from superclaude.cli.sweep import probes

    fake = GitFake()
    monkeypatch.setattr(probes, "_git", fake)
    return fake


@dataclass
class OrcaFake:
    """Recording fake for ``probes._orca``.

    ``calls`` holds one dict per call (``args`` and ``timeout``). ``responses`` maps an
    argv tuple (the arguments after the binary) to canned data. The returned object is
    ``probes.OrcaResult`` once item 8.10 defines it, else a namespace with the same
    ``kind``, ``data`` and ``reason`` attributes.
    """

    calls: list[dict] = field(default_factory=list)
    responses: dict[tuple[str, ...], tuple[str, object, str | None]] = field(
        default_factory=dict
    )

    def respond(
        self,
        args: tuple[str, ...],
        data: object = None,
        kind: str = "ok",
        reason: str | None = None,
    ) -> None:
        self.responses[tuple(args)] = (kind, data, reason)

    def __call__(self, *args, timeout=10.0):
        from superclaude.cli.sweep import probes

        check = getattr(probes, "check_orca_argv", None)
        if check is not None:  # added by item 8.10; the real seam checks first
            check(tuple(args))
        self.calls.append({"args": tuple(args), "timeout": timeout})
        kind, data, reason = self.responses.get(
            tuple(args), ("call_failed", None, "no canned response")
        )
        factory = getattr(probes, "OrcaResult", None) or SimpleNamespace
        return factory(kind=kind, data=data, reason=reason)


@pytest.fixture
def patch_orca(monkeypatch) -> OrcaFake:
    """Replace ``probes._orca`` with a recording fake (``_orca`` exists from item 8.10)."""
    from superclaude.cli.sweep import probes

    fake = OrcaFake()
    monkeypatch.setattr(probes, "_orca", fake)
    return fake


@pytest.fixture
def fixed_now() -> datetime:
    """A fixed, timezone-aware UTC clock value; tests never read the real clock."""
    return datetime(2026, 11, 8, 12, 0, 0, tzinfo=timezone.utc)


@dataclass(frozen=True)
class SweepHome:
    home: Path
    state: Path


@pytest.fixture
def sweep_home(tmp_path, monkeypatch) -> SweepHome:
    """Move ``HOME`` and ``XDG_STATE_HOME`` inside ``tmp_path``."""
    home = tmp_path / "home"
    state = home / ".local" / "state"
    state.mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_STATE_HOME", str(state))
    return SweepHome(home=home, state=state)


_ISO = "%Y-%m-%dT%H:%M:%S.%f"


def _iso(value: datetime | str) -> str:
    """A transcript record time: strings pass through, datetimes become ISO 8601 UTC."""
    if isinstance(value, str):
        return value
    return value.astimezone(timezone.utc).strftime(_ISO)[:-3] + "Z"


@dataclass
class SweepRoot:
    """A ``tmp_path`` layout for the disk sources (DESIGN section 11).

    ``root`` is a checkout stand-in (an empty ``.git`` folder, so the root check passes;
    git itself is never run). ``home`` and ``state`` are ``sweep_home``'s ``HOME`` and
    ``XDG_STATE_HOME``. Every builder writes real files and returns the path it wrote,
    so a test can then break the file (truncate it, make it a symlink, chmod it).
    A malformed or boundary variant is built by the caller through ``text``, ``raw`` or
    ``lines``; none of those is ever a file under ``tests/sweep/fixtures/``.
    """

    root: Path
    home: Path
    state: Path
    base: Path

    @property
    def tabs(self) -> Path:
        """The ccsession ``orca-tabs/`` folder (not created until an entry is added)."""
        return self.state / "ccsession" / "orca-tabs"

    def worktree(self, name: str) -> Path:
        """A second checkout stand-in beside the root (a ``.git`` file, as in a worktree)."""
        path = self.base / "worktrees" / name
        path.mkdir(parents=True, exist_ok=True)
        (path / ".git").write_text("gitdir: /nonexistent\n", encoding="utf-8")
        return path

    def package(
        self,
        name: str,
        *,
        worktree: Path | None = None,
        location: str = "to-do",
        ledger: str | bytes | None = "",
        final: bool = False,
        archiving: bool = False,
    ) -> Path:
        """``.dev/tasks/<location>/<name>/`` with a ``progress.md`` ledger.

        ``ledger`` is the ledger text or bytes (None writes no ledger file); ``final`` appends
        a ``FINAL:`` line to text; ``archiving`` adds the ``.archiving`` marker file.
        """
        folder = (worktree or self.root) / ".dev" / "tasks" / location / name
        folder.mkdir(parents=True, exist_ok=True)
        if ledger is not None:
            if isinstance(ledger, bytes):
                (folder / "progress.md").write_bytes(ledger)
            else:
                text = ledger + ("FINAL: all tasks complete\n" if final else "")
                (folder / "progress.md").write_text(text, encoding="utf-8")
        if archiving:
            (folder / ".archiving").write_text("", encoding="utf-8")
        return folder

    def contract(
        self,
        report_dir: Path | str = "reports/run",
        *,
        worker_status: str | None = "succeeded",
        command: str | None = None,
        report_path: str | None = None,
        artifacts: tuple[str, ...] = (),
        blocked_question: str | None = None,
        reason: str | None = None,
        text: str | bytes | None = None,
        worktree: Path | None = None,
    ) -> Path:
        """``<report_dir>/return-contract.yaml``; a relative ``report_dir`` is under ``.dev/``.

        ``text`` replaces the whole body (use it for malformed or oversize contracts).
        """
        folder = Path(report_dir)
        if not folder.is_absolute():
            folder = (worktree or self.root) / ".dev" / folder
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "return-contract.yaml"
        if isinstance(text, bytes):
            path.write_bytes(text)
            return path
        if text is None:
            lines = ['worker_contract_version: "1"']
            for key, value in (
                ("worker_status", worker_status),
                ("command", command),
                ("report_path", report_path),
                ("blocked_question", blocked_question),
                ("reason", reason),
            ):
                if value is not None:
                    lines.append(f"{key}: {json.dumps(value)}")
            if artifacts:
                lines.append("artifacts:")
                lines.extend(f"  - {json.dumps(a)}" for a in artifacts)
            text = "\n".join(lines) + "\n"
        path.write_text(text, encoding="utf-8")
        return path

    def transcript(
        self,
        session_id: str = "session-0001",
        stamps: tuple[datetime | str, ...] = (),
        *,
        worktree: Path | None = None,
        name: str | None = None,
        raw: bytes | None = None,
        mtime: datetime | None = None,
    ) -> Path:
        """``~/.claude/projects/<key>/<name>.jsonl`` with one record per stamp.

        ``<key>`` is the worktree path with every non-alphanumeric character as ``-``. Each
        record carries ``timestamp`` and ``sessionId``. ``raw`` replaces the whole file
        (a cut last line, a record without a timestamp, a file over a byte limit);
        ``mtime`` sets the file time.
        """
        key = re.sub(r"[^A-Za-z0-9]", "-", str(worktree or self.root))
        folder = self.home / ".claude" / "projects" / key
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{name or session_id}.jsonl"
        if raw is None:
            records = [
                json.dumps(
                    {"type": "user", "timestamp": _iso(s), "sessionId": session_id}
                )
                for s in stamps
            ]
            raw = ("\n".join(records) + "\n" if records else "").encode("utf-8")
        path.write_bytes(raw)
        if mtime is not None:
            stamp = mtime.timestamp()
            os.utime(path, (stamp, stamp))
        return path

    def tab_entry(
        self,
        pane_key: str,
        session_id: str,
        folder: Path | str,
        handle: str,
        *,
        lines: tuple[str, ...] | None = None,
    ) -> Path:
        """One ``orca-tabs/<pane_key>`` file: session id, launch folder, terminal handle.

        ``pane_key`` is ``<tabId>+<leafId>`` (the captured shape). ``lines`` replaces the
        three lines (a short or blank entry).
        """
        self.tabs.mkdir(parents=True, exist_ok=True)
        path = self.tabs / pane_key
        body = lines if lines is not None else (session_id, str(folder), handle)
        path.write_text("\n".join(body) + "\n", encoding="utf-8")
        return path


@pytest.fixture
def sweep_root(tmp_path, sweep_home) -> SweepRoot:
    """A checkout stand-in under ``tmp_path`` plus builders for the disk sources."""
    root = tmp_path / "root"
    (root / ".git").mkdir(parents=True)
    return SweepRoot(
        root=root, home=sweep_home.home, state=sweep_home.state, base=tmp_path
    )
