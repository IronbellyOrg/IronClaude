"""Tests for the R1.4 score-step tool-write migration (Step 9.7).

Mirrors ``test_tool_write_step_diff.py`` for the score step. The score step is
SIMPLE: it reads the debate transcript and both roadmap variants, scores both,
and selects a base variant for the final merge. Like diff/debate it carries NO
``roadmap_ids`` and therefore has NO §MVR §3 / Contract #3 phantom-ID subset
constraint -- the executor routes it through the PLAIN ``render_step_tool_write``
(not the id-check variant).

These tests exercise the full tool-write loop for the score step:

* schema loads and exposes the required keys;
* a well-formed structured fixture passes schema validation and renders to
  markdown that satisfies SCORE_GATE (frontmatter fields + min_lines);
* malformed/invalid output is rejected without writing any artifact;
* the registry entry is distinct (its own config_flag);
* ``build_score_prompt(..., tool_write=True)`` swaps the output contract to JSON
  while the default markdown path is byte-identical (dual-write proof).

CONTRACT #8 (master:§Flaw 5) -- CRITICAL: the score schema and template MUST NOT
bake in any convergence threshold literal (``0.7`` / ``0.5``); those thresholds
are sourced at runtime from ``superclaude.contracts.CONVERGENCE_THRESHOLDS`` via
``prompts.roadmap_convergence_thresholds()``. Two dedicated tests enforce this.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import SCORE_GATE
from superclaude.cli.roadmap.prompts import (
    build_score_prompt,
    roadmap_convergence_thresholds,
    score_tool_definition,
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
from superclaude.contracts import CONVERGENCE_THRESHOLDS


@pytest.fixture
def score_fixture() -> dict:
    """A representative, schema-valid score structured output (renders >=20 lines)."""
    return {
        "frontmatter": {
            "base_variant": "roadmap-opus-architect.md",
            "variant_scores": "A:78 B:72",
            "generated": "2026-06-02T00:00:00Z",
            "generator": "score-agent",
            "variant_a": "roadmap-opus-architect.md",
            "variant_b": "roadmap-sonnet-backend.md",
        },
        "scoring_criteria": [
            "Coverage of all spec requirements.",
            "Milestone sequencing and dependency clarity.",
            "Risk register completeness.",
            "Testability of deliverables.",
        ],
        "per_criterion_scores": [
            {
                "criterion": "Requirement coverage",
                "variant_a_score": 20,
                "variant_b_score": 18,
            },
            {
                "criterion": "Milestone sequencing",
                "variant_a_score": 19,
                "variant_b_score": 20,
            },
            {
                "criterion": "Risk completeness",
                "variant_a_score": 20,
                "variant_b_score": 16,
            },
            {"criterion": "Testability", "variant_a_score": 19, "variant_b_score": 18},
        ],
        "overall_scores": {
            "variant_a": 78,
            "variant_b": 72,
            "justification": (
                "Variant A scores higher on requirement coverage and risk "
                "completeness; Variant B edges ahead only on milestone sequencing."
            ),
        },
        "base_selection_rationale": (
            "Variant A is selected as the base: it covers every spec requirement "
            "and carries the more complete risk register, which is the harder "
            "property to retrofit during merge."
        ),
        "improvements_to_incorporate": [
            "Adopt Variant B's finer-grained milestone sequencing.",
            "Pull Variant B's earlier integration-test milestone forward.",
        ],
    }


def test_score_schema_loads() -> None:
    schema = load_schema("score.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "base_selection_rationale"} <= required
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {"base_variant", "variant_scores"} <= fm_required


def test_valid_output_passes_schema(score_fixture: dict) -> None:
    schema = load_schema("score.schema.json")
    assert validate_tool_output(score_fixture, schema) == []


def test_missing_base_selection_rationale_fails(score_fixture: dict) -> None:
    schema = load_schema("score.schema.json")
    bad = json.loads(json.dumps(score_fixture))
    del bad["base_selection_rationale"]
    errors = validate_tool_output(bad, schema)
    assert errors, (
        "missing required base_selection_rationale should fail schema validation"
    )


def test_missing_frontmatter_field_fails(score_fixture: dict) -> None:
    schema = load_schema("score.schema.json")
    bad = json.loads(json.dumps(score_fixture))
    del bad["frontmatter"]["base_variant"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required base_variant frontmatter field should fail"


def test_per_criterion_requires_criterion(score_fixture: dict) -> None:
    schema = load_schema("score.schema.json")
    bad = json.loads(json.dumps(score_fixture))
    del bad["per_criterion_scores"][0]["criterion"]
    errors = validate_tool_output(bad, schema)
    assert errors, "per-criterion score missing required criterion should fail"


def test_render_parity(score_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path."""
    rendered = render_tool_output(score_fixture, TEMPLATES_DIR / "score.md.j2")
    assert rendered.startswith("---")
    assert "base_variant:" in rendered
    assert "variant_scores:" in rendered
    # All five body sections present.
    assert "## Scoring Criteria" in rendered
    assert "## Per-Criterion Scores" in rendered
    assert "## Overall Scores" in rendered
    assert "## Base Variant Selection Rationale" in rendered
    assert "## Improvements to Incorporate" in rendered
    for criterion in score_fixture["scoring_criteria"]:
        assert criterion in rendered, f"missing criterion: {criterion}"
    assert rendered.count("\n") >= 20, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 20"
    )


