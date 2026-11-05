"""Retire step: remove stale MCP registrations IronClaude can prove it wrote.

Runs at the end of ``superclaude install`` and never changes its exit code.
Only user-scope registrations are touched, and only when their shape proves
IronClaude code wrote them (Tier R). A shape another writer could also have
produced (Coder's bundle, a hand-typed docs command) is kept and reported with
the exact removal command (Tier K). Binaries, uv tools, indexes, caches and
memories are never touched; IronClaude's own receipt and marker files are
deleted once the binary they describe is gone.
"""

from __future__ import annotations

import os
import shlex
import shutil
import stat
import time
from pathlib import Path
from typing import Callable, NamedTuple

import click

from . import install_mcp
from .install_mcp import _remove_exact_user_entry, read_user_mcp_servers

CBM_NAME = "codebase-memory-mcp"
SERENA_NAME = "serena"
# The one launcher name the codegraph-ready sweep never removes: the re-register hint's name.
SERENA_KEEP_NAME = "serena-local"
RECEIPT_NAME = ".superclaude-codebase-memory.json"
MARKER_NAME = ".superclaude-codebase-memory.pending"

PER_CALL_TIMEOUT = 10.0
STEP_CAP = 15.0

SERENA_PIN_ARGS = [
    "--from",
    "serena-agent==1.7.0",
    "serena",
    "start-mcp-server",
    "--context",
    "claude-code",
    "--project-from-cwd",
    "--enable-web-dashboard",
    "false",
    "--enable-gui-log-window",
    "false",
]
SERENA_REREGISTER = "claude mcp add --scope user serena-local -- uvx " + shlex.join(
    SERENA_PIN_ARGS
)

# Tier R: argv only IronClaude (or its pre-fork ancestor) ever wrote.
# (a) IronClaude registry 050d5ea2..0e7bc31f^; (b), (c) pre-fork setup/components/mcp.py.
_SERENA_TIER_R = {
    "a": (
        "uvx",
        [
            "--from",
            "git+https://github.com/oraios/serena",
            "serena",
            "start-mcp-server",
            "--context",
            "ide-assistant",
            "--enable-web-dashboard",
            "false",
            "--enable-gui-log-window",
            "false",
        ],
    ),
    "b": (
        "uvx",
        [
            "--from",
            "git+https://github.com/oraios/serena",
            "serena",
            "start-mcp-server",
            "--context",
            "ide-assistant",
            "--project",
            "$(pwd)",
        ],
    ),
    "c": (
        "serena",
        ["start-mcp-server", "--context", "ide-assistant", "--project", "$(pwd)"],
    ),
}

TIER_K_LINE = (
    "Legacy Serena registration kept until codegraph is ready (IronClaude cannot "
    "prove it wrote it; the next `superclaude install` that installs codegraph "
    "removes it). Remove it now with `claude mcp remove serena --scope user`."
)

RESTART_LINE = (
    "Restart running Claude sessions; a running session can write the entry back. "
    "Check with `superclaude install --list`."
)
CBM_COMPANION_LINE = (
    "If you installed codebase-memory-mcp yourself, its own `uninstall` removes "
    "its client companions."
)
CBM_UNINSTALL_LINE = (
    '"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"'
    "  # for a codebase-memory you or IronClaude installed under ~/.local/bin; "
    "removes its own client companions, keeps indexes"
)
SERENA_TOOL_LINE = (
    "uv tool uninstall serena-agent  # if you installed it yourself; "
    "Coder workspaces reinstall it at start"
)
DELETE_CBM_DATA_LINE = (
    "rm -rf ~/.cache/codebase-memory-mcp  # only if you no longer need the indexes"
)
DELETE_SERENA_DATA_LINE = (
    "rm -rf ~/.serena  # only if you no longer need Serena's memories "
    "(project .serena/ folders are yours to delete)"
)
UNKNOWN_CAUSE = (
    "could not read the user MCP configuration (empty CLAUDE_CONFIG_DIR, "
    "unreadable or unparseable file, duplicate key, or non-object value)"
)


class Finding(NamedTuple):
    """name, verdict (absent|remove|keep|list|unknown), reason."""

    name: str
    verdict: str
    reason: str


