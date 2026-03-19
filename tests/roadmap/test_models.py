"""Tests for roadmap/models.py -- AgentSpec, RoadmapConfig, and Finding."""

from pathlib import Path

import pytest

from superclaude.cli.pipeline.models import PipelineConfig
from superclaude.cli.roadmap.models import (
    AgentSpec,
    Finding,
    RoadmapConfig,
    VALID_DEVIATION_CLASSES,
)


class TestAgentSpec:
    def test_parse_model_persona(self):
        a = AgentSpec.parse("opus:architect")
        assert a.model == "opus"
        assert a.persona == "architect"

    def test_parse_model_only(self):
        a = AgentSpec.parse("haiku")
        assert a.model == "haiku"
        assert a.persona == "architect"

    def test_parse_with_whitespace(self):
        a = AgentSpec.parse("  sonnet : security  ")
        assert a.model == "sonnet"
        assert a.persona == "security"

    def test_id_property(self):
        a = AgentSpec("opus", "architect")
        assert a.id == "opus-architect"

    def test_parse_various_formats(self):
        cases = [
            ("opus:architect", "opus", "architect"),
            ("haiku:qa", "haiku", "qa"),
            ("sonnet", "sonnet", "architect"),
            ("claude-3-opus:security", "claude-3-opus", "security"),
        ]
        for spec, expected_model, expected_persona in cases:
            result = AgentSpec.parse(spec)
            assert result.model == expected_model
            assert result.persona == expected_persona


class TestRoadmapConfig:
    def test_inherits_pipeline_config(self):
        assert issubclass(RoadmapConfig, PipelineConfig)

    def test_default_agents(self):
        config = RoadmapConfig()
        assert len(config.agents) == 2
        assert config.agents[0].model == "opus"
        assert config.agents[0].persona == "architect"
        assert config.agents[1].model == "haiku"
        assert config.agents[1].persona == "architect"

    def test_default_depth(self):
        config = RoadmapConfig()
        assert config.depth == "standard"

    def test_custom_agents(self):
        agents = [AgentSpec("sonnet", "security"), AgentSpec("haiku", "qa")]
        config = RoadmapConfig(agents=agents)
        assert config.agents[0].model == "sonnet"
        assert config.agents[1].persona == "qa"

    def test_has_pipeline_fields(self):
        config = RoadmapConfig(
            work_dir=Path("/tmp"),
            dry_run=True,
            max_turns=100,
            model="opus",
            debug=True,
        )
        assert config.work_dir == Path("/tmp")
        assert config.dry_run is True
        assert config.max_turns == 100
        assert config.model == "opus"
        assert config.debug is True

    def test_roadmap_specific_fields(self):
        config = RoadmapConfig(
            spec_file=Path("/tmp/spec.md"),
            output_dir=Path("/tmp/output"),
            depth="deep",
        )
        assert config.spec_file == Path("/tmp/spec.md")
        assert config.output_dir == Path("/tmp/output")
        assert config.depth == "deep"


# ═══════════════════════════════════════════════════════════════
# T06.02 -- Finding.deviation_class tests (v2.26)
# ═══════════════════════════════════════════════════════════════


def _make_finding(deviation_class: str = "UNCLASSIFIED") -> Finding:
    return Finding(
        id="F-01",
        severity="BLOCKING",
        dimension="Test",
        description="Test finding",
        location="file.py:1",
        evidence="test evidence",
        fix_guidance="fix it",
        deviation_class=deviation_class,
    )