def test_rendered_score_satisfies_gate_frontmatter(score_fixture: dict) -> None:
    """The rendered tool-write output must PASS SCORE_GATE.

    Asserts every required frontmatter field appears as a ``key:`` line in the
    render and the render meets the gate's ``min_lines`` floor (>=20 newlines).
    """
    rendered = render_tool_output(score_fixture, TEMPLATES_DIR / "score.md.j2")
    for field in SCORE_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= SCORE_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {SCORE_GATE.min_lines}"
    )


def test_render_step_tool_write_roundtrip(score_fixture: dict, tmp_path) -> None:
    out = tmp_path / "base-selection.md"
    errors = render_step_tool_write("score", json.dumps(score_fixture), out)
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "base-selection.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == score_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "base-selection.md"
    errors = render_step_tool_write("score", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "base-selection.json").exists()


def test_render_step_tool_write_dual_write_proof(score_fixture: dict, tmp_path) -> None:
    """Dual-write proof: the PASS path writes BOTH the .md artifact and .json sidecar."""
    out = tmp_path / "base-selection.md"
    sidecar = tmp_path / "base-selection.json"
    assert not out.exists()
    assert not sidecar.exists()
    errors = render_step_tool_write("score", json.dumps(score_fixture), out)
    assert errors == []
    assert out.exists(), "markdown artifact must be written on PASS"
    assert sidecar.exists(), "JSON sidecar must be written on PASS"
    # The sidecar is the durable typed substrate; the markdown is rendered from it.
    assert json.loads(sidecar.read_text(encoding="utf-8")) == score_fixture
    assert out.read_text(encoding="utf-8").startswith("---")


def test_score_registry_key_distinct() -> None:
    """The score registry entry must have its own config_flag and step_id."""
    assert TOOL_WRITE_REGISTRY["score"].config_flag == "tool_write_score"
    assert TOOL_WRITE_REGISTRY["score"].step_id == "score"
    assert TOOL_WRITE_REGISTRY["score"].schema_name == "score.schema.json"
    assert TOOL_WRITE_REGISTRY["score"].template_name == "score.md.j2"


def test_score_tool_definition() -> None:
    td = score_tool_definition()
    assert td.name == "score"
    assert td.input_schema == {}
    assert td.render_template == TEMPLATES_DIR / "score.md.j2"
    assert "base_selection_rationale" in set(td.output_schema["required"])


def test_build_score_prompt_tool_write_emits_json_contract() -> None:
    tw = build_score_prompt(
        Path("debate.md"), Path("a.md"), Path("b.md"), tool_write=True
    )
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in (
        "scoring_criteria",
        "per_criterion_scores",
        "overall_scores",
        "base_selection_rationale",
        "improvements_to_incorporate",
    ):
        assert key in tw, f"tool-write prompt missing score key: {key}"

    md = build_score_prompt(Path("debate.md"), Path("a.md"), Path("b.md"))
    assert "<output_format>" in md


def test_build_score_prompt_default_byte_identical() -> None:
    """The default markdown path must be byte-identical with/without tool_write=False.

    Guards the dual-write contract: enabling the flag changes ONLY the output
    block; the default production prompt is unchanged.
    """
    default = build_score_prompt(Path("debate.md"), Path("a.md"), Path("b.md"))
    explicit_false = build_score_prompt(
        Path("debate.md"), Path("a.md"), Path("b.md"), tool_write=False
    )
    assert default == explicit_false
    # TDD/PRD conditional blocks remain intact in the default path.
    with_tdd = build_score_prompt(
        Path("debate.md"), Path("a.md"), Path("b.md"), tdd_file=Path("design.md")
    )
    assert "Supplementary TDD Context" in with_tdd
    with_prd = build_score_prompt(
        Path("debate.md"), Path("a.md"), Path("b.md"), prd_file=Path("prd.md")
    )
    assert "Supplementary PRD Context" in with_prd


# --- CONTRACT #8 tests (CRITICAL) -----------------------------------------


def test_score_schema_no_hardcoded_thresholds() -> None:
    """Contract #8: no convergence threshold literal is baked into the substrate.

    The score schema file and the render template MUST NOT contain the literal
    threshold values ``0.7`` or ``0.5`` -- those are convergence thresholds
    sourced at runtime from ``superclaude.contracts.CONVERGENCE_THRESHOLDS``,
    NOT properties of the 0-100 score evaluation.
    """
    schema_text = (TOOL_SCHEMAS_DIR / "score.schema.json").read_text(encoding="utf-8")
    template_text = (TEMPLATES_DIR / "score.md.j2").read_text(encoding="utf-8")
    for forbidden in ("0.7", "0.5"):
        assert forbidden not in schema_text, (
            f"score.schema.json must NOT bake in threshold literal {forbidden!r} "
            "(Contract #8: thresholds are registry-sourced)"
        )
        assert forbidden not in template_text, (
            f"score.md.j2 must NOT bake in threshold literal {forbidden!r} "
            "(Contract #8: thresholds are registry-sourced)"
        )


def test_score_thresholds_registry_sourced() -> None:
    """Contract #8: the score path's convergence thresholds come from the SoT.

    ``roadmap_convergence_thresholds()`` MUST return the SAME object/values as
    ``CONVERGENCE_THRESHOLDS["sc:roadmap"]`` -- proving the thresholds are read
    from the single source of truth, not duplicated.
    """
    thresholds = roadmap_convergence_thresholds()
    assert thresholds == (0.7, 0.5)
    assert thresholds == CONVERGENCE_THRESHOLDS["sc:roadmap"]
    # Same object identity -- the helper reads the registry, it does not redefine.
    assert thresholds is CONVERGENCE_THRESHOLDS["sc:roadmap"]
