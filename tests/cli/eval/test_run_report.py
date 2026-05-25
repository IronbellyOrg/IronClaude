"""Tests for ``superclaude.cli.eval.run_report`` (FR-RPT1 / D-0054 / T03.11).

The aggregated run report writer is the file-emitting layer behind
COMP-008 Reporter (T03.13). These tests pin its three load-bearing
contracts:

* The FR-RPT1 N'-vs-K invariant — ``len(evals) ==
  counts.expanded_n_prime``. A mismatched summary raises
  :class:`ReporterContractViolation`, the exception carries exit code 2
  (``REPORTER_CONTRACT_VIOLATION_EXIT_CODE``), and no artefact is written
  before the exception fires.
* SKIPPED rows are included in ``evals[]`` with ``skip_reason``
  populated (design-spec §9 dimensional invariant).
* The three emitters (markdown, JSON, JUnit) produce byte-stable output
  for a given :class:`RunSummary` input — verified by hashing two
  independent calls for the same payload.
* The JSON emitter writes a payload that validates against
  ``summary.schema.json`` (DM-012 / T03.10).
* JUnit XML is feature-gated — it is only emitted when ``emit_junit=True``.
"""

from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from superclaude.cli.eval.models import (
    EvalOutcome,
    ExpectResult,
    RunCounts,
    RunSummary,
    RunTotals,
)
from superclaude.cli.eval.run_report import (
    REPORTER_CONTRACT_VIOLATION_EXIT_CODE,
    ReporterContractViolation,
    render_junit_xml,
    render_summary_json,
    render_summary_markdown,
    write_aggregated_report,
)
from superclaude.cli.eval.schemas import load_summary_schema

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _pass_outcome(eval_id: str = "E1") -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} sticky lifecycle",
        status="PASS",
        duration_sec=8.3,
        expects=(
            ExpectResult(name="file.exists", passed=True, message="ok"),
        ),
        artifacts={"stdout": f"evals/{eval_id}/stdout.log"},
    )


def _skipped_outcome(eval_id: str = "E2", reason: str = "capability_gate") -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} requires mcp",
        status="SKIPPED",
        duration_sec=0.0,
        skip_reason=reason,
        skip_flag_triggered="--no-mcp",
    )


def _fail_outcome(eval_id: str = "E3") -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} timeout fail-open",
        status="FAIL",
        duration_sec=12.0,
        expects=(
            ExpectResult(name="exit_code", passed=False, message="expected 0 got 1"),
        ),
        artifacts={"transcript": f"evals/{eval_id}/transcript.txt"},
    )


def _summary(
    *,
    evals: tuple[EvalOutcome, ...],
    manifest_n: int | None = None,
    expanded_n_prime: int | None = None,
    kept_k: int | None = None,
    skipped_s: int | None = None,
    finished_at: str = "2026-05-20T12:00:30Z",
    duration_sec: float = 30.0,
) -> RunSummary:
    """Build a RunSummary with auto-computed counts unless explicitly overridden."""

    auto_skipped = sum(1 for o in evals if o.status in {"SKIPPED", "INTERRUPTED"})
    auto_kept = len(evals) - auto_skipped
    expanded = expanded_n_prime if expanded_n_prime is not None else len(evals)
    kept = kept_k if kept_k is not None else auto_kept
    skipped = skipped_s if skipped_s is not None else auto_skipped
    manifest = manifest_n if manifest_n is not None else expanded

    counts = RunCounts(
        manifest_n=manifest,
        expanded_n_prime=expanded,
        kept_k=kept,
        skipped_s=skipped,
        kept_plus_skipped_equals_n_prime=(kept + skipped == expanded),
    )

    totals = RunTotals(
        passed=sum(1 for o in evals if o.status == "PASS"),
        failed=sum(1 for o in evals if o.status == "FAIL"),
        skipped=sum(1 for o in evals if o.status == "SKIPPED"),
        errored=sum(1 for o in evals if o.status == "ERRORED"),
        interrupted=sum(1 for o in evals if o.status == "INTERRUPTED"),
        timeout=sum(1 for o in evals if o.status == "TIMEOUT"),
    )

    return RunSummary(
        run_id="run-abc123",
        started_at="2026-05-20T12:00:00Z",
        finished_at=finished_at,
        duration_sec=duration_sec,
        suite="tests/fixtures/cliEval/real.yaml",
        manifest_version="1.0",
        parallel=8,
        counts=counts,
        totals=totals,
        evals=evals,
    )


