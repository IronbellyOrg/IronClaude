"""Tests for ``superclaude.cli.eval.models.RunSummary``.

Covers cliEval Phase 3 / Task T03.09 acceptance criteria (DM-004 / DM-012):

* Module exports a frozen ``RunSummary`` dataclass with the 11 DM-004
  fields and a nested ``counts`` sub-structure carrying the 5 DM-012
  counts sub-fields.
* ``RunSummary.__post_init__`` asserts the
  ``kept_k + skipped_s == expanded_n_prime`` equation matches the
  ``kept_plus_skipped_equals_n_prime`` boolean flag; a mismatch raises
  ``ValueError``.
* ``to_dict()`` returns a deterministic JSON-serialisable mapping with
  nested ``RunCounts`` / ``RunTotals`` / ``EvalOutcome`` records unwrapped
  via their own ``to_dict``.
* The dataclass is frozen so reporter consumers cannot mutate it
  mid-render.

Cross-link: ``EvalOutcome`` (DM-001 / T03.01) is the per-eval payload
carried by ``evals``. ``RunSummary`` is consumed by COMP-008 Reporter
(T03.13) and is the canonical payload behind ``summary.md`` /
``summary.json`` (FR-RPT1 / T03.11).
"""

from __future__ import annotations

import dataclasses
import json

import pytest

from superclaude.cli.eval.models import (
    EvalOutcome,
    RunCounts,
    RunSummary,
    RunTotals,
)


def _outcome(eval_id: str = "ExampleEval1", status: str = "PASS") -> EvalOutcome:
    return EvalOutcome(
        eval_id=eval_id,
        title="example",
        status=status,  # type: ignore[arg-type]
        duration_sec=0.123,
    )


def _counts(
    *,
    manifest_n: int = 3,
    expanded_n_prime: int = 3,
    kept_k: int = 3,
    skipped_s: int = 0,
    kept_plus_skipped_equals_n_prime: bool = True,
) -> RunCounts:
    return RunCounts(
        manifest_n=manifest_n,
        expanded_n_prime=expanded_n_prime,
        kept_k=kept_k,
        skipped_s=skipped_s,
        kept_plus_skipped_equals_n_prime=kept_plus_skipped_equals_n_prime,
    )


def _summary(**overrides) -> RunSummary:
    defaults = dict(
        run_id="run-2026-05-20T11:00:00Z-abc",
        started_at="2026-05-20T11:00:00",
        finished_at="2026-05-20T11:00:05",
        duration_sec=5.0,
        suite="suites/example.yaml",
        manifest_version="1.0.0",
        parallel=3,
        counts=_counts(),
        totals=RunTotals(passed=3),
        evals=(_outcome("E1"), _outcome("E2"), _outcome("E3")),
        artifacts={"jsonl_dir": "/tmp/run/.eval-logs"},
    )
    defaults.update(overrides)
    return RunSummary(**defaults)


def test_run_summary_has_required_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(RunSummary)]
    # Field order matches DM-004 verbatim so to_dict() ordering stays stable
    # across reporter snapshots and review diffs.
    assert field_names == [
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
    assert len(field_names) == 11


def test_run_counts_has_required_sub_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(RunCounts)]
    assert field_names == [
        "manifest_n",
        "expanded_n_prime",
        "kept_k",
        "skipped_s",
        "kept_plus_skipped_equals_n_prime",
    ]
    assert len(field_names) == 5


def test_run_totals_has_required_sub_fields() -> None:
    field_names = [f.name for f in dataclasses.fields(RunTotals)]
    assert field_names == [
        "passed",
        "failed",
        "skipped",
        "errored",
        "interrupted",
        "timeout",
    ]


def test_run_summary_is_frozen() -> None:
    summary = _summary()
    with pytest.raises(dataclasses.FrozenInstanceError):
        summary.run_id = "tampered"  # type: ignore[misc]


def test_run_counts_is_frozen() -> None:
    counts = _counts()
    with pytest.raises(dataclasses.FrozenInstanceError):
        counts.expanded_n_prime = 99  # type: ignore[misc]


def test_run_summary_defaults() -> None:
    summary = RunSummary(
        run_id="r",
        started_at="2026-05-20T11:00:00",
        finished_at="2026-05-20T11:00:00",
        duration_sec=0.0,
        suite="suites/x.yaml",
        manifest_version="1.0.0",
        parallel=1,
        counts=_counts(manifest_n=0, expanded_n_prime=0, kept_k=0, skipped_s=0),
        totals=RunTotals(),
    )
    assert summary.evals == ()
    assert summary.artifacts == {}


def test_run_summary_artifacts_default_is_independent_per_instance() -> None:
    a = _summary(run_id="A")
    b = _summary(run_id="B")
    # Built with the same dict literal in the helper, but each instance must
    # hold its own mapping (the helper passes a fresh dict each call; the
    # dataclass's default_factory=dict guarantees the empty-default case too).
    assert a.artifacts is not b.artifacts


def test_run_summary_accepts_consistent_counts() -> None:
    summary = _summary(
        counts=_counts(
            manifest_n=5,
            expanded_n_prime=5,
            kept_k=3,
            skipped_s=2,
            kept_plus_skipped_equals_n_prime=True,
        ),
    )
    assert summary.counts.kept_k == 3
    assert summary.counts.skipped_s == 2


