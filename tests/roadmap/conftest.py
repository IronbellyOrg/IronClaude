"""Audit trail fixture registration for tests/roadmap/ test suite.

Re-exports the session-scoped ``audit_trail`` fixture from
``tests/v3.3/conftest.py`` so that roadmap integration tests can emit
JSONL audit records using the same infrastructure.

The fixture is session-scoped: all roadmap tests in a single pytest session
share one ``AuditTrailHelper`` instance and write to one JSONL file.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audit-trail"))

from audit_writer import AuditWriter

# Import the helper class to avoid duplication
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "v3.3"))
from conftest import AuditTrailHelper


@pytest.fixture(scope="session")
def results_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Session-scoped results directory for roadmap audit artifacts."""
    d = tmp_path_factory.mktemp("roadmap-results")
    return d


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
        f"\n{'='*60}\n"
        f"  Roadmap Audit Trail Session Summary\n"
        f"{'='*60}\n"
        f"  Total:              {summary['total']}\n"
        f"  Passed:             {summary['passed']}\n"
        f"  Failed:             {summary['failed']}\n"
        f"  Skipped:            {summary['skipped']}\n"
        f"  Wiring Coverage:    {summary['wiring_coverage_pct']}%\n"
        f"{'='*60}\n"
        f"  JSONL:    {output_path}\n"
        f"  Summary:  {summary_path}\n"
        f"{'='*60}"
    )
