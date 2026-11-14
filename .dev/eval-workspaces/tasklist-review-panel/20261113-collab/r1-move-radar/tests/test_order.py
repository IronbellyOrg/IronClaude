"""T-4: receiver order is a rotation by sha256(rid)[0:8] mod len."""

from conftest import TOOLS, run


def order(rid, role):
    r = run(["bash", str(TOOLS / "launch.sh"), "--order", rid, role])
    assert r.returncode == 0, r.stderr
    return r.stdout.strip().split(",")


def test_offsets():
    assert order("t4-1", "reader") == ["M3", "M5", "M6", "M9", "M8", "M10"]  # offset 0
    assert order("t3-1", "reader") == ["M8", "M10", "M3", "M5", "M6", "M9"]  # offset 4
    assert order("t2b-1", "searcher") == ["M2", "M7", "M4", "M1"]  # offset 1
    assert order("t1b-1", "searcher") == ["M7", "M4", "M1", "M2"]  # offset 2
    assert order("t2-1", "searcher") == ["M1", "M2", "M7", "M4"]  # offset 0


def test_lunas_differ_at_both_checkpoints():
    a, b = order("t4-1", "reader"), order("t3-1", "reader")
    assert a[0] != b[0] and a[1] != b[1]