def test_run_summary_rejects_mismatched_counts_when_flag_true() -> None:
    # Acceptance: build a RunSummary with mismatched counts and confirm the
    # equation assertion fires. Here the flag claims True but the math
    # disagrees: 2 + 2 != 5.
    with pytest.raises(ValueError) as excinfo:
        _summary(
            counts=_counts(
                manifest_n=5,
                expanded_n_prime=5,
                kept_k=2,
                skipped_s=2,
                kept_plus_skipped_equals_n_prime=True,
            ),
        )
    msg = str(excinfo.value)
    assert "kept_plus_skipped_equals_n_prime" in msg
    assert "expanded_n_prime" in msg


def test_run_summary_rejects_mismatched_counts_when_flag_false() -> None:
    # The flag must also mirror reality in the other direction: if the math
    # holds but the flag claims False, the orchestrator is misreporting and
    # the model fails loudly.
    with pytest.raises(ValueError):
        _summary(
            counts=_counts(
                manifest_n=3,
                expanded_n_prime=3,
                kept_k=3,
                skipped_s=0,
                kept_plus_skipped_equals_n_prime=False,
            ),
        )


def test_run_summary_accepts_consistent_false_flag() -> None:
    # A run where kept_k + skipped_s != expanded_n_prime can still be
    # serialised so the Reporter can render the row and FR-RPT1 (T03.11)
    # raises ReporterContractViolation downstream. The model only enforces
    # that the flag mirrors reality.
    summary = _summary(
        counts=_counts(
            manifest_n=3,
            expanded_n_prime=5,
            kept_k=2,
            skipped_s=2,
            kept_plus_skipped_equals_n_prime=False,
        ),
    )
    assert summary.counts.kept_plus_skipped_equals_n_prime is False


def test_run_summary_to_dict_field_order_matches_dm004() -> None:
    payload = _summary().to_dict()
    assert list(payload.keys()) == [
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


def test_run_summary_to_dict_counts_sub_field_order() -> None:
    payload = _summary().to_dict()
    assert list(payload["counts"].keys()) == [
        "manifest_n",
        "expanded_n_prime",
        "kept_k",
        "skipped_s",
        "kept_plus_skipped_equals_n_prime",
    ]


def test_run_summary_to_dict_totals_sub_field_order() -> None:
    payload = _summary().to_dict()
    assert list(payload["totals"].keys()) == [
        "passed",
        "failed",
        "skipped",
        "errored",
        "interrupted",
        "timeout",
    ]


def test_run_summary_to_dict_is_json_serialisable() -> None:
    summary = _summary()
    payload = summary.to_dict()
    encoded = json.dumps(payload, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded["run_id"] == "run-2026-05-20T11:00:00Z-abc"
    assert decoded["counts"]["expanded_n_prime"] == 3
    assert decoded["totals"]["passed"] == 3
    assert len(decoded["evals"]) == 3
    assert decoded["evals"][0]["eval_id"] == "E1"
    assert decoded["artifacts"] == {"jsonl_dir": "/tmp/run/.eval-logs"}


def test_run_summary_to_dict_unwraps_nested_outcomes() -> None:
    outcome = _outcome("E1")
    summary = _summary(evals=(outcome,), counts=_counts(manifest_n=1, expanded_n_prime=1, kept_k=1))
    payload = summary.to_dict()
    # Reporter relies on each EvalOutcome being a plain dict, not a nested
    # dataclass, so it can iterate without bespoke unwrapping.
    assert isinstance(payload["evals"], list)
    assert payload["evals"][0] == outcome.to_dict()


def test_run_summary_to_dict_artifacts_is_independent_of_source() -> None:
    artifacts = {"jsonl_dir": "/tmp/run/.eval-logs"}
    summary = _summary(artifacts=artifacts)
    payload = summary.to_dict()
    payload["artifacts"]["jsonl_dir"] = "/dev/null"
    # Mutating the returned mapping must not bleed into the frozen source.
    assert summary.artifacts["jsonl_dir"] == "/tmp/run/.eval-logs"


def test_run_summary_deterministic_equality() -> None:
    a = _summary()
    b = _summary()
    assert a == b


def test_run_summary_unequal_when_field_differs() -> None:
    base = _summary()
    assert base != dataclasses.replace(base, run_id="other")
    assert base != dataclasses.replace(base, parallel=8)
    assert base != dataclasses.replace(base, suite="suites/other.yaml")
    assert base != dataclasses.replace(base, manifest_version="2.0.0")


def test_run_counts_to_dict_is_json_serialisable() -> None:
    counts = _counts(
        manifest_n=10,
        expanded_n_prime=12,
        kept_k=8,
        skipped_s=4,
        kept_plus_skipped_equals_n_prime=True,
    )
    payload = counts.to_dict()
    encoded = json.dumps(payload, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded == {
        "manifest_n": 10,
        "expanded_n_prime": 12,
        "kept_k": 8,
        "skipped_s": 4,
        "kept_plus_skipped_equals_n_prime": True,
    }


def test_run_totals_to_dict_is_json_serialisable() -> None:
    totals = RunTotals(
        passed=2, failed=1, skipped=3, errored=0, interrupted=1, timeout=1
    )
    payload = totals.to_dict()
    encoded = json.dumps(payload, sort_keys=True)
    decoded = json.loads(encoded)
    assert decoded == {
        "passed": 2,
        "failed": 1,
        "skipped": 3,
        "errored": 0,
        "interrupted": 1,
        "timeout": 1,
    }


def test_run_summary_reexported_from_package() -> None:
    from superclaude.cli.eval import (
        RunCounts as PkgRunCounts,
        RunSummary as PkgRunSummary,
        RunTotals as PkgRunTotals,
    )

    assert PkgRunSummary is RunSummary
    assert PkgRunCounts is RunCounts
    assert PkgRunTotals is RunTotals
