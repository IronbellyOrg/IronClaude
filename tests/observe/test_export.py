"""Text record, atomic writer and state directory tests (AD-11; T27, T29 export half, T48)."""

from __future__ import annotations

import json
import os
import re
import stat
import unicodedata
from pathlib import Path

import pytest

import superclaude.cli.observe.export as export_module
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector, FixtureSource
from superclaude.cli.observe.export import (
    record_path,
    record_text,
    snapshot_json,
    snapshot_path,
    state_dir,
    write_atomic,
)
from superclaude.cli.observe.render import screen_lines
from superclaude.cli.observe.terminal import resolve_policy
from superclaude.cli.observe.view import Session, build_view
from tests.observe.conftest import FakeDiscover, FakeRunner, make_envelope, make_rows


def fixture_view(variant, clock, session=None, cycles=1):
    collector = Collector(FixtureSource(variant), clock)
    for _ in range(cycles):
        result = collector.run_once()
    return build_view(result, session or Session(), clock)


def bad_chars(text):
    return [
        ch
        for ch in text
        if ch == "\x1b"
        or (ch != "\n" and unicodedata.category(ch) in ("Cc", "Cf", "Cs"))
    ]


# -- T27 -----------------------------------------------------------------------------------------------------


def test_record_has_full_identifiers_no_escape_and_no_truncation_marker(fake_clock):
    view = fixture_view("long-identifiers", fake_clock, Session(show_historical=True))
    text = record_text(view)
    assert "\x1b" not in text and ">" not in text
    for row in view.all_rows:
        assert f"dispatchId={row.dispatch_id} |" in text
        assert len(row.dispatch_id) >= 60
    lines = [line for line in text.splitlines() if line.startswith("dispatchId=")]
    assert len(lines) == 4 == len(view.all_rows)


def test_record_first_line_is_the_header_and_names_the_synthetic_fixture(fake_clock):
    text = record_text(fixture_view("base", fake_clock))
    first, second = text.splitlines()[:2]
    assert "SYNTHETIC FIXTURE base, not Orca data" in first and first.startswith(
        "ORCA OBSERVER"
    )
    assert second.startswith("worker-list OK")
    assert text.endswith("\n") and "Human questions: source UNVERIFIED" in text


def test_record_header_names_the_filter_and_toggle_but_lists_every_row(fake_clock):
    plain = record_text(fixture_view("base", fake_clock))
    session = Session(filter_text="run-a", show_historical=True)
    narrowed = record_text(fixture_view("base", fake_clock, session))
    assert "screen filter: none  historical rows on screen: hidden" in plain
    assert "screen filter: run-a  historical rows on screen: shown" in narrowed

    def rows(text):
        return [line for line in text.splitlines() if line.startswith("dispatchId=")]

    assert rows(plain) == rows(narrowed) and len(rows(plain)) == 80


def test_a_newline_inside_an_identifier_still_gives_one_line_per_row(
    fake_clock, argv_log
):
    rows = make_rows(3, 1)
    rows[1]["dispatchId"] = "w-002\nsecond line\r\nthird"
    runner = FakeRunner(argv_log, [(0, json.dumps(make_envelope(rows, total=3)))])
    result = Collector(
        LiveSource(runner, FakeDiscover(argv_log)), fake_clock
    ).run_once()
    text = record_text(build_view(result, Session(), fake_clock))
    assert (
        len([line for line in text.splitlines() if line.startswith("dispatchId=")]) == 3
    )
    assert "dispatchId=w-002 second line third" in text


def test_empty_and_not_polled_records_say_so_without_inventing_rows(fake_clock):
    empty = record_text(fixture_view("empty", fake_clock))
    assert "no observed items in this source window; not proof none exist" in empty
    assert not any(line.startswith("dispatchId=") for line in empty.splitlines())
    never = record_text(
        build_view(
            Collector(FixtureSource("base"), fake_clock).latest(), Session(), fake_clock
        )
    )
    assert "no successful worker-list read yet" in never and "as of never" in never


