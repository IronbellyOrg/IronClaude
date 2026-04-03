"""Tests for roadmap/gates.py -- gate criteria data definitions and semantic checks."""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import (
    ALL_GATES,
    DEBATE_GATE,
    DEVIATION_ANALYSIS_GATE,
    DIFF_GATE,
    EXTRACT_GATE,
    GENERATE_A_GATE,
    GENERATE_B_GATE,
    MERGE_GATE,
    SCORE_GATE,
    SPEC_FIDELITY_GATE,
    TEST_STRATEGY_GATE,
    _certified_is_true,
    _complexity_class_valid,
    _convergence_score_valid,
    _cross_refs_resolve,
    _extraction_mode_valid,
    _frontmatter_values_non_empty,
    _interleave_ratio_consistent,
    _major_issue_policy_correct,
    _parse_frontmatter,
    _milestone_counts_positive,
    _has_actionable_content,
    _high_severity_count_zero,
    _no_ambiguous_deviations,
    _no_duplicate_headings,
    _no_heading_gaps,
    _pre_approved_not_in_fix_roadmap,
    _routing_consistent_with_slip_count,
    _routing_ids_valid,
    _slip_count_matches_routing,
    _tasklist_ready_consistent,
    _total_analyzed_consistent,
    _total_annotated_consistent,
    _deviation_counts_reconciled,
    _validation_complete_true,
    _validation_philosophy_correct,
)
from superclaude.cli.pipeline.models import GateCriteria


class TestGateInstances:
    def test_all_gates_are_gate_criteria(self):
        for name, gate in ALL_GATES:
            assert isinstance(gate, GateCriteria), f"{name} is not GateCriteria"

    def test_fourteen_gates_defined(self):
        assert len(ALL_GATES) == 14

    def test_extract_gate_fields(self):
        assert "functional_requirements" in EXTRACT_GATE.required_frontmatter_fields
        assert "complexity_score" in EXTRACT_GATE.required_frontmatter_fields
        assert "complexity_class" in EXTRACT_GATE.required_frontmatter_fields
        assert "spec_source" in EXTRACT_GATE.required_frontmatter_fields
        assert "generated" in EXTRACT_GATE.required_frontmatter_fields
        assert "generator" in EXTRACT_GATE.required_frontmatter_fields
        assert "nonfunctional_requirements" in EXTRACT_GATE.required_frontmatter_fields
        assert "total_requirements" in EXTRACT_GATE.required_frontmatter_fields
        assert "domains_detected" in EXTRACT_GATE.required_frontmatter_fields
        assert "risks_identified" in EXTRACT_GATE.required_frontmatter_fields
        assert "dependencies_identified" in EXTRACT_GATE.required_frontmatter_fields
        assert "success_criteria_count" in EXTRACT_GATE.required_frontmatter_fields
        assert "extraction_mode" in EXTRACT_GATE.required_frontmatter_fields
        assert len(EXTRACT_GATE.required_frontmatter_fields) == 13
        assert EXTRACT_GATE.enforcement_tier == "STRICT"
        assert EXTRACT_GATE.min_lines == 50

    def test_generate_gates_are_strict(self):
        assert GENERATE_A_GATE.enforcement_tier == "STRICT"
        assert GENERATE_B_GATE.enforcement_tier == "STRICT"

    def test_generate_gates_have_semantic_checks(self):
        assert GENERATE_A_GATE.semantic_checks is not None
        assert len(GENERATE_A_GATE.semantic_checks) == 2
        assert GENERATE_B_GATE.semantic_checks is not None
        assert len(GENERATE_B_GATE.semantic_checks) == 2

    def test_diff_gate_standard(self):
        assert DIFF_GATE.enforcement_tier == "STANDARD"
        assert "total_diff_points" in DIFF_GATE.required_frontmatter_fields

    def test_debate_gate_strict_with_convergence(self):
        assert DEBATE_GATE.enforcement_tier == "STRICT"
        assert "convergence_score" in DEBATE_GATE.required_frontmatter_fields
        assert DEBATE_GATE.semantic_checks is not None

    def test_merge_gate_has_three_semantic_checks(self):
        assert MERGE_GATE.enforcement_tier == "STRICT"
        assert len(MERGE_GATE.semantic_checks) == 3
        check_names = {c.name for c in MERGE_GATE.semantic_checks}
        assert check_names == {
            "no_heading_gaps",
            "cross_refs_resolve",
            "no_duplicate_headings",
        }

    def test_score_gate_standard(self):
        assert SCORE_GATE.enforcement_tier == "STANDARD"
        assert "base_variant" in SCORE_GATE.required_frontmatter_fields

    def test_test_strategy_gate_strict(self):
        assert TEST_STRATEGY_GATE.enforcement_tier == "STRICT"
        assert "validation_milestones" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "interleave_ratio" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "spec_source" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "generated" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "generator" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "complexity_class" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "validation_philosophy" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "work_milestones" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert "major_issue_policy" in TEST_STRATEGY_GATE.required_frontmatter_fields
        assert len(TEST_STRATEGY_GATE.required_frontmatter_fields) == 9

    def test_test_strategy_gate_has_five_semantic_checks(self):
        assert TEST_STRATEGY_GATE.semantic_checks is not None
        assert len(TEST_STRATEGY_GATE.semantic_checks) == 5
        check_names = {c.name for c in TEST_STRATEGY_GATE.semantic_checks}
        assert check_names == {
            "complexity_class_valid",
            "interleave_ratio_consistent",
            "milestone_counts_positive",
            "validation_philosophy_correct",
            "major_issue_policy_correct",
        }

    def test_test_strategy_reuses_complexity_class_valid(self):
        """_complexity_class_valid is the same function on both EXTRACT_GATE and TEST_STRATEGY_GATE."""
        extract_check = next(
            c
            for c in EXTRACT_GATE.semantic_checks
            if c.name == "complexity_class_valid"
        )
        test_strategy_check = next(
            c
            for c in TEST_STRATEGY_GATE.semantic_checks
            if c.name == "complexity_class_valid"
        )
        assert extract_check.check_fn is test_strategy_check.check_fn

    def test_extract_gate_has_semantic_checks(self):
        assert EXTRACT_GATE.semantic_checks is not None
        assert len(EXTRACT_GATE.semantic_checks) == 2
        check_names = {c.name for c in EXTRACT_GATE.semantic_checks}
        assert check_names == {"complexity_class_valid", "extraction_mode_valid"}


