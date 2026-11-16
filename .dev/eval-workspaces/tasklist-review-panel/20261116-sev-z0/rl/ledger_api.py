"""The one adapter between rl/rowcheck.py and the ledger code (DESIGN 3.3, at most 40 lines).

Today the ledger code is the local `scaffold/ledgerv1.py` (Tier B, built locally). If a later build swaps it for the
sibling's file and its signatures differ, only this file changes; rowcheck.py calls nothing else.
"""

from __future__ import annotations

from scaffold import ledgerv1 as _impl


def read(report: str, assigned=None) -> dict:
    """Parse the ledger of one final message; `assigned` is a container of the row ids to accept (None: any)."""
    return _impl.read(report, assigned)


def transcript_text(events) -> str:
    """The tool results of a run (never assistant text): the corpus a `quote_other` may come from (DR-9)."""
    return _impl.transcript_text(events)


def check(rows: list[dict], corpora: dict) -> list[dict]:
    """Quote tests and support of each row; corpora is {candidate, source, transcript}."""
    return _impl.check(rows, corpora)


def link_demote(report: str, rows: list[dict], errors=(), scope=None) -> dict:
    """Link findings lines to rows and demote the unsupported blockers; returns the new text and the counts."""
    return _impl.link_demote(report, rows, errors, scope)


def promote(
    report: str, rows: list[dict], linked=(), categories=None, via_reask=False
) -> dict:
    """Add one MINOR line per PROBLEM row nothing links to; over_budget, unknown and re-asked rows are skipped."""
    return _impl.promote(report, rows, linked, categories, via_reask)
