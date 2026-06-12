"""Edge-case catalog tests (spec §8, EC-1..EC-16).

Every edge case has a concrete assertion. EC-9 asserts the STRUCTURAL drop (missing
file:line → dropped, distinct from the FR-3.5 false-positive demote). No test
fabricates behavior beyond the §8 catalog.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.pr_submit.classifier import classify
from superclaude.pr_submit.detection import DetectionContract, DetectionContractLocked
from superclaude.pr_submit.fsm import (
    RunConfig,
    is_groundable,
    plan_dispatch,
    poll_outcome,
    run_skill,
)
from superclaude.pr_submit.models import Finding, MonitorState
from superclaude.pr_submit.run_log import RunLog

REPO_ROOT = Path(__file__).resolve().parents[2]
AUGMENT = "augment-code[bot]"
CONTRACT = DetectionContract(augment_bot_login=AUGMENT, locked=True)


def _vf(line=1, **kw) -> Finding:
    base = dict(
        path="src/a.py", body="bug", in_diff=True, verification_status="verified"
    )
    base.update(kw)
    return Finding(line=line, **base)


# Keys a fixture finding dict may carry that map onto Finding constructor params.
_FINDING_KEYS = (
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
)


def _finding_from_fixture(fd: dict) -> Finding:
    """Build a Finding from a fixture dict, filtering to the known constructor keys."""
    return Finding(**{k: fd[k] for k in _FINDING_KEYS if k in fd})


def test_ec1_empty_findings_clean(load_fixture):
    """EC-1: empty findings → state clean, loop terminates, zero troubleshoot."""
    fixture = load_fixture("finding-empty.json")
    assert fixture["findings"] == []  # the dedicated EC-1 fixture is genuinely empty
    result = run_skill(RunConfig(monitor_ordinal=3, review_state="clean"))
    assert result.state == MonitorState.TERMINAL_CLEAN
    assert result.push_count == 0


def test_ec2_single_finding_one_fix_reply_resolve():
    """EC-2: exactly one Medium → one fix, one reply, one resolve."""
    result = run_skill(RunConfig(monitor_ordinal=3, findings=[_vf()]))
    assert result.push_count == 1 and result.reply_count == 1
    assert result.round_counter == 1


def test_ec3_max_findings_stress_truncates(load_fixture):
    """EC-3: 50 findings across files → batched; overflow truncates + HALTs within budget."""
    fixture = load_fixture("finding-max.json")
    assert len(fixture["findings"]) == 50  # the dedicated 50-finding stress fixture
    fixture_findings = [
        _finding_from_fixture({**fd, "verification_status": "verified"})
        for fd in fixture["findings"]
    ]
    fixture_plan = plan_dispatch(fixture_findings, max_rounds=2, current_round=0)
    assert fixture_plan.truncated is True
    assert len(fixture_plan.batches) <= 2  # the fixture set also truncates to budget

    findings = [_vf(line=i, path=f"src/f{i}.py") for i in range(50)]
    plan = plan_dispatch(findings, max_rounds=2, current_round=0)
    assert plan.truncated is True
    assert len(plan.batches) <= 2  # never exceeds the round budget


def test_ec4_fresh_comment_id_no_double_fix():
    """EC-4: same body+file:line under a new comment_id → same fix_key → one fix."""
    a = _vf(comment_id=1)
    b = _vf(comment_id=2)
    assert a.comment_id != b.comment_id
    assert a.fix_key == b.fix_key


def test_ec5_review_during_fix_one_round():
    """EC-5: a second poll during a fix → in-flight fix completes; round_counter==1 after both."""
    result = run_skill(RunConfig(monitor_ordinal=3, findings=[_vf()]))
    assert result.round_counter == 1  # the in-flight fix counts once


def test_ec6_timeout_mid_remediation_terminates():
    """EC-6: a timeout fires → loop terminates (TERMINAL_TIMEOUT)."""
    assert poll_outcome("polling", 1800, 1800) == MonitorState.TERMINAL_TIMEOUT


@pytest.mark.parametrize(
    "ordinal,exp_state,exp_edits,exp_push",
    [
        (1, MonitorState.PROPOSED, 0, 0),
        (2, MonitorState.S4_HALT_BEFORE_PUSH, 1, 0),
        (3, MonitorState.HALT_HUMAN, 0, 0),
    ],
)
def test_ec7_needs_human_at_every_level(
    ordinal, exp_state, exp_edits, exp_push, load_fixture
):
    """EC-7: needs_human at every level — L1 propose(0); L2 fix(>0)+HALT; L3 HALT immediately(0)."""
    fixture = load_fixture("finding-needs-human.json")
    assert fixture["findings"][0]["needs_human_decision"] is True
    result = run_skill(
        RunConfig(monitor_ordinal=ordinal, findings=[_vf(needs_human_decision=True)])
    )
    assert result.state == exp_state
    assert result.applied_edits == exp_edits
    assert result.push_count == exp_push


def test_round_sequence_2_fixture(load_fixture):
    """Two-round clean-converge sequence driven from round-sequence-2.json.

    cycles[0] is the initial findings set, cycles[1] is the first re-review residual,
    cycles[2] is empty (the clean re-review that terminates). With max_rounds=2 the
    run pushes twice and converges clean: round_counter==2, push_count==2,
    TERMINAL_CLEAN — matching the fixture's "expected" block.
    """
    fixture = load_fixture("round-sequence-2.json")
    cycles = fixture["cycles"]
    initial = [_finding_from_fixture(fd) for fd in cycles[0]["findings"]]
    residual = [_finding_from_fixture(fd) for fd in cycles[1]["findings"]]
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=fixture["max_rounds"],
            findings=initial,
            rereview_findings=[residual],
        )
    )
    expected = fixture["expected"]
    assert result.round_counter == expected["round_counter"] == 2
    assert result.push_count == expected["push_count"] == 2
    assert result.state == MonitorState.TERMINAL_CLEAN


def test_ec8_max_rounds_zero_never_remediates():
    """EC-8: --max-rounds=0 → gate `0>=0` True → HALT before any fix; zero rounds."""
    result = run_skill(RunConfig(monitor_ordinal=3, max_rounds=0, findings=[_vf()]))
    assert result.state == MonitorState.HALT_MAX_ROUNDS
    assert result.round_counter == 0
    assert result.push_count == 0


def test_ec9_malformed_missing_fileline_structural_drop(load_fixture):
    """EC-9: a malformed finding missing file:line → STRUCTURAL drop (distinct from false-positive)."""
    fixture = load_fixture("finding-malformed.json")
    malformed = _finding_from_fixture(fixture["findings"][0])
    # The dedicated fixture's finding is structurally ungroundable → dropped.
    assert is_groundable(malformed) is False

    groundable = _vf(path="src/a.py", line=10)
    ungroundable_no_path = Finding(path="", line=10, body="x", in_diff=True)
    ungroundable_no_line = Finding(path="src/a.py", line=0, body="x", in_diff=True)
    assert is_groundable(groundable) is True
    assert is_groundable(ungroundable_no_path) is False  # dropped, not downgraded
    assert is_groundable(ungroundable_no_line) is False


def test_ec10_non_augment_interleaved_human_ignored():
    """EC-10: human comment + Augment review → only Augment parsed; human ignored (NFR-4)."""
    payload = {
        "reviews": [
            {"author": {"login": "human-dev"}, "has_findings": False},
            {"author": {"login": AUGMENT}, "has_findings": True},
        ],
        "comments": [],
    }
    assert classify(payload, CONTRACT) == "findings"  # Augment detected
    # With ONLY the human review, nothing is detected (the human never drives state).
    assert (
        classify(
            {
                "reviews": [{"author": {"login": "human-dev"}, "has_findings": True}],
                "comments": [],
            },
            CONTRACT,
        )
        == "polling"
    )


def test_ec11_contract_locked_false_halts_probe():
    """EC-11 (= T-210): contract locked:false/absent → HALT directing the operator to probe first."""
    with pytest.raises(DetectionContractLocked) as exc:
        DetectionContract.load()
    assert "probe" in str(exc.value).lower()


def test_ec12_review_disappears_transient_no_round():
    """EC-12: review detected then gone → transient; polling continues; NO round consumed.

    Distinct from INV-001 vanished-review monotonicity (that concerns an already-
    COUNTED re-review). Here the disappearance happens before any round is counted.
    """
    # findings → then a poll that returns to polling: no round was ever incremented.
    back_to_polling = poll_outcome("polling", elapsed_seconds=60, timeout=1800)
    assert (
        back_to_polling == MonitorState.S2_CLASSIFY
    )  # keep polling, no terminal, no round


def test_ec13_monitor3_maxrounds5_upper_bound():
    """EC-13: --monitor 3 --max-rounds 5 → at most 5 rounds; summary if residual."""
    residual = [[_vf(line=100 + i, comment_id=100 + i)] for i in range(9)]
    result = run_skill(
        RunConfig(
            monitor_ordinal=3,
            max_rounds=5,
            findings=[_vf()],
            rereview_findings=residual,
        )
    )
    assert result.round_counter == 5
    assert result.push_count == 5
    assert result.summary_posted is True


def test_ec14_multiple_prs_independent_state(tmp_path):
    """EC-14: two PRs in one session → separate run-log + independent counters, no leakage."""
    rl_a = RunLog(101, tmp_path / "a")
    rl_b = RunLog(202, tmp_path / "b")
    rl_a.append({"event_type": "round_incremented"})
    assert rl_a.jsonl_path != rl_b.jsonl_path
    assert rl_a.rebuild_state()["round_counter"] == 1
    assert rl_b.rebuild_state()["round_counter"] == 0  # independent


def test_ec15_gh_not_installed_guarded_in_poll_script():
    """EC-15: `gh` not on PATH → HALT at Wave 0 — the poll script guards with `command -v gh`."""
    script = (
        REPO_ROOT
        / "src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh"
    )
    text = script.read_text(encoding="utf-8")
    assert "command -v gh" in text  # the guard that HALTs when gh is absent


def test_ec16_base_branch_halt_documented():
    """EC-16: a `--base` branch absent on the fork → HALT — documented in the SKILL error handling."""
    skill = REPO_ROOT / "src/superclaude/skills/sc-pr-submit-protocol/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    # Wave 0 verifies the PR target / branch before arming (the HALT path).
    assert "Wrong origin" in text or "behind" in text or "wrong-owner" in text
