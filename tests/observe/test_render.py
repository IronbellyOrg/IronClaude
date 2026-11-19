"""Screen renderer tests (AD-11, AD-13; T6, T16, T23, T24, T28, T29 render half, T35, T44, T49)."""
# ruff: noqa: E741  (``l`` is a screen line in the comprehensions below)

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import pytest
from rich.cells import cell_len

import superclaude.cli.observe.render as render_module
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.render import render
from superclaude.cli.observe.render import screen_lines as framed_screen_lines
from superclaude.cli.observe.terminal import MIN_ROWS, make_console, resolve_policy
from superclaude.cli.observe.view import GAP_NOTICE, Session, build_view
from tests.observe.conftest import (
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_rows,
    pane_body,
    split_panes,
    unframe,
    unframed,
)

WIDTHS = (160, 116, 80)


def screen_lines(view, policy, message=None):
    """The screen with each frame read as before it existed (top border to its title row, body
    rows without their borders, bottom borders dropped), for the checks of text and order.
    The checks of frame shape and of height use ``framed_screen_lines``."""
    return unframed(
        split_panes(framed_screen_lines(view, policy, message), policy.width)
    )


def policy_for(width, height=40, ascii=False, no_color=False):
    env = {"NO_COLOR": "1"} if no_color else {}
    return resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)


def fixture_view(variant, clock, session=None, cycles=1):
    collector = Collector(FixtureSource(variant), clock)
    for _ in range(cycles):
        result = collector.run_once()
    return build_view(result, session or Session(), clock)


def generated_view(clock, n_rows, n_runs, session=None):
    runner = FakeRunner(
        [], [(0, json.dumps(make_envelope(make_rows(n_rows, n_runs), total=n_rows)))]
    )
    result = Collector(LiveSource(runner, FakeDiscover([])), clock).run_once()
    return build_view(result, session or Session(), clock)


def printed(view, policy):
    """What the console writes for ``render(view, policy)`` (no styles)."""
    import io

    buffer = io.StringIO()
    console = make_console(policy, file=buffer, record=True)
    console.print(render(view, policy))
    return buffer.getvalue()


def bad_chars(text):
    return [
        ch
        for ch in text
        if ch == "\x1b"
        or (ch != "\n" and unicodedata.category(ch) in ("Cc", "Cf", "Cs"))
    ]


# -- T23 and T16: widths and counts ------------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_every_line_fits_the_width_for_the_base_variant(fake_clock, width):
    policy = policy_for(width)
    for session in (Session(), Session(show_historical=True)):
        view = fixture_view("base", fake_clock, session)
        lines = screen_lines(view, policy)
        assert all(cell_len(line) <= width for line in lines), [
            l for l in lines if cell_len(l) > width
        ]
        out = strip_sgr(printed(view, policy))
        assert all(cell_len(line) <= width for line in out.splitlines())


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("n_runs", [5, 8, 10])
@pytest.mark.parametrize("n_rows", [50, 80, 100])
def test_matrix_lines_fit_counts_are_k_of_n_and_overflow_names_the_total(
    fake_clock, n_rows, n_runs, width
):
    view = generated_view(fake_clock, n_rows, n_runs)
    policy = policy_for(width, height=30)
    lines = screen_lines(view, policy)
    assert all(cell_len(line) <= width for line in lines)
    assert len(lines) <= 30
    for line in lines:
        for k, n in re.findall(r"(\d+) of (\d+)", line):
            assert int(k) <= int(n)
    assert not any(re.match(r"^\d+/\d+ shown", l) or "more" in l.split() for l in lines)
    footer = [l for l in lines if re.search(r"shown \d+/\d+$", l)]
    assert len(footer) == 1  # the footer names the total once; no "+N more" row
    x, y = map(int, re.search(r"shown (\d+)/(\d+)$", footer[0]).groups())
    assert y == n_rows and x < y
    assert any(f"collected {n_rows} / reported {n_rows}" in l for l in lines)


# -- T24 and T44 ------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_long_identifiers_truncate_with_a_marker_in_lists(fake_clock, width):
    view = fixture_view("long-identifiers", fake_clock)
    lines = screen_lines(view, policy_for(width))
    assert any(">" in l for l in lines)
    assert all(cell_len(l) <= width for l in lines)
    full = view.visible_rows[0].dispatch_id
    assert full not in "\n".join(lines)  # truncated in the list


def test_the_inspector_shows_the_full_identifier_wrapped_by_cells(fake_clock):
    for width in WIDTHS:
        view0 = fixture_view("long-identifiers", fake_clock)
        for row in view0.visible_rows:
            view = fixture_view(
                "long-identifiers",
                fake_clock,
                Session(focus="inspector", selected=row.identity),
            )
            lines = screen_lines(view, policy_for(width))
            assert all(cell_len(l) <= width for l in lines)
            start = next(i for i, l in enumerate(lines) if l.startswith("dispatchId:"))
            block = [lines[start]]
            for l in lines[start + 1 :]:
                if not l.startswith("  "):
                    break
                block.append(l.strip())
            # the wrap may break at the space after the label; nothing of the ID is lost
            assert "".join(block).replace(" ", "") == f"dispatchId:{row.dispatch_id}"
            assert not any(l.endswith(">") for l in block)


def test_worker_text_with_markup_renders_literally(fake_clock):
    view = fixture_view("injection", fake_clock, Session(show_historical=True))
    out = strip_sgr(printed(view, policy_for(160)))
    assert "[bold]x[/bold]" in out


# -- T29 render half, T28 --------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("focus", ["list", "inspector"])
def test_injection_renders_no_escape_c1_or_format_characters(fake_clock, width, focus):
    base = fixture_view("injection", fake_clock, Session(show_historical=True))
    for row in base.visible_rows:
        view = fixture_view(
            "injection",
            fake_clock,
            Session(focus=focus, selected=row.identity, show_historical=True),
        )
        policy = policy_for(width, no_color=True)
        out = printed(view, policy)
        assert bad_chars(out) == [], out
        assert bad_chars("\n".join(screen_lines(view, policy))) == []
    assert "red detail" in strip_sgr(
        printed(
            fixture_view(
                "injection",
                fake_clock,
                Session(
                    focus="inspector",
                    selected=base.visible_rows[0].identity,
                    show_historical=True,
                ),
            ),
            policy_for(160),
        )
    )


def test_no_blink_code_appears_in_any_render(fake_clock):
    view = fixture_view("base", fake_clock)
    for width in WIDTHS:
        for no_color in (False, True):
            out = printed(view, policy_for(width, no_color=no_color))
            params = [
                p for m in re.findall(r"\x1b\[([0-9;]*)m", out) for p in m.split(";")
            ]
            assert "5" not in params and "6" not in params


# -- T35 and T49 ---------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_counts_strip_keeps_its_priority_tokens_intact(fake_clock, width):
    view = fixture_view("base", fake_clock)
    text = "\n".join(screen_lines(view, policy_for(width)))
    assert "collected 80 / reported 80" in text and "scope=all" in text
    first_lines = screen_lines(view, policy_for(width))
    gap = next(i for i, l in enumerate(first_lines) if l.startswith("Human questions"))
    title = next(
        i for i, l in enumerate(first_lines) if l.startswith(view.ledger_title)
    )
    assert gap < title  # the gap notice sits above the ledger at every width


def test_partial_literal_is_never_truncated_at_80_columns(fake_clock):
    runner = FakeRunner(
        [],
        [
            lambda argv, t: (
                0,
                json.dumps(make_envelope(make_rows(2, 1), total=9999, has_more=True)),
            )
        ],
    )
    result = Collector(LiveSource(runner, FakeDiscover([])), fake_clock).run_once()
    view = build_view(result, Session(), fake_clock)
    text = " ".join(l.strip() for l in screen_lines(view, policy_for(80)))
    assert "PARTIAL (cursor missing or not advancing, page 1)" in text


@pytest.mark.parametrize("width", [79, 60, 40, 30])
def test_below_80_columns_the_screen_says_too_narrow_and_keeps_counts_and_gap(
    fake_clock, width
):
    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(width))
    assert lines[0].startswith("terminal too narrow") or width < 40
    flat = "".join("".join(lines).split())
    assert "terminaltoonarrow(min80)" in flat
    assert "collected80/reported80".replace(" ", "") in flat
    assert "".join(GAP_NOTICE.split()) in flat
    assert all(cell_len(l) <= width for l in lines)
    assert (
        lines.index(next(l for l in lines if l.startswith("collected"))) > 0
    )  # counts below the diagnostic


@pytest.mark.parametrize("height", [1, 3, MIN_ROWS - 1])
def test_a_too_small_terminal_shows_a_diagnostic_that_still_carries_the_gap_notice(
    fake_clock, height
):
    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(120, height=height))
    assert lines[0].startswith("terminal too small")
    assert GAP_NOTICE in lines
    assert any("collected 80 / reported 80" in l for l in lines)


# -- T6 and modes --------------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_rendering_twice_is_byte_identical_and_no_color_changes_no_text(
    fake_clock, width
):
    view = fixture_view("base", fake_clock, Session(show_historical=True))
    colour = policy_for(width)
    nocolor = printed(view, policy_for(width, no_color=True))
    assert printed(view, colour) == printed(view, colour)
    assert strip_sgr(printed(view, colour)) == nocolor  # colour adds no text
    assert "\x1b" in printed(view, colour) and "\x1b" not in nocolor
    assert screen_lines(view, colour) == screen_lines(
        view, policy_for(width, no_color=True)
    )


@pytest.mark.parametrize("width", WIDTHS)
def test_ascii_mode_renders_only_ascii_for_the_base_variant(fake_clock, width):
    view = fixture_view(
        "base", fake_clock, Session(selected=None, show_historical=True)
    )
    selected = (
        fixture_view("base", fake_clock, Session(show_historical=True))
        .visible_rows[2]
        .identity
    )
    view = fixture_view(
        "base", fake_clock, Session(selected=selected, show_historical=True)
    )
    policy = policy_for(width, ascii=True)
    assert (
        printed(view, policy).isascii()
        and "\n".join(screen_lines(view, policy)).isascii()
    )
    cjk = fixture_view("long-identifiers", fake_clock)
    assert "\n".join(screen_lines(cjk, policy)).isascii()


# -- layout per width ----------------------------------------------------------------------------------------------------------------------


def test_full_width_is_a_table_without_a_stage_column_and_with_the_verbatim_kind(
    fake_clock,
):
    view = fixture_view("base", fake_clock, Session(show_historical=True))
    lines = screen_lines(view, policy_for(160))
    header = next(l for l in lines if "dispatchId" in l and "workerState" in l)
    for name in (
        "run",
        "workerState",
        "status",
        "nextAction.kind",
        "alive",
        "evidence age",
    ):
        assert name in header
    assert "flags" not in header and "dispatchStatus" not in header  # one status cell
    assert "stage" not in header.lower() and "orchestrator" not in header
    first = view.visible_rows[0]
    row = next(
        l
        for l in lines
        if l.split()[:1] == [first.dispatch_id] or f" {first.dispatch_id} " in f" {l} "
    )
    assert first.run in row and first.next_action in row
    assert (
        "●" in row or first.raw.liveness_verdict in row
    )  # a dot, or the spelled-out value


def test_line_and_short_forms_follow_kind_id_verdict_age(fake_clock):
    view = fixture_view("base", fake_clock, Session(show_historical=True))
    first = view.visible_rows[0]
    line_form = next(
        l
        for l in screen_lines(view, policy_for(116))
        if first.dispatch_id in l and l.strip()
    )
    verdict = first.raw.liveness_verdict
    alive_cell = "●" if verdict in ("alive", "live") else verdict  # dot or spelled out
    assert (
        line_form.index(first.next_action)
        < line_form.index(first.dispatch_id)
        < line_form.index(alive_cell)
    )
    short = next(
        l
        for l in screen_lines(view, policy_for(80))
        if first.dispatch_id in l and l.strip()
    )
    assert short.index(first.next_action) < short.index(first.dispatch_id)
    assert first.evidence_age in short and "liveness" not in short


