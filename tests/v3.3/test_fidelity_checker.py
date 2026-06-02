"""T03.07: Impl-vs-spec fidelity checker positive + negative tests (R-045).

Two tests validating FidelityChecker against synthetic fixtures (per R-3 mitigation):
(a) Positive — checker finds existing implementation evidence for a known FR.
(b) Negative — checker flags a gap for a synthetic FR with no matching implementation.

Both tests use the real ``FidelityChecker`` class with no mocks on checker internals.
Synthetic source dirs and spec files control test conditions deterministically.

Spec refs: FR-5.2, SC-11
Dependencies: T03.02 (fidelity_checker.py)
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from superclaude.cli.roadmap.fidelity_checker import FidelityChecker

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_spec(spec_path: Path, content: str) -> Path:
    """Write a synthetic spec file."""
    spec_path.write_text(textwrap.dedent(content), encoding="utf-8")
    return spec_path


def _write_python(source_dir: Path, rel_path: str, content: str) -> Path:
    """Write a synthetic Python file into source_dir."""
    file_path = source_dir / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(textwrap.dedent(content), encoding="utf-8")
    return file_path


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def synth_workspace(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Provide (source_dir, spec_path, tmp_path) for synthetic test scenarios."""
    source_dir = tmp_path / "src"
    source_dir.mkdir()
    spec_path = tmp_path / "spec.md"
    return source_dir, spec_path, tmp_path


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestFidelityCheckerPositive:
    """Positive case: checker finds existing implementation evidence."""

    def test_fidelity_checker_positive(
        self, synth_workspace: tuple[Path, Path, Path], audit_trail
    ) -> None:
        """Checker reports evidence found for known existing function/class.

        Setup:
        - Synthetic spec mentions FR-1.1 with function `run_wiring_analysis()`
          and class `WiringReport`.
        - Synthetic codebase contains both definitions.
        - Checker should report both as FOUND.

        Spec refs: FR-5.2, SC-11
        """
        audit_trail.start_timer()

        source_dir, spec_path, _ = synth_workspace

        # Create synthetic codebase with known implementations
        _write_python(
            source_dir,
            "audit/wiring_gate.py",
            """\
            class WiringReport:
                \"\"\"Report from wiring analysis.\"\"\"
                def __init__(self):
                    self.files_analyzed = 0
                    self.failure_reason = ""

            def run_wiring_analysis(config, source_dir):
                \"\"\"Run wiring analysis on source directory.\"\"\"
                return WiringReport()
        """,
        )

        # Create spec referencing FR-1.1 with those function/class names
        _write_spec(
            spec_path,
            """\
            # Specification

            ## FR-1.1 Wiring Analysis Gate

            The `run_wiring_analysis()` function shall analyze Python source files
            in the target directory and produce a `WiringReport` instance containing
            analysis results.
        """,
        )

        # Run checker with no allowlist — rely on auto-extraction
        checker = FidelityChecker(source_dir=source_dir)
        results = checker.check(spec_path)

        # Should find FR-1.1 with evidence
        assert len(results) >= 1, f"Expected at least 1 result, got {len(results)}"

        fr_1_1 = next((r for r in results if r.fr_id == "FR-1.1"), None)
        assert fr_1_1 is not None, (
            f"Expected result for FR-1.1, got FRs: {[r.fr_id for r in results]}"
        )
        assert fr_1_1.found is True, (
            f"Expected FR-1.1 found=True, got found={fr_1_1.found}; "
            f"searched={fr_1_1.searched_names}, evidence={fr_1_1.evidence_names}"
        )
        assert len(fr_1_1.evidence_names) > 0, (
            "Expected at least one evidence name for FR-1.1"
        )

        # Verify the specific names were found
        evidence_set = set(fr_1_1.evidence_names)
        assert (
            "run_wiring_analysis" in evidence_set or "WiringReport" in evidence_set
        ), (
            f"Expected 'run_wiring_analysis' or 'WiringReport' in evidence, "
            f"got {fr_1_1.evidence_names}"
        )

        audit_trail.record(
            test_id="test_fidelity_checker_positive",
            spec_ref="FR-5.2, SC-11",
            assertion_type="behavioral",
            inputs={
                "spec_fr": "FR-1.1",
                "spec_names": ["run_wiring_analysis", "WiringReport"],
                "codebase_has": ["run_wiring_analysis", "WiringReport"],
                "scenario": "positive — known impl exists",
            },
            observed={
                "fr_id": fr_1_1.fr_id,
                "found": fr_1_1.found,
                "evidence_names": fr_1_1.evidence_names,
                "searched_names": fr_1_1.searched_names,
            },
            expected={
                "found": True,
                "evidence_contains": ["run_wiring_analysis", "WiringReport"],
            },
            verdict="PASS",
            evidence=(
                f"FidelityChecker correctly found implementation evidence for FR-1.1: "
                f"evidence={fr_1_1.evidence_names}. "
                f"Searched names: {fr_1_1.searched_names}"
            ),
        )