class TestSemanticCheckFunctions:
    def test_no_heading_gaps_valid(self):
        content = "# H1\n## H2\n### H3\n#### H4\n"
        assert _no_heading_gaps(content) is True

    def test_no_heading_gaps_skip(self):
        content = "## H2\n#### H4\n"
        assert _no_heading_gaps(content) is False

    def test_no_heading_gaps_empty(self):
        assert _no_heading_gaps("") is True

    def test_no_duplicate_headings_clean(self):
        content = "## Alpha\n### Beta\n## Gamma\n### Delta\n"
        assert _no_duplicate_headings(content) is True

    def test_no_duplicate_headings_h2_dup(self):
        content = "## Alpha\n### Beta\n## Alpha\n"
        assert _no_duplicate_headings(content) is not True

    def test_no_duplicate_headings_h3_dup(self):
        content = "### Beta\ntext\n### Beta\n"
        assert _no_duplicate_headings(content) is not True


class TestNoDuplicateHeadingsScoped:
    """H3 duplicate detection is scoped to parent H2 section."""

    def test_h3_same_name_different_h2_parents_passes(self):
        """The core false-positive fix: ### Tasks under different ## Phase sections."""
        content = (
            "## Phase 1\n### Tasks\n### Exit Criteria\n"
            "## Phase 2\n### Tasks\n### Exit Criteria\n"
            "## Phase 3\n### Tasks\n### Exit Criteria\n"
        )
        assert _no_duplicate_headings(content) is True

    def test_h3_same_name_same_h2_parent_fails(self):
        """Duplicate H3 within the same H2 section is still caught."""
        content = "## Phase 1\n### Tasks\nsome text\n### Tasks\n"
        result = _no_duplicate_headings(content)
        assert result is not True
        assert "Tasks" in result  # diagnostic contains the heading text

    def test_h2_global_duplicate_still_fails(self):
        """H2 duplicates are always caught regardless of position."""
        content = "## Phase 1\n### Tasks\n## Phase 2\n### Tasks\n## Phase 1\n"
        result = _no_duplicate_headings(content)
        assert result is not True
        assert "Phase 1" in result

    def test_h3_before_any_h2_duplicate_fails(self):
        """H3s before any H2 share a preamble scope -- duplicates are caught."""
        content = "### Intro\ntext\n### Intro\n"
        assert _no_duplicate_headings(content) is not True

    def test_h3_preamble_then_same_under_h2_passes(self):
        """H3 in top-level scope vs under an H2 are different scopes."""
        content = "### Tasks\n## Phase 1\n### Tasks\n"
        assert _no_duplicate_headings(content) is True

    def test_case_insensitive_h3_within_section_fails(self):
        """Duplicate detection is case-insensitive within a section."""
        content = "## Phase 1\n### Tasks\n### tasks\n"
        assert _no_duplicate_headings(content) is not True

    def test_empty_content_passes(self):
        assert _no_duplicate_headings("") is True

    def test_no_headings_passes(self):
        assert _no_duplicate_headings("Just text\nwith no headings\n") is True

    def test_failure_contains_line_number(self):
        """Diagnostic string includes the line number of the offending duplicate."""
        content = "## Phase 1\n### Tasks\n### Tasks\n"
        result = _no_duplicate_headings(content)
        assert result is not True
        assert "line 3" in result.lower()

    def test_real_roadmap_structure_passes(self):
        """Mirrors the actual failing roadmap structure that triggered this bug."""
        content = (
            "## Phase 1: Preparation\n### Tasks\n### Exit Criteria\n"
            "## Phase 2: Extraction\n### Tasks\n### Integration Points\n"
            "### Risk Burn-Down\n### Exit Criteria\n"
            "## Phase 3: Restructuring\n### Tasks\n### Integration Points\n"
            "### Risk Burn-Down\n### Exit Criteria\n"
            "## Phase 4: Verification\n### Tasks\n### Evidence Artifacts\n"
            "### Risk Burn-Down\n### Exit Criteria\n"
            "## Risk Assessment\n## Resource Requirements\n"
            "### Prerequisites\n### Staffing\n### External Dependencies\n"
        )
        assert _no_duplicate_headings(content) is True


def test_prd_refactor_roadmap_passes_duplicate_gate():
    """Regression: the actual roadmap that exposed this bug should pass."""
    roadmap = Path(".dev/releases/backlog/prd-skill-refactor/roadmap.md")
    if not roadmap.exists():
        pytest.skip("roadmap file not present")
    content = roadmap.read_text()
    assert _no_duplicate_headings(content) is True


class TestSemanticCheckFunctionsContinued:
    """Continuation of semantic check function tests (split by scoped heading tests)."""

    def test_frontmatter_values_non_empty_valid(self):
        content = "---\ntitle: Hello\nversion: 1.0\n---\n"
        assert _frontmatter_values_non_empty(content) is True

    def test_frontmatter_values_non_empty_missing_value(self):
        content = "---\ntitle: \nversion: 1.0\n---\n"
        assert _frontmatter_values_non_empty(content) is False

    def test_has_actionable_content_with_bullets(self):
        content = "## Plan\n- Step one\n- Step two\n"
        assert _has_actionable_content(content) is True

    def test_has_actionable_content_with_numbers(self):
        content = "## Plan\n1. Step one\n2. Step two\n"
        assert _has_actionable_content(content) is True

    def test_has_actionable_content_none(self):
        content = "## Plan\nJust text here\nNo lists\n"
        assert _has_actionable_content(content) is False

    def test_convergence_score_valid_good(self):
        content = "---\nconvergence_score: 0.85\nrounds_completed: 2\n---\n"
        assert _convergence_score_valid(content) is True

    def test_convergence_score_valid_boundary_zero(self):
        content = "---\nconvergence_score: 0.0\n---\n"
        assert _convergence_score_valid(content) is True

    def test_convergence_score_valid_boundary_one(self):
        content = "---\nconvergence_score: 1.0\n---\n"
        assert _convergence_score_valid(content) is True

    def test_convergence_score_out_of_range(self):
        content = "---\nconvergence_score: 1.5\n---\n"
        assert _convergence_score_valid(content) is False

    def test_convergence_score_not_a_number(self):
        content = "---\nconvergence_score: high\n---\n"
        assert _convergence_score_valid(content) is False

    def test_convergence_score_missing(self):
        content = "---\nother_field: value\n---\n"
        assert _convergence_score_valid(content) is False


