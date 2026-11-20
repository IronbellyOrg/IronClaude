"""The dispatch record, schema 2: validation, migration, transitions, the baseline and the holds (design 4.3, 4.10, 4.11)."""

from __future__ import annotations

import json
import os
import stat
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from superclaude.cli.issue_watch import record
from superclaude.cli.issue_watch.record import (
    FileStore,
    Hold,
    LockError,
    LockHeld,
    StateExists,
    StoreError,
    TransitionError,
)

from .conftest import FIXED_NOW

REPO = "IronbellyOrg/IronClaude"
KEY = f"{REPO}#7"
T0 = FIXED_NOW
WAKE = "20261107T120000Z-0000000a"


def t(minutes: float) -> datetime:
    return T0 + timedelta(minutes=minutes)


def doc() -> record.StoreDoc:
    return record.empty_doc(T0)


def pending(
    d: record.StoreDoc | None = None, n: int = 7, orch: str = "ironclaude-1"
) -> record.StoreDoc:
    return record.mark_pending(d or doc(), REPO, n, orch, t(1))


# --- validate, save, load -----------------------------------------------------------------


def raw_of(d: record.StoreDoc) -> dict:
    return json.loads(json.dumps(record._to_raw(d)))


def test_an_empty_store_round_trips_through_validate():
    assert record.validate(raw_of(doc())) == doc()


def test_a_full_store_round_trips_with_entries_holds_and_bookkeeping():
    d = pending()
    d = record.mark_woken(d, KEY, WAKE, t(2))
    d = record.record_seen(d, REPO, 8, "baseline", t(2))
    d = record.set_hold(
        d,
        f"{REPO}#9",
        Hold(
            state="held",
            first_held_at=t(1),
            seen_updated_at=t(1),
            last_evidence_at=t(3),
            evidence_kind="branch",
            plan_requested_at=t(5),
            plan_request_orchestrator="ironclaude-1",
            plan_request="woken",
            plan_acked_at=None,
            plan_wake_id=WAKE,
            plan_attempts=1,
            plan_woken_at=t(5),
            missing=("fix_approach", "test_plan"),
        ),
    )
    d = record.add_info_seen(d, ["mentions o/r#1 2026-11-07T12:00:00Z"])
    d = record.set_last_poll(d, t(4))
    d = replace(d, rate_streak=2, next_permitted_at=t(30), baseline=True)
    assert record.validate(raw_of(d)) == d


def test_save_writes_mode_0600_and_load_reads_it_back(tmp_state):
    d = record.mark_pending(tmp_state.load(), REPO, 7, "ironclaude-1", t(1))
    tmp_state.save(d)
    assert stat.S_IMODE(os.stat(tmp_state.state_dir / "dispatch.json").st_mode) == 0o600
    assert tmp_state.load() == d


def mutated(path: list, value: object, base: record.StoreDoc | None = None) -> dict:
    raw = raw_of(base or woken_doc())
    node = raw
    for key in path[:-1]:
        node = node[key]
    if value is KeyError:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return raw


def woken_doc() -> record.StoreDoc:
    return record.mark_woken(pending(), KEY, WAKE, t(2))


def held_doc() -> record.StoreDoc:
    return record.set_hold(
        doc(), KEY, Hold(state="held", first_held_at=t(1), missing=("priority",))
    )


