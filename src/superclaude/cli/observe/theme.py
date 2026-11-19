"""Colour roles for the observer screens, one explicit table per colour depth.

The screen builders tag text with a semantic role (``attention``, ``muted``, ``state_running``
and so on); this module maps a role and a depth to a Rich ``Style``. The depth is the
``color_system`` of the terminal policy: ``"truecolor"`` uses the design-mockup palette exactly,
``"256"`` the nearest indexed colours, and ``"standard"`` (16 colours) named ANSI colours only,
because Rich's automatic downgrade of the mockup RGB values collapses several roles onto one
index. No role sets blink, dim or reverse. No module here builds a console or reads the
environment: the terminal policy module owns both.
"""

from __future__ import annotations

from rich.style import Style

ROLES: tuple[str, ...] = (
    "title",
    "attention",
    "attention_title",
    "identity",
    "secondary",
    "body",
    "body_bold",
    "muted",
    "selected",
    "border_attention",
    "border_secondary",
    "border_count",
    "state_running",
    "state_settled",
    "state_failed",
    "state_frozen",
)

# Each role names one of the eight palette colours and says whether it is bold.
_PALETTE_OF: dict[str, str] = {
    "title": "cyan",
    "attention": "amber",
    "attention_title": "amber",
    "identity": "base",
    "secondary": "slate",
    "body": "base",
    "body_bold": "base",
    "muted": "muted",
    "selected": "amber",
    "border_attention": "amber",
    "border_secondary": "slate",
    "border_count": "cyan",
    "state_running": "green",
    "state_settled": "cyan",
    "state_failed": "red",
    "state_frozen": "violet",
}
_BOLD: frozenset[str] = frozenset(
    {"title", "attention", "attention_title", "secondary", "body_bold", "selected"}
)

# The eight palette colours per depth (mockup RGB; 256-colour indexes; named 16-colour ANSI colours).
_COLOURS: dict[str, dict[str, str]] = {
    "truecolor": {
        "base": "rgb(225,233,238)",
        "muted": "rgb(165,182,194)",
        "slate": "rgb(82,108,128)",
        "amber": "rgb(250,178,25)",
        "cyan": "rgb(112,205,226)",
        "green": "rgb(139,215,175)",
        "red": "rgb(240,141,150)",
        "violet": "rgb(194,173,242)",
    },
    "256": {
        "base": "color(189)",
        "muted": "color(145)",
        "slate": "color(60)",
        "amber": "color(214)",
        "cyan": "color(80)",
        "green": "color(115)",
        "red": "color(210)",
        "violet": "color(147)",
    },
    "standard": {
        "base": "bright_white",
        "muted": "white",
        "slate": "bright_black",
        "amber": "bright_yellow",
        "cyan": "bright_cyan",
        "green": "green",
        "red": "red",
        "violet": "magenta",
    },
}

# Display mapping from a real state word to a state role, keyed by (field, exact raw value).
# This is a display choice, not a count mapping and not a health verdict: the word is always
# printed, and every value not listed here keeps the body role.
STATE_ROLE: dict[tuple[str, str], str] = {
    ("workerState", "running"): "state_running",
    ("liveness", "alive"): "state_running",
    ("liveness", "live"): "state_running",
    ("workerState", "succeeded"): "state_settled",
    ("dispatchStatus", "completed"): "state_settled",
    ("workerState", "failed"): "state_failed",
    ("dispatchStatus", "failed"): "state_failed",
}
FROZEN_ROLE = (
    "state_frozen"  # a flags cell holding the frozen marker (fixture mode only)
)

_CACHE: dict[tuple[str, str], Style] = {}


def style_for(role: str, depth: str | None) -> Style | None:
    """The Rich style of ``role`` at ``depth``; ``None`` when there is no colour depth.

    Styles are cached per ``(role, depth)`` so a style made for one depth in a process is never
    reused for another (Rich caches the ANSI codes it renders on a ``Style``).
    """
    if role not in _PALETTE_OF:
        raise KeyError(f"unknown role: {role!r}")
    if depth is None:
        return None
    key = (role, depth)
    style = _CACHE.get(key)
    if style is None:
        style = Style(color=_COLOURS[depth][_PALETTE_OF[role]], bold=role in _BOLD)
        _CACHE[key] = style
    return style