class TestFidelityCheckerNegative:
    """Negative case: checker flags gap for missing implementation."""

    def test_fidelity_checker_negative(
        self, synth_workspace: tuple[Path, Path, Path], audit_trail
    ) -> None:
        """Checker reports gap for synthetic FR with no matching implementation.

        Setup:
        - Synthetic spec mentions FR-9.9 with function `compute_flux_capacitor()`
          and class `FluxCapacitorEngine`.
        - Synthetic codebase does NOT contain these definitions.
        - Checker should report FR-9.9 as NOT FOUND (gap).

        Spec refs: FR-5.2, SC-11
        """
        audit_trail.start_timer()

        source_dir, spec_path, _ = synth_workspace

        # Create synthetic codebase with UNRELATED implementations only
        _write_python(
            source_dir,
            "utils/helpers.py",
            """\
            def format_output(data):
                \"\"\"Format data for display — unrelated to FR-9.9.\"\"\"
                return str(data)

            class OutputFormatter:
                \"\"\"Formatter class — unrelated to FR-9.9.\"\"\"
                pass
        """,
        )

        # Create spec referencing FR-9.9 with names that do NOT exist in codebase
        _write_spec(
            spec_path,
            """\
            # Specification

            ## FR-9.9 Flux Capacitor Integration

            The `compute_flux_capacitor()` function shall initialize the
            `FluxCapacitorEngine` class and execute temporal synchronization.
        """,
        )

        # Run checker — should flag FR-9.9 as missing
        checker = FidelityChecker(source_dir=source_dir)
        results = checker.check(spec_path)

        assert len(results) >= 1, f"Expected at least 1 result, got {len(results)}"

        fr_9_9 = next((r for r in results if r.fr_id == "FR-9.9"), None)
        assert fr_9_9 is not None, (
            f"Expected result for FR-9.9, got FRs: {[r.fr_id for r in results]}"
        )
        assert fr_9_9.found is False, (
            f"Expected FR-9.9 found=False (gap), got found={fr_9_9.found}; "
            f"evidence={fr_9_9.evidence_names}"
        )
        assert len(fr_9_9.evidence_names) == 0, (
            f"Expected no evidence for FR-9.9, got {fr_9_9.evidence_names}"
        )
        assert len(fr_9_9.searched_names) > 0, (
            "Expected searched_names to list what was looked for"
        )

        # Also verify Finding-compatible output reports the gap
        findings = checker.check_as_findings(spec_path)
        gap_findings = [f for f in findings if "FR-9.9" in f.description]
        assert len(gap_findings) >= 1, (
            f"Expected at least 1 Finding for FR-9.9 gap, got {len(gap_findings)}"
        )
        assert gap_findings[0].severity == "HIGH"
        assert gap_findings[0].dimension == "fidelity"

        audit_trail.record(
            test_id="test_fidelity_checker_negative",
            spec_ref="FR-5.2, SC-11",
            assertion_type="behavioral",
            inputs={
                "spec_fr": "FR-9.9",
                "spec_names": ["compute_flux_capacitor", "FluxCapacitorEngine"],
                "codebase_has": ["format_output", "OutputFormatter"],
                "scenario": "negative — no matching impl exists",
            },
            observed={
                "fr_id": fr_9_9.fr_id,
                "found": fr_9_9.found,
                "evidence_names": fr_9_9.evidence_names,
                "searched_names": fr_9_9.searched_names,
                "finding_count": len(gap_findings),
                "finding_severity": gap_findings[0].severity,
            },
            expected={
                "found": False,
                "evidence_names": [],
                "finding_count_gte": 1,
                "finding_severity": "HIGH",
            },
            verdict="PASS",
            evidence=(
                f"FidelityChecker correctly flagged FR-9.9 as gap (found=False). "
                f"Searched for: {fr_9_9.searched_names}. "
                f"No evidence found in codebase. "
                f"check_as_findings() produced {len(gap_findings)} HIGH-severity "
                f"Finding(s) for the gap."
            ),
        )


