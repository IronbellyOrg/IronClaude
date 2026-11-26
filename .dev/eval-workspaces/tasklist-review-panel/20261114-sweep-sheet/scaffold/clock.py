"""Time-budget arithmetic of DESIGN 11.4, 11.5 and 12 (REQ-29, REQ-30, REQ-31, REQ-18).

    kill_s(b)              pre-pass kill limit `min(15, 0.10 b)` (12.2)
    expected_overhead(..)  29 s (SS, ember panel), 37 s (haiku), 31 s (sonnet); 0 for every other arm (11.5)
    hang_s(b, overhead)    `1.5 * (b + overhead)` from t0 (11.5, INV-008)
    breakeven(b)           pre-pass seconds and seconds per item the +35% cap leaves, for n items (12.3)
    no_budget(b)           True when `0.35 b - 13` is under 8 s: an SS run is refused and recorded `no_budget` (12.3)
    PanelClock             the one clock per run and the `timing.json` fields of 11.4

Every constant comes from config/values.json (the keys `kill_s`, `hang_s`, `cap_factor`, `no_budget`, `breakeven`);
the functions accept a `values` dict so a test can pass its own. Results are rounded to 6 decimals so that
`0.10 * 122` is `12.2` and not `12.200000000000001`.

The break-even and the refusal rule use the planning pre-pass of 8 s (`breakeven.prepass_planning_s`, DESIGN 12.3:
"With the planning pre-pass S1 = 8 s this is n * c <= 0.35 b - 13"), not the measured `prepass_s`: the design states
the rule and its table (2.75 s and 3.71 s) on the planning value, and a faster measured pre-pass is reported next to
it, never over it.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

SW = Path(__file__).resolve().parents[1]
VALUES = SW / "config" / "values.json"
SS = "SS"
ND = 6


def load_values(path: Path = VALUES) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _v(values: dict | None) -> dict:
    return load_values() if values is None else values


def kill_s(b: float, values: dict | None = None) -> float:
    """Pre-pass kill limit: min(cap_s, frac_of_b * b). 10.0 at b = 100, 12.2 at 122, 15.0 at 200."""
    k = _v(values)["kill_s"]
    return round(min(k["cap_s"], k["frac_of_b"] * b), ND)


def expected_overhead(arm: str, panel: str, values: dict | None = None) -> float:
    """SS adds the expected non-reviewer seconds of its panel (S1 + render + sheet + items + S5); other arms add 0."""
    v = _v(values)
    table = v["hang_s"]["expected_overhead_s"]
    if arm in v["launcher"]["overhead_arms"]:
        return table[panel]
    return table[v["launcher"]["overhead_other"]]


def hang_s(b: float, overhead: float = 0, values: dict | None = None) -> float:
    """Hang guard from t0: factor * (b + overhead). 193.5 for the primary panel at b = 100 (SS), 150.0 for Z0."""
    return round(_v(values)["hang_s"]["factor"] * (b + overhead), ND)


def _slack(b: float, values: dict) -> float:
    """What the cap leaves above b: (cap_factor - 1) * b."""
    return round((values["cap_factor"] - 1) * b, ND)


class Breakeven(NamedTuple):
    prepass_s: float  # longest pre-pass that still fits, with c_ref per item
    per_item_s: float  # largest cost per item that fits, with the planning pre-pass


def breakeven(b: float, n: int | None = None, values: dict | None = None) -> Breakeven:
    """DESIGN 12.3. critical path = S1 + 1 + b + 3 + n*c + 1 and the cap is 1.35 b.

    per_item_s = (0.35 b - S1 - 5) / n with S1 = 8 (planning); prepass_s = 0.35 b - 5 - n * c_ref with c_ref = 2.
    n = 8: b = 100 gives 14.0 and 2.75; b = 122 gives 21.7 and 3.7125.
    """
    v = _v(values)
    be = v["breakeven"]
    n = be["n"] if n is None else n
    slack = _slack(b, v)
    return Breakeven(
        prepass_s=round(slack - be["fixed_s"] - n * be["c_ref"], ND),
        per_item_s=round((slack - be["prepass_planning_s"] - be["fixed_s"]) / n, ND),
    )


def budget_s(b: float, values: dict | None = None) -> float:
    """Seconds the cap leaves for the items: 0.35 b - 13 (DESIGN 12.3)."""
    v = _v(values)
    return round(
        _slack(b, v) - v["breakeven"]["prepass_planning_s"] - v["breakeven"]["fixed_s"],
        ND,
    )


def no_budget(b: float, values: dict | None = None) -> bool:
    """True when the budget is under min_budget_s (8): the harness refuses an SS start and records `no_budget`."""
    return budget_s(b, values) < _v(values)["no_budget"]["min_budget_s"]


SPIKE_RUNS = 5  # REQ-32: five luna runs with an SS brief
LUNA_FALLBACK_ITEMS = 6  # DESIGN 12.3: each luna's share when c is above the break-even


def spike_plan(values: dict | None = None) -> dict:
    """REQ-32: the spike record (`spike.runs` of at least 5 and a numeric `spike.c_luna`) and the fallback it sets.

    `ok` is False without such a record: no arm may start. `fallback` is True when c_luna is above the break-even seconds
    per item at b = 100 (2.75 s for n = 8): each luna then takes 6 items and the search reviewer the rest (`fallback_panels`).
    """
    v = _v(values)
    s = v.get("spike") or {}
    runs, c = s.get("runs"), s.get("c_luna")
    ok = (
        isinstance(runs, int)
        and not isinstance(runs, bool)
        and runs >= SPIKE_RUNS
        and isinstance(c, (int, float))
        and not isinstance(c, bool)
    )
    limit = breakeven(100, values=v).per_item_s
    return {
        "ok": ok,
        "runs": runs,
        "c_luna": c,
        "limit_s": limit,
        "fallback": bool(ok and c > limit),
        "luna_items": LUNA_FALLBACK_ITEMS,
    }


def fallback_panels(panels: dict) -> dict:
    """A copy of a panel file with the spike fallback: L1 and L2 (the lunas) capped at 6 items, S at the rest of the
    panel's total (12 when the caps sum to 24, as they do for every panel of config/panels.json)."""
    out = json.loads(json.dumps(panels))
    for p in out["panels"].values():
        total = sum(p[r]["cap"] for r in ("S", "L1", "L2"))
        p["L1"]["cap"] = p["L2"]["cap"] = LUNA_FALLBACK_ITEMS
        p["S"]["cap"] = total - 2 * LUNA_FALLBACK_ITEMS
    return out


