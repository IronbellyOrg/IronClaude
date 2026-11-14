from r3lib import digest


def test_deal_r0_r1():
    a = ["a0", "a1", "a2", "a3"]
    d0 = digest.deal(a, ["A", "B"], 0)
    assert d0 == {"A": ["a0", "a2"], "B": ["a1", "a3"]}
    d1 = digest.deal(a, ["A", "B"], 1)
    assert d1 == {"A": ["a1", "a3"], "B": ["a0", "a2"]}
    assert not set(d0["A"]) & set(d0["B"])


def test_interleave():
    assert digest.interleave([["A0", "A1", "A2"], ["B0", "B1"]]) == [
        "A0",
        "B0",
        "A1",
        "B1",
        "A2",
    ]
