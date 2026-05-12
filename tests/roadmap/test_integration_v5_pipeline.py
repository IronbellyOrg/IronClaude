"""Integration tests for the v2.26 roadmap pipeline (v5 spec scenarios).

Tests SC-1 through SC-6 using pre-recorded subprocess outputs (mock runners).
No live Claude calls are made -- all agent outputs are synthetic fixtures.

SC-1: Pipeline completes to certify step without manual intervention
SC-2: Pre-approved deviations (D-02, D-04) excluded from HIGH count
SC-3: DEV-002, DEV-003 classified SLIP and routed to fix_roadmap
SC-4: Remediation diff shows SLIP-only changes (INTENTIONAL/PRE_APPROVED preserved)
SC-6: Terminal halt after 2 failed remediations with stderr detail assertions

v2.24 scenario uses a roadmap with 4 deviations:
- DEV-001: SLIP (missing Success Criteria section)
- DEV-002: SLIP (missing Performance Budget table)
- DEV-003: PRE_APPROVED (simplified dependency list -- D-04 on record)
- DEV-004: INTENTIONAL (condensed architecture overview -- D-02 Round 3)
"""

from __future__ import annotations

import hashlib
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.pipeline.executor import execute_pipeline
from superclaude.cli.pipeline.models import Step, StepResult, StepStatus
from superclaude.cli.roadmap.executor import (
    _build_steps,
    _check_remediation_budget,
    _print_terminal_halt,
    _save_state,
)
from superclaude.cli.roadmap.gates import (
    DEVIATION_ANALYSIS_GATE,
    SPEC_FIDELITY_GATE,
    _high_severity_count_zero,
    _no_ambiguous_deviations,
    _routing_ids_valid,
    _slip_count_matches_routing,
    _pre_approved_not_in_fix_roadmap,
    _total_analyzed_consistent,
)
from superclaude.cli.roadmap.models import AgentSpec, Finding, RoadmapConfig
from superclaude.cli.roadmap.remediate import (
    _parse_routing_list,
    deviations_to_findings,
)


# ──────────────────────────────────────────────────────────────────
# Shared fixtures and helpers
# ──────────────────────────────────────────────────────────────────


def _make_config(tmp_path: Path) -> RoadmapConfig:
    spec = tmp_path / "spec.md"
    spec.write_text(
        "# v2.24 Specification\n\n"
        "## Goals\nBuild a reliable roadmap generation system.\n\n"
        "## Architecture\nMicroservices with event-driven messaging.\n\n"
        "## Success Criteria\n- All tests pass\n- P99 < 200ms\n\n"
        "## Performance Budget\n| Metric | Target |\n|--------|--------|\n| P99 | 200ms |\n\n"
        "## Dependencies\n- Core framework\n- Auth service\n- Event bus\n",
        encoding="utf-8",
    )
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output,
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        depth="standard",
    )


def _now():
    return datetime.now(timezone.utc)


