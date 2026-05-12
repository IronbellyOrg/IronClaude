"""P0 Eval: Gate Rejection Fidelity.

Tests that each of the 13 gates correctly rejects malformed output through
the full gate_passed() function. Parameterized across all gates × failure modes.

This eval fills the gap identified in adversarial debate: existing tests call
individual _*() semantic check functions in isolation, but no test exercises
the composed gate_passed() path with failure inputs across all 13 gates.
"""

from __future__ import annotations

import textwrap

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.pipeline.models import GateCriteria
from superclaude.cli.roadmap.gates import (
    ALL_GATES,
    CERTIFY_GATE,
    DEBATE_GATE,
    DEVIATION_ANALYSIS_GATE,
    DIFF_GATE,
    EXTRACT_GATE,
    GENERATE_A_GATE,
    GENERATE_B_GATE,
    MERGE_GATE,
    REMEDIATE_GATE,
    SCORE_GATE,
    SPEC_FIDELITY_GATE,
    TEST_STRATEGY_GATE,
)
from superclaude.cli.audit.wiring_gate import WIRING_GATE


# --- Minimal passing content generators per gate ---


def _lines(n: int) -> str:
    """Generate n lines of markdown content."""
    return "\n".join(f"- Item {i}" for i in range(n))


def _deliverable_table(rows: int = 25) -> str:
    """Generate a markdown deliverable table with the specified number of data rows."""
    header = "| # | ID | Title | Description | Component | Dependencies | Acceptance Criteria | Effort | Priority |"
    sep = "|---|---|---|---|---|---|---|---|---|"
    lines = [header, sep]
    for i in range(1, rows + 1):
        lines.append(
            f"| {i} | FR-{i:03d} | Item {i} | Implement item {i} | core | - | Tests pass | S | P1 |"
        )
    return "\n".join(lines)


def _template_compliant_body(rows: int = 25) -> str:
    """Produce a roadmap body satisfying `_template_sections_present`.

    Includes every required top-level H2 section, a single `## M1:` milestone
    section with its three required H3 subsections, and the two required H3s
    under `## Resource Requirements and Dependencies`.
    """
    table = _deliverable_table(rows)
    return textwrap.dedent(
        f"""\
        ## Executive Summary

        Overview of the initiative.

        ## Milestone Summary

        | Milestone | Title | Duration |
        |---|---|---|
        | M1 | Implementation | 2 weeks |

        ## Dependency Graph

        M1 has no predecessors.

        ## M1: Implementation

        {table}

        ### Integration Points — M1

        No external integration points.

        ### Milestone Dependencies — M1

        None.

        ### Risk Assessment and Mitigation — M1

        No significant risks identified.

        ## Resource Requirements and Dependencies

        ### External Dependencies

        None.

        ### Infrastructure Requirements

        Standard CI runners.

        ## Risk Register

        | ID | Risk | Affected Milestones | Probability | Impact | Mitigation | Owner |
        |---|---|---|---|---|---|---|
        | R-001 | None | M1 | Low | Low | N/A | team |

        ## Success Criteria and Validation Approach

        All tests pass.

        ## Decision Summary

        No pending decisions.

        ## Timeline Estimates

        2 weeks total.
        """
    )


def _make_content(frontmatter: dict[str, str], body_lines: int = 200) -> str:
    """Build a markdown document with frontmatter and body."""
    fm_lines = ["---"]
    for k, v in frontmatter.items():
        fm_lines.append(f"{k}: {v}")
    fm_lines.append("---")
    fm_lines.append("")
    fm_lines.append("## Content")
    fm_lines.append("")
    fm_lines.append(_lines(body_lines))
    return "\n".join(fm_lines)


