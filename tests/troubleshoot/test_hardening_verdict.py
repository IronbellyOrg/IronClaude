"""Verdict aggregation / waiver-latch / H5-mapping content-assertion tests.

Asserts the §5.4 verdict mechanics (incl. the advisory invariant) and FR-12 in the
source-of-truth ref src/superclaude/skills/sc-troubleshoot-protocol/refs/hardening-output-contract.md.

Unit tests live here (Step 7.7). The verdict-aggregation and downstream-no-override
integration tests are appended by Steps 7.8 and 7.9.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REFS = REPO_ROOT / "src" / "superclaude" / "skills" / "sc-troubleshoot-protocol" / "refs"
OC = (REFS / "hardening-output-contract.md").read_text(encoding="utf-8")


def test_waiver_latch_one_way() -> None:
    """FR-12 / F-S1: the one-way none->latched latch forces
    pipeline_hardening_verdict ∈ {blocked, advisory} and never resets."""
    low = OC.lower()
    assert "one-way" in low, "one-way latch not documented"
    assert "never resets to `none`" in low, "latch must never reset to none"
    assert "{blocked, advisory}" in OC, "latch must force verdict into {blocked, advisory}"


def test_h5_decision_maps_to_status_and_latch() -> None:
    """§5.4 H5 mapping: the 4-row decision-to-status table
    (performed->PASS/none, not_required->PASS/none, required->FAIL/none,
    waived_with_rationale->N/A-with-rationale/latched)."""
    assert "`performed` | `PASS` | `none`" in OC
    assert "`not_required` | `PASS` | `none`" in OC
    assert "`required` | `FAIL` | `none`" in OC
    assert "`waived_with_rationale` | `N/A` with rationale | `latched`" in OC


def test_known_escapes_requires_cited_card() -> None:
    """FR-12 AC3 / F-A1 anti-inflation: an escape ID may appear in known_escapes_caught
    ONLY with a cited passing wave/card. Also guards the FOUR-token advisory-inclusive enum."""
    low = OC.lower()
    assert "known_escapes_caught" in OC
    assert "only if a passing wave/card is cited" in low, "anti-inflation rule not documented"
    # advisory-inclusive 4-token enum (a 3-token enum is a defect)
    assert "pass | blocked | advisory | not_applicable" in OC


# ---------------------------------------------------------------------------
# Integration tests (Steps 7.8 / 7.9)
# ---------------------------------------------------------------------------

HANDOFF = (REFS / "remediation-handoff.md").read_text(encoding="utf-8")


def test_verdict_aggregation_from_h_statuses() -> None:
    """FR-13 AC2: the §5.4 truth table reproduces ALL 7 ROWS in priority order with exact
    verdicts — row 1 not_applicable, rows 2/3/4 blocked, ROW 5 advisory AND ROW 6 advisory,
    row 7 pass — and EVERY row's "Downstream Override Allowed?" is No."""
    # all 7 priority rows present
    for n in range(1, 8):
        assert f"| {n} |" in OC, f"truth-table row {n} missing"
    # row 1 -> not_applicable
    assert "`not_applicable`" in OC
    # rows 2/3/4 -> blocked (three blocked rows)
    assert OC.count("`blocked`") >= 3
    # rows 5 AND 6 -> advisory (guards against the prior 3-token-enum regression)
    assert "ADVISORY — closure relies on waived/substituted proof" in OC  # row 5
    assert "ADVISORY — scoped closure with rationalized N/A" in OC  # row 6
    assert OC.count("`advisory`") >= 2
    # row 7 -> pass
    assert "`pass`" in OC
    # EVERY row's "Downstream Override Allowed?" is No (all 7 truth-table rows)
    assert OC.count("| No |") >= 7, "every truth-table row must forbid downstream override"


def test_downstream_success_cannot_override_latched_hardening_verdict() -> None:
    """FR-12 ↔ NFR-4 pairing (spec §10 L596): hardening-output-contract.md documents the
    §5.4 L411 downstream-no-override rule, the rendered downstream result is
    success_with_hardening_blocker / success_with_hardening_advisory (never plain success)
    whenever the table returns blocked/advisory, and remediation-handoff.md carries
    pipeline_hardening_verdict + waiver_status into BUILD_REQUEST."""
    low = OC.lower()
    # (a) §5.4 L411 no-override rule names the downstream stages and forbids conversion
    assert "not** convert" in low, "no-override rule (may NOT convert) not documented"
    for stage in ("task-builder", "sc:reflect", "sc:adversarial", "report-rendering"):
        assert stage in low, f"no-override rule must name the {stage} stage"
    # (b) success_with_hardening_* rendering, never plain success
    assert "success_with_hardening_blocker" in OC
    assert "success_with_hardening_advisory" in OC
    assert "never plain `success`" in low
    # (c) the handoff carries the latched verdict + waiver_status into BUILD_REQUEST
    assert "build_request" in HANDOFF.lower()
    assert "pipeline_hardening_verdict" in HANDOFF
    assert "waiver_status" in HANDOFF
