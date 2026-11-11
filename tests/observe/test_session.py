"""Session transition tests (AD-15, CD-2; T3, T8, T25, T41 in acceptance-tests.md)."""

from __future__ import annotations

import copy
import inspect
import json
import re
import string
from pathlib import Path

import pytest

import superclaude.cli.observe.view as view_module
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.view import (
    Effect,
    Key,
    Session,
    apply_cycle,
    apply_key,
    build_view,
)
from tests.observe.conftest import (
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_rows,
)


def text(char):
    return Key("text", char)


def view_of(result, session, clock):
    return build_view(result, session, clock)


def press(session, key, result, clock):
    """Build the view for this session, apply one key, return (session, effect)."""
    return apply_key(session, key, build_view(result, session, clock), clock)


def live_collector(responses, clock, argv_log):
    runner = FakeRunner(argv_log, responses)
    return Collector(LiveSource(runner, FakeDiscover(argv_log)), clock)


def reply(rows):
    return 0, json.dumps(make_envelope(rows, total=len(rows)))


def three_active_rows(clock):
    """One cycle with three active rows w-001..w-003, none historical."""
    return live_collector([reply(make_rows(3, 1))], clock, []).run_once()


def fixture_cycles(variant, clock, count):
    collector = Collector(FixtureSource(variant), clock)
    return [collector.run_once() for _ in range(count)]


# -- apply_cycle ---------------------------------------------------------------------------------


def test_the_first_successful_observation_is_the_baseline_with_no_change_flags(
    fake_clock,
):
    (first,) = fixture_cycles("base", fake_clock, 1)
    session = apply_cycle(Session(), first, fake_clock)
    assert session.baseline is not None and len(session.baseline) == 80
    assert session.mark_wall_time == fake_clock.wall() and session.marked is False
    view = view_of(first, session, fake_clock)
    assert not any(rv.changed for rv in view.all_rows)
    assert (
        view.changes_line
        == "new baseline at 12:00 (observer started) | changed since 12:00 (0)"
    )


def test_no_baseline_is_taken_before_a_successful_read(fake_clock, argv_log):
    collector = live_collector([(2, "")], fake_clock, argv_log)
    assert apply_cycle(Session(), collector.latest(), fake_clock).baseline is None
    failed = collector.run_once()
    assert failed.state == "FAILED"
    assert apply_cycle(Session(), failed, fake_clock).baseline is None
    unavailable = live_collector([reply([])], fake_clock, []).latest()
    assert apply_cycle(Session(), unavailable, fake_clock).baseline is None


def test_a_later_cycle_never_replaces_the_baseline(fake_clock):
    first, second = fixture_cycles("base", fake_clock, 2)
    session = apply_cycle(Session(), first, fake_clock)
    fake_clock.advance(30)
    later = apply_cycle(session, second, fake_clock)
    assert (
        later.baseline == session.baseline
        and later.mark_wall_time == session.mark_wall_time
    )


def test_an_empty_first_observation_still_sets_the_baseline(fake_clock):
    (empty,) = fixture_cycles("empty", fake_clock, 1)
    assert apply_cycle(Session(), empty, fake_clock).baseline == {}


def test_apply_cycle_refreshes_the_selected_rows_last_known_values(fake_clock):
    first, second = fixture_cycles("base", fake_clock, 2)
    session = apply_cycle(Session(), first, fake_clock)
    row = next(r for r in first.snapshot.rows if r.dispatch_id == "w-005")
    ident = row.identity
    session = Session(selected=ident, selected_row=row, baseline=session.baseline)
    assert session.selected_row.next_action_kind == "none"
    session = apply_cycle(session, second, fake_clock)
    assert (
        session.selected_row.next_action_kind == "approve" and session.selected == ident
    )


# -- T8: m marks, a changed row is starred ------------------------------------------------------------


def test_after_m_a_changed_next_action_stars_exactly_that_row(fake_clock):
    first, second = fixture_cycles("base", fake_clock, 2)
    session = apply_cycle(Session(), first, fake_clock)
    session, effect = press(session, text("m"), first, fake_clock)
    assert effect is Effect.NONE and session.marked is True
    session = apply_cycle(session, second, fake_clock)
    view = view_of(second, session, fake_clock)
    assert [rv.dispatch_id for rv in view.all_rows if rv.changed] == ["w-005"]
    assert view.changes_line == "changed since 12:00 (1)"


