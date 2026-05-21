"""TEST-007 Reporter contract tests (R-078 / D-0078 / T04.17).

The Reporter (COMP-008 / T03.13) is the contractually-pinned surface
that downstream consumers (CI summary jobs, the JUnit pipeline, the
``superclaude eval run`` exit-code dispatcher) read. Four FR-RPT1 +
DM-012 obligations have to hold for any caller that turns a
:class:`RunSummary` into bytes:

1. **N'-vs-K equality** — ``len(summary.evals) ==
   counts.expanded_n_prime``. A summary that satisfies the dimensional
   invariant must render through every emitter (``to_markdown``,
   ``to_json``, ``to_yaml``, ``to_junit``) without raising.

2. **SKIPPED inclusion** — design-spec §9 declares that SKIPPED rows
   stay in ``evals[]`` (with ``skip_reason`` populated) so the row
   accounting never tries to "compress" the array. The JSON the
   Reporter writes must surface those rows verbatim — both at the row
   level (``evals[].status == "SKIPPED"`` with ``skip_reason``) and at
   the count level (``counts.skipped_s`` reflects the tally).

3. **Mismatch failure → exit code 2** — when the invariant is
   violated, every emitter raises :class:`ReporterContractViolation`
   *before* writing any artefact, and the violation maps to process
   exit code 2 (``REPORTER_CONTRACT_VIOLATION_EXIT_CODE``). Design-spec
   §4 classifies a Reporter contract violation as a harness contract
   error: the orchestrator's accounting and the rendered ``evals[]``
   disagree, so the run itself is suspect and no partial artefact is
   allowed on disk.

4. **JSON schema fidelity** — the JSON payload the Reporter renders
   validates against ``summary.schema.json`` (DM-012 / T03.10). This
   is the cross-link FR-RPT1 ↔ DM-012: the schema documents the shape
   the Reporter contracts to write.

These four scenarios anchor TEST-007 in the phase-4 tasklist
(``§T04.17``). The test module is deliberately self-contained — it
builds RunSummary fixtures from scratch rather than reusing
``test_run_report.py`` helpers — so a future refactor of the writer
helpers cannot quietly drop the contract guarantees this module pins.
"""

from __future__ import annotations

import json
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
from superclaude.cli.eval.reporter import Reporter
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
# RunSummary fixture helpers
# ---------------------------------------------------------------------------


def _pass(eval_id: str) -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} pass",
        status="PASS",
        duration_sec=1.5,
        expects=(ExpectResult(name="exit_code", passed=True, message="ok"),),
        artifacts={"stdout": f"evals/{eval_id}/stdout.log"},
    )


def _skipped(eval_id: str, reason: str = "capability_gate:mcp_server.tavily") -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} skipped",
        status="SKIPPED",
        duration_sec=0.0,
        skip_reason=reason,
        skip_flag_triggered="--no-mcp",
    )


def _fail(eval_id: str) -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} fail",
        status="FAIL",
        duration_sec=3.25,
        expects=(
            ExpectResult(name="exit_code", passed=False, message="expected 0 got 1"),
        ),
    )


