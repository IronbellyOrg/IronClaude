"""Tmux integration — session management for detachable sprint execution.

v3.7 Wave 4 layout (F9):

    +----------------------------------+
    |                                  |
    |   TUI pane (:0.0, 50%)           |
    |                                  |
    +----------------------------------+
    |   Summary pane (:0.1, 25%)       |
    +----------------------------------+
    |   Tail pane (:0.2, 25%)          |
    +----------------------------------+

The summary pane hosts an idle shell so ``tmux send-keys`` can update it
with ``cat <results/phase-N-summary.md>`` whenever the background
:class:`~.summarizer.SummaryWorker` finishes a phase. The tail pane
follows the running phase's stream-json output file.

Compared to v3.6 (2-pane: TUI 75% / tail 25% at ``:0.1``), every
hardcoded ``:0.1`` reference for the tail pane moves to ``:0.2``.
"""

from __future__ import annotations

import hashlib
import os
import shlex
import shutil
import signal
import subprocess
import time
from pathlib import Path

import click

from .models import SprintConfig

# v3.7 Wave 4: canonical pane indices for the 3-pane layout.
TUI_PANE = "0.0"
SUMMARY_PANE = "0.1"
TAIL_PANE = "0.2"

# The initial prompt shown in the summary pane before any phase has
# completed. Kept short so it fits inside a 25%-height pane on narrow
# terminals.
_SUMMARY_PANE_PLACEHOLDER = "Phase summaries will appear here..."


def is_tmux_available() -> bool:
    """Check if tmux is installed and we are not already inside tmux."""
    if shutil.which("tmux") is None:
        return False
    # If TMUX env var is set, we are already inside a tmux session.
    return "TMUX" not in os.environ


def session_name(release_dir: Path) -> str:
    """Deterministic session name from release directory."""
    h = hashlib.sha1(str(release_dir.resolve()).encode()).hexdigest()[:8]
    return f"sc-sprint-{h}"


