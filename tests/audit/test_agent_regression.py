"""Regression tests for Phase 6 audit agent extensions.

Validates that each agent spec (audit-scanner, audit-analyzer, audit-validator,
audit-comparator, audit-consolidator) has correct wiring extensions while
preserving all existing content. Tests per SC-011, SC-012, and R7 mitigation.

Run: uv run pytest tests/audit/test_agent_regression.py -v -k "agent_regression"
"""

from __future__ import annotations

from pathlib import Path

import pytest

AGENTS_DIR = Path(__file__).resolve().parents[2] / "src" / "superclaude" / "agents"


def _read_agent(name: str) -> str:
    """Read an agent spec file and return its content."""
    path = AGENTS_DIR / f"{name}.md"
    assert path.exists(), f"Agent spec not found: {path}"
    return path.read_text()


# ---------------------------------------------------------------------------
# Scanner: REVIEW:wiring signal (T06.01, SC-011)
# ---------------------------------------------------------------------------


class TestScannerWiringExtension:
    """Regression tests for audit-scanner REVIEW:wiring signal."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.content = _read_agent("audit-scanner")

    @pytest.mark.agent_regression
    def test_review_wiring_signal_defined(self):
        """SC-011: scanner defines REVIEW:wiring classification signal."""
        assert "REVIEW:wiring" in self.content

    @pytest.mark.agent_regression
    def test_trigger_optional_callable(self):
        """Scanner triggers on Optional[Callable] parameter pattern."""
        assert "Optional[Callable]" in self.content

    @pytest.mark.agent_regression
    def test_trigger_registry_patterns(self):
        """Scanner triggers on registry naming patterns."""
        assert "_REGISTRY" in self.content
        assert "_DISPATCH" in self.content

    @pytest.mark.agent_regression
    def test_trigger_provider_directories(self):
        """Scanner triggers on provider directory membership."""
        assert "steps/" in self.content
        assert "handlers/" in self.content

    @pytest.mark.agent_regression
    def test_existing_classification_preserved(self):
        """R7: existing DELETE/REVIEW/KEEP classification taxonomy unchanged."""
        assert "| **DELETE**" in self.content
        assert "| **REVIEW**" in self.content
        assert "| **KEEP**" in self.content

    @pytest.mark.agent_regression
    def test_existing_safety_constraint_preserved(self):
        """R7: safety constraint (read-only) still present."""
        assert "DO NOT modify, edit, delete, move, or rename" in self.content

    @pytest.mark.agent_regression
    def test_existing_dynamic_loading_check_preserved(self):
        """R7: dynamic loading check section still present."""
        assert "Dynamic Loading Check" in self.content

    @pytest.mark.agent_regression
    def test_existing_incremental_save_preserved(self):
        """R7: incremental save protocol still present."""
        assert "Incremental Save Protocol" in self.content

    @pytest.mark.agent_regression
    def test_wiring_signal_is_additive(self):
        """R7: wiring signal described as additive, not replacing existing signals."""
        assert "additive" in self.content.lower()


# ---------------------------------------------------------------------------
# Analyzer: 9th field (T06.02, SC-012)
# ---------------------------------------------------------------------------


class TestAnalyzerWiringExtension:
    """Regression tests for audit-analyzer 9th field extension."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.content = _read_agent("audit-analyzer")

    @pytest.mark.agent_regression
    def test_9th_field_wiring_path_defined(self):
        """SC-012: analyzer defines Wiring path as 9th mandatory field."""
        assert "Wiring path" in self.content

    @pytest.mark.agent_regression
    def test_finding_type_unwired_declaration(self):
        """SC-012: UNWIRED_DECLARATION finding type defined."""
        assert "UNWIRED_DECLARATION" in self.content

    @pytest.mark.agent_regression
    def test_finding_type_broken_registration(self):
        """SC-012: BROKEN_REGISTRATION finding type defined."""
        assert "BROKEN_REGISTRATION" in self.content

    @pytest.mark.agent_regression
    def test_finding_type_orphan_provider(self):
        """SC-012: ORPHAN_PROVIDER finding type defined."""
        assert "ORPHAN_PROVIDER" in self.content

    @pytest.mark.agent_regression
    def test_existing_8_fields_preserved(self):
        """R7: original 8 mandatory profile fields still present."""
        required_fields = [
            "What it does",
            "Nature",
            "References",
            "CI/CD usage",
            "Superseded by",
            "Risk notes",
            "Recommendation",
            "Verification notes",
        ]
        for field in required_fields:
            assert field in self.content, f"Missing original field: {field}"

    @pytest.mark.agent_regression
    def test_existing_finding_types_preserved(self):
        """R7: original finding types still present."""
        for ftype in ("MISPLACED", "STALE", "STRUCTURAL ISSUE", "BROKEN REFS", "VERIFIED OK"):
            assert ftype in self.content, f"Missing original finding type: {ftype}"

    @pytest.mark.agent_regression
    def test_existing_safety_constraint_preserved(self):
        """R7: safety constraint still present."""
        assert "DO NOT modify, edit, delete, move, or rename" in self.content

    @pytest.mark.agent_regression
    def test_wiring_path_chain_structure(self):
        """SC-012: Wiring path describes Declaration -> Registration -> Invocation chain."""
        assert "Declaration" in self.content
        assert "Registration" in self.content
        assert "Invocation" in self.content
        assert "MISSING" in self.content

    @pytest.mark.agent_regression
    def test_references_run_wiring_analysis(self):
        """SC-012: profile instructions reference run_wiring_analysis()."""
        assert "run_wiring_analysis()" in self.content


