"""The screen renderer: a ``View`` and a ``TerminalPolicy`` become Rich renderables (AD-11, AD-13).

It only lays out and truncates. Every status literal and both row orders come from the
``View``; every truncation goes through ``terminal.clip``; text is built as ``rich.text.Text``
from data (never markup strings). It never imports the adapter or the collector.
"""

from __future__ import annotations

from rich.cells import cell_len
from rich.console import Group
from rich.text import Text

from superclaude.cli.observe.terminal import (
    TOO_NARROW_TEXT,
    TOO_SMALL_TEXT,
    TerminalPolicy,
    ascii_safe,
    clip,
    glyph,
)
from superclaude.cli.observe.view import (
    INSPECTOR_ABOVE_TEXT,
    INSPECTOR_BELOW_TEXT,
    INSPECTOR_HELP,
    INSPECTOR_TITLE,
    NO_MATCH_TEXT,
    CountsToken,
    RowView,
    View,
    text_of,
)

MAX_COUNT_LINES = 2  # the COUNTS strip wraps to a second line before anything is cut
SEPARATOR = " "


# -- text fitting ------------------------------------------------------------------------------


def _prefix_length(text: str, width: int) -> int:
    """Largest number of characters of ``text`` that fit in ``width`` cells."""
    used = 0
    for index, ch in enumerate(text):
        step = cell_len(ch)
        if used + step > width:
            return index
        used += step
    return len(text)


def wrap(text: str, width: int, policy: TerminalPolicy) -> list[str]:
    """Wrap by cells without losing anything (never truncates; never splits a wide character)."""
    if policy.ascii:
        text = ascii_safe(text)
    if width <= 0:
        return [""]
    lines: list[str] = []
    for paragraph in text.split("\n"):
        while cell_len(paragraph) > width:
            cut = max(_prefix_length(paragraph, width), 1)
            space = paragraph[:cut].rfind(" ")
            if space > 0 and paragraph[:space].strip() and cut < len(paragraph):
                lines.append(paragraph[:space].rstrip())
                paragraph = paragraph[space:].lstrip(" ")
            else:
                lines.append(paragraph[:cut])
                paragraph = paragraph[cut:]
        lines.append(paragraph)
    return lines


def _pad(text: str, width: int) -> str:
    return text + " " * max(width - cell_len(text), 0)


def _cell(text: str, width: int, policy: TerminalPolicy) -> str:
    return _pad(clip(text, width, policy), width)


# -- the COUNTS strip ------------------------------------------------------------------------------


def counts_lines(
    tokens: tuple[CountsToken, ...],
    policy: TerminalPolicy,
    max_lines: int | None = MAX_COUNT_LINES,
) -> list[str]:
    """Lay tokens out in priority order. Protected tokens are never truncated: they wrap.

    Lower-priority tokens that do not fit within ``max_lines`` are cut with ``>``.
    """
    width = policy.width
    lines: list[str] = []
    current = ""
    cut = False
    for token in tokens:
        text = ascii_safe(token.text) if policy.ascii else token.text
        if cut and not token.protected:
            continue
        candidate = f"{current}  {text}" if current else text
        if cell_len(candidate) <= width:
            current = candidate
            continue
        if token.protected:
            if current:
                lines.append(current)
            chunks = wrap(text, width, policy)
            lines.extend(chunks[:-1])
            current = chunks[-1]
            continue
        if max_lines is None or len(lines) + 1 < max_lines:
            if current:
                lines.append(current)
            current = clip(text, width, policy)
            continue
        room = width - cell_len(current) - 2
        if room >= 2:
            current = f"{current}  {clip(text, room, policy)}"
        else:
            current = clip(current + " " + glyph("truncate", policy), width, policy)
        cut = True
    if current:
        lines.append(current)
    return lines


# -- ledger rows -----------------------------------------------------------------------------------------


def _flags_text(row: RowView) -> str:
    return ", ".join(row.flags)  # the view owns every marker, FROZEN included


def _marker(row: RowView, policy: TerminalPolicy) -> str:
    return (glyph("selected", policy) if row.selected else " ") + (
        "*" if row.changed else " "
    )


def _verdict(row: RowView) -> str:
    return text_of(row.raw.liveness_verdict)