class TestComplexityClassValid:
    """_complexity_class_valid: boundary tests for LOW, MEDIUM, HIGH enum."""

    def test_low_passes(self):
        assert _complexity_class_valid("---\ncomplexity_class: LOW\n---\n") is True

    def test_medium_passes(self):
        assert _complexity_class_valid("---\ncomplexity_class: MEDIUM\n---\n") is True

    def test_high_passes(self):
        assert _complexity_class_valid("---\ncomplexity_class: HIGH\n---\n") is True

    def test_case_insensitive(self):
        assert _complexity_class_valid("---\ncomplexity_class: low\n---\n") is True
        assert _complexity_class_valid("---\ncomplexity_class: Medium\n---\n") is True

    def test_simple_rejected(self):
        assert _complexity_class_valid("---\ncomplexity_class: simple\n---\n") is False

    def test_moderate_rejected(self):
        assert (
            _complexity_class_valid("---\ncomplexity_class: moderate\n---\n") is False
        )

    def test_complex_rejected(self):
        assert _complexity_class_valid("---\ncomplexity_class: complex\n---\n") is False

    def test_enterprise_rejected(self):
        assert (
            _complexity_class_valid("---\ncomplexity_class: enterprise\n---\n") is False
        )

    def test_missing_field_fails(self):
        assert _complexity_class_valid("---\nother: value\n---\n") is False

    def test_no_frontmatter_fails(self):
        assert _complexity_class_valid("No frontmatter.\n") is False


class TestExtractionModeValid:
    """_extraction_mode_valid: boundary tests for standard/chunked enum."""

    def test_standard_passes(self):
        assert _extraction_mode_valid("---\nextraction_mode: standard\n---\n") is True

    def test_chunked_passes(self):
        assert _extraction_mode_valid("---\nextraction_mode: chunked\n---\n") is True

    def test_chunked_with_count_passes(self):
        assert (
            _extraction_mode_valid("---\nextraction_mode: chunked (3 chunks)\n---\n")
            is True
        )

    def test_case_insensitive(self):
        assert _extraction_mode_valid("---\nextraction_mode: Standard\n---\n") is True
        assert _extraction_mode_valid("---\nextraction_mode: CHUNKED\n---\n") is True

    def test_full_rejected(self):
        assert _extraction_mode_valid("---\nextraction_mode: full\n---\n") is False

    def test_partial_rejected(self):
        assert _extraction_mode_valid("---\nextraction_mode: partial\n---\n") is False

    def test_incremental_rejected(self):
        assert (
            _extraction_mode_valid("---\nextraction_mode: incremental\n---\n") is False
        )

    def test_missing_field_fails(self):
        assert _extraction_mode_valid("---\nother: value\n---\n") is False

    def test_no_frontmatter_fails(self):
        assert _extraction_mode_valid("No frontmatter.\n") is False


class TestInterleaveRatioConsistent:
    """_interleave_ratio_consistent: complexity-to-ratio mapping tests."""

    def test_low_1_3_passes(self):
        content = "---\ncomplexity_class: LOW\ninterleave_ratio: 1:3\n---\n"
        assert _interleave_ratio_consistent(content) is True

    def test_medium_1_2_passes(self):
        content = "---\ncomplexity_class: MEDIUM\ninterleave_ratio: 1:2\n---\n"
        assert _interleave_ratio_consistent(content) is True

    def test_high_1_1_passes(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: 1:1\n---\n"
        assert _interleave_ratio_consistent(content) is True

    def test_low_1_1_rejected(self):
        content = "---\ncomplexity_class: LOW\ninterleave_ratio: 1:1\n---\n"
        assert _interleave_ratio_consistent(content) is False

    def test_high_1_3_rejected(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: 1:3\n---\n"
        assert _interleave_ratio_consistent(content) is False

    def test_medium_1_1_rejected(self):
        content = "---\ncomplexity_class: MEDIUM\ninterleave_ratio: 1:1\n---\n"
        assert _interleave_ratio_consistent(content) is False

    def test_case_insensitive_complexity(self):
        content = "---\ncomplexity_class: low\ninterleave_ratio: 1:3\n---\n"
        assert _interleave_ratio_consistent(content) is True

    def test_missing_complexity_fails(self):
        content = "---\ninterleave_ratio: 1:3\n---\n"
        assert _interleave_ratio_consistent(content) is False

    def test_missing_ratio_fails(self):
        content = "---\ncomplexity_class: LOW\n---\n"
        assert _interleave_ratio_consistent(content) is False

    def test_no_frontmatter_fails(self):
        assert _interleave_ratio_consistent("No frontmatter.\n") is False

    def test_invalid_complexity_fails(self):
        content = "---\ncomplexity_class: moderate\ninterleave_ratio: 1:2\n---\n"
        assert _interleave_ratio_consistent(content) is False


class TestMilestoneCountsPositive:
    """_milestone_counts_positive: positive integer validation."""

    def test_both_positive_passes(self):
        content = "---\nvalidation_milestones: 3\nwork_milestones: 6\n---\n"
        assert _milestone_counts_positive(content) is True

    def test_zero_validation_fails(self):
        content = "---\nvalidation_milestones: 0\nwork_milestones: 6\n---\n"
        assert _milestone_counts_positive(content) is False

    def test_zero_work_fails(self):
        content = "---\nvalidation_milestones: 3\nwork_milestones: 0\n---\n"
        assert _milestone_counts_positive(content) is False

    def test_negative_fails(self):
        content = "---\nvalidation_milestones: -1\nwork_milestones: 6\n---\n"
        assert _milestone_counts_positive(content) is False

    def test_non_integer_fails(self):
        content = "---\nvalidation_milestones: many\nwork_milestones: 6\n---\n"
        assert _milestone_counts_positive(content) is False

    def test_missing_field_fails(self):
        content = "---\nvalidation_milestones: 3\n---\n"
        assert _milestone_counts_positive(content) is False

    def test_no_frontmatter_fails(self):
        assert _milestone_counts_positive("No frontmatter.\n") is False


class TestValidationPhilosophyCorrect:
    """_validation_philosophy_correct: exact match tests."""

    def test_correct_value_passes(self):
        content = "---\nvalidation_philosophy: continuous-parallel\n---\n"
        assert _validation_philosophy_correct(content) is True

    def test_underscore_variant_rejected(self):
        content = "---\nvalidation_philosophy: continuous_parallel\n---\n"
        assert _validation_philosophy_correct(content) is False

    def test_space_variant_rejected(self):
        content = "---\nvalidation_philosophy: continuous parallel\n---\n"
        assert _validation_philosophy_correct(content) is False

    def test_missing_field_fails(self):
        content = "---\nother: value\n---\n"
        assert _validation_philosophy_correct(content) is False

    def test_no_frontmatter_fails(self):
        assert _validation_philosophy_correct("No frontmatter.\n") is False


class TestMajorIssuePolicyCorrect:
    """_major_issue_policy_correct: exact match tests."""

    def test_correct_value_passes(self):
        content = "---\nmajor_issue_policy: stop-and-fix\n---\n"
        assert _major_issue_policy_correct(content) is True

    def test_underscore_variant_rejected(self):
        content = "---\nmajor_issue_policy: stop_and_fix\n---\n"
        assert _major_issue_policy_correct(content) is False

    def test_wrong_value_rejected(self):
        content = "---\nmajor_issue_policy: continue\n---\n"
        assert _major_issue_policy_correct(content) is False

    def test_missing_field_fails(self):
        content = "---\nother: value\n---\n"
        assert _major_issue_policy_correct(content) is False

    def test_no_frontmatter_fails(self):
        assert _major_issue_policy_correct("No frontmatter.\n") is False


class TestTestStrategyGateIntegration:
    """Full TEST_STRATEGY_GATE integration tests."""

    def test_gate_passes_clean_document(self, tmp_path):
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "spec_source: test-spec.md\n"
            "generated: 2026-03-18T00:00:00Z\n"
            "generator: superclaude-roadmap-executor\n"
            "complexity_class: MEDIUM\n"
            "validation_philosophy: continuous-parallel\n"
            "validation_milestones: 3\n"
            "work_milestones: 6\n"
            "interleave_ratio: 1:2\n"
            "major_issue_policy: stop-and-fix\n"
            "---\n"
        ) + "\n".join([f"- test strategy line {i}" for i in range(45)])
        doc = tmp_path / "test-strategy.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, TEST_STRATEGY_GATE)
        assert passed is True, f"Expected pass, got reason: {reason}"

    def test_gate_fails_wrong_ratio_for_complexity(self, tmp_path):
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "spec_source: test-spec.md\n"
            "generated: 2026-03-18T00:00:00Z\n"
            "generator: superclaude-roadmap-executor\n"
            "complexity_class: LOW\n"
            "validation_philosophy: continuous-parallel\n"
            "validation_milestones: 3\n"
            "work_milestones: 6\n"
            "interleave_ratio: 1:1\n"
            "major_issue_policy: stop-and-fix\n"
            "---\n"
        ) + "\n".join([f"- test strategy line {i}" for i in range(45)])
        doc = tmp_path / "test-strategy.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, TEST_STRATEGY_GATE)
        assert passed is False

    def test_gate_fails_underscore_philosophy(self, tmp_path):
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "spec_source: test-spec.md\n"
            "generated: 2026-03-18T00:00:00Z\n"
            "generator: superclaude-roadmap-executor\n"
            "complexity_class: MEDIUM\n"
            "validation_philosophy: continuous_parallel\n"
            "validation_milestones: 3\n"
            "work_milestones: 6\n"
            "interleave_ratio: 1:2\n"
            "major_issue_policy: stop-and-fix\n"
            "---\n"
        ) + "\n".join([f"- test strategy line {i}" for i in range(45)])
        doc = tmp_path / "test-strategy.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, TEST_STRATEGY_GATE)
        assert passed is False


