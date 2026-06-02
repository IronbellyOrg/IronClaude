"""Tests for the R1.4 debate-step tool-write migration (Step 9.6).

The debate step is part of the PRESERVED adversarial-debate mechanism: the
tool-write rewrite changes ONLY the prompt/output contract (markdown ->
structured JSON rendered deterministically). ``semantic_layer.py`` MUST stay
byte-untouched. Like the diff step, debate carries NO ``roadmap_ids`` and
therefore has NO §MVR §3 / Contract #3 phantom-ID subset constraint -- the
executor routes it through the PLAIN ``render_step_tool_write`` (not the
id-check variant).

These tests exercise the full tool-write loop for the debate step:

* schema loads and exposes the required keys;
* a well-formed structured fixture passes schema validation and renders to
  markdown that satisfies DEBATE_GATE (frontmatter fields + min_lines) AND the
  convergence_score_valid semantic check;
* malformed/invalid output is rejected without writing any artifact;
* the registry entry is distinct (its own config_flag);
* ``build_debate_prompt(..., tool_write=True)`` swaps the output contract to
  JSON while the default markdown path is unchanged (dual-write proof);
* the PRESERVED ``semantic_layer.py`` module remains importable and exposes
  ``run_semantic_layer``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import DEBATE_GATE, _convergence_score_valid
from superclaude.cli.roadmap.prompts import build_debate_prompt
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_tool_output,
)


@pytest.fixture
def debate_fixture() -> dict:
    """A representative, schema-valid debate structured output (>=2 rounds)."""
    return {
        "frontmatter": {
            "convergence_score": 0.72,
            "rounds_completed": 3,
            "generated": "2026-06-02T00:00:00Z",
            "generator": "debate-agent",
            "variant_a": "roadmap-opus-architect.md",
            "variant_b": "roadmap-sonnet-backend.md",
        },
        "rounds": [
            {
                "round": 1,
                "variant_a_position": (
                    "Variant A argues for 5 coarse milestones to reduce "
                    "tracking overhead and keep the roadmap legible."
                ),
                "variant_b_position": (
                    "Variant B argues for 9 fine-grained milestones so progress "
                    "is measurable at weekly cadence."
                ),
                "exchange": (
                    "A concedes B's point on measurability but counters that "
                    "fine granularity multiplies coordination cost."
                ),
            },
            {
                "round": 2,
                "variant_a_position": (
                    "Variant A prefers a single consolidated risk register for "
                    "cross-cutting visibility."
                ),
                "variant_b_position": (
                    "Variant B prefers per-milestone risk attachment so "
                    "mitigation ownership is local."
                ),
                "exchange": (
                    "Both agree a hybrid -- global register with per-milestone "
                    "annotations -- captures most of the value."
                ),
            },
            {
                "round": 3,
                "variant_a_position": (
                    "Variant A front-loads integration tests to catch wiring "
                    "defects early."
                ),
                "variant_b_position": (
                    "Variant B front-loads unit tests for fast feedback loops."
                ),
            },
        ],
        "convergence_assessment": {
            "agreements": [
                "A hybrid risk model (global register + per-milestone notes) "
                "is acceptable to both variants.",
                "Both agree the toolchain is UV-only Python.",
            ],
            "remaining_disputes": [
                "Optimal milestone granularity for this complexity class.",
                "Whether integration or unit tests should be front-loaded.",
            ],
            "summary": (
                "Substantial convergence on risk handling and toolchain; "
                "granularity and test sequencing remain open."
            ),
        },
    }


def test_debate_schema_loads() -> None:
    schema = load_schema("debate.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "rounds", "convergence_assessment"} <= required
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {"convergence_score", "rounds_completed"} <= fm_required


def test_valid_output_passes_schema(debate_fixture: dict) -> None:
    schema = load_schema("debate.schema.json")
    assert validate_tool_output(debate_fixture, schema) == []


def test_convergence_score_out_of_range_fails(debate_fixture: dict) -> None:
    schema = load_schema("debate.schema.json")
    bad = json.loads(json.dumps(debate_fixture))
    # convergence_score has maximum 1; 1.5 must violate the schema.
    bad["frontmatter"]["convergence_score"] = 1.5
    errors = validate_tool_output(bad, schema)
    assert errors, "convergence_score 1.5 should fail schema (maximum 1)"


def test_missing_rounds_fails(debate_fixture: dict) -> None:
    schema = load_schema("debate.schema.json")
    bad = json.loads(json.dumps(debate_fixture))
    del bad["rounds"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required rounds should fail schema validation"


def test_round_requires_both_positions(debate_fixture: dict) -> None:
    schema = load_schema("debate.schema.json")
    bad = json.loads(json.dumps(debate_fixture))
    del bad["rounds"][0]["variant_b_position"]
    errors = validate_tool_output(bad, schema)
    assert errors, "round missing required variant_b_position should fail"


def test_render_parity(debate_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path."""
    rendered = render_tool_output(debate_fixture, TEMPLATES_DIR / "debate.md.j2")
    assert rendered.startswith("---")
    assert "convergence_score:" in rendered
    assert "rounds_completed:" in rendered
    assert "### Round" in rendered
    assert "## Convergence Assessment" in rendered
    # convergence_score renders as a float (e.g. 0.72), not an int.
    assert "convergence_score: 0.72" in rendered
    assert rendered.count("\n") >= 50, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 50"
    )


