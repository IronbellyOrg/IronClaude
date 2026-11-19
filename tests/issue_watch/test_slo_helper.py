"""``cycle.slo_numbers``: NFR-013's four numbers, with the time from assignment to acknowledgment (FU-10)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from superclaude.cli.issue_watch import cycle, record

NOW = datetime(2026, 11, 19, 12, 0, tzinfo=timezone.utc)
REPO = "o/r"


def ts(minutes_ago: float) -> str:
    return (NOW - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def decision(reason: str, minutes_ago: float, number: int = 1, **over) -> dict:
    return {
        "kind": "decision", "ts": ts(minutes_ago), "reason": reason, "repo": REPO,
        "issue": number, "dry_run": False, **over,
    }  # fmt: skip


def cycle_line(
    minutes_ago: float, exit_code: int = 0, reason: str = "cycle_complete", **over
) -> dict:
    return {
        "kind": "cycle",
        "ts": ts(minutes_ago),
        "reason": reason,
        "exit": exit_code,
        "dry_run": False,
        **over,
    }


def numbers(lines, doc=None):
    return cycle.slo_numbers(
        lines, doc or record.empty_doc(NOW - timedelta(days=30)), NOW
    )


def test_no_lines_give_no_numbers():
    n = numbers([])
    assert (
        n.assignment_to_ack_p95_s,
        n.cycle_exit0_share,
        n.acked_within_lease_share,
        n.stale_count,
    ) == (None, None, None, 0)


def test_the_time_is_measured_from_the_first_woken_line_to_the_acked_line():
    lines = [
        decision("woken", 30),
        decision("woken", 20),
        decision("acked", 10),
    ]  # a resend does not restart it
    assert numbers(lines).assignment_to_ack_p95_s == 20 * 60
    many = []
    for n in range(1, 21):
        many += [decision("woken", 60, n), decision("acked", 60 - n, n)]
    assert (
        numbers(many).assignment_to_ack_p95_s == 19 * 60
    )  # nearest rank: ceil(0.95 * 20) = 19th of 20


def test_the_share_acked_within_the_lease_counts_only_wakes_that_are_due():
    lines = [
        decision("woken", 50, 1), decision("acked", 45, 1),   # within 10 minutes
        decision("woken", 50, 2), decision("acked", 30, 2),   # 20 minutes: too late
        decision("woken", 50, 3),                             # never acknowledged, lease over
        decision("woken", 5, 4),                              # lease not over yet: not due
    ]  # fmt: skip
    assert numbers(lines).acked_within_lease_share == 1 / 3


def test_the_exit_0_share_ignores_the_disabled_and_not_enabled_cycles_and_old_ones():
    lines = [
        cycle_line(5), cycle_line(10), cycle_line(15, 5, "rate_limited"), cycle_line(20, 7, "ack_not_observed"),
        cycle_line(25, 0, "disabled"), cycle_line(30, 0, "not_enabled"),
        cycle_line(60 * 24 * 8),  # outside the seven days
    ]  # fmt: skip
    assert numbers(lines).cycle_exit0_share == 0.5


def test_a_dry_run_line_or_a_malformed_line_counts_toward_nothing_and_never_raises():
    lines = [
        decision("woken", 30, dry_run=True), decision("acked", 10, dry_run=True), cycle_line(5, dry_run=True),
        "not a dict", {"kind": "decision"}, {"kind": "cycle", "ts": "yesterday", "exit": 0},
        decision("woken", 30, repo=5), decision("acked", 10, issue="x"),
        {"kind": "decision", "ts": ts(1), "reason": "woken", "repo": REPO, "issue": 1},  # no dry_run key: counts
    ]  # fmt: skip
    n = numbers(lines)
    assert n.assignment_to_ack_p95_s is None and n.cycle_exit0_share is None


def test_stale_entries_are_unknown_or_abandoned_ack_not_observed_over_24_hours():
    old = NOW - timedelta(hours=25)
    d = record.empty_doc(old)
    for n, state in ((1, "unknown"), (2, "abandoned")):
        d = record.mark_pending(d, REPO, n, "x-1", old)
        d = (
            record.mark_unknown(d, f"{REPO}#{n}", None, None, old)
            if state == "unknown"
            else d
        )
    d = record.mark_spawn_error(
        d, f"{REPO}#2", old
    )  # abandoned for another reason: not stale
    d = record.mark_pending(d, REPO, 3, "x-1", old)
    d = record.mark_unknown(d, f"{REPO}#3", None, None, NOW)  # fresh
    assert numbers([], d).stale_count == 1
    d3 = record.sweep(
        record.mark_woken(
            record.mark_pending(record.empty_doc(old), REPO, 4, "x-1", old),
            f"{REPO}#4",
            "20261118T100000Z-0000000a",
            old,
        ),
        old + timedelta(hours=1),
    ).doc
    assert d3.entries[f"{REPO}#4"].state == "pending"  # a resend is not stale
