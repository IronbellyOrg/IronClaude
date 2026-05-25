"""Tests for ``superclaude.cli.eval.reporter`` (COMP-008 / D-0055 / T03.13).

The :class:`Reporter` class is the OO surface that wraps a
:class:`RunSummary` and exposes the four canonical emitter methods
declared by COMP-008. These tests pin the load-bearing acceptance
criteria from the roadmap row:

* ``Reporter`` exposes ``to_markdown()``, ``to_yaml()``, ``to_json()``,
  ``to_junit()`` and the assertion guard fires *before* any emitter
  writes output on mismatch.
* All four emitter outputs are byte-stable for a given ``RunSummary``
  input (verified by hashing two independent calls).
* JUnit XML is feature-gated: :meth:`Reporter.write` only writes
  ``junit.xml`` when ``emit_junit=True``; calling ``to_junit()`` is
  itself the explicit request and is always valid.
* :class:`AggregatedRunReport` is an alias of :class:`Reporter` (the
  roadmap row uses the two names interchangeably).
"""

from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml

from superclaude.cli.eval.models import (
    EvalOutcome,
    ExpectResult,
    RunCounts,
    RunSummary,
    RunTotals,
)
from superclaude.cli.eval.reporter import (
    AggregatedRunReport,
    Reporter,
    render_summary_yaml,
)
from superclaude.cli.eval.run_report import (
    REPORTER_CONTRACT_VIOLATION_EXIT_CODE,
    ReporterContractViolation,
)

# ---------------------------------------------------------------------------
# Fixtures (mirror tests/cli/eval/test_run_report.py shape)
# ---------------------------------------------------------------------------


def _pass_outcome(eval_id: str = "E1") -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title=f"{eval_id} sticky lifecycle",
        status="PASS",
        duration_sec=8.3,
        expects=(ExpectResult(name="file.exists", passed=True, message="ok"),),
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
        expects=(ExpectResult(name="exit_code", passed=False, message="expected 0 got 1"),),
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


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Reporter surface — 4 emitter methods are present
# ---------------------------------------------------------------------------


def test_reporter_exposes_four_emitter_methods() -> None:
    """Acceptance: ``Reporter`` exposes ``to_markdown/yaml/json/junit``."""

    summary = _summary(evals=(_pass_outcome("E1"),))
    reporter = Reporter(summary)

    assert callable(getattr(reporter, "to_markdown"))
    assert callable(getattr(reporter, "to_yaml"))
    assert callable(getattr(reporter, "to_json"))
    assert callable(getattr(reporter, "to_junit"))


def test_aggregated_run_report_is_reporter_alias() -> None:
    """``AggregatedRunReport`` and ``Reporter`` are the same class."""

    assert AggregatedRunReport is Reporter


# ---------------------------------------------------------------------------
# Contract guard fires before any emitter writes output on mismatch
# ---------------------------------------------------------------------------


def test_to_markdown_raises_on_mismatch() -> None:
    """The class delegate fires the same N'-vs-K guard the module renderer does."""

    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=2, kept_k=2)
    reporter = Reporter(summary)
    with pytest.raises(ReporterContractViolation):
        reporter.to_markdown()


def test_to_yaml_raises_on_mismatch() -> None:
    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=3, kept_k=3)
    reporter = Reporter(summary)
    with pytest.raises(ReporterContractViolation):
        reporter.to_yaml()


def test_to_json_raises_on_mismatch() -> None:
    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=4, kept_k=4)
    reporter = Reporter(summary)
    with pytest.raises(ReporterContractViolation):
        reporter.to_json()


def test_to_junit_raises_on_mismatch() -> None:
    summary = _summary(evals=(_pass_outcome("E1"),), expanded_n_prime=5, kept_k=5)
    reporter = Reporter(summary)
    with pytest.raises(ReporterContractViolation):
        reporter.to_junit()


def test_write_raises_before_any_file_is_written(tmp_path: Path) -> None:
    """Mismatched summary: write() raises *before* mkdir / file emission."""

    evals = tuple(_pass_outcome(f"E{i}") for i in range(4))
    summary = _summary(evals=evals, expanded_n_prime=5, kept_k=5, skipped_s=0)
    reporter = Reporter(summary, emit_junit=True)

    target = tmp_path / "report"
    with pytest.raises(ReporterContractViolation):
        reporter.write(target)

    assert not target.exists(), "no directory should be created on contract violation"


def test_reporter_contract_violation_exit_code_is_two() -> None:
    """The exit-code constant exported by ``run_report`` stays at 2."""

    assert REPORTER_CONTRACT_VIOLATION_EXIT_CODE == 2


# ---------------------------------------------------------------------------
# Byte-stable emitters (all four)
# ---------------------------------------------------------------------------


def _stable_summary() -> RunSummary:
    return _summary(
        evals=(_pass_outcome("E1"), _skipped_outcome("E2"), _fail_outcome("E3"))
    )


def test_to_markdown_is_byte_stable() -> None:
    reporter = Reporter(_stable_summary())
    a = reporter.to_markdown()
    b = reporter.to_markdown()
    assert _sha256(a) == _sha256(b)


def test_to_yaml_is_byte_stable() -> None:
    reporter = Reporter(_stable_summary())
    a = reporter.to_yaml()
    b = reporter.to_yaml()
    assert _sha256(a) == _sha256(b)


def test_to_json_is_byte_stable() -> None:
    reporter = Reporter(_stable_summary())
    a = reporter.to_json()
    b = reporter.to_json()
    assert _sha256(a) == _sha256(b)


def test_to_junit_is_byte_stable() -> None:
    reporter = Reporter(_stable_summary())
    a = reporter.to_junit()
    b = reporter.to_junit()
    assert _sha256(a) == _sha256(b)


