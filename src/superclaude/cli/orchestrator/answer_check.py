"""The verb ``superclaude orchestrator answer-check``: is this answer really Clay's, for this question (design 5.6).

    answer-check --entry <id> --source <session|clickup-dm> --answered-at <UTC time>
                 [--question-key <key>] [--answer-text-file <file>]
                 [--reply-to <entry id>] [--sender-id <ClickUp user id>]

It passes only when all of these hold, and prints each result (a fourth with a question
key, a fifth for a bare number):

1. ``source``: the source is Clay's. ``session`` is input typed in the orchestrator's own
   terminal by a person (FR-17's accepted v1 guard); ``clickup-dm`` is a ClickUp DM reply
   whose ``--sender-id`` equals Clay's ClickUp user id, read from the environment variable
   ``ORCHESTRATOR_CLAY_CLICKUP_ID`` (UNVERIFIED U36: how a reply's author is read back, and
   where Clay's id is kept, is not designed; with no id set a DM never passes). Any other
   source, an answer relayed by another agent included, is refused.
2. ``entry``: it names the right entry: the entry id appears in the answer text, or the
   answer is a reply in that entry's thread (``--reply-to`` names that entry). The entry
   must be one that ``escalate`` recorded (``questions.record_question``).
3. ``newer``: ``--answered-at`` is later than the entry's last edit and than its notice.
4. ``key`` (only with ``--question-key``): the key equals, exactly, the key recorded for the
   answered question, so an answer to another question never stands for this one.
5. ``option`` (only when the answer is a bare number): the number is a low-stakes option of
   that entry. A bare number answers a low-stakes option only.

Every run writes a row to the action log (``actions.jsonl``), accepted or refused, and prints
its id as ``ref``. A caller that must show Clay's word, such as ``repos`` and the merge gate,
takes that id as ``--answer-ref`` and checks it with ``require_accepted``; a refused row
never passes. A refused answer exits 3 and leaves the item waiting.

THE LIMIT (finding F25 of issue 675): this verb checks only what its caller passes it. It
cannot tell a person's typed text from text the model typed itself, nor read who really
sent a ClickUp reply. The guard is the rule that the caller passes an answer exactly as it
arrived and never as the model's own words, plus these checks on its shape. It is a check
on mistakes and on relayed answers, not a lock against a determined model.
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

import click

from superclaude.cli.issue_watch.predicates import parse_utc

from . import actions, common, questions
from .state import EXIT_CONFLICT, EXIT_INVALID, StateError

SOURCES: Final = ("session", "clickup-dm")
CLAY_CLICKUP_ENV: Final = "ORCHESTRATOR_CLAY_CLICKUP_ID"
MAX_ANSWER_BYTES: Final = 64 * 1024

_BARE_NUMBER = re.compile(r"[0-9]{1,2}")
_SENDER = re.compile(r"[A-Za-z0-9._:-]{1,64}")
_SOURCE = re.compile(r"[A-Za-z0-9._-]{1,40}")


def _names_entry(text: str | None, reply_to: str | None, entry: str) -> bool:
    if reply_to is not None and reply_to == entry:
        return True
    if text is None:
        return False
    pattern = r"(?<![A-Za-z0-9._-])" + re.escape(entry) + r"(?![A-Za-z0-9._-])"
    return re.search(pattern, text) is not None


def check(
    root: Path | str,
    *,
    entry: str,
    source: str,
    answered_at: str,
    question_key: str | None = None,
    answer_text: str | None = None,
    reply_to: str | None = None,
    sender_id: str | None = None,
    env: Mapping[str, str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Check one answer, write the action row and return ``{accepted, ref, results}``."""
    if questions.ENTRY_ID.fullmatch(entry) is None:
        raise StateError("invalid_entry_id", EXIT_INVALID)
    answered = parse_utc(answered_at)
    clay_id = (os.environ if env is None else env).get(CLAY_CLICKUP_ENV)
    try:
        record: dict[str, Any] | None = questions.load_question(root, entry)
    except StateError as exc:
        if exc.reason != "question_not_found":
            raise
        record = None

    text = answer_text.strip() if answer_text is not None else None
    bare = text if text is not None and _BARE_NUMBER.fullmatch(text) else None
    results: dict[str, bool] = {
        "source": source == "session"
        or (
            source == "clickup-dm"
            and bool(clay_id)
            and sender_id is not None
            and _SENDER.fullmatch(sender_id) is not None
            and sender_id == clay_id
        ),
        "entry": record is not None and _names_entry(text, reply_to, entry),
        "newer": record is not None
        and answered > parse_utc(record["edited_at"])
        and answered > parse_utc(record["notified_at"]),
    }
    if question_key is not None:
        results["key"] = record is not None and record["question_key"] == question_key
    if bare is not None:
        results["option"] = record is not None and int(bare) in record["low_stakes"]
    accepted = all(results.values())
    ref = actions.append(
        root,
        "answer-check",
        now=now,
        entry=entry,
        source=source if _SOURCE.fullmatch(source) else "invalid",
        answered_at=answered_at,
        question_key=(
            question_key
            if question_key is None or questions.KEY.fullmatch(question_key)
            else "invalid"
        ),
        results=results,
        accepted=accepted,
    )
    return {"accepted": accepted, "ref": ref, "results": results}