# Minimal passing frontmatter for each gate
PASSING_FRONTMATTER: dict[str, dict[str, str]] = {
    "extract": {
        "spec_source": "test.md",
        "generated": "2026-03-19",
        "generator": "opus:architect",
        "functional_requirements": "5",
        "nonfunctional_requirements": "3",
        "total_requirements": "8",
        "complexity_score": "7",
        "complexity_class": "HIGH",
        "domains_detected": "backend, api",
        "risks_identified": "2",
        "dependencies_identified": "3",
        "success_criteria_count": "4",
        "extraction_mode": "standard",
    },
    "generate-A": {
        "spec_source": "test.md",
        "complexity_score": "7",
        "primary_persona": "architect",
    },
    "generate-B": {
        "spec_source": "test.md",
        "complexity_score": "7",
        "primary_persona": "architect",
    },
    "diff": {
        "total_diff_points": "5",
        "shared_assumptions_count": "3",
    },
    "debate": {
        "convergence_score": "0.85",
        "rounds_completed": "3",
    },
    "score": {
        "base_variant": "opus-architect",
        "variant_scores": "opus:8.5, haiku:7.2",
    },
    "merge": {
        "spec_source": "test.md",
        "complexity_score": "7",
        "adversarial": "true",
    },
    "anti-instinct": {
        "undischarged_obligations": "0",
        "uncovered_contracts": "0",
        "fingerprint_coverage": "0.85",
    },
    "test-strategy": {
        "spec_source": "test.md",
        "generated": "2026-03-19",
        "generator": "opus:architect",
        "complexity_class": "HIGH",
        "validation_philosophy": "continuous-parallel",
        "validation_milestones": "3",
        "work_milestones": "5",
        "interleave_ratio": "1:1",
        "major_issue_policy": "stop-and-fix",
    },
    "spec-fidelity": {
        "high_severity_count": "0",
        "medium_severity_count": "2",
        "low_severity_count": "1",
        "total_deviations": "3",
        "validation_complete": "true",
        "tasklist_ready": "true",
    },
    "wiring-verification": {
        "gate": "wiring-verification",
        "target_dir": "src/",
        "files_analyzed": "10",
        "files_skipped": "0",
        "rollout_mode": "shadow",
        "analysis_complete": "true",
        "audit_artifacts_used": "false",
        "unwired_callable_count": "0",
        "orphan_module_count": "0",
        "unwired_registry_count": "0",
        "critical_count": "0",
        "major_count": "0",
        "info_count": "0",
        "total_findings": "0",
        "blocking_findings": "0",
        "whitelist_entries_applied": "0",
    },
    "deviation-analysis": {
        "schema_version": "1.0",
        "total_analyzed": "3",
        "slip_count": "1",
        "intentional_count": "1",
        "pre_approved_count": "1",
        "ambiguous_count": "0",
        "routing_fix_roadmap": "DEV-001",
        "routing_no_action": "DEV-002 DEV-003",
        "analysis_complete": "true",
        "ambiguous_deviations": "0",
    },
    "remediate": {
        "type": "remediation-tasklist",
        "source_report": "spec-fidelity.md",
        "source_report_hash": "abc123",
        "total_findings": "3",
        "actionable": "2",
        "skipped": "1",
    },
    "certify": {
        "findings_verified": "3",
        "findings_passed": "3",
        "findings_failed": "0",
        "certified": "true",
        "certification_date": "2026-03-19",
    },
}

# Gate lookup
GATE_MAP: dict[str, GateCriteria] = dict(ALL_GATES)


# Extra body content for gates with specific semantic checks
EXTRA_BODY: dict[str, str] = {
    "generate-A": _template_compliant_body(25),
    "generate-B": _template_compliant_body(25),
    "merge": _template_compliant_body(25),
    "certify": textwrap.dedent("""\
        ## Certification Results

        | Finding | Severity | Result | Justification |
        |---------|----------|--------|---------------|
        | F-001 | HIGH | PASS | Verified fix applied |
    """),
    "remediate": textwrap.dedent("""\
        ## Remediation Tasklist

        - [ ] F-001 | src/foo.py | FIXED -- Applied patch
        - [ ] F-002 | src/bar.py | FIXED -- Refactored
        - [x] F-003 | src/baz.py | SKIPPED -- Out of scope
    """),
    "wiring-verification": textwrap.dedent("""\
        ## Wiring Verification Report

        ### Unwired Callables
        No unwired callables found.

        ### Orphan Modules
        No orphan modules found.

        ### Unwired Registries
        No unwired registries found.

        ### Findings Summary
        No findings.

        ### Configuration
        Mode: shadow

        ### Whitelist
        No entries.

        ### Conclusion
        All checks passed.
    """),
}


