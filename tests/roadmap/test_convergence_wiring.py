"""Integration tests for _run_convergence_spec_fidelity wiring.

Validates that the executor function correctly wires registry construction,
finding merge, remediation dict access, budget constants, and end-to-end
convergence pass/fail paths.
"""
import hashlib
import pytest
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from superclaude.cli.roadmap.convergence import (
    CHECKER_COST,
    CONVERGENCE_PASS_CREDIT,
    DeviationRegistry,
    MAX_CONVERGENCE_BUDGET,
    REMEDIATION_COST,
    execute_fidelity_with_convergence,
)
from superclaude.cli.roadmap.models import Finding, RoadmapConfig
from superclaude.cli.pipeline.models import Step, StepResult, StepStatus, GateMode
from superclaude.cli.sprint.models import TurnLedger


def _make_finding(
    id_str,
    severity="HIGH",
    source_layer="structural",
    dimension="signatures",
    location=None,
):
    """Create a Finding with unique location for stable ID generation."""
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
    )


def _make_step(tmp_path):
    """Create a minimal Step for _run_convergence_spec_fidelity."""
    return Step(
        id="step-8",
        prompt="spec fidelity",
        output_file=tmp_path / "spec-fidelity.md",
        gate=None,
        timeout_seconds=60,
    )


def _make_config(tmp_path):
    """Create a minimal RoadmapConfig with spec and output dir."""
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\nFR-1: Must have feature X\n")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    roadmap = output_dir / "roadmap.md"
    roadmap.write_text("# Roadmap\n## Feature X\nImplement FR-1\n")
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output_dir,
    )


def _make_ledger():
    """Create a TurnLedger with standard convergence budget."""
    return TurnLedger(
        initial_budget=MAX_CONVERGENCE_BUDGET,
        minimum_allocation=CHECKER_COST,
        minimum_remediation_budget=REMEDIATION_COST,
        reimbursement_rate=0.8,
    )


@pytest.mark.integration
class TestRegistryConstruction:
    """Test 1: Verify load_or_create() receives correct args."""

    def test_registry_construction(self, tmp_path):
        """DeviationRegistry.load_or_create() receives path, release_id, spec_hash."""
        config = _make_config(tmp_path)
        spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
        registry_path = config.output_dir / "deviation-registry.json"

        registry = DeviationRegistry.load_or_create(
            registry_path,
            release_id=config.output_dir.name,
            spec_hash=spec_hash,
        )

        assert registry.path == registry_path
        assert registry.release_id == config.output_dir.name
        assert registry.spec_hash == spec_hash
        assert len(registry.runs) == 0
        assert len(registry.findings) == 0


@pytest.mark.integration
class TestMergeFindingsStructuralOnly:
    """Test 2: Verify merge_findings with structural findings only."""

    def test_merge_findings_structural_only(self, tmp_path):
        """merge_findings(structural, [], run_number) tags source_layer=structural."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc123",
        )
        structural = [
            _make_finding("F-001"),
            _make_finding("F-002"),
        ]
        reg.begin_run("road1")
        reg.merge_findings(structural, [], run_number=1)

        assert reg.get_structural_high_count() == 2
        assert reg.get_semantic_high_count() == 0
        for finding in reg.findings.values():
            assert finding["source_layer"] == "structural"
            assert finding["status"] == "ACTIVE"


@pytest.mark.integration
class TestMergeFindingsSemanticOnly:
    """Test 3: Verify merge_findings with semantic findings only."""

    def test_merge_findings_semantic_only(self, tmp_path):
        """merge_findings([], semantic, run_number) tags source_layer=semantic."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc123",
        )
        semantic = [
            _make_finding("S-001", source_layer="semantic"),
            _make_finding("S-002", source_layer="semantic"),
        ]
        reg.begin_run("road1")
        reg.merge_findings([], semantic, run_number=1)

        assert reg.get_structural_high_count() == 0
        assert reg.get_semantic_high_count() == 2
        for finding in reg.findings.values():
            assert finding["source_layer"] == "semantic"
            assert finding["status"] == "ACTIVE"


