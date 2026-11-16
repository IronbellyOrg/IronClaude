"""REQ-29 (DESIGN 11.4), REQ-31 and DESIGN 12.3: the panel clock, the break-even and the no_budget refusal."""

import pytest

from scaffold.clock import (
    ClockError,
    PanelClock,
    breakeven,
    budget_s,
    no_budget,
    panel_elapsed_s,
)


class FakeClock:
    """A clock the test moves by hand: fc.t = 1008 sets the time the next clock call returns."""

    def __init__(self, t=1000.0):
        self.t = t

    def __call__(self):
        return self.t


def run_ss(fc):
    """t0=1000; S1 1000-1008; render 1008-1009; reviewers start 1009; ember ends 1070, luna 1130 and 1135; S5 1135-1136."""
    c = PanelClock("SS", fc)
    c.start()
    c.stage_start("prepass")
    fc.t = 1008
    c.stage_end("prepass")
    c.stage_start("render")
    fc.t = 1009
    c.stage_end("render")
    for rid in ("t2b-1", "t4-1", "t3-1"):
        c.reviewer_start(rid)
    for rid, t in (("t2b-1", 1070), ("t4-1", 1130), ("t3-1", 1135)):
        fc.t = t
        c.reviewer_end(rid)
    c.stage_start("s5")
    fc.t = 1136
    c.stage_end("s5")
    return c


def test_panel_elapsed_ss_and_other_arms():
    fc = FakeClock()
    tm = run_ss(fc).timing()
    # SS: end of S5 minus t0 (the H2, merge, judge and verifier come after and are not on the clock)
    assert tm["panel_elapsed_s"] == 136.0
    assert (tm["prepass_s"], tm["render_s"], tm["s5_s"]) == (8.0, 1.0, 1.0)
    assert tm["slowest_reviewer_s"] == 126.0  # t3-1: 1135 - 1009

    # other arms: last reviewer end minus t0; the stages stay 0
    for arm in ("Z0", "K", "Z0-raw"):
        fc = FakeClock()
        c = PanelClock(arm, fc)
        c.start()
        fc.t = 1002
        for rid in ("a", "b"):
            c.reviewer_start(rid)
        fc.t = 1100
        c.reviewer_end("a")
        fc.t = 1120
        c.reviewer_end("b")
        fc.t = 5000  # H2, merge and judge run later and must not move the clock
        tm = c.timing()
        assert tm["panel_elapsed_s"] == 120.0, arm
        assert (tm["prepass_s"], tm["render_s"], tm["s5_s"]) == (0.0, 0.0, 0.0)
        assert tm["slowest_reviewer_s"] == 118.0

    # pure form of the same arithmetic
    assert panel_elapsed_s("SS", 10.0, {"a": 50.0}, s5_end=70.0) == 60.0
    assert panel_elapsed_s("Z0", 10.0, {"a": 50.0, "b": 40.0}) == 40.0
    with pytest.raises(ClockError):
        panel_elapsed_s("SS", 10.0, {"a": 50.0})


def test_clock_starts_before_prepass():
    fc = FakeClock()
    c = PanelClock("SS", fc)
    with pytest.raises(ClockError):  # S1 or a reviewer cannot start before t0
        c.stage_start("prepass")
    with pytest.raises(ClockError):
        c.reviewer_start("t4-1")
    t0 = c.start()
    fc.t = 1003
    s1 = c.stage_start("prepass")
    assert t0 < s1
    fc.t = 1011
    c.stage_end("prepass")
    c.stage_start("s5")
    c.stage_end("s5")
    tm = c.timing()
    # the pre-pass and the 3 s before it are inside the panel clock
    assert tm["t0"] == 1000.0 and tm["prepass_s"] == 8.0
    assert tm["panel_elapsed_s"] == 11.0


def test_breakeven_b100_and_b122():
    be = breakeven(b=100)
    assert be.prepass_s == 14.0 and be.per_item_s == 2.75
    be = breakeven(b=122)
    assert be.prepass_s == pytest.approx(21.7, abs=0.05)
    assert be.per_item_s == pytest.approx(3.71, abs=0.005)
    # n = 6 (the MR fallback): c <= 3.67 at b = 100 and 4.95 at b = 122
    assert breakeven(100, n=6).per_item_s == pytest.approx(3.67, abs=0.005)
    assert breakeven(122, n=6).per_item_s == pytest.approx(4.95, abs=0.005)


def test_no_budget_refuses_below_eight_seconds():
    assert budget_s(100) == 22.0 and budget_s(122) == pytest.approx(29.7)
    assert not no_budget(100)
    assert not no_budget(60)  # 0.35 * 60 - 13 = 8.0: exactly 8 s is allowed
    assert no_budget(59)
    assert budget_s(37) <= 0  # no budget at all at b <= 37
    assert no_budget(37)
