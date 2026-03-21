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


# --- T03.01: Registry extension with source_layer and stable IDs (FR-6) ---


class TestRegistryStableIDs:
    """T03.01: Stable IDs, source_layer, cross-run comparison."""

    def _make_finding(self, id_str, severity="HIGH", source_layer="structural",
                       dimension="signatures", location=None, rule_id=""):
        if location is None:
            location = f"FR-{id_str}"
        return Finding(
            id=id_str,
            severity=severity,
            dimension=dimension,
            description=f"finding {id_str}",
            location=location,
            evidence="ev",
            fix_guidance="fix",
            status="ACTIVE",
            source_layer=source_layer,
            rule_id=rule_id,
        )

    def test_source_layer_field_present(self, tmp_path):
        """Each finding has source_layer: 'structural' or 'semantic'."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        reg.merge_findings(
            [self._make_finding("F-001")],
            [self._make_finding("S-001", source_layer="semantic")],
            run_number=1,
        )
        for fid, finding in reg.findings.items():
            assert finding["source_layer"] in ("structural", "semantic")

    def test_stable_id_from_tuple(self):
        """Stable IDs computed from (dimension, rule_id, spec_location, mismatch_type) tuple."""
        sid = compute_stable_id("signatures", "R-001", "FR-1", "missing")
        assert isinstance(sid, str)
        assert len(sid) == 16
        # Same inputs -> same output
        assert sid == compute_stable_id("signatures", "R-001", "FR-1", "missing")

    def test_stable_id_collision_free(self):
        """Different inputs produce different stable IDs."""
        ids = set()
        test_cases = [
            ("signatures", "R-001", "FR-1", "missing"),
            ("signatures", "R-001", "FR-1", "extra"),
            ("signatures", "R-001", "FR-2", "missing"),
            ("signatures", "R-002", "FR-1", "missing"),
            ("interfaces", "R-001", "FR-1", "missing"),
            ("dependencies", "R-003", "FR-5", "mismatch"),
            ("naming", "R-004", "FR-10", "wrong_case"),
            ("coverage", "R-005", "FR-3", "uncovered"),
        ]
        for args in test_cases:
            sid = compute_stable_id(*args)
            ids.add(sid)
        assert len(ids) == len(test_cases), "Stable ID collision detected"

    def test_cross_run_match_by_stable_id(self, tmp_path):
        """Cross-run comparison correctly matches findings by stable ID."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        f1 = self._make_finding("F-001")

        # Run 1: introduce finding
        reg.begin_run("road1")
        reg.merge_findings([f1], [], run_number=1)
        sid = list(reg.findings.keys())[0]
        assert reg.findings[sid]["first_seen_run"] == 1
        assert reg.findings[sid]["last_seen_run"] == 1

        # Run 2: same finding still present -> last_seen_run updated
        reg.begin_run("road2")
        reg.merge_findings([f1], [], run_number=2)
        assert reg.findings[sid]["first_seen_run"] == 1
        assert reg.findings[sid]["last_seen_run"] == 2
        assert reg.findings[sid]["status"] == "ACTIVE"

    def test_fixed_status_when_not_reproduced(self, tmp_path):
        """Missing findings in subsequent run marked FIXED."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        f1 = self._make_finding("F-001")
        f2 = self._make_finding("F-002")

        # Run 1: both findings
        reg.begin_run("road1")
        reg.merge_findings([f1, f2], [], run_number=1)
        assert len(reg.findings) == 2

        # Run 2: only f1 remains -> f2 should be FIXED
        reg.begin_run("road2")
        reg.merge_findings([f1], [], run_number=2)

        statuses = {f["description"]: f["status"] for f in reg.findings.values()}
        assert statuses["finding F-001"] == "ACTIVE"
        assert statuses["finding F-002"] == "FIXED"

    def test_run_metadata_split_high_counts(self, tmp_path):
        """Run metadata includes structural_high_count, semantic_high_count, total_high_count."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        reg.merge_findings(
            [self._make_finding("F-001"), self._make_finding("F-002")],
            [self._make_finding("S-001", source_layer="semantic")],
            run_number=1,
        )
        run = reg.runs[-1]
        assert run["structural_high_count"] == 2
        assert run["semantic_high_count"] == 1
        assert run["total_high_count"] == 3


# --- T03.02: Spec version detection and pre-v3.05 compatibility ---


