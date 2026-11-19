"""The hold and the acceptance check on issues (design 4.11): ``plan_check``, the decision table, the quiet hour."""

from __future__ import annotations

import json
from datetime import timedelta

import pytest

from superclaude.cli.issue_watch import cycle, hold, record, wake
from superclaude.cli.issue_watch.hold import plan_check, table_row
from superclaude.cli.issue_watch.record import Hold

from .conftest import (
    CYCLE_NOW,
    EMPTY_BODY,
    GOOD_BODY,
    REPO_A,
    FakeWaker,
    decisions,
    load_fixture,
    make_config,
    orch_dir,
    read_wake,
    reasons,
    result,
    run,
    wake_files,
    write_plan_record,
    write_registry,
    write_repos,
    write_run,
    write_state_file,
)

K5 = f"{REPO_A}#5"
ALL_MISSING = ("priority", "fix_approach", "test_plan")


# --- plan_check ------------------------------------------------------------------------------------


def body(priority="P2", fix="Change the poll.", test="Run the tests."):
    parts = []
    for heading, text in (
        ("Priority", priority),
        ("Fix approach", fix),
        ("Test plan", test),
    ):
        if text is not None:
            parts.append(f"## {heading}\n{text}\n")
    return "\n".join(parts)


def test_all_three_sections_pass():
    check = plan_check(GOOD_BODY)
    assert (check.ok, check.missing) == (True, ())


@pytest.mark.parametrize(
    ("token", "slot"),
    [("priority", "priority"), ("fix_approach", "fix"), ("test_plan", "test")],
)
@pytest.mark.parametrize(
    "bad",
    [
        None,  # the heading is removed
        "",  # emptied
        "   \n\n",
        "Not known yet",
        "not known yet",
        "NOT KNOWN YET",
        "<!-- sc:issue:create round=1 -->",  # only an HTML comment
        "<!-- a\nmultiline comment -->\n",
        "<!-- never closed",
    ],
)
def test_each_section_that_is_absent_empty_unknown_or_a_comment_gives_its_token(
    token, slot, bad
):
    check = plan_check(body(**{slot: bad}))
    assert (check.ok, check.missing) == (False, (token,))


@pytest.mark.parametrize(
    ("token", "heading"),
    [
        ("priority", "Priority"),
        ("fix_approach", "Fix approach"),
        ("test_plan", "Test plan"),
    ],
)
def test_a_heading_written_twice_gives_its_token_even_when_both_are_filled(
    token, heading
):
    doubled = GOOD_BODY + f"\n## {heading}\nAnother text.\n"
    assert plan_check(doubled).missing == (token,)


def test_the_tokens_come_in_the_fixed_order_and_a_body_that_is_not_text_counts_as_empty():
    assert plan_check(EMPTY_BODY).missing == ALL_MISSING
    assert plan_check(None).missing == ALL_MISSING
    assert plan_check("").ok is False and plan_check(5).missing == ALL_MISSING
    assert plan_check(body(priority=None, test=None)).missing == (
        "priority",
        "test_plan",
    )


def test_a_section_ends_at_the_next_heading_and_at_the_hidden_create_marker():
    text = "## Priority\nP2\n\n## Fix approach\n\n## Test plan\nRun it.\n"  # the middle section is empty: the next heading ends it
    assert plan_check(text).missing == ("fix_approach",)
    # finding F17 of issue 675: text after the create marker is not part of the section
    marked = "## Priority\nP2\n## Fix approach\nDo it.\n## Test plan\n<!-- sc:issue:create round=1 -->\nstray text\n"
    assert plan_check(marked).missing == ("test_plan",)
    assert plan_check(
        marked.replace("<!-- sc:issue:create round=1 -->\n", "")
    ).ok  # without the marker the text counts
    # an h3 inside a section does not end it
    assert plan_check(
        "## Priority\n### Detail\nP2\n## Fix approach\nx\n## Test plan\ny\n"
    ).ok


def test_a_mutation_removing_a_heading_from_a_copy_turns_the_check_red():
    """The style of ``test_marker_check_fails_when_marker_is_removed``."""
    assert plan_check(GOOD_BODY).ok
    for heading in ("## Priority", "## Fix approach", "## Test plan"):
        assert not plan_check(GOOD_BODY.replace(heading, "## Other")).ok
    assert not plan_check(
        GOOD_BODY.replace("## Priority", "## priority")
    ).ok  # read as written


