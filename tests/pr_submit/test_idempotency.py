"""Idempotency tests (spec §11.4 / NFR-1).

T-N01 replaying findings twice → reply once per thread; T-N02 reply-tracking
persisted across polls (survives a JSONL rebuild); T-FRESH-COMMENT-NO-DOUBLE-FIX a
fresh `comment_id` with the same `path+line+body` hashes to the same `fix_key`
(comment_id-independent) → `idempotency_skip` → exactly one fix.
"""

from __future__ import annotations

from superclaude.pr_submit.models import Finding
from superclaude.pr_submit.run_log import RunLog, fix_key


def test_tn01_replay_findings_reply_once_per_thread(tmp_path):
    """T-N01: replaying the same finding twice → reply posted once per thread."""
    rl = RunLog(42, tmp_path)
    comment_id = 7001
    # First reply: newly recorded → proceed.
    assert rl.record_idempotent("replied_comment_ids", comment_id) is True
    rl.append({"event_type": "reply_posted", "comment_id": comment_id})
    # Replay (second poll surfaces the same finding) → already replied → skip.
    assert rl.record_idempotent("replied_comment_ids", comment_id) is False
    # Exactly one reply_posted event in the log.
    replies = [e for e in rl.read_events() if e["event_type"] == "reply_posted"]
    assert len(replies) == 1
    # An idempotency_skip was recorded for the duplicate.
    skips = [e for e in rl.read_events() if e["event_type"] == "idempotency_skip"]
    assert len(skips) == 1


def test_tn02_reply_tracking_persisted_across_polls(tmp_path):
    """T-N02: reply-tracking persists across polls — rebuilt state still shows the replied id."""
    rl = RunLog(8, tmp_path)
    rl.record_idempotent("replied_comment_ids", 9009)
    rl.append({"event_type": "reply_posted", "comment_id": 9009})
    # Simulate a new poll cycle: a fresh RunLog over the SAME dir rebuilds from JSONL.
    rl2 = RunLog(8, tmp_path)
    state = rl2.rebuild_state()
    assert 9009 in state["replied_comment_ids"]
    # The dedup still fires on the persisted set.
    assert rl2.record_idempotent("replied_comment_ids", 9009) is False


def test_fresh_comment_no_double_fix(tmp_path):
    """T-FRESH-COMMENT-NO-DOUBLE-FIX: same path+line+body, new comment_id → same fix_key → one fix."""
    # Two findings: identical path+line+body, DIFFERENT comment_id (a fresh Augment comment).
    original = Finding(
        path="src/auth.py",
        line=42,
        body="missing authz check",
        comment_id=100,
        in_diff=True,
    )
    fresh = Finding(
        path="src/auth.py",
        line=42,
        body="missing authz check",
        comment_id=999,
        in_diff=True,
    )
    assert original.comment_id != fresh.comment_id
    # The fix_key is comment_id-INDEPENDENT → identical.
    assert (
        original.fix_key
        == fresh.fix_key
        == fix_key("src/auth.py", 42, "missing authz check")
    )

    rl = RunLog(13, tmp_path)
    # First fix proceeds and is recorded under the fix_key.
    assert rl.record_idempotent("processed_finding_ids", original.fix_key) is True
    rl.append({"event_type": "fix_applied", "fix_key": original.fix_key})
    # The fresh comment hashes to the SAME fix_key → skip → no second fix.
    assert rl.record_idempotent("processed_finding_ids", fresh.fix_key) is False
    fixes = [e for e in rl.read_events() if e["event_type"] == "fix_applied"]
    assert len(fixes) == 1  # exactly one fix despite two comments