class TestCrossRefsResolve:
    def test_cross_refs_resolve_valid(self):
        """Valid cross-references resolve to existing headings."""
        content = (
            "# Document\n"
            "## 1.0 Introduction\n"
            "### 1.1 Overview\n"
            "See section 1.1 for details.\n"
        )
        assert _cross_refs_resolve(content) is True

    def test_cross_refs_resolve_invalid(self):
        """Dangling cross-references emit warnings but return True (warning-only mode)."""
        content = "# Document\n## 1.0 Introduction\nSee section 9.9 for details.\n"
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _cross_refs_resolve(content)
            # Warning-only mode: returns True despite dangling ref
            assert result is True
            # But a warning was emitted
            assert len(w) == 1
            assert "9.9" in str(w[0].message)

    def test_cross_refs_resolve_no_refs(self):
        """Documents with no cross-references pass without warnings."""
        content = (
            "# Document\n## Introduction\nThis document has no cross-references.\n"
        )
        import warnings

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = _cross_refs_resolve(content)
            assert result is True
            assert len(w) == 0


class TestHighSeverityCountZero:
    def test_high_severity_count_zero_passes(self):
        """count=0 returns True."""
        content = "---\nhigh_severity_count: 0\n---\n"
        assert _high_severity_count_zero(content) is True

    def test_high_severity_count_nonzero_fails(self):
        """count>0 returns False."""
        content = "---\nhigh_severity_count: 3\n---\n"
        assert _high_severity_count_zero(content) is False

    def test_high_severity_count_missing_field(self):
        """Missing high_severity_count field returns False."""
        content = "---\nother_field: value\n---\n"
        assert _high_severity_count_zero(content) is False

    def test_high_severity_count_non_integer(self):
        """Non-integer value raises TypeError."""
        content = "---\nhigh_severity_count: high\n---\n"
        with pytest.raises(TypeError, match="must be an integer"):
            _high_severity_count_zero(content)

    def test_high_severity_count_no_frontmatter(self):
        """Missing frontmatter returns False."""
        content = "No frontmatter here.\n"
        assert _high_severity_count_zero(content) is False


