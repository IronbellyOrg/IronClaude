"""Oversized-PR auggie-review fallback tests (V1.1 R2/R3 / FR-9/FR-10, addendum §6.4).

When Augment posts an "abnormally large" decline, the skill engages a single-shot
in-session `/sc:auggie-review` fallback: clamp the budget to 1 (INV-R3), invoke
`/sc:auggie-review` AT MOST ONCE per PR (INV-R2 strict-once), remediate ONCE under the
clamp with NO loop-back, and keep `push_count <= max_rounds + 1`. The two counters
(`round_counter`, `fallback_round_counter`) are independent; `round_counter` is frozen
at fallback entry.

T-1110..T-1118 decline detection + routing to S5b from BOTH the initial S2 poll and the
S5 re-trigger poll; T-1120..T-1125 + T-AUGGIE-AT-MOST-ONCE the strict-once gate, clamp,
single-shot sub-loop, frozen `round_counter`, and total-push bound.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import RunConfig, _run_fallback, run_skill, transition
from superclaude.pr_submit.models import Finding, MonitorState, SkillResult


def _f(line: int, **kw) -> Finding:
    return Finding(
        path="src/a.py",
        line=line,
        body=f"bug{line}",
        in_diff=True,
        verification_status="verified",
        comment_id=2000 + line,
        **kw,
    )


def _ff(line: int, **kw) -> Finding:
    """A fallback finding (distinct path so it is visibly the fallback's output).

    Caller ``**kw`` overrides the defaults (e.g. ``verification_status="unverified"``).
    """
    fields = dict(
        path="src/app/db.py",
        line=line,
        body=f"fallback-bug{line}",
        in_diff=True,
        verification_status="verified",
        comment_id=9000 + line,
    )
    fields.update(kw)
    return Finding(**fields)


# --- decline detection + routing to S5b (FR-9.1, T-1110..T-1118) --------------


@pytest.mark.inv
def test_t1110_t1113b_decline_at_initial_poll_routes_to_fallback():
    """T-1110 / T-1113b (FR-9.2, EC-19): a decline at the INITIAL S2 poll (before any push)
    routes to the fallback (S5b)."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            review_state="declined",
            fallback_findings=[_ff(88)],
        )
    )
    assert result.fallback_engaged is True
    assert result.decline_detected is True
    assert result.round_counter == 0  # round_counter FROZEN (no Augment round ran)


@pytest.mark.inv
def test_t1113_decline_at_s5_retrigger_poll_routes_to_fallback():
    """T-1113: a decline observed at the S5 re-trigger poll (after a push) → fallback."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_outcome=["declined"],
            fallback_findings=[_ff(88)],
        )
    )
    assert result.fallback_engaged is True
    # The push happened, but the declined cycle did NOT tick round_counter.
    assert result.round_counter == 0
    assert result.push_count >= 1


# --- strict-once + clamp + single-shot (FR-10, INV-R2/R3, T-1120..T-1125) ------


@pytest.mark.inv
def test_t1114_auggie_at_most_once_across_two_declines_and_resume():
    """T-1114 / T-AUGGIE-AT-MOST-ONCE / INV-R2 (FR-9.3): the fallback INVOKES
    `/sc:auggie-review` (the core decides to invoke via the `invoke_auggie_review` seam),
    and does so EXACTLY once.

    NON-VACUOUS cross-entry test: drives `_run_fallback` TWICE against the SAME
    `SkillResult` (simulating a second decline observation re-entering the fallback) and
    asserts the `invoke_auggie_review` recorder fires EXACTLY once — genuinely exercising
    the `if not result.auggie_review_invoked` strict-once guard (a second-entry double
    invoke, the exact thing the flag exists to prevent, would otherwise slip through).
    The durable cross-RESUME strict-once is separately covered by test_idempotency T-1124.
    """
    calls: list[dict] = []
    config = RunConfig(
        monitor_ordinal=3,
        max_rounds=2,
        review_state="declined",
        fallback_findings=[_ff(88)],
        invoke_auggie_review=lambda **kw: calls.append(kw),
    )
    # First engagement via the full run_skill path.
    result = run_skill(config)
    assert result.auggie_review_invoked is True
    assert len(calls) == 1
    # Second engagement on the SAME result (a later decline re-enters _run_fallback)
    # → the strict-once flag must SUPPRESS a second invoke.
    _run_fallback(result, config)
    assert (
        len(calls) == 1
    )  # STILL exactly once — strict-once guard held across re-entry

    # And a fresh result (no prior invoke) DOES invoke — proving the guard is the cause,
    # not an inert recorder.
    fresh = SkillResult()
    _run_fallback(fresh, config)
    assert len(calls) == 2 and fresh.auggie_review_invoked is True


@pytest.mark.inv
def test_t1121_clamp_to_one_on_fallback_engage():
    """T-1121 / FR-10.2 / INV-R3: engaging the fallback clamps `effective_max_rounds` to 1
    (`min(max_rounds, 1)`, monotone non-increasing)."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=5,  # a large budget...
            review_state="declined",
            fallback_findings=[_ff(88)],
        )
    )
    assert result.effective_max_rounds == 1  # ...clamped to 1 on fallback engage


