"""Tests for the R1.4 certify tool-write migration (Step 9.11, SECONDARY).

Mirrors ``test_tool_write_step_score.py`` for the certify step. The certify step
is a SECONDARY LLM step: it verifies that remediation fixes were applied
correctly and emits a per-finding PASS/FAIL verdict plus aggregate counts. It
carries NO ``roadmap_ids`` and therefore has NO §MVR §3 / Contract #3 phantom-ID
subset constraint -- the executor routes it through the PLAIN
``render_step_tool_write`` (not the id-check variant).

PRESERVE: the R1.3 CodeAssertion (``assert_step_reachable``) on CERTIFY_GATE is
unaffected -- tool-write only changes HOW the markdown report is produced, not
the dispatch reachability of the certify step. ``test_certify_prompts.py`` is the
unchanged-guarantee witness for the legacy markdown path.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.pipeline.gates import gate_passed
from superclaude.cli.roadmap.certify_prompts import (
    build_certification_prompt,
)
from superclaude.cli.roadmap.certify_prompts import (
    certify_tool_definition as _certify_tool_definition,
)
from superclaude.cli.roadmap.gates import CERTIFY_GATE
from superclaude.cli.roadmap.models import Finding
from superclaude.cli.roadmap.tool_writer import (
    TEMPLATES_DIR,
    TOOL_WRITE_REGISTRY,
    load_schema,
    render_step_tool_write,
    render_tool_output,
    validate_tool_output,
)


@pytest.fixture
def certify_fixture() -> dict:
    """A representative, schema-valid certify structured output.

    Renders >= 15 lines, carries the per-finding results table (header +
    >= 1 ``F-XX`` row) the gate's ``per_finding_table_present`` check requires,
    and ``certified: true`` so ``certified_is_true`` passes. All frontmatter
    values are non-empty.
    """
    return {
        "frontmatter": {
            "findings_verified": 3,
            "findings_passed": 3,
            "findings_failed": 0,
            "certified": True,
            "certification_date": "2026-06-02T00:00:00Z",
        },
        "results": [
            {
                "finding_id": "F-01",
                "severity": "BLOCKING",
                "result": "PASS",
                "justification": "Milestone count updated from 3 to 5 matching spec.",
            },
            {
                "finding_id": "F-02",
                "severity": "WARNING",
                "result": "PASS",
                "justification": "Heading hierarchy corrected; H2 > H3 restored.",
            },
            {
                "finding_id": "F-03",
                "severity": "BLOCKING",
                "result": "PASS",
                "justification": "Traceability gap closed; every FR maps to a deliverable.",
            },
        ],
        "summary": (
            "All 3 findings verified and passed. The roadmap is certified and "
            "ready for tasklist generation."
        ),
    }


def test_certify_schema_loads() -> None:
    schema = load_schema("certify.schema.json")
    assert isinstance(schema, dict)
    required = set(schema["required"])
    assert {"frontmatter", "results"} <= required
    fm_required = set(schema["properties"]["frontmatter"]["required"])
    assert {
        "findings_verified",
        "findings_passed",
        "findings_failed",
        "certified",
        "certification_date",
    } <= fm_required


def test_valid_output_passes_schema(certify_fixture: dict) -> None:
    schema = load_schema("certify.schema.json")
    assert validate_tool_output(certify_fixture, schema) == []


def test_missing_frontmatter_field_fails(certify_fixture: dict) -> None:
    schema = load_schema("certify.schema.json")
    bad = json.loads(json.dumps(certify_fixture))
    del bad["frontmatter"]["certified"]
    errors = validate_tool_output(bad, schema)
    assert errors, "missing required certified frontmatter field should fail"


def test_invalid_result_enum_fails(certify_fixture: dict) -> None:
    schema = load_schema("certify.schema.json")
    bad = json.loads(json.dumps(certify_fixture))
    bad["results"][0]["result"] = "MAYBE"
    errors = validate_tool_output(bad, schema)
    assert errors, "result outside PASS/FAIL enum should fail schema validation"


def test_result_requires_finding_id(certify_fixture: dict) -> None:
    schema = load_schema("certify.schema.json")
    bad = json.loads(json.dumps(certify_fixture))
    del bad["results"][0]["finding_id"]
    errors = validate_tool_output(bad, schema)
    assert errors, "results entry missing required finding_id should fail"


def test_render_parity(certify_fixture: dict) -> None:
    """Side-by-side parity: rendered output mirrors generate_certification_report."""
    rendered = render_tool_output(certify_fixture, TEMPLATES_DIR / "certify.md.j2")
    assert rendered.startswith("---")
    assert "findings_verified:" in rendered
    assert "certified: true" in rendered
    assert "# Certification Report" in rendered
    assert "## Per-Finding Results" in rendered
    assert "| Finding | Severity | Result | Justification |" in rendered
    assert "| F-01 |" in rendered
    assert "## Summary" in rendered


def test_rendered_certify_satisfies_gate(certify_fixture: dict) -> None:
    """The rendered tool-write output must PASS CERTIFY_GATE runtime checks.

    Evaluated without an envelope -- matching ``_run_certify_after_remediate``,
    which omits the CI-only ``assert_step_reachable`` CodeAssertion and runs only
    the three runtime-meaningful semantic checks (certified_is_true,
    per_finding_table_present, frontmatter_values_non_empty).
    """
    out_text = render_tool_output(certify_fixture, TEMPLATES_DIR / "certify.md.j2")
    for field in CERTIFY_GATE.required_frontmatter_fields:
        assert f"{field}:" in out_text, (
            f"required frontmatter field {field!r} missing from render"
        )
    assert out_text.count("\n") >= CERTIFY_GATE.min_lines


def test_render_step_tool_write_passes_gate(certify_fixture: dict, tmp_path) -> None:
    """Full pipeline-style check: render to disk then evaluate the real gate."""
    out = tmp_path / "certification-report.md"
    errors = render_step_tool_write("certify", json.dumps(certify_fixture), out)
    assert errors == []
    passed, reason = gate_passed(out, CERTIFY_GATE)
    assert passed, f"rendered certify must pass CERTIFY_GATE runtime checks: {reason}"


def test_render_step_tool_write_roundtrip(certify_fixture: dict, tmp_path) -> None:
    out = tmp_path / "certification-report.md"
    errors = render_step_tool_write("certify", json.dumps(certify_fixture), out)
    assert errors == []
    assert out.exists()
    markdown = out.read_text(encoding="utf-8")
    assert markdown.startswith("---")
    sidecar = tmp_path / "certification-report.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == certify_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "certification-report.md"
    errors = render_step_tool_write("certify", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "certification-report.json").exists()


def test_render_step_tool_write_dual_write_proof(
    certify_fixture: dict, tmp_path
) -> None:
    """Dual-write proof: the PASS path writes BOTH the .md artifact and .json sidecar."""
    out = tmp_path / "certification-report.md"
    sidecar = tmp_path / "certification-report.json"
    assert not out.exists()
    assert not sidecar.exists()
    errors = render_step_tool_write("certify", json.dumps(certify_fixture), out)
    assert errors == []
    assert out.exists(), "markdown artifact must be written on PASS"
    assert sidecar.exists(), "JSON sidecar must be written on PASS"
    assert json.loads(sidecar.read_text(encoding="utf-8")) == certify_fixture


def test_certify_registry_key_distinct() -> None:
    spec = TOOL_WRITE_REGISTRY["certify"]
    assert spec.config_flag == "tool_write_certify"
    assert spec.step_id == "certify"
    assert spec.schema_name == "certify.schema.json"
    assert spec.template_name == "certify.md.j2"


def test_certify_config_flag_defaults_false() -> None:
    """The new dual-write flag MUST default to False (deterministic path is production)."""
    from superclaude.cli.roadmap.models import RoadmapConfig

    config = RoadmapConfig(spec_file=Path("spec.md"), output_dir=Path("."))
    assert config.tool_write_certify is False


def test_certify_tool_definition() -> None:
    td = _certify_tool_definition()
    assert td.name == "certify"
    assert td.input_schema == {}
    assert td.render_template == TEMPLATES_DIR / "certify.md.j2"
    assert "results" in set(td.output_schema["required"])


def _make_findings() -> list[Finding]:
    return [
        Finding(
            id="F-01",
            severity="BLOCKING",
            dimension="Structure",
            description="Milestone count mismatch",
            location="roadmap.md:section 3",
            evidence="spec says 5, roadmap has 3",
            fix_guidance="Add the two missing milestones",
        ),
    ]


def test_build_certification_prompt_tool_write_emits_json_contract() -> None:
    tw = build_certification_prompt(
        findings=_make_findings(),
        context_sections={},
        tool_write=True,
    )
    assert "JSON" in tw
    assert "tool-write JSON mode" in tw
    # The legacy free-form output instruction must be gone in tool-write mode.
    assert "FINDING_ID: PASS|FAIL -- one-line justification" not in tw
    for key in ("frontmatter", "results", "summary"):
        assert key in tw, f"tool-write prompt missing certify key: {key}"


def test_build_certification_prompt_default_byte_identical() -> None:
    """The default markdown path must be byte-identical with/without tool_write=False.

    Guards the dual-write contract: enabling the flag changes ONLY the output
    block; the default production prompt (the verification checklist + the
    free-form FINDING_ID instruction) is unchanged.
    """
    findings = _make_findings()
    default = build_certification_prompt(findings=findings, context_sections={})
    explicit_false = build_certification_prompt(
        findings=findings, context_sections={}, tool_write=False
    )
    assert default == explicit_false
    # The default path retains the legacy free-form output instruction.
    assert "FINDING_ID: PASS|FAIL -- one-line justification" in default