class TestFidelityCheckerFailClosed:
    """§MVR §4 / R1.6 Step 11.4: unverifiable FRs fail CLOSED, not open.

    Regression for the deleted fail-open defaults (fidelity_checker.py:302/:320):
    an FR that cannot be positively verified (no extractable names, or only a
    partial name match) must report found=False + surface a HIGH gap Finding,
    NOT silently default to found=True.
    """

    def test_no_extractable_names_reports_not_found(
        self, synth_workspace: tuple[Path, Path, Path], audit_trail
    ) -> None:
        """An FR with no extractable function/class names is NOT auto-passed.

        Pre-R1.6 this branch defaulted to ``found=True`` (fail-open). Fail-closed
        (§MVR §4): found=False, ambiguous=True, and a HIGH gap Finding surfaces.
        """
        audit_trail.start_timer()
        source_dir, spec_path, _ = synth_workspace
        _write_python(
            source_dir,
            "utils/helpers.py",
            """\
            def format_output(data):
                return str(data)
            """,
        )
        # FR prose carries NO code-quoted function/class names → no extractable names
        _write_spec(
            spec_path,
            """\
            # Specification

            ## FR-7.1 Performance Budget

            The system shall respond to user requests promptly and remain
            responsive under sustained load.
            """,
        )
        checker = FidelityChecker(source_dir=source_dir)
        results = checker.check(spec_path)
        fr = next((r for r in results if r.fr_id == "FR-7.1"), None)
        assert fr is not None, (
            f"Expected FR-7.1 result, got {[r.fr_id for r in results]}"
        )
        assert fr.found is False, (
            f"Fail-closed: unverifiable FR must be found=False, got {fr.found}"
        )
        assert fr.ambiguous is True, "Unverifiable FR should be flagged ambiguous"
        findings = checker.check_as_findings(spec_path)
        gap = [f for f in findings if "FR-7.1" in f.description]
        assert gap and gap[0].severity == "HIGH", (
            "Fail-closed must surface a HIGH gap Finding for the unverifiable FR"
        )
        audit_trail.record(
            test_id="test_no_extractable_names_reports_not_found",
            spec_ref="§MVR §4, Contract #4",
            assertion_type="behavioral",
            inputs={
                "fr": "FR-7.1",
                "extractable_names": [],
                "scenario": "no names → fail-closed",
            },
            observed={
                "found": fr.found,
                "ambiguous": fr.ambiguous,
                "gap_findings": len(gap),
            },
            expected={"found": False, "ambiguous": True, "gap_findings_gte": 1},
            verdict="PASS",
            evidence="Unverifiable FR-7.1 fail-closed (found=False) + HIGH gap Finding; was found=True under the deleted fail-open.",
        )

    def test_partial_evidence_does_not_auto_pass(
        self, synth_workspace: tuple[Path, Path, Path], audit_trail
    ) -> None:
        """Partial name evidence (some expected names missing) does NOT auto-PASS.

        Pre-R1.6 any single matching name set ``found=True`` (fail-open). Fail-closed
        (§MVR §4): a PASS requires ALL expected names; a partial match is
        found=False, ambiguous=True, with a HIGH gap Finding.
        """
        audit_trail.start_timer()
        source_dir, spec_path, _ = synth_workspace
        # Codebase has ONLY alpha_handler, NOT BetaProcessor
        _write_python(
            source_dir,
            "mod/alpha.py",
            """\
            def alpha_handler(x):
                return x
            """,
        )
        _write_spec(
            spec_path,
            """\
            # Specification

            ## FR-8.1 Dual Component Coordination

            The `alpha_handler()` function and the `BetaProcessor` class shall
            coordinate request handling.
            """,
        )
        checker = FidelityChecker(source_dir=source_dir)
        results = checker.check(spec_path)
        fr = next((r for r in results if r.fr_id == "FR-8.1"), None)
        assert fr is not None, (
            f"Expected FR-8.1 result, got {[r.fr_id for r in results]}"
        )
        assert "alpha_handler" in fr.evidence_names, (
            "Partial match should still record the matched name as evidence"
        )
        assert fr.found is False, (
            f"Fail-closed: partial match (BetaProcessor missing) must be found=False, "
            f"got {fr.found}; evidence={fr.evidence_names}"
        )
        assert fr.ambiguous is True, "Partial match should be flagged ambiguous"
        findings = checker.check_as_findings(spec_path)
        gap = [f for f in findings if "FR-8.1" in f.description]
        assert gap and gap[0].severity == "HIGH", (
            "Fail-closed must surface a HIGH gap Finding for the partial match"
        )
        audit_trail.record(
            test_id="test_partial_evidence_does_not_auto_pass",
            spec_ref="§MVR §4, Contract #4",
            assertion_type="behavioral",
            inputs={
                "fr": "FR-8.1",
                "expected": ["alpha_handler", "BetaProcessor"],
                "codebase_has": ["alpha_handler"],
                "scenario": "partial match → fail-closed",
            },
            observed={
                "found": fr.found,
                "ambiguous": fr.ambiguous,
                "evidence": fr.evidence_names,
            },
            expected={"found": False, "ambiguous": True},
            verdict="PASS",
            evidence="Partial-match FR-8.1 fail-closed (found=False) + HIGH gap Finding; was found=True under the deleted fail-open.",
        )