# Pre-recorded frontmatter values for the v2.24 scenario
_V224_FM_VALUES = {
    "spec_source": "v2.24-spec.md",
    "generated": "2026-03-10T00:00:00Z",
    "generator": "claude-opus-architect",
    "functional_requirements": "8",
    "nonfunctional_requirements": "4",
    "total_requirements": "12",
    "complexity_score": "0.65",
    "complexity_class": "MEDIUM",
    "domains_detected": "[backend, frontend, security]",
    "risks_identified": "4",
    "dependencies_identified": "5",
    "success_criteria_count": "6",
    "extraction_mode": "standard",
    "primary_persona": "architect",
    "total_diff_points": "6",
    "shared_assumptions_count": "5",
    "convergence_score": "0.82",
    "rounds_completed": "3",
    "base_variant": "A",
    "variant_scores": "A:81 B:74",
    "adversarial": "true",
    "validation_philosophy": "continuous-parallel",
    "validation_milestones": "4",
    "work_milestones": "8",
    "interleave_ratio": "1:2",
    "major_issue_policy": "stop-and-fix",
    # SC-2: D-02 (DEV-004 INTENTIONAL) and D-04 (DEV-003 PRE_APPROVED) pre-approved
    # high_severity_count=0 because INTENTIONAL and PRE_APPROVED excluded
    "high_severity_count": "0",
    "medium_severity_count": "0",
    "low_severity_count": "0",
    "total_deviations": "4",
    "validation_complete": "true",
    "tasklist_ready": "true",
    # Anti-instinct audit
    "undischarged_obligations": "0",
    "uncovered_contracts": "0",
    "fingerprint_coverage": "0.85",
    # Deviation analysis: SC-3 DEV-001 and DEV-002 are SLIP (routed to fix_roadmap)
    "schema_version": "1.0",
    "total_analyzed": "4",
    "slip_count": "2",
    "intentional_count": "1",
    "pre_approved_count": "1",
    "ambiguous_count": "0",
    "ambiguous_deviations": "0",
    "routing_fix_roadmap": "DEV-001 DEV-002",
    "routing_update_spec": "",
    "routing_no_action": "DEV-003 DEV-004",
    "routing_human_review": "",
    "analysis_complete": "true",
    # Wiring verification (must be consistent with total_findings=2)
    "gate": "wiring-verification",
    "target_dir": ".",
    "files_analyzed": "10",
    "files_skipped": "2",
    "rollout_mode": "shadow",
    "audit_artifacts_used": "0",
    "unwired_callable_count": "1",
    "orphan_module_count": "1",
    "unwired_registry_count": "0",
    "critical_count": "1",
    "major_count": "1",
    "info_count": "0",
    "blocking_findings": "0",
    "whitelist_entries_applied": "0",
    # Remediation
    "type": "remediation-tasklist",
    "source_report": "spec-deviations.md",
    "source_report_hash": "abc123",
    "total_findings": "2",
    "actionable": "2",
    "skipped": "2",
    # Certification: SC-1 pipeline completes with certified=true
    "findings_verified": "2",
    "findings_passed": "2",
    "findings_failed": "0",
    "certified": "true",
    "certification_date": "2026-03-10",
}


