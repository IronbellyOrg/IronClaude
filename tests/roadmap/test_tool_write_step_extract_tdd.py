"""Tests for the R1.4 extract_tdd-step tool-write migration (Step 9.3).

Mirrors ``test_tool_write_step_extract.py`` for the TDD-input variant of the
extract step. The TDD-extract path builds a Step whose ``id`` is still
``"extract"`` (shared with the spec-extract path), so the tool-write registry
disambiguates via a SECOND key ``"extract_tdd"`` whose ``step_id`` is still
``"extract"`` but whose ``config_flag`` is ``"tool_write_extract_tdd"``. These
tests exercise the full tool-write loop and prove the two registry entries do
not collide.

The extract_tdd contract is FULL parity with ``build_extract_prompt_tdd``: the
markdown path emits a 19-field frontmatter and 14 ``## `` sections (8 standard +
6 TDD design sections), and ``EXTRACT_TDD_GATE`` REQUIRES all 19 frontmatter
fields. The tool-write rendering must satisfy that gate, so these tests assert
full-parity rendering (not the lossy 9-section/13-field subset).
"""

from __future__ import annotations

import json

import pytest

from superclaude.cli.roadmap.gates import EXTRACT_TDD_GATE
from superclaude.cli.roadmap.prompts import build_extract_prompt_tdd
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_id_subset,
    validate_tool_output,
)
from superclaude.contracts import ID_PATTERNS

# 14 verbatim section headers the rendered markdown must contain
# (8 standard + 6 TDD design sections).
_SECTION_HEADERS = [
    "## Functional Requirements",
    "## Non-Functional Requirements",
    "## Complexity Assessment",
    "## Architectural Constraints",
    "## Risk Inventory",
    "## Dependency Inventory",
    "## Success Criteria",
    "## Open Questions",
    "## Data Models and Interfaces",
    "## API Specifications",
    "## Component Inventory",
    "## Testing Strategy",
    "## Migration and Rollout Plan",
    "## Operational Readiness",
]

# 19 frontmatter field names that must appear as `key:` lines in the render.
_FRONTMATTER_FIELDS = [
    "spec_source",
    "generated",
    "generator",
    "functional_requirements",
    "nonfunctional_requirements",
    "total_requirements",
    "complexity_score",
    "complexity_class",
    "domains_detected",
    "risks_identified",
    "dependencies_identified",
    "success_criteria_count",
    "extraction_mode",
    "data_models_identified",
    "api_surfaces_identified",
    "components_identified",
    "test_artifacts_identified",
    "migration_items_identified",
    "operational_items_identified",
]


@pytest.fixture
def extract_tdd_fixture() -> dict:
    """A representative, schema-valid, FULL-parity extract_tdd output."""
    return {
        "frontmatter": {
            "spec_source": "design.tdd.md",
            "generated": "2026-06-02T00:00:00Z",
            "generator": "extract-tdd-agent",
            "functional_requirements": 2,
            "nonfunctional_requirements": 1,
            "total_requirements": 3,
            "complexity_score": 0.55,
            "complexity_class": "HIGH",
            "domains_detected": ["backend", "testing", "devops"],
            "risks_identified": 1,
            "dependencies_identified": 2,
            "success_criteria_count": 1,
            "extraction_mode": "standard",
            "data_models_identified": 1,
            "api_surfaces_identified": 1,
            "components_identified": 1,
            "test_artifacts_identified": 1,
            "migration_items_identified": 1,
            "operational_items_identified": 1,
        },
        "functional_requirements": [
            {
                "id": "FR-1",
                "description": "The system shall extract design artifacts.",
                "paths": ["/api/extract-tdd"],
            },
            {
                "id": "FR-2.1",
                "description": "The system shall surface synthetic design IDs.",
            },
        ],
        "non_functional_requirements": [
            {"id": "NFR-1", "description": "TDD extraction completes within 1800s."},
        ],
        "complexity_assessment": "High complexity driven by data-model and API surface.",
        "architectural_constraints": ["Must use UV for Python operations."],
        "risk_inventory": [
            {
                "id": "RSK-1",
                "risk": "Schema drift between prompt and template.",
                "severity": "medium",
                "mitigation": "SoT-drift guard test.",
            },
        ],
        "dependency_inventory": ["jsonschema", "jinja2"],
        "success_criteria": ["All extract_tdd tool-write tests pass."],
        "open_questions": ["Should chunked mode be auto-detected for large TDDs?"],
        "data_models": [
            {
                "id": "DM-001",
                "name": "ExtractionResult",
                "fields": "requirements: list, entities: list",
                "relationships": "owns API-001 surfaces",
            },
        ],
        "api_specifications": [
            {
                "id": "API-001",
                "method": "POST",
                "path": "/api/extract-tdd",
                "description": "Submit a TDD for structured extraction.",
            },
        ],
        "component_inventory": [
            {
                "id": "COMP-001",
                "name": "TddExtractor",
                "type": "service",
                "dependencies": ["COMP-parser"],
            },
        ],
        "testing_strategy": [
            {
                "id": "TEST-001",
                "name": "extract_tdd render-parity",
                "level": "unit",
            },
        ],
        "migration_plan": [
            {
                "id": "MIG-001",
                "phase": "dual-write rollout",
                "rollback": "Disable tool_write_extract_tdd flag.",
            },
        ],
        "operational_readiness": [
            {
                "id": "OPS-001",
                "scenario": "Gate rejects rendered extraction.",
                "resolution": "Inspect frontmatter field coverage.",
            },
        ],
        "roadmap_ids": [
            "FR-1",
            "FR-2.1",
            "NFR-1",
            "DM-001",
            "API-001",
            "COMP-001",
            "TEST-001",
            "MIG-001",
            "OPS-001",
        ],
    }


