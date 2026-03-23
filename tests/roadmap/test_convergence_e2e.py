"""E2E tests for the convergence system.

Exercises DeviationRegistry persistence, monotonic progress,
budget exhaustion, regression handling, convergence pass, and
semantic fluctuation through the full execute_fidelity_with_convergence
loop with controlled mock checkers and real registries.
"""
import pytest
from pathlib import Path

from superclaude.cli.roadmap.convergence import (
    DeviationRegistry,
    ConvergenceResult,
    RegressionResult,
    execute_fidelity_with_convergence,
    CHECKER_COST,
    REMEDIATION_COST,
    CONVERGENCE_PASS_CREDIT,
)
from superclaude.cli.roadmap.models import Finding
from superclaude.cli.sprint.models import TurnLedger


def _make_finding(
    id_str: str,
    severity: str = "HIGH",
    source_layer: str = "structural",
    dimension: str = "signatures",
    location: str | None = None,
) -> Finding:
    """Build a Finding with unique identity fields."""
    if location is None:
        location = f"FR-{id_str}"
    return Finding(
        id=id_str,
        severity=severity,
        dimension=dimension,
        description=f"finding-{id_str}",
        location=location,
        evidence="ev",
        fix_guidance="fix",
        status="ACTIVE",
        source_layer=source_layer,
    )


