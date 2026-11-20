"""The questions that were asked of Clay: ``.orchestrator/questions/<entry id>.json`` (design 5.6).

``answer-check`` needs to know, for the entry an answer says it belongs to, the question
key that ``escalate`` recorded, the time of the entry's last edit, the time of its notice
and the options that may be answered with a bare number. The design says each question
gets its own entry id (finding F48 of issue 675) and that the key is "recorded with the
entry" but names no file, so this is that record: one small file for each asked question,
written by ``escalate`` (B4a) through ``record_question`` and read by ``answer_check``.

Fields: ``schema``, ``entry_id``, ``question_key`` (``<issue>:<row>:<question>`` or
``merge_safety:<PR>:<head sha>``), ``issue`` (``owner/repo#N`` or null), ``row`` (1 to 9, the
row of the table of 5.6), ``low_stakes`` (the option numbers a bare number may answer; empty
for rows 1 to 7, which never hold a low-stakes option), ``created_at``, ``edited_at`` and
``notified_at`` (UTC). A rerun with the same fields is not a new ask. An entry id is
``[A-Za-z0-9._-]{1,100}``.
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from superclaude.cli.issue_watch.predicates import format_utc, parse_utc
from superclaude.cli.issue_watch.route import STATE_DIR

from . import ext, state
from .state import (
    EXIT_CONFLICT,
    EXIT_INVALID,
    EXIT_NOT_FOUND,
    EXIT_UNREADABLE,
    StateError,
)

QUESTION_SCHEMA: Final = "orchestrator-question/1"
QUESTIONS_DIR: Final = "questions"
NO_LOW_STAKES_ROWS: Final = range(1, 8)
"""Rows 1 to 7 of 5.6 never hold a low-stakes option."""

ENTRY_ID = re.compile(r"[A-Za-z0-9._-]{1,100}")
KEY = re.compile(r"[ -~]{1,300}")


def question_path(root: Path | str, entry_id: str) -> Path:
    """``<root>/.orchestrator/questions/<entry id>.json``."""
    if ENTRY_ID.fullmatch(entry_id) is None:
        raise StateError("invalid_entry_id", EXIT_INVALID)
    return Path(root) / STATE_DIR / QUESTIONS_DIR / f"{entry_id}.json"


def _check(doc: object) -> dict[str, Any]:
    ok = (
        isinstance(doc, dict)
        and doc.get("schema") == QUESTION_SCHEMA
        and isinstance(doc.get("entry_id"), str)
        and ENTRY_ID.fullmatch(doc["entry_id"]) is not None
        and isinstance(doc.get("question_key"), str)
        and KEY.fullmatch(doc["question_key"]) is not None
        and type(doc.get("row")) is int
        and 1 <= doc["row"] <= 9
        and isinstance(doc.get("low_stakes"), list)
        and all(type(n) is int and 0 < n < 100 for n in doc["low_stakes"])
        and all(
            isinstance(doc.get(k), str)
            for k in ("created_at", "edited_at", "notified_at")
        )
    )
    if ok:
        try:
            for name in ("created_at", "edited_at", "notified_at"):
                parse_utc(doc[name])  # type: ignore[index]
        except ValueError:
            ok = False
    if not ok:
        raise StateError("question_unreadable", EXIT_UNREADABLE)
    assert isinstance(doc, dict)
    return doc


def load_question(root: Path | str, entry_id: str) -> dict[str, Any]:
    """Read one question record (``question_not_found`` or ``question_unreadable``)."""
    try:
        with open(question_path(root, entry_id), "rb") as handle:
            data = handle.read(65537)
    except FileNotFoundError:
        raise StateError("question_not_found", EXIT_NOT_FOUND) from None
    except OSError:
        raise StateError("question_unreadable", EXIT_UNREADABLE) from None
    try:
        doc = json.loads(data.decode("utf-8")) if len(data) <= 65536 else None
    except (ValueError, RecursionError):
        doc = None
    return _check(doc)


def record_question(
    root: Path | str,
    entry_id: str,
    *,
    question_key: str,
    row: int,
    issue: str | None = None,
    low_stakes: Sequence[int] = (),
    now: datetime | None = None,
) -> tuple[dict[str, Any], bool]:
    """Record a question; ``(record, created)``. A rerun with the same fields returns the old record.

    A different key, row or issue under an id that exists is ``entry_id_taken`` (exit 3).
    A low-stakes option on a row from 1 to 7 is refused (``low_stakes_not_allowed``).
    """
    stamp = format_utc(now if now is not None else datetime.now(timezone.utc))
    if row in NO_LOW_STAKES_ROWS and list(low_stakes):
        raise StateError("low_stakes_not_allowed", EXIT_INVALID)
    doc = {
        "schema": QUESTION_SCHEMA,
        "entry_id": entry_id,
        "question_key": question_key,
        "issue": issue,
        "row": row,
        "low_stakes": sorted(set(low_stakes)),
        "created_at": stamp,
        "edited_at": stamp,
        "notified_at": stamp,
    }
    _check(doc)
    path = question_path(root, entry_id)
    with state.locked(root):
        try:
            old = load_question(root, entry_id)
        except StateError as exc:
            if exc.reason != "question_not_found":
                raise
        else:
            same = all(
                old[k] == doc[k] for k in ("question_key", "issue", "row", "low_stakes")
            )
            if not same:
                raise StateError("entry_id_taken", EXIT_CONFLICT)
            return old, False
        ext.write_json(path, doc)
    return doc, True


def touch(
    root: Path | str,
    entry_id: str,
    *,
    edited: bool = False,
    notified: bool = False,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Move ``edited_at`` and, or, ``notified_at`` to now (an answer must be newer than both)."""
    stamp = format_utc(now if now is not None else datetime.now(timezone.utc))
    with state.locked(root):
        doc = load_question(root, entry_id)
        if edited:
            doc["edited_at"] = stamp
        if notified:
            doc["notified_at"] = stamp
        ext.write_json(question_path(root, entry_id), doc)
    return doc


__all__ = ["load_question", "question_path", "record_question", "touch"]