class TestTasklistReadyConsistent:
    def test_consistent_ready_true(self):
        """tasklist_ready=true with high=0 and validation_complete=true is consistent."""
        content = "---\ntasklist_ready: true\nhigh_severity_count: 0\nvalidation_complete: true\n---\n"
        assert _tasklist_ready_consistent(content) is True

    def test_inconsistent_ready_true_high_nonzero(self):
        """tasklist_ready=true but high_severity_count>0 is inconsistent."""
        content = "---\ntasklist_ready: true\nhigh_severity_count: 2\nvalidation_complete: true\n---\n"
        assert _tasklist_ready_consistent(content) is False

    def test_consistent_ready_false(self):
        """tasklist_ready=false is always consistent regardless of counts."""
        content = "---\ntasklist_ready: false\nhigh_severity_count: 5\nvalidation_complete: false\n---\n"
        assert _tasklist_ready_consistent(content) is True

    def test_missing_tasklist_ready(self):
        """Missing tasklist_ready field returns False."""
        content = "---\nhigh_severity_count: 0\n---\n"
        assert _tasklist_ready_consistent(content) is False

    def test_missing_high_severity_when_ready_true(self):
        """tasklist_ready=true but missing high_severity_count returns False."""
        content = "---\ntasklist_ready: true\nvalidation_complete: true\n---\n"
        assert _tasklist_ready_consistent(content) is False

    def test_inconsistent_validation_incomplete(self):
        """tasklist_ready=true but validation_complete=false is inconsistent."""
        content = "---\ntasklist_ready: true\nhigh_severity_count: 0\nvalidation_complete: false\n---\n"
        assert _tasklist_ready_consistent(content) is False

    def test_no_frontmatter(self):
        """Missing frontmatter returns False."""
        content = "No frontmatter.\n"
        assert _tasklist_ready_consistent(content) is False


class TestSpecFidelityGate:
    """Tests for SPEC_FIDELITY_GATE -- SC-001, SC-002, SC-007."""

    def test_spec_fidelity_gate_is_gate_criteria(self):
        assert isinstance(SPEC_FIDELITY_GATE, GateCriteria)

    def test_spec_fidelity_gate_is_strict(self):
        """SC-001: Gate must be STRICT enforcement."""
        assert SPEC_FIDELITY_GATE.enforcement_tier == "STRICT"

    def test_spec_fidelity_gate_required_frontmatter_fields(self):
        fields = SPEC_FIDELITY_GATE.required_frontmatter_fields
        assert "high_severity_count" in fields
        assert "medium_severity_count" in fields
        assert "low_severity_count" in fields
        assert "total_deviations" in fields
        assert "validation_complete" in fields
        assert "tasklist_ready" in fields
        assert len(fields) == 6

    def test_spec_fidelity_gate_has_two_semantic_checks(self):
        assert SPEC_FIDELITY_GATE.semantic_checks is not None
        assert len(SPEC_FIDELITY_GATE.semantic_checks) == 2
        check_names = {c.name for c in SPEC_FIDELITY_GATE.semantic_checks}
        assert check_names == {"high_severity_count_zero", "tasklist_ready_consistent"}

    def test_spec_fidelity_gate_reuses_phase2_checks(self):
        """Gate reuses _high_severity_count_zero() and _tasklist_ready_consistent() from Phase 2."""
        checks = SPEC_FIDELITY_GATE.semantic_checks
        hsc_check = next(c for c in checks if c.name == "high_severity_count_zero")
        trc_check = next(c for c in checks if c.name == "tasklist_ready_consistent")
        assert hsc_check.check_fn is _high_severity_count_zero
        assert trc_check.check_fn is _tasklist_ready_consistent

    def test_spec_fidelity_gate_blocks_high_severity(self):
        """SC-001: Gate blocks when high_severity_count > 0."""
        content = (
            "---\n"
            "high_severity_count: 2\n"
            "medium_severity_count: 1\n"
            "low_severity_count: 0\n"
            "total_deviations: 3\n"
            "validation_complete: true\n"
            "tasklist_ready: false\n"
            "---\n"
            "## Deviation Report\n"
            "- DEV-001: HIGH severity\n"
            "- DEV-002: HIGH severity\n"
            "- DEV-003: MEDIUM severity\n"
        )
        hsc_check = next(
            c
            for c in SPEC_FIDELITY_GATE.semantic_checks
            if c.name == "high_severity_count_zero"
        )
        assert hsc_check.check_fn(content) is False

    def test_spec_fidelity_gate_passes_clean(self):
        """SC-002: Gate passes when high_severity_count == 0 and all consistent."""
        content = (
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 2\n"
            "low_severity_count: 1\n"
            "total_deviations: 3\n"
            "validation_complete: true\n"
            "tasklist_ready: true\n"
            "---\n"
            "## Deviation Report\n"
            "- DEV-001: MEDIUM severity\n"
            "- DEV-002: MEDIUM severity\n"
            "- DEV-003: LOW severity\n"
        )
        for check in SPEC_FIDELITY_GATE.semantic_checks:
            assert check.check_fn(content) is True, f"Failed: {check.name}"

    def test_spec_fidelity_gate_degraded_passthrough(self):
        """SC-007: Gate passes in degraded mode (validation_complete=false, fidelity_check_attempted=true).

        When validation_complete=false AND tasklist_ready=false, semantic checks
        should not block: _high_severity_count_zero returns True for count=0,
        and _tasklist_ready_consistent returns True for tasklist_ready=false.
        """
        content = (
            "---\n"
            "high_severity_count: 0\n"
            "medium_severity_count: 0\n"
            "low_severity_count: 0\n"
            "total_deviations: 0\n"
            "validation_complete: false\n"
            "fidelity_check_attempted: true\n"
            "tasklist_ready: false\n"
            "---\n"
            "## Degraded Fidelity Report\n"
            "Spec-fidelity validation could not be completed.\n"
        )
        for check in SPEC_FIDELITY_GATE.semantic_checks:
            assert check.check_fn(content) is True, f"Failed: {check.name}"

    def test_spec_fidelity_gate_min_lines(self):
        assert SPEC_FIDELITY_GATE.min_lines == 20

    def test_spec_fidelity_gate_in_all_gates(self):
        """SPEC_FIDELITY_GATE is registered in ALL_GATES."""
        gate_names = {name for name, _gate in ALL_GATES}
        assert "spec-fidelity" in gate_names
        gate = next(g for name, g in ALL_GATES if name == "spec-fidelity")
        assert gate is SPEC_FIDELITY_GATE


# ═══════════════════════════════════════════════════════════════
# T06.01 -- DEVIATION_ANALYSIS_GATE semantic check functions
# ═══════════════════════════════════════════════════════════════


class TestNoAmbiguousDeviations:
    """_no_ambiguous_deviations: boundary-input unit tests."""

    def test_zero_passes(self):
        assert _no_ambiguous_deviations("---\nambiguous_deviations: 0\n---\n") is True

    def test_nonzero_fails(self):
        assert _no_ambiguous_deviations("---\nambiguous_deviations: 1\n---\n") is False

    def test_missing_field_fail_closed(self):
        assert _no_ambiguous_deviations("---\nslip_count: 3\n---\n") is False

    def test_no_frontmatter_fail_closed(self):
        assert _no_ambiguous_deviations("No frontmatter.\n") is False

    def test_non_integer_fail_closed(self):
        assert (
            _no_ambiguous_deviations("---\nambiguous_deviations: not_a_number\n---\n")
            is False
        )

    def test_large_count_fails(self):
        assert _no_ambiguous_deviations("---\nambiguous_deviations: 10\n---\n") is False