class ClockError(RuntimeError):
    pass


def panel_elapsed_s(
    arm: str, t0: float, rev_end: dict[str, float], s5_end: float | None = None
) -> float:
    """SS: end of S5 minus t0. Any other arm: last reviewer end minus t0 (H2, merge, judge, verifier are outside)."""
    if arm == SS:
        if s5_end is None:
            raise ClockError("SS has no panel_elapsed_s before S5 ends")
        return round(s5_end - t0, ND)
    if not rev_end:
        raise ClockError(f"arm {arm}: no reviewer ended")
    return round(max(rev_end.values()) - t0, ND)


class PanelClock:
    """The one clock of a run (REQ-29). `now` is injectable so tests use a fake clock.

    start() takes t0 and must come first: before S1 (SS) or before the first brief render (other arms).
    stage(name) times the stages "prepass", "render" and "s5" (SS only; other arms leave them at 0).
    reviewer_start/reviewer_end time each reviewer process. timing() returns the fields of DESIGN 11.4.
    """

    STAGES = ("prepass", "render", "s5")

    def __init__(self, arm: str, now: Callable[[], float] = time.monotonic):
        self.arm = arm
        self.now = now
        self.t0: float | None = None
        self.stage_t: dict[str, list[float]] = {}
        self.rev_start: dict[str, float] = {}
        self.rev_end: dict[str, float] = {}

    def start(self) -> float:
        self.t0 = self.now()
        return self.t0

    def _need_t0(self) -> float:
        if self.t0 is None:
            raise ClockError("t0 not taken: call start() before S1 or the first render")
        return self.t0

    def stage_start(self, name: str) -> float:
        if name not in self.STAGES:
            raise ClockError(f"unknown stage {name}")
        self._need_t0()
        self.stage_t[name] = [self.now()]
        return self.stage_t[name][0]

    def stage_end(self, name: str) -> float:
        if name not in self.stage_t or len(self.stage_t[name]) != 1:
            raise ClockError(f"stage {name} not running")
        self.stage_t[name].append(self.now())
        return self.stage_t[name][1]

    def reviewer_start(self, rid: str) -> float:
        self._need_t0()
        self.rev_start[rid] = self.now()
        return self.rev_start[rid]

    def reviewer_end(self, rid: str) -> float:
        if rid not in self.rev_start:
            raise ClockError(f"reviewer {rid} never started")
        self.rev_end[rid] = self.now()
        return self.rev_end[rid]

    def _dur(self, name: str) -> float:
        t = self.stage_t.get(name)
        return round(t[1] - t[0], ND) if t and len(t) == 2 else 0.0

    def timing(self) -> dict:
        """timing.json: t0, prepass_s, render_s, rev_start, rev_end, s5_s, panel_elapsed_s, slowest_reviewer_s."""
        t0 = self._need_t0()
        s5 = self.stage_t.get("s5")
        s5_end = s5[1] if s5 and len(s5) == 2 else None
        done = {r: self.rev_end[r] - self.rev_start[r] for r in self.rev_end}
        return {
            "t0": t0,
            "prepass_s": self._dur("prepass"),
            "render_s": self._dur("render"),
            "rev_start": dict(self.rev_start),
            "rev_end": dict(self.rev_end),
            "s5_s": self._dur("s5"),
            "panel_elapsed_s": panel_elapsed_s(self.arm, t0, self.rev_end, s5_end),
            "slowest_reviewer_s": round(max(done.values()), ND) if done else None,
        }