def _manual_remove(name: str) -> str:
    return f"claude mcp remove {name} --scope user"


def _canonical_cbm(home: Path) -> Path:
    return home / ".local" / "bin" / CBM_NAME


def _empty(value: object) -> bool:
    return value is None or value == {}


def _has_extra_config(entry: dict) -> bool:
    return any(key in entry and not _empty(entry[key]) for key in ("env", "headers"))


def _classify_cbm(entry: dict, home: Path, ready: bool = False) -> tuple[str, str]:
    command = entry.get("command")
    args = entry.get("args", [])
    if (
        not isinstance(command, str)
        or not os.path.isabs(command)
        or Path(command).name != CBM_NAME
        or entry.get("type", "stdio") != "stdio"
        or args != []
        or _has_extra_config(entry)
    ):
        return "keep", "not an IronClaude registration"
    canonical = _canonical_cbm(home)
    if command == str(canonical):
        if canonical.exists():
            if ready:
                return (
                    "remove",
                    "codegraph is ready: kind-B registration (binary and companions stay)",
                )
            return "keep", "upstream-installed binary still present"
        return "remove", "IronClaude shape, binary gone"
    if command.endswith("/.local/bin/" + CBM_NAME):
        return "keep", "path differs from current HOME"
    return "remove", "IronClaude shape"


def _classify_serena(entry: dict, home: Path, ready: bool = False) -> tuple[str, str]:
    command = entry.get("command")
    args = entry.get("args", [])
    if (
        entry.get("type", "stdio") != "stdio"
        or not isinstance(command, str)
        or not isinstance(args, list)
        or "start-mcp-server" not in [command, *args]
    ):
        return "keep", "not a Serena launcher registration"
    if _has_extra_config(entry):
        return "keep", "customised registration"
    for row, (row_command, row_args) in _SERENA_TIER_R.items():
        if command == row_command and args == row_args:
            return "remove", f"Tier R row ({row}): {shlex.join([command, *args])}"
    if ready:
        return "remove", f"codegraph is ready: {shlex.join([command, *args])}"
    return "keep", TIER_K_LINE


# Remove after the first release in which Coder's image and bundle no longer ship
# either server.
RETIRED_MCP_SERVERS: dict[str, Callable[[dict, Path, bool], tuple[str, str]]] = {
    CBM_NAME: _classify_cbm,
    SERENA_NAME: _classify_serena,
}


def _private_file_problem(path: Path) -> str | None:
    """None when ``path`` is a private regular file we own (and may delete)."""
    try:
        info = path.lstat()
    except FileNotFoundError:
        return None
    if (
        not stat.S_ISREG(info.st_mode)
        or info.st_uid != os.getuid()
        or info.st_nlink != 1
        or info.st_mode & 0o077
    ):
        return "not a private owned regular file"
    return None


def _install_directory_problem(home: Path) -> str | None:
    for directory in (home / ".local", home / ".local" / "bin"):
        try:
            if directory.resolve() != directory:
                return "symlinked directory"
            if directory.exists():
                info = directory.stat()
                if (
                    not stat.S_ISDIR(info.st_mode)
                    or info.st_uid != os.getuid()
                    or info.st_mode & 0o022
                ):
                    return "directory ownership or permissions are uncertain"
        except OSError:
            return "directory could not be inspected"
    return None


def _classify_file(path: Path, home: Path) -> Finding:
    if not os.path.lexists(path):
        return Finding(path.name, "absent", "")
    if os.path.lexists(_canonical_cbm(home)):
        return Finding(path.name, "keep", "binary still present")
    problem = _private_file_problem(path) or _install_directory_problem(home)
    if problem:
        return Finding(path.name, "list", problem)
    return Finding(path.name, "remove", "binary gone")


def _codegraph_ready_now() -> bool:
    """The one readiness predicate (``install_mcp.codegraph_ready``); False on any error."""
    try:
        return bool(install_mcp.codegraph_ready()[0])
    except Exception:
        return False


