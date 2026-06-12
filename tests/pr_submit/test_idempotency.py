"""Idempotency tests (spec §11.4 / NFR-1).

T-N01 replaying findings twice → reply once per thread; T-N02 reply-tracking
persisted across polls (survives a JSONL rebuild); T-FRESH-COMMENT-NO-DOUBLE-FIX a
fresh `comment_id` with the same `path+line+body` hashes to the same `fix_key`
(comment_id-independent) → `idempotency_skip` → exactly one fix.
"""

from __future__ import annotations

from superclaude.pr_submit.models import EventType, Finding
from superclaude.pr_submit.run_log import IDEMPOTENCY_SETS, RunLog, fix_key


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


# --- V1.1 6th idempotency set: auggie_review_invoked (INV-R2 strict-once) -----


def test_t1120_auggie_review_invoked_at_most_once(tmp_path):
    """T-1120 / T-AUGGIE-AT-MOST-ONCE: the 6th idempotency set is the durable
    strict-once gate — record_idempotent("auggie_review_invoked", pr) returns True
    the first time and False on replay, emitting an idempotency_skip (INV-R2)."""
    assert "auggie_review_invoked" in IDEMPOTENCY_SETS
    assert len(IDEMPOTENCY_SETS) == 6  # 5→6, NOT a "4"/reconcile framing
    rl = RunLog(55, tmp_path)
    pr = 55
    # First fallback invoke: newly recorded → proceed.
    assert rl.record_idempotent("auggie_review_invoked", pr) is True
    rl.append({"event_type": EventType.AUGGIE_FALLBACK_INVOKED.value, "pr_number": pr})
    # Replay (a second decline later) → already invoked → skip.
    assert rl.record_idempotent("auggie_review_invoked", pr) is False
    # The set folds the pr_number exactly once.
    state = rl.rebuild_state()
    assert state["auggie_review_invoked"] == [pr]
    skips = [e for e in rl.read_events() if e["event_type"] == "idempotency_skip"]
    assert len(skips) == 1


def test_t1124_auggie_strict_once_survives_resume(tmp_path, load_fixture):
    """T-1124: the strict-once gate survives a resume — a second RunLog over the same
    dir rebuilds the auggie_review_invoked set and the gate still skips (INV-R2)."""
    fixture = load_fixture("decline-twice.json")
    pr = 55
    rl = RunLog(pr, tmp_path)
    assert rl.record_idempotent("auggie_review_invoked", pr) is True
    rl.append({"event_type": EventType.AUGGIE_FALLBACK_INVOKED.value, "pr_number": pr})
    # New poll cycle / resume: a fresh RunLog rebuilds the set from the JSONL.
    rl2 = RunLog(pr, tmp_path)
    state = rl2.rebuild_state()
    assert pr in state["auggie_review_invoked"]
    assert len(state["auggie_review_invoked"]) == 1
    # Even across the two declines in the fixture, the invoke is recorded once.
    assert (
        len(state["auggie_review_invoked"])
        == fixture["expected"]["auggie_review_invoked_count"]
    )
    # The dedup still fires on the persisted set after resume.
    assert rl2.record_idempotent("auggie_review_invoked", pr) is False
