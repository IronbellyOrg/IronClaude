"""Tests for BF-5: --allow-regeneration flag."""
import pytest
from superclaude.cli.roadmap.models import RoadmapConfig


class TestAllowRegeneration:
    """BF-5: --allow-regeneration flag support."""

    def test_default_is_false(self):
        """allow_regeneration defaults to False."""
        assert hasattr(RoadmapConfig, "__dataclass_fields__")
        field = RoadmapConfig.__dataclass_fields__["allow_regeneration"]
        assert field.default is False

    def test_convergence_enabled_default_true(self):
        """convergence_enabled defaults to True (v3.05 convergence engine is default ON)."""
        field = RoadmapConfig.__dataclass_fields__["convergence_enabled"]
        assert field.default is True
