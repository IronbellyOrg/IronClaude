import json
import pathlib
import sys

AB = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AB))
import ledger_lite as L  # noqa: E402
import shadow as SH  # noqa: E402
import test_ab3 as T  # noqa: E402

REVIEW = SH.REVIEW


def fake_est(cap, open_blocking=0):
    n = len([d for d in cap["defects"] if d["blocking"]])
    return {"S_obs": n, "Q": {"1": n, "2": 0}, "chao2": {"N": n + 1, "ci95": [n, n + 2.5]}, "jackknife1": {"N": n + 1, "ci95": [n, n + 2]},
            "unseen_upper95": 2.5}


def mkrun(root, i, audited=True):
    d = root / "runs" / f"b1-r{i}"
    rv = d / "ws" / REVIEW
    rv.mkdir(parents=True)
    spec = T.ORIG.read_text()
    lg = L.Ledger(cap=3)
    f = T.finding("F1", T.ANCH1)
    lg.add_round(1, spec, [{"reviewer_id": "t1b-1", "model": "claude-sonnet-5-5", "text": T.fblock(f)},
                           {"reviewer_id": "t3-1", "model": "claude-haiku-5-5", "text": T.fblock(f)},
                           {"reviewer_id": "t3-2", "model": "claude-haiku-5-5", "text": T.fblock()}])
    lg.save(rv / "ledger.json")
    for s in ("aud", "aud2"):
        a = d / s / "ws" / REVIEW
        a.mkdir(parents=True)
        (a / "audit.md").write_text("Blocking finding ids: none.\n\nverdict: PASS\n")
    (d / "state.json").write_text(json.dumps({"done": ["R1", "AUD", "AUD2"] if audited else ["R1"]}))


def test_shadow_not_run_below_five(tmp_path):
    for i in range(1, 4):
        mkrun(tmp_path, i)
    out = tmp_path / "s.md"
    assert SH.main(ab1=tmp_path, out=out, est=fake_est) is None
    assert "Not run" in out.read_text()


def test_shadow_calibrated_with_five(tmp_path):
    for i in range(1, 6):
        mkrun(tmp_path, i)
    mkrun(tmp_path, 6, audited=False)
    out = tmp_path / "s.md"
    assert SH.main(ab1=tmp_path, out=out, est=fake_est) == "CALIBRATED"
    t = out.read_text()
    assert "5/5" in t and "haiku only" in t
    res = json.loads((AB / "shadow.json").read_text())
    assert res["n"] == 5 and res["runs"][0]["haiku_union"] == 1 and res["runs"][0]["sonnet_union"] == 1
    (AB / "shadow.json").write_text(json.dumps({"ran": False, "completed": 0}))
    (AB / "shadow.md").write_text("# Shadow calibration (F3)\n\nNot run: 0 completed PN1 runs found (need at least 5 with both audits ingested).\n")
