"""Reply / resolve / terminate tests (spec FR-6.1/FR-6.2/FR-6.4/FR-6.5).

T-601 reply posted to the correct thread; T-602 resolve AFTER reply (ordering);
T-603 `applied_edits==0` → "no code change applied", NOT "resolved"; T-610 clean
re-review → terminate; T-611 findings but round budget exhausted → terminate +
summary; T-630 residual after max rounds → summary listing the residual findings;
T-640 trivial fix → reply has a ```suggestion``` block; T-641 non-trivial → prose +
SHA only; T-642 clean re-review → exactly ONE summary thread; T-FRESH-COMMENT-NO-
DOUBLE-FIX a fresh comment_id with the same path+line+body → same fix_key → one fix.
"""

from __future__ import annotations

from superclaude.pr_submit.fsm import RunConfig, build_reply, run_skill
from superclaude.pr_submit.models import Finding, MonitorState


def _verified(path="src/a.py", line=1, body="bug", comment_id=1001) -> Finding:
    return Finding(
        path=path,
        line=line,
        body=body,
        in_diff=True,
        verification_status="verified",
        comment_id=comment_id,
    )


class _Log:
    def __init__(self) -> None:
        self.events: list[tuple] = []

    def push(self, **kw):
        self.events.append(("push",))

    def reply(self, **kw):
        self.events.append(
            ("reply", tuple(f.comment_id for f in kw.get("findings", [])))
        )

    def resolve(self, **kw):
        self.events.append(("resolve",))


def test_t601_reply_posted_to_correct_thread():
    """T-601: a reply is posted, targeting the finding's comment thread id."""
    log = _Log()
    run_skill(
        RunConfig(
            monitor_ordinal=3,
            findings=[_verified(comment_id=4242)],
            do_push=log.push,
            do_reply=log.reply,
            do_resolve=log.resolve,
        )
    )
    reply_events = [e for e in log.events if e[0] == "reply"]
    assert len(reply_events) == 1
    assert 4242 in reply_events[0][1]  # the reply targeted comment_id 4242


def test_t602_resolve_after_reply():
    """T-602: resolve happens AFTER the reply (reply-then-resolve ordering)."""
    log = _Log()
    run_skill(
        RunConfig(
            monitor_ordinal=3,
            findings=[_verified()],
            do_push=log.push,
            do_reply=log.reply,
            do_resolve=log.resolve,
        )
    )
    kinds = [e[0] for e in log.events]
    assert kinds.index("reply") < kinds.index("resolve")


def test_t603_zero_edit_reply_says_no_code_change():
    """T-603: an `applied_edits==0` reply contains "no code change applied", NOT "resolved"."""
    text = build_reply(applied_edits=0)
    assert "no code change applied" in text
    assert "resolved" not in text.replace(
        "not marked resolved", ""
    )  # never claims resolved


def test_t610_clean_rereview_terminates():
    """T-610: a clean re-review terminates (TERMINAL_CLEAN)."""
    result = run_skill(RunConfig(monitor_ordinal=3, review_state="clean"))
    assert result.state == MonitorState.TERMINAL_CLEAN


def test_t611_findings_over_budget_terminate_with_summary():
    """T-611: findings present but `round_counter >= max_rounds` → terminate with summary."""
    # max_rounds=1: cycle 0 pushes (round→1); the residual cycle hits the budget gate.
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=1,
            findings=[_verified(line=1)],
            rereview_findings=[[_verified(line=2, comment_id=2002)]],
        )
    )
    assert result.state == MonitorState.HALT_MAX_ROUNDS
    assert result.summary_posted is True


def test_t630_residual_summary_lists_findings():
    """T-630: residual after max rounds → summary lists the exact residual findings."""
    residual = _verified(line=99, comment_id=9009)
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=1,
            findings=[_verified(line=1)],
            rereview_findings=[[residual]],
        )
    )
    assert result.state == MonitorState.HALT_MAX_ROUNDS
    assert result.summary_posted is True
    assert result.findings == [residual]  # the exact residual list


def test_t640_trivial_fix_has_suggestion_block():
    """T-640: a trivial fix reply embeds a ```suggestion``` block with the applied hunk."""
    text = build_reply(
        applied_edits=1, sha="abc1234", hunk="    return x + 1", trivial=True
    )
    assert "```suggestion" in text
    assert "return x + 1" in text


def test_t641_nontrivial_fix_no_suggestion_block():
    """T-641: a non-trivial fix carries prose + SHA only, no suggestion block."""
    text = build_reply(applied_edits=3, sha="def5678", trivial=False)
    assert "```suggestion" not in text
    assert "def5678" in text


def test_t642_clean_rereview_single_summary_thread():
    """T-642: a clean re-review posts exactly ONE summary thread, not N per-finding comments."""
    result = run_skill(RunConfig(monitor_ordinal=3, review_state="clean"))
    assert result.summary_posted is True
    # A clean re-review has no per-finding replies — one summary, not N.
    assert result.reply_count == 0


def test_fresh_comment_no_double_fix(load_fixture):
    """T-FRESH-COMMENT-NO-DOUBLE-FIX: a fresh comment_id, same path+line+body → same fix_key → one fix."""
    raw = load_fixture("finding-fresh-comment-id.json")
    dup = load_fixture("finding-duplicate.json")
    fresh = Finding(
        **{
            k: v
            for k, v in raw["findings"][0].items()
            if k in {"path", "line", "body", "comment_id", "in_diff"}
        }
    )
    original = Finding(
        **{
            k: v
            for k, v in dup["findings"][0].items()
            if k in {"path", "line", "body", "comment_id", "in_diff"}
        }
    )
    # Different comment_id, identical path+line+body → identical fix_key (comment_id-independent).
    assert fresh.comment_id != original.comment_id
    assert fresh.fix_key == original.fix_key
    # Dedup by fix_key → exactly one fix.
    assert len({fresh.fix_key, original.fix_key}) == 1