E = ["entries", KEY]
H = ["holds", KEY]
INVALID = [
    mutated(["schema_version"], 1),
    mutated(["rate_streak"], -1),
    mutated(["rate_streak"], True),
    mutated(["baseline"], "yes"),
    mutated(["info_seen"], "x"),
    mutated(["info_seen"], ["not a key"]),
    mutated(["info_seen"], ["mentions o/r#1 2026-11-07T12:00:00Z"] * 501),
    mutated(["extra"], 1),
    mutated(["holds"], KeyError),
    mutated([*E, "issue"], 8),  # unequal to its key
    mutated([*E, "repo"], "Other/Repo"),
    mutated([*E, "state"], "launched"),
    mutated([*E, "attempts"], -1),
    mutated([*E, "wake_attempts"], 4),
    mutated([*E, "wake_id"], "not-a-wake-id"),
    mutated([*E, "orchestrator"], "Iron-1"),
    mutated([*E, "ack_reason"], "Has Space"),
    mutated([*E, "operation_id"], "bad id!"),
    mutated([*E, "created_at"], "yesterday"),
    mutated([*E, "approver_id"], 1),  # a removed field
    mutated([*E, "attempts"], KeyError),
    mutated([*E, "woken_at"], None),  # a woken entry needs its time
    mutated([*E, "orchestrator"], None),  # a woken entry needs its orchestrator
    mutated([*E, "wake_attempts"], 0),  # a woken entry has had an attempt
    mutated(["entries", "no key"], {}),
    mutated(["entries", f"{REPO}#0"], {}),
    mutated([*H, "state"], "gone", held_doc()),
    mutated([*H, "plan_request"], "running", held_doc()),
    mutated([*H, "evidence_kind"], "rumour", held_doc()),
    mutated([*H, "missing"], ["priority", "priority"], held_doc()),
    mutated([*H, "missing"], ["title"], held_doc()),
    mutated([*H, "plan_attempts"], 9, held_doc()),
    # an unhashable value is store_invalid, never a TypeError (review finding)
    mutated([*H, "state"], [], held_doc()),
    mutated([*H, "plan_request"], [], held_doc()),
    mutated([*H, "evidence_kind"], {}, held_doc()),
    mutated([*H, "missing"], [[]], held_doc()),
    mutated(
        [*H, "plan_request"], "acked", held_doc()
    ),  # a request needs its time and orchestrator
]


@pytest.mark.parametrize("raw", INVALID)
def test_an_invalid_document_is_store_invalid(raw):
    with pytest.raises(StoreError) as err:
        record.validate(raw)
    assert err.value.reason == "store_invalid"


def test_a_v1_store_is_dropped_by_the_migration_and_asks_for_the_baseline(tmp_state):
    v1 = {
        "schema_version": 1,
        "created_at": "2026-11-01T00:00:00Z",
        "next_permitted_at": None,
        "last_completed_cycle_at": None,
        "considered": {"5": "2026-11-01T00:00:00Z"},
        "consumed_log": [],
        "entries": {"5": {"issue": 5, "state": "claimed"}},
    }
    migrated = record.migrate(v1)
    assert (
        migrated["schema_version"] == 2
        and migrated["entries"] == {}
        and migrated["baseline"] is True
    )
    (tmp_state.state_dir / "dispatch.json").write_text(json.dumps(v1))
    loaded = tmp_state.load()
    assert tmp_state.migrated is True and loaded.entries == {} and loaded.baseline
    assert loaded.created_at == datetime(2026, 11, 1, tzinfo=timezone.utc)
    tmp_state.save(loaded)
    tmp_state.load()
    assert tmp_state.migrated is False


def test_migrate_refuses_a_future_version_a_gap_and_a_non_dict():
    for bad in (
        [],
        {"schema_version": 3},
        {"schema_version": "2"},
        {"schema_version": 0},
    ):
        with pytest.raises(StoreError):
            record.migrate(bad)
    with pytest.raises(StoreError):
        record.migrate({"schema_version": 1, "created_at": 5})
    with pytest.raises(StoreError):  # a step that returns the wrong version
        record.migrate({"schema_version": 1}, {1: lambda d: {"schema_version": 5}})


def test_load_errors_are_closed_reasons(tmp_state):
    path = tmp_state.state_dir / "dispatch.json"
    path.write_bytes(b"\xff\xfe")
    with pytest.raises(StoreError, match="store_invalid"):
        tmp_state.load()
    path.write_text("[" * 5000)
    with pytest.raises(StoreError, match="store_invalid"):
        tmp_state.load()
    path.unlink()
    with pytest.raises(StoreError, match="store_missing"):
        tmp_state.load()


def test_the_lock_is_exclusive_and_unsafe_lock_files_are_refused(tmp_state):
    with tmp_state.lock():
        with pytest.raises(LockHeld):
            with FileStore(tmp_state.state_dir).lock():
                pass
    with tmp_state.lock():  # released again
        pass
    lock = tmp_state.state_dir / "lock"
    lock.unlink()
    with pytest.raises(LockError, match="lock_missing"):
        with tmp_state.lock():
            pass
    lock.mkdir()
    with pytest.raises(LockError, match="lock_invalid"):
        with tmp_state.lock():
            pass


