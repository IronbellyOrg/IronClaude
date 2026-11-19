"""Terminal policy tests (AD-13; T26, T28, T30 helper part in acceptance-tests.md)."""

from __future__ import annotations

import io
import re
from pathlib import Path

import pytest
from rich.cells import cell_len
from rich.text import Text

import superclaude.cli.observe as observe_pkg
from superclaude.cli.observe import terminal
from superclaude.cli.observe.terminal import (
    MIN_ROWS,
    clip,
    make_console,
    resolve_policy,
)

SGR = re.compile(r"\x1b\[([0-9;]*)m")


def policy(env=None, encoding="utf-8", flags=None, width=160, height=40):
    return resolve_policy(env or {}, encoding, flags, width, height)


def render(pol, style, text="hello"):
    """What the console writes to its stream (not export_text, which always styles)."""
    buffer = io.StringIO()
    console = make_console(pol, file=buffer, record=True)
    console.print(Text(text, style=style))
    return buffer.getvalue()


# -- T26: NO_COLOR -----------------------------------------------------------


@pytest.mark.parametrize("value", ["1", "yes"])
def test_no_color_set_and_non_empty_gives_no_sgr_codes(value):
    pol = policy({"NO_COLOR": value})
    assert pol.no_color is True
    assert "\x1b" not in render(pol, "red")


@pytest.mark.parametrize("env", [{}, {"NO_COLOR": ""}])
def test_no_color_unset_or_empty_keeps_colour_available(env):
    pol = policy(env)
    assert pol.no_color is False
    assert "31" in [p for m in SGR.findall(render(pol, "red")) for p in m.split(";")]


# -- colour depth (D2): none, truecolor, 256-colour, 16-colour floor ---------------


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({"NO_COLOR": "1"}, None),
        ({"NO_COLOR": "1", "COLORTERM": "truecolor"}, None),
        ({"TERM": "dumb"}, None),
        ({"TERM": "unknown"}, None),
        ({"COLORTERM": "truecolor", "TERM": "xterm"}, "truecolor"),
        ({"COLORTERM": "24bit"}, "truecolor"),
        ({"COLORTERM": "TrueColor"}, "truecolor"),
        ({"TERM": "xterm-256color"}, "256"),
        ({"TERM": "xterm"}, "standard"),
        ({}, "standard"),
        ({"NO_COLOR": ""}, "standard"),
    ],
)
def test_colour_depth_is_resolved_from_the_environment(env, expected):
    pol = policy(env)
    assert pol.color_system == expected
    assert make_console(pol, file=io.StringIO()).color_system == expected


def test_truecolor_beats_256_colour_when_both_are_set():
    pol = policy({"COLORTERM": "truecolor", "TERM": "xterm-256color"})
    assert pol.color_system == "truecolor"


@pytest.mark.parametrize(
    ("env", "style", "needle"),
    [
        # A different colour per case: Rich caches the ANSI codes on a parsed style, so
        # reusing one colour string at two depths would show the first depth's codes.
        ({"COLORTERM": "truecolor"}, "rgb(10,200,30)", "38;2;10;200;30"),
        ({"TERM": "xterm-256color"}, "rgb(11,201,31)", "38;5;"),
    ],
)
def test_the_chosen_depth_reaches_the_bytes_the_console_writes(env, style, needle):
    out = render(policy(env), style)
    assert needle in out


# -- width classes, height, ASCII -----------------------------------------------


@pytest.mark.parametrize(
    ("width", "expected"),
    [
        (79, "narrow"),
        (80, "short"),
        (115, "short"),
        (116, "line"),
        (159, "line"),
        (160, "full"),
        (200, "full"),
    ],
)
def test_width_classes(width, expected):
    pol = policy(width=width)
    assert pol.width_class == expected
    assert pol.too_narrow is (expected == "narrow")


def test_too_small_below_min_rows():
    assert policy(height=MIN_ROWS - 1).too_small is True
    assert policy(height=MIN_ROWS).too_small is False


@pytest.mark.parametrize(
    ("encoding", "flags", "expected"),
    [
        ("utf-8", None, False),
        ("UTF-8", {}, False),
        ("utf8", {}, False),
        ("ascii", {}, True),
        ("latin-1", {}, True),
        (None, {}, True),
        ("utf-8", {"ascii": True}, True),
    ],
)
def test_ascii_mode_from_flag_or_non_utf8_encoding(encoding, flags, expected):
    pol = policy(encoding=encoding, flags=flags)
    assert pol.ascii is expected


