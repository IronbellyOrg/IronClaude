"""Regression test: broken wiring detection via reachability gate (T03.06, R-044).

Verifies that the reachability gate detects a gap when ``run_post_phase_wiring_hook()``
is intentionally removed from the call chain. Uses a synthetic module structure
(does NOT modify production code) to simulate the regression scenario.

Spec refs: FR-4.4, SC-7, SC-9
Dependencies: T03.04 (GateCriteria interface), T01.06 (ReachabilityAnalyzer)
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest
import yaml

from superclaude.cli.audit.reachability import (
    ReachabilityAnalyzer,
    run_reachability_gate,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_module(source_root: Path, module_dotted: str, source: str) -> Path:
    """Write a synthetic Python module to ``source_root``."""
    parts = module_dotted.split(".")
    file_path = source_root / Path(*parts).with_suffix(".py")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    for i in range(1, len(parts)):
        init = source_root / Path(*parts[:i]) / "__init__.py"
        if not init.exists():
            init.write_text("")
    file_path.write_text(textwrap.dedent(source))
    return file_path


def _write_manifest(manifest_path: Path, entry_points: list[dict], targets: list[dict]) -> None:
    """Write a minimal wiring manifest YAML."""
    data = {
        "wiring_manifest": {
            "entry_points": entry_points,
            "required_reachable": targets,
        }
    }
    manifest_path.write_text(yaml.dump(data, default_flow_style=False))


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def workspace(tmp_path: Path) -> tuple[Path, Path]:
    """Provide a (source_root, manifest_path) pair backed by tmp_path."""
    source_root = tmp_path / "src"
    source_root.mkdir()
    manifest_path = tmp_path / "manifest.yaml"
    return source_root, manifest_path


# ---------------------------------------------------------------------------
# Test: broken wiring detection regression
# ---------------------------------------------------------------------------


def test_broken_wiring_detected(
    workspace: tuple[Path, Path], audit_trail
) -> None:
    """Removing run_post_phase_wiring_hook() call causes reachability gate FAIL.

    This regression test creates two synthetic module variants:
    1. A "healthy" executor that calls run_post_phase_wiring_hook() from
       execute_sprint() — gate should PASS.
    2. A "broken" executor identical except the hook call is removed —
       gate should FAIL with a gap referencing the missing wiring point.

    The test does NOT modify production code; it uses fully synthetic modules.
    """
    source_root, manifest_path = workspace

    # -- Broken executor: execute_sprint does NOT call run_post_phase_wiring_hook --
    _write_module(source_root, "sprint.executor", """\
        from sprint.models import PhaseResult
        from sprint.hooks import run_post_task_wiring_hook

        def run_post_phase_wiring_hook(phase, config, phase_result):
            \"\"\"Post-phase wiring hook — exists but is never called.\"\"\"
            return phase_result

        def execute_phase_tasks(phase, config):
            \"\"\"Execute tasks within a phase.\"\"\"
            run_post_task_wiring_hook(phase, config)
            return []

        def execute_sprint(config):
            \"\"\"Main sprint entry point — BROKEN: missing run_post_phase_wiring_hook() call.\"\"\"
            for phase in config.phases:
                results = execute_phase_tasks(phase, config)
                # BUG: run_post_phase_wiring_hook() should be called here but is missing
                phase_result = PhaseResult(phase=phase, results=results)
            return phase_result
    """)

    _write_module(source_root, "sprint.models", """\
        class PhaseResult:
            def __init__(self, phase=None, results=None):
                self.phase = phase
                self.results = results
    """)

    _write_module(source_root, "sprint.hooks", """\
        def run_post_task_wiring_hook(phase, config):
            pass
    """)

    # Manifest declares run_post_phase_wiring_hook must be reachable from execute_sprint
    _write_manifest(manifest_path,
        entry_points=[{"module": "sprint.executor", "function": "execute_sprint"}],
        targets=[{
            "target": "sprint.executor.run_post_phase_wiring_hook",
            "from_entry": "execute_sprint",
            "spec_ref": "FR-4.4/SC-7",
        }],
    )

    analyzer = ReachabilityAnalyzer(manifest_path)
    report = analyzer.analyze(source_root)

    # Gate must FAIL — the hook is defined but never called from execute_sprint
    assert report.passed is False, (
        "Expected FAIL: run_post_phase_wiring_hook() is not called from execute_sprint()"
    )
    assert len(report.gaps) == 1
    assert "run_post_phase_wiring_hook" in report.gaps[0].target
    assert report.gaps[0].reachable is False
    assert report.gaps[0].chain == []
    assert report.gaps[0].spec_ref == "FR-4.4/SC-7"

    # Verify structured output contains the specific missing wiring point
    report_dict = report.to_dict()
    assert report_dict["gap_count"] == 1
    assert report_dict["passed"] is False
    gap_targets = [g["target"] for g in report_dict["gaps"]]
    assert any("run_post_phase_wiring_hook" in t for t in gap_targets)

    audit_trail.record(
        test_id="test_broken_wiring_detected",
        spec_ref="FR-4.4, SC-7, SC-9",
        assertion_type="structural",
        inputs={
            "entry": "sprint.executor.execute_sprint",
            "target": "sprint.executor.run_post_phase_wiring_hook",
            "scenario": "hook defined but call removed from execute_sprint",
        },
        observed={
            "passed": report.passed,
            "gap_count": len(report.gaps),
            "gap_target": report.gaps[0].target,
            "gap_reachable": report.gaps[0].reachable,
        },
        expected={
            "passed": False,
            "gap_count": 1,
            "gap_target_contains": "run_post_phase_wiring_hook",
        },
        verdict="PASS",
        evidence=(
            "Reachability gate correctly detected that run_post_phase_wiring_hook() "
            "is defined in sprint.executor but never called from execute_sprint(). "
            "Gap reported with spec_ref FR-4.4/SC-7. Regression scenario for v3.2-T02."
        ),
    )


def test_healthy_wiring_passes(
    workspace: tuple[Path, Path], audit_trail
) -> None:
    """Contrast test: when run_post_phase_wiring_hook() IS called, gate PASSES.

    Confirms the regression test above is meaningful — a healthy executor
    with the hook call present should produce a PASS verdict.
    """
    source_root, manifest_path = workspace

    # -- Healthy executor: execute_sprint DOES call run_post_phase_wiring_hook --
    _write_module(source_root, "sprint.executor", """\
        from sprint.models import PhaseResult
        from sprint.hooks import run_post_task_wiring_hook

        def run_post_phase_wiring_hook(phase, config, phase_result):
            \"\"\"Post-phase wiring hook.\"\"\"
            return phase_result

        def execute_phase_tasks(phase, config):
            \"\"\"Execute tasks within a phase.\"\"\"
            run_post_task_wiring_hook(phase, config)
            return []

        def execute_sprint(config):
            \"\"\"Main sprint entry point — HEALTHY: calls run_post_phase_wiring_hook().\"\"\"
            for phase in config.phases:
                results = execute_phase_tasks(phase, config)
                phase_result = PhaseResult(phase=phase, results=results)
                phase_result = run_post_phase_wiring_hook(phase, config, phase_result)
            return phase_result
    """)

    _write_module(source_root, "sprint.models", """\
        class PhaseResult:
            def __init__(self, phase=None, results=None):
                self.phase = phase
                self.results = results
    """)

    _write_module(source_root, "sprint.hooks", """\
        def run_post_task_wiring_hook(phase, config):
            pass
    """)

    _write_manifest(manifest_path,
        entry_points=[{"module": "sprint.executor", "function": "execute_sprint"}],
        targets=[{
            "target": "sprint.executor.run_post_phase_wiring_hook",
            "from_entry": "execute_sprint",
            "spec_ref": "FR-4.4/SC-7",
        }],
    )

    analyzer = ReachabilityAnalyzer(manifest_path)
    report = analyzer.analyze(source_root)

    # Gate must PASS — the hook IS called from execute_sprint
    assert report.passed is True, (
        f"Expected PASS: run_post_phase_wiring_hook() is called from execute_sprint(). "
        f"Gaps: {[g.target for g in report.gaps]}"
    )
    assert len(report.gaps) == 0
    assert report.results[0].reachable is True
    assert len(report.results[0].chain) > 0

    audit_trail.record(
        test_id="test_healthy_wiring_passes",
        spec_ref="FR-4.4, SC-7, SC-9",
        assertion_type="structural",
        inputs={
            "entry": "sprint.executor.execute_sprint",
            "target": "sprint.executor.run_post_phase_wiring_hook",
            "scenario": "hook call present in execute_sprint (healthy baseline)",
        },
        observed={
            "passed": report.passed,
            "gap_count": len(report.gaps),
            "reachable": report.results[0].reachable,
            "chain": report.results[0].chain,
        },
        expected={"passed": True, "gap_count": 0},
        verdict="PASS",
        evidence=(
            "Reachability gate correctly reports PASS when run_post_phase_wiring_hook() "
            "is called from execute_sprint(). Confirms the broken-wiring regression "
            "test is meaningful — removal of the call is what triggers detection."
        ),
    )
