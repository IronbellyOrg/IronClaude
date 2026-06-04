"""Tests for the R1.4 diff-step tool-write migration (Step 9.5).

Mirrors ``test_tool_write_step_extract.py`` for the diff step. The diff step is
SIMPLE: it compares two roadmap variants and surfaces divergence points, shared
assumptions, relative strengths, and debate areas. Unlike generate/merge it
carries NO ``roadmap_ids`` and therefore has NO §MVR §3 / Contract #3 phantom-ID
subset constraint -- the executor routes it through the PLAIN
``render_step_tool_write`` (not the id-check variant).

These tests exercise the full tool-write loop for the diff step:

* schema loads and exposes the required keys;
* a well-formed structured fixture passes schema validation and renders to
  markdown that satisfies DIFF_GATE (frontmatter fields + min_lines);
* malformed/invalid output is rejected without writing any artifact;
* the registry entry is distinct (its own config_flag);
* ``build_diff_prompt(..., tool_write=True)`` swaps the output contract to JSON
  while the default markdown path is unchanged (dual-write proof).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import DIFF_GATE
from superclaude.cli.roadmap.prompts import build_diff_prompt
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_tool_output,
)


@pytest.fixture
def diff_fixture() -> dict:
    """A representative, schema-valid diff structured output (renders >=30 lines)."""
    return {
        "frontmatter": {
            "total_diff_points": 3,
            "shared_assumptions_count": 2,
            "generated": "2026-06-02T00:00:00Z",
            "generator": "diff-agent",
            "variant_a": "roadmap-opus-architect.md",
            "variant_b": "roadmap-sonnet-backend.md",
        },
        "shared_assumptions": [
            "Both variants assume a UV-only Python toolchain.",
            "Both variants phase the work Foundation -> Core -> Hardening.",
        ],
        "divergence_points": [
            {
                "n": 1,
                "description": "Milestone granularity differs between variants.",
                "variant_a_position": "Variant A uses 5 coarse milestones.",
                "variant_b_position": "Variant B uses 9 fine-grained milestones.",
                "impact": "Finer granularity improves tracking but adds overhead.",
            },
            {
                "n": 2,
                "description": "Risk-register placement differs.",
                "variant_a_position": "Variant A consolidates risks globally.",
                "variant_b_position": "Variant B attaches risks per-milestone.",
                "impact": "Per-milestone risks localize mitigation ownership.",
            },
            {
                "description": "Testing strategy emphasis differs.",
                "variant_a_position": "Variant A front-loads integration tests.",
                "variant_b_position": "Variant B front-loads unit tests.",
                "impact": "Earlier integration tests catch wiring defects sooner.",
            },
        ],
        "stronger_areas": [
            "Variant A is stronger on cross-cutting risk visibility.",
            {
                "area": "Deliverable traceability",
                "variant": "B",
                "rationale": "Per-milestone risks map cleanly to deliverables.",
            },
        ],
        "debate_areas": [
            "Optimal milestone granularity for this complexity class.",
            "Whether risks belong globally or per-milestone.",
        ],
    }


def test_diff_schema_loads() -> None:
    schema = load_schema("diff.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "divergence_points"} <= required
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {"total_diff_points", "shared_assumptions_count"} <= fm_required


def test_valid_output_passes_schema(diff_fixture: dict) -> None:
    schema = load_schema("diff.schema.json")
    assert validate_tool_output(diff_fixture, schema) == []


def test_missing_divergence_points_fails(diff_fixture: dict) -> None:
    schema = load_schema("diff.schema.json")
    bad = json.loads(json.dumps(diff_fixture))
    del bad["divergence_points"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required divergence_points should fail schema validation"


def test_wrong_type_fails(diff_fixture: dict) -> None:
    schema = load_schema("diff.schema.json")
    bad = json.loads(json.dumps(diff_fixture))
    # total_diff_points must be an integer; a string is a violation.
    bad["frontmatter"]["total_diff_points"] = "three"
    errors = validate_tool_output(bad, schema)
    assert errors, "wrong type for a count field should fail schema validation"


def test_divergence_point_requires_description(diff_fixture: dict) -> None:
    schema = load_schema("diff.schema.json")
    bad = json.loads(json.dumps(diff_fixture))
    del bad["divergence_points"][0]["description"]
    errors = validate_tool_output(bad, schema)
    assert errors, "divergence point missing required description should fail"


def test_render_parity(diff_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path."""
    rendered = render_tool_output(diff_fixture, TEMPLATES_DIR / "diff.md.j2")
    assert rendered.startswith("---")
    assert "total_diff_points:" in rendered
    assert "shared_assumptions_count:" in rendered
    # Numbered divergence list present.
    assert "1. " in rendered
    for dp in diff_fixture["divergence_points"]:
        assert dp["description"] in rendered, f"missing divergence: {dp['description']}"
    assert rendered.count("\n") >= 30, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 30"
    )


def test_rendered_diff_satisfies_gate_frontmatter(diff_fixture: dict) -> None:
    """The rendered tool-write output must PASS DIFF_GATE.

    Asserts every required frontmatter field appears as a ``key:`` line in the
    render and the render meets the gate's ``min_lines`` floor (>=30 newlines).
    """
    rendered = render_tool_output(diff_fixture, TEMPLATES_DIR / "diff.md.j2")
    for field in DIFF_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= DIFF_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {DIFF_GATE.min_lines}"
    )


def test_render_step_tool_write_roundtrip(diff_fixture: dict, tmp_path) -> None:
    out = tmp_path / "diff-analysis.md"
    errors = render_step_tool_write("diff", json.dumps(diff_fixture), out)
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "diff-analysis.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == diff_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "diff-analysis.md"
    errors = render_step_tool_write("diff", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "diff-analysis.json").exists()


def test_diff_registry_key_distinct() -> None:
    """The diff registry entry must have its own config_flag and step_id."""
    assert TOOL_WRITE_REGISTRY["diff"].config_flag == "tool_write_diff"
    assert TOOL_WRITE_REGISTRY["diff"].step_id == "diff"
    assert TOOL_WRITE_REGISTRY["diff"].schema_name == "diff.schema.json"
    assert TOOL_WRITE_REGISTRY["diff"].template_name == "diff.md.j2"


def test_build_diff_prompt_tool_write_emits_json_contract() -> None:
    tw = build_diff_prompt(Path("a.md"), Path("b.md"), tool_write=True)
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in (
        "shared_assumptions",
        "divergence_points",
        "stronger_areas",
        "debate_areas",
    ):
        assert key in tw, f"tool-write prompt missing diff key: {key}"

    md = build_diff_prompt(Path("a.md"), Path("b.md"))
    assert "<output_format>" in md