def test_the_kill_switch(tmp_state):
    assert not tmp_state.disabled() and tmp_state.disabled_since() is None
    (tmp_state.state_dir / "DISABLED").write_text("")
    assert tmp_state.disabled() and tmp_state.disabled_since() is not None
    assert record.disabled_present(tmp_state.state_dir)


# --- init_state and the baseline --------------------------------------------------------------


def test_init_state_asks_for_the_baseline_unless_told_not_to(tmp_path):
    store = record.init_state(tmp_path / "a", T0)
    assert store.load().baseline is True
    other = record.init_state(tmp_path / "b", T0, baseline=False)
    assert other.load().baseline is False
    assert stat.S_IMODE(os.stat(tmp_path / "a").st_mode) == 0o700
    assert stat.S_IMODE(os.stat(tmp_path / "a" / "lock").st_mode) == 0o600
    with pytest.raises(StateExists):
        record.init_state(tmp_path / "a", T0)
    with pytest.raises(ValueError):
        record.init_state(
            tmp_path / "c", datetime(2026, 1, 1)
        )  # a naive time creates nothing
    assert not (tmp_path / "c").exists()


def test_an_issue_recorded_at_the_baseline_is_seen_and_never_new():
    d = record.record_seen(doc(), REPO, 7, "baseline", t(1))
    entry = d.entries[KEY]
    assert (entry.state, entry.ack_reason, entry.orchestrator, entry.consumed_at) == (
        "acked",
        "baseline",
        None,
        None,
    )
    assert (
        record.record_seen(d, REPO, 7, "other", t(2)) == d
    )  # an existing entry is left alone
    assert record.day_cap_count(d, t(2)) == 0  # the baseline does not use the day cap
    d = record.end_baseline(replace(d, baseline=True))
    assert d.baseline is False
    with pytest.raises(ValueError):
        record.record_seen(doc(), REPO, 8, "Bad Reason", t(1))


# --- transitions ------------------------------------------------------------------------------


def test_pending_woken_acked_is_the_happy_path():
    d = pending()
    e = d.entries[KEY]
    assert (e.state, e.orchestrator, e.consumed_at, e.pending_at) == (
        "pending",
        "ironclaude-1",
        t(1),
        t(1),
    )
    d = record.mark_woken(d, KEY, WAKE, t(2))
    e = d.entries[KEY]
    assert (e.state, e.wake_id, e.wake_attempts, e.woken_at, e.last_reason) == (
        "woken",
        WAKE,
        1,
        t(2),
        "woken",
    )
    assert e.lease_expires_at == t(12)  # the lease is 10 minutes
    d = record.mark_acked(d, KEY, t(3), "claimed_elsewhere")
    e = d.entries[KEY]
    assert (e.state, e.ack_reason, e.lease_expires_at) == (
        "acked",
        "claimed_elsewhere",
        None,
    )


def test_a_free_text_skip_reason_is_stored_only_after_the_pattern_check():
    d = record.mark_woken(pending(), KEY, WAKE, t(2))
    assert (
        record.mark_acked(d, KEY, t(3), "Not A Token\nrm -rf").entries[KEY].ack_reason
        == "unrecognized"
    )
    assert record.mark_acked(d, KEY, t(3)).entries[KEY].ack_reason is None


def test_marks_refuse_the_wrong_state_and_bad_ids():
    with pytest.raises(TransitionError):
        record.mark_woken(doc(), KEY, WAKE, t(1))  # no entry
    with pytest.raises(TransitionError):
        record.mark_pending(pending(), REPO, 7, "ironclaude-1", t(2))  # already pending
    with pytest.raises(ValueError):
        record.mark_pending(doc(), REPO, 7, "Bad Orch", t(1))
    with pytest.raises(ValueError):
        record.mark_woken(pending(), KEY, "nope", t(2))
    with pytest.raises(TransitionError):
        record.mark_acked(doc(), KEY, t(1))
    with pytest.raises(ValueError):
        record.mark_pending(doc(), "bad", 7, "ironclaude-1", t(1))