def require_accepted(
    root: Path | str, ref: object, question_key: str | None = None
) -> dict[str, Any]:
    """The action row of an accepted ``answer-check`` with id ``ref``, or a refusal (exit 2).

    ``answer_ref_unknown``: no such answer-check row. ``answer_ref_rejected``: the row is a
    refused answer. With ``question_key`` the row must also have been checked for that
    exact key (``answer_ref_key_mismatch``), so an OK for one question never opens another.
    """
    row = actions.find(root, ref)
    if row is None or row.get("kind") != "answer-check":
        raise StateError("answer_ref_unknown", EXIT_INVALID)
    if row.get("accepted") is not True:
        raise StateError("answer_ref_rejected", EXIT_INVALID)
    if question_key is not None and row.get("question_key") != question_key:
        raise StateError("answer_ref_key_mismatch", EXIT_INVALID)
    return row


def _read_text(path: Path) -> str:
    try:
        with open(path, "rb") as handle:
            data = handle.read(MAX_ANSWER_BYTES + 1)
        if len(data) > MAX_ANSWER_BYTES:
            raise ValueError("answer too large")
        return data.decode("utf-8")
    except OSError:
        raise StateError("answer_text_unreadable", EXIT_INVALID) from None


@click.command("answer-check")
@click.option("--entry", required=True, help="The entry id the answer belongs to.")
@click.option(
    "--source", required=True, help="session (typed here by a person) or clickup-dm."
)
@click.option(
    "--answered-at",
    required=True,
    help="When it was answered, UTC like 2026-11-19T10:00:00Z.",
)
@click.option(
    "--question-key",
    default=None,
    help="The question key the answer must match exactly.",
)
@click.option(
    "--answer-text-file",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="The answer exactly as it arrived (the entry id must appear in it, or use --reply-to).",
)
@click.option(
    "--reply-to", default=None, help="The entry whose thread the answer was a reply in."
)
@click.option(
    "--sender-id", default=None, help="The ClickUp user id of the author (clickup-dm)."
)
def answer_check_cmd(
    entry, source, answered_at, question_key, answer_text_file, reply_to, sender_id
) -> None:
    """Check that an answer is Clay's, names this entry, is newer and matches the question key."""

    def action() -> dict[str, Any]:
        text = _read_text(answer_text_file) if answer_text_file is not None else None
        result = check(
            common.root(),
            entry=entry,
            source=source,
            answered_at=answered_at,
            question_key=question_key,
            answer_text=text,
            reply_to=reply_to,
            sender_id=sender_id,
            now=datetime.now(timezone.utc),
        )
        if not result["accepted"]:
            raise StateError(
                "answer_refused",
                EXIT_CONFLICT,
                ref=result["ref"],
                results=result["results"],
            )
        return result

    common.run(action)