def test_marks_flags_overflow_and_empty_text_are_laid_out(fake_clock):
    base = fixture_view("base", fake_clock, Session(show_historical=True))
    target = base.visible_rows[2].identity  # w-003, the frozen row
    view = fixture_view(
        "base", fake_clock, Session(selected=target, show_historical=True)
    )
    lines = screen_lines(view, policy_for(160, height=24))
    frozen = next(l for l in lines if "w-003" in l)
    assert (
        "FROZEN" in frozen
        and frozen.lstrip().startswith(("▸", "@"))
        or frozen.startswith("▸")
    )
    assert any(re.search(r"shown \d+/80$", l) for l in lines)  # no "+N more" row
    empty = screen_lines(fixture_view("empty", fake_clock), policy_for(120))
    assert "no observed items in this source window; not proof none exist" in empty
    assert "worker-list returned 0 workers in scope=bound" in empty
    never = Collector(FixtureSource("base"), fake_clock).latest()
    lines = screen_lines(build_view(never, Session(), fake_clock), policy_for(120))
    assert "no successful worker-list read yet" in lines
    assert not any("as of" in l for l in lines)  # no ``as of`` on the title any more


def test_changed_rows_and_filter_notes_show_on_screen(fake_clock):
    first = Collector(FixtureSource("base"), fake_clock)
    one = first.run_once()
    two = first.run_once()
    from superclaude.cli.observe.view import apply_cycle

    session = apply_cycle(
        Session(show_historical=True, filter_text="w-005"), one, fake_clock
    )
    view = build_view(two, session, fake_clock)
    lines = screen_lines(view, policy_for(160))
    starred = next(l for l in lines if "w-005" in l and not l.startswith("filter"))
    assert starred.startswith(" *")
    assert any(l.startswith("filter w-005: 1 of 80 collected") for l in lines)
    assert any(l.startswith("new baseline at 12:00") for l in lines)


def test_selection_placeholder_and_filter_prompt_lines(fake_clock):
    base = fixture_view("base", fake_clock)
    row = base.visible_rows[0]
    gone = fixture_view(
        "empty",
        fake_clock,
        Session(
            selected=row.identity,
            selected_row=row.raw,
            focus="filter",
            filter_text="ab",
        ),
    )
    lines = screen_lines(gone, policy_for(120))
    assert any("selected w-001 no longer in source window" in l for l in lines)
    assert "/ab" in lines


def test_render_returns_renderables_and_never_sorts_or_decides_literals(fake_clock):
    view = fixture_view("base", fake_clock, Session(show_historical=True))
    group = render(view, policy_for(120))
    assert len(group.renderables) == len(framed_screen_lines(view, policy_for(120)))
    text = Path(render_module.__file__).read_text(encoding="utf-8")
    assert not re.search(
        r"observe\.(adapter|collector|parse)\b|sorted\(|\.sort\(|from_markup|Console\(",
        text,
    )


# -- R2: the coordinator questions panel on screen (T19, T47, T49, T12, T11, T23) ------------------------------------------

from superclaude.cli.observe.view import (  # noqa: E402
    QUESTIONS_NOT_HELD,
    Key,
    apply_key,
)
from tests.observe.conftest import (  # noqa: E402
    QRUN,
    make_question_envelope,
    make_question_error,
    make_question_rows,
    routed_runner_responses,
)


def question_result(message, clock, n_workers=4):
    worker = (0, json.dumps(make_envelope(make_rows(n_workers, 1), total=n_workers)))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    collector = Collector(
        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
    )
    return collector, collector.run_once()


def ok_message(rows):
    return 0, json.dumps(make_question_envelope(rows))


@pytest.mark.parametrize("width", WIDTHS)
def test_t19_the_screen_carries_the_title_disclosure_and_one_line_per_question(
    fake_clock, width
):
    _, result = question_result(ok_message(make_question_rows(5)), fake_clock)
    lines = screen_lines(build_view(result, Session(), fake_clock), policy_for(width))
    flat = " ".join(" ".join(lines).split())
    assert "COORDINATOR QUESTIONS" in flat
    assert f"one Run only: {QRUN}" in flat
    assert "at most 100 rows per read, not 100 questions" in flat
    assert "bounded best effort; coverage unknown" in flat
    assert "bursts over 100 rows between reads may be lost" in flat
    # the count whole on one line: the strip's middle row at 160 and 116 (full words), the list
    # line at 80 (the two short forms, owner ruling 2026-11-18)
    want = (
        "seen, not resolved: 5 | closed by evidence: unavailable (no source)"
        if width > 80
        else "seen !done: 5 | proof-done: unavailable (no source)"
    )
    assert any(want in ln for ln in lines)
    assert (
        "retention reset at 12:00; questions observed before this start are not retained"
        in flat
    )
    assert len(question_rows(lines)) == 5
    assert "synthetic body" not in flat and GAP_NOTICE not in lines
    assert all(cell_len(l) <= width for l in lines)


@pytest.mark.parametrize("height", [40, 24, 14])
@pytest.mark.parametrize("width", WIDTHS)
def test_every_screen_line_fits_at_160_116_and_80_with_the_panel(
    fake_clock, width, height
):
    rows = make_question_rows(
        30, subject="界" * 60 + " [bold]x[/bold] very long subject " * 4
    )
    _, result = question_result(ok_message(rows), fake_clock)
    policy = policy_for(width, height=height)
    lines = framed_screen_lines(build_view(result, Session(), fake_clock), policy)
    assert all(cell_len(l) <= width for l in lines)
    assert len(lines) <= height or policy.too_small
    if height >= 24:
        assert any("[bold]x[/bold]" in l or "界" in l for l in lines)


def test_a_long_question_list_is_windowed_with_x_of_y_shown(fake_clock):
    _, result = question_result(ok_message(make_question_rows(60)), fake_clock)
    policy = policy_for(120, height=30)
    lines = screen_lines(build_view(result, Session(), fake_clock), policy)
    shown = [l for l in lines if l.startswith("questions shown ") and "of 60" in l]
    assert len(shown) == 1 and len(lines) <= 30
    assert len(question_rows(lines)) < 60
    assert any(
        l.startswith("collected") or "collected 4" in l for l in lines
    )  # counts stay


def test_t47_questions_off_the_screen_is_the_release_1_screen(fake_clock):
    off = fixture_view("base", fake_clock)
    lines = screen_lines(off, policy_for(160))
    assert any(l.startswith(GAP_NOTICE) for l in lines)  # the note shares its row
    # the attention pane carries the gap notice under the questions title; no questions panel
    assert not any(
        "question read" in l or "RETAIN CONTEXT" in l or "seen, not resolved" in l
        for l in lines
    )
    assert any("messages UNVERIFIED (not read)" in l for l in lines)


def test_the_pending_screen_keeps_the_gap_notice_and_adds_one_pending_line(fake_clock):
    collector, _ = question_result(ok_message([]), fake_clock)
    pending = collector.latest()  # a fresh collector's NOT_POLLED result
    fresh = Collector(
        LiveSource(FakeRunner([], [(0, "{}")]), FakeDiscover([])),
        fake_clock,
        run_id=QRUN,
        questions=True,
    ).latest()
    lines = screen_lines(build_view(fresh, Session(), fake_clock), policy_for(160))
    assert GAP_NOTICE in lines
    assert any("question read pending" in l for l in lines)
    assert pending.question_state == "OK"


def test_the_fenced_state_names_the_sentence_and_keeps_the_retained_lines(fake_clock):
    fenced = (1, json.dumps(make_question_error("consumer_fenced")))
    collector, first = question_result(
        [ok_message(make_question_rows(2)), fenced], fake_clock
    )
    second = collector.run_once()
    lines = screen_lines(build_view(second, Session(), fake_clock), policy_for(160))
    flat = " ".join(lines)
    assert "FAILED (consumer-fenced)" in flat and QUESTIONS_NOT_HELD in flat
    assert len(question_rows(lines)) == 2
    assert "seen, not resolved: 2 |" in flat and first.question_state == "OK"


def test_t12_a_question_that_left_the_window_stays_listed_on_screen(fake_clock):
    collector, _ = question_result(
        [ok_message(make_question_rows(2)), ok_message(make_question_rows(2, start=1))],
        fake_clock,
    )
    lines = screen_lines(
        build_view(collector.run_once(), Session(), fake_clock), policy_for(160)
    )
    assert sum("no longer in source window" in l for l in lines) == 1
    assert len(question_rows(lines)) == 3


def test_an_empty_good_read_screen_says_not_proof_and_never_no_questions(fake_clock):
    _, result = question_result(ok_message([]), fake_clock)
    lines = screen_lines(build_view(result, Session(), fake_clock), policy_for(160))
    flat = " ".join(lines)
    assert "no observed questions in this source window; not proof none exist" in flat
    assert "no questions" not in flat.lower()


def test_window_full_text_is_on_screen_at_exactly_100_rows(fake_clock):
    _, result = question_result(ok_message(make_question_rows(100)), fake_clock)
    lines = screen_lines(
        build_view(result, Session(), fake_clock), policy_for(160, height=60)
    )
    assert "window full: older questions may be missing" in lines


@pytest.mark.parametrize("height", [1, 3, MIN_ROWS - 1])
def test_t49_the_too_small_diagnostic_carries_a_question_source_line(
    fake_clock, height
):
    _, result = question_result(ok_message(make_question_rows(2)), fake_clock)
    view = build_view(result, Session(), fake_clock)
    lines = screen_lines(view, policy_for(120, height=height))
    assert lines[0].startswith("terminal too small")
    flat = "".join("".join(lines).split())  # the summary may wrap on a narrow screen
    assert "".join(view.gap_notice.split()) in flat
    assert view.gap_notice.startswith("coordinator questions:")
    assert "coveragenknown" not in flat and "coverageunknown" in flat


@pytest.mark.parametrize("width", [79, 60, 40])
def test_below_80_columns_the_diagnostic_keeps_the_question_source_line(
    fake_clock, width
):
    _, result = question_result(ok_message(make_question_rows(2)), fake_clock)
    view = build_view(result, Session(), fake_clock)
    lines = screen_lines(view, policy_for(width))
    flat = "".join("".join(lines).split())
    assert "".join(view.gap_notice.split()) in flat
    assert all(cell_len(l) <= width for l in lines)


def test_the_inspector_keeps_room_by_showing_only_the_one_line_summary(fake_clock):
    _, result = question_result(ok_message(make_question_rows(40)), fake_clock)
    session, _ = apply_key(
        Session(), Key("down"), build_view(result, Session(), fake_clock), fake_clock
    )
    session, _ = apply_key(
        session, Key("enter"), build_view(result, session, fake_clock), fake_clock
    )
    view = build_view(result, session, fake_clock)
    lines = screen_lines(view, policy_for(120, height=30))
    flat = "".join("".join(lines).split())
    assert view.focus == "inspector" and "".join(view.gap_notice.split()) in flat
    assert not question_rows(lines)  # the inspector shows no question rows


def test_ascii_mode_renders_only_ascii_for_a_non_ascii_subject(fake_clock):
    rows = make_question_rows(2, subject="héllo wörld 界")
    _, result = question_result(ok_message(rows), fake_clock)
    lines = screen_lines(
        build_view(result, Session(), fake_clock), policy_for(120, ascii=True)
    )
    assert all(ord(ch) < 128 for l in lines for ch in l)
    assert not any(bad_chars(l) for l in lines)


def test_rendering_the_panel_twice_is_byte_identical(fake_clock):
    _, result = question_result(ok_message(make_question_rows(7)), fake_clock)
    view = build_view(result, Session(), fake_clock)
    policy = policy_for(116)
    assert printed(view, policy) == printed(view, policy)


# -- T47: questions off is byte-identical to release 1 (against release 1's own recorded bytes) ------------------------


def test_presentation_goldens_hold_no_escape_bytes():
    """A styled capture can never be written into a presentation golden."""
    here = Path(__file__).parent
    for name in ("golden_release1_surface.json", "golden_questions_linkoff.json"):
        text = (here / name).read_text(encoding="utf-8")
        assert "\x1b" not in text and "\\u001b" not in text, name


def test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface():
    """Pins the recorded presentation (the plain screen lines and printed text of the five
    questions-off variants). The release-1 record guarantee is held by
    ``golden_release1_records.json`` in the next test, which is never regenerated."""
    from tests.observe.release1_surface import surface

    golden = json.loads(
        (Path(__file__).parent / "golden_release1_surface.json").read_text(
            encoding="utf-8"
        )
    )
    current = surface()
    assert current.keys() == golden.keys()
    for variant, expected in golden.items():
        assert current[variant].keys() == expected.keys(), variant
        for key, text in expected.items():
            assert current[variant][key] == text, f"{variant}:{key}"


RECORD_KEYS = ("header1", "header2", "gap_notice", "record_text", "snapshot_json")


