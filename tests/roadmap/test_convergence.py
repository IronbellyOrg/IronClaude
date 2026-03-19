"""Tests for BF-2, BF-3, BF-4: Convergence engine."""
import json
import pytest
from pathlib import Path

from superclaude.cli.roadmap.convergence import (
    DeviationRegistry,
    ConvergenceResult,
    compute_stable_id,
    _check_regression,
    _create_validation_dirs,
    _cleanup_validation_dirs,
)
from superclaude.cli.roadmap.models import Finding


# --- BF-2: Dual authority elimination ---


class TestDualAuthorityElimination:
    """BF-2: Registry vs SPEC_FIDELITY_GATE conflict resolution."""

    def test_convergence_mode_no_gate_reference(self):
        """convergence.py has zero references to SPEC_FIDELITY_GATE."""
        import superclaude.cli.roadmap.convergence as mod

        source = Path(mod.__file__).read_text()
        assert "SPEC_FIDELITY_GATE" not in source

    def test_registry_pass_with_zero_active_highs(self, tmp_path):
        """Registry with 0 active HIGHs reports passing."""
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test",
            spec_hash="abc123",
        )
        assert reg.get_active_high_count() == 0

    def test_registry_fail_with_active_highs(self, tmp_path):
        """Registry with active HIGHs reports non-zero."""
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test",
            spec_hash="abc123",
        )
        finding = Finding(
            id="F-001",
            severity="HIGH",
            dimension="signatures",
            description="test",
            location="FR-1",
            evidence="ev",
            fix_guidance="fix",
            status="ACTIVE",
            source_layer="structural",
        )
        reg.begin_run("road1")
        reg.merge_findings([finding], [], run_number=1)
        assert reg.get_active_high_count() == 1


# --- BF-3: Split tracking and regression ---


class TestSplitTracking:
    """BF-3: Structural vs semantic HIGH tracking."""

    def _make_finding(self, id_str, severity="HIGH", source_layer="structural",
                       dimension="signatures", location=None):
        # Use id_str in location to ensure unique stable IDs
        if location is None:
            location = f"FR-{id_str}"
        return Finding(
            id=id_str,
            severity=severity,
            dimension=dimension,
            description="test",
            location=location,
            evidence="ev",
            fix_guidance="fix",
            status="ACTIVE",
            source_layer=source_layer,
        )

    def test_structural_regression_triggers(self, tmp_path):
        """Structural HIGH increase triggers regression."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        # Run 1: 1 structural HIGH
        reg.begin_run("road1")
        reg.merge_findings([self._make_finding("F-001")], [], run_number=1)

        # Run 2: 2 structural HIGHs
        reg.begin_run("road2")
        reg.merge_findings(
            [self._make_finding("F-001"), self._make_finding("F-002")],
            [],
            run_number=2,
        )

        assert _check_regression(reg) is True

    def test_semantic_fluctuation_no_regression(self, tmp_path):
        """Semantic HIGH increase does NOT trigger regression."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        # Run 1: 0 semantic HIGHs
        reg.begin_run("road1")
        reg.merge_findings([], [], run_number=1)

        # Run 2: 2 semantic HIGHs (increase)
        reg.begin_run("road2")
        reg.merge_findings(
            [],
            [
                self._make_finding("S-001", source_layer="semantic"),
                self._make_finding("S-002", source_layer="semantic"),
            ],
            run_number=2,
        )

        assert _check_regression(reg) is False

    def test_gate_requires_zero_total_highs(self, tmp_path):
        """Gate requires 0 total HIGHs (structural + semantic)."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        # Only semantic HIGHs, no structural
        reg.begin_run("road1")
        reg.merge_findings(
            [],
            [self._make_finding("S-001", source_layer="semantic")],
            run_number=1,
        )
        # Gate should NOT pass -- semantic HIGHs still block
        assert reg.get_active_high_count() == 1

    def test_source_layer_correctly_tagged(self, tmp_path):
        """Findings get correct source_layer in registry."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        structural = [self._make_finding("F-001")]
        semantic = [self._make_finding("S-001", source_layer="semantic")]
        reg.begin_run("road1")
        reg.merge_findings(structural, semantic, run_number=1)

        assert reg.get_structural_high_count() == 1
        assert reg.get_semantic_high_count() == 1


# --- BF-4: Temp directory isolation ---


class TestTempDirIsolation:
    """BF-4: Temp directories replace git worktrees."""

    def test_creates_independent_copies(self, tmp_path):
        """Each validation dir gets independent file copies."""
        spec = tmp_path / "spec.md"
        roadmap = tmp_path / "roadmap.md"
        registry = tmp_path / "registry.json"
        spec.write_text("# Spec")
        roadmap.write_text("# Roadmap")
        registry.write_text("{}")

        dirs = _create_validation_dirs(spec, roadmap, registry, count=3)
        try:
            assert len(dirs) == 3
            for d in dirs:
                assert (d / "spec.md").exists()
                assert (d / "roadmap.md").exists()
                assert (d / "registry.json").exists()

            # Mutate file in dir 0
            (dirs[0] / "spec.md").write_text("# Modified")
            # Dirs 1 and 2 are unaffected
            assert (dirs[1] / "spec.md").read_text() == "# Spec"
            assert (dirs[2] / "spec.md").read_text() == "# Spec"
        finally:
            _cleanup_validation_dirs(dirs)

    def test_cleanup_removes_dirs(self, tmp_path):
        """Cleanup removes all temporary directories."""
        spec = tmp_path / "spec.md"
        roadmap = tmp_path / "roadmap.md"
        registry = tmp_path / "registry.json"
        spec.write_text("# Spec")
        roadmap.write_text("# Roadmap")
        registry.write_text("{}")

        dirs = _create_validation_dirs(spec, roadmap, registry, count=2)
        paths = [d for d in dirs]
        _cleanup_validation_dirs(dirs)

        for p in paths:
            assert not p.exists()


# --- Registry persistence ---


class TestRegistryPersistence:
    """FR-6: Registry load/save/reset."""

    def test_save_and_reload(self, tmp_path):
        """Registry persists across save/load cycles."""
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        reg.save()

        loaded = DeviationRegistry.load_or_create(path, "test", "abc")
        assert len(loaded.runs) == 1

    def test_spec_hash_change_resets(self, tmp_path):
        """Spec hash change resets registry (FR-6)."""
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        reg.save()

        loaded = DeviationRegistry.load_or_create(path, "test", "NEW_HASH")
        assert len(loaded.runs) == 0

    def test_stable_id_determinism(self):
        """Same inputs produce same stable ID."""
        id1 = compute_stable_id("sig", "phantom_id", "FR-1", "phantom_id")
        id2 = compute_stable_id("sig", "phantom_id", "FR-1", "phantom_id")
        assert id1 == id2
        assert len(id1) == 16
