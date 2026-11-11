"""Sanitizer tests (AD-9; T29 and T44 in acceptance-tests.md)."""

from __future__ import annotations

import unicodedata

import pytest

from superclaude.cli.observe.sanitize import sanitize

RLO = chr(0x202E)  # bidi override, a Unicode Cf character
LINE_SEPARATOR = chr(0x2028)
IDEOGRAPHIC_SPACE = chr(0x3000)
REPLACEMENT = chr(0xFFFD)

INJECTION = (
    "a\x1b[31mred\x1b[0m "  # CSI colour
    "b\x1b]8;;http://evil.example\x1b\\link\x1b]8;;\x1b\\ "  # OSC 8 hyperlink, ST terminated
    "c\x1b]2;window title\x07title "  # window-title sequence, BEL terminated
    "d\x9b31mC1 "  # 8-bit CSI
    "e\x07bell "  # BEL
    f"f{RLO}RLO "  # bidi override (Cf)
    "g\x1bPdcs payload\x1b\\dcs "  # DCS string
    "h\x1b_apc payload\x1b\\apc "  # APC string
    "i\x1b(Bplain "  # other ESC plus next character
    "end\x1b]0;unterminated"  # unterminated OSC runs to the end
)


def _bad_chars(text: str, allow_newline: bool = False) -> list[str]:
    bad = []
    for ch in text:
        if ch == "\n" and allow_newline:
            continue
        if ch == "\x1b" or unicodedata.category(ch) in ("Cc", "Cf", "Cs"):
            bad.append(repr(ch))
    return bad


@pytest.mark.parametrize("mode", ["line", "block"])
def test_injection_leaves_no_control_or_format_characters(mode):
    out = sanitize(INJECTION, mode)
    assert _bad_chars(out, allow_newline=(mode == "block")) == []
    assert "\x9b" not in out and RLO not in out
    for word in (
        "red",
        "link",
        "title",
        "C1",
        "bell",
        "RLO",
        "dcs",
        "apc",
        "plain",
        "end",
    ):
        assert word in out
    for payload in (
        "evil.example",
        "window title",
        "dcs payload",
        "apc payload",
        "unterminated",
    ):
        assert payload not in out


def test_unterminated_osc_runs_to_the_end_of_the_text():
    assert sanitize("keep\x1b]0;gone forever") == "keep"
    assert sanitize("keep\u009d0;gone forever") == "keep"


def test_incomplete_csi_is_removed_without_eating_text_before_it():
    assert sanitize("ok\x1b[31") == "ok"
    assert sanitize("ok\x1b") == "ok"


def test_newline_line_mode_is_one_line_and_block_mode_keeps_it():
    value = f"first\nsecond\r\nthird\rfourth{LINE_SEPARATOR}fifth"
    assert sanitize(value, "line") == "first second third fourth fifth"
    assert "\n" not in sanitize(value, "line")
    assert sanitize(value, "block") == "first\nsecond\nthird\nfourth\nfifth"


def test_default_mode_is_line():
    assert sanitize("a\nb") == "a b"


@pytest.mark.parametrize(
    "text",
    [
        "plain text 123",
        "日本語のテキスト",
        "中文 and English",
        "rocket 🚀 ok",
        f"café{IDEOGRAPHIC_SPACE}spaced",
    ],
)
def test_plain_cjk_and_emoji_pass_through_unchanged(text):
    assert sanitize(text) == text
    assert sanitize(text, "block") == text


def test_square_brackets_pass_through_unchanged():
    assert sanitize("[bold]x[/bold] [red]y") == "[bold]x[/bold] [red]y"


def test_always_returns_str():
    assert sanitize(None) == ""
    assert sanitize(b"bytes \xff ok") == f"bytes {REPLACEMENT} ok"
    assert sanitize(42) == "42"
    assert isinstance(sanitize(""), str)


def test_sanitize_is_idempotent():
    once = sanitize(INJECTION, "block")
    assert sanitize(once, "block") == once


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        sanitize("x", "other")