# ---------------------------------------------------------------------------
# Validator: Check 5 (T06.03)
# ---------------------------------------------------------------------------


class TestValidatorWiringExtension:
    """Regression tests for audit-validator Check 5 extension."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.content = _read_agent("audit-validator")

    @pytest.mark.agent_regression
    def test_check_5_defined(self):
        """Check 5 wiring claim verification is defined."""
        assert "Check 5" in self.content

    @pytest.mark.agent_regression
    def test_check_5_delete_guard(self):
        """Check 5 guards DELETE recommendations on files with live wiring."""
        assert "DELETE" in self.content
        assert "live wiring" in self.content

    @pytest.mark.agent_regression
    def test_wiring_false_negative_type(self):
        """WIRING_FALSE_NEGATIVE discrepancy type defined."""
        assert "WIRING_FALSE_NEGATIVE" in self.content

    @pytest.mark.agent_regression
    def test_existing_checks_1_through_4_preserved(self):
        """R7: Checks 1-4 still present and unmodified."""
        assert "Check 1" in self.content
        assert "Check 2" in self.content
        assert "Check 3" in self.content
        assert "Check 4" in self.content

    @pytest.mark.agent_regression
    def test_existing_pass_fail_criteria_preserved(self):
        """R7: original pass/fail criteria still present."""
        assert "Discrepancy rate < 20%" in self.content

    @pytest.mark.agent_regression
    def test_existing_safety_constraint_preserved(self):
        """R7: safety constraint still present."""
        assert "DO NOT modify" in self.content

    @pytest.mark.agent_regression
    def test_critical_fail_on_wiring_false_negative(self):
        """Check 5 includes CRITICAL FAIL for DELETE on wired files."""
        assert "CRITICAL FAIL" in self.content
        assert "WIRING_FALSE_NEGATIVE" in self.content


# ---------------------------------------------------------------------------
# Comparator: Cross-file wiring check (T06.04)
# ---------------------------------------------------------------------------


class TestComparatorWiringExtension:
    """Regression tests for audit-comparator cross-file wiring check."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.content = _read_agent("audit-comparator")

    @pytest.mark.agent_regression
    def test_cross_file_wiring_check_defined(self):
        """Cross-file wiring consistency check section exists."""
        assert "Cross-File Wiring Consistency Check" in self.content

    @pytest.mark.agent_regression
    def test_orphan_claim_type(self):
        """ORPHAN_WIRING_CLAIM inconsistency type defined."""
        assert "ORPHAN_WIRING_CLAIM" in self.content

    @pytest.mark.agent_regression
    def test_phantom_consumer_type(self):
        """PHANTOM_CONSUMER inconsistency type defined."""
        assert "PHANTOM_CONSUMER" in self.content

    @pytest.mark.agent_regression
    def test_registry_mismatch_type(self):
        """REGISTRY_MISMATCH inconsistency type defined."""
        assert "REGISTRY_MISMATCH" in self.content

    @pytest.mark.agent_regression
    def test_wiring_consistency_matrix(self):
        """Wiring Consistency Matrix output format defined."""
        assert "Wiring Consistency Matrix" in self.content

    @pytest.mark.agent_regression
    def test_existing_duplication_matrix_preserved(self):
        """R7: original Duplication Matrix requirement still present."""
        assert "Duplication Matrix" in self.content

    @pytest.mark.agent_regression
    def test_existing_classification_taxonomy_preserved(self):
        """R7: original classification taxonomy still present."""
        for cat in ("DELETE", "CONSOLIDATE", "MOVE", "FLAG", "KEEP", "BROKEN REF"):
            assert cat in self.content, f"Missing original category: {cat}"

    @pytest.mark.agent_regression
    def test_existing_safety_constraint_preserved(self):
        """R7: safety constraint still present."""
        assert "DO NOT modify, edit, delete, move, or rename" in self.content


