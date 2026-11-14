"""T-12 and T-13: timing formulas and the Spike 4 values writer (R-30, R-41, R-42, R-45)."""
import hashlib
import json
from datetime import datetime, timedelta, timezone

import pytest
from conftest import CT
from r5 import timing


@pytest.mark.parametrize("B,turn,rep,k", [
    (116, 6.4, 6.4, 2), (116, 6.4, 11.0, 1), (100, 6.4, 13.8, 1), (100, 6.4, 13.9, 0),
    (273.7, 14, 23.79, 2), (273.7, 14, 23.80, 1), (273.7, 14, 51.79, 1), (273.7, 14, 51.80, 0),
    (238, 23, 12.3, 1), (238, 23, 12.4, 0),
])
def test_k(B, turn, rep, k):
    assert timing.k(B, turn, rep) == k


def test_offsets_and_limits():
    assert timing.finish_offset(116, 6.4, 6.4) == pytest.approx(143.8)
    assert timing.hang_offset(273.7) == pytest.approx(410.55)
    assert timing.slowdown_limit(273.7, 2, 14) == pytest.approx(0.1381, abs=5e-5)
    assert timing.slowdown_limit(116, 2, 6.4) == pytest.approx(0.1121, abs=5e-5)


def session(path, gaps):
    """gaps: list of (user->assistant seconds); returns the expected turn list."""
    t = datetime(2026, 11, 13, tzinfo=timezone.utc)
    lines = []
    for g in gaps:
        lines.append({"type": "user", "timestamp": t.isoformat().replace("+00:00", "Z")})
        t += timedelta(seconds=g)
        lines.append({"type": "assistant", "timestamp": t.isoformat().replace("+00:00", "Z"), "message": {"id": "m"}})
        t += timedelta(seconds=0.5)
    lines.append({"type": "assistant", "isSidechain": True, "timestamp": t.isoformat().replace("+00:00", "Z")})
    path.write_text("".join(json.dumps(x) + "\n" for x in lines))


def test_turns_parse(tmp_path):
    p = tmp_path / "s.jsonl"
    session(p, [2, 3, 10])
    assert timing.turns(p) == pytest.approx([2, 3, 10])


def test_spike4_writes_values_once(env):  # T-13
    rows = []
    for i, (el, gaps) in enumerate([(100, [2, 3, 10]), (110, [4, 5, 12]), (120, [1, 1, 8]), (130, [2, 2, 9])]):
        row = f"s4-a1-sl2-r{i + 1}"
        rows.append(row)
        d = env["out"] / "runs" / row / CT
        (d / "reviews").mkdir(parents=True)
        (d / "collab.json").write_text(json.dumps({"elapsed_s": el}))
        session(d / "reviews" / "t1b-1.attempt1.session.jsonl", gaps)
        (d / "reviews" / "t1b-1.cost.json").write_text(json.dumps({"total_wall_s": el}))
    kd = env["out"] / "runs" / "s4-a2-sl2-r1" / CT / "reviews"
    kd.mkdir(parents=True)
    (kd / "t1b-1.cost.json").write_text(json.dumps({"total_wall_s": 121}))
    assert timing.main(["spike4", "--panel", "sl2", "--rows", ",".join(rows), "--kit-rows", "s4-a2-sl2-r1"]) == 0
    v = json.loads((env["cfg"] / "values" / "sl2" / f"{CT}.json").read_text())
    assert v["B_f_s"] == 115 and v["turn_p90_s"] == pytest.approx(10) and v["T_report_p90_s"] == pytest.approx(12)
    assert v["k"] == timing.k(115, 10, 12)
    assert v["slowdown_s"] == pytest.approx(121 / 115 - 1)
    sums = (env["cfg"] / "values" / "sl2" / "SHA256SUMS").read_text()
    assert hashlib.sha256((env["cfg"] / "values" / "sl2" / f"{CT}.json").read_bytes()).hexdigest() in sums
    assert timing.main(["spike4", "--panel", "sl2", "--rows", ",".join(rows)]) == 1
