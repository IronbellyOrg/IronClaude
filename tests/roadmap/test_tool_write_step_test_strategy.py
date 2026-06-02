"""Tests for the R1.4 test-strategy tool-write migration (Step 9.11, SECONDARY).

Mirrors ``test_tool_write_step_score.py`` for the test-strategy step. The
test-strategy step is a SECONDARY LLM step: it reads the merged roadmap + the
requirements extraction and produces a continuous-parallel test strategy. It
carries NO ``roadmap_ids`` and therefore has NO §MVR §3 / Contract #3 phantom-ID
subset constraint -- the executor routes it through the PLAIN
``render_step_tool_write`` (not the id-check variant).

These tests exercise the full tool-write loop for the test-strategy step:

* schema loads and exposes the required keys;
* a well-formed structured fixture passes schema validation and renders to
  markdown that satisfies TEST_STRATEGY_GATE (frontmatter fields + min_lines);
* malformed/invalid output is rejected without writing any artifact;
* the registry entry is distinct (its own config_flag);
* ``build_test_strategy_prompt(..., tool_write=True)`` swaps the output contract
  to JSON while the default markdown path is byte-identical (dual-write proof).

CONTRACT #8: ``interleave_ratio`` is a test:work milestone ratio string, NOT a
convergence threshold -- the schema/template MUST NOT bake in any threshold
literal (``0.7`` / ``0.5``).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import TEST_STRATEGY_GATE
from superclaude.cli.roadmap.prompts import (
    build_test_strategy_prompt,
)
from superclaude.cli.roadmap.prompts import (
    test_strategy_tool_definition as _test_strategy_tool_definition,
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
def test_strategy_fixture() -> dict:
    """A representative, schema-valid test-strategy output (renders >=40 lines)."""
    return {
        "frontmatter": {
            "complexity_class": "MEDIUM",
            "validation_philosophy": "continuous-parallel",
            "validation_milestones": 3,
            "work_milestones": 6,
            "interleave_ratio": "1:2",
            "major_issue_policy": "stop-and-fix",
            "spec_source": "spec.md",
            "generated": "2026-06-02T00:00:00Z",
            "generator": "test-strategy-agent",
        },
        "issue_classification": [
            {
                "severity": "CRITICAL",
                "action": "stop-and-fix immediately",
                "gate_impact": "Blocks current milestone",
            },
            {
                "severity": "MAJOR",
                "action": "stop-and-fix before next milestone",
                "gate_impact": "Blocks next milestone",
            },
            {
                "severity": "MINOR",
                "action": "Track and fix in next sprint",
                "gate_impact": "No gate impact",
            },
            {
                "severity": "COSMETIC",
                "action": "Backlog",
                "gate_impact": "No gate impact",
            },
        ],
        "validation_milestone_map": [
            {"milestone": "V1", "validates": "M1-M2 work milestones"},
            {"milestone": "V2", "validates": "M3-M4 work milestones"},
            {"milestone": "V3", "validates": "M5-M6 work milestones"},
        ],
        "test_categories": [
            "Unit tests for individual functions and classes.",
            "Integration tests across module boundaries.",
            "End-to-end tests of the full pipeline.",
            "Acceptance tests against spec requirements.",
        ],
        "interleaving_strategy": (
            "A MEDIUM-complexity roadmap interleaves one validation milestone per "
            "two work milestones (1:2). Each validation milestone gates the two "
            "preceding work milestones before the next work block begins."
        ),
        "risk_based_prioritization": [
            "Prioritize tests for the convergence engine (highest risk).",
            "Cover the phantom-ID rejection path early.",
            "Defer cosmetic-remediation tests to a later sprint.",
        ],
        "acceptance_criteria": [
            {"milestone": "M1", "criteria": "Extraction schema validates all fixtures."},
            {"milestone": "M3", "criteria": "Generate step rejects phantom IDs."},
            {"milestone": "M6", "criteria": "Full pipeline produces a certified roadmap."},
        ],
        "quality_gates": [
            "All BLOCKING findings resolved before the next milestone.",
            "Coverage threshold met per test category.",
            "No CRITICAL issues open at milestone close.",
        ],
    }


def test_test_strategy_schema_loads() -> None:
    schema = load_schema("test_strategy.schema.json")
    assert isinstance(schema, dict)
    assert "frontmatter" in set(schema["required"])
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {
        "complexity_class",
        "validation_philosophy",
        "validation_milestones",
        "work_milestones",
        "interleave_ratio",
        "major_issue_policy",
    } <= fm_required


def test_valid_output_passes_schema(test_strategy_fixture: dict) -> None:
    schema = load_schema("test_strategy.schema.json")
    assert validate_tool_output(test_strategy_fixture, schema) == []


def test_missing_frontmatter_field_fails(test_strategy_fixture: dict) -> None:
    schema = load_schema("test_strategy.schema.json")
    bad = json.loads(json.dumps(test_strategy_fixture))
    del bad["frontmatter"]["interleave_ratio"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required interleave_ratio frontmatter field should fail"


def test_invalid_complexity_class_fails(test_strategy_fixture: dict) -> None:
    schema = load_schema("test_strategy.schema.json")
    bad = json.loads(json.dumps(test_strategy_fixture))
    bad["frontmatter"]["complexity_class"] = "EXTREME"
    errors = validate_tool_output(bad, schema)
    assert errors, "complexity_class outside LOW/MEDIUM/HIGH enum should fail"


def test_render_parity(test_strategy_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path."""
    rendered = render_tool_output(
        test_strategy_fixture, TEMPLATES_DIR / "test_strategy.md.j2"
    )
    assert rendered.startswith("---")
    assert "complexity_class:" in rendered
    assert "validation_philosophy: continuous-parallel" in rendered
    assert "major_issue_policy: stop-and-fix" in rendered
    assert "## Issue Classification" in rendered
    assert "## Validation Milestones" in rendered
    assert "## Test Categories" in rendered
    assert "## Test-Implementation Interleaving Strategy" in rendered
    assert "## Risk-Based Test Prioritization" in rendered
    assert "## Acceptance Criteria per Milestone" in rendered
    assert "## Quality Gates Between Milestones" in rendered
    assert rendered.count("\n") >= 40, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 40"
    )