# ---------------------------------------------------------------------------
# YAML rendering — shape and round-trip
# ---------------------------------------------------------------------------


def test_to_yaml_round_trips_to_summary_dict() -> None:
    """YAML rendering parses back to the canonical ``summary.to_dict()`` payload."""

    summary = _stable_summary()
    reporter = Reporter(summary)
    body = reporter.to_yaml()
    parsed = yaml.safe_load(body)
    assert parsed == summary.to_dict()


def test_render_summary_yaml_module_function_matches_method() -> None:
    """The module-level renderer and the class delegate produce identical output."""

    summary = _stable_summary()
    reporter = Reporter(summary)
    assert reporter.to_yaml() == render_summary_yaml(summary)


def test_to_yaml_preserves_dm_004_field_order() -> None:
    """YAML keeps the DM-004 declaration order at the top level."""

    summary = _stable_summary()
    body = Reporter(summary).to_yaml()
    # Collect top-level keys in document order by scanning the YAML body
    # for left-margin keys (every top-level key starts at column 0).
    top_keys = [
        line.split(":", 1)[0]
        for line in body.splitlines()
        if line and not line.startswith(" ") and not line.startswith("-")
        and ":" in line
    ]
    assert top_keys == [
        "run_id",
        "started_at",
        "finished_at",
        "duration_sec",
        "suite",
        "manifest_version",
        "parallel",
        "counts",
        "totals",
        "evals",
        "artifacts",
    ]


# ---------------------------------------------------------------------------
# JUnit feature gate — write() skips junit.xml unless emit_junit=True
# ---------------------------------------------------------------------------


def test_write_default_skips_junit_xml(tmp_path: Path) -> None:
    """Acceptance: junit.xml is feature-gated — default write() does not emit it."""

    reporter = Reporter(_stable_summary())  # emit_junit defaults to False
    written = reporter.write(tmp_path)

    assert (tmp_path / "summary.md").is_file()
    assert (tmp_path / "summary.json").is_file()
    assert (tmp_path / "summary.yaml").is_file()
    assert not (tmp_path / "junit.xml").exists()
    assert "junit.xml" not in written


def test_write_emits_junit_when_flag_set(tmp_path: Path) -> None:
    """Acceptance: emit_junit=True writes junit.xml alongside the other artefacts."""

    reporter = Reporter(_stable_summary(), emit_junit=True)
    written = reporter.write(tmp_path)

    assert (tmp_path / "junit.xml").is_file()
    assert written["junit.xml"] == tmp_path / "junit.xml"
    # The XML body must parse as a single <testsuite> element.
    root = ET.fromstring((tmp_path / "junit.xml").read_text(encoding="utf-8"))
    assert root.tag == "testsuite"


def test_to_junit_callable_regardless_of_flag() -> None:
    """``to_junit()`` is the explicit request — always callable directly."""

    summary = _stable_summary()
    # emit_junit defaults to False but the method is still callable.
    body = Reporter(summary).to_junit()
    root = ET.fromstring(body)
    assert root.tag == "testsuite"


# ---------------------------------------------------------------------------
# Class delegate outputs match module-level renderer outputs
# ---------------------------------------------------------------------------


def test_to_markdown_matches_module_renderer() -> None:
    from superclaude.cli.eval.run_report import render_summary_markdown

    summary = _stable_summary()
    assert Reporter(summary).to_markdown() == render_summary_markdown(summary)


def test_to_json_matches_module_renderer() -> None:
    from superclaude.cli.eval.run_report import render_summary_json

    summary = _stable_summary()
    assert Reporter(summary).to_json() == render_summary_json(summary)


def test_to_junit_matches_module_renderer() -> None:
    from superclaude.cli.eval.run_report import render_junit_xml

    summary = _stable_summary()
    assert Reporter(summary).to_junit() == render_junit_xml(summary)


# ---------------------------------------------------------------------------
# write() emits the standard triplet and the artefact paths are returned
# ---------------------------------------------------------------------------


def test_write_returns_artifact_path_mapping(tmp_path: Path) -> None:
    """write() returns a mapping of artifact-name → Path for every file written."""

    reporter = Reporter(_stable_summary(), emit_junit=True)
    written = reporter.write(tmp_path)

    assert set(written.keys()) == {
        "summary.md",
        "summary.json",
        "summary.yaml",
        "junit.xml",
    }
    for name, path in written.items():
        assert path == tmp_path / name
        assert path.is_file()


def test_write_creates_missing_output_dir(tmp_path: Path) -> None:
    target = tmp_path / "deep" / "nested" / "out"
    Reporter(_stable_summary()).write(target)

    assert (target / "summary.md").is_file()
    assert (target / "summary.json").is_file()
    assert (target / "summary.yaml").is_file()


# ---------------------------------------------------------------------------
# Reporter immutability (frozen dataclass keeps the summary stable)
# ---------------------------------------------------------------------------


def test_reporter_is_frozen() -> None:
    """``Reporter`` is a frozen dataclass — its summary cannot be swapped."""

    reporter = Reporter(_stable_summary())
    with pytest.raises(Exception):
        reporter.summary = _stable_summary()  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Partial summary path (SIGINT — INTERRUPTED row with finished_at='')
# ---------------------------------------------------------------------------


def test_to_yaml_handles_partial_summary(tmp_path: Path) -> None:
    """An INTERRUPTED row is renderable under a partial summary."""

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
    body = Reporter(summary).to_yaml()
    parsed = yaml.safe_load(body)
    statuses = [row["status"] for row in parsed["evals"]]
    assert statuses == ["PASS", "INTERRUPTED"]
    assert parsed["finished_at"] == ""
