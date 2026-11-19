"""Several orchestrators: the registry, the in-flight count, routing and the lifecycle (design 5.7)."""

from __future__ import annotations

import os
import re
import stat
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from superclaude.cli.issue_watch import record, repos, route, wake
from superclaude.cli.issue_watch.record import Hold

from .conftest import (
    CYCLE_NOW,
    FIXED_NOW,
    REPO_A,
    REPO_B,
    FakeWaker,
    decisions,
    make_config,
    orch_dir,
    read_wake,
    run,
    wake_files,
    write_json,
    write_plan_record,
    write_registry,
    write_repos,
    write_run,
    write_state_file,
)

NOW = datetime(2026, 11, 19, 12, 0, tzinfo=timezone.utc)
K = lambda n, repo=REPO_A: f"{repo}#{n}"  # noqa: E731
TIERS = "Tiers in this workspace:\n    ccsession --tier tier1b\n    ccsession --tier tier2\n"


def rdoc_of(tmp_path, **repo_over):
    orch = tmp_path / "orch"
    orch.mkdir(exist_ok=True)
    repo = {"repo": REPO_A, "enabled": True, "checkout": None, **repo_over}
    write_repos(orch, repos=[repo, {"repo": REPO_B, "enabled": True, "checkout": None}])
    return repos.parse_repos((orch / "repos.yaml").read_text(), ("tier1b", "tier2"))


def entry(ident="ironclaude-1", repo=REPO_A, status="active", n=None):
    return route.OrchEntry(ident, repo, f"orchestrator-{ident}", NOW, status)


def no_runs(_ident):
    return None


def doc_with(*, entries=(), holds=None):
    d = record.empty_doc(FIXED_NOW)
    for repo, n, state, orch in entries:
        d = record.mark_pending(d, repo, n, orch, FIXED_NOW)
        if state == "woken":
            d = record.mark_woken(d, K(n, repo), "20261107T120000Z-0000000a", FIXED_NOW)
        elif state == "unknown":
            d = record.mark_unknown(d, K(n, repo), None, None, FIXED_NOW)
        elif state == "acked":
            d = record.mark_acked(d, K(n, repo), FIXED_NOW)
    for key, hold in (holds or {}).items():
        d = record.set_hold(d, key, hold)
    return d


# --- names -------------------------------------------------------------------------------------------


def test_the_tag_is_orchestrator_short_n_and_fits_the_ccsession_tag_pattern():
    assert route.tag_of("orchestrator", "ironclaude", 1) == "orchestrator-ironclaude-1"
    assert route.orchestrator_id("ironclaude", 1) == "ironclaude-1"
    assert re.fullmatch(
        r"[A-Za-z0-9._-]{1,32}", route.tag_of("orchestrator", "ironclaude", 12)
    )
    with pytest.raises(ValueError):
        route.orchestrator_id("ironclaude", 0)
    with pytest.raises(ValueError):
        route.orchestrator_id("Iron", 1)


def test_n_is_the_smallest_unused_number_and_an_ended_id_is_never_reused():
    reg = {
        "ironclaude-1": entry(),
        "ironclaude-3": entry("ironclaude-3", status="ended"),
    }
    assert route.next_n(reg, "ironclaude") == 2
    reg["ironclaude-2"] = entry("ironclaude-2", status="ended")
    assert route.next_n(reg, "ironclaude") == 4
    assert route.next_n(reg, "example") == 1
    assert route.n_of("ironclaude-12") == 12


# --- the registry ----------------------------------------------------------------------------------------


def test_a_missing_registry_is_empty_and_a_saved_one_round_trips(tmp_path):
    assert route.load_registry(tmp_path) == {}
    reg = {
        "ironclaude-1": replace(entry(), tier="tier2", fallback_from="tier1b"),
        "example-1": entry("example-1", REPO_B, "ended"),
    }
    route.save_registry(tmp_path, reg)
    path = tmp_path / ".orchestrator" / "orchestrators.json"
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    assert route.load_registry(tmp_path) == reg
    assert sorted(p.name for p in path.parent.iterdir()) == [
        "orchestrators.json"
    ]  # no temp file left


