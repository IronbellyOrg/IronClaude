"""Tests for the R1.4 merge-step tool-write migration (Step 9.8).

The merge step is the SECOND primary phantom-ID source (master:§Top-3 #3): it
consumes two candidate roadmaps + diff + debate + score and produces the FINAL
merged roadmap, where the LLM can re-introduce ids absent from the spec. So the
load-bearing deliverable here -- exactly as for generate (Step 9.4) -- is the
GENERATION-TIME phantom-ID rejection: ``render_step_tool_write_with_id_check``
extracts ``roadmap_ids`` from the validated JSON and runs ``validate_id_subset``
against the spec's id universe BEFORE writing any artifact; a phantom id (e.g.
FR-99 absent from the extraction) is rejected and NEITHER the .md NOR the .json
sidecar is written.

These tests mirror ``test_tool_write_step_generate.py`` and additionally assert
the rendered output satisfies the STRICTer MERGE_GATE (which requires the
``adversarial`` frontmatter field plus the per-milestone Integration Points /
Milestone Dependencies subsections and the Resource Requirements External
Dependencies / Infrastructure Requirements subsections that generate does not).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.roadmap.gates import (
    MERGE_GATE,
    _deliverable_table_schema,
    _minimum_deliverable_rows,
    _no_duplicate_headings,
    _no_heading_gaps,
    _no_template_sentinels,
    _template_sections_present,
)
from superclaude.cli.roadmap.prompts import build_merge_prompt
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write_with_id_check,
    render_tool_output,
    validate_id_subset,
    validate_tool_output,
)
from superclaude.contracts import ID_PATTERNS


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


@pytest.fixture
def merge_fixture() -> dict:
    """A representative, schema-valid, MERGE_GATE-passing merged roadmap.

    Four milestones spanning 24 deliverable rows (>= the 20-row granularity
    floor), roadmap_ids listing every deliverable id, ``adversarial: true``
    frontmatter, and the per-milestone + resource subsections MERGE_GATE
    requires. Realistic in size so the rendered markdown clears the
    MERGE_GATE >= 150-line floor.
    """
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
            {"milestone": "M1", "title": "Foundation", "duration": "weeks 1-3",
             "exit_criteria": "FR-1..FR-3 implemented."},
            {"milestone": "M2", "title": "Core Logic", "duration": "weeks 4-6",
             "exit_criteria": "FR-4..FR-6 implemented."},
            {"milestone": "M3", "title": "Integration", "duration": "weeks 7-9",
             "exit_criteria": "FR-7..FR-9 implemented."},
            {"milestone": "M4", "title": "Hardening and Production Readiness",
             "duration": "weeks 10-12", "exit_criteria": "FR-10..FR-12 implemented."},
        ],
        "dependency_graph": "M1 -> M2 -> M3 -> M4",
        "milestones": [
            _milestone(
                "M1", "Foundation",
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
                "M2", "Core Logic",
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
                "M3", "Integration",
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
                "M4", "Hardening and Production Readiness",
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


def test_merge_schema_loads() -> None:
    schema = load_schema("merge.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "milestones", "roadmap_ids"} <= required
    fm = schema["properties"]["frontmatter"]
    assert {"complexity_score", "adversarial"} <= set(fm["required"])
    # spec_source / spec_sources is a one-of (mutual exclusion) at the gate.
    one_of_required = {tuple(branch["required"]) for branch in fm["oneOf"]}
    assert ("spec_source",) in one_of_required
    assert ("spec_sources",) in one_of_required


def test_merge_schema_id_pattern_matches_contracts() -> None:
    """The roadmap_ids pattern must embed every ID_PATTERNS family body AND the
    entity-family prefixes (DM-/API-/COMP-/TEST-/MIG-/OPS-).

    SoT-drift guard (Contract #8): the pattern is composed from the same
    families generate uses; this fails if contracts drift away from the schema.
    """
    schema = load_schema("merge.schema.json")
    pattern = schema["properties"]["roadmap_ids"]["items"]["pattern"]
    for family in ("FR", "NFR", "SC", "G", "D"):
        assert ID_PATTERNS[family] in pattern, (
            f"ID_PATTERNS['{family}'] body {ID_PATTERNS[family]!r} "
            f"missing from roadmap_ids pattern {pattern!r}"
        )
    for prefix in ("DM-", "API-", "COMP-", "TEST-", "MIG-", "OPS-"):
        assert prefix in pattern, (
            f"entity-family prefix {prefix!r} missing from "
            f"roadmap_ids pattern {pattern!r}"
        )


def test_merge_schema_matches_generate_id_pattern() -> None:
    """Merge reuses the SAME roadmap_ids pattern as generate (no divergence)."""
    merge_pattern = load_schema("merge.schema.json")[
        "properties"
    ]["roadmap_ids"]["items"]["pattern"]
    generate_pattern = load_schema("generate.schema.json")[
        "properties"
    ]["roadmap_ids"]["items"]["pattern"]
    assert merge_pattern == generate_pattern


def test_valid_output_passes_schema(merge_fixture: dict) -> None:
    schema = load_schema("merge.schema.json")
    assert validate_tool_output(merge_fixture, schema) == []


def test_missing_adversarial_fails_schema(merge_fixture: dict) -> None:
    schema = load_schema("merge.schema.json")
    bad = json.loads(json.dumps(merge_fixture))
    del bad["frontmatter"]["adversarial"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required 'adversarial' must fail schema validation"


def test_both_spec_source_keys_fails_schema(merge_fixture: dict) -> None:
    """The frontmatter oneOf forbids BOTH spec_source and spec_sources."""
    schema = load_schema("merge.schema.json")
    bad = json.loads(json.dumps(merge_fixture))
    bad["frontmatter"]["spec_sources"] = ["a.md", "b.md"]
    errors = validate_tool_output(bad, schema)
    assert errors, "supplying both spec_source and spec_sources must fail oneOf"


def test_missing_milestones_fails_schema(merge_fixture: dict) -> None:
    schema = load_schema("merge.schema.json")
    bad = json.loads(json.dumps(merge_fixture))
    del bad["milestones"]
    assert validate_tool_output(bad, schema), "missing 'milestones' must fail"
    bad2 = json.loads(json.dumps(merge_fixture))
    bad2["milestones"] = []
    assert validate_tool_output(bad2, schema), "empty milestones must fail minItems"


def test_render_parity(merge_fixture: dict) -> None:
    """Rendered tool-write output is a structurally complete merged roadmap."""
    rendered = render_tool_output(merge_fixture, TEMPLATES_DIR / "merge.md.j2")
    assert rendered.startswith("---")
    assert "## Executive Summary" in rendered
    assert "## Timeline Estimates" in rendered
    assert "## M1:" in rendered
    assert "| # | ID | Title |" in rendered
    # Realistic fixture renders >= 150 lines (MERGE_GATE floor).
    assert rendered.count("\n") >= 150, (
        f"render has {rendered.count(chr(10))} newlines, expected >= 150"
    )
    for rid in merge_fixture["roadmap_ids"]:
        assert rid in rendered, f"deliverable id {rid} not in rendered markdown"


def test_render_emits_adversarial_frontmatter_lowercase(merge_fixture: dict) -> None:
    """``adversarial`` renders as a lowercase YAML boolean (true/false)."""
    rendered = render_tool_output(merge_fixture, TEMPLATES_DIR / "merge.md.j2")
    assert "adversarial: true" in rendered
    other = json.loads(json.dumps(merge_fixture))
    other["frontmatter"]["adversarial"] = False
    assert "adversarial: false" in render_tool_output(
        other, TEMPLATES_DIR / "merge.md.j2"
    )


def test_rendered_merge_satisfies_gate_frontmatter(merge_fixture: dict) -> None:
    """The rendered tool-write output must PASS MERGE_GATE frontmatter + the key
    semantic checks (sections present, 9-col schema, >=20 rows, no gaps/dups/
    sentinels) and the >= min_lines floor."""
    rendered = render_tool_output(merge_fixture, TEMPLATES_DIR / "merge.md.j2")

    for field in MERGE_GATE.required_frontmatter_fields:
        if isinstance(field, tuple):
            assert any(f"{alias}:" in rendered for alias in field), (
                f"none of the aliases {field} appear as a key: line in render"
            )
        else:
            assert f"{field}:" in rendered, (
                f"required frontmatter field {field!r} missing from render"
            )

    assert rendered.count("\n") >= MERGE_GATE.min_lines, (
        f"render has {rendered.count(chr(10))} newlines, "
        f"gate requires >= {MERGE_GATE.min_lines}"
    )

    # Key semantic checks from MERGE_GATE.
    assert _template_sections_present(rendered) is True
    assert _deliverable_table_schema(rendered) is True
    assert _minimum_deliverable_rows(rendered) is True
    assert _no_heading_gaps(rendered) is True
    assert _no_template_sentinels(rendered) is True
    assert _no_duplicate_headings(rendered) is True


def test_merge_rejects_phantom_id(merge_fixture: dict, tmp_path) -> None:
    """CRITICAL (Contract #3): merge rejects phantom ids AT GENERATION TIME.

    Mirrors generate's phantom test: a roadmap_id absent from spec_ids causes
    ``render_step_tool_write_with_id_check`` to return errors and write NEITHER
    the .md NOR the .json sidecar.
    """
    spec_ids = set(merge_fixture["roadmap_ids"])

    # 1. Direct validate_id_subset behavior.
    errors = validate_id_subset(["FR-1", "FR-99"], spec_ids=spec_ids)
    assert errors and any("FR-99" in e for e in errors), (
        "phantom FR-99 must be rejected by validate_id_subset"
    )
    assert validate_id_subset(["FR-1", "FR-2"], spec_ids=spec_ids) == []

    # 2. Phantom id in roadmap_ids -> rejected at generation time, no .md/.json.
    phantom_fixture = json.loads(json.dumps(merge_fixture))
    phantom_fixture["roadmap_ids"] = phantom_fixture["roadmap_ids"] + ["FR-99"]
    out = tmp_path / "merged.md"
    tw_errors = render_step_tool_write_with_id_check(
        "merge",
        json.dumps(phantom_fixture),
        out,
        spec_ids=spec_ids,
    )
    assert tw_errors and any("FR-99" in e for e in tw_errors), (
        "phantom id must be rejected by render_step_tool_write_with_id_check"
    )
    assert not out.exists(), "no .md may be written when a phantom id is present"
    assert not (tmp_path / "merged.json").exists(), (
        "no JSON sidecar may be written when a phantom id is present"
    )

    # 3. Clean fixture (roadmap_ids subset of spec_ids) -> PASS, .md + sidecar.
    clean_out = tmp_path / "merged_clean.md"
    clean_errors = render_step_tool_write_with_id_check(
        "merge",
        json.dumps(merge_fixture),
        clean_out,
        spec_ids=spec_ids,
    )
    assert clean_errors == []
    assert clean_out.exists()
    assert clean_out.read_text(encoding="utf-8").startswith("---")
    sidecar = tmp_path / "merged_clean.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == merge_fixture


def test_id_check_skips_when_spec_ids_empty(merge_fixture: dict, tmp_path) -> None:
    """Empty spec_ids -> subset check skipped (identity); render still runs."""
    out = tmp_path / "merged.md"
    phantom_fixture = json.loads(json.dumps(merge_fixture))
    phantom_fixture["roadmap_ids"] = phantom_fixture["roadmap_ids"] + ["FR-99"]
    errors = render_step_tool_write_with_id_check(
        "merge",
        json.dumps(phantom_fixture),
        out,
        spec_ids=set(),
    )
    assert errors == []
    assert out.exists()


def test_render_step_tool_write_with_id_check_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "merged.md"
    errors = render_step_tool_write_with_id_check(
        "merge", "{not valid json", out, spec_ids={"FR-1"}
    )
    assert errors
    assert not out.exists()
    assert not (tmp_path / "merged.json").exists()


def test_merge_registry_key_distinct() -> None:
    """The merge registry entry maps the right config flag + step_id."""
    assert TOOL_WRITE_REGISTRY["merge"].step_id == "merge"
    assert TOOL_WRITE_REGISTRY["merge"].config_flag == "tool_write_merge"
    assert TOOL_WRITE_REGISTRY["merge"].schema_name == "merge.schema.json"
    assert TOOL_WRITE_REGISTRY["merge"].template_name == "merge.md.j2"


def test_build_merge_prompt_tool_write_emits_json_contract() -> None:
    tw = build_merge_prompt(
        Path("score.md"), Path("a.md"), Path("b.md"), Path("debate.md"),
        tool_write=True,
    )
    assert "JSON" in tw
    assert "<output_format>" not in tw
    for key in ("milestones", "deliverables", "roadmap_ids", "adversarial"):
        assert key in tw, f"tool-write prompt missing key: {key}"
    # Phantom-ID guidance present.
    assert "phantom" in tw.lower()

    # Default (markdown/incremental) path unchanged: contains the output_format
    # behavior and the incremental completeness checklist.
    md = build_merge_prompt(
        Path("score.md"), Path("a.md"), Path("b.md"), Path("debate.md")
    )
    assert "<output_format>" in md
    assert "INCREMENTAL_WRITE_COMPLETE" in md


def test_build_merge_prompt_default_byte_identical() -> None:
    """The default (flag=False) prompt is byte-identical to omitting the param
    entirely -- the dual-write switch is purely additive."""
    args = (Path("score.md"), Path("a.md"), Path("b.md"), Path("debate.md"))
    assert build_merge_prompt(*args) == build_merge_prompt(*args, tool_write=False)