def test_rendered_debate_satisfies_gate_frontmatter(debate_fixture: dict) -> None:
    """The rendered tool-write output must PASS DEBATE_GATE.

    Asserts every required frontmatter field appears as a ``key:`` line in the
    render and the render meets the gate's ``min_lines`` floor (>=50 newlines).
    """
    rendered = render_tool_output(debate_fixture, TEMPLATES_DIR / "debate.md.j2")
    for field in DEBATE_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= DEBATE_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {DEBATE_GATE.min_lines}"
    )


def test_rendered_debate_passes_convergence_semantic_check(
    debate_fixture: dict,
) -> None:
    """The rendered output must satisfy the DEBATE_GATE convergence semantic check.

    Imports ``_convergence_score_valid`` from gates.py (also reachable via
    ``DEBATE_GATE.semantic_checks[0].check_fn``) and asserts it returns truthy
    for the rendered fixture content -- i.e. convergence_score is a valid float
    in [0.0, 1.0].
    """
    rendered = render_tool_output(debate_fixture, TEMPLATES_DIR / "debate.md.j2")
    assert _convergence_score_valid(rendered)
    # The gate wires the SAME function.
    assert DEBATE_GATE.semantic_checks[0].check_fn is _convergence_score_valid
    assert DEBATE_GATE.semantic_checks[0].check_fn(rendered)


def test_render_step_tool_write_roundtrip(debate_fixture: dict, tmp_path) -> None:
    out = tmp_path / "debate.md"
    errors = render_step_tool_write("debate", json.dumps(debate_fixture), out)
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "debate.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == debate_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "debate.md"
    errors = render_step_tool_write("debate", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "debate.json").exists()


def test_debate_registry_key_distinct() -> None:
    """The debate registry entry must have its own config_flag and step_id."""
    assert TOOL_WRITE_REGISTRY["debate"].config_flag == "tool_write_debate"
    assert TOOL_WRITE_REGISTRY["debate"].step_id == "debate"
    assert TOOL_WRITE_REGISTRY["debate"].schema_name == "debate.schema.json"
    assert TOOL_WRITE_REGISTRY["debate"].template_name == "debate.md.j2"


def test_build_debate_prompt_tool_write_emits_json_contract() -> None:
    tw = build_debate_prompt(
        Path("d.md"), Path("a.md"), Path("b.md"), "standard", tool_write=True
    )
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in ("frontmatter", "rounds", "convergence_assessment"):
        assert key in tw, f"tool-write prompt missing debate key: {key}"

    md = build_debate_prompt(Path("d.md"), Path("a.md"), Path("b.md"), "standard")
    assert "<output_format>" in md


def test_semantic_layer_untouched() -> None:
    """PRESERVE check: semantic_layer.py imports and exposes run_semantic_layer.

    The debate tool-write rewrite changes ONLY the prompt/output contract; the
    adversarial-debate substrate in ``semantic_layer.py`` must remain intact.
    """
    import superclaude.cli.roadmap.semantic_layer as semantic_layer

    assert hasattr(semantic_layer, "run_semantic_layer")
    assert callable(semantic_layer.run_semantic_layer)