@pytest.mark.parametrize(
    "raw",
    [
        "[]",
        "not json",
        '{"Bad-Id": {"repo": "o/r", "tag": "t", "created_at": "2026-11-19T12:00:00Z", "status": "active"}}',
        '{"x-0": {"repo": "o/r", "tag": "t", "created_at": "2026-11-19T12:00:00Z", "status": "active"}}',
        '{"x-1": {"repo": "o/r", "tag": "t", "created_at": "2026-11-19T12:00:00Z", "status": "paused"}}',
        '{"x-1": {"repo": "bad", "tag": "t", "created_at": "2026-11-19T12:00:00Z", "status": "active"}}',
        '{"x-1": {"repo": "o/r", "tag": "t", "created_at": "soon", "status": "active"}}',
        '{"x-1": {"repo": "o/r", "tag": "t", "created_at": "2026-11-19T12:00:00Z"}}',
        '{"x-1": {"repo": "o/r", "tag": "t", "created_at": "2026-11-19T12:00:00Z", "status": "active", "extra": 1}}',
        '{"x-1": {"repo": "o/r", "tag": "t", "created_at": "2026-11-19T12:00:00Z", "status": "active", "tier": "claude-opus"}}',
        '{"x-1": 5}',
    ],
)
def test_an_unreadable_or_malformed_registry_is_registry_invalid(tmp_path, raw):
    (tmp_path / ".orchestrator").mkdir()
    (tmp_path / ".orchestrator" / "orchestrators.json").write_text(raw)
    with pytest.raises(route.RegistryError) as err:
        route.load_registry(tmp_path)
    assert err.value.reason == "registry_invalid"


def test_the_state_lock_is_exclusive_and_waits_a_bounded_time(tmp_path):
    clock = {"t": 0.0}
    sleeps: list[float] = []

    def sleep(s):
        sleeps.append(s)
        clock["t"] += s

    with route.state_lock(tmp_path):
        assert (
            stat.S_IMODE(os.stat(tmp_path / ".orchestrator" / "state.lock").st_mode)
            == 0o600
        )
        with pytest.raises(route.StateLockBusy):
            with route.state_lock(
                tmp_path, 1.0, sleep=sleep, monotonic=lambda: clock["t"]
            ):
                pass
    assert sleeps and sum(sleeps) >= 1.0
    with route.state_lock(tmp_path):  # free again
        pass


# --- what the orchestrators wrote (read only) -------------------------------------------------------------


def test_the_run_file_gives_status_and_run_id_and_a_missing_one_is_a_first_start(
    tmp_path,
):
    config = make_config(tmp_path)
    assert route.read_run(config.orchestrator_repo, "ironclaude-1") == route.RunInfo(
        None, None
    )
    write_run(config, "ironclaude-1", "ending", "run_7")
    assert route.read_run(config.orchestrator_repo, "ironclaude-1") == route.RunInfo(
        "ending", "run_7"
    )
    write_json(
        orch_dir(config) / "runs" / "ironclaude-2.json",
        {"status": "gone", "run_id": "bad id!"},
    )
    assert route.read_run(config.orchestrator_repo, "ironclaude-2") == route.RunInfo(
        None, None
    )
    assert route.read_run(config.orchestrator_repo, "../x") == route.RunInfo(None, None)


def test_state_files_are_read_by_key_and_plan_records_and_subfolders_are_skipped(
    tmp_path,
):
    config = make_config(tmp_path)
    write_state_file(config, REPO_A, 5, "in_progress", "ironclaude-1")
    write_state_file(config, REPO_A, 6, "escalated", "ironclaude-1")
    write_plan_record(config, REPO_A, 9, CYCLE_NOW, "in_progress")
    (orch_dir(config) / "issues" / "retaken").mkdir()
    (orch_dir(config) / "issues" / "retaken" / "x.json").write_text("{}")
    (orch_dir(config) / "issues" / "IronbellyOrg__IronClaude__7.json").write_text(
        "{broken"
    )
    (orch_dir(config) / "issues" / "IronbellyOrg__IronClaude__8.json").write_text(
        '{"status": "odd"}'
    )
    (orch_dir(config) / "issues" / "notes.json").write_text("{}")
    files = route.read_state_files(config.orchestrator_repo)
    assert sorted(files) == [K(5), K(6), K(7), K(8)]
    assert (files[K(5)].status, files[K(5)].orchestrator, files[K(5)].readable) == (
        "in_progress",
        "ironclaude-1",
        True,
    )
    assert (
        files[K(7)].readable is False and files[K(8)].readable is False
    )  # damaged: they count as in flight
    assert route.read_state_files(tmp_path / "none") == {}


