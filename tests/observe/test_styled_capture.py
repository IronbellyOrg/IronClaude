"""The one-shot path can carry the screen's colour and weight; the capture is never export_text(styles=True)."""

from __future__ import annotations

import io

import pytest

from superclaude.cli.observe.commands import (
    Options,
    _screen_text,
    _stdout_is_tty,
    execute,
)
from superclaude.cli.observe.terminal import resolve_policy
from tests.observe.conftest import strip_sgr
from tests.observe.test_commands import deps_for
from tests.observe.test_render import WIDTHS, fixture_view


class _Tty(io.StringIO):
    def isatty(self) -> bool:
        return True


def _policy(width, env=None, ascii=False):
    return resolve_policy(env or {}, "utf-8", {"ascii": ascii}, width, 40)


@pytest.mark.parametrize("width", WIDTHS)
def test_a_styled_screen_has_escapes_and_the_same_text_as_the_plain_one(
    fake_clock, width
):
    view = fixture_view("base", fake_clock)
    policy = _policy(width)
    styled = _screen_text(view, policy, styled=True)
    plain = _screen_text(view, policy, styled=False)
    assert "\x1b[" in styled
    assert strip_sgr(styled) == plain and "\x1b" not in plain


@pytest.mark.parametrize("width", WIDTHS)
def test_no_color_gives_zero_escape_bytes_even_when_styled_is_asked_for(
    fake_clock, width
):
    view = fixture_view("base", fake_clock)
    out = _screen_text(view, _policy(width, {"NO_COLOR": "1"}), styled=True)
    assert "\x1b" not in out


@pytest.mark.parametrize("width", WIDTHS)
def test_ascii_stays_ascii_with_colour_on(fake_clock, width):
    view = fixture_view("long-identifiers", fake_clock)
    out = _screen_text(view, _policy(width, ascii=True), styled=True)
    assert "\x1b[" in out and out.isascii()


def test_the_styled_capture_follows_the_colour_depth(fake_clock):
    view = fixture_view("base", fake_clock)
    truecolor = _screen_text(
        view, _policy(160, {"COLORTERM": "truecolor"}), styled=True
    )
    standard = _screen_text(view, _policy(160), styled=True)
    assert "38;2;" in truecolor and "38;2;" not in standard


def test_a_piped_one_shot_stays_plain_and_a_terminal_one_is_styled(fake_clock):
    options = Options(once=True, fixture="base", width=160)
    piped = deps_for(fake_clock)  # a StringIO: not a terminal
    assert execute(options, piped) == 0 and "\x1b" not in piped.stdout.getvalue()
    tty = deps_for(fake_clock, stdout=_Tty())
    assert execute(options, tty) == 0 and "\x1b[" in tty.stdout.getvalue()
    quiet = deps_for(fake_clock, stdout=_Tty(), env={"NO_COLOR": "1"})
    assert execute(options, quiet) == 0 and "\x1b" not in quiet.stdout.getvalue()
    assert strip_sgr(tty.stdout.getvalue()) == piped.stdout.getvalue()


def test_a_stream_without_isatty_counts_as_not_a_terminal(fake_clock):
    class _Bare:
        def write(self, text):
            return len(text)

    assert _stdout_is_tty(deps_for(fake_clock, stdout=_Bare())) is False