@pytest.fixture(scope="module")
def schema_validator() -> Draft202012Validator:
    schema = dict(load_summary_schema())
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


# ---------------------------------------------------------------------------
# N'-vs-K invariant
# ---------------------------------------------------------------------------


def test_writer_raises_on_n_prime_vs_k_mismatch(tmp_path: Path) -> None:
    """Acceptance: mismatched summary (len(evals)=4 vs expanded=5) raises."""

    evals = tuple(_pass_outcome(f"E{i}") for i in range(4))
    summary = _summary(evals=evals, expanded_n_prime=5, kept_k=5, skipped_s=0)

    with pytest.raises(ReporterContractViolation) as exc_info:
        write_aggregated_report(summary, tmp_path)

    err = exc_info.value
    assert err.expected == 5
    assert err.actual == 4
    assert err.run_id == "run-abc123"
    assert not (tmp_path / "summary.md").exists(), "no file should be written"
    assert not (tmp_path / "summary.json").exists()


def test_reporter_contract_violation_exit_code_is_two() -> None:
    """Acceptance: violation maps to exit code 2."""

    assert REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2


def test_render_markdown_raises_on_mismatch() -> None:
    """The markdown renderer applies the same invariant as the writer."""

    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=2, kept_k=2)
    with pytest.raises(ReporterContractViolation):
        render_summary_markdown(summary)


def test_render_json_raises_on_mismatch() -> None:
    """The JSON renderer applies the same invariant as the writer."""

    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=3, kept_k=3)
    with pytest.raises(ReporterContractViolation):
        render_summary_json(summary)


def test_render_junit_raises_on_mismatch() -> None:
    """The JUnit renderer applies the same invariant as the writer."""

    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=4, kept_k=4)
    with pytest.raises(ReporterContractViolation):
        render_junit_xml(summary)


# ---------------------------------------------------------------------------
# SKIPPED rows kept in evals[]
# ---------------------------------------------------------------------------


def test_skipped_rows_present_in_evals_with_skip_reason(tmp_path: Path) -> None:
    """Acceptance: SKIPPED rows are included in evals[] with skip_reason populated."""

    evals = (
        _pass_outcome("E1"),
        _skipped_outcome("E2", reason="capability_gate:mcp_server.auggie"),
    )
    summary = _summary(evals=evals)
    written = write_aggregated_report(summary, tmp_path)

    payload = json.loads(written["summary.json"].read_text(encoding="utf-8"))
    statuses = [row["status"] for row in payload["evals"]]
    assert statuses == ["PASS", "SKIPPED"]
    skipped_row = payload["evals"][1]
    assert skipped_row["skip_reason"] == "capability_gate:mcp_server.auggie"
    assert skipped_row["skip_flag_triggered"] == "--no-mcp"


# ---------------------------------------------------------------------------
# Writer emits all three artifacts under the output dir
# ---------------------------------------------------------------------------


def test_writer_emits_markdown_json_and_yaml(tmp_path: Path) -> None:
    """Acceptance: writer emits summary.md + summary.json + summary.yaml by default.

    M4: ``summary.yaml`` is now unconditional, closing the +1 yaml divergence
    between ``write_aggregated_report`` and :meth:`Reporter.write`. Both
    surfaces delegate to the shared :func:`_write_artifact_set` helper.
    """

    summary = _summary(evals=(_pass_outcome("E1"), _skipped_outcome("E2")))
    written = write_aggregated_report(summary, tmp_path)

    assert (tmp_path / "summary.md").is_file()
    assert (tmp_path / "summary.json").is_file()
    assert (tmp_path / "summary.yaml").is_file()
    assert not (tmp_path / "junit.xml").exists()
    assert written == {
        "summary.md": tmp_path / "summary.md",
        "summary.json": tmp_path / "summary.json",
        "summary.yaml": tmp_path / "summary.yaml",
    }


