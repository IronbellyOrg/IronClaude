"""Tests for semantic check helper functions and gate diagnostics (T04.02, T04.03).

Covers:
- All semantic check helpers return tuple[bool, str] per AC-004
- Each helper passes on valid input and fails on invalid input
- Diagnostic messages on failure are non-empty
- format_gate_failure() produces multi-line output with all required fields
- GateFailure dataclass is importable and constructable
"""

from __future__ import annotations

import pytest

from superclaude.cli.cli_portify.gates import (
    GateFailure,
    format_gate_failure,
    has_approval_status,
    has_brainstorm_section,
    has_component_inventory,
    has_criticals_addressed,
    has_exit_recommendation,
    has_quality_scores,
    has_required_analysis_sections,
    has_return_type_pattern,
    has_step_count_consistency,
    has_valid_yaml_config,
    has_zero_placeholders,
)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


def _assert_tuple_bool_str(result):
    """Assert result is tuple[bool, str] per AC-004."""
    assert isinstance(result, tuple), f"Expected tuple, got {type(result)}"
    assert len(result) == 2, f"Expected 2-tuple, got {len(result)}-tuple"
    passed, msg = result
    assert isinstance(passed, bool), f"Expected bool for index 0, got {type(passed)}"
    assert isinstance(msg, str), f"Expected str for index 1, got {type(msg)}"
    return passed, msg


# ---------------------------------------------------------------------------
# T04.02: Semantic check helper functions — tuple[bool, str] return type
# ---------------------------------------------------------------------------

class TestSemanticCheckReturnTypes:
    """All semantic check helpers return tuple[bool, str] per AC-004."""

    @pytest.mark.parametrize("fn,valid_input", [
        (has_valid_yaml_config, "---\nworkflow_path: /foo\ncli_name: bar\noutput_dir: /out\n---\n"),
        (has_component_inventory, "---\ncomponent_count: 1\n---\n\nSKILL.md present.\n"),
        (has_required_analysis_sections, (
            "## Source Components\n## Step Graph\n## Parallel Groups\n"
            "## Gates Summary\n## Data Flow\n## Classifications\n## Recommendations\n"
        )),
        (has_approval_status, "---\napproval_status: pending\n---\n"),
        (has_exit_recommendation, "EXIT_RECOMMENDATION: CONTINUE\n"),
        (has_zero_placeholders, "Clean content with no placeholders.\n"),
        (has_brainstorm_section, "## Brainstorm\nSome content.\n"),
        (has_quality_scores, "clarity: 4\ncompleteness: 5\ntestability: 3\nconsistency: 4\noverall: 4\n"),
        (has_criticals_addressed, "No critical items here.\n"),
        (has_return_type_pattern, "tuple[bool, str]\n"),
        (has_step_count_consistency, "pipeline_steps: 3\n### Step 1: foo\n### Step 2: bar\n### Step 3: baz\n"),
    ])
    def test_semantic_check_returns_tuple_bool_str(self, fn, valid_input):
        result = fn(valid_input)
        passed, msg = _assert_tuple_bool_str(result)
        assert passed is True, f"{fn.__name__} failed on valid input: {msg}"
        assert msg == ""

    @pytest.mark.parametrize("fn,invalid_input", [
        (has_valid_yaml_config, "---\nother_field: value\n---\n"),
        (has_component_inventory, "# No components here\nJust text.\n"),
        (has_required_analysis_sections, "## Only One Section\nContent.\n"),
        (has_approval_status, "---\nstep: analyze\n---\n"),
        (has_exit_recommendation, "No marker here.\n"),
        (has_zero_placeholders, "Has {{SC_PLACEHOLDER:SECTION_NAME}} sentinel.\n"),
        (has_brainstorm_section, "## Overview\nNo brainstorm.\n"),
        (has_quality_scores, "---\nstep: test\n---\nNo scores.\n"),
        (has_return_type_pattern, "Just some text without types.\n"),
    ])
    def test_semantic_check_fails_on_invalid_input(self, fn, invalid_input):
        result = fn(invalid_input)
        passed, msg = _assert_tuple_bool_str(result)
        assert passed is False, f"{fn.__name__} passed on invalid input"
        assert msg, f"{fn.__name__} returned empty diagnostic on failure"


# ---------------------------------------------------------------------------
# T04.02: Individual semantic check behavior
# ---------------------------------------------------------------------------

