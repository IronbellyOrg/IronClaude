"""Tests for BF-6 and BF-7: Semantic layer, debate protocol, prompt budget."""
import pytest
from superclaude.cli.roadmap.semantic_layer import (
    RubricScores,
    score_argument,
    judge_verdict,
    _truncate_to_budget,
    build_semantic_prompt,
    SemanticCheckRequest,
    MAX_PROMPT_BYTES,
    VERDICT_MARGIN_THRESHOLD,
    wire_debate_verdict,
)


# --- BF-6: Debate protocol ---


class TestRubricScoring:
    """BF-6: Deterministic rubric scoring."""

    def test_weighted_score_range(self):
        """Weighted score is in [0.0, 1.0]."""
        zero = RubricScores(0, 0, 0, 0)
        max_scores = RubricScores(3, 3, 3, 3)
        assert zero.weighted_score == 0.0
        assert max_scores.weighted_score == 1.0

    def test_score_determinism(self):
        """Same scores always produce same weighted result."""
        s1 = RubricScores(2, 1, 3, 0)
        s2 = RubricScores(2, 1, 3, 0)
        assert s1.weighted_score == s2.weighted_score

    def test_score_argument_empty_response(self):
        """Empty response scores zero across all criteria."""
        scores = score_argument({})
        assert scores.evidence_quality == 0
        assert scores.impact_specificity == 0

    def test_score_argument_strong_response(self):
        """Well-structured response scores higher."""
        response = {
            "argument": " ".join(["word"] * 120)
            + " however this has caveats although limited",
            "evidence_points": ["point1", "point2", "point3"],
            "confidence": 0.9,
        }
        scores = score_argument(response)
        assert scores.evidence_quality == 3
        assert scores.impact_specificity == 3
        assert scores.logical_coherence == 3
        assert scores.concession_handling >= 2  # "however" + "although"


class TestJudgeVerdict:
    """BF-6: Deterministic verdict from rubric scores."""

    def test_clear_prosecutor_win(self):
        """Strong prosecutor -> CONFIRM_HIGH."""
        p = RubricScores(3, 3, 3, 3)
        d = RubricScores(0, 0, 0, 0)
        verdict, margin = judge_verdict(p, d)
        assert verdict == "CONFIRM_HIGH"
        assert margin > VERDICT_MARGIN_THRESHOLD

    def test_clear_defender_win(self):
        """Strong defender -> DOWNGRADE."""
        p = RubricScores(0, 0, 0, 0)
        d = RubricScores(3, 3, 3, 3)
        verdict, margin = judge_verdict(p, d, defender_recommendation="MEDIUM")
        assert verdict == "DOWNGRADE_TO_MEDIUM"
        assert margin < -VERDICT_MARGIN_THRESHOLD

    def test_tiebreak_favors_high(self):
        """Equal scores -> CONFIRM_HIGH (conservative)."""
        p = RubricScores(2, 2, 2, 2)
        d = RubricScores(2, 2, 2, 2)
        verdict, margin = judge_verdict(p, d)
        assert verdict == "CONFIRM_HIGH"


# --- BF-7: Prompt budget enforcement ---


class TestPromptBudget:
    """BF-7: 30KB prompt size enforcement."""

    def test_truncate_within_budget(self):
        """Content within budget is unchanged."""
        text = "Hello world\n"
        result = _truncate_to_budget(text, 1000)
        assert result == text

    def test_truncate_oversized(self):
        """Oversized content is truncated with marker."""
        text = "x" * 50_000
        result = _truncate_to_budget(text, 1000)
        assert len(result.encode("utf-8")) <= 1000
        assert "TRUNCATED" in result

    def test_truncate_on_line_boundary(self):
        """Truncation happens on line boundaries."""
        lines = ["Line " + str(i) for i in range(100)]
        text = "\n".join(lines)
        result = _truncate_to_budget(text, 200)
        # Should not end mid-line (before the marker)
        before_marker = result.split("[TRUNCATED")[0]
        assert before_marker.endswith("\n") or before_marker == ""

    def test_build_prompt_under_budget(self):
        """Normal prompt stays under 30KB."""
        request = SemanticCheckRequest(
            dimension="signatures",
            spec_sections=[],
            roadmap_sections=[],
            structural_findings=[],
            prior_findings_summary="No prior findings",
        )
        prompt = build_semantic_prompt(request)
        assert len(prompt.encode("utf-8")) <= MAX_PROMPT_BYTES

    def test_build_prompt_large_input_still_under_budget(self):
        """Even with large input, prompt respects budget."""

        class FakeSection:
            def __init__(self, heading, content):
                self.heading = heading
                self.content = content

        large_section = FakeSection("Big Section", "x " * 20_000)
        request = SemanticCheckRequest(
            dimension="signatures",
            spec_sections=[large_section],
            roadmap_sections=[large_section],
            structural_findings=[],
            prior_findings_summary="summary " * 5000,
        )
        prompt = build_semantic_prompt(request)
        assert len(prompt.encode("utf-8")) <= MAX_PROMPT_BYTES
        assert "TRUNCATED" in prompt
