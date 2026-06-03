"""Generation-time phantom-ID PREVENTION regression (TASK-RF-20260603-180207 Area B).

Area B closes the gap where the executor sourced the generate/merge step's
generation-time ``spec_ids`` from ``extraction.json`` -- which is empty unless
``--tool-write-extract`` is set (default False) -- so the
``render_step_tool_write_with_id_check`` subset check silently degraded to a
no-op and phantom-ID PREVENTION fell back entirely to the merge GATE.

The fix sources ``_spec_ids`` + ``accepted_deviations`` from the ALWAYS-written
``spec_id_registry.json`` via ``SpecIdRegistry.from_payload(...).union_of_known()``,
FAILS SHUT (StepResult FAIL) for generate/merge when the registry is
missing/unreadable, and passes ``require_spec_ids=True`` to the renderer so an
empty universe is itself a hard error rather than a silent skip.

These tests are deterministic (NO real LLM / NO network):

* (a, d) renderer-level: pure file-I/O over ``tmp_path`` calling
  ``render_step_tool_write_with_id_check`` directly.
* (b, c) executor-level: drive ``roadmap_run_step`` with a mocked
  ``ClaudeProcess`` (house idiom, see ``tests/roadmap/test_file_passing.py``)
  so the render-dispatch branch -- which lives AFTER ``proc.start()``/
  ``proc.wait()`` -- is reached with no subprocess.

The pre-existing merge-gate catch (``test_merge_rejects_phantom_id``) and the
renderer-level skip (``test_id_check_skips_when_spec_ids_empty``) remain green
as defense-in-depth; this file adds the missing EXECUTOR-level regression.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from superclaude.cli.pipeline.models import Step, StepStatus
from superclaude.cli.roadmap.executor import roadmap_run_step
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig
from superclaude.cli.roadmap.tool_writer import (
    render_step_tool_write_with_id_check,
)

# ---------------------------------------------------------------------------
# Schema-valid fixtures (copied from test_tool_write_step_{generate,merge}.py,
# which prove these dicts pass generate.schema.json / merge.schema.json -- so
# the only validation that can fail here is the phantom-ID subset check, not the
# schema gate).
# ---------------------------------------------------------------------------


def _deliverable(num: int, rid: str, title: str) -> dict:
    return {
        "num": num,
        "id": rid,
        "title": title,
        "description": f"Implement {rid}.",
        "comp": "M",
        "deps": "",
        "ac": "Covered by tests.",
        "eff": "M",
        "pri": "P1",
    }


def _milestone(mid: str, title: str, deliverables: list[dict], **extra: object) -> dict:
    base = {
        "id": mid,
        "title": title,
        "duration": "weeks",
        "exit_criteria": f"{mid} deliverables implemented and tested.",
        "deliverables": deliverables,
        "integration_points": (
            f"{mid} integrates with the adjacent milestones via the shared "
            "schema/template substrate and the phantom-ID gate."
        ),
        "milestone_dependencies": (
            f"{mid} depends on the prior milestone's exit criteria being met."
        ),
        "risk_assessment": (
            f"{mid}-specific risks are mitigated by tests and the gate suite."
        ),
    }
    base.update(extra)
    return base


def _generate_json() -> dict:
    """Schema-valid generate output; roadmap_ids = FR-1..FR-5 (all FR-family)."""
    return {
        "frontmatter": {
            "spec_source": "spec.md",
            "generated": "2026-06-02T00:00:00Z",
            "generator": "opus-architect",
            "complexity_score": 0.62,
            "complexity_class": "HIGH",
            "primary_persona": "architect",
            "total_requirements": 5,
            "milestone_count": 3,
            "deliverable_count": 9,
        },
        "executive_summary": (
            "This roadmap sequences the foundational, core-logic, and hardening "
            "milestones needed to deliver all five functional requirements while "
            "preserving every identifier surfaced by the extraction step. Each "
            "milestone carries its own deliverable table, risk assessment, and "
            "exit criteria so progress is independently verifiable."
        ),
        "milestone_summary": [
            {
                "milestone": "M1",
                "title": "Foundation",
                "duration": "weeks 1-3",
                "exit_criteria": "FR-1, FR-2 implemented and tested.",
            },
            {
                "milestone": "M2",
                "title": "Core Logic",
                "duration": "weeks 4-6",
                "exit_criteria": "FR-3, FR-4 implemented and tested.",
            },
            {
                "milestone": "M3",
                "title": "Hardening and Production Readiness",
                "duration": "weeks 7-9",
                "exit_criteria": "FR-5 implemented; observability in place.",
            },
        ],
        "dependency_graph": "M1 -> M2 -> M3",
        "milestones": [
            {
                "id": "M1",
                "title": "Foundation",
                "duration": "weeks 1-3",
                "exit_criteria": "FR-1, FR-2 implemented and tested.",
                "deliverables": [
                    _deliverable(1, "FR-1", "Bootstrap the extraction substrate"),
                    _deliverable(2, "FR-2", "Persist the structured sidecar"),
                    _deliverable(3, "COMP-loader", "Schema loader component"),
                ],
                "risk_assessment": (
                    "Schema drift between prompt and template is mitigated by the "
                    "SoT-drift guard test. Sidecar corruption is mitigated by "
                    "atomic writes and pretty-printed JSON."
                ),
                "open_questions": [
                    {
                        "id": "OQ-1",
                        "question": "Should chunked mode auto-detect?",
                        "impact": "Throughput on large specs",
                        "owner": "TBD",
                        "target": "M1",
                    }
                ],
            },
            {
                "id": "M2",
                "title": "Core Logic",
                "duration": "weeks 4-6",
                "exit_criteria": "FR-3, FR-4 implemented and tested.",
                "deliverables": [
                    _deliverable(4, "FR-3", "Render the markdown artifact"),
                    _deliverable(5, "FR-4", "Wire the phantom-ID gate"),
                    _deliverable(6, "API-render", "Render API surface"),
                ],
                "risk_assessment": (
                    "Phantom ids are rejected at generation time by "
                    "validate_id_subset; the render is skipped entirely when a "
                    "phantom id is present, so no polluted markdown is written."
                ),
            },
            {
                "id": "M3",
                "title": "Hardening and Production Readiness",
                "duration": "weeks 7-9",
                "exit_criteria": "FR-5 implemented; observability in place.",
                "deliverables": [
                    _deliverable(7, "FR-5", "Emit the timeline estimates"),
                    _deliverable(8, "OPS-metrics", "Metrics and alerting"),
                    _deliverable(9, "TEST-e2e", "End-to-end gate-parity tests"),
                ],
                "risk_assessment": (
                    "Insufficient observability is mitigated by a dedicated "
                    "metrics deliverable and an end-to-end test row."
                ),
            },
        ],
        "resource_requirements": (
            "External Dependencies: jsonschema, jinja2.\n"
            "Infrastructure Requirements: CI runner with UV and Python 3.10+."
        ),
        "risk_register": [
            {
                "id": "RSK-1",
                "risk": "Phantom ids leak into the roadmap.",
                "severity": "high",
                "mitigation": "validate_id_subset at generation time.",
            },
            {
                "id": "RSK-2",
                "risk": "Schema and template drift apart.",
                "severity": "medium",
                "mitigation": "SoT-drift guard test recomposes from ID_PATTERNS.",
            },
        ],
        "success_criteria": [
            "All generate tool-write tests pass.",
            "Phantom ids are rejected before any markdown is written.",
            "Rendered roadmap satisfies GENERATE_A_GATE.",
        ],
        "decision_summary": (
            "Adopt the tool-write JSON substrate for the generate step. The LLM "
            "emits typed data; deterministic code renders the gate-bearing "
            "markdown and enforces the phantom-ID subset constraint."
        ),
        "timeline_estimates": [
            {"milestone": "M1", "start_week": "1", "end_week": "3", "duration": "3 weeks"},
            {"milestone": "M2", "start_week": "4", "end_week": "6", "duration": "3 weeks"},
            {"milestone": "M3", "start_week": "7", "end_week": "9", "duration": "3 weeks"},
        ],
        "roadmap_ids": ["FR-1", "FR-2", "FR-3", "FR-4", "FR-5"],
    }


def _merge_json() -> dict:
    """Schema-valid merge output; roadmap_ids span FR-1..FR-12 + entity families."""
    return {
        "frontmatter": {
            "spec_source": "spec.md",
            "generated": "2026-06-02T00:00:00Z",
            "generator": "merge",
            "complexity_score": 0.71,
            "complexity_class": "HIGH",
            "primary_persona": "architect",
            "adversarial": True,
            "base_variant": "A",
            "variant_scores": "A:81 B:74",
            "convergence_score": 0.88,
            "total_requirements": 12,
            "milestone_count": 4,
            "deliverable_count": 24,
        },
        "executive_summary": (
            "This merged roadmap combines the strongest elements of both adversarial "
            "variants, preserving every identifier from both while adopting variant A "
            "as the base and folding in variant B's hardening and observability rows. "
            "Each milestone carries its own deliverable table, integration points, "
            "milestone dependencies, and risk assessment so progress is independently "
            "verifiable against the spec."
        ),
        "milestone_summary": [
            {"milestone": "M1", "title": "Foundation", "duration": "weeks 1-3", "exit_criteria": "FR-1..FR-3 implemented."},
            {"milestone": "M2", "title": "Core Logic", "duration": "weeks 4-6", "exit_criteria": "FR-4..FR-6 implemented."},
            {"milestone": "M3", "title": "Integration", "duration": "weeks 7-9", "exit_criteria": "FR-7..FR-9 implemented."},
            {"milestone": "M4", "title": "Hardening and Production Readiness", "duration": "weeks 10-12", "exit_criteria": "FR-10..FR-12 implemented."},
        ],
        "dependency_graph": "M1 -> M2 -> M3 -> M4",
        "milestones": [
            _milestone(
                "M1",
                "Foundation",
                [
                    _deliverable(1, "FR-1", "Bootstrap the substrate"),
                    _deliverable(2, "FR-2", "Persist the sidecar"),
                    _deliverable(3, "FR-3", "Schema loader"),
                    _deliverable(4, "COMP-loader", "Loader component"),
                    _deliverable(5, "DM-config", "Config data model"),
                    _deliverable(6, "API-load", "Load API surface"),
                ],
                open_questions=[
                    {
                        "id": "OQ-1",
                        "question": "Should chunked mode auto-detect?",
                        "impact": "Throughput on large specs",
                        "owner": "TBD",
                        "target": "M1",
                    }
                ],
            ),
            _milestone(
                "M2",
                "Core Logic",
                [
                    _deliverable(7, "FR-4", "Render the artifact"),
                    _deliverable(8, "FR-5", "Wire the phantom-ID gate"),
                    _deliverable(9, "FR-6", "Validate completeness"),
                    _deliverable(10, "API-render", "Render API surface"),
                    _deliverable(11, "DM-roadmap", "Roadmap data model"),
                    _deliverable(12, "COMP-renderer", "Renderer component"),
                ],
            ),
            _milestone(
                "M3",
                "Integration",
                [
                    _deliverable(13, "FR-7", "Integrate the executor hook"),
                    _deliverable(14, "FR-8", "Dual-write wiring"),
                    _deliverable(15, "FR-9", "Sidecar derivation"),
                    _deliverable(16, "API-merge", "Merge API surface"),
                    _deliverable(17, "TEST-integration", "Integration tests"),
                    _deliverable(18, "MIG-cutover", "Cutover migration phase"),
                ],
            ),
            _milestone(
                "M4",
                "Hardening and Production Readiness",
                [
                    _deliverable(19, "FR-10", "Emit timeline estimates"),
                    _deliverable(20, "FR-11", "Risk register aggregation"),
                    _deliverable(21, "FR-12", "Decision summary"),
                    _deliverable(22, "OPS-metrics", "Metrics and alerting"),
                    _deliverable(23, "TEST-e2e", "End-to-end gate-parity tests"),
                    _deliverable(24, "NFR-1", "Performance budget instrumentation"),
                ],
            ),
        ],
        "resource_requirements": (
            "The merge step reuses the shared tool-write substrate; no new "
            "external services are introduced beyond the variants' union."
        ),
        "external_dependencies": "jsonschema, jinja2, and the UV toolchain.",
        "infrastructure_requirements": (
            "CI runner with UV and Python 3.10+; no additional runtime infra."
        ),
        "risk_register": [
            {
                "id": "R-1",
                "risk": "Phantom ids leak into the merged roadmap.",
                "affected_milestones": "M1, M2, M3, M4",
                "probability": "Low",
                "impact": "High",
                "mitigation": "validate_id_subset at generation time.",
                "owner": "architect",
            },
            {
                "id": "R-2",
                "risk": "Merge silently consolidates rows from the base variant.",
                "affected_milestones": "M2, M3",
                "probability": "Medium",
                "impact": "High",
                "mitigation": "Anti-consolidation rule + 20-row floor gate.",
                "owner": "qa",
            },
        ],
        "success_criteria": [
            "All merge tool-write tests pass.",
            "Phantom ids are rejected before any markdown is written.",
            "Rendered merged roadmap satisfies MERGE_GATE.",
        ],
        "decision_summary": (
            "Adopt variant A as the base and incorporate variant B's hardening and "
            "observability rows, as recommended by the score step and debate."
        ),
        "timeline_estimates": [
            {"milestone": "M1", "start_week": "1", "end_week": "3", "duration": "3 weeks"},
            {"milestone": "M2", "start_week": "4", "end_week": "6", "duration": "3 weeks"},
            {"milestone": "M3", "start_week": "7", "end_week": "9", "duration": "3 weeks"},
            {"milestone": "M4", "start_week": "10", "end_week": "12", "duration": "3 weeks"},
        ],
        "roadmap_ids": [
            "FR-1", "FR-2", "FR-3", "COMP-loader", "DM-config", "API-load",
            "FR-4", "FR-5", "FR-6", "API-render", "DM-roadmap", "COMP-renderer",
            "FR-7", "FR-8", "FR-9", "API-merge", "TEST-integration", "MIG-cutover",
            "FR-10", "FR-11", "FR-12", "OPS-metrics", "TEST-e2e", "NFR-1",
        ],
    }


def _write_registry(output_dir: Path, *, fr_ids, nfr_ids=(), accepted=()) -> Path:
    """Write a spec_id_registry.json whose union_of_known() == the given ids.

    Matches SpecIdRegistry.to_dict() key shape so the executor's
    SpecIdRegistry.from_payload(...) reconstructs it cleanly.
    """
    payload = {
        "fr_ids": list(fr_ids),
        "nfr_ids": list(nfr_ids),
        "sc_ids": [],
        "g_ids": [],
        "d_ids": [],
        "md_ids": [],
        "accepted_deviation_ids": list(accepted),
        "spec_hash": "0" * 16,
        "spec_path": str(output_dir / "spec.md"),
    }
    path = output_dir / "spec_id_registry.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def _make_roadmap_config(tmp_path: Path, **flags: object) -> RoadmapConfig:
    spec = tmp_path / "spec.md"
    spec.write_text("# Spec\n\n## FR-1\n## FR-2\n")
    output = tmp_path / "output"
    output.mkdir(exist_ok=True)
    return RoadmapConfig(
        spec_file=spec,
        output_dir=output,
        agents=[AgentSpec("opus", "architect")],
        depth="standard",
        **flags,
    )


def _make_step(output_dir: Path, step_id: str) -> Step:
    return Step(
        id=step_id,
        prompt="emit tool-write JSON",
        output_file=output_dir / f"{step_id}.md",
        gate=None,
        timeout_seconds=60,
        inputs=[],
    )


def _patched_proc_writing(step: Step, json_text: str):
    """Patch executor.ClaudeProcess so the render-dispatch branch is reached
    deterministically with ``json_text`` already on step.output_file.

    The render branch sits AFTER proc.start()/proc.wait(); the mock skips the
    poll loop (``_process is None``) and returns exit code 0. The phantom JSON
    is written to step.output_file BEFORE the executor reads it (the real
    ClaudeProcess would have produced it; a MagicMock does not).
    """
    step.output_file.parent.mkdir(parents=True, exist_ok=True)
    step.output_file.write_text(json_text, encoding="utf-8")
    instance = MagicMock()
    instance._process = None
    instance.wait.return_value = 0
    instance.start.return_value = None
    return patch(
        "superclaude.cli.roadmap.executor.ClaudeProcess", return_value=instance
    )


# ---------------------------------------------------------------------------
# (a) renderer-level: generate phantom FR-99 -> rejected, no artifact written
# ---------------------------------------------------------------------------


def test_renderer_generate_rejects_phantom_id(tmp_path) -> None:
    """(a) render_step_tool_write_with_id_check rejects a phantom roadmap_id at
    generation: errors mention FR-99 and NEITHER .md NOR .json sidecar is written."""
    out = tmp_path / "generate.md"
    phantom = _generate_json()
    phantom["roadmap_ids"] = phantom["roadmap_ids"] + ["FR-99"]
    errors = render_step_tool_write_with_id_check(
        "generate",
        json.dumps(phantom),
        out,
        spec_ids={"FR-1", "FR-2", "FR-3", "FR-4", "FR-5"},
    )
    assert errors, "phantom FR-99 must produce a non-empty error list"
    assert any("FR-99" in e for e in errors)
    assert any("not in spec_ids" in e for e in errors)
    assert not out.exists(), "no .md may be written when a phantom id is present"
    assert not (tmp_path / "generate.json").exists(), "no JSON sidecar either"


# ---------------------------------------------------------------------------
# (d) renderer-level: require_spec_ids=True + empty spec_ids -> hard error
# ---------------------------------------------------------------------------


def test_renderer_require_spec_ids_errors_on_empty_universe(tmp_path) -> None:
    """(d) require_spec_ids=True with an empty spec_ids universe is a HARD error
    (not the legacy identity skip); no artifact is written."""
    out = tmp_path / "generate.md"
    errors = render_step_tool_write_with_id_check(
        "generate",
        json.dumps(_generate_json()),
        out,
        spec_ids=set(),
        require_spec_ids=True,
    )
    assert errors == ["require_spec_ids=True but spec_ids universe is empty"]
    assert not out.exists()
    assert not (tmp_path / "generate.json").exists()


def test_renderer_require_spec_ids_false_preserves_identity_skip(tmp_path) -> None:
    """PRESERVE control: require_spec_ids=False (default) keeps the legacy
    identity skip on empty spec_ids -> renders normally (extract-like callers)."""
    out = tmp_path / "generate.md"
    errors = render_step_tool_write_with_id_check(
        "generate",
        json.dumps(_generate_json()),
        out,
        spec_ids=set(),
    )
    assert errors == []
    assert out.exists()
    assert (tmp_path / "generate.json").exists()


# ---------------------------------------------------------------------------
# (b) executor-level: generate/merge source spec_ids from spec_id_registry.json
#     (NOT extraction.json) and FAIL on a phantom id -- no artifact persisted.
# ---------------------------------------------------------------------------


def test_executor_generate_rejects_phantom_via_registry(tmp_path) -> None:
    """(b) The executor's generate render branch sources spec_ids from the
    always-written spec_id_registry.json (NO extraction.json present) and FAILS
    the step on a phantom FR-99 -- the regression for the gap where spec_ids came
    from an empty extraction.json and the subset check silently skipped."""
    config = _make_roadmap_config(tmp_path, tool_write_generate=True)
    out_dir = config.output_dir
    _write_registry(out_dir, fr_ids=["FR-1", "FR-2", "FR-3", "FR-4", "FR-5"])
    assert not (out_dir / "extraction.json").exists()

    phantom = _generate_json()
    phantom["roadmap_ids"] = phantom["roadmap_ids"] + ["FR-99"]
    step = _make_step(out_dir, "generate-opus-architect")

    with _patched_proc_writing(step, json.dumps(phantom)):
        result = roadmap_run_step(step, config, cancel_check=lambda: False)

    assert result.status == StepStatus.FAIL
    assert "FR-99" in (result.gate_failure_reason or "")
    assert "not in spec_ids" in (result.gate_failure_reason or "")
    # The render path did NOT overwrite output_file with rendered markdown
    # (still the raw JSON) and did NOT write the JSON sidecar.
    assert step.output_file.read_text(encoding="utf-8").lstrip().startswith("{")
    assert not step.output_file.with_suffix(".json").exists()


def test_executor_merge_rejects_phantom_via_registry(tmp_path) -> None:
    """(b, merge) The merge render branch -- the SECOND primary phantom-ID source
    -- shares the identical registry-sourced path and FAILS on a phantom FR-99."""
    config = _make_roadmap_config(tmp_path, tool_write_merge=True)
    out_dir = config.output_dir
    # Cover every clean merge roadmap_id: FR-family in fr_ids, NFR-1 in nfr_ids,
    # entity ids (COMP-/DM-/API-/TEST-/MIG-/OPS-) in accepted_deviation_ids so the
    # only violation is the injected phantom.
    _write_registry(
        out_dir,
        fr_ids=[f"FR-{n}" for n in range(1, 13)],
        nfr_ids=["NFR-1"],
        accepted=[
            "COMP-loader", "DM-config", "API-load", "API-render", "DM-roadmap",
            "COMP-renderer", "API-merge", "TEST-integration", "MIG-cutover",
            "OPS-metrics", "TEST-e2e",
        ],
    )
    phantom = _merge_json()
    phantom["roadmap_ids"] = phantom["roadmap_ids"] + ["FR-99"]
    step = _make_step(out_dir, "merge")

    with _patched_proc_writing(step, json.dumps(phantom)):
        result = roadmap_run_step(step, config, cancel_check=lambda: False)

    assert result.status == StepStatus.FAIL
    assert "FR-99" in (result.gate_failure_reason or "")
    assert not step.output_file.with_suffix(".json").exists()


# ---------------------------------------------------------------------------
# (c) executor-level fail-shut: MISSING spec_id_registry.json -> StepResult FAIL
# ---------------------------------------------------------------------------


def test_executor_generate_fail_shut_on_missing_registry(tmp_path) -> None:
    """(c) generate FAILS SHUT when spec_id_registry.json is absent -- it must NOT
    silently emit an unconstrained roadmap."""
    config = _make_roadmap_config(tmp_path, tool_write_generate=True)
    out_dir = config.output_dir
    assert not (out_dir / "spec_id_registry.json").exists()  # the fail-shut trigger

    step = _make_step(out_dir, "generate-opus-architect")
    with _patched_proc_writing(step, json.dumps(_generate_json())):
        result = roadmap_run_step(step, config, cancel_check=lambda: False)

    assert result.status == StepStatus.FAIL
    assert "spec_id_registry.json" in (result.gate_failure_reason or "")
    assert "fail-shut" in (result.gate_failure_reason or "")
    assert not step.output_file.with_suffix(".json").exists()


def test_executor_merge_fail_shut_on_missing_registry(tmp_path) -> None:
    """(c, merge) merge FAILS SHUT on a missing registry, same as generate."""
    config = _make_roadmap_config(tmp_path, tool_write_merge=True)
    out_dir = config.output_dir
    assert not (out_dir / "spec_id_registry.json").exists()

    step = _make_step(out_dir, "merge")
    with _patched_proc_writing(step, json.dumps(_merge_json())):
        result = roadmap_run_step(step, config, cancel_check=lambda: False)

    assert result.status == StepStatus.FAIL
    assert "spec_id_registry.json" in (result.gate_failure_reason or "")