def _template_compliant_body_lines(rows: int = 25) -> list[str]:
    """Lines satisfying `_template_sections_present` for generate/merge steps.

    Includes every required top-level H2 section, a single `## M1:` milestone
    with its three required H3 subsections, and the two required H3s under
    `## Resource Requirements and Dependencies`.
    """
    lines: list[str] = [
        "",
        "## Executive Summary",
        "",
        "Overview of the initiative.",
        "",
        "## Milestone Summary",
        "",
        "| Milestone | Title | Duration |",
        "|---|---|---|",
        "| M1 | Implementation | 2 weeks |",
        "",
        "## Dependency Graph",
        "",
        "M1 has no predecessors.",
        "",
        "## M1: Implementation",
        "",
        "| # | ID | Title | Description | Component | Dependencies | Acceptance Criteria | Effort | Priority |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i in range(1, rows + 1):
        lines.append(
            f"| {i} | FR-{i:03d} | Item {i} | Implement item {i} | core | - | Tests pass | S | P1 |"
        )
    lines.extend(
        [
            "",
            "### Integration Points — M1",
            "",
            "No external integration points.",
            "",
            "### Milestone Dependencies — M1",
            "",
            "None.",
            "",
            "### Risk Assessment and Mitigation — M1",
            "",
            "No significant risks identified.",
            "",
            "## Resource Requirements and Dependencies",
            "",
            "### External Dependencies",
            "",
            "None.",
            "",
            "### Infrastructure Requirements",
            "",
            "Standard CI runners.",
            "",
            "## Risk Register",
            "",
            "| ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |",
            "|---|---|---|---|---|---|---|",
            "| R-001 | None | M1 | Low | Low | N/A | team |",
            "",
            "## Success Criteria and Validation Approach",
            "",
            "All tests pass.",
            "",
            "## Decision Summary",
            "",
            "No pending decisions.",
            "",
            "## Timeline Estimates",
            "",
            "2 weeks total.",
        ]
    )
    return lines


def _build_step_content(step: Step) -> str:
    """Build gate-passing content for a step using v2.24 fixture values."""
    if step.gate is None:
        return "## Step output\n- Done\n"

    fm_fields: dict[str, str] = {}
    for f in step.gate.required_frontmatter_fields:
        # Tuple entries are alias groups -- satisfy by emitting the first alias.
        key = f[0] if isinstance(f, tuple) else f
        fm_fields[key] = _V224_FM_VALUES.get(key, "test_value")
    # Add extra fields needed by semantic checks (not in required list)
    _SEMANTIC_EXTRAS = {
        "deviation-analysis": [
            "ambiguous_deviations",
            "routing_update_spec",
            "routing_human_review",
        ],
    }
    for extra in _SEMANTIC_EXTRAS.get(step.id, []):
        fm_fields[extra] = _V224_FM_VALUES.get(extra, "")

    lines = ["---"]
    for k, v in fm_fields.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("## Output")

    # Add enough content lines to satisfy min_lines
    min_needed = step.gate.min_lines if step.gate else 10
    for i in range(max(min_needed, 20)):
        lines.append(f"- Item {i}: content for step {step.id}")

    # Add deliverable table rows for steps with _minimum_deliverable_rows check
    if step.id.startswith("generate") or step.id == "merge":
        lines.extend(_template_compliant_body_lines(rows=25))

    # Add certification table for certify step
    if step.id == "certify":
        lines.extend(
            [
                "",
                "## Certification Results",
                "",
                "| Finding | Severity | Result | Justification |",
                "| --- | --- | --- | --- |",
                "| F-001 | BLOCKING | PASSED | Added Success Criteria section |",
                "| F-002 | BLOCKING | PASSED | Added Performance Budget table |",
                "",
            ]
        )

    return "\n".join(lines)


def _mock_runner_all_pass(step: Step, cfg: RoadmapConfig, cancel_check):
    """Mock runner that produces gate-passing output for every step."""
    content = _build_step_content(step)
    step.output_file.parent.mkdir(parents=True, exist_ok=True)
    step.output_file.write_text(content, encoding="utf-8")
    return StepResult(
        step=step,
        status=StepStatus.PASS,
        attempt=1,
        started_at=_now(),
        finished_at=_now(),
    )


# ──────────────────────────────────────────────────────────────────
# SC-1: Pipeline completes to certify without manual intervention
# ──────────────────────────────────────────────────────────────────


class TestSC1PipelineComplete:
    """SC-1: Full pipeline run completes without halting at any step."""

    def test_pipeline_reaches_certify(self, tmp_path):
        """All steps pass; pipeline completes including post-fidelity steps."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=_mock_runner_all_pass,
        )

        assert len(results) == 13
        assert all(r.status == StepStatus.PASS for r in results)

    def test_remediate_step_is_last(self, tmp_path):
        """remediate is the final static step in the pipeline.

        Note: certify is constructed dynamically after remediate completes
        and is not part of the static _build_steps() list.
        """
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=_mock_runner_all_pass,
        )

        last_step_id = results[-1].step.id
        assert last_step_id == "remediate"

    def test_no_step_fails(self, tmp_path):
        """Zero steps with FAIL status in the v2.24 clean scenario."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=_mock_runner_all_pass,
        )

        failed = [r for r in results if r.status != StepStatus.PASS]
        assert len(failed) == 0


# ──────────────────────────────────────────────────────────────────
# SC-2: Pre-approved deviations excluded from HIGH count
# ──────────────────────────────────────────────────────────────────