def test_release1_records_are_byte_identical_to_the_recorded_surface():
    """The record, the JSON snapshot and the three header texts of release 1, kept apart from
    the screen lines so they stay enforced after the presentation golden is re-baselined.
    ``golden_release1_records.json`` is never regenerated."""
    from tests.observe.release1_surface import surface

    path = Path(__file__).parent / "golden_release1_records.json"
    golden = json.loads(path.read_text(encoding="utf-8"))
    current = surface()
    assert current.keys() == golden.keys()
    for variant, expected in golden.items():
        assert expected.keys() == set(RECORD_KEYS), variant
        for key, text in expected.items():
            assert current[variant][key] == text, f"{variant}:{key}"
    # The file itself is the recorded serialisation of exactly these keys.
    subset = {v: {k: e[k] for k in RECORD_KEYS} for v, e in current.items()}
    assert json.dumps(
        subset, indent=1, sort_keys=True, ensure_ascii=False
    ) == path.read_text(encoding="utf-8")


# -- R2 UX review follow-up (2026-11-12): owner decisions and the critical and high findings -------------------------------

import dataclasses  # noqa: E402

from superclaude.cli.observe.view import QUESTIONS_KEYS_LINE  # noqa: E402
from tests.observe.conftest import FakeClock  # noqa: E402


def flat_of(lines):
    return " ".join(" ".join(lines).split())


def test_decision_1_when_cut_the_oldest_questions_stay_and_the_screen_says_so(
    fake_clock,
):
    rows = make_question_rows(20)
    _, result = question_result(ok_message(rows), fake_clock)
    view = build_view(result, Session(), fake_clock)
    lines = screen_lines(view, policy_for(120, height=24))
    cut = [ln for ln in lines if ln.startswith("questions shown ")]
    assert len(cut) == 1 and "oldest first" in cut[0] and "newer not shown" in cut[0]
    assert "e exports all" in cut[0]
    shown = question_rows(lines)
    oldest = sorted(r["created_at"] for r in rows)[0]
    assert shown and view.questions.lines[0].created_at == oldest
    assert (
        shown[0].split("  ", 1)[1].startswith("synthetic question 0")
    )  # the oldest first
    assert not any(
        "synthetic question 19" in ln for ln in lines
    )  # the newest is the one cut


def test_decision_2_the_questions_win_on_a_short_terminal_the_ledger_is_squeezed(
    fake_clock,
):
    _, result = question_result(
        ok_message(make_question_rows(8)), fake_clock, n_workers=30
    )
    view = build_view(result, Session(), fake_clock)
    framed = framed_screen_lines(view, policy_for(120, height=26))
    lines = unframed(framed)
    # Measured with the count strip (5 rows) in place and the RETAIN pane dropped: 4 of the 8
    # questions fit (at least MIN_QUESTION_ROWS = 3 are kept) and the cut line says so; the ledger
    # is squeezed to its one forced row. The owner's rule "the questions win on a short terminal"
    # still holds: the ledger gives way before the list, and the strip and the RETAIN pane
    # give way before fewer than 3 rows of the list.
    assert len(question_rows(lines)) == 4
    assert any(ln.startswith("questions shown 4 of 8") for ln in lines)
    ledger_rows = [ln for ln in lines if " w-0" in ln]
    assert len(ledger_rows) == 1
    assert any(re.search(r"shown 1/30$", ln) for ln in lines)
    flat = flat_of(lines)  # nothing is lost with the RETAIN pane dropped
    assert (
        flat.count("one Run only:") == 1 and flat.count("no read marker in source") == 1
    )
    assert flat.count("retention reset at") == 1
    assert len(framed) <= 26


def test_decision_3_and_4_the_count_is_seen_not_resolved_and_a_full_window_reads_100_plus(
    fake_clock,
):
    _, result = question_result(ok_message(make_question_rows(100)), fake_clock)
    view = build_view(result, Session(), fake_clock)
    lines = screen_lines(view, policy_for(160, height=200))
    flat = flat_of(lines)
    assert (
        "seen, not resolved: 100+ (window full) | closed by evidence: unavailable"
        in flat
    )
    assert "observed open" not in flat
    assert "window full: older questions may be missing" in flat
    assert "no read marker in source: answered questions stay listed" in flat
    _, short = question_result(ok_message(make_question_rows(99)), fake_clock)
    short_flat = flat_of(
        screen_lines(
            build_view(short, Session(), fake_clock), policy_for(160, height=200)
        )
    )
    assert "seen, not resolved: 99 |" in short_flat and "100+" not in short_flat


def test_f04_the_state_word_comes_before_the_subject_and_is_never_clipped(fake_clock):
    collector, _ = question_result(
        [
            ok_message(make_question_rows(2, subject="x" * 300)),
            ok_message(make_question_rows(2, start=1, subject="y" * 300)),
        ],
        fake_clock,
    )
    result = collector.run_once()
    for width in (160, 116, 80):
        lines = screen_lines(
            build_view(result, Session(), fake_clock), policy_for(width, height=60)
        )
        left = [ln for ln in lines if "[no longer in source window]" in ln]
        assert len(left) == 1 and all(cell_len(ln) <= width for ln in lines)


def test_f07_the_header_cell_names_the_state_in_every_state(fake_clock):
    fenced = (1, json.dumps(make_question_error("consumer_fenced")))
    collector, first = question_result(
        [ok_message(make_question_rows(1)), fenced], fake_clock
    )
    ok_cell = build_view(first, Session(), fake_clock).header2
    assert f"coordinator questions OK 0s (one Run {QRUN})" in ok_cell
    fake_clock.advance(50)
    assert (
        f"coordinator questions STALE 50s (one Run {QRUN})"
        in build_view(first, Session(), fake_clock).header2
    )
    failed = collector.run_once()
    assert (
        f"coordinator questions FAILED (consumer-fenced) (one Run {QRUN})"
        in build_view(failed, Session(), fake_clock).header2
    )
    fresh = Collector(
        LiveSource(FakeRunner([], [(0, "{}")]), FakeDiscover([])),
        fake_clock,
        run_id=QRUN,
        questions=True,
    ).latest()
    assert (
        f"coordinator questions not read yet (one Run {QRUN})"
        in build_view(fresh, Session(), fake_clock).header2
    )


def test_f08_the_key_line_is_never_cut_at_80_columns_when_questions_are_on(fake_clock):
    _, result = question_result(ok_message(make_question_rows(2)), fake_clock)
    lines = screen_lines(
        build_view(result, Session(), fake_clock), policy_for(80, height=40)
    )
    assert " ".join(QUESTIONS_KEYS_LINE.split()) in flat_of(lines[-3:]) or all(
        token in flat_of(lines[-4:])
        for token in ("e export all", "q quit", "m mark rows")
    )
    assert not any(ln.endswith(">") and "exp" in ln for ln in lines)
    assert all(cell_len(ln) <= 80 for ln in lines)


def test_f01_the_collapsed_summary_never_prints_a_bare_number(fake_clock):
    cases = {
        "empty": (
            ok_message([]),
            "seen, not resolved 0 (source window only; not proof none exist)",
        ),
        "full": (
            ok_message(make_question_rows(100)),
            "seen, not resolved 100+ (window full)",
        ),
        "some": (ok_message(make_question_rows(3)), "seen, not resolved 3;"),
    }
    for label, (message, expected) in cases.items():
        _, result = question_result(message, fake_clock)
        view = build_view(result, Session(), fake_clock)
        summary = view.gap_notice
        assert expected in summary, label
        assert (
            "best effort, coverage unknown" in summary
            and "observed open" not in summary
        )
        short = flat_of(screen_lines(view, policy_for(120, height=5)))
        assert expected in short, label


def test_f17_f15_the_failed_state_gives_the_action_and_the_time_of_the_list(fake_clock):
    fenced = (1, json.dumps(make_question_error("no_active_terminal")))
    collector, _ = question_result(
        [ok_message(make_question_rows(2)), fenced], fake_clock
    )
    failed = collector.run_once()
    flat = flat_of(
        screen_lines(
            build_view(failed, Session(), fake_clock), policy_for(160, height=60)
        )
    )
    assert "question read: FAILED (no-active-terminal)" in flat
    assert "list as of 12:00:00 (last good read)" in flat
    assert (
        f"start the observer in the terminal that holds {QRUN} (inferred, not an Orca message)"
        in flat
    )


def test_f39_a_question_from_the_future_shows_age_unknown_not_a_fresh_zero():
    clock = FakeClock()
    rows = make_question_rows(1)
    rows[0]["created_at"] = "2026-11-08T13:00:00Z"  # an hour after the fake clock
    runner = FakeRunner(
        [],
        [
            routed_runner_responses(
                (0, json.dumps(make_envelope(make_rows(1, 1), total=1))),
                ok_message(rows),
            )
        ],
    )
    result = Collector(
        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
    ).run_once()
    panel = build_view(result, Session(), clock).questions
    assert "age unknown (clock skew)" in panel.lines[0].text
    assert panel.lines[0].age_seconds.__class__.__name__ == "_Unknown"


def test_the_latest_empty_read_is_said_when_older_rows_are_listed(fake_clock):
    collector, _ = question_result(
        [ok_message(make_question_rows(2)), ok_message([])], fake_clock
    )
    result = collector.run_once()
    flat = flat_of(
        screen_lines(
            build_view(result, Session(), fake_clock), policy_for(160, height=60)
        )
    )
    assert "latest read returned 0 questions; the rows below are older" in flat
    assert "reasons: none in source" in flat and "no questions" not in flat.lower()
    assert "reason unknown" not in flat  # said once in the title, not per row
    assert dataclasses.is_dataclass(result)


# -- R3: the question text and the Decision Desk on screen (T60, T61, T66) ---------------------------------

from superclaude.cli.observe.view import (  # noqa: E402
    DESK_HIDDEN,
    DESK_SELECTED_HIDDEN,
    DESK_TITLE,
    DESK_UNKNOWN_SCOPE,
    QUESTIONS_LINK_KEYS_LINE,
)
from tests.observe.conftest import question_payload  # noqa: E402


def r3_rows(specs, start=0):
    rows = []
    for index, (dispatch, text) in enumerate(specs, start):
        rows += make_question_rows(
            1, start=index, payload=question_payload(dispatch, text)
        )
    return rows


def r3_screen(
    clock,
    rows,
    selected=0,
    width=160,
    height=40,
    ascii=False,
    no_color=False,
    workers=3,
    raw=False,
):
    """(lines, view) of a link-on questions screen with question ``selected`` chosen. The lines
    are read without their frames unless ``raw`` is true (the checks of frame shape and height)."""
    worker = (0, json.dumps(make_envelope(make_rows(workers, 1), total=workers)))
    runner = FakeRunner([], [routed_runner_responses(worker, ok_message(rows))])
    result = Collector(
        LiveSource(runner, FakeDiscover([])),
        clock,
        run_id=QRUN,
        questions=True,
        link=True,
    ).run_once()
    session = Session(
        selected_question=None if selected is None else (QRUN, f"msg_{selected:012x}")
    )
    view = build_view(result, session, clock)
    policy = policy_for(width, height=height, ascii=ascii, no_color=no_color)
    shown = framed_screen_lines if raw else screen_lines
    return shown(view, policy), view


@pytest.mark.parametrize("width", WIDTHS)
def test_r3_the_selected_question_has_the_selected_glyph_and_the_desk_follows(
    fake_clock, width
):
    lines, view = r3_screen(
        fake_clock, r3_rows([("w-001", "first?"), ("w-002", "second?")]), 1, width
    )
    marked = [ln for ln in lines if ln.startswith("▸ ")]
    assert len(marked) == 1 and marked[0].endswith(
        "second>"
    )  # a strict prefix with `>`
    assert all(cell_len(ln) <= width for ln in lines)
    assert DESK_TITLE in lines and view.desk.ask == "second?"
    flat = flat_of(lines)
    assert "session w-002" in flat and "worktree " in flat
    assert (
        "dispatchId:" not in flat and "resource.worktreeId" not in flat
    )  # plain labels
    ascii_lines, _ = r3_screen(
        fake_clock, r3_rows([("w-001", "first?")]), 0, width, ascii=True
    )
    assert any(ln.startswith("@ ") for ln in ascii_lines)
    assert "\n".join(ascii_lines).isascii()