def test_writer_emits_junit_when_requested(tmp_path: Path) -> None:
    """Acceptance: junit.xml is feature-gated and only emitted when requested."""

    summary = _summary(evals=(_pass_outcome("E1"),))
    written = write_aggregated_report(summary, tmp_path, emit_junit=True)

    assert (tmp_path / "junit.xml").is_file()
    assert "junit.xml" in written
    # The XML body must parse as a single <testsuite> element with one <testcase>.
    root = ET.fromstring((tmp_path / "junit.xml").read_text(encoding="utf-8"))
    assert root.tag == "testsuite"
    cases = list(root.findall("testcase"))
    assert [c.attrib["name"] for c in cases] == ["E1"]


def test_writer_creates_missing_output_dir(tmp_path: Path) -> None:
    """Writer mkdirs parents=True so the orchestrator does not need to pre-create."""

    target = tmp_path / "a" / "b" / "c"
    summary = _summary(evals=(_pass_outcome("E1"),))
    write_aggregated_report(summary, target)

    assert (target / "summary.md").is_file()
    assert (target / "summary.json").is_file()


# ---------------------------------------------------------------------------
# Byte-stable emitters
# ---------------------------------------------------------------------------


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_render_markdown_is_byte_stable() -> None:
    """Two independent renderings of the same RunSummary produce identical bytes."""

    summary = _summary(
        evals=(_pass_outcome("E1"), _skipped_outcome("E2"), _fail_outcome("E3"))
    )
    a = render_summary_markdown(summary)
    b = render_summary_markdown(summary)
    assert _sha256(a) == _sha256(b)


def test_render_json_is_byte_stable() -> None:
    """JSON output is byte-stable across independent invocations."""

    summary = _summary(
        evals=(_pass_outcome("E1"), _skipped_outcome("E2"), _fail_outcome("E3"))
    )
    a = render_summary_json(summary)
    b = render_summary_json(summary)
    assert _sha256(a) == _sha256(b)


def test_render_junit_is_byte_stable() -> None:
    """JUnit output is byte-stable across independent invocations."""

    summary = _summary(
        evals=(_pass_outcome("E1"), _skipped_outcome("E2"), _fail_outcome("E3"))
    )
    a = render_junit_xml(summary)
    b = render_junit_xml(summary)
    assert _sha256(a) == _sha256(b)


# ---------------------------------------------------------------------------
# Schema fidelity (JSON output validates against summary.schema.json)
# ---------------------------------------------------------------------------


def test_writer_json_validates_against_summary_schema(
    tmp_path: Path, schema_validator: Draft202012Validator
) -> None:
    """The JSON the writer drops on disk validates against DM-012."""

    summary = _summary(
        evals=(_pass_outcome("E1"), _skipped_outcome("E2"), _fail_outcome("E3"))
    )
    written = write_aggregated_report(summary, tmp_path)
    payload = json.loads(written["summary.json"].read_text(encoding="utf-8"))
    schema_validator.validate(payload)


# ---------------------------------------------------------------------------
# Markdown structural checks (the renderer surfaces required headers)
# ---------------------------------------------------------------------------


def test_markdown_contains_headline_and_result(tmp_path: Path) -> None:
    """Markdown carries the design-spec §9 header lines."""

    summary = _summary(evals=(_pass_outcome("E1"), _fail_outcome("E3")))
    body = render_summary_markdown(summary)
    assert body.startswith("# Eval Run: 2026-05-20T12:00:00Z / run-abc123")
    assert "**Suite:** tests/fixtures/cliEval/real.yaml" in body
    assert "## Result:" in body
    assert "1 passed, 1 failed" in body
    assert "## Failures (1)" in body
    assert "### E3:" in body
    # Counts block is present.
    assert "## Counts" in body
    assert "expanded_n_prime: 2" in body


