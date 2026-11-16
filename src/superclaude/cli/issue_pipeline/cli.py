"""The ``superclaude issue-pipeline`` command group.

Verbs only sequence calls into the package and print closed result words; no
verb prints file or GitHub text.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from superclaude.cli.issue_watch import cycle
from superclaude.cli.issue_watch import github as gh
from superclaude.cli.issue_watch.runner import Runner, SubprocessRunner

from . import approval_line, approval_record, plan_hash, reads, stage_predicates

_EXIT_REFUSED = 1
_EXIT_CONFIG = 2
_GH_TIMEOUT_S = 60.0
_EXIT_LOCK_HELD = 75  # the watcher's own code for a held lock


def _run_record(action: Callable[[], dict[str, Any]]) -> None:
    """Print the closed JSON result of one record verb, or one closed refusal."""
    try:
        result = action()
    except approval_record.ApprovalError as exc:
        if exc.reason == "lock-held":
            click.echo("lock-held, retry")
            raise SystemExit(_EXIT_LOCK_HELD) from None
        click.echo(f"refused:{exc.reason}")
        raise SystemExit(_EXIT_REFUSED) from None
    click.echo(json.dumps(result, sort_keys=True))


_DIR = click.argument("approvals_dir", type=click.Path())
_ISSUE = click.option("--issue", type=click.IntRange(min=1), required=True)
_STAGE = click.option("--stage", default="plan", show_default=True)
_PLAN_HASH = click.option("--plan-hash", "plan_hash_value", required=True, help="64 lowercase hex.")


@click.group(name="issue-pipeline")
def issue_pipeline_group() -> None:
    """Approval core for a coordinator-started plan-writing worker."""


@issue_pipeline_group.command("plan-hash")
@click.argument("report_dir", type=click.Path())
@click.argument("names", nargs=-1)
def plan_hash_command(report_dir: str, names: tuple[str, ...]) -> None:
    """Print the ordered plan file list and the plan hash of REPORT_DIR."""
    try:
        ordered, digest = plan_hash.compute(report_dir, list(names))
    except plan_hash.PlanHashError as exc:
        click.echo(f"refused:{exc.reason}")
        raise SystemExit(_EXIT_REFUSED) from None
    for name in ordered:
        click.echo(f"file: {name}")
    click.echo(f"plan-sha256: {digest}")


@issue_pipeline_group.command("check-approval")
@click.argument("report_dir", type=click.Path())
@click.argument("names", nargs=-1)
@click.option("--line", "line", required=True, help="The approval text, matched whole.")
@click.option("--issue", type=click.IntRange(min=1), default=None, help="Also require this issue number in the record id.")
def check_approval_command(report_dir: str, names: tuple[str, ...], line: str, issue: int | None) -> None:
    """Print ok or a closed refusal for the approval LINE against the plan files."""
    result = approval_line.check(report_dir, list(names), line, issue)
    click.echo(result)
    if result != approval_line.OK:
        raise SystemExit(_EXIT_REFUSED)


@issue_pipeline_group.command("init")
@_DIR
def init_command(approvals_dir: str) -> None:
    """Create the approvals directory (0700) and its lock file (0600)."""
    try:
        approval_record.init_dir(approvals_dir)
    except approval_record.ApprovalError as exc:
        click.echo(f"refused:{exc.reason}")
        raise SystemExit(_EXIT_REFUSED) from None
    click.echo("ok")


@issue_pipeline_group.command("adopt-create")
@_DIR
@_ISSUE
@_STAGE
def adopt_create_command(approvals_dir: str, issue: int, stage: str) -> None:
    """Reserve (issue, stage); only a `created` result may start a worker."""
    _run_record(lambda: approval_record.adopt_create(approvals_dir, issue, stage))


@issue_pipeline_group.command("adopt-mark")
@_DIR
@_ISSUE
@_STAGE
@click.option("--state", type=click.Choice(["started", "uncertain"]), required=True)
@click.option("--dispatch-id", default=None, help="Required for `started`.")
def adopt_mark_command(approvals_dir: str, issue: int, stage: str, state: str, dispatch_id: str | None) -> None:
    """Mark the adoption row `started` (with the Dispatch id) or `uncertain`."""
    _run_record(lambda: approval_record.adopt_mark(approvals_dir, issue, stage, state, dispatch_id))


@issue_pipeline_group.command("record-create")
@_DIR
@_ISSUE
@_STAGE
@_PLAN_HASH
@click.option("--channel", type=click.Choice(list(approval_record.CHANNELS)), required=True)
@click.option("--evidence-id", required=True, help="Event, comment or message id.")
@click.option("--actor", required=True, help="Actor id.")
def record_create_command(
    approvals_dir: str, issue: int, stage: str, plan_hash_value: str, channel: str, evidence_id: str, actor: str
) -> None:
    """Create the approval row, or append evidence to the existing one."""
    _run_record(
        lambda: approval_record.record_create(approvals_dir, issue, stage, plan_hash_value, channel, evidence_id, actor)
    )


@issue_pipeline_group.command("record-show")
@_DIR
@_ISSUE
@_STAGE
@_PLAN_HASH
def record_show_command(approvals_dir: str, issue: int, stage: str, plan_hash_value: str) -> None:
    """Print the approval row."""
    _run_record(lambda: {"row": approval_record.record_show(approvals_dir, issue, stage, plan_hash_value)})


@issue_pipeline_group.command("record-mark")
@_DIR
@_ISSUE
@_STAGE
@_PLAN_HASH
@click.option("--state", type=click.Choice(list(approval_record.APPROVAL_STATES[1:])), required=True)
def record_mark_command(approvals_dir: str, issue: int, stage: str, plan_hash_value: str, state: str) -> None:
    """Move the approval row forward (`instructed`, `acked`) or to `revoked`."""
    _run_record(lambda: approval_record.record_mark(approvals_dir, issue, stage, plan_hash_value, state))


# --- stage-status: read-only -------------------------------------------------


def _make_runner() -> Runner:
    """The one place a real ``gh`` runner is made (tests replace it)."""
    return SubprocessRunner()


def _load_stage_inputs(config_path: Path) -> tuple[str, frozenset[int]]:
    """The approval label and the approver ids of the watcher's configuration."""
    config = cycle.load_config(config_path)
    return config.approval_label, cycle.validate_approvers(config.approvers_file)