@pytest.mark.parametrize(
    ("payload", "sender", "reason"),
    [
        (None, "dispatch:w-001", "no payload"),
        ("{bad", "dispatch:w-001", "payload not readable"),
        (json.dumps({"question": "q?"}), "dispatch:w-001", "payload has no dispatchId"),
        (question_payload("w-001", "q?"), "term_x", "sender mismatch"),
    ],
)
def test_r3_each_unlinked_text_shows_in_the_desk(fake_clock, payload, sender, reason):
    rows = make_question_rows(1, payload=payload, from_handle=sender)
    for width in WIDTHS:
        lines, _ = r3_screen(fake_clock, rows, 0, width)
        flat = flat_of(lines)
        assert DESK_TITLE in lines and DESK_UNKNOWN_SCOPE in flat and reason in flat
        assert "dispatchId:" not in flat  # no session fields without a link
        assert all(cell_len(ln) <= width for ln in lines)


@pytest.mark.parametrize("width", (116, 80))
def test_r3_every_linked_question_line_keeps_age_and_state_and_has_no_per_row_reason(
    fake_clock, width
):
    rows = r3_rows([("w-001", "x" * 300), ("w-002", "short?")])
    lines, _ = r3_screen(fake_clock, rows, None, width, height=60)
    question_lines = question_rows(lines)
    assert len(question_lines) == 2
    assert all(cell_len(ln) <= width for ln in question_lines)
    assert not any("reason unknown" in ln for ln in lines)
    assert "reasons: none in source" in flat_of(lines)  # one title note instead
    assert "..." in question_lines[0] or "x" * 20 in question_lines[0]
    assert re.match(r"^\s*\d+[smh]  ", question_lines[0])  # the age stays


def test_r3_a_long_question_shows_a_visible_mark_in_the_desk_and_on_the_list(
    fake_clock,
):
    rows = r3_rows([("w-001", "word " * 200)])
    lines, view = r3_screen(fake_clock, rows, 0, 160, height=60)
    listed = question_rows(lines)
    assert listed and listed[0].endswith(
        ">"
    )  # one short line; the full text is in the desk
    assert "word word word word word word word word word word" not in listed[0]
    text_lines = desk_text_lines(lines)
    assert 1 <= len(text_lines) <= 4 and text_lines[-1].endswith("...")
    assert all(cell_len(ln) <= 160 for ln in lines)


def test_r3_the_desk_text_is_bounded_to_four_lines_with_a_mark_at_80_columns(
    fake_clock,
):
    rows = r3_rows([("w-001", "word " * 200)])
    lines, _ = r3_screen(fake_clock, rows, 0, 80, height=70)
    text_lines = desk_text_lines(lines)
    assert len(text_lines) == 4 and text_lines[-1].endswith("...")
    assert all(cell_len(ln) <= 80 for ln in lines)


def test_r3_a_hostile_question_text_is_inert_on_screen(fake_clock):
    hostile = "[bold]x[/bold] \x1b[31mred 日本語の質問 😀 \x9b0m end"
    for width in WIDTHS:
        lines, _ = r3_screen(fake_clock, r3_rows([("w-001", hostile)]), 0, width)
        text = "\n".join(lines)
        assert bad_chars(text) == [] and "[bold]x[/bold]" in text
        assert all(cell_len(ln) <= width for ln in lines)
        assert "\x1b" not in printed(
            r3_screen(
                fake_clock, r3_rows([("w-001", hostile)]), 0, width, no_color=True
            )[1],
            policy_for(width, no_color=True),
        )


def test_r3_no_color_output_has_no_escape_code(fake_clock):
    _, view = r3_screen(fake_clock, r3_rows([("w-001", "q?")]), 0, no_color=True)
    assert "\x1b" not in printed(view, policy_for(160, no_color=True))


def test_r3_the_desk_gives_way_to_its_notice_and_the_list_is_kept(fake_clock):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    seen = {"desk": 0, "notice": 0, "collapsed": 0}
    for height in range(8, 61):
        lines, _ = r3_screen(fake_clock, rows, 0, 116, height=height)
        flat = flat_of(lines)
        listed = len(question_rows(lines))
        if DESK_TITLE in lines:
            seen["desk"] += 1
            assert listed >= 1 and DESK_HIDDEN not in flat  # the list keeps a line
        elif DESK_HIDDEN in flat and listed:
            seen["notice"] += 1
            assert listed >= 1 and DESK_TITLE not in lines
        elif DESK_HIDDEN in flat:
            seen["collapsed"] += 1  # the one-line summary names the hidden desk
            assert "coordinator questions:" in flat
    assert all(seen.values()), seen


def test_r3_a_selection_beyond_the_shown_window_is_signalled(fake_clock):
    rows = r3_rows([("w-001", f"q{i}?") for i in range(20)])
    lines, _ = r3_screen(fake_clock, rows, 19, 120, height=26)
    flat = flat_of(lines)
    assert DESK_SELECTED_HIDDEN in lines and "questions shown" in flat
    assert not any(ln.startswith("▸ ") for ln in lines)


def test_r3_the_link_on_keys_line_is_shown_only_with_the_link_on(fake_clock):
    lines, view = r3_screen(
        fake_clock, r3_rows([("w-001", "q?")]), None, 160, height=60
    )
    assert view.help_line == QUESTIONS_LINK_KEYS_LINE
    assert any("n/p question" in ln for ln in lines)


# -- Q7: a plan-approval ask with a 64-hex hash and paths in the Decision Desk (pins today's behaviour) ------------------

from superclaude.cli.observe.export import record_text, snapshot_json  # noqa: E402
from tests.observe.conftest import question_rows, sgr_params, strip_sgr  # noqa: E402

HASH = "0123456789abcdef" * 4
# Twin of PLAN_ASK in .dev/issues/409/visual-parity/inputs/tools/render_current.py: keep the two identical.
PLAN_ASK = (
    "Approve the plan in .dev/plans/observer-visual-parity/plan.md before the worker edits "
    "src/superclaude/cli/observe/render.py and src/superclaude/cli/observe/terminal.py "
    f"(plan hash {HASH})?"
)
# A path list that fills the four desk lines at 80 columns, with the hash last (under ASK_CAP = 400).
PATHS_THEN_HASH = (
    " ".join(f"src/superclaude/cli/observe/module_{i:02d}.py" for i in range(8))
    + f" {HASH}"
)


def pane_rows(lines, title):
    """``title`` and the body rows of its pane in the unframed ``lines``, up to the next pane
    title (or the ledger title). The panes of a two-column desk are read one after the other."""
    pane = lines[lines.index(title) :]
    stops = (
        "COORDINATOR QUESTIONS",
        "RETAIN CONTEXT",
        "DECISION DESK",
        "LINKED SESSION",
    )
    end = next(
        (
            i
            for i, ln in enumerate(pane)
            if i and (ln.startswith(stops) or ln.startswith("worker-reported"))
        ),
        len(pane),
    )
    return pane[:end]


def desk_text_lines(lines):
    """The question-text lines of the unframed Decision Desk: its body after the age line."""
    return pane_rows(lines, DESK_TITLE)[2:]


@pytest.mark.parametrize("width", WIDTHS)
def test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk(
    fake_clock, width
):
    assert len(PLAN_ASK) < 400
    rows = r3_rows([("w-001", "first?"), ("w-002", PLAN_ASK)])
    lines, view = r3_screen(fake_clock, rows, 1, width, height=70)
    assert all(cell_len(ln) <= width for ln in lines)
    text = desk_text_lines(lines)
    assert 1 <= len(text) <= 4 and not text[-1].endswith("...")
    assert not any(HASH in ln for ln in lines)  # no hash anywhere on the screen
    assert "".join(text).replace(" ", "") == PLAN_ASK.replace(f"{HASH}", "").replace(
        " ", ""
    )  # the rest of the ask is intact
    assert HASH not in record_text(view) and HASH not in snapshot_json(view)  # canary


@pytest.mark.parametrize("width", WIDTHS)
def test_r3_a_hash_after_a_long_path_list_never_reaches_the_screen(fake_clock, width):
    assert len(PATHS_THEN_HASH) <= 400  # the parse cap (ASK_CAP) does not cut it
    rows = r3_rows([("w-001", PATHS_THEN_HASH)])
    lines, view = r3_screen(fake_clock, rows, 0, width, height=70)
    assert all(cell_len(ln) <= width for ln in lines)
    assert not any(HASH in ln for ln in lines)
    text = desk_text_lines(lines)
    shown = PATHS_THEN_HASH.replace(f" {HASH}", "")  # 327 characters
    if (
        width != 116
    ):  # four lines of 74 (80 columns) or 72 (160, two columns) cut the ask
        assert len(text) == 4 and text[-1].endswith("...")
    else:  # the 110-cell question pane holds the whole ask inside four lines
        assert not text[-1].endswith("...")
        assert "".join(text).replace(" ", "") == shown.replace(" ", "")
    assert HASH not in record_text(view) and HASH not in snapshot_json(view)  # canary


def test_strip_hex_removes_only_runs_of_32_or_more_hex_digits_and_collapses_spaces():
    from superclaude.cli.observe.view import strip_hex

    assert strip_hex(f"plan hash {HASH} ok") == "plan hash ok"
    assert strip_hex(f"(plan hash {HASH})?") == "(plan hash )?"
    assert strip_hex(HASH) == ""
    assert strip_hex("a" * 31) == "a" * 31  # 31 is not a hash
    assert strip_hex("deadbeef cafe 1234") == "deadbeef cafe 1234"  # short words stay
    assert strip_hex("x" + "a" * 32) == "x"  # a long run is removed even inside a word


@pytest.mark.parametrize("width", WIDTHS)
def test_reasons_are_said_once_in_the_title_and_not_on_every_row(fake_clock, width):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    lines, view = r3_screen(fake_clock, rows, 0, width, height=70)
    plain = [strip_sgr(ln) for ln in lines]
    assert not any("reason unknown" in ln for ln in plain)
    assert sum("reasons: none in source" in ln for ln in plain) == 1
    rows_at = [i for i, ln in enumerate(plain) if question_rows([ln])]
    note = next(i for i, ln in enumerate(plain) if "reasons: none in source" in ln)
    assert note > max(rows_at)  # the note stands under the rows: the rows lead the pane
    assert len(question_rows(plain)) == 2
    assert "reason unknown" in record_text(view)  # the record keeps its wording


@pytest.mark.parametrize("width", WIDTHS)
def test_the_question_rows_lead_the_list_pane_and_the_run_id_is_in_its_title(
    fake_clock, width
):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    lines, view = r3_screen(fake_clock, rows, None, width, height=70, raw=True)
    top = next(i for i, ln in enumerate(lines) if "COORDINATOR QUESTIONS" in ln)
    if width == 80:  # the list alone: rows lead it and the Run id is in its title
        assert view.questions.run_id in lines[top]
        assert question_rows([unframe(lines[top + 1])])
    else:  # strip, list, RETAIN: the disclosure, then the rows; the Run id is in RETAIN
        assert view.questions.run_id not in lines[top]
        assert unframe(lines[top + 1]).startswith("bounded best effort")
        first_row = next(
            i for i in range(top + 1, len(lines)) if question_rows([unframe(lines[i])])
        )
        assert all(
            unframe(ln).strip() for ln in lines[top + 1 : first_row]
        )  # only the disclosure lines sit before the first question row


def test_a_row_with_a_reason_shows_it_and_the_title_note_goes(fake_clock):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    lines, view = r3_screen(fake_clock, rows, 0, 160, height=70)
    panel = view.questions
    with_reason = dataclasses.replace(
        panel,
        lines=[
            dataclasses.replace(panel.lines[0], reason="needs a sign-off"),
            *panel.lines[1:],
        ],
    )
    shown = screen_lines(
        dataclasses.replace(view, questions=with_reason), policy_for(160, height=70)
    )
    plain = [strip_sgr(ln) for ln in shown]
    assert sum("needs a sign-off" in ln for ln in plain) == 1
    assert not any("reasons: none in source" in ln for ln in plain)


@pytest.mark.parametrize("width", WIDTHS)
def test_r3_a_120_character_worktree_id_continues_on_two_cell_indented_lines(
    fake_clock, width
):
    worktree = "wt-" + "0123456789" * 11 + "0123456"
    assert len(worktree) == 120
    workers = make_rows(3, 1)
    for row in workers:
        row["resource"] = {"worktreeId": worktree}
    worker = (0, json.dumps(make_envelope(workers, total=3)))
    message = ok_message(r3_rows([("w-001", "first?"), ("w-002", "second?")]))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    result = Collector(
        LiveSource(runner, FakeDiscover([])),
        fake_clock,
        run_id=QRUN,
        questions=True,
        link=True,
    ).run_once()
    session = Session(selected_question=(QRUN, f"msg_{1:012x}"))
    lines = screen_lines(build_view(result, session, fake_clock), policy_for(width, 70))
    assert all(cell_len(ln) <= width for ln in lines)
    start = next(i for i, ln in enumerate(lines) if ln.startswith("worktree"))
    note = "(this session only)"
    # too wide beside its label at every width (evidence inner 76, 62, 74): the label stands
    # alone and the value follows on lines indented two cells (hard-split, nothing lost)
    assert lines[start] == "worktree"
    tail = []
    for ln in lines[start + 1 :]:
        if not ln.startswith("  "):
            break
        tail.append(ln)
    assert tail and all(ln.startswith("  ") for ln in tail)
    shown = "".join(ln[2:] for ln in tail).replace(" ", "")
    assert shown == (worktree + note).replace(" ", "")