class TestFindingDeviationClass:
    """T06.02: Finding.deviation_class field -- default, valid classes, invalid class, backward compat."""

    def test_default_is_unclassified(self):
        """Finding() without deviation_class defaults to 'UNCLASSIFIED'."""
        f = Finding(
            id="F-01",
            severity="BLOCKING",
            dimension="Test",
            description="desc",
            location="loc",
            evidence="ev",
            fix_guidance="fix",
        )
        assert f.deviation_class == "UNCLASSIFIED"

    def test_slip_class_accepted(self):
        f = _make_finding("SLIP")
        assert f.deviation_class == "SLIP"

    def test_intentional_class_accepted(self):
        f = _make_finding("INTENTIONAL")
        assert f.deviation_class == "INTENTIONAL"

    def test_ambiguous_class_accepted(self):
        f = _make_finding("AMBIGUOUS")
        assert f.deviation_class == "AMBIGUOUS"

    def test_pre_approved_class_accepted(self):
        f = _make_finding("PRE_APPROVED")
        assert f.deviation_class == "PRE_APPROVED"

    def test_unclassified_explicit(self):
        f = _make_finding("UNCLASSIFIED")
        assert f.deviation_class == "UNCLASSIFIED"

    def test_all_five_valid_classes(self):
        """All 5 VALID_DEVIATION_CLASSES construct successfully."""
        for cls in VALID_DEVIATION_CLASSES:
            f = _make_finding(cls)
            assert f.deviation_class == cls

    def test_invalid_class_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid deviation_class"):
            _make_finding("WRONG")

    def test_invalid_class_lowercase_raises_value_error(self):
        with pytest.raises(ValueError):
            _make_finding("slip")

    def test_backward_compatibility_no_deviation_class(self):
        """Existing Finding constructors without deviation_class continue to work."""
        f = Finding(
            id="F-01",
            severity="BLOCKING",
            dimension="Test",
            description="Backward compat test",
            location="module.py:10",
            evidence="test evidence",
            fix_guidance="apply fix",
            files_affected=["module.py"],
            status="PENDING",
            agreement_category="",
        )
        assert f.deviation_class == "UNCLASSIFIED"

    def test_backward_compatibility_with_files_affected(self):
        """Finding with files_affected list still works without deviation_class."""
        f = Finding(
            id="F-02",
            severity="WARNING",
            dimension="Style",
            description="Style issue",
            location="a.py:5",
            evidence="evidence",
            fix_guidance="reformat",
            files_affected=["a.py", "b.py"],
        )
        assert f.deviation_class == "UNCLASSIFIED"
        assert f.status == "PENDING"

    def test_valid_deviation_classes_set_completeness(self):
        """VALID_DEVIATION_CLASSES contains exactly the 5 expected classes."""
        assert VALID_DEVIATION_CLASSES == frozenset(
            {"SLIP", "INTENTIONAL", "AMBIGUOUS", "PRE_APPROVED", "UNCLASSIFIED"}
        )


# ═══════════════════════════════════════════════════════════════
# BF-1: ACTIVE status support in Finding
# ═══════════════════════════════════════════════════════════════

from superclaude.cli.roadmap.models import VALID_FINDING_STATUSES


def test_active_status_in_valid_set():
    """ACTIVE is a recognized status."""
    assert "ACTIVE" in VALID_FINDING_STATUSES


def test_finding_with_active_status():
    """Finding can be created with status='ACTIVE'."""
    f = Finding(
        id="test-001",
        severity="HIGH",
        dimension="signatures",
        description="test finding",
        location="FR-1",
        evidence="spec says X",
        fix_guidance="add X",
        status="ACTIVE",
    )
    assert f.status == "ACTIVE"


def test_finding_with_pending_status():
    """PENDING still works (backward compat)."""
    f = Finding(
        id="test-002",
        severity="HIGH",
        dimension="signatures",
        description="test",
        location="FR-1",
        evidence="evidence",
        fix_guidance="fix",
        status="PENDING",
    )
    assert f.status == "PENDING"


def test_finding_invalid_status_raises():
    """Invalid status still raises ValueError."""
    with pytest.raises(ValueError, match="Invalid Finding status"):
        Finding(
            id="test-003",
            severity="HIGH",
            dimension="signatures",
            description="test",
            location="FR-1",
            evidence="evidence",
            fix_guidance="fix",
            status="INVALID",
        )


def test_finding_default_source_layer():
    """Default source_layer is 'structural' (BF-3)."""
    f = Finding(
        id="test-004",
        severity="HIGH",
        dimension="signatures",
        description="test",
        location="FR-1",
        evidence="evidence",
        fix_guidance="fix",
    )
    assert f.source_layer == "structural"


def test_finding_semantic_source_layer():
    """source_layer can be set to 'semantic'."""
    f = Finding(
        id="test-005",
        severity="HIGH",
        dimension="signatures",
        description="test",
        location="FR-1",
        evidence="evidence",
        fix_guidance="fix",
        source_layer="semantic",
    )
    assert f.source_layer == "semantic"
