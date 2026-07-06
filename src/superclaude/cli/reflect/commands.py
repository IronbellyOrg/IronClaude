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

# Recursion-breaker (FR-2 / contract Section 3). When the wrapper auto-runs a
# corrective ``/task`` (or its audit) as a child ``claude --print`` subprocess,
# it exports this env var == "1" into that child. If that child's own terminal
# reflect gate fires ``superclaude reflect run`` again, this guard makes it
# immediately exit 0 BEFORE any audit -- breaking the recursion. The truthy
# value is EXACTLY the string "1"; absent/empty/"0"/"2"/any-other do NOT suppress.
_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"


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
    # FR-2 recursion breaker (contract Section 3). This GROUP callback runs
    # during parsing BEFORE the ``run`` subcommand's ``exists=True`` tasklist
    # argument is validated, so a nested gate on a SINCE-MOVED file still exits
    # 0 cleanly ("immediately exits 0 ... before any audit"). Placing the check
    # here -- not inside ``run()``'s body -- is load-bearing: an in-body check
    # cannot pre-empt Click's parse-time path validation. Truthiness is EXACTLY
    # the string "1" (absent/empty/"0"/"2"/any-other run normally).
    if os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1":
        click.echo(
            "reflect-wrapper recursion breaker: nested gate suppressed", err=True
        )
        sys.exit(0)


@reflect_group.command("contract-status")
@click.option(
    "--validate",
    "run_validation",
    is_flag=True,
    help="Validate existing file-based evidence before reporting status.",
)
@click.option(
    "--repo",
    default=None,
    help="Repository owner/name to compare against validation metadata.",
)
@click.option(
    "--pr",
    "pr_number",
    type=int,
    default=None,
    help="Pull request number to compare against validation metadata.",
)
def contract_status(
    run_validation: bool, repo: str | None, pr_number: int | None
) -> None:
    """Report detection-contract readiness without launching reflect audit machinery."""
    from superclaude.pr_submit.contract_setup import (
        derive_candidate,
        diagnose,
        load_evidence,
        validate_candidate,
        write_report,
    )
    from superclaude.pr_submit.contract_setup.writer import ContractSetupError

    diagnosis = diagnose(repo=repo, pr_number=pr_number)
    validation_summary: str | None = None
    validation_report_path: Path | None = None
    validation_error: str | None = None

    if run_validation:
        if diagnosis.evidence_path is None:
            validation_error = "validation skipped: no evidence path is available"
        else:
            probe_dir = (
                diagnosis.evidence_path.parent
                if diagnosis.evidence_path.is_file()
                else diagnosis.evidence_path
            )
            try:
                evidence = load_evidence(probe_dir)
                candidate = derive_candidate(evidence)
                report = validate_candidate(
                    candidate,
                    evidence,
                    expected_result=candidate.expected_classifier_result,
                )
                validation_report_path = write_report(report, evidence, probe_dir)
                validation_summary = report.summary()
                diagnosis = diagnose(repo=repo, pr_number=pr_number)
            except (ContractSetupError, OSError, ValueError, FileNotFoundError) as exc:
                validation_error = f"validation failed: {exc}"

    _render_contract_status(
        diagnosis,
        run_validation=run_validation,
        validation_summary=validation_summary,
        validation_report_path=validation_report_path,
        validation_error=validation_error,
    )


def _render_contract_status(
    diagnosis,
    *,
    run_validation: bool,
    validation_summary: str | None,
    validation_report_path: Path | None,
    validation_error: str | None,
) -> None:
    """Render safe readiness metadata: status, paths, hashes, counts, blockers."""
    click.echo(f"state: {diagnosis.state.value}")
    click.echo(f"override_present: {diagnosis.override_present}")
    click.echo(f"override_locked: {diagnosis.override_locked}")
    click.echo(f"shipped_locked: {diagnosis.shipped_locked}")
    click.echo("checked_paths:")
    for path in diagnosis.checked_paths:
        click.echo(f"  - {path}")
    if diagnosis.evidence_path is not None:
        click.echo(f"evidence_path: {diagnosis.evidence_path}")
    if diagnosis.evidence_sha256 is not None:
        click.echo(f"evidence_sha256: {diagnosis.evidence_sha256}")
    if diagnosis.validation_report_path is not None:
        click.echo(f"validation_report: {diagnosis.validation_report_path}")
    if diagnosis.validation_result is not None:
        click.echo(f"validation_result: {diagnosis.validation_result}")
    click.echo(f"blocker_count: {len(diagnosis.blockers)}")
    if diagnosis.blockers:
        click.echo("blockers:")
        for blocker in diagnosis.blockers:
            click.echo(f"  - {blocker}")
    click.echo(f"next_command: {_contract_status_next_command(diagnosis)}")
    if run_validation:
        click.echo("validation_requested: true")
        if validation_report_path is not None:
            click.echo(f"validation_report_written: {validation_report_path}")
        if validation_summary is not None:
            click.echo("validation_summary:")
            for line in validation_summary.splitlines():
                click.echo(f"  {line}")
        if validation_error is not None:
            click.echo(f"validation_error: {validation_error}")
    else:
        click.echo("validation_requested: false")


