"""Tests for ``cycle.slo_numbers``: NFR-013's four SLO numbers (plan step 6.9, AC-24).

Every case writes a synthetic ``audit.jsonl.4`` to ``audit.jsonl`` (oldest
first) under ``tmp_path``, reads it back the way an operator script would (one
``json.loads`` per line, text that is not JSON dropped) and reduces it with a
hand-built ``StoreDoc``. Every expected number is a literal worked out by hand
in the comment beside the fixture; none is computed with the code under test.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from superclaude.cli.issue_watch import cycle, record
from superclaude.cli.issue_watch.predicates import format_utc

NOW = datetime(2026, 11, 7, 12, 0, 0, tzinfo=timezone.utc)
LOG_NAMES = (
    "audit.jsonl.4",
    "audit.jsonl.3",
    "audit.jsonl.2",
    "audit.jsonl.1",
    "audit.jsonl",
)


# -- fixture builders ----------------------------------------------------------


def _ago(**delta: float) -> datetime:
    return NOW - timedelta(**delta)


def _cycle(
    at: datetime, exit_code: int = 0, reason: str = "not_approved", *, dry_run=False
) -> dict:
    return {
        "kind": "cycle",
        "ts": format_utc(at),
        "host": "test-host",
        "login": "owner-login",
        "cycle_id": "0" * 32,
        "dry_run": dry_run,
        "exit": exit_code,
        "reason": reason,
        "gh_calls": 4,
        "duration_ms": 120,
    }


def _decision(
    at: datetime,
    issue: int,
    reason: str,
    *,
    approved_at: datetime | None = None,
    dry_run: bool = False,
) -> dict:
    return {
        "kind": "decision",
        "ts": format_utc(at),
        "host": "test-host",
        "login": "owner-login",
        "cycle_id": "0" * 32,
        "dry_run": dry_run,
        "reason": reason,
        "issue": issue,
        "approver_id": 1001,
        "approval_event_id": 2,
        "approved_at": None if approved_at is None else format_utc(approved_at),
    }


def _launched(issue: int, at: datetime, wait_s: int, **kw) -> dict:
    """A ``launched`` line approved ``wait_s`` seconds before its ``ts``."""
    approved = at - timedelta(seconds=wait_s)
    return _decision(at, issue, "launched", approved_at=approved, **kw)


def _claimed(issue: int, at: datetime, **kw) -> dict:
    return _decision(at, issue, "claimed", **kw)


def _entry(
    issue: int, state: str, updated_at: datetime, last_reason: str | None = None
) -> record.Entry:
    return record.Entry(
        issue=issue,
        state=state,
        attempts=1,
        launches=1,
        operation_id=None,
        approver_id=None,
        approval_event_id=None,
        approved_at=None,
        launch_cwd=None,
        launch_login=None,
        launch_account_id=None,
        consumed_at=None,
        pending_at=None,
        created_at=updated_at,
        updated_at=updated_at,
        lease_expires_at=None,
        last_reason=last_reason,
    )


def _doc(*entries: record.Entry) -> record.StoreDoc:
    return record.StoreDoc(
        schema_version=cycle.SCHEMA_VERSION,
        created_at=_ago(days=60),
        next_permitted_at=None,
        last_completed_cycle_at=None,
        considered={},
        consumed_log=(),
        entries={e.issue: e for e in entries},
    )


def _write_rotated(tmp_path: Path, chunks: list[list[dict | str]]) -> None:
    """Write ``chunks`` (oldest first) to the newest ``len(chunks)`` log files."""
    assert len(chunks) <= len(LOG_NAMES)
    for name, chunk in zip(LOG_NAMES[-len(chunks) :], chunks):
        text = "".join(
            (json.dumps(item) if isinstance(item, dict) else item) + "\n"
            for item in chunk
        )
        (tmp_path / name).write_text(text, encoding="utf-8")


def _read_log(tmp_path: Path) -> list:
    """Parse every line of the rotated files, oldest file first, dropping non-JSON."""
    parsed: list = []
    for name in LOG_NAMES:
        path = tmp_path / name
        if not path.exists():
            continue
        for text in path.read_text(encoding="utf-8").splitlines():
            try:
                parsed.append(json.loads(text))
            except ValueError:
                continue
    return parsed


def _slo(
    tmp_path: Path, lines: list[dict], doc: record.StoreDoc | None = None
) -> cycle.SloNumbers:
    """Spread ``lines`` over all five files in time order and reduce them."""
    ordered = sorted(lines, key=lambda ln: ln["ts"])
    n = len(ordered)
    _write_rotated(tmp_path, [ordered[k * n // 5 : (k + 1) * n // 5] for k in range(5)])
    return cycle.slo_numbers(_read_log(tmp_path), doc or _doc(), NOW)


def _cycle_lines() -> list[dict]:
    """The (b) fixture: 7 counted exit-0 and 3 counted failures, plus excluded lines.

    Counted: exit 0 for reasons not_approved x3, launched, day_cap,
    disabled_mid_cycle and already_dispatched (the last at 6 days 23 h, inside the
    window), and failures gh_timeout (3), rate_limited (5) and lock_held (75).
    Excluded: 5 ``disabled`` and 4 ``not_enabled`` (exit 0), 6 dry-run exit 0 and
    2 dry-run exit 3 lines, and 13 lines older than 7 days (10 failures, 3 exit 0).
    """
    ok = ["not_approved"] * 3 + ["launched", "day_cap", "disabled_mid_cycle"]
    lines = [_cycle(_ago(hours=h), 0, r) for h, r in enumerate(ok, start=1)]
    lines.append(_cycle(_ago(hours=167), 0, "already_dispatched"))
    for hours, code, reason in ((8, 3, "gh_timeout"), (9, 5, "rate_limited")):
        lines.append(_cycle(_ago(hours=hours), code, reason))
    lines.append(_cycle(_ago(hours=10), 75, "lock_held"))
    lines += [_cycle(_ago(hours=11 + k), 0, "disabled") for k in range(5)]
    lines += [_cycle(_ago(hours=16 + k), 0, "not_enabled") for k in range(4)]
    lines += [_cycle(_ago(hours=20 + k), 0, dry_run=True) for k in range(6)]
    lines += [
        _cycle(_ago(hours=26 + k), 3, "gh_timeout", dry_run=True) for k in range(2)
    ]
    lines += [_cycle(_ago(days=7, hours=1 + k), 3, "gh_timeout") for k in range(10)]
    lines += [_cycle(_ago(days=8 + k), 0) for k in range(3)]
    return lines


def _stale_entries() -> list[record.Entry]:
    """The (d) fixture: issues 1, 2 and 9 are stale, the other six are not."""
    return [
        _entry(1, "unknown", _ago(hours=25)),  # stale: unknown, 25 h
        _entry(2, "abandoned", _ago(hours=48), "pending_orphan"),  # stale
        _entry(3, "unknown", _ago(hours=23)),  # fresh
        _entry(4, "abandoned", _ago(hours=1), "pending_orphan"),  # fresh
        _entry(5, "abandoned", _ago(hours=100), "claim_not_observed"),  # wrong reason
        _entry(6, "launched", _ago(hours=100), "launched"),  # wrong state
        _entry(7, "claimed", _ago(hours=100), "claimed"),  # wrong state
        _entry(8, "unknown", _ago(hours=24)),  # exactly 24 h: not "more than"
        _entry(9, "unknown", _ago(hours=24, seconds=1)),  # stale: 24 h and 1 s
    ]


# -- (a) approval-to-launch p95 -------------------------------------------------


def test_p95_is_the_nearest_rank_of_launch_minus_approval(tmp_path):
    """NFR-013, AC-24: (a) the p95 is the nearest rank of launch minus approval."""
    # 30 waits, a permutation of 60 s..1800 s in steps of 60 s (17k mod 31 hits
    # every residue 1..30 once). Nearest rank: ceil(0.95 * 30) = 29, so the 29th
    # smallest wait, 29 * 60 = 1740 s. The maximum would be 1800 and the 28th 1680.
    perm = [(k * 17) % 31 for k in range(1, 31)]
    lines = [
        _launched(issue, _ago(days=2) + timedelta(minutes=issue), 60 * p)
        for issue, p in enumerate(perm, start=1)
    ]
    assert _slo(tmp_path, lines).approval_to_launch_p95_s == 1740.0


@pytest.mark.parametrize(
    ("count", "expected"),
    [
        (1, 60.0),  # ceil(0.95) = 1: the only wait
        (2, 120.0),  # ceil(1.90) = 2: the larger wait
        (20, 1140.0),  # ceil(19.0) = 19: 19 * 60
        (21, 1200.0),  # ceil(19.95) = 20: 20 * 60
        (100, 5700.0),  # ceil(95.0) = 95: 95 * 60
    ],
)
def test_p95_rank_for_small_and_round_sample_sizes(tmp_path, count, expected):
    # Waits 60 s * k for k = 1..count, written largest first so the sort matters.
    lines = [
        _launched(k, _ago(days=2) + timedelta(minutes=k), 60 * k)
        for k in range(count, 0, -1)
    ]
    assert _slo(tmp_path, lines).approval_to_launch_p95_s == expected


def test_launched_line_without_a_usable_approved_at_is_left_out_of_p95(tmp_path):
    at = _ago(hours=5)
    null_approved = _launched(1, at, 100)
    null_approved["approved_at"] = None
    absent_approved = _launched(2, at, 100)
    del absent_approved["approved_at"]
    bad_approved = _launched(3, at, 100)
    bad_approved["approved_at"] = "not a time"
    lines = [null_approved, absent_approved, bad_approved, _launched(4, at, 600)]
    slo = _slo(tmp_path, lines)
    # Only issue 4 has a wait: its 600 s is the single sample. The other three
    # launched lines still count for (c): 4 due, none claimed, 0 / 4.
    assert slo.approval_to_launch_p95_s == 600.0
    assert slo.claimed_within_lease_share == 0.0


# -- (b) cycle exit-0 share -----------------------------------------------------


def test_exit0_share_covers_seven_days_and_skips_disabled_and_dry_run(tmp_path):
    """NFR-013, AC-24: (b) the exit-0 share of the counted cycles of seven days."""
    # Counted: 7 exit-0 and 3 failing cycles, so 7 / 10 = 0.7. Counting the old
    # lines would give 10 / 23, the disabled and not_enabled lines 16 / 19, the
    # dry-run lines 13 / 18.
    assert _slo(tmp_path, _cycle_lines()).cycle_exit0_share == 0.7


def test_cycle_lines_without_the_optional_counters_still_count(tmp_path):
    plain = _cycle(_ago(hours=1))
    full = {**_cycle(_ago(hours=2)), "discovery_count": 7, "clock_skew_s": 3}
    failed = {**_cycle(_ago(hours=3), 3, "gh_timeout"), "discovery_count": 1}
    # 2 exit-0 of 3 counted lines.
    assert _slo(tmp_path, [plain, full, failed]).cycle_exit0_share == pytest.approx(
        2 / 3
    )


# -- (c) claimed within the lease ----------------------------------------------


def test_claimed_share_counts_in_time_late_and_never(tmp_path):
    """NFR-013, AC-24: (c) the share of launches claimed within the lease."""
    t = _ago(hours=5)
    lines = [
        _launched(11, t, 60),
        _claimed(11, t + timedelta(minutes=30)),  # in time
        _launched(12, t + timedelta(minutes=1), 60),
        _claimed(12, t + timedelta(minutes=62)),  # 61 min after its launch: late
        _launched(13, t + timedelta(minutes=2), 60),  # never claimed
        _claimed(90, t + timedelta(minutes=3)),  # another issue: counts for nobody
    ]
    # Three launched lines past their lease, one reached claimed: 1 / 3.
    assert _slo(tmp_path, lines).claimed_within_lease_share == pytest.approx(1 / 3)


@pytest.mark.parametrize(
    ("claim_after_s", "expected"),
    [
        (0, 1.0),  # same second as the launch
        (3599, 1.0),  # one second before the 60-minute lease ends
        (3600, 0.0),  # exactly at lease end is not "before" it
        (3601, 0.0),
    ],
)
def test_claim_must_land_before_the_lease_ends(tmp_path, claim_after_s, expected):
    t = _ago(hours=5)
    lines = [_launched(1, t, 60), _claimed(1, t + timedelta(seconds=claim_after_s))]
    assert _slo(tmp_path, lines).claimed_within_lease_share == expected


def test_a_launch_still_inside_its_lease_is_not_yet_a_miss(tmp_path):
    lines = [
        _launched(21, _ago(hours=5), 60),
        _claimed(21, _ago(hours=5) + timedelta(minutes=10)),  # old, in time
        _launched(22, _ago(minutes=10), 60),  # lease open for 50 more minutes
        _launched(23, _ago(minutes=10), 60),
        _claimed(23, _ago(minutes=5)),  # open lease but already reached
    ]
    # Due: 21 and 23 (both reached); 22 cannot be judged yet. 2 / 2, not 2 / 3.
    assert _slo(tmp_path, lines).claimed_within_lease_share == 1.0


# -- (d) stale count ------------------------------------------------------------


def test_stale_count_takes_old_unknown_and_old_pending_orphan_only(tmp_path):
    """NFR-013, AC-24: (d) the stale count is old unknown and pending_orphan only."""
    # Issues 1 (unknown, 25 h), 2 (abandoned pending_orphan, 48 h) and 9
    # (unknown, 24 h 1 s) are stale: 3. Issue 8 is exactly 24 h, 3 and 4 are
    # fresh, 5 has another reason, 6 and 7 are the wrong state.
    slo = _slo(tmp_path, [_cycle(_ago(hours=1))], _doc(*_stale_entries()))
    assert slo.stale_count == 3


# -- dry run, malformed lines, empty log, all four together ---------------------


def test_dry_run_lines_count_toward_none_of_a_b_and_c(tmp_path):
    t = _ago(hours=3)
    lines = [
        _launched(1, t, 600),  # live: never claimed by a live line
        _cycle(_ago(hours=1)),  # live: exit 0
        _launched(2, t + timedelta(minutes=1), 9000, dry_run=True),
        _claimed(2, t + timedelta(minutes=2), dry_run=True),
        _claimed(1, t + timedelta(minutes=30), dry_run=True),  # must not rescue 1
        _cycle(_ago(hours=2), 3, "gh_timeout", dry_run=True),
    ]
    slo = _slo(tmp_path, lines)
    # Counting dry-run lines would give p95 9000, share 1 / 2 and claimed 2 / 2.
    assert slo.approval_to_launch_p95_s == 600.0
    assert slo.cycle_exit0_share == 1.0
    assert slo.claimed_within_lease_share == 0.0


def test_malformed_lines_are_dropped_without_changing_the_numbers(tmp_path):
    clean = [
        _cycle(_ago(hours=2)),
        _launched(1, _ago(hours=3), 300),
        _claimed(1, _ago(hours=3) + timedelta(minutes=10)),
    ]
    base_cycle = _cycle(_ago(hours=1), 3, "gh_timeout")
    no_ts = {k: v for k, v in base_cycle.items() if k != "ts"}
    junk: list[dict | str] = [
        "not json at all",
        '{"kind": "cycle", "ts": ',  # truncated by a crash
        "",
        "[1, 2]",
        '"just a string"',
        "7",
        "null",
        {**base_cycle, "ts": "2026-11-07 11:00:00"},  # not the Z form
        {**base_cycle, "ts": "2026-11-07T11:00:00+00:00"},  # offset form
        {**base_cycle, "ts": 12345},  # not a string
        no_ts,
        {"kind": "cycle"},
        {**_launched(2, _ago(hours=3), 400), "ts": "yesterday"},
        {**_launched(3, _ago(hours=3), 500), "issue": True},  # bool is not an issue
        {**_launched(4, _ago(hours=3), 500), "issue": "4"},
        {k: v for k, v in _launched(5, _ago(hours=3), 500).items() if k != "issue"},
        {"kind": "warning", "ts": format_utc(_ago(hours=1)), "reason": "clock_skew"},
    ]
    _write_rotated(tmp_path, [junk[:6], junk[6:11], [clean[0]], junk[11:], clean[1:]])
    slo = cycle.slo_numbers(_read_log(tmp_path), _doc(), NOW)
    # Only the clean lines count: wait 300 s, 1 / 1 cycles, 1 / 1 claimed, 0 stale.
    assert slo == cycle.SloNumbers(300.0, 1.0, 1.0, 0)


def test_empty_log_gives_no_samples_and_a_zero_stale_count(tmp_path):
    assert _read_log(tmp_path) == []  # no log files at all
    assert cycle.slo_numbers([], _doc(), NOW) == cycle.SloNumbers(None, None, None, 0)

    _write_rotated(tmp_path, [[], [], [], [], []])  # five empty files
    assert _read_log(tmp_path) == []
    assert cycle.slo_numbers(_read_log(tmp_path), _doc(), NOW) == cycle.SloNumbers(
        None, None, None, 0
    )


def test_stale_count_comes_from_the_store_even_with_an_empty_log(tmp_path):
    slo = cycle.slo_numbers([], _doc(*_stale_entries()), NOW)
    assert slo == cycle.SloNumbers(None, None, None, 3)


def test_the_four_numbers_from_one_rotated_fixture_log(tmp_path):
    """NFR-013, AC-24: slo_numbers returns the four values on one fixture log."""
    t = _ago(hours=5)
    lines = _cycle_lines() + [
        _launched(31, t, 120),
        _claimed(31, t + timedelta(minutes=20)),  # in time
        _launched(32, t + timedelta(minutes=1), 600),
        _claimed(32, t + timedelta(minutes=70)),  # 69 min after launch: late
        _launched(33, t + timedelta(minutes=2), 1800),  # never claimed
    ]
    slo = _slo(tmp_path, lines, _doc(*_stale_entries()))
    for name in LOG_NAMES:  # the log really is spread over all five files
        assert (tmp_path / name).stat().st_size > 0
    # (a) waits 120, 600, 1800: ceil(0.95 * 3) = 3, the largest: 1800 s.
    # (b) 7 of 10 counted cycles exit 0. (c) 1 of 3 launches claimed in time.
    # (d) issues 1, 2 and 9 are stale.
    assert slo.approval_to_launch_p95_s == 1800.0
    assert slo.cycle_exit0_share == 0.7
    assert slo.claimed_within_lease_share == pytest.approx(1 / 3)
    assert slo.stale_count == 3
    # A generator of the same lines gives the same result: the input is one pass.
    again = cycle.slo_numbers(iter(_read_log(tmp_path)), _doc(*_stale_entries()), NOW)
    assert again == slo