@pytest.mark.parametrize("width", WIDTHS)
def test_a_short_non_ascii_evidence_value_is_converted_in_ascii_mode(fake_clock, width):
    workers = make_rows(3, 1)
    for row in workers:
        row["resource"] = {"worktreeId": "工作树"}
    worker = (0, json.dumps(make_envelope(workers, total=3)))
    message = ok_message(r3_rows([("w-001", "first?"), ("w-002", "second?")]))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    result = Collector(
        LiveSource(runner, FakeDiscover([])),
        fake_clock,
        run_id=QRUN,
        questions=True,
        link=True,
    ).run_once()
    session = Session(selected_question=(QRUN, f"msg_{1:012x}"))
    lines = screen_lines(
        build_view(result, session, fake_clock),
        policy_for(width, height=70, ascii=True),
    )
    assert all(
        ln.isascii() for ln in lines
    )  # the terminal policy holds for every field
    assert any(ln.startswith("worktree") and "???" in ln for ln in lines)
    assert all(cell_len(ln) <= width for ln in lines)


def test_strip_sgr_removes_colour_codes_and_sgr_params_lists_them():
    coloured = "\x1b[1;38;2;250;178;25mage\x1b[0m plain \x1b[31mred\x1b[0m"
    assert strip_sgr(coloured) == "age plain red"
    assert sgr_params(coloured) == {"1;38;2;250;178;25", "0", "31"}
    assert strip_sgr("no escapes") == "no escapes" and sgr_params("no escapes") == set()


# -- the Line layer: role spans over plain text ----------------------------------------------------------

from superclaude.cli.observe.render import Line, Span, _roled, join, seg  # noqa: E402
from superclaude.cli.observe.terminal import clip  # noqa: E402


def test_join_shifts_span_offsets_by_characters_not_cells():
    wide = seg("中中", "attention")  # two characters, four cells
    line = join(wide, seg(" "), seg("ab", "muted"))
    assert line.plain == "中中 ab"
    assert line.spans == (Span(0, 2, "attention"), Span(3, 5, "muted"))
    assert cell_len(line.plain) == 7  # the spans are not in cells


def test_a_clipped_line_keeps_its_plain_text_and_trims_its_spans():
    pol = policy_for(80)
    line = seg("x" * 30, "body")
    cut = line.clipped(10, pol)
    assert cut.plain == "x" * 9 + ">" and cut.plain == clip(line.plain, 10, pol)
    assert cut.spans == (Span(0, 9, "body"),)
    assert line.clipped(40, pol) == line  # nothing to cut: unchanged


def test_ascii_mode_replaces_each_character_with_one_question_mark():
    line = join(seg("▸ ", "selected"), seg("中", "body")).to_ascii()
    assert line.plain == "? ?" and line.spans == (
        Span(0, 2, "selected"),
        Span(2, 3, "body"),
    )


def test_roled_wraps_existing_plain_lines_with_one_whole_line_role():
    lines = _roled(["ab", ""], "muted")
    assert lines == [Line("ab", (Span(0, 2, "muted"),)), Line("", ())]


def test_render_colours_a_span_only_when_the_policy_has_a_colour_depth(
    monkeypatch, fake_clock
):
    view = fixture_view("base", fake_clock)
    monkeypatch.setattr(
        render_module,
        "_compose",
        lambda v, p, m=None: [Line("hello world", (Span(0, 5, "attention"),))],
    )
    coloured = printed(view, policy_for(80))
    plain = printed(view, policy_for(80, no_color=True))
    assert "\x1b[" in coloured and strip_sgr(coloured) == plain == "hello world\n"
    assert "\x1b" not in plain


# -- roles assigned at the builders (no text change) ------------------------------------------------------

from superclaude.cli.observe.render import (  # noqa: E402
    _columns,
    _compose,
    _header_lines,
    _row_segments,
)
from superclaude.cli.observe.view import FROZEN_MARKER  # noqa: E402


def roles_at(line, needle):
    """The roles covering the first character of ``needle`` in ``line.plain``."""
    index = line.plain.index(needle)
    return {s.role for s in line.spans if s.start <= index < s.end}


def first_line(lines, needle):
    return next(ln for ln in lines if needle in ln.plain)


@pytest.mark.parametrize("width", WIDTHS)
def test_colour_never_changes_the_text_of_a_questions_screen(fake_clock, width):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    _, view = r3_screen(fake_clock, rows, 1, width, height=60)
    coloured = printed(view, policy_for(width, height=60))
    plain = printed(view, policy_for(width, height=60, no_color=True))
    assert "\x1b" in coloured and strip_sgr(coloured) == plain


def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
    fake_clock,
):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    _, view = r3_screen(fake_clock, rows, 1, 160, height=60)
    lines = _compose(view, policy_for(160, height=60))
    selected = next(ln for ln in lines if "▸ " in ln.plain)
    assert roles_at(selected, "second>") == {"selected"}
    assert roles_at(selected, "▸") == {"selected"}
    assert "reason unknown" not in selected.plain  # said once in the title note
    other = first_line(lines, "first?")
    assert roles_at(other, "first?") == {"body_bold"}
    assert roles_at(other, "1h") == {"attention"}  # the age
    title = first_line(
        lines, "COORDINATOR QUESTIONS"
    )  # inset in the border of a round frame
    assert roles_at(title, "COORDINATOR") == {"secondary"}
    assert roles_at(title, "╭") == {"border_secondary"}
    note = first_line(lines, "reasons: none in source")
    assert roles_at(note, "reasons: none in source") == {"muted"}


def test_absent_values_are_muted_and_state_words_follow_the_table(fake_clock):
    view = fixture_view("missing-fields", fake_clock)
    lines = _compose(view, policy_for(160, height=60))
    text = "\n".join(ln.plain for ln in lines)
    assert "source counts:" not in text and "runs seen" not in text  # in the inspector
    dim = first_line(lines, "no source: settled, frozen, cost")
    assert roles_at(dim, "no source: settled, frozen, cost") == {
        "muted"
    }  # one dim token
    absent = first_line(lines, "● unknown")
    assert roles_at(absent, "● unknown") == {"muted"}  # the bare verdict, spelled out
    assert any(
        roles_at(ln, "running") == {"state_running"}
        for ln in lines
        if " running " in ln.plain
    )
    blocked = first_line(
        lines, "blocked/active/none"
    )  # not in the table: body, never a state role
    assert roles_at(blocked, "blocked/active/none") == {"body"}


def test_a_frozen_flag_cell_takes_the_frozen_role(fake_clock):
    view = fixture_view("base", fake_clock)
    policy = policy_for(160)
    columns, getters = _columns(policy, 160)
    row = dataclasses.replace(
        view.window(1).rows[0], flags=(FROZEN_MARKER,), frozen=True
    )
    line = _row_segments(row, columns, getters, policy, 160)
    assert roles_at(line, FROZEN_MARKER) == {"state_frozen"}


# -- text defects of the existing layouts: heading, whole key groups, footer rule, counts -----------------------

from superclaude.cli.observe.render import wrap_groups  # noqa: E402


def heading_index(lines):
    return next(
        (
            i
            for i, ln in enumerate(lines)
            if "dispatchId" in ln and "age" in ln and "w-0" not in ln
        ),
        None,
    )


@pytest.mark.parametrize("width", WIDTHS)
def test_the_column_heading_shows_at_every_width_with_no_rule_row_under_it(
    fake_clock, width
):
    lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
    i = heading_index(lines)
    assert i is not None
    assert "w-0" in lines[i + 1]  # the first row follows the heading directly
    assert not any(set(ln) <= {"─", " "} and "─" in ln for ln in lines[:-4])


@pytest.mark.parametrize("width", WIDTHS)
def test_no_heading_when_there_are_no_rows(fake_clock, width):
    lines = screen_lines(fixture_view("empty", fake_clock), policy_for(width))
    assert heading_index(lines) is None


@pytest.mark.parametrize("width", WIDTHS)
def test_the_key_list_is_never_cut_and_no_key_pair_is_split(fake_clock, width):
    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(width))
    groups = [g for g in view.help_line.split("  ") if g]
    assert all(any(g in ln for ln in lines) for g in groups)
    assert not any(ln.endswith(" >") or ln.endswith("e exp>") for ln in lines[-6:])
    assert any("q quit" in ln for ln in lines[-3:])


@pytest.mark.parametrize("width", WIDTHS)
def test_a_rule_line_precedes_the_footer_keys(fake_clock, width):
    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(width))
    first_key = next(i for i, ln in enumerate(lines) if "j/k move" in ln)
    assert (
        set(lines[first_key - 1]) == {"─"} and cell_len(lines[first_key - 1]) == width
    )


def test_the_link_on_key_pair_n_p_question_stays_on_one_line_at_every_width(fake_clock):
    rows = r3_rows([("w-001", "q?")])
    for width in WIDTHS:
        lines, _ = r3_screen(fake_clock, rows, None, width, height=60)
        assert any("n/p question" in ln for ln in lines)


def test_wrap_groups_packs_whole_groups_and_falls_back_to_wrap_for_a_wide_group():
    pol = policy_for(80)
    assert wrap_groups("a b  c d  e f", 20, pol) == ["a b  c d  e f"]
    assert wrap_groups("a b  c d  e f", 8, pol) == ["a b  c d", "e f"]  # 8 cells fit
    assert wrap_groups("a b  c d  e f", 7, pol) == ["a b", "c d", "e f"]
    assert wrap_groups("x" * 15, 10, pol) == ["x" * 10, "x" * 5]  # one wide group
    assert wrap_groups("", 10, pol) == [""]


def test_the_truncation_marker_drops_whole_tokens_until_it_fits_and_never_cuts_one():
    from superclaude.cli.observe.render import counts_lines
    from superclaude.cli.observe.view import CountsToken

    pol = dataclasses.replace(policy_for(80), width=20)
    tokens = (
        CountsToken("a" * 10, True),
        CountsToken("b" * 8, False),  # fills the line exactly: no room for " >"
        CountsToken("cc", False),
    )
    assert counts_lines(tokens, pol, max_lines=1) == ["a" * 10 + " >"]
    # a lone unprotected token wider than the line is dropped whole, never cut inside
    wide = (CountsToken("x" * 30, False),)
    assert counts_lines(wide, pol, max_lines=None) == [">"]


@pytest.mark.parametrize("width", WIDTHS)
def test_no_counts_line_ends_inside_a_token(fake_clock, width):
    lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
    for ln in lines[:6]:
        if ln.endswith(">"):
            assert ln[-2] == " ", ln  # the marker follows a whole token


# -- the title bar and its READ ONLY badge -----------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_the_read_only_badge_is_right_aligned_once_and_every_line_fits(
    fake_clock, width
):
    from superclaude.cli.observe.view import READ_ONLY_BADGE

    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(width))
    badged = [ln for ln in lines if READ_ONLY_BADGE in ln]
    assert len(badged) == 1
    index = lines.index(badged[0])
    assert index <= 1  # the title wraps to at most two lines
    assert cell_len(badged[0]) == width and badged[0].endswith(READ_ONLY_BADGE)
    title = " ".join(lines[: index + 1]).replace(READ_ONLY_BADGE, "")
    assert " ".join(title.split()) == " ".join(
        view.screen_header1.split()
    )  # the title text, without ``mode=`` and ``as of``
    assert "mode=" not in title and "as of" not in title
    assert "mode=" in view.header1 and "as of" in view.header1  # the record keeps them
    assert all(cell_len(ln) <= width for ln in lines)


def test_the_badge_role_is_attention_and_the_title_keeps_its_role(fake_clock):
    from superclaude.cli.observe.view import READ_ONLY_BADGE

    view = fixture_view("base", fake_clock)
    first = _compose(view, policy_for(160))[0]
    assert roles_at(first, READ_ONLY_BADGE) == {"attention"}
    assert roles_at(first, "ORCA OBSERVER") == {"title"}