def _contract_status_next_command(diagnosis) -> str:
    """Return an actionable next step now that contract-status exists."""
    from superclaude.pr_submit.contract_setup import ContractState

    repo_arg = f" --repo {diagnosis.repo}" if diagnosis.repo else " --repo <owner/repo>"
    pr_arg = (
        f" --pr {diagnosis.pr_number}"
        if diagnosis.pr_number is not None
        else " --pr <number>"
    )
    if diagnosis.state is ContractState.READY:
        return f"/sc:pr-submit --monitor 1{pr_arg}"
    if diagnosis.state is ContractState.DECLINED_BY_USER:
        return (
            "cancelled: setup declined by user; existing contract files left untouched"
        )
    if diagnosis.state in {
        ContractState.VALIDATION_MISSING,
        ContractState.VALIDATION_FAILED,
        ContractState.STALE,
        ContractState.UNLOCKED,
        ContractState.EVIDENCE_MISSING,
    }:
        return f"superclaude reflect contract-status --validate{repo_arg}{pr_arg}"
    return f"superclaude reflect contract-status{repo_arg}{pr_arg}"


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
    default=True,
    help="Allow reflect's gated Wave-7 promotion (default: --promote). O2 callers pass --no-promote.",
)
@click.option(
    "--reachability/--no-reachability",
    "reachability",
    default=True,
    help="Enable the §6.1 step-5.6 contracted-sink reachability gate (default: --reachability). Pass --no-reachability to disable (telemetry-only skip).",
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
# --transport enum guard (Whittaker sentinel/divergence).
# transport_enum:
#   accepted: [openai_compat, stub]
#   unknown_value: "rejected at CLI parse (Click enum), before any dispatch -- non-zero exit, no partial run"
@click.option(
    "--transport",
    type=click.Choice(["openai_compat", "stub"], case_sensitive=False),
    default="openai_compat",
    help="Tier-2 worker transport: openai_compat live proxy or stub credit-free CI lane.",
)
@click.option(
    "--reviewers",
    type=int,
    default=3,
    help="Tier-2 reviewer slots; default 3; 1 is the negative-witness degrade case.",
)
@click.option(
    "--output",
    default=None,
    help="Pinned output dir (default <task-dir>/reflect/post/<short-sha>/).",
)
@click.option(
    "--allow-single-vendor",
    is_flag=True,
    help="Do not flag DEGRADED (exit 11) on single-vendor Tier-2 diversity.",
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
@click.option(
    "--fix/--no-fix",
    "fix",
    default=False,
    help="Run the bounded audit->apply->re-verify auto-fix loop (Click default --no-fix; the O1/O2 gates pass --fix).",
)
@click.option(
    "--max-fix-iterations",
    type=int,
    default=2,
    help="Max apply->verify cycles before terminal HALT (D3, default 2).",
)
@click.option(
    "--base",
    "base_override",
    default=None,
    help=(
        "Explicit audit base ref (single ref vs working tree). Highest precedence "
        "over frontmatter start_commit + merge-base."
    ),
)
@click.option(
    "--isolate-reviewers/--no-isolate-reviewers",
    "isolate_reviewers",
    default=False,
    help=(
        "Opt in to L2 reviewer-isolation: ground Wave-3 reviewers in an isolated "
        "git-worktree snapshot; STOP on a non-committable (dirty/uncommitted) audit "
        "target. OFF by default — preserves today's dirty-tree audit."
    ),
)
def run(
    tasklist: str,
    tmux: bool,
    print_command: bool,
    promote: bool,
    timeout: int | None,
    depth: str,
    transport: str,
    reviewers: int,
    output: str | None,
    allow_single_vendor: bool,
    dry_run: bool,
    resume: bool,
    fix: bool,
    max_fix_iterations: int,
    base_override: str | None,
    isolate_reviewers: bool,
    reachability: bool,
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
            transport=transport,
            reviewers=reviewers,
            output_dir=output,
            model=model,
            timeout=timeout,
            promote=promote,
            allow_single_vendor=allow_single_vendor,
            tmux=tmux,
            dry_run=dry_run,
            print_command=print_command,
            resume=resume,
            fix=fix,
            max_fix_iterations=max_fix_iterations,
            base_override=base_override,
            isolate_reviewers=isolate_reviewers,
            reachability=reachability,
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
        "--transport",
        config.transport,
        "--reviewers",
        str(config.reviewers),
    ]
    # Forward promote EXPLICITLY in both directions. Since the --promote default
    # flipped to True (FR-5), an absent flag in the inner reinvocation would
    # default to promote-on -- so a --tmux + --no-promote outer call must emit
    # --no-promote explicitly, else the inner foreground run would silently promote.
    cmd.append("--promote" if config.promote else "--no-promote")
    if not config.reachability:
        cmd.append("--no-reachability")
    if config.allow_single_vendor:
        cmd.append("--allow-single-vendor")
    cmd.append(
        "--isolate-reviewers" if config.isolate_reviewers else "--no-isolate-reviewers"
    )
    if config.resume:
        cmd.append("--resume")
    # Forward --base so --tmux + --base does not silently lose the base ref in the
    # inner foreground reinvocation (R1 Section 1b gap). Single-ref pass-through, no `..` range.
    if config.base_override:
        cmd += ["--base", config.base_override]
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
