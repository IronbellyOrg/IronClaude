"""Tests for the R1.4 generate-step tool-write migration (Step 9.4).

The generate step is the PRIMARY phantom-ID source (master:§Top-3 #3), so the
load-bearing deliverable here is the GENERATION-TIME phantom-ID rejection:
``render_step_tool_write_with_id_check`` extracts ``roadmap_ids`` from the
validated JSON and runs ``validate_id_subset`` against the spec's id universe
BEFORE writing any artifact -- a phantom id (e.g. FR-99 absent from the
extraction) is rejected and no markdown is written.

These tests mirror ``test_tool_write_step_extract.py`` /
``test_tool_write_step_extract_tdd.py`` and additionally exercise the
phantom-ID gate (Contract #3) and the gate-frontmatter parity against
``GENERATE_A_GATE``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import GENERATE_A_GATE
from superclaude.cli.roadmap.models import AgentSpec
from superclaude.cli.roadmap.prompts import build_generate_prompt
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write_with_id_check,
    render_tool_output,
    validate_id_subset,
    validate_tool_output,
)
from superclaude.contracts import (
    ID_PATTERNS,
    ROADMAP_ENTITY_ID_FAMILIES,
    TOOL_WRITE_ROADMAP_ID_FAMILIES,
)


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


@pytest.fixture
def generate_fixture() -> dict:
    """A representative, schema-valid, gate-passing generate output.

    Three milestones spanning deliverable rows for FR-1..FR-5 (plus several
    entity-family rows), roadmap_ids listing FR-1..FR-5. Realistic in size so
    the rendered markdown clears the GENERATE_A_GATE >= 100-line floor.
    """
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
            {
                "milestone": "M1",
                "start_week": "1",
                "end_week": "3",
                "duration": "3 weeks",
            },
            {
                "milestone": "M2",
                "start_week": "4",
                "end_week": "6",
                "duration": "3 weeks",
            },
            {
                "milestone": "M3",
                "start_week": "7",
                "end_week": "9",
                "duration": "3 weeks",
            },
        ],
        "roadmap_ids": ["FR-1", "FR-2", "FR-3", "FR-4", "FR-5"],
    }


def test_generate_schema_loads() -> None:
    schema = load_schema("generate.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "milestones", "roadmap_ids"} <= required
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {"spec_source", "complexity_score", "primary_persona"} <= fm_required


def test_generate_schema_id_pattern_matches_contracts() -> None:
    """The roadmap_ids pattern must embed every ID_PATTERNS family body AND the
    generate step's full entity family set, each as an EXACT alternation arm.

    Guards against silent SoT drift (Contract #8): keys-driven on BOTH halves
    from the live SoT — ``ID_PATTERNS`` for spec families (incl. MD) and
    ``TOOL_WRITE_ROADMAP_ID_FAMILIES`` / ``ROADMAP_ENTITY_ID_FAMILIES`` for the
    per-step entity families (DM/API/COMP/TEST/MIG/OPS/OQ). Arm-level
    membership (split on ``|``) is immune to the MD-subset-of-D substring trap.
    """
    schema = load_schema("generate.schema.json")
    pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
    arms = pattern[2:-2].split("|")  # strip leading "^(" and trailing ")$"
    for family, body in ID_PATTERNS.items():  # MD, FR, NFR, SC, G, D
        assert body in arms, (
            f"ID_PATTERNS['{family}'] body {body!r} is not an exact "
            f"alternation arm of {arms!r}"
        )
    for prefix in TOOL_WRITE_ROADMAP_ID_FAMILIES["generate"]:
        body = ROADMAP_ENTITY_ID_FAMILIES[prefix]
        assert body in arms, (
            f"generate entity family {prefix!r} body {body!r} is not an exact "
            f"alternation arm of {arms!r}"
        )


def test_valid_output_passes_schema(generate_fixture: dict) -> None:
    schema = load_schema("generate.schema.json")
    assert validate_tool_output(generate_fixture, schema) == []


def test_wrong_type_fails_schema(generate_fixture: dict) -> None:
    schema = load_schema("generate.schema.json")
    bad = json.loads(json.dumps(generate_fixture))
    # complexity_score must be a number; a string is a violation.
    bad["frontmatter"]["complexity_score"] = "high"
    errors = validate_tool_output(bad, schema)
    assert errors, "wrong type for complexity_score should fail schema validation"


def test_missing_milestones_fails_schema(generate_fixture: dict) -> None:
    schema = load_schema("generate.schema.json")
    bad = json.loads(json.dumps(generate_fixture))
    del bad["milestones"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required 'milestones' must fail schema validation"

    # Empty milestones array also fails (minItems 1).
    bad2 = json.loads(json.dumps(generate_fixture))
    bad2["milestones"] = []
    assert validate_tool_output(bad2, schema), "empty milestones must fail minItems"


def test_render_parity(generate_fixture: dict) -> None:
    """Rendered tool-write output is a structurally complete roadmap."""
    rendered = render_tool_output(generate_fixture, TEMPLATES_DIR / "generate.md.j2")
    assert rendered.startswith("---")
    assert "## Executive Summary" in rendered
    assert "## Timeline Estimates" in rendered
    # At least one milestone header `## M{N}: ...`.
    assert "## M1:" in rendered
    # 9-column deliverable table header.
    assert "| # | ID | Title |" in rendered
    # Numbered/bulleted content present (Risk Register uses numbered list).
    import re

    assert re.search(r"^\s*(?:[-*]|\d+\.)\s+\S", rendered, re.MULTILINE)
    # Realistic fixture renders >= 100 lines.
    assert rendered.count("\n") >= 100, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 100"
    )
    # Every deliverable id is present.
    for rid in generate_fixture["roadmap_ids"]:
        assert rid in rendered, f"deliverable id {rid} not in rendered markdown"


def test_rendered_generate_satisfies_gate_frontmatter(generate_fixture: dict) -> None:
    """The rendered tool-write output must PASS GENERATE_A_GATE frontmatter.

    For each required frontmatter field in the gate, assert it (or one of its
    aliases, for tuple entries) appears as a ``key:`` line; and assert the
    render meets the gate's ``min_lines`` floor.
    """
    rendered = render_tool_output(generate_fixture, TEMPLATES_DIR / "generate.md.j2")
    for field in GENERATE_A_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= GENERATE_A_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {GENERATE_A_GATE.min_lines}"
    )


def test_generate_rejects_phantom_id(generate_fixture: dict, tmp_path) -> None:
    """CRITICAL (Contract #3): phantom ids rejected AT GENERATION TIME.

    1. ``validate_id_subset`` flags a phantom id and passes a clean subset.
    2. ``render_step_tool_write_with_id_check`` with a fixture whose
       roadmap_ids contains a phantom id returns errors AND writes NO markdown.
    3. A clean fixture (roadmap_ids ⊆ spec_ids) returns [] and writes the .md.
    """
    spec_ids = {"FR-1", "FR-2", "FR-3", "FR-4", "FR-5"}

    # 1. Direct validate_id_subset behavior.
    errors = validate_id_subset(["FR-1", "FR-99"], spec_ids=spec_ids)
    assert errors and any("FR-99" in e for e in errors), (
        "phantom FR-99 must be rejected by validate_id_subset"
    )
    assert validate_id_subset(["FR-1", "FR-2"], spec_ids=spec_ids) == []

    # 2. Phantom id in roadmap_ids -> rejected at generation time, no .md.
    phantom_fixture = json.loads(json.dumps(generate_fixture))
    phantom_fixture["roadmap_ids"] = phantom_fixture["roadmap_ids"] + ["FR-99"]
    out = tmp_path / "roadmap.md"
    tw_errors = render_step_tool_write_with_id_check(
        "generate",
        json.dumps(phantom_fixture),
        out,
        spec_ids=spec_ids,
    )
    assert tw_errors and any("FR-99" in e for e in tw_errors), (
        "phantom id must be rejected by render_step_tool_write_with_id_check"
    )
    assert not out.exists(), "no .md may be written when a phantom id is present"
    assert not (tmp_path / "roadmap.json").exists(), (
        "no JSON sidecar may be written when a phantom id is present"
    )

    # 3. Clean fixture (roadmap_ids ⊆ spec_ids) -> PASS, .md written.
    clean_out = tmp_path / "roadmap_clean.md"
    clean_errors = render_step_tool_write_with_id_check(
        "generate",
        json.dumps(generate_fixture),
        clean_out,
        spec_ids=spec_ids,
    )
    assert clean_errors == []
    assert clean_out.exists()
    markdown = clean_out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "roadmap_clean.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == generate_fixture


def test_id_check_skips_when_spec_ids_empty(generate_fixture: dict, tmp_path) -> None:
    """Empty spec_ids -> subset check skipped (identity); render still runs."""
    out = tmp_path / "roadmap.md"
    # A phantom id is present, but with no spec_ids universe the check is skipped.
    phantom_fixture = json.loads(json.dumps(generate_fixture))
    phantom_fixture["roadmap_ids"] = phantom_fixture["roadmap_ids"] + ["FR-99"]
    errors = render_step_tool_write_with_id_check(
        "generate",
        json.dumps(phantom_fixture),
        out,
        spec_ids=set(),
    )
    assert errors == []
    assert out.exists()


def test_render_step_tool_write_with_id_check_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "roadmap.md"
    errors = render_step_tool_write_with_id_check(
        "generate", "{not valid json", out, spec_ids={"FR-1"}
    )
    assert errors
    assert not out.exists()
    assert not (tmp_path / "roadmap.json").exists()


def test_generate_registry_key_distinct() -> None:
    """The generate registry entry maps the right config flag + step_id."""
    assert TOOL_WRITE_REGISTRY["generate"].config_flag == "tool_write_generate"
    assert TOOL_WRITE_REGISTRY["generate"].schema_name == "generate.schema.json"
    assert TOOL_WRITE_REGISTRY["generate"].template_name == "generate.md.j2"
    # Distinct from the extract entries.
    assert TOOL_WRITE_REGISTRY["extract"].config_flag == "tool_write_extract"


def test_build_generate_prompt_tool_write_emits_json_contract() -> None:
    agent = AgentSpec("opus", "architect")
    tw = build_generate_prompt(agent, Path("e.md"), tool_write=True)
    assert "JSON" in tw
    assert "<output_format>" not in tw
    # Mentions the structured keys.
    for key in ("milestones", "deliverables", "roadmap_ids"):
        assert key in tw, f"tool-write prompt missing key: {key}"
    # Phantom-ID guidance present.
    assert "phantom" in tw.lower()

    # Default (markdown) path unchanged: contains the output_format behavior and
    # the template structure directive.
    md = build_generate_prompt(agent, Path("e.md"))
    assert "<output_format>" in md
    assert "9-column deliverable table" in md