class TestHasValidYamlConfig:
    """has_valid_yaml_config checks for workflow_path, cli_name, output_dir."""

    def test_passes_with_all_fields(self):
        content = "---\nworkflow_path: /skills/foo\ncli_name: foo\noutput_dir: /out\n---\n"
        passed, msg = has_valid_yaml_config(content)
        assert passed is True

    def test_fails_missing_workflow_path(self):
        content = "---\ncli_name: foo\noutput_dir: /out\n---\n"
        passed, msg = has_valid_yaml_config(content)
        assert passed is False
        assert "workflow_path" in msg

    def test_fails_missing_cli_name(self):
        content = "---\nworkflow_path: /foo\noutput_dir: /out\n---\n"
        passed, msg = has_valid_yaml_config(content)
        assert passed is False
        assert "cli_name" in msg

    def test_fails_missing_output_dir(self):
        content = "---\nworkflow_path: /foo\ncli_name: bar\n---\n"
        passed, msg = has_valid_yaml_config(content)
        assert passed is False
        assert "output_dir" in msg

    def test_fails_empty_content(self):
        passed, msg = has_valid_yaml_config("")
        assert passed is False
        assert msg


class TestHasComponentInventory:
    """has_component_inventory checks for ≥1 component with SKILL.md."""

    def test_passes_with_component_count(self):
        content = "---\ncomponent_count: 2\n---\n\nSKILL.md is present.\n"
        passed, msg = has_component_inventory(content)
        assert passed is True

    def test_passes_with_skill_md_reference(self):
        content = "## Skill\n\nSKILL.md: Present\n"
        passed, msg = has_component_inventory(content)
        assert passed is True

    def test_fails_on_empty_content(self):
        passed, msg = has_component_inventory("# Nothing\n")
        assert passed is False
        assert msg


class TestHasRequiredAnalysisSections:
    """has_required_analysis_sections checks for all 7 required sections."""

    FULL_CONTENT = (
        "## Source Components\nfoo\n"
        "## Step Graph\nbar\n"
        "## Parallel Groups\nbaz\n"
        "## Gates Summary\nqux\n"
        "## Data Flow\nquux\n"
        "## Classifications\ncorge\n"
        "## Recommendations\ngrault\n"
    )

    def test_passes_with_all_sections(self):
        passed, msg = has_required_analysis_sections(self.FULL_CONTENT)
        assert passed is True

    def test_fails_missing_step_graph(self):
        content = self.FULL_CONTENT.replace("## Step Graph\nbar\n", "")
        passed, msg = has_required_analysis_sections(content)
        assert passed is False
        assert "Step Graph" in msg

    def test_diagnostic_lists_missing_sections(self):
        content = "## Source Components\nfoo\n"
        passed, msg = has_required_analysis_sections(content)
        assert passed is False
        assert msg
        # Should list at least one missing section
        assert len(msg) > 10


class TestHasApprovalStatus:
    """has_approval_status checks for approval_status field."""

    def test_passes_on_approved(self):
        content = "---\napproval_status: approved\n---\n"
        passed, _ = has_approval_status(content)
        assert passed is True

    def test_passes_on_rejected(self):
        content = "---\napproval_status: rejected\n---\n"
        passed, _ = has_approval_status(content)
        assert passed is True

    def test_passes_on_pending(self):
        content = "---\napproval_status: pending\n---\n"
        passed, _ = has_approval_status(content)
        assert passed is True

    def test_fails_without_field(self):
        content = "---\nstep: test\n---\n"
        passed, msg = has_approval_status(content)
        assert passed is False
        assert "approval_status" in msg


class TestHasExitRecommendation:
    """has_exit_recommendation checks for EXIT_RECOMMENDATION marker."""

    def test_passes_on_continue(self):
        passed, _ = has_exit_recommendation("EXIT_RECOMMENDATION: CONTINUE\n")
        assert passed is True

    def test_passes_on_halt(self):
        passed, _ = has_exit_recommendation("EXIT_RECOMMENDATION: HALT\n")
        assert passed is True

    def test_fails_without_marker(self):
        passed, msg = has_exit_recommendation("No marker here.\n")
        assert passed is False
        assert msg


class TestHasZeroPlaceholders:
    """has_zero_placeholders detects {{SC_PLACEHOLDER:*}} sentinels."""

    def test_passes_on_clean_content(self):
        passed, _ = has_zero_placeholders("Clean content.\n")
        assert passed is True

    def test_fails_on_placeholder(self):
        passed, msg = has_zero_placeholders("Has {{SC_PLACEHOLDER:SECTION_NAME}} here.\n")
        assert passed is False
        assert "placeholder" in msg.lower()

    def test_fails_on_multiple_placeholders(self):
        content = "{{SC_PLACEHOLDER:A}} and {{SC_PLACEHOLDER:B}}\n"
        passed, msg = has_zero_placeholders(content)
        assert passed is False
        assert msg