def test_extract_tdd_schema_loads() -> None:
    schema = load_schema("extract_tdd.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {
        "frontmatter",
        "functional_requirements",
        "non_functional_requirements",
        "roadmap_ids",
    } <= required
    # All 19 frontmatter fields are required by the schema (gate parity).
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert set(_FRONTMATTER_FIELDS) <= fm_required


def test_extract_tdd_schema_id_pattern_matches_contracts() -> None:
    """The roadmap_ids pattern must embed every ID_PATTERNS family body AND
    the 6 synthetic TDD-artifact family prefixes.

    Guards against silent SoT drift (Contract #8): if a family regex in
    ``superclaude.contracts.ID_PATTERNS`` changes, this assertion fails until
    the schema pattern is recomposed from the SoT.
    """
    schema = load_schema("extract_tdd.schema.json")
    pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
    for family in ("FR", "NFR", "SC", "G", "D"):
        assert ID_PATTERNS[family] in pattern, (
            f"ID_PATTERNS['{family}'] body {ID_PATTERNS[family]!r} "
            f"missing from roadmap_ids pattern {pattern!r}"
        )
    for prefix in ("DM-", "API-", "COMP-", "TEST-", "MIG-", "OPS-"):
        assert prefix in pattern, (
            f"synthetic TDD-artifact prefix {prefix!r} missing from "
            f"roadmap_ids pattern {pattern!r}"
        )


def test_valid_output_passes_schema(extract_tdd_fixture: dict) -> None:
    schema = load_schema("extract_tdd.schema.json")
    assert validate_tool_output(extract_tdd_fixture, schema) == []


def test_phantom_field_type_fails(extract_tdd_fixture: dict) -> None:
    schema = load_schema("extract_tdd.schema.json")
    bad = json.loads(json.dumps(extract_tdd_fixture))
    # functional_requirements count must be an integer; a string is a violation.
    bad["frontmatter"]["functional_requirements"] = "two"
    errors = validate_tool_output(bad, schema)
    assert errors, "wrong type for a count field should fail schema validation"


def test_extraction_mode_matches_gate_tolerance(extract_tdd_fixture: dict) -> None:
    """The extraction_mode schema constraint must be interchangeable with the
    markdown-path gate ``_extraction_mode_valid`` (gates.py): it accepts
    'standard' or ANY value starting with 'chunked' (e.g. 'chunked (3 chunks)').

    Regression for the dual-write semantic-narrowing finding F1: the prior
    ``enum: ["standard","chunked"]`` rejected the gate-legal 'chunked (3 chunks)'
    form, which would have failed a tool-write extract whose equivalent markdown
    extract passed its gate. Also confirms a non-chunked/non-standard value is
    still rejected (the gate rejects 'full'/'partial'/'incremental').
    """
    from superclaude.cli.roadmap.gates import _extraction_mode_valid

    schema = load_schema("extract_tdd.schema.json")

    for legal in ("standard", "chunked", "chunked (3 chunks)"):
        ok = json.loads(json.dumps(extract_tdd_fixture))
        ok["frontmatter"]["extraction_mode"] = legal
        assert validate_tool_output(ok, schema) == [], (
            f"schema must accept gate-legal extraction_mode {legal!r}"
        )
        # Parity with the markdown gate's semantic check on the same value.
        assert _extraction_mode_valid(f"---\nextraction_mode: {legal}\n---\n"), (
            f"gate must also accept {legal!r} (interchangeability)"
        )

    bad = json.loads(json.dumps(extract_tdd_fixture))
    bad["frontmatter"]["extraction_mode"] = "full"
    assert validate_tool_output(bad, schema), (
        "schema must reject a non-standard/non-chunked extraction_mode"
    )


