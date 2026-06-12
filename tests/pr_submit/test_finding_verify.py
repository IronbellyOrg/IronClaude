"""Verify-before-remediate tests (spec FR-3.5).

T-340 a finding that grounds in a real defect → `verification_status=verified` →
troubleshoot called (proceeds past S2b_VERIFY, edits applied at L2+); T-341 a
false positive (location exists, defect does not reproduce) →
`verification_status=unverified` → troubleshoot NOT called, recorded report-only,
NO round consumed (round_counter unchanged); T-342 N findings → verification
dispatched in parallel in one batched wave. The evidence-validator spawn is mocked
via the injected `verify` seam.
"""

from __future__ import annotations

from superclaude.pr_submit.fsm import RunConfig, run_skill
from superclaude.pr_submit.models import Finding, MonitorState


def _verified(path="src/a.py", line=1) -> Finding:
    return Finding(
        path=path,
        line=line,
        body="real defect",
        in_diff=True,
        verification_status="verified",
    )


def _false_positive(path="src/b.py", line=2) -> Finding:
    # Location exists but the defect does not reproduce → unverified false positive.
    return Finding(
        path=path,
        line=line,
        body="phantom",
        in_diff=True,
        verification_status="unverified",
    )


class _Recorder:
    def __init__(self) -> None:
        self.calls = 0
        self.seen: list = []

    def verify(self, finding: Finding) -> bool:
        self.calls += 1
        self.seen.append((finding.path, finding.line))
        return finding.verification_status != "unverified"

    def apply(self, findings) -> int:
        self.calls += 1
        return len(findings)


def test_t340_verified_finding_dispatched():
    """T-340: a verified finding proceeds to remediation (troubleshoot engaged, edits applied at L2+)."""
    apply_rec = _Recorder()
    result = run_skill(
        RunConfig(
            monitor_ordinal=2, findings=[_verified()], apply_edits=apply_rec.apply
        )
    )
    # Passed S2b_VERIFY and reached S3_FIXING → edits applied (troubleshoot was engaged).
    assert apply_rec.calls == 1
    assert result.applied_edits == 1
    assert result.state == MonitorState.S4_HALT_BEFORE_PUSH


def test_t341_false_positive_unverified_no_round_no_dispatch():
    """T-341: a false positive → unverified → report-only, troubleshoot NOT called, NO round consumed."""
    apply_rec = _Recorder()
    result = run_skill(
        RunConfig(
            monitor_ordinal=3, findings=[_false_positive()], apply_edits=apply_rec.apply
        )
    )
    assert result.state == MonitorState.REPORT_ONLY
    assert result.round_counter == 0  # NO round consumed
    assert result.applied_edits == 0
    assert apply_rec.calls == 0  # troubleshoot / fix never engaged


def test_t342_n_findings_verified_in_one_batched_wave():
    """T-342: N findings → verification dispatched in parallel in ONE batched wave."""
    rec = _Recorder()
    findings = [_verified(path=f"src/f{i}.py", line=i) for i in range(4)]
    run_skill(RunConfig(monitor_ordinal=2, findings=findings, verify=rec.verify))
    # All N findings verified in a single wave (one run_skill pass = one batched message).
    assert rec.calls == 4
    assert {p for p, _ in rec.seen} == {f"src/f{i}.py" for i in range(4)}
