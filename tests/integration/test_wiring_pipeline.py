"""Integration tests for wiring-verification pipeline step.

Tests:
1. End-to-end pipeline executes wiring-verification, emits report, shadow mode
2. gate_passed() processes WIRING_GATE correctly (SC-005)
3. Resume behavior: completed wiring-verification step not re-executed
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.pipeline.models import (
    GateMode,
    PipelineConfig,
    Step,
    StepResult,
    StepStatus,
)
from superclaude.cli.pipeline.executor import execute_pipeline
from superclaude.cli.roadmap.executor import (
    _build_steps,
    _get_all_step_ids,
    roadmap_run_step,
    _apply_resume,
)
from superclaude.cli.roadmap.gates import ALL_GATES, WIRING_GATE
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig


def _now():
    return datetime.now(timezone.utc)


def _make_config(tmp_path: Path) -> RoadmapConfig:
    spec = tmp_path / "spec.md"
    spec.write_text("# Test Spec\nContent for testing.\n")
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output,
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        depth="standard",
    )


def _write_shadow_wiring_report(path: Path) -> None:
    """Write a well-formed shadow-mode wiring report that passes WIRING_GATE."""
    content = (
        "---\n"
        "gate: wiring-verification\n"
        "target_dir: .\n"
        "files_analyzed: 10\n"
        "files_skipped: 2\n"
        "rollout_mode: shadow\n"
        "analysis_complete: true\n"
        "audit_artifacts_used: 0\n"
        "unwired_callable_count: 0\n"
        "orphan_module_count: 0\n"
        "unwired_registry_count: 0\n"
        "critical_count: 0\n"
        "major_count: 0\n"
        "info_count: 0\n"
        "total_findings: 0\n"
        "blocking_findings: 0\n"
        "whitelist_entries_applied: 0\n"
        "---\n"
        "\n"
        "## Summary\n"
        "\n"
        "No wiring issues detected.\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# Frontmatter values for all existing steps (reusable mock runner)
_FM_VALUES = {
    "spec_source": "spec.md",
    "generated": "2026-03-19T00:00:00Z",
    "generator": "test-agent",
    "functional_requirements": "5",
    "nonfunctional_requirements": "3",
    "total_requirements": "8",
    "complexity_score": "0.7",
    "complexity_class": "MEDIUM",
    "domains_detected": "[backend, frontend]",
    "risks_identified": "3",
    "dependencies_identified": "4",
    "success_criteria_count": "5",
    "extraction_mode": "standard",
    "primary_persona": "architect",
    "total_diff_points": "3",
    "shared_assumptions_count": "4",
    "convergence_score": "0.85",
    "rounds_completed": "2",
    "base_variant": "A",
    "variant_scores": "A:78 B:72",
    "adversarial": "true",
    "validation_philosophy": "continuous-parallel",
    "validation_milestones": "3",
    "work_milestones": "6",
    "interleave_ratio": "1:2",
    "major_issue_policy": "stop-and-fix",
    "high_severity_count": "0",
    "medium_severity_count": "0",
    "low_severity_count": "0",
    "total_deviations": "0",
    "validation_complete": "true",
    "tasklist_ready": "true",
    # Wiring verification fields
    "gate": "wiring-verification",
    "target_dir": ".",
    "files_analyzed": "10",
    "files_skipped": "2",
    "rollout_mode": "shadow",
    "analysis_complete": "true",
    "audit_artifacts_used": "0",
    "unwired_callable_count": "0",
    "orphan_module_count": "0",
    "unwired_registry_count": "0",
    "critical_count": "0",
    "major_count": "0",
    "info_count": "0",
    "total_findings": "0",
    "blocking_findings": "0",
    "whitelist_entries_applied": "0",
}


def _mock_runner(step, cfg, cancel_check):
    """Mock step runner that writes gate-passing output for each step."""
    fm_fields = {}
    if step.gate and step.gate.required_frontmatter_fields:
        for f in step.gate.required_frontmatter_fields:
            fm_fields[f] = _FM_VALUES.get(f, "test_value")

    content_lines = ["---"]
    for k, v in fm_fields.items():
        content_lines.append(f"{k}: {v}")
    content_lines.append("---")
    content_lines.append("## Overview")
    min_needed = step.gate.min_lines if step.gate else 10
    for i in range(max(min_needed, 10)):
        content_lines.append(f"- Item {i}: content for {step.id}")
    content = "\n".join(content_lines)

    step.output_file.parent.mkdir(parents=True, exist_ok=True)
    step.output_file.write_text(content)

    return StepResult(
        step=step,
        status=StepStatus.PASS,
        attempt=1,
        started_at=_now(),
        finished_at=_now(),
    )


class TestWiringVerificationEndToEnd:
    """Test 1: End-to-end pipeline executes wiring-verification step."""

    def test_pipeline_runs_wiring_verification_in_shadow_mode(self, tmp_path):
        """Pipeline runs wiring-verification step, emits report, does not block."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        results = execute_pipeline(
            steps=steps,
            config=config,
            run_step=_mock_runner,
        )

        # All 10 individual steps should pass (including wiring-verification)
        assert len(results) == 10
        assert all(r.status == StepStatus.PASS for r in results)

        # Verify wiring-verification step was executed
        wiring_results = [r for r in results if r.step.id == "wiring-verification"]
        assert len(wiring_results) == 1
        assert wiring_results[0].status == StepStatus.PASS

        # Verify wiring-verification output file was created
        wiring_output = config.output_dir / "wiring-verification.md"
        assert wiring_output.exists()

    def test_wiring_verification_step_has_trailing_gate_mode(self, tmp_path):
        """Wiring-verification step must use GateMode.TRAILING."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        # Find the wiring-verification step
        flat_steps = []
        for entry in steps:
            if isinstance(entry, list):
                flat_steps.extend(entry)
            else:
                flat_steps.append(entry)

        wiring_step = next(s for s in flat_steps if s.id == "wiring-verification")
        assert wiring_step.gate_mode == GateMode.TRAILING
        assert wiring_step.timeout_seconds == 60
        assert wiring_step.retry_limit == 0

    def test_wiring_verification_positioned_after_spec_fidelity(self, tmp_path):
        """Wiring-verification appears after spec-fidelity in step order."""
        config = _make_config(tmp_path)
        step_ids = _get_all_step_ids(config)

        sf_idx = step_ids.index("spec-fidelity")
        wv_idx = step_ids.index("wiring-verification")
        rem_idx = step_ids.index("remediate")

        assert wv_idx == sf_idx + 1
        assert wv_idx < rem_idx


class TestWiringGatePassed:
    """Test 2: gate_passed() processes WIRING_GATE correctly (SC-005)."""

    def test_gate_passed_accepts_valid_shadow_report(self, tmp_path):
        """gate_passed(report_path, WIRING_GATE) returns (True, None) for
        well-formed shadow-mode report."""
        report_path = tmp_path / "wiring-verification.md"
        _write_shadow_wiring_report(report_path)

        passed, reason = gate_passed(report_path, WIRING_GATE)
        assert passed is True
        assert reason is None

    def test_gate_passed_rejects_missing_report(self, tmp_path):
        """gate_passed returns (False, reason) when report file is missing."""
        report_path = tmp_path / "nonexistent.md"
        passed, reason = gate_passed(report_path, WIRING_GATE)
        assert passed is False
        assert reason is not None

    def test_gate_passed_rejects_incomplete_frontmatter(self, tmp_path):
        """gate_passed returns (False, reason) when frontmatter is incomplete."""
        report_path = tmp_path / "wiring-verification.md"
        report_path.write_text(
            "---\ngate: wiring-verification\n---\n\nIncomplete report.\n"
        )
        passed, reason = gate_passed(report_path, WIRING_GATE)
        assert passed is False
        assert reason is not None

    def test_wiring_gate_in_all_gates(self):
        """WIRING_GATE is discoverable in ALL_GATES."""
        gate_dict = dict(ALL_GATES)
        assert "wiring-verification" in gate_dict
        assert gate_dict["wiring-verification"] is WIRING_GATE


class TestWiringVerificationResume:
    """Test 3: Resume behavior -- completed wiring-verification not re-executed."""

    def test_resume_skips_completed_wiring_verification(self, tmp_path):
        """Pipeline resumes correctly: completed wiring-verification step
        is not re-executed when its output passes the gate."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        # Pre-write all step outputs so they pass gates (simulating prior run)
        for entry in steps:
            step_list = entry if isinstance(entry, list) else [entry]
            for step in step_list:
                _mock_runner(step, config, lambda: False)

        # Apply resume logic
        resumed_steps = _apply_resume(steps, config, gate_passed)

        # All steps pass their gates, so nothing should be re-run
        assert len(resumed_steps) == 0

    def test_resume_reruns_wiring_verification_when_gate_fails(self, tmp_path):
        """When wiring-verification output fails gate, it is re-run on resume."""
        config = _make_config(tmp_path)
        steps = _build_steps(config)

        # Pre-write all step outputs EXCEPT wiring-verification
        for entry in steps:
            step_list = entry if isinstance(entry, list) else [entry]
            for step in step_list:
                if step.id != "wiring-verification":
                    _mock_runner(step, config, lambda: False)

        # Apply resume logic -- wiring-verification should need re-run
        resumed_steps = _apply_resume(steps, config, gate_passed)

        # Should have at least one step to re-run
        flat_ids = []
        for entry in resumed_steps:
            if isinstance(entry, list):
                flat_ids.extend(s.id for s in entry)
            else:
                flat_ids.append(entry.id)

        assert "wiring-verification" in flat_ids


class TestNFR007Compliance:
    """Static check: no pipeline/* imports into roadmap/* or audit/*."""

    def test_no_pipeline_imports_in_wiring_gate(self):
        """wiring_gate.py must not import from pipeline/* (except models)."""
        import ast

        wiring_gate_path = Path("src/superclaude/cli/audit/wiring_gate.py")
        if not wiring_gate_path.exists():
            pytest.skip("wiring_gate.py not found")

        source = wiring_gate_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        pipeline_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                # Allow imports from pipeline.models (data types only)
                if "pipeline" in node.module and "models" not in node.module:
                    pipeline_imports.append(node.module)

        assert pipeline_imports == [], (
            f"NFR-007 violation: wiring_gate.py imports from pipeline: {pipeline_imports}"
        )
