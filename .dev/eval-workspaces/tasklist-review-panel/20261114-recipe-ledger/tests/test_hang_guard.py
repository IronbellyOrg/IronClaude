"""REQ-30: the hang guard is 1.5 x (b + expected overhead) from t0 (DESIGN 9.4). The bin side (the `timeout` and the
`killed` field) is tested in test_run_reviewer.py; the launcher side comes with Task 13."""

import pytest
from helpers import SW

from rl import lens
from scaffold import clock

# DESIGN 9.4 table, written out by hand: (arm, panel, b) -> hang_s
TABLE = [
    ("RL", "primary", 100, 192),
    ("RL", "primary", 120, 222),
    ("RL", "primary", 122, 225),
    ("Z0", "primary", 100, 150),
    ("Z0", "primary", 120, 180),
    ("Z0", "primary", 122, 183),
    ("RL", "haiku", 220, 375),
    ("RL", "haiku", 238, 402),
    ("RL", "sonnet", 259, 433.5),
    ("RL", "sonnet", 302, 498),
]


@pytest.mark.parametrize(("arm", "panel", "b", "expected"), TABLE)
def test_formula_per_panel(arm, panel, b, expected):
    assert clock.hang_s(b, arm, panel) == expected


def test_table_b_values_are_the_planning_values():
    b = lens.values(SW / "config" / "values.json")["b"]
    for _arm, panel, value, _ in TABLE:
        assert value in b[panel].values(), (panel, value)


def test_overhead_is_28_30_30_for_rl_and_zero_for_the_other_arms():
    assert [
        clock.expected_overhead("RL", p) for p in ("primary", "haiku", "sonnet")
    ] == [28, 30, 30]
    for arm in ("Z0-raw", "Z0", "K"):
        assert clock.expected_overhead(arm, "primary") == 0
        assert clock.hang_s(100, arm, "primary") == 150


def test_unknown_arm_is_refused():
    with pytest.raises(ValueError, match="unknown arm"):
        clock.hang_s(100, "RLx", "primary")