# ---------------------------------------------------------------------------
# Consolidator: Wiring Health section (T06.05)
# ---------------------------------------------------------------------------


class TestConsolidatorWiringExtension:
    """Regression tests for audit-consolidator Wiring Health section."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.content = _read_agent("audit-consolidator")

    @pytest.mark.agent_regression
    def test_wiring_health_section_defined(self):
        """Wiring Health section is defined in consolidator spec."""
        assert "Wiring Health" in self.content

    @pytest.mark.agent_regression
    def test_wiring_health_metrics(self):
        """Wiring Health section includes finding counts by type."""
        assert "UNWIRED_DECLARATION" in self.content
        assert "BROKEN_REGISTRATION" in self.content
        assert "ORPHAN_PROVIDER" in self.content

    @pytest.mark.agent_regression
    def test_wiring_health_score(self):
        """Wiring Health section includes health score levels."""
        assert "HEALTHY" in self.content
        assert "DEGRADED" in self.content
        assert "CRITICAL" in self.content

    @pytest.mark.agent_regression
    def test_wiring_health_suppressed_count(self):
        """Wiring Health section includes suppressed count."""
        assert "Suppressed" in self.content or "suppressed" in self.content

    @pytest.mark.agent_regression
    def test_existing_methodology_preserved(self):
        """R7: original methodology (merge, deduplicate, extract patterns) preserved."""
        assert "Merge" in self.content or "merge" in self.content
        assert "Deduplicate" in self.content or "deduplicate" in self.content

    @pytest.mark.agent_regression
    def test_existing_quality_requirements_preserved(self):
        """R7: original quality requirements preserved."""
        assert "Mandatory Sections" in self.content

    @pytest.mark.agent_regression
    def test_existing_safety_constraint_preserved(self):
        """R7: safety constraint still present."""
        assert "DO NOT modify any existing repository file" in self.content

    @pytest.mark.agent_regression
    def test_aggregation_rules_defined(self):
        """Wiring Health section defines aggregation rules."""
        assert "Aggregation Rules" in self.content

    @pytest.mark.agent_regression
    def test_deduplication_rules_for_wiring(self):
        """Wiring Health section has deduplication rules for wiring findings."""
        assert "Deduplication" in self.content
