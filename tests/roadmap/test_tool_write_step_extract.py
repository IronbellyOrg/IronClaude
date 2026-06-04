"""Tests for the R1.4 extract-step tool-write migration (Step 9.2).

These tests are the pattern-establishing reference for Steps 9.3-9.11. They
exercise the full tool-write loop for the ``extract`` step:

* schema loads and is consistent with the ``superclaude.contracts.ID_PATTERNS``
  source of truth (Contract #8 SoT-drift guard);
* a well-formed structured fixture passes schema validation and renders to
  markdown that is *structurally equivalent* to the legacy markdown-path output
  (the side-by-side parity check);
* malformed/invalid output is rejected without writing any artifact;
* the ``validate_id_subset`` §MVR §3 constraint behaves as specified;
* ``build_extract_prompt(..., tool_write=True)`` swaps the output contract to
  JSON while the default markdown path is unchanged (dual-write proof).
"""

from __future__ import annotations

import json

import pytest

from superclaude.cli.roadmap.prompts import build_extract_prompt
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_id_subset,
    validate_tool_output,
)
from superclaude.contracts import (
    ID_PATTERNS,
    ROADMAP_ENTITY_ID_FAMILIES,
    TOOL_WRITE_ROADMAP_ID_FAMILIES,
)

# 9 verbatim section headers the rendered markdown must contain.
_SECTION_HEADERS = [
    "## Functional Requirements",
    "## Non-Functional Requirements",
    "## Complexity Assessment",
    "## Architectural Constraints",
    "## Component Inventory",
    "## Risk Inventory",
    "## Dependency Inventory",
    "## Success Criteria",
    "## Open Questions",
]


@pytest.fixture
def extract_fixture() -> dict:
    """A representative, schema-valid extract structured output."""
    return {
        "frontmatter": {
            "spec_source": "spec.md",
            "generated": "2026-06-02T00:00:00Z",
            "generator": "extract-agent",
            "functional_requirements": 2,
            "nonfunctional_requirements": 1,
            "total_requirements": 3,
            "complexity_score": 0.42,
            "complexity_class": "MEDIUM",
            "domains_detected": ["backend", "security"],
            "risks_identified": 1,
            "dependencies_identified": 1,
            "success_criteria_count": 1,
            "extraction_mode": "standard",
        },
        "functional_requirements": [
            {
                "id": "FR-1",
                "description": "The system shall extract requirements.",
                "paths": ["/api/extract"],
            },
            {
                "id": "FR-2.1",
                "description": "The system shall surface synthetic component IDs.",
            },
        ],
        "non_functional_requirements": [
            {"id": "NFR-1", "description": "Extraction completes within 300s."},
        ],
        "complexity_assessment": "Moderate complexity driven by schema validation.",
        "architectural_constraints": ["Must use UV for Python operations."],
        "component_inventory": [
            {
                "id": "COMP-extractor",
                "name": "RequirementExtractor",
                "role": "Parses the spec into typed requirements.",
                "dependencies": ["COMP-parser"],
                "source_ref": "§3.1",
            },
            {
                "id": "DM-extraction",
                "name": "ExtractionResult",
                "role": "DTO carrying extracted requirements.",
            },
        ],
        "risk_inventory": [
            {
                "id": "RSK-1",
                "risk": "Schema drift between prompt and template.",
                "severity": "medium",
                "mitigation": "SoT-drift guard test.",
            },
        ],
        "dependency_inventory": ["jsonschema", "jinja2"],
        "success_criteria": ["All extract tool-write tests pass."],
        "open_questions": ["Should chunked mode be auto-detected?"],
        "roadmap_ids": [
            "FR-1",
            "FR-2.1",
            "NFR-1",
            "COMP-extractor",
            "DM-extraction",
        ],
    }


def test_extract_schema_loads() -> None:
    schema = load_schema("extract.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {
        "frontmatter",
        "functional_requirements",
        "non_functional_requirements",
        "roadmap_ids",
    } <= required


def test_extract_schema_id_pattern_matches_contracts() -> None:
    """The roadmap_ids pattern must embed every ID_PATTERNS family body AND the
    extract step's entity families, each as an EXACT alternation arm.

    Guards against silent SoT drift (Contract #8): keys-driven on BOTH halves
    from the live SoT — ``ID_PATTERNS`` for spec families (incl. MD) and
    ``TOOL_WRITE_ROADMAP_ID_FAMILIES`` / ``ROADMAP_ENTITY_ID_FAMILIES`` for the
    per-step entity families. Arm-level membership (split the alternation on
    ``|`` and compare whole arms) is immune to the MD-subset-of-D substring
    trap, where ``D-?\\d+`` is a literal substring of ``M\\d+-D-?\\d+``.
    """
    schema = load_schema("extract.schema.json")
    pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
    arms = pattern[2:-2].split("|")  # strip leading "^(" and trailing ")$"
    for family, body in ID_PATTERNS.items():  # MD, FR, NFR, SC, G, D
        assert body in arms, (
            f"ID_PATTERNS['{family}'] body {body!r} is not an exact "
            f"alternation arm of {arms!r}"
        )
    for prefix in TOOL_WRITE_ROADMAP_ID_FAMILIES["extract"]:
        body = ROADMAP_ENTITY_ID_FAMILIES[prefix]
        assert body in arms, (
            f"extract entity family {prefix!r} body {body!r} is not an exact "
            f"alternation arm of {arms!r}"
        )


def test_valid_output_passes_schema(extract_fixture: dict) -> None:
    schema = load_schema("extract.schema.json")
    assert validate_tool_output(extract_fixture, schema) == []


def test_phantom_field_type_fails(extract_fixture: dict) -> None:
    schema = load_schema("extract.schema.json")
    bad = json.loads(json.dumps(extract_fixture))
    # functional_requirements count must be an integer; a string is a violation.
    bad["frontmatter"]["functional_requirements"] = "two"
    errors = validate_tool_output(bad, schema)
    assert errors, "wrong type for a count field should fail schema validation"


def test_render_parity(extract_fixture: dict) -> None:
    """Side-by-side parity: rendered tool-write output mirrors markdown path."""
    rendered = render_tool_output(extract_fixture, TEMPLATES_DIR / "extract.md.j2")
    assert rendered.startswith("---")
    for header in _SECTION_HEADERS:
        assert header in rendered, f"missing section header: {header}"
    for fr in extract_fixture["functional_requirements"]:
        assert fr["id"] in rendered, f"FR id {fr['id']} not in rendered markdown"


def test_render_step_tool_write_roundtrip(extract_fixture: dict, tmp_path) -> None:
    out = tmp_path / "extraction.md"
    errors = render_step_tool_write("extract", json.dumps(extract_fixture), out)
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "extraction.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == extract_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "extraction.md"
    errors = render_step_tool_write("extract", "{not valid json", out)
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


def test_build_extract_prompt_tool_write_emits_json_contract() -> None:
    from pathlib import Path

    tw = build_extract_prompt(Path("s.md"), tool_write=True)
    assert "JSON" in tw
    assert "<output_format>" not in tw

    md = build_extract_prompt(Path("s.md"))
    assert "<output_format>" in md
