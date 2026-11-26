"""The panel clock and the hang guard arithmetic (DESIGN 9.3, 9.4, 10.2; contract SWD 11.4 and 11.5).

Built locally to the sibling's written contract (config/shared-manifest.json: `built-local`). Pure functions: no wall
clock is read here, the launcher passes its monotonic stamps in. The row cap is `lens_row_cap` of rl/lens.py and is
re-exported so the launcher has one import for the arithmetic.

    hang_s(b, arm, panel)            1.5 * (b + expected overhead), counted from t0 (REQ-30)
    breakeven_row_cost(b, rows)      seconds per ledger row at which the arm still meets the +35% rule (REQ-31)
    panel_elapsed_s(...)             RL: end of R3 minus t0; other arms: last reviewer end minus t0 (REQ-29)
    timing_record(...)               the fields of timing.json (DESIGN 9.3)
"""

from __future__ import annotations

from fractions import Fraction

from rl.lens import lens_row_cap, values

__all__ = [
    "ARMS",
    "breakeven_row_cost",
    "expected_overhead",
    "hang_s",
    "lens_row_cap",
    "panel_elapsed_s",
    "slowest_reviewer_s",
    "timing_record",
]

ARMS = ("Z0-raw", "Z0", "K", "RL")
HANG_FACTOR = 1.5


def _arm(arm: str) -> str:
    if arm not in ARMS:
        raise ValueError(f"unknown arm {arm!r}; expected one of {ARMS}")
    return arm


def expected_overhead(arm: str, panel: str) -> float:
    """Seconds the arm adds to the slowest reviewer: RL 28 s (primary) or 30 s (haiku, sonnet); 0 for Z0, K, Z0-raw."""
    if _arm(arm) != "RL":
        return 0
    return values()["overhead_s"][panel]


def hang_s(b: float, arm: str, panel: str) -> float:
    """The hang guard in seconds from t0: 1.5 * (b + expected overhead of the arm)."""
    return HANG_FACTOR * (b + expected_overhead(arm, panel))


def breakeven_row_cost(b: float, rows: int) -> float:
    """Seconds per ledger row, to 2 places, at which RL ends exactly at 1.35 b (DESIGN 10.2).

    `0.35 b - 6` seconds are left for the rows (6 = render 1 + reading the recipes 4 + check 1); with `rows` rows the
    cost per row is that divided by `rows`: 29 / 14 = 2.07 at b 100.
    """
    k = values()["row_cap"]
    left = Fraction(str(k["share"])) * Fraction(str(b)) - Fraction(str(k["fixed_s"]))
    return round(float(left / rows), 2)


def slowest_reviewer_s(rev_start: dict, rev_end: dict) -> float:
    """max over reviewers of rev_end - rev_start: the quantity b is a median of, for Z0."""
    return round(max(rev_end[r] - rev_start[r] for r in rev_end), 3)


def panel_elapsed_s(
    arm: str, t0: float, rev_end: dict, r3_end: float | None = None
) -> float:
    """RL: the end of R3 (check and the ember re-ask included) minus t0. Other arms: the last reviewer end minus t0.
    H2, the merge, the judge and the optional verifier are outside the clock in every arm."""
    if _arm(arm) == "RL":
        if r3_end is None:
            raise ValueError("arm RL needs r3_end, the end of the ledger check")
        return round(r3_end - t0, 3)
    return round(max(rev_end.values()) - t0, 3)


def timing_record(
    arm: str,
    t0: float,
    rev_start: dict,
    rev_end: dict,
    render_s: float = 0,
    check_s: float = 0,
    reask_s: float = 0,
    r3_end: float | None = None,
) -> dict:
    """The fields of timing.json (DESIGN 9.3). All stamps are one monotonic clock; t0 is taken before the lens render.

    Refused: a reviewer that starts before t0 (the clock began after the render) or, for RL, before t0 + render_s;
    an RL r3_end before the last reviewer ended; render, check or re-ask seconds on an arm that has none.
    """
    rl = _arm(arm) == "RL"
    if not rl and (render_s or check_s or reask_s):
        raise ValueError(f"arm {arm} has no render, check or re-ask seconds")
    earliest = t0 + render_s
    for rid, start in rev_start.items():
        if start < earliest - 1e-9:
            raise ValueError(
                f"reviewer {rid} started at {start}, before t0 + render_s = {earliest}: the clock must start "
                "before the lens render"
            )
        if rev_end[rid] < start:
            raise ValueError(f"reviewer {rid} ended before it started")
    if rl and r3_end is not None and r3_end < max(rev_end.values()) - 1e-9:
        raise ValueError("r3_end is before the last reviewer ended")
    return {
        "t0": t0,
        "render_s": render_s,
        "rev_start": dict(rev_start),
        "rev_end": dict(rev_end),
        "check_s": check_s,
        "reask_s": reask_s,
        "panel_elapsed_s": panel_elapsed_s(arm, t0, rev_end, r3_end),
        "slowest_reviewer_s": slowest_reviewer_s(rev_start, rev_end),
    }