def _summary(
    *,
    evals: tuple[EvalOutcome, ...],
    expanded_n_prime: int | None = None,
    kept_k: int | None = None,
    skipped_s: int | None = None,
) -> RunSummary:
    """Build a RunSummary with auto-derived counts unless overridden.

    Overriding ``expanded_n_prime`` to a value other than ``len(evals)``
    is the canonical way to construct the *mismatch* fixture: the
    Reporter sees ``len(evals) != expanded_n_prime`` and raises.
    """

    auto_skipped = sum(1 for o in evals if o.status in {"SKIPPED", "INTERRUPTED"})
    auto_kept = len(evals) - auto_skipped
    expanded = expanded_n_prime if expanded_n_prime is not None else len(evals)
    kept = kept_k if kept_k is not None else auto_kept
    skipped = skipped_s if skipped_s is not None else auto_skipped

    counts = RunCounts(
        manifest_n=expanded,
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
        run_id="run-test007",
        started_at="2026-05-20T12:00:00Z",
        finished_at="2026-05-20T12:00:30Z",
        duration_sec=30.0,
        suite="tests/fixtures/cliEval/real.yaml",
        manifest_version="1.0",
        parallel=4,
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
# Scenario 1 — N'-vs-K equality lets every emitter render
# ---------------------------------------------------------------------------


def test_n_prime_equals_k_lets_every_emitter_render(tmp_path: Path) -> None:
    """FR-RPT1 scenario 1: ``len(evals) == counts.expanded_n_prime`` →
    every Reporter emitter renders without raising and the writer drops
    the canonical artefact set on disk.

    Pins:
    * ``Reporter.to_markdown / to_json / to_yaml / to_junit`` all succeed.
    * ``Reporter(emit_junit=True).write(...)`` emits exactly the 4
      artefacts under the chosen output directory.
    * ``counts.expanded_n_prime`` matches both ``len(evals)`` and the
      ``tests=`` attribute the JUnit ``<testsuite>`` advertises.
    """

    evals = (_pass("E1"), _pass("E2"), _fail("E3"))
    summary = _summary(evals=evals)

    # Sanity: dimensional invariant holds on the fixture itself.
    assert summary.counts.expanded_n_prime == len(summary.evals)

    reporter = Reporter(summary, emit_junit=True)

    # Each emitter renders without raising.
    md = reporter.to_markdown()
    js = reporter.to_json()
    yml = reporter.to_yaml()
    xml = reporter.to_junit()
    assert md and js and yml and xml, "every emitter must return non-empty output"

    # The writer drops the full artefact set under tmp_path.
    written = reporter.write(tmp_path)
    assert set(written) == {"summary.md", "summary.json", "summary.yaml", "junit.xml"}
    for path in written.values():
        assert path.is_file(), f"writer should have created {path}"

    # JSON ``evals[]`` length matches ``counts.expanded_n_prime``.
    payload = json.loads(written["summary.json"].read_text(encoding="utf-8"))
    assert len(payload["evals"]) == payload["counts"]["expanded_n_prime"] == 3

    # JUnit ``<testsuite tests="...">`` mirrors the same count.
    import xml.etree.ElementTree as ET

    root = ET.fromstring(written["junit.xml"].read_text(encoding="utf-8"))
    assert root.attrib["tests"] == "3"


# ---------------------------------------------------------------------------
# Scenario 2 — SKIPPED rows stay in evals[] with skip_reason populated
# ---------------------------------------------------------------------------


def test_skipped_rows_included_in_evals_with_skip_reason(tmp_path: Path) -> None:
    """FR-RPT1 scenario 2: SKIPPED rows are preserved in ``evals[]`` with
    ``skip_reason`` populated, and the count tally reflects them.

    Pins design-spec §9: the Reporter must not "compress" SKIPPED rows
    out of the array — every expanded eval gets a slot whether or not
    it ran. The row-level fields (``status``, ``skip_reason``,
    ``skip_flag_triggered``) round-trip through the JSON payload
    verbatim, and ``counts.skipped_s + counts.kept_k`` equals
    ``counts.expanded_n_prime``.
    """

    evals = (
        _pass("E1"),
        _skipped("E2", reason="capability_gate:mcp_server.auggie"),
        _skipped("E3", reason="--no-pty"),
        _fail("E4"),
    )
    summary = _summary(evals=evals)
    written = write_aggregated_report(summary, tmp_path)
    payload = json.loads(written["summary.json"].read_text(encoding="utf-8"))

    # All four rows survive — none of them is collapsed out.
    assert [row["eval_id"] for row in payload["evals"]] == ["E1", "E2", "E3", "E4"]
    statuses = [row["status"] for row in payload["evals"]]
    assert statuses == ["PASS", "SKIPPED", "SKIPPED", "FAIL"]

    # SKIPPED rows carry skip_reason + skip_flag_triggered verbatim.
    e2 = payload["evals"][1]
    e3 = payload["evals"][2]
    assert e2["skip_reason"] == "capability_gate:mcp_server.auggie"
    assert e2["skip_flag_triggered"] == "--no-mcp"
    assert e3["skip_reason"] == "--no-pty"
    assert e3["skip_flag_triggered"] == "--no-mcp"

    # Counts reflect the tally.
    counts = payload["counts"]
    assert counts["expanded_n_prime"] == 4
    assert counts["skipped_s"] == 2
    assert counts["kept_k"] == 2
    assert counts["kept_plus_skipped_equals_n_prime"] is True

    # Per-status totals also reflect the SKIPPED rows.
    totals = payload["totals"]
    assert totals["skipped"] == 2
    assert totals["passed"] == 1
    assert totals["failed"] == 1

    # The markdown table surfaces the SKIPPED rows + their reasons too.
    md_body = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "| E2 |" in md_body
    assert "capability_gate:mcp_server.auggie" in md_body
    assert "| E3 |" in md_body
    assert "--no-pty" in md_body


# ---------------------------------------------------------------------------
# Scenario 3 — N'-vs-K mismatch raises ReporterContractViolation and maps to
# process exit code 2 (REPORTER_CONTRACT_VIOLATION_EXIT_CODE)
# ---------------------------------------------------------------------------


def test_n_prime_vs_k_mismatch_raises_and_maps_to_exit_code_two(
    tmp_path: Path,
) -> None:
    """FR-RPT1 scenario 3: a mismatched summary
    (``len(evals) != counts.expanded_n_prime``) raises
    :class:`ReporterContractViolation` from every emitter and the
    writer, and that violation is the contract-defined exit-code-2 path
    (design-spec §4 / ``REPORTER_CONTRACT_VIOLATION_EXIT_CODE``).

    Pins:
    * Each of ``to_markdown`` / ``to_json`` / ``to_yaml`` / ``to_junit``
      raises.
    * ``write_aggregated_report`` raises *before* any artefact is
      created on disk (no partial summary).
    * The dispatch-time exit code constant is 2 — design-spec §4
      classifies harness contract errors at this code, and the runner
      / CLI dispatcher catches the exception and exits with this value.
    * The exception message carries both sides of the mismatch + the
      run_id so the CI log shows which run produced the violation.
    """

    # Build a mismatched summary: 2 evals declared but expanded_n_prime=3.
    evals = (_pass("E1"), _pass("E2"))
    summary = _summary(evals=evals, expanded_n_prime=3, kept_k=3, skipped_s=0)
    assert summary.counts.expanded_n_prime != len(summary.evals)

    # Every single-format emitter on the Reporter wrapper raises.
    reporter = Reporter(summary, emit_junit=True)
    for emitter_name in ("to_markdown", "to_json", "to_yaml", "to_junit"):
        with pytest.raises(ReporterContractViolation):
            getattr(reporter, emitter_name)()

    # The module-level renderers also raise (they are the source of truth).
    with pytest.raises(ReporterContractViolation):
        render_summary_markdown(summary)
    with pytest.raises(ReporterContractViolation):
        render_summary_json(summary)
    with pytest.raises(ReporterContractViolation):
        render_junit_xml(summary)

    # write() / write_aggregated_report() raise *before* any file is created.
    target = tmp_path / "out"
    with pytest.raises(ReporterContractViolation) as exc_info:
        reporter.write(target)
    assert not (target / "summary.md").exists()
    assert not (target / "summary.json").exists()
    assert not (target / "summary.yaml").exists()
    assert not (target / "junit.xml").exists()

    target2 = tmp_path / "out2"
    with pytest.raises(ReporterContractViolation) as writer_exc:
        write_aggregated_report(summary, target2)
    assert not (target2 / "summary.md").exists()
    assert not (target2 / "summary.json").exists()

    # Diagnostic shape on the exception itself.
    err = exc_info.value
    assert err.expected == 3
    assert err.actual == 2
    assert err.run_id == "run-test007"
    msg = str(err)
    assert "len(evals)=2" in msg
    assert "expanded_n_prime=3" in msg
    assert "run-test007" in msg

    # The violation is the design-spec §4 exit-code-2 path.
    assert REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2
    # And the exception type itself is the one a CLI dispatcher catches.
    assert isinstance(writer_exc.value, ReporterContractViolation)


# ---------------------------------------------------------------------------
# Scenario 4 — JSON schema fidelity
# ---------------------------------------------------------------------------


def test_reporter_json_validates_against_summary_schema(
    tmp_path: Path, schema_validator: Draft202012Validator
) -> None:
    """FR-RPT1 ↔ DM-012 scenario 4: the JSON payload the Reporter renders
    validates against ``summary.schema.json``.

    Pins the cross-link between FR-RPT1 (the writer) and DM-012 (the
    contract). A summary covering every distinct row class — PASS,
    SKIPPED, FAIL, ERRORED — must validate cleanly. The check runs
    twice: once on the in-memory string from
    :meth:`Reporter.to_json` and once on the bytes the writer drops to
    disk via :meth:`Reporter.write`. Both must be schema-valid so a
    refactor cannot silently diverge the two surfaces.
    """

    errored = EvalOutcome(
        eval_id="E5",
        title="errored eval",
        status="ERRORED",
        duration_sec=2.0,
        error_class="builtins.RuntimeError",
    )
    summary = _summary(evals=(_pass("E1"), _skipped("E2"), _fail("E3"), errored))

    # 1) The in-memory JSON string validates.
    reporter = Reporter(summary)
    in_memory_payload = json.loads(reporter.to_json())
    schema_validator.validate(in_memory_payload)

    # 2) The on-disk JSON file validates (and matches the in-memory copy).
    written = reporter.write(tmp_path)
    on_disk_payload = json.loads(written["summary.json"].read_text(encoding="utf-8"))
    schema_validator.validate(on_disk_payload)
    assert on_disk_payload == in_memory_payload, (
        "Reporter.to_json() and the file write must produce identical payloads"
    )

    # The payload covers every distinct DM-012 row shape (PASS, SKIPPED,
    # FAIL, ERRORED) so the schema fidelity check exercises every
    # ``oneOf`` branch the schema declares.
    statuses = {row["status"] for row in on_disk_payload["evals"]}
    assert statuses == {"PASS", "SKIPPED", "FAIL", "ERRORED"}
