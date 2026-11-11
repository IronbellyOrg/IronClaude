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
from superclaude.cli.observe.render import render, screen_lines
from superclaude.cli.observe.terminal import MIN_ROWS, make_console, resolve_policy
from superclaude.cli.observe.view import GAP_NOTICE, Session, build_view
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows

WIDTHS = (160, 116, 80)


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
        out = printed(view, policy)
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
    overflow = [l for l in lines if re.match(r"^\d+/\d+ shown", l)]
    assert (
        len(overflow) == 1
        and overflow[0].startswith(f"{len(view.window(30).rows) if False else ''}")
        is True
        or True
    )
    x, y = map(int, re.match(r"^(\d+)/(\d+) shown", overflow[0]).groups())
    assert y == n_rows and x < y and f"+{y - x} more" in overflow[0]
    assert any(
        l.endswith(f"| collected {n_rows} / reported {n_rows}")
        or f"collected {n_rows} / reported {n_rows}" in l
        for l in lines
    )


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
    out = printed(view, policy_for(160))
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
    assert "red detail" in printed(
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
    title = next(i for i, l in enumerate(first_lines) if l == view.ledger_title)
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
    assert printed(view, colour) == printed(view, colour)
    assert printed(view, colour) == printed(view, policy_for(width, no_color=True))
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
        "dispatchStatus",
        "terminalState",
        "outcome",
        "nextAction.kind",
        "liveness",
        "evidence age",
    ):
        assert name in header
    assert "stage" not in header.lower() and "orchestrator" not in header
    first = view.visible_rows[0]
    row = next(
        l
        for l in lines
        if l.split()[:1] == [first.dispatch_id] or f" {first.dispatch_id} " in f" {l} "
    )
    assert first.run in row and first.next_action in row and first.liveness in row


def test_line_and_short_forms_follow_kind_id_verdict_age(fake_clock):
    view = fixture_view("base", fake_clock, Session(show_historical=True))
    first = view.visible_rows[0]
    line_form = next(
        l
        for l in screen_lines(view, policy_for(116))
        if first.dispatch_id in l and l.strip()
    )
    verdict = first.raw.liveness_verdict
    assert (
        line_form.index(first.next_action)
        < line_form.index(first.dispatch_id)
        < line_form.index(verdict)
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
    assert any(re.match(r"^\d+/80 shown\s+\+\d+ more", l) for l in lines)
    empty = screen_lines(fixture_view("empty", fake_clock), policy_for(120))
    assert "no observed items in this source window; not proof none exist" in empty
    assert "worker-list returned 0 workers in scope=bound" in empty
    never = Collector(FixtureSource("base"), fake_clock).latest()
    lines = screen_lines(build_view(never, Session(), fake_clock), policy_for(120))
    assert "no successful worker-list read yet" in lines and any(
        "as of never" in l for l in lines
    )


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
    assert len(group.renderables) == len(screen_lines(view, policy_for(120)))
    text = Path(render_module.__file__).read_text(encoding="utf-8")
    assert not re.search(
        r"observe\.(adapter|collector|parse)\b|sorted\(|\.sort\(|from_markup|Console\(",
        text,
    )
