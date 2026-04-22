"""Sprint CLI commands — Click command group and subcommands.

Defines the ``superclaude sprint`` command group with five subcommands:
run, attach, status, logs, kill.
"""

from __future__ import annotations

import os
from pathlib import Path

import click


@click.group("sprint")
def sprint_group():
    """Orchestrate multi-phase Claude Code sprint execution.

    Reads a tasklist-index.md, discovers phase files, and executes
    each phase as a fresh Claude Code session with strict compliance.
    Supports tmux for detachable long-running sprints.

    Examples:
        superclaude sprint run path/to/tasklist-index.md
        superclaude sprint run path/to/tasklist-index.md --start 3 --end 6
        superclaude sprint run path/to/tasklist-index.md --dry-run
        superclaude sprint attach
        superclaude sprint status
        superclaude sprint logs
        superclaude sprint kill
    """
    pass


def _check_fidelity(index_path: Path) -> tuple[bool, str]:
    """Check sprint dir for spec-fidelity fail state.

    Returns (blocked, message). blocked=True means execution should be blocked.
    """
    import json as _json

    from .config import _resolve_release_dir

    sprint_dir = _resolve_release_dir(index_path)
    state_file = sprint_dir / ".roadmap-state.json"
    if not state_file.exists():
        return False, ""
    try:
        state = _json.loads(state_file.read_text())
    except (ValueError, OSError):
        return False, ""
    if state.get("fidelity_status") != "fail":
        return False, ""
    deviations_summary = ""
    fidelity_output = state.get("steps", {}).get("spec-fidelity", {}).get("output_file")
    if fidelity_output:
        fidelity_file = Path(fidelity_output)
        if fidelity_file.exists():
            lines = fidelity_file.read_text(errors="replace").splitlines()
            high_lines = [ln for ln in lines if "HIGH" in ln or "### DEV-" in ln][:20]
            deviations_summary = "\n".join(high_lines)
    msg = (
        f"Sprint blocked: spec-fidelity check FAILED.\n"
        f"The tasklist was generated from a spec with unresolved HIGH severity deviations:\n"
        f"{deviations_summary or '(see spec-fidelity.md for details)'}\n\n"
        f"To override: add --force-fidelity-fail '<justification>' to your command."
    )
    return True, msg