def test_a_plan_record_is_read_by_the_name_of_its_own_request(tmp_path):
    config = make_config(tmp_path)
    at = datetime(2026, 11, 19, 10, 15, 0, tzinfo=timezone.utc)
    assert route.plan_record_status(config.orchestrator_repo, REPO_A, 5, at) is None
    write_plan_record(config, REPO_A, 5, at, "done")
    assert route.plan_record_status(config.orchestrator_repo, REPO_A, 5, at) == "done"
    assert (
        route.plan_record_status(
            config.orchestrator_repo, REPO_A, 5, at + timedelta(days=1)
        )
        is None
    )
    path = (
        orch_dir(config)
        / "issues"
        / "plan-IronbellyOrg__IronClaude__5.20261119T101500Z.json"
    )
    path.write_text("{broken")
    assert (
        route.plan_record_status(config.orchestrator_repo, REPO_A, 5, at)
        == "in_progress"
    )


# --- the in-flight count (5.7 point 1) -----------------------------------------------------------------------------


def count(registry, doc, files=None, plans=None):
    files = files or {}
    plans = plans or {}
    return route.in_flight(
        registry, doc, files, lambda repo, n, at: plans.get((repo, n))
    )


def sf(n, status="in_progress", orch="ironclaude-1", readable=True, repo=REPO_A):
    return route.StateFile(repo, n, status, orch, readable)


def test_in_progress_files_and_unacknowledged_entries_both_count_and_a_key_once():
    reg = {"ironclaude-1": entry()}
    doc = doc_with(
        entries=[
            (REPO_A, 1, "pending", "ironclaude-1"),
            (REPO_A, 2, "woken", "ironclaude-1"),
            (REPO_A, 3, "unknown", "ironclaude-1"),
        ]
    )
    files = {K(4): sf(4), K(2): sf(2)}  # issue 2 has its file now: counted once
    got = count(reg, doc, files)
    assert got == {"ironclaude-1": {K(1), K(2), K(3), K(4)}}


def test_done_skipped_failed_and_escalated_files_do_not_count_and_an_escalated_one_that_returns_does():
    reg = {"ironclaude-1": entry()}
    files = {
        K(n): sf(n, status)
        for n, status in ((1, "done"), (2, "skipped"), (3, "failed"), (4, "escalated"))
    }
    assert count(reg, record.empty_doc(FIXED_NOW), files) == {"ironclaude-1": set()}
    files[K(4)] = sf(4, "in_progress")  # the human answered
    assert count(reg, record.empty_doc(FIXED_NOW), files) == {"ironclaude-1": {K(4)}}


def test_an_acknowledged_entry_and_an_entry_of_another_orchestrator_do_not_count_here():
    reg = {"ironclaude-1": entry(), "ironclaude-2": entry("ironclaude-2")}
    doc = doc_with(
        entries=[
            (REPO_A, 1, "acked", "ironclaude-1"),
            (REPO_A, 2, "woken", "ironclaude-2"),
        ]
    )
    assert count(reg, doc) == {"ironclaude-1": set(), "ironclaude-2": {K(2)}}


def test_a_state_file_that_cannot_be_parsed_counts_against_every_active_orchestrator_of_its_repo():
    reg = {
        "ironclaude-1": entry(),
        "ironclaude-2": entry("ironclaude-2"),
        "example-1": entry("example-1", REPO_B),
        "ironclaude-3": entry("ironclaude-3", status="ended"),
    }
    files = {K(9): sf(9, None, None, readable=False)}
    got = count(reg, record.empty_doc(FIXED_NOW), files)
    assert got["ironclaude-1"] == got["ironclaude-2"] == {K(9)}
    assert got["example-1"] == set() and got["ironclaude-3"] == set()