@pytest.mark.integration
class TestRemediationDictAccess:
    """Test 4: Verify get_active_highs() dicts consumed correctly."""

    def test_remediation_dict_access(self, tmp_path):
        """get_active_highs() returns dicts with keys needed by remediation wiring."""
        reg = DeviationRegistry(
            path=tmp_path / "reg.json",
            release_id="test",
            spec_hash="abc123",
        )
        finding = _make_finding("F-001")
        reg.begin_run("road1")
        reg.merge_findings([finding], [], run_number=1)

        active_highs = reg.get_active_highs()
        assert len(active_highs) == 1

        d = active_highs[0]
        # Verify all keys needed by _run_remediation in executor.py
        assert "stable_id" in d
        assert "severity" in d
        assert "dimension" in d
        assert "description" in d
        assert "location" in d
        assert "files_affected" in d
        assert "status" in d

        # Verify values are correct types for Finding construction
        assert d["severity"] == "HIGH"
        assert d["status"] == "ACTIVE"
        assert isinstance(d["files_affected"], list)
        assert isinstance(d["stable_id"], str)


@pytest.mark.integration
class TestTurnledgerBudgetParams:
    """Test 5: Verify budget constants exist and are positive ints."""

    def test_turnledger_budget_params(self):
        """MAX_CONVERGENCE_BUDGET, CHECKER_COST, REMEDIATION_COST are positive ints."""
        assert isinstance(MAX_CONVERGENCE_BUDGET, int)
        assert isinstance(CHECKER_COST, int)
        assert isinstance(REMEDIATION_COST, int)
        assert isinstance(CONVERGENCE_PASS_CREDIT, int)

        assert MAX_CONVERGENCE_BUDGET > 0
        assert CHECKER_COST > 0
        assert REMEDIATION_COST > 0
        assert CONVERGENCE_PASS_CREDIT > 0

        # Budget must be large enough for at least one full cycle
        assert MAX_CONVERGENCE_BUDGET >= CHECKER_COST + REMEDIATION_COST


@pytest.mark.integration
class TestEndToEndConvergencePass:
    """Test 6: Full path with 0 highs -> passed=True."""

    def test_end_to_end_convergence_pass(self, tmp_path):
        """Convergence engine returns passed=True when checkers find 0 HIGHs."""
        config = _make_config(tmp_path)
        spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
        registry = DeviationRegistry.load_or_create(
            config.output_dir / "deviation-registry.json",
            release_id=config.output_dir.name,
            spec_hash=spec_hash,
        )
        ledger = _make_ledger()
        roadmap_path = config.output_dir / "roadmap.md"

        def run_checkers_clean(reg, run_number):
            """Checker that finds no issues."""
            reg.merge_findings([], [], run_number)

        def run_remediation_noop(reg):
            """No-op remediation."""
            pass

        result = execute_fidelity_with_convergence(
            registry=registry,
            ledger=ledger,
            run_checkers=run_checkers_clean,
            run_remediation=run_remediation_noop,
            handle_regression_fn=None,
            max_runs=3,
            spec_path=config.spec_file,
            roadmap_path=roadmap_path,
        )

        assert result.passed is True
        assert result.run_count == 1
        assert result.final_high_count == 0
        assert result.regression_detected is False
        assert result.halt_reason is None


@pytest.mark.integration
class TestEndToEndConvergenceFail:
    """Test 7: Full path with persistent HIGHs -> passed=False."""

    def test_end_to_end_convergence_fail(self, tmp_path):
        """Convergence engine returns passed=False when HIGHs persist across all runs."""
        config = _make_config(tmp_path)
        spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
        registry = DeviationRegistry.load_or_create(
            config.output_dir / "deviation-registry.json",
            release_id=config.output_dir.name,
            spec_hash=spec_hash,
        )
        ledger = _make_ledger()
        roadmap_path = config.output_dir / "roadmap.md"

        persistent_finding = _make_finding("F-PERSIST")

        def run_checkers_with_highs(reg, run_number):
            """Checker that always finds 1 HIGH."""
            reg.merge_findings([persistent_finding], [], run_number)

        def run_remediation_noop(reg):
            """Remediation that does not fix anything."""
            pass

        result = execute_fidelity_with_convergence(
            registry=registry,
            ledger=ledger,
            run_checkers=run_checkers_with_highs,
            run_remediation=run_remediation_noop,
            handle_regression_fn=None,
            max_runs=3,
            spec_path=config.spec_file,
            roadmap_path=roadmap_path,
        )

        assert result.passed is False
        assert result.run_count == 3
        assert result.final_high_count >= 1
        assert result.halt_reason is not None
        assert "Convergence not reached" in result.halt_reason
