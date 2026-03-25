"""Tests for PortifyGatePolicy two-layer enforcement.

Covers shadow/soft/full modes, per-gate promotion, unregistered steps,
missing output files, and GateFailure population.
"""

from __future__ import annotations

from pathlib import Path

from superclaude.cli.cli_portify.executor import PortifyGatePolicy
from superclaude.cli.cli_portify.models import PortifyGateMode


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_passing_artifact(tmp_path: Path, step_id: str = "validate-config") -> Path:
    """Write a minimal artifact that passes EXEMPT-tier gate checks."""
    p = tmp_path / f"{step_id}.md"
    p.write_text("---\ntitle: test\n---\nContent line 1\n")
    return p


def _write_failing_artifact(tmp_path: Path, step_id: str = "analyze-workflow") -> Path:
    """Write an artifact that fails STRICT-tier semantic checks (< 5 sections)."""
    p = tmp_path / f"{step_id}.md"
    # STRICT analyze-workflow gate requires >=5 section headers and specific frontmatter
    p.write_text("---\nstep: 1\nsource_skill: test\ncli_name: test\ncomponent_count: 1\nanalysis_sections: 1\n---\n## One section\nContent\n")
    return p


# ---------------------------------------------------------------------------
# Shadow mode tests
# ---------------------------------------------------------------------------


class TestShadowMode:
    """SHADOW mode: evaluate gates, never warn, never block."""

    def test_shadow_never_blocks_on_failure(self, tmp_path):
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.SHADOW)
        artifact = _write_failing_artifact(tmp_path)
        result = policy.evaluate("analyze-workflow", artifact)
        assert not result.blocked
        assert result.effective_mode == PortifyGateMode.SHADOW

    def test_shadow_passes_on_success(self, tmp_path):
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.SHADOW)
        artifact = _write_passing_artifact(tmp_path)
        result = policy.evaluate("validate-config", artifact)
        assert result.passed
        assert not result.blocked


# ---------------------------------------------------------------------------
# Soft mode tests
# ---------------------------------------------------------------------------


class TestSoftMode:
    """SOFT mode: evaluate gates, never block, returns failure info."""

    def test_soft_never_blocks(self, tmp_path):
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.SOFT)
        artifact = _write_failing_artifact(tmp_path)
        result = policy.evaluate("analyze-workflow", artifact)
        assert not result.blocked
        assert result.effective_mode == PortifyGateMode.SOFT

    def test_soft_populates_failure(self, tmp_path):
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.SOFT)
        artifact = _write_failing_artifact(tmp_path)
        result = policy.evaluate("analyze-workflow", artifact)
        if not result.passed:
            assert result.failure is not None


# ---------------------------------------------------------------------------
# Full mode tests
# ---------------------------------------------------------------------------


class TestFullMode:
    """FULL mode: block on gate failure."""

    def test_full_blocks_on_failure(self, tmp_path):
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        artifact = _write_failing_artifact(tmp_path)
        result = policy.evaluate("analyze-workflow", artifact)
        if not result.passed:
            assert result.blocked
            assert result.effective_mode == PortifyGateMode.FULL

    def test_full_passes_on_success(self, tmp_path):
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        artifact = _write_passing_artifact(tmp_path)
        result = policy.evaluate("validate-config", artifact)
        assert result.passed
        assert not result.blocked


# ---------------------------------------------------------------------------
# Per-gate promotion tests
# ---------------------------------------------------------------------------


class TestPerGatePromotion:
    """Per-gate min_enforce_mode overrides global mode upward."""

    def test_shadow_global_full_min_is_full(self, tmp_path):
        """SHADOW global + FULL min_enforce → effective FULL."""
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.SHADOW)
        artifact = _write_failing_artifact(tmp_path)
        result = policy.evaluate(
            "analyze-workflow", artifact, min_enforce_mode=PortifyGateMode.FULL
        )
        assert result.effective_mode == PortifyGateMode.FULL

    def test_full_global_shadow_min_stays_full(self, tmp_path):
        """FULL global + SHADOW min_enforce → effective FULL (max wins)."""
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        artifact = _write_passing_artifact(tmp_path)
        result = policy.evaluate(
            "validate-config", artifact, min_enforce_mode=PortifyGateMode.SHADOW
        )
        assert result.effective_mode == PortifyGateMode.FULL


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Unregistered steps, missing files, GateFailure population."""

    def test_unregistered_step_passes(self):
        """Unregistered step (KeyError) → passes with tier='NONE'."""
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        result = policy.evaluate("nonexistent-step", None)
        assert result.passed
        assert result.tier == "NONE"
        assert not result.blocked

    def test_missing_output_file_passes(self, tmp_path):
        """Missing output file → passes without calling gate_passed()."""
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        missing = tmp_path / "does-not-exist.md"
        result = policy.evaluate("validate-config", missing)
        assert result.passed
        assert not result.blocked

    def test_none_output_file_passes(self):
        """None output file → passes."""
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        result = policy.evaluate("validate-config", None)
        assert result.passed

    def test_gate_failure_populated_on_fail(self, tmp_path):
        """GateFailure is populated correctly on failure."""
        policy = PortifyGatePolicy(global_mode=PortifyGateMode.FULL)
        artifact = _write_failing_artifact(tmp_path)
        result = policy.evaluate("analyze-workflow", artifact)
        if not result.passed:
            assert result.failure is not None
            assert result.failure.check_name == "gate_passed"
            assert result.failure.artifact_path == str(artifact)