def test_the_badge_moves_to_the_last_title_line_or_its_own_line_when_it_does_not_fit():
    from superclaude.cli.observe.render import _title_bar
    from superclaude.cli.observe.view import READ_ONLY_BADGE

    pol = dataclasses.replace(policy_for(80), width=30)
    fits_last = _title_bar(["x" * 30, "short"], pol)
    assert fits_last[0].plain == "x" * 30 and fits_last[1].plain.endswith(
        READ_ONLY_BADGE
    )
    own_line = _title_bar(["x" * 30, "y" * 30], pol)
    assert len(own_line) == 3 and own_line[2].plain == READ_ONLY_BADGE.rjust(30)
    ascii_pol = dataclasses.replace(pol, ascii=True)
    assert _title_bar(["ab"], ascii_pol)[0].plain.isascii()


def test_the_record_title_keeps_no_badge(fake_clock):
    from superclaude.cli.observe.view import READ_ONLY_BADGE

    assert READ_ONLY_BADGE not in record_text(fixture_view("base", fake_clock))


# -- Task 14: each fact once, questions first, aligned desk labels, one status badge --------------------------

CENSUS_ASK = "Approve the release notes before the worker publishes the package to the registry today?"


@pytest.mark.parametrize("width", WIDTHS)
def test_each_fact_occurs_once_on_the_questions_screen(fake_clock, width):
    rows = r3_rows([("w-001", "first?"), ("w-002", CENSUS_ASK)])
    lines, view = r3_screen(fake_clock, rows, 1, width, height=70)
    flat = flat_of(lines)
    assert (
        flat.count(CENSUS_ASK) == 1
    )  # the desk holds the full text; the list row is a stub
    selected = next(ln for ln in lines if ln.startswith("▸ "))
    assert selected.endswith(">") and CENSUS_ASK not in selected
    assert flat.count(QRUN) == 1  # the Run id: the panel title row only
    # one count: the full words at 160 and 116, the 10-character short forms at 80
    full, short = "seen, not resolved", "seen !done"
    assert flat.count(full if width > 80 else short) == 1
    assert flat.count(short if width > 80 else full) == 0
    assert flat.count("closed by evidence" if width > 80 else "proof-done") == 1
    assert (
        flat.count("questions OK 0s") == 1
    )  # the strip cell; the panel keeps "question read:"
    assert flat.count("question read: OK 0s") == 1
    assert flat.count("msg_") == 0  # the message id is not on the desk pane
    assert flat.count("worker-reported, not questions") == 1
    assert flat.count("retention reset at") == 1


# -- Task 15: the ledger diet ----------------------------------------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_the_ledger_has_no_flags_column_no_rule_row_and_no_more_row(fake_clock, width):
    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(width, height=24))
    head = heading_index(lines)
    assert head is not None and "flags" not in lines[head]
    assert not any(re.search(r"\+\d+ more", ln) for ln in lines)  # no "+N more" row
    footer = next(i for i, ln in enumerate(lines) if "j/k move" in ln)
    assert set(lines[footer - 1]) == {"─"}  # the footer rule is the one rule left
    assert "─" not in "".join(lines[: footer - 1])
    assert re.search(r"shown \d+/54$", lines[footer])  # 26 historical rows are hidden
    assert "collected" not in lines[footer]


@pytest.mark.parametrize("no_color", [False, True])
@pytest.mark.parametrize("width", WIDTHS)
def test_a_non_alive_value_is_spelled_out_and_the_legend_says_so(
    fake_clock, width, no_color
):
    view = fixture_view("missing-fields", fake_clock)
    lines = screen_lines(view, policy_for(width, height=60, no_color=no_color))
    assert any("● unknown" in ln for ln in lines)  # a word, not only a colour
    assert view.ledger_title in lines  # the title of the ledger pane
    assert "● alive; any other state is spelled out" in lines  # its legend row


@pytest.mark.parametrize(
    ("needed", "width", "expected"),
    [
        (28, 80, 28),
        (31, 80, 28),
        (38, 116, 38),
        (38, 160, 38),
        (90, 80, 28),
        (None, 160, 36),
    ],
)
def test_the_status_column_grows_to_the_widest_status_and_leaves_the_id_room(
    needed, width, expected
):
    columns, _ = _columns(policy_for(width), width, needed)
    widths = dict(columns)
    assert widths["status"] == expected
    assert (
        widths["dispatchId"] >= 20 and sum(widths.values()) + len(columns) - 1 <= width
    )


# -- Task 25: the table is parametrised by the cells it may use ----------------------------------------------------


@pytest.mark.parametrize("width", WIDTHS)
def test_the_columns_fit_the_cells_they_are_given_and_keep_their_set(width):
    names = {
        160: [
            "",
            "dispatchId",
            "run",
            "workerState",
            "status",
            "nextAction.kind",
            "alive",
            "evidence age",
        ],
        116: ["", "kind", "dispatchId", "alive", "status", "age"],
        80: ["", "kind", "dispatchId", "alive", "status", "age"],
    }[width]
    for avail in (width, width - 2):  # the screen, or a border-only frame around it
        columns, getters = _columns(policy_for(width), avail, 35, 7, 146)
        assert [name for name, _ in columns] == names and len(getters) == len(columns)
        assert sum(w for _, w in columns) + len(columns) - 1 <= avail


@pytest.mark.parametrize("width", WIDTHS)
def test_rows_and_heading_clip_to_the_cells_they_are_given(fake_clock, width):
    view = fixture_view("long-identifiers", fake_clock)
    policy = policy_for(width)
    avail = width - 2
    columns, getters = _columns(policy, avail, 35, 7, 146)
    assert cell_len(_header_lines(columns, policy, avail)[0].plain) <= avail
    for row in view.all_rows:
        line = _row_segments(row, columns, getters, policy, avail)
        assert cell_len(line.plain) <= avail


@pytest.mark.parametrize("width", WIDTHS)
def test_the_merged_status_cell_keeps_all_three_raw_values_uncut(fake_clock, width):
    view = fixture_view("base", fake_clock, Session(show_historical=True))
    lines = screen_lines(view, policy_for(width, height=100))
    triples = {
        f"{rv.dispatch_status}/{rv.terminal_state}/{rv.outcome}"
        for rv in view.visible_rows
        if (rv.dispatch_status, rv.terminal_state, rv.outcome)
        != ("active", "active", "none")
    }
    assert triples  # the fixture has non-active combinations
    text = "\n".join(lines)
    assert all(triple in text for triple in triples)


def test_the_status_cell_is_one_badge_or_three_raw_values(fake_clock):
    lines = screen_lines(
        fixture_view("missing-fields", fake_clock), policy_for(160, height=60)
    )
    assert any(" ACTIVE " in f" {ln} " for ln in lines)
    assert any("blocked/active/none" in ln for ln in lines)  # any other combination


@pytest.mark.parametrize("width", WIDTHS)
def test_the_frozen_marker_reaches_the_status_cell_at_every_width(fake_clock, width):
    base = fixture_view("base", fake_clock, Session(show_historical=True))
    lines = screen_lines(base, policy_for(width, height=100))
    frozen = next(ln for ln in lines if "w-003" in ln)
    assert "FROZEN" in frozen


@pytest.mark.parametrize("width", WIDTHS)
def test_the_title_has_no_mode_and_no_as_of_and_the_scope_shows_once(fake_clock, width):
    lines = screen_lines(fixture_view("base", fake_clock), policy_for(width))
    text = " ".join(lines)
    assert "mode=" not in text and "as of" not in text
    assert text.count("scope=all") == 1
    assert "no source: settled, frozen, cost" in text
    assert "unavailable (no source)" not in text
    assert "runs seen" not in text  # in the inspector
    assert "source counts: active" in text  # known counts stay; unknown ones leave


def test_source_counts_and_runs_seen_live_in_the_inspector(fake_clock):
    view = fixture_view("base", fake_clock)
    labels = [label for label, _ in view.visible_rows[0].inspector]
    assert "source counts" in labels and "runs seen" in labels


@pytest.mark.parametrize("width", WIDTHS)
def test_the_gap_notice_and_the_historical_note_share_one_row(fake_clock, width):
    view = fixture_view("base", fake_clock)
    lines = screen_lines(view, policy_for(width))
    row = next(ln for ln in lines if ln.startswith("Human questions"))
    assert "26 historical hidden (h)" in row or width == 80  # 80: too wide for one row
    assert sum("26 historical hidden (h)" in ln for ln in lines) == 1


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("text", ["Ship it now?", "ab?", "x" * 24, "y" * 25])
def test_a_short_selected_question_is_also_on_the_screen_once(fake_clock, width, text):
    lines, _ = r3_screen(fake_clock, r3_rows([("w-001", text)]), 0, width, height=70)
    assert flat_of(lines).count(text) == 1
    assert next(ln for ln in lines if ln.startswith("▸ ")).endswith(">")


@pytest.mark.parametrize("width", WIDTHS)
def test_question_rows_come_first_then_the_standing_lines_adjacent(fake_clock, width):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    lines, view = r3_screen(fake_clock, rows, None, width, height=70)
    last_row = max(i for i, ln in enumerate(lines) if question_rows([ln]))
    first_row = min(i for i, ln in enumerate(lines) if question_rows([ln]))
    disclosure = next(
        i for i, ln in enumerate(lines) if ln.startswith("bounded best effort")
    )
    marker = next(i for i, ln in enumerate(lines) if "no read marker in source" in ln)
    retention = next(i for i, ln in enumerate(lines) if "retention reset at" in ln)
    if width == 80:  # the list alone: the rows lead, the standing lines follow
        assert last_row < disclosure < marker
    else:  # the disclosure leads the list, the caveat and retention are in RETAIN CONTEXT
        assert disclosure < first_row <= last_row < marker
    assert retention == marker + len(wrap_text(view.questions.caveat_line, width))
    assert "".join(lines[disclosure : disclosure + 1]).startswith(
        "bounded best effort; coverage unknown"
    )


def wrap_text(text, width):
    return render_module.wrap(text, width, policy_for(width))


def desk_after(fake_clock, mutate, width=116):
    """The desk pane lines of a linked question whose worker row was changed by ``mutate``."""
    workers = make_rows(3, 1)
    for row in workers:
        mutate(row)
    worker = (0, json.dumps(make_envelope(workers, total=3)))
    message = ok_message(r3_rows([("w-001", "first?"), ("w-002", "second?")]))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    result = Collector(
        LiveSource(runner, FakeDiscover([])),
        fake_clock,
        run_id=QRUN,
        questions=True,
        link=True,
    ).run_once()
    session = Session(selected_question=(QRUN, f"msg_{1:012x}"))
    lines = screen_lines(build_view(result, session, fake_clock), policy_for(width, 70))
    return pane_rows(lines, DESK_EVIDENCE_TITLE)


def test_the_full_worktree_note_lives_in_the_inspector_only_with_questions_on(
    fake_clock,
):
    from superclaude.cli.observe.view import DESK_WORKTREE_NOTE

    lines, view = r3_screen(
        fake_clock, r3_rows([("w-001", "first?")]), 0, 160, height=70
    )
    assert DESK_WORKTREE_NOTE not in flat_of(lines)  # the desk shows it short
    assert ("worktree note", DESK_WORKTREE_NOTE) in view.all_rows[0].inspector
    off = fixture_view("base", fake_clock)
    assert all(
        label != "worktree note" for row in off.all_rows for label, _ in row.inspector
    )


def test_desk_labels_are_plain_aligned_and_alive_is_one_value(fake_clock):
    desk = desk_after(fake_clock, lambda row: None)
    fields = {
        ln[:9].strip(): ln[9:] for ln in desk[1:] if ln[:1].isalpha() and ln[8:9] == " "
    }
    assert list(fields) == ["session", "state", "alive", "next", "status", "worktree"]
    assert fields["session"] == "w-002" and fields["state"] == "idle"
    assert fields["alive"] == "yes (terminal), 6s ago"
    assert fields["status"] == "ACTIVE"
    assert (
        fields["worktree"].endswith("(this session only)")
        or fields["worktree"] == "unknown"
    )
    assert not any(raw in " ".join(desk) for raw in ("dispatchStatus", "terminalState"))