class TestCertifiedIsTrue:
    """_certified_is_true: true/false/missing/malformed boundary tests (SC-5)."""

    def test_true_passes(self):
        assert _certified_is_true("---\ncertified: true\n---\n") is True

    def test_true_mixed_case_passes(self):
        assert _certified_is_true("---\ncertified: True\n---\n") is True

    def test_false_fails(self):
        assert _certified_is_true("---\ncertified: false\n---\n") is False

    def test_missing_field_fails(self):
        assert _certified_is_true("---\nfindings_verified: 3\n---\n") is False

    def test_malformed_yes_fails(self):
        assert _certified_is_true("---\ncertified: yes\n---\n") is False

    def test_malformed_one_fails(self):
        assert _certified_is_true("---\ncertified: 1\n---\n") is False

    def test_empty_value_fails(self):
        assert _certified_is_true("---\ncertified: \n---\n") is False

    def test_no_frontmatter_fails(self):
        assert _certified_is_true("No frontmatter here.\n") is False


class TestValidationCompleteTrue:
    """_validation_complete_true: analysis_complete boundary tests."""

    def test_true_passes(self):
        assert _validation_complete_true("---\nanalysis_complete: true\n---\n") is True

    def test_false_fails(self):
        assert (
            _validation_complete_true("---\nanalysis_complete: false\n---\n") is False
        )

    def test_missing_field_fails(self):
        assert _validation_complete_true("---\nslip_count: 2\n---\n") is False

    def test_no_frontmatter_fails(self):
        assert _validation_complete_true("No frontmatter.\n") is False

    def test_malformed_value_fails(self):
        assert _validation_complete_true("---\nanalysis_complete: yes\n---\n") is False


class TestRoutingIdsValid:
    """_routing_ids_valid: DEV-\\d+ validation boundary tests."""

    def test_valid_single_id(self):
        assert _routing_ids_valid("---\nrouting_fix_roadmap: DEV-001\n---\n") is True

    def test_valid_multiple_ids(self):
        content = "---\nrouting_fix_roadmap: DEV-001 DEV-002\nrouting_no_action: DEV-003\n---\n"
        assert _routing_ids_valid(content) is True

    def test_empty_routing_fields(self):
        content = "---\nrouting_fix_roadmap: \nrouting_no_action: \n---\n"
        assert _routing_ids_valid(content) is True

    def test_invalid_id_fails(self):
        assert (
            _routing_ids_valid("---\nrouting_fix_roadmap: INVALID-001\n---\n") is False
        )

    def test_mixed_valid_invalid_fails(self):
        assert (
            _routing_ids_valid("---\nrouting_fix_roadmap: DEV-001 bad-id\n---\n")
            is False
        )

    def test_no_routing_fields(self):
        assert _routing_ids_valid("---\nslip_count: 0\n---\n") is True

    def test_no_frontmatter_fails(self):
        assert _routing_ids_valid("No frontmatter.\n") is False


class TestSlipCountMatchesRouting:
    """_slip_count_matches_routing: slip_count vs routing_fix_roadmap count."""

    def test_zero_slip_empty_routing_matches(self):
        content = "---\nslip_count: 0\nrouting_fix_roadmap: \n---\n"
        assert _slip_count_matches_routing(content) is True

    def test_one_slip_one_routing_matches(self):
        content = "---\nslip_count: 1\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _slip_count_matches_routing(content) is True

    def test_two_slips_two_routing_matches(self):
        content = "---\nslip_count: 2\nrouting_fix_roadmap: DEV-001 DEV-002\n---\n"
        assert _slip_count_matches_routing(content) is True

    def test_mismatch_fails(self):
        content = "---\nslip_count: 2\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _slip_count_matches_routing(content) is False

    def test_missing_slip_count_fails(self):
        content = "---\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _slip_count_matches_routing(content) is False

    def test_non_integer_slip_count_fails(self):
        content = "---\nslip_count: many\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _slip_count_matches_routing(content) is False

    def test_no_frontmatter_fails(self):
        assert _slip_count_matches_routing("No frontmatter.\n") is False


class TestRoutingConsistentWithSlipCount:
    """_routing_consistent_with_slip_count: alias for _slip_count_matches_routing."""

    def test_consistent_passes(self):
        content = "---\nslip_count: 1\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _routing_consistent_with_slip_count(content) is True

    def test_inconsistent_fails(self):
        content = "---\nslip_count: 2\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _routing_consistent_with_slip_count(content) is False


class TestPreApprovedNotInFixRoadmap:
    """_pre_approved_not_in_fix_roadmap: no overlap between routing_no_action and routing_fix_roadmap."""

    def test_no_overlap_passes(self):
        content = "---\nrouting_no_action: DEV-003\nrouting_fix_roadmap: DEV-001 DEV-002\n---\n"
        assert _pre_approved_not_in_fix_roadmap(content) is True

    def test_overlap_fails(self):
        content = "---\nrouting_no_action: DEV-001\nrouting_fix_roadmap: DEV-001 DEV-002\n---\n"
        assert _pre_approved_not_in_fix_roadmap(content) is False

    def test_empty_both_passes(self):
        content = "---\nrouting_no_action: \nrouting_fix_roadmap: \n---\n"
        assert _pre_approved_not_in_fix_roadmap(content) is True

    def test_empty_no_action_passes(self):
        content = "---\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _pre_approved_not_in_fix_roadmap(content) is True

    def test_no_frontmatter_fails(self):
        assert _pre_approved_not_in_fix_roadmap("No frontmatter.\n") is False