def test_added_and_removed_rows_count_in_changed_since(fake_clock, argv_log):
    rows = make_rows(4, 1)
    collector = live_collector(
        [reply(rows[:3]), reply([rows[0], rows[1], rows[3]])], fake_clock, argv_log
    )
    first = collector.run_once()
    session, _ = press(
        apply_cycle(Session(), first, fake_clock), text("m"), first, fake_clock
    )
    second = collector.run_once()  # w-004 added; w-003 not returned
    view = view_of(second, apply_cycle(session, second, fake_clock), fake_clock)
    assert [rv.dispatch_id for rv in view.all_rows if rv.changed] == ["w-004"]
    assert (
        view.changes_line == "changed since 12:00 (1)"
    )  # w-003 is kept, flagged not reobserved
    assert (
        "not reobserved"
        in next(rv for rv in view.all_rows if rv.dispatch_id == "w-003").flags
    )


def test_m_replaces_the_baseline_and_never_changes_any_count(fake_clock):
    first, second = fixture_cycles("base", fake_clock, 2)
    session = apply_cycle(Session(), first, fake_clock)
    before = view_of(second, session, fake_clock)
    fake_clock.advance(90)
    marked, _ = press(session, text("m"), second, fake_clock)
    after = view_of(second, marked, fake_clock)
    assert marked.mark_wall_time == fake_clock.wall() != session.mark_wall_time
    assert after.counts_tokens == before.counts_tokens
    assert (
        after.collected_text == before.collected_text
        and after.meta.counts == before.meta.counts
    )
    assert after.changes_line.endswith("(0)") and not any(
        rv.changed for rv in after.all_rows
    )


# -- T41: first look and dropped rows ------------------------------------------------------------------------


def test_a_row_missing_from_the_next_cycle_shows_not_reobserved_not_unchanged(
    fake_clock, argv_log
):
    rows = make_rows(3, 1)
    collector = live_collector([reply(rows), reply(rows[:2])], fake_clock, argv_log)
    first = collector.run_once()
    session = apply_cycle(Session(), first, fake_clock)
    second = collector.run_once()
    view = view_of(second, apply_cycle(session, second, fake_clock), fake_clock)
    dropped = next(rv for rv in view.all_rows if rv.dispatch_id == "w-003")
    assert "not reobserved" in dropped.flags and dropped.changed is False
    assert view.changes_line.endswith("(0)")


# -- T25: selection is anchored to identity ----------------------------------------------------------------------


def test_a_reordering_cycle_keeps_the_cursor_on_the_same_identity(fake_clock, argv_log):
    rows = make_rows(3, 1)
    collector = live_collector(
        [reply(rows), reply(list(reversed(rows)))], fake_clock, argv_log
    )
    first = collector.run_once()
    session = apply_cycle(Session(), first, fake_clock)
    session, _ = press(session, Key("down"), first, fake_clock)
    session, _ = press(session, Key("down"), first, fake_clock)
    assert view_of(first, session, fake_clock).selected.dispatch_id == "w-002"
    second = collector.run_once()
    session = apply_cycle(session, second, fake_clock)
    view = view_of(second, session, fake_clock)
    assert view.selected.dispatch_id == "w-002" and view.selected.selected
    assert [rv.dispatch_id for rv in view.visible_rows] == ["w-003", "w-002", "w-001"]
    assert view.selection_note is None


def test_a_dropped_selected_row_stays_selected_until_a_movement_key(
    fake_clock, argv_log
):
    rows = make_rows(3, 1)
    collector = live_collector(
        [reply(rows), reply([rows[0], rows[2]])], fake_clock, argv_log
    )
    first = collector.run_once()
    session = apply_cycle(Session(), first, fake_clock)
    session, _ = press(session, Key("down"), first, fake_clock)
    session, _ = press(session, Key("down"), first, fake_clock)
    assert session.selected_row.dispatch_id == "w-002"
    second = collector.run_once()
    session = apply_cycle(session, second, fake_clock)
    view = view_of(second, session, fake_clock)
    assert view.selection_note == "selected w-002 no longer in source window"
    assert (
        view.selected.dispatch_id == "w-002" and "not reobserved" in view.selected.flags
    )
    # a cycle that drops the row altogether leaves the placeholder from its last-known values
    gone = Collector(FixtureSource("empty"), fake_clock).run_once()
    placeholder = view_of(gone, apply_cycle(session, gone, fake_clock), fake_clock)
    assert placeholder.selection_note == "selected w-002 no longer in source window"
    assert placeholder.selected.dispatch_id == "w-002"
    # until a movement key is pressed: then the selection goes to a real row
    moved, _ = press(
        session, Key("up"), second, fake_clock
    )  # w-002 is last in source order
    assert moved.selected != session.selected
    assert view_of(second, moved, fake_clock).selection_note is None