def test_unknown_counts_an_attempt_and_names_its_reason():
    for reason in ("wake_unknown", "no_session"):
        e = record.mark_unknown(pending(), KEY, WAKE, "term_x-1", t(2), reason).entries[
            KEY
        ]
        assert (e.state, e.last_reason, e.wake_attempts, e.operation_id) == (
            "unknown",
            reason,
            1,
            "term_x-1",
        )
    with pytest.raises(ValueError):
        record.mark_unknown(pending(), KEY, WAKE, None, t(2), "woken")
    with pytest.raises(ValueError):
        record.mark_unknown(pending(), KEY, WAKE, "bad id!", t(2))


def test_spawn_error_abandons_the_entry():
    e = record.mark_spawn_error(pending(), KEY, t(2)).entries[KEY]
    assert (e.state, e.last_reason) == ("abandoned", "spawn_error")


def test_three_failed_preparations_end_abandoned_attempts_exhausted():
    d = doc()
    for n, state in enumerate(("failed", "failed", "abandoned"), start=1):
        d = record.fail(d, REPO, 7, "wake_line_invalid", t(n))
        assert d.entries[KEY].state == state and d.entries[KEY].attempts == n
    assert d.entries[KEY].last_reason == "attempts_exhausted"
    with pytest.raises(TransitionError):
        record.fail(d, REPO, 7, "wake_line_invalid", t(9))
    with pytest.raises(TransitionError):
        record.fail(doc(), REPO, 7, "pending_orphan", t(1))


def test_a_failed_entry_is_eligible_again_after_its_backoff_and_goes_pending():
    d = record.fail(doc(), REPO, 7, "revalidation_transient", t(0))
    e = d.entries[KEY]
    assert not record.backoff_elapsed(e, t(9)) and record.backoff_elapsed(e, t(10))
    d = record.mark_pending(d, REPO, 7, "ironclaude-1", t(11))
    assert d.entries[KEY].state == "pending" and d.entries[KEY].attempts == 1
    with pytest.raises(TransitionError):
        record.backoff_elapsed(d.entries[KEY], t(20))


# --- the sweep (4.5 step 6) ---------------------------------------------------------------------


def test_a_pending_entry_at_the_start_of_a_cycle_is_a_resend_and_never_abandoned():
    swept = record.sweep(pending(), t(2))
    assert (
        swept.orphans == (KEY,)
        and [e.key for e in swept.resend] == [KEY]
        and swept.abandoned == ()
    )
    assert swept.doc.entries[KEY].state == "pending"


def test_a_woken_or_unknown_entry_past_its_lease_goes_back_to_pending_for_a_resend():
    for make in (
        lambda: record.mark_woken(pending(), KEY, WAKE, t(2)),
        lambda: record.mark_unknown(pending(), KEY, WAKE, None, t(2)),
    ):
        d = make()
        early = record.sweep(d, t(11))
        assert early.resend == () and early.doc == d  # 9 minutes: still waiting
        late = record.sweep(d, t(12))
        assert [e.key for e in late.resend] == [KEY]
        e = late.doc.entries[KEY]
        assert (e.state, e.orchestrator, e.wake_attempts) == (
            "pending",
            "ironclaude-1",
            1,
        )  # same target


def test_the_third_unacknowledged_attempt_is_abandoned_ack_not_observed():
    d = pending()
    for attempt in range(1, 4):
        d = record.mark_woken(d, KEY, WAKE, t(2 * attempt * 10))
        swept = record.sweep(d, t(2 * attempt * 10 + 10))
        if attempt < 3:
            d = swept.doc
            assert swept.abandoned == ()
        else:
            (dead,) = swept.abandoned
            assert (dead.state, dead.last_reason, dead.wake_attempts) == (
                "abandoned",
                "ack_not_observed",
                3,
            )
            assert swept.resend == ()


def test_requeue_is_refused_when_the_attempts_are_used():
    d = record.mark_woken(pending(), KEY, WAKE, t(2))
    assert record.requeue(d, KEY, t(13)).entries[KEY].state == "pending"
    used = replace(d, entries={KEY: replace(d.entries[KEY], wake_attempts=3)})
    with pytest.raises(TransitionError):
        record.requeue(used, KEY, t(13))


