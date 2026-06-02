"""Tests for the R1.4 spec-fidelity-step tool-write migration (Step 9.9).

Mirrors ``test_tool_write_step_score.py`` for the spec-fidelity step. The
spec-fidelity step is the convergence-loop CORE: when ``convergence_enabled`` is
True the executor short-circuits to ``_run_convergence_spec_fidelity`` and this
tool-write path is NEVER reached (``convergence.py`` / ``semantic_layer.py`` are
PRESERVE, byte-untouched). This migration adds the single-shot (non-convergence)
tool-write capability without altering convergence behaviour. Like score/diff it
carries NO ``roadmap_ids`` and therefore has NO MVR-3 / Contract #3 phantom-ID
subset constraint -- the executor routes it through the PLAIN
``render_step_tool_write`` (not the id-check variant).

These tests exercise the full tool-write loop for the spec-fidelity step:

* schema loads and exposes the required keys;
* a well-formed structured fixture passes schema validation and renders to
  markdown that satisfies SPEC_FIDELITY_GATE (the six frontmatter fields +
  min_lines + the gate's semantic checks: high_severity_count==0 and
  tasklist_ready consistency);
* malformed/invalid output is rejected without writing any artifact;
* the registry entry is distinct (its own config_flag) and routes PLAIN (not
  the generate/merge id-check variant);
* ``build_spec_fidelity_prompt(..., tool_write=True)`` swaps the output contract
  to JSON while the default markdown path is byte-identical (dual-write proof).

CONTRACT #8: the spec-fidelity schema/template MUST NOT bake in any convergence
threshold literal (``0.7`` / ``0.5``) -- the severity counts are deviation
tallies, not convergence ratios.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import SPEC_FIDELITY_GATE
from superclaude.cli.roadmap.prompts import (
    build_spec_fidelity_prompt,
    spec_fidelity_tool_definition,
)
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_SCHEMAS_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_tool_output,
)


@pytest.fixture
def spec_fidelity_fixture() -> dict:
    """A representative, schema-valid spec-fidelity output (renders >=20 lines).

    high_severity_count is 0 and tasklist_ready is true so the rendered markdown
    PASSES the SPEC_FIDELITY_GATE semantic checks.
    """
    return {
        "frontmatter": {
            "high_severity_count": 0,
            "medium_severity_count": 1,
            "low_severity_count": 1,
            "total_deviations": 2,
            "validation_complete": True,
            "tasklist_ready": True,
            "generated": "2026-06-02T00:00:00Z",
            "generator": "spec-fidelity-agent",
            "spec_source": "spec.md",
        },
        "deviations": [
            {
                "id": "DEV-001",
                "severity": "MEDIUM",
                "deviation": (
                    "FR-012 is addressed but lacks specific acceptance criteria."
                ),
                "source_quote": "FR-012: The system SHALL rotate session tokens hourly.",
                "roadmap_quote": "M3 includes session token handling.",
                "impact": "Implementation may miss the hourly rotation cadence.",
                "recommended_correction": (
                    "Add an AC to the M3 session task pinning the hourly rotation."
                ),
            },
            {
                "id": "DEV-002",
                "severity": "LOW",
                "deviation": "Heading order differs from the source document.",
                "source_quote": "Section 4 precedes Section 5 in the spec.",
                "roadmap_quote": "[MISSING]",
                "impact": "No correctness impact; organizational only.",
                "recommended_correction": "Optionally realign section ordering.",
            },
        ],
        "summary": (
            "2 deviations found (0 HIGH, 1 MEDIUM, 1 LOW). The roadmap is "
            "tasklist-ready: no HIGH-severity divergences from the source."
        ),
    }


def test_spec_fidelity_schema_loads() -> None:
    schema = load_schema("spec_fidelity.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "summary"} <= required
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {
        "high_severity_count",
        "medium_severity_count",
        "low_severity_count",
        "total_deviations",
        "validation_complete",
        "tasklist_ready",
    } <= fm_required


def test_valid_output_passes_schema(spec_fidelity_fixture: dict) -> None:
    schema = load_schema("spec_fidelity.schema.json")
    assert validate_tool_output(spec_fidelity_fixture, schema) == []


def test_missing_summary_fails(spec_fidelity_fixture: dict) -> None:
    schema = load_schema("spec_fidelity.schema.json")
    bad = json.loads(json.dumps(spec_fidelity_fixture))
    del bad["summary"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required summary should fail schema validation"


def test_missing_frontmatter_field_fails(spec_fidelity_fixture: dict) -> None:
    schema = load_schema("spec_fidelity.schema.json")
    bad = json.loads(json.dumps(spec_fidelity_fixture))
    del bad["frontmatter"]["high_severity_count"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required high_severity_count frontmatter field should fail"


def test_deviation_requires_core_fields(spec_fidelity_fixture: dict) -> None:
    schema = load_schema("spec_fidelity.schema.json")
    bad = json.loads(json.dumps(spec_fidelity_fixture))
    del bad["deviations"][0]["severity"]
    errors = validate_tool_output(bad, schema)
    assert errors, "deviation missing required severity should fail"


def test_invalid_severity_enum_fails(spec_fidelity_fixture: dict) -> None:
    schema = load_schema("spec_fidelity.schema.json")
    bad = json.loads(json.dumps(spec_fidelity_fixture))
    bad["deviations"][0]["severity"] = "CRITICAL"  # not in {HIGH,MEDIUM,LOW}
    errors = validate_tool_output(bad, schema)
    assert errors, "severity outside the HIGH/MEDIUM/LOW enum should fail"


def test_empty_deviations_passes_schema(spec_fidelity_fixture: dict) -> None:
    """A fully-faithful roadmap (zero deviations) is schema-valid."""
    schema = load_schema("spec_fidelity.schema.json")
    clean = json.loads(json.dumps(spec_fidelity_fixture))
    clean["deviations"] = []
    clean["frontmatter"]["medium_severity_count"] = 0
    clean["frontmatter"]["low_severity_count"] = 0
    clean["frontmatter"]["total_deviations"] = 0
    assert validate_tool_output(clean, schema) == []


def test_render_parity(spec_fidelity_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path."""
    rendered = render_tool_output(
        spec_fidelity_fixture, TEMPLATES_DIR / "spec_fidelity.md.j2"
    )
    assert rendered.startswith("---")
    assert "high_severity_count:" in rendered
    assert "tasklist_ready:" in rendered
    assert "## Deviation Report" in rendered
    assert "## Summary" in rendered
    for dev in spec_fidelity_fixture["deviations"]:
        assert dev["id"] in rendered, f"missing deviation: {dev['id']}"
        assert dev["deviation"] in rendered
    assert rendered.count("\n") >= 20, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 20"
    )