def _columns(policy: TerminalPolicy) -> tuple[list[tuple[str, int]], list]:
    """Column (header, width) pairs and one getter per column, for the width class."""
    width = policy.width
    sep = len(SEPARATOR)
    if policy.width_class == "full":
        fixed = [12, 12, 14, 14, 12, 16, 22, 12]  # run .. evidence age
        flags_min = 12
        base = 2 + sum(fixed) + flags_min + sep * 10
        extra = max(width - base - 22, 0)
        id_width = 22 + min(extra, 26)
        flags_width = width - (2 + sum(fixed) + sep * 10) - id_width
        names = [
            ("", 2),
            ("dispatchId", id_width),
            ("run", fixed[0]),
            ("workerState", fixed[1]),
            ("dispatchStatus", fixed[2]),
            ("terminalState", fixed[3]),
            ("outcome", fixed[4]),
            ("nextAction.kind", fixed[5]),
            ("liveness", fixed[6]),
            ("evidence age", fixed[7]),
            ("flags", flags_width),
        ]
        getters = [
            None,
            lambda r: r.dispatch_id,
            lambda r: r.run,
            lambda r: r.worker_state,
            lambda r: r.dispatch_status,
            lambda r: r.terminal_state,
            lambda r: r.outcome,
            lambda r: r.next_action,
            lambda r: r.liveness,
            lambda r: r.evidence_age,
            _flags_text,
        ]
        return names, getters
    if policy.width_class == "line":
        kind, verdict, age = 18, 14, 7
        id_width = min(width - (2 + kind + verdict + age + 18 + sep * 5), 60)
        flags_width = width - (2 + kind + verdict + age + id_width + sep * 5)
        names = [
            ("", 2),
            ("kind", kind),
            ("dispatchId", id_width),
            ("liveness", verdict),
            ("age", age),
            ("flags", flags_width),
        ]
        getters = [
            None,
            lambda r: r.next_action,
            lambda r: r.dispatch_id,
            _verdict,
            lambda r: r.evidence_age,
            _flags_text,
        ]
        return names, getters
    kind, age, flags_width = 14, 6, 16
    id_width = width - (2 + kind + age + flags_width + sep * 4)
    names = [
        ("", 2),
        ("kind", kind),
        ("dispatchId", id_width),
        ("age", age),
        ("flags", flags_width),
    ]
    getters = [
        None,
        lambda r: r.next_action,
        lambda r: r.dispatch_id,
        lambda r: r.evidence_age,
        _flags_text,
    ]
    return names, getters


def _row_line(
    row: RowView, columns: list[tuple[str, int]], getters: list, policy: TerminalPolicy
) -> str:
    cells = []
    for (_, width), getter in zip(columns, getters, strict=True):
        cells.append(
            _pad(_marker(row, policy), width)
            if getter is None
            else _cell(getter(row), width, policy)
        )
    return clip(SEPARATOR.join(cells).rstrip(), policy.width, policy)


def _header_lines(columns: list[tuple[str, int]], policy: TerminalPolicy) -> list[str]:
    head = SEPARATOR.join(_cell(name, width, policy) for name, width in columns)
    rule = SEPARATOR.join(glyph("hrule", policy) * width for _, width in columns)
    return [clip(head.rstrip(), policy.width, policy), clip(rule, policy.width, policy)]


# -- screens -------------------------------------------------------------------------------------------------


def _inspector_lines(
    view: View, policy: TerminalPolicy, budget: int
) -> list[str]:
    """The title, then whole fields from ``view.inspector_scroll`` on while they fit ``budget`` lines.

    Hidden fields are counted in an "above" and a "below" line, so every field stays reachable (d/u).
    """
    selected = view.selected
    title = f"{INSPECTOR_TITLE}  {selected.dispatch_id if selected else ''}"
    lines = wrap(title, policy.width, policy)
    blocks: list[list[str]] = []
    for label, value in view.inspector or ():
        first, *rest = wrap(f"{label}: {value}", policy.width, policy)
        block = [first]
        for continuation in rest:  # continuation lines are indented two cells
            block.extend(
                "  " + part
                for part in wrap(continuation, max(policy.width - 2, 1), policy)
            )
        blocks.append(block)
    start = min(max(view.inspector_scroll, 0), max(len(blocks) - 1, 0))
    if start:
        lines += wrap(INSPECTOR_ABOVE_TEXT.format(n=start), policy.width, policy)
    room = budget - len(lines)
    shown = 0
    for index, block in enumerate(blocks[start:], start):
        last = index == len(blocks) - 1
        need = len(block) + (0 if last else 1)  # keep one line for the "below" text
        if shown and need > room:
            break
        lines += block
        room -= len(block)
        shown += 1
    hidden = len(blocks) - start - shown
    if hidden:
        lines += wrap(INSPECTOR_BELOW_TEXT.format(n=hidden), policy.width, policy)
    return lines