def test_an_open_plan_request_is_one_place_until_its_record_is_final_or_it_is_stuck():
    reg = {"ironclaude-1": entry()}
    at = NOW

    def hold(state="woken", **over):
        return Hold(
            state="held",
            first_held_at=NOW,
            plan_requested_at=at,
            plan_request_orchestrator="ironclaude-1",
            plan_request=state,
            **over,
        )

    key = K(5)
    assert count(reg, doc_with(holds={key: hold("pending")})) == {"ironclaude-1": {key}}
    assert count(
        reg, doc_with(holds={key: hold("acked")}), plans={(REPO_A, 5): "in_progress"}
    ) == {"ironclaude-1": {key}}
    assert count(reg, doc_with(holds={key: hold("acked")})) == {
        "ironclaude-1": {key}
    }  # taken, no record yet
    for ended in ("done", "failed"):
        assert count(
            reg, doc_with(holds={key: hold("acked")}), plans={(REPO_A, 5): ended}
        ) == {"ironclaude-1": set()}
    for state in ("stuck", "skipped", "abandoned"):
        assert count(reg, doc_with(holds={key: hold(state)})) == {"ironclaude-1": set()}
    gone = replace(hold("acked"), state="hand_removed")  # the hold ended
    assert count(reg, doc_with(holds={key: gone})) == {"ironclaude-1": set()}
    unrequested = Hold(state="held", first_held_at=NOW)
    assert count(reg, doc_with(holds={key: unrequested})) == {"ironclaude-1": set()}


# --- routing (5.7 point 3) --------------------------------------------------------------------------------------------


def do_route(
    tmp_path, items, reg=None, counts=None, run_status=no_runs, plans=False, **repo_over
):
    reg = {} if reg is None else reg
    counts = (
        {i: set(c) for i, c in (counts or {}).items()}
        if counts is not None
        else {i: set() for i in reg}
    )
    out = route.route(
        reg,
        counts,
        items,
        rdoc_of(tmp_path, **repo_over),
        "orchestrator",
        NOW,
        run_status,
        plan_requests=plans,
    )
    return out, reg, counts


def test_four_issues_of_one_repo_give_three_to_the_first_orchestrator_and_start_a_second(
    tmp_path,
):
    out, reg, counts = do_route(tmp_path, [(REPO_A, n) for n in (1, 2, 3, 4)])
    assert [(r.number, r.orchestrator, r.new) for r in out] == [
        (1, "ironclaude-1", True),
        (2, "ironclaude-1", False),
        (3, "ironclaude-1", False),
        (4, "ironclaude-2", True),
    ]
    assert (
        sorted(reg) == ["ironclaude-1", "ironclaude-2"]
        and reg["ironclaude-2"].tag == "orchestrator-ironclaude-2"
    )
    assert [len(counts[i]) for i in sorted(counts)] == [
        3,
        1,
    ]  # a routed issue counts in the same cycle


def test_max_in_flight_one_with_two_issues_starts_two(tmp_path):
    out, reg, _ = do_route(tmp_path, [(REPO_A, 1), (REPO_A, 2)], max_in_flight=1)
    assert [r.orchestrator for r in out] == ["ironclaude-1", "ironclaude-2"]


def test_an_issue_goes_to_the_first_active_orchestrator_with_room(tmp_path):
    reg = {"ironclaude-1": entry(), "ironclaude-2": entry("ironclaude-2")}
    counts = {"ironclaude-1": {K(10), K(11), K(12)}, "ironclaude-2": {K(13)}}
    out, _, _ = do_route(tmp_path, [(REPO_A, 1)], reg, counts)
    assert out[0].orchestrator == "ironclaude-2" and out[0].new is False


def test_each_repo_has_its_own_orchestrators(tmp_path):
    out, reg, _ = do_route(tmp_path, [(REPO_A, 1), (REPO_B, 2)])
    assert {r.orchestrator for r in out} == {"ironclaude-1", "example-1"}
    assert reg["example-1"].repo == REPO_B


def test_an_ending_or_ended_orchestrator_never_gets_a_new_issue_and_its_id_is_not_reused(
    tmp_path,
):
    reg = {"ironclaude-1": entry()}
    for status in ("ending", "ended"):
        out, new_reg, _ = do_route(
            tmp_path, [(REPO_A, 1)], dict(reg), run_status=lambda i, s=status: s
        )
        assert out[0].orchestrator == "ironclaude-2" and out[0].new is True
    out, _, _ = do_route(
        tmp_path, [(REPO_A, 1)], {"ironclaude-1": entry(status="ended")}
    )
    assert out[0].orchestrator == "ironclaude-2"