@sprint_group.command()
@click.argument("index_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--start",
    "start_phase",
    type=int,
    default=1,
    help="Start from phase N (default: 1)",
)
@click.option(
    "--end",
    "end_phase",
    type=int,
    default=0,
    help="End at phase N (default: last discovered)",
)
@click.option(
    "--max-turns",
    type=int,
    default=100,
    help="Max agent turns per phase (default: 100)",
)
@click.option(
    "--model",
    default="",
    help="Claude model to use (default: env CLAUDE_MODEL or claude default)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show discovered phases without executing",
)
@click.option(
    "--no-tmux",
    is_flag=True,
    help="Run in foreground even if tmux is available",
)
@click.option(
    "--permission-flag",
    type=click.Choice(
        [
            "--dangerously-skip-permissions",
            "--allow-hierarchical-permissions",
        ]
    ),
    default="--dangerously-skip-permissions",
    help="Permission flag for claude CLI",
)
@click.option(
    "--tmux-session-name",
    default="",
    hidden=True,
    help="Internal: tmux session name for tail pane updates (set by launch_in_tmux)",
)
@click.option(
    "--debug",
    "debug_mode",
    is_flag=True,
    default=False,
    help="Enable debug logging to results/debug.log",
)
@click.option(
    "--stall-timeout",
    type=int,
    default=0,
    help="Stall timeout in seconds (0 = disabled, default: 0)",
)
@click.option(
    "--stall-action",
    type=click.Choice(["warn", "kill"]),
    default="warn",
    help="Action on stall detection (default: warn)",
)
@click.option(
    "--shadow-gates",
    is_flag=True,
    default=False,
    help="Enable shadow mode: trailing gates run in parallel, results are metrics-only",
)
@click.option(
    "--force-fidelity-fail",
    "force_fidelity_fail",
    default="",
    metavar="JUSTIFICATION",
    help=(
        "Override fidelity block with a justification string, "
        "e.g. --force-fidelity-fail 'reason here'. "
        "Use --force-fidelity to override without a justification."
    ),
)
@click.option(
    "--force-fidelity",
    "force_fidelity_fail",
    flag_value="no justification provided",
    help="Override fidelity block without providing a justification string.",
)
@click.option(
    "--release-dir",
    "release_dir_override",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=None,
    help="Explicit release directory (overrides auto-detection from index path).",
)
def run(
    index_path: Path,
    start_phase: int,
    end_phase: int,
    max_turns: int,
    model: str,
    dry_run: bool,
    no_tmux: bool,
    permission_flag: str,
    tmux_session_name: str,
    debug_mode: bool,
    stall_timeout: int,
    stall_action: str,
    shadow_gates: bool,
    force_fidelity_fail: str,
    release_dir_override: Path | None,
):
    """Execute a sprint from a tasklist index.

    INDEX_PATH is the path to a tasklist-index.md file.

    Discovers phase files, validates they exist, then executes each
    phase sequentially in fresh Claude Code sessions. Results are
    written to a results/ directory alongside the index.

    By default, starts a tmux session so the sprint survives SSH
    disconnects. Use --no-tmux to run in the foreground.
    """
    from .config import load_sprint_config
    from .executor import execute_sprint
    from .tmux import is_tmux_available, launch_in_tmux

    config = load_sprint_config(
        index_path=index_path,
        start_phase=start_phase,
        end_phase=end_phase,
        max_turns=max_turns,
        model=model or os.environ.get("CLAUDE_MODEL", ""),
        dry_run=dry_run,
        permission_flag=permission_flag,
        debug=debug_mode,
        stall_timeout=stall_timeout,
        stall_action=stall_action,
        shadow_gates=shadow_gates,
    )

    # Thread tmux session name into config when relaunched by launch_in_tmux
    if tmux_session_name:
        config.tmux_session_name = tmux_session_name

    # Override release_dir if explicitly provided
    if release_dir_override is not None:
        resolved = Path(release_dir_override).resolve()
        object.__setattr__(config, "release_dir", resolved)
        object.__setattr__(config, "work_dir", resolved)

    # Preflight: fidelity block
    blocked, fidelity_msg = _check_fidelity(index_path)
    if blocked:
        if not force_fidelity_fail:
            click.echo(fidelity_msg, err=True)
            raise SystemExit(1)
        else:
            click.echo(
                f"[WARN] Fidelity block overridden: {force_fidelity_fail}",
                err=True,
            )

    if dry_run:
        _print_dry_run(config)
        return

    # Tmux decision: use tmux unless --no-tmux or tmux unavailable
    if not no_tmux and is_tmux_available():
        launch_in_tmux(config)
    else:
        execute_sprint(config)


@sprint_group.command()
def attach():
    """Attach to a running sprint tmux session.

    Reconnects to the sc-sprint-* tmux session to see the
    live TUI dashboard.
    """
    from .tmux import attach_to_sprint

    attach_to_sprint()


@sprint_group.command()
def status():
    """Show current sprint status without attaching.

    Reads the execution log to display phase completion
    status, timing, and current activity.
    """
    from .logging_ import read_status_from_log

    read_status_from_log()


@sprint_group.command()
@click.option(
    "--lines",
    "-n",
    type=int,
    default=50,
    help="Number of lines to show (default: 50)",
)
@click.option(
    "--follow",
    "-f",
    is_flag=True,
    help="Follow log output (like tail -f)",
)
def logs(lines: int, follow: bool):
    """Tail the sprint execution log.

    Shows the human-readable execution log. Use -f to
    follow new output as it appears.
    """
    from .logging_ import tail_log

    tail_log(lines=lines, follow=follow)