def classify_retired_entries(ready: bool = False) -> list[Finding]:
    """Read all state once; no writes. Order: receipt, marker, codebase-memory, serena.

    When ``ready`` (codegraph is registered and usable) the current-pin Serena entry,
    the kind-B codebase-memory registration and every renamed Serena launcher
    (any user entry other than ``serena-local``) are also verdict ``remove``.
    """
    home = Path.home().absolute()
    bin_dir = home / ".local" / "bin"
    findings = [
        _classify_file(bin_dir / RECEIPT_NAME, home),
        _classify_file(bin_dir / MARKER_NAME, home),
    ]
    known, servers = read_user_mcp_servers()
    classifiers = dict(RETIRED_MCP_SERVERS)
    if ready and known:
        for name, entry in servers.items():
            if (
                name not in classifiers
                and name != SERENA_KEEP_NAME
                and isinstance(entry, dict)
                and _classify_serena(entry, home, True)[0] == "remove"
            ):
                classifiers[name] = _classify_serena
    for name, classify in classifiers.items():
        if not known or (name in servers and not isinstance(servers[name], dict)):
            findings.append(Finding(name, "unknown", UNKNOWN_CAUSE))
        elif name not in servers:
            findings.append(Finding(name, "absent", ""))
        else:
            findings.append(Finding(name, *classify(servers[name], home, ready)))
    return findings


def list_lines() -> list[str]:
    """One line per retired name for ``superclaude install --list``."""
    lines = []
    for finding in classify_retired_entries(_codegraph_ready_now()):
        if finding.name in (RECEIPT_NAME, MARKER_NAME):
            continue
        if finding.verdict == "absent":
            status = "absent"
        elif finding.verdict == "remove":
            cause = (
                "codegraph is ready"
                if finding.reason.startswith("codegraph is ready")
                else "IronClaude shape"
            )
            status = f"will be removed ({cause})"
        elif finding.verdict == "unknown":
            status = "unknown (lookup failed; no repair attempted)"
        else:
            status = f"kept: {finding.reason}"
        lines.append(f"   {finding.name:22} {status}")
    return lines


def _removable(findings: list[Finding]) -> list[Finding]:
    return [f for f in findings if f.verdict == "remove"]


def update_notice() -> str | None:
    """The only thing ``superclaude update`` says about retired servers."""
    if _removable(classify_retired_entries(_codegraph_ready_now())):
        return "legacy registration present: run `superclaude install`"
    return None


def doctor_warning() -> str | None:
    """Warn-only text for ``superclaude doctor`` (never a failure)."""
    names = [
        f.name
        for f in _removable(classify_retired_entries(_codegraph_ready_now()))
        if f.name not in (RECEIPT_NAME, MARKER_NAME)
    ]
    if not names:
        return None
    return (
        "legacy registration present for "
        + ", ".join(names)
        + "; run `superclaude install` to retire it"
    )


def _delete_private_file(path: Path) -> str:
    """Delete one private file; re-check the identity right before unlinking."""
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        opened = os.fstat(descriptor)
        current = path.lstat()
        if (
            not stat.S_ISREG(opened.st_mode)
            or opened.st_uid != os.getuid()
            or opened.st_nlink != 1
            or opened.st_mode & 0o077
            or (opened.st_dev, opened.st_ino) != (current.st_dev, current.st_ino)
        ):
            return "list"
        path.unlink()
        return "deleted"
    finally:
        os.close(descriptor)


def _retire_files(findings: list[Finding], home: Path) -> bool:
    removed = False
    for finding in findings:
        if finding.name not in (RECEIPT_NAME, MARKER_NAME):
            continue
        path = home / ".local" / "bin" / finding.name
        if finding.verdict == "list":
            click.echo(f"   Left in place (not deleted): {path} ({finding.reason})")
        elif finding.verdict == "remove":
            try:
                outcome = _delete_private_file(path)
            except OSError as exc:
                click.echo(f"   ⚠️  Could not delete {path}: {type(exc).__name__}")
                continue
            if outcome == "deleted":
                click.echo(f"   Removed {path} (its binary is gone)")
                removed = True
            else:
                click.echo(f"   Left in place (not deleted): {path} (changed)")
    return removed


