"""REQ-29 at the level of the clock module (DESIGN 9.3).

Task 13 completes two of the three tests at launcher level: `test_clock_starts_before_lens_render` (the launcher
takes t0 before it calls the lens render) and `test_reask_seconds_inside_the_clock` (the launcher stamps r3_end after
the ember re-ask). Here the arithmetic is pinned: what the module accepts and what `panel_elapsed_s` counts.
"""

import pytest

from scaffold import clock

START = {"r1": 1.0, "r2": 1.0, "r3": 1.0}
END = {"r1": 81.0, "r2": 126.0, "r3": 127.0}


def test_panel_elapsed_rl_and_other_arms():
    # RL: the end of R3 minus t0, whatever the reviewers did; the other arms: the last reviewer end minus t0
    assert clock.panel_elapsed_s("RL", 0.0, END, r3_end=128.0) == 128.0
    assert clock.panel_elapsed_s("RL", 10.0, END, r3_end=128.0) == 118.0
    for arm in ("Z0-raw", "Z0", "K"):
        assert clock.panel_elapsed_s(arm, 0.0, END) == 127.0
        assert clock.panel_elapsed_s(arm, 0.0, END, r3_end=500.0) == 127.0
    with pytest.raises(ValueError, match="r3_end"):
        clock.panel_elapsed_s("RL", 0.0, END)


def test_slowest_reviewer_is_end_minus_start():
    assert clock.slowest_reviewer_s(START, END) == 126.0


def test_clock_starts_before_lens_render():
    # RL: t0 = 0, the render takes 1 s, reviewers start at 1: the render is inside panel_elapsed_s
    rec = clock.timing_record(
        "RL", 0.0, START, END, render_s=1.0, check_s=1.0, r3_end=128.0
    )
    assert rec["panel_elapsed_s"] == 128.0
    assert (
        rec["panel_elapsed_s"] - rec["slowest_reviewer_s"] == 2.0
    )  # render 1 s + check 1 s
    # a clock that began after the render (t0 = 1, reviewers starting at 1 with render_s 1) is refused
    with pytest.raises(ValueError, match="before the lens render"):
        clock.timing_record("RL", 1.0, START, END, render_s=1.0, r3_end=128.0)
    # a reviewer may not start before t0
    with pytest.raises(ValueError, match="before t0"):
        clock.timing_record("Z0", 2.0, START, END)


def test_reask_seconds_inside_the_clock():
    # ember ends at 81 s and is re-asked for 25 s; luna ends at 127 s; check 1 s: the re-ask is off the critical path
    rec = clock.timing_record(
        "RL", 0.0, START, END, render_s=1.0, check_s=1.0, reask_s=25.0, r3_end=128.0
    )
    assert rec["reask_s"] == 25.0
    assert rec["check_s"] == 1.0  # check_s excludes the re-ask
    # ember last: it ends at 140 after its own re-ask, and panel_elapsed_s grows with the re-ask seconds
    late = dict(END, r1=140.0)
    slow = clock.timing_record(
        "RL", 0.0, START, late, render_s=1.0, check_s=1.0, reask_s=25.0, r3_end=167.0
    )
    assert slow["panel_elapsed_s"] == 167.0 > rec["panel_elapsed_s"]
    # r3_end before a reviewer ended is a stamp from the wrong clock
    with pytest.raises(ValueError, match="r3_end"):
        clock.timing_record("RL", 0.0, START, END, render_s=1.0, r3_end=100.0)


def test_other_arms_have_no_render_check_or_reask_seconds():
    rec = clock.timing_record("Z0", 0.0, START, END)
    assert (rec["render_s"], rec["check_s"], rec["reask_s"]) == (0, 0, 0)
    assert rec["panel_elapsed_s"] == 127.0
    for field in ("render_s", "check_s", "reask_s"):
        with pytest.raises(ValueError, match="no render"):
            clock.timing_record("K", 0.0, START, END, **{field: 1.0})
