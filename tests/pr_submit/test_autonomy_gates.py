"""Autonomy-tier gate tests (spec FR-4.1–FR-4.4, §5.3).

The `--monitor` ordinal is a capability ceiling on ONE FSM. These tests prove the
ceiling behaviorally: L1 applies zero edits and proposes "fix these? y/n"; L2
applies edits but never pushes/commits/replies, halting at S4'_HALT_BEFORE_PUSH;
L3 runs the full cycle; the `needs_human_decision` override HALTs at L3; and the
INV-016 predicate-5 zero-edit-no-push gate blocks a push when nothing was applied.
"""

from __future__ import annotations

import pytest

from superclaude.pr_submit.fsm import PROPOSE_PROMPT, RunConfig, run_skill
from superclaude.pr_submit.models import Finding, MonitorState


def _verified(path="src/app.py", line=10, body="off-by-one", **kw) -> Finding:
    return Finding(
        path=path,
        line=line,
        body=body,
        in_diff=True,
        verification_status="verified",
        **kw,
    )


def _finding_from_dict(d: dict) -> Finding:
    """Build a Finding from a fixture dict (only known keys; ignores extras)."""
    keys = {
        "path",
        "line",
        "body",
        "severity_hint",
        "category",
        "confidence",
        "in_diff",
        "comment_id",
        "verification_status",
        "needs_human_decision",
    }
    return Finding(**{k: v for k, v in d.items() if k in keys})


class _Recorder:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, *_a, **_k) -> None:
        self.calls += 1


@pytest.mark.autonomy
@pytest.mark.p0
def test_t401_l1_zero_edits():
    """T-401: at L1, zero edits are applied (no Write/Edit/NotebookEdit)."""
    edit_recorder = _Recorder()
    result = run_skill(
        RunConfig(monitor_ordinal=1, findings=[_verified()], apply_edits=edit_recorder)
    )
    assert result.applied_edits == 0
    assert edit_recorder.calls == 0
    assert result.state == MonitorState.PROPOSED


@pytest.mark.autonomy
def test_t402_l1_emits_exact_proposal():
    """T-402: at L1 the skill emits the exact "fix these? y/n" proposal."""
    result = run_skill(RunConfig(monitor_ordinal=1, findings=[_verified()]))
    assert result.proposal == "fix these? y/n" == PROPOSE_PROMPT


@pytest.mark.autonomy
@pytest.mark.p0
def test_t410_l2_files_modified():
    """T-410: at L2 the diagnosed edits ARE applied in the working tree."""
    result = run_skill(RunConfig(monitor_ordinal=2, findings=[_verified()]))
    assert result.applied_edits >= 1
    assert result.state == MonitorState.S4_HALT_BEFORE_PUSH


@pytest.mark.autonomy
@pytest.mark.p0
def test_t411_t412_t413_l2_no_push_commit_reply():
    """T-411/T-412/T-413: at L2 push/commit and reply are NEVER performed."""
    push_rec, reply_rec, resolve_rec = _Recorder(), _Recorder(), _Recorder()
    result = run_skill(
        RunConfig(
            monitor_ordinal=2,
            findings=[_verified()],
            do_push=push_rec,
            do_reply=reply_rec,
            do_resolve=resolve_rec,
        )
    )
    assert result.push_count == 0  # T-411 (git push never) / T-412 (git commit never)
    assert push_rec.calls == 0
    assert result.reply_count == 0 and reply_rec.calls == 0  # T-413 (reply never)
    assert result.state == MonitorState.S4_HALT_BEFORE_PUSH


@pytest.mark.autonomy
@pytest.mark.p0
def test_t420_l3_full_e2e(load_fixture):
    """T-420: full E2E at L3 — fix, validate, push, reply, resolve (AC-2).

    Uses the finding-medium-high.json fixture (Phase 10). The run pushes, replies,
    and resolves, ending TERMINAL_CLEAN with the round counter ticked once.
    """
    raw = load_fixture("finding-medium-high.json")
    findings = [_finding_from_dict(f) for f in raw["findings"]]
    # Ensure verified+groundable for the E2E happy path.
    for f in findings:
        f.in_diff = True
        f.verification_status = "verified"
    result = run_skill(RunConfig(monitor_ordinal=3, findings=findings))
    assert result.push_count == 1
    assert result.reply_count == 1
    assert result.round_counter == 1
    assert result.state == MonitorState.TERMINAL_CLEAN


@pytest.mark.autonomy
@pytest.mark.p0
def test_t430_l3_needs_human_halts():
    """T-430: at L3, a `needs_human_decision` finding HALTs with no push and no reply (FR-4.4 override)."""
    f = _verified()
    f.needs_human_decision = True
    push_rec, reply_rec = _Recorder(), _Recorder()
    result = run_skill(
        RunConfig(monitor_ordinal=3, findings=[f], do_push=push_rec, do_reply=reply_rec)
    )
    assert result.state == MonitorState.HALT_HUMAN
    assert result.push_count == 0 and push_rec.calls == 0
    assert result.reply_count == 0 and reply_rec.calls == 0


@pytest.mark.autonomy
@pytest.mark.p0
def test_zero_edit_no_push(load_fixture):
    """T-ZERO-EDIT-NO-PUSH: an ungroundable cycle (applied_edits==0) never pushes (INV-016 predicate 5).

    Asserts ALL THREE: push_count==0, push_decision.authorized==False,
    push_decision.predicate_5_applied_edits==0. Uses finding-ungroundable.json.
    """
    raw = load_fixture("finding-ungroundable.json")
    findings = [_finding_from_dict(f) for f in raw["findings"]]
    result = run_skill(RunConfig(monitor_ordinal=3, findings=findings))
    assert result.applied_edits == 0
    assert result.push_count == 0
    assert result.push_decision is not None
    assert result.push_decision.authorized is False
    assert result.push_decision.predicate_5_applied_edits == 0