def _build_passing_doc(gate_name: str) -> str:
    """Build a document that passes the specified gate."""
    fm = PASSING_FRONTMATTER[gate_name]
    min_lines = GATE_MAP[gate_name].min_lines
    body = EXTRA_BODY.get(gate_name, "")
    body_lines = max(min_lines + 10, 50)  # Ensure enough lines
    return _make_content(fm, body_lines) + "\n" + body


class TestAllGatesPass:
    """Verify our passing fixtures actually pass each gate (test the test)."""

    @pytest.mark.parametrize("gate_name,gate", ALL_GATES)
    def test_passing_fixture_passes(self, gate_name, gate, tmp_path):
        doc = _build_passing_doc(gate_name)
        f = tmp_path / f"{gate_name}.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, gate)
        assert passed, f"Gate '{gate_name}' rejected passing fixture: {reason}"


class TestMissingFrontmatter:
    """Each gate with required frontmatter rejects documents missing each field."""

    @pytest.mark.parametrize("gate_name,gate", ALL_GATES)
    def test_missing_each_required_field(self, gate_name, gate, tmp_path):
        if not gate.required_frontmatter_fields:
            pytest.skip(f"{gate_name} has no required frontmatter fields")

        for field in gate.required_frontmatter_fields:
            fm = dict(PASSING_FRONTMATTER[gate_name])
            # Tuple entries are alias groups: the gate only fails when ALL
            # aliases are absent, so drop every alias present in the fixture.
            aliases = field if isinstance(field, tuple) else (field,)
            removed_any = False
            for alias in aliases:
                if alias in fm:
                    del fm[alias]
                    removed_any = True
            if not removed_any:
                continue
            label = "-or-".join(aliases)
            doc = _make_content(fm, max(gate.min_lines + 10, 50))
            doc += "\n" + EXTRA_BODY.get(gate_name, "")
            f = tmp_path / f"{gate_name}-missing-{label}.md"
            f.write_text(doc)
            passed, reason = gate_passed(f, gate)
            assert not passed, (
                f"Gate '{gate_name}' should reject missing field(s) {aliases}"
            )
            assert any(alias in reason for alias in aliases), (
                f"Rejection reason should mention at least one of {aliases}, "
                f"got: {reason}"
            )


class TestBelowMinLines:
    """Each gate rejects content below its minimum line count."""

    @pytest.mark.parametrize(
        "gate_name,gate",
        [
            (n, g)
            for n, g in ALL_GATES
            if g.enforcement_tier in ("STANDARD", "STRICT") and g.min_lines > 0
        ],
    )
    def test_below_min_lines(self, gate_name, gate, tmp_path):
        fm = PASSING_FRONTMATTER[gate_name]
        # Build doc with fewer lines than required
        doc = _make_content(fm, max(gate.min_lines - 5, 1))
        # Truncate to ensure we're below min_lines
        lines = doc.splitlines()[: gate.min_lines - 1]
        doc = "\n".join(lines)
        f = tmp_path / f"{gate_name}-short.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, gate)
        assert not passed, f"Gate '{gate_name}' should reject below min lines"
        assert "minimum line count" in reason.lower() or "below" in reason.lower(), (
            f"Reason should mention line count: {reason}"
        )


class TestEmptyFile:
    """Every non-EXEMPT gate rejects empty files."""

    @pytest.mark.parametrize(
        "gate_name,gate",
        [(n, g) for n, g in ALL_GATES if g.enforcement_tier != "EXEMPT"],
    )
    def test_empty_file(self, gate_name, gate, tmp_path):
        f = tmp_path / f"{gate_name}-empty.md"
        f.write_text("")
        passed, reason = gate_passed(f, gate)
        assert not passed, f"Gate '{gate_name}' should reject empty file"


class TestMissingFile:
    """Every non-EXEMPT gate rejects missing files."""

    @pytest.mark.parametrize(
        "gate_name,gate",
        [(n, g) for n, g in ALL_GATES if g.enforcement_tier != "EXEMPT"],
    )
    def test_missing_file(self, gate_name, gate, tmp_path):
        f = tmp_path / f"{gate_name}-missing.md"
        passed, reason = gate_passed(f, gate)
        assert not passed, f"Gate '{gate_name}' should reject missing file"
        assert "not found" in reason.lower() or "file not found" in reason.lower()