# -- keys ------------------------------------------------------------------------------------------------------------


def test_movement_keys_select_by_identity_and_clamp_at_the_ends(fake_clock):
    result = three_active_rows(fake_clock)
    session = Session()
    ids = []
    for key in (
        Key("down"),
        text("j"),
        Key("down"),
        Key("down"),
    ):  # the last one clamps
        session, effect = press(session, key, result, fake_clock)
        assert effect is Effect.NONE
        ids.append(view_of(result, session, fake_clock).selected.dispatch_id)
    assert ids == ["w-001", "w-002", "w-003", "w-003"]
    top = session
    for key in (Key("up"), text("k"), Key("up")):
        top, _ = press(top, key, result, fake_clock)
    assert view_of(result, top, fake_clock).selected.dispatch_id == "w-001"
    from_nothing, _ = press(Session(), Key("up"), result, fake_clock)
    assert view_of(result, from_nothing, fake_clock).selected.dispatch_id == "w-003"
    empty = Collector(FixtureSource("empty"), fake_clock).run_once()
    none_selected, _ = press(Session(), Key("down"), empty, fake_clock)
    assert none_selected.selected is None


def test_enter_opens_the_inspector_and_escape_returns(fake_clock):
    result = three_active_rows(fake_clock)
    nothing, _ = press(Session(), Key("enter"), result, fake_clock)
    assert nothing.focus == "list"  # nothing selected: nothing to inspect
    selected, _ = press(Session(), Key("down"), result, fake_clock)
    opened, effect = press(selected, Key("enter"), result, fake_clock)
    assert (opened.focus, effect) == ("inspector", Effect.NONE)
    assert view_of(result, opened, fake_clock).inspector is not None
    still, _ = press(opened, Key("enter"), result, fake_clock)
    assert still.focus == "inspector"
    moved, _ = press(opened, Key("down"), result, fake_clock)
    assert moved.focus == "inspector" and moved.selected != opened.selected
    back, effect = press(opened, Key("escape"), result, fake_clock)
    assert (back.focus, effect) == ("list", Effect.NONE)
    same, effect = press(selected, Key("escape"), result, fake_clock)
    assert (same.focus, effect) == ("list", Effect.NONE)  # Esc in the list does nothing


def test_filter_mode_takes_letters_as_text_including_q_and_edits_with_backspace(
    fake_clock,
):
    (result,) = fixture_cycles("base", fake_clock, 1)
    session, effect = press(Session(), text("/"), result, fake_clock)
    assert (session.focus, effect) == ("filter", Effect.NONE)
    for char in "qjhme/r":
        session, effect = press(session, text(char), result, fake_clock)
        assert effect is Effect.NONE and session.focus == "filter"
    assert session.filter_text == "qjhme/r"
    session, _ = press(session, Key("backspace"), result, fake_clock)
    session, _ = press(session, Key("backspace"), result, fake_clock)
    assert session.filter_text == "qjhme"
    ignored, effect = press(session, Key("down"), result, fake_clock)
    assert (
        ignored.filter_text == "qjhme"
        and ignored.selected is None
        and effect is Effect.NONE
    )
    left, _ = press(session, Key("enter"), result, fake_clock)
    assert (left.focus, left.filter_text) == ("list", "qjhme")
    escaped, _ = press(session, Key("escape"), result, fake_clock)
    assert (escaped.focus, escaped.filter_text) == ("list", "qjhme")
    quit_session, effect = press(session, Key("ctrl_c"), result, fake_clock)
    assert effect is Effect.QUIT and quit_session.focus == "filter"
    empty_backspace, _ = press(
        Session(focus="filter"), Key("backspace"), result, fake_clock
    )
    assert empty_backspace.filter_text == ""
    assert view_of(
        result, Session(filter_text="run-b"), fake_clock
    ).filter_line.startswith("filter run-b")