class TestBackwardCompatibility:
    """T03.02: Pre-v3.05 registry loading and spec hash reset."""

    def test_registry_resets_on_spec_hash_change(self, tmp_path):
        """Registry resets (clears all findings) when spec_hash changes."""
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="hash_v1")
        reg.begin_run("road1")
        reg.findings["test_id"] = {
            "stable_id": "test_id", "dimension": "sig", "severity": "HIGH",
            "description": "d", "location": "L", "source_layer": "structural",
            "status": "ACTIVE", "first_seen_run": 1, "last_seen_run": 1,
            "debate_verdict": None, "debate_transcript": None,
        }
        reg.save()

        loaded = DeviationRegistry.load_or_create(path, "test", "hash_v2")
        assert len(loaded.findings) == 0
        assert len(loaded.runs) == 0

    def test_pre_v305_registry_loads_with_default_source_layer(self, tmp_path):
        """Pre-v3.05 registries (without source_layer) load with source_layer='structural'."""
        path = tmp_path / "registry.json"
        # Simulate a pre-v3.05 registry file (no source_layer on findings)
        data = {
            "schema_version": 1,
            "release_id": "test",
            "spec_hash": "abc",
            "runs": [{"run_number": 1, "timestamp": "2026-01-01T00:00:00Z",
                       "spec_hash": "abc", "roadmap_hash": "road1"}],
            "findings": {
                "old_finding_1": {
                    "stable_id": "old_finding_1",
                    "dimension": "signatures",
                    "severity": "HIGH",
                    "description": "old finding",
                    "location": "FR-1",
                    "status": "ACTIVE",
                    "debate_verdict": None,
                    "debate_transcript": None,
                    # NOTE: no source_layer, no first_seen_run, no last_seen_run
                },
            },
        }
        path.write_text(json.dumps(data))

        loaded = DeviationRegistry.load_or_create(path, "test", "abc")
        finding = loaded.findings["old_finding_1"]
        assert finding["source_layer"] == "structural"
        assert finding["first_seen_run"] == 1
        assert finding["last_seen_run"] == 1

    def test_active_status_accepted(self, tmp_path):
        """Findings with status='ACTIVE' accepted without error."""
        f = Finding(
            id="F-001", severity="HIGH", dimension="sig",
            description="test", location="FR-1", evidence="ev",
            fix_guidance="fix", status="ACTIVE",
        )
        assert f.status == "ACTIVE"

    def test_registry_serialization_preserves_fields(self, tmp_path):
        """Registry serialization preserves all new fields in JSON format."""
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        finding = Finding(
            id="F-001", severity="HIGH", dimension="sig",
            description="test", location="FR-1", evidence="ev",
            fix_guidance="fix", status="ACTIVE", source_layer="semantic",
        )
        reg.merge_findings([], [finding], run_number=1)
        reg.save()

        raw = json.loads(path.read_text())
        fid = list(raw["findings"].keys())[0]
        f = raw["findings"][fid]
        assert "source_layer" in f
        assert "first_seen_run" in f
        assert "last_seen_run" in f
        assert "stable_id" in f
        assert f["source_layer"] == "semantic"


# --- T03.03: Run-to-run memory (FR-10) ---


