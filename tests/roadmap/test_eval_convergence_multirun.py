"""P1 Eval: Convergence Multi-Run Regression Detection.

Tests the 3-run sequence pattern: baseline → improvement → regression.
Verifies registry persistence, stable IDs, split structural/semantic counts,
and correct regression detection across runs.

This eval fills the gap: existing tests cover registry CRUD and split tracking
in isolation, but no test exercises the multi-run regression sequence with
registry persistence.
"""

from __future__ import annotations

import json

import pytest

from superclaude.cli.roadmap.convergence import (
    DeviationRegistry,
    _check_regression,
    compute_stable_id,
)
from superclaude.cli.roadmap.models import Finding


def _make_finding(
    dimension: str = "completeness",
    rule_id: str = "R-001",
    location: str = "spec:3.1",
    severity: str = "HIGH",
    source_layer: str = "structural",
) -> Finding:
    """Create a Finding with a unique dimension/location to produce unique stable IDs.

    Note: merge_findings() computes stable_id from (dimension, rule_id, location, rule_id)
    via getattr(f, 'rule_id', ''). Since Finding lacks rule_id, we vary dimension and
    location to get unique IDs.
    """
    # Vary dimension and location by rule_id to ensure unique stable IDs
    unique_dim = f"{dimension}-{rule_id}"
    unique_loc = f"{location}-{rule_id}"
    return Finding(
        id=compute_stable_id(unique_dim, rule_id, unique_loc, rule_id)[:8],
        severity=severity,
        dimension=unique_dim,
        description=f"Test finding {rule_id}",
        location=unique_loc,
        evidence="Test evidence",
        fix_guidance="Fix it",
        source_layer=source_layer,
    )


class TestMultiRunRegressionSequence:
    """3-run sequence: baseline → improvement → regression."""

    def test_run1_baseline(self, tmp_path):
        """Run 1: Establish baseline with 2 structural HIGHs."""
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test",
            spec_hash="hash1",
        )

        f1 = _make_finding(rule_id="R-001", severity="HIGH", source_layer="structural")
        f2 = _make_finding(rule_id="R-002", severity="HIGH", source_layer="structural")

        run_num = reg.begin_run("roadmap_hash_1")
        reg.merge_findings(structural=[f1, f2], semantic=[], run_number=run_num)
        reg.save()

        assert reg.get_structural_high_count() == 2
        assert reg.get_semantic_high_count() == 0
        assert reg.get_active_high_count() == 2
        assert not _check_regression(reg)  # First run, no regression possible

    def test_run2_improvement_no_regression(self, tmp_path):
        """Run 2: Fix one structural HIGH, add semantic HIGH → no regression."""
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test",
            spec_hash="hash1",
        )

        # Run 1: 2 structural HIGHs
        f1 = _make_finding(rule_id="R-001", severity="HIGH", source_layer="structural")
        f2 = _make_finding(rule_id="R-002", severity="HIGH", source_layer="structural")
        run1 = reg.begin_run("roadmap_hash_1")
        reg.merge_findings(structural=[f1, f2], semantic=[], run_number=run1)

        # Run 2: R-002 fixed (absent), new semantic HIGH
        f3 = _make_finding(rule_id="R-003", severity="HIGH", source_layer="semantic")
        run2 = reg.begin_run("roadmap_hash_2")
        reg.merge_findings(structural=[f1], semantic=[f3], run_number=run2)

        assert reg.get_structural_high_count() == 1  # Decreased
        assert reg.get_semantic_high_count() == 1  # New but not a regression
        assert not _check_regression(reg)  # Structural decreased, semantic doesn't count

    def test_run3_structural_regression(self, tmp_path):
        """Run 3: Structural HIGH increases → regression detected."""
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test",
            spec_hash="hash1",
        )

        # Run 1
        f1 = _make_finding(rule_id="R-001")
        run1 = reg.begin_run("roadmap_hash_1")
        reg.merge_findings(structural=[f1], semantic=[], run_number=run1)

        # Run 2: improvement (f1 fixed)
        run2 = reg.begin_run("roadmap_hash_2")
        reg.merge_findings(structural=[], semantic=[], run_number=run2)

        assert not _check_regression(reg)

        # Run 3: f1 reappears + new f4 → structural increase
        f4 = _make_finding(rule_id="R-004")
        run3 = reg.begin_run("roadmap_hash_3")
        reg.merge_findings(structural=[f1, f4], semantic=[], run_number=run3)

        assert reg.get_structural_high_count() == 2
        assert _check_regression(reg)  # Structural increased from 0 to 2

    def test_semantic_increase_not_regression(self, tmp_path):
        """Semantic HIGH increase does NOT trigger regression."""
        reg = DeviationRegistry(
            path=tmp_path / "registry.json",
            release_id="test",
            spec_hash="hash1",
        )

        # Run 1: 1 semantic HIGH
        f1 = _make_finding(rule_id="R-001", source_layer="semantic")
        run1 = reg.begin_run("rh1")
        reg.merge_findings(structural=[], semantic=[f1], run_number=run1)

        # Run 2: 3 semantic HIGHs (increase)
        f2 = _make_finding(rule_id="R-002", source_layer="semantic")
        f3 = _make_finding(rule_id="R-003", source_layer="semantic")
        run2 = reg.begin_run("rh2")
        reg.merge_findings(structural=[], semantic=[f1, f2, f3], run_number=run2)

        assert reg.get_semantic_high_count() == 3
        assert not _check_regression(reg)  # Semantic doesn't trigger regression