def run_retire_step(codegraph_ready: bool = False) -> dict[str, str]:
    """Retire stale registrations. Prints one line per action; returns name -> outcome.

    ``codegraph_ready`` is true only when the codegraph phase passed in this run and
    ``install_mcp.codegraph_ready()`` agrees; it widens removal to the Serena launchers
    and the kind-B codebase-memory registration (spec 2.12).
    Callers wrap this in ``try/except``: no outcome may change the install exit code.
    """
    home = Path.home().absolute()
    deadline = time.monotonic() + STEP_CAP
    findings = classify_retired_entries(codegraph_ready)
    outcomes: dict[str, str] = {}
    if all(f.verdict == "absent" for f in findings):
        click.echo("   No retired MCP registrations present.")
        return outcomes
    click.echo("   Retired MCP registrations (user scope only):")

    _retire_files(findings, home)

    removed_any = False
    removed_cbm = False
    removed_launchers: list[str] = []
    claude = shutil.which("claude")
    for finding in findings:
        name = finding.name
        if name in (RECEIPT_NAME, MARKER_NAME):
            continue
        if finding.verdict == "absent":
            outcomes[name] = "absent"
        elif finding.verdict == "unknown":
            click.echo(
                f"   ⚠️  {name}: {finding.reason}. Check it yourself: "
                f"`{_manual_remove(name)}` if it is a stale registration."
            )
            outcomes[name] = "unknown"
        elif finding.verdict == "keep":
            if finding.reason == TIER_K_LINE:
                click.echo(f"   {finding.reason}")
            else:
                click.echo(f"   {name}: kept: {finding.reason}")
            outcomes[name] = "kept"
        elif claude is None:
            click.echo(
                f"   {name}: `claude` CLI not found; remove it yourself with "
                f"`{_manual_remove(name)}`"
            )
            outcomes[name] = "skipped"
        else:
            classify = RETIRED_MCP_SERVERS.get(name, _classify_serena)
            status = _remove_exact_user_entry(
                name,
                lambda entry, _c=classify: (
                    _c(entry, home, codegraph_ready)[0] == "remove"
                ),
                deadline=deadline,
                per_call_timeout=PER_CALL_TIMEOUT,
            )
            outcomes[name] = status
            if status == "removed":
                click.echo(
                    f"   Removed the {name} user registration ({finding.reason})"
                )
                removed_any = True
                if name == CBM_NAME:
                    removed_cbm = True
                if name != CBM_NAME:
                    removed_launchers.append(finding.reason.split(": ", 1)[-1])
            elif status == "absent":
                click.echo(f"   {name}: already gone")
            elif status == "changed":
                click.echo(f"   {name}: kept (changed before removal; not retried)")
            elif status == "replaced":
                click.echo(f"   {name}: replaced concurrently, kept (not retried)")
            elif status == "skipped":
                click.echo(
                    f"   ⚠️  {name}: step time cap reached; the next install "
                    f"retries, or run `{_manual_remove(name)}`"
                )
            else:
                reason = {
                    "timeout": "claude did not answer in time",
                    "unverified": "could not verify the removal",
                    "unknown": UNKNOWN_CAUSE,
                }.get(status, "claude mcp remove failed")
                click.echo(
                    f"   ⚠️  {name}: {reason}. Check it and run "
                    f"`{_manual_remove(name)}` if it is still there."
                )

    if removed_any:
        click.echo(f"   {RESTART_LINE}")
    if removed_cbm:
        click.echo(f"   {CBM_COMPANION_LINE}")
    if removed_launchers:
        for argv in removed_launchers:
            click.echo(f"   Removed Serena registration: {argv}")
        click.echo(
            "   To keep using Serena, register it yourself under the name "
            f"`serena-local`, e.g. `{SERENA_REREGISTER}`"
        )

    touched = {f.name: f for f in findings if f.verdict != "absent"}
    if os.path.lexists(_canonical_cbm(home)):
        click.echo(f"   {CBM_UNINSTALL_LINE}")
    if CBM_NAME in touched or RECEIPT_NAME in touched or MARKER_NAME in touched:
        click.echo(f"   {DELETE_CBM_DATA_LINE}")
    if any(name not in (CBM_NAME, RECEIPT_NAME, MARKER_NAME) for name in touched):
        click.echo(f"   {SERENA_TOOL_LINE}")
        click.echo(f"   {DELETE_SERENA_DATA_LINE}")
    return outcomes
