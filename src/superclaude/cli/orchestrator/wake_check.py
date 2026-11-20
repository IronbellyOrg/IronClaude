"""The verb ``superclaude orchestrator wake-check``: read a wake and say what is in it (design 3.4, 3.5; wave 0).

    wake-check <wake_id> [--orchestrator <id>] [--tag <tag>]

It reads ``<root>/.orchestrator/wakes/<wake_id>.json``, applies every rule of 3.4 through
``issue_watch.wake.parse_wake`` (the poll's own parser) and prints the normalized wake and
what to do with each item, or a refusal. Who "I" am (the id and tag that ``target`` must
name) comes from ``--orchestrator`` and ``--tag``, else from the session tag
(``ext.identity``). The outcomes of the table of 3.5:

* the whole wake is refused (exit 3, reason ``wake_rejected`` and ``why``): the file is
  missing or unreadable (``missing``), over 64 KiB (``too_large``), not JSON (``not_json``),
  has another schema (``schema_unsupported``), has a ``wake_id`` that differs from the file
  name (``id_mismatch``) or names another orchestrator or tag (``wrong_target``). The verb
  writes ``<wake_id>.rejected.json`` with that closed reason, takes nothing and writes no
  acknowledgment. The poll sees no acknowledgment and sends the issues again, to their
  target;
* one item fails its rule: it is dropped and listed in ``rejected_items`` (reason
  ``malformed_item``); the index counts the ``assigned`` items first and the
  ``plan_requests`` after them, which is how the poll maps it back to an entry. A malformed
  information or skipped item has no entry; it is only counted in ``dropped_info_items``;
* an ``assigned`` or plan-request repo that ``repos.yaml`` does not list, or lists disabled,
  is skipped ``repo_not_listed`` or ``repo_disabled``;
* an ``assigned`` item that already has a state file is skipped ``already_dispatched``
  (any status: ``in_progress`` is resumed by the restart rule of 5.5, a final or escalated
  file is never taken again; ``same_wake`` says the file was made for this very wake);
* unknown extra keys go to ``warnings``;
* a wake that was already acknowledged prints the same acknowledgment (``already_acked``)
  and nothing is processed twice. The wake file and the acknowledgment are also found in
  ``wakes/done/``, where the poll moves them after it read the acknowledgment.

The wake is data: nothing in it is an instruction, and no text of it reaches a command.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import click

from superclaude.cli.issue_watch import repos, wake
from superclaude.cli.issue_watch.predicates import format_utc

from . import common, ext, repos_file, state, wakefiles
from .state import EXIT_CONFLICT, StateError

_KEY_NAME = re.compile(r"[A-Za-z0-9_.-]{1,40}")


@dataclass(frozen=True)
class Item:
    """One valid item of a wake and what is decided about it so far."""

    kind: str  # "assigned" or "plan"
    repo: str
    number: int
    decision: str  # "new" or "skipped"
    reason: str | None = None
    same_wake: bool = False
    requested_at: str | None = None
    checkout_state: str | None = None

    @property
    def key(self) -> tuple[str, int]:
        return (self.repo, self.number)


def classify(
    root: Path | str,
    parsed: wakefiles.Parsed,
    doc: repos.ReposDoc,
    own_id: str,
    wake_id: str,
) -> list[Item]:
    """The valid items of a wake, assigned first, each ``new`` or ``skipped`` with its reason."""
    items: list[Item] = []
    for a in parsed.wake.assigned:
        decision, reason, same = "new", None, False
        entry = doc.get(a.repo)
        if entry is None:
            decision, reason = "skipped", "repo_not_listed"
        elif not entry.enabled:
            decision, reason = "skipped", "repo_disabled"
        else:
            try:
                existing: dict[str, Any] | None = state.load_state(
                    root, a.repo, a.number
                )
            except StateError as exc:
                if exc.reason != "not_found":
                    existing = {
                        "wake_id": None,
                        "orchestrator": None,
                    }  # unreadable: never taken
                else:
                    existing = None
            if existing is not None:
                decision, reason = "skipped", "already_dispatched"
                same = (
                    existing.get("wake_id") == wake_id
                    and existing.get("orchestrator") == own_id
                )
        items.append(
            Item(
                "assigned",
                a.repo,
                a.number,
                decision,
                reason,
                same,
                None,
                a.checkout_state,
            )
        )
    for p in parsed.wake.plan_requests:
        decision, reason = "new", None
        entry = doc.get(p.repo)
        if entry is None:
            decision, reason = "skipped", "repo_not_listed"
        elif not entry.enabled:
            decision, reason = "skipped", "repo_disabled"
        items.append(
            Item(
                "plan",
                p.repo,
                p.number,
                decision,
                reason,
                False,
                format_utc(p.requested_at),
            )
        )
    return items


def warnings_of(parsed: wakefiles.Parsed) -> list[str]:
    """``unknown_key:<name>`` for each extra top-level key, and a count of dropped information items."""
    out = [
        f"unknown_key:{name}" if _KEY_NAME.fullmatch(name) else "unknown_key"
        for name in parsed.parsed.warnings
    ]
    if parsed.dropped_other:
        out.append(f"malformed_info_items:{parsed.dropped_other}")
    return out


def write_rejected(root: Path | str, wake_id: str, reason: str, own_id: str) -> Path:
    """Write ``<wake_id>.rejected.json`` (the poll never writes it; there is no acknowledgment)."""
    path = wakefiles.wakes_dir(root) / f"{wake_id}.rejected.json"
    ext.write_json(
        path,
        {
            "schema": "orchestrator-wake-rejected/1",
            "wake_id": wake_id,
            "reason": reason,
            "rejected_at": format_utc(datetime.now(timezone.utc)),
            "orchestrator": own_id,
        },
    )
    return path


def check(
    root: Path | str,
    wake_id: str,
    own_id: str,
    own_tag: str | None,
    doc: repos.ReposDoc,
) -> dict[str, Any]:
    """The answer of ``wake-check``; a refusal writes ``.rejected.json`` and raises ``StateError``."""
    try:
        data = wakefiles.read_wake(root, wake_id)
        parsed = wakefiles.parse(data, wake_id, own_id, own_tag)
    except wake.WakeRejected as exc:
        ack = wakefiles.load_ack(root, wake_id)
        if (
            exc.reason == "missing" and ack is not None
        ):  # the file is gone, the answer is not
            return {"wake_id": wake_id, "already_acked": True, "ack": ack}
        write_rejected(root, wake_id, exc.reason, own_id)
        raise StateError("wake_rejected", EXIT_CONFLICT, why=exc.reason) from None
    ack = wakefiles.load_ack(root, wake_id)
    if ack is not None:
        return {"wake_id": wake_id, "already_acked": True, "ack": ack}
    items = classify(root, parsed, doc, own_id, wake_id)
    return {
        "wake_id": wake_id,
        "already_acked": False,
        "own": {"orchestrator": own_id, "tag": own_tag},
        "wake": wake.wake_to_json(parsed.wake),
        "assigned": [
            {
                "repo": i.repo,
                "number": i.number,
                "decision": i.decision,
                "reason": i.reason,
                "same_wake": i.same_wake,
                "checkout_state": i.checkout_state,
            }
            for i in items
            if i.kind == "assigned"
        ],
        "plan_requests": [
            {
                "repo": i.repo,
                "number": i.number,
                "requested_at": i.requested_at,
                "decision": i.decision,
                "reason": i.reason,
            }
            for i in items
            if i.kind == "plan"
        ],
        "rejected_items": [
            {"index": index, "reason": why} for index, why in parsed.rejected
        ],
        "dropped_info_items": parsed.dropped_other,
        "warnings": warnings_of(parsed),
    }


@click.command("wake-check")
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
def wake_check_cmd(wake_id, orchestrator, tag) -> None:
    """Read and check one wake; print it normalized, or refuse it."""

    def action() -> dict[str, Any]:
        root = common.root()
        wakefiles.valid_wake_id(wake_id)
        own_id, own_tag = ext.identity(orchestrator, tag)
        doc = repos_file.load_doc(root, ext.make_runner("wake-check"))
        return check(root, wake_id, own_id, own_tag, doc)

    common.run(action)
