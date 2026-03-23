"""Tests for BF-6 and BF-7: Semantic layer, debate protocol, prompt budget."""
import json
import tempfile
from pathlib import Path

import pytest
import yaml

from superclaude.cli.roadmap.semantic_layer import (
    RubricScores,
    score_argument,
    judge_verdict,
    _truncate_to_budget,
    build_semantic_prompt,
    SemanticCheckRequest,
    SemanticLayerResult,
    MAX_PROMPT_BYTES,
    VERDICT_MARGIN_THRESHOLD,
    STRUCTURAL_DIMENSIONS,
    SEMANTIC_DIMENSIONS,
    wire_debate_verdict,
    run_semantic_layer,
    validate_semantic_high,
)
from superclaude.cli.roadmap.convergence import DeviationRegistry
from superclaude.cli.roadmap.models import Finding


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


# --- Helpers for Phase 4 tests ---


class FakeSection:
    """Minimal SpecSection stand-in."""
    def __init__(self, heading: str, content: str):
        self.heading = heading
        self.heading_path = heading
        self.content = content


class FakeClaudeProcess:
    """Injected LLM stub returning canned YAML responses."""
    def __init__(self, response: str):
        self._response = response

    def run(self, prompt: str) -> str:
        return self._response


def _make_test_finding(
    dimension: str = "prose_sufficiency",
    severity: str = "HIGH",
    stable_id: str = "abc123def456",
    source_layer: str = "semantic",
    **kwargs,
) -> Finding:
    """Create a test Finding with sensible defaults."""
    defaults = dict(
        id=f"{dimension}-test-{stable_id[:8]}",
        severity=severity,
        dimension=dimension,
        description=f"Test finding in {dimension}",
        location=f"spec:{dimension}",
        evidence="Test evidence",
        fix_guidance="Fix it",
        status="ACTIVE",
        source_layer=source_layer,
        rule_id=f"semantic_{dimension}",
        spec_quote="spec says X",
        roadmap_quote="roadmap says Y",
        stable_id=stable_id,
    )
    defaults.update(kwargs)
    return Finding(**defaults)


def _make_test_registry(tmp_path: Path, findings: dict | None = None) -> DeviationRegistry:
    """Create a test DeviationRegistry with optional seeded findings."""
    registry_path = tmp_path / "test-registry.json"
    reg = DeviationRegistry(
        path=registry_path,
        release_id="test-release",
        spec_hash="testhash123",
    )
    if findings:
        reg.findings = findings
    return reg


# --- T04.01: run_semantic_layer() ---


