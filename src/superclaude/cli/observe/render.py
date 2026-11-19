"""The screen renderer: a ``View`` and a ``TerminalPolicy`` become Rich renderables (AD-11, AD-13).

It only lays out and truncates. Every status literal and both row orders come from the
``View``; every truncation goes through ``terminal.clip``; text is built as ``rich.text.Text``
from data (never markup strings). It never imports the adapter or the collector.

Each screen line is a ``Line``: its plain text (the source of truth for the record, the goldens
and every test) plus colour roles that ``render`` turns into styles for the terminal's colour
depth. Roles are attached where a builder already knows what a piece of text is; no pattern is
matched over worker-controlled text.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import zip_longest

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
from superclaude.cli.observe.theme import FROZEN_ROLE, STATE_ROLE, style_for
from superclaude.cli.observe.view import (
    ABSENT_IN_SOURCE,
    DESK_EVIDENCE_TITLE,
    DESK_HIDDEN,
    DESK_SELECTED_HIDDEN,
    DESK_TEXT_LINES,
    DESK_TITLE,
    DESK_WORKTREE_NOTE,
    FROZEN_MARKER,
    INSPECTOR_ABOVE_TEXT,
    INSPECTOR_BELOW_TEXT,
    INSPECTOR_HELP,
    INSPECTOR_TITLE,
    LEDGER_LEGEND,
    NO_MATCH_TEXT,
    QUESTIONS_COUNT_LABEL,
    QUESTIONS_REASON,
    QUESTIONS_REASONS_NOTE,
    QUESTIONS_TITLE,
    READ_ONLY_BADGE,
    RETAIN_TITLE,
    UNAVAILABLE,
    CountsToken,
    DeskView,
    QuestionLine,
    QuestionsPanel,
    RowView,
    View,
    text_of,
)

MAX_COUNT_LINES = 2  # the COUNTS strip wraps to a second line before anything is cut
DESK_STUB_CELLS = 24  # the selected list row shows at most this much question text
DESK_LABEL_CELLS = (
    9  # the label column of the desk pane (wider only for raw field names)
)
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


def wrap_groups(text: str, width: int, policy: TerminalPolicy) -> list[str]:
    """Wrap a key list on its two-space separators: whole groups are packed greedily into lines
    joined by two spaces, so no key pair is ever split. Only a single group wider than the width
    falls back to ``wrap``."""
    if policy.ascii:
        text = ascii_safe(text)
    groups = [g for g in text.split("  ") if g]
    lines: list[str] = []
    current = ""
    for group in groups:
        candidate = f"{current}  {group}" if current else group
        if cell_len(candidate) <= width:
            current = candidate
            continue
        if current:
            lines.append(current)
            current = ""
        if cell_len(group) <= width:
            current = group
        else:
            chunks = wrap(group, width, policy)
            lines.extend(chunks[:-1])
            current = chunks[-1]
    if current or not lines:
        lines.append(current)
    return lines


def _pad(text: str, width: int) -> str:
    return text + " " * max(width - cell_len(text), 0)


# -- lines with colour roles ---------------------------------------------------------------------


@dataclass(frozen=True)
class Span:
    """A role over ``plain[start:end]``. Offsets count characters, never cells (a wide character
    is two cells but one character), so they stay valid whatever the terminal width."""

    start: int
    end: int
    role: str


@dataclass(frozen=True)
class Line:
    """One screen line: its plain text (the source of truth for every test, golden and export)
    plus the role spans that colour it."""

    plain: str
    spans: tuple[Span, ...] = ()

    def clipped(self, width: int, policy: TerminalPolicy) -> Line:
        """The line cut to ``width`` cells by ``clip``; spans are trimmed to the kept text."""
        text = clip(self.plain, width, policy)
        source = ascii_safe(self.plain) if policy.ascii else self.plain
        kept = 0
        while kept < min(len(text), len(source)) and text[kept] == source[kept]:
            kept += 1
        spans = tuple(
            Span(s.start, min(s.end, kept), s.role)
            for s in self.spans
            if s.start < kept
        )
        return Line(text, spans)

    def rstripped(self) -> Line:
        """The line without trailing spaces; spans are trimmed to the kept text."""
        text = self.plain.rstrip()
        spans = tuple(
            Span(s.start, min(s.end, len(text)), s.role)
            for s in self.spans
            if s.start < len(text)
        )
        return Line(text, spans)

    def to_ascii(self) -> Line:
        """Every non-ASCII character becomes one ``?``, so the span offsets stay valid."""
        return Line(ascii_safe(self.plain), self.spans)

    def padded(self, width: int, policy: TerminalPolicy) -> Line:
        """The line cut or padded with spaces to exactly ``width`` cells (measured by ``cell_len``)."""
        line = self if cell_len(self.plain) <= width else self.clipped(width, policy)
        return join(line, seg(" " * max(width - cell_len(line.plain), 0)))


def seg(text: str, role: str | None = None) -> Line:
    """A piece of text, with one role over all of it when ``role`` is given."""
    return Line(text, (Span(0, len(text), role),) if role and text else ())


def join(*parts: Line) -> Line:
    """The parts end to end; each span moves by the character length of what precedes it."""
    plain = ""
    spans: list[Span] = []
    for part in parts:
        spans += [
            Span(s.start + len(plain), s.end + len(plain), s.role) for s in part.spans
        ]
        plain += part.plain
    return Line(plain, tuple(spans))


# The count strip's font: each of 0 to 9 and + is 3 rows of 3 cells; ``#`` marks a block cell.
# A figure with any other character (``unknown``) is not drawn in the font.
_BIG: dict[str, tuple[str, str, str]] = {
    "0": ("###", "# #", "###"),
    "1": (" # ", "## ", " # "),
    "2": ("## ", " # ", "###"),
    "3": ("###", " ##", "###"),
    "4": ("# #", "###", "  #"),
    "5": ("###", "## ", "###"),
    "6": ("#  ", "###", "###"),
    "7": ("###", "  #", "  #"),
    "8": ("###", "###", "###"),
    "9": ("###", "###", "  #"),
    "+": (" # ", "###", " # "),
}


def _figure_rows(figure: str, policy: TerminalPolicy) -> list[str] | None:
    """The figure as 3 rows of block glyphs (one blank cell between digits), or None when it has
    a character the font does not have."""
    if not figure or any(ch not in _BIG for ch in figure):
        return None
    block = glyph("block", policy)
    return [
        " ".join(_BIG[ch][row] for ch in figure).replace("#", block) for row in range(3)
    ]


MARGIN = 1  # blank cells left of every pane
FRAME_ROWS = 2  # a frame costs its top and bottom border
INNER_PAD = 1  # blank cells between a border and the text


def _indent(lines: list[Line], cells: int) -> list[Line]:
    return [join(seg(" " * cells), line) for line in lines]


def _two_columns(
    left: list[Line], right: list[Line], wl: int, wr: int, gap: int = 2
) -> list[Line]:
    """``left`` and ``right`` side by side: each row is the left line padded with spaces to ``wl``
    cells, a gap of ``gap`` cells, then the right line. Both columns are built to fit (``wl`` and
    ``wr`` cells), so nothing is cut here; a column that is shorter is padded with blank rows.
    ``join`` moves each right-hand span by the character length of what precedes it (the padded
    left side and the gap), never by cell widths, so a wide character on the left cannot shift
    the colour of the right."""
    blank = seg("")
    rows: list[Line] = []
    for l_line, r_line in zip_longest(left, right, fillvalue=blank):
        pad = " " * max(wl - cell_len(l_line.plain), 0)
        rows.append(join(l_line, seg(pad + " " * gap), r_line))
    return rows


def _frame(
    title: str,
    body: list[Line],
    width: int,
    policy: TerminalPolicy,
    *,
    weight: str = "round",
    border_role: str | None = None,
    title_role: str | None = None,
    pad: int = INNER_PAD,
) -> list[Line]:
    """``body`` inside a titled border, every line exactly ``width`` cells wide. The inner text
    width is ``width - 2 - 2 * pad`` (a border and ``pad`` blank cells on each side, so
    ``width - 4`` by default); the title is cut to ``inner - 2`` so it never crowds the body.
    Heavy borders use ``border_attention``, round ones ``border_secondary``; the title is bold
    in the same colour. ``border_role`` and ``title_role`` override the two roles (the count
    strip is cyan); ``pad=0`` is the border-only frame of the ledger table."""
    heavy = weight == "heavy"
    prefix = "hbox" if heavy else "box"
    border = border_role or ("border_attention" if heavy else "border_secondary")
    title_role = title_role or ("attention_title" if heavy else "secondary")

    def g(name: str) -> str:
        return glyph(f"{prefix}_{name}", policy)

    inner = width - 2 * (1 + pad)
    shown = clip(title, max(inner - 2, 1), policy) if title else ""
    if policy.ascii:
        shown = ascii_safe(shown)
    if shown:
        fill = max(width - 5 - cell_len(shown), 0)
        top = join(
            seg(g("tl") + g("h") + " ", border),
            seg(shown, title_role),
            seg(" " + g("h") * fill + g("tr"), border),
        )
    else:
        top = seg(g("tl") + g("h") * (width - 2) + g("tr"), border)
    blank = " " * pad
    rows = [
        join(
            seg(g("v") + blank, border),
            line.padded(inner, policy),
            seg(blank + g("v"), border),
        )
        for line in body
    ]
    bottom = seg(g("bl") + g("h") * (width - 2) + g("br"), border)
    return [top, *rows, bottom]


def _roled(strings: list[str], role: str) -> list[Line]:
    """Existing plain lines (from ``wrap`` and friends), each carrying one whole-line role."""
    return [seg(text, role) for text in strings]


def _wrapped(text: str, width: int, policy: TerminalPolicy, role: str) -> list[Line]:
    return _roled(wrap(text, width, policy), role)


def _cell(text: str, width: int, policy: TerminalPolicy, role: str = "body") -> Line:
    """One padded column cell; the role covers the text, never the padding."""
    shown = clip(text, width, policy)
    return join(seg(shown, role), seg(" " * max(width - cell_len(shown), 0)))


def _absent_role(text: str, role: str = "body") -> str:
    """``muted`` for a bare absent value (``text_of`` quotes a real value "unknown", so the bare
    word means the source had none); otherwise ``role``."""
    return "muted" if text.strip() in ("unknown", ABSENT_IN_SOURCE) else role


# -- the COUNTS strip ------------------------------------------------------------------------------


def _absent_tail(text: str, role: str) -> Line:
    """``text`` in ``role``, except a trailing absent value (the source had none), which is muted.
    ``text_of`` quotes a real value "unknown", so a bare trailing word means absent."""
    for absent in (UNAVAILABLE, "unavailable", "unknown"):
        cut = len(text) - len(absent)
        if text.endswith(absent) and (cut == 0 or text[cut - 1] == " "):
            return join(seg(text[:cut], role), seg(text[cut:], "muted"))
    return seg(text, role)


def _token_line(text: str, token: CountsToken) -> Line:
    if token.dim:
        return seg(text, "muted")
    return _absent_tail(text, "identity" if token.protected else "body")


def _row_of(pieces: list[Line]) -> Line:
    """The tokens of one counts line, two spaces apart."""
    parts: list[Line] = []
    for index, piece in enumerate(pieces):
        if index:
            parts.append(seg("  "))
        parts.append(piece)
    return join(*parts)


def counts_line_objects(
    tokens: tuple[CountsToken, ...],
    policy: TerminalPolicy,
    max_lines: int | None = MAX_COUNT_LINES,
    width: int | None = None,
) -> list[Line]:
    """Lay tokens out in priority order. Protected tokens are never truncated: they wrap.

    Lower-priority tokens that do not fit within ``max_lines`` are cut with ``>``. ``width`` is
    the cells a line may use (the screen width, or the inner width of the pane that holds it).
    """
    width = width or policy.width
    lines: list[Line] = []
    pieces: list[Line] = []  # the whole tokens of the line being built
    cut = False
    for token in tokens:
        text = ascii_safe(token.text) if policy.ascii else token.text
        if cut and not token.protected:
            continue
        piece = _token_line(text, token)
        if cell_len(_row_of([*pieces, piece]).plain) <= width:
            pieces.append(piece)
            continue
        if token.protected:
            if pieces:
                lines.append(_row_of(pieces))
            chunks = wrap(text, width, policy)
            lines.extend(seg(chunk, "identity") for chunk in chunks[:-1])
            pieces = [seg(chunks[-1], "identity")]
            continue
        if cell_len(piece.plain) <= width and (
            max_lines is None or len(lines) + 1 < max_lines
        ):
            if pieces:
                lines.append(_row_of(pieces))
            pieces = [piece]
            continue
        # A token that does not fit is dropped whole, never cut inside: the line ends with the
        # truncation marker after the last whole token (whole tokens are dropped from the end
        # of the line until the marker fits).
        marker = glyph("truncate", policy)
        while pieces and cell_len(_row_of(pieces).plain) + 1 + cell_len(marker) > width:
            pieces.pop()
        pieces = [join(_row_of(pieces), seg(" " + marker)) if pieces else seg(marker)]
        cut = True
    if pieces:
        lines.append(_row_of(pieces))
    return lines


def counts_lines(
    tokens: tuple[CountsToken, ...],
    policy: TerminalPolicy,
    max_lines: int | None = MAX_COUNT_LINES,
) -> list[str]:
    """The plain text of ``counts_line_objects``."""
    return [line.plain for line in counts_line_objects(tokens, policy, max_lines)]


# -- ledger rows -----------------------------------------------------------------------------------------


def _is_active(row: RowView) -> bool:
    """The one ``ACTIVE`` badge: dispatchStatus, terminalState and outcome exactly active,
    active and none. Any other combination (an absent value too) shows its raw values."""
    return (row.dispatch_status, row.terminal_state, row.outcome) == (
        "active",
        "active",
        "none",
    )


def _status_text(row: RowView) -> str:
    """The merged status cell: the badge, or the three raw values in field order; a frozen
    row (fixture mode) leads with the frozen marker."""
    status = (
        "ACTIVE"
        if _is_active(row)
        else f"{row.dispatch_status}/{row.terminal_state}/{row.outcome}"
    )
    return f"{FROZEN_MARKER} {status}" if FROZEN_MARKER in row.flags else status


def _alive_text(row: RowView, policy: TerminalPolicy) -> str:
    """The liveness cell: a dot for ``alive``; any other value is spelled out after the dot, so
    the state is a word with the colours off too."""
    verdict = _verdict(row)
    dot = glyph("alive", policy)
    return dot if verdict in ("alive", "live") else f"{dot} {verdict}"


def _marker(row: RowView, policy: TerminalPolicy) -> str:
    return (glyph("selected", policy) if row.selected else " ") + (
        "*" if row.changed else " "
    )


def _verdict(row: RowView) -> str:
    return text_of(row.raw.liveness_verdict)


MIN_ID_CELLS = (
    20  # the dispatch id column never gives up more than this to the status column
)


def _status_cells(
    needed: int | None, default: int, room: int, id_needed: int | None = None
) -> int:
    """The status column width: the longest status text on screen (``needed``), else
    ``default``, never more than leaves the id its room (``MIN_ID_CELLS``, or less when the
    longest id shown is shorter); at least the heading."""
    id_min = MIN_ID_CELLS if id_needed is None else min(MIN_ID_CELLS, id_needed)
    return max(len("status"), min(needed if needed else default, room - id_min))


def _columns(
    policy: TerminalPolicy,
    avail: int,
    status_needed: int | None = None,
    alive_needed: int | None = None,
    id_needed: int | None = None,
) -> tuple[list[tuple[str, int]], list]:
    """Column (header, width) pairs and one getter per column, for the width class (which
    decides the column set) and ``avail``, the cells the table may use (the screen width, or the
    inner width of the pane that holds it). ``status_needed`` is the widest status text of the
    rows shown, so no merged status is cut unless ``avail`` is too small."""
    width = avail
    sep = len(SEPARATOR)
    alive = lambda r: _alive_text(r, policy)  # noqa: E731
    if policy.width_class == "full":
        # run, workerState, status, nextAction.kind, alive, evidence age
        fixed = [12, 12, 0, 16, 14, 12]
        room = width - (2 + sum(fixed) + sep * 7)
        fixed[2] = _status_cells(status_needed, 36, room)
        id_width = min(width - (2 + sum(fixed) + sep * 7), 48)
        names = [
            ("", 2),
            ("dispatchId", id_width),
            ("run", fixed[0]),
            ("workerState", fixed[1]),
            ("status", fixed[2]),
            ("nextAction.kind", fixed[3]),
            ("alive", fixed[4]),
            ("evidence age", fixed[5]),
        ]
        getters = [
            None,
            lambda r: r.dispatch_id,
            lambda r: r.run,
            lambda r: r.worker_state,
            _status_text,
            lambda r: r.next_action,
            alive,
            lambda r: r.evidence_age,
        ]
        return names, getters
    if policy.width_class == "line":
        kind, state, age = 18, 14, 7
        status = _status_cells(
            status_needed, 36, width - (2 + kind + state + age + sep * 5)
        )
        id_width = min(width - (2 + kind + state + status + age + sep * 5), 48)
        names = [
            ("", 2),
            ("kind", kind),
            ("dispatchId", id_width),
            ("alive", state),
            ("status", status),
            ("age", age),
        ]
        getters = [
            None,
            lambda r: r.next_action,
            lambda r: r.dispatch_id,
            alive,
            _status_text,
            lambda r: r.evidence_age,
        ]
        return names, getters
    kind, age = 14, 6
    state = max(
        len("alive"), min(alive_needed or 5, 12)
    )  # a dot, or a spelled-out value
    status = _status_cells(
        status_needed, 30, width - (2 + kind + state + age + sep * 5), id_needed
    )
    id_width = width - (2 + kind + state + status + age + sep * 5)
    names = [
        ("", 2),
        ("kind", kind),
        ("dispatchId", id_width),
        ("alive", state),
        ("status", status),
        ("age", age),
    ]
    getters = [
        None,
        lambda r: r.next_action,
        lambda r: r.dispatch_id,
        alive,
        _status_text,
        lambda r: r.evidence_age,
    ]
    return names, getters


def _cell_role(name: str, row: RowView, text: str) -> str:
    """The role of one row cell, from the column and the exact raw value (never a pattern)."""
    if name == "workerState":
        role = STATE_ROLE.get(("workerState", row.worker_state))
    elif name == "status":
        role = "state_running" if _is_active(row) else None
    else:
        role = None
    if name in ("nextAction.kind", "kind"):  # the verbatim kind is never classified
        return _absent_role(text)
    return role or _absent_role(text)


def _row_segments(
    row: RowView,
    columns: list[tuple[str, int]],
    getters: list,
    policy: TerminalPolicy,
    avail: int,
) -> Line:
    cells: list[Line] = []
    for (name, width), getter in zip(columns, getters, strict=True):
        if getter is None:
            cells.append(_cell(_marker(row, policy), width, policy, "body"))
            continue
        text = getter(row)
        cell = _cell(text, width, policy, _cell_role(name, row, text))
        if name == "alive":
            # the dot takes the state colour; a spelled-out value is amber (muted when absent)
            verdict = _verdict(row)
            alive = verdict in ("alive", "live")
            role = "state_running" if alive else (_absent_role(verdict, "attention"))
            shown = clip(text, width, policy)
            cell = join(seg(shown, role), seg(" " * max(width - cell_len(shown), 0)))
        elif name == "status" and FROZEN_MARKER in row.flags:
            shown = clip(text, width, policy)
            lead = shown[: len(FROZEN_MARKER)]
            body = _cell_role(name, row, text)
            cell = join(
                seg(lead, FROZEN_ROLE),
                seg(shown[len(lead) :], body),
                seg(" " * max(width - cell_len(shown), 0)),
            )
        cells.append(cell)
    parts: list[Line] = []
    for index, cell in enumerate(cells):
        if index:
            parts.append(seg(SEPARATOR))
        parts.append(cell)
    return join(*parts).rstripped().clipped(avail, policy)


def _header_lines(
    columns: list[tuple[str, int]], policy: TerminalPolicy, avail: int
) -> list[Line]:
    head = SEPARATOR.join(
        _pad(clip(name, width, policy), width) for name, width in columns
    )
    return [seg(clip(head.rstrip(), avail, policy), "muted")]


def _heading_rows(view: View, policy: TerminalPolicy) -> int:
    """The column heading takes 1 row whenever ledger rows are visible, at every width class
    (the rule row under it is gone: the footer rule is the only rule left)."""
    return 1 if view.visible_rows and not policy.too_narrow else 0


# -- screens -------------------------------------------------------------------------------------------------


def _labelled(
    label: str, value: str, width: int, policy: TerminalPolicy, role: str
) -> list[Line]:
    """``label: value`` wrapped to ``width``; continuation lines are indented two cells.
    The label is muted; ``role`` covers the value."""
    first, *rest = wrap(f"{label}: {value}", width, policy)
    prefix = f"{label}:"
    if first.startswith(prefix):
        lines = [join(seg(prefix, "muted"), seg(first[len(prefix) :], role))]
    else:
        lines = [seg(first, role)]
    for continuation in rest:
        lines += [
            seg("  " + part, role)
            for part in wrap(continuation, max(width - 2, 1), policy)
        ]
    return lines


def _inspector_lines(view: View, policy: TerminalPolicy, budget: int) -> list[Line]:
    """The title, then the field lines from ``view.inspector_scroll`` on, never more than ``budget`` lines.

    The scroll is in wrapped lines, so a field taller than the screen is still readable (d/u);
    "above" and "below" lines count what is hidden and are inside the budget.
    """
    selected = view.selected
    title = f"{INSPECTOR_TITLE}  {selected.dispatch_id if selected else ''}"
    lines = _wrapped(title, policy.width, policy, "attention_title")
    body: list[Line] = []
    for label, value in view.inspector or ():
        body += _labelled(label, value, policy.width, policy, _absent_role(value))
    room = max(budget - len(lines), 1)
    # never scroll past the point where the last line is on screen under an "above" line
    start = min(max(view.inspector_scroll, 0), max(len(body) - max(room - 1, 1), 0))
    space = room - (1 if start else 0)
    if len(body) - start <= space:
        shown, below = body[start:], 0
    else:
        take = max(space - 1, 1)  # one line kept for the "below" text
        shown, below = body[start : start + take], len(body) - start - take
    if start:
        lines += _wrapped(
            INSPECTOR_ABOVE_TEXT.format(n=start), policy.width, policy, "muted"
        )
    lines += shown
    if below:
        lines += _wrapped(
            INSPECTOR_BELOW_TEXT.format(n=below), policy.width, policy, "muted"
        )
    return lines[: max(budget, 1)]


def _notes(view: View, skip_historical: bool = False) -> list[str]:
    parts = [
        n
        for n in (
            view.filter_line,
            None if skip_historical else view.historical_note,
            view.duplicates_note,
            view.selection_note,
        )
        if n
    ]
    return ["  ".join(parts)] if parts else []


def _ledger_title(view: View, policy: TerminalPolicy) -> list[Line]:
    """The ledger title; at the widths with a liveness dot the legend shares its row."""
    width = policy.width
    title = _wrapped(view.ledger_title, width, policy, "secondary")
    if len(title) != 1:
        return title
    legend = LEDGER_LEGEND.format(dot=glyph("alive", policy))
    if cell_len(view.ledger_title) + 2 + cell_len(legend) > width:
        return title
    return [join(title[0], seg("  " + legend, "muted"))]


def _help_lines(view: View, policy: TerminalPolicy) -> list[Line]:
    """The key list, wrapped by whole key groups: no key is cut and no pair is split."""
    return _roled(wrap_groups(view.help_line, policy.width, policy), "muted")


def _question_line(
    q: QuestionLine,
    policy: TerminalPolicy,
    stub: bool = False,
    inner: int | None = None,
) -> Line:
    """One question line. With the link off it is the row text clipped as in R2; with it on the
    age and the bracketed state stay and only the question text is cut. The row carries a reason
    only when the source gave one (the record keeps its own ``reason unknown`` wording).

    The age is ``attention``, the subject ``body_bold`` and the reason tail ``muted``; the
    selected question is one ``selected`` line. ``inner`` is the text width of the pane the row
    sits in (the screen width when there is no pane)."""
    width = inner or policy.width
    # The row shows a reason only when the source gave one (it has no such field today): the
    # per-row "reason unknown" is replaced by one note in the title (see _panel_lines).
    reason = "  " + q.reason if q.reason else ""
    if not q.link:
        text = clip((q.row_text or q.text) + reason, width, policy)
        split = text.find("  ")
        tail = text.rfind("  " + (q.reason or QUESTIONS_REASON))
        if split <= 0:
            return seg(text, "body_bold")
        if tail > split:
            return join(
                seg(text[:split], "attention"),
                seg(text[split:tail], "body_bold"),
                seg(text[tail:], "muted"),
            )
        return join(seg(text[:split], "attention"), seg(text[split:], "body_bold"))
    mark = glyph("selected", policy) + " " if q.selected else "  "
    head = ascii_safe(mark + q.lead + "  ") if policy.ascii else mark + q.lead + "  "
    tail = ascii_safe(reason) if policy.ascii else reason
    room = max(width - cell_len(head) - cell_len(tail), 1)
    text = ascii_safe(q.shown) if policy.ascii else q.shown
    if stub and q.selected:
        # The desk holds the full text: the selected row is one short line, always a strict
        # prefix of the text, ending in ``>``, so the text is never on screen twice.
        keep = min(DESK_STUB_CELLS, cell_len(text)) - 1
        text = text[: _prefix_length(text, max(keep, 0))] + ">"
    if (
        cell_len(text) > room and room > 3
    ):  # a cut question text ends in a visible "..."
        text = text[: _prefix_length(text, room - 3)] + "..."
    shown = clip(text, room, policy)
    if (
        q.selected
    ):  # marker, age and question text in one role; the absent reason stays muted
        return join(seg(head + shown, "selected"), seg(tail, "muted")).clipped(
            width, policy
        )
    lead = ascii_safe(q.lead) if policy.ascii else q.lead
    marker = head[: len(head) - len(lead) - 2]
    line = join(
        seg(marker),
        seg(lead, "attention"),
        seg("  "),
        seg(shown, "body_bold"),
        seg(tail, "muted"),
    )
    return line.clipped(width, policy)


def _desk_question_pane(
    desk: DeskView, width: int, policy: TerminalPolicy
) -> list[Line]:
    """The question pane of the Decision Desk: a heavy frame ``width`` cells wide. The first body
    line is the age (the message id is not shown; the record and the export keep it), then the
    question text, at most ``DESK_TEXT_LINES`` lines with the last cut by ``...``. Reads only
    ``desk``."""
    inner = width - 2 * (1 + INNER_PAD)
    body: list[Line] = []
    if desk.age_text:
        body += _wrapped(f"age {desk.age_text}", inner, policy, "attention")
    if desk.ask:
        text = wrap(desk.ask, inner, policy)
        if len(text) > DESK_TEXT_LINES:
            last = text[DESK_TEXT_LINES - 1]
            text = text[: DESK_TEXT_LINES - 1] + [
                last[: _prefix_length(last, max(inner - 3, 1))] + "..."
            ]
        body += _roled(text, "attention")
    return _frame(DESK_TITLE, body, width, policy, weight="heavy")


def _desk_evidence_pane(
    desk: DeskView, width: int, policy: TerminalPolicy
) -> list[Line]:
    """The evidence pane: a round frame ``width`` cells wide with the linked session fields
    (label column aligned) and then each note. Everything wraps to the inner width; nothing is
    cut. Reads only ``desk``."""
    inner = width - 2 * (1 + INNER_PAD)
    body: list[Line] = []
    rows = _desk_rows(desk.session_fields)
    column = _label_width(rows)
    for label, value, role in rows:
        body += _field_lines(label, value, inner, column, policy, role)
    for note in desk.notes:
        if note != DESK_WORKTREE_NOTE:  # the full note lives with the worker detail
            body += _wrapped(note, inner, policy, "muted")
    return _frame(DESK_EVIDENCE_TITLE, body, width, policy, weight="round")


def _plain_absent(value: str) -> str:
    """The bare word ``unknown`` for a value the source did not carry."""
    return "unknown" if value.strip() == ABSENT_IN_SOURCE else value


def _desk_rows(fields: tuple[tuple[str, str], ...]) -> list[tuple[str, str, str]]:
    """(label, value, role) per desk field line: plain labels, one ``alive`` value, one ``ACTIVE``
    badge only when the three status values are exactly active, active and none."""
    if not fields:
        return []
    got = {label: _plain_absent(value) for label, value in fields}

    def get(name: str) -> str:
        return got.get(name, "unknown")

    verdict, _, rest = get("liveness").partition(" (")
    source = rest.rstrip(")")
    age = get("evidence age")
    if verdict in ("unknown", ""):
        alive, alive_role = "unknown", "muted"
    else:
        alive = "yes" if verdict in ("alive", "live") else verdict
        if source and source != "unknown":
            alive += f" ({source})"
        alive += f", {age} ago" if age[:1].isdigit() else ", age unknown"
        alive_role = "state_running" if verdict in ("alive", "live") else "body"
    state = get("workerState")
    worktree = get("resource.worktreeId")
    rows = [
        ("session", get("dispatchId"), _absent_role(get("dispatchId"))),
        (
            "state",
            state,
            STATE_ROLE.get(("workerState", state)) or _absent_role(state),
        ),
        ("alive", alive, alive_role),
        ("next", get("nextAction.kind"), _absent_role(get("nextAction.kind"))),
    ]
    status = (get("dispatchStatus"), get("terminalState"), get("outcome"))
    if status == ("active", "active", "none"):
        rows.append(("status", "ACTIVE", "state_running"))
    else:  # any other combination, an absent value included: three separate raw rows
        rows += [
            (name, value, STATE_ROLE.get((name, value)) or _absent_role(value))
            for name, value in zip(
                ("dispatchStatus", "terminalState", "outcome"), status
            )
        ]
    if worktree == "unknown":
        rows.append(("worktree", "unknown", "muted"))
    else:
        rows.append(("worktree", f"{worktree}  (this session only)", "body"))
    return rows


def _field_lines(
    label: str,
    value: str,
    inner: int,
    label_width: int,
    policy: TerminalPolicy,
    role: str = "body",
) -> list[Line]:
    """One evidence field. The muted label is padded to ``label_width`` cells and the value starts
    at that same cell on every one-line field. A value that does not fit beside its label sits on
    the next line, indented two cells (and is hard-split to ``inner - 2`` when still too wide, with
    nothing lost). ``role`` covers the value; the label is always ``muted``."""
    # The same conversion as ``wrap`` and ``clip``, before the value is measured.
    if policy.ascii:
        value = ascii_safe(value)
    value_room = max(inner - label_width, 1)
    if cell_len(value) <= value_room:
        pad = " " * max(label_width - len(label), 1)
        return [join(seg(label + pad, "muted"), seg(value, role))]
    lines = [seg(label, "muted")]
    lines += [
        join(seg("  "), seg(part, role))
        for part in wrap(value, max(inner - 2, 1), policy)
    ]
    return lines


def _label_width(rows: list[tuple[str, str, str]]) -> int:
    """The label column of a field list: the longest label plus one cell, never under the
    ``DESK_LABEL_CELLS`` of the Part C layout."""
    return max([DESK_LABEL_CELLS, *(len(label) + 1 for label, _, _ in rows)])


def _pane_widths(policy: TerminalPolicy) -> tuple[int, int]:
    """(pane, inner): the frame width and the text width inside it, for the screen width."""
    pane = policy.width - 2 * MARGIN
    return pane, pane - 2 * (1 + INNER_PAD)


RIGHT_DESK = 80  # the evidence column at 160 columns
RIGHT_LIST = 46  # the list column at 116 columns


def _desk_widths(policy: TerminalPolicy) -> tuple[int, int, int]:
    """(question, evidence, list) pane widths of the open desk. At ``full`` the question pane sits
    over the list in a left column beside the evidence; at ``line`` the question pane spans the
    width over the evidence and the list; below that the three panes stack. Each two-column row
    is margin + left + 2 + right + margin cells."""
    pane = _pane_widths(policy)[0]
    if policy.width_class == "full":
        left = policy.width - 4 - RIGHT_DESK
        return left, RIGHT_DESK, left
    if policy.width_class == "line":
        return pane, policy.width - 4 - RIGHT_LIST, RIGHT_LIST
    return pane, pane, pane


MIN_QUESTION_ROWS = (
    3  # the strip and the RETAIN pane are drawn only while this many rows fit
)
LAYOUTS = ("A", "B", "C")  # A: strip, list, RETAIN. B: strip, list. C: the list alone.


def _count_strip(
    panel: QuestionsPanel, width: int, policy: TerminalPolicy
) -> list[Line]:
    """The count as a cyan frame titled ``QUESTIONS_COUNT_LABEL`` in capitals. When the figure
    can be drawn in the 3-row font and fits beside the count line, the body is three rows (the
    figure in ``attention``, the count line in ``identity`` on the middle row); otherwise it is
    one bold figure and the wrapped count line."""
    inner = width - 2 * (1 + INNER_PAD)
    counts = ascii_safe(panel.counts_line) if policy.ascii else panel.counts_line
    figure = _figure_rows(panel.count_figure, policy)
    if figure and cell_len(figure[0]) + 2 + cell_len(counts) <= inner:
        body = [
            seg(figure[0], "attention"),
            join(
                seg(figure[1], "attention"), seg("  "), _absent_tail(counts, "identity")
            ),
            seg(figure[2], "attention"),
        ]
    else:
        text = panel.count_figure
        lead = cell_len(text) + 2
        first, *rest = wrap(counts, max(inner - lead, 1), policy) or [""]
        body = [
            join(seg(text, "attention"), seg("  "), _absent_tail(first, "identity"))
        ]
        body += [join(seg(" " * lead), _absent_tail(part, "identity")) for part in rest]
    return _indent(
        _frame(
            QUESTIONS_COUNT_LABEL.upper(),
            body,
            width,
            policy,
            border_role="border_count",
            title_role="title",
        ),
        MARGIN,
    )


def _retain_pane(
    panel: QuestionsPanel, width: int, policy: TerminalPolicy
) -> list[Line]:
    """The run, the caveat and the retention sentence together, in a round slate frame."""
    inner = width - 2 * (1 + INNER_PAD)
    body: list[Line] = []
    for text in (panel.run_line, panel.caveat_line, panel.retention_line):
        body += _wrapped(text, inner, policy, "muted")
    return _indent(_frame(RETAIN_TITLE, body, width, policy, weight="round"), MARGIN)


def _list_frame(
    panel: QuestionsPanel,
    policy: TerminalPolicy,
    capacity: int | None,
    layout: str,
    width: int,
    desk_open: bool,
    notice: list[Line] | None = None,
) -> list[Line]:
    """The list frame of the questions, exactly ``width`` cells wide (no margin): the disclosure,
    up to ``capacity`` questions, the state of the read and the reasons note. The frame is heavy
    when no desk is shown and round when one is; ``notice`` is the hidden-desk notice and goes
    inside the frame. The layout decides where the run line, the caveat and the retention
    sentence sit (see ``_panel_lines``)."""
    inner = width - 2 * (1 + INNER_PAD)
    strip = layout in ("A", "B")
    retain = layout == "A"
    shown, cut = panel.window(capacity)
    rows = [_question_line(q, policy, stub=desk_open, inner=inner) for q in shown]
    if cut:
        rows += _wrapped(cut, inner, policy, "muted")
    if any(q.selected for q in panel.lines) and not any(q.selected for q in shown):
        rows += _wrapped(
            DESK_SELECTED_HIDDEN, inner, policy, "muted"
        )  # the owner's oldest-first window
    rows += notice or []  # the hidden-desk notice sits inside the list frame
    for text in (panel.empty_text, panel.window_full_text, *panel.notes):
        if text:
            rows += _wrapped(text, inner, policy, "muted")
    standing: list[Line] = []
    for state_line in panel.state_lines:  # the state of the read
        standing += _wrapped(state_line, inner, policy, "muted")
    if not strip:  # no strip: the count is a plain list line
        # at 80 columns it stays as before the strip existed (without the "(no source)" tail)
        count = (
            panel.screen_counts_line or panel.counts_line
            if policy.width_class == "short"
            else panel.counts_line
        )
        standing += [
            _absent_tail(text, "identity") for text in wrap(count, inner, policy)
        ]
    if not any(q.reason for q in panel.lines):  # said once, not on every row
        standing += _wrapped(QUESTIONS_REASONS_NOTE, inner, policy, "muted")
    disclosure = _wrapped(panel.disclosure, inner, policy, "muted")
    caveats: list[Line] = []
    title = panel.title
    if not retain:
        title = f"{panel.title}  {panel.run_line}"
        if (
            cell_len(title) > inner - 2
        ):  # a narrow pane would cut the title: the run line
            title = panel.title  # goes into the body instead, so no fact is lost
            caveats += _wrapped(panel.run_line, inner, policy, "muted")
        caveats += _wrapped(panel.caveat_line, inner, policy, "muted")
        caveats += _wrapped(panel.retention_line, inner, policy, "muted")
    if strip and not desk_open:  # the disclosure leads, then the rows
        body = disclosure + rows + standing + caveats
    else:  # the rows lead (always beside an open desk, where the pane is narrow)
        body = rows + standing + disclosure + caveats
    return _frame(title, body, width, policy, weight="round" if desk_open else "heavy")


def _desk_block(
    panel: QuestionsPanel,
    policy: TerminalPolicy,
    capacity: int | None,
    layout: str,
    desk: DeskView,
) -> list[Line]:
    """The open desk with the list, indented by the margin. At ``full`` the left column is the
    question pane over the list and the right column is the evidence pane; at ``line`` the
    question pane spans the width over the evidence (left) and the list (right); at ``short`` the
    three panes stack. A two-column row is the left pane padded to its width, a gap of 2, then
    the right pane."""
    question_w, evidence_w, list_w = _desk_widths(policy)
    question = _desk_question_pane(desk, question_w, policy)
    evidence = _desk_evidence_pane(desk, evidence_w, policy)
    listing = _list_frame(panel, policy, capacity, layout, list_w, True)
    if policy.width_class == "full":
        rows = _two_columns(question + listing, evidence, question_w, evidence_w)
    elif policy.width_class == "line":
        rows = question + _two_columns(evidence, listing, evidence_w, list_w)
    else:
        rows = question + evidence + listing
    return _indent(rows, MARGIN)


def _panel_lines(
    panel: QuestionsPanel,
    policy: TerminalPolicy,
    capacity: int | None,
    notice: list[Line] | None = None,
    desk: DeskView | None = None,
    layout: str = "C",
) -> list[Line]:
    """The coordinator-questions panes.

    Layout A (160 and 116 columns): the count strip, the list frame and the RETAIN CONTEXT pane,
    in that order. Layout B drops the RETAIN pane under height pressure: the run line goes back
    into the list title and the caveat and the retention sentence into the list body. Layout C
    (80 columns, or under more height pressure) drops the strip too: the question rows lead the
    list, and the count line is a plain list line. No fact is lost in any layout.
    ``desk`` is the open Decision Desk: the list is then drawn inside ``_desk_block`` beside or
    under its panes. Without it the list spans the screen, and ``notice`` (the hidden-desk
    notice) goes inside the list frame."""
    pane = _pane_widths(policy)[0]
    out = _count_strip(panel, pane, policy) if layout in ("A", "B") else []
    if desk is None:
        out += _indent(
            _list_frame(panel, policy, capacity, layout, pane, False, notice), MARGIN
        )
    else:
        out += _desk_block(panel, policy, capacity, layout, desk)
    if layout == "A":
        out += _retain_pane(panel, pane, policy)
    return out


def _title_bar(lines: list[str], policy: TerminalPolicy) -> list[Line]:
    """The title lines with the ``READ ONLY`` badge right-aligned: on the first line when it
    fits there, else on the last, else on a line of its own. ``view.header1`` is not edited, so
    the record keeps its title text."""
    width = policy.width
    badge = ascii_safe(READ_ONLY_BADGE) if policy.ascii else READ_ONLY_BADGE
    out = [seg(text, "title") for text in lines]
    for index in (0, len(lines) - 1):
        if cell_len(lines[index]) + 2 + cell_len(badge) <= width:
            pad = width - cell_len(lines[index]) - cell_len(badge)
            out[index] = join(out[index], seg(" " * pad), seg(badge, "attention"))
            return out
    return out + [join(seg(" " * (width - cell_len(badge))), seg(badge, "attention"))]


def _plain_ledger(
    view: View, policy: TerminalPolicy, top_len: int, footer_height: int
) -> tuple[list[Line], object]:
    """The unframed ledger: its title (with the legend), the column heading and the rows that
    fit under ``top_len`` head rows and the footer. Returns ``(lines, window)``."""
    width = policy.width
    body = _ledger_title(view, policy)
    avail = width  # the table's cells
    columns, getters = _columns(
        policy,
        avail,
        max((cell_len(_status_text(r)) for r in view.visible_rows), default=None),
        max(
            (cell_len(_alive_text(r, policy)) for r in view.visible_rows), default=None
        ),
        max((cell_len(r.dispatch_id) for r in view.visible_rows), default=None),
    )
    heading = _heading_rows(view, policy)
    # The column heading at every width, unless that would leave no room for even one ledger
    # row (then the rows win and the heading is left out).
    if heading and policy.height - (top_len + len(body) + heading + footer_height) >= 1:
        body += _header_lines(columns, policy, avail)
    reserved = top_len + len(body) + footer_height
    capacity = max(policy.height - reserved, 1)
    window = view.window(capacity)
    if not view.all_rows:
        for text in view.ledger_empty:
            body += _wrapped(text, width, policy, "muted")
    elif not window.rows:
        body += _wrapped(NO_MATCH_TEXT, width, policy, "muted")
    for row in window.rows:
        body.append(_row_segments(row, columns, getters, policy, avail))
    return body, window


OBSERVATION_TITLE = (
    "OBSERVATION WINDOW"  # the pane of the per-source freshness and counts
)
MIN_LEDGER_ROWS = 3  # the framed ledger screen is drawn only while this many rows fit


def _framed_ledger(
    view: View,
    policy: TerminalPolicy,
    title: list[Line],
    tail: list[Line],
    footer_height: int,
) -> tuple[list[Line], object] | None:
    """The ledger screen (no questions panel) as three full-width panes, or ``None`` when the
    framed screen would leave fewer than ``MIN_LEDGER_ROWS`` ledger rows (or overflow the
    height), in which case the caller keeps the plain head.

    Order: the title bar, the attention pane (heavy amber, ``QUESTIONS_TITLE``, the gap notice and
    the historical-hidden note, or the panel summary while nothing is read), the observation pane
    (round slate: ``header2``, the counts lines laid out to the inner width, ``changes_line``),
    ``tail`` (the filter input, notes and the one-off message stay outside the frames), then the
    ledger pane (round slate, border only: the legend, the column heading and the rows). Every
    body is built from those view fields and the ledger rows, nothing else.
    Returns ``(lines above the footer rule, window)``."""
    width = policy.width
    inner = width - 2 * (1 + INNER_PAD)
    panel = view.questions
    hist = view.historical_note
    attention = _wrapped(view.gap_notice, inner, policy, "muted")
    if panel is not None and not panel.replaces_gap:  # questions on, nothing read yet
        attention += _wrapped(panel.summary, inner, policy, "muted")
    if hist:  # shares the gap notice's row when both fit on it, else its own lines
        if (
            len(attention) == 1
            and cell_len(attention[0].plain) + 2 + cell_len(hist) <= inner
        ):
            attention[0] = join(attention[0], seg(f"  {hist}", "muted"))
        else:
            attention += _wrapped(hist, inner, policy, "muted")
    observation = _wrapped(view.screen_header2 or view.header2, inner, policy, "muted")
    observation += counts_line_objects(
        view.screen_counts_tokens or view.counts_tokens, policy, width=inner
    )
    if view.changes_line:
        observation += _wrapped(view.changes_line, inner, policy, "muted")
    above = list(title)
    above += _frame(QUESTIONS_TITLE, attention, width, policy, weight="heavy")
    above += _frame(OBSERVATION_TITLE, observation, width, policy)
    above += tail
    above_len = len(above)

    avail = width - 2  # the ledger frame is border only: no pad, no margin
    if cell_len(view.ledger_title) > avail - 2:  # the title would be cut: keep it whole
        return None
    legend = LEDGER_LEGEND.format(dot=glyph("alive", policy))
    heading = _heading_rows(view, policy)
    capacity = policy.height - above_len - FRAME_ROWS - 1 - heading - footer_height
    if capacity < min(MIN_LEDGER_ROWS, max(len(view.visible_rows), 1)):
        return None
    columns, getters = _columns(
        policy,
        avail,
        max((cell_len(_status_text(r)) for r in view.visible_rows), default=None),
        max(
            (cell_len(_alive_text(r, policy)) for r in view.visible_rows), default=None
        ),
        max((cell_len(r.dispatch_id) for r in view.visible_rows), default=None),
    )
    window = view.window(capacity)
    body = [seg(legend, "muted")]
    if heading:
        body += _header_lines(columns, policy, avail)
    if not view.all_rows:
        for text in view.ledger_empty:
            body += _wrapped(text, avail, policy, "muted")
    elif not window.rows:
        body += _wrapped(NO_MATCH_TEXT, avail, policy, "muted")
    body += [_row_segments(row, columns, getters, policy, avail) for row in window.rows]
    ledger = _frame(view.ledger_title, body, width, policy, pad=0)
    if above_len + len(ledger) + footer_height > policy.height:
        return None
    return above + ledger, window


def screen_lines(
    view: View, policy: TerminalPolicy, message: str | None = None
) -> list[str]:
    """The screen as plain lines, each at most ``policy.width`` cells wide.

    ``message`` is a one-off notice from the command loop (an export result); it sits above the footer.
    """
    return [line.plain for line in _compose(view, policy, message)]


def _compose(
    view: View, policy: TerminalPolicy, message: str | None = None
) -> list[Line]:
    """The screen as ``Line`` objects: the plain text of ``screen_lines`` plus colour roles."""
    width = policy.width
    if (
        policy.too_narrow
    ):  # below 80 columns: the denominators and the gap notice still print
        lines = _wrapped(TOO_NARROW_TEXT, width, policy, "attention")
        lines += counts_line_objects(view.counts_tokens, policy, max_lines=None)
        return lines + _wrapped(view.gap_notice, width, policy, "muted")
    if policy.too_small:
        lines = _wrapped(TOO_SMALL_TEXT, width, policy, "attention")
        lines += _wrapped(view.collected_text, width, policy, "muted")
        return lines + _wrapped(view.gap_notice, width, policy, "muted")

    title_lines = _title_bar(
        wrap(view.screen_header1 or view.header1, width, policy), policy
    )
    head: list[Line] = list(title_lines)
    head += _wrapped(view.screen_header2 or view.header2, width, policy, "muted")
    head += counts_line_objects(view.screen_counts_tokens or view.counts_tokens, policy)
    if view.changes_line:
        head += _wrapped(view.changes_line, width, policy, "muted")
    # The R2 panel stands in for the gap notice once the question source has read; in the
    # inspector only its one-line summary (``gap_notice``) is shown, so the inspector keeps room.
    panel = view.questions
    inspecting = view.focus == "inspector" and view.inspector is not None
    panel_in_gap = panel is not None and panel.replaces_gap and not inspecting
    # The gap notice and the historical-hidden note share one row when both fit on it.
    hist = view.historical_note
    merge_hist = bool(
        hist
        and not panel_in_gap
        and len(wrap(view.gap_notice, width, policy)) == 1
        and cell_len(view.gap_notice) + 2 + cell_len(hist) <= width
    )
    outside: list[Line] = []  # the notes, the filter input and the one-off message
    for note in _notes(view, skip_historical=True):
        outside += _wrapped(note, width, policy, "muted")
    if view.focus == "filter":
        outside += _wrapped("/" + view.filter_text, width, policy, "body")
    if message:
        outside += _wrapped(message, width, policy, "muted")
    tail = (
        _wrapped(hist, width, policy, "muted") if hist and not merge_hist else []
    ) + outside

    # The footer is one line when it fits, else the key list and the counts on two lines.
    window_probe = view.window(None)
    one_line = view.footer(window_probe)
    footer_height = 1 + (  # one rule line above the footer
        1
        if cell_len(one_line) <= width
        else len(_help_lines(view, policy))
        + len(wrap(view.footer_counts(window_probe), width, policy))
    )

    if panel_in_gap:
        ledger_fixed = len(wrap(view.ledger_title, width, policy)) + (
            _heading_rows(view, policy)
        )
        # The questions win on a short terminal (owner decision, 2026-11-12): the ledger keeps
        # its title, one row and its overflow line, and the cut line of the list is budgeted.
        selected_note = 1 if any(q.selected for q in panel.lines) else 0
        desk = view.desk
        notice = _wrapped(DESK_HIDDEN, _pane_widths(policy)[1], policy, "muted")
        rows_wanted = min(MIN_QUESTION_ROWS, len(panel.lines))
        empty = replace(panel, lines=(), empty_text=None)

        def plan(layout: str) -> tuple[int, str, int]:
            """(spare, kind, list capacity) of one layout. Every height is measured from the
            built panes, so every frame row of the strip and the panes is counted."""
            base = len(_panel_lines(empty, policy, None, layout=layout))
            rest = policy.height - (
                len(head)
                + len(tail)
                + footer_height
                + ledger_fixed
                + 1  # one ledger row
                + 1  # the cut line of the list
                + selected_note
            )
            spare = rest - base
            if desk is None:
                return spare, "plain", spare if spare >= 1 else 0
            # The desk is sized first and the list keeps a line. The strip and the RETAIN pane
            # are full width; the desk block is max(...) of its columns at ``full``, the question
            # pane plus the taller of evidence and list at ``line``, and the sum when stacked.
            pane = _pane_widths(policy)[0]
            fixed = (
                len(_count_strip(panel, pane, policy)) if layout in ("A", "B") else 0
            ) + (len(_retain_pane(panel, pane, policy)) if layout == "A" else 0)
            question_w, evidence_w, list_w = _desk_widths(policy)
            question_h = len(_desk_question_pane(desk, question_w, policy))
            evidence_h = len(_desk_evidence_pane(desk, evidence_w, policy))
            list_h = len(_list_frame(empty, policy, None, layout, list_w, True))
            room = rest - fixed
            if policy.width_class == "full":
                shows, left = evidence_h <= room, room - question_h - list_h
            elif policy.width_class == "line":
                shows, left = (
                    question_h + evidence_h <= room,
                    room - question_h - list_h,
                )
            else:
                shows, left = True, room - question_h - evidence_h - list_h
            if shows and left >= 1:
                return spare, "desk", left
            if (
                spare - len(notice) >= 1
            ):  # the desk gives way to its notice, never the list
                return spare, "notice", spare - len(notice)
            return spare, "none", 0

        # The strip and the RETAIN pane are dropped (RETAIN first) while fewer than
        # MIN_QUESTION_ROWS question rows would fit; each drop puts its lines back in the list,
        # so no fact disappears. At most three layouts are measured, never a loop on the result.
        options = LAYOUTS if policy.width_class in ("full", "line") else ("C",)
        # Each layout is measured once, richest first; a layout is taken when the desk still
        # shows whole and at least MIN_QUESTION_ROWS rows fit. The last layout is taken as is.
        plans: dict[str, tuple[int, str, int]] = {}
        for candidate in options:
            plans[candidate] = plan(candidate)
            _, kind, cap = plans[candidate]
            if kind in ("plain", "desk") and cap >= max(rows_wanted, 1):
                break
        chosen = candidate
        spare, kind, cap = plans[chosen]
        panel_part: list[Line] | None
        if kind == "plain":
            panel_part = _panel_lines(panel, policy, spare, layout=chosen)
        elif kind == "desk":
            panel_part = _panel_lines(panel, policy, cap, desk=desk, layout=chosen)
        elif kind == "notice":
            panel_part = _panel_lines(panel, policy, cap, notice=notice, layout=chosen)
        else:
            panel_part = None
        if kind == "plain" and spare < 1:
            panel_part = None
        if panel_part is not None:
            gap_part = panel_part
        elif (
            desk is not None
        ):  # no room for the panel: the summary names the hidden desk
            gap_part = _wrapped(
                f"{view.gap_notice}; {DESK_HIDDEN}", width, policy, "muted"
            )
        else:  # no room for the panel: its one-line summary stands in for it
            gap_part = _wrapped(view.gap_notice, width, policy, "muted")
    else:
        gap_part = _wrapped(view.gap_notice, width, policy, "muted")
        if (
            panel is not None and not panel.replaces_gap
        ):  # questions on, nothing read yet
            gap_part += _wrapped(panel.summary, width, policy, "muted")
        if merge_hist and gap_part:
            gap_part[0] = join(gap_part[0], seg(f"  {hist}", "muted"))
    top = head + gap_part + tail

    if view.focus == "inspector" and view.inspector is not None:
        footer_lines = [seg(clip(INSPECTOR_HELP, width, policy), "muted")]
        body = _inspector_lines(
            view, policy, max(policy.height - len(top) - len(footer_lines), 1)
        )
        return top + body + footer_lines

    framed = (
        None
        if panel_in_gap
        else _framed_ledger(view, policy, title_lines, outside, footer_height)
    )
    if framed is not None:
        top, window = framed
        body: list[Line] = []
    else:  # the plain head and the unframed table
        body, window = _plain_ledger(view, policy, len(top), footer_height)

    footer = view.footer(window)
    if cell_len(footer) <= width:
        footer_lines = [
            seg(footer if not policy.ascii else ascii_safe(footer), "muted")
        ]
    else:
        footer_lines = _help_lines(view, policy) + _wrapped(
            view.footer_counts(window), width, policy, "muted"
        )
    rule = seg(glyph("hrule", policy) * width, "border_secondary")
    return top + body + [rule] + footer_lines


def render(view: View, policy: TerminalPolicy, message: str | None = None) -> Group:
    """The screen as Rich renderables: one ``Text`` per line, never reflowed, coloured by role
    only when the policy has a colour depth."""
    texts = []
    for line in _compose(view, policy, message):
        text = Text(line.plain, no_wrap=True, overflow="crop")
        if policy.color_system is not None:
            for span in line.spans:
                style = style_for(span.role, policy.color_system)
                if style is not None and span.end > span.start:
                    text.stylize(style, span.start, span.end)
        texts.append(text)
    return Group(*texts)
