"""py/values.py (R-41, R-42, D-2)."""
import datetime as dt
import hashlib
import json
import sys

import pytest
from conftest import PKGS, PY, R2

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


# ---- PANEL_SLACK_S (owner decision 2026-11-14: cap = 1.35 B + SLACK_S)

# Spike 4 EL2 on the control package: measured turn 12.519 s, report 15.563 s, B 102.8185 s
EL2_MEASURED = ("EL2", "p", 102.8185, 12.519, 15.563, 102.8185, 12.519, 15.563)


def test_slack_default_is_zero_and_values_unchanged():
    assert V.slack_s() == 0
    v = V.compute(*EL2_MEASURED)
    assert "slack_s" not in v and v["k"] == 0 and v["panel_finish_at_s"] == 110.723
    assert V.finish_at(100, 6.4, 6.4) == pytest.approx(1.35 * 100 - 12.8)


def test_slack_empty_env_is_zero(monkeypatch):
    monkeypatch.setenv("PANEL_SLACK_S", "")
    assert V.slack_s() == 0


def test_slack30_k_changes_for_a_measured_case_that_was_zero(monkeypatch):
    before = V.compute(*EL2_MEASURED)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    after = V.compute(*EL2_MEASURED)
    assert before["k"] == 0 and after["k"] == 1
    assert V.k_r42(102.8185, 12.519, 15.563) == 1  # literal R-42 form agrees


def test_slack30_finish_offset_plus_30_kill_plus_30_hang_unchanged(monkeypatch):
    before = V.compute(*EL2_MEASURED)
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    after = V.compute(*EL2_MEASURED)
    assert after["panel_finish_at_s"] == pytest.approx(before["panel_finish_at_s"] + 30, abs=1e-3)
    assert after["sweeper_kill_s"] == pytest.approx(before["sweeper_kill_s"] + 30, abs=1e-3)
    assert after["hang_s"] == before["hang_s"]  # 1.5 B is not derived from the 35% cap
    assert after["slack_s"] == 30


@pytest.mark.parametrize("B", [90, 100, 116, 150, 200])
@pytest.mark.parametrize("turn", [6.4, 14.0])
@pytest.mark.parametrize("rep", [1.0, 11.0, 20.0])
def test_slack30_d2_still_equals_r42(monkeypatch, B, turn, rep):
    monkeypatch.setenv("PANEL_SLACK_S", "30")
    assert V.k(V.finish_at(B, turn, rep), B, turn) == V.k_r42(B, turn, rep)


@pytest.mark.parametrize("bad", ["abc", "-1", "nan", "inf"])
def test_slack_bad_value_refused(monkeypatch, bad):
    monkeypatch.setenv("PANEL_SLACK_S", bad)
    with pytest.raises(ValueError, match="PANEL_SLACK_S"):
        V.slack_s()


@pytest.mark.parametrize("panel", ["EL2", "SL2", "HL2"])
@pytest.mark.parametrize("pkg", PKGS)
def test_frozen_slack30_values_match_pinned_ones_plus_30(panel, pkg):
    old = json.loads((R2 / f"config/values/{panel}/{pkg}.json").read_text())
    path = R2 / f"config/values-slack30/{panel}/{pkg}.json"
    new = json.loads(path.read_text())
    assert new["slack_s"] == 30 and new["source"] == "spike4"
    assert new["panel_finish_at_s"] == pytest.approx(old["panel_finish_at_s"] + 30, abs=1e-3)
    assert new["sweeper_kill_s"] == pytest.approx(old["sweeper_kill_s"] + 30, abs=1e-3)
    assert new["hang_s"] == old["hang_s"] and new["B_f"] == old["B_f"] and new["k"] >= old["k"]
    pins = json.loads((R2 / "config/manifest-slack30.json").read_text())["sha256"]
    assert pins[f"values-slack30/{panel}/{pkg}.json"] == hashlib.sha256(path.read_bytes()).hexdigest()