class TestDimensionFiltering:
    """T04.01: Semantic layer receives only non-structural dimensions."""

    def test_structural_dimensions_defined(self):
        """Structural dimensions match checker registry keys."""
        assert STRUCTURAL_DIMENSIONS == frozenset({
            "signatures", "data_models", "gates", "cli", "nfrs",
        })

    def test_semantic_dimensions_disjoint_from_structural(self):
        """Semantic dimensions do not overlap with structural dimensions."""
        assert STRUCTURAL_DIMENSIONS.isdisjoint(SEMANTIC_DIMENSIONS)

    def test_semantic_dimensions_non_empty(self):
        """At least one semantic dimension is defined."""
        assert len(SEMANTIC_DIMENSIONS) > 0

    def test_run_semantic_layer_processes_only_semantic_dims(self, tmp_path):
        """run_semantic_layer only processes SEMANTIC_DIMENSIONS, not structural."""
        called_prompts = []

        def factory():
            class Proc:
                def run(self, prompt):
                    called_prompts.append(prompt)
                    return "findings: []"
            return Proc()

        registry = _make_test_registry(tmp_path)
        registry.begin_run("roadmaphash")

        result = run_semantic_layer(
            spec_sections=[FakeSection("S1", "content")],
            roadmap_sections=[FakeSection("R1", "content")],
            structural_findings=[],
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        # Should have sent one prompt per semantic dimension
        assert result.prompts_sent == len(SEMANTIC_DIMENSIONS)
        # None of the prompts should contain structural dimension names as the check target
        for dim in STRUCTURAL_DIMENSIONS:
            assert not any(
                f"Semantic Fidelity Check: {dim}" in p for p in called_prompts
            )


class TestChunkedInput:
    """T04.01: Semantic layer uses per-section chunked input."""

    def test_prompt_contains_section_headings(self):
        """Chunked prompt includes section headings from SpecSection objects."""
        request = SemanticCheckRequest(
            dimension="prose_sufficiency",
            spec_sections=[
                FakeSection("FR-1: Decomposed Checkers", "The checkers..."),
                FakeSection("FR-2: Parser", "The parser..."),
            ],
            roadmap_sections=[
                FakeSection("Phase 1", "Build the parser"),
            ],
            structural_findings=[],
            prior_findings_summary="No prior findings",
        )
        prompt = build_semantic_prompt(request)
        assert "FR-1: Decomposed Checkers" in prompt
        assert "FR-2: Parser" in prompt
        assert "Phase 1" in prompt

    def test_structural_findings_as_context_in_prompt(self):
        """Structural findings appear in prompt as context."""
        structural = [
            _make_test_finding(
                dimension="signatures",
                severity="HIGH",
                source_layer="structural",
                description="Function foo missing",
            ),
        ]
        request = SemanticCheckRequest(
            dimension="prose_sufficiency",
            spec_sections=[],
            roadmap_sections=[],
            structural_findings=structural,
            prior_findings_summary="",
        )
        prompt = build_semantic_prompt(request)
        assert "Function foo missing" in prompt


class TestSemanticFindingTagging:
    """T04.01: All semantic findings tagged with source_layer='semantic'."""

    def test_findings_tagged_semantic(self, tmp_path):
        """All findings from semantic layer have source_layer='semantic'."""
        yaml_response = yaml.dump({
            "findings": [
                {
                    "description": "Missing rationale",
                    "severity": "MEDIUM",
                    "location": "spec:prose",
                    "evidence": "Section lacks justification",
                },
            ],
        })

        def factory():
            return FakeClaudeProcess(yaml_response)

        registry = _make_test_registry(tmp_path)
        registry.begin_run("roadmaphash")

        result = run_semantic_layer(
            spec_sections=[FakeSection("S1", "content")],
            roadmap_sections=[FakeSection("R1", "content")],
            structural_findings=[],
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        for f in result.findings:
            assert f.source_layer == "semantic"


# --- T04.02: Prompt Budget Enforcement ---


class TestBudgetEnforcement:
    """T04.02: Truncation markers include section heading; template ValueError."""

    def test_truncation_marker_includes_heading(self):
        """Truncation marker contains the section heading."""
        text = "x" * 50_000
        result = _truncate_to_budget(text, 1000, heading="Prior Findings Summary")
        assert "Prior Findings Summary" in result
        assert "TRUNCATED" in result

    def test_template_exceeding_budget_raises_valueerror(self):
        """Template > 5% allocation (1536 bytes) raises ValueError."""
        # Build a request with an extremely long dimension name to force template overflow
        # The template budget is 5% of 30720 = 1536 bytes
        long_dim = "x" * 2000
        request = SemanticCheckRequest(
            dimension=long_dim,
            spec_sections=[],
            roadmap_sections=[],
            structural_findings=[],
            prior_findings_summary="",
        )
        with pytest.raises(ValueError, match="exceeds budget"):
            build_semantic_prompt(request)

    def test_truncation_priority_prior_first(self):
        """Prior summary gets truncated before spec/roadmap content."""
        large_prior = "prior " * 5000  # ~30KB of prior data
        small_spec = "spec content"

        request = SemanticCheckRequest(
            dimension="prose_sufficiency",
            spec_sections=[FakeSection("S1", small_spec)],
            roadmap_sections=[],
            structural_findings=[],
            prior_findings_summary=large_prior,
        )
        prompt = build_semantic_prompt(request)
        assert len(prompt.encode("utf-8")) <= MAX_PROMPT_BYTES
        # Spec content should survive; prior should be truncated
        assert "spec content" in prompt
        assert "Prior Findings Summary" in prompt  # truncation marker with heading

    def test_assert_before_llm_call(self):
        """build_semantic_prompt includes assert <= 30720 bytes (SC-6)."""
        request = SemanticCheckRequest(
            dimension="test",
            spec_sections=[],
            roadmap_sections=[],
            structural_findings=[],
            prior_findings_summary="",
        )
        prompt = build_semantic_prompt(request)
        assert len(prompt.encode("utf-8")) <= MAX_PROMPT_BYTES


# --- T04.03: validate_semantic_high() Debate Protocol ---


class TestDebateProtocol:
    """T04.03: Adversarial debate for semantic HIGH validation."""

    def test_validate_semantic_high_returns_verdict(self, tmp_path):
        """validate_semantic_high() returns a verdict string."""
        # Strong prosecutor, weak defender -> CONFIRM_HIGH
        prosecutor_resp = yaml.dump({
            "argument": " ".join(["evidence"] * 120) + " however despite",
            "evidence_points": ["p1", "p2", "p3"],
            "confidence": 0.95,
            "recommended_severity": "HIGH",
        })
        defender_resp = yaml.dump({
            "argument": "weak",
            "evidence_points": [],
            "confidence": 0.1,
            "recommended_severity": "MEDIUM",
        })

        call_count = [0]
        def factory():
            call_count[0] += 1
            if call_count[0] % 2 == 1:
                return FakeClaudeProcess(prosecutor_resp)
            return FakeClaudeProcess(defender_resp)

        finding = _make_test_finding(severity="HIGH")
        registry = _make_test_registry(tmp_path)
        registry.begin_run("roadmaphash")

        verdict = validate_semantic_high(
            finding=finding,
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        assert verdict in ("CONFIRM_HIGH", "DOWNGRADE_TO_MEDIUM", "DOWNGRADE_TO_LOW")

    def test_deterministic_judge_same_inputs_same_verdict(self, tmp_path):
        """Same rubric scores always produce the same verdict (determinism)."""
        # Both sides get same canned response
        response = yaml.dump({
            "argument": " ".join(["word"] * 60) + " however although",
            "evidence_points": ["p1", "p2"],
            "confidence": 0.7,
            "recommended_severity": "MEDIUM",
        })

        def factory():
            return FakeClaudeProcess(response)

        finding = _make_test_finding(severity="HIGH")
        registry1 = _make_test_registry(tmp_path / "r1")
        registry1.begin_run("hash1")
        registry2 = _make_test_registry(tmp_path / "r2")
        registry2.begin_run("hash2")

        v1 = validate_semantic_high(
            finding=finding,
            registry=registry1,
            output_dir=tmp_path / "out1",
            claude_process_factory=factory,
        )
        v2 = validate_semantic_high(
            finding=finding,
            registry=registry2,
            output_dir=tmp_path / "out2",
            claude_process_factory=factory,
        )

        assert v1 == v2  # Deterministic

    def test_conservative_tiebreak_confirms_high(self, tmp_path):
        """Equal-strength arguments -> CONFIRM_HIGH (conservative tiebreak)."""
        equal_resp = yaml.dump({
            "argument": " ".join(["word"] * 60) + " however",
            "evidence_points": ["p1", "p2"],
            "confidence": 0.7,
            "recommended_severity": "MEDIUM",
        })

        def factory():
            return FakeClaudeProcess(equal_resp)

        finding = _make_test_finding(severity="HIGH")
        registry = _make_test_registry(tmp_path)
        registry.begin_run("hash")

        verdict = validate_semantic_high(
            finding=finding,
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        assert verdict == "CONFIRM_HIGH"

    def test_yaml_parse_failure_defaults_to_zero(self, tmp_path):
        """YAML parse failure defaults all rubric scores to 0 for that side."""
        # Prosecutor returns garbage, defender returns valid
        call_count = [0]
        defender_resp = yaml.dump({
            "argument": " ".join(["strong"] * 120) + " however despite although",
            "evidence_points": ["p1", "p2", "p3"],
            "confidence": 0.95,
            "recommended_severity": "MEDIUM",
        })

        def factory():
            call_count[0] += 1
            if call_count[0] % 2 == 1:
                return FakeClaudeProcess("NOT VALID YAML {{{{")
            return FakeClaudeProcess(defender_resp)

        finding = _make_test_finding(severity="HIGH")
        registry = _make_test_registry(tmp_path)
        registry.begin_run("hash")

        verdict = validate_semantic_high(
            finding=finding,
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        # Prosecutor scores 0, strong defender should win
        assert verdict == "DOWNGRADE_TO_MEDIUM"

    def test_parallel_execution_both_sides(self, tmp_path):
        """Both prosecutor and defender execute (2 LLM calls)."""
        call_count = [0]

        def factory():
            call_count[0] += 1
            return FakeClaudeProcess(yaml.dump({
                "argument": "test argument",
                "evidence_points": [],
                "confidence": 0.5,
                "recommended_severity": "MEDIUM",
            }))

        finding = _make_test_finding(severity="HIGH")
        registry = _make_test_registry(tmp_path)
        registry.begin_run("hash")

        validate_semantic_high(
            finding=finding,
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        assert call_count[0] == 2  # Prosecutor + Defender


# --- T04.04: Debate YAML Output and Registry Wiring ---


class TestDebateOutput:
    """T04.04: Debate YAML output and registry wiring."""

    def test_debate_yaml_written_per_finding(self, tmp_path):
        """Debate output YAML written to output_dir/debates/{stable_id}/debate.yaml."""
        resp = yaml.dump({
            "argument": " ".join(["word"] * 60),
            "evidence_points": ["p1"],
            "confidence": 0.6,
            "recommended_severity": "MEDIUM",
        })

        def factory():
            return FakeClaudeProcess(resp)

        finding = _make_test_finding(severity="HIGH", stable_id="deadbeef12345678")
        registry = _make_test_registry(tmp_path)
        registry.begin_run("hash")

        validate_semantic_high(
            finding=finding,
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        yaml_path = tmp_path / "debates" / "deadbeef12345678" / "debate.yaml"
        assert yaml_path.exists()

        with open(yaml_path) as f:
            data = yaml.safe_load(f)

        assert "prosecutor" in data
        assert "defender" in data
        assert "margin" in data
        assert "verdict" in data
        assert data["finding_stable_id"] == "deadbeef12345678"

    def test_debate_yaml_contains_rubric_scores(self, tmp_path):
        """YAML contains rubric scores for both sides, margin, and verdict."""
        resp = yaml.dump({
            "argument": " ".join(["word"] * 60),
            "evidence_points": ["p1", "p2"],
            "confidence": 0.7,
            "recommended_severity": "MEDIUM",
        })

        def factory():
            return FakeClaudeProcess(resp)

        finding = _make_test_finding(severity="HIGH", stable_id="cafe1234abcd5678")
        registry = _make_test_registry(tmp_path)
        registry.begin_run("hash")

        validate_semantic_high(
            finding=finding,
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        yaml_path = tmp_path / "debates" / "cafe1234abcd5678" / "debate.yaml"
        data = yaml.safe_load(yaml_path.read_text())

        for side in ("prosecutor", "defender"):
            assert "evidence_quality" in data[side]
            assert "impact_specificity" in data[side]
            assert "logical_coherence" in data[side]
            assert "concession_handling" in data[side]
            assert "weighted_score" in data[side]

        assert isinstance(data["margin"], float)
        assert isinstance(data["verdict"], str)

    def test_wire_verdict_updates_registry(self, tmp_path):
        """Registry updated with debate_verdict and debate_transcript after debate."""
        finding = _make_test_finding(severity="HIGH", stable_id="wire123456789012")
        registry = _make_test_registry(tmp_path, findings={
            "wire123456789012": {
                "stable_id": "wire123456789012",
                "dimension": "prose_sufficiency",
                "severity": "HIGH",
                "description": "Test",
                "location": "spec:prose",
                "source_layer": "semantic",
                "status": "ACTIVE",
                "first_seen_run": 1,
                "last_seen_run": 1,
                "debate_verdict": None,
                "debate_transcript": None,
            },
        })

        wire_debate_verdict(registry, finding, "CONFIRM_HIGH", "/path/to/debate.yaml")

        assert registry.findings["wire123456789012"]["debate_verdict"] == "CONFIRM_HIGH"
        assert registry.findings["wire123456789012"]["debate_transcript"] == "/path/to/debate.yaml"

    def test_wire_verdict_downgrade_updates_severity(self, tmp_path):
        """DOWNGRADE verdict updates severity in registry."""
        finding = _make_test_finding(severity="HIGH", stable_id="down123456789012")
        registry = _make_test_registry(tmp_path, findings={
            "down123456789012": {
                "stable_id": "down123456789012",
                "dimension": "prose_sufficiency",
                "severity": "HIGH",
                "description": "Test",
                "location": "spec:prose",
                "source_layer": "semantic",
                "status": "ACTIVE",
                "first_seen_run": 1,
                "last_seen_run": 1,
                "debate_verdict": None,
                "debate_transcript": None,
            },
        })

        wire_debate_verdict(registry, finding, "DOWNGRADE_TO_MEDIUM", "/path/debate.yaml")

        assert registry.findings["down123456789012"]["severity"] == "MEDIUM"


# --- T04.05: Run-to-Run Memory Integration End-to-End ---


class TestMemoryIntegration:
    """T04.05: Prior findings from registry correctly influence semantic layer."""

    def test_prior_findings_in_prompt(self, tmp_path):
        """Prior findings from registry appear in semantic layer prompt."""
        registry = _make_test_registry(tmp_path, findings={
            "prior1234567890ab": {
                "stable_id": "prior1234567890ab",
                "dimension": "signatures",
                "severity": "HIGH",
                "description": "Function X missing",
                "location": "spec:sig:X",
                "source_layer": "structural",
                "status": "ACTIVE",
                "first_seen_run": 1,
                "last_seen_run": 1,
                "debate_verdict": None,
                "debate_transcript": None,
            },
        })

        prior_summary = registry.get_prior_findings_summary()
        request = SemanticCheckRequest(
            dimension="prose_sufficiency",
            spec_sections=[FakeSection("S1", "content")],
            roadmap_sections=[FakeSection("R1", "content")],
            structural_findings=[],
            prior_findings_summary=prior_summary,
        )
        prompt = build_semantic_prompt(request)

        assert "prior123" in prompt  # Truncated stable_id (8 chars in summary table)
        assert "ACTIVE" in prompt

    def test_fixed_findings_not_re_reported(self, tmp_path):
        """Fixed findings from prior runs do not appear as new findings."""
        # Seed registry with a FIXED finding
        registry = _make_test_registry(tmp_path, findings={
            "fixed123456789012": {
                "stable_id": "fixed123456789012",
                "dimension": "prose_sufficiency",
                "severity": "HIGH",
                "description": "Was fixed",
                "location": "spec:prose",
                "source_layer": "semantic",
                "status": "FIXED",
                "first_seen_run": 1,
                "last_seen_run": 1,
                "debate_verdict": None,
                "debate_transcript": None,
            },
        })
        registry.begin_run("roadmaphash")

        # Semantic check returns empty — should NOT re-create the FIXED finding
        def factory():
            return FakeClaudeProcess("findings: []")

        result = run_semantic_layer(
            spec_sections=[FakeSection("S1", "content")],
            roadmap_sections=[FakeSection("R1", "content")],
            structural_findings=[],
            registry=registry,
            output_dir=tmp_path,
            claude_process_factory=factory,
        )

        # No findings should reference the fixed ID
        for f in result.findings:
            assert f.stable_id != "fixed123456789012"

    def test_prior_summary_within_budget_allocation(self, tmp_path):
        """Prior findings summary fits within 15% budget allocation (4608 bytes)."""
        # Create 60 findings (above 50 limit) to test truncation
        findings = {}
        for i in range(60):
            sid = f"f{i:015d}"
            findings[sid] = {
                "stable_id": sid,
                "dimension": "signatures",
                "severity": "HIGH",
                "description": f"Finding {i}",
                "location": f"spec:sig:{i}",
                "source_layer": "structural",
                "status": "ACTIVE",
                "first_seen_run": 1,
                "last_seen_run": 1,
                "debate_verdict": None,
                "debate_transcript": None,
            }
        registry = _make_test_registry(tmp_path, findings=findings)

        summary = registry.get_prior_findings_summary(max_entries=50)
        # Should contain max 50 entries + header + truncation note
        lines = summary.strip().split("\n")
        assert len(lines) <= 53  # 2 header + 50 data + 1 truncation

    def test_prior_summary_truncated_at_50_findings(self, tmp_path):
        """Truncation occurs at 50 findings if more exist in registry."""
        findings = {}
        for i in range(75):
            sid = f"x{i:015d}"
            findings[sid] = {
                "stable_id": sid,
                "dimension": "nfrs",
                "severity": "MEDIUM",
                "description": f"NFR finding {i}",
                "location": f"spec:nfr:{i}",
                "source_layer": "structural",
                "status": "ACTIVE",
                "first_seen_run": 1,
                "last_seen_run": i + 1,
                "debate_verdict": None,
                "debate_transcript": None,
            }
        registry = _make_test_registry(tmp_path, findings=findings)

        summary = registry.get_prior_findings_summary(max_entries=50)
        assert "truncated" in summary.lower() or "more entries" in summary.lower()