def test_the_labels_are_constants_not_settings():
    assert (hold.HOLD_LABEL, hold.BACKLOG_LABEL) == ("hold:plan", "hold:backlog")
    assert (hold.HOLD_QUIET_MINUTES, hold.PLAN_CALL_MAX_MINUTES) == (60, 60)


# --- the pure parts -----------------------------------------------------------------------------------


def a_hold(**over) -> Hold:
    return Hold(**{"state": "held", "first_held_at": CYCLE_NOW, **over})


@pytest.mark.parametrize(
    ("backlog", "passes", "label", "entry", "row"),
    [
        (True, True, True, None, 1),
        (True, False, False, a_hold(), 1),
        (False, True, False, None, 2),
        (
            False,
            True,
            False,
            a_hold(),
            2,
        ),  # finding F1 of issue 665: a passing issue is clear
        (False, True, True, None, 3),
        (False, True, True, a_hold(state="hand_removed"), 3),
        (False, False, False, None, 4),
        (False, False, False, a_hold(), 5),
        (False, False, False, a_hold(state="hand_removed"), 5),
        (False, False, True, None, 6),
        (False, False, True, a_hold(), 6),
    ],
)
def test_the_decision_table_picks_one_of_six_rows(backlog, passes, label, entry, row):
    assert table_row(backlog=backlog, passes=passes, label=label, entry=entry) == row


def test_the_quiet_clock_is_the_later_of_the_hold_and_the_newest_signal():
    h = a_hold()
    assert hold.quiet_since(h) == CYCLE_NOW
    later = hold.with_evidence(h, CYCLE_NOW + timedelta(minutes=10), "branch")
    assert (
        hold.quiet_since(later) == CYCLE_NOW + timedelta(minutes=10)
        and later.evidence_kind == "branch"
    )
    older = hold.with_evidence(later, CYCLE_NOW + timedelta(minutes=5), "session")
    assert older == later  # an older signal changes nothing
    edit = hold.with_evidence(h, CYCLE_NOW + timedelta(minutes=2), "edit")
    assert edit.seen_updated_at == CYCLE_NOW + timedelta(minutes=2)
    early = hold.with_evidence(
        h, CYCLE_NOW - timedelta(hours=2), "edit"
    )  # before the hold started
    assert hold.quiet_since(early) == CYCLE_NOW


def test_a_request_is_due_after_sixty_minutes_and_only_once_per_hold():
    h = a_hold()
    assert not hold.plan_request_due(h, CYCLE_NOW + timedelta(minutes=59, seconds=59))
    assert hold.plan_request_due(h, CYCLE_NOW + timedelta(minutes=60))
    asked = Hold(
        state="held",
        first_held_at=CYCLE_NOW,
        plan_requested_at=CYCLE_NOW,
        plan_request_orchestrator="x-1",
        plan_request="acked",
    )
    assert not hold.plan_request_due(asked, CYCLE_NOW + timedelta(hours=9))
    assert not hold.plan_request_due(
        a_hold(state="hand_removed"), CYCLE_NOW + timedelta(hours=9)
    )


def test_session_evidence_reads_orca_and_a_failed_read_is_unknown(fake_runner):
    url = "https://github.com/IronbellyOrg/IronClaude/issues/5"
    show = ["/o", "worktree", "show", "--worktree", "issue:5", "--json"]
    find = ["/o", "reference", "find", url, "--json"]
    found = result(
        stdout=json.dumps(load_fixture("orca_worktree_show_found.json")["payload"])
    )
    none = result(
        stdout=json.dumps(load_fixture("orca_worktree_show_none.json")["payload"]),
        returncode=1,
    )
    ref_none = result(
        stdout=json.dumps(load_fixture("orca_reference_find.json")["payload"])
    )
    ref_hit = result(
        stdout=json.dumps({"ok": True, "result": {"matches": [{"id": 1}]}})
    )

    def check(show_reply, ref_reply):
        runner = fake_runner({tuple(show): show_reply, tuple(find): ref_reply})
        return hold.session_evidence(runner, "/o", 5, url, 5)

    assert check(found, ref_none) is True
    assert check(none, ref_hit) is True
    assert check(none, ref_none) is False
    assert (
        check(result(timed_out=True), ref_none) is None
    )  # unreadable: the request waits
    assert check(none, result(stdout="not json")) is None
    assert check(none, result(returncode=1, stderr="boom")) is None
    assert hold.session_evidence(fake_runner(), None, 5, url, 5) is None
    assert hold.session_evidence(fake_runner(), "/o", 5, "not a url", 5) is None


