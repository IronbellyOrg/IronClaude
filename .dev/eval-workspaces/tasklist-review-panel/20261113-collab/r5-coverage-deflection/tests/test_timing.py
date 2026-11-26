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


def test_slack_default_is_zero(monkeypatch):  # PANEL_SLACK_S unset or empty: the pinned numbers above stand
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    assert timing.slack_s() == 0 and timing.values_dirname() == "values"
    monkeypatch.setenv("PANEL_SLACK_S", "")
    assert timing.slack_s() == 0 and timing.k(100, 14, 14) == 0 and timing.finish_offset(100, 14, 14) == pytest.approx(107)


@pytest.mark.parametrize("bad", ["30.5", "-1", "abc", "030", " 30"])
def test_slack_rejects_bad_values(monkeypatch, bad):
    monkeypatch.setenv("PANEL_SLACK_S", bad)
    with pytest.raises(ValueError, match="PANEL_SLACK_S"):
        timing.slack_s()


@pytest.mark.parametrize("B,turn,rep,k0,k30", [
    (100, 14, 14, 0, 1),        # 35 - 2 - 28 = 5 s of room -> 35 s with slack: one card fits
    (273.7, 14, 51.80, 0, 2),   # sl2-like: 95.8 - 2 - 65.8 = 28 s -> 58 s: two cards fit
    (238, 23, 12.4, 0, 1),      # hl2 alias with planning turns: just short without slack
    (116.782, 40.382, 57.42, 0, 0),  # el2 design: 40.9 - 99.8 < 0 and 70.9 - 99.8 < 0: slack does not help
])
def test_slack30_k(monkeypatch, B, turn, rep, k0, k30):
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    assert timing.k(B, turn, rep) == k0
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert timing.k(B, turn, rep) == k30


def test_slack30_offsets_and_limits(monkeypatch):
    monkeypatch.delenv("PANEL_SLACK_S", raising=False)
    f0, h0, s0 = timing.finish_offset(116, 6.4, 6.4), timing.hang_offset(116), timing.slowdown_limit(116, 2, 6.4)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert timing.values_dirname() == "values-slack30"
    assert timing.finish_offset(116, 6.4, 6.4) == pytest.approx(f0 + 30)
    assert timing.hang_offset(116) == h0  # the hang guard is not derived from the 35% cap
    assert timing.slowdown_limit(116, 2, 6.4) == pytest.approx(s0 + 30 / 116)


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


def make_rows(env):
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
    return rows


def test_spike4_writes_values_once(env):  # T-13
    rows = make_rows(env)
    assert timing.main(["spike4", "--panel", "sl2", "--rows", ",".join(rows), "--kit-rows", "s4-a2-sl2-r1"]) == 0
    v = json.loads((env["cfg"] / "values" / "sl2" / f"{CT}.json").read_text())
    assert v["B_f_s"] == 115 and v["turn_p90_s"] == pytest.approx(10) and v["T_report_p90_s"] == pytest.approx(12)
    assert v["k"] == timing.k(115, 10, 12)
    assert v["slowdown_s"] == pytest.approx(121 / 115 - 1)
    sums = (env["cfg"] / "values" / "sl2" / "SHA256SUMS").read_text()
    assert hashlib.sha256((env["cfg"] / "values" / "sl2" / f"{CT}.json").read_bytes()).hexdigest() in sums
    assert timing.main(["spike4", "--panel", "sl2", "--rows", ",".join(rows)]) == 1


def test_spike4_slack30_writes_new_folder_only(env, monkeypatch):
    rows = make_rows(env)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert timing.main(["spike4", "--panel", "sl2", "--rows", ",".join(rows), "--kit-rows", "s4-a2-sl2-r1"]) == 0
    assert not (env["cfg"] / "values").exists()  # the normal values folder is untouched
    vd = env["cfg"] / "values-slack30" / "sl2"
    v = json.loads((vd / f"{CT}.json").read_text())
    assert v["slack_s"] == 30 and v["B_f_s"] == 115 and v["k"] == 2 and timing.k(115, 10, 12) == 2
    assert v["finish_offset_s"] == pytest.approx(1.35 * 115 + 30 - 10 - 12) and v["hang_offset_s"] == pytest.approx(1.5 * 115)
    assert v["slowdown_limit"] == pytest.approx((0.35 * 115 + 30 - (2 + 2 * 2 * 10)) / 115)
    assert hashlib.sha256((vd / f"{CT}.json").read_bytes()).hexdigest() in (vd / "SHA256SUMS").read_text()
    monkeypatch.delenv("PANEL_SLACK_S")
    assert timing.k(115, 10, 12) == 0  # same rows, no slack: k = 0
