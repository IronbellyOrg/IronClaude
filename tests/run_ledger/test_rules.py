"""Pure inclusion rules of the Run ledger (``decide``). Plain dicts, no monkeypatching."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from superclaude.cli.sweep.ledger import decide

NOW = datetime(2026, 11, 26, 18, 0, 0, tzinfo=timezone.utc)
OLD = "2026-11-01 10:00:00"  # SQLite form, well before NOW and the 24 h window
WT_MAIN = {"id": "repoA::/home/u/main", "isMainWorktree": True}
WT_FEATURE = {"id": "repoA::/home/u/feature", "isMainWorktree": False}


def run(run_id: str = "run_aaaaaaaaaaaa", created: str = OLD, **extra) -> dict:
    return {
        "id": run_id,
        "objective": "obj",
        "legacy": 0,
        "created_at": created,
        **extra,
    }


def worker(worktree_id: str | None) -> dict:
    return {"resource": {"worktreeId": worktree_id}} if worktree_id is not None else {}


def task(status: str, created: str = OLD) -> dict:
    return {"status": status, "created_at": created}


def decide_one(
    r, workers=None, tasks=None, worktrees=(WT_MAIN, WT_FEATURE), previous=None
):
    rid = r["id"]
    entries, counts = decide(
        [r],
        {rid: workers or []},
        {rid: tasks or []},
        list(worktrees),
        previous,
        NOW,
    )
    return (entries[0] if entries else None), counts


def test_live_worktree_run_in():
    entry, counts = decide_one(run(), workers=[worker(WT_FEATURE["id"])])
    assert entry["reasons"] == ["live_worktree"]
    assert entry["live_worktree_ids"] == [WT_FEATURE["id"]]
    assert counts["live_worktree"] == 1


def test_deleted_worktrees_only_run_out():
    entry, _ = decide_one(
        run(),
        workers=[worker("repoA::/gone")],
        tasks=[task("completed"), task("failed")],
    )
    assert entry is None


@pytest.mark.parametrize(
    ("status", "is_in"),
    [
        ("ready", True),
        ("blocked", True),
        ("in_progress", True),
        ("some_unknown_status", True),
        ("completed", False),
        ("failed", False),
        ("cancelled", False),
    ],
)
def test_unfinished_task_run_in(status, is_in):
    entry, _ = decide_one(run(), tasks=[task(status)])
    assert (entry is not None) is is_in
    if is_in:
        assert entry["reasons"] == ["unfinished_task"]
        assert entry["unfinished_task_count"] == 1


def test_new_run_in():
    previous = {"generated_at": "2026-11-26T17:00:00Z"}
    entry, counts = decide_one(run(created="2026-11-26 17:30:00"), previous=previous)
    assert entry["reasons"] == ["new"]
    assert counts["new"] == 1


def test_new_fallback_24h_when_no_previous_ledger():
    recent, _ = decide_one(run(created="2026-11-25 20:00:00"))  # 22 h old
    older, _ = decide_one(run(created="2026-11-25 17:00:00"))  # 25 h old
    assert recent["reasons"] == ["new"]
    assert older is None


def test_legacy_run_out():
    wid = WT_FEATURE["id"]
    by_name, _ = decide_one(run("run_legacy_local"), workers=[worker(wid)])
    by_flag, _ = decide_one(run(legacy=1), workers=[worker(wid)])
    assert by_name is None
    assert by_flag is None


def test_worktree_id_exact_match_only():
    entry, _ = decide_one(run(), workers=[worker("otherRepo::/home/u/feature")])
    assert entry is None


def test_null_worktree_id_no_match():
    entry, _ = decide_one(
        run(), workers=[worker(None), {"resource": {"worktreeId": None}}]
    )
    assert entry is None


def test_time_forms_compare_correctly():
    previous = {"generated_at": "2026-11-26T18:00:00Z"}  # ISO form
    after, _ = decide_one(
        run(created="2026-11-26 18:00:01"), previous=previous
    )  # SQLite form
    before, _ = decide_one(run(created="2026-11-26 17:59:59"), previous=previous)
    assert after is not None
    assert before is None
    # an unparseable created_at is "not new" and never raises
    junk, _ = decide_one(run(created="not a time"), previous=previous)
    assert junk is None


def test_main_checkout_only_requires_only_reason_and_a_match():
    main_only, counts = decide_one(run(), workers=[worker(WT_MAIN["id"])])
    assert main_only["main_checkout_only"] is True
    assert counts["main_checkout_only"] == 1
    no_match, _ = decide_one(run(), tasks=[task("ready")])
    with_task, _ = decide_one(
        run(), workers=[worker(WT_MAIN["id"])], tasks=[task("ready")]
    )
    mixed, _ = decide_one(
        run(), workers=[worker(WT_MAIN["id"]), worker(WT_FEATURE["id"])]
    )
    assert no_match["main_checkout_only"] is False
    assert with_task["main_checkout_only"] is False
    assert mixed["main_checkout_only"] is False


def test_stale_flag_is_null_without_task_timestamp():
    undated = {"status": "ready"}
    entry, counts = decide_one(run(), tasks=[undated])
    assert entry["stale_open_tasks_only"] is None
    assert counts["open_task_stale_7d_only"] == 0


def test_stale_flag_true_for_old_ready_or_blocked_and_blocked_only_counted():
    entry, counts = decide_one(run(), tasks=[task("ready"), task("blocked")])
    assert entry["stale_open_tasks_only"] is True
    assert entry["blocked_only"] is False
    assert counts["open_task_stale_7d_only"] == 1
    blocked, counts2 = decide_one(run(), tasks=[task("blocked")])
    assert blocked["blocked_only"] is True
    assert counts2["blocked_only"] == 1
    fresh, _ = decide_one(run(), tasks=[task("ready", created="2026-11-26 12:00:00")])
    assert fresh["stale_open_tasks_only"] is False
    busy, _ = decide_one(run(), tasks=[task("in_progress")])
    assert busy["stale_open_tasks_only"] is False