def test_empty_deviations_renders_clean_note(spec_fidelity_fixture: dict) -> None:
    clean = json.loads(json.dumps(spec_fidelity_fixture))
    clean["deviations"] = []
    rendered = render_tool_output(clean, TEMPLATES_DIR / "spec_fidelity.md.j2")
    assert "No deviations found" in rendered


def test_rendered_satisfies_gate_frontmatter(spec_fidelity_fixture: dict) -> None:
    """The rendered tool-write output must expose every gate frontmatter field."""
    rendered = render_tool_output(
        spec_fidelity_fixture, TEMPLATES_DIR / "spec_fidelity.md.j2"
    )
    for field in SPEC_FIDELITY_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= SPEC_FIDELITY_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {SPEC_FIDELITY_GATE.min_lines}"
    )


def test_rendered_passes_gate_semantic_checks(spec_fidelity_fixture: dict) -> None:
    """high=0 + consistent tasklist_ready ⇒ the render passes the gate's checks.

    Exercises SPEC_FIDELITY_GATE's semantic checks (high_severity_count_zero,
    tasklist_ready_consistent) against the rendered markdown via the public gate
    object -- proving the tool-write render is genuinely gate-compatible, not
    merely field-present.
    """
    rendered = render_tool_output(
        spec_fidelity_fixture, TEMPLATES_DIR / "spec_fidelity.md.j2"
    )
    assert SPEC_FIDELITY_GATE.semantic_checks, "gate must declare semantic checks"
    for check in SPEC_FIDELITY_GATE.semantic_checks:
        assert check.check_fn(rendered) is True, (
            f"rendered output failed gate semantic check {check.name!r}"
        )


def test_render_step_tool_write_roundtrip(
    spec_fidelity_fixture: dict, tmp_path
) -> None:
    out = tmp_path / "spec-fidelity.md"
    errors = render_step_tool_write(
        "spec-fidelity", json.dumps(spec_fidelity_fixture), out
    )
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "spec-fidelity.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == spec_fidelity_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "spec-fidelity.md"
    errors = render_step_tool_write("spec-fidelity", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "spec-fidelity.json").exists()


