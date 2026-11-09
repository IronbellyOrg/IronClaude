"""Static regression checks, NOT runtime/model behavior or an executable gate.

Scenario expectations are documented in docs/designs/document-review-contract.md.
These checks only pin the corresponding instructions and reject old conflicts.
"""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PANELS = (
    "src/superclaude/commands/spec-panel.md",
    "plugins/superclaude/commands/spec-panel.md",
)


@pytest.mark.parametrize("path", PANELS)
@pytest.mark.parametrize(
    "required",
    [
        "Only confirmed High/Critical findings block",
        "substantiated severe dependency defect",
        "Genuine Medium/Low/Nit findings are warnings or notes",
        "adequately evidenced zero findings is valid",
        "Unknown required predicates or material credible severe concerns mean INCOMPLETE",
        "unsupported speculation cannot invent an assurance predicate",
        "Missing headers never reset an ongoing loop",
        "Check known exhaustion before any initial-review default",
        "including INCOMPLETE and empty-diff reviews",
        "predeclared bounded recovery allowance, default zero",
        "No automatic fourth review or hidden F3",
        "after F2 freezes, necessity audits are report-only",
        "Preserve every prior finding id and its source report",
        "missing required prior rows mean INCOMPLETE, not zero",
        "Record duplicate/unknown identities explicitly",
        "gross added/deleted and net bytes per finding",
        "count shared/uncertain attribution once",
        "allow safe deletion or narrowing, preserve required safety behavior",
        "only the attended top-level session asks one batched optional issue question",
        "Unattended runs record warnings and unresolved decisions without waiting, filing or acting",
        "no row quota",
        "Cover relevant states, thresholds, sentinels and dependencies",
        "With no guards",
        "Completed formatting alone is not assurance",
    ],
)
def test_document_review_instruction_is_present(path, required):
    assert required in (ROOT / path).read_text()


@pytest.mark.parametrize("path", PANELS)
@pytest.mark.parametrize(
    "obsolete",
    [
        "CRITICAL and FR-8/FR-9 findings are blocking",
        "minimum 6 input condition rows per guard",
        "automatically generates a finding with **MAJOR** severity minimum",
        "is classified as **MAJOR** severity minimum",
        "Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL**",
        "without them the run is a first review",
        "an `origin=unchanged` finding is a minor note unless",
    ],
)
def test_historical_conflicting_instruction_is_absent(path, obsolete):
    assert obsolete not in (ROOT / path).read_text()


def test_coordinator_retains_budget_and_uncertainty_fields():
    text = (
        ROOT / "src/superclaude/templates/documents/document-review-coordinator.md"
    ).read_text()
    for required in (
        "Reviews consumed: __ / 3; fixes consumed: __ / 2",
        "Actual reviewer model and source (or unknown)",
        "If phase outcome or mutation ownership is uncertain",
        "do not reset spent budget",
        "Per-finding gross added/deleted and net bytes",
        "Post-F2 necessity audit: report-only",
        "default zero",
    ):
        assert required in text