def test_a_late_acknowledgment_still_counts_for_an_abandoned_entry():
    d = record.mark_woken(pending(), KEY, WAKE, t(2))
    d = replace(d, entries={KEY: replace(d.entries[KEY], wake_attempts=3)})
    dead = record.sweep(d, t(30)).doc
    assert dead.entries[KEY].state == "abandoned"
    assert record.mark_acked(dead, KEY, t(31)).entries[KEY].state == "acked"


# --- reset, day cap, rate limit, info -------------------------------------------------------------


def test_reset_removes_only_an_abandoned_or_unknown_entry_and_keeps_the_day_cap_count():
    d = record.mark_spawn_error(pending(), KEY, t(2))
    assert record.day_cap_count(d, t(3)) == 1
    after = record.reset_entry(d, KEY, t(3))
    assert KEY not in after.entries and record.day_cap_count(after, t(3)) == 1
    with pytest.raises(TransitionError):
        record.reset_entry(pending(), KEY, t(3))
    with pytest.raises(TransitionError):
        record.reset_entry(doc(), KEY, t(3))


def test_the_day_cap_window_is_24_hours_and_a_plan_request_counts_when_it_is_sent():
    d = record.add_consumed(pending(), t(5))
    assert record.day_cap_count(d, t(6)) == 2
    assert (
        record.day_cap_count(d, t(60 * 24 + 1)) == 1
    )  # the entry (t=1) left the window
    assert record.prune_consumed_log(d, t(60 * 24 + 6)).consumed_log == ()


def test_rate_limit_state():
    d = record.set_next_permitted(doc(), t(30), 3)
    assert (d.next_permitted_at, d.rate_streak) == (t(30), 3)
    assert record.set_next_permitted(d, t(40)).rate_streak == 3  # the streak is kept
    assert (
        record.set_last_completed(d, t(5)).rate_streak == 0
    )  # a completed cycle ends it
    cleared = record.reset_rate_limit(d)
    assert (cleared.next_permitted_at, cleared.rate_streak) == (None, 0)


def test_info_seen_keeps_the_500_newest_keys_once_each():
    keys = [f"mentions o/r#{n} 2026-11-07T12:00:00Z" for n in range(1, 601)]
    d = record.add_info_seen(doc(), keys[:300])
    d = record.add_info_seen(d, keys[100:600] + keys[:5])
    assert len(d.info_seen) == 500 and len(set(d.info_seen)) == 500
    assert d.info_seen[-1] == keys[599] and keys[0] not in d.info_seen
    record.validate(raw_of(d))


# --- holds -----------------------------------------------------------------------------------------


def test_holds_are_written_dropped_and_pruned_when_the_issue_leaves_s1():
    d = held_doc()
    d = record.set_hold(d, f"{REPO}#8", Hold(state="hand_removed", first_held_at=t(1)))
    assert set(d.holds) == {KEY, f"{REPO}#8"}
    assert record.drop_hold(d, KEY).holds.keys() == {f"{REPO}#8"}
    assert record.drop_hold(doc(), KEY) == doc()  # no entry is not an error
    assert record.prune_holds(d, [KEY]).holds.keys() == {KEY}
    with pytest.raises(StoreError):
        record.set_hold(d, "bad key", Hold(state="held", first_held_at=t(1)))
        record.validate(
            raw_of(
                record.set_hold(d, "bad key", Hold(state="held", first_held_at=t(1)))
            )
        )


# --- dry-run shadow ---------------------------------------------------------------------------------


def test_the_dry_run_shadow_is_a_whole_store_document(tmp_path):
    assert record.load_dry_run(tmp_path) == (None, False)  # the first dry run
    d = record.mark_acked(
        record.mark_woken(pending(), KEY, WAKE, t(2)), KEY, t(3), "dry_run"
    )
    record.save_dry_run(tmp_path, d)
    assert stat.S_IMODE(os.stat(tmp_path / "dry-run.json").st_mode) == 0o600
    assert record.load_dry_run(tmp_path) == (d, False)
    (tmp_path / "dry-run.json").write_text("{not json")
    assert record.load_dry_run(tmp_path) == (None, True)  # replaced: a warning is due
    (tmp_path / "dry-run.json").write_text(json.dumps({"schema_version": 2}))
    assert record.load_dry_run(tmp_path) == (None, True)