@pytest.mark.inv
def test_t1123_single_shot_fallback_no_loopback(load_fixture):
    """T-1123: the fallback runs ONE remediation cycle (fallback_round_counter == 1),
    invokes auggie once, and terminates — no loop-back, no second invoke."""
    fx = load_fixture("auggie-fallback-findings.json")
    findings = [Finding(**{k: v for k, v in d.items()}) for d in fx["findings"]]
    calls: list[dict] = []
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            review_state="declined",
            fallback_findings=findings,
            invoke_auggie_review=lambda **kw: calls.append(kw),
        )
    )
    assert (
        result.fallback_round_counter == fx["expected"]["fallback_round_counter"] == 1
    )
    assert result.effective_max_rounds == fx["expected"]["effective_max_rounds"] == 1
    assert len(calls) == fx["expected"]["auggie_review_invoked_count"] == 1
    assert result.state in (MonitorState.TERMINAL_CLEAN, MonitorState.HALT_MAX_ROUNDS)


@pytest.mark.inv
def test_fallback_invocation_is_pr_targeted_and_records_posted_output():
    """S5b invokes PR-targeted auggie-review, posts to PR, and suppresses remediation offer."""
    calls: list[dict] = []

    def invoke(**kw):
        calls.append(kw)
        return {
            "pr_review_url": "https://github.com/IronbellyOrg/IronClaude/pull/188#issuecomment-77",
            "comment_id": 77,
        }

    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            pr_number=188,
            review_state="declined",
            fallback_findings=[_ff(88)],
            invoke_auggie_review=invoke,
        )
    )

    assert calls == [
        {
            "pr_number": 188,
            "target": 188,
            "post_pr": True,
            "no_remediation_offer": True,
        }
    ]
    assert (
        result.fallback_review_url
        == "https://github.com/IronbellyOrg/IronClaude/pull/188#issuecomment-77"
    )
    assert result.fallback_review_comment_id == 77


@pytest.mark.inv
def test_fallback_only_findings_post_one_pr_followup_without_inline_resolution():
    """Fallback-only findings with no inline ids reply once and skip inline resolution."""
    replies: list[dict] = []
    resolves: list[dict] = []
    fallback_finding = _ff(88, comment_id=None)

    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            pr_number=188,
            review_state="declined",
            fallback_findings=[fallback_finding],
            invoke_auggie_review=lambda **_: {
                "review_url": "https://example.test/fallback",
                "comment_id": 901,
            },
            do_reply=lambda **kw: replies.append(kw),
            do_resolve=lambda **kw: resolves.append(kw),
        )
    )

    assert result.reply_count == 1
    assert len(replies) == 1
    assert replies[0]["fallback_only"] is True
    assert replies[0]["fallback_review_url"] == "https://example.test/fallback"
    assert replies[0]["fallback_review_comment_id"] == 901
    assert resolves == []


@pytest.mark.inv
def test_inline_fallback_findings_keep_normal_resolution_path():
    """Findings with inline ids still use the normal reply plus resolve path."""
    replies: list[dict] = []
    resolves: list[dict] = []

    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            pr_number=188,
            review_state="declined",
            fallback_findings=[_ff(88)],
            do_reply=lambda **kw: replies.append(kw),
            do_resolve=lambda **kw: resolves.append(kw),
        )
    )

    assert result.reply_count == 1
    assert replies[0]["fallback_only"] is False
    assert len(resolves) == 1


@pytest.mark.inv
def test_t1125_round_counter_frozen_two_independent_counters():
    """T-1125 / INV-R3: `round_counter` is FROZEN at fallback entry; the fallback advances
    only `fallback_round_counter`. The two counters are independent."""
    # One attributed Augment round (round_counter→1), THEN a decline → fallback.
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_findings=[[_f(2)]],
            rereview_outcome=["attributed", "declined"],
            fallback_findings=[_ff(88)],
        )
    )
    assert result.round_counter == 1  # frozen at the value reached BEFORE the fallback
    assert result.fallback_round_counter == 1  # the fallback's own cycle
    assert result.fallback_engaged is True


