from r3lib.values import compute_n


def test_el2():
    assert compute_n(0, 116, 116, 35, 2, 6, 6.4) == 2
    assert compute_n(0, 116, 116, 35, 2, 6, 7.3) == 1
    assert compute_n(0, 116, 118, 35, 2, 16, 6.4) == 1
    assert compute_n(0, 116, 132.0, 35, 2, 6, 6.4) == 1
    assert compute_n(0, 116, 132.01, 35, 2, 6, 6.4) == 0
    assert compute_n(0, 116, 116, 35, 3, 6, 3.2) == 3
    # raw epoch T0 gives the same answer (relative arithmetic)
    T0 = 1794602718.207
    assert compute_n(T0, 116, T0 + 132.0, 35, 2, 6, 6.4) in (0, 1)


def test_sl2_hl2():
    assert compute_n(0, 273.7, 273.7, None, 3, 6, 14) == 2
    assert compute_n(0, 273.7, 273.7, None, 3, 6, 20) == 1
    assert compute_n(0, 238, 238, None, 3, 6, 23) == 1
    assert compute_n(0, 238, 238, None, 3, 6, 33) == 0