def test_markdown_lists_skipped_with_reason() -> None:
    """SKIPPED rows show the skip reason in the table notes."""

    skipped = _skipped_outcome("E5", reason="capability_gate:mcp_server.tavily")
    summary = _summary(evals=(skipped,))
    body = render_summary_markdown(summary)
    assert "| E5 |" in body
    assert "capability_gate:mcp_server.tavily" in body


# ---------------------------------------------------------------------------
# JUnit XML structural checks
# ---------------------------------------------------------------------------


def test_junit_maps_status_to_correct_child_tag() -> None:
    """FAIL → <failure>, SKIPPED → <skipped>, ERRORED → <error>, PASS → bare."""

    errored = EvalOutcome(
        eval_id="E4",
        title="errored eval",
        status="ERRORED",
        duration_sec=1.0,
        error_class="builtins.RuntimeError",
    )
    summary = _summary(
        evals=(
            _pass_outcome("E1"),
            _fail_outcome("E2"),
            _skipped_outcome("E3"),
            errored,
        )
    )
    body = render_junit_xml(summary)
    root = ET.fromstring(body)
    by_name = {c.attrib["name"]: c for c in root.findall("testcase")}

    assert list(by_name["E1"]) == []  # PASS → no child
    assert by_name["E2"].find("failure") is not None
    assert by_name["E2"].find("failure").attrib["type"] == "FAIL"
    assert by_name["E3"].find("skipped") is not None
    assert by_name["E3"].find("skipped").attrib["message"] == "capability_gate"
    assert by_name["E4"].find("error") is not None
    assert by_name["E4"].find("error").attrib["message"] == "builtins.RuntimeError"


def test_junit_testsuite_attributes_reflect_counts() -> None:
    """Top-level <testsuite> tests= attribute reflects expanded_n_prime."""

    summary = _summary(
        evals=(_pass_outcome("E1"), _fail_outcome("E2"), _skipped_outcome("E3"))
    )
    body = render_junit_xml(summary)
    root = ET.fromstring(body)
    assert root.attrib["tests"] == "3"
    assert root.attrib["failures"] == "1"
    assert root.attrib["skipped"] == "1"


# ---------------------------------------------------------------------------
# Partial-summary path (SIGINT-style INTERRUPTED with finished_at='')
# ---------------------------------------------------------------------------


def test_writer_handles_partial_summary_with_interrupted_row(tmp_path: Path) -> None:
    """An INTERRUPTED row is written under a partial summary (finished_at='')."""

    interrupted = EvalOutcome(
        eval_id="E9",
        title="interrupted mid-run",
        status="INTERRUPTED",
        duration_sec=2.0,
    )
    summary = _summary(
        evals=(_pass_outcome("E1"), interrupted),
        finished_at="",
        duration_sec=2.0,
    )

    written = write_aggregated_report(summary, tmp_path)
    payload = json.loads(written["summary.json"].read_text(encoding="utf-8"))
    statuses = [row["status"] for row in payload["evals"]]
    assert statuses == ["PASS", "INTERRUPTED"]
    assert payload["finished_at"] == ""


# ---------------------------------------------------------------------------
# Reporter contract violation message carries diagnostic context
# ---------------------------------------------------------------------------


def test_reporter_contract_violation_message_includes_counts() -> None:
    """The exception message includes both sides of the mismatch + run_id."""

    summary = _summary(
        evals=(_pass_outcome("E1"),), expanded_n_prime=2, kept_k=2
    )
    with pytest.raises(ReporterContractViolation) as exc_info:
        render_summary_json(summary)

    msg = str(exc_info.value)
    assert "len(evals)=1" in msg
    assert "expanded_n_prime=2" in msg
    assert "run-abc123" in msg
