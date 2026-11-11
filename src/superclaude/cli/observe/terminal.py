"""Terminal policy: the one module that owns colour, ASCII mode, width classes, truncation
and every ``Console`` the observer builds (AD-13, CD-4, CD-5, CD-8).

No other module in this package constructs a ``Console`` or reads the colour switch,
the column count or the stream encoding.
"""

from __future__ import annotations

import codecs
import locale
import shutil
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from typing import IO

from rich import box
from rich.cells import cell_len
from rich.console import Console
from rich.style import Style

MIN_WIDTH = 80  # below this every view shows "terminal too narrow (min 80)"
MIN_ROWS = 8  # PROPOSED (CD-4): two header lines, COUNTS strip, gap notice, one ledger row, footer
FULL_WIDTH = 160  # 160 and wider: full table
LINE_WIDTH = 116  # 116 to 159: line form; 80 to 115: short form

TOO_NARROW_TEXT = "terminal too narrow (min 80)"
TOO_SMALL_TEXT = f"terminal too small (min {MIN_ROWS} rows)"  # PROPOSED wording (T49)

# Glyph table: name -> (unicode form, ASCII form). Everything else non-ASCII maps to "?".
GLYPHS: dict[str, tuple[str, str]] = {
    "sep": ("·", "."),
    "selected": ("▸", "@"),
    "truncate": (">", ">"),
    "hrule": ("─", "-"),
    "vrule": ("│", "|"),
    "cross": ("┼", "+"),
}

# Palette table (CD-8): empty, so every style is plain text and meaning lives in words.
PALETTE: dict[str, str] = {}

# Style attributes the observer never uses; the background is never painted either.
_FORBIDDEN_ATTRS = (
    "blink",
    "blink2",
    "dim",
    "italic",
    "underline",
    "underline2",
    "conceal",
)


@dataclass(frozen=True)
class TerminalPolicy:
    width: int
    height: int
    no_color: bool
    ascii: bool
    width_class: str  # "full" | "line" | "short" | "narrow"

    @property
    def too_narrow(self) -> bool:
        return self.width_class == "narrow"

    @property
    def too_small(self) -> bool:
        return self.height < MIN_ROWS

    @property
    def box_style(self) -> box.Box:
        return box.ASCII if self.ascii else box.SQUARE


def _is_utf8(encoding: str | None) -> bool:
    if not encoding:
        return False
    try:
        return codecs.lookup(encoding).name == "utf-8"
    except LookupError:
        return False


def width_class(width: int) -> str:
    if width >= FULL_WIDTH:
        return "full"
    if width >= LINE_WIDTH:
        return "line"
    if width >= MIN_WIDTH:
        return "short"
    return "narrow"


def resolve_policy(
    env: Mapping[str, str],
    encoding: str | None,
    flags: Mapping[str, bool] | None,
    width: int,
    height: int,
) -> TerminalPolicy:
    """Decide colour, ASCII mode and width class once, from explicit inputs."""
    flags = flags or {}
    # NO_COLOR counts when set and non-empty ("1" and "yes" alike).
    no_color = bool(env.get("NO_COLOR"))
    # ASCII with --ascii; turning it on for a non-UTF-8 output encoding is PROPOSED.
    use_ascii = bool(flags.get("ascii")) or not _is_utf8(encoding)
    return TerminalPolicy(
        width=width,
        height=height,
        no_color=no_color,
        ascii=use_ascii,
        width_class=width_class(width),
    )


def output_encoding() -> str:
    """The encoding of standard output, falling back to the locale's."""
    return (
        getattr(sys.stdout, "encoding", None)
        or locale.getpreferredencoding(False)
        or "utf-8"
    )


def detect_size() -> tuple[int, int]:
    """Current terminal size as (columns, rows); (80, 24) when it cannot be read."""
    size = shutil.get_terminal_size(fallback=(80, 24))
    return size.columns, size.lines


def make_console(
    policy: TerminalPolicy, file: IO[str] | None = None, record: bool = False
) -> Console:
    """The only place a ``Console`` is built: explicit width, no highlighting, no markup."""
    return Console(
        file=file,
        width=policy.width,
        height=policy.height,
        highlight=False,
        markup=False,
        emoji=False,
        color_system=None if policy.no_color else "standard",
        no_color=policy.no_color,
        safe_box=policy.ascii,
        record=record,
    )


def glyph(name: str, policy: TerminalPolicy) -> str:
    unicode_form, ascii_form = GLYPHS[name]
    return ascii_form if policy.ascii else unicode_form


def ascii_safe(text: str) -> str:
    """Map every non-ASCII character to ``?`` (PROPOSED rule for ASCII mode)."""
    return text.encode("ascii", errors="replace").decode("ascii")


def palette_style(name: str) -> Style:
    """A palette entry as a ``Style``; refuses blink, faint, italic, underline and backgrounds."""
    spec = PALETTE.get(name, "")
    style = Style.parse(spec) if spec else Style.null()
    for attr in _FORBIDDEN_ATTRS:
        if getattr(style, attr):
            raise ValueError(
                f"palette style {name!r} uses forbidden attribute {attr!r}"
            )
    if style.bgcolor is not None:
        raise ValueError(f"palette style {name!r} paints a background")
    return style


def clip(text: str, width: int, policy: TerminalPolicy) -> str:
    """The single truncation helper: fits ``text`` in ``width`` terminal cells.

    Measures with ``cell_len`` (never ``len``), never splits a double-width character, and
    marks a cut with one ``>`` that fits inside the width.
    """
    if policy.ascii:
        text = ascii_safe(text)
    if width <= 0:
        return ""
    if cell_len(text) <= width:
        return text
    marker = glyph("truncate", policy)
    room = width - cell_len(marker)
    kept: list[str] = []
    used = 0
    for ch in text:
        step = cell_len(ch)
        if used + step > room:
            break
        kept.append(ch)
        used += step
    return "".join(kept) + marker