class TestRegistryPersistence:
    """Registry survives save/reload cycles."""

    def test_save_reload_preserves_findings(self, tmp_path):
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="hash1")
        f1 = _make_finding(rule_id="R-001")
        run1 = reg.begin_run("rh1")
        reg.merge_findings(structural=[f1], semantic=[], run_number=run1)
        reg.save()

        # Reload
        reg2 = DeviationRegistry.load_or_create(path, "test", "hash1")
        assert reg2.get_active_high_count() == 1
        assert len(reg2.runs) == 1
        assert len(reg2.findings) == 1

    def test_spec_hash_change_resets(self, tmp_path):
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="hash1")
        f1 = _make_finding(rule_id="R-001")
        run1 = reg.begin_run("rh1")
        reg.merge_findings(structural=[f1], semantic=[], run_number=run1)
        reg.save()

        # Reload with different spec hash
        reg2 = DeviationRegistry.load_or_create(path, "test", "hash2")
        assert len(reg2.findings) == 0
        assert len(reg2.runs) == 0

    def test_corrupted_registry_creates_fresh(self, tmp_path):
        path = tmp_path / "registry.json"
        path.write_text("{invalid json")

        reg = DeviationRegistry.load_or_create(path, "test", "hash1")
        assert len(reg.findings) == 0
        assert len(reg.runs) == 0


class TestStableIDDeterminism:
    """Stable IDs are deterministic and consistent."""

    def test_same_inputs_same_id(self):
        id1 = compute_stable_id("completeness", "R-001", "spec:3.1", "R-001")
        id2 = compute_stable_id("completeness", "R-001", "spec:3.1", "R-001")
        assert id1 == id2

    def test_different_inputs_different_id(self):
        id1 = compute_stable_id("completeness", "R-001", "spec:3.1", "R-001")
        id2 = compute_stable_id("completeness", "R-002", "spec:3.1", "R-002")
        assert id1 != id2

    def test_id_length(self):
        sid = compute_stable_id("dim", "rule", "loc", "type")
        assert len(sid) == 16

    def test_id_is_hex(self):
        sid = compute_stable_id("dim", "rule", "loc", "type")
        int(sid, 16)  # Should not raise


class TestFindingStatusMutations:
    """Registry correctly tracks status transitions."""

    def test_active_to_fixed_when_absent(self, tmp_path):
        """Missing finding in subsequent run → marked FIXED."""
        reg = DeviationRegistry(path=tmp_path / "r.json", release_id="t", spec_hash="h")
        f1 = _make_finding(rule_id="R-001")
        run1 = reg.begin_run("rh1")
        reg.merge_findings(structural=[f1], semantic=[], run_number=run1)

        # Run 2: f1 absent
        run2 = reg.begin_run("rh2")
        reg.merge_findings(structural=[], semantic=[], run_number=run2)

        fixed = [f for f in reg.findings.values() if f["status"] == "FIXED"]
        assert len(fixed) == 1

    def test_debate_verdict_downgrades_severity(self, tmp_path):
        reg = DeviationRegistry(path=tmp_path / "r.json", release_id="t", spec_hash="h")
        f1 = _make_finding(rule_id="R-001", severity="HIGH")
        run1 = reg.begin_run("rh1")
        reg.merge_findings(structural=[f1], semantic=[], run_number=run1)

        # Find the stable_id
        sid = list(reg.findings.keys())[0]
        assert reg.findings[sid]["severity"] == "HIGH"

        # Record debate verdict to downgrade
        reg.record_debate_verdict(sid, "DOWNGRADE_TO_MEDIUM", "debate.md")
        assert reg.findings[sid]["severity"] == "MEDIUM"
        assert reg.findings[sid]["debate_verdict"] == "DOWNGRADE_TO_MEDIUM"