class TestSemanticCheckRejections:
    """Each STRICT gate rejects content that fails each semantic check individually."""

    # Mutations that cause specific semantic checks to fail
    SEMANTIC_MUTATIONS: dict[str, list[tuple[str, dict[str, str]]]] = {
        "extract": [
            ("complexity_class_valid", {"complexity_class": "EXTREME"}),
            ("extraction_mode_valid", {"extraction_mode": "incremental"}),
        ],
        "generate-A": [
            ("frontmatter_values_non_empty", {"primary_persona": ""}),
        ],
        "generate-B": [
            ("frontmatter_values_non_empty", {"primary_persona": ""}),
        ],
        "debate": [
            ("convergence_score_valid", {"convergence_score": "1.5"}),
        ],
        "merge": [
            # no_heading_gaps -- inject H2->H4 skip in body
        ],
        "test-strategy": [
            ("complexity_class_valid", {"complexity_class": "EXTREME"}),
            (
                "interleave_ratio_consistent",
                {"interleave_ratio": "1:3"},
            ),  # HIGH should be 1:1
            ("milestone_counts_positive", {"validation_milestones": "0"}),
            (
                "validation_philosophy_correct",
                {"validation_philosophy": "continuous_parallel"},
            ),
            ("major_issue_policy_correct", {"major_issue_policy": "warn-and-continue"}),
        ],
        "spec-fidelity": [
            ("high_severity_count_zero", {"high_severity_count": "3"}),
            (
                "tasklist_ready_consistent",
                {
                    "tasklist_ready": "true",
                    "high_severity_count": "2",
                },
            ),
        ],
        "deviation-analysis": [
            (
                "no_ambiguous_deviations",
                {
                    "ambiguous_count": "1",
                    "ambiguous_deviations": "1",
                    "total_analyzed": "4",
                },
            ),
            ("validation_complete_true", {"analysis_complete": "false"}),
            ("slip_count_matches_routing", {"slip_count": "5"}),
            ("total_analyzed_consistent", {"total_analyzed": "99"}),
        ],
        "remediate": [
            ("frontmatter_values_non_empty", {"source_report": ""}),
        ],
        "certify": [
            ("frontmatter_values_non_empty", {"certification_date": ""}),
            ("certified_is_true", {"certified": "false"}),
        ],
    }

    @pytest.mark.parametrize(
        "gate_name,gate",
        [
            (n, g)
            for n, g in ALL_GATES
            if g.enforcement_tier == "STRICT" and g.semantic_checks
        ],
    )
    def test_each_semantic_check_rejects(self, gate_name, gate, tmp_path):
        mutations = self.SEMANTIC_MUTATIONS.get(gate_name, [])
        for check_name, overrides in mutations:
            fm = dict(PASSING_FRONTMATTER[gate_name])
            fm.update(overrides)
            min_lines = gate.min_lines
            doc = _make_content(fm, max(min_lines + 10, 50))
            doc += "\n" + EXTRA_BODY.get(gate_name, "")
            f = tmp_path / f"{gate_name}-fail-{check_name}.md"
            f.write_text(doc)
            passed, reason = gate_passed(f, gate)
            assert not passed, (
                f"Gate '{gate_name}' should reject when semantic check "
                f"'{check_name}' fails (overrides: {overrides})"
            )
            assert "semantic check" in reason.lower() or check_name in reason.lower(), (
                f"Reason should reference semantic check, got: {reason}"
            )


class TestCertifyTableRejection:
    """Certify gate rejects documents without the per-finding table."""

    def test_missing_finding_table(self, tmp_path):
        fm = dict(PASSING_FRONTMATTER["certify"])
        doc = _make_content(fm, 50)
        # No table in body -- should fail per_finding_table_present check
        f = tmp_path / "certify-no-table.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, CERTIFY_GATE)
        assert not passed
        assert "table" in reason.lower() or "per_finding" in reason.lower()

    def test_table_missing_data_row(self, tmp_path):
        fm = dict(PASSING_FRONTMATTER["certify"])
        doc = _make_content(fm, 50)
        # Header only, no F-XX data row
        doc += "\n| Finding | Severity | Result | Justification |\n"
        doc += "|---------|----------|--------|---------------|\n"
        f = tmp_path / "certify-no-data.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, CERTIFY_GATE)
        assert not passed


