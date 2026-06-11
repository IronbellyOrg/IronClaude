"""Run-log substrate tests (spec §11) + the NFR-7/NFR-8 additions.

T-N20 log existence + per-event timestamp/round/state populated; T-N21 JSONL
well-formedness + event ordering; T-N22 JSONL validity (every line parses,
`event_id` monotonic). T-N51 (NFR-7): no token/credential reaches the JSONL.
T-N52 (NFR-8): replaying a fixture twice yields identical deterministic decisions.
"""

from __future__ import annotations

import json

import pytest

from superclaude.pr_submit.fsm import RunConfig, run_skill
from superclaude.pr_submit.models import Finding
from superclaude.pr_submit.run_log import RunLog, fix_key


@pytest.mark.recovery
def test_tn20_log_exists_and_events_populated(tmp_path):
    """T-N20: the run-log exists and each event carries timestamp/round/state fields."""
    rl = RunLog(42, tmp_path)
    rl.append(
        {
            "event_type": "run_started",
            "timestamp": "2026-06-11T00:00:00Z",
            "round_counter": 0,
            "state_after": "S0_IDLE",
        }
    )
    rl.append(
        {
            "event_type": "monitor_armed",
            "timestamp": "2026-06-11T00:00:30Z",
            "round_counter": 0,
            "state_after": "S2_CLASSIFY",
        }
    )
    assert rl.jsonl_path.exists()
    events = rl.read_events()
    assert len(events) == 2
    for ev in events:
        assert ev.get("timestamp") is not None
        assert "round_counter" in ev
        assert ev.get("state_after") is not None


def test_tn21_jsonl_well_formed_and_ordered(tmp_path):
    """T-N21: every line is well-formed JSON and events are in append order."""
    rl = RunLog(7, tmp_path)
    for i, et in enumerate(
        ["run_started", "poll_attempt", "poll_result", "review_detected"]
    ):
        rl.append({"event_type": et, "seq": i})
    lines = rl.jsonl_path.read_text(encoding="utf-8").splitlines()
    parsed = [json.loads(line) for line in lines if line.strip()]
    assert [p["seq"] for p in parsed] == [0, 1, 2, 3]  # append order preserved


def test_tn22_jsonl_validity_event_id_monotonic(tmp_path):
    """T-N22: every line parses and `event_id` is unique + monotonically increasing."""
    rl = RunLog(9, tmp_path)
    for et in [
        "run_started",
        "poll_attempt",
        "round_incremented",
        "push_completed",
        "terminal_clean",
    ]:
        rl.append({"event_type": et})
    ids = [
        json.loads(line)["event_id"]
        for line in rl.jsonl_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert ids == sorted(ids)
    assert len(ids) == len(set(ids))  # unique
    assert ids == list(range(1, len(ids) + 1))  # monotonic from 1


@pytest.mark.recovery
def test_tn51_no_credentials_reach_jsonl(tmp_path):
    """T-N51 (NFR-7): token/credential patterns are redacted before reaching the JSONL."""
    rl = RunLog(11, tmp_path)
    rl.append(
        {
            "event_type": "fix_applied",
            "body": "set token=ghp_ABCDEFGHIJKLMNOP0123456789 and Authorization: Bearer abcd1234efgh",
            "nested": {
                "cmd": "export GITHUB_TOKEN=github_pat_11ABCDEFGHIJKLMNOPQRSTU",
                "ok": True,
            },
        }
    )
    raw = rl.jsonl_path.read_text(encoding="utf-8")
    # No raw token survives in the JSONL.
    for leak in ("ghp_ABCDEFGHIJKLMNOP", "github_pat_11ABCDEFGH", "Bearer abcd1234"):
        assert leak not in raw
    assert "[REDACTED]" in raw


def test_tn52_replay_determinism(tmp_path):
    """T-N52 (NFR-8): replaying the same input twice yields identical deterministic decisions."""

    def make_config():
        return RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[
                Finding(
                    path="src/a.py",
                    line=1,
                    body="bug",
                    in_diff=True,
                    verification_status="verified",
                    comment_id=1,
                )
            ],
            rereview_findings=[
                [
                    Finding(
                        path="src/a.py",
                        line=2,
                        body="bug2",
                        in_diff=True,
                        verification_status="verified",
                        comment_id=2,
                    )
                ]
            ],
        )

    r1 = run_skill(make_config())
    r2 = run_skill(make_config())
    # Identical classifier/counter/route/terminal-outcome decisions.
    assert (
        r1.state,
        r1.round_counter,
        r1.push_count,
        r1.reply_count,
        r1.applied_edits,
    ) == (r2.state, r2.round_counter, r2.push_count, r2.reply_count, r2.applied_edits)


def test_rebuild_from_jsonl_is_authoritative(tmp_path):
    """§11.1: rebuilding state from the JSONL reconstructs counters + idempotency sets."""
    rl = RunLog(13, tmp_path)
    rl.append({"event_type": "fix_applied", "fix_key": fix_key("a.py", 1, "bug")})
    rl.append({"event_type": "round_incremented"})
    rl.append({"event_type": "push_completed", "target_sha": "abc123"})
    rl.append({"event_type": "reply_posted", "comment_id": 55})
    state = rl.rebuild_state()
    assert state["round_counter"] == 1
    assert state["push_count"] == 1
    assert state["reply_count"] == 1
    assert "abc123" in state["pushed_commit_shas"]
    assert 55 in state["replied_comment_ids"]
