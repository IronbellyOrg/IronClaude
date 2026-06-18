"""Sprint CLI commands — Click command group and subcommands.

Defines the ``superclaude sprint`` command group with five subcommands:
run, attach, status, logs, kill.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

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
    "--startup-stall-timeout",
    "startup_stall_timeout",
    type=int,
    default=300,
    show_default=True,
    help="Seconds to wait for the first event from a subprocess before treating as startup-stall (0 = disabled).",
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
@click.option(
    "--state-dir",
    "state_dir_override",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Transient state directory for .sprint-exitcode and other runtime artifacts (default: $SPRINT_STATE_DIR or .dev/sprint-state/<tasklist-id>/).",
)
@click.option(
    "--handoff/--no-handoff",
    "handoff_enabled",
    default=True,
    help="Enable per-task handoff records (default: enabled).",
)
@click.option(
    "--resume",
    "resume_task_id",
    default="",
    help="Resume from a task id, skipping validated-successful tasks (composes with --start/--end).",
)
@click.option(
    "--task-parallelism",
    "task_parallelism",
    type=int,
    default=1,
    show_default=True,
    help="Number of tasks to execute concurrently per phase (1 = sequential).",
)
@click.option(
    "--fresh",
    "fresh",
    is_flag=True,
    default=False,
    help="Ignore prior on-disk state; clean run from phase 1 with auto-resume OFF.",
)
@click.option(
    "--restart",
    "fresh",
    is_flag=True,
    default=False,
    help="Alias for --fresh.",
)
@click.option(
    "--yes",
    "-y",
    "assume_yes",
    is_flag=True,
    default=False,
    help="Non-interactive assent for the auto-resume confirmation prompt "
    "(also honored via SUPERCLAUDE_SPRINT_ASSUME_YES=1 or CI=1).",
)
@click.pass_context
def run(
    ctx: click.Context,
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
    startup_stall_timeout: int,
    stall_action: str,
    shadow_gates: bool,
    force_fidelity_fail: str,
    release_dir_override: Path | None,
    state_dir_override: Path | None,
    handoff_enabled: bool,
    resume_task_id: str,
    task_parallelism: int,
    fresh: bool,
    assume_yes: bool,
):
    """Execute a sprint from a tasklist index.

    INDEX_PATH is the path to a tasklist-index.md file.

    Discovers phase files, validates they exist, then executes each
    phase sequentially in fresh Claude Code sessions. Results are
    written to a results/ directory alongside the index.

    By default, starts a tmux session so the sprint survives SSH
    disconnects. Use --no-tmux to run in the foreground.

    AUTO-RESUME (default): with no explicit --start/--end window and no
    --fresh, an interrupted run auto-detects the boundary phase from on-disk
    state and resumes there (re-running only the unfinished task on the
    task-level path). Explicit --start/--end (even --start 1) or --fresh
    disables auto-detection and preserves today's exact behavior.
    """
    # Diagnostic (TASK-RF-faulthandler-redirect): enable all-threads fault
    # dumping so the next real Rich Live refresh-thread crash (Thread-1) prints
    # a Python-vs-C stack, distinguishing a concurrency TypeError (H-C) from a
    # fork/heap segfault (H-A). See .dev/troubleshoot/bug-rich-render-none-*.
    import faulthandler

    # Don't clobber a faulthandler config an outer harness may have set (e.g. a
    # custom output file via faulthandler.enable(file=...), or external stderr
    # redirection — note PYTHONFAULTHANDLER only *enables* the handler, it does
    # not set an output file); only enable if not already on (PR #182 review,
    # low). The default handler writes to stderr, which is what the crash-capture
    # diagnostic wants.
    if not faulthandler.is_enabled():
        faulthandler.enable(all_threads=True)

    from click.core import ParameterSource

    from .config import load_sprint_config
    from .executor import execute_sprint
    from .tmux import is_tmux_available, launch_in_tmux

    # --- Auto-resume (DD-5 / AC-7): explicit window via Click parameter source,
    # NOT value comparison (an explicit `--start 1` MUST bypass auto-resume).
    position_explicit = (
        ctx.get_parameter_source("start_phase") == ParameterSource.COMMANDLINE
        or ctx.get_parameter_source("end_phase") == ParameterSource.COMMANDLINE
    )
    assume_yes = (
        assume_yes
        or bool(os.environ.get("SUPERCLAUDE_SPRINT_ASSUME_YES"))
        or bool(os.environ.get("CI"))
    )

    if fresh:
        # Clean run from phase 1 with auto-detect OFF (DD-5).
        start_phase, end_phase = 1, 0
    elif not position_explicit:
        # AUTO-RESUME branch (FR-4.2). Detect → print → (gate/drift STOP) →
        # prompt → proceed/dispatch.
        from .resume.models import Granularity

        decision = _auto_resume(index_path, assume_yes=assume_yes, dry_run=dry_run)
        if decision.action == "nothing_to_resume":
            click.echo("Nothing to resume — all discovered phases are complete.")
            return
        if decision.action == "ambiguous":
            click.echo("Ambiguous resume state — refusing to auto-pick:", err=True)
            for reason in decision.messages:
                click.echo(f"  - {reason}", err=True)
            click.echo(
                "Disambiguate with an explicit --start/--end window or --fresh.",
                err=True,
            )
            raise SystemExit(decision.exit_code)
        if decision.action == "dry_run":
            _print_resume_decision(decision)
            return
        if decision.action == "stop":
            for line in decision.messages:
                click.echo(line, err=True)
            raise SystemExit(decision.exit_code)
        # action == "proceed"
        plan = decision.plan
        if plan.granularity == Granularity.TASK and plan.rerun_task_ids:
            _dispatch_resume_rerun(index_path, plan)
            return
        # PHASE path: narrow the window to the boundary and fall through to the
        # existing executor loop (NG1 — nothing about phase execution changes).
        start_phase, end_phase = plan.start_phase, plan.end_phase

    state_dir = state_dir_override or (
        Path(os.environ["SPRINT_STATE_DIR"])
        if os.environ.get("SPRINT_STATE_DIR")
        else None
    )

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
        startup_stall_timeout=startup_stall_timeout,
        stall_action=stall_action,
        shadow_gates=shadow_gates,
        state_dir=state_dir,
        handoff_enabled=handoff_enabled,
        resume_task_id=resume_task_id,
        task_parallelism=task_parallelism,
    )

    # Thread tmux session name into config when relaunched by launch_in_tmux
    if tmux_session_name:
        config.tmux_session_name = tmux_session_name

    # Override release_dir if explicitly provided
    if release_dir_override is not None:
        original_release_dir_name = config.release_dir.name
        resolved = Path(release_dir_override).resolve()
        object.__setattr__(config, "release_dir", resolved)
        object.__setattr__(config, "work_dir", resolved)
        # Re-derive state_dir under the new release name when no explicit
        # state_dir was provided AND the current state_dir matches the
        # original auto-derivation. This resolves OQ-1 by keeping the
        # default factory consistent with the post-override release_dir.
        if (
            state_dir is None
            and config.state_dir
            == Path(".dev/sprint-state") / original_release_dir_name
        ):
            object.__setattr__(
                config,
                "state_dir",
                Path(".dev/sprint-state") / resolved.name,
            )

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


def _auto_resume(index_path: Path, *, assume_yes: bool, dry_run: bool):
    """Plan → drift → gate → (dry-run/STOP/prompt) → ResumeDecision (design §8).

    Pure-read planning; the gate is run in report-only mode (no results/
    mutation). Returns a :class:`ResumeDecision` whose ``action`` the caller acts
    on: ``nothing_to_resume`` | ``ambiguous`` | ``dry_run`` | ``stop`` | ``proceed``.
    """
    from .resume import BoundaryIntegrityGate, DriftAssessor, ResumePlanner
    from .resume.models import Granularity, ResumeDecision

    plan = ResumePlanner().plan(index_path)
    if plan.ambiguous:
        return ResumeDecision(
            plan=plan,
            action="ambiguous",
            messages=list(plan.ambiguity_reasons),
            exit_code=2,
        )
    if plan.granularity == Granularity.NONE:
        return ResumeDecision(plan=plan, action="nothing_to_resume", exit_code=0)

    drift = DriftAssessor().assess(index_path, plan)
    report = BoundaryIntegrityGate().run(plan)

    if dry_run:
        return ResumeDecision(
            plan=plan, drift=drift, report=report, action="dry_run", exit_code=0
        )

    if not report.passed:
        return ResumeDecision(
            plan=plan,
            drift=drift,
            report=report,
            action="stop",
            messages=[
                "Resume blocked by the boundary integrity gate:",
                *(f"  - {r}" for r in report.blocking_reasons),
            ],
            exit_code=2,
        )

    if drift.confidence < 0.8:
        return ResumeDecision(
            plan=plan,
            drift=drift,
            report=report,
            action="stop",
            messages=[
                f"Resume blocked: tasklist drift confidence "
                f"{drift.confidence:.2f} < 0.80.",
                f"  {drift.explanation}",
                "Choose an explicit --start/--end window, or --fresh to discard "
                "prior state.",
            ],
            exit_code=2,
        )

    # Drift confidence >= 0.8: confirm unless --yes / non-interactive (NFR-4).
    if not assume_yes:
        import sys

        if sys.stdin is not None and sys.stdin.isatty():
            _print_resume_decision(
                ResumeDecision(plan=plan, drift=drift, report=report, action="proceed")
            )
            if not click.confirm("Proceed with auto-resume?", default=True):
                return ResumeDecision(
                    plan=plan,
                    drift=drift,
                    report=report,
                    action="stop",
                    messages=["Auto-resume aborted by operator."],
                    exit_code=1,
                )
        else:
            return ResumeDecision(
                plan=plan,
                drift=drift,
                report=report,
                action="stop",
                messages=[
                    "Non-interactive session: auto-resume confirmation required. "
                    "Re-run with --yes (or set SUPERCLAUDE_SPRINT_ASSUME_YES=1 / "
                    "CI=1), or pass an explicit --start/--end window.",
                ],
                exit_code=2,
            )

    # On the --yes / CI proceed path the interactive block above is skipped, so the
    # plan was never printed. Realize design §7's "print_plan THEN prompt(skipped:
    # --yes)" sequence (AC-1 / FR-4.2 / G5 visible-by-default UX, NEW-R1): print the
    # inferred plan + half-written partial-work paths before proceeding, skipping
    # ONLY the click.confirm. Guarded by ``assume_yes`` so the interactive-confirm
    # path (which already printed at the TTY branch above) does not print twice.
    if assume_yes:
        _print_resume_decision(
            ResumeDecision(plan=plan, drift=drift, report=report, action="proceed")
        )

    return ResumeDecision(
        plan=plan, drift=drift, report=report, action="proceed", exit_code=0
    )


def _dispatch_resume_rerun(index_path: Path, plan) -> None:
    """Dispatch a task-level resume to the existing rerun engine (AC-2)."""
    from .config import load_sprint_config
    from .rerun_tasks import run_rerun_tasks

    config = load_sprint_config(index_path)
    exit_code = run_rerun_tasks(
        config,
        phase=plan.interrupted_phase,
        tasks=list(plan.rerun_task_ids),
        from_reflect_report=None,
        merge_back=True,
        dry_run=False,
        include_transitive=False,
        ignore_deps=False,
        force_merge=False,
        allow_loop=False,
        no_verify_checkpoints=False,
        bundle_dir=None,
        restore=False,
    )
    raise SystemExit(exit_code)


def _print_resume_decision(decision) -> None:
    """Print the ResumePlan + DriftAssessment + BoundaryReport (FR-4.2 / FR-4.5)."""
    plan = decision.plan
    click.echo("── Auto-resume plan ──")
    click.echo(f"  index:            {plan.index_path}")
    click.echo(f"  completed phases: {plan.completed_phases}")
    click.echo(
        f"  interrupted:      phase {plan.interrupted_phase} ({plan.interrupt_kind})"
    )
    click.echo(f"  resume window:    phases {plan.start_phase}–{plan.end_phase}")
    click.echo(f"  granularity:      {plan.granularity.value}")
    if plan.rerun_task_ids:
        click.echo(f"  re-run tasks:     {', '.join(plan.rerun_task_ids)}")
    if decision.drift is not None:
        d = decision.drift
        click.echo(
            f"  drift:            confidence {d.confidence:.2f} "
            f"(tier {d.tier}) — {d.explanation}"
        )
        for changed in d.changed_paths:
            click.echo(f"                    changed: {changed}")
    if decision.report is not None:
        r = decision.report
        click.echo(
            f"  integrity gate:   {'PASS' if r.passed else 'STOP'} "
            f"(last-completed validated: {r.validated_last})"
        )
        for s in r.suspects:
            click.echo(
                f"    suspect: {s.task_id} [{s.role}] "
                f"persisted={s.persisted_status} derived={s.derived_status}"
            )
        for task, reason in r.coherence_warnings:
            click.echo(f"    coherence (advisory): {task.task_id}: {reason}")
        # F-2/CG-1: surface the half-written partial-work paths on the report-only
        # path (design §4(b) "report suspect paths in BoundaryReport (always)").
        # ``partial_paths`` is populated regardless of quarantine opt-in, so these
        # print on the dry-run and interactive-confirm paths where ``quarantined``
        # is empty.
        for p in r.partial_paths:
            click.echo(f"    partial work (uncommitted): {p}")
        for canonical, copy in r.quarantined.items():
            click.echo(f"    quarantined: {canonical} -> {copy}")
        for reason in r.blocking_reasons:
            click.echo(f"    blocking: {reason}")


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
    "--reevaluate-stale",
    is_flag=True,
    help=(
        "When recovering, re-stamp an existing stale FAIL/BLOCKED checkpoint "
        "whose phase has recovered to UNKNOWN/Auto-Recovered (never auto-PASS)."
    ),
)
@click.option(
    "--json",
    "as_json",
    is_flag=True,
    help="Emit the manifest as machine-readable JSON instead of a table.",
)
def verify_checkpoints(
    output_dir: Path, recover: bool, reevaluate_stale: bool, as_json: bool
):
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
        raise click.ClickException(f"No tasklist-index.md found in {output_dir}")

    manifest = build_manifest(index_path, output_dir)

    if recover:
        artifacts_dir = output_dir / "artifacts"
        try:
            phases = discover_phases(index_path)
        except Exception as exc:  # noqa: BLE001
            raise click.ClickException(f"Phase discovery failed: {exc}") from exc
        phase_tasklists = {p.number: p.file for p in phases}
        manifest = recover_missing_checkpoints(
            manifest,
            artifacts_dir,
            phase_tasklists,
            reevaluate_stale=reevaluate_stale,
        )

    manifest_path = output_dir / "manifest.json"
    write_manifest(manifest, manifest_path)

    if as_json:
        click.echo(manifest_path.read_text().rstrip())
        return

    _print_checkpoint_table(manifest, manifest_path)


@sprint_group.command("rerun-tasks")
@click.argument("index_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--phase",
    type=int,
    default=None,
    help="Phase number whose failed tasks should be re-executed.",
)
@click.option(
    "--tasks",
    type=str,
    default=None,
    help="Comma-separated task IDs to rerun (e.g. T07.11,T07.12).",
)
@click.option(
    "--from-reflect-report",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Resolve failed tasks from a reflect report instead of --phase/--tasks.",
)
@click.option(
    "--merge-back/--no-merge-back",
    default=True,
    help="Merge rerun results back into canonical results (default: enabled).",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Preview the rerun plan without executing or merging.",
)
@click.option(
    "--include-transitive",
    is_flag=True,
    help="Include transitive dependencies of the target tasks in the rerun.",
)
@click.option(
    "--ignore-deps",
    is_flag=True,
    help="Rerun only the named tasks, ignoring dependency edges.",
)
@click.option(
    "--force-merge",
    is_flag=True,
    help="Merge results even when the source tasklist SHA256 changed mid-flight.",
)
@click.option(
    "--allow-loop",
    is_flag=True,
    help="Permit rerun of a task that has already hit the retry cap.",
)
@click.option(
    "--no-verify-checkpoints",
    is_flag=True,
    help="Skip the post-merge verify-checkpoints --recover auto-invoke.",
)
@click.option(
    "--bundle-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Explicit recovery bundle directory (default: auto-suffixed under results).",
)
@click.option(
    "--restore",
    is_flag=True,
    help="Restore deliverables and checkboxes from a prior aborted rerun bundle.",
)
@click.option(
    "--fresh",
    "fresh",
    is_flag=True,
    default=False,
    help="Disable auto-detection; require explicit --phase/--tasks.",
)
@click.option(
    "--restart",
    "fresh",
    is_flag=True,
    default=False,
    help="Alias for --fresh.",
)
@click.option(
    "--yes",
    "-y",
    "assume_yes",
    is_flag=True,
    default=False,
    help="Non-interactive assent (also via SUPERCLAUDE_SPRINT_ASSUME_YES=1 / CI=1).",
)
def rerun_tasks(
    index_path: Path,
    phase: Optional[int],
    tasks: Optional[str],
    from_reflect_report: Optional[Path],
    merge_back: bool,
    dry_run: bool,
    include_transitive: bool,
    ignore_deps: bool,
    force_merge: bool,
    allow_loop: bool,
    no_verify_checkpoints: bool,
    bundle_dir: Optional[Path],
    restore: bool,
    fresh: bool,
    assume_yes: bool,
) -> None:
    """Re-execute only the named failed tasks within a single sprint phase.

    INDEX_PATH is the sprint release's tasklist-index.md — the same file
    `superclaude sprint run` consumes. Use --phase N together with
    --tasks T07.11,T07.12 to surgically re-run a subset of a phase's tasks,
    then merge their results back into the canonical results directory and
    tasklist. As an alternative to --phase/--tasks, pass --from-reflect-report
    to let a reflect report nominate the failed tasks; that flag is mutually
    exclusive with --phase / --tasks. By default results are merged back and a
    `verify-checkpoints --recover` pass runs afterward; use --no-merge-back or
    --no-verify-checkpoints to opt out, and --dry-run to preview the plan.
    """
    from .config import load_sprint_config
    from .rerun_tasks import run_rerun_tasks

    if from_reflect_report and (phase or tasks):
        raise click.ClickException(
            "--from-reflect-report is mutually exclusive with --phase / --tasks"
        )

    # Auto-detect parity (FR-4.1 / AC-9): when no explicit selector is given and
    # --fresh is absent, the planner nominates the boundary phase + failed-task
    # set, and we proceed exactly as if the operator had passed --phase/--tasks.
    explicit = phase is not None or tasks is not None or from_reflect_report is not None
    tasks_list = tasks.split(",") if tasks else None
    if not explicit and not fresh:
        from .resume import ResumePlanner
        from .resume.models import Granularity

        assume_yes_eff = (
            assume_yes
            or bool(os.environ.get("SUPERCLAUDE_SPRINT_ASSUME_YES"))
            or bool(os.environ.get("CI"))
        )
        _ = assume_yes_eff  # reserved for future interactive assent symmetry
        plan = ResumePlanner().plan(index_path)
        if plan.ambiguous:
            click.echo("Ambiguous resume state — refusing to auto-pick:", err=True)
            for reason in plan.ambiguity_reasons:
                click.echo(f"  - {reason}", err=True)
            raise SystemExit(2)
        if plan.granularity == Granularity.NONE:
            if not plan.completed_phases:
                # No phases discovered at all — not a resumable sprint index.
                raise click.UsageError(
                    "No sprint phases were discovered from the given index, so "
                    "there is nothing to auto-detect. Pass an explicit --phase "
                    "(with --tasks) or a valid tasklist-index.md."
                )
            click.echo("Nothing to rerun — all discovered phases are complete.")
            return
        if plan.granularity != Granularity.TASK or not plan.rerun_task_ids:
            raise click.ClickException(
                "Auto-detect found a phase-level interruption with no recoverable "
                "per-task failures. Use `superclaude sprint run` to re-run the "
                "phase, or pass explicit --phase/--tasks."
            )
        phase = plan.interrupted_phase
        tasks_list = list(plan.rerun_task_ids)
        click.echo(
            f"Auto-detected rerun target: phase {phase}, tasks {', '.join(tasks_list)}."
        )
    elif not from_reflect_report and not phase:
        raise click.UsageError(
            "--phase is required when --from-reflect-report is not used"
        )

    config = load_sprint_config(index_path)
    exit_code = run_rerun_tasks(
        config,
        phase=phase,
        tasks=tasks_list,
        from_reflect_report=from_reflect_report,
        merge_back=merge_back,
        dry_run=dry_run,
        include_transitive=include_transitive,
        ignore_deps=ignore_deps,
        force_merge=force_merge,
        allow_loop=allow_loop,
        no_verify_checkpoints=no_verify_checkpoints,
        bundle_dir=bundle_dir,
        restore=restore,
    )
    raise SystemExit(exit_code)


def _print_checkpoint_table(manifest: list, manifest_path: Path) -> None:
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
        click.echo(f"{entry.phase:>5}  {status:<11}  {name:<30}  {entry.expected_path}")
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