def test_h_toggles_historical_rows_and_e_exports_and_q_quits(fake_clock):
    (result,) = fixture_cycles("historical", fake_clock, 1)
    session, effect = press(Session(), text("h"), result, fake_clock)
    assert session.show_historical is True and effect is Effect.NONE
    assert len(view_of(result, session, fake_clock).visible_rows) == 9
    session, _ = press(session, text("h"), result, fake_clock)
    assert session.show_historical is False
    exported, effect = press(session, text("e"), result, fake_clock)
    assert effect is Effect.EXPORT and exported == session
    for key in (text("q"), Key("ctrl_c")):
        quit_session, effect = press(session, key, result, fake_clock)
        assert effect is Effect.QUIT and quit_session == session


def test_unknown_keys_do_nothing_and_there_is_no_refresh_key(fake_clock):
    (result,) = fixture_cycles("base", fake_clock, 1)
    session = Session(
        selected=result.snapshot.rows[0].identity, selected_row=result.snapshot.rows[0]
    )
    for key in (
        text("r"),
        text("x"),
        text("Z"),
        text("1"),
        text(" "),
        Key("backspace"),
    ):
        after, effect = press(session, key, result, fake_clock)
        assert (after, effect) == (session, Effect.NONE), key


# -- T3: no key reaches Orca; nothing mutates ------------------------------------------------------------------------------


def test_no_key_can_reach_the_adapter_or_collector(fake_clock):
    (result,) = fixture_cycles("shared-unmapped", fake_clock, 1)
    assert list(inspect.signature(apply_key).parameters) == [
        "session",
        "key",
        "view",
        "clock",
    ]
    assert list(inspect.signature(apply_cycle).parameters) == [
        "session",
        "result",
        "clock",
    ]
    source = Path(view_module.__file__).read_text(encoding="utf-8")
    assert not re.search(r"observe\.(adapter|collector)\b|import subprocess", source)
    keys = [
        Key(name) for name in ("up", "down", "enter", "escape", "backspace", "ctrl_c")
    ]
    keys += [text(c) for c in string.printable.strip() + " " + "é日"]
    effects = {}
    for focus in ("list", "inspector", "filter"):
        for key in keys:
            session, effect = apply_key(
                Session(focus=focus, selected=result.snapshot.rows[0].identity),
                key,
                view_of(result, Session(focus=focus), fake_clock),
                fake_clock,
            )
            assert isinstance(session, Session) and isinstance(effect, Effect)
            effects.setdefault(effect, set()).add((focus, key.name, key.char))
    assert {f[2] or f[1] for f in effects[Effect.EXPORT]} == {"e"}
    assert {f[2] or f[1] for f in effects[Effect.QUIT]} == {"q", "ctrl_c"}
    # in filter mode only Ctrl-C quits; "q" and "e" are text there
    assert {f[1:] for f in effects[Effect.QUIT] if f[0] == "filter"} == {("ctrl_c", "")}
    assert not any(f[0] == "filter" for f in effects[Effect.EXPORT])


def test_transitions_return_new_sessions_and_never_mutate_their_input(fake_clock):
    first, second = fixture_cycles("base", fake_clock, 2)
    session = apply_cycle(Session(), first, fake_clock)
    snapshot = copy.deepcopy(session)
    view = view_of(first, session, fake_clock)
    keys = [
        Key("down"),
        Key("enter"),
        text("m"),
        text("h"),
        text("/"),
        text("q"),
        text("e"),
        Key("escape"),
    ]
    for key in keys:
        new, _ = apply_key(session, key, view, fake_clock)
        assert new is not session and session == snapshot
    assert (
        apply_cycle(session, second, fake_clock) is not session and session == snapshot
    )
    marked, _ = apply_key(session, text("m"), view, fake_clock)
    assert (
        marked.baseline is not session.baseline
        and session.baseline == snapshot.baseline
    )


def test_session_defaults_are_the_start_up_state():
    session = Session()
    assert (session.focus, session.selected, session.filter_text) == ("list", None, "")
    assert (session.show_historical, session.baseline, session.mark_wall_time) == (
        False,
        None,
        None,
    )
    with pytest.raises(Exception):
        session.focus = "filter"  # frozen
