"""The verb ``superclaude orchestrator wake-ack``: write the acknowledgment of a wake (design 3.6; wave 0).

    wake-ack <wake_id> [--orchestrator <id>] [--tag <tag>]
             [--taken <owner/repo#N>]... [--skipped <owner/repo#N:reason>]...

When wave 0 has decided every item, this writes ``<root>/.orchestrator/wakes/<wake_id>.ack.json``
(schema ``orchestrator-wake-ack/1``) with a temporary file and ``rename``, mode 0600. The
poll reads it at its next cycle: ``taken`` and ``skipped`` entries become ``acked``, and an
entry named in none of the lists is sent again.

The wake is read again here with the same parser as ``wake-check``, so the lists cannot
name an item that is not in it. The verb checks the decisions before it writes:

* every valid ``assigned`` item is in exactly one of ``taken`` and ``skipped``, and every
  ``plan_requests`` item in exactly one of ``taken`` and ``skipped`` (``item_undecided``,
  ``unknown_item``, ``duplicate_decision``, all exit 2, nothing written);
* an item that ``wake-check`` skips for a reason the caller cannot change (``repo_not_listed``,
  ``repo_disabled``, or ``already_dispatched`` for a state file of another wake) is added with
  that reason when the caller leaves it out, and cannot be ``taken`` (``conflicts_with_check``);
* a plan request is skipped only as ``already_planned``, ``held_backlog`` or ``not_open``
  (the three of 3.6), or ``repo_not_listed`` and ``repo_disabled`` (an addition: 3.6 gives a
  plan request no other way out when ``repos.yaml`` changed after the poll read it); an
  ``assigned`` skip reason is any token of ``[a-z][a-z0-9_]{0,39}`` (the poll's own pattern);
* record first, acknowledgment second: an ``assigned`` item can be ``taken`` only when its
  state file exists for this wake and this orchestrator (``taken_without_record``), and a
  plan request only when its plan record exists (``taken_without_plan_record``). Otherwise the
  poll would stop counting the issue as in flight before the orchestrator counts it (5.7).
* ``rejected_items`` and ``warnings`` are not decided by the caller: they come from the parse,
  the same ones ``wake-check`` printed.

A wake that was already acknowledged is not written again: the existing acknowledgment is
printed (``already_acked``). A wake that ``wake-check`` would refuse is refused here
(``wake_not_ackable``, exit 3) and writes nothing. The run file ``runs/<id>.json`` must exist
(wave 0 writes it first): its ``run_id`` and ``host`` go into the acknowledgment.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

import click

from superclaude.cli.issue_watch import repos, wake
from superclaude.cli.issue_watch.predicates import format_utc, split_issue_key

from . import common, ext, repos_file, state, wake_check, wakefiles
from .state import EXIT_CONFLICT, EXIT_INVALID, EXIT_NOT_FOUND, StateError

PLAN_SKIP_REASONS: Final = (
    "already_planned",
    "held_backlog",
    "not_open",
    "repo_not_listed",
    "repo_disabled",
)
_REASON = re.compile(r"[a-z][a-z0-9_]{0,39}")


def _decisions(
    taken: list[tuple[str, int]], skipped: list[tuple[str, int, str]]
) -> tuple[set[tuple[str, int]], dict[tuple[str, int], str]]:
    keys = [*taken, *((r, n) for r, n, _ in skipped)]
    if len(set(keys)) != len(keys):
        raise StateError("duplicate_decision", EXIT_INVALID)
    for _, _, reason in skipped:
        if _REASON.fullmatch(reason) is None:
            raise StateError("invalid_reason", EXIT_INVALID)
    return set(taken), {(r, n): reason for r, n, reason in skipped}


def _own_record(
    root: Path | str, item: wake_check.Item, own_id: str, wake_id: str
) -> None:
    """Refuse ``taken`` for an item whose record does not exist yet (record first, acknowledgment second)."""
    if item.kind == "assigned":
        try:
            doc = state.load_state(root, item.repo, item.number)
        except StateError:
            raise StateError(
                "taken_without_record",
                EXIT_CONFLICT,
                repo=item.repo,
                number=item.number,
            ) from None
        if doc["orchestrator"] != own_id or doc["wake_id"] != wake_id:
            raise StateError(
                "taken_without_record",
                EXIT_CONFLICT,
                repo=item.repo,
                number=item.number,
            )
        return
    assert item.requested_at is not None
    try:
        plan = state.load_plan(root, item.repo, item.number, item.requested_at)
    except StateError:
        raise StateError(
            "taken_without_plan_record",
            EXIT_CONFLICT,
            repo=item.repo,
            number=item.number,
        ) from None
    if plan["orchestrator"] != own_id:
        raise StateError(
            "taken_without_plan_record",
            EXIT_CONFLICT,
            repo=item.repo,
            number=item.number,
        )


def acknowledge(
    root: Path | str,
    wake_id: str,
    own_id: str,
    own_tag: str | None,
    doc: repos.ReposDoc,
    taken: list[tuple[str, int]],
    skipped: list[tuple[str, int, str]],
    now: datetime | None = None,
) -> dict[str, Any]:
    """Check the decisions and write the acknowledgment (or return the one that exists)."""
    try:
        parsed = wakefiles.parse(
            wakefiles.read_wake(root, wake_id), wake_id, own_id, own_tag
        )
    except wake.WakeRejected as exc:
        raise StateError("wake_not_ackable", EXIT_CONFLICT, why=exc.reason) from None
    existing = wakefiles.load_ack(root, wake_id)
    if (
        existing is not None
    ):  # the first acknowledgment stands; nothing is decided twice
        return {"wake_id": wake_id, "already_acked": True, "ack": existing}
    taken_set, skip_map = _decisions(taken, skipped)
    items = wake_check.classify(root, parsed, doc, own_id, wake_id)
    known = {i.key for i in items}
    if not (taken_set | set(skip_map)) <= known:
        raise StateError("unknown_item", EXIT_INVALID)
    try:
        run = state.load_run(root, own_id)
    except StateError as exc:
        if exc.reason == "not_found":
            raise StateError("run_not_found", EXIT_NOT_FOUND) from None
        raise

    out_taken: list[dict[str, Any]] = []
    out_skipped: list[dict[str, Any]] = []
    undecided: list[str] = []
    seen: set[tuple[str, int]] = set()
    for item in items:
        if item.key in seen:
            continue
        seen.add(item.key)
        forced = item.decision == "skipped" and not item.same_wake
        if forced:
            if item.key in taken_set:
                raise StateError(
                    "conflicts_with_check",
                    EXIT_INVALID,
                    repo=item.repo,
                    number=item.number,
                )
            if item.key in skip_map and skip_map[item.key] != item.reason:
                raise StateError(
                    "conflicts_with_check",
                    EXIT_INVALID,
                    repo=item.repo,
                    number=item.number,
                )
            out_skipped.append(
                {"repo": item.repo, "number": item.number, "reason": item.reason}
            )
        elif item.key in taken_set:
            _own_record(root, item, own_id, wake_id)
            out_taken.append({"repo": item.repo, "number": item.number})
        elif item.key in skip_map:
            reason = skip_map[item.key]
            if item.kind == "plan" and reason not in PLAN_SKIP_REASONS:
                raise StateError(
                    "invalid_reason", EXIT_INVALID, repo=item.repo, number=item.number
                )
            out_skipped.append(
                {"repo": item.repo, "number": item.number, "reason": reason}
            )
        else:
            undecided.append(f"{item.repo}#{item.number}")
    if undecided:
        raise StateError("item_undecided", EXIT_INVALID, items=undecided)

    ack = {
        "schema": wake.ACK_SCHEMA,
        "wake_id": wake_id,
        "acked_at": format_utc(now if now is not None else datetime.now(timezone.utc)),
        "orchestrator": {"id": own_id, "run_id": run["run_id"], "host": run["host"]},
        "taken": out_taken,
        "skipped": out_skipped,
        "rejected_items": [{"index": i, "reason": why} for i, why in parsed.rejected],
        "warnings": wake_check.warnings_of(parsed),
    }
    with state.locked(root):
        existing = wakefiles.load_ack(root, wake_id)
        if existing is not None:
            return {"wake_id": wake_id, "already_acked": True, "ack": existing}
        ext.write_json(wakefiles.wakes_dir(root) / f"{wake_id}.ack.json", ack)
    return {"wake_id": wake_id, "already_acked": False, "ack": ack}


def _item(text: str) -> tuple[str, int]:
    try:
        return split_issue_key(text)
    except ValueError:
        raise StateError("invalid_item", EXIT_INVALID) from None


@click.command("wake-ack")
@click.argument("wake_id")
@click.option(
    "--orchestrator",
    default=None,
    help="My orchestrator id (default: from the session tag).",
)
@click.option(
    "--tag",
    default=None,
    help="My session tag (default: the CLAUDE_TOPIC of this session).",
)
@click.option(
    "--taken",
    multiple=True,
    metavar="OWNER/REPO#N",
    help="An item this orchestrator took (record exists).",
)
@click.option(
    "--skipped",
    multiple=True,
    metavar="OWNER/REPO#N:REASON",
    help="An item it did not take, with the reason.",
)
def wake_ack_cmd(wake_id, orchestrator, tag, taken, skipped) -> None:
    """Write the acknowledgment of a wake once every item is decided."""

    def action() -> dict[str, Any]:
        root = common.root()
        wakefiles.valid_wake_id(wake_id)
        own_id, own_tag = ext.identity(orchestrator, tag)
        skips = []
        for text in skipped:
            key, sep, reason = text.rpartition(":")
            if not sep:
                raise StateError("invalid_item", EXIT_INVALID)
            skips.append((*_item(key), reason))
        doc = repos_file.load_doc(root, ext.make_runner("wake-ack"))
        return acknowledge(
            root, wake_id, own_id, own_tag, doc, [_item(t) for t in taken], skips
        )

    common.run(action)
