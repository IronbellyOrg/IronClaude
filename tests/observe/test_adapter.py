"""Adapter tests (AD-3, AD-4, AD-5; T1, T2, T4 adapter half, T36, T37 in acceptance-tests.md)."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import superclaude.cli.observe.adapter as adapter
from superclaude.cli.observe.adapter import (
    CURSOR_MAX_BYTES,
    FORBIDDEN_PREFIXES,
    ArgvRejected,
    LiveSource,
    RunnerFailure,
    assert_allowed,
    build_argv,
    production_runner,
)
from tests.observe.conftest import (
    FakeDiscover,
    FakeRunner,
    argv_allowed,
    make_envelope,
    make_rows,
)

ORCA = "/opt/fake/orca"
TEMPLATE = [ORCA, "orchestration", "worker-list", "--json", "--limit", "100"]


def reply(n=1, has_more=False, cursor=None, total=None, rows=None):
    envelope = make_envelope(
        make_rows(n, 1) if rows is None else rows, total=total, has_more=has_more
    )
    if cursor is not None:
        envelope["result"]["page"]["nextCursor"] = cursor
    return 0, json.dumps(envelope)


def source_with(responses, argv_log, **kw):
    runner = FakeRunner(argv_log, responses)
    return LiveSource(runner, FakeDiscover(argv_log, ORCA), **kw), runner


def read(source, clock, budget=15.0, run_id=None):
    return source.read_pages(clock, clock.monotonic() + budget, run_id)


# -- T1: only the two templates, ever ----------------------------------------------------------


def test_every_argv_across_all_adapter_paths_is_a_template(argv_log, fake_clock):
    scenarios = [
        [reply(3)],  # one page
        [
            reply(2, True, "c1", 5),
            reply(2, True, "c2", 5),
            reply(1, False, None, 5),
        ],  # three pages
        [(2, "")],  # exit failure
        [TimeoutError("slow")],
        [reply(1, True, None)],  # cursor missing
    ]
    for responses in scenarios:
        source, _ = source_with(responses, argv_log)
        read(source, fake_clock)
        read(source, fake_clock, run_id="run-a")
    assert argv_log
    for argv in argv_log:
        assert argv_allowed(argv)
        assert argv == [ORCA, "skills", "list", "--json"] or argv[:6] == TEMPLATE
    assert sum(1 for a in argv_log if a[1] == "skills") == len(
        scenarios
    )  # discovery once per source


def test_real_find_orca_probes_with_the_discovery_argv_only(
    monkeypatch, argv_log, fake_clock
):
    import superclaude.cli.install_user_setup as setup

    probes: list[list[str]] = []

    def fake_run(argv, **kwargs):
        probes.append(list(argv))
        return SimpleNamespace(
            returncode=0, stdout=json.dumps({"topics": [{"name": "orca-cli"}]})
        )

    monkeypatch.setattr(setup.shutil, "which", lambda name: f"/opt/fake/{name}")
    monkeypatch.setattr(setup.subprocess, "run", fake_run)
    runner = FakeRunner(argv_log, [reply(1)])
    source = LiveSource(runner)  # the default Discover is _find_orca
    result = read(source, fake_clock)
    assert result.state == "OK"
    assert len(probes) <= 2 and all(
        p[1:] == ["skills", "list", "--json"] for p in probes
    )
    assert runner.log[-1][1:6] == [
        "orchestration",
        "worker-list",
        "--json",
        "--limit",
        "100",
    ]
    assert source.namespace == os.path.realpath(probes[0][0])


def test_two_failing_candidates_mean_at_most_two_probes_and_not_available(
    monkeypatch, argv_log, fake_clock
):
    import superclaude.cli.install_user_setup as setup

    probes: list[list[str]] = []

    def failing_run(argv, **kwargs):
        probes.append(list(argv))
        return SimpleNamespace(returncode=1, stdout="{}")

    monkeypatch.setattr(setup.shutil, "which", lambda name: f"/opt/fake/{name}")
    monkeypatch.setattr(setup.subprocess, "run", failing_run)
    runner = FakeRunner(argv_log, [reply(1)])
    source = LiveSource(runner)
    assert source.available is False
    assert read(source, fake_clock).code == "not-found"
    assert len(probes) <= 2 and runner.calls == 0


def test_discover_none_is_not_available_with_zero_worker_list_calls(
    argv_log, fake_clock
):
    runner = FakeRunner(argv_log, [reply(1)])
    discover = FakeDiscover(argv_log, None)
    source = LiveSource(runner, discover)
    assert source.available is False and source.namespace == ""
    for _ in range(3):
        result = read(source, fake_clock)
        assert (result.state, result.code, result.pages) == ("FAILED", "not-found", ())
    assert runner.calls == 0 and discover.calls == 1  # discovery runs once


def test_namespace_is_the_resolved_absolute_path_of_the_orca_cli(argv_log):
    source, _ = source_with([reply(1)], argv_log)
    assert source.namespace == os.path.realpath(ORCA)


# -- T2: forbidden words only inside the forbidden set ---------------------------------------------


def test_forbidden_words_appear_only_inside_the_forbidden_set():
    text = Path(adapter.__file__).read_text(encoding="utf-8")
    for word in ("--ack", "--wait", "--retry-request"):
        assert text.count(word) == 1, word
    block = re.search(r"^FORBIDDEN_PREFIXES = frozenset\(.*?\)\n", text, re.M | re.S)
    assert block, "the forbidden set must be one frozenset literal"
    for word in ("--ack", "--wait", "--retry-request"):
        assert word in block.group(0)
    assert text.count('"check"') == 1 and '"check"' in block.group(0)
    assert (
        "check" not in adapter.WORKER_LIST_TEMPLATE
        and "check" not in adapter.DISCOVERY_TEMPLATE
    )
    assert FORBIDDEN_PREFIXES >= {
        "check",
        "--ack",
        "--wait",
        "--retry-request",
        "dispatch",
        "inbox",
    }


# -- T36 and T37: argv validation before any call -----------------------------------------------------


@pytest.mark.parametrize(
    "bad", ["-x", "--run", "bad id", "", "a" * 129, "a/b", "x;y", "run\n1", 5]
)
def test_malformed_run_ids_are_rejected(bad):
    with pytest.raises(ArgvRejected) as info:
        build_argv(ORCA, run_id=bad)
    assert info.value.code == "run-id"


@pytest.mark.parametrize(
    "bad",
    [
        "-x",
        "--ack",
        "a\x00b",
        "x" * (CURSOR_MAX_BYTES + 1),
        "é" * CURSOR_MAX_BYTES,
        "",
        7,
    ],
)
def test_bad_cursors_are_rejected(bad):
    with pytest.raises(ArgvRejected) as info:
        build_argv(ORCA, cursor=bad)
    assert info.value.code == "cursor-rejected"


def test_good_values_are_separate_argv_items_and_the_cursor_is_unchanged():
    cursor = "abc==/+def.ghi_JKL-0"
    assert build_argv(ORCA) == TEMPLATE
    assert build_argv(ORCA, "run_A-1.b:2") == [*TEMPLATE, "--run", "run_A-1.b:2"]
    assert build_argv(ORCA, "run-a", cursor) == [
        *TEMPLATE,
        "--run",
        "run-a",
        "--cursor",
        cursor,
    ]
    assert build_argv(ORCA, cursor="x" * CURSOR_MAX_BYTES)[-1] == "x" * CURSOR_MAX_BYTES
    assert not any(
        "=" in a and a.startswith("--") for a in build_argv(ORCA, "run-a", cursor)
    )


@pytest.mark.parametrize(
    "argv",
    [
        [ORCA, "check"],
        [ORCA, "check", "--peek"],
        [ORCA, "check", "--all"],
        [ORCA, "inbox"],
        [ORCA, "dispatch"],
        [ORCA, "orchestration", "dispatch", "--json"],
        [*TEMPLATE, "--ack"],
        [*TEMPLATE, "--wait"],
        [*TEMPLATE, "--wait=5"],
        [*TEMPLATE, "--retry-request"],
        [*TEMPLATE, "--include-remote"],
        [ORCA, "orchestration", "worker-list", "--json"],
        [ORCA, "orchestration", "worker-stop", "--json", "--limit", "100"],
        [ORCA, "skills", "install"],
        [ORCA, "skills", "list"],
        [*TEMPLATE, "--cursor", "-x"],
        [*TEMPLATE, "--run", "--evil"],
        [*TEMPLATE, "--cursor", "c", "--run", "run-a"],
        [*TEMPLATE, "--run", "a", "--run", "b"],
        [ORCA],
        [],
        ["-evil", "skills", "list", "--json"],
    ],
)
def test_unlisted_argv_is_rejected_before_any_call(argv):
    with pytest.raises(ArgvRejected):
        assert_allowed(argv)


@pytest.mark.parametrize("prefix", sorted(FORBIDDEN_PREFIXES))
def test_every_forbidden_prefix_is_rejected_by_name_in_any_verb_or_flag_position(
    prefix,
):
    for argv in (
        [ORCA, prefix],
        [ORCA, f"{prefix}-more"],
        [*TEMPLATE, prefix],
        [ORCA, "orchestration", prefix],
    ):
        with pytest.raises(ArgvRejected) as info:
            assert_allowed(argv)
        assert info.value.code == "forbidden"


def test_forbidden_words_inside_option_values_are_values_not_verbs():
    assert_allowed(
        [*TEMPLATE, "--run", "dispatch-7"]
    )  # a run id that happens to start like a verb


def test_templates_pass_the_check():
    assert_allowed(TEMPLATE)
    assert_allowed([ORCA, "skills", "list", "--json"])
    assert_allowed([*TEMPLATE, "--run", "run-a", "--cursor", "c1"])


def test_bad_run_id_fails_before_any_runner_call(argv_log, fake_clock):
    source, runner = source_with([reply(1)], argv_log)
    with pytest.raises(ArgvRejected):
        read(source, fake_clock, run_id="-x")
    assert runner.calls == 0 and not any(a[1] == "orchestration" for a in argv_log)


def test_an_unlisted_argv_fails_loudly_in_the_fake_runner_and_with_real_subprocess_blocked(
    argv_log, fake_clock
):
    with pytest.raises(AssertionError, match="allow-list"):
        FakeRunner(argv_log)([ORCA, "check"], 1.0)
    live = LiveSource(production_runner, FakeDiscover(argv_log, ORCA))
    with pytest.raises(AssertionError, match="subprocess is blocked"):
        read(live, fake_clock)  # the real runner would spawn; the guard raises instead


def test_a_rejected_cursor_stops_paging_with_partial(argv_log, fake_clock):
    source, runner = source_with([reply(2, True, "-evil", 9)], argv_log)
    result = read(source, fake_clock)
    assert (result.state, result.code, len(result.pages), result.calls) == (
        "PARTIAL",
        "cursor-rejected",
        1,
        1,
    )
    assert runner.calls == 1


# -- T4 (adapter half) and paging integrity ------------------------------------------------------------


def test_a_source_that_always_has_more_stops_at_five_calls_with_partial(
    argv_log, fake_clock
):
    counter = {"n": 0}

    def always_more(argv, timeout):
        counter["n"] += 1
        return reply(100, True, f"cursor-{counter['n']}", 9999)

    source, runner = source_with([always_more], argv_log)
    result = read(source, fake_clock)
    assert (result.state, result.capped, result.calls, len(result.pages)) == (
        "PARTIAL",
        True,
        5,
        5,
    )
    assert runner.calls == 5 and result.code is None
    cursors = [a[a.index("--cursor") + 1] for a in argv_log if "--cursor" in a]
    assert cursors == ["cursor-1", "cursor-2", "cursor-3", "cursor-4"]


def test_a_finished_traversal_is_ok_and_follows_next_cursor(argv_log, fake_clock):
    source, runner = source_with(
        [reply(2, True, "c1", 3), reply(1, False, None, 3)], argv_log
    )
    result = read(source, fake_clock, run_id="run-a")
    assert (result.state, result.code, result.calls, len(result.pages)) == (
        "OK",
        None,
        2,
        2,
    )
    worker_calls = [a for a in argv_log if a[1] == "orchestration"]
    assert worker_calls[0][6:] == ["--run", "run-a"]
    assert worker_calls[1][6:] == ["--run", "run-a", "--cursor", "c1"]


@pytest.mark.parametrize(
    ("second_cursor", "code"),
    [
        (None, "cursor-stalled"),
        ("", "cursor-stalled"),
        ("c1", "cursor-stalled"),
        (5, "cursor-rejected"),
        ({"a": 1}, "cursor-rejected"),
    ],
)
def test_cursor_that_is_missing_empty_repeated_or_not_text_stops_paging(
    argv_log, fake_clock, second_cursor, code
):
    page2 = reply(1, True, None, 9)
    envelope = json.loads(page2[1])
    envelope["result"]["page"]["nextCursor"] = second_cursor
    source, _ = source_with(
        [reply(1, True, "c1", 9), (0, json.dumps(envelope))], argv_log
    )
    result = read(source, fake_clock)
    assert (result.state, result.code, len(result.pages)) == ("PARTIAL", code, 2)


def test_missing_cursor_on_the_first_page_is_partial_with_one_page(
    argv_log, fake_clock
):
    source, _ = source_with([reply(1, True, None, 9)], argv_log)
    result = read(source, fake_clock)
    assert (result.state, result.code, len(result.pages)) == (
        "PARTIAL",
        "cursor-stalled",
        1,
    )


def test_an_empty_page_while_total_is_above_zero_is_partial(argv_log, fake_clock):
    source, _ = source_with([reply(0, False, None, 7, rows=[])], argv_log)
    assert read(source, fake_clock).code == "empty-page"
    source, _ = source_with([reply(0, False, None, 0, rows=[])], argv_log)
    assert read(source, fake_clock).state == "OK"  # total 0: a genuinely empty fleet
    source, _ = source_with(
        [reply(2, True, "c1", 5), reply(0, True, "c2", 5, rows=[])], argv_log
    )
    result = read(source, fake_clock)
    assert (result.state, result.code, len(result.pages)) == (
        "PARTIAL",
        "empty-page",
        2,
    )


def test_the_adapter_only_peeks_and_leaves_shape_checks_to_the_parser(
    argv_log, fake_clock
):
    source, _ = source_with([(0, json.dumps({"result": {"workers": "x"}}))], argv_log)
    result = read(source, fake_clock)
    assert (
        result.state == "OK" and len(result.pages) == 1
    )  # parse.py turns this into FAILED (shape)


# -- errors, timeouts and the time budget ----------------------------------------------------------------


def test_failures_on_the_first_page_are_failed_with_a_code(argv_log, fake_clock):
    cases = [
        ([(2, "", "boom")], "exit:2"),
        ([(127, "")], "exit:127"),
        ([TimeoutError("slow")], "timeout"),
        ([RunnerFailure("output-cap", "big")], "output-cap"),
        ([RunnerFailure("spawn-error", "no such file")], "spawn-error"),
        ([FileNotFoundError("gone")], "spawn-error"),
        ([(0, "not json")], "json"),
        ([(0, "")], "json"),
    ]
    for responses, code in cases:
        source, _ = source_with(responses, argv_log)
        result = read(source, fake_clock)
        assert (result.state, result.code, result.pages) == ("FAILED", code, ()), code


def test_a_failure_on_a_later_page_keeps_the_pages_already_read_as_partial(
    argv_log, fake_clock
):
    source, _ = source_with(
        [reply(2, True, "c1", 9), (3, "", "late failure")], argv_log
    )
    result = read(source, fake_clock)
    assert (result.state, result.code, len(result.pages)) == ("PARTIAL", "exit:3", 1)
    assert result.diagnostic == "late failure"


def test_stderr_is_sanitized_and_kept_to_two_kib(argv_log, fake_clock):
    noisy = "\x1b[31mred\x1b[0m line\nsecond " + "x" * 5000
    source, _ = source_with([(1, "", noisy)], argv_log)
    result = read(source, fake_clock)
    assert "\x1b" not in result.diagnostic and result.diagnostic.startswith(
        "red line\nsecond"
    )
    assert len(result.diagnostic) <= 2048


def test_per_call_timeout_is_passed_and_capped_by_the_time_left(argv_log, fake_clock):
    source, runner = source_with([reply(1)], argv_log)
    read(source, fake_clock, budget=15)
    assert runner.timeouts == [10.0]
    source, runner = source_with([TimeoutError("slow")], argv_log)
    result = read(source, fake_clock, budget=3)
    assert (
        runner.timeouts == [3.0] and result.code == "overrun"
    )  # the budget, not the call limit, cut it
    source, runner = source_with([TimeoutError("slow")], argv_log, per_call_timeout=4.0)
    assert read(
        source, fake_clock, budget=15
    ).code == "timeout" and runner.timeouts == [4.0]


def test_the_budget_running_out_between_pages_is_overrun_partial(argv_log, fake_clock):
    def slow_first_page(argv, timeout):
        fake_clock.advance(20)
        return reply(2, True, "c1", 9)

    source, runner = source_with([slow_first_page], argv_log)
    result = read(source, fake_clock)
    assert (result.state, result.code, len(result.pages), runner.calls) == (
        "PARTIAL",
        "overrun",
        1,
        1,
    )
    source, runner = source_with([reply(1)], argv_log)
    result = source.read_pages(fake_clock, fake_clock.monotonic() - 1)  # no time at all
    assert (result.state, result.code, runner.calls) == ("FAILED", "overrun", 0)


def test_a_runner_timeout_failure_cut_by_the_budget_is_overrun(argv_log, fake_clock):
    source, _ = source_with([RunnerFailure("timeout", "")], argv_log)
    assert read(source, fake_clock, budget=2).code == "overrun"
    source, _ = source_with([RunnerFailure("timeout", "")], argv_log)
    assert read(source, fake_clock, budget=15).code == "timeout"


# -- the production runner on real processes ---------------------------------------------------------------

PY = [sys.executable, "-I", "-c"]


@pytest.mark.observe_real_process
def test_production_runner_returns_stdout_stderr_and_returncode():
    rc, out, err = production_runner(
        [*PY, "import sys; print('{\"ok\": 1}'); sys.stderr.write('warn')"], 10
    )
    assert (rc, out.strip(), err) == (0, '{"ok": 1}', "warn")
    rc, out, err = production_runner([*PY, "import sys; sys.exit(3)"], 10)
    assert rc == 3 and out == ""


@pytest.mark.observe_real_process
def test_production_runner_kills_and_reaps_a_child_that_sleeps_past_the_timeout(
    tmp_path,
):
    pidfile = tmp_path / "pid"
    code = "import os, sys, time; open(sys.argv[1], 'w').write(str(os.getpid())); time.sleep(60)"
    started = time.monotonic()
    with pytest.raises(RunnerFailure) as info:
        production_runner([*PY, code, str(pidfile)], 1.5)
    assert info.value.code == "timeout" and time.monotonic() - started < 10
    pid = int(pidfile.read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)  # gone, and reaped: not even a zombie is left


@pytest.mark.observe_real_process
def test_production_runner_kills_a_child_that_writes_more_than_8_mib(tmp_path):
    pidfile = tmp_path / "pid"
    code = (
        "import os, sys, time; open(sys.argv[1], 'w').write(str(os.getpid()));"
        "sys.stdout.buffer.write(b'x' * (9 * 1024 * 1024)); sys.stdout.flush(); time.sleep(60)"
    )
    started = time.monotonic()
    with pytest.raises(RunnerFailure) as info:
        production_runner([*PY, code, str(pidfile)], 20)
    assert info.value.code == "output-cap" and time.monotonic() - started < 15
    with pytest.raises(ProcessLookupError):
        os.kill(int(pidfile.read_text()), 0)


@pytest.mark.observe_real_process
def test_production_runner_keeps_at_most_2_kib_of_stderr_without_blocking_the_child():
    code = "import sys; sys.stderr.write('e' * 300000); sys.stdout.write('{}')"
    rc, out, err = production_runner([*PY, code], 20)
    assert (rc, out) == (0, "{}")
    assert 0 < len(err.encode()) <= 2048


@pytest.mark.observe_real_process
def test_production_runner_returns_spawn_error_when_the_binary_does_not_exist():
    with pytest.raises(RunnerFailure) as info:
        production_runner(["/nonexistent/dir/binary-xyz", "--json"], 5)
    assert info.value.code == "spawn-error"


@pytest.mark.observe_real_process
def test_live_source_with_the_production_runner_maps_a_missing_binary_to_a_failed_cycle(
    argv_log, fake_clock
):
    source = LiveSource(production_runner, lambda: "/nonexistent/dir/orca")
    result = read(source, fake_clock)
    assert (result.state, result.code) == ("FAILED", "spawn-error")


# -- module hygiene (AD-1) ---------------------------------------------------------------------------------


def test_adapter_imports_sanitize_but_not_parse_or_collector_and_owns_subprocess():
    text = Path(adapter.__file__).read_text(encoding="utf-8")
    assert re.search(r"^from superclaude\.cli\.observe\.sanitize import", text, re.M)
    assert not re.search(r"observe\.(parse|collector|view|render|export)\b", text)
    assert re.search(r"^import subprocess$", text, re.M)
