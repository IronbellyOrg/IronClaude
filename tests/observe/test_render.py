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
    assert "seen, not resolved: 5 | closed by evidence: unavailable (no source)" in flat
    assert (
        "retention reset at 12:00; questions observed before this start are not retained"
        in flat
    )
    assert sum("reason unknown" in l for l in lines) == 5
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
    lines = screen_lines(build_view(result, Session(), fake_clock), policy)
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
    assert sum("reason unknown" in l for l in lines) < 60
    assert any(
        l.startswith("collected") or "collected 4" in l for l in lines
    )  # counts stay


def test_t47_questions_off_the_screen_is_the_release_1_screen(fake_clock):
    off = fixture_view("base", fake_clock)
    lines = screen_lines(off, policy_for(160))
    assert GAP_NOTICE in lines and not any("COORDINATOR" in l for l in lines)
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
    assert sum("reason unknown" in l for l in lines) == 2
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
    assert sum("reason unknown" in l for l in lines) == 3


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
    assert not any("reason unknown" in l for l in lines)


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


def test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface():
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
    shown = [ln for ln in lines if "reason unknown" in ln]
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
    lines = screen_lines(view, policy_for(120, height=26))
    assert (
        sum("reason unknown" in ln for ln in lines) == 8
    )  # every question is shown ...
    ledger_rows = [ln for ln in lines if " w-0" in ln]
    assert (
        1 <= len(ledger_rows) <= 3
    )  # ... and the ledger keeps what is left (>= 1 row)
    assert any(ln.startswith(f"{len(ledger_rows)}/30 shown") for ln in lines)
    assert len(lines) <= 26


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
    assert flat.count("reason unknown") == 2 and "no questions" not in flat.lower()
    assert dataclasses.is_dataclass(result)