def test_a_plan_request_goes_only_to_an_active_orchestrator_with_a_free_place(tmp_path):
    reg = {"ironclaude-1": entry()}
    full = {"ironclaude-1": {K(1), K(2), K(3)}}
    out, new_reg, _ = do_route(tmp_path, [(REPO_A, 9)], dict(reg), full, plans=True)
    assert out == [(REPO_A, 9)] and sorted(new_reg) == [
        "ironclaude-1"
    ]  # nothing sent, none started
    out, _, _ = do_route(
        tmp_path, [(REPO_A, 9)], dict(reg), {"ironclaude-1": {K(1)}}, plans=True
    )
    assert out[0].orchestrator == "ironclaude-1" and out[0].new is False
    out, new_reg, _ = do_route(
        tmp_path, [(REPO_A, 9)], {}, plans=True
    )  # the repo has none at all
    assert (
        out[0].orchestrator == "ironclaude-1"
        and out[0].new is True
        and "ironclaude-1" in new_reg
    )


def test_an_item_of_a_repo_that_is_not_listed_is_not_routed(tmp_path):
    out, reg, _ = do_route(tmp_path, [("Other/Repo", 1)])
    assert out == [("Other/Repo", 1)] and reg == {}


# --- the dead-orchestrator check and the lifecycle (5.7 point 5) --------------------------------------------------------


def test_an_active_orchestrator_with_no_terminal_and_files_in_progress_is_resumed():
    reg = {"ironclaude-1": entry(), "ironclaude-2": entry("ironclaude-2")}
    counts = {"ironclaude-1": {K(1)}, "ironclaude-2": set()}
    ended, resume = route.end_finished(
        reg, counts, {"ironclaude-1"}, no_runs, lambda e: False
    )
    assert (ended, resume) == (["ironclaude-2"], ["ironclaude-1"])
    assert (
        reg["ironclaude-2"].status == "ended" and reg["ironclaude-1"].status == "active"
    )


def test_a_dead_orchestrator_with_only_unacknowledged_wakes_is_left_for_the_resend_to_start():
    reg = {"ironclaude-1": entry()}
    ended, resume = route.end_finished(
        reg, {"ironclaude-1": {K(1)}}, set(), no_runs, lambda e: False
    )
    assert (ended, resume) == ([], []) and reg["ironclaude-1"].status == "active"


def test_a_live_or_unreadable_orchestrator_is_left_alone_and_a_run_that_says_ended_ends_it():
    reg = {"ironclaude-1": entry(), "ironclaude-2": entry("ironclaude-2")}
    assert route.end_finished(
        reg,
        {"ironclaude-1": set(), "ironclaude-2": set()},
        set(),
        no_runs,
        lambda e: True,
    ) == ([], [])
    assert route.end_finished(
        reg, {"ironclaude-1": set()}, {"ironclaude-1"}, no_runs, lambda e: None
    ) == ([], [])
    ended, _ = route.end_finished(
        reg,
        {},
        set(),
        lambda i: "ended" if i == "ironclaude-2" else None,
        lambda e: True,
    )
    assert ended == ["ironclaude-2"] and reg["ironclaude-2"].status == "ended"


# --- in the cycle -----------------------------------------------------------------------------------------------------------------


def test_the_poll_starts_a_dead_orchestrator_again_with_the_same_tag_and_a_resume_wake(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}})
    write_state_file(world.config, REPO_A, 77, "in_progress", "ironclaude-1")
    waker = FakeWaker(dead={"orchestrator-ironclaude-1"})
    res = run(world, tmp_path, tmp_state, waker=waker)
    ((target, wake_id, _),) = waker.deliveries
    assert (target.orchestrator, target.tag) == (
        "ironclaude-1",
        "orchestrator-ironclaude-1",
    )
    (path,) = wake_files(world.config)
    d = read_wake(path)
    assert d["target"] == {
        "orchestrator": "ironclaude-1",
        "tag": "orchestrator-ironclaude-1",
        "repo": REPO_A,
        "resume": True,
    }
    assert d["assigned"] == [] and d["plan_requests"] == [] and d["attempt"] == 1
    assert res.exit_code == 0 and wake_id == d["wake_id"]


