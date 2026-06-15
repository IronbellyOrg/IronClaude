"""H2 (Contract-Enumeration Ledger + Sibling Sweep) content-assertion tests.

Asserts the documented FR-5 / FR-6 / §5.6 H2 markers in the source-of-truth ref
src/superclaude/skills/sc-troubleshoot-protocol/refs/contract-enumeration.md.
test_h2_sibling_sweep_required_when_concept_shared is NEW (reflect gap G-PRE-1).
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
H2 = (REFS / "contract-enumeration.md").read_text(encoding="utf-8")


def test_h2_empty_ledger_fails() -> None:
    """FR-5 AC1 / F-N3: an empty/zero-row ledger does NOT vacuously pass (empty ledger =
    FAIL) and unclassified live consumers cause FAIL."""
    low = H2.lower()
    assert "vacuously pass" in low, "empty-ledger non-vacuous rule not documented"
    assert "zero-row" in low and "ledger" in low
    assert "unclassified live consumer" in low, "unclassified-consumer FAIL not documented"
    # §5.6 H2 Contract Ledger Row schema fields present
    for field in (
        "contract_token",
        "role",
        "component_path",
        "discovery_method",
        "classification",
        "unreachability_proof",
    ):
        assert field in H2, f"H2 ledger field missing: {field}"


def test_h2_sibling_sweep_required_when_concept_shared() -> None:
    """FR-6 AC1 (NEW — reflect gap G-PRE-1): H2 FAILs if sibling pipelines / duplicate
    evaluators are NOT swept when the concept is shared."""
    low = H2.lower()
    assert "concept is shared" in low, "FR-6 shared-concept trigger not documented"
    assert "sibling pipelines" in low
    assert "duplicate evaluator" in low  # matches "duplicate evaluators"
    assert "swept" in low
    assert "fail" in low, "FR-6 must state H2 FAILs when the sweep is skipped"
