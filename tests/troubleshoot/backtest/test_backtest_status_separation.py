"""backtest_status separation invariant -- signoff stays advisory until complete (RELEASE-SPEC sec 5.4).

The spec's single most load-bearing invariant: ``backtest_status`` is SEPARATE from any run-level
verdict. A clean run (``pipeline_hardening_verdict=pass``) does NOT earn production signoff until the
E1-E5 corpus is ``complete``; ``partial`` lists the missing escape ids; only ``complete`` may MIRROR
the run-level verdict. (Spec names the governing test
``test_backtest_status_keeps_pipeline_health_advisory_until_complete``.) Asserted here against the
real ``CatchRateReport.production_signoff`` so the separation is a product invariant, not test-local.
"""

from __future__ import annotations

from tests.troubleshoot.backtest.catch_rate import (
    EscapeResult,
    build_catch_rate_report,
)

_RUN_LEVEL_PASS = "pass"


def _full_caught_escapes() -> tuple[EscapeResult, ...]:
    return tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, f"refs/c{i}.md") for i in range(1, 6)
    )


def test_backtest_status_keeps_signoff_advisory_until_complete() -> None:
    """not_run keeps signoff advisory regardless of a passing run-level verdict (sec 5.4)."""
    report = build_catch_rate_report(
        run_id="sep-not-run",
        generated_at="t",
        contract_version="1.0.0",
        escapes=(),
        proxy_limitation="proxy",
    )
    assert report.backtest_status == "not_run"
    # Even with a green run-level verdict, production signoff stays advisory.
    assert report.production_signoff(_RUN_LEVEL_PASS) == "advisory"


def test_backtest_status_partial_exposes_missing_escape_ids() -> None:
    """A partial report surfaces the missing escape ids and stays advisory (sec 5.4)."""
    mixed = (EscapeResult("E1", "H1", "MISS", True, None),) + _full_caught_escapes()[1:]
    report = build_catch_rate_report(
        run_id="sep-partial",
        generated_at="t",
        contract_version="1.0.0",
        escapes=mixed,
        proxy_limitation="proxy",
    )
    assert report.backtest_status == "partial"
    assert "E1" in report.missing_escape_ids()
    assert report.production_signoff(_RUN_LEVEL_PASS) == "advisory"


def test_backtest_status_complete_may_mirror_run_level_verdict() -> None:
    """Only a complete report (all 5 CATCH + witness + card) lets signoff mirror the verdict."""
    report = build_catch_rate_report(
        run_id="sep-complete",
        generated_at="t",
        contract_version="1.0.0",
        escapes=_full_caught_escapes(),
        proxy_limitation="proxy",
    )
    assert report.backtest_status == "complete"
    assert report.missing_escape_ids() == ()
    # complete MAY mirror the run-level verdict (here: pass).
    assert report.production_signoff(_RUN_LEVEL_PASS) == _RUN_LEVEL_PASS
    # A blocked run-level verdict is still mirrored (separation is one-directional gating only).
    assert report.production_signoff("blocked") == "blocked"
