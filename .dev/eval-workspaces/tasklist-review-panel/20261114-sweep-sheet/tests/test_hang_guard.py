"""REQ-30 (DESIGN 11.5): the hang guard is 1.5 x (b + expected overhead) from t0, per panel."""

from scaffold.clock import expected_overhead, hang_s, load_values

DOC = "TASK-WF-designSpec-20261107-075614"  # the document with the smallest b of every panel


def test_formula_per_panel():
    v = load_values()
    assert v["b"]["primary"][DOC] == 100
    assert v["b"]["haiku"][DOC] == 220
    assert v["b"]["sonnet"][DOC] == 259

    # SS carries the expected overhead of its panel: 29 s (ember), 37 s (haiku), 31 s (sonnet)
    assert [expected_overhead("SS", p) for p in ("primary", "haiku", "sonnet")] == [
        29,
        37,
        31,
    ]
    guard = {
        p: hang_s(v["b"][p][DOC], expected_overhead("SS", p))
        for p in ("primary", "haiku", "sonnet")
    }
    assert guard == {"primary": 193.5, "haiku": 385.5, "sonnet": 435.0}

    # every other arm adds nothing: Z0 at b = 100 is 150 s, on every panel
    for arm in ("Z0", "K", "Z0-raw"):
        assert expected_overhead(arm, "primary") == 0
        assert hang_s(100, expected_overhead(arm, "primary")) == 150.0
    assert hang_s(220, expected_overhead("Z0", "haiku")) == 330.0