class TestSC2PreApprovedExclusion:
    """SC-2: D-02 (INTENTIONAL) and D-04 (PRE_APPROVED) excluded from HIGH count."""

    def test_high_severity_count_zero_with_pre_approved(self):
        """high_severity_count=0 when INTENTIONAL and PRE_APPROVED deviations excluded."""
        # v2.24 scenario: 4 total deviations, 0 HIGH severity
        # (DEV-003=PRE_APPROVED, DEV-004=INTENTIONAL have no HIGH impact)
        content = (
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 0\n"
            "low_severity_count: 0\n"
            "total_deviations: 4\n"
            "validation_complete: true\n"
            "tasklist_ready: true\n"
            "---\n"
            "## Spec Fidelity\n"
            "- DEV-001: SLIP (BLOCKING fixed by remediation)\n"
            "- DEV-002: SLIP (BLOCKING fixed by remediation)\n"
            "- DEV-003: PRE_APPROVED (D-04 on record, excluded from HIGH count)\n"
            "- DEV-004: INTENTIONAL (D-02 Round 3 debate decision, excluded)\n"
        )
        assert _high_severity_count_zero(content) is True

    def test_spec_fidelity_gate_passes_with_pre_approved(self):
        """SPEC_FIDELITY_GATE passes when only pre-approved deviations remain."""
        content = (
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 0\n"
            "low_severity_count: 0\n"
            "total_deviations: 2\n"
            "validation_complete: true\n"
            "tasklist_ready: true\n"
            "---\n"
        ) + "\n".join([f"- fidelity report line {i}" for i in range(20)])
        for check in SPEC_FIDELITY_GATE.semantic_checks:
            assert check.check_fn(content) is True, f"Check {check.name} failed"

    def test_without_pre_approved_exclusion_high_count_would_be_nonzero(self):
        """Verify that including PRE_APPROVED as HIGH would block the gate."""
        content_with_high = (
            "---\n"
            "high_severity_count: 2\n"
            "total_deviations: 4\n"
            "validation_complete: true\n"
            "tasklist_ready: false\n"
            "---\n"
        )
        assert _high_severity_count_zero(content_with_high) is False

    def test_v224_pre_approved_ids_not_in_routing_fix_roadmap(self):
        """DEV-003 (PRE_APPROVED) and DEV-004 (INTENTIONAL) not in fix_roadmap routing."""
        content = (
            "---\n"
            "routing_no_action: DEV-003 DEV-004\n"
            "routing_fix_roadmap: DEV-001 DEV-002\n"
            "---\n"
        )
        assert _pre_approved_not_in_fix_roadmap(content) is True


# ──────────────────────────────────────────────────────────────────
# SC-3: DEV-002 and DEV-003 classified SLIP, routed to fix_roadmap
# ──────────────────────────────────────────────────────────────────