def find_running_session() -> str | None:
    """Find any running sc-sprint-* session."""
    if shutil.which("tmux") is None:
        return None
    result = subprocess.run(
        ["tmux", "list-sessions", "-F", "#{session_name}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    for line in result.stdout.strip().splitlines():
        if line.startswith("sc-sprint-"):
            return line
    return None


def launch_in_tmux(config: SprintConfig):
    """Create a tmux session and run the sprint inside it.

    The session is cleaned up on any setup failure to prevent stale sessions
    from blocking future sprint runs on the same release directory.
    """
    name = session_name(config.release_dir)
    config.tmux_session_name = name

    # Build the command that runs the sprint in foreground (--no-tmux)
    sprint_cmd = _build_foreground_command(config)

    # Create the session with the sprint as the main command
    subprocess.run(
        [
            "tmux",
            "new-session",
            "-d",  # detached
            "-s",
            name,  # session name
            "-x",
            "120",
            "-y",
            "40",  # default size
            *sprint_cmd,
        ],
        check=True,
    )

    # All post-creation setup — clean up session on any failure
    try:
        # v3.7 Wave 4 (F9): build the 3-pane layout by splitting twice.
        # Step 1: split :0.0 vertically at 50% → creates :0.1 (bottom 50%).
        # The new pane hosts an idle shell; the SummaryWorker will push
        # phase summaries into it via update_summary_pane().
        placeholder = shlex.quote(_SUMMARY_PANE_PLACEHOLDER)
        subprocess.run(
            [
                "tmux",
                "split-window",
                "-t",
                f"{name}:{TUI_PANE}",
                "-v",
                "-p",
                "50",  # bottom half is 50% of the session
                "bash",
                "-c",
                # Print placeholder, then drop into a plain prompt so
                # subsequent send-keys are read by a live shell.
                f"printf '%s\\n' {placeholder}; exec bash --noprofile --norc",
            ],
            check=True,
        )
        # Step 2: split :0.1 again at 50% → creates :0.2 (bottom 25% of
        # the session). Tails the first active phase's output file.
        if config.active_phases:
            output_file = config.output_file(config.active_phases[0])
            quoted = shlex.quote(str(output_file))
            subprocess.run(
                [
                    "tmux",
                    "split-window",
                    "-t",
                    f"{name}:{SUMMARY_PANE}",
                    "-v",
                    "-p",
                    "50",  # split the bottom 50% again → 25/25
                    "bash",
                    "-c",
                    f"touch {quoted} && tail -f {quoted}; read",
                ],
                check=True,
            )

        # Select the top pane (the TUI)
        subprocess.run(
            ["tmux", "select-pane", "-t", f"{name}:{TUI_PANE}"], check=True
        )
    except Exception:
        # Kill the partial session before re-raising
        subprocess.run(["tmux", "kill-session", "-t", name], check=False)
        raise

    # Attach — blocks until the user detaches or the session ends
    subprocess.run(["tmux", "attach-session", "-t", name])

    # Read the exit code written by execute_sprint() inside the tmux session
    sentinel = config.release_dir / ".sprint-exitcode"
    exit_code = 0
    try:
        exit_code = int(sentinel.read_text().strip())
    except (OSError, ValueError):
        pass  # session may have been killed externally; assume success
    if exit_code != 0:
        raise SystemExit(exit_code)


def _build_foreground_command(config: SprintConfig) -> list[str]:
    """Build the superclaude sprint run ... --no-tmux command."""
    cmd = [
        "superclaude",
        "sprint",
        "run",
        str(config.index_path),
        "--no-tmux",
        "--start",
        str(config.start_phase),
        "--max-turns",
        str(config.max_turns),
        "--permission-flag",
        config.permission_flag,
    ]
    if config.end_phase:
        cmd.extend(["--end", str(config.end_phase)])
    if config.model:
        cmd.extend(["--model", config.model])
    if config.tmux_session_name:
        cmd.extend(["--tmux-session-name", config.tmux_session_name])
    # Diagnostic flags
    if config.debug:
        cmd.append("--debug")
    if config.stall_timeout > 0:
        cmd.extend(["--stall-timeout", str(config.stall_timeout)])
    if config.stall_action != "warn":
        cmd.extend(["--stall-action", config.stall_action])
    return cmd


def update_tail_pane(tmux_session_name: str, output_file: Path):
    """Switch the tail pane (``:0.2``) to follow a different output file.

    v3.7 Wave 4: the tail pane moved from ``:0.1`` to ``:0.2`` because
    ``:0.1`` is now reserved for phase summaries. Callers that touched
    the raw index must go through this function (or use
    :data:`TAIL_PANE`).
    """
    target = f"{tmux_session_name}:{TAIL_PANE}"
    subprocess.run(
        ["tmux", "send-keys", "-t", target, "C-c"],  # kill the prior tail
        check=False,
    )
    quoted = shlex.quote(str(output_file))
    subprocess.run(
        ["tmux", "send-keys", "-t", target, f"tail -f {quoted}\n"],
        check=False,
    )


def update_summary_pane(tmux_session_name: str, summary_file: Path) -> None:
    """Refresh the summary pane (``:0.1``) with the contents of *summary_file*.

    Called by the executor whenever :class:`~.summarizer.SummaryWorker`
    finishes writing a ``results/phase-N-summary.md``. Sends ``clear``
    followed by a ``cat`` of the file so the pane shows only the latest
    phase summary. Missing files are a no-op so the pane keeps showing
    its placeholder.

    Failures from tmux (session gone, pane gone, binary missing) are
    swallowed: a stale TUI must never affect sprint execution.
    """
    if not summary_file.exists():
        return
    target = f"{tmux_session_name}:{SUMMARY_PANE}"
    quoted = shlex.quote(str(summary_file))
    subprocess.run(
        ["tmux", "send-keys", "-t", target, f"clear && cat {quoted}\n"],
        check=False,
    )


def attach_to_sprint():
    """Attach to a running sprint session."""
    name = find_running_session()
    if name is None:
        click.echo("No running sprint session found.")
        raise SystemExit(1)
    subprocess.run(["tmux", "attach-session", "-t", name])


def kill_sprint(force: bool = False):
    """Kill a running sprint session."""
    name = find_running_session()
    if name is None:
        click.echo("No running sprint session found.")
        raise SystemExit(1)
    if force:
        subprocess.run(["tmux", "kill-session", "-t", name])
    else:
        # Non-force escalation: SIGTERM -> wait -> SIGKILL via pane PID.
        pane_pid_result = subprocess.run(
            ["tmux", "display-message", "-p", "-t", f"{name}:0.0", "#{pane_pid}"],
            capture_output=True,
            text=True,
            check=False,
        )
        pane_pid = (
            int(pane_pid_result.stdout.strip())
            if pane_pid_result.returncode == 0
            and pane_pid_result.stdout.strip().isdigit()
            else None
        )

        if pane_pid is not None:
            try:
                os.kill(pane_pid, signal.SIGTERM)
                click.echo(
                    f"Sent SIGTERM to {name} pane pid {pane_pid}. Waiting 10s..."
                )
            except ProcessLookupError:
                click.echo(
                    f"Sprint process already exited for {name}. Cleaning session..."
                )
        else:
            # Fallback when pane pid is unavailable
            subprocess.run(
                ["tmux", "send-keys", "-t", f"{name}:0.0", "C-c"], check=False
            )
            click.echo(
                f"Sent interrupt to {name}. Waiting 10s for graceful shutdown..."
            )

        time.sleep(10)

        has_session = (
            subprocess.run(
                ["tmux", "has-session", "-t", name],
                check=False,
                capture_output=True,
                text=True,
            ).returncode
            == 0
        )
        if has_session:
            if pane_pid is not None:
                try:
                    os.kill(pane_pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            subprocess.run(["tmux", "kill-session", "-t", name], check=False)