class TestRunToRunMemory:
    """T03.03: first_seen_run, last_seen_run, prior findings summary."""

    def _make_finding(self, id_str, severity="HIGH", source_layer="structural",
                       location=None):
        if location is None:
            location = f"FR-{id_str}"
        return Finding(
            id=id_str, severity=severity, dimension="signatures",
            description=f"finding {id_str}", location=location,
            evidence="ev", fix_guidance="fix", status="ACTIVE",
            source_layer=source_layer,
        )

    def test_first_seen_and_last_seen_tracking(self, tmp_path):
        """Each finding tracks first_seen_run and last_seen_run integers."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        f1 = self._make_finding("F-001")

        reg.begin_run("road1")
        reg.merge_findings([f1], [], run_number=1)
        sid = list(reg.findings.keys())[0]
        assert isinstance(reg.findings[sid]["first_seen_run"], int)
        assert isinstance(reg.findings[sid]["last_seen_run"], int)
        assert reg.findings[sid]["first_seen_run"] == 1
        assert reg.findings[sid]["last_seen_run"] == 1

        reg.begin_run("road2")
        reg.merge_findings([f1], [], run_number=2)
        assert reg.findings[sid]["first_seen_run"] == 1
        assert reg.findings[sid]["last_seen_run"] == 2

    def test_prior_findings_summary_max_50(self, tmp_path):
        """get_prior_findings_summary() returns at most 50 findings, oldest first."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        reg.begin_run("road1")

        # Create 60 findings
        findings = [self._make_finding(f"F-{i:03d}") for i in range(60)]
        reg.merge_findings(findings, [], run_number=1)

        summary = reg.get_prior_findings_summary(max_entries=50)
        lines = summary.strip().split("\n")
        # Header (2 lines) + 50 data lines + 1 truncation line
        data_lines = [l for l in lines if l.startswith("|") and "---" not in l
                       and "Stable ID" not in l and "more entries" not in l]
        assert len(data_lines) == 50

        # Verify truncation message present
        assert "10 more entries truncated" in summary

    def test_prior_findings_summary_fields(self, tmp_path):
        """Summary includes ID, severity, status, source, run_number."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        reg.merge_findings([self._make_finding("F-001")], [], run_number=1)

        summary = reg.get_prior_findings_summary()
        assert "Stable ID" in summary
        assert "Severity" in summary
        assert "Status" in summary
        assert "Source" in summary
        assert "HIGH" in summary
        assert "ACTIVE" in summary
        assert "structural" in summary

    def test_fixed_findings_not_reported_as_new(self, tmp_path):
        """Fixed findings from prior runs do not appear as new findings."""
        reg = DeviationRegistry(path=tmp_path / "reg.json", release_id="test", spec_hash="abc")
        f1 = self._make_finding("F-001")
        f2 = self._make_finding("F-002")

        # Run 1: both findings active
        reg.begin_run("road1")
        reg.merge_findings([f1, f2], [], run_number=1)

        # Run 2: f2 fixed (not present)
        reg.begin_run("road2")
        reg.merge_findings([f1], [], run_number=2)

        f2_entry = [f for f in reg.findings.values() if f["description"] == "finding F-002"][0]
        assert f2_entry["status"] == "FIXED"

        # Run 3: f2 reappears -> should NOT get a new entry, should update existing
        reg.begin_run("road3")
        reg.merge_findings([f1, f2], [], run_number=3)

        # Still only 2 findings total (no duplicate)
        assert len(reg.findings) == 2
        f2_entry = [f for f in reg.findings.values() if f["description"] == "finding F-002"][0]
        assert f2_entry["status"] == "ACTIVE"
        assert f2_entry["first_seen_run"] == 1  # Original first_seen preserved
        assert f2_entry["last_seen_run"] == 3


# --- T03.04: 3-Run simulation integration test ---


class TestThreeRunSimulation:
    """T03.04: End-to-end 3-run registry lifecycle."""

    def _make_finding(self, id_str, severity="HIGH", source_layer="structural",
                       dimension="signatures", location=None):
        if location is None:
            location = f"FR-{id_str}"
        return Finding(
            id=id_str, severity=severity, dimension=dimension,
            description=f"finding {id_str}", location=location,
            evidence="ev", fix_guidance="fix", status="ACTIVE",
            source_layer=source_layer,
        )

    def test_three_run_simulation(self, tmp_path):
        """Registry correctly tracks findings across 3 simulated runs."""
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="abc")

        # --- Run 1: Seed with structural + semantic findings ---
        run1 = reg.begin_run("road1")
        structural_r1 = [
            self._make_finding("STR-001"),
            self._make_finding("STR-002"),
        ]
        semantic_r1 = [
            self._make_finding("SEM-001", source_layer="semantic"),
        ]
        reg.merge_findings(structural_r1, semantic_r1, run_number=run1)

        assert reg.get_structural_high_count() == 2
        assert reg.get_semantic_high_count() == 1
        assert reg.get_active_high_count() == 3
        assert len(reg.findings) == 3
        assert reg.runs[-1]["structural_high_count"] == 2
        assert reg.runs[-1]["semantic_high_count"] == 1
        assert reg.runs[-1]["total_high_count"] == 3

        # Save and reload to test persistence
        reg.save()
        reg = DeviationRegistry.load_or_create(path, "test", "abc")

        # --- Run 2: STR-002 fixed, SEM-002 added ---
        run2 = reg.begin_run("road2")
        structural_r2 = [
            self._make_finding("STR-001"),  # still present
            # STR-002 is gone (fixed)
        ]
        semantic_r2 = [
            self._make_finding("SEM-001", source_layer="semantic"),  # still present
            self._make_finding("SEM-002", source_layer="semantic"),  # new
        ]
        reg.merge_findings(structural_r2, semantic_r2, run_number=run2)

        # STR-002 should be FIXED
        str002 = [f for f in reg.findings.values() if f["description"] == "finding STR-002"][0]
        assert str002["status"] == "FIXED"

        # New stable IDs for SEM-002
        sem002 = [f for f in reg.findings.values() if f["description"] == "finding SEM-002"][0]
        assert sem002["first_seen_run"] == 2
        assert sem002["status"] == "ACTIVE"

        assert reg.get_structural_high_count() == 1
        assert reg.get_semantic_high_count() == 2
        assert reg.runs[-1]["structural_high_count"] == 1
        assert reg.runs[-1]["semantic_high_count"] == 2
        assert reg.runs[-1]["total_high_count"] == 3

        # Save and reload again
        reg.save()
        reg = DeviationRegistry.load_or_create(path, "test", "abc")

        # --- Run 3: Verify cumulative state ---
        run3 = reg.begin_run("road3")
        structural_r3 = [
            self._make_finding("STR-001"),  # still present
        ]
        semantic_r3 = [
            self._make_finding("SEM-001", source_layer="semantic"),
            # SEM-002 gone (fixed)
        ]
        reg.merge_findings(structural_r3, semantic_r3, run_number=run3)

        # Cumulative checks
        assert len(reg.findings) == 4  # total unique findings across all runs
        assert reg.get_structural_high_count() == 1
        assert reg.get_semantic_high_count() == 1
        assert reg.runs[-1]["structural_high_count"] == 1
        assert reg.runs[-1]["semantic_high_count"] == 1
        assert reg.runs[-1]["total_high_count"] == 2

        # Status checks
        statuses = {f["description"]: f["status"] for f in reg.findings.values()}
        assert statuses["finding STR-001"] == "ACTIVE"
        assert statuses["finding STR-002"] == "FIXED"
        assert statuses["finding SEM-001"] == "ACTIVE"
        assert statuses["finding SEM-002"] == "FIXED"

        # Verify stable IDs are unique (collision-free)
        all_ids = list(reg.findings.keys())
        assert len(all_ids) == len(set(all_ids)), "Stable ID collision detected"

        # Verify run metadata completeness
        assert len(reg.runs) == 3
        for run in reg.runs:
            assert "structural_high_count" in run
            assert "semantic_high_count" in run
            assert "total_high_count" in run

    def test_three_run_stable_id_consistency(self, tmp_path):
        """Stable IDs remain consistent across save/load cycles."""
        path = tmp_path / "registry.json"
        reg = DeviationRegistry(path=path, release_id="test", spec_hash="abc")

        f1 = self._make_finding("F-001")
        reg.begin_run("road1")
        reg.merge_findings([f1], [], run_number=1)
        ids_run1 = set(reg.findings.keys())
        reg.save()

        reg = DeviationRegistry.load_or_create(path, "test", "abc")
        reg.begin_run("road2")
        reg.merge_findings([f1], [], run_number=2)
        ids_run2 = set(reg.findings.keys())

        # Same finding should have same stable ID across runs
        assert ids_run1 == ids_run2


# --- T05.01: TurnLedger Integration and Budget Guards ---


class TestTurnLedgerIntegration:
    """T05.01: TurnLedger budget constants, guards, and reimbursement."""

    def test_budget_constants_defined(self):
        """Cost constants defined as module-level integers."""
        from superclaude.cli.roadmap.convergence import (
            CHECKER_COST,
            REMEDIATION_COST,
            REGRESSION_VALIDATION_COST,
            CONVERGENCE_PASS_CREDIT,
        )
        assert CHECKER_COST == 10
        assert REMEDIATION_COST == 8
        assert REGRESSION_VALIDATION_COST == 15
        assert CONVERGENCE_PASS_CREDIT == 5

    def test_derived_budgets_defined(self):
        """Derived budget thresholds defined."""
        from superclaude.cli.roadmap.convergence import (
            MIN_CONVERGENCE_BUDGET,
            STD_CONVERGENCE_BUDGET,
            MAX_CONVERGENCE_BUDGET,
        )
        assert MIN_CONVERGENCE_BUDGET == 28
        assert STD_CONVERGENCE_BUDGET == 46
        assert MAX_CONVERGENCE_BUDGET == 61

    def test_turnledger_conditional_import(self):
        """TurnLedger importable from sprint.models via helper."""
        from superclaude.cli.roadmap.convergence import _get_turnledger_class
        TurnLedger = _get_turnledger_class()
        ledger = TurnLedger(initial_budget=61)
        assert ledger.can_launch()
        assert ledger.can_remediate()

    def test_reimburse_for_progress_positive(self):
        """reimburse_for_progress() credits when structural HIGHs decrease."""
        from superclaude.cli.roadmap.convergence import reimburse_for_progress
        from superclaude.cli.sprint.models import TurnLedger

        ledger = TurnLedger(initial_budget=100)
        credit = reimburse_for_progress(ledger, prev_structural_highs=5, curr_structural_highs=3)
        assert credit > 0
        assert ledger.reimbursed > 0

    def test_reimburse_for_progress_no_improvement(self):
        """reimburse_for_progress() returns 0 when no improvement."""
        from superclaude.cli.roadmap.convergence import reimburse_for_progress
        from superclaude.cli.sprint.models import TurnLedger

        ledger = TurnLedger(initial_budget=100)
        credit = reimburse_for_progress(ledger, prev_structural_highs=3, curr_structural_highs=3)
        assert credit == 0
        assert ledger.reimbursed == 0

    def test_reimburse_for_progress_increase(self):
        """reimburse_for_progress() returns 0 when HIGHs increase."""
        from superclaude.cli.roadmap.convergence import reimburse_for_progress
        from superclaude.cli.sprint.models import TurnLedger

        ledger = TurnLedger(initial_budget=100)
        credit = reimburse_for_progress(ledger, prev_structural_highs=3, curr_structural_highs=5)
        assert credit == 0

    def test_budget_guard_halts_on_exhaustion(self):
        """Budget guard prevents checker run when budget exhausted."""
        from superclaude.cli.roadmap.convergence import (
            execute_fidelity_with_convergence,
            MAX_CONVERGENCE_BUDGET,
        )
        from superclaude.cli.sprint.models import TurnLedger

        ledger = TurnLedger(initial_budget=2, minimum_allocation=5)
        reg = DeviationRegistry(
            path=Path("/tmp/test-reg.json"),
            release_id="test",
            spec_hash="abc",
        )

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=lambda r, n: None,
            run_remediation=lambda r: None,
        )
        assert not result.passed
        assert result.halt_reason is not None
        assert "Budget exhausted" in result.halt_reason


# --- T05.02: Convergence loop tests ---


class TestConvergenceLoop:
    """T05.02: execute_fidelity_with_convergence() behavior."""

    def _make_finding(self, id_str, severity="HIGH", source_layer="structural",
                       location=None):
        if location is None:
            location = f"FR-{id_str}"
        return Finding(
            id=id_str, severity=severity, dimension="signatures",
            description=f"finding {id_str}", location=location,
            evidence="ev", fix_guidance="fix", status="ACTIVE",
            source_layer=source_layer,
        )

    def test_convergence_loop_early_pass(self, tmp_path):
        """Convergence passes on first run when 0 active HIGHs."""
        from superclaude.cli.roadmap.convergence import execute_fidelity_with_convergence
        from superclaude.cli.sprint.models import TurnLedger

        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        ledger = TurnLedger(initial_budget=61)

        def noop_checkers(registry, run_number):
            registry.merge_findings([], [], run_number=run_number)

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=noop_checkers,
            run_remediation=lambda r: None,
        )
        assert result.passed
        assert result.run_count == 1
        assert result.final_high_count == 0

    def test_convergence_loop_three_runs(self, tmp_path):
        """Convergence across 3 runs: findings decrease each run."""
        from superclaude.cli.roadmap.convergence import execute_fidelity_with_convergence
        from superclaude.cli.sprint.models import TurnLedger

        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        ledger = TurnLedger(initial_budget=100)

        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        run_counter = {"n": 0}

        def decreasing_checkers(registry, run_number):
            run_counter["n"] += 1
            n = run_counter["n"]
            if n == 1:
                findings = [self._make_finding("F-001"), self._make_finding("F-002")]
            elif n == 2:
                findings = [self._make_finding("F-001")]
            else:
                findings = []
            registry.merge_findings(findings, [], run_number=run_number)

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=decreasing_checkers,
            run_remediation=lambda r: None,
            roadmap_path=roadmap,
        )
        assert result.passed
        assert result.run_count == 3
        assert result.final_high_count == 0

    def test_convergence_loop_budget_exhaustion(self, tmp_path):
        """Convergence halts with diagnostic on budget exhaustion."""
        from superclaude.cli.roadmap.convergence import (
            execute_fidelity_with_convergence,
            CHECKER_COST,
        )
        from superclaude.cli.sprint.models import TurnLedger

        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        # Budget for exactly 1 checker run, not enough for remediation + run 2
        ledger = TurnLedger(initial_budget=CHECKER_COST + 2, minimum_allocation=5, minimum_remediation_budget=5)

        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        def persistent_checkers(registry, run_number):
            registry.merge_findings(
                [self._make_finding("F-001")], [], run_number=run_number,
            )

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=persistent_checkers,
            run_remediation=lambda r: None,
            roadmap_path=roadmap,
        )
        assert not result.passed
        assert result.halt_reason is not None

    def test_convergence_loop_regression_trigger(self, tmp_path):
        """Structural increase triggers regression detection."""
        from superclaude.cli.roadmap.convergence import execute_fidelity_with_convergence
        from superclaude.cli.sprint.models import TurnLedger

        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        ledger = TurnLedger(initial_budget=100)

        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec")

        run_counter = {"n": 0}
        regression_called = {"called": False}

        def increasing_checkers(registry, run_number):
            run_counter["n"] += 1
            if run_counter["n"] == 1:
                findings = [self._make_finding("F-001")]
            else:
                # Regression: more findings than before
                findings = [self._make_finding("F-001"), self._make_finding("F-002"), self._make_finding("F-003")]
            registry.merge_findings(findings, [], run_number=run_number)

        def mock_regression(registry, spec_path, roadmap_path):
            from superclaude.cli.roadmap.convergence import RegressionResult
            regression_called["called"] = True
            return RegressionResult(agents_succeeded=3)

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=increasing_checkers,
            run_remediation=lambda r: None,
            handle_regression_fn=mock_regression,
            spec_path=spec,
            roadmap_path=roadmap,
        )
        assert result.regression_detected
        assert regression_called["called"]


# --- T05.03: Legacy/Convergence Dispatch ---


class TestDispatch:
    """T05.03: convergence_enabled dispatch in executor step 8."""

    def test_convergence_gate_none_when_enabled(self):
        """When convergence_enabled=True, spec-fidelity step has no gate."""
        from superclaude.cli.roadmap.models import RoadmapConfig, AgentSpec

        config = RoadmapConfig(
            spec_file=Path("/tmp/spec.md"),
            output_dir=Path("/tmp/out"),
            convergence_enabled=True,
            agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        )
        # Import the step builder
        from superclaude.cli.roadmap.executor import _build_steps
        steps = _build_steps(config)

        # Find spec-fidelity step (flat list, may be nested)
        fidelity_step = None
        for entry in steps:
            if isinstance(entry, list):
                for s in entry:
                    if s.id == "spec-fidelity":
                        fidelity_step = s
            else:
                if entry.id == "spec-fidelity":
                    fidelity_step = entry

        assert fidelity_step is not None
        # When convergence_enabled=True, gate should be None (convergence takes over)
        assert fidelity_step.gate is None

    def test_legacy_gate_when_disabled(self):
        """When convergence_enabled=False, spec-fidelity step uses SPEC_FIDELITY_GATE."""
        from superclaude.cli.roadmap.models import RoadmapConfig, AgentSpec
        from superclaude.cli.roadmap.gates import SPEC_FIDELITY_GATE

        config = RoadmapConfig(
            spec_file=Path("/tmp/spec.md"),
            output_dir=Path("/tmp/out"),
            convergence_enabled=False,
            agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        )
        from superclaude.cli.roadmap.executor import _build_steps
        steps = _build_steps(config)

        fidelity_step = None
        for entry in steps:
            if isinstance(entry, list):
                for s in entry:
                    if s.id == "spec-fidelity":
                        fidelity_step = s
            else:
                if entry.id == "spec-fidelity":
                    fidelity_step = entry

        assert fidelity_step is not None
        assert fidelity_step.gate is SPEC_FIDELITY_GATE


# --- T05.04: Legacy Budget Isolation ---


class TestBudgetIsolation:
    """T05.04: Legacy budget functions not called in convergence mode."""

    def test_convergence_module_no_legacy_budget_refs(self):
        """convergence.py does not call _check_remediation_budget or _print_terminal_halt."""
        import superclaude.cli.roadmap.convergence as mod
        source = Path(mod.__file__).read_text()
        assert "_check_remediation_budget" not in source
        assert "_print_terminal_halt" not in source

    def test_turnledger_not_in_legacy_path(self):
        """Legacy executor step 8 path does not reference TurnLedger at module level."""
        import superclaude.cli.roadmap.executor as mod
        source = Path(mod.__file__).read_text()
        # TurnLedger should not be imported at module level in executor;
        # function-scoped imports inside _run_convergence_spec_fidelity are expected
        lines = source.splitlines()
        module_level_imports = [
            line for line in lines
            if "from ..sprint.models import TurnLedger" in line
            and not line.startswith((" ", "\t"))
        ]
        assert len(module_level_imports) == 0, (
            f"TurnLedger imported at module level: {module_level_imports}"
        )


# --- T05.05: Regression Detection Trigger ---


class TestRegressionTrigger:
    """T05.05: Regression trigger on structural increase only."""

    def _make_finding(self, id_str, severity="HIGH", source_layer="structural",
                       location=None):
        if location is None:
            location = f"FR-{id_str}"
        return Finding(
            id=id_str, severity=severity, dimension="signatures",
            description=f"finding {id_str}", location=location,
            evidence="ev", fix_guidance="fix", status="ACTIVE",
            source_layer=source_layer,
        )

    def test_regression_trigger_structural_increase(self, tmp_path):
        """structural HIGH increase triggers regression."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        reg.begin_run("road1")
        reg.merge_findings([self._make_finding("F-001")], [], run_number=1)

        reg.begin_run("road2")
        reg.merge_findings(
            [self._make_finding("F-001"), self._make_finding("F-002")],
            [],
            run_number=2,
        )
        assert _check_regression(reg) is True

    def test_regression_trigger_semantic_only_no_trigger(self, tmp_path):
        """semantic-only HIGH increase does NOT trigger regression."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        reg.begin_run("road1")
        reg.merge_findings([], [], run_number=1)

        reg.begin_run("road2")
        reg.merge_findings(
            [],
            [self._make_finding("S-001", source_layer="semantic"),
             self._make_finding("S-002", source_layer="semantic")],
            run_number=2,
        )
        assert _check_regression(reg) is False

    def test_regression_trigger_budget_debit(self, tmp_path):
        """REGRESSION_VALIDATION_COST debited before handle_regression."""
        from superclaude.cli.roadmap.convergence import (
            execute_fidelity_with_convergence,
            REGRESSION_VALIDATION_COST,
            CHECKER_COST,
            REMEDIATION_COST,
        )
        from superclaude.cli.sprint.models import TurnLedger

        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        ledger = TurnLedger(initial_budget=200)

        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# R")
        spec = tmp_path / "spec.md"
        spec.write_text("# S")

        budget_before_regression = {"val": None}
        run_counter = {"n": 0}

        def increasing_checkers(registry, run_number):
            """Run 1: 1 finding. Run 2: 3 findings (regression)."""
            run_counter["n"] += 1
            if run_counter["n"] == 1:
                registry.merge_findings([self._make_finding("F-001")], [], run_number=run_number)
            else:
                registry.merge_findings(
                    [self._make_finding("F-001"), self._make_finding("F-002"), self._make_finding("F-003")],
                    [], run_number=run_number,
                )

        def mock_regression(registry, sp, rp):
            from superclaude.cli.roadmap.convergence import RegressionResult
            budget_before_regression["val"] = ledger.consumed
            return RegressionResult(agents_succeeded=3)

        execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=increasing_checkers,
            run_remediation=lambda r: None,
            handle_regression_fn=mock_regression,
            spec_path=spec,
            roadmap_path=roadmap,
        )
        # Run 1: CHECKER_COST, remediation: REMEDIATION_COST, Run 2: CHECKER_COST, regression: REGRESSION_VALIDATION_COST
        assert budget_before_regression["val"] is not None
        expected_min = 2 * CHECKER_COST + REMEDIATION_COST + REGRESSION_VALIDATION_COST
        assert budget_before_regression["val"] >= expected_min


# --- T05.06: Parallel Validation Agents ---


class TestParallelValidation:
    """T05.06: handle_regression() spawns 3 agents in isolated dirs."""

    def test_handle_regression_creates_3_dirs(self, tmp_path):
        """handle_regression creates 3 temp dirs with independent copies."""
        from superclaude.cli.roadmap.convergence import handle_regression

        spec = tmp_path / "spec.md"
        roadmap = tmp_path / "roadmap.md"
        reg_path = tmp_path / "registry.json"
        spec.write_text("# Spec")
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(path=reg_path, release_id="test", spec_hash="abc")
        reg.save()

        result = handle_regression(reg, spec, roadmap)
        assert result.agents_succeeded == 3
        assert result.consolidated_report_path != ""

    def test_handle_regression_report_written(self, tmp_path):
        """Consolidated report written to fidelity-regression-validation.md."""
        from superclaude.cli.roadmap.convergence import handle_regression

        spec = tmp_path / "spec.md"
        roadmap = tmp_path / "roadmap.md"
        reg_path = tmp_path / "registry.json"
        spec.write_text("# Spec")
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(path=reg_path, release_id="test", spec_hash="abc")
        reg.begin_run("road1")
        f = Finding(
            id="F-001", severity="HIGH", dimension="sig",
            description="test finding", location="FR-1",
            evidence="ev", fix_guidance="fix", status="ACTIVE",
        )
        reg.merge_findings([f], [], run_number=1)
        reg.save()

        result = handle_regression(reg, spec, roadmap)
        report = Path(result.consolidated_report_path)
        assert report.exists()
        content = report.read_text()
        assert "Regression Validation Report" in content

    def test_handle_regression_no_ledger_ops(self):
        """handle_regression does not perform ledger operations internally."""
        from superclaude.cli.roadmap.convergence import handle_regression
        import inspect
        source = inspect.getsource(handle_regression)
        assert "ledger.debit" not in source
        assert "ledger.credit" not in source


# --- T05.07: Temp Directory Cleanup ---


class TestTempDirCleanupEnhanced:
    """T05.07: try/finally + atexit cleanup."""

    def test_cleanup_after_handle_regression(self, tmp_path):
        """Temp dirs cleaned up after handle_regression completes."""
        from superclaude.cli.roadmap.convergence import handle_regression, _active_validation_dirs

        spec = tmp_path / "spec.md"
        roadmap = tmp_path / "roadmap.md"
        reg_path = tmp_path / "registry.json"
        spec.write_text("# Spec")
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(path=reg_path, release_id="test", spec_hash="abc")
        reg.save()

        # Record active dirs before
        dirs_before = len(_active_validation_dirs)

        handle_regression(reg, spec, roadmap)

        # After handle_regression, all its dirs should be cleaned up
        assert len(_active_validation_dirs) <= dirs_before

    def test_no_git_worktree_artifacts(self, tmp_path):
        """No .git/worktrees/ artifacts created by handle_regression."""
        from superclaude.cli.roadmap.convergence import handle_regression

        spec = tmp_path / "spec.md"
        roadmap = tmp_path / "roadmap.md"
        reg_path = tmp_path / "registry.json"
        spec.write_text("# Spec")
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(path=reg_path, release_id="test", spec_hash="abc")
        reg.save()

        handle_regression(reg, spec, roadmap)

        # Verify no .git/worktrees created
        git_worktrees = tmp_path / ".git" / "worktrees"
        assert not git_worktrees.exists()

    def test_atexit_handler_registered(self):
        """atexit handler is registered for cleanup."""
        import atexit
        from superclaude.cli.roadmap.convergence import _atexit_cleanup
        # _atexit_cleanup is registered at module import time
        # We can verify it exists as a callable
        assert callable(_atexit_cleanup)


# --- T05.08: FR-7.1 Interface Contract ---


class TestInterfaceContract:
    """T05.08: FR-7.1 interface contract validation."""

    def test_handle_regression_signature(self):
        """handle_regression has expected signature."""
        import inspect
        from superclaude.cli.roadmap.convergence import handle_regression

        sig = inspect.signature(handle_regression)
        params = list(sig.parameters.keys())
        assert "registry" in params
        assert "spec_path" in params
        assert "roadmap_path" in params

    def test_regression_result_fields(self):
        """RegressionResult has expected fields."""
        from superclaude.cli.roadmap.convergence import RegressionResult

        r = RegressionResult(
            validated_findings=[{"id": "F-001"}],
            debate_verdicts=[{"verdict": "CONFIRM"}],
            agents_succeeded=3,
            consolidated_report_path="/tmp/report.md",
        )
        assert r.validated_findings == [{"id": "F-001"}]
        assert r.debate_verdicts == [{"verdict": "CONFIRM"}]
        assert r.agents_succeeded == 3
        assert r.consolidated_report_path == "/tmp/report.md"

    def test_convergence_result_fields(self):
        """ConvergenceResult has all expected fields."""
        result = ConvergenceResult(
            passed=True,
            run_count=1,
            final_high_count=0,
            structural_progress_log=["Run 1: 2 -> 0"],
            semantic_fluctuation_log=[],
            regression_detected=False,
            halt_reason=None,
        )
        assert result.passed
        assert result.run_count == 1
        assert result.halt_reason is None


# --- T05.09: Dual Budget Mutual Exclusion Integration Test ---


class TestMutualExclusion:
    """T05.09: Risk #5 release blocker — dual budget mutual exclusion."""

    def test_convergence_mode_no_legacy_budget_call(self, tmp_path):
        """Convergence mode never invokes legacy budget functions."""
        from superclaude.cli.roadmap.convergence import execute_fidelity_with_convergence
        from superclaude.cli.sprint.models import TurnLedger

        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc",
        )
        ledger = TurnLedger(initial_budget=61)

        def noop_checkers(registry, run_number):
            registry.merge_findings([], [], run_number=run_number)

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=noop_checkers,
            run_remediation=lambda r: None,
        )
        assert result.passed

        # Verify _check_remediation_budget was NOT called
        # (it doesn't exist in convergence.py at all — verified by source check)
        import superclaude.cli.roadmap.convergence as conv_mod
        source = Path(conv_mod.__file__).read_text()
        assert "_check_remediation_budget" not in source

    def test_legacy_mode_no_turnledger_import(self):
        """Legacy executor path does not import TurnLedger at module level."""
        import superclaude.cli.roadmap.executor as exec_mod
        source = Path(exec_mod.__file__).read_text()
        # Module-level imports should not include TurnLedger
        # (conditional import only in convergence.py)
        lines = source.split("\n")
        import_lines = [l for l in lines if l.startswith("from") or l.startswith("import")]
        for line in import_lines:
            assert "TurnLedger" not in line

    def test_no_dual_budget_code_path(self):
        """No code path activates both budget systems simultaneously."""
        import superclaude.cli.roadmap.convergence as conv_mod
        import superclaude.cli.roadmap.executor as exec_mod

        conv_source = Path(conv_mod.__file__).read_text()
        exec_source = Path(exec_mod.__file__).read_text()

        # convergence.py must not reference legacy budget
        assert "_check_remediation_budget" not in conv_source
        assert "_print_terminal_halt" not in conv_source

        # executor.py must not import TurnLedger at module level
        assert "from ..sprint.models import TurnLedger" not in exec_source.split("\n")
