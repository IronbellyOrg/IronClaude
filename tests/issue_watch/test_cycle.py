"""The poll cycle (design 4.5): configuration, exit rules, the wake of new issues, resend, backoff.

A cycle runs over ``GhWorld`` (a scripted GitHub, git and Orca behind one
``FakeRunner``) and ``FakeWaker``; nothing here reaches a real ``gh``, ``orca``
or clock.
"""

from __future__ import annotations

import json
from datetime import timedelta

import pytest

from superclaude.cli.issue_watch import cycle, record, wake
from superclaude.cli.issue_watch.record import FileStore

from .conftest import (
    CYCLE_NOW,
    EMPTY_BODY,
    FIXED_NOW,
    GOOD_BODY,
    OWN_ID,
    REPO_A,
    REPO_B,
    FakeClock,
    FakeRunner,
    FakeWaker,
    GhWorld,
    decisions,
    make_config,
    orch_dir,
    read_wake,
    reasons,
    result,
    run,
    wake_files,
    write_ack,
    write_registry,
    write_repos,
    write_run,
)

K5 = f"{REPO_A}#5"


# --- configuration -------------------------------------------------------------------------------


def write_config(tmp_path, **over):
    raw = {
        "schema_version": 2,
        "enabled": True,
        "orchestrator_repo": str(tmp_path / "orch"),
        "state_dir": str(tmp_path / "state"),
    }
    raw.update(over)
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps({k: v for k, v in raw.items() if v is not KeyError}))
    return path


def test_load_config_reads_the_new_keys_and_only_those(tmp_path):
    cfg = cycle.load_config(
        write_config(tmp_path, owner_account_id=5, session_tag_prefix="poll")
    )
    assert (cfg.enabled, cfg.owner_account_id, cfg.session_tag_prefix) == (
        True,
        5,
        "poll",
    )
    assert (
        cfg.orchestrator_repo == tmp_path / "orch"
        and cfg.state_dir == tmp_path / "state"
    )
    assert (
        cycle.load_config(write_config(tmp_path)).session_tag_prefix == "orchestrator"
    )


@pytest.mark.parametrize(
    "over",
    [
        {"schema_version": 1},
        {"schema_version": KeyError},
        {"enabled": "yes"},
        {"orchestrator_repo": "relative/path"},
        {"orchestrator_repo": KeyError},
        {"orchestrator_repo": "~/orch"},
        {"owner_account_id": 0},
        {"owner_account_id": True},
        {"session_tag_prefix": "Has Space"},
        {"session_tag_prefix": "x" * 13},
        {"state_dir": "relative"},
        # the keys of the retired gate are unknown now
        {"labels": {"trigger": "x"}},
        {"project_id": "PVT_x"},
        {"approvers_file": "/abs/approvers"},
        {"worktree": "/abs/wt"},
    ],
)
def test_load_config_refuses_a_bad_or_retired_key(tmp_path, over):
    with pytest.raises(cycle.ConfigError) as err:
        cycle.load_config(write_config(tmp_path, **over))
    assert err.value.reason == "config_invalid"


def test_load_config_refuses_a_missing_file_bad_json_and_a_network_state_dir(
    tmp_path, monkeypatch
):
    for text in (None, "{", "[]"):
        path = tmp_path / "bad.json"
        if text is not None:
            path.write_text(text)
        with pytest.raises(cycle.ConfigError):
            cycle.load_config(path)
    monkeypatch.setattr(
        cycle, "_read_mountinfo", lambda: "1 0 0:1 / / rw - nfs4 server:/x rw\n"
    )
    with pytest.raises(cycle.ConfigError, match="config_invalid"):
        cycle.load_config(write_config(tmp_path))


def test_validate_setup_names_the_two_new_exit_2_reasons(tmp_path):
    cfg = make_config(tmp_path)
    runner = FakeRunner(
        {
            ("ccsession", "--help"): result(
                stdout="Tiers in this workspace:\n    ccsession --tier tier2\n"
            )
        }
    )
    assert cycle.validate_setup(cfg, runner).repos[0].repo == REPO_A
    with pytest.raises(cycle.ConfigError) as err:
        cycle.validate_setup(
            make_config(tmp_path, orchestrator_repo=tmp_path / "missing"), runner
        )
    assert err.value.reason == "orchestrator_repo_invalid"
    (cfg.orchestrator_repo / "repos.yaml").write_text("schema_version: 9\n")
    with pytest.raises(cycle.ConfigError) as err:
        cycle.validate_setup(cfg, runner)
    assert err.value.reason == "repos_invalid"


def test_the_resolve_exit_precedence_is_2_6_7_5_3_4_and_75_alone():
    r = cycle.resolve_exit
    assert r(frozenset({4, 3, 5, 7, 6, 2})) == 2
    assert r(frozenset({4, 3, 5, 7, 6})) == 6
    assert r(frozenset({4, 3, 5, 7})) == 7
    assert r(frozenset({4, 3, 5})) == 5
    assert r(frozenset({4, 3})) == 3 and r(frozenset({4})) == 4
    assert (
        r(frozenset({75})) == 75 and r(frozenset({75, 4})) == 4 and r(frozenset()) == 0
    )