def test_the_active_badge_needs_active_active_none_else_three_raw_rows(fake_clock):
    def changed(row):
        row["projection"]["outcome"] = "blocked"

    desk = desk_after(fake_clock, changed)
    text = "\n".join(desk)
    assert "ACTIVE" not in text
    for raw, value in (
        ("dispatchStatus", "active"),
        ("terminalState", "active"),
        ("outcome", "blocked"),
    ):
        assert any(ln.startswith(raw) and ln.endswith(value) for ln in desk), raw
    assert not any(ln.startswith("status ") for ln in desk)


def test_an_absent_status_value_expands_to_three_rows_and_reads_unknown(fake_clock):
    def absent(row):
        del row["terminalState"]

    desk = desk_after(fake_clock, absent)
    assert "ACTIVE" not in "\n".join(desk)
    terminal = next(ln for ln in desk if ln.startswith("terminalState"))
    assert terminal.endswith("unknown") and "absent in source" not in terminal
    assert any(ln.startswith("dispatchStatus") for ln in desk)
    assert any(ln.startswith("outcome") for ln in desk)


# -- Task 22: the two-column composer and the evidence field lines ---------------------------------------------

from superclaude.cli.observe.render import (  # noqa: E402
    _desk_widths,
    _field_lines,
    _label_width,
    _two_columns,
)
from superclaude.cli.observe.view import DESK_EVIDENCE_TITLE  # noqa: E402
from tests.observe.conftest import panes_flat, split_columns  # noqa: E402


@pytest.mark.parametrize(
    ("status", "role"), [("completed", "state_settled"), ("failed", "state_failed")]
)
def test_a_raw_dispatch_status_row_takes_its_state_role(status, role):
    from superclaude.cli.observe.render import _desk_rows

    fields = (
        ("dispatchStatus", status),
        ("terminalState", "released"),
        ("outcome", "succeeded"),
    )
    rows = {label: r for label, _, r in _desk_rows(fields)}
    assert rows["dispatchStatus"] == role
    assert rows["outcome"] == "body"  # not in the table: never a state role


def test_the_evidence_title_is_the_named_literal():
    assert DESK_EVIDENCE_TITLE == "LINKED SESSION"


def test_two_columns_pads_the_left_and_shifts_the_right_spans_by_characters():
    pol = policy_for(160)
    left = [
        seg("界" * 3, "body"),
        seg("ab", "attention"),
    ]  # a wide character: 3 chars, 6 cells
    right = [seg("xx", "state_running"), seg("yy", "muted"), seg("zz", "identity")]
    rows = _two_columns(left, right, 10, 5)
    assert [cell_len(r.plain) for r in rows[:2]] == [10 + 2 + 2] * 2
    assert rows[2].plain.endswith("zz") and rows[2].plain.startswith(
        " " * 12
    )  # left ran out
    assert len(rows) == 3
    first = rows[0]
    assert roles_at(first, "界") == {"body"}
    assert roles_at(first, "xx") == {
        "state_running"
    }  # the right text only, not the padding
    pad_start = first.plain.index("xx") - 1
    assert (
        roles_at_index(first, pad_start) == set()
    )  # the gap and padding carry no role
    assert pol.width == 160


def roles_at_index(line, index):
    return {s.role for s in line.spans if s.start <= index < s.end}


@pytest.mark.parametrize("inner", (74, 62, 110))
def test_every_one_line_field_starts_its_value_at_the_same_cell(inner):
    pol = policy_for(160)
    rows = [
        ("session", "w-002", "body"),
        ("state", "idle", "body"),
        ("worktree", "unknown", "muted"),
    ]
    width = _label_width(rows)
    out = [
        _field_lines(label, value, inner, width, pol, role)[0]
        for label, value, role in rows
    ]
    offsets = {ln.plain.index(value) for ln, (_, value, _) in zip(out, rows)}
    assert offsets == {width}
    assert all(cell_len(ln.plain) <= inner for ln in out)
    assert roles_at(out[2], "unknown") == {"muted"} and roles_at(
        out[2], "worktree"
    ) == {"muted"}


def test_a_value_too_wide_for_its_label_moves_to_the_next_line_indented_two_cells():
    pol = policy_for(160)
    value = "wt-" + "0123456789" * 8  # 83 cells
    lines = _field_lines("worktree", value, 62, 9, pol)
    assert lines[0].plain == "worktree" and all(
        ln.plain.startswith("  ") for ln in lines[1:]
    )
    assert (
        "".join(ln.plain[2:] for ln in lines[1:]) == value
    )  # hard-split, nothing lost
    assert all(cell_len(ln.plain) <= 62 for ln in lines)
    short = _field_lines("worktree", "wt-1", 62, 9, pol)
    assert len(short) == 1 and short[0].plain == "worktree wt-1"


def test_split_columns_and_panes_flat_read_two_panes_of_one_row():
    row = " ┃ left text    ┃  ┃ right text ┃"
    a, b = split_columns(row, 17, 2)
    assert unframe(a) == "left text" and unframe(b) == "right text"
    assert panes_flat([row], 17, 2) == "left text right text"


# -- Task 19: the 3-row block-digit font ------------------------------------------------------------------------

from superclaude.cli.observe.render import _BIG, _figure_rows  # noqa: E402


def test_every_digit_and_plus_is_three_rows_of_three_cells_and_the_glyphs_differ():
    assert set(_BIG) == set("0123456789+")
    for ch, rows in _BIG.items():
        assert len(rows) == 3 and all(
            len(r) == 3 and set(r) <= {"#", " "} for r in rows
        ), ch
    grids = [tuple(rows) for rows in _BIG.values()]
    assert len(set(grids)) == len(grids)  # pairwise distinguishable


@pytest.mark.parametrize("ascii_mode", [False, True])
def test_a_figure_draws_in_three_rows_of_block_glyphs_and_a_word_does_not(ascii_mode):
    pol = policy_for(160, ascii=ascii_mode)
    rows = _figure_rows("100+", pol)
    block = "#" if ascii_mode else "█"
    assert rows is not None and len(rows) == 3
    assert all(set(r) <= {block, " "} for r in rows)
    assert len({cell_len(r) for r in rows}) == 1  # equal width: 3 per char and 3 gaps
    assert cell_len(rows[0]) == 4 * 3 + 3
    assert _figure_rows("unknown", pol) is None and _figure_rows("", pol) is None
    assert _figure_rows("12a", pol) is None  # any other character: not drawn


# -- Task 20: the count strip, the RETAIN CONTEXT pane and the degrade rule ------------------------------------

from superclaude.cli.observe.view import RETAIN_TITLE  # noqa: E402

RUN_LINE = f"one Run only: {QRUN}"
CAVEAT = "no read marker in source: answered questions stay listed"


def stack(fake_clock, width, height, selected=None, ascii_mode=False, count=3):
    rows = r3_rows([(f"w-00{i}", f"q{i}?") for i in range(1, count + 1)])
    return r3_screen(
        fake_clock, rows, selected, width, height=height, ascii=ascii_mode, raw=True
    )[0]


def layout_of(lines):
    text = "\n".join(lines)
    if RETAIN_TITLE in text:
        return "A"
    return "B" if "SEEN, NOT RESOLVED" in text else "C"


@pytest.mark.parametrize("width", (160, 116))
def test_the_strip_the_list_and_the_retain_pane_stack_in_that_order(fake_clock, width):
    lines = stack(fake_clock, width, 70)
    tops = {
        name: next(i for i, ln in enumerate(lines) if name in ln)
        for name in ("SEEN, NOT RESOLVED", "COORDINATOR QUESTIONS", RETAIN_TITLE)
    }
    assert (
        tops["SEEN, NOT RESOLVED"] < tops["COORDINATOR QUESTIONS"] < tops[RETAIN_TITLE]
    )
    for name, i in tops.items():
        assert cell_len(lines[i]) == width - MARGIN, name  # each pane is width - 2 wide
    plain = flat_of(unframed(lines))
    assert plain.count(RUN_LINE) == 1 and plain.count(CAVEAT) == 1
    assert plain.count("retention reset at") == 1


def test_the_count_line_stands_whole_on_the_strip_middle_row_beside_the_figure(
    fake_clock,
):
    lines = stack(fake_clock, 160, 70, count=3)
    rows = pane_body(lines, "SEEN, NOT RESOLVED")
    assert len(rows) == 3  # the figure is the tallest text: three rows
    assert rows[1].endswith(
        "seen, not resolved: 3 | closed by evidence: unavailable (no source)"
    )
    assert rows[0].strip() and set(rows[0].strip()) <= {"█"}  # the figure: blocks
    assert rows[2].strip() and set(rows[2].strip()) <= {"█"}
    assert rows[1].startswith(
        " ██  seen"
    )  # the middle row of the digit 3, then two cells


@pytest.mark.parametrize("ascii_mode", [False, True])
def test_the_strip_has_a_cyan_border_and_the_figure_is_amber_in_unicode_and_hash_in_ascii(
    fake_clock, ascii_mode
):
    rows = r3_rows([("w-001", "q1?"), ("w-002", "q2?")])
    _, view = r3_screen(fake_clock, rows, None, 160, height=70, ascii=ascii_mode)
    lines = _compose(view, policy_for(160, height=70, ascii=ascii_mode))
    top = first_line(lines, "SEEN, NOT RESOLVED")
    corner = "+" if ascii_mode else "╭"
    assert roles_at(top, corner) == {"border_count"}
    assert roles_at(top, "SEEN") == {"title"}
    middle = first_line(lines, "seen, not resolved: 2")
    block = "#" if ascii_mode else "█"
    assert roles_at(middle, block) == {"attention"}
    assert roles_at(middle, "seen, not resolved") == {"identity"}
    if ascii_mode:
        assert "\n".join(ln.plain for ln in lines).isascii()


def test_a_word_figure_and_a_narrow_strip_use_the_one_row_form(fake_clock):
    # a figure that is not digits is one bold figure and the count line on the same row
    result = question_result(ok_message([]), fake_clock)[1]
    view = build_view(result, Session(), fake_clock)
    lines = screen_lines(view, policy_for(160, height=70))
    flat = flat_of(lines)
    assert "seen, not resolved: 0" in flat


def test_no_strip_and_no_retain_pane_at_80_columns(fake_clock):
    lines = stack(fake_clock, 80, 70)
    text = "\n".join(lines)
    assert "SEEN, NOT RESOLVED" not in text and RETAIN_TITLE not in text
    flat = flat_of(unframed(lines))
    # the 80 column list line uses the two 10-character short forms (owner ruling 2026-11-18);
    # each short form is 10 characters or less and plain ASCII
    assert "seen !done: 3 | proof-done: unavailable (no source)" in flat
    from superclaude.cli.observe.view import QUESTIONS_COUNT_SHORT

    assert len(QUESTIONS_COUNT_SHORT) <= 10 and QUESTIONS_COUNT_SHORT.isascii()
    assert len("proof-done") <= 10 and "seen, not resolved" not in flat


@pytest.mark.parametrize("width", (160, 116))
def test_the_panes_drop_in_order_retain_first_then_the_strip_and_no_fact_is_lost(
    fake_clock, width
):
    seen = []
    for height in range(12, 61):
        lines = stack(fake_clock, width, height)
        if "COORDINATOR QUESTIONS" not in "\n".join(lines):
            continue  # too short for the panel: its one-line summary stands in
        layout = layout_of(lines)
        if not seen or seen[-1] != layout:
            seen.append(layout)
        plain = flat_of(unframed(lines))
        # every fact exactly once, whether the pane is drawn or dropped
        assert plain.count(RUN_LINE) == 1, (height, layout)
        assert plain.count(CAVEAT) == 1, (height, layout)
        assert plain.count("retention reset at") == 1, (height, layout)
        assert plain.count("seen, not resolved") == 1, (height, layout)
        assert len(lines) <= height and all(cell_len(ln) <= width for ln in lines)
    assert seen == [
        "C",
        "B",
        "A",
    ]  # RETAIN drops first, then the strip, as height shrinks


@pytest.mark.parametrize("width", (160, 116))
@pytest.mark.parametrize("height", (24, 26))
@pytest.mark.parametrize("selected", (None, 1))
def test_heights_24_and_26_keep_every_required_line_once(
    fake_clock, width, height, selected
):
    lines = stack(fake_clock, width, height, selected=selected, count=8)
    plain = flat_of(unframed(lines))
    assert plain.count(RUN_LINE) == 1 and plain.count(CAVEAT) == 1
    assert plain.count("retention reset at") == 1
    assert len(lines) <= height and all(cell_len(ln) <= width for ln in lines)


