"""Fixture variants, the fixture loader and the shared test support (AD-16; harness of acceptance-tests.md)."""

from __future__ import annotations

import re
import subprocess
import sys
from importlib import resources
from pathlib import Path

import pytest

from superclaude.cli.observe.parse import (
    FIXTURE_PACKAGE,
    VARIANTS,
    load_fixture,
    parse_page,
)
from tests.observe.conftest import FakeClock, argv_allowed

ROOT = Path(__file__).resolve().parents[2]


def fixture_files():
    return [
        p
        for p in resources.files(FIXTURE_PACKAGE).iterdir()
        if p.name.endswith(".json")
    ]


# -- loading ---------------------------------------------------------------------------------


@pytest.mark.parametrize("variant", VARIANTS)
def test_every_variant_loads_and_every_cycle_parses(variant):
    fixture = load_fixture(variant)
    assert fixture.variant == variant and fixture.cycles
    for index, cycle in enumerate(fixture.cycles):
        if cycle.fail is not None:
            assert cycle.envelope is None and cycle.fail
            continue
        page = fixture.parse(index, f"fixture:{variant}", index + 1)
        assert page.raw_count == len(cycle.envelope["result"]["workers"])


def test_importlib_resources_lists_all_ten_variants():
    names = {
        p.name for p in resources.files("superclaude.cli.observe.fixtures").iterdir()
    }
    assert {f"{v}.json" for v in VARIANTS} <= names
    assert len(VARIANTS) == 10


@pytest.mark.parametrize("bad", ["../base", "nope", "Base", "", "base.json", "a/b"])
def test_unknown_or_unsafe_variant_names_are_refused(bad):
    with pytest.raises(ValueError):
        load_fixture(bad)


def test_replay_repeats_the_last_cycle():
    fixture = load_fixture("source-loss")
    assert [c.fail for c in fixture.cycles] == [
        None,
        None,
        "timeout",
        "timeout",
        "exit:2",
    ]
    assert fixture.cycle(99).fail == "exit:2"


# -- variant contents ------------------------------------------------------------------------


def workers(variant, index=0):
    return load_fixture(variant).cycle(index).envelope["result"]["workers"]


def test_base_has_80_rows_and_8_runs_and_cycle_two_changes_one_next_action():
    rows = workers("base")
    assert len(rows) == 80 and len({r["runId"] for r in rows}) == 8
    changed = [
        (
            a["dispatchId"],
            a["projection"]["nextAction"]["kind"],
            b["projection"]["nextAction"]["kind"],
        )
        for a, b in zip(workers("base", 0), workers("base", 1), strict=True)
        if a != b
    ]
    assert changed == [("w-005", "none", "approve")]


def test_empty_has_no_rows_and_total_zero():
    assert workers("empty") == []
    assert load_fixture("empty").cycle(0).envelope["result"]["page"]["total"] == 0


def test_uneven_shared_historical_and_missing_variants_have_their_shapes():
    rows = workers("uneven")
    assert sum(1 for r in rows if r["runId"] == "run-a") == 60
    shared = workers("shared-unmapped")
    assert shared[0]["resource"]["worktreeId"] == shared[1]["resource"]["worktreeId"]
    assert "worktreeId" not in shared[2]["resource"]
    states = [r.get("terminalState", "<absent>") for r in workers("historical")]
    assert {"released", "retained", "<absent>", "orphaned", "active"} <= set(states)
    missing = load_fixture("missing-fields").cycle(0).envelope["result"]
    assert "scope" not in missing and "total" not in missing["page"]
    assert any("dispatchId" not in r for r in missing["workers"])
    assert any(r.get("taskId") is None and "taskId" in r for r in missing["workers"])


def test_long_identifiers_are_over_sixty_characters_with_cjk_and_emoji():
    ids = [r["dispatchId"] for r in workers("long-identifiers")]
    assert all(len(i) >= 60 for i in ids)
    assert any(
        any(0x3040 <= ord(ch) <= 0x30FF or 0x4E00 <= ord(ch) <= 0x9FFF for ch in i)
        for i in ids
    )
    assert any(any(ord(ch) > 0x1F000 for ch in i) for i in ids)


def test_duplicate_variant_has_duplicates_untimed_rows_and_a_backward_timestamp():
    first = workers("duplicate-out-of-order", 0)
    ids = [r["dispatchId"] for r in first]
    assert len(ids) != len(set(ids))
    assert "observedAt" not in first[3]["projection"]["liveness"]
    old = workers("duplicate-out-of-order", 1)[0]["projection"]["liveness"][
        "observedAt"
    ]
    assert old < first[0]["projection"]["liveness"]["observedAt"]


# -- frozen marker (T34) ---------------------------------------------------------------------


def test_a_frozen_fixture_row_comes_out_of_the_loader_with_fixture_frozen_true():
    fixture = load_fixture("base")
    page = fixture.parse(0, "fixture:base", 1)
    frozen = [r.dispatch_id for r in page.rows if r.fixture_frozen]
    assert frozen == ["w-003"]
    assert "fixtureOnly" not in fixture.cycle(0).envelope["result"]["workers"][2]
    assert page.rows[2].unrecognised_keys == 0
    # source-rank offsets are honoured
    assert [
        r.dispatch_id
        for r in fixture.parse(0, "fixture:base", 1, 100).rows
        if r.fixture_frozen
    ] == ["w-003"]