def test_the_deadline_gives_a_timeout_and_a_floor():
    clock = FakeClock(CYCLE_NOW)
    deadline = cycle.Deadline(clock)
    assert deadline.timeout_for(20) == 20.0 and deadline.launch_allowed()
    clock.advance(121)
    assert not deadline.launch_allowed() and deadline.timeout_for(20) == 20.0
    clock.advance(116)  # 237 s: under the 5 s floor
    assert deadline.timeout_for(20) is None


def test_the_design_constants_are_kept():
    assert (
        cycle.MAX_CANDIDATES == 10
        and cycle.DAY_CAP == 6
        and cycle.DEADLINE_TOTAL_S == 240.0
    )
    assert cycle.LAUNCH_CUTOFF_S == 120.0 and cycle.SCHEMA_VERSION == 2
    for gone in (
        "MAX_LAUNCHES_PER_CYCLE",
        "DEFAULT_TRIGGER_LABEL",
        "validate_approvers",
        "approvers_summary",
        "_retry_orca",
    ):
        assert not hasattr(cycle, gone), gone


# --- nothing new, one new issue, four new issues --------------------------------------------------------


def test_nothing_new_gives_no_wake_file_and_no_orca_call(tmp_path, tmp_state, gh_world):
    world = gh_world()
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert (res.exit_code, res.reason) == (0, "cycle_complete")
    assert wake_files(world.config) == [] and waker.deliveries == []
    assert (
        world.runner.argvs("orca") == []
        and not (world.config.orchestrator_repo / ".orchestrator").exists()
    )
    assert res.woken == ()