@sprint_group.command()
@click.option(
    "--force",
    is_flag=True,
    help="Force kill without grace period",
)
def kill(force: bool):
    """Stop a running sprint.

    Sends SIGTERM to the sprint process with a 10-second
    grace period, then SIGKILL if needed. Use --force
    to skip the grace period.
    """
    from .tmux import kill_sprint

    kill_sprint(force=force)


@sprint_group.command("verify-checkpoints")
@click.argument(
    "output_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "--recover",
    is_flag=True,
    help="Auto-generate missing checkpoint reports from evidence artifacts.",
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit the manifest as machine-readable JSON instead of a table.",
)
def verify_checkpoints(output_dir: Path, recover: bool, as_json: bool):
    """Verify (and optionally recover) checkpoint reports for a sprint.

    OUTPUT_DIR is a sprint release directory — the one that contains
    `tasklist-index.md`, per-phase tasklists, and the `checkpoints/`
    subtree. The command parses every phase tasklist, checks whether each
    declared `Checkpoint Report Path:` file exists on disk, and prints a
    status table (or JSON with --json). Pass --recover to regenerate
    missing reports from evidence artifacts under `artifacts/`.
    """
    from .checkpoints import (
        build_manifest,
        recover_missing_checkpoints,
        write_manifest,
    )
    from .config import discover_phases

    index_path = output_dir / "tasklist-index.md"
    if not index_path.is_file():
        raise click.ClickException(
            f"No tasklist-index.md found in {output_dir}"
        )

    manifest = build_manifest(index_path, output_dir)

    if recover:
        artifacts_dir = output_dir / "artifacts"
        try:
            phases = discover_phases(index_path)
        except Exception as exc:  # noqa: BLE001
            raise click.ClickException(f"Phase discovery failed: {exc}") from exc
        phase_tasklists = {p.number: p.file for p in phases}
        manifest = recover_missing_checkpoints(
            manifest, artifacts_dir, phase_tasklists
        )

    manifest_path = output_dir / "manifest.json"
    write_manifest(manifest, manifest_path)

    if as_json:
        click.echo(manifest_path.read_text().rstrip())
        return

    _print_checkpoint_table(manifest, manifest_path)


def _print_checkpoint_table(
    manifest: list, manifest_path: Path
) -> None:
    """Render a concise table of the manifest to stdout."""
    total = len(manifest)
    found = sum(1 for e in manifest if e.exists and not e.recovered)
    recovered = sum(1 for e in manifest if e.recovered)
    missing = total - found - recovered

    if total == 0:
        click.echo("No `### Checkpoint:` sections declared in any phase tasklist.")
        click.echo(f"Manifest: {manifest_path}")
        return

    click.echo(
        f"Checkpoints: {total} declared  |  "
        f"{found} found  |  "
        f"{recovered} recovered  |  "
        f"{missing} missing"
    )
    click.echo()
    click.echo(f"{'Phase':>5}  {'Status':<11}  {'Name':<30}  Path")
    click.echo("-" * 80)
    for entry in manifest:
        if entry.recovered:
            status = "recovered"
        elif entry.exists:
            status = "found"
        else:
            status = "MISSING"
        name = entry.name[:30]
        click.echo(
            f"{entry.phase:>5}  {status:<11}  {name:<30}  {entry.expected_path}"
        )
    click.echo()
    click.echo(f"Manifest: {manifest_path}")


def _print_dry_run(config) -> None:
    """Display discovered phases without executing."""
    click.echo(f"Dry run: {len(config.phases)} phases discovered")
    click.echo()
    for phase in config.active_phases:
        click.echo(f"  Phase {phase.number}: {phase.display_name}")
        click.echo(f"    File: {phase.file}")
    click.echo()
    click.echo(
        f"Would execute phases {config.start_phase}"
        f"–{config.end_phase or max(p.number for p in config.phases)}"
    )