def test_render_parity(extract_tdd_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path.

    Asserts the render starts with frontmatter, contains all 14 section
    headers, all 19 frontmatter field names as ``key:`` lines, and the
    synthetic TDD-artifact ids in their respective sections.
    """
    rendered = render_tool_output(
        extract_tdd_fixture, TEMPLATES_DIR / "extract_tdd.md.j2"
    )
    assert rendered.startswith("---")
    for header in _SECTION_HEADERS:
        assert header in rendered, f"missing section header: {header}"
    for field in _FRONTMATTER_FIELDS:
        assert f"{field}:" in rendered, f"missing frontmatter field: {field}"
    for fr in extract_tdd_fixture["functional_requirements"]:
        assert fr["id"] in rendered, f"FR id {fr['id']} not in rendered markdown"
    for synthetic_id in (
        "DM-001",
        "API-001",
        "COMP-001",
        "TEST-001",
        "MIG-001",
        "OPS-001",
    ):
        assert synthetic_id in rendered, f"synthetic id {synthetic_id} not rendered"


def test_rendered_tdd_satisfies_gate_frontmatter(extract_tdd_fixture: dict) -> None:
    """The rendered tool-write output must PASS EXTRACT_TDD_GATE.

    For each required frontmatter field in the gate, assert it (or one of its
    aliases, for tuple entries) appears as a ``key:`` line in the rendered
    frontmatter; and assert the render meets the gate's ``min_lines`` floor.
    Proves the tool-write path is gate-passing -- the parity defect being fixed.
    """
    rendered = render_tool_output(
        extract_tdd_fixture, TEMPLATES_DIR / "extract_tdd.md.j2"
    )
    for field in EXTRACT_TDD_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )
    assert rendered.count("\n") >= EXTRACT_TDD_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {EXTRACT_TDD_GATE.min_lines}"
    )


def test_render_step_tool_write_roundtrip(extract_tdd_fixture: dict, tmp_path) -> None:
    out = tmp_path / "extraction.md"
    errors = render_step_tool_write("extract_tdd", json.dumps(extract_tdd_fixture), out)
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "extraction.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == extract_tdd_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "extraction.md"
    errors = render_step_tool_write("extract_tdd", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "extraction.json").exists()


def test_validate_id_subset() -> None:
    spec_ids = {"FR-1", "FR-2", "NFR-1"}
    # Subset -> PASS.
    assert validate_id_subset(["FR-1", "NFR-1"], spec_ids) == []
    # Extra id -> FAIL.
    errors = validate_id_subset(["FR-1", "FR-99"], spec_ids)
    assert errors and "FR-99" in errors[0]
    # accepted_deviations rescues the extra id.
    assert validate_id_subset(["FR-1", "FR-99"], spec_ids, {"FR-99"}) == []


def test_build_extract_prompt_tdd_tool_write_emits_json_contract() -> None:
    from pathlib import Path

    tw = build_extract_prompt_tdd(Path("s.md"), tool_write=True)
    assert "JSON" in tw
    assert "<output_format>" not in tw
    # The True branch must list the FULL TDD key set, not the lossy subset.
    for key in (
        "data_models",
        "api_specifications",
        "component_inventory",
        "testing_strategy",
        "migration_plan",
        "operational_readiness",
    ):
        assert key in tw, f"tool-write prompt missing TDD key: {key}"
    assert "operational_items_identified" in tw

    md = build_extract_prompt_tdd(Path("s.md"))
    assert "<output_format>" in md


def test_extract_tdd_registry_key_distinct() -> None:
    """The extract_tdd registry entry must not collide with extract.

    Both pipeline paths build a Step with ``id == "extract"``; the registry
    disambiguates via the ``"extract_tdd"`` KEY (resolved by input_type in the
    executor). Each key maps to its own config_flag.
    """
    assert TOOL_WRITE_REGISTRY["extract_tdd"].config_flag == "tool_write_extract_tdd"
    assert TOOL_WRITE_REGISTRY["extract"].config_flag == "tool_write_extract"
    # Both entries share the real Step.id, proving the key is the disambiguator.
    assert TOOL_WRITE_REGISTRY["extract_tdd"].step_id == "extract"
    assert TOOL_WRITE_REGISTRY["extract"].step_id == "extract"