def test_one_new_issue_gives_one_wake_file_one_delivery_and_a_woken_entry(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert res.exit_code == 0 and res.woken == (K5,)
    (path,) = wake_files(world.config)
    data = read_wake(path)
    assert (
        data["schema"] == "orchestrator-wake/1"
        and path.name == f"{data['wake_id']}.json"
    )
    assert data["target"] == {
        "orchestrator": "ironclaude-1", "tag": "orchestrator-ironclaude-1",
        "repo": REPO_A, "resume": False,
    }  # fmt: skip
    (item,) = data["assigned"]
    assert (
        item["repo"],
        item["number"],
        item["assignees"],
        item["checkout_state"],
    ) == (REPO_A, 5, ["owner-login"], "ok")
    assert (
        data["attempt"] == 1
        and data["poll"]["dry_run"] is False
        and data["plan_requests"] == []
    )
    ((target, wake_id, start),) = waker.deliveries
    assert (target.orchestrator, target.tag, wake_id, start) == (
        "ironclaude-1",
        "orchestrator-ironclaude-1",
        data["wake_id"],
        True,
    )
    e = tmp_state.load().entries[K5]
    assert (e.state, e.orchestrator, e.wake_id, e.wake_attempts) == (
        "woken",
        "ironclaude-1",
        data["wake_id"],
        1,
    )
    assert decisions(res) == [("woken", K5, "woken")]
    assert (
        json.loads((orch_dir(world.config) / "orchestrators.json").read_text())[
            "ironclaude-1"
        ]["repo"]
        == REPO_A
    )


def test_four_issues_of_one_repo_give_two_wakes_three_and_one(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    for n in (1, 2, 3, 4):
        world.issue(REPO_A, n)
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker)
    by_orch = {}
    for path in wake_files(world.config):
        d = read_wake(path)
        by_orch[d["target"]["orchestrator"]] = [i["number"] for i in d["assigned"]]
        assert d["target"]["tag"] == f"orchestrator-{d['target']['orchestrator']}"
    assert by_orch == {"ironclaude-1": [1, 2, 3], "ironclaude-2": [4]}
    assert sorted(t.orchestrator for t, _, _ in waker.deliveries) == [
        "ironclaude-1",
        "ironclaude-2",
    ]
    assert {e.orchestrator for e in tmp_state.load().entries.values()} == {
        "ironclaude-1",
        "ironclaude-2",
    }


def test_a_repo_with_max_in_flight_1_and_two_issues_starts_two_orchestrators(
    tmp_path, tmp_state, gh_world
):
    config = make_config(tmp_path)
    write_repos(
        config.orchestrator_repo,
        repos=[
            {
                "repo": REPO_A,
                "enabled": True,
                "checkout": str(tmp_path / "checkouts" / "IronClaude"),
                "max_in_flight": 1,
            }
        ],
    )
    world = gh_world(config=config)
    world.issue(REPO_A, 1)
    world.issue(REPO_A, 2)
    run(world, tmp_path, tmp_state)
    assert sorted(
        json.loads((orch_dir(config) / "orchestrators.json").read_text())
    ) == ["ironclaude-1", "ironclaude-2"]


def test_a_second_cycle_sends_nothing_for_an_issue_that_is_already_woken(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    run(world, tmp_path, tmp_state)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker, advance=300)
    assert (
        res.exit_code == 0
        and waker.deliveries == []
        and len(wake_files(world.config)) == 1
    )


def test_issues_of_two_repos_go_to_their_own_orchestrators_with_a_per_repo_origin_check(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 1)
    world.issue(REPO_B, 2)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert res.exit_code == 0
    targets = {}
    for path in wake_files(world.config):
        d = read_wake(path)
        targets[d["target"]["repo"]] = (
            d["target"]["orchestrator"],
            d["assigned"][0]["checkout_state"],
        )
    assert targets == {REPO_A: ("ironclaude-1", "ok"), REPO_B: ("example-1", "missing")}
    # the checkout of the first repo is asked for its own origin, once
    assert [
        a
        for a in world.runner.argvs("git")
        if a[-3:] == ("remote", "get-url", "origin")
    ].__len__() == 1


# --- the filters (4.5 step 8) -----------------------------------------------------------------------------


def test_a_co_assigned_issue_is_skipped_and_not_recorded(tmp_path, tmp_state, gh_world):
    world = gh_world()
    world.issue(REPO_A, 5, assignees=["owner-login", "someone-else"])
    res = run(world, tmp_path, tmp_state)
    assert (
        decisions(res) == [("assigned_other", K5, None)]
        and wake_files(world.config) == []
    )
    assert K5 not in tmp_state.load().entries  # re-examined while the co-assignee stays


def test_an_unlisted_or_disabled_repo_is_recorded_as_seen_and_named_in_the_next_wake(
    tmp_path, tmp_state, gh_world
):
    config = make_config(tmp_path)
    write_repos(
        config.orchestrator_repo,
        repos=[
            {
                "repo": REPO_A,
                "enabled": True,
                "checkout": str(tmp_path / "checkouts" / "IronClaude"),
            },
            {"repo": "IronbellyOrg/Off", "enabled": False, "checkout": None},
        ],
    )
    world = gh_world(config=config)
    world.issue("IronbellyOrg/Coder", 477)
    world.issue("IronbellyOrg/Off", 3)
    world.issue(REPO_A, 5)
    res = run(world, tmp_path, tmp_state)
    assert ("repo_not_listed", "IronbellyOrg/Coder#477", None) in decisions(res)
    assert ("repo_disabled", "IronbellyOrg/Off#3", None) in decisions(res)
    entries = tmp_state.load().entries
    assert entries["IronbellyOrg/Coder#477"].ack_reason == "repo_not_listed"
    assert entries["IronbellyOrg/Off#3"].state == "acked"
    skipped = read_wake(wake_files(config)[0])["skipped"]
    assert {(s["repo"], s["number"], s["reason"]) for s in skipped} == {
        ("IronbellyOrg/Coder", 477, "repo_not_listed"),
        ("IronbellyOrg/Off", 3, "repo_disabled"),
    }
    again = run(world, tmp_path, tmp_state, advance=300)
    assert [
        d for d in decisions(again) if d[0].startswith("repo_")
    ] == []  # seen: not examined again


def test_a_pull_request_row_and_a_closed_issue_are_never_candidates(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5, pull_request=True)
    world.issue(REPO_A, 6, state="closed")
    assert run(world, tmp_path, tmp_state).woken == ()


def test_the_day_cap_stops_a_seventh_new_issue(tmp_path, tmp_state, gh_world):
    config = make_config(tmp_path)
    write_repos(
        config.orchestrator_repo,
        repos=[
            {
                "repo": REPO_A,
                "enabled": True,
                "checkout": str(tmp_path / "checkouts" / "IronClaude"),
                "max_in_flight": 10,
            }
        ],
    )
    world = gh_world(config=config)
    for n in range(1, 9):
        world.issue(REPO_A, n)
    res = run(world, tmp_path, tmp_state)
    assert len(res.woken) == cycle.DAY_CAP == 6
    assert [d[1] for d in decisions(res) if d[0] == "day_cap"] == [
        f"{REPO_A}#7",
        f"{REPO_A}#8",
    ]
    doc = tmp_state.load()
    for key in res.woken:  # acknowledged, so nothing is sent again
        doc = record.mark_acked(doc, key, world.clock.now())
    tmp_state.save(doc)
    nxt = run(world, tmp_path, tmp_state, advance=24 * 3600 + 60)
    assert nxt.woken == (f"{REPO_A}#7", f"{REPO_A}#8")  # the window moved on


def test_at_most_ten_candidates_a_cycle(tmp_path, tmp_state, gh_world):
    config = make_config(tmp_path)
    write_repos(
        config.orchestrator_repo,
        repos=[
            {
                "repo": REPO_A,
                "enabled": True,
                "checkout": str(tmp_path / "checkouts" / "IronClaude"),
                "max_in_flight": 10,
            }
        ],
    )
    world = gh_world(config=config)
    for n in range(1, 15):
        world.issue(REPO_A, n)
    # lift the day cap so only the candidate cap acts
    old = cycle.DAY_CAP
    cycle.DAY_CAP = 99
    try:
        res = run(world, tmp_path, tmp_state)
    finally:
        cycle.DAY_CAP = old
    assert len(res.woken) == 10


# --- the baseline (4.3 rule 5) ----------------------------------------------------------------------------


def test_the_first_cycle_records_the_assigned_issues_as_seen_and_wakes_nobody(
    tmp_path, tmp_state, gh_world
):
    store = record.init_state(tmp_path / "state2", FIXED_NOW, baseline=True)
    config = make_config(tmp_path, state_dir=tmp_path / "state2")
    world = gh_world(config=config)
    world.issue(REPO_A, 5)
    world.issue(REPO_A, 6, assignees=["owner-login", "x"])
    world.info["mentions"].append(
        {"repo": REPO_B, "number": 12, "kind": "issue", "updated_at": CYCLE_NOW}
    )
    waker = FakeWaker()
    res = cycle.run_cycle(world.deps(tmp_path, store, waker=waker), False)
    assert res.exit_code == 0 and waker.deliveries == [] and wake_files(config) == []
    doc = store.load()
    assert doc.baseline is False and {e.ack_reason for e in doc.entries.values()} == {
        "baseline"
    }
    assert set(doc.entries) == {K5, f"{REPO_A}#6"} and len(doc.info_seen) == 1
    world.issue(REPO_A, 7)
    later = cycle.run_cycle(world.deps(tmp_path, store, waker=waker), False)
    assert later.woken == (f"{REPO_A}#7",)


def test_no_baseline_wakes_every_assigned_issue(tmp_path, gh_world):
    store = record.init_state(tmp_path / "state3", FIXED_NOW, baseline=False)
    config = make_config(tmp_path, state_dir=tmp_path / "state3")
    world = gh_world(config=config)
    world.issue(REPO_A, 5)
    assert cycle.run_cycle(world.deps(tmp_path, store), False).woken == (K5,)


# --- the information streams ---------------------------------------------------------------------------------


def test_new_information_rides_with_a_wake_and_is_marked_seen(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    world.info["mentions"].append(
        {"repo": REPO_B, "number": 12, "kind": "issue", "updated_at": CYCLE_NOW}
    )
    world.info["affects"].append(
        {
            "repo": REPO_A,
            "number": 40,
            "pull_request": True,
            "kind": "pull_request",
            "updated_at": CYCLE_NOW,
        }
    )
    world.info["could_assign"].append(
        {
            "repo": "IronbellyOrg/Unlisted",
            "number": 1,
            "kind": "issue",
            "updated_at": CYCLE_NOW,
        }
    )
    run(world, tmp_path, tmp_state)
    d = read_wake(wake_files(world.config)[0])
    assert [(i["repo"], i["number"], i["kind"]) for i in d["info"]["mentions"]] == [
        (REPO_B, 12, "issue")
    ]
    assert [(i["number"], i["kind"]) for i in d["info"]["affects"]] == [
        (40, "pull_request")
    ]
    assert d["info"]["could_assign"] == []  # S3 is kept only for repos in the list
    assert len(tmp_state.load().info_seen) == 2
    again = run(world, tmp_path, tmp_state, advance=300)
    assert len(wake_files(world.config)) == 1 and again.woken == ()  # seen: not new


def test_only_the_information_a_wake_carries_is_marked_seen(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    total = wake.MAX_INFO + 3
    for n in range(100, 100 + total):
        world.info["mentions"].append(
            {"repo": REPO_B, "number": n, "kind": "issue", "updated_at": CYCLE_NOW}
        )
    run(world, tmp_path, tmp_state)
    d = read_wake(wake_files(world.config)[0])
    assert len(d["info"]["mentions"]) == wake.MAX_INFO
    # the three items cut from the wake stay eligible for a later one
    assert len(tmp_state.load().info_seen) == wake.MAX_INFO


def test_information_alone_goes_to_an_active_orchestrator_and_starts_no_session(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    write_registry(world.config, {"ironclaude-1": {}})
    write_run(world.config, "ironclaude-1", run_id="run_9")
    world.info["mentions"].append(
        {"repo": REPO_B, "number": 12, "kind": "issue", "updated_at": CYCLE_NOW}
    )
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker)
    ((target, wake_id, start),) = waker.deliveries
    assert (target.orchestrator, target.run_id, start) == (
        "ironclaude-1",
        "run_9",
        False,
    )
    assert read_wake(wake_files(world.config)[0])["assigned"] == []
    assert len(tmp_state.load().info_seen) == 1


def test_information_alone_with_no_orchestrator_is_not_worth_a_session(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.info["mentions"].append(
        {"repo": REPO_B, "number": 12, "kind": "issue", "updated_at": CYCLE_NOW}
    )
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker)
    assert (
        waker.deliveries == []
        and wake_files(world.config) == []
        and world.runner.argvs("orca") == []
    )


# --- acknowledgments, resend, abandon (3.6, 4.3 rule 4) --------------------------------------------------------------


def woken_issue(tmp_path, tmp_state, gh_world, n=5):
    world = gh_world()
    world.issue(REPO_A, n)
    run(world, tmp_path, tmp_state)
    wake_id = read_wake(wake_files(world.config)[0])["wake_id"]
    return world, wake_id


def test_a_taken_acknowledgment_moves_the_entry_to_acked_and_the_files_to_done(
    tmp_path, tmp_state, gh_world
):
    world, wake_id = woken_issue(tmp_path, tmp_state, gh_world)
    write_ack(world.config, wake_id, taken=[(REPO_A, 5)])
    res = run(world, tmp_path, tmp_state, advance=300)
    e = tmp_state.load().entries[K5]
    assert (e.state, e.ack_reason) == ("acked", None)
    assert ("acked", K5, "acked") in decisions(res)
    wakes = world.config.orchestrator_repo / ".orchestrator" / "wakes"
    assert (
        not (wakes / f"{wake_id}.json").exists()
        and (wakes / "done" / f"{wake_id}.json").exists()
    )
    assert (wakes / "done" / f"{wake_id}.ack.json").exists()


def test_the_acknowledgment_is_saved_before_its_files_move_to_done(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world, wake_id = woken_issue(tmp_path, tmp_state, gh_world)
    write_ack(world.config, wake_id, taken=[(REPO_A, 5)])
    seen = []
    real = wake.move_to_done

    def spy(repo, wid):
        seen.append(tmp_state.load().entries[K5].state)  # what a crash here would keep
        real(repo, wid)

    monkeypatch.setattr(wake, "move_to_done", spy)
    run(world, tmp_path, tmp_state, advance=300)
    assert seen == ["acked"]


def test_a_skipped_acknowledgment_stores_its_free_reason_and_wakes_nobody_again(
    tmp_path, tmp_state, gh_world
):
    world, wake_id = woken_issue(tmp_path, tmp_state, gh_world)
    write_ack(world.config, wake_id, skipped=[(REPO_A, 5, "claimed_elsewhere")])
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker, advance=300)
    assert tmp_state.load().entries[K5].ack_reason == "claimed_elsewhere"
    run(world, tmp_path, tmp_state, waker=waker, advance=1200)
    assert waker.deliveries == []  # not resent after 10 minutes either


def test_a_rejected_item_is_acked_as_malformed_and_an_unlisted_entry_stays_woken(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    world.issue(REPO_A, 6)
    run(world, tmp_path, tmp_state)
    wake_id = read_wake(wake_files(world.config)[0])["wake_id"]
    write_ack(world.config, wake_id, taken=[(REPO_A, 5)], rejected=[])
    run(world, tmp_path, tmp_state, advance=300)
    entries = tmp_state.load().entries
    assert (
        entries[K5].state == "acked" and entries[f"{REPO_A}#6"].state == "woken"
    )  # in none of the lists
    wakes = world.config.orchestrator_repo / ".orchestrator" / "wakes"
    assert (
        wakes / f"{wake_id}.json"
    ).exists()  # the wake stays until every item is decided
    write_ack(world.config, wake_id, taken=[(REPO_A, 5)], rejected=[1])
    run(world, tmp_path, tmp_state, advance=300)
    assert tmp_state.load().entries[f"{REPO_A}#6"].ack_reason == "malformed_item"


def test_an_unreadable_acknowledgment_changes_nothing(tmp_path, tmp_state, gh_world):
    world, wake_id = woken_issue(tmp_path, tmp_state, gh_world)
    (orch_dir(world.config) / "wakes" / f"{wake_id}.ack.json").write_text("{bad")
    run(world, tmp_path, tmp_state, advance=300)
    assert tmp_state.load().entries[K5].state == "woken"


def test_an_unacknowledged_wake_is_sent_again_after_ten_minutes_to_the_same_orchestrator(
    tmp_path, tmp_state, gh_world
):
    world, first_id = woken_issue(tmp_path, tmp_state, gh_world)
    waker = FakeWaker()
    quiet = run(world, tmp_path, tmp_state, waker=waker, advance=540)
    assert waker.deliveries == [] and quiet.exit_code == 0
    res = run(world, tmp_path, tmp_state, waker=waker, advance=61)
    ((target, second_id, _),) = waker.deliveries
    assert target.orchestrator == "ironclaude-1" and second_id != first_id
    assert len(wake_files(world.config)) == 2
    d = read_wake([p for p in wake_files(world.config) if p.stem == second_id][0])
    assert d["attempt"] == 2 and d["target"]["orchestrator"] == "ironclaude-1"
    assert [i["number"] for i in d["assigned"]] == [5]
    e = tmp_state.load().entries[K5]
    assert (e.state, e.wake_id, e.wake_attempts) == ("woken", second_id, 2)
    assert reasons(res) == ["woken"]
    assert res.exit_code == 0


def test_a_resend_for_a_repo_removed_from_repos_yaml_is_skipped_not_a_crash(
    tmp_path, tmp_state, gh_world
):
    world, _ = woken_issue(tmp_path, tmp_state, gh_world)
    write_repos(
        world.config.orchestrator_repo,
        repos=[{"repo": REPO_B, "enabled": True, "checkout": None, "clone_parent": str(tmp_path)}],
    )  # fmt: skip
    waker = FakeWaker()
    run(world, tmp_path, tmp_state, waker=waker, advance=601)  # must not raise
    assert waker.deliveries == []
    assert tmp_state.load().entries[K5].state in ("pending", "woken")  # not acked


def test_the_third_unacknowledged_attempt_abandons_the_entry_exit_7_and_marks_unread(
    tmp_path, tmp_state, gh_world
):
    world, _ = woken_issue(tmp_path, tmp_state, gh_world)
    waker = FakeWaker()
    for _ in range(2):  # attempts 2 and 3
        run(world, tmp_path, tmp_state, waker=waker, advance=601)
    assert tmp_state.load().entries[K5].wake_attempts == 3
    res = run(world, tmp_path, tmp_state, waker=waker, advance=601)
    e = tmp_state.load().entries[K5]
    assert (e.state, e.last_reason) == ("abandoned", "ack_not_observed")
    assert (res.exit_code, res.reason) == (7, "ack_not_observed")
    assert waker.unread == ["ack_not_observed"]
    assert len(waker.deliveries) == 2  # never a fourth try
    after = run(world, tmp_path, tmp_state, waker=waker, advance=601)
    assert after.exit_code == 0 and len(waker.deliveries) == 2


def test_three_failed_preparations_end_abandoned_attempts_exhausted_exit_7(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    world.fail("reread", "transient", key=(REPO_A, 5), times=None)
    waker = FakeWaker()
    codes = []
    for _ in range(3):
        res = run(world, tmp_path, tmp_state, waker=waker, advance=601)
        codes.append((res.exit_code, res.reason))
    e = tmp_state.load().entries[K5]
    assert (e.state, e.last_reason, e.attempts) == (
        "abandoned",
        "attempts_exhausted",
        3,
    )
    assert codes == [(7, "revalidation_transient")] * 2 + [
        (7, "revalidation_transient")
    ]
    assert (
        decisions(res)[-1] == ("attempts_exhausted", K5, "abandoned")
        and waker.deliveries == []
    )
    assert (
        waker.unread == ["revalidation_transient"] or waker.unread == []
    )  # only the named reasons mark it


def test_a_failed_entry_is_examined_again_once_its_backoff_has_elapsed(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    world.fail("reread", "transient", key=(REPO_A, 5), times=1)
    run(world, tmp_path, tmp_state)
    assert tmp_state.load().entries[K5].state == "failed"
    held_back = run(world, tmp_path, tmp_state, advance=300)
    assert decisions(held_back) == [("in_backoff", K5, None)]
    res = run(world, tmp_path, tmp_state, advance=400)
    assert res.woken == (K5,)  # F21 of issue 665: re-examined after its backoff


# --- delivery outcomes -----------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("outcome", "state", "reason", "unread"),
    [
        (
            wake.WakeOutcome("unknown", "busy", "unavailable"),
            "unknown",
            "wake_unknown",
            [],
        ),
        (
            wake.WakeOutcome("no_session", "no_tier"),
            "unknown",
            "no_session",
            ["no_session"],
        ),
        (
            wake.WakeOutcome("spawn_error", "spawn_error"),
            "abandoned",
            "spawn_error",
            [],
        ),
    ],
)
def test_a_failed_delivery_is_recorded_and_exits_7(
    tmp_path, tmp_state, gh_world, outcome, state, reason, unread
):
    world = gh_world()
    world.issue(REPO_A, 5)
    waker = FakeWaker(outcome)
    res = run(world, tmp_path, tmp_state, waker=waker)
    e = tmp_state.load().entries[K5]
    assert (e.state, e.last_reason) == (state, reason)
    assert (res.exit_code, res.reason) == (7, reason) and res.woken == ()
    assert waker.unread == unread
    if outcome.mailbox == "unavailable":
        assert "mailbox_unavailable" in reasons(res)


def test_a_started_session_records_its_tier_in_the_registry(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    out = wake.WakeOutcome(
        "woken",
        "typed",
        "skipped",
        typed=True,
        started=True,
        tier="tier2",
        fallback_from="tier1b",
        stages=("input_accepted", "turn_started"),
    )
    res = run(world, tmp_path, tmp_state, waker=FakeWaker(out))
    reg = json.loads((orch_dir(world.config) / "orchestrators.json").read_text())[
        "ironclaude-1"
    ]
    assert (reg["tier"], reg["fallback_from"]) == ("tier2", "tier1b")
    line = next(ln for ln in res.lines if ln["reason"] == "woken")
    assert line["stages"] == "input_accepted,turn_started"


def test_without_orca_nothing_is_saved_pending_and_the_cycle_stops_orca_not_found(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    res = run(world, tmp_path, tmp_state, which=lambda name: None)
    assert (res.exit_code, res.reason) == (2, "orca_not_found")
    assert K5 not in tmp_state.load().entries and wake_files(world.config) == []


def test_a_wake_file_that_cannot_be_written_is_exit_6_and_the_entry_stays_pending(
    tmp_path, tmp_state, gh_world, monkeypatch
):
    world = gh_world()
    world.issue(REPO_A, 5)

    def boom(*a, **k):
        raise wake.WakeError("disk")

    monkeypatch.setattr(wake, "write_wake_file", boom)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert (res.exit_code, res.reason) == (
        6,
        "wake_write_failed",
    ) and waker.deliveries == []
    assert (
        tmp_state.load().entries[K5].state == "pending"
    )  # found next cycle as a resend


def test_the_poll_never_sends_a_held_issue_as_an_assignment(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5, body=EMPTY_BODY)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert res.woken == () and waker.deliveries == [] and wake_files(world.config) == []


# --- the per-repo origin check and the checkout (4.4) -----------------------------------------------------------------------


def test_a_checkout_whose_origin_names_another_repo_skips_its_issues_with_exit_2(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    world.origins[REPO_A] = "https://github.com/example-org/other-repo.git"
    res = run(world, tmp_path, tmp_state)
    assert (res.exit_code, res.reason) == (2, "origin_mismatch")
    assert ("origin_mismatch", K5, None) in decisions(res) and wake_files(
        world.config
    ) == []
    assert K5 not in tmp_state.load().entries  # retried when the checkout is fixed


def test_a_repo_with_no_checkout_and_no_clone_parent_is_skipped_checkout_missing_and_seen(
    tmp_path, tmp_state, gh_world
):
    config = make_config(tmp_path)
    write_repos(
        config.orchestrator_repo,
        repos=[{"repo": REPO_A, "enabled": True, "checkout": None}],
    )
    world = gh_world(config=config)
    world.issue(REPO_A, 5)
    res = run(world, tmp_path, tmp_state)
    assert ("checkout_missing", K5, None) in decisions(res)
    assert tmp_state.load().entries[K5].ack_reason == "checkout_missing"


# --- re-read, rate limits, stops -----------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "change",
    [
        {"state": "closed"},
        {"assignees": ["owner-login", "other"]},
        {"assignees": []},
        {"body": EMPTY_BODY},
        {"labels": ["hold:backlog"]},
        {"labels": ["hold:plan"]},
    ],
)
def test_a_candidate_that_changed_since_the_search_is_not_woken(
    tmp_path, tmp_state, gh_world, change
):
    world = gh_world()
    item = world.issue(REPO_A, 5)

    def flip():
        for k, v in change.items():
            setattr(item, k, v)

    world.on("reread", flip, key=(REPO_A, 5))
    res = run(world, tmp_path, tmp_state, waker=(waker := FakeWaker()))
    assert res.woken == () and waker.deliveries == []
    assert K5 not in tmp_state.load().entries


def test_the_reread_names_the_issues_own_repo(tmp_path, tmp_state, gh_world):
    world = gh_world()
    world.issue(REPO_B, 9)
    run(world, tmp_path, tmp_state)
    rereads = [a for a in world.gh_argvs if "issues/9" in " ".join(a)]
    assert rereads and all(REPO_B in " ".join(a) for a in rereads)


def test_a_rate_limit_with_a_header_waits_that_long_and_the_next_cycle_stops(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.fail("user", "rate", times=1)
    res = run(world, tmp_path, tmp_state)
    assert (res.exit_code, res.reason) == (5, "rate_limited")
    doc = tmp_state.load()
    assert (
        doc.next_permitted_at == CYCLE_NOW + timedelta(seconds=120)
        and doc.rate_streak == 1
    )
    waiting = run(world, tmp_path, tmp_state, advance=60)
    assert (waiting.exit_code, waiting.reason) == (5, "rate_limited") and world.count(
        "user"
    ) == 1
    assert tmp_state.load().rate_streak == 1  # no request was made: the streak stands
    resumed = run(world, tmp_path, tmp_state, advance=61)
    assert (
        resumed.exit_code == 0 and tmp_state.load().rate_streak == 0
    )  # reset by a clean cycle


def test_a_rate_limit_with_no_header_backs_off_exponentially_to_an_hour(
    tmp_path, tmp_state, gh_world
):
    assert [cycle.rate_wait_seconds(n) for n in range(0, 7)] == [
        300,
        300,
        600,
        1200,
        2400,
        3600,
        3600,
    ]
    world = gh_world()
    world.fail("search", "rate", key="IronbellyOrg", times=None)
    waits = []
    for _ in range(5):
        res = run(world, tmp_path, tmp_state, advance=3601)
        assert (res.exit_code, res.reason) == (5, "rate_limit_clamped")
        doc = tmp_state.load()
        waits.append(int((doc.next_permitted_at - world.clock.now()).total_seconds()))
    assert waits == [300, 600, 1200, 2400, 3600] and doc.rate_streak == 5


@pytest.mark.parametrize(
    ("call", "how", "reason", "code"),
    [
        ("user", "auth", "gh_auth_failed", 3),
        ("user", "timeout", "gh_timeout", 3),
        ("search", "non_json", "gh_non_json", 3),
        ("info", "timeout", "gh_timeout", 3),
    ],
)
def test_shared_read_failures_stop_the_cycle_with_their_reason(
    tmp_path, tmp_state, gh_world, call, how, reason, code
):
    world = gh_world()
    world.fail(call, how, times=None)
    res = run(world, tmp_path, tmp_state)
    assert (res.exit_code, res.reason) == (code, reason)


def test_a_search_with_a_hundred_rows_stops_the_cycle_truncated(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    for n in range(1, 101):
        world.issue(REPO_A, n)
    res = run(world, tmp_path, tmp_state)
    assert (res.exit_code, res.reason) == (4, "truncated") and res.woken == ()


def test_the_account_id_check_the_kill_switch_and_the_enabled_flag(
    tmp_path, tmp_state, gh_world
):
    world = gh_world(config=make_config(tmp_path, owner_account_id=OWN_ID + 1))
    assert run(world, tmp_path, tmp_state).reason == "account_id_mismatch"
    world = gh_world(config=make_config(tmp_path, enabled=False))
    assert run(world, tmp_path, tmp_state).reason == "not_enabled"
    assert (
        run(world, tmp_path, tmp_state, dry_run=True).reason == "cycle_complete"
    )  # a dry run ignores it
    (tmp_state.state_dir / "DISABLED").write_text("")
    assert run(gh_world(), tmp_path, tmp_state).reason == "disabled"


def test_a_bad_repos_file_stops_the_cycle_with_exit_2(tmp_path, tmp_state, gh_world):
    world = gh_world()
    (world.config.orchestrator_repo / "repos.yaml").write_text("schema_version: 9\n")
    assert (
        run(world, tmp_path, tmp_state).exit_code,
        run(world, tmp_path, tmp_state).reason,
    ) == (2, "repos_invalid")
    world = gh_world(config=make_config(tmp_path, orchestrator_repo=tmp_path / "nope"))
    assert run(world, tmp_path, tmp_state).reason == "orchestrator_repo_invalid"


def test_a_clock_that_runs_far_from_the_server_time_is_a_warning(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.skew_s = 120
    res = run(world, tmp_path, tmp_state)
    assert "clock_skew" in reasons(res) and res.lines[-1]["clock_skew_s"] == 120


def test_a_second_cycle_while_one_holds_the_lock_exits_75(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    with tmp_state.lock():
        res = run(world, tmp_path, tmp_state, store=FileStore(tmp_state.state_dir))
    assert (res.exit_code, res.reason) == (75, "lock_held")


def test_every_audit_line_is_closed_and_free_of_issue_text(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5, title="PWNED-TITLE", body=GOOD_BODY + "PWNED-BODY")
    res = run(world, tmp_path, tmp_state)
    text = (tmp_state.state_dir / "audit.jsonl").read_text()
    assert "PWNED" not in text and "PWNED" not in json.dumps(res.lines)
    assert all(
        ln["reason"]
        in __import__("superclaude.cli.issue_watch.audit", fromlist=["x"]).REASONS
        for ln in res.lines
    )


def test_a_dry_run_writes_no_wake_file_no_registry_no_orca_call_and_no_store(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    before = (tmp_state.state_dir / "dispatch.json").read_bytes()
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker, dry_run=True)
    assert res.would_wake == (K5,) and res.woken == ()
    assert (
        decisions(res)[0][0] == "woken"
        and res.lines[0]["dry_run"] is True
        and "state" not in res.lines[0]
    )
    assert wake_files(world.config) == [] and waker.deliveries == []
    assert (
        world.runner.argvs("orca") == []
        and not (world.config.orchestrator_repo / ".orchestrator").exists()
    )
    assert (tmp_state.state_dir / "dispatch.json").read_bytes() == before
    again = run(
        world, tmp_path, tmp_state, dry_run=True, advance=300
    )  # the shadow remembers it
    assert again.would_wake == ()
    assert (tmp_state.state_dir / "dry-run.json").exists()


def test_a_dry_run_ignores_a_damaged_shadow_with_a_warning(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    (tmp_state.state_dir / "dry-run.json").write_text("{bad")
    res = run(world, tmp_path, tmp_state, dry_run=True)
    assert "dry_run_shadow_reset" in reasons(res)


def test_the_state_directory_failing_to_write_is_exit_6(tmp_path, tmp_state, gh_world):
    from .conftest import FailingStore

    world = gh_world()
    world.issue(REPO_A, 5)
    store = FailingStore(tmp_state, fail_saves=(1,))
    res = run(world, tmp_path, tmp_state, store=store)
    assert (res.exit_code, res.reason) == (6, "state_dir_unwritable")


def test_status_report_has_no_retry_and_lists_wake_counts(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    run(world, tmp_path, tmp_state)
    report = cycle.status_report(tmp_state, None, world.clock.now())
    assert (
        "retry" not in report
        and report["counts"] == {"woken": 1}
        and report["healthy"] is True
    )
    assert report["held"] == [] and report["baseline_pending"] is False
    assert "orca" not in json.dumps(report)


def test_check_config_preview_shows_what_each_orchestrator_holds(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    for n in (1, 2, 3, 4):
        world.issue(REPO_A, n)
    run(world, tmp_path, tmp_state)
    rdoc = cycle.validate_setup(world.config, world.runner)
    rows = cycle.routing_preview(world.config, rdoc, tmp_state, world.clock.now())
    mine = next(r for r in rows if r["repo"] == REPO_A)
    assert [(o["id"], o["in_flight"]) for o in mine["orchestrators"]] == [
        ("ironclaude-1", 3),
        ("ironclaude-2", 1),
    ]
    assert mine["next_issue_goes_to"] == "ironclaude-2"
    other = next(r for r in rows if r["repo"] == REPO_B)
    assert other["next_issue_goes_to"] == "a new example-1" and isinstance(
        world, GhWorld
    )