class TestHasBrainstormSection:
    """has_brainstorm_section checks for Section 12 (brainstorm/gaps)."""

    def test_passes_on_brainstorm_heading(self):
        passed, _ = has_brainstorm_section("## Brainstorm\nContent.\n")
        assert passed is True

    def test_passes_on_gaps_heading(self):
        passed, _ = has_brainstorm_section("## Gaps\nContent.\n")
        assert passed is True

    def test_passes_on_gap_analysis_heading(self):
        passed, _ = has_brainstorm_section("## Gap Analysis\nContent.\n")
        assert passed is True

    def test_passes_on_missing_heading(self):
        passed, _ = has_brainstorm_section("## Missing\nContent.\n")
        assert passed is True

    def test_fails_on_no_matching_section(self):
        content = "## Overview\nContent.\n## Architecture\nDesign.\n"
        passed, msg = has_brainstorm_section(content)
        assert passed is False
        assert msg


class TestHasQualityScores:
    """has_quality_scores checks for 5 quality score fields."""

    def test_passes_with_all_scores(self):
        content = "clarity: 4\ncompleteness: 5\ntestability: 3\nconsistency: 4\noverall: 4\n"
        passed, _ = has_quality_scores(content)
        assert passed is True

    def test_fails_missing_testability(self):
        content = "clarity: 4\ncompleteness: 5\nconsistency: 4\noverall: 4\n"
        passed, msg = has_quality_scores(content)
        assert passed is False
        assert "testability" in msg

    def test_fails_empty_content(self):
        passed, msg = has_quality_scores("")
        assert passed is False
        assert msg


class TestHasCriticalsAddressed:
    """has_criticals_addressed checks CRITICAL items are resolved."""

    def test_passes_with_no_criticals(self):
        passed, _ = has_criticals_addressed("No critical items.\n")
        assert passed is True

    def test_passes_with_incorporated_critical(self):
        content = "CRITICAL: Fix this [INCORPORATED]\nOther content.\n"
        passed, _ = has_criticals_addressed(content)
        assert passed is True

    def test_passes_with_dismissed_critical(self):
        content = "CRITICAL: Fix this [DISMISSED]\nOther content.\n"
        passed, _ = has_criticals_addressed(content)
        assert passed is True


# ---------------------------------------------------------------------------
# T04.03: Gate diagnostics formatting
# ---------------------------------------------------------------------------

class TestFormatGateFailure:
    """format_gate_failure produces human-readable gate failure messages."""

    def test_returns_string(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "analysis.md")
        assert isinstance(result, str)

    def test_contains_gate_id(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "analysis.md")
        assert "G-003" in result

    def test_contains_check_name(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "analysis.md")
        assert "has_required_analysis_sections" in result

    def test_contains_artifact_path(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "portify-analysis-report.md")
        assert "portify-analysis-report.md" in result

    def test_contains_reason(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "analysis.md")
        assert "Missing: Step Graph" in result

    def test_contains_fix_hint(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "analysis.md")
        assert "Fix:" in result

    def test_is_multiline(self):
        result = format_gate_failure("G-003", "has_required_analysis_sections", "Missing: Step Graph", "analysis.md")
        assert "\n" in result
        assert len(result.splitlines()) >= 4

    def test_acceptance_criteria_example(self):
        """Verify the specific example from acceptance criteria."""
        result = format_gate_failure(
            "G-003",
            "has_required_analysis_sections",
            "Missing: Step Graph",
            "portify-analysis-report.md",
        )
        assert "G-003" in result
        assert "has_required_analysis_sections" in result
        assert "portify-analysis-report.md" in result
        assert "Missing: Step Graph" in result

    def test_unknown_check_name_has_default_hint(self):
        result = format_gate_failure("G-000", "unknown_check", "Some diagnostic", "artifact.md")
        assert "Fix:" in result
        assert len(result.splitlines()) >= 4

    def test_diagnostic_never_empty_in_output(self):
        result = format_gate_failure("G-010", "has_zero_placeholders", "Placeholder found: {{SC_PLACEHOLDER:X}}", "spec.md")
        assert "Placeholder found" in result


class TestGateFailureDataclass:
    """GateFailure dataclass is importable and correct."""

    def test_importable(self):
        from superclaude.cli.cli_portify.gates import GateFailure
        assert GateFailure is not None

    def test_constructable(self):
        gf = GateFailure(
            gate_id="G-003",
            check_name="has_required_analysis_sections",
            diagnostic="Missing: Step Graph",
            artifact_path="analysis.md",
            tier="STRICT",
        )
        assert gf.gate_id == "G-003"
        assert gf.check_name == "has_required_analysis_sections"
        assert gf.diagnostic == "Missing: Step Graph"
        assert gf.artifact_path == "analysis.md"
        assert gf.tier == "STRICT"

    def test_default_tier_is_standard(self):
        gf = GateFailure(
            gate_id="G-001",
            check_name="has_component_inventory",
            diagnostic="No components",
            artifact_path="inv.md",
        )
        assert gf.tier == "STANDARD"