def test_rendered_satisfies_gate_frontmatter(test_strategy_fixture: dict) -> None:
    """The rendered tool-write output must PASS TEST_STRATEGY_GATE."""
    rendered = render_tool_output(
        test_strategy_fixture, TEMPLATES_DIR / "test_strategy.md.j2"
    )
    for field in TEST_STRATEGY_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= TEST_STRATEGY_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {TEST_STRATEGY_GATE.min_lines}"
    )


def test_render_step_tool_write_roundtrip(
    test_strategy_fixture: dict, tmp_path
) -> None:
    out = tmp_path / "test-strategy.md"
    errors = render_step_tool_write(
        "test-strategy", json.dumps(test_strategy_fixture), out
    )
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "test-strategy.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == test_strategy_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "test-strategy.md"
    errors = render_step_tool_write("test-strategy", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "test-strategy.json").exists()


def test_test_strategy_registry_key_distinct() -> None:
    spec = TOOL_WRITE_REGISTRY["test-strategy"]
    assert spec.config_flag == "tool_write_test_strategy"
    assert spec.step_id == "test-strategy"
    assert spec.schema_name == "test_strategy.schema.json"
    assert spec.template_name == "test_strategy.md.j2"


def test_test_strategy_tool_definition() -> None:
    td = _test_strategy_tool_definition()
    assert td.name == "test-strategy"
    assert td.input_schema == {}
    assert td.render_template == TEMPLATES_DIR / "test_strategy.md.j2"
    assert "frontmatter" in set(td.output_schema["required"])


def test_build_prompt_tool_write_emits_json_contract() -> None:
    tw = build_test_strategy_prompt(
        Path("roadmap.md"), Path("extraction.md"), tool_write=True
    )
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in (
        "issue_classification",
        "validation_milestone_map",
        "test_categories",
        "interleaving_strategy",
        "acceptance_criteria",
        "quality_gates",
    ):
        assert key in tw, f"tool-write prompt missing test-strategy key: {key}"

    md = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
    assert "<output_format>" in md


def test_build_prompt_default_byte_identical() -> None:
    """The default markdown path must be byte-identical with/without tool_write=False."""
    default = build_test_strategy_prompt(Path("roadmap.md"), Path("extraction.md"))
    explicit_false = build_test_strategy_prompt(
        Path("roadmap.md"), Path("extraction.md"), tool_write=False
    )
    assert default == explicit_false
    with_tdd = build_test_strategy_prompt(
        Path("roadmap.md"), Path("extraction.md"), tdd_file=Path("design.md")
    )
    assert "Supplementary TDD Context" in with_tdd
    with_prd = build_test_strategy_prompt(
        Path("roadmap.md"), Path("extraction.md"), prd_file=Path("prd.md")
    )
    assert "Supplementary PRD Context" in with_prd


def test_no_hardcoded_thresholds() -> None:
    """Contract #8: no convergence threshold literal in the substrate."""
    schema_text = (TOOL_SCHEMAS_DIR / "test_strategy.schema.json").read_text(
        encoding="utf-8"
    )
    template_text = (TEMPLATES_DIR / "test_strategy.md.j2").read_text(encoding="utf-8")
    for forbidden in ("0.7", "0.5"):
        assert forbidden not in schema_text, (
            f"test_strategy.schema.json must NOT bake in threshold literal {forbidden!r}"
        )
        assert forbidden not in template_text, (
            f"test_strategy.md.j2 must NOT bake in threshold literal {forbidden!r}"
        )