def _notes(view: View) -> list[str]:
    parts = [
        n
        for n in (
            view.filter_line,
            view.historical_note,
            view.duplicates_note,
            view.selection_note,
        )
        if n
    ]
    return ["  ".join(parts)] if parts else []


def screen_lines(
    view: View, policy: TerminalPolicy, message: str | None = None
) -> list[str]:
    """The screen as plain lines, each at most ``policy.width`` cells wide.

    ``message`` is a one-off notice from the command loop (an export result); it sits above the footer.
    """
    width = policy.width
    if (
        policy.too_narrow
    ):  # below 80 columns: the denominators and the gap notice still print
        lines = wrap(TOO_NARROW_TEXT, width, policy)
        lines += counts_lines(view.counts_tokens, policy, max_lines=None)
        return lines + wrap(view.gap_notice, width, policy)
    if policy.too_small:
        lines = wrap(TOO_SMALL_TEXT, width, policy)
        lines += wrap(view.collected_text, width, policy)
        return lines + wrap(view.gap_notice, width, policy)

    top: list[str] = []
    top += wrap(view.header1, width, policy)
    top += wrap(view.header2, width, policy)
    top += counts_lines(view.counts_tokens, policy)
    if view.changes_line:
        top += wrap(view.changes_line, width, policy)
    top += wrap(view.gap_notice, width, policy)
    for note in _notes(view):
        top += wrap(note, width, policy)
    if view.focus == "filter":
        top += wrap("/" + view.filter_text, width, policy)
    if message:
        top += wrap(message, width, policy)

    # The footer is one line when it fits, else the key list and the counts on two lines.
    window_probe = view.window(None)
    one_line = view.footer(window_probe)
    footer_height = (
        1
        if cell_len(one_line) <= width
        else 1 + len(wrap(view.footer_counts(window_probe), width, policy))
    )

    if view.focus == "inspector" and view.inspector is not None:
        footer_lines = [clip(INSPECTOR_HELP, width, policy)]
        body = _inspector_lines(
            view, policy, max(policy.height - len(top) - len(footer_lines), 1)
        )
        return top + body + footer_lines

    body = wrap(view.ledger_title, width, policy)
    columns, getters = _columns(policy)
    if policy.width_class == "full" and view.visible_rows:
        body += _header_lines(columns, policy)
    reserved = (
        len(top) + len(body) + footer_height + 1
    )  # one line kept for the overflow text
    capacity = max(policy.height - reserved, 1)
    window = view.window(capacity)
    if not view.all_rows:
        for text in view.ledger_empty:
            body += wrap(text, width, policy)
    elif not window.rows:
        body += wrap(NO_MATCH_TEXT, width, policy)
    for row in window.rows:
        body.append(_row_line(row, columns, getters, policy))
    if window.more:
        body += wrap(f"{window.text}  {window.more_text}", width, policy)

    footer = view.footer(window)
    if cell_len(footer) <= width:
        footer_lines = [footer if not policy.ascii else ascii_safe(footer)]
    else:
        footer_lines = [clip(view.help_line, width, policy)] + wrap(
            view.footer_counts(window), width, policy
        )
    return top + body + footer_lines


def render(view: View, policy: TerminalPolicy, message: str | None = None) -> Group:
    """The screen as Rich renderables: one plain ``Text`` per line, never reflowed."""
    return Group(
        *(
            Text(line, no_wrap=True, overflow="crop")
            for line in screen_lines(view, policy, message)
        )
    )