# -- T29 export half -----------------------------------------------------------------------------------------


def test_injection_variant_exports_contain_no_escape_c1_or_format_characters(
    fake_clock,
):
    for session in (Session(), Session(show_historical=True, filter_text="w-inj")):
        view = fixture_view("injection", fake_clock, session)
        assert bad_chars(record_text(view)) == []
        assert bad_chars(snapshot_json(view)) == []
    assert "[bold]x[/bold]" in record_text(
        fixture_view("injection", fake_clock, Session(show_historical=True))
    )


# -- T48 --------------------------------------------------------------------------------------------------------


def test_an_id_truncated_on_screen_appears_in_full_in_the_record(fake_clock):
    view = fixture_view("long-identifiers", fake_clock, Session(show_historical=True))
    policy = resolve_policy({}, "utf-8", {}, 80, 40)
    screen = "\n".join(screen_lines(view, policy))
    record = record_text(view)
    truncated = [row for row in view.all_rows if row.dispatch_id not in screen]
    assert truncated and all(">" in screen for _ in truncated)
    for row in truncated:
        assert row.dispatch_id in record


def test_two_sessions_over_one_cycle_result_give_byte_identical_snapshots(fake_clock):
    collector = Collector(FixtureSource("base"), fake_clock)
    result = collector.run_once()
    sessions = [
        Session(),
        Session(filter_text="run-b", show_historical=True),
        Session(show_historical=False, focus="inspector"),
    ]
    outputs = {snapshot_json(build_view(result, s, fake_clock)) for s in sessions}
    assert len(outputs) == 1
    assert len(json.loads(outputs.pop())["rows"]) == 80  # historical rows are in it too


# -- files ------------------------------------------------------------------------------------------------------


def test_atomic_writer_creates_a_0600_file_and_replaces_atomically(tmp_path):
    target = tmp_path / "state" / "out.json"
    write_atomic(target, "first")
    assert (
        target.read_text() == "first" and stat.S_IMODE(target.stat().st_mode) == 0o600
    )
    target.chmod(0o644)
    write_atomic(target, "second")
    assert (
        target.read_text() == "second" and stat.S_IMODE(target.stat().st_mode) == 0o600
    )
    assert [p.name for p in target.parent.iterdir()] == [
        "out.json"
    ]  # no temporary file left


def test_an_interrupted_write_leaves_the_old_file_whole_and_no_temporary_file(
    tmp_path, monkeypatch
):
    target = tmp_path / "snapshot.json"
    write_atomic(target, "old content")

    def boom(src, dst):
        raise OSError("interrupted between the temporary write and the replace")

    monkeypatch.setattr(os, "replace", boom)
    with pytest.raises(OSError):
        write_atomic(target, "new content that must never be seen half written")
    assert target.read_text() == "old content"
    assert [p.name for p in tmp_path.iterdir()] == ["snapshot.json"]
    fresh = tmp_path / "never-written.json"
    with pytest.raises(OSError):
        write_atomic(fresh, "x")
    assert not fresh.exists()


def test_state_dir_honours_xdg_state_home_and_falls_back_to_the_home_folder(tmp_path):
    assert (
        state_dir({"XDG_STATE_HOME": str(tmp_path)})
        == tmp_path / "superclaude" / "observe"
    )
    assert (
        state_dir({}, home=str(tmp_path))
        == tmp_path / ".local" / "state" / "superclaude" / "observe"
    )
    assert "relative" not in str(
        state_dir({"XDG_STATE_HOME": "relative/path"}, home=str(tmp_path))
    )
    assert state_dir({"XDG_STATE_HOME": ""}, home=str(tmp_path)).parts[-3:] == (
        "state",
        "superclaude",
        "observe",
    )


