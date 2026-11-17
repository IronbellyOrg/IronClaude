"""Mechanical checks over the lines a fix pass edited (L2 of the blocker work).

Read-only: it opens files to read and writes nothing. It returns one result per check it ran,
passes included, so the fix log is complete. Checks:

- pipe: a markdown table row has as many unescaped pipes as the table's header row (an edited
  header is compared with the separator row); the optional outer pipes are normalized.
- range: a requested line number outside the file is reported, not skipped.
- quote: `"quoted text"` followed by a `path:line` cite is byte-present on that cited line.
- count: a line saying `N rows` right above a table matches the table's data row count.
- link: a relative markdown link `[text](path)` points at a file or folder that exists.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

_PIPE = re.compile(r"(?<!\\)\|")
_QUOTE_CITE = re.compile(r"\"([^\"\n]{8,})\"\s*\(?\s*`?([\w./-]+\.\w+):(\d+)")
_ROWS = re.compile(r"\b(\d+) rows\b")
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


@dataclass(frozen=True)
class CheckResult:
    check: str
    file: str
    line: int  # 1-based line in the edited file
    ok: bool
    detail: str


def parse_range(text: str) -> list[int]:
    """`5-9` -> [5..9]; `7` -> [7]. Raises ValueError on anything else."""
    start, _, end = text.partition("-")
    first, last = int(start), int(end or start)
    if first < 1 or last < first:
        raise ValueError(f"bad line range {text!r}")
    return list(range(first, last + 1))


def edited_lines(base_text: str, new_text: str) -> list[int]:
    """1-based numbers of lines in new_text that are new or changed against base_text."""
    old, new = base_text.splitlines(), new_text.splitlines()
    out: list[int] = []
    for tag, _i1, _i2, j1, j2 in difflib.SequenceMatcher(None, old, new).get_opcodes():
        if tag in ("replace", "insert"):
            out.extend(range(j1 + 1, j2 + 1))
    return out


def _table_block(lines: list[str], n: int) -> tuple[int, int]:
    """Index range [first, last] of the run of `|` lines holding index n."""
    first = n
    while first > 0 and lines[first - 1].lstrip().startswith("|"):
        first -= 1
    last = n
    while last + 1 < len(lines) and lines[last + 1].lstrip().startswith("|"):
        last += 1
    return first, last


def _pipes(row: str) -> int:
    """Unescaped pipes the row would hold with both optional outer pipes present."""
    text = row.strip()
    inner = len(_PIPE.findall(text))
    if _PIPE.match(text):
        inner -= 1  # leading pipe
    if len(text) > 1 and re.search(r"(?<!\\)\|$", text):
        inner -= 1  # trailing pipe
    return inner + 2


def _cited_text(cite: str, line: int, base: Path) -> str | None:
    for candidate in (Path(cite), base.parent / cite):
        if candidate.is_file():
            rows = candidate.read_text(encoding="utf-8", errors="replace").splitlines()
            return rows[line - 1] if 1 <= line <= len(rows) else ""
    return None


def run_checks(path: str | Path, line_numbers: list[int]) -> list[CheckResult]:
    """Run every check that applies to the given 1-based lines of the file."""
    file = Path(path)
    lines = file.read_text(encoding="utf-8").splitlines()
    name = str(path)
    results: list[CheckResult] = []
    for number in sorted(set(line_numbers)):
        if not 1 <= number <= len(lines):
            results.append(
                CheckResult(
                    "range",
                    name,
                    number,
                    False,
                    f"line {number} is outside the file ({len(lines)} lines)",
                )
            )
            continue
        idx, row = number - 1, lines[number - 1]
        if row.lstrip().startswith("|"):
            first, last = _table_block(lines, idx)
            got = _pipes(row)
            if idx == first and last > first:
                # The edited row is the header: compare it with the separator row
                # below it, not with itself.
                want, against = _pipes(lines[first + 1]), "separator row"
            else:
                want, against = _pipes(lines[first]), "header row"
            results.append(
                CheckResult(
                    "pipe",
                    name,
                    number,
                    got == want,
                    f"{got} unescaped pipes, {against} has {want}",
                )
            )
        for quote, cite, cited_line in _QUOTE_CITE.findall(row):
            text = _cited_text(cite, int(cited_line), file)
            if text is None:
                results.append(
                    CheckResult(
                        "quote", name, number, False, f"cited file {cite} not found"
                    )
                )
            else:
                present = quote in text
                results.append(
                    CheckResult(
                        "quote",
                        name,
                        number,
                        present,
                        f"quote {'found' if present else 'not found'} at {cite}:{cited_line}",
                    )
                )
        counted = _ROWS.search(row)
        if counted and idx + 1 < len(lines) and lines[idx + 1].lstrip().startswith("|"):
            first, last = _table_block(lines, idx + 1)
            data_rows = max(last - first + 1 - 2, 0)  # minus header and separator
            results.append(
                CheckResult(
                    "count",
                    name,
                    number,
                    data_rows == int(counted.group(1)),
                    f"says {counted.group(1)} rows, the table below has {data_rows}",
                )
            )
        for target in _LINK.findall(row):
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            bare = unquote(target.split("#", 1)[0])
            exists = bool(bare) and (file.parent / bare).exists()
            results.append(
                CheckResult(
                    "link",
                    name,
                    number,
                    exists,
                    f"{target} {'exists' if exists else 'does not exist'}",
                )
            )
    return results
