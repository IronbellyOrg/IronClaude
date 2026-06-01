"""Audit trail fixture registration for tests/roadmap/ test suite.

Re-exports the session-scoped ``audit_trail`` fixture from
``tests/v3.3/conftest.py`` so that roadmap integration tests can emit
JSONL audit records using the same infrastructure.

The fixture is session-scoped: all roadmap tests in a single pytest session
share one ``AuditTrailHelper`` instance and write to one JSONL file.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audit-trail"))

from audit_writer import AuditWriter

# Import the helper class to avoid duplication
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "v3.3"))
from conftest import AuditTrailHelper

# ---------------------------------------------------------------------------
# Contract #9 sidecar registration helper (sc:reflect M9 / D-REGRESSION-01)
# ---------------------------------------------------------------------------
#
# R0.1 added the ``_roadmap_ids_within_spec`` SemanticCheck to MERGE_GATE.
# That check is fail-shut: if ``set_id_registry_sidecar_path`` was never
# called before the gate runs, the check returns a failure string
# (master:§Flaw 4 -- no fail-open defaults).
#
# Pipeline-integration tests that exercise MERGE_GATE via mock subprocess
# fixtures (no real executor) never register a sidecar. The fixture below
# writes a permissive sidecar covering the IDs those mock fixtures emit
# (FR-001..FR-999, NFR-001..NFR-099, SC-001..SC-099, G-001..G-099,
# D1..D99) and registers it for the duration of the test. State is cleared
# on teardown so test_spec_roadmap_id_containment.py's own ``autouse``
# isolation fixture sees a clean slate.
#
# Apply via ``pytestmark = pytest.mark.usefixtures(
#     "_merge_gate_id_registry_sidecar"
# )`` in the affected test modules rather than ``autouse=True`` here,
# because the fixture should be scoped to integration tests that
# exercise MERGE_GATE with synthetic IDs, not to the entire roadmap
# test suite.


@pytest.fixture
def _merge_gate_id_registry_sidecar(tmp_path: Path):
    """Register a permissive spec_id_registry.json sidecar for MERGE_GATE.

    Writes a JSON sidecar covering the synthetic ID families used by
    pipeline-integration mock fixtures and registers it via
    ``gates.set_id_registry_sidecar_path``. Cleared on teardown.
    """
    from superclaude.cli.roadmap import gates as _gates

    sidecar = tmp_path / "spec_id_registry.json"
    payload = {
        "fr_ids": [f"FR-{i:03d}" for i in range(1, 1000)],
        "nfr_ids": [f"NFR-{i:03d}" for i in range(1, 100)],
        "sc_ids": [f"SC-{i:03d}" for i in range(1, 100)],
        "g_ids": [f"G-{i:03d}" for i in range(1, 100)],
        # D-family lenient pattern matches both ``D5`` and ``D-5``; cover both.
        "d_ids": (
            [f"D{i}" for i in range(1, 100)] + [f"D-{i:02d}" for i in range(1, 100)]
        ),
        "accepted_deviation_ids": [],
        "spec_hash": "0" * 16,
        "spec_path": str(tmp_path / "spec.md"),
    }
    sidecar.write_text(json.dumps(payload), encoding="utf-8")
    _gates.set_id_registry_sidecar_path(sidecar)
    try:
        yield sidecar
    finally:
        _gates.set_id_registry_sidecar_path(None)


@pytest.fixture(scope="session")
def results_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Session-scoped results directory for roadmap audit artifacts."""
    d = tmp_path_factory.mktemp("roadmap-results")
    return d


@pytest.fixture(scope="session")
def recurrence_corpus_dir() -> Path:
    """Path to tests/roadmap/fixtures/recurrence/ — base for all recurrence cases.

    Registered for Contract #9 (id_containment) and reused by Contract #10
    (anti_instinct), #4 (spec_fidelity), #6 (frontmatter_parser), #7
    (retry_contract), #8 (threshold_registry) in later phases.
    Layout convention documented at
    ``tests/roadmap/fixtures/recurrence/README.md``.
    """
    return Path(__file__).parent / "fixtures" / "recurrence"


@pytest.fixture
def recurrence_case(request, recurrence_corpus_dir):
    """Indirect-parametrized loader: (failure_class, case_name) -> (path, expected).

    Usage::

        @pytest.mark.parametrize(
            "recurrence_case",
            [("id_containment", "spec_roadmap_drift_case")],
            indirect=True,
        )
        def test_xxx(recurrence_case):
            input_path, expected = recurrence_case
            ...
    """
    failure_class, case_name = request.param
    input_path = recurrence_corpus_dir / failure_class / f"{case_name}.md"
    expected_path = recurrence_corpus_dir / failure_class / f"{case_name}.expected.json"
    return (input_path, json.loads(expected_path.read_text(encoding="utf-8")))


@pytest.fixture(scope="session")
def audit_trail(results_dir: Path) -> AuditTrailHelper:
    """Session-scoped audit trail fixture for roadmap integration tests.

    Identical contract to the v3.3 audit_trail fixture. Instantiates its
    own ``AuditWriter`` so roadmap tests can run independently or together
    with v3.3 tests.

    Yields
    ------
    AuditTrailHelper
        Helper with ``record()`` and ``summary()`` methods.
    """
    output_path = results_dir / "audit.jsonl"
    writer = AuditWriter(output_path)
    helper = AuditTrailHelper(writer, results_dir)

    yield helper

    # Session teardown: generate summary report
    summary = helper.summary()

    # 1. Append summary as final JSONL record
    summary_record = {"assertion_type": "session_summary", **summary}
    summary_line = json.dumps(summary_record, separators=(",", ":"))
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(summary_line + "\n")

    # 2. Write standalone summary JSON file
    summary_path = results_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_record, f, indent=2)

    # 3. Print summary to stdout
    print(
        f"\n{'=' * 60}\n"
        f"  Roadmap Audit Trail Session Summary\n"
        f"{'=' * 60}\n"
        f"  Total:              {summary['total']}\n"
        f"  Passed:             {summary['passed']}\n"
        f"  Failed:             {summary['failed']}\n"
        f"  Skipped:            {summary['skipped']}\n"
        f"  Wiring Coverage:    {summary['wiring_coverage_pct']}%\n"
        f"{'=' * 60}\n"
        f"  JSONL:    {output_path}\n"
        f"  Summary:  {summary_path}\n"
        f"{'=' * 60}"
    )
