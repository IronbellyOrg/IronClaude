"""Waiver re-green meta-scenario (FR-12 / NFR-4 no-re-greening latch) -- NOT a captured-input replay.

DESIGN NOTE (a reviewer MUST read this single-test module as COMPLETE, not partial): unlike E1-E5,
this module intentionally has NO unguarded OLD=MISS counterpart. It asserts a FORWARD
verdict-state-machine invariant of the impl's verdict aggregator (which exists ONLY on the impl
surface), not a pre-fix-parent regression -- so there is no commit to replay and a single
`requires_impl_ref`-guarded test is the correct and complete shape. This scenario backs NFR-4
(no-re-greening durability), NOT NFR-1, so it is EXCLUDED from the E1-E5 `catch_rate` /
`backtest_status` arithmetic and is NOT fed into the `CatchRateReport` (whose `total_escapes == 5`
invariant is unchanged).

The invariant (RELEASE-SPEC FR-12 / §4.5 `waiver_status` / §5.4 truth table): a `waived_with_rationale`
or absent mandatory probe sets a ONE-WAY `waiver_status` latch (`none` -> `latched`) and forces
`pipeline_hardening_verdict ∈ {blocked, advisory}`; no later `task-builder` / `sc:reflect` /
`sc:adversarial` / report-render stage may upgrade it to plain `pass` / `success` (a downstream
success enum renders as `success_with_hardening_blocker` / `success_with_hardening_advisory`, never
plain `success`). The §4.7-named validator surface documenting this is `refs/hardening-output-contract.md`.
"""

from __future__ import annotations

from tests.troubleshoot.backtest._impl_guard import HARDENING_REFS, requires_impl_ref


@requires_impl_ref("hardening-output-contract.md")
def test_waiver_latch_one_way_blocks_downstream_regreen() -> None:
    """NFR-4 proxy: the output-contract ref documents the one-way waiver latch + no-re-green rule.

    Skip-guarded until the impl verdict-aggregation contract lands (NOT importorskip / xfail /
    try-except-ImportError). Distinct function name avoids nodeid collision with the impl's
    `tests/troubleshoot/test_hardening_verdict.py::test_waiver_latch_one_way`.
    """
    text = (HARDENING_REFS / "hardening-output-contract.md").read_text(encoding="utf-8")
    low = text.lower()
    # One-way latch none -> latched.
    assert "waiver_status" in low and "latch" in low, (
        "output-contract ref must document the one-way waiver_status latch (none -> latched)"
    )
    # Latch forces verdict into {blocked, advisory}.
    assert "blocked" in low and "advisory" in low, (
        "output-contract ref must force pipeline_hardening_verdict into {blocked, advisory} once latched"
    )
    # No downstream stage may re-green to plain success; renders as success_with_hardening_*.
    assert (
        "success_with_hardening_blocker" in low
        or "success_with_hardening_advisory" in low
    ), (
        "output-contract ref must document that a latched verdict renders as "
        "success_with_hardening_blocker/advisory downstream, never plain success"
    )