class TestTotalAnalyzedConsistent:
    """_total_analyzed_consistent: sum of component fields equals total_analyzed."""

    def test_consistent_passes(self):
        content = (
            "---\ntotal_analyzed: 4\nslip_count: 1\nintentional_count: 2\n"
            "pre_approved_count: 1\nambiguous_count: 0\n---\n"
        )
        assert _total_analyzed_consistent(content) is True

    def test_inconsistent_fails(self):
        content = (
            "---\ntotal_analyzed: 5\nslip_count: 1\nintentional_count: 2\n"
            "pre_approved_count: 1\nambiguous_count: 0\n---\n"
        )
        assert _total_analyzed_consistent(content) is False

    def test_all_zeros_consistent(self):
        content = (
            "---\ntotal_analyzed: 0\nslip_count: 0\nintentional_count: 0\n"
            "pre_approved_count: 0\nambiguous_count: 0\n---\n"
        )
        assert _total_analyzed_consistent(content) is True

    def test_missing_field_fails(self):
        content = "---\ntotal_analyzed: 3\nslip_count: 1\nintentional_count: 2\n---\n"
        assert _total_analyzed_consistent(content) is False

    def test_non_integer_fails(self):
        content = (
            "---\ntotal_analyzed: many\nslip_count: 1\nintentional_count: 2\n"
            "pre_approved_count: 0\nambiguous_count: 0\n---\n"
        )
        assert _total_analyzed_consistent(content) is False

    def test_no_frontmatter_fails(self):
        assert _total_analyzed_consistent("No frontmatter.\n") is False


class TestTotalAnnotatedConsistent:
    """_total_annotated_consistent: optional total_annotated equals classified sum."""

    def test_consistent_passes(self):
        content = (
            "---\ntotal_annotated: 3\nslip_count: 1\n"
            "intentional_count: 1\npre_approved_count: 1\n---\n"
        )
        assert _total_annotated_consistent(content) is True

    def test_inconsistent_fails(self):
        content = (
            "---\ntotal_annotated: 5\nslip_count: 1\n"
            "intentional_count: 1\npre_approved_count: 1\n---\n"
        )
        assert _total_annotated_consistent(content) is False

    def test_absent_field_passes(self):
        """total_annotated is optional; absent means valid."""
        content = (
            "---\nslip_count: 1\nintentional_count: 1\npre_approved_count: 0\n---\n"
        )
        assert _total_annotated_consistent(content) is True

    def test_non_integer_fails(self):
        content = (
            "---\ntotal_annotated: many\nslip_count: 1\n"
            "intentional_count: 1\npre_approved_count: 1\n---\n"
        )
        assert _total_annotated_consistent(content) is False

    def test_no_frontmatter_fails(self):
        assert _total_annotated_consistent("No frontmatter.\n") is False


class TestDeviationAnalysisGate:
    """DEVIATION_ANALYSIS_GATE: structure and semantic check tests."""

    def test_gate_is_gate_criteria(self):
        from superclaude.cli.pipeline.models import GateCriteria

        assert isinstance(DEVIATION_ANALYSIS_GATE, GateCriteria)

    def test_gate_is_strict(self):
        assert DEVIATION_ANALYSIS_GATE.enforcement_tier == "STRICT"

    def test_gate_requires_ambiguous_count(self):
        assert "ambiguous_count" in DEVIATION_ANALYSIS_GATE.required_frontmatter_fields

    def test_gate_requires_analysis_complete(self):
        assert (
            "analysis_complete" in DEVIATION_ANALYSIS_GATE.required_frontmatter_fields
        )

    def test_gate_has_seven_semantic_checks(self):
        assert DEVIATION_ANALYSIS_GATE.semantic_checks is not None
        assert len(DEVIATION_ANALYSIS_GATE.semantic_checks) == 7

    def test_gate_semantic_check_names(self):
        names = {c.name for c in DEVIATION_ANALYSIS_GATE.semantic_checks}
        expected = {
            "no_ambiguous_deviations",
            "validation_complete_true",
            "routing_ids_valid",
            "slip_count_matches_routing",
            "pre_approved_not_in_fix_roadmap",
            "total_analyzed_consistent",
            "deviation_counts_reconciled",
        }
        assert names == expected

    def test_gate_in_all_gates(self):
        gate_names = {name for name, _ in ALL_GATES}
        assert "deviation-analysis" in gate_names

    def test_gate_passes_clean_document(self, tmp_path):
        """A well-formed deviation-analysis document passes all checks."""
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "schema_version: 1.0\n"
            "total_analyzed: 3\n"
            "slip_count: 1\n"
            "intentional_count: 1\n"
            "pre_approved_count: 1\n"
            "ambiguous_count: 0\n"
            "ambiguous_deviations: 0\n"
            "routing_fix_roadmap: DEV-001\n"
            "routing_update_spec: DEV-003\n"
            "routing_no_action: DEV-002\n"
            "routing_human_review: \n"
            "analysis_complete: true\n"
            "---\n"
        ) + "\n".join([f"- deviation line {i}" for i in range(25)])
        doc = tmp_path / "deviation-analysis.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, DEVIATION_ANALYSIS_GATE)
        assert passed is True, f"Expected pass, got reason: {reason}"

    def test_gate_fails_ambiguous_deviation(self, tmp_path):
        """Ambiguous deviation (ambiguous_deviations=1) fails gate (SC-T05.03)."""
        from superclaude.cli.pipeline.gates import gate_passed

        content = (
            "---\n"
            "schema_version: 1.0\n"
            "total_analyzed: 2\n"
            "slip_count: 1\n"
            "intentional_count: 0\n"
            "pre_approved_count: 0\n"
            "ambiguous_count: 1\n"
            "ambiguous_deviations: 1\n"
            "routing_fix_roadmap: DEV-001\n"
            "routing_update_spec: \n"
            "routing_no_action: \n"
            "routing_human_review: DEV-002\n"
            "analysis_complete: true\n"
            "---\n"
        ) + "\n".join([f"- deviation line {i}" for i in range(25)])
        doc = tmp_path / "deviation-analysis.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, DEVIATION_ANALYSIS_GATE)
        assert passed is False
        assert reason is not None


# ═══════════════════════════════════════════════════════════════
# yaml.safe_load parser replacement -- quote tolerance tests
# ═══════════════════════════════════════════════════════════════


