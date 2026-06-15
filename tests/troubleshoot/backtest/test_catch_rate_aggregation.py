"""Catch-rate aggregation runner (L6 + L5) -- build CatchRateReport from E1-E5, derive backtest_status.

The catch-rate roll-up lives in the pytest aggregation (NOT a suite YAML). It parametrizes over the
five `REPLAY_ESCAPES`, collects one `EscapeResult` per escape, builds a `CatchRateReport`, writes
`catch-rate.json` to `tmp_path`, and asserts `backtest_status` is correctly derived.

backtest_status driver (NFR-1 / §5.4):
  - NO NEW=CATCH impl ref present  -> the NEW (catch) dimension never ran  -> `not_run` (0 records).
    This is TODAY's state (the impl refs have not landed); the OLD=MISS witnesses are asserted in
    test_backtest_e1..e5.py but do not by themselves populate the catch-rate denominator.
  - >=1 impl ref present -> collect ALL 5 records (present-ref => CATCH+card, absent-ref => MISS):
      * all 5 CATCH + negative_witness + card_path -> `complete`
      * otherwise                                  -> `partial` (missing escape ids surfaced)
    `total_escapes == 5` in this case -- the denominator is EXACTLY the five E1-E5 escapes.

The Waiver re-green meta-scenario (test_waiver_regreen.py) is NOT collected here and is EXCLUDED from
the catch_rate / backtest_status arithmetic (it backs NFR-4, not NFR-1).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.troubleshoot.backtest._impl_guard import HARDENING_REFS
from tests.troubleshoot.backtest.catch_rate import (
    VERDICT_CATCH,
    VERDICT_MISS,
    EscapeResult,
    build_catch_rate_report,
    unresolved_card_paths,
)
from tests.troubleshoot.backtest.catch_rate_report import write_catch_rate_report
from tests.troubleshoot.backtest.git_replay import REPLAY_ESCAPES

# Each escape's NEW=CATCH proof surface (the impl ref documenting its catch mechanism).
_ESCAPE_REFS = {
    "E1": "runtime-entrypoint-verification.md",
    "E2": "unmask-and-sweep.md",
    "E3": "unmask-and-sweep.md",
    "E4": "contract-enumeration.md",
    "E5": "effective-input-proof.md",
}

_PROXY_LIMITATION = (
    "NEW=CATCH is a documentation-presence proxy (impl-ref existence), NOT an executed gate; "
    "complete is unreachable until feat/troubleshoot-pipeline-hardening lands the hardening refs."
)


def _collect_escape_results() -> list[EscapeResult]:
    """Collect one EscapeResult per E1-E5 -- but ONLY when >=1 NEW=CATCH impl ref is present.

    No refs at all -> empty list -> not_run (the NEW/catch dimension never ran). When at least one
    ref is present, every escape is collected (present-ref => CATCH+card, absent-ref => MISS) so the
    denominator is the full E1-E5 set and a partial landing derives `partial`, never a vacuous
    `complete` over a subset.
    """
    present = {
        e.escape_id: (HARDENING_REFS / _ESCAPE_REFS[e.escape_id]).exists()
        for e in REPLAY_ESCAPES
    }
    if not any(present.values()):
        return []
    out: list[EscapeResult] = []
    for e in REPLAY_ESCAPES:
        if present[e.escape_id]:
            out.append(
                EscapeResult(
                    escape_id=e.escape_id,
                    wave=e.wave,
                    verdict=VERDICT_CATCH,
                    negative_witness=True,
                    card_path=str(HARDENING_REFS / _ESCAPE_REFS[e.escape_id]),
                    detail="NEW=CATCH proof ref present; OLD=MISS witness in test_backtest_*.py",
                )
            )
        else:
            out.append(
                EscapeResult(
                    escape_id=e.escape_id,
                    wave=e.wave,
                    verdict=VERDICT_MISS,
                    negative_witness=True,
                    card_path=None,
                    detail="NEW=CATCH proof ref not landed yet; not proven caught",
                )
            )
    return out


@pytest.mark.parametrize(
    "escape", REPLAY_ESCAPES, ids=[e.escape_id for e in REPLAY_ESCAPES]
)
def test_backtest_escape_collected_into_catch_rate(escape) -> None:
    """Each escape collects as CATCH iff its NEW=CATCH ref is present; else MISS. Skips at not_run."""
    collected = {r.escape_id: r for r in _collect_escape_results()}
    if not collected:
        pytest.skip(
            "No NEW=CATCH impl refs landed yet -> catch-rate is not_run; the OLD=MISS negative "
            "witnesses are asserted in test_backtest_e1..e5.py."
        )
    rec = collected[escape.escape_id]
    ref_present = (HARDENING_REFS / _ESCAPE_REFS[escape.escape_id]).exists()
    assert rec.verdict == (VERDICT_CATCH if ref_present else VERDICT_MISS)
    assert rec.wave == escape.wave


def test_backtest_catch_rate_report_drives_status(tmp_path: Path) -> None:
    """Build the CatchRateReport over E1-E5, write to tmp_path, assert the derived backtest_status."""
    results = tuple(_collect_escape_results())
    report = build_catch_rate_report(
        run_id="backtest-aggregation",
        generated_at="2026-06-12T00:00:00Z",
        contract_version="1.0.0",
        escapes=results,
        proxy_limitation=_PROXY_LIMITATION,
    )
    written = write_catch_rate_report(report, tmp_path)
    # EXACT-equality guard (not a vacuous "docs" substring check): the written report's parent dir
    # IS tmp_path, which proves the artifact is tmp_path-rooted and never under docs/.
    assert written["catch-rate.json"].parent == tmp_path, (
        "report must be written under tmp_path (never docs/)"
    )
    payload = json.loads((tmp_path / "catch-rate.json").read_text(encoding="utf-8"))

    if not results:
        # TODAY: no impl refs -> not_run; the denominator is 0, not a failure.
        assert payload["backtest_status"] == "not_run"
        assert payload["total_escapes"] == 0
        assert payload["caught"] == 0
    else:
        # The denominator is EXACTLY the five E1-E5 escapes (waiver scenario excluded).
        assert payload["total_escapes"] == 5
        fully_caught = all(
            r.verdict == VERDICT_CATCH
            and r.negative_witness
            and r.card_path is not None
            for r in results
        )
        expected = "complete" if fully_caught else "partial"
        assert payload["backtest_status"] == expected
        if expected == "partial":
            missing = set(report.missing_escape_ids())
            assert missing == {
                r.escape_id
                for r in results
                if not (
                    r.verdict == VERDICT_CATCH and r.negative_witness and r.card_path
                )
            }
            assert missing, (
                "a partial report must surface at least one missing escape id"
            )


def test_backtest_aggregation_complete_and_partial_derivations(tmp_path: Path) -> None:
    """HERMETIC: exercise the today-dead complete/partial arms with SYNTHETIC EscapeResults.

    The live ``_collect_escape_results`` path only ever yields the ``not_run`` arm until the impl
    refs land, so the aggregation's own derivation + missing-id + unresolved-card wiring is never
    exercised by the ref-gated tests. This test builds escapes by hand (no impl refs, no skips) so
    the ``complete`` and ``partial`` branches run unconditionally on synthetic data.
    """
    # (a) COMPLETE: all five escapes CATCH + negative_witness + a real card under tmp_path.
    complete_escapes: list[EscapeResult] = []
    for i in range(1, 6):
        escape_id = f"E{i}"
        card_rel = f"cards/{escape_id}.md"
        card_file = tmp_path / card_rel
        card_file.parent.mkdir(parents=True, exist_ok=True)
        card_file.write_text(f"# synthetic card for {escape_id}\n", encoding="utf-8")
        complete_escapes.append(
            EscapeResult(
                escape_id=escape_id,
                wave="H1",
                verdict=VERDICT_CATCH,
                negative_witness=True,
                card_path=card_rel,
                detail="synthetic complete escape",
            )
        )

    complete_report = build_catch_rate_report(
        run_id="hermetic-complete",
        generated_at="2026-06-12T00:00:00Z",
        contract_version="1.0.0",
        escapes=tuple(complete_escapes),
        proxy_limitation=_PROXY_LIMITATION,
    )
    assert complete_report.backtest_status == "complete"
    assert complete_report.total_escapes == 5
    assert complete_report.caught == 5
    assert complete_report.missed == 0
    assert complete_report.catch_rate == 1.0
    assert complete_report.missing_escape_ids() == ()

    # All recorded cards exist under tmp_path -> no unresolved cards.
    assert unresolved_card_paths(complete_report, base_dir=tmp_path) == ()
    # Pointing base_dir elsewhere surfaces every card as unresolved (they don't exist there).
    other_dir = tmp_path / "elsewhere"
    other_dir.mkdir()
    assert set(unresolved_card_paths(complete_report, base_dir=other_dir)) == {
        e.card_path for e in complete_escapes
    }

    # Write both artifacts and assert they exist + the md headline carries the 5/5 catch count.
    complete_written = write_catch_rate_report(complete_report, tmp_path)
    assert complete_written["catch-rate.json"].exists()
    assert complete_written["catch-rate.md"].exists()
    assert (tmp_path / "catch-rate.json").exists()
    assert (tmp_path / "catch-rate.md").exists()
    md_text = complete_written["catch-rate.md"].read_text(encoding="utf-8")
    assert "5/5" in md_text

    # A fabricated (never-created) card surfaces as unresolved even when base_dir is correct.
    fabricated_report = build_catch_rate_report(
        run_id="hermetic-fabricated",
        generated_at="2026-06-12T00:00:00Z",
        contract_version="1.0.0",
        escapes=(
            EscapeResult(
                escape_id="E1",
                wave="H1",
                verdict=VERDICT_CATCH,
                negative_witness=True,
                card_path="cards/does-not-exist.md",
                detail="synthetic escape with a fabricated card",
            ),
        ),
        proxy_limitation=_PROXY_LIMITATION,
    )
    assert unresolved_card_paths(fabricated_report, base_dir=tmp_path) == (
        "cards/does-not-exist.md",
    )

    # (b) PARTIAL: one MISS (null card) + four CATCH -> partial, and the MISS id is surfaced.
    partial_escapes: list[EscapeResult] = [
        EscapeResult(
            escape_id="E1",
            wave="H1",
            verdict=VERDICT_MISS,
            negative_witness=True,
            card_path=None,
            detail="synthetic miss escape",
        )
    ]
    for i in range(2, 6):
        escape_id = f"E{i}"
        card_rel = f"cards/{escape_id}.md"
        partial_escapes.append(
            EscapeResult(
                escape_id=escape_id,
                wave="H1",
                verdict=VERDICT_CATCH,
                negative_witness=True,
                card_path=card_rel,
                detail="synthetic caught escape",
            )
        )

    partial_report = build_catch_rate_report(
        run_id="hermetic-partial",
        generated_at="2026-06-12T00:00:00Z",
        contract_version="1.0.0",
        escapes=tuple(partial_escapes),
        proxy_limitation=_PROXY_LIMITATION,
    )
    assert partial_report.backtest_status == "partial"
    assert partial_report.total_escapes == 5
    assert partial_report.caught == 4
    assert partial_report.missed == 1
    assert "E1" in partial_report.missing_escape_ids()
    assert set(partial_report.missing_escape_ids()) == {"E1"}