# --- the decision table in the cycle (the writes are asserted exactly) ----------------------------------


def writes(world) -> list[tuple[str, ...]]:
    """Every gh argv that is not a plain read."""
    return [
        a
        for a in world.gh_argvs
        if "POST" in a or "DELETE" in a or "PATCH" in a or "comment" in a
    ]


def held_world(gh_world, **spec):
    world = gh_world()
    world.issue(REPO_A, 5, body=EMPTY_BODY, **spec)
    return world


def test_row_1_backlog_skips_with_nothing_written_read_woken_requested_or_stored(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world, labels=["hold:backlog"])
    waker = FakeWaker()
    for advance in (0, 3600 * 5):  # not even after many hours
        res = run(world, tmp_path, tmp_state, waker=waker, advance=advance)
        assert decisions(res) == [("held_backlog", K5, None)] and res.exit_code == 0
    doc = tmp_state.load()
    assert doc.entries == {} and doc.holds == {}
    assert (
        writes(world) == []
        and waker.deliveries == []
        and wake_files(world.config) == []
    )
    for call in ("develop", "timeline", "labels", "updated", "reread"):
        assert world.count(call) == 0
    assert world.runner.argvs("orca") == []


def test_backlog_wins_over_a_complete_plan_and_over_the_hold_label(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5, labels=["hold:backlog", "hold:plan"])  # a plan, both labels
    res = run(world, tmp_path, tmp_state)
    assert decisions(res) == [("held_backlog", K5, None)] and writes(world) == []


def test_row_2_a_passing_issue_with_no_label_is_woken_as_a_normal_assignment(
    tmp_path, tmp_state, gh_world
):
    world = gh_world()
    world.issue(REPO_A, 5)
    res = run(world, tmp_path, tmp_state)
    assert res.woken == (K5,) and writes(world) == []
    assert tmp_state.load().holds == {}


def test_row_2_drops_a_left_over_entry_when_the_plan_was_filled_and_the_label_taken_off(
    tmp_path, tmp_state, gh_world
):
    """Finding F1 of issue 665: a pass with no label and a ``held`` entry is clear."""
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)  # row 4: held
    item = world.issues[(REPO_A, 5)]
    item.body, item.labels = GOOD_BODY, []
    res = run(world, tmp_path, tmp_state, advance=300)
    assert res.woken == (K5,) and tmp_state.load().holds == {}


def test_row_3_removes_the_label_lifts_the_hold_and_wakes_in_the_next_cycle(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    item = world.issues[(REPO_A, 5)]
    item.body = GOOD_BODY  # somebody (or the plan call) filled it in
    before = len(writes(world))
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker, advance=300)
    assert decisions(res) == [("hold_released", K5, None)] and res.woken == ()
    assert writes(world)[before:] == [
        ("gh", "api", "--method", "DELETE", f"repos/{REPO_A}/issues/5/labels/hold:plan")
    ]
    assert item.labels == [] and tmp_state.load().holds == {} and waker.deliveries == []
    nxt = run(world, tmp_path, tmp_state, waker=waker, advance=300)
    assert nxt.woken == (K5,)  # row 2 applies