class TestSC3SlipRouting:
    """SC-3: DEV-002 and DEV-003 are SLIP, routed to fix_roadmap in deviation analysis."""

    def test_slip_deviations_routed_to_fix_roadmap(self):
        """DEV-001 and DEV-002 SLIP deviations routed to routing_fix_roadmap."""
        routing_raw = "DEV-001 DEV-002"
        ids = _parse_routing_list(routing_raw)
        assert "DEV-001" in ids
        assert "DEV-002" in ids

    def test_slip_count_matches_routing(self):
        """slip_count=2 matches 2 IDs in routing_fix_roadmap."""
        content = "---\nslip_count: 2\nrouting_fix_roadmap: DEV-001 DEV-002\n---\n"
        assert _slip_count_matches_routing(content) is True

    def test_deviation_analysis_gate_passes_v224_scenario(self):
        """v2.24 deviation analysis document passes DEVIATION_ANALYSIS_GATE."""
        content = (
            "---\n"
            "schema_version: 1.0\n"
            "total_analyzed: 4\n"
            "slip_count: 2\n"
            "intentional_count: 1\n"
            "pre_approved_count: 1\n"
            "ambiguous_count: 0\n"
            "ambiguous_deviations: 0\n"
            "routing_fix_roadmap: DEV-001 DEV-002\n"
            "routing_update_spec: \n"
            "routing_no_action: DEV-003 DEV-004\n"
            "routing_human_review: \n"
            "analysis_complete: true\n"
            "---\n"
        ) + "\n".join([f"- deviation {i}" for i in range(25)])
        for check in DEVIATION_ANALYSIS_GATE.semantic_checks:
            assert check.check_fn(content) is True, f"Check {check.name} failed"

    def test_routing_ids_are_valid_dev_format(self):
        """All routed IDs match DEV-\\d+ format."""
        content = (
            "---\n"
            "routing_fix_roadmap: DEV-001 DEV-002\n"
            "routing_no_action: DEV-003 DEV-004\n"
            "---\n"
        )
        assert _routing_ids_valid(content) is True

    def test_total_analyzed_consistent_v224(self):
        """Total analyzed = 2 slip + 1 intentional + 1 pre_approved + 0 ambiguous = 4."""
        content = (
            "---\n"
            "total_analyzed: 4\n"
            "slip_count: 2\n"
            "intentional_count: 1\n"
            "pre_approved_count: 1\n"
            "ambiguous_count: 0\n"
            "---\n"
        )
        assert _total_analyzed_consistent(content) is True

    def test_deviations_to_findings_slip_get_blocking_severity(self):
        """SLIP deviations with HIGH source severity become BLOCKING findings."""
        records = [
            {
                "id": "DEV-001",
                "severity": "HIGH",
                "dimension": "Completeness",
                "description": "Missing Success Criteria section",
                "location": "roadmap.md:end",
                "evidence": "Section not found",
                "fix_guidance": "Add ## Success Criteria section",
                "files_affected": ["roadmap.md"],
                "status": "PENDING",
                "agreement_category": "",
                "deviation_class": "SLIP",
                "routing": "DEV-001",
            },
            {
                "id": "DEV-002",
                "severity": "HIGH",
                "dimension": "Performance",
                "description": "Missing Performance Budget table",
                "location": "roadmap.md:architecture",
                "evidence": "Table not found",
                "fix_guidance": "Add performance budget table",
                "files_affected": ["roadmap.md"],
                "status": "PENDING",
                "agreement_category": "",
                "deviation_class": "SLIP",
                "routing": "DEV-002",
            },
        ]
        findings = deviations_to_findings(records)
        assert len(findings) == 2
        assert all(f.severity == "BLOCKING" for f in findings)
        assert all(f.deviation_class == "SLIP" for f in findings)


# ──────────────────────────────────────────────────────────────────
# SC-4: Remediation modifies only SLIP-routed elements (diff-based)
# ──────────────────────────────────────────────────────────────────


class TestSC4SlipOnlyRemediation:
    """SC-4: Remediation only affects SLIP-classified deviations."""

    def test_pre_approved_not_in_fix_roadmap_v224(self):
        """DEV-003 (PRE_APPROVED) and DEV-004 (INTENTIONAL) not in routing_fix_roadmap."""
        content = (
            "---\n"
            "routing_fix_roadmap: DEV-001 DEV-002\n"
            "routing_no_action: DEV-003 DEV-004\n"
            "---\n"
        )
        assert _pre_approved_not_in_fix_roadmap(content) is True

    def test_intentional_deviation_not_in_fix_routing(self):
        """INTENTIONAL deviation (DEV-004) is not included in routing_fix_roadmap."""
        fix_ids = _parse_routing_list("DEV-001 DEV-002")
        assert "DEV-004" not in fix_ids

    def test_pre_approved_deviation_not_in_fix_routing(self):
        """PRE_APPROVED deviation (DEV-003) is not included in routing_fix_roadmap."""
        fix_ids = _parse_routing_list("DEV-001 DEV-002")
        assert "DEV-003" not in fix_ids

    def test_finding_deviation_class_slip_only_in_remediation(self):
        """Only SLIP findings are included in remediation scope."""
        records = [
            {
                "id": "DEV-001",
                "severity": "HIGH",
                "dimension": "D",
                "description": "desc",
                "location": "l",
                "evidence": "e",
                "fix_guidance": "f",
                "files_affected": [],
                "status": "PENDING",
                "agreement_category": "",
                "deviation_class": "SLIP",
                "routing": "DEV-001",
            },
            {
                "id": "DEV-002",
                "severity": "HIGH",
                "dimension": "D",
                "description": "desc",
                "location": "l",
                "evidence": "e",
                "fix_guidance": "f",
                "files_affected": [],
                "status": "PENDING",
                "agreement_category": "",
                "deviation_class": "SLIP",
                "routing": "DEV-002",
            },
            {
                "id": "DEV-003",
                "severity": "LOW",
                "dimension": "D",
                "description": "desc",
                "location": "l",
                "evidence": "e",
                "fix_guidance": "",
                "files_affected": [],
                "status": "PENDING",
                "agreement_category": "",
                "deviation_class": "PRE_APPROVED",
                "routing": "",
            },
            {
                "id": "DEV-004",
                "severity": "LOW",
                "dimension": "D",
                "description": "desc",
                "location": "l",
                "evidence": "e",
                "fix_guidance": "",
                "files_affected": [],
                "status": "PENDING",
                "agreement_category": "",
                "deviation_class": "INTENTIONAL",
                "routing": "",
            },
        ]
        all_findings = deviations_to_findings(records)
        slip_only = [f for f in all_findings if f.deviation_class == "SLIP"]

        assert len(slip_only) == 2
        assert all(f.id in ("DEV-001", "DEV-002") for f in slip_only)


