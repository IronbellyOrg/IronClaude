"""py/values.py (R-41, R-42, D-2)."""
import datetime as dt
import json
import sys

import pytest
from conftest import PY

sys.path.insert(0, str(PY))
import values as V  # noqa: E402


def test_r42_planning_k2():
    assert V.k_r42(116, 6.4, 6.4) == 2


def test_r42_report_11_k1():
    assert V.k_r42(116, 6.4, 11.0) == 1


def test_r42_b100_threshold():
    assert V.k_r42(100, 6.4, 13.8) == 1 and V.k_r42(100, 6.4, 13.9) == 0
    assert V.k_r42(100, 6.4, 1.0) == 2 and V.k_r42(100, 6.4, 1.1) == 1


def test_r42_sl2_threshold():
    # MR's table rounds the threshold to 51.8 s; the exact value is 0.35*273.7 - 2 - 14 - 28 = 51.795 s
    assert V.k_r42(273.7, 14, 51.79) >= 1 and V.k_r42(273.7, 14, 51.8) == 0


@pytest.mark.parametrize("B", [90, 100, 116, 120, 122, 150, 200])
@pytest.mark.parametrize("turn", [3.2, 6.4, 8.0, 14.0])
@pytest.mark.parametrize("rep", [1.0, 6.4, 8.0, 11.0, 13.8, 20.0])
def test_d2_equals_r42_when_receiver_is_critical(B, turn, rep):
    f = V.finish_at(B, turn, rep)
    assert V.k(f, B, turn) == V.k_r42(B, turn, rep)


def test_hl2_planning_k2():
    assert V.compute("HL2", "p", 238, 23, 23, 102, 6.4, 6.4)["k"] == 2


def test_el2_planning_values():
    v = V.compute("EL2", "p", 116, 6.4, 6.4, 116, 6.4, 6.4)
    assert v["panel_finish_at_s"] == 143.8 and v["sweeper_kill_s"] == 131.0 and v["hang_s"] == 174.0 and v["k"] == 2


def test_k_bounds():
    assert V.k(10, 500, 6.4) == 0 and V.k(10_000, 0, 6.4) == 2


def test_reducer_turn_durations(tmp_path):
    t0 = dt.datetime(2026, 1, 1, tzinfo=dt.timezone.utc)
    lines = []
    for s in (0, 5, 12, 30):
        lines.append({"type": "assistant", "timestamp": (t0 + dt.timedelta(seconds=s)).isoformat().replace("+00:00", "Z")})
        lines.append({"type": "user", "timestamp": (t0 + dt.timedelta(seconds=s + 1)).isoformat()})
    p = tmp_path / "s.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in lines))
    assert V.turn_durations(p) == [5.0, 7.0, 18.0]
    assert V.p90([5.0, 7.0, 18.0]) == 18.0