def test_record_and_snapshot_names(fake_clock, tmp_path):
    view = fixture_view("base", fake_clock)
    assert record_path(tmp_path, view) == tmp_path / "observe-2026-11-08T12-00-00Z.txt"
    assert snapshot_path(tmp_path) == tmp_path / "snapshot.json"


def test_a_failed_cycle_exports_error_with_the_short_code_and_the_last_good_rows(
    fake_clock,
):
    collector = Collector(FixtureSource("source-loss"), fake_clock)
    for _ in range(3):
        failed = collector.run_once()
    data = json.loads(snapshot_json(build_view(failed, Session(), fake_clock)))
    assert data["source"]["status"] == "ERROR" and data["source"]["error"] == "timeout"
    assert (
        len(data["rows"]) == 5
        and data["source"]["observedAt"] == "2026-11-08T12:00:00Z"
    )
    assert "worker-list FAILED (timeout)" in record_text(
        build_view(failed, Session(), fake_clock)
    )


# -- hygiene ------------------------------------------------------------------------------------------------------


def test_export_does_not_import_render_parse_or_adapter_or_use_a_console():
    text = Path(export_module.__file__).read_text(encoding="utf-8")
    assert not re.search(
        r"observe\.(render|parse|adapter|collector)\b|Console\b|from rich|import rich",
        text,
    )


# -- R2: the record export carries the same question lines as the screen ---------------------------------------------------

from superclaude.cli.observe.view import QUESTIONS_DISCLOSURE  # noqa: E402
from tests.observe.conftest import (  # noqa: E402
    QRUN,
    make_question_envelope,
    make_question_rows,
    routed_runner_responses,
)


def question_view(rows, clock, session=None):
    from superclaude.cli.observe.view import Session, build_view

    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
    message = (0, json.dumps(make_question_envelope(rows)))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    collector = Collector(
        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
    )
    return build_view(collector.run_once(), session or Session(), clock)


def test_the_record_lists_every_question_with_its_full_id_and_no_escape(fake_clock):
    long_id = "msg_" + "a" * 60
    rows = make_question_rows(3, subject="[bold]loud[/bold] \x1b[31mred\x1b[0m")
    rows[0]["id"] = long_id
    text = record_text(question_view(rows, fake_clock))
    assert "\x1b" not in text and long_id in text
    lines = text.splitlines()
    assert "COORDINATOR QUESTIONS" in lines and f"one Run only: {QRUN}" in lines
    assert QUESTIONS_DISCLOSURE in lines
    assert sum(" | " in ln and "reason unknown" in ln for ln in lines) == 3
    assert (
        "seen, not resolved: 3 | closed by evidence: unavailable (no source)" in lines
    )
    assert any(ln.startswith("retention reset at ") for ln in lines)
    assert "[bold]loud[/bold]" in text  # literal text, as on the screen
    assert not any(ord(ch) in range(0x80, 0xA0) for ch in text)


def test_the_record_with_questions_off_has_no_question_lines(fake_clock):
    text = record_text(fixture_view("base", fake_clock))
    assert "COORDINATOR" not in text and "reason unknown" not in text
    assert (
        "Human questions: source UNVERIFIED" in text
    )  # the release 1 gap notice stays


def test_the_record_keeps_the_question_lines_in_a_failed_state(fake_clock):
    from superclaude.cli.observe.view import Session, build_view

    worker = (0, json.dumps(make_envelope(make_rows(2, 1), total=2)))
    good = (0, json.dumps(make_question_envelope(make_question_rows(2))))
    fenced = (1, json.dumps({"ok": False, "error": {"code": "consumer_fenced"}}))
    runner = FakeRunner([], [routed_runner_responses(worker, [good, fenced])])
    collector = Collector(
        LiveSource(runner, FakeDiscover([])), fake_clock, run_id=QRUN, questions=True
    )
    collector.run_once()
    text = record_text(build_view(collector.run_once(), Session(), fake_clock))
    assert "FAILED (consumer-fenced)" in text
    assert "this terminal does not hold the named Run" in text
    assert text.count("reason unknown") == 2