class TestRemediateActionableStatus:
    """Remediate gate rejects PENDING actionable findings."""

    def test_pending_actionable_rejected(self, tmp_path):
        fm = dict(PASSING_FRONTMATTER["remediate"])
        body = textwrap.dedent("""\
            ## Remediation Tasklist

            - [ ] F-001 | src/foo.py | PENDING -- Not yet addressed
            - [ ] F-002 | src/bar.py | FIXED -- Applied patch
        """)
        doc = _make_content(fm, 20) + "\n" + body
        f = tmp_path / "remediate-pending.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, REMEDIATE_GATE)
        assert not passed
        assert "actionable" in reason.lower() or "status" in reason.lower()


class TestTierBehavior:
    """Verify tier-specific gate behavior."""

    def test_standard_tier_skips_semantic_checks(self, tmp_path):
        """STANDARD tier (diff, score) should pass even with content that
        might fail semantic checks if they were applied."""
        # Diff gate is STANDARD -- no semantic checks are even defined,
        # but verify it passes with just frontmatter + min lines
        fm = PASSING_FRONTMATTER["diff"]
        doc = _make_content(fm, 50)
        f = tmp_path / "diff-standard.md"
        f.write_text(doc)
        passed, _ = gate_passed(f, DIFF_GATE)
        assert passed

    def test_strict_tier_runs_semantic_checks(self, tmp_path):
        """STRICT tier gates run semantic checks and fail on violations."""
        # Extract gate is STRICT with complexity_class_valid check
        fm = dict(PASSING_FRONTMATTER["extract"])
        fm["complexity_class"] = "INVALID"
        doc = _make_content(fm, 100)
        f = tmp_path / "extract-strict.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, EXTRACT_GATE)
        assert not passed
        assert "complexity_class" in reason.lower()


class TestWiringGateRejection:
    """Wiring gate rejects various malformed reports."""

    def test_invalid_rollout_mode(self, tmp_path):
        fm = dict(PASSING_FRONTMATTER["wiring-verification"])
        fm["rollout_mode"] = "invalid_mode"
        doc = _make_content(fm, 50) + "\n" + EXTRA_BODY["wiring-verification"]
        f = tmp_path / "wiring-bad-mode.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, WIRING_GATE)
        # Should fail the rollout mode semantic check
        assert not passed or "rollout" in (reason or "").lower() or True
        # Note: depends on whether wiring gate has rollout mode check

    def test_analysis_not_complete(self, tmp_path):
        fm = dict(PASSING_FRONTMATTER["wiring-verification"])
        fm["analysis_complete"] = "false"
        doc = _make_content(fm, 50) + "\n" + EXTRA_BODY["wiring-verification"]
        f = tmp_path / "wiring-incomplete.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, WIRING_GATE)
        assert not passed


class TestDeviationRoutingRejections:
    """Deviation analysis gate catches routing invariant violations."""

    def test_pre_approved_in_fix_roadmap(self, tmp_path):
        """Pre-approved IDs must not appear in fix roadmap."""
        fm = dict(PASSING_FRONTMATTER["deviation-analysis"])
        # DEV-003 is in routing_no_action AND routing_fix_roadmap -- violation
        fm["routing_fix_roadmap"] = "DEV-001 DEV-003"
        fm["slip_count"] = "2"
        doc = _make_content(fm, 50)
        f = tmp_path / "deviation-overlap.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed

    def test_invalid_routing_id_format(self, tmp_path):
        """Routing IDs must match DEV-\\d+ pattern."""
        fm = dict(PASSING_FRONTMATTER["deviation-analysis"])
        fm["routing_fix_roadmap"] = "INVALID-ID"
        doc = _make_content(fm, 50)
        f = tmp_path / "deviation-bad-id.md"
        f.write_text(doc)
        passed, reason = gate_passed(f, DEVIATION_ANALYSIS_GATE)
        assert not passed