def _timeout() -> float | None:
    return _GH_TIMEOUT_S


def _channel(result: stage_predicates.ChannelResult) -> dict[str, Any]:
    return {
        "accepted": result.accepted,
        "reason": result.reason,
        "evidence_id": result.evidence_id,
        "actor_id": result.actor_id,
        "actor_is_host_login": result.actor_is_host_login,
    }


def _row_facts(approvals_dir: Path | None, issue: int, key: tuple[int, str, str] | None) -> tuple[str | None, int | None, str | None]:
    """Adoption state, approval-row state and its evidence count, read without writing."""
    if approvals_dir is None:
        return None, None, None
    try:
        adoption = approval_record.adopt_show(approvals_dir, issue, stage_predicates.STAGE)["state"]
    except approval_record.ApprovalError:
        adoption = None
    if key is None:
        return adoption, None, None
    try:
        row = approval_record.record_show(approvals_dir, issue, key[1], key[2])
    except approval_record.ApprovalError:
        return adoption, None, None
    return adoption, len(row["evidence"]), row["state"]


def _stage_status(
    issue: int,
    runner: Runner,
    label: str,
    approvers: frozenset[int],
    approvals_dir: Path | None,
    plan_dir: Path | None,
    plan_names: list[str],
) -> dict[str, Any]:
    budget = gh.CallBudget()
    login = gh.user(runner, _timeout)
    if login.value is None:
        raise _StatusRefused(login.reason)
    snapshot = gh.reread(runner, budget, issue, _timeout)
    if snapshot.value is None:
        raise _StatusRefused(snapshot.reason)
    evidence = reads.read_stage_evidence(runner, issue, _timeout, budget)
    if evidence.value is None:
        raise _StatusRefused(evidence.reason)
    host = login.value.login
    checked = plan_dir is not None and bool(plan_names)
    if checked:
        try:
            now: str | None = plan_hash.compute(plan_dir, plan_names)[1]
        except plan_hash.PlanHashError:
            now = None  # an unreadable plan counts as changed
    else:
        latest = stage_predicates.latest_plan_reply(evidence.value.comments, host)
        now = latest.plan_marker.plan_hash if latest and latest.plan_marker else None
    status = stage_predicates.evaluate(
        issue,
        evidence.value.comments,
        evidence.value.events,
        evidence.value.edits,
        plan_hash_now=now,
        host_login=host,
        assignees=snapshot.value.assignees,
        approvers=approvers,
        approval_label=label,
    )
    adoption, evidence_count, row_state = _row_facts(approvals_dir, issue, status.key)
    return {
        "issue": issue,
        "state": status.state,
        "plan_reason": status.plan_reason,
        "plan_reply_id": status.plan_reply_id,
        "plan_hash": status.plan_hash,
        "record_id": status.record_id,
        "plan_files_checked": checked,
        "approvals": {"label": _channel(status.label), "comment": _channel(status.comment)},
        "approved": status.approved,
        "label_revoked": status.label_revoked,
        "status_seen": status.status_seen,
        "assignee_is_host_login": status.assignee_is_host_login,
        "adoption_state": adoption,
        "row_state": row_state,
        "row_evidence_count": evidence_count,
    }


class _StatusRefused(Exception):
    def __init__(self, reason: str | None) -> None:
        super().__init__(reason)
        self.reason = reason or "unreadable"


@issue_pipeline_group.command("stage-status")
@click.argument("issue", type=click.IntRange(min=1))
@click.option("--json", "as_json", is_flag=True, help="Accepted for symmetry; the output is always JSON.")
@click.option("--config", "config_path", type=click.Path(path_type=Path), default="~/.config/superclaude/issue-watch.json", show_default=True)
@click.option("--approvals-dir", type=click.Path(path_type=Path), default=None, help="Read the adoption and approval rows here.")
@click.option("--plan-dir", type=click.Path(path_type=Path), default=None, help="Report directory holding the plan files.")
@click.option("--plan-file", "plan_files", multiple=True, help="A plan file name under --plan-dir (repeat).")
def stage_status_command(
    issue: int,
    as_json: bool,
    config_path: Path,
    approvals_dir: Path | None,
    plan_dir: Path | None,
    plan_files: tuple[str, ...],
) -> None:
    """Print the plan-stage status of ISSUE as closed keys; writes nothing, prints no GitHub text."""
    try:
        label, approvers = _load_stage_inputs(config_path.expanduser())
    except cycle.ConfigError as exc:
        click.echo(f"refused:{exc.reason}")
        raise SystemExit(_EXIT_CONFIG) from None
    try:
        result = _stage_status(issue, _make_runner(), label, approvers, approvals_dir, plan_dir, list(plan_files))
    except _StatusRefused as exc:
        click.echo(f"refused:{exc.reason}")
        raise SystemExit(_EXIT_REFUSED) from None
    click.echo(json.dumps(result, sort_keys=True))
