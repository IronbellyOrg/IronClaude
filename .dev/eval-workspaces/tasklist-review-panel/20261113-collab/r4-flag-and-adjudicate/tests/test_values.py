"""lib/values.py (design 2.7; R-42 verification set and the section 3 rows)."""

import json
import os

import pytest
from r4help import PKGS, R4, REPO, run

import values


@pytest.mark.parametrize("args,k", [((116, 6.4, 6.4), 2), ((116, 6.4, 11.0), 1), ((100, 6.4, 13.8), 1), ((100, 6.4, 13.9), 0),
                                    ((273.7, 14, 51.795), 1), ((273.7, 14, 51.8), 0), ((238, 23, 23), 0), ((238, 20.3, 20.3), 1)])
def test_k_of(args, k):
    assert values.k_of(*args) == k


def test_offsets():
    assert values.finish_offset(116, 6.4, 6.4) == pytest.approx(143.8)
    assert values.hang_s(116) == pytest.approx(174.0)


def tr_entries(path, base=1_700_000_000.0):
    def ts(s):
        import datetime
        return datetime.datetime.fromtimestamp(base + s, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    rows = [
        {"type": "user", "timestamp": ts(0)},
        {"type": "assistant", "message": {"id": "m1"}, "timestamp": ts(3)},                       # turn 1: 3 s
        {"type": "user", "timestamp": ts(4)},
        {"type": "assistant", "message": {"id": "sc"}, "timestamp": ts(50), "isSidechain": True},  # ignored
        {"type": "assistant", "message": {"id": "m2"}, "timestamp": ts(9)},                       # turn 2: 5 s
        {"type": "user", "timestamp": ts(10)},
        {"type": "assistant", "message": {"id": "m3"}, "timestamp": ts(12)},                      # final: thinking
        {"type": "assistant", "message": {"id": "m3"}, "timestamp": ts(30)},                      # final: long text -> 20 s
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def test_turn_parsing(tmp_path):
    p = tmp_path / "t.jsonl"
    tr_entries(p)
    assert values.turns(str(p)) == pytest.approx([3.0, 5.0, 20.0])


def test_p90():
    assert values.p90([4, 1, 3, 2]) == 4          # ceil(3.6) = 4th
    assert values.p90(list(range(1, 11))) == 9    # ceil(9) = 9th


def fake_row(root, name, el, cp_rids, t0=1_000_000):
    for i, p in enumerate(PKGS):
        d = root / name / p
        (d / "reviews").mkdir(parents=True)
        (d / "panel.json").write_text(json.dumps({"t0_ms": t0, "reviewers": [{"rid": r} for r in ("t2b-1", "t4-1", "t3-1")]}))
        for r in ("t2b-1", "t4-1", "t3-1"):
            end = t0 + int(el * 1000) - (0 if r in cp_rids else 5000)
            (d / "reviews" / f"{r}.meta.json").write_text(json.dumps({"t_end_ms": end}))
            tr_entries(d / "reviews" / f"{r}.transcript.jsonl")
    return str(root / name)


def test_clis(tmp_path):
    env = dict(os.environ, R4_OUT=str(tmp_path / "out"))
    py = ["uv", "run", "--frozen", "--project", str(REPO), "python", str(R4 / "lib" / "values.py")]
    a1 = [fake_row(tmp_path, f"a{i}", 100 + i, ("t4-1", "t3-1")) for i in range(4)]
    sr = [fake_row(tmp_path, f"s{i}", 110 + i, ("t4-1", "t3-1")) for i in range(2)]
    for cmd in (["planning", "--panel", "EL2"], ["build", "--panel", "EL2", "--runs", *a1], ["srun", "--panel", "EL2"],
                ["slowdown", "--panel", "EL2", "--a1", *a1, "--srun", *sr]):
        r = run(py + cmd, env=env)
        assert r.returncode == 0, r.stderr
        path = r.stdout.strip()
        h = open(path + ".sha256").read().split()[0]
        assert h == __import__("hashlib").sha256(open(path, "rb").read()).hexdigest()
    v = json.load(open(tmp_path / "out/values/EL2.json"))["packages"][PKGS[0]]
    assert v["B_A1"] == pytest.approx(101.5) and v["turn_p90"] == 20.0 and v["T_report_p90"] == 20.0 and v["n_runs"] == 4
    s = json.load(open(tmp_path / "out/values/EL2-srun.json"))
    assert all(x["deliver"] is False for x in s["packages"].values())
    sd = json.load(open(tmp_path / "out/values/EL2-slowdown.json"))["packages"][PKGS[0]]
    assert sd["s"] == pytest.approx(110.5 / 101.5 - 1, abs=1e-4)
    pl = json.load(open(tmp_path / "out/values/planning-EL2.json"))["packages"][PKGS[0]]
    assert pl["planning"] is True and pl["k"] == 2 and pl["hang_s"] == 174.0


def test_slowdown_limits():
    assert values.slowdown_limit(116, 6.4, 2) == pytest.approx(0.057, abs=5e-4)
    assert values.slowdown_limit(116, 6.4, 1) == pytest.approx(0.167, abs=5e-4)
    assert values.slowdown_limit(273.7, 14, 2) == pytest.approx(0.087, abs=5e-4)
    assert values.slowdown_limit(273.7, 14, 1) == pytest.approx(0.189, abs=5e-4)
    assert values.slowdown_limit(238, 23, 1) == pytest.approx(0.052, abs=5e-4)
    assert values.slowdown_limit(238, 23, 0) is None
