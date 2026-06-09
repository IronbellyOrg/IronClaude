"""Reflect-wrapper CLI surface -- the ``superclaude reflect run`` command group.

Exposes the thin fail-closed POST reflect gate as a Click subcommand. Options
match the spec Section 9 in-scope set exactly. Heavy imports (config/runner)
are lazy inside the command body (house convention). Exit codes are wired to
``Verdict.exit_code`` (pass 0 / halted 10 / degraded 11 / blocked 2) -- never
hardcoded a second time.

The ``--tmux`` opt-in reuses the sprint detached-window + sentinel idiom but
INVERTS its fail-open posture: a missing/garbage ``.reflect-exitcode`` sentinel
is treated as ``blocked`` (exit 2), never success. The ``is_tmux_available`` /
session-name helpers are copied locally (no cross-subcommand-package import).
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import click

# Top-level orchestrator model for the headless ``claude --print`` run. The
# spec Section 9 option set is exact (no ``--model`` flag), so the model is
# sourced from the ``ANTHROPIC_MODEL`` env var with a default fallback; the
# Tier-2 reviewer diversity comes from the ``ANTHROPIC_DEFAULT_*`` aliases, not
# this value. (Flagged decision -- see Task Log.)
_DEFAULT_MODEL = "claude-opus-4-8"

_TMUX_SESSION_PREFIX = "sc-reflect-"
_EXIT_SENTINEL_NAME = ".reflect-exitcode"
# Fail-closed exit code for a missing/unreadable sentinel (Verdict.BLOCKED).
_BLOCKED_EXIT = 2


@click.group("reflect")
def reflect_group():
    """Run the post-execution reflect gate as a top-level subprocess.

    Launches ``/sc:reflect --mode post`` as a top-level ``claude --print``
    subprocess (so Tier 2 fans out), parses ``return-contract.yaml``, derives a
    fail-closed 4-state verdict, and writes a ``reflect_post:`` block back into
    the tasklist frontmatter. Only a clean, full, non-degraded Tier-2 pass
    exits 0.

    Examples:
        superclaude reflect run path/to/TASK.md
        superclaude reflect run path/to/TASK.md --tmux
        superclaude reflect run path/to/TASK.md --depth deep --print-command
    """
    pass


@reflect_group.command()
@click.argument(
    "tasklist",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
@click.option(
    "--tmux", is_flag=True, help="Run inside a detached tmux window to watch live."
)
@click.option(
    "--print-command",
    is_flag=True,
    help="Print the composed claude argv + prompt and exit without launching.",
)
@click.option(
    "--promote/--no-promote",
    "promote",
    default=False,
    help="Allow reflect's gated Wave-7 promotion (default: --no-promote, audit-only).",
)
@click.option(
    "--timeout",
    type=int,
    default=None,
    help="Subprocess timeout seconds (default 3600).",
)
@click.option(
    "--depth",
    type=click.Choice(["standard", "deep"], case_sensitive=False),
    default="standard",
    help="Reflect depth passthrough (POST never runs quick).",
)
@click.option(
    "--output",
    default=None,
    help="Pinned output dir (default <task-dir>/reflect/post/<sha>/).",
)
@click.option(
    "--allow-single-vendor",
    is_flag=True,
    help="Do not HALT on single-vendor Tier-2 diversity.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Derive + preflight + construct command, but do not launch or edit the task file.",
)
@click.option(
    "--resume",
    is_flag=True,
    help="Skip the launch when the prior reflect_post is a pass on the current HEAD.",
)
def run(
    tasklist: str,
    tmux: bool,
    print_command: bool,
    promote: bool,
    timeout: int | None,
    depth: str,
    output: str | None,
    allow_single_vendor: bool,
    dry_run: bool,
    resume: bool,
) -> None:
    """Execute the POST reflect gate for TASKLIST.

    TASKLIST is the absolute path to the MDTM task file whose ``reflect_post:``
    frontmatter block this command writes back. The process exit code is the
    fail-closed verdict code (pass 0 / halted 10 / degraded 11 / blocked 2).
    """
    from .config import resolve_config
    from .runner import ReflectRunner

    model = os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL

    try:
        config = resolve_config(
            tasklist,
            depth=depth,
            output_dir=output,
            model=model,
            timeout=timeout,
            promote=promote,
            allow_single_vendor=allow_single_vendor,
            tmux=tmux,
            dry_run=dry_run,
            print_command=print_command,
            resume=resume,
        )
    except ValueError as exc:
        # A config / preflight STOP is blocked -> exit 2 (Section 6).
        click.echo(f"Error: {exc}", err=True)
        # F4 (FR-7: a sidecar ALWAYS records the verdict whenever an output dir is
        # reservable). A config-STOP short-circuits before the runner exists, so
        # the runner's own always-write sidecar never fires. Resolve the output
        # dir from the explicit --output (no cleanly reusable default-dir helper
        # exists without re-running the failing resolve_config, so the default
        # <task-dir>/reflect/post/<sha> case is an accepted skip). Sidecar-write
        # failure must never mask the original config error.
        if output:
            from .models import ReflectResult, Verdict
            from .runner import write_sidecar

            try:
                output_path = Path(output).resolve()
                output_path.mkdir(parents=True, exist_ok=True)
                blocked = ReflectResult(
                    verdict=Verdict.BLOCKED,
                    status=None,
                    tier_reached=None,
                    reason="config-error",
                    report_path=None,
                    contract_path=None,
                    deviations={},
                    child_exit_code=None,
                    write_status="not-attempted",
                )
                write_sidecar(
                    output_path,
                    blocked,
                    env_alias_count=0,
                    write_status="not-attempted",
                )
            except OSError:
                pass
        sys.exit(_BLOCKED_EXIT)

    # --tmux opt-in: delegate to the detached-window mechanic (fail-closed).
    if config.tmux and _is_tmux_available():
        sys.exit(_launch_tmux(config))

    # Foreground (default / inner --no-tmux reinvocation) path.
    result = ReflectRunner(config).run()
    exit_code = result.verdict.exit_code

    # Write the .reflect-exitcode sentinel for the tmux outer reader (skip the
    # no-launch dry-run/print path so it leaves no output-dir artifacts).
    if not (config.dry_run or config.print_command):
        _write_exit_sentinel(config.output_dir, exit_code)

    if exit_code != 0:
        click.echo(f"reflect: {result.verdict.value} ({result.reason})", err=True)
        if result.report_path:
            click.echo(f"  report: {result.report_path}", err=True)
        if result.contract_path:
            click.echo(f"  contract: {result.contract_path}", err=True)

    sys.exit(exit_code)


# ---------------------------------------------------------------------------
# --tmux window mechanic (copied idiom; fail-open -> fail-closed inversion)
# ---------------------------------------------------------------------------


def _is_tmux_available() -> bool:
    """True if tmux is installed and we are not already inside a tmux session."""
    if shutil.which("tmux") is None:
        return False
    return "TMUX" not in os.environ


def _session_name(output_dir: Path) -> str:
    """Deterministic ``sc-reflect-<8hex>`` session name from the pinned output dir."""
    h = hashlib.sha1(str(output_dir.resolve()).encode()).hexdigest()[:8]
    return f"{_TMUX_SESSION_PREFIX}{h}"


def _write_exit_sentinel(output_dir: Path, exit_code: int) -> None:
    """Write ``.reflect-exitcode`` into the pinned output dir (best-effort)."""
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / _EXIT_SENTINEL_NAME).write_text(str(exit_code), encoding="utf-8")
    except OSError:
        pass


def _build_inner_command(config) -> list[str]:
    """Build the inner foreground ``reflect run`` argv (no --tmux, same output)."""
    cmd = [
        "superclaude",
        "reflect",
        "run",
        str(config.tasklist_path),
        # Forward the SAME pinned --output so the inner writer and outer reader
        # agree on the .reflect-exitcode path (the sprint desync footgun).
        "--output",
        str(config.output_dir),
        "--depth",
        config.depth,
        "--timeout",
        str(config.timeout_seconds),
    ]
    if config.promote:
        cmd.append("--promote")
    if config.allow_single_vendor:
        cmd.append("--allow-single-vendor")
    if config.resume:
        cmd.append("--resume")
    return cmd


def _launch_tmux(config) -> int:
    """Run the wrapper inside a detached single tmux window; return its exit code.

    Reuses the sprint ``new-session -d`` + ``attach`` + sentinel-readback shape
    (ONE window only -- no 3-pane TUI). Inverts the sprint fail-open posture:
    a missing/garbage ``.reflect-exitcode`` is ``blocked`` (exit 2), not success.
    """
    name = _session_name(config.output_dir)
    inner = _build_inner_command(config)
    subprocess.run(
        ["tmux", "new-session", "-d", "-s", name, "-x", "120", "-y", "40", *inner],
        check=True,
    )
    try:
        subprocess.run(["tmux", "attach-session", "-t", name])
    except Exception:
        subprocess.run(["tmux", "kill-session", "-t", name], check=False)
        raise

    sentinel = config.output_dir / _EXIT_SENTINEL_NAME
    try:
        return int(sentinel.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        # Fail-closed inversion: no readable sentinel -> blocked, never success.
        return _BLOCKED_EXIT
