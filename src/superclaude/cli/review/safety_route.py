"""Safety scan of plain row text (GR1 vocabulary) and the raise-only outcome rule (GR12).

The scan reads one row per line and reports rows that hold destructive or secret
vocabulary. It stores nothing and calls nothing: it only reports. The outcome rule can
raise an outcome and never lowers one, so a hit is never a plain follow-up.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Outcomes in their fixed order, defined once. A higher index is a higher outcome.
OUTCOMES = ("Note", "Medium", "Blocking")

# The GR1 vocabulary, kept in this one list and nowhere else. A word matches
# case-insensitively at the start of a word: "deleted" and "tokens" hit, "reinforce" does not.
VOCABULARY = (
    "delete",
    "overwrite",
    "force",
    "token",
    "secret",
    "password",
    "chmod",
    "credential",
    "wipe",
)

_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(w) for w in VOCABULARY) + ")",
    re.IGNORECASE,
)

# A row that starts with this prefix is history: skipped and counted, never scanned.
SUPERSEDED_PREFIX = "superseded "


@dataclass(frozen=True)
class Hit:
    line: int  # 1-based line number in the input
    word: str  # the matched vocabulary word, as written in the row
    row: str  # the row text


@dataclass(frozen=True)
class ScanResult:
    hits: tuple[Hit, ...]
    rows_read: int
    rows_skipped: int
    empty: bool  # the input held no text at all (only whitespace)


@dataclass(frozen=True)
class Unreadable:
    """The input could not be read. Different from a read that found zero hits."""

    path: str
    reason: str


def scan_text(text: str) -> ScanResult:
    """Scan plain row text, one row per line. Blank lines are not rows."""
    hits: list[Hit] = []
    rows_read = 0
    rows_skipped = 0
    for number, raw in enumerate(text.splitlines(), start=1):
        row = raw.strip()
        if not row:
            continue
        if row.startswith(SUPERSEDED_PREFIX):
            rows_skipped += 1
            continue
        rows_read += 1
        found = _PATTERN.search(row)
        if found:
            hits.append(Hit(line=number, word=found.group(1), row=row))
    return ScanResult(
        hits=tuple(hits),
        rows_read=rows_read,
        rows_skipped=rows_skipped,
        empty=not text.strip(),
    )


def scan_file(path: str | Path) -> ScanResult | Unreadable:
    """Read a file as UTF-8 and scan it; an unreadable input is its own result."""
    name = str(path)
    try:
        data = Path(path).read_bytes()
    except FileNotFoundError:
        return Unreadable(name, "no such file")
    except IsADirectoryError:
        return Unreadable(name, "is a directory")
    except OSError as exc:
        return Unreadable(name, exc.strerror or "unreadable")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return Unreadable(name, "not valid UTF-8")
    return scan_text(text)


def raise_outcome(graded: str, has_hit: bool) -> str:
    """GR12: a row with a hit becomes Blocking; otherwise the graded outcome stands.

    The result is never below the graded outcome.
    """
    if graded not in OUTCOMES:
        raise ValueError(f"unknown outcome {graded!r}; expected one of {OUTCOMES}")
    if not has_hit:
        return graded
    return max(graded, OUTCOMES[-1], key=OUTCOMES.index)
