"""Tests for the R1.4 validate-reflect tool-write migration (Step 9.11, SECONDARY).

Mirrors ``test_tool_write_step_score.py`` for the validate reflect step. The
reflect step is a SECONDARY validate-subsystem LLM step: it validates the roadmap
across 7 (or 9 with original inputs) dimensions and classifies every finding
BLOCKING/WARNING/INFO. It carries NO ``roadmap_ids`` and therefore has NO §MVR §3
/ Contract #3 phantom-ID subset constraint -- it renders through the PLAIN
``render_step_tool_write`` (not the id-check variant).

Execution-path note: the reflect step runs under the validate sub-executor
(``validate_run_step``), NOT ``roadmap_run_step``; the tool-write render hook
lives in ``validate_run_step`` and reads ``ValidateConfig.tool_write_validate_reflect``.
``test_validate_*.py`` are the unchanged-guarantee witnesses for the legacy path.
"""

from __future__ import annotations

import json

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_tool_output,
)
from superclaude.cli.roadmap.validate_gates import REFLECT_GATE
from superclaude.cli.roadmap.validate_prompts import (
    build_reflect_prompt,
)
from superclaude.cli.roadmap.validate_prompts import (
    reflect_tool_definition as _reflect_tool_definition,
)


@pytest.fixture
def reflect_fixture() -> dict:
    """A representative, schema-valid reflect output (tasklist_ready, renders >=20 lines)."""
    return {
        "frontmatter": {
            "blocking_issues_count": 0,
            "warnings_count": 2,
            "tasklist_ready": True,
            "generated": "2026-06-02T00:00:00Z",
            "generator": "reflect-agent",
        },
        "findings": [
            {
                "severity": "WARNING",
                "dimension": "Interleave",
                "description": "Test activities are mildly back-loaded.",
                "location": "roadmap.md:section M5",
                "evidence": "interleave_ratio 0.35; tests cluster in M5-M6.",
                "fix_guidance": "Pull one integration-test milestone earlier.",
            },
            {
                "severity": "WARNING",
                "dimension": "Decomposition",
                "description": "One compound deliverable joins two outputs with 'and'.",
                "location": "roadmap.md:M3 row 4",
                "evidence": "'Build parser and wire dispatch' is two outputs.",
                "fix_guidance": "Split into two deliverable rows.",
            },
            {
                "severity": "INFO",
                "dimension": "Structure",
                "description": "Heading hierarchy is valid throughout.",
                "location": "roadmap.md",
                "evidence": "H2 > H3 > H4 with no gaps.",
                "fix_guidance": "None required.",
            },
        ],
        "summary": (
            "0 blocking, 2 warning, 1 info. The roadmap is ready for tasklist "
            "generation; the two warnings are advisory."
        ),
        "interleave_ratio": (
            "interleave_ratio = 4 milestones_with_deliverables / 6 total = 0.67 "
            "(within [0.1, 1.0])."
        ),
    }


def test_reflect_schema_loads() -> None:
    schema = load_schema("reflect.schema.json")
    assert isinstance(schema, dict)
    assert "frontmatter" in set(schema["required"])
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {"blocking_issues_count", "warnings_count", "tasklist_ready"} <= fm_required


def test_valid_output_passes_schema(reflect_fixture: dict) -> None:
    schema = load_schema("reflect.schema.json")
    assert validate_tool_output(reflect_fixture, schema) == []


def test_missing_frontmatter_field_fails(reflect_fixture: dict) -> None:
    schema = load_schema("reflect.schema.json")
    bad = json.loads(json.dumps(reflect_fixture))
    del bad["frontmatter"]["tasklist_ready"]
    assert validate_tool_output(bad, schema), "missing tasklist_ready should fail"


def test_invalid_severity_enum_fails(reflect_fixture: dict) -> None:
    schema = load_schema("reflect.schema.json")
    bad = json.loads(json.dumps(reflect_fixture))
    bad["findings"][0]["severity"] = "FATAL"
    assert validate_tool_output(bad, schema), "severity outside enum should fail"


def test_render_parity(reflect_fixture: dict) -> None:
    rendered = render_tool_output(reflect_fixture, TEMPLATES_DIR / "reflect.md.j2")
    assert rendered.startswith("---")
    assert "blocking_issues_count: 0" in rendered
    assert "warnings_count: 2" in rendered
    assert "tasklist_ready: true" in rendered
    assert "## Findings" in rendered
    assert "## Summary" in rendered
    assert "## Interleave Ratio" in rendered
    assert "[WARNING]" in rendered
    assert rendered.count("\n") >= 20


def test_rendered_satisfies_reflect_gate(reflect_fixture: dict, tmp_path) -> None:
    """The rendered tool-write output must PASS REFLECT_GATE."""
    out = tmp_path / "validation-report.md"
    out.write_text(
        render_tool_output(reflect_fixture, TEMPLATES_DIR / "reflect.md.j2"),
        encoding="utf-8",
    )
    passed, reason = gate_passed(out, REFLECT_GATE)
    assert passed, f"rendered reflect report failed REFLECT_GATE: {reason}"


def test_render_step_tool_write_roundtrip(reflect_fixture: dict, tmp_path) -> None:
    out = tmp_path / "validation-report.md"
    errors = render_step_tool_write("reflect", json.dumps(reflect_fixture), out)
    assert errors == []
    assert out.exists()
    assert out.read_text(encoding="utf-8").startswith("---")
    sidecar = tmp_path / "validation-report.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == reflect_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "validation-report.md"
    errors = render_step_tool_write("reflect", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "validation-report.json").exists()


def test_reflect_registry_key_distinct() -> None:
    spec = TOOL_WRITE_REGISTRY["reflect"]
    assert spec.config_flag == "tool_write_validate_reflect"
    assert spec.step_id == "reflect"
    assert spec.schema_name == "reflect.schema.json"
    assert spec.template_name == "reflect.md.j2"


def test_reflect_tool_definition() -> None:
    td = _reflect_tool_definition()
    assert td.name == "reflect"
    assert td.input_schema == {}
    assert td.render_template == TEMPLATES_DIR / "reflect.md.j2"
    assert "frontmatter" in set(td.output_schema["required"])


def test_build_prompt_tool_write_emits_json_contract() -> None:
    tw = build_reflect_prompt(
        "roadmap.md", "test-strategy.md", "extraction.md", tool_write=True
    )
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in ("frontmatter", "findings", "summary", "interleave_ratio"):
        assert key in tw, f"tool-write prompt missing reflect key: {key}"

    md = build_reflect_prompt("roadmap.md", "test-strategy.md", "extraction.md")
    assert "<output_format>" in md


def test_build_prompt_default_byte_identical() -> None:
    """The default markdown path must be byte-identical with/without tool_write=False."""
    default = build_reflect_prompt("roadmap.md", "test-strategy.md", "extraction.md")
    explicit_false = build_reflect_prompt(
        "roadmap.md", "test-strategy.md", "extraction.md", tool_write=False
    )
    assert default == explicit_false
    # The 9-dimension (input-aware) conditional still fires on the default path.
    with_spec = build_reflect_prompt(
        "roadmap.md", "test-strategy.md", "extraction.md", spec_file="spec.md"
    )
    assert "Coverage" in with_spec
    assert "Proportionality" in with_spec