@pytest.mark.integration
class TestConvergenceE2E:
    """E2E convergence scenarios using real DeviationRegistry and mock checkers."""

    # --- SC-1: Registry persistence round-trip ---

    def test_sc1_registry_persistence(self, tmp_path: Path, audit_trail):
        """Write registry via save(), reload via load_or_create(), verify findings survive."""
        reg_path = tmp_path / "registry.json"
        release_id = "rel-1"
        spec_hash = "hash-abc"

        # Build and populate
        reg = DeviationRegistry(
            path=reg_path,
            release_id=release_id,
            spec_hash=spec_hash,
        )
        run_number = reg.begin_run("road1")
        structural = [_make_finding("F-001"), _make_finding("F-002")]
        semantic = [_make_finding("S-001", source_layer="semantic")]
        reg.merge_findings(structural, semantic, run_number=run_number)
        reg.save()

        # Reload from disk
        reg2 = DeviationRegistry.load_or_create(reg_path, release_id, spec_hash)

        # SC-1 assertion: persistence round-trip preserves all findings
        assert reg2.release_id == release_id
        assert reg2.spec_hash == spec_hash
        assert len(reg2.findings) == len(reg.findings)
        assert reg2.get_structural_high_count() == 2
        assert reg2.get_semantic_high_count() == 1
        assert reg2.get_active_high_count() == 3

        # Verify individual finding fields survived
        for stable_id, original in reg.findings.items():
            reloaded = reg2.findings[stable_id]
            assert reloaded["severity"] == original["severity"]
            assert reloaded["source_layer"] == original["source_layer"]
            assert reloaded["status"] == original["status"]
            assert reloaded["first_seen_run"] == original["first_seen_run"]
            assert reloaded["last_seen_run"] == original["last_seen_run"]

        audit_trail.record(
            test_id="test_sc1_registry_persistence",
            spec_ref="SC-1",
            assertion_type="structural",
            inputs={
                "structural_count": 2,
                "semantic_count": 1,
                "release_id": release_id,
                "spec_hash": spec_hash,
            },
            observed={
                "findings_count_match": len(reg2.findings) == len(reg.findings),
                "structural_high_count": reg2.get_structural_high_count(),
                "semantic_high_count": reg2.get_semantic_high_count(),
                "active_high_count": reg2.get_active_high_count(),
                "all_fields_survived": all(
                    reg2.findings[sid]["severity"] == orig["severity"]
                    for sid, orig in reg.findings.items()
                ),
            },
            expected={
                "findings_count_match": True,
                "structural_high_count": 2,
                "semantic_high_count": 1,
                "active_high_count": 3,
                "all_fields_survived": True,
            },
            verdict="PASS",
            evidence="Registry save/load round-trip preserves all finding fields (SC-1)",
        )

    # --- SC-2: Monotonic structural progress ---

    def test_sc2_monotonic_progress(self, tmp_path: Path, audit_trail):
        """3 convergence cycles with decreasing structural HIGHs (3->2->1).

        Verifies structural HIGH count never increases between cycles.
        """
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(
            path=reg_path, release_id="rel-1", spec_hash="hash-1",
        )
        ledger = TurnLedger(
            initial_budget=200,
            minimum_allocation=5,
            minimum_remediation_budget=3,
        )

        # Findings per run: 3 -> 2 -> 1 structural HIGHs
        findings_per_run = [
            [_make_finding("F-001"), _make_finding("F-002"), _make_finding("F-003")],
            [_make_finding("F-001"), _make_finding("F-002")],
            [_make_finding("F-001")],
        ]
        call_count = {"n": 0}

        def mock_checkers(registry: DeviationRegistry, run_number: int):
            idx = call_count["n"]
            call_count["n"] += 1
            registry.merge_findings(findings_per_run[idx], [], run_number=run_number)

        def mock_remediation(registry: DeviationRegistry):
            pass  # Remediation is a no-op; checker controls the findings

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=mock_checkers,
            run_remediation=mock_remediation,
            max_runs=3,
            roadmap_path=roadmap,
        )

        # SC-2 assertion: no regression when HIGHs monotonically decrease
        assert result.regression_detected is False

        # Verify monotonic decrease in run metadata
        structural_counts = [
            run.get("structural_high_count", 0) for run in reg.runs
        ]
        for i in range(1, len(structural_counts)):
            assert structural_counts[i] <= structural_counts[i - 1], (
                f"Structural HIGHs increased from run {i} to {i + 1}: "
                f"{structural_counts[i - 1]} -> {structural_counts[i]}"
            )

        audit_trail.record(
            test_id="test_sc2_monotonic_progress",
            spec_ref="SC-2",
            assertion_type="behavioral",
            inputs={
                "findings_per_run": [3, 2, 1],
                "max_runs": 3,
                "initial_budget": 200,
            },
            observed={
                "regression_detected": result.regression_detected,
                "structural_counts": structural_counts,
                "monotonic": all(
                    structural_counts[i] <= structural_counts[i - 1]
                    for i in range(1, len(structural_counts))
                ),
            },
            expected={
                "regression_detected": False,
                "monotonic": True,
            },
            verdict="PASS",
            evidence="Monotonically decreasing HIGHs (3->2->1) produce no regression (SC-2)",
        )

    # --- SC-3: Budget exhaustion halts after 1 run ---

    def test_sc3_budget_exhaustion(self, tmp_path: Path, audit_trail):
        """Set budget just above CHECKER_COST; convergence halts after 1 run."""
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(
            path=reg_path, release_id="rel-1", spec_hash="hash-1",
        )
        # Budget: enough for 1 checker run but not remediation + run 2
        ledger = TurnLedger(
            initial_budget=CHECKER_COST + 2,
            minimum_allocation=5,
            minimum_remediation_budget=5,
        )

        def mock_checkers(registry: DeviationRegistry, run_number: int):
            registry.merge_findings(
                [_make_finding("F-001")], [], run_number=run_number,
            )

        def mock_remediation(registry: DeviationRegistry):
            pass

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=mock_checkers,
            run_remediation=mock_remediation,
            max_runs=3,
            roadmap_path=roadmap,
        )

        # SC-3 assertion: budget exhaustion halts after 1 run
        assert result.passed is False
        assert result.run_count == 1
        assert result.halt_reason is not None
        assert "Budget" in result.halt_reason or "budget" in result.halt_reason.lower()

        audit_trail.record(
            test_id="test_sc3_budget_exhaustion",
            spec_ref="SC-3",
            assertion_type="behavioral",
            inputs={
                "initial_budget": CHECKER_COST + 2,
                "checker_cost": CHECKER_COST,
                "max_runs": 3,
            },
            observed={
                "passed": result.passed,
                "run_count": result.run_count,
                "halt_reason": result.halt_reason,
            },
            expected={
                "passed": False,
                "run_count": 1,
                "halt_reason_mentions_budget": True,
            },
            verdict="PASS",
            evidence="Budget exhaustion halts convergence after 1 run (SC-3)",
        )

    # --- SC-4: Regression handling on increasing structural HIGHs ---

    def test_sc4_regression_handling(self, tmp_path: Path, audit_trail):
        """Inject increasing structural HIGHs (1->3); verify regression detected."""
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        spec = tmp_path / "spec.md"
        roadmap.write_text("# Roadmap")
        spec.write_text("# Spec")

        reg = DeviationRegistry(
            path=reg_path, release_id="rel-1", spec_hash="hash-1",
        )
        ledger = TurnLedger(
            initial_budget=200,
            minimum_allocation=5,
            minimum_remediation_budget=3,
        )

        # Run 1: 1 HIGH, Run 2: 3 HIGHs (regression)
        findings_per_run = [
            [_make_finding("F-001")],
            [_make_finding("F-001"), _make_finding("F-002"), _make_finding("F-003")],
        ]
        call_count = {"n": 0}

        def mock_checkers(registry: DeviationRegistry, run_number: int):
            idx = call_count["n"]
            call_count["n"] += 1
            registry.merge_findings(findings_per_run[idx], [], run_number=run_number)

        def mock_remediation(registry: DeviationRegistry):
            pass

        regression_called = {"val": False}

        def mock_handle_regression(registry, sp, rp):
            regression_called["val"] = True
            return RegressionResult(agents_succeeded=3)

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=mock_checkers,
            run_remediation=mock_remediation,
            handle_regression_fn=mock_handle_regression,
            max_runs=3,
            spec_path=spec,
            roadmap_path=roadmap,
        )

        # SC-4 assertion: regression detected and handler invoked on increasing HIGHs
        assert result.regression_detected is True
        assert result.passed is False
        assert regression_called["val"] is True
        # Loop should have stopped at run 2 (regression halts further runs)
        assert result.run_count == 2

        audit_trail.record(
            test_id="test_sc4_regression_handling",
            spec_ref="SC-4",
            assertion_type="behavioral",
            inputs={
                "findings_per_run": [1, 3],
                "max_runs": 3,
            },
            observed={
                "regression_detected": result.regression_detected,
                "passed": result.passed,
                "regression_handler_called": regression_called["val"],
                "run_count": result.run_count,
            },
            expected={
                "regression_detected": True,
                "passed": False,
                "regression_handler_called": True,
                "run_count": 2,
            },
            verdict="PASS",
            evidence="Increasing HIGHs (1->3) triggers regression detection and halts at run 2 (SC-4)",
        )

    # --- SC-5: Convergence pass with credit ---

    def test_sc5_convergence_pass(self, tmp_path: Path, audit_trail):
        """Inject 0 HIGHs on run 2; verify passed=True and credit applied."""
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(
            path=reg_path, release_id="rel-1", spec_hash="hash-1",
        )
        ledger = TurnLedger(
            initial_budget=200,
            minimum_allocation=5,
            minimum_remediation_budget=3,
        )

        # Run 1: 2 HIGHs, Run 2: 0 HIGHs (pass)
        findings_per_run = [
            [_make_finding("F-001"), _make_finding("F-002")],
            [],  # all clear
        ]
        call_count = {"n": 0}

        def mock_checkers(registry: DeviationRegistry, run_number: int):
            idx = call_count["n"]
            call_count["n"] += 1
            registry.merge_findings(findings_per_run[idx], [], run_number=run_number)

        def mock_remediation(registry: DeviationRegistry):
            pass

        budget_before = ledger.reimbursed

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=mock_checkers,
            run_remediation=mock_remediation,
            max_runs=3,
            roadmap_path=roadmap,
        )

        # SC-5 assertion: convergence pass with credit applied
        assert result.passed is True
        assert result.run_count == 2
        assert result.final_high_count == 0
        # CONVERGENCE_PASS_CREDIT should have been applied
        assert ledger.reimbursed > budget_before
        assert ledger.reimbursed >= CONVERGENCE_PASS_CREDIT

        audit_trail.record(
            test_id="test_sc5_convergence_pass",
            spec_ref="SC-5",
            assertion_type="behavioral",
            inputs={
                "findings_per_run": [2, 0],
                "max_runs": 3,
                "budget_before_reimbursed": budget_before,
            },
            observed={
                "passed": result.passed,
                "run_count": result.run_count,
                "final_high_count": result.final_high_count,
                "reimbursed": ledger.reimbursed,
                "credit_applied": ledger.reimbursed > budget_before,
            },
            expected={
                "passed": True,
                "run_count": 2,
                "final_high_count": 0,
                "credit_applied": True,
            },
            verdict="PASS",
            evidence="Convergence pass on run 2 (0 HIGHs) with CONVERGENCE_PASS_CREDIT applied (SC-5)",
        )

    # --- SC-6: Semantic fluctuation warns but does not halt ---

    def test_sc6_semantic_fluctuation(self, tmp_path: Path, audit_trail):
        """Vary semantic HIGH counts between runs; verify no halt from fluctuation."""
        reg_path = tmp_path / "registry.json"
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("# Roadmap")

        reg = DeviationRegistry(
            path=reg_path, release_id="rel-1", spec_hash="hash-1",
        )
        ledger = TurnLedger(
            initial_budget=200,
            minimum_allocation=5,
            minimum_remediation_budget=3,
        )

        # Structural stays at 1 (no regression), semantic fluctuates: 1->3->0
        structural_per_run = [
            [_make_finding("F-001")],
            [_make_finding("F-001")],
            [_make_finding("F-001")],
        ]
        semantic_per_run = [
            [_make_finding("S-001", source_layer="semantic")],
            [
                _make_finding("S-001", source_layer="semantic"),
                _make_finding("S-002", source_layer="semantic"),
                _make_finding("S-003", source_layer="semantic"),
            ],
            [],  # semantic drops to 0
        ]
        call_count = {"n": 0}

        def mock_checkers(registry: DeviationRegistry, run_number: int):
            idx = call_count["n"]
            call_count["n"] += 1
            registry.merge_findings(
                structural_per_run[idx], semantic_per_run[idx], run_number=run_number,
            )

        def mock_remediation(registry: DeviationRegistry):
            pass

        result = execute_fidelity_with_convergence(
            registry=reg,
            ledger=ledger,
            run_checkers=mock_checkers,
            run_remediation=mock_remediation,
            max_runs=3,
            roadmap_path=roadmap,
        )

        # SC-6 assertion: semantic fluctuation warns but does not halt
        assert result.regression_detected is False
        # All 3 runs should have executed (structural HIGHs never cleared)
        assert result.run_count == 3
        # Semantic fluctuation was logged
        assert len(result.semantic_fluctuation_log) > 0

        audit_trail.record(
            test_id="test_sc6_semantic_fluctuation",
            spec_ref="SC-6",
            assertion_type="behavioral",
            inputs={
                "structural_per_run": [1, 1, 1],
                "semantic_per_run": [1, 3, 0],
                "max_runs": 3,
            },
            observed={
                "regression_detected": result.regression_detected,
                "run_count": result.run_count,
                "semantic_fluctuation_logged": len(result.semantic_fluctuation_log) > 0,
                "fluctuation_entries": len(result.semantic_fluctuation_log),
            },
            expected={
                "regression_detected": False,
                "run_count": 3,
                "semantic_fluctuation_logged": True,
            },
            verdict="PASS",
            evidence="Semantic fluctuation (1->3->0) warns but does not halt convergence (SC-6)",
        )
