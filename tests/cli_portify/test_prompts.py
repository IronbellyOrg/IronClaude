"""Tests for prompt builder framework.

Covers:
- Prompt builders exist for all 5 Claude-assisted steps (Steps 3-7)
- Each builder constructs prompts with @path references to prior artifacts
- Output contracts and frontmatter expectations are embedded
- Retry augmentation supports targeted failures (placeholder residue)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.cli_portify.prompts import (
    AnalyzeWorkflowPrompt,
    BasePromptBuilder,
    BrainstormGapsPrompt,
    DesignPipelinePrompt,
    PanelReviewPrompt,
    PromptContext,
    SynthesizeSpecPrompt,
)


@pytest.fixture
def ctx(tmp_path):
    return PromptContext(
        workflow_path=tmp_path / "workflow",
        work_dir=tmp_path / "output",
        cli_name="test-cli",
        source_skill="test-skill",
        iteration=1,
        max_convergence=3,
    )


class TestAtPathReferences:
    """Each builder constructs prompts with @path references to prior artifacts."""

    def test_analyze_workflow_refs_inventory(self, ctx):
        builder = AnalyzeWorkflowPrompt(ctx)
        prompt = builder.build()
        expected_ref = str(
            (ctx.work_dir / "results" / "component-inventory.md").resolve()
        )
        assert f"@{expected_ref}" in prompt

    def test_design_pipeline_refs_two_artifacts(self, ctx):
        builder = DesignPipelinePrompt(ctx)
        prompt = builder.build()
        assert "@" in prompt
        refs = [line for line in prompt.splitlines() if line.startswith("@")]
        assert len(refs) == 2

    def test_synthesize_spec_refs_analysis_and_design(self, ctx):
        builder = SynthesizeSpecPrompt(ctx)
        refs = builder.input_artifacts()
        assert len(refs) == 2
        ref_names = [r.name for r in refs]
        assert "portify-analysis.md" in ref_names
        assert "portify-spec.md" in ref_names

    def test_brainstorm_gaps_refs_synthesized(self, ctx):
        builder = BrainstormGapsPrompt(ctx)
        refs = builder.input_artifacts()
        assert len(refs) == 1
        assert refs[0].name == "synthesized-spec.md"

    def test_panel_review_refs_spec_and_gaps(self, ctx):
        builder = PanelReviewPrompt(ctx)
        refs = builder.input_artifacts()
        assert len(refs) == 2
        ref_names = [r.name for r in refs]
        assert "synthesized-spec.md" in ref_names
        assert "brainstorm-gaps.md" in ref_names


class TestRetryAugmentation:
    """Retry augmentation supports targeted failures (placeholder residue)."""

    def test_retry_includes_failure_reason(self, ctx):
        builder = AnalyzeWorkflowPrompt(ctx)
        retry = builder.build_retry("Missing section: Complexity Assessment")
        assert "RETRY CONTEXT" in retry
        assert "Missing section: Complexity Assessment" in retry

    def test_retry_includes_remaining_placeholders(self, ctx):
        builder = SynthesizeSpecPrompt(ctx)
        retry = builder.build_retry(
            "Placeholder sentinels remaining",
            remaining_placeholders=[
                "{{SC_PLACEHOLDER:data_flow}}",
                "{{SC_PLACEHOLDER:error_handling}}",
            ],
        )
        assert "{{SC_PLACEHOLDER:data_flow}}" in retry
        assert "{{SC_PLACEHOLDER:error_handling}}" in retry
        assert "MUST be resolved" in retry

    def test_retry_without_placeholders(self, ctx):
        builder = DesignPipelinePrompt(ctx)
        retry = builder.build_retry("Gate check failed")
        assert "RETRY CONTEXT" in retry
        # Should not contain the "MUST be resolved" placeholder list section
        assert "MUST be resolved" not in retry

    def test_retry_preserves_base_prompt(self, ctx):
        builder = BrainstormGapsPrompt(ctx)
        base = builder.build()
        retry = builder.build_retry("test failure")
        assert base in retry


class TestStepNames:
    """Each builder reports the correct step_name."""

    @pytest.mark.parametrize(
        "cls,expected",
        [
            (AnalyzeWorkflowPrompt, "analyze-workflow"),
            (DesignPipelinePrompt, "design-pipeline"),
            (SynthesizeSpecPrompt, "synthesize-spec"),
            (BrainstormGapsPrompt, "brainstorm-gaps"),
            (PanelReviewPrompt, "panel-review"),
        ],
    )
    def test_step_name_correct(self, cls, expected, ctx):
        builder = cls(ctx)
        assert builder.step_name == expected