def test_a_failed_restart_is_exit_7(tmp_path, tmp_state, gh_world):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}})
    write_state_file(world.config, REPO_A, 77, "in_progress", "ironclaude-1")
    waker = FakeWaker(
        wake.WakeOutcome("no_session", "no_tier"), dead={"orchestrator-ironclaude-1"}
    )
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert (res.exit_code, res.reason) == (7, "no_session") and waker.unread == [
        "no_session"
    ]


def test_a_dead_orchestrator_with_nothing_in_flight_is_marked_ended_and_not_started(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}})
    waker = FakeWaker(dead={"orchestrator-ironclaude-1"})
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert waker.deliveries == [] and res.exit_code == 0
    assert (
        route.load_registry(world.config.orchestrator_repo)["ironclaude-1"].status
        == "ended"
    )


def test_a_live_idle_orchestrator_is_asked_nothing_when_nothing_is_new_and_the_registry_is_not_rewritten(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}})
    path = orch_dir(world.config) / "orchestrators.json"
    before = (path.read_bytes(), path.stat().st_mtime_ns)
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker)
    assert (
        waker.deliveries == []
        and (path.read_bytes(), path.stat().st_mtime_ns) == before
    )


def test_a_run_that_is_ending_gets_no_issue_and_a_new_orchestrator_takes_it(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}})
    write_run(world.config, "ironclaude-1", "ending")
    world.issue(REPO_A, 5)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert [t.orchestrator for t, _, _ in waker.deliveries] == [
        "ironclaude-2"
    ] and res.exit_code == 0
    assert (
        route.load_registry(world.config.orchestrator_repo)["ironclaude-2"].status
        == "active"
    )


def test_the_mailbox_goes_to_the_run_of_the_target_orchestrator_only(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}, "ironclaude-2": {}})
    write_run(world.config, "ironclaude-1", run_id="run_one")
    write_run(world.config, "ironclaude-2", run_id="run_two")
    for n in (11, 12, 13):
        write_state_file(world.config, REPO_A, n, "in_progress", "ironclaude-1")
    world.issue(REPO_A, 5)
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker)
    ((target, _, _),) = waker.deliveries
    assert (target.orchestrator, target.run_id) == (
        "ironclaude-2",
        "run_two",
    )  # the first is full


def test_an_unreadable_registry_stops_the_cycle_with_exit_2_and_nothing_is_saved_pending(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    (orch_dir(world.config) / "orchestrators.json").write_text("[]")
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert (res.exit_code, res.reason) == (
        2,
        "registry_invalid",
    ) and waker.deliveries == []
    assert tmp_state.load().entries == {}


def test_a_busy_state_lock_ends_the_cycle_lock_held_with_nothing_written(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world = gh_world()
    world.issue(REPO_A, 5)

    def busy(*a, **k):
        raise route.StateLockBusy

    monkeypatch.setattr(route, "state_lock", busy)
    res = run(world, tmp_path, tmp_state)
    assert (res.exit_code, res.reason) == (
        75,
        "lock_held",
    ) and tmp_state.load().entries == {}


def test_routing_and_the_wake_files_are_written_under_the_state_lock(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world = gh_world()
    world.issue(REPO_A, 5)
    seen = []
    real = route.state_lock

    from contextlib import contextmanager

    @contextmanager
    def spy(*a, **k):
        with real(*a, **k):
            seen.append(("in", len(wake_files(world.config))))
            yield
            seen.append(("out", len(wake_files(world.config))))

    monkeypatch.setattr(route, "state_lock", spy)
    waker = FakeWaker(
        on_deliver=lambda t, w: seen.append(("send", len(wake_files(world.config))))
    )
    run(world, tmp_path, tmp_state, waker=waker)
    assert seen[:3] == [
        ("in", 0),
        ("out", 1),
        ("send", 1),
    ]  # the file is written before the lock is released


def test_a_dry_run_reports_the_routing_and_saves_no_registry(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    for n in (1, 2, 3, 4):
        world.issue(REPO_A, n)
    res = run(world, tmp_path, tmp_state, dry_run=True)
    assert len(res.would_wake) == 4
    lines = [ln for ln in res.lines if ln["kind"] == "decision"]
    assert [ln["orchestrator"] for ln in lines] == ["ironclaude-1"] * 3 + [
        "ironclaude-2"
    ]
    assert not (world.config.orchestrator_repo / ".orchestrator").exists()
    assert decisions(res)[0][0] == "woken"
