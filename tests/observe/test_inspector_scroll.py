"""The inspector never outgrows the screen and every line stays reachable (PR review findings)."""
# ruff: noqa: E741  (``l`` is a screen line in the comprehensions below)

from __future__ import annotations

from dataclasses import replace

from superclaude.cli.observe.render import screen_lines
from superclaude.cli.observe.view import (
    INSPECTOR_ABOVE_TEXT,
    INSPECTOR_SCROLL_STEP,
    Effect,
    Key,
    Session,
    apply_key,
    inspector_line_bound,
)
from tests.observe.test_render import fixture_view, policy_for

HEIGHT = 24


def _opened(clock):
    base = fixture_view("base", clock)
    row = base.visible_rows[0]
    session = Session(focus="inspector", selected=row.identity, selected_row=row.raw)
    return fixture_view("base", clock, session), session


def _fields(view):
    return [label for label, _ in view.inspector]


def test_the_inspector_fits_a_24_row_terminal(fake_clock):
    view, _ = _opened(fake_clock)
    lines = screen_lines(view, policy_for(80, HEIGHT))
    assert len(lines) <= HEIGHT
    assert any("below (d)" in l for l in lines)  # something is hidden, and it says so


def test_scrolling_reaches_every_inspector_field(fake_clock):
    view, _ = _opened(fake_clock)
    seen = set()
    for step in range(inspector_line_bound(view.inspector)):
        lines = screen_lines(
            replace(view, inspector_scroll=step), policy_for(80, HEIGHT)
        )
        assert len(lines) <= HEIGHT
        text = "\n".join(lines)
        seen.update(label for label in _fields(view) if f"{label}:" in text)
    assert seen == set(_fields(view))


def test_a_field_taller_than_the_screen_is_cut_to_it_and_still_readable(fake_clock):
    view, _ = _opened(fake_clock)
    tall = replace(
        view, inspector=(("poll error", ("lorem ipsum " * 330) + "END-MARKER"),)
    )
    seen_end = False
    for step in range(inspector_line_bound(tall.inspector) + 5):
        lines = screen_lines(
            replace(tall, inspector_scroll=step), policy_for(80, HEIGHT)
        )
        assert len(lines) <= HEIGHT
        seen_end = seen_end or any("END-MARKER" in l for l in lines)
    assert seen_end


def test_a_very_short_terminal_never_gets_more_lines_than_it_has(fake_clock):
    view, _ = _opened(fake_clock)
    lines = screen_lines(view, policy_for(80, 10))
    assert len(lines) <= 10


def test_d_and_u_scroll_the_inspector_and_do_not_change_the_selected_worker(
    fake_clock,
):
    view, session = _opened(fake_clock)
    down, effect = apply_key(session, Key("text", "d"), view, fake_clock)
    assert (down.inspector_scroll, effect) == (INSPECTOR_SCROLL_STEP, Effect.NONE)
    assert down.selected == session.selected
    up, _ = apply_key(down, Key("text", "u"), view, fake_clock)
    assert up.inspector_scroll == 0
    floor, _ = apply_key(up, Key("text", "u"), view, fake_clock)
    assert floor.inspector_scroll == 0
    ceiling = session
    for _ in range(inspector_line_bound(view.inspector) + 5):
        ceiling, _ = apply_key(ceiling, Key("text", "d"), view, fake_clock)
    assert ceiling.inspector_scroll == inspector_line_bound(view.inspector) - 1


def test_scroll_resets_on_leaving_and_on_moving_to_another_worker(fake_clock):
    view, session = _opened(fake_clock)
    scrolled, _ = apply_key(session, Key("text", "d"), view, fake_clock)
    left, _ = apply_key(scrolled, Key("escape"), view, fake_clock)
    assert (left.focus, left.inspector_scroll) == ("list", 0)
    moved, _ = apply_key(scrolled, Key("down"), view, fake_clock)
    assert moved.inspector_scroll == 0


def test_the_hidden_above_line_appears_once_scrolled(fake_clock):
    view, _ = _opened(fake_clock)
    lines = screen_lines(replace(view, inspector_scroll=2), policy_for(80, HEIGHT))
    assert INSPECTOR_ABOVE_TEXT.format(n=2) in lines