@pytest.mark.inv
def test_t1122_total_push_bound_inv_r2():
    """T-1122 / FR-10.3 / INV-R2 / AC-21: the single-shot fallback sub-loop contributes
    AT MOST one push, so `push_count <= max_rounds + 1` for the whole run."""
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            findings=[_f(1)],
            rereview_findings=[[_f(2)]],
            rereview_outcome=["attributed", "declined"],
            fallback_findings=[_ff(88)],
        )
    )
    # Worst case: 2 main pushes (attributed cycle 0 + declined cycle 1) + 1 fallback push.
    # Assert the BOUNDARY is reached EXACTLY (push_count == max_rounds + 1) — proving the
    # fallback contributes EXACTLY one push (a loose `<= 3` would not catch a suppressed
    # fallback push). 2 main pushes happened before the fallback; the fallback adds the 1.
    assert result.push_count == 2 + 1  # == max_rounds + 1 (tight INV-R2 boundary)
    assert result.fallback_round_counter == 1  # the fallback's single push cycle


@pytest.mark.inv
def test_t1116_fallback_findings_pass_verify_before_remediate():
    """T-1116 (FR-9.4): the fallback findings are NOT trusted verbatim — they re-enter
    verify-before-remediate, which gates the push.

    ISOLATES the fallback's verify gate: the fallback finding is fully VERIFIED + in-diff
    (so the downstream `apply_edits` filter would accept it and push), but an injected
    `verify` seam REJECTS it. The resulting `push_count == 0` is therefore held ONLY by the
    fallback's verify-before-remediate gate — not by `apply_edits` — proving FR-9.4 is the
    cause. A control case (verify accepts) confirms the same finding WOULD push otherwise.
    """
    # Verify gate REJECTS → the fallback drops the finding before any push (FR-9.4).
    rejected = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            review_state="declined",
            fallback_findings=[
                _ff(88)
            ],  # verified + in_diff (apply_edits would push it)
            verify=lambda _f: False,  # ...but verify-before-remediate rejects it
        )
    )
    assert rejected.push_count == 0  # held by the VERIFY gate, not apply_edits
    assert rejected.fallback_engaged is True
    assert rejected.state == MonitorState.TERMINAL_CLEAN

    # Control: the SAME finding WITH verify accepting → it does push (proving the gate is
    # what blocked above, not an intrinsically unpushable finding).
    accepted = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=2,
            review_state="declined",
            fallback_findings=[_ff(88)],
            verify=lambda _f: True,
        )
    )
    assert accepted.push_count == 1  # same finding pushes once when verify accepts


# --- dual-surface coverage: transition() table edges (R1+R2) ------------------
# run_skill() is the imperative run-to-terminal driver and does NOT call transition();
# transition() is the SEPARATE declarative FSM-topology surface. This test exercises
# transition()'s 6 V1.1 edges directly so the two surfaces are pinned together and a
# future transition()-side drift is caught (the dual-surface gate's mandate).


@pytest.mark.inv
def test_transition_v11_edges():
    """transition() topology: the 6 V1.1 edges + the byte-identical INV-001 edge."""
    ms = MonitorState
    # MOD: RESOLVING/resolved retargets to S5a (re-trigger BEFORE awaiting re-review).
    assert transition(ms.RESOLVING, "resolved") == ms.S5A_RETRIGGER_REVIEW
    # ADD: S5a/retriggered → await the re-review.
    assert transition(ms.S5A_RETRIGGER_REVIEW, "retriggered") == ms.S5_AWAITING_REREVIEW
    # PRESERVED INV-001 edge — byte-identical S5→S2 on an attributed re-review.
    assert transition(ms.S5_AWAITING_REREVIEW, "rereview_attributed") == ms.S2_CLASSIFY
    # PRESERVED sibling: timeout → terminal.
    assert transition(ms.S5_AWAITING_REREVIEW, "timeout") == ms.TERMINAL_TIMEOUT
    # ADD: declines (at S5 re-trigger poll AND at the initial S2 poll) → fallback.
    assert transition(ms.S5_AWAITING_REREVIEW, "declined") == ms.S5B_AUGGIE_FALLBACK
    assert transition(ms.S2_CLASSIFY, "declined") == ms.S5B_AUGGIE_FALLBACK
    # ADD: fallback re-enters classification once.
    assert transition(ms.S5B_AUGGIE_FALLBACK, "fallback_findings") == ms.S2_CLASSIFY
    # ADD: fallback_skip terminal selector AGREES with _run_fallback's residual logic.
    assert transition(ms.S5B_AUGGIE_FALLBACK, "fallback_skip") == ms.TERMINAL_CLEAN
    assert (
        transition(
            ms.S5B_AUGGIE_FALLBACK,
            "fallback_skip",
            {"fallback_residual_findings": [object()]},
        )
        == ms.HALT_MAX_ROUNDS
    )
    # needs_human pre-gate still short-circuits AHEAD of the new V1.1 routing.
    assert (
        transition(ms.S2_CLASSIFY, "declined", {"needs_human_decision": True})
        == ms.HALT_HUMAN
    )