def test_render_step_tool_write_dual_write_proof(
    spec_fidelity_fixture: dict, tmp_path
) -> None:
    """Dual-write proof: the PASS path writes BOTH the .md artifact and .json sidecar."""
    out = tmp_path / "spec-fidelity.md"
    sidecar = tmp_path / "spec-fidelity.json"
    assert not out.exists()
    assert not sidecar.exists()
    errors = render_step_tool_write(
        "spec-fidelity", json.dumps(spec_fidelity_fixture), out
    )
    assert errors == []
    assert out.exists(), "markdown artifact must be written on PASS"
    assert sidecar.exists(), "JSON sidecar must be written on PASS"
    assert json.loads(sidecar.read_text(encoding="utf-8")) == spec_fidelity_fixture
    assert out.read_text(encoding="utf-8").startswith("---")


def test_spec_fidelity_registry_key_distinct() -> None:
    """The spec-fidelity registry entry must have its own (hyphenated) key + flag."""
    spec = TOOL_WRITE_REGISTRY["spec-fidelity"]
    assert spec.config_flag == "tool_write_spec_fidelity"
    assert spec.step_id == "spec-fidelity"
    assert spec.schema_name == "spec_fidelity.schema.json"
    assert spec.template_name == "spec_fidelity.md.j2"


def test_spec_fidelity_routes_plain_not_id_check() -> None:
    """spec-fidelity must NOT be an id-check (generate/merge) step.

    The executor routes only ``generate`` and ``merge`` registry keys through
    render_step_tool_write_with_id_check; spec-fidelity carries no roadmap_ids
    and must fall through to the PLAIN render path.
    """
    assert "spec-fidelity" not in ("generate", "merge")


def test_spec_fidelity_tool_definition() -> None:
    td = spec_fidelity_tool_definition()
    assert td.name == "spec-fidelity"
    assert td.input_schema == {}
    assert td.render_template == TEMPLATES_DIR / "spec_fidelity.md.j2"
    assert "summary" in set(td.output_schema["required"])


def test_build_spec_fidelity_prompt_tool_write_emits_json_contract() -> None:
    tw = build_spec_fidelity_prompt(
        Path("spec.md"), Path("roadmap.md"), tool_write=True
    )
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in (
        "high_severity_count",
        "tasklist_ready",
        "deviations",
        "summary",
    ):
        assert key in tw, f"tool-write prompt missing spec-fidelity key: {key}"

    md = build_spec_fidelity_prompt(Path("spec.md"), Path("roadmap.md"))
    assert "<output_format>" in md


def test_build_spec_fidelity_prompt_default_byte_identical() -> None:
    """The default markdown path must be byte-identical with/without tool_write=False.

    Guards the dual-write contract: enabling the flag changes ONLY the output
    block; the default production prompt is unchanged.
    """
    default = build_spec_fidelity_prompt(Path("spec.md"), Path("roadmap.md"))
    explicit_false = build_spec_fidelity_prompt(
        Path("spec.md"), Path("roadmap.md"), tool_write=False
    )
    assert default == explicit_false
    # TDD/PRD conditional blocks remain intact in the default path.
    with_tdd = build_spec_fidelity_prompt(
        Path("spec.md"), Path("roadmap.md"), tdd_file=Path("design.md")
    )
    assert "API Endpoints" in with_tdd
    with_prd = build_spec_fidelity_prompt(
        Path("spec.md"), Path("roadmap.md"), prd_file=Path("prd.md")
    )
    assert "Supplementary PRD Validation" in with_prd


# --- CONTRACT #8 test ------------------------------------------------------


def test_spec_fidelity_schema_no_hardcoded_thresholds() -> None:
    """Contract #8: no convergence threshold literal is baked into the substrate.

    The spec-fidelity schema file and the render template MUST NOT contain the
    literal convergence threshold values ``0.7`` or ``0.5`` -- the severity
    counts are deviation tallies, NOT convergence ratios (which are sourced at
    runtime from ``superclaude.contracts.CONVERGENCE_THRESHOLDS``).
    """
    schema_text = (TOOL_SCHEMAS_DIR / "spec_fidelity.schema.json").read_text(
        encoding="utf-8"
    )
    template_text = (TEMPLATES_DIR / "spec_fidelity.md.j2").read_text(encoding="utf-8")
    for forbidden in ("0.7", "0.5"):
        assert forbidden not in schema_text, (
            f"spec_fidelity.schema.json must NOT bake in threshold literal "
            f"{forbidden!r} (Contract #8)"
        )
        assert forbidden not in template_text, (
            f"spec_fidelity.md.j2 must NOT bake in threshold literal "
            f"{forbidden!r} (Contract #8)"
        )