class TestParseFrontmatterYaml:
    """Tests for yaml.safe_load-based _parse_frontmatter."""

    def test_quoted_colon_value_stripped(self):
        """The original bug: quoted '1:1' must not retain quote chars."""
        content = '---\ninterleave_ratio: "1:1"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm is not None
        assert fm["interleave_ratio"] == "1:1"

    def test_unquoted_colon_value(self):
        """Unquoted colon value parsed correctly."""
        content = "---\ninterleave_ratio: 1:1\n---\n"
        fm = _parse_frontmatter(content)
        assert fm is not None
        assert fm["interleave_ratio"] == "1:1"

    def test_single_quoted_value(self):
        content = "---\ninterleave_ratio: '1:1'\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["interleave_ratio"] == "1:1"

    def test_integer_value_unchanged(self):
        content = "---\nhigh_severity_count: 0\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["high_severity_count"] == "0"

    def test_float_value_unchanged(self):
        content = "---\nconvergence_score: 0.85\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["convergence_score"] == "0.85"

    def test_boolean_value_unchanged(self):
        """Hand-rolled parser keeps booleans as strings (no type coercion)."""
        content = "---\ncertified: true\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["certified"] == "true"

    def test_empty_value_is_empty_string(self):
        content = "---\ntitle:\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["title"] == ""

    def test_no_frontmatter_returns_none(self):
        assert _parse_frontmatter("No frontmatter here.") is None

    def test_quoted_string_stripped(self):
        content = '---\nspec_source: "my-spec.md"\n---\n'
        fm = _parse_frontmatter(content)
        assert fm["spec_source"] == "my-spec.md"

    def test_single_quoted_string_stripped(self):
        content = "---\nspec_source: 'my-spec.md'\n---\n"
        fm = _parse_frontmatter(content)
        assert fm["spec_source"] == "my-spec.md"


class TestInterleaveRatioQuotedValues:
    """Regression tests for the quoted-value bug (RC-1)."""

    def test_quoted_high_1_1_passes(self):
        """The exact failure case from production."""
        content = '---\ncomplexity_class: HIGH\ninterleave_ratio: "1:1"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_quoted_medium_1_2_passes(self):
        content = '---\ncomplexity_class: MEDIUM\ninterleave_ratio: "1:2"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_quoted_low_1_3_passes(self):
        content = '---\ncomplexity_class: LOW\ninterleave_ratio: "1:3"\n---\n'
        assert _interleave_ratio_consistent(content) is True

    def test_single_quoted_high_1_1_passes(self):
        content = "---\ncomplexity_class: HIGH\ninterleave_ratio: '1:1'\n---\n"
        assert _interleave_ratio_consistent(content) is True


class TestValidationPhilosophyQuoteTolerance:
    def test_quoted_value_passes(self):
        content = '---\nvalidation_philosophy: "continuous-parallel"\n---\n'
        assert _validation_philosophy_correct(content) is True


class TestMajorIssuePolicyQuoteTolerance:
    def test_quoted_value_passes(self):
        content = '---\nmajor_issue_policy: "stop-and-fix"\n---\n'
        assert _major_issue_policy_correct(content) is True


class TestHighSeverityCountQuoteTolerance:
    def test_quoted_zero_passes(self):
        content = '---\nhigh_severity_count: "0"\n---\n'
        assert _high_severity_count_zero(content) is True


class TestConvergenceScoreQuoteTolerance:
    def test_quoted_float_passes(self):
        content = '---\nconvergence_score: "0.85"\n---\n'
        assert _convergence_score_valid(content) is True


class TestCertifiedIsTrueQuoteTolerance:
    def test_quoted_true_passes(self):
        content = '---\ncertified: "true"\n---\n'
        assert _certified_is_true(content) is True


# ═══════════════════════════════════════════════════════════════
# Deviation count reconciliation (SC-008)
# ═══════════════════════════════════════════════════════════════


class TestDeviationCountsReconciled:
    """SC-008: Cross-gate deviation count reconciliation."""

    def test_reconciled_when_counts_match(self):
        content = (
            "---\n"
            "total_analyzed: 3\n"
            "routing_fix_roadmap: DEV-001\n"
            "routing_update_spec: DEV-003\n"
            "routing_no_action: DEV-002\n"
            "routing_human_review: \n"
            "---\n"
        )
        assert _deviation_counts_reconciled(content) is True

    def test_fails_when_reported_exceeds_actual(self):
        """Deterministic failure: total_analyzed=3 but only 2 IDs routed."""
        content = (
            "---\n"
            "total_analyzed: 3\n"
            "routing_fix_roadmap: DEV-001\n"
            "routing_no_action: DEV-002\n"
            "---\n"
        )
        assert _deviation_counts_reconciled(content) is False

    def test_fails_when_actual_exceeds_reported(self):
        """Deterministic failure: total_analyzed=2 but 3 IDs routed."""
        content = (
            "---\n"
            "total_analyzed: 2\n"
            "routing_fix_roadmap: DEV-001 DEV-002\n"
            "routing_no_action: DEV-003\n"
            "---\n"
        )
        assert _deviation_counts_reconciled(content) is False

    def test_all_routing_empty_matches_zero(self):
        content = (
            "---\n"
            "total_analyzed: 0\n"
            "routing_fix_roadmap: \n"
            "routing_no_action: \n"
            "---\n"
        )
        assert _deviation_counts_reconciled(content) is True

    def test_duplicate_ids_counted_once(self):
        """Same ID in two routing fields is still one unique deviation."""
        content = (
            "---\n"
            "total_analyzed: 1\n"
            "routing_fix_roadmap: DEV-001\n"
            "routing_human_review: DEV-001\n"
            "---\n"
        )
        assert _deviation_counts_reconciled(content) is True

    def test_missing_frontmatter_fails(self):
        assert _deviation_counts_reconciled("No frontmatter here.") is False

    def test_missing_total_analyzed_fails(self):
        content = "---\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _deviation_counts_reconciled(content) is False

    def test_non_integer_total_analyzed_fails(self):
        content = "---\ntotal_analyzed: three\nrouting_fix_roadmap: DEV-001\n---\n"
        assert _deviation_counts_reconciled(content) is False

    def test_gate_failure_on_mismatch_is_deterministic(self, tmp_path):
        """SC-008: deviation count mismatch causes deterministic gate failure."""
        from superclaude.cli.pipeline.gates import gate_passed

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
            "routing_update_spec: DEV-003\n"
            "routing_no_action: \n"
            "routing_human_review: \n"
            "analysis_complete: true\n"
            "---\n"
        ) + "\n".join([f"- deviation line {i}" for i in range(25)])
        doc = tmp_path / "deviation-analysis.md"
        doc.write_text(content, encoding="utf-8")
        passed, reason = gate_passed(doc, DEVIATION_ANALYSIS_GATE)
        # total_analyzed=4 but only 3 unique IDs → deterministic failure
        assert passed is False
        assert "deviation_counts_reconciled" in reason.lower() or "SC-008" in reason
