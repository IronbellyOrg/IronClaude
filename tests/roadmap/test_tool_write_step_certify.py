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
    """A representative, schema-valid certify output (certified=true, renders >=15 lines)."""
    return {
        "frontmatter": {
            "findings_verified": 3,
            "findings_passed": 3,
            "findings_failed": 0,
            "certified": True,
            "certification_date": "2026-06-02T00:00:00+00:00",
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
                "justification": "Dangling reference removed; cross-file refs resolve.",
            },
            {
                "finding_id": "F-03",
                "severity": "WARNING",
                "result": "PASS",
                "justification": "Compound deliverable split into two task rows.",
            },
        ],
        "summary": (
            "All 3 findings verified and passed. The remediation correctly "
            "addressed every blocking and warning finding."
        ),
    }


@pytest.fixture
def findings() -> list[Finding]:
    return [
        Finding(
            id="F-01",
            severity="BLOCKING",
            dimension="Schema",
            description="Milestone count mismatch",
            location="roadmap.md:12",
            evidence="frontmatter says 3, body has 5",
            fix_guidance="Update frontmatter milestone count",
        ),
    ]


def test_certify_schema_loads() -> None:
    schema = load_schema("certify.schema.json")
    assert isinstance(schema, dict)
    assert {"frontmatter", "results"} <= set(schema["required"])
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


def test_missing_results_fails(certify_fixture: dict) -> None:
    schema = load_schema("certify.schema.json")
    bad = json.loads(json.dumps(certify_fixture))
    del bad["results"]
    assert validate_tool_output(bad, schema), "missing required results should fail"


def test_invalid_result_value_fails(certify_fixture: dict) -> None:
    schema = load_schema("certify.schema.json")
    bad = json.loads(json.dumps(certify_fixture))
    bad["results"][0]["result"] = "MAYBE"
    assert validate_tool_output(bad, schema), "result outside PASS/FAIL enum should fail"


def test_render_parity(certify_fixture: dict) -> None:
    rendered = render_tool_output(certify_fixture, TEMPLATES_DIR / "certify.md.j2")
    assert rendered.startswith("---")
    assert "findings_verified:" in rendered
    assert "certified: true" in rendered
    assert "# Certification Report" in rendered
    assert "## Per-Finding Results" in rendered
    assert "| Finding | Severity | Result | Justification |" in rendered
    assert "| F-01 |" in rendered
    assert "## Summary" in rendered
    assert rendered.count("\n") >= 15


def test_rendered_satisfies_certify_gate(certify_fixture: dict, tmp_path) -> None:
    """The rendered tool-write output must PASS CERTIFY_GATE's runtime checks.

    Evaluated WITHOUT an envelope so the CI-only assert_step_reachable
    code-assertion is skipped (mirrors the production certify gate evaluation in
    _run_certify_after_remediate). The three runtime semantic checks
    (frontmatter_values_non_empty, per_finding_table_present, certified_is_true)
    plus required frontmatter + min_lines must hold.
    """
    out = tmp_path / "certification-report.md"
    out.write_text(
        render_tool_output(certify_fixture, TEMPLATES_DIR / "certify.md.j2"),
        encoding="utf-8",
    )
    passed, reason = gate_passed(out, CERTIFY_GATE)
    assert passed, f"rendered certify report failed CERTIFY_GATE: {reason}"


def test_render_step_tool_write_roundtrip(certify_fixture: dict, tmp_path) -> None:
    out = tmp_path / "certification-report.md"
    errors = render_step_tool_write("certify", json.dumps(certify_fixture), out)
    assert errors == []
    assert out.exists()
    assert out.read_text(encoding="utf-8").startswith("---")
    sidecar = tmp_path / "certification-report.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == certify_fixture


def test_render_step_tool_write_rejects_invalid(tmp_path) -> None:
    out = tmp_path / "certification-report.md"
    errors = render_step_tool_write("certify", "{not valid json", out)
    assert errors
    assert not out.exists()
    assert not (tmp_path / "certification-report.json").exists()


def test_certify_registry_key_distinct() -> None:
    spec = TOOL_WRITE_REGISTRY["certify"]
    assert spec.config_flag == "tool_write_certify"
    assert spec.step_id == "certify"
    assert spec.schema_name == "certify.schema.json"
    assert spec.template_name == "certify.md.j2"


def test_certify_tool_definition() -> None:
    td = _certify_tool_definition()
    assert td.name == "certify"
    assert td.input_schema == {}
    assert td.render_template == TEMPLATES_DIR / "certify.md.j2"
    assert "results" in set(td.output_schema["required"])


def test_build_prompt_tool_write_emits_json_contract(findings: list[Finding]) -> None:
    tw = build_certification_prompt(findings, {}, tool_write=True)
    assert "JSON" in tw
    # The legacy free-form output line must be gone in tool-write mode.
    assert "FINDING_ID: PASS|FAIL -- one-line justification" not in tw
    for key in ("frontmatter", "results", "summary", "findings_verified"):
        assert key in tw, f"tool-write prompt missing certify key: {key}"


def test_build_prompt_default_byte_identical(findings: list[Finding]) -> None:
    """The default markdown path must be byte-identical with/without tool_write=False."""
    default = build_certification_prompt(findings, {})
    explicit_false = build_certification_prompt(findings, {}, tool_write=False)
    assert default == explicit_false
    # Legacy output instruction present on the default path.
    assert "FINDING_ID: PASS|FAIL -- one-line justification" in default
