"""Read the wake directory the way the poll writes it (design 3.1 to 3.6); shared by ``wake-check``,
``wake-ack`` and ``idle-end``.

This module only reads. The parser itself is ``issue_watch.wake.parse_wake`` (PR A), so the
poll and the orchestrator apply one set of rules. What is added here:

* a wake file or acknowledgment is found in ``wakes/`` and, once the poll has read the
  acknowledgment and moved both, in ``wakes/done/``;
* ``parse`` separates the malformed items that the poll can map back to an entry (the
  ``assigned`` items, then the ``plan_requests``, counted in that order, which is how
  ``cycle._wake_item_keys`` reads ``rejected_items``) from malformed information or
  skipped items, which have no entry and must not claim an index of one.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from superclaude.cli.issue_watch import wake
from superclaude.cli.issue_watch.predicates import WAKE_ID_PATTERN

from .state import EXIT_INVALID, StateError

DONE_DIR = "done"


def wakes_dir(root: Path | str) -> Path:
    """``<root>/.orchestrator/wakes``."""
    return Path(root) / wake.WAKES_DIR


def valid_wake_id(wake_id: object) -> str:
    """The wake id, or ``invalid_wake_id`` (exit 2): no file is named from a bad id."""
    if not isinstance(wake_id, str) or WAKE_ID_PATTERN.fullmatch(wake_id) is None:
        raise StateError("invalid_wake_id", EXIT_INVALID)
    return wake_id


def read_capped(path: Path) -> bytes:
    """Up to one byte more than a wake file may hold (the parser says ``too_large``)."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as handle:
        return handle.read(wake.MAX_WAKE_BYTES + 1)


def read_wake(root: Path | str, wake_id: str) -> bytes:
    """The bytes of the wake file; ``WakeRejected('missing')`` when there is none or it cannot be read."""
    base = wakes_dir(root)
    for folder in (base, base / DONE_DIR):
        try:
            return read_capped(folder / f"{wake_id}.json")
        except FileNotFoundError:
            continue
        except OSError:
            break  # a link, a folder or a denied read: the same as no file
    raise wake.WakeRejected("missing")


def load_ack(root: Path | str, wake_id: str) -> dict[str, Any] | None:
    """The acknowledgment of a wake as written, or None when there is none or it cannot be trusted.

    The same test as ``wake.read_ack`` (schema and wake id), on the raw document so that
    a wake already acknowledged can be answered with the very same content.
    """
    base = wakes_dir(root)
    for folder in (base, base / DONE_DIR):
        try:
            data = read_capped(folder / f"{wake_id}.ack.json")
        except FileNotFoundError:
            continue
        except OSError:
            return None
        try:
            doc = (
                json.loads(data.decode("utf-8"))
                if len(data) <= wake.MAX_WAKE_BYTES
                else None
            )
        except (ValueError, RecursionError):
            return None
        if (
            isinstance(doc, dict)
            and doc.get("schema") == wake.ACK_SCHEMA
            and doc.get("wake_id") == wake_id
        ):
            return doc
        return None
    return None


@dataclass(frozen=True)
class Parsed:
    """A parsed wake with the rejected items split by what they can be mapped to.

    ``rejected`` are the ``(index, 'malformed_item')`` of the ``assigned`` and
    ``plan_requests`` items (the indexes of ``rejected_items``); ``dropped_other`` counts
    malformed information or skipped items.
    """

    parsed: wake.ParsedWake
    rejected: tuple[tuple[int, str], ...]
    dropped_other: int

    @property
    def wake(self) -> wake.Wake:
        return self.parsed.wake


def parse(data: bytes, wake_id: str, own_id: str | None, own_tag: str | None) -> Parsed:
    """Apply ``wake.parse_wake`` (``WakeRejected`` carries the closed reason of a whole-wake refusal)."""
    name = f"{wake_id}.json"
    full = wake.parse_wake(data, name, own_id=own_id, own_tag=own_tag)
    raw = json.loads(data.decode("utf-8"))
    raw["info"] = {key: [] for key in ("mentions", "could_assign", "affects")}
    raw["skipped"] = []
    mapped = wake.parse_wake(
        json.dumps(raw).encode("utf-8"), name, own_id=own_id, own_tag=own_tag
    )
    return Parsed(full, mapped.rejected, len(full.rejected) - len(mapped.rejected))
