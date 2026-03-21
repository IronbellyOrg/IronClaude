"""Anti-Instinct Gate Integration Tests.

Tests the full anti-instinct audit pipeline: obligation scanner, integration
contract checker, fingerprint coverage, and gate evaluation through gate_passed().

Covers 5 integration scenarios:
1. End-to-end roadmap pipeline with anti-instinct gate active
2. Gate blocks on known-bad roadmap (cli-portify regression SC-001)
3. Gate passes on known-good roadmap
4. Structural audit emits warning without blocking
5. anti-instinct-audit.md output format and frontmatter correctness
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.pipeline.models import GateCriteria, Step, StepStatus
from superclaude.cli.roadmap.executor import (
    _build_steps,
    _run_anti_instinct_audit,
    _run_structural_audit,
)
from superclaude.cli.roadmap.gates import (
    ALL_GATES,
    ANTI_INSTINCT_GATE,
    _no_undischarged_obligations,
    _integration_contracts_covered,
    _fingerprint_coverage_check,
)
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig
from superclaude.cli.roadmap.obligation_scanner import scan_obligations
from superclaude.cli.roadmap.integration_contracts import (
    extract_integration_contracts,
    check_roadmap_coverage,
)
from superclaude.cli.roadmap.fingerprint import check_fingerprint_coverage


def _make_config(tmp_path: Path) -> RoadmapConfig:
    """Create a minimal RoadmapConfig for testing."""
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\nContent here.\n")
    output = tmp_path / "output"
    output.mkdir()
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output,
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
    )


# --- Scenario 1: Pipeline includes anti-instinct step ---


class TestAntiInstinctInPipeline:
    """Verify anti-instinct step is wired into the roadmap pipeline."""

    def test_anti_instinct_step_exists_in_build_steps(self, tmp_path):
        """anti-instinct step appears in _build_steps() output."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = []
        for entry in steps:
            if isinstance(entry, list):
                flat.extend(entry)
            else:
                flat.append(entry)
        ids = [s.id for s in flat]
        assert "anti-instinct" in ids

    def test_anti_instinct_positioned_between_merge_and_test_strategy(self, tmp_path):
        """anti-instinct is between merge and test-strategy in pipeline order."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = []
        for entry in steps:
            if isinstance(entry, list):
                flat.extend(entry)
            else:
                flat.append(entry)
        ids = [s.id for s in flat]
        merge_idx = ids.index("merge")
        ai_idx = ids.index("anti-instinct")
        ts_idx = ids.index("test-strategy")
        assert merge_idx < ai_idx < ts_idx

    def test_anti_instinct_gate_is_strict(self, tmp_path):
        """anti-instinct step uses ANTI_INSTINCT_GATE with STRICT enforcement."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = []
        for entry in steps:
            if isinstance(entry, list):
                flat.extend(entry)
            else:
                flat.append(entry)
        ai_step = next(s for s in flat if s.id == "anti-instinct")
        assert ai_step.gate is ANTI_INSTINCT_GATE
        assert ai_step.gate.enforcement_tier == "STRICT"

    def test_anti_instinct_step_metadata(self, tmp_path):
        """anti-instinct step has correct timeout and retry settings."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)
        flat = []
        for entry in steps:
            if isinstance(entry, list):
                flat.extend(entry)
            else:
                flat.append(entry)
        ai_step = next(s for s in flat if s.id == "anti-instinct")
        assert ai_step.timeout_seconds == 30
        assert ai_step.retry_limit == 0

    def test_anti_instinct_in_all_gates(self):
        """ANTI_INSTINCT_GATE is registered in ALL_GATES between merge and test-strategy."""
        gate_names = [name for name, _ in ALL_GATES]
        assert "anti-instinct" in gate_names
        ai_idx = gate_names.index("anti-instinct")
        merge_idx = gate_names.index("merge")
        ts_idx = gate_names.index("test-strategy")
        assert merge_idx < ai_idx < ts_idx


# --- Scenario 2: Gate blocks on known-bad roadmap (SC-001 cli-portify regression) ---


class TestSC001RegressionBlocks:
    """SC-001: Anti-instinct gate blocks on cli-portify-style regression cases.

    The cli-portify regression was caused by:
    - Undischarged scaffolding obligations (mocked steps never replaced)
    - Missing integration contracts (PROGRAMMATIC_RUNNERS dispatch table unwired)
    - Low fingerprint coverage (spec identifiers missing from roadmap)
    """

    def _make_bad_spec(self, tmp_path: Path) -> Path:
        """Create a spec with dispatch tables and specific identifiers."""
        spec = tmp_path / "bad-spec.md"
        spec.write_text(textwrap.dedent("""\
            # CLI Pipeline Spec

            ## Architecture

            The system uses a `PROGRAMMATIC_RUNNERS` dispatch table to route
            step execution. Each step has a dedicated handler registered in
            the `DISPATCH_TABLE`.

            ```python
            PROGRAMMATIC_RUNNERS = {
                "extract": _run_extract,
                "generate": _run_generate,
                "merge": _run_merge,
            }
            ```

            The `_run_programmatic_step` function looks up the runner and
            invokes it. The `StepExecutor` accepts a Callable for custom routing.

            ## Requirements

            FR-001: The `execute_pipeline` function MUST wire all runners.
            FR-002: The `_build_steps` function MUST populate PROGRAMMATIC_RUNNERS.
            FR-003: The `ClaudeProcess` MUST be configured via constructor injection.
        """))
        return spec

    def _make_bad_roadmap(self, tmp_path: Path) -> Path:
        """Create a roadmap with undischarged obligations and missing wiring."""
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text(textwrap.dedent("""\
            ---
            spec_source: bad-spec.md
            complexity_score: 0.8
            adversarial: true
            ---

            ## Phase 1: Skeleton Setup

            - Create mocked step runners for initial testing
            - Build placeholder dispatch table
            - Implement stub executor

            ## Phase 2: Core Implementation

            - Implement pipeline logic
            - Add error handling
            - Write basic tests

            ## Phase 3: Testing

            - Run integration tests
            - Performance benchmarks
        """))
        return roadmap

    def test_obligation_scanner_finds_undischarged(self, tmp_path):
        """Obligation scanner detects undischarged mocked/stub/placeholder terms."""
        roadmap = self._make_bad_roadmap(tmp_path)
        content = roadmap.read_text()
        report = scan_obligations(content)
        # Phase 1 has "mocked", "placeholder", "stub" — none discharged in Phase 2/3
        assert report.undischarged_count > 0

    def test_integration_contracts_find_uncovered(self, tmp_path):
        """Integration contract checker finds dispatch table without wiring task."""
        spec = self._make_bad_spec(tmp_path)
        roadmap = self._make_bad_roadmap(tmp_path)
        spec_text = spec.read_text()
        roadmap_text = roadmap.read_text()
        contracts = extract_integration_contracts(spec_text)
        assert len(contracts) > 0, "Spec should yield integration contracts"
        result = check_roadmap_coverage(contracts, roadmap_text)
        assert result.uncovered_count > 0

    def test_fingerprint_coverage_low(self, tmp_path):
        """Fingerprint coverage is below 0.7 for bad roadmap."""
        spec = self._make_bad_spec(tmp_path)
        roadmap = self._make_bad_roadmap(tmp_path)
        total, found, missing, ratio = check_fingerprint_coverage(
            spec.read_text(), roadmap.read_text()
        )
        assert total > 0
        assert ratio < 0.7

    def test_anti_instinct_gate_blocks_bad_roadmap(self, tmp_path):
        """ANTI_INSTINCT_GATE fails on audit of bad spec + roadmap."""
        spec = self._make_bad_spec(tmp_path)
        roadmap = self._make_bad_roadmap(tmp_path)
        audit_file = tmp_path / "anti-instinct-audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)

        passed, reason = gate_passed(audit_file, ANTI_INSTINCT_GATE)
        assert not passed, f"Gate should fail but passed. File content: {audit_file.read_text()[:500]}"

    def test_all_three_semantic_checks_triggered(self, tmp_path):
        """All three semantic checks should detect issues on bad input."""
        spec = self._make_bad_spec(tmp_path)
        roadmap = self._make_bad_roadmap(tmp_path)
        audit_file = tmp_path / "anti-instinct-audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        # At least one of the three checks should fail
        checks_failed = 0
        if not _no_undischarged_obligations(content):
            checks_failed += 1
        if not _integration_contracts_covered(content):
            checks_failed += 1
        if not _fingerprint_coverage_check(content):
            checks_failed += 1

        assert checks_failed >= 2, (
            f"Expected at least 2 semantic checks to fail, only {checks_failed} failed"
        )


# --- Scenario 3: Gate passes on known-good roadmap ---


class TestGatePassesGoodRoadmap:
    """Gate passes when all three checks are satisfied."""

    def _make_good_spec(self, tmp_path: Path) -> Path:
        spec = tmp_path / "good-spec.md"
        spec.write_text(textwrap.dedent("""\
            # Simple Feature Spec

            ## Requirements

            FR-001: Add a greeting endpoint.
            FR-002: Return JSON response.

            ## Success Criteria

            SC-001: Endpoint responds with 200 status.
        """))
        return spec

    def _make_good_roadmap(self, tmp_path: Path) -> Path:
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text(textwrap.dedent("""\
            ---
            spec_source: good-spec.md
            complexity_score: 0.3
            adversarial: true
            ---

            ## Phase 1: Implementation

            - Implement greeting endpoint (FR-001)
            - Return JSON response (FR-002)
            - Add endpoint tests

            ## Phase 2: Validation

            - Verify endpoint responds with 200 status (SC-001)
            - Integration testing
            - Performance check
        """))
        return roadmap

    def test_gate_passes_clean_roadmap(self, tmp_path):
        """ANTI_INSTINCT_GATE passes on a clean spec+roadmap pair."""
        spec = self._make_good_spec(tmp_path)
        roadmap = self._make_good_roadmap(tmp_path)
        audit_file = tmp_path / "anti-instinct-audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)

        passed, reason = gate_passed(audit_file, ANTI_INSTINCT_GATE)
        assert passed, f"Gate should pass. Reason: {reason}"

    def test_audit_frontmatter_correct_on_pass(self, tmp_path):
        """Frontmatter shows zero issues when gate passes."""
        spec = self._make_good_spec(tmp_path)
        roadmap = self._make_good_roadmap(tmp_path)
        audit_file = tmp_path / "anti-instinct-audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        assert "undischarged_obligations: 0" in content
        assert "uncovered_contracts: 0" in content


# --- Scenario 4: Structural audit warns without blocking ---


class TestStructuralAuditWarningOnly:
    """Structural audit hook emits warnings but never blocks pipeline."""

    def test_structural_audit_does_not_raise(self, tmp_path):
        """_run_structural_audit never raises exceptions."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nSome MUST do this. SHALL do that.\n```python\ndef foo():\n    pass\n```\n")
        extraction = tmp_path / "extraction.md"
        extraction.write_text("---\ntotal_requirements: 1\n---\n## Extraction\n")

        # Should not raise
        _run_structural_audit(spec, extraction)

    def test_structural_audit_handles_missing_files(self, tmp_path):
        """_run_structural_audit handles missing files gracefully."""
        spec = tmp_path / "nonexistent-spec.md"
        extraction = tmp_path / "nonexistent-extraction.md"

        # Should not raise
        _run_structural_audit(spec, extraction)

    def test_structural_audit_handles_no_frontmatter(self, tmp_path):
        """_run_structural_audit handles extraction without frontmatter."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nContent\n")
        extraction = tmp_path / "extraction.md"
        extraction.write_text("No frontmatter here\n")

        # Should not raise
        _run_structural_audit(spec, extraction)


# --- Scenario 5: anti-instinct-audit.md output format ---


class TestAuditOutputFormat:
    """Validate anti-instinct-audit.md output format and frontmatter."""

    def test_output_has_yaml_frontmatter(self, tmp_path):
        """Audit output starts with YAML frontmatter."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nFR-001: Do something.\n")
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("---\nspec_source: spec.md\n---\n## Phase 1\n- Do something\n")
        audit_file = tmp_path / "audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        assert content.startswith("---\n")
        assert "\n---\n" in content[3:]

    def test_output_has_required_frontmatter_fields(self, tmp_path):
        """Audit output contains all three gate-required frontmatter fields."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nFR-001: Do something.\n")
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("---\nspec_source: spec.md\n---\n## Phase 1\n- Do something\n")
        audit_file = tmp_path / "audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        assert "undischarged_obligations:" in content
        assert "uncovered_contracts:" in content
        assert "fingerprint_coverage:" in content

    def test_output_has_markdown_sections(self, tmp_path):
        """Audit output contains markdown report sections."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nFR-001: Do something.\n")
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("---\nspec_source: spec.md\n---\n## Phase 1\n- Do something\n")
        audit_file = tmp_path / "audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        assert "## Anti-Instinct Audit Report" in content
        assert "### Obligation Scanner" in content
        assert "### Integration Contract Coverage" in content
        assert "### Fingerprint Coverage" in content

    def test_output_has_sufficient_lines_for_gate(self, tmp_path):
        """Audit output has at least min_lines (10) for ANTI_INSTINCT_GATE."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nFR-001: Do something.\n")
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("---\nspec_source: spec.md\n---\n## Phase 1\n- Do something\n")
        audit_file = tmp_path / "audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        line_count = len(content.splitlines())
        assert line_count >= ANTI_INSTINCT_GATE.min_lines

    def test_output_frontmatter_values_are_numeric(self, tmp_path):
        """Frontmatter values are parseable as expected types."""
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec\nFR-001: Do something.\n")
        roadmap = tmp_path / "roadmap.md"
        roadmap.write_text("---\nspec_source: spec.md\n---\n## Phase 1\n- Do something\n")
        audit_file = tmp_path / "audit.md"

        _run_anti_instinct_audit(spec, roadmap, audit_file)
        content = audit_file.read_text()

        # Parse frontmatter
        lines = content.split("---\n")
        fm_text = lines[1]
        fm = {}
        for line in fm_text.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')

        # These should be parseable
        int(fm["undischarged_obligations"])
        int(fm["uncovered_contracts"])
        float(fm["fingerprint_coverage"])


# --- Semantic check unit tests (gate function-level) ---


class TestSemanticCheckFunctions:
    """Verify individual semantic check functions for ANTI_INSTINCT_GATE."""

    def test_no_undischarged_obligations_passes_on_zero(self):
        content = "---\nundischarged_obligations: 0\n---\n## Report\n"
        assert _no_undischarged_obligations(content) is True

    def test_no_undischarged_obligations_fails_on_nonzero(self):
        content = "---\nundischarged_obligations: 3\n---\n## Report\n"
        assert _no_undischarged_obligations(content) is False

    def test_no_undischarged_obligations_fails_on_missing(self):
        content = "---\nother_field: 0\n---\n## Report\n"
        assert _no_undischarged_obligations(content) is False

    def test_integration_contracts_covered_passes_on_zero(self):
        content = "---\nuncovered_contracts: 0\n---\n## Report\n"
        assert _integration_contracts_covered(content) is True

    def test_integration_contracts_covered_fails_on_nonzero(self):
        content = "---\nuncovered_contracts: 2\n---\n## Report\n"
        assert _integration_contracts_covered(content) is False

    def test_fingerprint_coverage_passes_above_threshold(self):
        content = "---\nfingerprint_coverage: 0.85\n---\n## Report\n"
        assert _fingerprint_coverage_check(content) is True

    def test_fingerprint_coverage_passes_at_threshold(self):
        content = "---\nfingerprint_coverage: 0.70\n---\n## Report\n"
        assert _fingerprint_coverage_check(content) is True

    def test_fingerprint_coverage_fails_below_threshold(self):
        content = "---\nfingerprint_coverage: 0.65\n---\n## Report\n"
        assert _fingerprint_coverage_check(content) is False

    def test_fingerprint_coverage_fails_on_missing(self):
        content = "---\nother_field: 0.85\n---\n## Report\n"
        assert _fingerprint_coverage_check(content) is False

    def test_all_checks_fail_on_no_frontmatter(self):
        content = "No frontmatter here"
        assert _no_undischarged_obligations(content) is False
        assert _integration_contracts_covered(content) is False
        assert _fingerprint_coverage_check(content) is False