def test_the_measured_trigger_heights_at_160_and_116_with_no_desk(fake_clock):
    # Measured (3 questions, no desk): the RETAIN pane appears from 27 rows at 160 columns and
    # from 28 at 116; the strip from 24 and 25. Below those the list stands alone.
    expected = {160: (24, 27), 116: (25, 28)}
    for width, (strip_from, retain_from) in expected.items():
        for height in (strip_from - 1, strip_from, retain_from - 1, retain_from):
            layout = layout_of(stack(fake_clock, width, height))
            want = (
                "A" if height >= retain_from else "B" if height >= strip_from else "C"
            )
            assert layout == want, (width, height)


# -- Task 17: the frame helper and the framed questions-on screens ---------------------------------------------

from superclaude.cli.observe.render import FRAME_ROWS, MARGIN, _frame  # noqa: E402

FRAME_STARTS = ("╭", "┏", "+")


def frame_lines(lines):
    """The lines that belong to a pane: they start with the margin and then a border glyph."""
    return [ln for ln in lines if ln[:1] == " " and ln[1:2] in "╭╮╰╯│┏┓┗┛┃+|"]


def test_the_frame_is_exactly_its_width_with_a_clipped_title_and_the_right_roles():
    pol = policy_for(80)
    body = [seg("a"), seg("x" * 300), seg("界" * 3)]
    for weight, tl, bl, border in (
        ("round", "╭", "╰", "border_secondary"),
        ("heavy", "┏", "┗", "border_attention"),
    ):
        lines = _frame("T" * 200, body, 40, pol, weight=weight)
        assert len(lines) == len(body) + FRAME_ROWS
        assert all(cell_len(ln.plain) == 40 for ln in lines)
        assert lines[0].plain.startswith(tl) and lines[-1].plain.startswith(bl)
        assert roles_at(lines[0], tl) == {border}
        assert roles_at(lines[0], "T") != {border}  # the title has its own role
        assert lines[0].plain.count("T") <= 40 - 4 - 2  # cut to inner - 2


@pytest.mark.parametrize("ascii_mode", [False, True])
@pytest.mark.parametrize("width", WIDTHS)
def test_questions_on_panes_are_framed_to_the_pane_width_and_ascii_has_no_question_mark(
    fake_clock, width, ascii_mode
):
    rows = r3_rows([("w-001", "first?"), ("w-002", CENSUS_ASK)])
    lines, _ = r3_screen(
        fake_clock, rows, 1, width, height=70, ascii=ascii_mode, raw=True
    )
    lines = split_panes(lines, width)  # the two-column desk rows read pane by pane
    framed = frame_lines(lines)
    # a full-width pane, or one of the desk panes (the margin is part of each line)
    allowed = {width - MARGIN, *(w + MARGIN for w in _desk_widths(policy_for(width)))}
    assert framed and all(cell_len(ln) in allowed for ln in framed)
    if ascii_mode:
        assert "\n".join(lines).isascii() and "?" not in "".join(framed[:1])
        assert any(ln.startswith(" +-") and ln.endswith("+") for ln in lines)
        assert any(ln.startswith(" | ") and ln.endswith(" |") for ln in lines)
        assert not any("╭" in ln or "┏" in ln for ln in lines)
    else:
        list_top = next(ln for ln in lines if "COORDINATOR QUESTIONS" in ln)
        desk_top = next(ln for ln in lines if "DECISION DESK" in ln)
        assert list_top.startswith(" ╭") and desk_top.startswith(
            " ┏"
        )  # round list, heavy desk


@pytest.mark.parametrize("width", WIDTHS)
def test_the_text_inside_a_pane_is_at_most_width_minus_six_cells(fake_clock, width):
    """Single column: inner width is width - 6 (154 at 160, 110 at 116, 74 at 80)."""
    rows = r3_rows([("w-001", "x" * 300), ("w-002", PLAN_ASK)])
    lines, _ = r3_screen(fake_clock, rows, 1, width, height=70, raw=True)
    bodies = [unframe(ln) for ln in frame_lines(split_panes(lines, width))]
    assert bodies and all(cell_len(b) <= width - 6 for b in bodies)
    widest_desk_pane = max(_desk_widths(policy_for(width)))
    assert (
        max(cell_len(b) for b in bodies) >= widest_desk_pane - 4 - 40
    )  # long text uses the width of its pane
    assert width - 6 == {160: 154, 116: 110, 80: 74}[width]


@pytest.mark.parametrize("width", WIDTHS)
def test_the_list_pane_is_heavy_when_no_desk_is_shown(fake_clock, width):
    rows = r3_rows([("w-001", "first?")])
    lines, _ = r3_screen(fake_clock, rows, None, width, height=70, raw=True)
    list_top = next(ln for ln in lines if "COORDINATOR QUESTIONS" in ln)
    assert list_top.startswith(" ┏")  # the one attention pane when no desk is shown
    assert not any("DECISION DESK" in ln for ln in lines)


@pytest.mark.parametrize("ascii_mode", [False, True])
@pytest.mark.parametrize("selected", [None, 1])
@pytest.mark.parametrize("height", [12, 24, 40, 44])
@pytest.mark.parametrize("width", WIDTHS)
def test_framed_screens_never_exceed_the_height(
    fake_clock, width, height, selected, ascii_mode
):
    rows = r3_rows([("w-001", "first?"), ("w-002", CENSUS_ASK), ("w-003", "third?")])
    lines, _ = r3_screen(
        fake_clock, rows, selected, width, height=height, ascii=ascii_mode, raw=True
    )
    assert len(lines) <= height
    assert all(cell_len(ln) <= width for ln in lines)
    assert any("shown " in ln for ln in lines[-2:])  # the footer is the last row


def test_the_hidden_desk_notice_sits_inside_the_list_frame(fake_clock):
    from superclaude.cli.observe.view import DESK_HIDDEN

    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    seen_inside = False
    for height in range(16, 40):
        lines, _ = r3_screen(fake_clock, rows, 1, 116, height=height, raw=True)
        for ln in lines:
            if DESK_HIDDEN in ln and ln.startswith(" ┃ "):
                assert ln.endswith(" ┃")  # a heavy list frame row
                seen_inside = True
    assert (
        seen_inside
    )  # the notice is reached at some height and sits in the frame body


# -- Task 24: the two-column Decision Desk ---------------------------------------------------------------------

from tests.observe.conftest import title_of  # noqa: E402


@pytest.mark.parametrize(
    ("width", "left_title", "right_title", "left_w", "right_w"),
    [
        (160, DESK_TITLE, DESK_EVIDENCE_TITLE, 76, 80),
        (116, DESK_EVIDENCE_TITLE, "COORDINATOR QUESTIONS", 66, 46),
    ],
)
def test_the_desk_is_two_columns_at_160_and_116(
    fake_clock, width, left_title, right_title, left_w, right_w
):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    lines, _ = r3_screen(fake_clock, rows, 1, width, height=70, raw=True)
    top = next(ln for ln in lines if left_title in ln and right_title in ln)
    left, right = split_columns(top, 1 + left_w)
    assert left_title in left and right_title in right
    assert cell_len(left) == 1 + left_w  # the margin and the left pane
    assert cell_len(right.rstrip()) == 1 + right_w  # the margin and the right pane
    assert 1 + left_w + 2 + right_w + 1 == width  # margin, panes, gap, margin


def test_the_desk_panes_are_stacked_at_80_columns(fake_clock):
    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
    lines, _ = r3_screen(fake_clock, rows, 1, 80, height=70, raw=True)
    titles = title_of(lines)
    order = [
        next(i for i, t in enumerate(titles) if t.startswith(name))
        for name in (DESK_TITLE, DESK_EVIDENCE_TITLE, "COORDINATOR QUESTIONS")
    ]
    assert order == sorted(order)
    assert all(cell_len(ln) == 79 for ln in frame_lines(lines))  # 78 and the margin


def test_the_evidence_values_start_at_one_cell(fake_clock):
    desk = desk_after(fake_clock, lambda row: None)[1:]
    fields = [ln for ln in desk if ln.split(" ")[0] in {"session", "state", "alive"}]
    assert len(fields) == 3
    assert all(ln[8] == " " and ln[9] != " " for ln in fields)  # one value column


def test_a_64_character_worktree_id_is_hard_split_in_the_116_evidence_pane(fake_clock):
    worktree = "wt-" + "0123456789abcdef" * 3 + "0123456789abc"
    assert len(worktree) == 64

    def mutate(row):
        row["resource"] = {"worktreeId": worktree}

    desk = desk_after(fake_clock, mutate)
    assert all(cell_len(ln) <= 62 for ln in desk)  # evidence inner width at 116
    start = next(i for i, ln in enumerate(desk) if ln.startswith("worktree"))
    assert desk[start] == "worktree"  # too wide beside the label
    tail = [ln for ln in desk[start + 1 :] if ln.startswith("  ")]
    assert len(tail) >= 2  # hard-split, not cut
    assert "".join(ln[2:] for ln in tail).replace(" ", "") == (
        worktree + "(this session only)"
    ).replace(" ", "")


def test_the_plan_ask_is_one_short_row_in_the_46_cell_list_pane_and_whole_in_the_desk(
    fake_clock,
):
    rows = r3_rows([("w-001", "first?"), ("w-002", PLAN_ASK)])
    lines, _ = r3_screen(fake_clock, rows, 1, 116, height=70, raw=True)
    split = split_panes(lines, 116)
    listing = pane_body(split, "COORDINATOR QUESTIONS")
    assert listing and all(cell_len(ln) <= 42 for ln in listing)  # 46 less the frame
    selected = [ln for ln in listing if ln.startswith("▸ ")]
    assert len(selected) == 1 and selected[0].endswith(">")
    ask = "".join(desk_text_lines(unframed(split))).replace(" ", "")
    assert ask == PLAN_ASK.replace(HASH, "").replace(" ", "")  # nothing lost, no hash


# -- Task 26: the framed ledger screen and its small-height fallback --------------------------------------------

LEDGER_VARIANTS = (
    "base",
    "empty",
    "source-loss",
    "injection",
    "missing-fields",
    "long-identifiers",
)


@pytest.mark.parametrize("height", [24, 40, 44])
@pytest.mark.parametrize("variant", LEDGER_VARIANTS)
@pytest.mark.parametrize("width", WIDTHS)
def test_the_framed_ledger_screen_never_exceeds_the_height(
    fake_clock, width, variant, height
):
    view = fixture_view(variant, fake_clock)
    lines = framed_screen_lines(view, policy_for(width, height=height))
    titles = title_of(lines)
    assert "OBSERVATION WINDOW" in titles and "COORDINATOR QUESTIONS" in titles
    assert len(lines) <= height and all(cell_len(ln) <= width for ln in lines)
    assert any("shown " in ln for ln in lines[-2:])  # the footer stays last


@pytest.mark.parametrize("height", [12, 8])
@pytest.mark.parametrize("variant", LEDGER_VARIANTS)
@pytest.mark.parametrize("width", WIDTHS)
def test_a_short_terminal_keeps_the_plain_head_for_the_ledger(
    fake_clock, width, variant, height
):
    view = fixture_view(variant, fake_clock)
    lines = framed_screen_lines(view, policy_for(width, height=height))
    assert title_of(lines) == []  # no framed pane at all
    assert not any(ln and ln[0] in "╭┏╰┗│┃" for ln in lines)


def test_the_framed_ledger_is_drawn_from_the_height_where_three_rows_fit(fake_clock):
    """Measured on the six fixtures: the first framed height is 15 to 20 at 160, 116 and 80."""
    for variant in LEDGER_VARIANTS:
        view = fixture_view(variant, fake_clock)
        for width in WIDTHS:
            first = next(
                h
                for h in range(8, 61)
                if "OBSERVATION WINDOW"
                in title_of(framed_screen_lines(view, policy_for(width, height=h)))
            )
            assert 15 <= first <= 20, (variant, width, first)


def test_the_ledger_panes_are_built_from_the_allowed_fields_only():
    import inspect

    source = inspect.getsource(render_module._framed_ledger)
    used = set(re.findall(r"view\.(\w+)", source)) | set(
        re.findall(r"panel\.(\w+)", source)
    )
    assert used <= {
        "gap_notice",
        "historical_note",
        "questions",
        "replaces_gap",
        "summary",
        "screen_header2",
        "header2",
        "screen_counts_tokens",
        "counts_tokens",
        "changes_line",
        "ledger_title",
        "visible_rows",
        "all_rows",
        "ledger_empty",
        "window",
    }, used
    for invented in ("owner", "requester", "mapped", "SIGNALS", "affected"):
        assert invented not in source
        assert invented not in render_module.OBSERVATION_TITLE