def test_the_same_json_fed_straight_to_parse_page_leaves_it_false():
    raw = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath("base.json")
        .read_text(encoding="utf-8")
    )
    import json

    envelope = json.loads(raw)["cycles"][0]
    page = parse_page(envelope, "fixture:base", 1)
    assert not any(r.fixture_frozen for r in page.rows)
    assert (
        page.rows[2].unrecognised_keys == 1
    )  # fixtureOnly is just an unknown key here


# -- nothing sensitive in committed fixtures -------------------------------------------------

SENSITIVE = {
    "absolute path": re.compile(
        r"(?<![\w.:/-])/(?:home|Users|tmp|var|etc|usr|opt|root|mnt|srv)/|\b[A-Za-z]:\\\\"
    ),
    "terminal handle": re.compile(r"term_"),
    "token": re.compile(
        r"sk-[A-Za-z0-9]{16,}|gh[pousr]_[A-Za-z0-9]{16,}|xox[abprs]-|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{10,}"
        r"|[A-Fa-f0-9]{32,}|Bearer\s+\S+|(?i:secret|password|api[_-]?key)\"?\s*[:=]"
    ),
    "credential url": re.compile(r"://[^/\s\"]*:[^/\s\"]*@"),
}


@pytest.mark.parametrize("path", fixture_files(), ids=lambda p: p.name)
def test_committed_fixtures_hold_no_path_handle_token_or_escape_byte(path):
    text = path.read_text(encoding="utf-8")
    assert "\x1b" not in text
    assert not any(ord(ch) < 0x20 and ch not in "\n" for ch in text)
    for what, pattern in SENSITIVE.items():
        assert not pattern.search(text), f"{path.name}: {what}"


def test_the_injection_variant_stores_escapes_as_json_escape_sequences_only():
    text = (
        resources.files(FIXTURE_PACKAGE)
        .joinpath("injection.json")
        .read_text(encoding="utf-8")
    )
    assert "\\u001b[31m" in text and "\\u001b]8;;" in text and "\\u009b" in text
    assert "\\u202e" in text and "\\u0007" in text and "[bold]x[/bold]" in text
    assert text.isascii()


# -- shared test support ---------------------------------------------------------------------


def test_subprocess_calls_fail_with_the_guard_message():
    with pytest.raises(AssertionError, match="subprocess is blocked in tests/observe"):
        subprocess.run([sys.executable, "-c", "pass"], check=False)
    with pytest.raises(AssertionError, match="observe_real_process"):
        subprocess.Popen([sys.executable, "-c", "pass"])


@pytest.mark.observe_real_process
def test_the_marker_lifts_the_subprocess_guard():
    done = subprocess.run(
        [sys.executable, "-I", "-c", "print('ok')"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert done.stdout.strip() == "ok"


def test_pyproject_keeps_strict_markers_and_registers_the_marker():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '"--strict-markers"' in text
    assert '"observe_real_process:' in text


def test_fake_runner_and_discover_share_one_log_and_refuse_other_argv(
    fake_runner, fake_discover, argv_log
):
    orca = fake_discover()
    template = [orca, "orchestration", "worker-list", "--json", "--limit", "100"]
    fake_runner(template, 10.0)
    fake_runner([*template, "--run", "run-a", "--cursor", "abc"], 10.0)
    assert argv_log == [
        [orca, "skills", "list", "--json"],
        template,
        [*template, "--run", "run-a", "--cursor", "abc"],
    ]
    for bad in (
        [orca, "check"],
        [orca, "orchestration", "check", "--json"],
        [*template, "--ack"],
        [*template, "--run", "--evil"],
        [*template, "--cursor", "-x"],
        [orca],
        [],
    ):
        assert not argv_allowed(bad)
        with pytest.raises(AssertionError, match="allow-list"):
            fake_runner(bad, 1.0)


def test_fake_runner_responses_repeat_the_last_and_can_raise(argv_log):
    from tests.observe.conftest import FakeRunner

    runner = FakeRunner(
        argv_log, [(0, "a"), TimeoutError("slow"), lambda argv, t: (2, "b")]
    )
    argv = ["orca", "orchestration", "worker-list", "--json", "--limit", "100"]
    assert runner(argv, 1.0) == (0, "a")
    with pytest.raises(TimeoutError):
        runner(argv, 1.0)
    assert runner(argv, 1.0) == (2, "b") and runner(argv, 1.0) == (2, "b")


def test_fake_clock_advances_both_clocks_and_wall_jumps_leave_monotonic_alone():
    clock = FakeClock()
    mono, wall = clock.monotonic(), clock.wall()
    clock.advance(5)
    assert (clock.monotonic() - mono, clock.wall() - wall) == (5, 5)
    clock.jump_wall(-3600)
    assert clock.monotonic() - mono == 5 and clock.wall() - wall == 5 - 3600


def test_make_rows_spreads_rows_over_distinct_runs(make_rows):
    rows = make_rows(50, 5)
    assert len(rows) == 50 and len({r["runId"] for r in rows}) == 5
    assert len({r["dispatchId"] for r in rows}) == 50
    for n_rows, n_runs in ((50, 10), (100, 8), (80, 5)):
        generated = make_rows(n_rows, n_runs)
        assert (
            len(generated) == n_rows and len({r["runId"] for r in generated}) == n_runs
        )


def test_console_factory_builds_a_recording_console_through_make_console(
    console_factory,
):
    console, policy = console_factory(width=116, height=30, ascii=True, no_color=True)
    console.print("hello")
    assert console.width == 116 and policy.ascii and policy.no_color
    assert console.export_text().strip() == "hello"
