"""P0 Eval: Finding Lifecycle Chain.

Tests that a Finding object flows correctly through all 4 pipeline stages:
spec-fidelity → deviation-analysis → remediation → certification.

Verifies: ID stability, severity preservation, status transitions,
source_layer propagation, and routing correctness across subsystem boundaries.

Merged from proposed Evals 3 (Spec-Fidelity Chain) + 10 (Cross-Gate Data Flow)
per adversarial debate consensus.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.roadmap.gates import (
    CERTIFY_GATE,
    DEVIATION_ANALYSIS_GATE,
    REMEDIATE_GATE,
    SPEC_FIDELITY_GATE,
)
from superclaude.cli.roadmap.models import Finding


def _finding(
    id: str = "F-001",
    severity: str = "HIGH",
    deviation_class: str = "SLIP",
    source_layer: str = "structural",
    status: str = "PENDING",
) -> Finding:
    return Finding(
        id=id,
        severity=severity,
        dimension="completeness",
        description="Test finding",
        location="spec:3.1",
        evidence="Missing requirement",
        fix_guidance="Add requirement",
        files_affected=["src/foo.py"],
        status=status,
        deviation_class=deviation_class,
        source_layer=source_layer,
    )


def _write_spec_fidelity_report(
    path: Path,
    high: int = 0,
    medium: int = 0,
    low: int = 0,
    validation_complete: bool = True,
    tasklist_ready: bool = True,
) -> None:
    total = high + medium + low
    content = textwrap.dedent(f"""\
        ---
        high_severity_count: {high}
        medium_severity_count: {medium}
        low_severity_count: {low}
        total_deviations: {total}
        validation_complete: {"true" if validation_complete else "false"}
        tasklist_ready: {"true" if tasklist_ready else "false"}
        ---

        ## Spec Fidelity Analysis

        - Finding F-001: severity={("HIGH" if high > 0 else "MEDIUM")}
        - Finding F-002: severity=MEDIUM
        - Finding F-003: severity=LOW

        ## Details

    """)
    content += "\n".join(f"- Detail line {i}" for i in range(30))
    path.write_text(content)


def _write_deviation_report(
    path: Path,
    total: int = 3,
    slips: int = 1,
    intentional: int = 1,
    pre_approved: int = 1,
    ambiguous: int = 0,
    slip_ids: str = "DEV-001",
    no_action_ids: str = "DEV-003",
    analysis_complete: bool = True,
) -> None:
    content = textwrap.dedent(f"""\
        ---
        schema_version: 1.0
        total_analyzed: {total}
        slip_count: {slips}
        intentional_count: {intentional}
        pre_approved_count: {pre_approved}
        ambiguous_count: {ambiguous}
        ambiguous_deviations: {ambiguous}
        routing_fix_roadmap: {slip_ids}
        routing_no_action: {no_action_ids}
        analysis_complete: {"true" if analysis_complete else "false"}
        ---

        ## Deviation Analysis Report

        - DEV-001: SLIP -- structural completeness
        - DEV-002: INTENTIONAL -- design decision
        - DEV-003: PRE_APPROVED -- accepted variance

        ## Routing Summary

    """)
    content += "\n".join(f"- Analysis line {i}" for i in range(30))
    path.write_text(content)


def _write_remediation_report(
    path: Path,
    total: int = 3,
    actionable: int = 2,
    skipped: int = 1,
    statuses: list[str] | None = None,
) -> None:
    if statuses is None:
        statuses = ["FIXED", "FIXED"]
    items = []
    for i, status in enumerate(statuses):
        items.append(f"- [ ] F-{i+1:03d} | src/file{i}.py | {status} -- Applied fix {i+1}")
    items.append(f"- [x] F-{len(statuses)+1:03d} | src/skip.py | SKIPPED -- Out of scope")

    content = textwrap.dedent(f"""\
        ---
        type: remediation-tasklist
        source_report: spec-fidelity.md
        source_report_hash: abc123def456
        total_findings: {total}
        actionable: {actionable}
        skipped: {skipped}
        ---

        ## Remediation Tasklist

    """)
    content += "\n".join(items)
    path.write_text(content)


def _write_certification_report(
    path: Path,
    verified: int = 3,
    passed: int = 3,
    failed: int = 0,
    certified: bool = True,
    finding_rows: list[tuple[str, str, str, str]] | None = None,
) -> None:
    if finding_rows is None:
        finding_rows = [
            ("F-001", "HIGH", "PASS", "Fix verified"),
            ("F-002", "MEDIUM", "PASS", "Fix verified"),
            ("F-003", "LOW", "PASS", "Fix verified"),
        ]
    rows = "\n".join(
        f"| {fid} | {sev} | {res} | {just} |" for fid, sev, res, just in finding_rows
    )
    lines = [
        "---",
        f"findings_verified: {verified}",
        f"findings_passed: {passed}",
        f"findings_failed: {failed}",
        f"certified: {'true' if certified else 'false'}",
        "certification_date: 2026-03-19",
        "---",
        "",
        "## Certification Results",
        "",
        "| Finding | Severity | Result | Justification |",
        "|---------|----------|--------|---------------|",
        rows,
        "",
        "## Summary",
        "",
    ]
    lines.extend(f"- Certification line {i}" for i in range(20))
    path.write_text("\n".join(lines))


class TestScenarioZeroDeviations:
    """Scenario A: Zero deviations → fast-path certification."""

    def test_spec_fidelity_passes_clean(self, tmp_path):
        f = tmp_path / "spec-fidelity.md"
        _write_spec_fidelity_report(f, high=0, medium=0, low=0)
        passed, reason = gate_passed(f, SPEC_FIDELITY_GATE)
        assert passed, f"Clean spec-fidelity should pass: {reason}"

    def test_clean_certification(self, tmp_path):
        f = tmp_path / "certify.md"
        _write_certification_report(f, verified=0, passed=0, failed=0, finding_rows=[
            ("F-000", "LOW", "PASS", "No deviations found"),
        ])
        passed, reason = gate_passed(f, CERTIFY_GATE)
        assert passed, f"Clean certification should pass: {reason}"


class TestScenarioSlipsOnly:
    """Scenario B: SLIPs only → remediate → certify."""

    def test_spec_fidelity_blocks_on_high(self, tmp_path):
        f = tmp_path / "spec-fidelity.md"
        _write_spec_fidelity_report(f, high=2, medium=1, low=0, tasklist_ready=False)
        passed, reason = gate_passed(f, SPEC_FIDELITY_GATE)
        assert not passed, "Spec-fidelity should block with HIGH findings"

    def test_deviation_routes_slips_to_fix(self, tmp_path):
        f = tmp_path / "deviation.md"
        _write_deviation_report(
            f, total=2, slips=2, intentional=0, pre_approved=0,
            slip_ids="DEV-001 DEV-002", no_action_ids="",
        )
        passed, reason = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert passed, f"SLIP-only deviation should pass: {reason}"

    def test_remediation_with_all_fixed(self, tmp_path):
        f = tmp_path / "remediate.md"
        _write_remediation_report(f, total=2, actionable=2, skipped=0, statuses=["FIXED", "FIXED"])
        passed, reason = gate_passed(f, REMEDIATE_GATE)
        assert passed, f"All-fixed remediation should pass: {reason}"

    def test_certification_after_remediation(self, tmp_path):
        f = tmp_path / "certify.md"
        _write_certification_report(f, verified=2, passed=2, failed=0, finding_rows=[
            ("F-001", "HIGH", "PASS", "SLIP remediated"),
            ("F-002", "HIGH", "PASS", "SLIP remediated"),
        ])
        passed, reason = gate_passed(f, CERTIFY_GATE)
        assert passed, f"Post-remediation certification should pass: {reason}"


class TestScenarioMixedTypes:
    """Scenario C: Mixed SLIP + INTENTIONAL + PRE_APPROVED → only SLIPs remediated."""

    def test_deviation_excludes_non_slips(self, tmp_path):
        """INTENTIONAL and PRE_APPROVED should route to no_action."""
        f = tmp_path / "deviation.md"
        _write_deviation_report(
            f, total=4, slips=1, intentional=2, pre_approved=1, ambiguous=0,
            slip_ids="DEV-001", no_action_ids="DEV-003 DEV-004",
        )
        passed, reason = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert passed, f"Mixed deviation should pass: {reason}"

    def test_finding_model_preserves_deviation_class(self):
        """Finding.deviation_class is preserved through lifecycle."""
        slip = _finding(id="F-001", deviation_class="SLIP")
        intentional = _finding(id="F-002", deviation_class="INTENTIONAL")
        pre_approved = _finding(id="F-003", deviation_class="PRE_APPROVED")

        assert slip.deviation_class == "SLIP"
        assert intentional.deviation_class == "INTENTIONAL"
        assert pre_approved.deviation_class == "PRE_APPROVED"

    def test_finding_source_layer_preserved(self):
        """source_layer persists through status transitions."""
        f = _finding(source_layer="structural", status="PENDING")
        assert f.source_layer == "structural"

        # Simulate lifecycle: PENDING → ACTIVE → FIXED
        f2 = Finding(
            id=f.id, severity=f.severity, dimension=f.dimension,
            description=f.description, location=f.location,
            evidence=f.evidence, fix_guidance=f.fix_guidance,
            status="ACTIVE", source_layer=f.source_layer,
            deviation_class=f.deviation_class,
        )
        assert f2.source_layer == "structural"
        assert f2.status == "ACTIVE"

        f3 = Finding(
            id=f.id, severity=f.severity, dimension=f.dimension,
            description=f.description, location=f.location,
            evidence=f.evidence, fix_guidance=f.fix_guidance,
            status="FIXED", source_layer=f.source_layer,
            deviation_class=f.deviation_class,
        )
        assert f3.source_layer == "structural"
        assert f3.status == "FIXED"


class TestScenarioAmbiguousBlocks:
    """Scenario D: AMBIGUOUS deviation blocks the pipeline."""

    def test_ambiguous_blocks_deviation_gate(self, tmp_path):
        f = tmp_path / "deviation.md"
        _write_deviation_report(
            f, total=3, slips=1, intentional=1, pre_approved=0, ambiguous=1,
            slip_ids="DEV-001", no_action_ids="",
        )
        passed, reason = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed, "AMBIGUOUS deviation should block gate"
        assert "ambiguous" in reason.lower()

    def test_ambiguous_zero_required(self, tmp_path):
        """Even one ambiguous finding blocks the entire pipeline."""
        f = tmp_path / "deviation.md"
        _write_deviation_report(
            f, total=1, slips=0, intentional=0, pre_approved=0, ambiguous=1,
            slip_ids="", no_action_ids="",
        )
        passed, reason = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed


class TestScenarioRemediationExhaustion:
    """Scenario E: Remediation budget exhaustion."""

    def test_failed_remediation_still_valid_format(self, tmp_path):
        """A remediation with FAILED items is still structurally valid."""
        f = tmp_path / "remediate.md"
        _write_remediation_report(
            f, total=3, actionable=2, skipped=1,
            statuses=["FAILED", "FAILED"],
        )
        passed, reason = gate_passed(f, REMEDIATE_GATE)
        assert passed, f"FAILED status is terminal and valid: {reason}"

    def test_pending_remediation_blocks(self, tmp_path):
        """PENDING items block the remediation gate."""
        f = tmp_path / "remediate.md"
        _write_remediation_report(
            f, total=3, actionable=2, skipped=1,
            statuses=["PENDING", "FIXED"],
        )
        passed, reason = gate_passed(f, REMEDIATE_GATE)
        assert not passed, "PENDING findings should block remediation gate"

    def test_certification_rejects_failed(self, tmp_path):
        """Certification gate rejects if certified=false."""
        f = tmp_path / "certify.md"
        _write_certification_report(
            f, verified=3, passed=1, failed=2, certified=False,
            finding_rows=[
                ("F-001", "HIGH", "FAIL", "Not resolved"),
                ("F-002", "HIGH", "FAIL", "Not resolved"),
                ("F-003", "LOW", "PASS", "Verified"),
            ],
        )
        passed, reason = gate_passed(f, CERTIFY_GATE)
        assert not passed, "Uncertified report should not pass gate"


class TestFindingStatusTransitions:
    """Verify Finding model enforces valid status values."""

    @pytest.mark.parametrize("status", ["PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED"])
    def test_valid_statuses(self, status):
        f = _finding(status=status)
        assert f.status == status

    @pytest.mark.parametrize("status", ["OPEN", "CLOSED", "RESOLVED", "IN_PROGRESS", ""])
    def test_invalid_statuses_rejected(self, status):
        with pytest.raises(ValueError, match="Invalid Finding status"):
            _finding(status=status)

    @pytest.mark.parametrize("cls", ["SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"])
    def test_valid_deviation_classes(self, cls):
        f = _finding(deviation_class=cls)
        assert f.deviation_class == cls

    @pytest.mark.parametrize("cls", ["UNKNOWN", "APPROVED", "REJECTED", ""])
    def test_invalid_deviation_classes_rejected(self, cls):
        with pytest.raises(ValueError, match="Invalid deviation_class"):
            _finding(deviation_class=cls)


class TestSpecFidelityConsistency:
    """Spec-fidelity gate consistency invariants."""

    def test_tasklist_ready_true_requires_zero_high(self, tmp_path):
        """tasklist_ready=true with high>0 is inconsistent."""
        f = tmp_path / "sf.md"
        _write_spec_fidelity_report(f, high=1, tasklist_ready=True, validation_complete=True)
        passed, _ = gate_passed(f, SPEC_FIDELITY_GATE)
        assert not passed

    def test_tasklist_ready_false_always_consistent(self, tmp_path):
        """tasklist_ready=false is always consistent regardless of counts."""
        f = tmp_path / "sf.md"
        _write_spec_fidelity_report(f, high=5, medium=3, low=1, tasklist_ready=False)
        # The gate will fail on high_severity_count_zero, NOT on tasklist_ready_consistent
        passed, reason = gate_passed(f, SPEC_FIDELITY_GATE)
        assert not passed
        assert "high_severity_count" in reason.lower()

    def test_tasklist_ready_true_requires_validation_complete(self, tmp_path):
        """tasklist_ready=true with validation_complete=false is inconsistent."""
        f = tmp_path / "sf.md"
        _write_spec_fidelity_report(f, high=0, tasklist_ready=True, validation_complete=False)
        passed, _ = gate_passed(f, SPEC_FIDELITY_GATE)
        assert not passed


class TestDeviationRoutingInvariants:
    """Deviation analysis routing invariants."""

    def test_slip_count_must_match_routing_ids(self, tmp_path):
        """slip_count != len(routing_fix_roadmap IDs) fails."""
        f = tmp_path / "da.md"
        _write_deviation_report(f, total=3, slips=2, intentional=1, pre_approved=0,
                                slip_ids="DEV-001", no_action_ids="")  # Only 1 ID but slip_count=2
        passed, _ = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed

    def test_total_must_equal_sum_of_categories(self, tmp_path):
        """total_analyzed != sum of categories fails."""
        f = tmp_path / "da.md"
        _write_deviation_report(f, total=99, slips=1, intentional=1, pre_approved=1,
                                slip_ids="DEV-001", no_action_ids="DEV-003")
        passed, _ = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed

    def test_analysis_incomplete_blocks(self, tmp_path):
        """analysis_complete=false blocks the gate."""
        f = tmp_path / "da.md"
        _write_deviation_report(f, analysis_complete=False,
                                slip_ids="DEV-001", no_action_ids="DEV-003")
        passed, _ = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed
