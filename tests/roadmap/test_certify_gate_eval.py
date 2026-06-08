"""DEV-R13-001 / DEV-R13-006 — certify gate evaluation in the dynamic path.

R1.3 wired ``build_certify_step`` via ``_run_certify_after_remediate`` (a bare
``roadmap_run_step`` call outside ``execute_pipeline``), which meant
CERTIFY_GATE was never evaluated on the produced report. The sc:reflect UC-2
audit (.dev/reflect/r1-3-uc2-validation/) surfaced this; the adversarial debate
selected "simplified Option B": evaluate the gate explicitly with NO envelope
(so the runtime-meaningful semantic_checks run and the CI-only source-tree
code_assertion is correctly skipped via the gate_passed shim).

These tests pin:
  * gate evaluation now happens for the dynamic certify step;
  * a gate-fail is recorded as ``certified-with-caveats`` (not a hard exit);
  * certify outcome is persisted to .roadmap-state.json;
  * the spec-patch resume cycle also runs certify (DEV-R13-006).
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from superclaude.cli.pipeline.models import Step, StepResult, StepStatus
from superclaude.cli.roadmap import executor as roadmap_executor
from superclaude.cli.roadmap.executor import (
    _parse_certify_counts,
    _run_certify_after_remediate,
    derive_pipeline_status,
    read_state,
)
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig


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


def _remediate_pass_result() -> StepResult:
    now = datetime.now(timezone.utc)
    step = Step(
        id="remediate",
        prompt="",
        output_file=Path("remediation-tasklist.md"),
        gate=None,
        timeout_seconds=1,
    )
    return StepResult(
        step=step, status=StepStatus.PASS, attempt=1, started_at=now, finished_at=now
    )


def _certify_report(certified: bool) -> str:
    """A CERTIFY_GATE-compliant report (frontmatter + per-finding table + body).

    ``certified`` toggles the certified_is_true semantic check (PASS vs caveats).
    """
    return (
        "---\n"
        "findings_verified: 1\n"
        "findings_passed: 1\n"
        "findings_failed: 0\n"
        f"certified: {'true' if certified else 'false'}\n"
        "certification_date: 2026-06-02\n"
        "---\n"
        "\n"
        "# Certification Report\n"
        "\n"
        "## Per-Finding Results\n"
        "\n"
        "| Finding | Severity | Result | Justification |\n"
        "|---------|----------|--------|---------------|\n"
        "| F-01 | BLOCKING | PASS | Fixed and verified |\n"
        "\n"
        "## Summary\n"
        "\n"
        "All findings were reviewed and the remediation outcome recorded.\n"
        "This body exists to satisfy the STRICT min_lines requirement.\n"
        "Additional context line one.\n"
        "Additional context line two.\n"
    )


def _patched_run_step(report_text: str):
    """Return a roadmap_run_step replacement that writes the certify report."""

    def _fake(step: Step, config, cancel_check):
        step.output_file.parent.mkdir(parents=True, exist_ok=True)
        step.output_file.write_text(report_text, encoding="utf-8")
        now = datetime.now(timezone.utc)
        return StepResult(
            step=step,
            status=StepStatus.PASS,  # subprocess "succeeds"; gate is evaluated separately
            attempt=1,
            started_at=now,
            finished_at=now,
        )

    return _fake


def test_parse_certify_counts_missing_file_uses_defaults(tmp_path):
    counts = _parse_certify_counts(tmp_path / "nope.md", default=7)
    assert counts == {"verified": 7, "passed": 0, "failed": 0}


def test_parse_certify_counts_reads_frontmatter(tmp_path):
    p = tmp_path / "certification-report.md"
    p.write_text(_certify_report(certified=True))
    counts = _parse_certify_counts(p, default=0)
    assert counts == {"verified": 1, "passed": 1, "failed": 0}


def test_noop_when_no_remediate_pass(tmp_path):
    """No remediate-PASS in results -> certify is not constructed or run."""
    config = _make_config(tmp_path)
    results: list[StepResult] = []  # no remediate
    with patch.object(roadmap_executor, "roadmap_run_step") as mock_run:
        _run_certify_after_remediate(config, results)
    mock_run.assert_not_called()
    assert results == []


def test_certify_gate_pass_records_certified(tmp_path):
    config = _make_config(tmp_path)
    results = [_remediate_pass_result()]
    with patch.object(
        roadmap_executor,
        "roadmap_run_step",
        _patched_run_step(_certify_report(certified=True)),
    ):
        _run_certify_after_remediate(config, results)

    certify = [r for r in results if r.step and r.step.id == "certify"]
    assert len(certify) == 1
    assert certify[0].status == StepStatus.PASS

    state = read_state(config.output_dir / ".roadmap-state.json")
    assert state is not None
    assert state["certify"]["certified"] is True
    assert derive_pipeline_status(state) == "certified"


def test_certify_gate_fail_records_caveats_not_halt(tmp_path):
    """certified: false fails certified_is_true -> recorded as caveats, no exit."""
    config = _make_config(tmp_path)
    results = [_remediate_pass_result()]
    with patch.object(
        roadmap_executor,
        "roadmap_run_step",
        _patched_run_step(_certify_report(certified=False)),
    ):
        # Must NOT raise SystemExit — a failed certification is a caveat.
        _run_certify_after_remediate(config, results)

    certify = [r for r in results if r.step and r.step.id == "certify"]
    assert len(certify) == 1
    assert certify[0].status == StepStatus.FAIL
    assert certify[0].gate_failure_reason  # populated with the gate reason

    state = read_state(config.output_dir / ".roadmap-state.json")
    assert state is not None
    assert state["certify"]["certified"] is False
    assert derive_pipeline_status(state) == "certified-with-caveats"


def test_spec_patch_resume_cycle_runs_certify():
    """DEV-R13-006: the spec-patch auto-resume cycle invokes certify too."""
    import inspect

    src = inspect.getsource(roadmap_executor._apply_resume_after_spec_patch)
    assert "_run_certify_after_remediate(config, resumed_results)" in src, (
        "spec-patch resume cycle must run certify after the resumed pipeline "
        "succeeds (DEV-R13-006)"
    )