def test_glyph_table_maps_to_ascii():
    ascii_pol = policy(flags={"ascii": True})
    utf_pol = policy()
    assert terminal.glyph("selected", utf_pol) == "▸"
    assert terminal.glyph("selected", ascii_pol) == "@"
    assert all(terminal.glyph(name, ascii_pol).isascii() for name in terminal.GLYPHS)


def test_the_block_glyph_is_one_cell_with_the_ascii_form_hash():
    from rich.cells import cell_len

    assert terminal.glyph("block", policy()) == "█" and cell_len("█") == 1
    assert terminal.glyph("block", policy(flags={"ascii": True})) == "#"


def test_frame_glyph_pairs_are_one_cell_with_the_ascii_forms_plus_dash_bar():
    from rich.cells import cell_len

    ascii_pol = policy(flags={"ascii": True})
    utf_pol = policy()
    pairs = {
        "box_tl": "╭",
        "box_tr": "╮",
        "box_bl": "╰",
        "box_br": "╯",
        "box_h": "─",
        "box_v": "│",
        "hbox_tl": "┏",
        "hbox_tr": "┓",
        "hbox_bl": "┗",
        "hbox_br": "┛",
        "hbox_h": "━",
        "hbox_v": "┃",
    }
    for name, glyph_text in pairs.items():
        assert terminal.glyph(name, utf_pol) == glyph_text
        assert cell_len(glyph_text) == 1
        expected = "-" if name.endswith("_h") else "|" if name.endswith("_v") else "+"
        assert terminal.glyph(name, ascii_pol) == expected


def test_console_is_built_with_explicit_width_and_literal_text():
    pol = policy(width=120, height=30)
    console = make_console(pol, file=io.StringIO(), record=True)
    assert console.width == 120
    assert console.safe_box is False
    console.print("[bold]x[/bold] 123 http://a.example :smile:")
    out = console.export_text(styles=True)
    assert "[bold]x[/bold] 123 http://a.example :smile:" in out
    assert "\x1b" not in out  # no highlighting of numbers or links, no emoji or markup
    assert (
        make_console(policy(flags={"ascii": True}), file=io.StringIO()).safe_box is True
    )


def test_output_encoding_and_size_helpers_return_usable_values():
    assert isinstance(terminal.output_encoding(), str) and terminal.output_encoding()
    columns, rows = terminal.detect_size()
    assert columns > 0 and rows > 0


# -- T30: clip -------------------------------------------------------------------

SAMPLES = [
    "日本語のテキストです" * 3,
    "🚀🚀🚀🚀" * 5,
    "abc日本def",
    "x" * 100,
    "mixed 中文 and 🚀 text",
]


@pytest.mark.parametrize("text", SAMPLES)
def test_clip_never_overflows_never_splits_and_marks_a_cut(text):
    pol = policy()
    for width in range(1, 41):
        out = clip(text, width, pol)
        assert cell_len(out) <= width
        if cell_len(text) <= width:
            assert out == text
        else:
            assert out.endswith(">")
            kept = out[:-1]
            assert text.startswith(
                kept
            )  # whole characters only, a prefix of the original
            assert cell_len(kept) <= width - 1


def test_clip_does_not_leave_half_a_double_width_character():
    pol = policy()
    assert clip("日本語", 4, pol) == "日>"
    assert clip("日本語", 3, pol) == "日>"
    assert clip("日本語", 2, pol) == ">"
    assert clip("日本語", 1, pol) == ">"
    assert clip("日本語", 6, pol) == "日本語"


def test_clip_edge_widths():
    pol = policy()
    assert clip("abc", 0, pol) == ""
    assert clip("abc", -3, pol) == ""
    assert clip("", 5, pol) == ""


def test_clip_in_ascii_mode_gives_pure_ascii():
    pol = policy(flags={"ascii": True})
    for width in range(1, 41):
        assert clip("x" * 100, width, pol).isascii()
        assert clip("日本語 and 🚀", width, pol).isascii()
        assert cell_len(clip("日本語 and 🚀", width, pol)) <= width
    assert clip("x" * 100, 10, pol) == "x" * 9 + ">"


# -- no other module owns terminal facts ------------------------------------------


def test_only_terminal_py_builds_consoles_or_reads_terminal_facts():
    package_dir = Path(observe_pkg.__file__).parent
    patterns = [
        r"\bConsole\(",
        r"NO_COLOR",
        r"COLUMNS",
        r"stdout\.encoding",
        r"getpreferredencoding",
    ]
    offenders = []
    for path in sorted(package_dir.glob("*.py")):
        if path.name == "terminal.py":
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in patterns:
            if re.search(pattern, text):
                offenders.append(f"{path.name}: {pattern}")
    assert offenders == []