def test_a_refused_label_removal_is_hold_write_failed_and_tried_again_next_cycle(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    world.issues[(REPO_A, 5)].body = GOOD_BODY
    world.fail("label_remove", "failed", key=(REPO_A, 5), times=1)
    res = run(world, tmp_path, tmp_state, advance=300)
    assert (
        "hold_write_failed" in reasons(res)
        and res.woken == ()
        and "hold:plan" in world.issues[(REPO_A, 5)].labels
    )
    assert K5 in tmp_state.load().holds  # the entry stays until the label is gone
    again = run(world, tmp_path, tmp_state, advance=300)
    assert decisions(again) == [("hold_released", K5, None)]


def test_row_4_adds_the_label_records_the_hold_and_skips_with_no_comment(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    waker = FakeWaker()
    res = run(world, tmp_path, tmp_state, waker=waker)
    assert decisions(res) == [("hold_applied", K5, None)]
    assert res.woken == () and waker.deliveries == [] and wake_files(world.config) == []
    assert world.issues[(REPO_A, 5)].labels == ["hold:plan"]
    kinds = [a[3] for a in writes(world)]
    assert kinds == ["POST", "POST"]  # create the label (it did not exist), add it
    h = tmp_state.load().holds[K5]
    assert (h.state, h.first_held_at, h.missing) == ("held", CYCLE_NOW, ALL_MISSING)
    assert h.seen_updated_at == CYCLE_NOW  # re-read after the poll's own write
    assert "comment" not in " ".join(" ".join(a) for a in world.gh_argvs)
    assert K5 not in tmp_state.load().entries  # an issue that is held has no entry


def test_the_label_is_created_once_per_repo_and_never_when_it_exists(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    world.existing_labels.add(REPO_A)
    run(world, tmp_path, tmp_state)
    assert (
        world.count("label_create", REPO_A) == 0
        and world.count("label_add", (REPO_A, 5)) == 1
    )


@pytest.mark.parametrize("call", ["label_get", "label_create", "label_add"])
def test_a_refused_label_creation_or_a_403_is_hold_write_failed_and_the_issue_is_skipped(
    tmp_path, tmp_state, gh_world, call
):
    world = held_world(gh_world)
    key = REPO_A if call.startswith("label_") and call != "label_add" else (REPO_A, 5)
    world.fail(call, "failed", key=key, times=None)
    res = run(world, tmp_path, tmp_state)
    assert "hold_write_failed" in reasons(res) and res.woken == ()
    assert (
        K5 not in tmp_state.load().holds
    )  # nothing recorded for a write that did not happen
    assert res.exit_code == 0


def test_without_the_grant_issue_hold_the_poll_writes_nothing(
    tmp_path, tmp_state, gh_world
):
    config = make_config(tmp_path)
    write_repos(config.orchestrator_repo, grants=["issue.assign"])
    world = gh_world(config=config)
    world.issue(REPO_A, 5, body=EMPTY_BODY)
    res = run(world, tmp_path, tmp_state)
    assert (
        "hold_write_failed" in reasons(res) and writes(world) == [] and res.woken == ()
    )


def test_row_5_a_label_taken_off_by_hand_is_confirmed_by_one_live_read_and_never_put_back(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)  # row 4
    item = world.issues[(REPO_A, 5)]
    item.labels.clear()  # a person removes it
    done = len(writes(world))
    waker = FakeWaker()
    first = run(world, tmp_path, tmp_state, waker=waker, advance=300)
    assert decisions(first) == [("hold_removed_by_hand", K5, None)]
    assert world.count("labels", (REPO_A, 5)) == 1  # one live read
    assert tmp_state.load().holds[K5].state == "hand_removed"
    for _ in range(5):  # five more cycles: no write, no read, no wake
        res = run(world, tmp_path, tmp_state, waker=waker, advance=300)
        assert decisions(res) == [("hold_removed_by_hand", K5, None)]
    assert world.count("labels", (REPO_A, 5)) == 1 and len(writes(world)) == done
    assert item.labels == [] and waker.deliveries == [] and res.woken == ()


def test_row_5_a_search_that_shows_the_label_one_cycle_late_is_not_a_removal(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    item = world.issues[(REPO_A, 5)]
    shown = list(item.labels)
    # the search row lacks the label but the live read still has it (the index lags)
    item.labels = []
    world.on("labels", lambda: setattr(item, "labels", shown), key=(REPO_A, 5))
    res = run(world, tmp_path, tmp_state, advance=300)
    assert decisions(res) == [("held_incomplete", K5, None)]
    assert tmp_state.load().holds[K5].state == "held"


def test_row_6_a_label_placed_by_hand_starts_its_hour_now(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world, labels=["hold:plan"])
    run(world, tmp_path, tmp_state, advance=0)
    h = tmp_state.load().holds[K5]
    assert (h.state, h.first_held_at, h.seen_updated_at) == (
        "held",
        CYCLE_NOW,
        world.issues[(REPO_A, 5)].updated_at,
    )
    assert writes(world) == []  # it is already there


def test_a_label_put_back_by_hand_restarts_the_clock_and_clears_the_old_request(
    tmp_path, tmp_state, gh_world
):
    """Finding F20 of issue 675."""
    world = held_world(gh_world, labels=["hold:plan"])
    item = world.issues[(REPO_A, 5)]
    run(world, tmp_path, tmp_state)
    doc = tmp_state.load()
    old = doc.holds[K5]
    tmp_state.save(
        record.set_hold(
            doc,
            K5,
            Hold(
                state="hand_removed", first_held_at=old.first_held_at, plan_requested_at=CYCLE_NOW,
                plan_request_orchestrator="ironclaude-1", plan_request="acked",
                plan_acked_at=CYCLE_NOW, plan_wake_id="20261107T130000Z-00000001", plan_attempts=1,
            ),
        )
    )  # fmt: skip
    assert item.labels == ["hold:plan"]  # a person put it back
    res = run(world, tmp_path, tmp_state, advance=7200)
    h = tmp_state.load().holds[K5]
    assert decisions(res) == [("held_incomplete", K5, None)]
    assert h.state == "held" and h.first_held_at == world.clock.now()
    assert (
        h.plan_requested_at,
        h.plan_request,
        h.plan_request_orchestrator,
        h.plan_wake_id,
        h.plan_attempts,
    ) == (None, None, None, None, 0)


def test_an_issue_that_leaves_s1_and_returns_is_held_afresh(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    item = world.issues[(REPO_A, 5)]
    item.assignees = ["someone"]  # unassigned from the user: it leaves S1
    run(world, tmp_path, tmp_state, advance=300)
    assert tmp_state.load().holds == {}
    item.assignees = ["owner-login"]
    run(world, tmp_path, tmp_state, advance=300)
    assert tmp_state.load().holds[K5].first_held_at == world.clock.now()


# --- the quiet hour, the evidence and the plan request ---------------------------------------------------


def quiet_run(world, tmp_path, tmp_state, minutes, **kw):
    return run(world, tmp_path, tmp_state, advance=minutes * 60, **kw)


def test_59_minutes_is_held_incomplete_and_60_sends_one_plan_request_with_the_missing_list(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    world.issues[(REPO_A, 5)].body = "## Priority\nP2\n"  # only the priority is there
    run(world, tmp_path, tmp_state)
    waker = FakeWaker()
    early = quiet_run(world, tmp_path, tmp_state, 59, waker=waker)
    assert (
        decisions(early) == [("held_incomplete", K5, None)] and waker.deliveries == []
    )
    assert (
        world.count("develop", (REPO_A, 5)) == 0
    )  # the evidence is read only at the request
    res = quiet_run(world, tmp_path, tmp_state, 1, waker=waker)
    assert ("plan_requested", K5, None) in decisions(res)
    (path,) = wake_files(world.config)
    data = read_wake(path)
    assert data["assigned"] == []
    (item,) = data["plan_requests"]
    assert item["missing"] == ["fix_approach", "test_plan"]
    assert (item["repo"], item["number"], item["title"]) == (REPO_A, 5, "A title")
    assert item["url"] == f"https://github.com/{REPO_A}/issues/5"
    h = tmp_state.load().holds[K5]
    assert (h.plan_request, h.plan_request_orchestrator, h.plan_requested_at) == (
        "woken",
        "ironclaude-1",
        world.clock.now(),
    )
    assert h.plan_attempts == 1 and h.plan_wake_id == data["wake_id"]
    assert (
        K5 not in tmp_state.load().entries
    )  # a plan request is not a wake of the issue
    assert [(t.orchestrator, wid) for t, wid, _ in waker.deliveries] == [
        ("ironclaude-1", data["wake_id"])
    ]


def test_the_request_is_sent_once_per_hold_even_after_a_restart_of_the_poll(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    first = tmp_state.load().holds[K5]
    for _ in range(3):
        quiet_run(
            world, tmp_path, tmp_state, 120
        )  # the request stays unacknowledged and is resent, never asked again
    assert tmp_state.load().holds[K5].plan_requested_at == first.plan_requested_at
    assert world.count("develop", (REPO_A, 5)) == 1  # the evidence was read once


@pytest.mark.parametrize(
    ("setup", "kind"),
    [
        (
            lambda item, now: setattr(
                item, "branches", [("issue-5-x", now - timedelta(minutes=10))]
            ),
            "branch",
        ),
        (
            lambda item, now: setattr(
                item,
                "timeline",
                [
                    {
                        "event": "cross-referenced",
                        "created_at": (now - timedelta(minutes=5)).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "pull_request": True,
                    }
                ],
            ),
            "pull_request",
        ),
        (lambda item, now: setattr(item, "session", True), "session"),
    ],
)
def test_a_linked_branch_pull_request_or_session_moves_the_clock(
    tmp_path, tmp_state, gh_world, setup, kind
):
    world = held_world(gh_world)
    item = world.issues[(REPO_A, 5)]
    run(world, tmp_path, tmp_state)
    now = world.clock.now() + timedelta(minutes=60)
    setup(item, now)
    waker = FakeWaker()
    res = quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    assert decisions(res) == [("held_incomplete", K5, None)] and waker.deliveries == []
    h = tmp_state.load().holds[K5]
    assert h.evidence_kind == kind and h.plan_requested_at is None
    assert (
        world.count("develop", (REPO_A, 5)) == 1
    )  # read once, at the moment of the request
    quiet_run(
        world, tmp_path, tmp_state, 30, waker=waker
    )  # a quieter cycle reads nothing
    assert world.count("develop", (REPO_A, 5)) == 1


def test_a_signal_older_than_an_hour_does_not_hold_the_issue_back(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    world.issues[(REPO_A, 5)].branches = [
        ("old", world.clock.now() - timedelta(hours=3))
    ]
    res = quiet_run(world, tmp_path, tmp_state, 61)
    assert ("plan_requested", K5, None) in decisions(res)


def test_any_change_by_anyone_moves_the_clock_but_the_polls_own_write_does_not(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(
        world, tmp_path, tmp_state
    )  # the label write bumped updated_at; seen_updated_at was re-read
    item = world.issues[(REPO_A, 5)]
    quiet_run(world, tmp_path, tmp_state, 30)
    assert (
        tmp_state.load().holds[K5].last_evidence_at is None
    )  # the poll's own write is no evidence
    item.updated_at = world.clock.now()  # E1: a person commented
    quiet_run(world, tmp_path, tmp_state, 1)
    h = tmp_state.load().holds[K5]
    assert h.evidence_kind == "edit" and h.last_evidence_at == item.updated_at
    held = decisions(
        quiet_run(world, tmp_path, tmp_state, 58)
    )  # 59 minutes from the edit
    assert held[0][0] == "held_incomplete"
    assert ("plan_requested", K5, None) in decisions(
        quiet_run(world, tmp_path, tmp_state, 2)  # 61 from the edit
    )


def test_a_stale_search_row_older_than_what_the_poll_saw_is_not_a_change(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    item = world.issues[(REPO_A, 5)]
    seen = tmp_state.load().holds[K5].seen_updated_at
    item.updated_at = seen - timedelta(seconds=30)  # the index lags: an older value
    quiet_run(world, tmp_path, tmp_state, 5)
    assert tmp_state.load().holds[K5].last_evidence_at is None


def test_unreadable_evidence_holds_the_request_back_for_a_cycle(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    world.fail("timeline", "timeout", key=(REPO_A, 5), times=1)
    waker = FakeWaker()
    res = quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    assert decisions(res) == [("held_incomplete", K5, None)] and waker.deliveries == []
    assert tmp_state.load().holds[K5].plan_requested_at is None
    assert ("plan_requested", K5, None) in decisions(
        quiet_run(world, tmp_path, tmp_state, 5, waker=waker)
    )


def test_no_comment_and_no_comment_patch_is_ever_made_by_the_hold(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    world.issues[(REPO_A, 5)].body = GOOD_BODY
    quiet_run(world, tmp_path, tmp_state, 5)
    text = " ".join(" ".join(a) for a in world.gh_argvs)
    assert "comment" not in text and "PATCH" not in text and "issue edit" not in text
    assert {a[3] for a in writes(world)} <= {"POST", "DELETE"}


def test_the_poll_never_puts_a_failing_issue_in_assigned(tmp_path, tmp_state, gh_world):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    for path in wake_files(world.config):
        data = read_wake(path)
        assert data["assigned"] == []
        assert all(not ({"hold", "missing"} & set(a)) for a in data["assigned"])
        for item in data["plan_requests"]:
            assert set(item) == {
                "repo",
                "number",
                "title",
                "url",
                "missing",
                "held_since",
                "requested_at",
            }


def test_the_baseline_never_labels_an_issue(tmp_path, gh_world):
    store = record.init_state(
        tmp_path / "state9", CYCLE_NOW - timedelta(hours=1), baseline=True
    )
    config = make_config(tmp_path, state_dir=tmp_path / "state9")
    world = gh_world(config=config)
    world.issue(REPO_A, 5, body=EMPTY_BODY)
    cycle.run_cycle(world.deps(tmp_path, store), False)
    assert (
        writes(world) == []
        and store.load().holds == {}
        and store.load().entries[K5].ack_reason == "baseline"
    )


def test_a_dry_run_writes_no_label_and_lists_what_it_would_do(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world)
    res = run(world, tmp_path, tmp_state, dry_run=True)
    assert (
        res.would_hold == (K5,)
        and writes(world) == []
        and world.issues[(REPO_A, 5)].labels == []
    )
    assert all(ln["dry_run"] for ln in res.lines)
    # the shadow remembers the hold, so the hour can run in a 24-hour shadow run
    later = run(world, tmp_path, tmp_state, dry_run=True, advance=3600)
    assert later.would_request == (K5,) and writes(world) == []
    held = held_world(gh_world, labels=["hold:plan"])
    held.issues[(REPO_A, 5)].body = GOOD_BODY
    freed = run(held, tmp_path, tmp_state, dry_run=True)
    assert freed.would_release == (K5,) and writes(held) == []


# --- routing a plan request (5.7 point 1 and 3) --------------------------------------------------------------


def due_world(gh_world, tmp_path, tmp_state):
    world = held_world(gh_world)
    run(world, tmp_path, tmp_state)
    return world


def test_with_three_issues_in_flight_a_due_request_sends_nothing_and_leaves_the_time_unset(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    write_registry(world.config, {"ironclaude-1": {}})
    for n in (11, 12, 13):
        write_state_file(world.config, REPO_A, n)
    waker = FakeWaker()
    res = quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    assert waker.deliveries == [] and wake_files(world.config) == []
    assert tmp_state.load().holds[K5].plan_requested_at is None
    assert "plan_requested" not in reasons(res)
    # when a place frees up the next cycle sends it
    write_state_file(world.config, REPO_A, 13, status="done")
    sent = quiet_run(world, tmp_path, tmp_state, 5, waker=waker)
    assert "plan_requested" in reasons(sent) and len(waker.deliveries) == 1


def test_the_request_is_routed_after_the_assignments_of_the_same_cycle(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    for n in (11, 12, 13):
        world.issue(REPO_A, n)  # three new assignments take the three places
    waker = FakeWaker()
    res = quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    assert len(res.woken) == 3
    assert tmp_state.load().holds[K5].plan_requested_at is None
    assert all(read_wake(p)["plan_requests"] == [] for p in wake_files(world.config))
    assert all(t.orchestrator == "ironclaude-1" for t, _, _ in waker.deliveries)
    assert not any("ironclaude-2" in str(p) for p in orch_dir(world.config).iterdir())


def test_a_request_with_every_orchestrator_full_starts_no_new_one_but_with_none_it_starts_one(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    write_registry(world.config, {"ironclaude-1": {}})
    for n in (11, 12, 13):
        write_state_file(world.config, REPO_A, n)
    quiet_run(world, tmp_path, tmp_state, 60)
    reg = json.loads((orch_dir(world.config) / "orchestrators.json").read_text())
    assert list(reg) == ["ironclaude-1"]  # none added: a plan request can wait


def test_with_no_orchestrator_at_all_a_plan_request_starts_one(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    waker = FakeWaker()
    quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    assert [t.orchestrator for t, _, _ in waker.deliveries] == ["ironclaude-1"]
    assert list(
        json.loads((orch_dir(world.config) / "orchestrators.json").read_text())
    ) == ["ironclaude-1"]


def test_the_open_plan_request_counts_as_one_place_until_its_record_is_final(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    waker = FakeWaker()
    quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    rdoc = cycle.validate_setup(world.config, world.runner)

    def count():
        rows = cycle.routing_preview(world.config, rdoc, tmp_state, world.clock.now())
        return rows[0]["orchestrators"][0]["in_flight"]

    assert count() == 1
    h = tmp_state.load().holds[K5]
    write_plan_record(world.config, REPO_A, 5, h.plan_requested_at, "in_progress")
    assert count() == 1
    write_plan_record(world.config, REPO_A, 5, h.plan_requested_at, "done")
    assert count() == 0


def test_a_request_acknowledged_skipped_as_held_backlog_stops_counting_as_a_place(
    tmp_path, tmp_state, gh_world
):
    """Finding F21 of issue 675."""
    from .conftest import write_ack

    world = due_world(gh_world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    h = tmp_state.load().holds[K5]
    write_ack(world.config, h.plan_wake_id, skipped=[(REPO_A, 5, "held_backlog")])
    quiet_run(world, tmp_path, tmp_state, 5)
    assert tmp_state.load().holds[K5].plan_request == "skipped"
    rdoc = cycle.validate_setup(world.config, world.runner)
    row = cycle.routing_preview(world.config, rdoc, tmp_state, world.clock.now())[0]
    assert row["orchestrators"][0]["in_flight"] == 0


def test_a_taken_request_whose_record_is_not_final_an_hour_later_raises_plan_stuck_once(
    tmp_path, tmp_state, gh_world
):
    from .conftest import write_ack

    world = due_world(gh_world, tmp_path, tmp_state)
    waker = FakeWaker()
    quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    h = tmp_state.load().holds[K5]
    write_ack(world.config, h.plan_wake_id, taken=[(REPO_A, 5)])
    acked = quiet_run(world, tmp_path, tmp_state, 5, waker=waker)
    assert acked.exit_code == 0 and tmp_state.load().holds[K5].plan_request == "acked"
    write_plan_record(world.config, REPO_A, 5, h.plan_requested_at, "in_progress")
    quiet = quiet_run(world, tmp_path, tmp_state, 59, waker=waker)
    assert quiet.exit_code == 0
    stuck = quiet_run(world, tmp_path, tmp_state, 2, waker=waker)
    assert (stuck.exit_code, stuck.reason) == (7, "plan_stuck") and waker.unread == [
        "plan_stuck"
    ]
    after = tmp_state.load().holds[K5]
    assert (
        after.plan_request == "stuck" and after.plan_requested_at == h.plan_requested_at
    )
    again = quiet_run(world, tmp_path, tmp_state, 120, waker=waker)
    assert (
        again.exit_code == 0 and len(waker.deliveries) == 1
    )  # raised once, no second request


def test_a_taken_request_with_a_final_record_is_never_stuck(
    tmp_path, tmp_state, gh_world
):
    from .conftest import write_ack

    world = due_world(gh_world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    h = tmp_state.load().holds[K5]
    write_ack(world.config, h.plan_wake_id, taken=[(REPO_A, 5)])
    quiet_run(world, tmp_path, tmp_state, 5)
    write_plan_record(world.config, REPO_A, 5, h.plan_requested_at, "failed")
    res = quiet_run(world, tmp_path, tmp_state, 90)
    assert res.exit_code == 0 and tmp_state.load().holds[K5].plan_request == "acked"


def test_an_old_final_record_of_an_earlier_request_is_ignored(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    h = tmp_state.load().holds[K5]
    write_plan_record(
        world.config, REPO_A, 5, h.plan_requested_at - timedelta(days=3), "done"
    )
    rdoc = cycle.validate_setup(world.config, world.runner)
    row = cycle.routing_preview(world.config, rdoc, tmp_state, world.clock.now())[0]
    assert (
        row["orchestrators"][0]["in_flight"] == 1
    )  # its own record does not exist: still a place


def test_an_unacknowledged_plan_request_is_sent_again_and_abandoned_after_three_tries(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    waker = FakeWaker()
    quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    for _ in range(2):
        quiet_run(world, tmp_path, tmp_state, 11, waker=waker)
    assert tmp_state.load().holds[K5].plan_attempts == 3 and len(waker.deliveries) == 3
    res = quiet_run(world, tmp_path, tmp_state, 11, waker=waker)
    assert (res.exit_code, res.reason) == (7, "ack_not_observed")
    assert (
        tmp_state.load().holds[K5].plan_request == "abandoned"
        and len(waker.deliveries) == 3
    )


def test_a_plan_request_wake_file_matches_the_golden_item_and_the_title_has_no_control_characters(
    tmp_path, tmp_state, gh_world
):
    world = held_world(gh_world, title="Fix\tthe\nthing " + "x" * 400)
    run(world, tmp_path, tmp_state)
    quiet_run(world, tmp_path, tmp_state, 60)
    item = read_wake(wake_files(world.config)[0])["plan_requests"][0]
    assert (
        item["title"].isprintable() and 1 <= len(item["title"]) <= wake.PLAN_TITLE_MAX
    )
    parsed = wake.parse_wake(
        wake_files(world.config)[0].read_bytes(), wake_files(world.config)[0].name
    )
    assert parsed.rejected == () and parsed.wake.plan_requests[0].missing == ALL_MISSING


def test_the_plan_request_only_goes_to_a_repos_active_orchestrator_with_a_live_run(
    tmp_path, tmp_state, gh_world
):
    world = due_world(gh_world, tmp_path, tmp_state)
    write_registry(world.config, {"ironclaude-1": {}})
    write_run(world.config, "ironclaude-1", status="ending")
    waker = FakeWaker()
    quiet_run(world, tmp_path, tmp_state, 60, waker=waker)
    # the only orchestrator is ending, so the repo has none that is usable: a new one is made
    assert [t.orchestrator for t, _, _ in waker.deliveries] == ["ironclaude-2"]
    assert tmp_state.load().holds[K5].plan_request_orchestrator == "ironclaude-2"
