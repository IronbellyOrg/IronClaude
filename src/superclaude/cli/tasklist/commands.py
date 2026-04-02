"""Tasklist CLI commands -- Click command group for ``superclaude tasklist``.

Defines the ``superclaude tasklist validate`` command with all flags
per FR-016/FR-017.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click


@click.group("tasklist")
def tasklist_group():
    """Tasklist validation commands.

    Validate generated tasklists against their upstream roadmap.
    Catches fabricated traceability IDs, missing deliverables, and
    dependency chain errors.

    Examples:
        superclaude tasklist validate ./output
        superclaude tasklist validate ./output --roadmap-file roadmap.md
        superclaude tasklist validate ./output --tasklist-dir tasklists/
    """
    pass


@tasklist_group.command()
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.option(
    "--roadmap-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the roadmap file. Default: {output_dir}/roadmap.md.",
)
@click.option(
    "--tasklist-dir",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the tasklist directory. Default: {output_dir}/.",
)
@click.option(
    "--model",
    default="",
    help="Override model for validation steps.",
)
@click.option(
    "--max-turns",
    type=int,
    default=100,
    help="Max agent turns per claude subprocess. Default: 100.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging.",
)
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the TDD file used as an additional validation input.",
)
@click.option(
    "--prd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Path to the PRD file used as an additional validation input.",
)
def validate(
    output_dir: Path,
    roadmap_file: Path | None,
    tasklist_dir: Path | None,
    model: str,
    max_turns: int,
    debug: bool,
    tdd_file: Path | None,
    prd_file: Path | None,
) -> None:
    """Validate tasklist fidelity against a roadmap.

    OUTPUT_DIR is the directory where the validation report will be written.

    Checks deliverable coverage, signature preservation, traceability ID
    validity, and dependency chain correctness. Exits with code 1 if
    HIGH-severity deviations are found.

    Examples:
        superclaude tasklist validate ./output
        superclaude tasklist validate ./output --roadmap-file spec/roadmap.md
        superclaude tasklist validate ./output --debug
    """
    from .executor import execute_tasklist_validate
    from .models import TasklistValidateConfig

    # Resolve defaults
    resolved_output = output_dir.resolve()
    resolved_output.mkdir(parents=True, exist_ok=True)

    resolved_roadmap = (
        roadmap_file.resolve()
        if roadmap_file is not None
        else resolved_output / "roadmap.md"
    )

    resolved_tasklist_dir = (
        tasklist_dir.resolve() if tasklist_dir is not None else resolved_output
    )

    # Auto-wire tdd_file and prd_file from .roadmap-state.json if not explicitly passed
    from ..roadmap.executor import read_state

    state = read_state(resolved_output / ".roadmap-state.json") or {}
    if tdd_file is None:
        saved_tdd = state.get("tdd_file")
        if saved_tdd:
            saved_tdd_path = Path(saved_tdd)
            if saved_tdd_path.is_file():
                click.echo(
                    f"[tasklist validate] Auto-wired --tdd-file from .roadmap-state.json: {saved_tdd_path}",
                    err=True,
                )
                tdd_file = saved_tdd_path
            else:
                click.echo(
                    f"[tasklist validate] WARNING: State file references --tdd-file {saved_tdd} but file not found; skipping.",
                    err=True,
                )
        elif state.get("input_type") == "tdd":
            # When the primary input was a TDD, tdd_file is null in state
            # (because --tdd-file is the supplementary flag, not the primary).
            # Fall back to spec_file which IS the TDD in this case.
            saved_spec = state.get("spec_file")
            if saved_spec:
                saved_spec_path = Path(saved_spec)
                if saved_spec_path.is_file():
                    click.echo(
                        f"[tasklist validate] Auto-wired --tdd-file from .roadmap-state.json spec_file (input_type=tdd): {saved_spec_path}",
                        err=True,
                    )
                    tdd_file = saved_spec_path
    if prd_file is None:
        saved_prd = state.get("prd_file")
        if saved_prd:
            saved_prd_path = Path(saved_prd)
            if saved_prd_path.is_file():
                click.echo(
                    f"[tasklist validate] Auto-wired --prd-file from .roadmap-state.json: {saved_prd_path}",
                    err=True,
                )
                prd_file = saved_prd_path
            else:
                click.echo(
                    f"[tasklist validate] WARNING: State file references --prd-file {saved_prd} but file not found; skipping.",
                    err=True,
                )

    config = TasklistValidateConfig(
        output_dir=resolved_output,
        roadmap_file=resolved_roadmap,
        tasklist_dir=resolved_tasklist_dir,
        work_dir=resolved_output,
        max_turns=max_turns,
        model=model,
        debug=debug,
        tdd_file=tdd_file.resolve() if tdd_file is not None else None,
        prd_file=prd_file.resolve() if prd_file is not None else None,
    )

    passed = execute_tasklist_validate(config)

    report_path = resolved_output / "tasklist-fidelity.md"
    if report_path.exists():
        click.echo(f"[tasklist validate] Report written to {report_path}")
    else:
        click.echo("[tasklist validate] No report generated", err=True)

    if not passed:
        click.echo(click.style("FAIL: HIGH-severity deviations found", fg="red"))
        sys.exit(1)
    else:
        click.echo(click.style("PASS: No HIGH-severity deviations", fg="green"))
