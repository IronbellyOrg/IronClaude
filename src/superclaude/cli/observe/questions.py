"""Question retention for the R2 coordinator-questions panel (adapter-contract.md, "R2 onward").

A pure store with no I/O. Questions are kept by (Run, ``message.id``) until closure evidence
is seen; no closure source exists, so nothing is ever closed. A question that a later
successful read no longer returns stays, marked ``no longer in source window``. A failed
read changes nothing. The store is bounded at 1,000 records; the open total never falls, so
beyond the bound it reads ``unknown (retention exceeded)`` with the retained count.

Limit (no read marker): ``check --all`` rows carry no read or acknowledged marker, so a
question the coordinator already handled is listed again as open for as long as Orca still
returns it. ``seen`` is not ``resolved``, and neither is "handled".
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from superclaude.cli.observe.parse import UNKNOWN, Question

RETENTION_BOUND = 1000
WINDOW_ROWS = 100  # one read returning exactly this many rows may have lost older ones
NO_LONGER_IN_WINDOW = "no longer in source window"
RETENTION_EXCEEDED = "unknown (retention exceeded)"
CLOSURE_EVIDENCE = "unavailable (no source)"


@dataclass(frozen=True)
class QuestionRecord:
    key: tuple  # (Run id, message id)
    question: Question
    first_seen_cycle: int
    last_seen_cycle: int
    in_window: bool  # False: a later successful read did not return it

    @property
    def status_text(self) -> str:
        return "" if self.in_window else NO_LONGER_IN_WINDOW


@dataclass(frozen=True)
class QuestionState:
    """Immutable retained state. ``records`` are oldest created first, unknown created last."""

    records: tuple[QuestionRecord, ...] = ()
    evicted: int = 0  # records dropped at the bound; the open total counts them
    window_full: bool = False  # the last successful read returned exactly 100 rows
    last_read_cycle: int = 0  # cycle of the last successful question read; 0 = never
    identity_unknown_rows: int = (
        0  # rows of the last successful read with no id (not kept)
    )

    @property
    def retained(self) -> int:
        return len(self.records)

    @property
    def open_total(self) -> int:
        """Observed open questions: retained plus evicted. Never falls on eviction."""
        return len(self.records) + self.evicted

    @property
    def open_total_text(self) -> str:
        return RETENTION_EXCEEDED if self.evicted else str(len(self.records))

    @property
    def closure_evidence(self) -> str:
        return CLOSURE_EVIDENCE

    @property
    def never_read(self) -> bool:
        return self.last_read_cycle == 0


def _order(record: QuestionRecord) -> tuple:
    epoch = record.question.created_epoch
    known = epoch is not UNKNOWN
    return (not known, epoch if known else 0.0, str(record.key[0]), str(record.key[1]))


def _key(question: Question, run_id: Any) -> tuple:
    run = question.run_id if question.run_id is not UNKNOWN else run_id
    return (run, question.qid)


def merge_questions(
    previous: QuestionState | None,
    parsed_rows: Any,
    cycle: int,
    window_full: bool,
    source_ok: bool,
    run_id: Any = UNKNOWN,
) -> QuestionState:
    """Return the new retained state; ``previous`` is never modified.

    ``source_ok`` False (a failed read) returns ``previous`` unchanged. A row with no
    identity is counted and not retained. ``run_id`` is the Run that was read, used for a
    row that carries no ``run_id`` of its own.
    """
    state = previous if previous is not None else QuestionState()
    if not source_ok:
        return state
    seen: dict[tuple, Question] = {}
    anonymous = 0
    for question in parsed_rows:
        if question.qid is UNKNOWN or question.identity_unknown:
            anonymous += 1
            continue
        seen[_key(question, run_id)] = question
    records: dict[tuple, QuestionRecord] = {}
    for record in state.records:
        if record.key in seen:
            records[record.key] = replace(
                record,
                question=seen[record.key],
                last_seen_cycle=cycle,
                in_window=True,
            )
        else:
            records[record.key] = replace(record, in_window=False)
    for key, question in seen.items():
        if key not in records:
            records[key] = QuestionRecord(key, question, cycle, cycle, True)
    ordered = sorted(records.values(), key=_order)
    evicted = state.evicted
    if len(ordered) > RETENTION_BOUND:
        evicted += len(ordered) - RETENTION_BOUND
        ordered = ordered[-RETENTION_BOUND:]  # drop the oldest created
    return QuestionState(
        records=tuple(ordered),
        evicted=evicted,
        window_full=bool(window_full),
        last_read_cycle=cycle,
        identity_unknown_rows=anonymous,
    )


def window_is_full(raw_count: int) -> bool:
    """True when one read returned exactly 100 messages (the source gives no total)."""
    return raw_count == WINDOW_ROWS