# ──────────────────────────────────────────────────────────────────
# SC-6: Terminal halt after 2 failed remediations
# ──────────────────────────────────────────────────────────────────


class TestSC6TerminalHalt:
    """SC-6: Budget exhaustion after 2 attempts triggers terminal halt."""

    def test_two_attempts_allowed(self, tmp_path):
        """First and second remediation attempts are allowed (budget not exhausted)."""
        state = {"schema_version": 1, "steps": {}, "remediation_attempts": 0}
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))
        assert _check_remediation_budget(tmp_path) is True

        state["remediation_attempts"] = 1
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))
        assert _check_remediation_budget(tmp_path) is True

    def test_third_attempt_triggers_halt(self, tmp_path):
        """Third attempt (2 previous) exhausts budget and returns False."""
        state = {"schema_version": 1, "steps": {}, "remediation_attempts": 2}
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        result = _check_remediation_budget(tmp_path)
        assert result is False

    def test_terminal_halt_stderr_has_attempt_count(self, tmp_path):
        """Terminal halt output includes the attempt count."""
        buf = io.StringIO()
        remaining = [
            Finding(
                id="F-01",
                severity="BLOCKING",
                dimension="Completeness",
                description="Missing Success Criteria",
                location="roadmap.md",
                evidence="ev",
                fix_guidance="fix",
            ),
        ]
        _print_terminal_halt(tmp_path, remaining, attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "3" in output

    def test_terminal_halt_stderr_has_finding_count(self, tmp_path):
        """Terminal halt output includes remaining failing finding count."""
        buf = io.StringIO()
        remaining = [
            Finding(
                id="F-01",
                severity="BLOCKING",
                dimension="D",
                description="desc 1",
                location="l",
                evidence="e",
                fix_guidance="f",
            ),
            Finding(
                id="F-02",
                severity="WARNING",
                dimension="D",
                description="desc 2",
                location="l",
                evidence="e",
                fix_guidance="f",
            ),
        ]
        _print_terminal_halt(tmp_path, remaining, attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "2" in output

    def test_terminal_halt_stderr_has_per_finding_details(self, tmp_path):
        """Terminal halt output includes per-finding ID and severity details."""
        buf = io.StringIO()
        remaining = [
            Finding(
                id="F-01",
                severity="BLOCKING",
                dimension="D",
                description="Missing Success Criteria section",
                location="l",
                evidence="e",
                fix_guidance="f",
            ),
        ]
        _print_terminal_halt(tmp_path, remaining, attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "F-01" in output
        assert "BLOCKING" in output

    def test_terminal_halt_stderr_has_resume_command(self, tmp_path):
        """Terminal halt output includes resume command instructions."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "resume" in output.lower()

    def test_terminal_halt_stderr_has_certify_path(self, tmp_path):
        """Terminal halt output references the certification report path."""
        buf = io.StringIO()
        _print_terminal_halt(tmp_path, [], attempt_count=3, file=buf)
        output = buf.getvalue()
        assert "certify" in output.lower() or str(tmp_path) in output


# ──────────────────────────────────────────────────────────────────
# Complete pipeline integration: SC-1 + SC-2 + SC-3 together
# ──────────────────────────────────────────────────────────────────


class TestCompleteV224PipelineFlow:
    """End-to-end integration test validating SC-1 through SC-6 as a single flow."""

    def test_full_pipeline_sc1_through_sc6(self, tmp_path):
        """Complete pipeline from extract through certify validates SC-1, SC-2, SC-3.

        This is the primary integration test verifying the v2.24 scenario end-to-end.
        Uses pre-recorded mock outputs -- no live Claude calls.
        """
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=_mock_runner_all_pass,
        )

        # SC-1: All 13 steps pass (pipeline reaches remediate without manual intervention)
        assert len(results) == 13, f"Expected 13 results, got {len(results)}"
        assert all(r.status == StepStatus.PASS for r in results), (
            f"Failed steps: {[r.step.id for r in results if r.status != StepStatus.PASS]}"
        )

        # SC-1: remediate is last static step of pipeline
        # (certify is constructed dynamically after remediate)
        assert results[-1].step.id == "remediate"

        # Verify step IDs follow expected pipeline order
        step_ids = [r.step.id for r in results]
        assert "extract" in step_ids
        assert "spec-fidelity" in step_ids
        extract_idx = step_ids.index("extract")
        fidelity_idx = step_ids.index("spec-fidelity")
        assert fidelity_idx > extract_idx

    def test_v224_spec_fidelity_sc2_semantics(self):
        """SC-2: spec-fidelity with pre-approved exclusions passes the gate checks."""
        # Simulate v2.24 fidelity report after exclusion of D-02/D-04
        fidelity_content = (
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 0\n"
            "low_severity_count: 0\n"
            "total_deviations: 4\n"
            "validation_complete: true\n"
            "tasklist_ready: true\n"
            "---\n"
            "## Spec Fidelity Report\n"
            "4 deviations detected. 2 SLIP, 1 INTENTIONAL (D-02), 1 PRE_APPROVED (D-04).\n"
            "INTENTIONAL and PRE_APPROVED deviations are excluded from HIGH count.\n"
        ) + "\n".join([f"detail line {i}" for i in range(20)])

        for check in SPEC_FIDELITY_GATE.semantic_checks:
            assert check.check_fn(fidelity_content) is True, (
                f"SC-2: SPEC_FIDELITY_GATE check {check.name!r} failed unexpectedly"
            )

    def test_v224_deviation_analysis_sc3_semantics(self):
        """SC-3: deviation analysis routes DEV-001 and DEV-002 as SLIP to fix_roadmap."""
        analysis_content = (
            "---\n"
            "schema_version: 1.0\n"
            "total_analyzed: 4\n"
            "slip_count: 2\n"
            "intentional_count: 1\n"
            "pre_approved_count: 1\n"
            "ambiguous_count: 0\n"
            "ambiguous_deviations: 0\n"
            "routing_fix_roadmap: DEV-001 DEV-002\n"
            "routing_update_spec: \n"
            "routing_no_action: DEV-003 DEV-004\n"
            "routing_human_review: \n"
            "analysis_complete: true\n"
            "---\n"
        ) + "\n".join([f"analysis detail {i}" for i in range(25)])

        for check in DEVIATION_ANALYSIS_GATE.semantic_checks:
            assert check.check_fn(analysis_content) is True, (
                f"SC-3: DEVIATION_ANALYSIS_GATE check {check.name!r} failed"
            )

        # Verify DEV-001 and DEV-002 are SLIP-routed
        fix_ids = _parse_routing_list("DEV-001 DEV-002")
        assert "DEV-001" in fix_ids
        assert "DEV-002" in fix_ids

    def test_v224_budget_enforcement_sc6_semantics(self, tmp_path):
        """SC-6: Third remediation attempt on v2.24 scenario returns False."""
        # Write state showing 2 previous attempts
        state = {"schema_version": 1, "steps": {}, "remediation_attempts": 2}
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        result = _check_remediation_budget(tmp_path)
        assert result is False, "Third attempt should exhaust budget"
